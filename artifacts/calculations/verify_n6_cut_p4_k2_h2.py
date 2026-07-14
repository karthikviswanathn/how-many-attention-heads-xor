#!/usr/bin/env python3
"""Verify an exact two-head certificate for the P4 disjoint K2 cut threshold."""

from __future__ import annotations


EDGES = ((0, 1), (0, 2), (1, 3), (4, 5))
EXPECTED_MASK = 0x724E7FFE7FFE724E

DENOMINATOR_1 = (20, -3, -4, -3, -5, -2, -2)
DENOMINATOR_2 = (34, -5, -7, -4, -6, -3, -8)

# The cleared score is
#
#   c D1 D2 + N1 D2 + N2 D1.
CLEARED_COEFFICIENTS = (
    -15,
    272,
    -205,
    -315,
    -21,
    203,
    90,
    764,
    32,
    295,
    473,
    -46,
    -499,
    -193,
    -1139,
)


def affine_value(coefficients: tuple[int, ...], bits: tuple[int, ...]) -> int:
    assert len(coefficients) == len(bits) + 1
    return coefficients[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(coefficients[1:], bits)
    )


def main() -> None:
    constant = CLEARED_COEFFICIENTS[0]
    numerator_1 = CLEARED_COEFFICIENTS[1:8]
    numerator_2 = CLEARED_COEFFICIENTS[8:15]

    truth_mask = 0
    signed_margins: list[int] = []
    denominator_1_values: list[int] = []
    denominator_2_values: list[int] = []

    for vertex in range(64):
        bits = tuple((vertex >> coordinate) & 1 for coordinate in range(6))
        cut = sum(bits[first] ^ bits[second] for first, second in EDGES)
        target = cut >= 2
        if target:
            truth_mask |= 1 << vertex

        denominator_1 = affine_value(DENOMINATOR_1, bits)
        denominator_2 = affine_value(DENOMINATOR_2, bits)
        denominator_1_values.append(denominator_1)
        denominator_2_values.append(denominator_2)
        assert denominator_1 > 0
        assert denominator_2 > 0

        value_1 = affine_value(numerator_1, bits)
        value_2 = affine_value(numerator_2, bits)
        cleared = (
            constant * denominator_1 * denominator_2
            + value_1 * denominator_2
            + value_2 * denominator_1
        )
        signed_margins.append(cleared if target else -cleared)

    assert truth_mask == EXPECTED_MASK
    assert min(signed_margins) == 1
    assert all(margin > 0 for margin in signed_margins)
    assert (min(denominator_1_values), max(denominator_1_values)) == (1, 20)
    assert (min(denominator_2_values), max(denominator_2_values)) == (1, 34)

    print(f"truth mask: {truth_mask:#018x}")
    print(f"minimum signed cleared score: {min(signed_margins)}")
    print("verified exact two-head certificate")


if __name__ == "__main__":
    main()
