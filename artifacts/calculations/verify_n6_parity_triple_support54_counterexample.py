#!/usr/bin/env python3
"""Verify an exact strict separator for the proposed support54 subsystem.

The target is six-bit parity with vertices 21, 38, and 41 flipped.  The
four denominators below are a small integral perturbation of the symmetric
endpoint-complementarity family.  Their tangent space strictly separates the
target on support54, although the same score fails at six of the ten omitted
vertices.  Thus this is a counterexample to the fixed-support obstruction,
not a four-head representation of the full target.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import math


N = 6
MASK = 0x96696BD669B69669
OMITTED = frozenset((6, 9, 16, 21, 27, 36, 42, 47, 54, 57))
SUPPORT54 = tuple(code for code in range(1 << N) if code not in OMITTED)

DENOMINATORS = (
    (7000, -999, -1001, -1000, -1001, -1000, -1000),
    (8000, -999, -1000, -1001, -1000, -999, -1001),
    (7000, 1000, 1000, 1001, 1000, 1000, 1001),
    (8000, 1000, 1000, 1001, 1001, 1000, 999),
)

# One global coefficient, followed by six numerator-slope coefficients for
# each of the four heads.
TANGENT_COEFFICIENTS = (
    -4,
    17404471, 1964103, 2135496, 27504630, -74626339, 17563083,
    -22500772, 0, -271622, -37132307, 100000000, -22735419,
    -17259383, -1682841, -1884670, -26896563, 73082942, -17481914,
    22365675, -297405, 0, 36445738, -98196941, 22650461,
)

EXPECTED_RANGES = ((999, 13001), (2000, 14000), (998, 13002), (1999, 14001))
EXPECTED_FAILURES = (6, 16, 21, 42, 47, 57)
EXPECTED_SUPPORT_MARGIN = 53028365575824
REPAIR_VERTEX = 16
REPAIR_CIRCUIT_SUPPORT = (
    0, 1, 2, 4, 5, 8, 10, 15, 17, 20, 22, 23, 25,
    31, 32, 34, 35, 44, 55, 58, 59, 60, 61, 62, 63, 16,
)


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


def cleared_row(code: int) -> tuple[int, ...]:
    values = denominator_values(code)
    product = math.prod(values)
    sign = target_sign(code)
    return tuple(
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


def signed_score(code: int) -> int:
    return sum(
        row_value * coefficient
        for row_value, coefficient in zip(
            cleared_row(code), TANGENT_COEFFICIENTS
        )
    )


def primitive_repair_weights() -> tuple[int, ...]:
    """Return the exact primitive positive dependence on the 26 rows."""
    matrix = [
        [Fraction(cleared_row(code)[column]) for code in REPAIR_CIRCUIT_SUPPORT]
        for column in range(25)
    ]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        chosen = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if chosen is None:
            continue
        matrix[pivot_row], matrix[chosen] = matrix[chosen], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                left - multiplier * right
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1

    free_columns = tuple(
        column for column in range(column_count) if column not in pivot_columns
    )
    assert len(free_columns) == 1
    free = free_columns[0]
    rational = [Fraction(0) for _ in range(column_count)]
    rational[free] = Fraction(1)
    for row, column in enumerate(pivot_columns):
        rational[column] = -matrix[row][free]

    scale = math.lcm(*(value.denominator for value in rational))
    weights = [
        value.numerator * (scale // value.denominator) for value in rational
    ]
    divisor = math.gcd(*(abs(value) for value in weights))
    weights = [value // divisor for value in weights]
    if weights[0] < 0:
        weights = [-value for value in weights]
    return tuple(weights)


def verify() -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    assert len(TANGENT_COEFFICIENTS) == 25
    for head, denominator in enumerate(DENOMINATORS):
        orientation = -1 if head < 2 else 1
        assert all(
            orientation * coefficient > 0 for coefficient in denominator[1:]
        )

    ranges = tuple(
        (
            min(denominator_values(code)[head] for code in range(1 << N)),
            max(denominator_values(code)[head] for code in range(1 << N)),
        )
        for head in range(4)
    )
    assert ranges == EXPECTED_RANGES

    support_values = tuple(signed_score(code) for code in SUPPORT54)
    support_margin = min(support_values)
    assert support_margin == EXPECTED_SUPPORT_MARGIN
    assert support_margin > 0

    failures = tuple(
        code for code in range(1 << N) if signed_score(code) <= 0
    )
    assert failures == EXPECTED_FAILURES
    assert set(failures) < OMITTED

    assert REPAIR_VERTEX in OMITTED
    assert set(REPAIR_CIRCUIT_SUPPORT) <= set(SUPPORT54) | {REPAIR_VERTEX}
    repair_weights = primitive_repair_weights()
    assert len(repair_weights) == len(REPAIR_CIRCUIT_SUPPORT) == 26
    assert min(repair_weights) > 0
    for column in range(25):
        assert sum(
            weight * cleared_row(code)[column]
            for code, weight in zip(REPAIR_CIRCUIT_SUPPORT, repair_weights)
        ) == 0
    return support_margin, failures, repair_weights


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-repair-weights", action="store_true")
    arguments = parser.parse_args()
    support_margin, failures, repair_weights = verify()
    print(f"denominator ranges: {EXPECTED_RANGES}")
    print(f"minimum signed support54 score: {support_margin}")
    print(f"full-table failure codes: {failures}")
    print(f"support55 repair circuit: {REPAIR_CIRCUIT_SUPPORT}")
    print(
        "support55 repair weight digits: "
        f"{max(len(str(value)) for value in repair_weights)}"
    )
    if arguments.print_repair_weights:
        print(f"support55 repair weights: {repair_weights}")
    print("verified strict support54 counterexample")


if __name__ == "__main__":
    main()
