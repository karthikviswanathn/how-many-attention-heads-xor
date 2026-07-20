#!/usr/bin/env python3
"""Exact arithmetic checks for Theorem 193's diagonal blow-up."""

from __future__ import annotations

from fractions import Fraction
import json
import random
from typing import Sequence


Rational = Fraction


def product(values: Sequence[Rational]) -> Rational:
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def divided_product(
    base: Sequence[Rational],
    direction: Sequence[Rational],
    t: Rational,
) -> Rational:
    """Evaluate (prod(base + t direction) - prod(base)) / t without division."""
    if len(base) != len(direction):
        raise ValueError("base and direction lengths differ")
    suffix = [Fraction(1)] * (len(base) + 1)
    for index in range(len(base) - 1, -1, -1):
        suffix[index] = base[index] * suffix[index + 1]
    prefix = Fraction(1)
    answer = Fraction(0)
    for index, derivative in enumerate(direction):
        answer += derivative * prefix * suffix[index + 1]
        prefix *= base[index] + t * derivative
    return answer


def literal_value(
    code: int,
    dimension: int,
    orientation: int,
    literal_index: int,
) -> Rational:
    if literal_index == 0:
        return Fraction(1)
    bit = (code >> (literal_index - 1)) & 1
    if orientation == 1:
        return Fraction(bit)
    if orientation == -1:
        return Fraction(1 - bit)
    raise ValueError("orientation must be +1 or -1")


def factor_values(
    code: int,
    dimension: int,
    orientations: Sequence[int],
    theta: Sequence[Sequence[Rational]],
    direction: Sequence[Sequence[Rational]],
) -> tuple[list[Rational], list[Rational]]:
    base = []
    derivative = []
    for orientation, block, tangent in zip(orientations, theta, direction):
        if len(block) != dimension + 1 or len(tangent) != dimension + 1:
            raise ValueError("wrong barycentric block width")
        literals = [
            literal_value(code, dimension, orientation, index)
            for index in range(dimension + 1)
        ]
        base.append(sum(weight * value for weight, value in zip(block, literals)))
        derivative.append(
            sum(weight * value for weight, value in zip(tangent, literals))
        )
    return base, derivative


def divided_pair_gap(
    positive_code: int,
    negative_code: int,
    dimension: int,
    orientations: Sequence[int],
    theta: Sequence[Sequence[Rational]],
    direction: Sequence[Sequence[Rational]],
    t: Rational,
) -> Rational:
    positive_base, positive_direction = factor_values(
        positive_code,
        dimension,
        orientations,
        theta,
        direction,
    )
    negative_base, negative_direction = factor_values(
        negative_code,
        dimension,
        orientations,
        theta,
        direction,
    )
    return (
        product(negative_base)
        * divided_product(positive_base, positive_direction, t)
        - product(positive_base)
        * divided_product(negative_base, negative_direction, t)
    )


def original_pair_gap(
    positive_code: int,
    negative_code: int,
    dimension: int,
    orientations: Sequence[int],
    theta: Sequence[Sequence[Rational]],
    direction: Sequence[Sequence[Rational]],
    t: Rational,
) -> Rational:
    positive_base, positive_direction = factor_values(
        positive_code,
        dimension,
        orientations,
        theta,
        direction,
    )
    negative_base, negative_direction = factor_values(
        negative_code,
        dimension,
        orientations,
        theta,
        direction,
    )
    positive_perturbed = [
        value + t * derivative
        for value, derivative in zip(positive_base, positive_direction)
    ]
    negative_perturbed = [
        value + t * derivative
        for value, derivative in zip(negative_base, negative_direction)
    ]
    return (
        product(negative_base) * product(positive_perturbed)
        - product(positive_base) * product(negative_perturbed)
    )


def normalized_feasible_direction(
    theta: Sequence[Sequence[Rational]],
    direction: Sequence[Sequence[Rational]],
) -> bool:
    if len(theta) != len(direction):
        return False
    flattened = []
    for block, tangent in zip(theta, direction):
        if len(block) != len(tangent):
            return False
        if sum(block) != 1 or any(value < 0 for value in block):
            return False
        if sum(tangent) != 0:
            return False
        if any(value == 0 and derivative < 0 for value, derivative in zip(block, tangent)):
            return False
        flattened.extend(tangent)
    return max(abs(value) for value in flattened) == 1


