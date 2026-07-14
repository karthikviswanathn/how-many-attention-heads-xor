#!/usr/bin/env python3
"""Verify the exact five-bit fixed-center generic-line equations.

For a high-coefficient target q, retain the multiplier intercept m0 instead
of eliminating it.  The resulting fixed-center membership system consists
of five quotient cubics and one pentad equation.  Along a generic target
line, these have bidegrees (3,1)^5 and (10,5) on P5 times P1.
"""

from __future__ import annotations

import itertools
import math
import random


N = 5
AFFINE_MASKS = (0, 1, 2, 4, 8, 16)
EDGES = list(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}

# A basis of the left kernel of the unsigned K5 incidence matrix.
QUOTIENT = (
    (0, 1, -1, 0, -1, 1, 0, 0, 0, 0),
    (0, 1, 0, -1, -1, 0, 1, 0, 0, 0),
    (1, 0, -1, 0, -1, 0, 0, 1, 0, 0),
    (1, 0, 0, -1, -1, 0, 0, 0, 1, 0),
    (1, 1, -1, -1, -1, 0, 0, 0, 0, 1),
)


def hamiltonian_cycles() -> list[tuple[tuple[int, int], ...]]:
    answer = []
    for tail in itertools.permutations(range(1, N)):
        cycle = (0,) + tail
        if cycle[1] > cycle[-1]:
            continue
        answer.append(
            tuple(
                sorted(
                    tuple(sorted((cycle[index], cycle[(index + 1) % N])))
                    for index in range(N)
                )
            )
        )
    assert len(answer) == 12
    return answer


PENTAD_SIGNS = (-1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1)
PENTAD_CYCLES = hamiltonian_cycles()


def affine(coefficients: list[int]) -> list[int]:
    answer = [0] * (1 << N)
    for mask, coefficient in zip(AFFINE_MASKS, coefficients):
        answer[mask] = coefficient
    return answer


def boolean_product(left: list[int], right: list[int]) -> list[int]:
    answer = [0] * (1 << N)
    for left_mask, left_value in enumerate(left):
        if not left_value:
            continue
        for right_mask, right_value in enumerate(right):
            if right_value:
                answer[left_mask | right_mask] += left_value * right_value
    return answer


def fixed_center_target(parameters: list[list[int]]) -> list[int]:
    left, right, multiplier, numerator = map(affine, parameters)
    cubic = boolean_product(
        boolean_product(left, right), multiplier
    )
    quadratic = boolean_product(numerator, multiplier)
    return [x + y for x, y in zip(cubic, quadratic)]


def scaled_petersen_solution(
    target: list[int], slopes: list[int]
) -> list[int]:
    z = []
    for left, right in EDGES:
        complement = [
            vertex
            for vertex in range(N)
            if vertex not in (left, right)
        ]
        triangle = sum(1 << vertex for vertex in complement)
        z.append(slopes[left] * slopes[right] * target[triangle])
    total = sum(z)
    answer = []
    for index, (left, right) in enumerate(EDGES):
        disjoint_sum = sum(
            z[other]
            for other, (third, fourth) in enumerate(EDGES)
            if len({left, right, third, fourth}) == 4
        )
        answer.append(3 * (z[index] + disjoint_sum) - total)
    return answer


def quotient_cubics(
    target: list[int], multiplier: list[int]
) -> list[int]:
    intercept = multiplier[0]
    slopes = multiplier[1:]
    h_values = scaled_petersen_solution(target, slopes)
    edge_values = []
    for index, (left, right) in enumerate(EDGES):
        complement_product = math.prod(
            slopes[vertex]
            for vertex in range(N)
            if vertex not in (left, right)
        )
        quadratic_mask = (1 << left) | (1 << right)
        edge_values.append(
            6 * complement_product * target[quadratic_mask]
            - (slopes[left] + slopes[right] + intercept)
            * h_values[index]
        )
    return [
        sum(coefficient * value for coefficient, value in zip(row, edge_values))
        for row in QUOTIENT
    ]


def pentad(edge_values: list[int]) -> int:
    return sum(
        sign
        * math.prod(edge_values[EDGE_INDEX[edge]] for edge in cycle)
        for sign, cycle in zip(PENTAD_SIGNS, PENTAD_CYCLES)
    )


def verify() -> None:
    rng = random.Random(5_265)
    for _ in range(100):
        parameters = [
            [rng.randint(-7, 7) for _ in range(N + 1)]
            for _ in range(4)
        ]
        target = fixed_center_target(parameters)
        multiplier = parameters[2]
        quotient_values = quotient_cubics(target, multiplier)
        assert quotient_values == [0] * 5
        h_values = scaled_petersen_solution(target, multiplier[1:])
        assert pentad(h_values) == 0

    raw_intersection = 5 * 3**5 + 5 * 10 * 3**4
    assert raw_intersection == 5_265
    print("verified exact five-bit fixed-center generic-line system")
    print("quotient equations: five equations of bidegree (3,1)")
    print("pentad equation: one equation of bidegree (10,5)")
    print(f"raw P5 x P1 intersection count={raw_intersection}")


if __name__ == "__main__":
    verify()
