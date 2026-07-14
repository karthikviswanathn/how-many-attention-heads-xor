#!/usr/bin/env python3
"""Diagnose Fourier-level subsystems for the six parity-triple slices.

The target mask is parity with vertices 21, 38, and 41 flipped.  Each
coordinate has one five-bit slice containing exactly one exception.  A
quartic sign representative therefore obeys 31 strict coefficient signs on
each chosen slice.  For sampled admissible four-head denominators, this file
tests which Fourier levels already have a nonnegative Gordan multiplier.

All output is diagnostic.  Sampling is not a universal certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import linprog


N = 6
HEADS = 4
SUBSETS = 1 << N
EXCEPTION_BY_COORDINATE = (38, 38, 41, 41, 21, 21)
SLICE_SIGNS = (1, -1, 1, -1, -1, 1)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def xor_convolution(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    answer = np.zeros(SUBSETS, dtype=float)
    for left in np.flatnonzero(first):
        for right in np.flatnonzero(second):
            answer[left ^ right] += first[left] * second[right]
    return answer


def affine_coefficients(row: np.ndarray) -> np.ndarray:
    answer = np.zeros(SUBSETS, dtype=float)
    answer[0] = row[0]
    for coordinate, value in enumerate(row[1:]):
        answer[1 << coordinate] = value
    return answer


def tangent_map(denominators: np.ndarray) -> np.ndarray:
    factors = [affine_coefficients(row) for row in denominators]
    columns = []
    for omitted in range(HEADS):
        product = np.zeros(SUBSETS, dtype=float)
        product[0] = 1.0
        for head, factor in enumerate(factors):
            if head != omitted:
                product = xor_convolution(product, factor)
        for affine_mask in (0, 1, 2, 4, 8, 16, 32):
            columns.append(product[np.arange(SUBSETS) ^ affine_mask])
    return np.column_stack(columns)


def slice_rows() -> tuple[np.ndarray, tuple[tuple[int, int, int], ...]]:
    rows = []
    labels = []
    for coordinate in range(N):
        for subset in range(SUBSETS):
            if subset & (1 << coordinate):
                continue
            degree = bin(subset).count("1")
            if degree > N - 2:
                continue
            multiplier = character(
                subset, EXCEPTION_BY_COORDINATE[coordinate]
            )
            row = np.zeros(SUBSETS, dtype=float)
            row[subset] = multiplier
            union = subset | (1 << coordinate)
            if degree + 1 <= HEADS:
                row[union] = multiplier * SLICE_SIGNS[coordinate]
            rows.append(row)
            labels.append((coordinate, subset, degree))
    assert len(rows) == 186
    return np.vstack(rows), tuple(labels)


R, LABELS = slice_rows()


def eliminated_order_rows() -> tuple[
    np.ndarray, tuple[tuple[str, int, int, int], ...]
]:
    """Eliminate the shared odd coefficient from levels one and three.

    Each level-one family with fixed singleton and each level-three family
    with fixed cubic coefficient consists of upper and lower bounds on that
    shared odd coefficient.  Pairing every lower bound with every upper bound
    leaves strict order inequalities involving only degrees two and four.
    """
    rows = []
    labels = []

    for singleton in range(N):
        entries = []
        for coordinate in range(N):
            if coordinate == singleton:
                continue
            subset = 1 << singleton
            sign = character(
                subset, EXCEPTION_BY_COORDINATE[coordinate]
            )
            entries.append((coordinate, sign))
        for plus_coordinate, plus_sign in entries:
            if plus_sign <= 0:
                continue
            for minus_coordinate, minus_sign in entries:
                if minus_sign >= 0:
                    continue
                row = np.zeros(SUBSETS, dtype=float)
                plus_pair = (1 << singleton) | (1 << plus_coordinate)
                minus_pair = (1 << singleton) | (1 << minus_coordinate)
                row[plus_pair] = SLICE_SIGNS[plus_coordinate]
                row[minus_pair] = -SLICE_SIGNS[minus_coordinate]
                rows.append(row)
                labels.append(
                    ("low", singleton, plus_coordinate, minus_coordinate)
                )

    full = SUBSETS - 1
    for complementary_triple in itertools.combinations(range(N), 3):
        cubic = full
        for coordinate in complementary_triple:
            cubic ^= 1 << coordinate
        entries = []
        for coordinate in complementary_triple:
            sign = character(
                cubic, EXCEPTION_BY_COORDINATE[coordinate]
            )
            entries.append((coordinate, sign))
        for plus_coordinate, plus_sign in entries:
            if plus_sign <= 0:
                continue
            for minus_coordinate, minus_sign in entries:
                if minus_sign >= 0:
                    continue
                row = np.zeros(SUBSETS, dtype=float)
                plus_quartic = cubic | (1 << plus_coordinate)
                minus_quartic = cubic | (1 << minus_coordinate)
                row[plus_quartic] = SLICE_SIGNS[plus_coordinate]
                row[minus_quartic] = -SLICE_SIGNS[minus_coordinate]
                rows.append(row)
                labels.append(
                    (
                        "high",
                        sum(1 << value for value in complementary_triple),
                        plus_coordinate,
                        minus_coordinate,
                    )
                )
    return np.vstack(rows), tuple(labels)


ORDER_R, ORDER_LABELS = eliminated_order_rows()


def sample_denominators(
    rng: np.random.Generator, positive_heads: int
) -> np.ndarray:
    orientations = [-1] * (HEADS - positive_heads) + [1] * positive_heads
    rows = []
    for orientation in orientations:
        slopes = np.exp(rng.uniform(-2.0, 2.0, size=N))
        slack = float(np.exp(rng.uniform(-2.0, 2.0)))
        rows.append(
            np.concatenate([[np.sum(slopes) + slack], orientation * slopes])
        )
    return np.vstack(rows)


def has_gordan_multiplier(matrix: np.ndarray) -> tuple[bool, int]:
    equalities = np.vstack(
        [matrix.T, np.ones((1, matrix.shape[0]), dtype=float)]
    )
    target = np.zeros(equalities.shape[0], dtype=float)
    target[-1] = 1.0
    result = linprog(
        np.zeros(matrix.shape[0]),
        A_eq=equalities,
        b_eq=target,
        bounds=[(0.0, None)] * matrix.shape[0],
        method="highs-ds",
    )
    if not result.success:
        return False, 0
    support = int(np.sum(np.array(result.x) > 1e-8))
    return True, support


def strict_gordan_margin(matrix: np.ndarray) -> float:
    """Return the largest common lower bound after normalizing sum(y)=1."""
    rows = matrix.shape[0]
    objective = np.zeros(rows + 1, dtype=float)
    objective[-1] = -1.0
    equalities = np.zeros((matrix.shape[1] + 1, rows + 1), dtype=float)
    equalities[:-1, :rows] = matrix.T
    equalities[-1, :rows] = 1.0
    target = np.zeros(equalities.shape[0], dtype=float)
    target[-1] = 1.0
    inequalities = np.zeros((rows, rows + 1), dtype=float)
    inequalities[:, :rows] = -np.eye(rows)
    inequalities[:, -1] = 1.0
    result = linprog(
        objective,
        A_ub=inequalities,
        b_ub=np.zeros(rows),
        A_eq=equalities,
        b_eq=target,
        bounds=[(None, None)] * rows + [(None, None)],
        method="highs-ds",
    )
    if not result.success:
        return float("-inf")
    return float(result.x[-1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260714)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    level_sets = [
        levels
        for size in range(1, N)
        for levels in itertools.combinations(range(N - 1), size)
    ]
    for positive_heads in range(HEADS + 1):
        counts = {levels: 0 for levels in level_sets}
        supports = {levels: [] for levels in level_sets}
        for _ in range(args.samples):
            denominators = sample_denominators(rng, positive_heads)
            pulled_back = R @ tangent_map(denominators)
            for levels in level_sets:
                indices = [
                    index
                    for index, label in enumerate(LABELS)
                    if label[2] in levels
                ]
                found, support = has_gordan_multiplier(
                    pulled_back[indices]
                )
                counts[levels] += int(found)
                if found:
                    supports[levels].append(support)
        universal = [
            (
                levels,
                len(
                    [label for label in LABELS if label[2] in levels]
                ),
                min(supports[levels]),
                max(supports[levels]),
            )
            for levels in level_sets
            if counts[levels] == args.samples
        ]
        print(f"positive_heads={positive_heads}")
        for record in sorted(universal, key=lambda item: (item[1], item[0])):
            print(
                "  levels={} rows={} support_range={}..{}".format(
                    record[0], record[1], record[2], record[3]
                )
            )


if __name__ == "__main__":
    main()
