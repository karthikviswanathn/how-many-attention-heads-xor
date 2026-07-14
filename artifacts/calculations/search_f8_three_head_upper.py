#!/usr/bin/env python3
"""Search and exactly verify a three-head representation of HDTH4.

The target on ``x,y in {0,1}^4`` is positive exactly when their Hamming
distance is at least two.  The nonlinear phase searches all four orientation
counts for three admissible denominators.  Every candidate denominator tuple
is rounded, its numerators are solved by a fixed-denominator linear program,
and any reported certificate is checked with integer arithmetic.

A search failure is not an upper or lower bound.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

import search_gated_single_flip as common


DIMENSION = 8
HEADS = 3
WIDTH = DIMENSION + 1
VERTICES = 1 << DIMENSION
HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "f8_three_head_upper_search.json"


def target_signs() -> np.ndarray:
    answer = []
    for code in range(VERTICES):
        x = [(code >> index) & 1 for index in range(4)]
        y = [(code >> (index + 4)) & 1 for index in range(4)]
        distance = sum(left != right for left, right in zip(x, y))
        answer.append(1 if distance >= 2 else -1)
    return np.array(answer, dtype=np.int64)


def search_orientation(
    signs: np.ndarray,
    positive_heads: int,
    seed: int,
    restarts: int,
    max_iterations: int,
    scales: tuple[int, ...],
) -> tuple[dict[str, object] | None, dict[str, object]]:
    orientations = tuple(
        [-1] * (HEADS - positive_heads) + [1] * positive_heads
    )
    inputs = common.cube(DIMENSION).astype(float)
    affine = common.affine_matrix(DIMENSION, float)
    literals = [
        common.literal_matrix(inputs, orientation)
        for orientation in orientations
    ]
    rng = np.random.default_rng(seed)
    best_accuracy = 0
    best_minimum = float("-inf")
    best: dict[str, object] = {}

    def objective_gradient(
        variables: np.ndarray, regularization: float
    ) -> tuple[float, np.ndarray]:
        numerators = variables[: HEADS * WIDTH].reshape(HEADS, WIDTH)
        logits = variables[HEADS * WIDTH :].reshape(HEADS, WIDTH)
        theta = common.softmax(logits)
        denominator_values = np.column_stack(
            [literals[head] @ theta[head] for head in range(HEADS)]
        )
        numerator_values = affine @ numerators.T
        score = np.sum(numerator_values / denominator_values, axis=1)
        arguments = -signs * score
        score_gradient = -signs * expit(arguments) / VERTICES
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
                for head in range(HEADS)
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
                rng.normal(scale=0.7, size=HEADS * WIDTH),
                rng.normal(scale=3.0, size=HEADS * WIDTH),
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
        numerators = result.x[: HEADS * WIDTH].reshape(HEADS, WIDTH)
        theta = common.softmax(
            result.x[HEADS * WIDTH :].reshape(HEADS, WIDTH)
        )
        denominator_values = np.column_stack(
            [literals[head] @ theta[head] for head in range(HEADS)]
        )
        score = np.sum(
            (affine @ numerators.T) / denominator_values, axis=1
        )
        signed = signs * score
        accuracy = int(np.sum(signed > 0))
        minimum = float(np.min(signed))
        if (accuracy, minimum) > (best_accuracy, best_minimum):
            best_accuracy = accuracy
            best_minimum = minimum
            best = {
                "restart": restart,
                "accuracy": accuracy,
                "minimum_signed_score": minimum,
                "wrong_vertices": [
                    int(index) for index in np.flatnonzero(signed <= 0)
                ],
                "optimizer_success": bool(result.success),
            }
            print(
                f"positive_heads={positive_heads} restart={restart} "
                f"accuracy={accuracy}/{VERTICES} minimum={minimum}",
                flush=True,
            )

        for scale in scales:
            denominators = np.vstack(
                [
                    common.oriented_integer_denominator(
                        scale * theta[head], orientations[head]
                    )
                    for head in range(HEADS)
                ]
            )
            certificate = common.exact_fixed_certificate(
                signs, DIMENSION, denominators
            )
            if certificate is not None:
                certificate.update(
                    {
                        "positive_heads": positive_heads,
                        "orientations": list(orientations),
                        "restart": restart,
                        "rounding_scale": scale,
                    }
                )
                return certificate, best
    return None, best


def verify_certificate(certificate: dict[str, object]) -> int:
    signs = target_signs().astype(object)
    denominators = np.array(certificate["denominators"], dtype=object)
    assert denominators.shape == (HEADS, WIDTH)
    values = common.affine_matrix(DIMENSION, object) @ denominators.T
    assert np.all(values > 0)
    orientations = certificate["orientations"]
    for row, orientation in zip(denominators, orientations):
        slopes = row[1:]
        if orientation > 0:
            assert all(int(value) > 0 for value in slopes)
        else:
            assert all(int(value) < 0 for value in slopes)
    coefficients = np.array(
        certificate["score_coefficients"], dtype=object
    )
    matrix = common.cleared_matrix(DIMENSION, denominators)
    signed = signs * (matrix @ coefficients)
    minimum = int(min(signed))
    assert minimum > 0
    assert minimum == int(certificate["minimum_signed_cleared_score"])
    return minimum


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=128)
    parser.add_argument("--max-iterations", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=820260714)
    parser.add_argument(
        "--scales",
        type=int,
        nargs="+",
        default=(10, 30, 100, 300, 1000, 3000, 10000),
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        payload = json.loads(arguments.output.read_text())
        assert payload["certificate"] is not None
        minimum = verify_certificate(payload["certificate"])
        print(f"minimum signed cleared score: {minimum}")
        print("three-head certificate: verified")
        return

    signs = target_signs()
    payload: dict[str, object] = {
        "status": (
            "Every reported certificate is verified over the integers. "
            "A search failure is not a lower bound."
        ),
        "dimension": DIMENSION,
        "target": "Hamming distance at least two between two four-bit blocks",
        "attempts": [],
        "certificate": None,
    }
    for positive_heads in range(HEADS + 1):
        certificate, best = search_orientation(
            signs,
            positive_heads,
            arguments.seed + 1009 * positive_heads,
            arguments.restarts,
            arguments.max_iterations,
            tuple(arguments.scales),
        )
        payload["attempts"].append(
            {"positive_heads": positive_heads, "best": best}
        )
        if certificate is not None:
            verify_certificate(certificate)
            payload["certificate"] = certificate
            break
        arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
