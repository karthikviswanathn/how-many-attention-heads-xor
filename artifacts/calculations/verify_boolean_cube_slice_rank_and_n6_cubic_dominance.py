#!/usr/bin/env python3
"""Verify Theorem 191 and an exact six-bit cubic dominance witness.

Everything is computed with Python integers and modular Gaussian elimination.
The first check constructs the plane

    U_0 = span(1, x_0 + ... + x_{n-1})

in the Boolean quotient x_i^2 = x_i.  On a small grid it verifies the rank

    min(D_H, 2 D_{H-1} - D_{H-2})

and checks the explicit D_{H-2}-dimensional Koszul kernel family.

The second check stores an integer point in the standard affine chart on
Gr(2, 7).  It reconstructs the coefficient-map Jacobian by exact finite
differences and proves rank 42 modulo the prime 1,000,003.  Since the target
has dimension 42, the corresponding integer Jacobian has exact rank 42.
"""

from __future__ import annotations

from itertools import combinations
from math import comb
from typing import Iterable, Sequence


PRIME = 1_000_003
GRID_MAX_N = 7

WITNESS_N = 6
WITNESS_H = 3

# The chart rows represent affine forms with coefficient order
# (constant, x_0, x_1, ..., x_5).  The pivot columns are constant and x_0:
#
#     L_1 = 1 + sum_{j=1}^5 T[0][j-1] x_j,
#     L_2 = x_0 + sum_{j=1}^5 T[1][j-1] x_j.
WITNESS_T = (
    (-1, -1, 0, 0, -1),
    (-1, 0, 0, -1, -1),
)

# Coefficients use squarefree monomials ordered first by degree and then by
# itertools.combinations(range(6), degree).
WITNESS_C1 = (
    -2,
    2,
    -2,
    2,
    2,
    -2,
    2,
    0,
    0,
    1,
    -2,
    0,
    -1,
    1,
    -2,
    1,
    1,
    2,
    0,
    2,
    2,
    -2,
)

WITNESS_C2 = (
    2,
    -1,
    0,
    -1,
    -2,
    1,
    2,
    -1,
    1,
    2,
    1,
    1,
    2,
    1,
    0,
    -1,
    0,
    -1,
    0,
    -1,
    -1,
    0,
)

EXPECTED_WITNESS_PIVOTS = (
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    26,
    27,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    39,
    40,
    41,
    45,
    46,
    48,
)
EXPECTED_WITNESS_DETERMINANT = 534_528


def popcount(mask: int) -> int:
    return mask.bit_count()


def monomial_masks(n: int, maximum_degree: int) -> tuple[int, ...]:
    """Squarefree masks in degree-lexicographic order."""
    return tuple(
        sum(1 << coordinate for coordinate in subset)
        for degree in range(min(maximum_degree, n) + 1)
        for subset in combinations(range(n), degree)
    )


def dimension(n: int, maximum_degree: int) -> int:
    return sum(
        comb(n, degree)
        for degree in range(min(maximum_degree, n) + 1)
    )


def affine_times_monomial(
    n: int,
    affine: Sequence[int],
    monomial: int,
) -> dict[int, int]:
    """Return affine * x_monomial in the Boolean quotient."""
    assert len(affine) == n + 1
    answer: dict[int, int] = {}
    if affine[0] != 0:
        answer[monomial] = affine[0]
    for coordinate, coefficient in enumerate(affine[1:]):
        if coefficient == 0:
            continue
        output = monomial | (1 << coordinate)
        answer[output] = answer.get(output, 0) + coefficient
    return {mask: value for mask, value in answer.items() if value != 0}


def multiplication_matrix(
    n: int,
    maximum_degree: int,
    affine_forms: Iterable[Sequence[int]],
) -> list[list[int]]:
    """Matrix whose columns are L_a x_S for all forms and domain masks."""
    domain = monomial_masks(n, maximum_degree - 1)
    target = monomial_masks(n, maximum_degree)
    target_index = {mask: index for index, mask in enumerate(target)}
    columns: list[list[int]] = []
    for affine in affine_forms:
        for monomial in domain:
            column = [0] * len(target)
            for output, coefficient in affine_times_monomial(
                n, affine, monomial
            ).items():
                assert popcount(output) <= maximum_degree
                column[target_index[output]] += coefficient
            columns.append(column)
    return [
        [columns[column][row] for column in range(len(columns))]
        for row in range(len(target))
    ]


