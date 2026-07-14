#!/usr/bin/env python3
"""Adversarial search against the repaired-support cleared-q ansatz.

After dividing each cleared row by the positive product of denominators, the
two relation columns become R1/F and R2/F.  A strict separator in these 27
columns refutes the proposed positive degree-four cleared multiplier.

The inner linear program globally optimizes separator coefficients.  Its
dual marginals give the exact piecewise-smooth outer gradient, including the
derivative of the two product-denominator relation columns.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import linprog, minimize

import search_n6_h4_inner_lp as base
import verify_n6_parity_triple_repaired_degree4_relations as relations


MASK = 0x96696BD669B69669
SUPPORT = np.array(relations.SUPPORT56, dtype=int)
SIGNS = base.signs_from_mask(MASK)
RELATIONS = np.column_stack(
    [
        np.array(
            [relations.relation(normal, (code,))[0] for code in SUPPORT],
            dtype=float,
        )
        for normal in (relations.M1, relations.M2)
    ]
)


def interior_softmax(logits: np.ndarray) -> tuple[np.ndarray, float]:
    """Return simplex weights bounded away from zero and its Jacobian scale."""
    centered = logits - np.max(logits, axis=1, keepdims=True)
    exponentials = np.exp(np.maximum(centered, -700.0))
    raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
    epsilon = 2e-3
    scale = 1.0 - base.WIDTH * epsilon
    return scale * raw + epsilon, scale


def inner_lp(
    logits_flat: np.ndarray,
    orientations: tuple[int, ...],
    regularization: float,
    anchor_index: int,
    anchor_value: int,
) -> tuple[float, np.ndarray, dict[str, object]]:
    logits = logits_flat.reshape(base.HEADS, base.WIDTH)
    theta, softmax_scale = interior_softmax(logits)
    literals = [base.literal_matrix(value) for value in orientations]
    denominator_values = np.column_stack(
        [literals[head] @ theta[head] for head in range(base.HEADS)]
    )
    denominator_product = np.prod(denominator_values[SUPPORT], axis=1)
    tangent_features = np.column_stack(
        [np.ones(base.VERTICES)]
        + [
            base.AFFINE[:, 1:] / denominator_values[:, head, None]
            for head in range(base.HEADS)
        ]
    )
    signed_tangent = SIGNS[SUPPORT, None] * tangent_features[SUPPORT]
    scaled_relations = RELATIONS / denominator_product[:, None]
    augmented = np.column_stack([signed_tangent, scaled_relations])
    coefficient_count = augmented.shape[1]
    constraints = np.zeros((len(SUPPORT), coefficient_count + 1))
    constraints[:, :coefficient_count] = -augmented
    constraints[:, -1] = 1.0
    objective = np.zeros(coefficient_count + 1)
    objective[-1] = -1.0
    coefficient_bounds = [(-1.0, 1.0)] * coefficient_count
    coefficient_bounds[anchor_index] = (
        float(anchor_value),
        float(anchor_value),
    )
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(SUPPORT)),
        bounds=coefficient_bounds + [(None, None)],
        method="highs-ds",
    )
    if not result.success:
        result = linprog(
            objective,
            A_ub=constraints,
            b_ub=np.zeros(len(SUPPORT)),
            bounds=coefficient_bounds + [(None, None)],
            method="highs-ipm",
        )
    if not result.success:
        raise RuntimeError(result.message)

    coefficients = result.x[:coefficient_count]
    relation_value = scaled_relations @ coefficients[-2:]
    dual_marginals = np.array(result.ineqlin.marginals, dtype=float)
    theta_gradient = np.zeros_like(theta)
    for head in range(base.HEADS):
        start = 1 + head * base.N
        numerator = (
            base.AFFINE[SUPPORT, 1:]
            @ coefficients[start : start + base.N]
        )
        value_gradient = dual_marginals * (
            SIGNS[SUPPORT]
            * (-numerator / denominator_values[SUPPORT, head] ** 2)
            - relation_value / denominator_values[SUPPORT, head]
        )
        theta_gradient[head] = literals[head][SUPPORT].T @ value_gradient
    raw = (theta - 2e-3) / softmax_scale
    logit_gradient = softmax_scale * raw * (
        theta_gradient
        - np.sum(raw * theta_gradient, axis=1, keepdims=True)
    )
    centered = logits - np.mean(logits, axis=1, keepdims=True)
    loss = float(result.fun) + 0.5 * regularization * float(
        np.sum(centered * centered)
    )
    logit_gradient += regularization * centered
    return loss, logit_gradient.ravel(), {
        "margin": float(result.x[-1]),
        "theta": theta,
        "coefficients": coefficients,
        "active_dual_rows": int(np.sum(dual_marginals < -1e-10)),
    }


def finite_difference_error(
    positive_heads: int, seed: int = 202607145
) -> float:
    orientations = tuple(
        [-1] * (base.HEADS - positive_heads) + [1] * positive_heads
    )
    rng = np.random.default_rng(seed)
    point = rng.normal(size=base.HEADS * base.WIDTH)
    _, gradient, _ = inner_lp(point, orientations, 0.0, 0, 1)
    direction = rng.normal(size=len(point))
    direction /= np.linalg.norm(direction)
    epsilon = 1e-5
    plus = inner_lp(
        point + epsilon * direction, orientations, 0.0, 0, 1
    )[0]
    minus = inner_lp(
        point - epsilon * direction, orientations, 0.0, 0, 1
    )[0]
    numerical = (plus - minus) / (2.0 * epsilon)
    analytic = float(gradient @ direction)
    return abs(numerical - analytic) / max(1.0, abs(numerical), abs(analytic))


def search_orientation(
    positive_heads: int,
    restarts: int,
    iterations: int,
    seed: int,
) -> tuple[float, np.ndarray, np.ndarray]:
    orientations = tuple(
        [-1] * (base.HEADS - positive_heads) + [1] * positive_heads
    )
    rng = np.random.default_rng(seed)
    best_margin = float("-inf")
    best_theta = np.zeros((base.HEADS, base.WIDTH))
    best_coefficients = np.zeros(27)
    for restart in range(restarts):
        anchor_index = (restart // 2) % 27
        anchor_value = 1 if restart % 2 == 0 else -1
        scale = float(rng.choice((0.5, 1.5, 3.0, 6.0, 10.0, 15.0)))
        initial = rng.normal(scale=scale, size=(base.HEADS, base.WIDTH))
        regularization = 10 ** rng.uniform(-12.0, -7.0)

        def objective(current: np.ndarray) -> tuple[float, np.ndarray]:
            loss, gradient, _ = inner_lp(
                current,
                orientations,
                regularization,
                anchor_index,
                anchor_value,
            )
            return loss, gradient

        result = minimize(
            objective,
            initial.ravel(),
            jac=True,
            method="L-BFGS-B",
            bounds=[(-24.0, 24.0)] * (base.HEADS * base.WIDTH),
            options={
                "maxiter": iterations,
                "maxfun": 8 * iterations,
                "ftol": 1e-13,
                "gtol": 1e-8,
                "maxls": 30,
            },
        )
        _, _, diagnostics = inner_lp(
            result.x,
            orientations,
            regularization,
            anchor_index,
            anchor_value,
        )
        margin = float(diagnostics["margin"])
        if margin > best_margin:
            best_margin = margin
            best_theta = np.array(diagnostics["theta"], dtype=float)
            best_coefficients = np.array(
                diagnostics["coefficients"], dtype=float
            )
            print(
                f"orientation={positive_heads} restart={restart} "
                f"anchor=({anchor_index},{anchor_value}) margin={margin} "
                f"active={diagnostics['active_dual_rows']}",
                flush=True,
            )
            print(f"  theta={best_theta.tolist()}", flush=True)
    return best_margin, best_theta, best_coefficients


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=108)
    parser.add_argument("--iterations", type=int, default=240)
    parser.add_argument("--seed", type=int, default=202607145)
    parser.add_argument("--positive-heads", type=int, choices=range(3))
    parser.add_argument("--check-gradient", action="store_true")
    arguments = parser.parse_args()

    if arguments.check_gradient:
        for positive_heads in range(3):
            error = finite_difference_error(positive_heads)
            print(f"orientation={positive_heads} gradient_relative_error={error}")
        return

    orientation_counts = (
        range(3)
        if arguments.positive_heads is None
        else (arguments.positive_heads,)
    )
    for positive_heads in orientation_counts:
        margin, theta, coefficients = search_orientation(
            positive_heads,
            arguments.restarts,
            arguments.iterations,
            arguments.seed + 1009 * positive_heads,
        )
        print(f"orientation={positive_heads} best_margin={margin}")
        print(f"best_theta={theta.tolist()}")
        print(f"best_coefficients={coefficients.tolist()}")


if __name__ == "__main__":
    main()
