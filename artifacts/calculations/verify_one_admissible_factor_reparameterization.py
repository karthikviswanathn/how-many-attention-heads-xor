#!/usr/bin/env python3
"""Verify the one-admissible-factor reparameterization with exact arithmetic."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import math


def cube(dimension: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((vertex >> index) & 1 for index in range(dimension))
        for vertex in range(1 << dimension)
    )


def affine_value(coefficients: tuple[int, ...], point: tuple[int, ...]) -> int:
    return coefficients[0] + sum(
        coefficients[index + 1] * point[index]
        for index in range(len(point))
    )


def add_scaled(
    first: tuple[int, ...], second: tuple[int, ...], scale: int
) -> tuple[int, ...]:
    return tuple(left + scale * right for left, right in zip(first, second))


def product_coefficients(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[int, ...]:
    dimension = len(first) - 1
    answer = [first[0] * second[0]]
    answer.extend(
        first[0] * second[index]
        + first[index] * second[0]
        + first[index] * second[index]
        for index in range(1, dimension + 1)
    )
    answer.extend(
        first[first_index] * second[second_index]
        + first[second_index] * second[first_index]
        for first_index, second_index in combinations(
            range(1, dimension + 1), 2
        )
    )
    return tuple(answer)


def add_coefficients(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(left + right for left, right in zip(first, second))


def choose_shift(
    oriented: tuple[int, ...], free: tuple[int, ...]
) -> int:
    dimension = len(oriented) - 1
    points = cube(dimension)
    assert all(affine_value(oriented, point) > 0 for point in points)
    slopes = oriented[1:]
    assert all(value > 0 for value in slopes) or all(value < 0 for value in slopes)

    bounds = [
        Fraction(-free[index], oriented[index])
        for index in range(1, dimension + 1)
    ]
    bounds.extend(
        Fraction(-affine_value(free, point), affine_value(oriented, point))
        for point in points
    )
    largest = max(bounds)
    return max(1, math.floor(largest) + 1)


def verify_instance(
    first_numerator: tuple[int, ...],
    free_factor: tuple[int, ...],
    second_numerator: tuple[int, ...],
    oriented_factor: tuple[int, ...],
) -> int:
    dimension = len(oriented_factor) - 1
    shift = choose_shift(oriented_factor, free_factor)
    shifted_factor = add_scaled(free_factor, oriented_factor, shift)
    shifted_numerator = add_scaled(
        second_numerator, first_numerator, -shift
    )

    points = cube(dimension)
    assert all(affine_value(shifted_factor, point) > 0 for point in points)
    orientation = 1 if oriented_factor[1] > 0 else -1
    assert all(
        orientation * coefficient > 0 for coefficient in shifted_factor[1:]
    )

    original = add_coefficients(
        product_coefficients(first_numerator, free_factor),
        product_coefficients(second_numerator, oriented_factor),
    )
    shifted = add_coefficients(
        product_coefficients(first_numerator, shifted_factor),
        product_coefficients(shifted_numerator, oriented_factor),
    )
    assert original == shifted

    for point in points:
        original_value = (
            affine_value(first_numerator, point)
            * affine_value(free_factor, point)
            + affine_value(second_numerator, point)
            * affine_value(oriented_factor, point)
        )
        shifted_value = (
            affine_value(first_numerator, point)
            * affine_value(shifted_factor, point)
            + affine_value(shifted_numerator, point)
            * affine_value(oriented_factor, point)
        )
        assert original_value == shifted_value
    return shift


def verify_xor_example() -> None:
    first = (11, 8, -16, -6, -10, -18)
    second = (15, -6, 14, -12, -16, -16)
    oriented = (1, 1, 1, 1, 1, 1)
    negative_first = tuple(-value for value in first)
    zero = (0,) * 6
    shift = verify_instance(negative_first, second, zero, oriented)
    assert shift == 17

    shifted_factor = add_scaled(second, oriented, shift)
    shifted_numerator = add_scaled(zero, negative_first, -shift)
    assert shifted_factor == (32, 11, 31, 5, 1, 1)
    assert shifted_numerator == tuple(17 * value for value in first)

    points = cube(5)
    signs = []
    for point in points:
        first_value = affine_value(first, point)
        second_value = affine_value(second, point)
        assert first_value % 2 and second_value % 2
        xor_label = (first_value > 0) != (second_value > 0)
        product_value = -first_value * second_value
        assert xor_label == (product_value > 0)
        signs.append(1 if product_value > 0 else -1)

    support = (3, 8, 19, 24)
    moment = [0] * 6
    for vertex in support:
        row = (1,) + points[vertex]
        for index, value in enumerate(row):
            moment[index] += signs[vertex] * value
    assert moment == [0] * 6

    print("five-bit incompatible-slope XOR: shift 17 and degree-two circuit verified")


def main() -> None:
    positive_shift = verify_instance(
        (2, -3, 7, 1),
        (-7, 5, -4, 9),
        (-1, 6, -2, 5),
        (4, 2, 3, 1),
    )
    negative_shift = verify_instance(
        (-3, 4, 2, -5),
        (6, -8, 3, 7),
        (5, -1, 6, -2),
        (20, -2, -3, -4),
    )
    print(f"positive orientation: exact reparameterization with shift {positive_shift}")
    print(f"negative orientation: exact reparameterization with shift {negative_shift}")
    verify_xor_example()
    print("one-admissible-factor reparameterization: all exact checks passed")


if __name__ == "__main__":
    main()