def modular_rank_and_pivots(
    matrix: Sequence[Sequence[int]], prime: int = PRIME
) -> tuple[int, tuple[int, ...]]:
    """Return rank and pivot columns over the prime field."""
    if not matrix:
        return 0, ()
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    assert all(len(row) == columns for row in work)
    rank = 0
    pivots: list[int] = []
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, rows)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], prime - 2, prime)
        work[rank] = [value * inverse % prime for value in work[rank]]
        for row in range(rank + 1, rows):
            multiplier = work[row][column]
            if multiplier == 0:
                continue
            work[row] = [
                (left - multiplier * right) % prime
                for left, right in zip(work[row], work[rank])
            ]
        pivots.append(column)
        rank += 1
        if rank == rows:
            break
    return rank, tuple(pivots)


def determinant_mod(
    matrix: Sequence[Sequence[int]], prime: int = PRIME
) -> int:
    """Exact determinant reduced modulo prime."""
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    work = [[value % prime for value in row] for row in matrix]
    determinant = 1
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        for row in range(column + 1, size):
            if work[row][column] == 0:
                continue
            multiplier = work[row][column] * inverse % prime
            for entry in range(column, size):
                work[row][entry] = (
                    work[row][entry]
                    - multiplier * work[column][entry]
                ) % prime
    return determinant % prime


def transpose(columns: Sequence[Sequence[int]]) -> list[list[int]]:
    if not columns:
        return []
    return [
        [columns[column][row] for column in range(len(columns))]
        for row in range(len(columns[0]))
    ]


def matrix_vector_product(
    matrix: Sequence[Sequence[int]], vector: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        sum(left * right for left, right in zip(row, vector))
        for row in matrix
    )


def koszul_kernel_vectors(n: int, maximum_degree: int) -> list[list[int]]:
    """Vectors (L_2 R, -L_1 R) for the explicit plane U_0."""
    domain = monomial_masks(n, maximum_degree - 1)
    domain_index = {mask: index for index, mask in enumerate(domain)}
    kernel_domain = monomial_masks(n, maximum_degree - 2)
    constant = (1,) + (0,) * n
    coordinate_sum = (0,) + (1,) * n
    vectors: list[list[int]] = []
    for monomial in kernel_domain:
        vector = [0] * (2 * len(domain))
        for output, coefficient in affine_times_monomial(
            n, coordinate_sum, monomial
        ).items():
            vector[domain_index[output]] += coefficient
        for output, coefficient in affine_times_monomial(
            n, constant, monomial
        ).items():
            vector[len(domain) + domain_index[output]] -= coefficient
        vectors.append(vector)
    return vectors


def verify_rank_formula_grid() -> int:
    checks = 0
    for n in range(2, GRID_MAX_N + 1):
        for maximum_degree in range(2, n + 1):
            constant = (1,) + (0,) * n
            coordinate_sum = (0,) + (1,) * n
            matrix = multiplication_matrix(
                n, maximum_degree, (constant, coordinate_sum)
            )
            rank, _ = modular_rank_and_pivots(matrix)
            expected = min(
                dimension(n, maximum_degree),
                2 * dimension(n, maximum_degree - 1)
                - dimension(n, maximum_degree - 2),
            )
            assert rank == expected, (n, maximum_degree, rank, expected)

            kernel_vectors = koszul_kernel_vectors(n, maximum_degree)
            assert all(
                not any(matrix_vector_product(matrix, vector))
                for vector in kernel_vectors
            )
            kernel_rank, _ = modular_rank_and_pivots(
                transpose(kernel_vectors)
            )
            expected_kernel_rank = dimension(n, maximum_degree - 2)
            assert kernel_rank == expected_kernel_rank

            saturated = rank == dimension(n, maximum_degree)
            expected_saturated = maximum_degree >= (n + 2) // 2
            assert saturated == expected_saturated
            if not saturated:
                expected_codimension = comb(n, maximum_degree) - comb(
                    n, maximum_degree - 1
                )
                assert dimension(n, maximum_degree) - rank == (
                    expected_codimension
                )

            print(
                f"grid n={n} H={maximum_degree}: "
                f"rank={rank}, formula={expected}, "
                f"Koszul={kernel_rank}, saturated={str(saturated).lower()}"
            )
            checks += 1
    return checks


