#!/usr/bin/env python3
"""Verify an exact interior complementarity stratum on support54.

Let S be the sum of the six sign coordinates and choose the four positive
affine denominators

    A - S, C - S, A + S, C + S

with 6 < A < C.  A cleared tangent polynomial is nonnegative on support54,
positive only at the two antipodal endpoints, and zero on the other 52
vertices.  Four of those zero rows carry an equal-weight positive Gordan
circuit.  Thus the weak separator and its complementary circuit coexist.

The verifier uses A=7 and C=8, and checks every assertion with integers.
The displayed factorization is valid symbolically for arbitrary A and C.
"""

from __future__ import annotations

import math


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
OMITTED = frozenset((6, 9, 16, 21, 27, 36, 42, 47, 54, 57))
SUPPORT54 = tuple(code for code in range(1 << N) if code not in OMITTED)

A = 7
C = 8
SHAPE = (1, 1, 1, 1, -3, 1)
COMPLEMENTARY_SUPPORT = (35, 38, 41, 44)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def coordinate_sum(code: int) -> int:
    return sum(character(1 << coordinate, code) for coordinate in range(N))


def transverse_form(code: int) -> int:
    return sum(
        coefficient * character(1 << coordinate, code)
        for coordinate, coefficient in enumerate(SHAPE)
    )


def denominator_values(code: int) -> tuple[int, ...]:
    coordinate_total = coordinate_sum(code)
    return (
        A - coordinate_total,
        C - coordinate_total,
        A + coordinate_total,
        C + coordinate_total,
    )


def cleared_row(code: int) -> tuple[int, ...]:
    values = denominator_values(code)
    product = math.prod(values)
    sign = target_sign(code)
    return tuple(
        [sign * product]
        + [
            sign
            * character(1 << coordinate, code)
            * (product // values[head])
            for head in range(4)
            for coordinate in range(N)
        ]
    )


def tangent_vector() -> tuple[int, ...]:
    first = A * A - 4
    second = C * C - 4
    blocks = (
        tuple(first * value for value in SHAPE),
        tuple(-second * value for value in SHAPE),
        tuple(-first * value for value in SHAPE),
        tuple(second * value for value in SHAPE),
    )
    return tuple([0] + [value for block in blocks for value in block])


def factored_polynomial(code: int) -> int:
    coordinate_total = coordinate_sum(code)
    return (
        2
        * (C * C - A * A)
        * transverse_form(code)
        * coordinate_total
        * (coordinate_total * coordinate_total - 4)
    )


def modular_rank(matrix: list[list[int]], prime: int = 1000003) -> int:
    work = [[value % prime for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if row_count else 0
    pivot_row = 0
    for column in range(column_count):
        chosen = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if chosen is None:
            continue
        work[pivot_row], work[chosen] = work[chosen], work[pivot_row]
        inverse = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [
            value * inverse % prime for value in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                (left - multiplier * right) % prime
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def verify() -> tuple[tuple[int, ...], tuple[int, ...]]:
    assert A > 6 and C > A
    assert all(
        min(denominator_values(code)) > 0 for code in range(1 << N)
    )
    rows = {code: cleared_row(code) for code in SUPPORT54}
    vector = tangent_vector()
    evaluations = {
        code: sum(left * right for left, right in zip(rows[code], vector))
        for code in SUPPORT54
    }
    for code in SUPPORT54:
        assert evaluations[code] == target_sign(code) * factored_polynomial(code)
        assert evaluations[code] >= 0
    positive_support = tuple(
        code for code in SUPPORT54 if evaluations[code] > 0
    )
    zero_support = tuple(
        code for code in SUPPORT54 if evaluations[code] == 0
    )
    assert positive_support == (0, 63)
    assert len(zero_support) == 52
    assert evaluations[0] == evaluations[63] == 11520

    full_matrix = [list(rows[code]) for code in SUPPORT54]
    zero_matrix = [list(rows[code]) for code in zero_support]
    assert modular_rank(full_matrix) == 25
    assert modular_rank(zero_matrix) == 24

    assert set(COMPLEMENTARY_SUPPORT) <= set(zero_support)
    for column in range(25):
        assert sum(rows[code][column] for code in COMPLEMENTARY_SUPPORT) == 0
    return positive_support, zero_support


def main() -> None:
    positive_support, zero_support = verify()
    print("strictly positive denominators: verified on all 64 vertices")
    print("cleared tangent rank: 25")
    print(f"weak separator positive support: {positive_support}")
    print(f"weak separator zero support size: {len(zero_support)}, rank 24")
    print(f"equal-weight complementary circuit: {COMPLEMENTARY_SUPPORT}")
    print("verified endpoint-ray complementarity stratum")


if __name__ == "__main__":
    main()
