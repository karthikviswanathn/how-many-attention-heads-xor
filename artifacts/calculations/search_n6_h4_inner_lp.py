#!/usr/bin/env python3
"""Optimize six-bit four-head denominators through an exact inner LP.

For each denominator tuple, a linear program globally optimizes all affine
numerators and the intercept. The LP dual gives a subgradient with respect to
the denominator logits. Every reported success is rounded to integer
denominators and verified exactly. A failure is only search evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize

import search_gated_single_flip as exact


N = 6
HEADS = 4
WIDTH = N + 1
VERTICES = 1 << N


def cube() -> np.ndarray:
    return ((np.arange(VERTICES)[:, None] >> np.arange(N)) & 1).astype(float)


AFFINE = np.column_stack([np.ones(VERTICES), cube()])


def signs_from_mask(mask: int) -> np.ndarray:
    return np.array(
        [1 if (mask >> code) & 1 else -1 for code in range(VERTICES)],
        dtype=float,
    )


def literal_matrix(orientation: int) -> np.ndarray:
    inputs = cube()
    literals = inputs if orientation > 0 else 1.0 - inputs
    return np.column_stack([np.ones(VERTICES), literals])


def softmax(logits: np.ndarray) -> np.ndarray:
    centered = logits - np.max(logits, axis=1, keepdims=True)
    exponentials = np.exp(np.maximum(centered, -700.0))
    raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
    # Keep the inner LP numerically scaled while still allowing denominator
    # weight ratios of order one million.
    epsilon = 1e-6
    return (1.0 - WIDTH * epsilon) * raw + epsilon


def inner_lp(
    logits_flat: np.ndarray,
    signs: np.ndarray,
    orientations: tuple[int, ...],
    regularization: float,
    anchor_index: int,
    anchor_value: int,
) -> tuple[float, np.ndarray, dict[str, object]]:
    logits = logits_flat.reshape(HEADS, WIDTH)
    theta = softmax(logits)
    literals = [literal_matrix(orientation) for orientation in orientations]
    denominator_values = np.column_stack(
        [literals[head] @ theta[head] for head in range(HEADS)]
    )
    # Quotient the four exact redundancies N_h -> N_h + k B_h by fixing every
    # numerator intercept to zero and absorbing the resulting constants into
    # the one global intercept.
    features = np.column_stack(
        [np.ones(VERTICES)]
        + [
            AFFINE[:, 1:] / denominator_values[:, head, None]
            for head in range(HEADS)
        ]
    )
    coefficient_count = features.shape[1]
    constraints = np.zeros((VERTICES, coefficient_count + 1))
    constraints[:, :coefficient_count] = -(signs[:, None] * features)
    constraints[:, -1] = 1.0
    objective = np.zeros(coefficient_count + 1)
    objective[-1] = -1.0
    coefficient_bounds = [(-1.0, 1.0)] * coefficient_count
    coefficient_bounds[anchor_index] = (float(anchor_value), float(anchor_value))
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(VERTICES),
        bounds=coefficient_bounds + [(None, None)],
        method="highs-ds",
    )
    if not result.success:
        result = linprog(
            objective,
            A_ub=constraints,
            b_ub=np.zeros(VERTICES),
            bounds=coefficient_bounds + [(None, None)],
            method="highs-ipm",
        )
    if not result.success:
        raise RuntimeError(f"inner numerator LP failed: {result.message}")

    coefficients = result.x[:coefficient_count]
    dual_marginals = np.array(result.ineqlin.marginals, dtype=float)
    theta_gradient = np.zeros_like(theta)
    for head in range(HEADS):
        start = 1 + head * N
        numerator = AFFINE[:, 1:] @ coefficients[start : start + N]
        value_gradient = (
            dual_marginals
            * signs
            * (-numerator / denominator_values[:, head] ** 2)
        )
        theta_gradient[head] = literals[head].T @ value_gradient
    logit_gradient = theta * (
        theta_gradient
        - np.sum(theta * theta_gradient, axis=1, keepdims=True)
    )

    centered_logits = logits - np.mean(logits, axis=1, keepdims=True)
    loss = float(result.fun) + 0.5 * regularization * float(
        np.sum(centered_logits * centered_logits)
    )
    logit_gradient += regularization * centered_logits
    diagnostics = {
        "margin": float(result.x[-1]),
        "theta": theta,
        "coefficients": coefficients,
        "active_dual_rows": int(np.sum(dual_marginals < -1e-10)),
        "anchor_index": anchor_index,
        "anchor_value": anchor_value,
    }
    return loss, logit_gradient.ravel(), diagnostics


def finite_difference_check(
    signs: np.ndarray, orientations: tuple[int, ...], seed: int
) -> float:
    rng = np.random.default_rng(seed)
    logits = rng.normal(scale=1.0, size=HEADS * WIDTH)
    loss, gradient, _ = inner_lp(logits, signs, orientations, 0.0, 3, 1)
    direction = rng.normal(size=len(logits))
    direction /= np.linalg.norm(direction)
    epsilon = 1e-5
    plus = inner_lp(
        logits + epsilon * direction, signs, orientations, 0.0, 3, 1
    )[0]
    minus = inner_lp(
        logits - epsilon * direction, signs, orientations, 0.0, 3, 1
    )[0]
    finite_difference = (plus - minus) / (2.0 * epsilon)
    analytic = float(gradient @ direction)
    return abs(finite_difference - analytic) / max(
        1.0, abs(finite_difference), abs(analytic), abs(loss)
    )


def search_orientation(
    signs: np.ndarray,
    positive_heads: int,
    seed: int,
    restarts: int,
    max_iterations: int,
    scales: tuple[int, ...],
) -> tuple[dict[str, object] | None, dict[str, object]]:
    orientations = tuple([-1] * (HEADS - positive_heads) + [1] * positive_heads)
    rng = np.random.default_rng(seed)
    best_margin = float("-inf")
    best: dict[str, object] = {}

    for restart in range(restarts):
        anchor_index = (restart // 2) % (1 + HEADS * N)
        anchor_value = 1 if restart % 2 == 0 else -1
        logit_scale = float(rng.choice((0.5, 1.5, 3.0, 6.0, 10.0)))
        initial = rng.normal(scale=logit_scale, size=(HEADS, WIDTH))
        regularization = 10 ** rng.uniform(-11.0, -6.0)
        latest: dict[str, object] = {}

        def objective(current: np.ndarray) -> tuple[float, np.ndarray]:
            loss, gradient, diagnostics = inner_lp(
                current,
                signs,
                orientations,
                regularization,
                anchor_index,
                anchor_value,
            )
            latest.clear()
            latest.update(diagnostics)
            return loss, gradient

        result = minimize(
            objective,
            initial.ravel(),
            jac=True,
            method="L-BFGS-B",
            bounds=[(-15.0, 15.0)] * (HEADS * WIDTH),
            options={
                "maxiter": max_iterations,
                "maxfun": 8 * max_iterations,
                "ftol": 1e-13,
                "gtol": 1e-8,
                "maxls": 30,
            },
        )
        _, _, diagnostics = inner_lp(
            result.x,
            signs,
            orientations,
            regularization,
            anchor_index,
            anchor_value,
        )
        margin = float(diagnostics["margin"])
        theta = np.array(diagnostics["theta"], dtype=float)
        if margin > best_margin:
            best_margin = margin
            best = {
                "positive_heads": positive_heads,
                "restart": restart,
                "continuous_inner_lp_margin": margin,
                "active_dual_rows": diagnostics["active_dual_rows"],
                "anchor_index": anchor_index,
                "anchor_value": anchor_value,
                "optimizer_success": bool(result.success),
                "optimizer_message": str(result.message),
                "literal_weights": theta.tolist(),
            }
            print(
                f"positive_heads={positive_heads} restart={restart} "
                f"inner_lp_margin={margin}",
                flush=True,
            )

        for scale in scales:
            denominators = np.vstack(
                [
                    exact.oriented_integer_denominator(
                        np.maximum(1, np.rint(scale * theta[head])),
                        orientations[head],
                    )
                    for head in range(HEADS)
                ]
            )
            certificate = exact.exact_fixed_certificate(
                signs.astype(np.int64), N, denominators
            )
            if certificate is not None:
                certificate["positive_heads"] = positive_heads
                certificate["restart"] = restart
                certificate["rounding_scale"] = scale
                certificate["continuous_inner_lp_margin"] = margin
                return certificate, best
    return None, best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--max-iterations", type=int, default=180)
    parser.add_argument("--seed", type=int, default=202607142)
    parser.add_argument(
        "--scales",
        type=int,
        nargs="+",
        default=(30, 100, 300, 1000, 3000, 10000),
    )
    parser.add_argument("--positive-heads", type=int, choices=range(5))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-gradient", action="store_true")
    arguments = parser.parse_args()
    if arguments.mask < 0 or arguments.mask >= 1 << VERTICES:
        raise ValueError("mask is outside the six-bit truth-table range")

    signs = signs_from_mask(arguments.mask)
    if arguments.check_gradient:
        error = finite_difference_check(signs, (-1, -1, 1, 1), arguments.seed)
        print(f"relative directional gradient error: {error}")
        if error > 1e-4:
            raise AssertionError("inner LP gradient check failed")

    orientation_counts = (
        range(5)
        if arguments.positive_heads is None
        else (arguments.positive_heads,)
    )
    attempts = []
    certificate = None
    for positive_heads in orientation_counts:
        found, best = search_orientation(
            signs,
            positive_heads,
            arguments.seed + 1009 * positive_heads,
            arguments.restarts,
            arguments.max_iterations,
            tuple(arguments.scales),
        )
        attempts.append({"positive_heads": positive_heads, "best": best})
        if found is not None:
            certificate = found
            break

    payload = {
        "status": "Every success is exact. A failure is only search evidence.",
        "truth_mask_hex": f"0x{arguments.mask:016x}",
        "attempts": attempts,
        "h4_certificate": certificate,
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if arguments.output is not None:
        arguments.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
