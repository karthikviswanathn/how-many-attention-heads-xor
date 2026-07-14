#!/usr/bin/env python3
"""Extract exact full-truth-table Farkas circuits at a fixed H4 tuple.

This is a diagnostic for the six-bit parity-triple candidate.  The displayed
mixed-orientation denominators admit a tangent numerator satisfying all 186
one-exception slice coefficient inequalities, but not the 64 evaluation-sign
inequalities.  We enumerate extreme numerical duals and reconstruct any
one-dimensional supports over the integers.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import math

import numpy as np
from scipy.optimize import linprog

import analyze_n6_parity_triple_slice_subsystems as common


MASK = 0x96696BD669B69669

DENOMINATORS = np.array(
    [
        [9762, -4, -3, -7449, -5, -465, -2],
        [17785, -14, -1, -30, -3080, -505, -14153],
        [11288, -6128, -425, -1818, -2430, -226, -4],
        [21823, 2564, 1359, 7, 13588, 3265, 1028],
    ],
    dtype=object,
)

SMALL_DENOMINATORS = np.array(
    [
        [20, -1, -2, -3, -4, -1, -2],
        [22, -2, -1, -4, -3, -2, -1],
        [25, -3, -4, -1, -2, -3, -1],
        [24, 1, 3, 2, 4, 2, 1],
    ],
    dtype=object,
)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def exact_signed_evaluation_matrix(denominators: np.ndarray) -> np.ndarray:
    factors = []
    for denominator in denominators:
        factor = np.zeros(1 << common.N, dtype=object)
        factor[0] = int(denominator[0])
        for coordinate, value in enumerate(denominator[1:]):
            factor[1 << coordinate] = int(value)
        factors.append(factor)

    columns = []
    for omitted in range(common.HEADS):
        product = np.zeros(1 << common.N, dtype=object)
        product[0] = 1
        for head, factor in enumerate(factors):
            if head == omitted:
                continue
            updated = np.zeros(1 << common.N, dtype=object)
            for left in np.flatnonzero(product):
                for right in np.flatnonzero(factor):
                    updated[left ^ right] += int(product[left]) * int(factor[right])
            product = updated
        for affine_mask in (0, 1, 2, 4, 8, 16, 32):
            columns.append(
                np.array(
                    [product[subset ^ affine_mask] for subset in range(1 << common.N)],
                    dtype=object,
                )
            )
    tangent = np.column_stack(columns)
    evaluation = np.array(
        [
            [character(subset, code) for subset in range(1 << common.N)]
            for code in range(1 << common.N)
        ],
        dtype=object,
    )
    labels = np.array(
        [1 if (MASK >> code) & 1 else -1 for code in range(1 << common.N)],
        dtype=object,
    )
    return labels[:, None] * (evaluation @ tangent)


def primitive_integer_vector(vector: list[Fraction]) -> tuple[int, ...]:
    scale = math.lcm(*[value.denominator for value in vector])
    integers = [value.numerator * (scale // value.denominator) for value in vector]
    divisor = math.gcd(*[abs(value) for value in integers])
    assert divisor > 0
    integers = [value // divisor for value in integers]
    if sum(integers) < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def one_dimensional_nullspace(rows: list[list[int]]) -> list[Fraction] | None:
    if not rows:
        return None
    matrix = [[Fraction(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        chosen = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column] != 0
            ),
            None,
        )
        if chosen is None:
            continue
        matrix[pivot_row], matrix[chosen] = matrix[chosen], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                left - multiplier * right
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free_columns = [
        column for column in range(column_count) if column not in pivot_columns
    ]
    if len(free_columns) != 1:
        return None
    free = free_columns[0]
    vector = [Fraction(0) for _ in range(column_count)]
    vector[free] = Fraction(1)
    for row, column in enumerate(pivot_columns):
        vector[column] = -matrix[row][free]
    return vector


def exact_circuit(
    matrix: np.ndarray, support: tuple[int, ...]
) -> tuple[int, ...] | None:
    restricted = [
        [int(matrix[row, column]) for row in support]
        for column in range(matrix.shape[1])
    ]
    vector = one_dimensional_nullspace(restricted)
    if vector is None:
        return None
    weights = primitive_integer_vector(vector)
    if min(weights) <= 0:
        return None
    for column in range(matrix.shape[1]):
        assert sum(
            weight * int(matrix[row, column])
            for row, weight in zip(support, weights)
        ) == 0
    return weights


def extreme_supports(
    matrix: np.ndarray, trials: int, seed: int
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    floating = np.array(matrix, dtype=float)
    column_scale = np.maximum(np.linalg.norm(floating, axis=0), 1.0)
    normalized = floating / column_scale[None, :]
    equalities = np.vstack(
        [normalized.T, np.ones((1, normalized.shape[0]), dtype=float)]
    )
    target = np.zeros(equalities.shape[0], dtype=float)
    target[-1] = 1.0
    rng = np.random.default_rng(seed)
    answers: dict[tuple[int, ...], tuple[int, ...]] = {}
    for _ in range(trials):
        result = linprog(
            rng.normal(size=normalized.shape[0]),
            A_eq=equalities,
            b_eq=target,
            bounds=[(0.0, None)] * normalized.shape[0],
            method="highs-ds",
        )
        if not result.success:
            raise RuntimeError(result.message)
        support = tuple(
            int(value) for value in np.flatnonzero(np.array(result.x) > 1e-9)
        )
        if support in answers:
            continue
        weights = exact_circuit(matrix, support)
        if weights is not None:
            answers[support] = weights
    return sorted(answers.items(), key=lambda item: (len(item[0]), item[0]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--small-denominators", action="store_true")
    args = parser.parse_args()

    denominators = SMALL_DENOMINATORS if args.small_denominators else DENOMINATORS
    matrix = exact_signed_evaluation_matrix(denominators)
    assert np.linalg.matrix_rank(np.array(matrix, dtype=float)) == 25
    circuits = extreme_supports(matrix, args.trials, args.seed)
    print(f"signed tangent matrix: {matrix.shape[0]} rows, rank 25")
    print(f"exact positive circuits: {len(circuits)}")
    for support, weights in circuits[:20]:
        print(
            "support={} weights={} labels={}".format(
                support,
                weights,
                tuple(1 if (MASK >> code) & 1 else -1 for code in support),
            )
        )


if __name__ == "__main__":
    main()
