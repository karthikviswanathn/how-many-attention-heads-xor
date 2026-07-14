#!/usr/bin/env python3
"""Verify a rank-four relaxed separator for the eight-bit Hamming threshold.

The factorization has exactly the algebraic shape of a cleared two-head score,
but its rank-four affine span contains no positive affine function.  It
therefore demonstrates why rank and inertia alone cannot prove the desired
two-head lower bound.
"""

from itertools import permutations, product


A = (26, 52, -14, 1, -30, -21, -14, 0, -30)
D = (-46, 44, 10, -7, 26, -19, 10, 2, 26)
C = (4, 5, -30, 50, 10, -2, -30, -21, 10)
B = (-26, 1, 26, 46, -14, 0, 26, -19, -14)

POSITIVE_SPAN_OBSTRUCTION_CODES = (7, 12, 91, 109, 180)
POSITIVE_SPAN_OBSTRUCTION_WEIGHTS = (2, 1, 47, 18, 36)
EXPECTED_OBSTRUCTION_ROWS = (
    (65, 1, 29, 47),
    (-3, -27, 64, 6),
    (13, 17, -34, -32),
    (35, 29, 18, 14),
    (-38, -36, 32, 32),
)


def affine(coefficients, point):
    return coefficients[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(coefficients[1:], point)
    )


def determinant_four(matrix):
    value = 0
    for permutation in permutations(range(4)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        term = 1
        for row in range(4):
            term *= matrix[row][permutation[row]]
        value += (-1 if inversions % 2 else 1) * term
    return value


def point_from_code(code):
    return tuple((code >> coordinate) & 1 for coordinate in range(8))


def main():
    minimum_signed_score = None
    b_values = []
    d_values = []
    for point in product((0, 1), repeat=8):
        a = affine(A, point)
        d = affine(D, point)
        c = affine(C, point)
        b = affine(B, point)
        score = a * d + c * b
        distance = sum(point[index] != point[4 + index] for index in range(4))
        expected_sign = 1 if distance >= 2 else -1
        signed_score = expected_sign * score
        assert signed_score > 0
        minimum_signed_score = (
            signed_score
            if minimum_signed_score is None
            else min(minimum_signed_score, signed_score)
        )
        b_values.append(b)
        d_values.append(d)

    assert minimum_signed_score == 264
    assert (min(b_values), max(b_values)) == (-73, 73)
    assert (min(d_values), max(d_values)) == (-72, 72)

    coefficient_columns = tuple(zip(A, D, C, B))
    leading_minor = tuple(tuple(row) for row in coefficient_columns[:4])
    assert determinant_four(leading_minor) == -8007312

    obstruction_rows = tuple(
        tuple(
            affine(coefficients, point_from_code(code))
            for coefficients in (A, D, C, B)
        )
        for code in POSITIVE_SPAN_OBSTRUCTION_CODES
    )
    assert obstruction_rows == EXPECTED_OBSTRUCTION_ROWS
    weighted_sum = tuple(
        sum(
            weight * row[column]
            for weight, row in zip(
                POSITIVE_SPAN_OBSTRUCTION_WEIGHTS, obstruction_rows
            )
        )
        for column in range(4)
    )
    assert weighted_sum == (0, 0, 0, 0)

    print("input bits: 8")
    print("minimum signed rank-four score:", minimum_signed_score)
    print("B value range:", (min(b_values), max(b_values)))
    print("D value range:", (min(d_values), max(d_values)))
    print("rank-four leading minor:", determinant_four(leading_minor))
    print("positive-span obstruction weights:", POSITIVE_SPAN_OBSTRUCTION_WEIGHTS)
    print("certificate: verified")


if __name__ == "__main__":
    main()
