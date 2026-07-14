#!/usr/bin/env python3
"""Verify exact dimension facts for cleared three-head cubic forms.

Work in the Boolean quotient x_i^2 = x_i.  After absorbing the constant
readout term into one numerator, the order-three tangent map is

    Phi(D, A) = A1 D2 D3 + A2 D1 D3 + A3 D1 D2,

where all six factors are affine.  This script proves by modular Jacobian
minors that:

1. on five variables, the image is Zariski dense in all degree-at-most-three
   multilinear polynomials;
2. on six variables, its affine Zariski closure has dimension exactly 37 and
   hence codimension five in the 42-dimensional coefficient space;
3. the six-variable image has no nonzero homogeneous quadratic equation over
   the rationals;
4. positive-orientation tangent forms linearly span the full 42-dimensional
   coefficient space, so orientation supplies no nontrivial linear inequality.

The Jacobian witnesses use three strictly positive-orientation denominators.
Thus imposing any fixed admissible orientation tuple creates no new algebraic
equation: its real parameter region is Euclidean open, hence Zariski dense,
and already attains the unrestricted image dimension.  Orientation can only
contribute semialgebraic inequalities.  The first two checks also exhibit and
verify the five universal infinitesimal gauge directions.  Everything is
checked over finite prime fields using only integer arithmetic.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np


JACOBIAN_PRIME = 1_000_003
QUADRATIC_PRIME = 101


WITNESSES = {
    5: (
        (4, 7, 8, 12, 5, 4),
        (9, 5, 4, 3, 3, 8),
        (3, 6, 12, 12, 4, 2),
        (10, 3, 5, -10, -8, 9),
        (-5, -8, -2, -12, 11, 8),
        (-1, -5, -11, -8, -4, 7),
    ),
    6: (
        (7, 11, 3, 11, 5, 7, 11),
        (9, 2, 12, 7, 9, 1, 10),
        (12, 7, 1, 11, 9, 1, 1),
        (9, 4, 3, -5, -11, -9, 8),
        (12, 6, 0, -12, -2, 4, -6),
        (-5, -3, -11, -9, 12, -1, -8),
    ),
}


def monomials(dimension: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << index for index in subset)
        for degree in range(4)
        for subset in combinations(range(dimension), degree)
    )


def affine(coefficients: tuple[int, ...]) -> dict[int, int]:
    return {
        **{0: coefficients[0]},
        **{
            1 << (index - 1): coefficients[index]
            for index in range(1, len(coefficients))
        },
    }


def basis(coordinate: int) -> dict[int, int]:
    if coordinate == 0:
        return {0: 1}
    return {1 << (coordinate - 1): 1}


def add(*polynomials: dict[int, int]) -> dict[int, int]:
    answer: dict[int, int] = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def multiply(*polynomials: dict[int, int]) -> dict[int, int]:
    answer = {0: 1}
    for polynomial in polynomials:
        product: dict[int, int] = {}
        for first, first_coefficient in answer.items():
            for second, second_coefficient in polynomial.items():
                monomial = first | second
                product[monomial] = (
                    product.get(monomial, 0)
                    + first_coefficient * second_coefficient
                )
        answer = product
    return answer


def jacobian(dimension: int) -> list[list[int]]:
    values = WITNESSES[dimension]
    denominators = [affine(row) for row in values[:3]]
    numerators = [affine(row) for row in values[3:]]
    output_monomials = monomials(dimension)
    columns: list[list[int]] = []

    for factor in range(3):
        other = [index for index in range(3) if index != factor]
        for coordinate in range(dimension + 1):
            derivative = add(
                multiply(
                    numerators[other[0]],
                    basis(coordinate),
                    denominators[other[1]],
                ),
                multiply(
                    numerators[other[1]],
                    basis(coordinate),
                    denominators[other[0]],
                ),
            )
            columns.append([
                derivative.get(monomial, 0) for monomial in output_monomials
            ])

    for factor in range(3):
        other = [index for index in range(3) if index != factor]
        for coordinate in range(dimension + 1):
            derivative = multiply(
                basis(coordinate),
                denominators[other[0]],
                denominators[other[1]],
            )
            columns.append([
                derivative.get(monomial, 0) for monomial in output_monomials
            ])

    return [list(row) for row in zip(*columns)]


def modular_rank(matrix: list[list[int]] | np.ndarray, prime: int) -> int:
    work = np.array(matrix, dtype=np.int64) % prime
    rows, columns = work.shape
    pivot_row = 0
    for column in range(columns):
        candidates = np.flatnonzero(work[pivot_row:, column])
        if len(candidates) == 0:
            continue
        pivot = pivot_row + int(candidates[0])
        work[[pivot_row, pivot]] = work[[pivot, pivot_row]]
        inverse = pow(int(work[pivot_row, column]), prime - 2, prime)
        work[pivot_row] = work[pivot_row] * inverse % prime
        for row in range(rows):
            if row == pivot_row or work[row, column] == 0:
                continue
            multiplier = int(work[row, column])
            work[row] = (work[row] - multiplier * work[pivot_row]) % prime
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def gauge_vectors(dimension: int) -> list[list[int]]:
    values = WITNESSES[dimension]
    width = dimension + 1
    vectors: list[list[int]] = []

    for scaled_denominator in range(3):
        vector = [0] * (6 * width)
        start = scaled_denominator * width
        vector[start:start + width] = values[scaled_denominator]
        for numerator in range(3):
            if numerator == scaled_denominator:
                continue
            start = (3 + numerator) * width
            vector[start:start + width] = [
                -coefficient for coefficient in values[3 + numerator]
            ]
        vectors.append(vector)

    for first, second in ((0, 1), (0, 2)):
        vector = [0] * (6 * width)
        first_start = (3 + first) * width
        second_start = (3 + second) * width
        vector[first_start:first_start + width] = values[first]
        vector[second_start:second_start + width] = [
            -coefficient for coefficient in values[second]
        ]
        vectors.append(vector)

    return vectors


def verify_jacobian_dimensions() -> None:
    for dimension, expected_rank in ((5, 26), (6, 37)):
        assert all(
            coefficient > 0
            for denominator in WITNESSES[dimension][:3]
            for coefficient in denominator
        )
        matrix = jacobian(dimension)
        rank = modular_rank(matrix, JACOBIAN_PRIME)
        assert rank == expected_rank

        gauges = gauge_vectors(dimension)
        assert modular_rank(gauges, JACOBIAN_PRIME) == 5
        product = np.array(matrix, dtype=object) @ np.array(gauges, dtype=object).T
        assert np.all(product == 0)

        target_dimension = len(monomials(dimension))
        parameter_upper_bound = 6 * (dimension + 1) - 5
        assert rank <= min(target_dimension, parameter_upper_bound)
        print(
            f"n={dimension}: positive-orientation Jacobian rank {rank} "
            f"in target dimension {target_dimension}"
        )


def tangent_coefficients(
    parameters: tuple[tuple[int, ...], ...], dimension: int
) -> list[int]:
    denominators = [affine(row) for row in parameters[:3]]
    numerators = [affine(row) for row in parameters[3:]]
    answer: dict[int, int] = {}
    for factor in range(3):
        other = [index for index in range(3) if index != factor]
        term = multiply(
            numerators[factor],
            denominators[other[0]],
            denominators[other[1]],
        )
        for monomial, coefficient in term.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
    return [answer.get(monomial, 0) for monomial in monomials(dimension)]


def verify_positive_orientation_linear_span() -> None:
    state = 12_345
    samples = []
    for _ in range(100):
        parameters = []
        for factor in range(6):
            row = []
            for _ in range(7):
                state, value = lcg(state)
                if factor < 3:
                    row.append(1 + value % 17)
                else:
                    row.append(int(value % 31) - 15)
            parameters.append(tuple(row))
        assert all(
            coefficient > 0
            for denominator in parameters[:3]
            for coefficient in denominator
        )
        samples.append(tangent_coefficients(tuple(parameters), 6))
    rank = modular_rank(samples, JACOBIAN_PRIME)
    assert rank == 42
    print("n=6: positive-orientation linear span rank 42 of 42")


def lcg(state: int) -> tuple[int, int]:
    state = (1_664_525 * state + 1_013_904_223) & 0xFFFFFFFF
    return state, state


def tangent_sample_mod_prime(state: int) -> tuple[int, np.ndarray]:
    dimension = 6
    output_monomials = monomials(dimension)
    output_index = {
        monomial: index for index, monomial in enumerate(output_monomials)
    }
    parameters = np.empty((6, dimension + 1), dtype=np.int64)
    for factor in range(6):
        for coordinate in range(dimension + 1):
            state, value = lcg(state)
            parameters[factor, coordinate] = value % QUADRATIC_PRIME

    answer = np.zeros(len(output_monomials), dtype=np.int64)
    denominators = parameters[:3]
    numerators = parameters[3:]
    for factor in range(3):
        other = [index for index in range(3) if index != factor]
        for first in range(dimension + 1):
            first_monomial = 0 if first == 0 else 1 << (first - 1)
            for second in range(dimension + 1):
                second_monomial = 0 if second == 0 else 1 << (second - 1)
                for third in range(dimension + 1):
                    third_monomial = 0 if third == 0 else 1 << (third - 1)
                    monomial = first_monomial | second_monomial | third_monomial
                    answer[output_index[monomial]] += (
                        numerators[factor, first]
                        * denominators[other[0], second]
                        * denominators[other[1], third]
                    )
    return state, answer % QUADRATIC_PRIME


def verify_no_quadratic_equations() -> None:
    coordinate_count = len(monomials(6))
    pairs = np.triu_indices(coordinate_count)
    quadratic_count = len(pairs[0])
    samples = np.empty((1_000, quadratic_count), dtype=np.int64)
    state = 0xC0FFEE
    for sample in range(len(samples)):
        state, coefficients = tangent_sample_mod_prime(state)
        samples[sample] = (
            coefficients[:, None] * coefficients[None, :]
        )[pairs] % QUADRATIC_PRIME
    rank = modular_rank(samples, QUADRATIC_PRIME)
    assert rank == quadratic_count == 903
    print("n=6: homogeneous quadratic evaluation rank 903 of 903")


def main() -> None:
    verify_jacobian_dimensions()
    verify_positive_orientation_linear_span()
    verify_no_quadratic_equations()
    print("verified cubic tangent dimension certificates")


if __name__ == "__main__":
    main()
