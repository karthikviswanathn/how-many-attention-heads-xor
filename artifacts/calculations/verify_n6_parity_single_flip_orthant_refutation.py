#!/usr/bin/env python3
"""Verify that Fourier-orthant rigidity alone does not obstruct five heads.

The calculation is in sign coordinates w, after the exceptional vertex is
sent to (1, ..., 1).  Products are reduced in the Boolean quotient ring
R[w_1, ..., w_6] / (w_1^2 - 1, ..., w_6^2 - 1).  Coefficient multiplication
is therefore XOR convolution on subsets of [6].

The five denominators are admissible for a middle-weight exceptional vertex.
The exact tangent form has every proper Fourier coefficient strictly negative,
but it does not sign-represent parity with the exceptional vertex flipped.
"""

from __future__ import annotations

import math


DIMENSION = 6
SUBSETS = 1 << DIMENSION
FULL_SET = SUBSETS - 1

# The exceptional vertex has three negative and three positive sign coordinates
# before it is sent to the all-positive w vertex.
EXCEPTIONAL_SIGNS = (-1, -1, -1, 1, 1, 1)

# Rows are (constant, w_1, ..., w_6).
DENOMINATORS = (
    (20, 1, 3, 3, -5, -5, -1),
    (27, 1, 5, 2, -6, -6, -4),
    (24, 2, 4, 5, -6, -1, -5),
    (18, 2, 2, 3, -4, -1, -4),
    (25, 1, 2, 3, -1, -5, -6),
)

NUMERATORS = (
    (0, -14480, 1768, 28332, 29468, 115306, 0),
    (0, -503, -18040, -27708, 0, -82845, 20470),
    (0, -9127, 21989, -15559, -41077, 0, -90655),
    (-33433, 36671, 0, 4930, 32365, -115827, 41477),
    (0, -20102, -5547, 2203, -49910, 73492, 1252),
)

WRONG_CODES = (
    3, 5, 6, 9, 10, 12, 14, 15, 17, 18, 21, 23, 24, 27, 28, 30, 33,
    35, 37, 38, 40, 42, 44, 45, 47, 49, 50, 52, 55, 56, 59, 61, 62,
)


def affine_coefficients(row: tuple[int, ...]) -> list[int]:
    answer = [0] * SUBSETS
    answer[0] = row[0]
    for coordinate, coefficient in enumerate(row[1:]):
        answer[1 << coordinate] = coefficient
    return answer


def xor_convolution(first: list[int], second: list[int]) -> list[int]:
    answer = [0] * SUBSETS
    for left, left_value in enumerate(first):
        if left_value == 0:
            continue
        for right, right_value in enumerate(second):
            if right_value:
                answer[left ^ right] += left_value * right_value
    return answer


def tangent_coefficients() -> list[int]:
    denominators = [affine_coefficients(row) for row in DENOMINATORS]
    numerators = [affine_coefficients(row) for row in NUMERATORS]
    answer = [0] * SUBSETS
    for omitted in range(5):
        other_product = [1] + [0] * (SUBSETS - 1)
        for head, denominator in enumerate(denominators):
            if head != omitted:
                other_product = xor_convolution(other_product, denominator)
        term = xor_convolution(numerators[omitted], other_product)
        answer = [left + right for left, right in zip(answer, term)]
    return answer


def sign_point(code: int) -> tuple[int, ...]:
    return tuple(
        -1 if (code >> coordinate) & 1 else 1
        for coordinate in range(DIMENSION)
    )


def evaluate(coefficients: list[int], code: int) -> int:
    point = sign_point(code)
    return sum(
        coefficient
        * math.prod(
            point[coordinate]
            for coordinate in range(DIMENSION)
            if (subset >> coordinate) & 1
        )
        for subset, coefficient in enumerate(coefficients)
    )


def target_sign(code: int) -> int:
    parity = math.prod(sign_point(code))
    return -1 if code == 0 else parity


def main() -> None:
    for denominator in DENOMINATORS:
        assert denominator[0] > sum(abs(value) for value in denominator[1:])
        reoriented_slopes = [
            slope * exceptional
            for slope, exceptional in zip(
                denominator[1:], EXCEPTIONAL_SIGNS
            )
        ]
        assert all(value < 0 for value in reoriented_slopes)

    coefficients = tangent_coefficients()
    assert coefficients[FULL_SET] == 0
    assert max(coefficients[:FULL_SET]) == -404109
    assert min(coefficients[:FULL_SET]) == -1574974786
    assert sum(coefficients) == -7604818704

    shifted_magnitudes = {
        subset: -coefficients[FULL_SET ^ subset]
        for subset in range(1, SUBSETS)
    }
    assert shifted_magnitudes[1] == 993952
    assert shifted_magnitudes[2] == 997151
    assert shifted_magnitudes[3] == 7348490
    assert shifted_magnitudes[3] > (
        shifted_magnitudes[1] + shifted_magnitudes[2]
    )

    wrong = tuple(
        code
        for code in range(SUBSETS)
        if target_sign(code) * evaluate(coefficients, code) <= 0
    )
    assert wrong == WRONG_CODES
    assert SUBSETS - len(wrong) == 31

    print("five admissible middle-weight denominators: verified")
    print("all 63 proper Fourier coefficients are strictly negative")
    print("degree-six Fourier coefficient: 0")
    print("target signs correct on 31 of 64 vertices")
    print("weighted-cut triangle inequality: violated exactly")
    print("orthant-only obstruction: refuted")


if __name__ == "__main__":
    main()
