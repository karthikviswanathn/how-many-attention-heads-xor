#!/usr/bin/env python3
"""Verify an exact limit of the blockwise degree-two dual ansatz.

For a denominator tuple D, write P_h for the product of the other three
denominators.  If y is a nonnegative degree-two evaluation dual, then y/P_h
annihilates the h-th affine numerator block.  This verifier gives an exact
tuple for which no nonzero sum of four such rescaled measures annihilates the
full four-head tangent space.
"""

from __future__ import annotations

import math


N = 6
HEADS = 4
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669

SUPPORT40 = (
    1, 2, 3, 4, 7, 8, 10, 12, 13, 14, 15, 19, 20, 24, 25, 26, 28,
    29, 30, 31, 33, 34, 35, 39, 40, 41, 44, 45, 46, 49, 50, 51, 52,
    55, 56, 58, 60, 61, 62, 63,
)
SUPPORT54 = tuple(
    sorted(set(SUPPORT40) | {FULL ^ code for code in SUPPORT40})
)
DEGREE_TWO_MASKS = tuple(
    mask for mask in range(1 << N) if bin(mask).count("1") <= 2
)

DENOMINATORS = (
    (28, -5, -4, -8, -3, -3, -4),
    (32, -8, -5, -8, -5, -1, -4),
    (33, 5, 6, 3, 3, 5, 6),
    (30, 8, 5, 2, 3, 8, 2),
)

TANGENT_VECTOR = (
    1000, -731, -793, -873, -789, 543, -824,
    763, -236, 573, 725, 276, -46, 854,
    -1000, -424, -332, 52, -639, 269, 24,
    -1000, -261, -158, -132, 175, -386, -94,
)

CORRECTIONS = (
    (
        -137, -778, -142, 156, 341, 116, -12, -512, 130, 109, 92,
        884, -32, -106, -220, -52, 337, 92, -43, -144, 78, -209,
    ),
    (
        29, -879, -162, 203, 391, 71, -26, -586, 224, 139, 62,
        1000, -170, -147, -187, -139, 381, 63, -63, -141, 51, -195,
    ),
    (
        -148, -1000, -209, -174, 314, -128, 33, -643, -232, -104,
        -61, 1000, 65, 148, 206, -8, 351, -76, 20, 83, -21, 184,
    ),
    (
        -180, -940, -190, -162, 287, -59, 31, -600, -291, -91,
        -37, 901, 64, 100, 203, -71, 330, 64, 29, 28, 52, 97,
    ),
)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def affine_value(coefficients: tuple[int, ...], code: int) -> int:
    return coefficients[0] + sum(
        coefficients[coordinate + 1] * character(1 << coordinate, code)
        for coordinate in range(N)
    )


def polynomial_value(
    masks: tuple[int, ...], coefficients: tuple[int, ...], code: int
) -> int:
    return sum(
        coefficient * character(mask, code)
        for mask, coefficient in zip(masks, coefficients)
    )


def verify() -> tuple[int, int]:
    assert len(SUPPORT54) == 54
    assert len(DEGREE_TWO_MASKS) == 22
    assert len(TANGENT_VECTOR) == 28
    assert len(CORRECTIONS) == HEADS
    assert all(len(row) == 22 for row in CORRECTIONS)

    denominator_values = []
    for head, coefficients in enumerate(DENOMINATORS):
        orientation = -1 if head < 2 else 1
        assert all(orientation * value > 0 for value in coefficients[1:])
        assert coefficients[0] > sum(abs(value) for value in coefficients[1:])
        values = tuple(
            affine_value(coefficients, code) for code in SUPPORT54
        )
        assert min(values) > 0
        denominator_values.append(values)

    products = tuple(
        tuple(
            math.prod(
                denominator_values[other][vertex]
                for other in range(HEADS)
                if other != head
            )
            for vertex in range(len(SUPPORT54))
        )
        for head in range(HEADS)
    )

    signed_tangent_values = []
    for vertex, code in enumerate(SUPPORT54):
        tangent_value = sum(
            products[head][vertex]
            * affine_value(
                TANGENT_VECTOR[7 * head : 7 * (head + 1)], code
            )
            for head in range(HEADS)
        )
        signed_tangent_values.append(target_sign(code) * tangent_value)

    margins = []
    for head in range(HEADS):
        for vertex, code in enumerate(SUPPORT54):
            signed_correction = target_sign(code) * polynomial_value(
                DEGREE_TWO_MASKS, CORRECTIONS[head], code
            )
            margins.append(
                signed_tangent_values[vertex]
                - products[head][vertex] * signed_correction
            )

    minimum = min(margins)
    maximum = max(margins)
    assert minimum == 54912
    assert maximum == 10513500
    assert minimum > 0
    return minimum, maximum


def main() -> None:
    minimum, maximum = verify()
    print(f"support rows: {len(SUPPORT54)}")
    print("denominator orientation: 2 positive-slope heads")
    print(f"minimum exact separation margin: {minimum}")
    print(f"maximum exact separation value: {maximum}")


if __name__ == "__main__":
    main()
