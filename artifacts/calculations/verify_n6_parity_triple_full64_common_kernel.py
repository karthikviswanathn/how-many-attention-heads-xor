#!/usr/bin/env python3
"""Verify the exact common kernel of all full-cube literal corners."""

from __future__ import annotations

import itertools


N = 6
VERTICES = 1 << N
MASK = 0x96696BD669B69669
EXCEPTIONS = (21, 38, 41)
PRIME = 1000003


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def parity(code: int) -> int:
    return character(VERTICES - 1, code)


def modular_rank(matrix: list[list[int]], prime: int = PRIME) -> int:
    work = [[value % prime for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if row_count else 0
    pivot_row = 0
    for column in range(column_count):
        chosen = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if chosen is None:
            continue
        work[pivot_row], work[chosen] = work[chosen], work[pivot_row]
        inverse = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [
            value * inverse % prime for value in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                (left - multiplier * right) % prime
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def literal_product(code: int, subset: tuple[int, ...]) -> int:
    return_val = 1
    for coordinate in subset:
        return_val *= 1 - character(1 << coordinate, code)
    return return_val


def stacked_columns() -> list[list[int]]:
    subsets = tuple(
        subset
        for size in range(5)
        for subset in itertools.combinations(range(N), size)
    )
    assert len(subsets) == 57
    return [
        [
            *(
                target_sign(code) * literal_product(code, subset)
                for subset in subsets
            ),
            parity(code),
        ]
        for code in range(VERTICES)
    ]


def common_kernel_basis() -> list[list[int]]:
    exception_sum = tuple(
        sum(character(1 << coordinate, code) for code in EXCEPTIONS)
        for coordinate in range(N)
    )
    assert exception_sum == (-1, 1, -1, 1, 1, -1)
    basis = []
    for coordinate in range(N):
        current = []
        for code in range(VERTICES):
            defect = target_sign(code) * parity(code)
            linear = (
                3 * character(1 << coordinate, code)
                - exception_sum[coordinate]
            )
            current.append(defect * linear)
        basis.append(current)
    return basis


def verify() -> None:
    columns = stacked_columns()
    assert modular_rank(columns) == 58
    basis = common_kernel_basis()
    assert modular_rank([list(row) for row in zip(*basis)]) == 6
    for vector in basis:
        for column in range(58):
            assert sum(
                vector[code] * columns[code][column]
                for code in range(VERTICES)
            ) == 0


def main() -> None:
    verify()
    print("stacked literal-corner rank: 58 of 64")
    print("exact common-kernel dimension: 6")
    print("verified six affine-defect basis vectors")


if __name__ == "__main__":
    main()