def random_simplex(
    rng: random.Random,
    blocks: int,
    width: int,
) -> list[list[Rational]]:
    answer = []
    for _ in range(blocks):
        integers = [rng.randint(1, 11) for _ in range(width)]
        total = sum(integers)
        answer.append([Fraction(value, total) for value in integers])
    return answer


def verify_telescoping_identity() -> int:
    rng = random.Random(193)
    checks = 0
    for head_count in range(1, 7):
        for _ in range(50):
            base = [Fraction(rng.randint(-7, 9), 5) for _ in range(head_count)]
            direction = [
                Fraction(rng.randint(-5, 6), 7) for _ in range(head_count)
            ]
            for t in (Fraction(0), Fraction(1, 13), Fraction(7, 5)):
                left = product(
                    [
                        value + t * derivative
                        for value, derivative in zip(base, direction)
                    ]
                ) - product(base)
                right = t * divided_product(base, direction, t)
                assert left == right
                checks += 1
    return checks


def verify_secant_chart_identity() -> int:
    rng = random.Random(194)
    dimension = 2
    orientations = (1, -1, 1)
    checks = 0
    for _ in range(40):
        theta_zero = random_simplex(rng, len(orientations), dimension + 1)
        theta_one = random_simplex(rng, len(orientations), dimension + 1)
        raw_direction = [
            [right - left for left, right in zip(block_zero, block_one)]
            for block_zero, block_one in zip(theta_zero, theta_one)
        ]
        t = max(abs(value) for block in raw_direction for value in block)
        assert t > 0
        direction = [
            [value / t for value in block]
            for block in raw_direction
        ]
        assert normalized_feasible_direction(theta_zero, direction)
        for positive_code in range(1 << dimension):
            for negative_code in range(1 << dimension):
                original = original_pair_gap(
                    positive_code,
                    negative_code,
                    dimension,
                    orientations,
                    theta_zero,
                    direction,
                    t,
                )
                divided = divided_pair_gap(
                    positive_code,
                    negative_code,
                    dimension,
                    orientations,
                    theta_zero,
                    direction,
                    t,
                )
                assert original == t * divided
                checks += 1
    return checks


def verify_boundary_examples() -> dict[str, str | bool]:
    dimension = 1
    orientations = (1,)
    theta = ((Fraction(1), Fraction(0)),)
    valid_direction = ((Fraction(-1), Fraction(1)),)
    assert normalized_feasible_direction(theta, valid_direction)
    valid_at_zero = divided_pair_gap(
        1,
        0,
        dimension,
        orientations,
        theta,
        valid_direction,
        Fraction(0),
    )
    assert valid_at_zero == 1
    for t in (Fraction(1, 100), Fraction(1, 3), Fraction(1)):
        assert original_pair_gap(
            1,
            0,
            dimension,
            orientations,
            theta,
            valid_direction,
            t,
        ) == t

    invalid_direction = ((Fraction(1), Fraction(-1)),)
    assert not normalized_feasible_direction(theta, invalid_direction)
    spurious_at_zero = divided_pair_gap(
        0,
        1,
        dimension,
        orientations,
        theta,
        invalid_direction,
        Fraction(0),
    )
    assert spurious_at_zero == 1
    for t in (Fraction(1, 100), Fraction(1, 3)):
        endpoint = [
            theta[0][index] + t * invalid_direction[0][index]
            for index in range(2)
        ]
        assert endpoint[1] < 0

    return {
        "valid_boundary_divided_gap": str(valid_at_zero),
        "valid_boundary_opens_to_secant": True,
        "invalid_boundary_divided_gap": str(spurious_at_zero),
        "invalid_boundary_leaves_simplex": True,
    }


def main() -> None:
    payload = {
        "status": "verified",
        "theorem": (
            "lemmas/02_complexity_measure_upper_bounds/"
            "193_positive_secant_diagonal_blowup.md"
        ),
        "telescoping_identity_checks": verify_telescoping_identity(),
        "secant_chart_pair_checks": verify_secant_chart_identity(),
        "boundary_examples": verify_boundary_examples(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
