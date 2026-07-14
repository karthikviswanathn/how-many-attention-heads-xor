#!/usr/bin/env python3
"""Verify an exact failure of the S56 cleared degree-four ansatz.

The ansatz asks for a positive degree-at-most-four value vector q in the
kernel of the cleared tangent rows G = s(F, z_i F / B_h).  On the antipodal
support S56, degree at most four imposes two relations.  This file gives an
exact strict separator for G augmented by those relations.
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
    (100, -5, -49, -1, -4, -1, -39),
    (101, -2, -36, -25, -1, -33, -3),
    (100, -7, -6, -2, -7, -7, -30),
    (100, -7, -1, -6, -6, -22, -57),
)

# One global tangent coefficient, six numerator-slope coefficients per head,
# then coefficients for parity times M1 and parity times M2.
AUGMENTED_COEFFICIENTS = (
    5777,
    122716, -2239037, -103031, 292071, -2957531, -1609447,
    -60847, -899092, -1092096, -47421, -588822, -2872907,
    -169197, -7262409, 202449, -239922, 1622945, -285419,
    325227, 10613939, 847057, 193611, 2206967, 6632861,
    -10000000000, 5191960708,
)

EXPECTED_RANGES = ((1, 199), (1, 201), (41, 159), (1, 199))
EXPECTED_MARGIN = 852046508
EXPECTED_MINIMIZER = 51


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


def augmented_row(code: int) -> tuple[int, ...]:
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
        relation_weight(M1, code),
        relation_weight(M2, code),
    )


def augmented_score(code: int) -> int:
    return sum(
        row_value * coefficient
        for row_value, coefficient in zip(
            augmented_row(code), AUGMENTED_COEFFICIENTS
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
    assert len(AUGMENTED_COEFFICIENTS) == 27
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
    assert modular_rank(evaluation) == 54
    for normal in (M1, M2):
        relation = tuple(relation_weight(normal, code) for code in SUPPORT56)
        assert all(
            sum(
                relation[row] * evaluation[row][column]
                for row in range(len(SUPPORT56))
            )
            == 0
            for column in range(len(monomials4))
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
    print("relation coefficients: (-10000000000, 5191960708)")
    print("verified S56 cleared degree-four ansatz counterexample")


if __name__ == "__main__":
    main()
