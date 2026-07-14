#!/usr/bin/env python3
"""Search for an unrestricted two-affine-factor rank-four sign separator.

This drops every denominator positivity and orientation constraint.  A success
is therefore only a rank-four/tangent-Chow relaxation of H2, but an exact
success distinguishes an orientation obstruction from a stronger algebraic
one.  Every success is rounded to integer factors and checked exactly.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

import search_adversarial_low_dimension as core


def objective_gradient(
    variables: np.ndarray,
    signs: np.ndarray,
    affine: np.ndarray,
    regularization: float,
) -> tuple[float, np.ndarray]:
    width = affine.shape[1]
    first_numerator = variables[:width]
    second_numerator = variables[width : 2 * width]
    first_factor = variables[2 * width : 3 * width]
    second_factor = variables[3 * width :]
    a = affine @ first_numerator
    c = affine @ second_numerator
    b = affine @ first_factor
    d = affine @ second_factor
    score = a * d + c * b
    arguments = -signs * score
    score_gradient = -signs * expit(arguments) / len(signs)
    loss = float(np.mean(np.logaddexp(0.0, arguments)))
    loss += regularization * float(variables @ variables)
    gradient = np.concatenate(
        [
            affine.T @ (score_gradient * d),
            affine.T @ (score_gradient * b),
            affine.T @ (score_gradient * c),
            affine.T @ (score_gradient * a),
        ]
    )
    gradient += 2 * regularization * variables
    return loss, gradient


def integer_factor(values: np.ndarray, scale: int) -> np.ndarray:
    maximum = float(np.max(np.abs(values)))
    if maximum == 0:
        return np.zeros(len(values), dtype=np.int64)
    return np.rint(scale * values / maximum).astype(np.int64)


def search(arguments: argparse.Namespace) -> dict[str, object]:
    signs = core.signs_from_mask(arguments.mask, arguments.dimension)
    affine = core.affine_matrix(arguments.dimension).astype(float)
    width = affine.shape[1]
    rng = np.random.default_rng(arguments.seed)
    best_accuracy = 0
    best_minimum = float("-inf")
    for restart in range(arguments.restarts):
        initial = rng.normal(scale=0.5, size=4 * width)
        regularization = 10 ** rng.uniform(-11.0, -5.0)
        result = minimize(
            lambda current: objective_gradient(
                current, signs, affine, regularization
            ),
            initial,
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": arguments.max_iterations,
                "ftol": 1e-14,
                "gtol": 1e-9,
                "maxls": 50,
            },
        )
        variables = result.x
        a = affine @ variables[:width]
        c = affine @ variables[width : 2 * width]
        b = affine @ variables[2 * width : 3 * width]
        d = affine @ variables[3 * width :]
        signed = signs * (a * d + c * b)
        accuracy = int(np.sum(signed > 0))
        minimum = float(np.min(signed))
        if (accuracy, minimum) > (best_accuracy, best_minimum):
            best_accuracy, best_minimum = accuracy, minimum
            print(
                f"restart={restart} accuracy={accuracy}/{len(signs)} "
                f"minimum={minimum}",
                flush=True,
            )
        if minimum <= 1e-8:
            continue
        for scale in arguments.scales:
            denominators = np.array(
                [
                    integer_factor(
                        variables[2 * width : 3 * width], scale
                    ),
                    integer_factor(variables[3 * width :], scale),
                ],
                dtype=np.int64,
            )
            if not np.all(np.any(denominators != 0, axis=1)):
                continue
            matrix = core.cleared_two_head_matrix(
                arguments.dimension, denominators
            )
            exact = core.exact_integer_separator(signs, matrix)
            if exact is None:
                continue
            coefficients, floating_margin = exact
            signed_exact = signs.astype(object) * (
                matrix.astype(object) @ coefficients.astype(object)
            )
            return {
                "found": True,
                "dimension": arguments.dimension,
                "truth_mask_hex": hex(arguments.mask),
                "restart": restart,
                "factor_rounding_scale": scale,
                "factors": denominators.tolist(),
                "cleared_score_coefficients": [
                    int(value) for value in coefficients
                ],
                "minimum_signed_cleared_score": min(map(int, signed_exact)),
                "fixed_factor_floating_margin": floating_margin,
            }
    return {
        "found": False,
        "dimension": arguments.dimension,
        "truth_mask_hex": hex(arguments.mask),
        "restarts": arguments.restarts,
        "best_accuracy": best_accuracy,
        "best_minimum_signed_score": best_minimum,
        "warning": "Failure is not a rank-four impossibility certificate.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--mask", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--restarts", type=int, default=500)
    parser.add_argument("--max-iterations", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument(
        "--scales", type=int, nargs="+", default=(10, 30, 100, 300, 1000, 3000)
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = search(arguments)
    rendered = json.dumps(result, indent=2) + "\n"
    if arguments.output is not None:
        arguments.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
