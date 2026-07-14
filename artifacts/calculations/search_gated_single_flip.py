#!/usr/bin/env python3
"""Search fresh-bit gates over parity with one flipped vertex.

For ``m`` base bits, parity with one flipped vertex has threshold degree
``m - 1``.  Conjunction or disjunction with one fresh bit preserves threshold
degree.  This script asks whether the gated function is still representable
with ``m - 1`` heads.  Every success is rounded to integer denominators and
verified exactly.  A search failure is only diagnostic evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize
from scipy.special import expit


def cube(dimension: int) -> np.ndarray:
    vertices = 1 << dimension
    return (
        (np.arange(vertices)[:, None] >> np.arange(dimension)) & 1
    ).astype(np.int64)


def affine_matrix(dimension: int, dtype: type = np.int64) -> np.ndarray:
    return np.column_stack(
        [np.ones(1 << dimension, dtype=np.int64), cube(dimension)]
    ).astype(dtype)


def base_sign(code: int, base_bits: int, flipped: int) -> int:
    parity = 1 if bin(code).count("1") % 2 == 0 else -1
    return -parity if code == flipped else parity


def target_signs(base_bits: int, flipped: int, gate: str) -> np.ndarray:
    dimension = base_bits + 1
    base_mask = (1 << base_bits) - 1
    answer = []
    for code in range(1 << dimension):
        base_code = code & base_mask
        fresh = (code >> base_bits) & 1
        base_positive = base_sign(base_code, base_bits, flipped) > 0
        if gate == "and":
            positive = bool(fresh and base_positive)
        else:
            positive = bool(fresh or base_positive)
        answer.append(1 if positive else -1)
    return np.array(answer, dtype=np.int64)


def literal_matrix(inputs: np.ndarray, orientation: int) -> np.ndarray:
    literals = inputs if orientation > 0 else 1.0 - inputs
    return np.column_stack([np.ones(len(inputs)), literals])


def softmax(rows: np.ndarray) -> np.ndarray:
    shifted = rows - np.max(rows, axis=1, keepdims=True)
    exponentials = np.exp(np.maximum(shifted, -700.0))
    raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
    epsilon = 1e-12
    return (1.0 - rows.shape[1] * epsilon) * raw + epsilon


def oriented_integer_denominator(
    literal_weights: np.ndarray, orientation: int
) -> np.ndarray:
    weights = [max(1, int(value)) for value in literal_weights]
    if orientation > 0:
        return np.array(weights, dtype=np.int64)
    return np.array(
        [sum(weights)] + [-value for value in weights[1:]],
        dtype=np.int64,
    )


def ratio_features(
    dimension: int, denominators: np.ndarray
) -> np.ndarray:
    affine = affine_matrix(dimension, float)
    values = affine @ denominators.astype(float).T
    if not np.all(values > 0):
        raise ValueError("denominator is not positive")
    return np.column_stack(
        [np.ones(len(affine))]
        + [
            affine / values[:, head, None]
            for head in range(len(denominators))
        ]
    )


def cleared_matrix(
    dimension: int, denominators: np.ndarray
) -> np.ndarray:
    affine = affine_matrix(dimension, object)
    values = affine @ denominators.astype(object).T
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(len(denominators)):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(dimension + 1)
        )
    return np.column_stack(columns).astype(object)


def exact_fixed_certificate(
    signs: np.ndarray, dimension: int, denominators: np.ndarray
) -> dict[str, object] | None:
    features = ratio_features(dimension, denominators)
    norms = np.linalg.norm(features, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = features[:, keep] / norms[keep]
    variables = normalized.shape[1]
    constraints = np.zeros((len(signs), variables + 1))
    constraints[:, :variables] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(signs)),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
    )
    if not result.success or -float(result.fun) <= 1e-11:
        return None

    coefficients = np.zeros(features.shape[1])
    coefficients[keep] = result.x[:variables] / norms[keep]
    matrix = cleared_matrix(dimension, denominators)
    floating_matrix = np.array(matrix, dtype=float)
    floating_margin = float(
        np.min(signs * (floating_matrix @ coefficients))
    )
    if floating_margin <= 1e-12:
        return None
    row_norm = max(
        sum(abs(int(value)) for value in row) for row in matrix.tolist()
    )
    scale = max(1, int(math.ceil((row_norm + 1) / floating_margin)))
    exact_signs = signs.astype(object)
    for _ in range(180):
        integers = np.array(
            [int(round(scale * value)) for value in coefficients],
            dtype=object,
        )
        signed = exact_signs * (matrix @ integers)
        if min(signed) > 0:
            return {
                "denominators": denominators.tolist(),
                "score_coefficients": [int(value) for value in integers],
                "minimum_signed_cleared_score": int(min(signed)),
                "floating_margin": floating_margin,
            }
        scale *= 2
    return None


def search_orientation(
    signs: np.ndarray,
    base_bits: int,
    positive_heads: int,
    seed: int,
    restarts: int,
    max_iterations: int,
    scales: tuple[int, ...],
) -> tuple[dict[str, object] | None, dict[str, object]]:
    dimension = base_bits + 1
    heads = base_bits - 1
    width = dimension + 1
    orientations = tuple(
        [-1] * (heads - positive_heads) + [1] * positive_heads
    )
    inputs = cube(dimension).astype(float)
    affine = affine_matrix(dimension, float)
    literals = [literal_matrix(inputs, value) for value in orientations]
    rng = np.random.default_rng(seed)
    best_accuracy = 0
    best_minimum = float("-inf")
    best: dict[str, object] = {}

    def objective_gradient(
        variables: np.ndarray, regularization: float
    ) -> tuple[float, np.ndarray]:
        numerators = variables[: heads * width].reshape(heads, width)
        logits = variables[heads * width :].reshape(heads, width)
        theta = softmax(logits)
        denominator_values = np.column_stack(
            [literals[head] @ theta[head] for head in range(heads)]
        )
        numerator_values = affine @ numerators.T
        score = np.sum(numerator_values / denominator_values, axis=1)
        arguments = -signs * score
        score_gradient = -signs * expit(arguments) / len(signs)
        loss = float(np.mean(np.logaddexp(0.0, arguments)))
        loss += regularization * (
            np.sum(numerators * numerators)
            + 0.001 * np.sum(logits * logits)
        )

        numerator_gradient = (
            affine.T @ (score_gradient[:, None] / denominator_values)
        ).T
        numerator_gradient += 2 * regularization * numerators
        theta_gradient = np.vstack(
            [
                literals[head].T
                @ (
                    -score_gradient
                    * numerator_values[:, head]
                    / denominator_values[:, head] ** 2
                )
                for head in range(heads)
            ]
        )
        logit_gradient = theta * (
            theta_gradient
            - np.sum(theta * theta_gradient, axis=1, keepdims=True)
        )
        logit_gradient += 0.002 * regularization * logits
        return loss, np.concatenate(
            [numerator_gradient.ravel(), logit_gradient.ravel()]
        )

    for restart in range(restarts):
        variables = np.concatenate(
            [
                rng.normal(scale=0.7, size=heads * width),
                rng.normal(scale=3.0, size=heads * width),
            ]
        )
        regularization = 10 ** rng.uniform(-12.0, -6.0)
        result = minimize(
            lambda current: objective_gradient(current, regularization),
            variables,
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": max_iterations,
                "ftol": 1e-14,
                "gtol": 1e-9,
                "maxls": 60,
            },
        )
        numerators = result.x[: heads * width].reshape(heads, width)
        theta = softmax(result.x[heads * width :].reshape(heads, width))
        denominator_values = np.column_stack(
            [literals[head] @ theta[head] for head in range(heads)]
        )
        signed = signs * np.sum(
            (affine @ numerators.T) / denominator_values, axis=1
        )
        rank = (int(np.sum(signed > 0)), float(np.min(signed)))
        if rank > (best_accuracy, best_minimum):
            best_accuracy, best_minimum = rank
            best = {
                "restart": restart,
                "accuracy": best_accuracy,
                "minimum_signed_smooth_score": best_minimum,
            }

        for scale in scales:
            denominators = np.vstack(
                [
                    oriented_integer_denominator(
                        np.maximum(1, np.rint(scale * theta[head])),
                        orientations[head],
                    )
                    for head in range(heads)
                ]
            )
            certificate = exact_fixed_certificate(
                signs, dimension, denominators
            )
            if certificate is not None:
                certificate["positive_heads"] = positive_heads
                certificate["restart"] = restart
                certificate["rounding_scale"] = scale
                return certificate, best
    return None, best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-bits", type=int, choices=(4, 5), required=True)
    parser.add_argument("--flipped", type=int, required=True)
    parser.add_argument("--gate", choices=("and", "or"), default="and")
    parser.add_argument("--restarts", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=1800)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument(
        "--positive-heads",
        type=int,
        help="search only this denominator-orientation count",
    )
    parser.add_argument(
        "--scales", type=int, nargs="+", default=(30, 100, 300, 1000, 3000)
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if not 0 <= arguments.flipped < (1 << arguments.base_bits):
        raise ValueError("flipped vertex is outside the base cube")

    signs = target_signs(
        arguments.base_bits, arguments.flipped, arguments.gate
    )
    heads = arguments.base_bits - 1
    if arguments.positive_heads is not None and not (
        0 <= arguments.positive_heads <= heads
    ):
        raise ValueError("positive-heads must lie between zero and heads")
    orientation_counts = (
        range(heads + 1)
        if arguments.positive_heads is None
        else (arguments.positive_heads,)
    )
    attempts = []
    certificate = None
    for positive_heads in orientation_counts:
        found, best = search_orientation(
            signs,
            arguments.base_bits,
            positive_heads,
            arguments.seed + 1009 * positive_heads,
            arguments.restarts,
            arguments.max_iterations,
            tuple(arguments.scales),
        )
        attempts.append(
            {"positive_heads": positive_heads, "best": best}
        )
        if found is not None:
            certificate = found
            break

    payload = {
        "status": (
            "Every success is exact. A failure is only search evidence."
        ),
        "base_bits": arguments.base_bits,
        "input_bits": arguments.base_bits + 1,
        "flipped": arguments.flipped,
        "gate": arguments.gate,
        "threshold_degree": arguments.base_bits - 1,
        "heads_searched": heads,
        "attempts": attempts,
        "head_certificate": certificate,
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if arguments.output is not None:
        arguments.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