def witness_affine_forms(
    chart: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    assert len(chart) == 2
    assert all(len(row) == WITNESS_N - 1 for row in chart)
    first = (1, 0) + tuple(chart[0])
    second = (0, 1) + tuple(chart[1])
    return first, second


def slice_value(
    chart: Sequence[Sequence[int]],
    coefficients_1: Sequence[int],
    coefficients_2: Sequence[int],
) -> tuple[int, ...]:
    domain = monomial_masks(WITNESS_N, WITNESS_H - 1)
    target = monomial_masks(WITNESS_N, WITNESS_H)
    target_index = {mask: index for index, mask in enumerate(target)}
    assert len(coefficients_1) == len(coefficients_2) == len(domain)
    answer = [0] * len(target)
    for affine, coefficients in zip(
        witness_affine_forms(chart),
        (coefficients_1, coefficients_2),
    ):
        for monomial, polynomial_coefficient in zip(domain, coefficients):
            if polynomial_coefficient == 0:
                continue
            for output, affine_coefficient in affine_times_monomial(
                WITNESS_N, affine, monomial
            ).items():
                answer[target_index[output]] += (
                    polynomial_coefficient * affine_coefficient
                )
    return tuple(answer)


def witness_jacobian() -> list[list[int]]:
    """Build the 42 by 54 integer Jacobian by exact finite differences."""
    chart = [list(row) for row in WITNESS_T]
    coefficients_1 = list(WITNESS_C1)
    coefficients_2 = list(WITNESS_C2)
    base = slice_value(chart, coefficients_1, coefficients_2)
    columns: list[list[int]] = []
    chart_parameters = 2 * (WITNESS_N - 1)
    coefficient_parameters = len(coefficients_1)
    for parameter in range(
        chart_parameters + 2 * coefficient_parameters
    ):
        changed_chart = [row.copy() for row in chart]
        changed_1 = coefficients_1.copy()
        changed_2 = coefficients_2.copy()
        if parameter < chart_parameters:
            row, column = divmod(parameter, WITNESS_N - 1)
            changed_chart[row][column] += 1
        elif parameter < chart_parameters + coefficient_parameters:
            changed_1[parameter - chart_parameters] += 1
        else:
            changed_2[
                parameter - chart_parameters - coefficient_parameters
            ] += 1
        changed_value = slice_value(changed_chart, changed_1, changed_2)
        columns.append(
            [changed - original for changed, original in zip(changed_value, base)]
        )
    return transpose(columns)


def verify_n6_cubic_witness() -> tuple[tuple[int, ...], int]:
    assert len(WITNESS_C1) == len(WITNESS_C2) == dimension(6, 2) == 22
    jacobian = witness_jacobian()
    assert len(jacobian) == dimension(6, 3) == 42
    assert all(len(row) == 54 for row in jacobian)
    rank, pivots = modular_rank_and_pivots(jacobian)
    assert rank == 42
    assert pivots == EXPECTED_WITNESS_PIVOTS
    pivot_minor = [[row[column] for column in pivots] for row in jacobian]
    determinant = determinant_mod(pivot_minor)
    assert determinant == EXPECTED_WITNESS_DETERMINANT != 0
    print("verified exact n=6, H=3 slice-incidence dominance witness")
    print(f"Jacobian shape={len(jacobian)}x{len(jacobian[0])}")
    print(f"Jacobian rank modulo {PRIME}={rank}")
    print(f"pivot columns={pivots}")
    print(f"pivot determinant modulo {PRIME}={determinant}")
    return pivots, determinant


def main() -> None:
    checks = verify_rank_formula_grid()
    print(f"verified Theorem 191 rank formula on {checks} grid points")
    verify_n6_cubic_witness()


if __name__ == "__main__":
    main()
