#!/usr/bin/env python3
"""Verify an exact limitation of the R23 plus quotient-cut cone."""

from __future__ import annotations

import verify_n6_parity_triple_quotient_cut_circuit as cut_bridge
import verify_n6_parity_triple_slice_cone_limit as base


DENOMINATORS = (
    (135562, -131072, -256, -128, -4096, -1, -8),
    (794898, -524288, -8, -2, -8192, -262144, -8),
    (2433, -16, -1, -64, -256, -32, -2048),
    (1328512, -128, -262144, -1048576, -512, -512, -16384),
)
NUMERATORS = (
    -11329030,
    5108461,
    4538,
    24829,
    -46162,
    -6293421,
    -4856,
    100000000,
    -70958010,
    135121,
    -777072,
    261965,
    -4288401,
    264425,
    -234193,
    1551,
    254,
    6225,
    24745,
    3060,
    197204,
    30311522,
    -851731,
    -6352293,
    -24270944,
    -17408,
    227195,
    -455650,
)

EXPECTED_DOMINANCE_SLACKS = (1, 256, 16, 256)
EXPECTED_MIDDLE_MINIMUM = 16_025_004_790_688_768
EXPECTED_CUT_MINIMUM = 5_642_691_207_806_809_016
EXPECTED_ALL_SLICE_POSITIVE_COUNT = 174
EXPECTED_ALL_SLICE_MINIMUM = -6_201_053_679_933_420_144
EXPECTED_TARGET_FAILURE_COUNT = 29
EXPECTED_WORST_TARGET_VALUE = -194_977_864_413_678_764_224
EXPECTED_WORST_TARGET_VERTEX = 13


def tangent_coefficients() -> tuple[int, ...]:
    factors = tuple(base.affine_coefficients(row) for row in DENOMINATORS)
    numerators = tuple(
        base.affine_coefficients(NUMERATORS[7 * head : 7 * head + 7])
        for head in range(4)
    )
    answer = [0] * base.VERTICES
    for omitted in range(4):
        product = (1,) + (0,) * (base.VERTICES - 1)
        for head, factor in enumerate(factors):
            if head != omitted:
                product = base.xor_convolution(product, factor)
        term = base.xor_convolution(numerators[omitted], product)
        answer = [left + right for left, right in zip(answer, term)]
    return tuple(answer)


def row_value(row: tuple[int, ...], coefficients: tuple[int, ...]) -> int:
    return sum(
        row[mask] * coefficients[mask] for mask in range(base.VERTICES)
    )


def verify() -> None:
    slacks = tuple(
        row[0] - sum(abs(value) for value in row[1:])
        for row in DENOMINATORS
    )
    assert slacks == EXPECTED_DOMINANCE_SLACKS
    assert all(value < 0 for row in DENOMINATORS for value in row[1:])

    coefficients = tangent_coefficients()
    assert all(
        coefficient == 0
        for mask, coefficient in enumerate(coefficients)
        if bin(mask).count("1") > 4
    )

    middle_rows, _ = cut_bridge.middle_rows()
    cut_rows, cut_labels = cut_bridge.quotient_cut_rows()
    middle_values = tuple(
        row_value(row, coefficients) for row in middle_rows
    )
    cut_values = tuple(row_value(row, coefficients) for row in cut_rows)
    assert len(middle_values) == 120
    assert len(cut_values) == 15
    assert min(middle_values) == EXPECTED_MIDDLE_MINIMUM
    assert min(cut_values) == EXPECTED_CUT_MINIMUM
    assert all(value > 0 for value in middle_values)
    assert all(value > 0 for value in cut_values)
    assert cut_labels[0] == ("cut", (0, 15, 51, 60))

    all_slice_values = tuple(
        value for value, _, _, _ in base.slice_inequality_values(coefficients)
    )
    assert sum(value > 0 for value in all_slice_values) == (
        EXPECTED_ALL_SLICE_POSITIVE_COUNT
    )
    assert min(all_slice_values) == EXPECTED_ALL_SLICE_MINIMUM

    signed_target_values = tuple(
        base.target_sign(code) * base.polynomial_value(coefficients, code)
        for code in range(base.VERTICES)
    )
    assert sum(value <= 0 for value in signed_target_values) == (
        EXPECTED_TARGET_FAILURE_COUNT
    )
    assert min(signed_target_values) == EXPECTED_WORST_TARGET_VALUE
    assert signed_target_values[EXPECTED_WORST_TARGET_VERTEX] == (
        EXPECTED_WORST_TARGET_VALUE
    )


def main() -> None:
    verify()
    print(f"dominance slacks: {EXPECTED_DOMINANCE_SLACKS}")
    print(f"minimum of 120 middle rows: {EXPECTED_MIDDLE_MINIMUM}")
    print(f"minimum of 15 quotient cuts: {EXPECTED_CUT_MINIMUM}")
    print(
        "positive rows among all 186 slice rows: "
        f"{EXPECTED_ALL_SLICE_POSITIVE_COUNT}"
    )
    print(f"failed target vertices: {EXPECTED_TARGET_FAILURE_COUNT}")
    print(
        "worst signed target value: "
        f"{EXPECTED_WORST_TARGET_VALUE} at vertex "
        f"{EXPECTED_WORST_TARGET_VERTEX}"
    )


if __name__ == "__main__":
    main()
