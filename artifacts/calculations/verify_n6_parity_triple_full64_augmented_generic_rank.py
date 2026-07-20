#!/usr/bin/env python3
"""Verify a full-rank interior point in every H4 orientation branch.

The augmented matrix has the 25 cleared tangent columns from the full-cube
route and the parity column.  A rank of 26 modulo a prime proves rank 26 over
the rationals because the integer matrix has exactly 26 columns.
"""

from __future__ import annotations

import itertools


N = 6
HEADS = 4
VERTICES = 1 << N
MASK = 0x96696BD669B69669
PRIME = 1_000_003
SLOPES = (
    (1, 2, 3, 4, 5, 6),
    (2, 3, 5, 7, 11, 13),
    (1, 4, 9, 16, 25, 36),
    (3, 5, 8, 13, 21, 34),
)


def sign_coordinate(code: int, coordinate: int) -> int:
    return -1 if (code >> coordinate) & 1 else 1


def parity(code: int) -> int:
    return -1 if code.bit_count() % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def denominator_values(
    orientation: int,
    slopes: tuple[int, ...],
) -> tuple[int, ...]:
    intercept = 1 + sum(slopes)
    values = tuple(
        intercept
        + orientation
        * sum(
            slopes[coordinate] * sign_coordinate(code, coordinate)
            for coordinate in range(N)
        )
        for code in range(VERTICES)
    )
    assert min(values) == 1
    return values


def augmented_matrix(positive_heads: int) -> list[list[int]]:
    orientations = (1,) * positive_heads + (-1,) * (HEADS - positive_heads)
    denominators = tuple(
        denominator_values(orientation, SLOPES[head])
        for head, orientation in enumerate(orientations)
    )
    rows = []
    for code in range(VERTICES):
        product = 1
        for head in range(HEADS):
            product *= denominators[head][code]
        signed = target_sign(code)
        row = [signed * product]
        for head in range(HEADS):
            partial = product // denominators[head][code]
            row.extend(
                signed * sign_coordinate(code, coordinate) * partial
                for coordinate in range(N)
            )
        row.append(parity(code))
        assert len(row) == 26
        rows.append(row)
    return rows


def modular_rank(matrix: list[list[int]], prime: int) -> int:
    current = [[value % prime for value in row] for row in matrix]
    row_count = len(current)
    column_count = len(current[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if current[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        current[pivot_row], current[pivot] = current[pivot], current[pivot_row]
        inverse = pow(current[pivot_row][column], -1, prime)
        current[pivot_row] = [
            value * inverse % prime for value in current[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or current[row][column] == 0:
                continue
            multiplier = current[row][column]
            current[row] = [
                (left - multiplier * right) % prime
                for left, right in zip(current[row], current[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def main() -> None:
    assert len(set(itertools.chain.from_iterable(SLOPES))) > N
    for positive_heads in range(3):
        matrix = augmented_matrix(positive_heads)
        rank = modular_rank(matrix, PRIME)
        assert rank == 26
        print(
            f"orientation count {positive_heads}: "
            f"augmented rank={rank} modulo {PRIME}"
        )
    print("verified a rank-26 strict interior tuple in every orientation branch")


if __name__ == "__main__":
    main()
