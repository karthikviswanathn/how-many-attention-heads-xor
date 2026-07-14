#!/usr/bin/env python3
"""Search a fixed-support Gordan circuit for the six-bit H4 candidate.

For each orientation count, this diagnostic generates extreme circuits of the
90 one-exception-slice inequalities at Fourier levels one and three.  It then
tests whether the same 26-row support keeps one circuit sign throughout many
sampled admissible denominator tuples.  A surviving support is a candidate
for a symbolic minor-sign proof, not by itself a universal certificate.
"""

from __future__ import annotations

import argparse
import collections

import numpy as np
from scipy.optimize import linprog

import analyze_n6_parity_triple_slice_subsystems as common


LEVEL_INDICES = tuple(
    index for index, label in enumerate(common.LABELS) if label[2] in (1, 3)
)


def normalized_matrix(denominators: np.ndarray) -> np.ndarray:
    full = common.R @ common.tangent_map(denominators)
    matrix = full[list(LEVEL_INDICES)]
    norms = np.linalg.norm(matrix, axis=1)
    if np.any(norms <= 1e-12):
        raise RuntimeError("zero pulled-back inequality")
    return matrix / norms[:, None]


def extreme_support(
    matrix: np.ndarray, objective: np.ndarray
) -> tuple[int, ...] | None:
    rows = matrix.shape[0]
    equalities = np.vstack([matrix.T, np.ones((1, rows), dtype=float)])
    target = np.zeros(equalities.shape[0], dtype=float)
    target[-1] = 1.0
    result = linprog(
        objective,
        A_eq=equalities,
        b_eq=target,
        bounds=[(0.0, None)] * rows,
        method="highs-ds",
    )
    if not result.success:
        return None
    support = tuple(np.flatnonzero(np.array(result.x) > 1e-8).tolist())
    if len(support) != 26:
        return None
    return support


def circuit_margin(matrix: np.ndarray, support: tuple[int, ...]) -> float:
    restricted = matrix[list(support)].T
    _, singular_values, right = np.linalg.svd(restricted, full_matrices=True)
    if singular_values[-2] <= 1e-10:
        return float("-inf")
    if singular_values[-1] > 1e-7 * singular_values[0]:
        return float("-inf")
    vector = right[-1]
    if np.sum(vector) < 0:
        vector = -vector
    residual = float(np.linalg.norm(restricted @ vector))
    if residual > 1e-7:
        return float("-inf")
    return float(np.min(vector) / np.max(np.abs(vector)))


def label_support(support: tuple[int, ...]) -> list[tuple[int, int, int]]:
    return [common.LABELS[LEVEL_INDICES[index]] for index in support]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=int, default=1000)
    parser.add_argument("--tests", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260714)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    for positive_heads in range(3):
        test_matrices = [
            normalized_matrix(
                common.sample_denominators(rng, positive_heads)
            )
            for _ in range(args.tests)
        ]
        supports: set[tuple[int, ...]] = set()
        for seed_index in range(8):
            seed_matrix = normalized_matrix(
                common.sample_denominators(rng, positive_heads)
            )
            for _ in range((args.candidates + 7) // 8):
                support = extreme_support(
                    seed_matrix, rng.normal(size=seed_matrix.shape[0])
                )
                if support is not None:
                    supports.add(support)

        scores = []
        histogram: collections.Counter[int] = collections.Counter()
        for support in supports:
            margins = []
            for test_index, matrix in enumerate(test_matrices):
                margin = circuit_margin(matrix, support)
                if margin <= 1e-9:
                    break
                margins.append(margin)
            histogram[len(margins)] += 1
            scores.append((len(margins), min(margins, default=-1.0), support))
        scores.sort(reverse=True)
        print(
            f"positive_heads={positive_heads} supports={len(supports)} "
            f"coverage_histogram={dict(sorted(histogram.items()))}"
        )
        for coverage, margin, support in scores[:5]:
            print(
                f"  coverage={coverage}/{args.tests} min_margin={margin} "
                f"labels={label_support(support)}"
            )


if __name__ == "__main__":
    main()
