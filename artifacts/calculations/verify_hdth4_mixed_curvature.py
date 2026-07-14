#!/usr/bin/env python3
"""Verify the exact checkerboards used by the HDTH4 curvature proof."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import numpy as np


def bits(text: str) -> np.ndarray:
    return np.array([int(character) for character in text], dtype=int)


E = np.eye(4, dtype=int)
P = [sum(E[:index], start=np.zeros(4, dtype=int)) for index in range(1, 5)]

RECTANGLES = (
    (P[0], P[0], "1000", "0000", "1001", "0001"),
    (P[1], P[1], "1100", "0000", "1100", "0000"),
    (P[2], P[2], "1110", "0000", "1110", "0000"),
    (P[3], P[3], "1111", "0000", "1111", "0000"),
    (P[0], P[2], "1010", "0010", "1110", "0000"),
    (P[1], P[2], "1100", "0000", "1110", "0000"),
    (P[1], P[3], "1101", "0001", "1111", "0000"),
    (P[2], P[3], "1110", "0000", "1111", "0000"),
    (P[0], P[1] - E[2], "1000", "0000", "1100", "0010"),
    (P[0], P[3] - E[1], "1001", "0001", "1011", "0000"),
    (P[0], P[3] - E[2], "1001", "0001", "1101", "0000"),
    (P[3], E[0] + E[1], "1111", "0000", "1101", "0001"),
    (P[3], E[0] + E[2], "1111", "0000", "1011", "0001"),
    (P[3], E[0] + E[3], "1111", "0000", "1011", "0010"),
)


F = Fraction
WITNESS_C = (
    (F(1), F(0), F(51, 100), F(51, 100)),
    (F(0), F(1), F(51, 100), F(51, 100)),
    (F(0), F(0), F(1), F(0)),
    (F(0), F(0), F(0), F(1)),
)
WITNESS_E = (
    (F(1, 100), F(0), F(0), F(0)),
    (F(0), F(1, 100), F(0), F(0)),
    (F(0), F(0), F(-1, 100), F(0)),
    (F(0), F(0), F(0), F(-1, 100)),
)
WITNESS_T = (F(17, 25), F(17, 25), F(-99, 100), F(-99, 100))
WITNESS_LAMBDA = (F(1), F(1), F(-1), F(-1))


def matrix_vector(matrix: tuple[tuple[Fraction, ...], ...], vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum((entry * value for entry, value in zip(row, vector)), start=F(0)) for row in matrix)


def transpose_vector(matrix: tuple[tuple[Fraction, ...], ...], vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(
        sum((matrix[row][column] * vector[row] for row in range(4)), start=F(0))
        for column in range(4)
    )


def verify_shell_moment_counterexample() -> None:
    c_matrix = WITNESS_C
    e_matrix = WITNESS_E
    t_vector = WITNESS_T
    lambda_vector = WITNESS_LAMBDA

    assert all(c_matrix[index][index] == 1 for index in range(4))
    assert all(e_matrix[row][column] == e_matrix[column][row] for row in range(4) for column in range(4))

    symmetric_c = tuple(
        tuple(c_matrix[row][column] + c_matrix[column][row] for column in range(4))
        for row in range(4)
    )
    eigenpairs = (
        ((F(1), F(-1), F(0), F(0)), F(2)),
        ((F(0), F(0), F(1), F(-1)), F(2)),
        ((F(1), F(1), F(-1), F(-1)), F(49, 50)),
        ((F(1), F(1), F(1), F(1)), F(151, 50)),
    )
    for vector, eigenvalue in eigenpairs:
        assert matrix_vector(symmetric_c, vector) == tuple(eigenvalue * entry for entry in vector)
        assert eigenvalue > 0

    expected_rows = (F(4913, 5000), F(4913, 5000), F(9801, 10000), F(9801, 10000))
    expected_pointwise_rows = (F(17, 10), F(17, 10), F(99, 100), F(99, 100))
    for row in range(4):
        for excluded in range(4):
            if excluded == row:
                continue
            contraction = t_vector[row] ** 2
            contraction += (c_matrix[row][excluded] - e_matrix[row][excluded]) ** 2
            contraction += sum(
                (
                    (c_matrix[row][column] + e_matrix[row][column]) ** 2
                    for column in range(4)
                    if column not in (row, excluded)
                ),
                start=F(0),
            )
            assert contraction == expected_rows[row]
            assert contraction < 1

            pointwise_contraction = abs(t_vector[row])
            pointwise_contraction += abs(c_matrix[row][excluded] - e_matrix[row][excluded])
            pointwise_contraction += sum(
                (
                    abs(c_matrix[row][column] + e_matrix[row][column])
                    for column in range(4)
                    if column not in (row, excluded)
                ),
                start=F(0),
            )
            assert pointwise_contraction == expected_pointwise_rows[row]

    assert all(value > 1 for value in expected_pointwise_rows[:2])
    assert all(value < 1 for value in expected_pointwise_rows[2:])

    tau = F(3, 2)
    deltas = (F(1),) * 4
    assert all(0 < delta < tau for delta in deltas)
    assert all(deltas[first] + deltas[second] > tau for first in range(4) for second in range(first + 1, 4))

    a_vector = transpose_vector(c_matrix, lambda_vector)
    b_vector = transpose_vector(e_matrix, lambda_vector)
    assert a_vector == (F(1), F(1), F(1, 50), F(1, 50))
    assert b_vector == (F(1, 100),) * 4
    assert all(entry > 0 for entry in a_vector + b_vector)

    null_value = sum(
        (lambda_vector[row] * e_matrix[row][column] * lambda_vector[column] for row in range(4) for column in range(4)),
        start=F(0),
    )
    assert null_value == 0
    intercept = sum((left * right for left, right in zip(lambda_vector, t_vector)), start=F(0))
    slope_sum = sum(a_vector + b_vector, start=F(0))
    assert intercept == F(167, 50)
    assert slope_sum == F(52, 25)
    assert intercept > slope_sum

    j_diagonal = (F(-25), F(-25), F(25), F(25))
    for index in range(4):
        q_column = tuple(e_matrix[row][index] for row in range(4))
        d_column = tuple(-2 * entry for entry in q_column)
        phi_row = tuple(2 * d_column[column] * j_diagonal[column] for column in range(4))
        assert phi_row == tuple(F(1) if column == index else F(0) for column in range(4))
        delta = -4 * sum(
            (c_matrix[row][index] * j_diagonal[row] * q_column[row] for row in range(4)),
            start=F(0),
        )
        assert delta == 1


def label(left: np.ndarray, right: np.ndarray) -> int:
    return -1 if np.count_nonzero(left != right) <= 1 else 1


def main() -> None:
    for a, b, x0_text, x1_text, y0_text, y1_text in RECTANGLES:
        x0, x1 = bits(x0_text), bits(x1_text)
        y0, y1 = bits(y0_text), bits(y1_text)
        assert np.array_equal(x0 - x1, a)
        assert np.array_equal(y0 - y1, b)
        labels = (
            label(x0, y0),
            label(x0, y1),
            label(x1, y0),
            label(x1, y1),
        )
        assert labels == (-1, 1, 1, -1)

    assert np.array_equal((P[1] - E[2]) + P[2], 2 * P[1])
    assert np.array_equal(sum((P[3] - E[index] for index in (1, 2, 3))), P[0] + 2 * P[3])
    assert np.array_equal(sum((E[0] + E[index] for index in (1, 2, 3))), 2 * P[0] + P[3])

    signed_permutations = 0
    for permutation in product(range(4), repeat=4):
        if len(set(permutation)) != 4:
            continue
        for signs in product((-1, 1), repeat=4):
            matrix = np.zeros((4, 4), dtype=int)
            for row, column in enumerate(permutation):
                matrix[row, column] = signs[row]
            assert np.array_equal(matrix @ matrix.T, np.eye(4, dtype=int))
            signed_permutations += 1
    assert signed_permutations == 384

    verify_shell_moment_counterexample()

    print("checkerboard rectangles:", len(RECTANGLES))
    print("signed coordinate permutations:", signed_permutations)
    print("shell-moment counterexample: verified exactly")
    print("certificate: verified")


if __name__ == "__main__":
    main()
