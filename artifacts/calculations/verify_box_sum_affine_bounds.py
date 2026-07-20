#!/usr/bin/env python3
"""Compare the exact box-sum greedy rule with all polytope extreme points."""

from __future__ import annotations

from fractions import Fraction
import itertools
import json
import random

from hstar.signed_secant_mccormick import linear_box_sum_bounds


def extreme_point_bounds(
    coefficients: list[Fraction],
    bounds: list[tuple[Fraction, Fraction]],
    total: Fraction,
) -> tuple[Fraction, Fraction]:
    values = []
    for free_index in range(len(bounds)):
        fixed_indices = [
            index for index in range(len(bounds)) if index != free_index
        ]
        for choices in itertools.product((0, 1), repeat=len(fixed_indices)):
            point = [Fraction(0)] * len(bounds)
            fixed_sum = Fraction(0)
            for index, choice in zip(fixed_indices, choices):
                point[index] = bounds[index][choice]
                fixed_sum += point[index]
            free_value = total - fixed_sum
            lower, upper = bounds[free_index]
            if lower <= free_value <= upper:
                point[free_index] = free_value
                values.append(
                    sum(
                        coefficient * value
                        for coefficient, value in zip(coefficients, point)
                    )
                )
    if not values:
        raise RuntimeError("feasible box-sum polytope had no enumerated extreme point")
    return min(values), max(values)


def main() -> None:
    rng = random.Random(197)
    checks = 0
    for variable_count in range(1, 8):
        for _ in range(100):
            bounds = []
            for _index in range(variable_count):
                lower = Fraction(rng.randint(-8, 4), 4)
                upper = lower + Fraction(rng.randint(0, 8), 4)
                bounds.append((lower, upper))
            lower_sum = sum(lower for lower, _ in bounds)
            capacity = sum(upper - lower for lower, upper in bounds)
            fraction = Fraction(rng.randint(0, 12), 12)
            total = lower_sum + fraction * capacity
            coefficients = [
                Fraction(rng.randint(-12, 12), 6)
                for _index in range(variable_count)
            ]
            greedy = linear_box_sum_bounds(coefficients, bounds, total)
            enumerated = extreme_point_bounds(coefficients, bounds, total)
            assert greedy == enumerated
            checks += 1

    simplex_bounds = [(Fraction(0), Fraction(1))] * 9
    for mask in range(1 << 9):
        coefficients = [
            Fraction((mask >> index) & 1)
            for index in range(9)
        ]
        lower, upper = linear_box_sum_bounds(
            coefficients,
            simplex_bounds,
            Fraction(1),
        )
        assert 0 <= lower <= upper <= 1

    try:
        linear_box_sum_bounds(
            [Fraction(1)],
            [(Fraction(0), Fraction(1))],
            Fraction(2),
        )
    except ValueError:
        infeasible_rejected = True
    else:
        infeasible_rejected = False
    assert infeasible_rejected

    print(
        json.dumps(
            {
                "status": "verified",
                "random_extreme_point_comparisons": checks,
                "simplex_literal_masks_checked": 1 << 9,
                "infeasible_box_rejected": infeasible_rejected,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
