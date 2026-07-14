#!/usr/bin/env python3
"""Search evaluation-structured slice duals for the six-bit H4 candidate.

On slice ``i``, positivity of all level-one and level-three reoriented Fourier
coefficients implies positivity of the odd part at every positive vector.  A
dual of the form

    y(i, S) = lambda_i * product(u[i, j] for j in S)

is therefore a positive combination of six such odd-part evaluations.  This
diagnostic asks whether these structured weights can annihilate a fixed
four-head tangent space.  Numerical success is only evidence for a possible
analytic construction.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import least_squares

import analyze_n6_parity_triple_slice_subsystems as common


INDICES = tuple(
    index for index, label in enumerate(common.LABELS) if label[2] in (1, 3)
)
LABELS = tuple(common.LABELS[index] for index in INDICES)


def design_matrix() -> np.ndarray:
    answer = np.zeros((len(LABELS), common.N * common.N), dtype=float)
    for row, (coordinate, subset, _) in enumerate(LABELS):
        answer[row, coordinate] = 1.0
        other_coordinates = [
            value for value in range(common.N) if value != coordinate
        ]
        for position, value in enumerate(other_coordinates):
            if subset & (1 << value):
                answer[
                    row,
                    common.N + coordinate * (common.N - 1) + position,
                ] = 1.0
    return answer


DESIGN = design_matrix()


def weights(parameters: np.ndarray) -> np.ndarray:
    log_weights = DESIGN @ parameters
    log_weights -= np.max(log_weights)
    result = np.exp(np.maximum(log_weights, -700.0))
    return result / np.sum(result)


def search(
    matrix: np.ndarray,
    rng: np.random.Generator,
    restarts: int,
    evaluations: int,
) -> tuple[float, np.ndarray]:
    scale = np.linalg.norm(matrix, axis=0)
    scale = np.maximum(scale, 1e-12)
    normalized = matrix / scale[None, :]
    best = float("inf")
    best_parameters = np.zeros(common.N * common.N)
    for _ in range(restarts):
        initial = rng.normal(scale=1.0, size=common.N * common.N)
        def residual(current: np.ndarray) -> np.ndarray:
            return normalized.T @ weights(current)

        def jacobian(current: np.ndarray) -> np.ndarray:
            current_weights = weights(current)
            mean_design = current_weights @ DESIGN
            weight_jacobian = current_weights[:, None] * (
                DESIGN - mean_design[None, :]
            )
            return normalized.T @ weight_jacobian

        result = least_squares(
            residual,
            initial,
            jac=jacobian,
            bounds=(-12.0, 12.0),
            max_nfev=evaluations,
            ftol=1e-14,
            xtol=1e-14,
            gtol=1e-14,
        )
        residual = float(np.linalg.norm(normalized.T @ weights(result.x)))
        if residual < best:
            best = residual
            best_parameters = result.x
    return best, best_parameters


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--evaluations", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260714)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    for positive_heads in range(3):
        for sample in range(args.samples):
            denominators = common.sample_denominators(rng, positive_heads)
            full = common.R @ common.tangent_map(denominators)
            matrix = full[list(INDICES)]
            residual, parameters = search(
                matrix, rng, args.restarts, args.evaluations
            )
            current_weights = weights(parameters)
            print(
                f"positive_heads={positive_heads} sample={sample} "
                f"residual={residual} min_weight={np.min(current_weights)} "
                f"max_weight={np.max(current_weights)}"
            )
            if sample == 0:
                centered_lambda = parameters[: common.N] - np.max(
                    parameters[: common.N]
                )
                print("  lambda=", np.exp(centered_lambda).tolist())
                print(
                    "  u=",
                    np.exp(
                        parameters[common.N :].reshape(
                            common.N, common.N - 1
                        )
                    ).tolist(),
                )
                print("  denominators=", denominators.tolist())


if __name__ == "__main__":
    main()
