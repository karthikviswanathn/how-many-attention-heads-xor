#!/usr/bin/env python3
"""Verify an exact limitation of the six-bit slice-coefficient cone.

The displayed admissible four-denominator tangent polynomial satisfies every
one-exception slice coefficient inequality, but it does not sign-represent the
six-bit parity-triple target.  Thus those slice inequalities alone cannot give
a universal four-head obstruction.
"""

from __future__ import annotations

import itertools


N = 6
VERTICES = 1 << N
EXCEPTIONAL = (21, 38, 41)

# Fourier affine rows.  Entry zero is the constant coefficient, followed by
# the singleton coefficients in coordinate order.
DENOMINATORS = (
    (21, -1, -1, -15, -1, -1, -1),
    (40, -1, -1, -1, -6, -1, -29),
    (25, -12, -1, -4, -5, -1, -1),
    (46, 5, 3, 1, 27, 7, 2),
)

# Four Fourier affine numerator rows, flattened head by head.
NUMERATORS = (
    -100,
    -54,
    4,
    60,
    -71,
    15,
    -99,
    100,
    -72,
    23,
    -46,
    100,
    -66,
    68,
    -18,
    100,
    -15,
    -100,
    70,
    29,
    -5,
    -100,
    -18,
    -3,
    -21,
    -51,
    1,
    -3,
)

EXPECTED_DOMINANCE_SLACKS = (1, 1, 1, 1)
EXPECTED_ALL_SLICE_MINIMUM = 1_001
EXPECTED_MIDDLE_SLICE_MINIMUM = 1_327
EXPECTED_FAILURE_COUNT = 29
EXPECTED_WORST_SIGNED_VALUE = -23_919_252
EXPECTED_WORST_VERTEX = 52


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    parity = character(VERTICES - 1, code)
    return -parity if code in EXCEPTIONAL else parity


def affine_coefficients(row: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * VERTICES
    answer[0] = row[0]
    for coordinate, value in enumerate(row[1:]):
        answer[1 << coordinate] = value
    return tuple(answer)


def xor_convolution(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[int, ...]:
    answer = [0] * VERTICES
    for left, left_value in enumerate(first):
        if left_value == 0:
            continue
        for right, right_value in enumerate(second):
            if right_value != 0:
                answer[left ^ right] += left_value * right_value
    return tuple(answer)


def tangent_coefficients() -> tuple[int, ...]:
    factors = tuple(affine_coefficients(row) for row in DENOMINATORS)
    numerators = tuple(
        affine_coefficients(NUMERATORS[7 * head : 7 * head + 7])
        for head in range(4)
    )
    answer = [0] * VERTICES
    for omitted in range(4):
        product = (1,) + (0,) * (VERTICES - 1)
        for head, factor in enumerate(factors):
            if head != omitted:
                product = xor_convolution(product, factor)
        term = xor_convolution(numerators[omitted], product)
        answer = [left + right for left, right in zip(answer, term)]
    return tuple(answer)


def unique_slice_data() -> tuple[tuple[int, int], ...]:
    answer = []
    for coordinate in range(N):
        for bit in (0, 1):
            points = tuple(
                code
                for code in EXCEPTIONAL
                if ((code >> coordinate) & 1) == bit
            )
            if len(points) == 1:
                answer.append((points[0], 1 - 2 * bit))
                break
    return tuple(answer)


def slice_inequality_values(
    coefficients: tuple[int, ...]
) -> tuple[tuple[int, int, int, int], ...]:
    answer = []
    for coordinate, (exceptional, slice_sign) in enumerate(unique_slice_data()):
        remaining = tuple(index for index in range(N) if index != coordinate)
        for degree in range(5):
            for subset_tuple in itertools.combinations(remaining, degree):
                subset = sum(1 << index for index in subset_tuple)
                union = subset | (1 << coordinate)
                value = character(subset, exceptional) * (
                    coefficients[subset] + slice_sign * coefficients[union]
                )
                answer.append((value, coordinate, subset, degree))
    return tuple(answer)


def polynomial_value(coefficients: tuple[int, ...], code: int) -> int:
    return sum(
        coefficient * character(mask, code)
        for mask, coefficient in enumerate(coefficients)
    )


def verify() -> None:
    slacks = tuple(
        row[0] - sum(abs(value) for value in row[1:])
        for row in DENOMINATORS
    )
    assert slacks == EXPECTED_DOMINANCE_SLACKS
    assert all(slack > 0 for slack in slacks)
    assert all(value < 0 for row in DENOMINATORS[:3] for value in row[1:])
    assert all(value > 0 for value in DENOMINATORS[3][1:])

    assert unique_slice_data() == (
        (38, 1),
        (38, -1),
        (41, 1),
        (41, -1),
        (21, -1),
        (21, 1),
    )

    coefficients = tangent_coefficients()
    assert all(
        coefficient == 0
        for mask, coefficient in enumerate(coefficients)
        if bin(mask).count("1") > 4
    )

    slice_values = slice_inequality_values(coefficients)
    assert len(slice_values) == 186
    assert min(value for value, _, _, _ in slice_values) == (
        EXPECTED_ALL_SLICE_MINIMUM
    )
    middle_values = tuple(
        value for value, _, _, degree in slice_values if degree in (2, 3)
    )
    assert len(middle_values) == 120
    assert min(middle_values) == EXPECTED_MIDDLE_SLICE_MINIMUM

    signed_values = tuple(
        target_sign(code) * polynomial_value(coefficients, code)
        for code in range(VERTICES)
    )
    failures = tuple(
        code for code, value in enumerate(signed_values) if value <= 0
    )
    assert len(failures) == EXPECTED_FAILURE_COUNT
    assert min(signed_values) == EXPECTED_WORST_SIGNED_VALUE
    assert signed_values[EXPECTED_WORST_VERTEX] == EXPECTED_WORST_SIGNED_VALUE


def main() -> None:
    verify()
    print(f"dominance slacks: {EXPECTED_DOMINANCE_SLACKS}")
    print("all one-exception slice rows: 186")
    print(f"minimum slice row: {EXPECTED_ALL_SLICE_MINIMUM}")
    print("middle-level slice rows: 120")
    print(f"minimum middle-level row: {EXPECTED_MIDDLE_SLICE_MINIMUM}")
    print(f"failed target vertices: {EXPECTED_FAILURE_COUNT}")
    print(
        "worst signed target value: "
        f"{EXPECTED_WORST_SIGNED_VALUE} at vertex {EXPECTED_WORST_VERTEX}"
    )


if __name__ == "__main__":
    main()
