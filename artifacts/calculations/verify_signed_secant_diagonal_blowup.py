#!/usr/bin/env python3
"""Exact arithmetic checks for Theorem 194's signed diagonal blow-up."""

from __future__ import annotations

from fractions import Fraction
import json
import random
from typing import Sequence

from verify_positive_secant_diagonal_blowup import (
    divided_product,
    factor_values,
    product,
    random_simplex,
)


Rational = Fraction


def product_value(
    code: int,
    dimension: int,
    orientations: Sequence[int],
    theta: Sequence[Sequence[Rational]],
) -> Rational:
    zero_direction = [
        [Fraction(0) for _ in block]
        for block in theta
    ]
    base, _ = factor_values(
        code,
        dimension,
        orientations,
        theta,
        zero_direction,
    )
    return product(base)


def chart_score_and_quotient(
    code: int,
    dimension: int,
    orientations: Sequence[int],
    theta: Sequence[Sequence[Rational]],
    direction: Sequence[Sequence[Rational]],
    scalar_direction: Rational,
    t: Rational,
) -> tuple[Rational, Rational]:
    base, derivative = factor_values(
        code,
        dimension,
        orientations,
        theta,
        direction,
    )
    perturbed = [
        value + t * change
        for value, change in zip(base, derivative)
    ]
    q_zero = product(base)
    q_one = product(perturbed)
    divided = divided_product(base, derivative, t)
    score = (
        (1 + t * scalar_direction) * q_one
        - (1 - t * scalar_direction) * q_zero
    ) / 2
    quotient = (
        divided + scalar_direction * (q_one + q_zero)
    ) / 2
    return score, quotient


