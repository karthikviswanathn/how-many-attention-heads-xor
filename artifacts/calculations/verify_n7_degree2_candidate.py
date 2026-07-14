#!/usr/bin/env python3
"""Verify exact structural data for a refuted seven-bit H2 candidate.

The candidate is recorded exactly, its polynomial threshold degree is proved
to be two, and two useful rank-(2,2) relaxations are verified.  A separate
certificate in ``verify_two_head_candidate_refutations.py`` verifies that the
candidate is in fact representable by two heads.
"""

from __future__ import annotations

import itertools


DIMENSION = 7
TRUTH_MASK = 0x3351C040FAFF01010341CFD5EFFF

# Ordering: constant, seven linear monomials, then x_i x_j in lexicographic
# order over 0 <= i < j < 7.
QUADRATIC_COEFFICIENTS = (
    33,
    0,
    4,
    -8,
    -32,
    4,
    4,
    -4,
    0,
    0,
    64,
    -64,
    -64,
    0,
    64,
    0,
    -8,
    -64,
    -16,
    0,
    -2,
    -32,
    32,
    2,
    0,
    0,
    0,
    -64,
    8,
)

# A positive dependence among signed affine evaluation rows.  This is an
# exact Farkas certificate that no affine threshold represents the table.
LTF_WITNESS_VERTICES = (9, 22, 28, 36, 47, 48, 74, 81, 109)
LTF_WITNESS_WEIGHTS = (3, 5, 3, 3, 4, 2, 1, 4, 5)

# An unrestricted quadratic separator Q = A D + C B.  Its factors do not
# satisfy the positive oriented-affine denominator conditions required for
# two attention heads.
A = (-22, 23, 19, 16, -9, 3, 20, 30)
D = (-21, -7, 11, 19, 9, -30, -27, 18)
C = (-9, -16, 47, 4, 15, 4, -10, -5)
B = (-21, 5, 42, 4, -19, 9, -4, -16)

# The span of the four unrestricted factors contains this positive affine
# form.  The entries are the coefficients of A, D, C, B, respectively.
POSITIVE_SPAN_WEIGHTS = (5483, -4152, 6863, -9073)
POSITIVE_SPAN_FORM = (95332, 0, 0, 0, 188617, 86804, 189426, 200607)

# The still weaker relaxation that asks for only one positive factor also
# represents the table.  ONE_POSITIVE_B has mixed slope signs, so it is not an
# admissible attention denominator.
ONE_POSITIVE_A = (-181, -14, 11, -192, -4, 132, 285, 192)
ONE_POSITIVE_D = (-122, -56, -282, 86, 45, -94, 267, -125)
ONE_POSITIVE_C = (-8, -99, 63, -17, -24, -215, -29, 115)
ONE_POSITIVE_B = (42, 27, 48, 83, -41, 0, 0, 0)


def vertices() -> list[tuple[int, ...]]:
    return [
        tuple((code >> coordinate) & 1 for coordinate in range(DIMENSION))
        for code in range(1 << DIMENSION)
    ]


def label(code: int) -> int:
    return 1 if (TRUTH_MASK >> code) & 1 else -1


def affine_value(coefficients: tuple[int, ...], point: tuple[int, ...]) -> int:
    return coefficients[0] + sum(
        coefficient * coordinate
        for coefficient, coordinate in zip(coefficients[1:], point)
    )


def quadratic_value(point: tuple[int, ...]) -> int:
    value = QUADRATIC_COEFFICIENTS[0]
    value += sum(
        QUADRATIC_COEFFICIENTS[1 + index] * point[index]
        for index in range(DIMENSION)
    )
    coefficient_index = 1 + DIMENSION
    for first, second in itertools.combinations(range(DIMENSION), 2):
        value += (
            QUADRATIC_COEFFICIENTS[coefficient_index]
            * point[first]
            * point[second]
        )
        coefficient_index += 1
    return value


def main() -> None:
    cube = vertices()

    quadratic_signed_values = [
        label(code) * quadratic_value(point)
        for code, point in enumerate(cube)
    ]
    assert min(quadratic_signed_values) == 1

    signed_affine_moment = [0] * (DIMENSION + 1)
    for code, weight in zip(LTF_WITNESS_VERTICES, LTF_WITNESS_WEIGHTS):
        row = (1, *cube[code])
        for index, entry in enumerate(row):
            signed_affine_moment[index] += weight * label(code) * entry
    assert signed_affine_moment == [0] * (DIMENSION + 1)

    rank_four_signed_values = []
    for code, point in enumerate(cube):
        score = (
            affine_value(A, point) * affine_value(D, point)
            + affine_value(C, point) * affine_value(B, point)
        )
        rank_four_signed_values.append(label(code) * score)
    assert min(rank_four_signed_values) == 54

    factors = (A, D, C, B)
    reconstructed_positive_form = tuple(
        sum(
            weight * factor[coefficient]
            for weight, factor in zip(POSITIVE_SPAN_WEIGHTS, factors)
        )
        for coefficient in range(DIMENSION + 1)
    )
    assert reconstructed_positive_form == POSITIVE_SPAN_FORM
    positive_span_values = [
        affine_value(POSITIVE_SPAN_FORM, point) for point in cube
    ]
    assert min(positive_span_values) == 95332

    one_positive_values = [
        affine_value(ONE_POSITIVE_B, point) for point in cube
    ]
    assert min(one_positive_values) == 1
    assert max(one_positive_values) == 200
    one_positive_signed_values = []
    for code, point in enumerate(cube):
        score = (
            affine_value(ONE_POSITIVE_A, point)
            * affine_value(ONE_POSITIVE_D, point)
            + affine_value(ONE_POSITIVE_C, point)
            * affine_value(ONE_POSITIVE_B, point)
        )
        one_positive_signed_values.append(label(code) * score)
    assert min(one_positive_signed_values) == 1212

    print(f"dimension: {DIMENSION}")
    print(f"truth mask: {TRUTH_MASK:#034x}")
    print(f"minimum signed quadratic value: {min(quadratic_signed_values)}")
    print(f"LTF Farkas support size: {len(LTF_WITNESS_VERTICES)}")
    print(f"minimum signed unrestricted rank-four score: {min(rank_four_signed_values)}")
    print(f"positive span-form range: ({min(positive_span_values)}, {max(positive_span_values)})")
    print(f"one-positive factor range: ({min(one_positive_values)}, {max(one_positive_values)})")
    print(f"minimum signed one-positive score: {min(one_positive_signed_values)}")
    print("certificate: verified")


if __name__ == "__main__":
    main()
