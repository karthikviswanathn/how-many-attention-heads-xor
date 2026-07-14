#!/usr/bin/env python3
"""Test whether generic five-bit cubics admit admissible H3 factorizations.

This is a numerical structural diagnostic.  It minimizes the distance from a
target degree-at-most-three polynomial to the cleared score space of three
admissible affine denominators.  A small residual suggests a rational
factorization problem worth solving exactly.  Failure is not a lower bound.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import least_squares
from scipy.special import softmax

import search_adversarial_low_dimension as core


N = 5
HEADS = 3
WIDTH = N + 1
VERTICES = 1 << N


def denominators_from_logits(
    logits: np.ndarray, orientations: tuple[int, ...]
) -> np.ndarray:
    weights = softmax(logits.reshape(HEADS, WIDTH), axis=1)
    rows = []
    for row, orientation in zip(weights, orientations):
        if orientation > 0:
            rows.append(row)
        else:
            rows.append(np.concatenate([[np.sum(row)], -row[1:]]))
    return np.array(rows)


def cleared_matrix(denominators: np.ndarray) -> np.ndarray:
    affine = core.affine_matrix(N).astype(float)
    values = affine @ denominators.T
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(HEADS):
        other_product = np.prod(
            np.delete(values, head, axis=1), axis=1
        )
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(WIDTH)
        )
    return np.column_stack(columns)


def projection_residual(
    logits: np.ndarray,
    orientations: tuple[int, ...],
    target: np.ndarray,
) -> np.ndarray:
    matrix = cleared_matrix(
        denominators_from_logits(logits, orientations)
    )
    coefficients, _, _, _ = np.linalg.lstsq(matrix, target, rcond=1e-12)
    return matrix @ coefficients - target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--restarts", type=int, default=3)
    parser.add_argument("--max-evaluations", type=int, default=1500)
    parser.add_argument("--seed", type=int, default=20260714)
    arguments = parser.parse_args()

    rng = np.random.default_rng(arguments.seed)
    evaluation = core.monomial_matrix(N, 3).astype(float)
    for sample in range(arguments.samples):
        polynomial_coefficients = rng.normal(size=evaluation.shape[1])
        target = evaluation @ polynomial_coefficients
        target /= np.linalg.norm(target)
        best = float("inf")
        best_record = None
        for orientations in itertools.product((-1, 1), repeat=HEADS):
            for restart in range(arguments.restarts):
                initial = rng.normal(scale=2.0, size=HEADS * WIDTH)
                result = least_squares(
                    projection_residual,
                    initial,
                    args=(orientations, target),
                    max_nfev=arguments.max_evaluations,
                    ftol=1e-13,
                    xtol=1e-13,
                    gtol=1e-13,
                )
                residual = float(np.linalg.norm(result.fun))
                if residual < best:
                    best = residual
                    best_record = (
                        orientations,
                        denominators_from_logits(result.x, orientations),
                    )
                if best < 1e-9:
                    break
            if best < 1e-9:
                break
        assert best_record is not None
        orientations, denominators = best_record
        print(
            f"sample={sample} residual={best:.6e} "
            f"orientations={orientations}"
        )
        if best < 1e-9:
            print(f"denominators={denominators.tolist()}")


if __name__ == "__main__":
    main()
