#!/usr/bin/env python3
"""Verify an exact dominant chart for five-bit cubic tangent spaces.

Work in the Boolean quotient x_i^2 = x_i.  For affine forms A_h and B_h,
the cleared three-head polynomial is

    Phi(B, A) = sum_h A_h product_{k != h} B_k.

The script evaluates Phi at one integer point with strictly admissible B_h
and checks two exact ranks modulo a prime.  The numerator variables alone
span every squarefree cubic leading part.  The full parameter Jacobian has
rank 26, the dimension of all degree-at-most-three five-bit polynomials.
"""

from __future__ import annotations

from typing import Iterable


N = 5
HEADS = 3
WIDTH = N + 1
PRIME = 1_000_003


def popcount(mask: int) -> int:
    return bin(mask).count("1")


MONOMIALS = tuple(
    mask for mask in range(1 << N) if popcount(mask) <= 3
)

# Every coefficient of each B_h is positive.  Hence every B_h is strictly
# positive on the Boolean cube and lies in the interior positive orientation
# chart of admissible attention denominators.
DENOMINATORS = (
    (7, 1, 2, 3, 5, 8),
    (11, 2, 3, 5, 7, 11),
    (13, 3, 4, 7, 9, 14),
)

NUMERATORS = (
    (1, -2, 3, -1, 2, -3),
    (-2, 1, -1, 4, -2, 1),
    (3, 2, -4, 1, 1, -2),
)

EXPECTED_VALUE = (
    192,
    -8,
    175,
    41,
    848,
    87,
    441,
    39,
    804,
    97,
    285,
    32,
    1215,
    77,
    211,
    -1455,
    -457,
    -466,
    -38,
    469,
    -25,
    116,
    -541,
    -84,
    -82,
    341,
)

EXPECTED_FULL_PIVOTS = (
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
    24,
    25,
    26,
)

EXPECTED_TOP_PIVOTS = (1, 2, 3, 4, 5, 7, 8, 9, 10, 13)


def affine_polynomial(coefficients: Iterable[int]) -> list[int]:
    coefficients = tuple(coefficients)
    assert len(coefficients) == WIDTH
    answer = [0] * (1 << N)
    answer[0] = coefficients[0]
    for coordinate in range(N):
        answer[1 << coordinate] = coefficients[coordinate + 1]
    return answer


def boolean_product(left: list[int], right: list[int]) -> list[int]:
    """Multiply with x_i^2 = x_i, so monomial masks combine by OR."""
    answer = [0] * (1 << N)
    for left_mask, left_value in enumerate(left):
        if left_value == 0:
            continue
        for right_mask, right_value in enumerate(right):
            if right_value != 0:
                answer[left_mask | right_mask] += left_value * right_value
    return answer


def tangent_value(
    denominators: Iterable[Iterable[int]],
    numerators: Iterable[Iterable[int]],
) -> tuple[int, ...]:
    denominator_polynomials = [
        affine_polynomial(row) for row in denominators
    ]
    numerator_polynomials = [
        affine_polynomial(row) for row in numerators
    ]
    answer = [0] * (1 << N)
    for head in range(HEADS):
        others = [index for index in range(HEADS) if index != head]
        term = boolean_product(
            numerator_polynomials[head],
            boolean_product(
                denominator_polynomials[others[0]],
                denominator_polynomials[others[1]],
            ),
        )
        answer = [left + right for left, right in zip(answer, term)]
    assert all(
        answer[mask] == 0
        for mask in range(1 << N)
        if popcount(mask) > 3
    )
    return tuple(answer[mask] for mask in MONOMIALS)


def parameter_jacobian() -> list[list[int]]:
    denominators = [list(row) for row in DENOMINATORS]
    numerators = [list(row) for row in NUMERATORS]
    base = tangent_value(denominators, numerators)
    columns = []
    for parameter in range(2 * HEADS * WIDTH):
        perturbed_denominators = [row.copy() for row in denominators]
        perturbed_numerators = [row.copy() for row in numerators]
        if parameter < HEADS * WIDTH:
            head, coordinate = divmod(parameter, WIDTH)
            perturbed_denominators[head][coordinate] += 1
        else:
            head, coordinate = divmod(
                parameter - HEADS * WIDTH, WIDTH
            )
            perturbed_numerators[head][coordinate] += 1
        perturbed = tangent_value(
            perturbed_denominators, perturbed_numerators
        )
        columns.append(
            [perturbed[row] - base[row] for row in range(len(MONOMIALS))]
        )
    return [
        [columns[column][row] for column in range(len(columns))]
        for row in range(len(MONOMIALS))
    ]


def modular_rank_and_pivots(
    matrix: list[list[int]], prime: int = PRIME
) -> tuple[int, tuple[int, ...]]:
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    pivots = []
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
        for row in range(rows):
            if row == rank or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                (left - multiplier * right) % prime
                for left, right in zip(work[row], work[rank])
            ]
        pivots.append(column)
        rank += 1
        if rank == rows:
            break
    return rank, tuple(pivots)


def main() -> None:
    value = tangent_value(DENOMINATORS, NUMERATORS)
    assert value == EXPECTED_VALUE
    jacobian = parameter_jacobian()

    numerator_start = HEADS * WIDTH
    numerator_jacobian = [row[numerator_start:] for row in jacobian]
    numerator_rank, _ = modular_rank_and_pivots(numerator_jacobian)
    assert numerator_rank == 16

    cubic_rows = [
        row
        for row, mask in enumerate(MONOMIALS)
        if popcount(mask) == 3
    ]
    cubic_numerator_jacobian = [
        numerator_jacobian[row] for row in cubic_rows
    ]
    top_rank, top_pivots = modular_rank_and_pivots(
        cubic_numerator_jacobian
    )
    assert top_rank == 10
    assert top_pivots == EXPECTED_TOP_PIVOTS

    full_rank, full_pivots = modular_rank_and_pivots(jacobian)
    assert full_rank == len(MONOMIALS) == 26
    assert full_pivots == EXPECTED_FULL_PIVOTS

    print("verified exact five-bit cubic tangent dominance")
    print(f"numerator rank={numerator_rank}")
    print(f"top cubic rank={top_rank}")
    print(f"full parameter Jacobian rank={full_rank}")


if __name__ == "__main__":
    main()
