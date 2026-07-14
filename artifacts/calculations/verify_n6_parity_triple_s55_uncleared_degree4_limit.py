#!/usr/bin/env python3
"""Verify an exact failure of the S55 uncleared degree-four ansatz.

Let S55 be support54 together with code 47.  The proposed ansatz asks for a
strictly positive degree-at-most-four value vector y satisfying the uncleared
tangent equations W.T y = 0.  Degree at most four adds the single relation
R.T y = 0, where R is parity times the omitted-hyperplane form.

This file verifies an exact strict separator for the augmented rows [W, R].
It disproves this ansatz, but it does not separate the ordinary repaired
Gordan cone and does not give a four-head realization of the target.
"""

from __future__ import annotations

import math


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
OMITTED = frozenset((6, 9, 16, 21, 27, 36, 42, 47, 54, 57))
SUPPORT55 = tuple(
    sorted((set(range(1 << N)) - set(OMITTED)) | {47})
)
HYPERPLANE_NORMAL = (2, 1, -2, -3, -1, 1)

# Each row is the sign-coordinate affine denominator
# B_h(z) = row[0] + sum_i row[i + 1] z_i.
DENOMINATORS = (
    (10000, -533, -6866, -155, -454, -239, -955),
    (10000, -213, -4005, -3706, -299, -1322, -290),
    (9999, -783, -1196, -1359, -517, -862, -1107),
    (9999, -1540, -108, -2040, -1623, -889, -3741),
)

# One global tangent coefficient, six numerator-slope coefficients per head,
# and one final coefficient multiplying the degree-four relation R.
AUGMENTED_COEFFICIENTS = (
    676232,
    22438139, -5813574063, -1434011511, -97943353, -53959409, -283505930,
    -72894416, -262051774, -171916900, -242913606, -535526130, -1362791895,
    112519085, 755398088, 662838623, 329628783, 496579781, 1138945474,
    1385506287, 10000000000, 2343529441, 1501385062, 837077587, 3658910650,
    774,
)

EXPECTED_RANGES = ((798, 19202), (165, 19835), (4175, 15823), (58, 19940))
EXPECTED_MARGIN = 557595572110905986
EXPECTED_MINIMIZER = 31
EXPECTED_CODE16_SCORE = -172843742437269688320


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


def relation_weight(code: int) -> int:
    linear = sum(
        coefficient * character(1 << coordinate, code)
        for coordinate, coefficient in enumerate(HYPERPLANE_NORMAL)
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
    return tangent + (relation_weight(code) * product,)


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
    assert len(SUPPORT55) == 55
    assert len(AUGMENTED_COEFFICIENTS) == 26
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
        for code in SUPPORT55
    ]
    assert len(monomials4) == 57
    assert modular_rank(evaluation) == 54
    relation = tuple(relation_weight(code) for code in SUPPORT55)
    assert all(
        sum(
            relation[row] * evaluation[row][column]
            for row in range(len(SUPPORT55))
        )
        == 0
        for column in range(len(monomials4))
    )

    scores = tuple(augmented_score(code) for code in SUPPORT55)
    margin = min(scores)
    minimizer = SUPPORT55[scores.index(margin)]
    assert margin == EXPECTED_MARGIN
    assert minimizer == EXPECTED_MINIMIZER
    assert margin > 0
    assert augmented_score(16) == EXPECTED_CODE16_SCORE < 0
    return margin, minimizer


def main() -> None:
    margin, minimizer = verify()
    print(f"denominator ranges: {EXPECTED_RANGES}")
    print("S55 degree-four evaluation rank: 54 of 55")
    print(f"minimum augmented score: {margin} at code {minimizer}")
    print(f"added antipode code 16 score: {EXPECTED_CODE16_SCORE}")
    print("verified S55 uncleared degree-four ansatz counterexample")


if __name__ == "__main__":
    main()
