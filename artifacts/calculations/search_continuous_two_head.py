#!/usr/bin/env python3
"""Search a truth table for a strict two-head certificate.

The denominator coefficients are optimized on log-simplexes.  This is useful
for hard candidates whose successful denominators lie very close to a simplex
face and are therefore missed by broad integer sampling.  Every reported
success is rounded to integer denominators and an integer cleared score, then
verified exactly.

A failure is only a search failure.  It is not a two-head lower bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math

import numpy as np
from scipy.optimize import linprog, minimize
from scipy.special import expit


def cube(dimension: int) -> np.ndarray:
    return (
        (np.arange(1 << dimension)[:, None] >> np.arange(dimension)) & 1
    ).astype(np.int64)


def signs_from_mask(mask: int, dimension: int) -> np.ndarray:
    return np.array(
        [1 if (mask >> vertex) & 1 else -1 for vertex in range(1 << dimension)],
        dtype=np.int64,
    )


def softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - np.max(values)
    exponentials = np.exp(shifted)
    return exponentials / np.sum(exponentials)


def literal_matrix(inputs: np.ndarray, orientation: int) -> np.ndarray:
    literals = inputs if orientation > 0 else 1 - inputs
    return np.column_stack([np.ones(len(inputs)), literals]).astype(float)


def unpack(
    variables: np.ndarray,
    affine: np.ndarray,
    literal_matrices: tuple[np.ndarray, np.ndarray],
) -> tuple[np.ndarray, ...]:
    width = affine.shape[1]
    numerator_1 = variables[:width]
    numerator_2 = variables[width : 2 * width]
    theta_1 = softmax(variables[2 * width : 3 * width])
    theta_2 = softmax(variables[3 * width : 4 * width])
    denominator_1 = literal_matrices[0] @ theta_1
    denominator_2 = literal_matrices[1] @ theta_2
    return (
        numerator_1,
        numerator_2,
        theta_1,
        theta_2,
        denominator_1,
        denominator_2,
    )


def objective_and_gradient(
    variables: np.ndarray,
    signs: np.ndarray,
    affine: np.ndarray,
    literal_matrices: tuple[np.ndarray, np.ndarray],
    regularization: float,
) -> tuple[float, np.ndarray]:
    width = affine.shape[1]
    (
        numerator_1,
        numerator_2,
        theta_1,
        theta_2,
        denominator_1,
        denominator_2,
    ) = unpack(variables, affine, literal_matrices)

    numerator_values_1 = affine @ numerator_1
    numerator_values_2 = affine @ numerator_2
    cleared_score = (
        numerator_values_1 * denominator_2
        + numerator_values_2 * denominator_1
    )
    logistic_arguments = -signs * cleared_score
    score_gradient = -signs * expit(logistic_arguments) / len(signs)

    loss = float(np.mean(np.logaddexp(0.0, logistic_arguments)))
    loss += regularization * (
        numerator_1 @ numerator_1
        + numerator_2 @ numerator_2
        + 0.001 * variables[2 * width :] @ variables[2 * width :]
    )

    gradient_numerator_1 = affine.T @ (score_gradient * denominator_2)
    gradient_numerator_2 = affine.T @ (score_gradient * denominator_1)
    gradient_numerator_1 += 2 * regularization * numerator_1
    gradient_numerator_2 += 2 * regularization * numerator_2

    theta_gradient_1 = literal_matrices[0].T @ (
        score_gradient * numerator_values_2
    )
    theta_gradient_2 = literal_matrices[1].T @ (
        score_gradient * numerator_values_1
    )
    logit_gradient_1 = theta_1 * (
        theta_gradient_1 - theta_1 @ theta_gradient_1
    )
    logit_gradient_2 = theta_2 * (
        theta_gradient_2 - theta_2 @ theta_gradient_2
    )
    logit_gradient_1 += (
        0.002 * regularization * variables[2 * width : 3 * width]
    )
    logit_gradient_2 += (
        0.002 * regularization * variables[3 * width : 4 * width]
    )

    gradient = np.concatenate(
        [
            gradient_numerator_1,
            gradient_numerator_2,
            logit_gradient_1,
            logit_gradient_2,
        ]
    )
    return loss, gradient


def integer_denominator(
    theta: np.ndarray, orientation: int, scale: int
) -> list[int]:
    literal_weights = [
        max(1, int(round(scale * float(coefficient)))) for coefficient in theta
    ]
    if orientation > 0:
        return literal_weights
    return [sum(literal_weights)] + [-value for value in literal_weights[1:]]


def cleared_matrix(
    affine: np.ndarray, denominators: list[list[int]]
) -> np.ndarray:
    affine_object = affine.astype(object)
    denominator_values = (
        affine_object @ np.array(denominators, dtype=object).T
    )
    first = denominator_values[:, 0]
    second = denominator_values[:, 1]
    return np.column_stack(
        [
            first * second,
            affine_object * second[:, None],
            affine_object * first[:, None],
        ]
    ).astype(object)


def exact_score(
    signs: np.ndarray,
    affine: np.ndarray,
    denominators: list[list[int]],
) -> tuple[list[int], int, float] | None:
    denominator_values = (
        affine.astype(float) @ np.array(denominators, dtype=float).T
    )
    features = np.column_stack(
        [
            np.ones(len(signs)),
            affine / denominator_values[:, 0, None],
            affine / denominator_values[:, 1, None],
        ]
    )
    norms = np.linalg.norm(features, axis=0)
    normalized = features / norms
    variable_count = normalized.shape[1]

    constraints = np.zeros((len(signs), variable_count + 1))
    constraints[:, :variable_count] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variable_count + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(signs)),
        bounds=[(-1.0, 1.0)] * variable_count + [(None, None)],
        method="highs",
    )
    if not result.success or -result.fun <= 1e-12:
        return None

    floating_coefficients = result.x[:variable_count] / norms
    matrix = cleared_matrix(affine, denominators)
    signed_floating = signs.astype(object) * (
        matrix @ floating_coefficients.astype(object)
    )
    minimum_floating = min(float(value) for value in signed_floating)
    if minimum_floating <= 0:
        return None

    maximum_row_norm = max(
        sum(abs(int(value)) for value in row) for row in matrix.tolist()
    )
    coefficient_scale = max(
        1, int(math.ceil((maximum_row_norm + 1) / (2 * minimum_floating)))
    )
    signs_object = signs.astype(object)
    for _ in range(160):
        integer_coefficients = np.array(
            [
                int(round(coefficient_scale * coefficient))
                for coefficient in floating_coefficients
            ],
            dtype=object,
        )
        signed_exact = signs_object * (matrix @ integer_coefficients)
        if min(signed_exact) > 0:
            return (
                [int(value) for value in integer_coefficients],
                int(min(signed_exact)),
                float(-result.fun),
            )
        coefficient_scale *= 2
    return None


def search(arguments: argparse.Namespace) -> dict[str, object]:
    inputs = cube(arguments.dimension)
    affine = np.column_stack([np.ones(len(inputs)), inputs]).astype(float)
    signs = signs_from_mask(arguments.mask, arguments.dimension)
    width = arguments.dimension + 1
    rng = np.random.default_rng(arguments.seed)
    best_accuracy = 0
    best_minimum = float("-inf")

    for orientation_index, orientations in enumerate(
        itertools.product((-1, 1), repeat=2)
    ):
        literal_matrices = (
            literal_matrix(inputs, orientations[0]),
            literal_matrix(inputs, orientations[1]),
        )
        for restart in range(arguments.restarts):
            variables = np.concatenate(
                [
                    rng.normal(scale=0.5, size=2 * width),
                    rng.normal(scale=2.0, size=2 * width),
                ]
            )
            regularization = 10 ** rng.uniform(-10.0, -4.0)
            result = minimize(
                lambda current: objective_and_gradient(
                    current,
                    signs,
                    affine,
                    literal_matrices,
                    regularization,
                ),
                variables,
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": arguments.max_iterations,
                    "ftol": 1e-14,
                    "gtol": 1e-9,
                    "maxls": 50,
                },
            )
            (
                numerator_1,
                numerator_2,
                theta_1,
                theta_2,
                denominator_1,
                denominator_2,
            ) = unpack(result.x, affine, literal_matrices)
            signed_scores = signs * (
                (affine @ numerator_1) * denominator_2
                + (affine @ numerator_2) * denominator_1
            )
            accuracy = int(np.sum(signed_scores > 0))
            minimum = float(np.min(signed_scores))
            if (accuracy, minimum) > (best_accuracy, best_minimum):
                best_accuracy, best_minimum = accuracy, minimum
                print(
                    f"orientations={orientations} restart={restart} "
                    f"accuracy={accuracy}/{len(signs)} minimum={minimum}",
                    flush=True,
                )
            if minimum <= 1e-8:
                continue

            for scale in arguments.scales:
                denominators = [
                    integer_denominator(theta_1, orientations[0], scale),
                    integer_denominator(theta_2, orientations[1], scale),
                ]
                exact = exact_score(signs, affine, denominators)
                if exact is None:
                    continue
                coefficients, exact_minimum, fixed_margin = exact
                constant = coefficients[0]
                first_numerator = coefficients[1 : 1 + width]
                second_numerator = coefficients[1 + width :]
                absorbed_first_numerator = [
                    first_numerator[index]
                    + constant * denominators[0][index]
                    for index in range(width)
                ]
                return {
                    "found": True,
                    "dimension": arguments.dimension,
                    "truth_mask_hex": hex(arguments.mask),
                    "orientations": list(orientations),
                    "restart": restart,
                    "orientation_index": orientation_index,
                    "denominator_rounding_scale": scale,
                    "denominators": denominators,
                    "cleared_score_coefficients": coefficients,
                    "absorbed_numerators": [
                        absorbed_first_numerator,
                        second_numerator,
                    ],
                    "minimum_signed_cleared_score": exact_minimum,
                    "fixed_denominator_normalized_margin": fixed_margin,
                }

    return {
        "found": False,
        "dimension": arguments.dimension,
        "truth_mask_hex": hex(arguments.mask),
        "restarts_per_orientation": arguments.restarts,
        "best_accuracy": best_accuracy,
        "best_minimum_signed_score": best_minimum,
        "warning": "A search failure is not a lower bound.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--mask", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--restarts", type=int, default=500)
    parser.add_argument("--max-iterations", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20260713)
    parser.add_argument(
        "--scales",
        type=int,
        nargs="+",
        default=(10, 30, 100, 300, 1000, 3000, 10000, 100000, 1000000),
    )
    arguments = parser.parse_args()
    if arguments.mask < 0 or arguments.mask >= 1 << (1 << arguments.dimension):
        parser.error("mask does not fit the requested truth-table dimension")
    print(json.dumps(search(arguments), indent=2))


if __name__ == "__main__":
    main()
