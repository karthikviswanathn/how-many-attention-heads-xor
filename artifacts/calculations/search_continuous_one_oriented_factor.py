#!/usr/bin/env python3
"""Search for a two-head score through a one-oriented-factor relaxation.

The continuous model is Q = A D + C B, where A, C, D are unrestricted
affine forms and B is a positive affine form whose slopes all have one sign.
This relaxation is already equivalent to H2: for a sufficiently large positive
integer k, E = D + k B has the same admissible orientation as B, and

    Q = A E + (C - k A) B.

Every reported success rounds B and D, solves the resulting fixed-factor LP,
performs this reparameterization, and verifies the final integer certificate
exactly on the Boolean cube.  A failure is only a search failure.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

import search_adversarial_low_dimension as core


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
    literals: np.ndarray,
) -> tuple[np.ndarray, ...]:
    width = affine.shape[1]
    first_numerator = variables[:width]
    second_numerator = variables[width : 2 * width]
    free_factor = variables[2 * width : 3 * width]
    theta = softmax(variables[3 * width :])
    return (
        first_numerator,
        second_numerator,
        free_factor,
        theta,
        affine @ first_numerator,
        affine @ second_numerator,
        affine @ free_factor,
        literals @ theta,
    )


def objective_gradient(
    variables: np.ndarray,
    signs: np.ndarray,
    affine: np.ndarray,
    literals: np.ndarray,
    regularization: float,
) -> tuple[float, np.ndarray]:
    width = affine.shape[1]
    (
        first_numerator,
        second_numerator,
        free_factor,
        theta,
        first_values,
        second_values,
        free_values,
        oriented_values,
    ) = unpack(variables, affine, literals)
    score = first_values * free_values + second_values * oriented_values
    arguments = -signs * score
    score_gradient = -signs * expit(arguments) / len(signs)

    loss = float(np.mean(np.logaddexp(0.0, arguments)))
    loss += regularization * (
        first_numerator @ first_numerator
        + second_numerator @ second_numerator
        + free_factor @ free_factor
        + 0.001 * variables[3 * width :] @ variables[3 * width :]
    )

    gradient_first = affine.T @ (score_gradient * free_values)
    gradient_second = affine.T @ (score_gradient * oriented_values)
    gradient_free = affine.T @ (score_gradient * first_values)
    gradient_first += 2 * regularization * first_numerator
    gradient_second += 2 * regularization * second_numerator
    gradient_free += 2 * regularization * free_factor

    theta_gradient = literals.T @ (score_gradient * second_values)
    logit_gradient = theta * (theta_gradient - theta @ theta_gradient)
    logit_gradient += 0.002 * regularization * variables[3 * width :]
    return loss, np.concatenate(
        [gradient_first, gradient_second, gradient_free, logit_gradient]
    )


def integer_oriented_factor(
    theta: np.ndarray, orientation: int, scale: int
) -> np.ndarray:
    literal_weights = np.array(
        [max(1, int(round(scale * value))) for value in theta], dtype=np.int64
    )
    if orientation > 0:
        return literal_weights
    return np.concatenate(
        [[int(np.sum(literal_weights))], -literal_weights[1:]]
    ).astype(np.int64)


def integer_free_factor(values: np.ndarray, scale: int) -> np.ndarray:
    maximum = float(np.max(np.abs(values)))
    if maximum == 0:
        return np.zeros(len(values), dtype=np.int64)
    return np.rint(scale * values / maximum).astype(np.int64)


def admissible_shift(
    oriented: np.ndarray, free: np.ndarray, orientation: int
) -> int:
    bounds = []
    if orientation > 0:
        bounds.append(-free[0] / oriented[0])
        bounds.extend(
            -free[index] / oriented[index]
            for index in range(1, len(oriented))
        )
    else:
        bounds.extend(
            free[index] / (-oriented[index])
            for index in range(1, len(oriented))
        )
        oriented_minimum = int(np.sum(oriented))
        free_at_minimum = int(np.sum(free))
        bounds.append(-free_at_minimum / oriented_minimum)
    return max(1, int(math.floor(max(bounds))) + 1)


def exact_certificate(
    signs: np.ndarray,
    dimension: int,
    oriented: np.ndarray,
    free: np.ndarray,
    orientation: int,
) -> dict[str, object] | None:
    factors = np.vstack([oriented, free])
    matrix = core.cleared_two_head_matrix(dimension, factors)
    exact = core.exact_integer_separator(signs, matrix)
    if exact is None:
        return None
    coefficients, fixed_margin = exact
    width = dimension + 1
    constant = int(coefficients[0])
    first = np.array(coefficients[1 : 1 + width], dtype=object)
    second = np.array(coefficients[1 + width :], dtype=object)
    absorbed_first = first + constant * oriented.astype(object)

    shift = admissible_shift(oriented, free, orientation)
    second_admissible = free.astype(object) + shift * oriented.astype(object)
    shifted_second = second - shift * absorbed_first

    affine = core.affine_matrix(dimension).astype(object)
    values = affine @ np.vstack(
        [oriented.astype(object), second_admissible]
    ).T
    if not all(int(value) > 0 for value in values.flat):
        raise AssertionError("reparameterized denominator is not positive")
    for denominator in (oriented, second_admissible):
        slopes = denominator[1:]
        if orientation > 0:
            assert all(int(value) > 0 for value in slopes)
        else:
            assert all(int(value) < 0 for value in slopes)

    score = (
        (affine @ absorbed_first) * values[:, 1]
        + (affine @ shifted_second) * values[:, 0]
    )
    signed_score = signs.astype(object) * score
    minimum = int(min(signed_score))
    if minimum <= 0:
        raise AssertionError("integer reparameterization changed a score sign")
    return {
        "orientation": orientation,
        "one_factor_form": {
            "oriented_factor": [int(value) for value in oriented],
            "free_factor": [int(value) for value in free],
            "absorbed_numerators": [
                [int(value) for value in absorbed_first],
                [int(value) for value in second],
            ],
        },
        "admissible_shift": shift,
        "denominators": [
            [int(value) for value in oriented],
            [int(value) for value in second_admissible],
        ],
        "numerators": [
            [int(value) for value in absorbed_first],
            [int(value) for value in shifted_second],
        ],
        "denominator_value_ranges": [
            [int(np.min(values[:, index])), int(np.max(values[:, index]))]
            for index in range(2)
        ],
        "minimum_signed_cleared_score": minimum,
        "fixed_factor_normalized_margin": fixed_margin,
    }


def search(arguments: argparse.Namespace) -> dict[str, object]:
    inputs = core.cube(arguments.dimension).astype(float)
    affine = np.column_stack([np.ones(len(inputs)), inputs])
    signs = core.signs_from_mask(arguments.mask, arguments.dimension).astype(float)
    width = arguments.dimension + 1
    rng = np.random.default_rng(arguments.seed)
    best_accuracy = 0
    best_minimum = float("-inf")
    best_model: dict[str, object] | None = None

    for orientation in (-1, 1):
        literals = literal_matrix(inputs, orientation)
        for restart in range(arguments.restarts):
            variables = np.concatenate(
                [
                    rng.normal(scale=0.5, size=3 * width),
                    rng.normal(scale=2.0, size=width),
                ]
            )
            regularization = 10 ** rng.uniform(-11.0, -5.0)
            result = minimize(
                lambda current: objective_gradient(
                    current, signs, affine, literals, regularization
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
                first_numerator,
                second_numerator,
                free_factor,
                theta,
                first_values,
                second_values,
                free_values,
                oriented_values,
            ) = unpack(result.x, affine, literals)
            signed = signs * (
                first_values * free_values + second_values * oriented_values
            )
            accuracy = int(np.sum(signed > 0))
            minimum = float(np.min(signed))
            if (accuracy, minimum) > (best_accuracy, best_minimum):
                best_accuracy, best_minimum = accuracy, minimum
                best_model = {
                    "orientation": orientation,
                    "restart": restart,
                    "first_numerator": first_numerator.tolist(),
                    "second_numerator": second_numerator.tolist(),
                    "free_factor": free_factor.tolist(),
                    "oriented_literal_weights": theta.tolist(),
                    "oriented_factor_value_range": [
                        float(np.min(oriented_values)),
                        float(np.max(oriented_values)),
                    ],
                    "misclassified_vertex_codes": [
                        int(index) for index in np.flatnonzero(signed <= 0)
                    ],
                }
                print(
                    f"orientation={orientation} restart={restart} "
                    f"accuracy={accuracy}/{len(signs)} minimum={minimum}",
                    flush=True,
                )
            if minimum <= 1e-8:
                continue

            for oriented_scale, free_scale in itertools.product(
                arguments.scales, repeat=2
            ):
                oriented = integer_oriented_factor(
                    theta, orientation, oriented_scale
                )
                free = integer_free_factor(free_factor, free_scale)
                certificate = exact_certificate(
                    signs.astype(np.int64),
                    arguments.dimension,
                    oriented,
                    free,
                    orientation,
                )
                if certificate is None:
                    continue
                return {
                    "found": True,
                    "dimension": arguments.dimension,
                    "truth_mask_hex": hex(arguments.mask),
                    "restart": restart,
                    "oriented_rounding_scale": oriented_scale,
                    "free_rounding_scale": free_scale,
                    **certificate,
                }

    return {
        "found": False,
        "dimension": arguments.dimension,
        "truth_mask_hex": hex(arguments.mask),
        "restarts_per_orientation": arguments.restarts,
        "best_accuracy": best_accuracy,
        "best_minimum_signed_score": best_minimum,
        "best_model": best_model,
        "warning": "A search failure is not an H2 lower bound.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--mask", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--restarts", type=int, default=500)
    parser.add_argument("--max-iterations", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20260713)
    parser.add_argument(
        "--scales", type=int, nargs="+", default=(10, 30, 100, 300, 1000)
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = search(arguments)
    rendered = json.dumps(result, indent=2) + "\n"
    print(rendered, end="")
    if arguments.output is not None:
        arguments.output.write_text(rendered)


if __name__ == "__main__":
    main()
