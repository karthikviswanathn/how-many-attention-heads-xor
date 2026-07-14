#!/usr/bin/env python3
"""Verify the dimension of the six-bit cleared four-head tangent image.

In Fourier coordinates with z_i^2 = 1, the map is

    Phi(B, A) = sum_h A_h product_{j != h} B_j,

where the four B_h and four A_h are affine.  There are 56 parameters and
seven universal gauge directions.  A positive-orientation integer witness
has Jacobian rank 49 modulo 1000003, proving that the image closure has
dimension exactly 49 in the 57-dimensional quartic coefficient space.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np

import verify_cubic_tangent_dimension as cubic


JACOBIAN_PRIME = 1_000_003
SAMPLE_PRIME = 101
DIMENSION = 6
HEADS = 4
WIDTH = DIMENSION + 1

WITNESS = (
    (31, 2, 2, 5, 12, 1, 6),
    (31, 8, 1, 1, 3, 2, 10),
    (47, 9, 10, 12, 2, 1, 3),
    (34, 2, 4, 8, 3, 5, 3),
    (7, 11, 11, 0, 2, 4, 10),
    (-8, 4, -2, -4, 3, 15, -5),
    (-12, 0, -7, -6, -7, -6, -12),
    (0, 4, 11, -15, -3, -13, -13),
)


def monomials() -> tuple[int, ...]:
    return tuple(
        sum(1 << index for index in subset)
        for degree in range(5)
        for subset in combinations(range(DIMENSION), degree)
    )


OUTPUT_MONOMIALS = monomials()
OUTPUT_INDEX = {
    monomial: index for index, monomial in enumerate(OUTPUT_MONOMIALS)
}
AFFINE_MONOMIALS = (0, 1, 2, 4, 8, 16, 32)


def affine(coefficients: tuple[int, ...]) -> dict[int, int]:
    return dict(zip(AFFINE_MONOMIALS, coefficients))


def basis(coordinate: int) -> dict[int, int]:
    return {AFFINE_MONOMIALS[coordinate]: 1}


def add(*polynomials: dict[int, int]) -> dict[int, int]:
    answer: dict[int, int] = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
    return {
        monomial: coefficient
        for monomial, coefficient in answer.items()
        if coefficient
    }


def multiply(*polynomials: dict[int, int]) -> dict[int, int]:
    answer = {0: 1}
    for polynomial in polynomials:
        product: dict[int, int] = {}
        for first, first_coefficient in answer.items():
            for second, second_coefficient in polynomial.items():
                monomial = first ^ second
                product[monomial] = (
                    product.get(monomial, 0)
                    + first_coefficient * second_coefficient
                )
        answer = product
    return answer


def tangent_coefficients(
    parameters: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    denominators = [affine(row) for row in parameters[:HEADS]]
    numerators = [affine(row) for row in parameters[HEADS:]]
    answer: dict[int, int] = {}
    for head in range(HEADS):
        term = multiply(
            numerators[head],
            *[
                denominators[other]
                for other in range(HEADS)
                if other != head
            ],
        )
        for monomial, coefficient in term.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
    return tuple(answer.get(monomial, 0) for monomial in OUTPUT_MONOMIALS)


def jacobian(
    parameters: tuple[tuple[int, ...], ...],
) -> list[list[int]]:
    denominators = [affine(row) for row in parameters[:HEADS]]
    numerators = [affine(row) for row in parameters[HEADS:]]
    columns: list[list[int]] = []

    for denominator in range(HEADS):
        for coordinate in range(WIDTH):
            terms = []
            for numerator in range(HEADS):
                if numerator == denominator:
                    continue
                terms.append(
                    multiply(
                        numerators[numerator],
                        basis(coordinate),
                        *[
                            denominators[other]
                            for other in range(HEADS)
                            if other not in (numerator, denominator)
                        ],
                    )
                )
            derivative = add(*terms)
            columns.append(
                [
                    derivative.get(monomial, 0)
                    for monomial in OUTPUT_MONOMIALS
                ]
            )

    for numerator in range(HEADS):
        for coordinate in range(WIDTH):
            derivative = multiply(
                basis(coordinate),
                *[
                    denominators[other]
                    for other in range(HEADS)
                    if other != numerator
                ],
            )
            columns.append(
                [
                    derivative.get(monomial, 0)
                    for monomial in OUTPUT_MONOMIALS
                ]
            )
    return [list(row) for row in zip(*columns)]


def gauge_vectors(
    parameters: tuple[tuple[int, ...], ...],
) -> list[list[int]]:
    vectors: list[list[int]] = []

    for denominator in range(HEADS):
        vector = [0] * (2 * HEADS * WIDTH)
        start = denominator * WIDTH
        vector[start : start + WIDTH] = parameters[denominator]
        for numerator in range(HEADS):
            if numerator == denominator:
                continue
            start = (HEADS + numerator) * WIDTH
            vector[start : start + WIDTH] = [
                -coefficient
                for coefficient in parameters[HEADS + numerator]
            ]
        vectors.append(vector)

    for numerator in range(1, HEADS):
        vector = [0] * (2 * HEADS * WIDTH)
        first_start = HEADS * WIDTH
        second_start = (HEADS + numerator) * WIDTH
        vector[first_start : first_start + WIDTH] = parameters[0]
        vector[second_start : second_start + WIDTH] = [
            -coefficient for coefficient in parameters[numerator]
        ]
        vectors.append(vector)
    return vectors


def tangent_sample_mod_prime(state: int) -> tuple[int, np.ndarray]:
    parameters = np.empty((2 * HEADS, WIDTH), dtype=np.int64)
    for factor in range(2 * HEADS):
        for coordinate in range(WIDTH):
            state, value = cubic.lcg(state)
            parameters[factor, coordinate] = value % SAMPLE_PRIME

    answer = np.zeros(len(OUTPUT_MONOMIALS), dtype=np.int64)
    denominators = parameters[:HEADS]
    numerators = parameters[HEADS:]
    for head in range(HEADS):
        other = [index for index in range(HEADS) if index != head]
        for first in range(WIDTH):
            for second in range(WIDTH):
                for third in range(WIDTH):
                    partial = (
                        int(numerators[head, first])
                        * int(denominators[other[0], second])
                        * int(denominators[other[1], third])
                    )
                    mask = (
                        AFFINE_MONOMIALS[first]
                        ^ AFFINE_MONOMIALS[second]
                        ^ AFFINE_MONOMIALS[third]
                    )
                    for fourth in range(WIDTH):
                        monomial = mask ^ AFFINE_MONOMIALS[fourth]
                        answer[OUTPUT_INDEX[monomial]] += (
                            partial
                            * int(denominators[other[2], fourth])
                        )
    return state, answer % SAMPLE_PRIME


def verify_linear_span() -> int:
    state = 12_345
    samples = []
    for _ in range(100):
        state, coefficients = tangent_sample_mod_prime(state)
        samples.append(coefficients)
    rank = cubic.modular_rank(samples, SAMPLE_PRIME)
    assert rank == 57
    return rank


def verify() -> tuple[int, int, int]:
    assert len(OUTPUT_MONOMIALS) == 57
    assert all(
        denominator[0] > sum(denominator[1:])
        and all(coefficient > 0 for coefficient in denominator[1:])
        for denominator in WITNESS[:HEADS]
    )

    matrix = jacobian(WITNESS)
    rank = cubic.modular_rank(matrix, JACOBIAN_PRIME)
    assert rank == 49

    gauges = gauge_vectors(WITNESS)
    gauge_rank = cubic.modular_rank(gauges, JACOBIAN_PRIME)
    assert gauge_rank == 7
    product = np.array(matrix, dtype=object) @ np.array(gauges, dtype=object).T
    assert np.all(product == 0)

    direct = tangent_coefficients(WITNESS)
    assert len(direct) == 57
    linear_rank = verify_linear_span()
    return rank, gauge_rank, linear_rank


def main() -> None:
    rank, gauge_rank, linear_rank = verify()
    print(f"positive-orientation Jacobian rank: {rank} of 57")
    print(f"universal gauge rank: {gauge_rank}")
    print("quartic tangent closure dimension: 49")
    print(f"finite-field linear span rank: {linear_rank} of 57")


if __name__ == "__main__":
    main()
