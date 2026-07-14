#!/usr/bin/env python3
"""Verify an exact failure of the S56 uncleared degree-four ansatz.

The antipodal support S56 is support54 together with codes 16 and 47.  Its
degree-at-most-four value space has two relations, parity times M1 and parity
times M2.  This file gives positive affine denominators and an exact strict
separator for the uncleared tangent rows augmented by those two relations.

The certificate disproves the degree-four multiplier ansatz.  It does not
separate the ordinary S56 Gordan cone.
"""

from __future__ import annotations

import math


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
OMITTED = frozenset((6, 9, 16, 21, 27, 36, 42, 47, 54, 57))
SUPPORT56 = tuple(
    sorted((set(range(1 << N)) - set(OMITTED)) | {16, 47})
)
M1 = (0, 0, 1, 1, 0, 0)
M2 = (2, 1, 1, 0, -1, 1)

DENOMINATORS = (
    (10000, -415, -7490, -195, -294, -212, -931),
    (10000, -142, -4439, -2885, -91, -1908, -431),
    (9999, -1012, -1470, -615, -930, -543, -1667),
    (10001, -1212, -97, -2114, -844, -2985, -2724),
)

# One global tangent coefficient, six numerator-slope coefficients per head,
# then coefficients for parity times M1 and parity times M2.
AUGMENTED_COEFFICIENTS = (
    492430,
    151005964, -2468445949, -267239872, 190751123, -1120130567, 174134515,
    -243257599, -173262283, -1080324459, -203808427, -75421517, -708958739,
    -258797386, -4026682960, 564581502, -243992189, 506680213, -116993144,
    1096689853, 10000000000, 2187402909, 722992943, 3058022493, 2566025686,
    5363, 3733,
)

EXPECTED_RANGES = ((463, 19537), (104, 19896), (3762, 16236), (25, 19977))
EXPECTED_MARGIN = 101664750504266640
EXPECTED_MINIMIZER = 39


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def denominator_values(code: int) -> tuple[int, ...]:
    return tuple(
        denominator[0]
        + sum(
            denominator[coordinate + 1]
            * character(1 << coordinate, code)
            for coordinate in range(N)
        )
        for denominator in DENOMINATORS
    )


def relation_weight(normal: tuple[int, ...], code: int) -> int:
    linear = sum(
        coefficient * character(1 << coordinate, code)
        for coordinate, coefficient in enumerate(normal)
    )
    return character(FULL, code) * linear


def augmented_cleared_row(code: int) -> tuple[int, ...]:
    values = denominator_values(code)
    product = math.prod(values)
    sign = target_sign(code)
    tangent = tuple(
        [sign * product]
        + [
            sign
            * character(1 << coordinate, code)
            * math.prod(
                values[other] for other in range(4) if other != head
            )
            for head in range(4)
            for coordinate in range(N)
        ]
    )
    return tangent + (
        relation_weight(M1, code) * product,
        relation_weight(M2, code) * product,
    )


def augmented_score(code: int) -> int:
    return sum(
        row_value * coefficient
        for row_value, coefficient in zip(
            augmented_cleared_row(code), AUGMENTED_COEFFICIENTS
        )
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


def verify() -> tuple[int, int]:
    assert len(SUPPORT56) == 56
    assert len(AUGMENTED_COEFFICIENTS) == 27
    assert all(
        all(coefficient < 0 for coefficient in row[1:])
        for row in DENOMINATORS
    )
    ranges = tuple(
        (
            min(denominator_values(code)[head] for code in range(1 << N)),
            max(denominator_values(code)[head] for code in range(1 << N)),
        )
        for head in range(4)
    )
    assert ranges == EXPECTED_RANGES

    monomials4 = tuple(
        mask for mask in range(1 << N) if bin(mask).count("1") <= 4
    )
    evaluation = [
        [character(mask, code) for mask in monomials4]
        for code in SUPPORT56
    ]
    assert len(monomials4) == 57
    assert modular_rank(evaluation) == 54
    relations = tuple(
        tuple(relation_weight(normal, code) for code in SUPPORT56)
        for normal in (M1, M2)
    )
    for relation in relations:
        assert all(
            sum(
                relation[row] * evaluation[row][column]
                for row in range(len(SUPPORT56))
            )
            == 0
            for column in range(len(monomials4))
        )
    assert any(
        left * relations[1][0] != right * relations[0][0]
        for left, right in zip(relations[0], relations[1])
    )

    scores = tuple(augmented_score(code) for code in SUPPORT56)
    margin = min(scores)
    minimizer = SUPPORT56[scores.index(margin)]
    assert margin == EXPECTED_MARGIN
    assert minimizer == EXPECTED_MINIMIZER
    assert margin > 0
    return margin, minimizer


def main() -> None:
    margin, minimizer = verify()
    print(f"denominator ranges: {EXPECTED_RANGES}")
    print("S56 degree-four evaluation rank: 54 of 56")
    print(f"minimum augmented score: {margin} at code {minimizer}")
    print("relation coefficients: (5363, 3733)")
    print("verified S56 uncleared degree-four ansatz counterexample")


if __name__ == "__main__":
    main()
