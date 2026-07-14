#!/usr/bin/env python3
"""Diagnose fixed R23-plus-cut circuits across admissible orientation cones.

Known exact extreme-anisotropy tuples escape even all 15 quotient-cut rows.
This diagnostic records the stronger failure of fixed 26-row supports over
ordinary samples.  Its output is structural evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import linprog

import analyze_n6_parity_triple_slice_subsystems as common
import analyze_n6_parity_triple_quotient_cut_tangent as quotient


MIDDLE_INDICES = tuple(
    index for index, label in enumerate(common.LABELS)
    if label[2] in (2, 3)
)
ROWS = np.vstack([common.R[list(MIDDLE_INDICES)], quotient.CUT_R])
ROW_LABELS = tuple(
    ("edge",) + common.LABELS[index] for index in MIDDLE_INDICES
) + tuple(
    ("cut", tuple(sorted(coset)))
    for coset in quotient.NONEXCEPTIONAL_COSETS
)


def pulled_back(denominators: np.ndarray) -> np.ndarray:
    matrix = ROWS @ common.tangent_map(denominators.astype(float))
    scales = np.maximum(np.linalg.norm(matrix, axis=0), 1e-300)
    return matrix / scales[None, :]


def circuit_vector(
    matrix: np.ndarray, support: tuple[int, ...]
) -> np.ndarray | None:
    restricted = matrix[list(support)]
    _, singular, right = np.linalg.svd(restricted.T, full_matrices=True)
    rank = int(np.sum(singular > 1e-9 * singular[0]))
    if rank != len(support) - 1:
        return None
    vector = right[-1]
    if np.sum(vector) < 0:
        vector = -vector
    return vector / np.sum(vector)


def extreme_supports(
    matrix: np.ndarray, rng: np.random.Generator, trials: int
) -> set[tuple[int, ...]]:
    equalities = np.vstack(
        [matrix.T, np.ones((1, matrix.shape[0]), dtype=float)]
    )
    target = np.zeros(equalities.shape[0], dtype=float)
    target[-1] = 1.0
    answers = set()
    for _ in range(trials):
        result = linprog(
            rng.normal(size=matrix.shape[0]),
            A_eq=equalities,
            b_eq=target,
            bounds=[(0.0, None)] * matrix.shape[0],
            method="highs-ds",
        )
        if not result.success:
            raise RuntimeError(result.message)
        support = tuple(
            int(index)
            for index in np.flatnonzero(np.array(result.x) > 1e-8)
        )
        if len(support) == 26:
            answers.add(support)
    return answers


def sample_denominators_wide(
    rng: np.random.Generator, positive_heads: int, log_span: float
) -> np.ndarray:
    orientations = [-1] * (common.HEADS - positive_heads) + [1] * positive_heads
    rows = []
    for orientation in orientations:
        slopes = np.exp(rng.uniform(-log_span, log_span, size=common.N))
        slack = float(np.exp(rng.uniform(-log_span, log_span)))
        rows.append(
            np.concatenate([[np.sum(slopes) + slack], orientation * slopes])
        )
    return np.vstack(rows)


def sample_bank(
    rng: np.random.Generator,
    positive_heads: int,
    samples: int,
    log_span: float,
) -> list[np.ndarray]:
    bank = []
    for index in range(samples):
        span = log_span * (0.25 + 0.75 * (index + 1) / samples)
        bank.append(sample_denominators_wide(rng, positive_heads, span))
    return bank


def score_support(
    support: tuple[int, ...], matrices: list[np.ndarray]
) -> tuple[int, float]:
    passed = 0
    minimum = float("inf")
    for matrix in matrices:
        vector = circuit_vector(matrix, support)
        if vector is None:
            break
        current = float(np.min(vector))
        minimum = min(minimum, current)
        if current <= 1e-10:
            break
        passed += 1
    return passed, minimum


def main() -> None:
    global ROWS, ROW_LABELS
    parser = argparse.ArgumentParser()
    parser.add_argument("--bases", type=int, default=16)
    parser.add_argument("--trials", type=int, default=24)
    parser.add_argument("--samples", type=int, default=400)
    parser.add_argument("--log-span", type=float, default=10.0)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--aggregate-q0-q7", action="store_true")
    args = parser.parse_args()

    if args.aggregate_q0_q7:
        ROWS = np.vstack(
            [
                common.R[list(MIDDLE_INDICES)],
                quotient.CUT_R[0] + quotient.CUT_R[7],
            ]
        )
        ROW_LABELS = tuple(
            ("edge",) + common.LABELS[index]
            for index in MIDDLE_INDICES
        ) + (("aggregate_cut", (0, 7)),)
    assert ROWS.shape in ((121, 64), (135, 64))
    rng = np.random.default_rng(args.seed)
    for positive_heads in range(3):
        bank = sample_bank(
            rng, positive_heads, args.samples, args.log_span
        )
        matrices = [pulled_back(denominators) for denominators in bank]
        candidates = set()
        for base in range(args.bases):
            candidates.update(
                extreme_supports(matrices[base], rng, args.trials)
            )
        scored = sorted(
            (
                score_support(support, matrices),
                support,
            )
            for support in candidates
        )
        best_score, best_support = scored[-1]
        print(
            f"positive_heads={positive_heads} candidates={len(candidates)} "
            f"best_passed={best_score[0]}/{len(bank)} "
            f"minimum_weight={best_score[1]}"
        )
        print("  support=", best_support)
        print("  labels=")
        for index in best_support:
            print(f"    {index}: {ROW_LABELS[index]}")


if __name__ == "__main__":
    main()