def normalized_signed_direction(
    theta: Sequence[Sequence[Rational]],
    direction: Sequence[Sequence[Rational]],
    scalar_direction: Rational,
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
        flattened.extend(tangent)
    return max(
        [abs(value) for value in flattened] + [abs(scalar_direction)]
    ) == 1


def factor_graph_divided_product(
    base: Sequence[Rational],
    derivative: Sequence[Rational],
    t: Rational,
) -> tuple[Rational, Rational, Rational]:
    base_product = Fraction(1)
    divided = Fraction(0)
    for base_factor, derivative_factor in zip(base, derivative):
        endpoint_factor = base_factor + t * derivative_factor
        divided = divided * endpoint_factor + base_product * derivative_factor
        base_product *= base_factor
    endpoint_product = base_product + t * divided
    return base_product, divided, endpoint_product


def verify_factor_graph_recurrence() -> int:
    rng = random.Random(196)
    dimension = 4
    checks = 0
    for head_count in range(1, 7):
        orientations = tuple(
            1 if index % 3 else -1
            for index in range(head_count)
        )
        for _ in range(25):
            theta = random_simplex(rng, head_count, dimension + 1)
            direction = []
            for _head in range(head_count):
                raw = [Fraction(rng.randint(-4, 4), 5) for _ in range(dimension)]
                raw.append(-sum(raw))
                direction.append(raw)
            t = Fraction(rng.randint(0, 10), 10)
            for code in range(1 << dimension):
                base, derivative = factor_values(
                    code,
                    dimension,
                    orientations,
                    theta,
                    direction,
                )
                base_product, divided, endpoint_product = (
                    factor_graph_divided_product(base, derivative, t)
                )
                assert base_product == product(base)
                assert divided == divided_product(base, derivative, t)
                assert endpoint_product == product(
                    [
                        value + t * change
                        for value, change in zip(base, derivative)
                    ]
                )
                assert endpoint_product - base_product == t * divided
                checks += 1
    return checks


def verify_random_secant_charts() -> int:
    rng = random.Random(194)
    dimension = 3
    checks = 0
    for head_count in range(1, 6):
        orientations = tuple(
            1 if index % 2 == 0 else -1
            for index in range(head_count)
        )
        for _ in range(40):
            theta_zero = random_simplex(
                rng,
                head_count,
                dimension + 1,
            )
            theta_one = random_simplex(
                rng,
                head_count,
                dimension + 1,
            )
            s = Fraction(rng.randint(0, 20), 20)
            delta_s = 2 * s - 1
            endpoint_difference = [
                [right - left for left, right in zip(block_zero, block_one)]
                for block_zero, block_one in zip(theta_zero, theta_one)
            ]
            t = max(
                [
                    abs(value)
                    for block in endpoint_difference
                    for value in block
                ]
                + [abs(delta_s)]
            )
            assert 0 < t <= 1
            direction = [
                [value / t for value in block]
                for block in endpoint_difference
            ]
            scalar_direction = delta_s / t
            assert normalized_signed_direction(
                theta_zero,
                direction,
                scalar_direction,
            )
            for code in range(1 << dimension):
                direct = (
                    s
                    * product_value(
                        code,
                        dimension,
                        orientations,
                        theta_one,
                    )
                    - (1 - s)
                    * product_value(
                        code,
                        dimension,
                        orientations,
                        theta_zero,
                    )
                )
                score, quotient = chart_score_and_quotient(
                    code,
                    dimension,
                    orientations,
                    theta_zero,
                    direction,
                    scalar_direction,
                    t,
                )
                assert score == direct
                assert score == t * quotient
                checks += 1
    return checks


def verify_pair_gap_equivalence() -> int:
    rng = random.Random(195)
    dimension = 3
    orientations = (1, -1, 1)
    checks = 0
    for _ in range(200):
        theta_zero = random_simplex(
            rng,
            len(orientations),
            dimension + 1,
        )
        theta_one = random_simplex(
            rng,
            len(orientations),
            dimension + 1,
        )
        positive = {
            code
            for code in range(1 << dimension)
            if rng.randint(0, 1) == 1
        }
        if not positive or len(positive) == 1 << dimension:
            positive = {0, 3, 5}
        negative = set(range(1 << dimension)) - positive
        ratios = {}
        for code in range(1 << dimension):
            q_zero = product_value(
                code,
                dimension,
                orientations,
                theta_zero,
            )
            q_one = product_value(
                code,
                dimension,
                orientations,
                theta_one,
            )
            assert q_zero > 0 and q_one > 0
            ratios[code] = q_zero / q_one
        lower = max(ratios[code] for code in positive)
        upper = min(ratios[code] for code in negative)
        pair_feasible = lower < upper
        if pair_feasible:
            odds = (lower + upper) / 2
            s = odds / (1 + odds)
            for code in positive:
                assert (
                    s
                    * product_value(
                        code,
                        dimension,
                        orientations,
                        theta_one,
                    )
                    - (1 - s)
                    * product_value(
                        code,
                        dimension,
                        orientations,
                        theta_zero,
                    )
                    > 0
                )
            for code in negative:
                assert (
                    s
                    * product_value(
                        code,
                        dimension,
                        orientations,
                        theta_one,
                    )
                    - (1 - s)
                    * product_value(
                        code,
                        dimension,
                        orientations,
                        theta_zero,
                    )
                    < 0
                )
        checks += 1
    return checks


def verify_boundary_examples() -> dict[str, str | bool]:
    dimension = 1
    orientations = (1,)
    theta = ((Fraction(1), Fraction(0)),)
    valid_direction = ((Fraction(-1), Fraction(1)),)
    scalar_direction = Fraction(1, 4)
    assert normalized_signed_direction(
        theta,
        valid_direction,
        scalar_direction,
    )
    signed_margins = []
    for code, label in ((0, -1), (1, 1)):
        _, quotient = chart_score_and_quotient(
            code,
            dimension,
            orientations,
            theta,
            valid_direction,
            scalar_direction,
            Fraction(0),
        )
        signed_margins.append(label * quotient)
    assert signed_margins == [Fraction(1, 4), Fraction(1, 4)]
    for t in (Fraction(1, 100), Fraction(1, 3), Fraction(1)):
        for code, label in ((0, -1), (1, 1)):
            score, quotient = chart_score_and_quotient(
                code,
                dimension,
                orientations,
                theta,
                valid_direction,
                scalar_direction,
                t,
            )
            assert score == t * quotient
            assert label * score > 0

    outward_boundary_direction = ((Fraction(1), Fraction(-1)),)
    outward_scalar = Fraction(-1, 4)
    assert normalized_signed_direction(
        theta,
        outward_boundary_direction,
        outward_scalar,
    )
    outward_margins = []
    for code, label in ((0, 1), (1, -1)):
        _, quotient = chart_score_and_quotient(
            code,
            dimension,
            orientations,
            theta,
            outward_boundary_direction,
            outward_scalar,
            Fraction(0),
        )
        outward_margins.append(label * quotient)
    assert outward_margins == [Fraction(1, 4), Fraction(1, 4)]
    for t in (Fraction(1, 100), Fraction(1, 3)):
        endpoint = [
            theta[0][index] + t * outward_boundary_direction[0][index]
            for index in range(2)
        ]
        assert endpoint[1] < 0

    strict_theta = ((Fraction(99, 100), Fraction(1, 100)),)
    for t in (Fraction(1, 1000), Fraction(1, 200)):
        endpoint = [
            strict_theta[0][index]
            + t * outward_boundary_direction[0][index]
            for index in range(2)
        ]
        assert min(endpoint) >= 0 and sum(endpoint) == 1
        for code, label in ((0, 1), (1, -1)):
            score, _ = chart_score_and_quotient(
                code,
                dimension,
                orientations,
                strict_theta,
                outward_boundary_direction,
                outward_scalar,
                t,
            )
            assert label * score > 0

    scalar_only = ((Fraction(0), Fraction(0)),)
    scalar_only_margins = []
    for code, label in ((0, -1), (1, 1)):
        _, quotient = chart_score_and_quotient(
            code,
            dimension,
            orientations,
            theta,
            scalar_only,
            Fraction(1),
            Fraction(0),
        )
        scalar_only_margins.append(label * quotient)
    assert min(scalar_only_margins) < 0

    return {
        "valid_boundary_signed_margin": str(min(signed_margins)),
        "valid_boundary_opens_to_secant": True,
        "outward_boundary_formal_margin": str(min(outward_margins)),
        "outward_boundary_strictifies_and_opens": True,
        "scalar_only_chart_cannot_fit_nonconstant_labels": True,
    }


def main() -> None:
    dimension = 6
    head_count = 3
    payload = {
        "status": "verified",
        "theorem": (
            "lemmas/02_complexity_measure_upper_bounds/"
            "194_signed_secant_diagonal_blowup.md"
        ),
        "random_secant_vertex_checks": verify_random_secant_charts(),
        "factor_graph_recurrence_checks": verify_factor_graph_recurrence(),
        "pair_gap_equivalence_checks": verify_pair_gap_equivalence(),
        "boundary_examples": verify_boundary_examples(),
        "balanced_six_bit_constraint_counts": {
            "signed_constraints": 1 << dimension,
            "pair_gap_constraints": (1 << (dimension - 1)) ** 2,
            "raw_signed_charts": 2 * head_count * (dimension + 1) + 2,
            "symmetry_quotient_chart_types_upper_bound": 4 * (dimension + 1) + 2,
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
