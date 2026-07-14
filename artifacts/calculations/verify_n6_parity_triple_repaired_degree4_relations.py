#!/usr/bin/env python3
"""Verify degree-four evaluation relations on repaired supports.

For S55 = support54 union {47}, the degree-at-most-four evaluation space has
rank 54 and one left relation, parity times L.  For the antipodal support
S56 = support54 union {16, 47}, the rank remains 54 and the left relation
space is two-dimensional.  A convenient basis is parity times M1 and parity
times M2, with L = M2 - 3 M1.
"""

from __future__ import annotations

import verify_n6_parity_triple_support54_geometry as geometry


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
SUPPORT54 = frozenset(range(1 << N)) - geometry.EXPECTED_OMITTED
SUPPORT55 = tuple(sorted(SUPPORT54 | {47}))
SUPPORT56 = tuple(sorted(SUPPORT54 | {16, 47}))
MONOMIALS4 = tuple(
    mask for mask in range(1 << N) if bin(mask).count("1") <= 4
)

M1 = (0, 0, 1, 1, 0, 0)
M2 = (2, 1, 1, 0, -1, 1)
L = geometry.HYPERPLANE_NORMAL


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def parity(code: int) -> int:
    return character(FULL, code)


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def linear_value(normal: tuple[int, ...], code: int) -> int:
    return sum(
        coefficient * character(1 << coordinate, code)
        for coordinate, coefficient in enumerate(normal)
    )


def relation(normal: tuple[int, ...], support: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(parity(code) * linear_value(normal, code) for code in support)


def modular_rank(matrix: list[list[int]], prime: int = 1000003) -> int:
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


def evaluation_matrix(support: tuple[int, ...]) -> list[list[int]]:
    return [
        [character(mask, code) for mask in MONOMIALS4]
        for code in support
    ]


def annihilates(
    weights: tuple[int, ...], matrix: list[list[int]]
) -> bool:
    return all(
        sum(weights[row] * matrix[row][column] for row in range(len(matrix)))
        == 0
        for column in range(len(MONOMIALS4))
    )


def verify() -> tuple[int, int, tuple[tuple[int, int], ...]]:
    assert len(MONOMIALS4) == 57
    assert tuple(left - 3 * right for left, right in zip(M2, M1)) == L

    evaluation55 = evaluation_matrix(SUPPORT55)
    relation55 = relation(L, SUPPORT55)
    rank55 = modular_rank(evaluation55)
    assert rank55 == 54
    assert any(relation55)
    assert annihilates(relation55, evaluation55)

    evaluation56 = evaluation_matrix(SUPPORT56)
    relation1 = relation(M1, SUPPORT56)
    relation2 = relation(M2, SUPPORT56)
    rank56 = modular_rank(evaluation56)
    assert rank56 == 54
    assert annihilates(relation1, evaluation56)
    assert annihilates(relation2, evaluation56)
    assert any(
        left * relation2[0] != right * relation1[0]
        for left, right in zip(relation1, relation2)
    )
    for weights in (relation1, relation2):
        by_code = dict(zip(SUPPORT56, weights))
        assert all(by_code[FULL ^ code] == -by_code[code] for code in SUPPORT56)

    representatives = tuple(code for code in SUPPORT56 if code < (FULL ^ code))
    assert len(representatives) == 28
    exceptional_pairs = tuple(
        (code, FULL ^ code)
        for code in representatives
        if target_sign(FULL ^ code) == -target_sign(code)
    )
    assert exceptional_pairs == ((22, 41), (25, 38))
    return rank55, rank56, exceptional_pairs


def main() -> None:
    rank55, rank56, exceptional_pairs = verify()
    print(f"S55 degree-four evaluation rank: {rank55} of 55")
    print(f"S56 degree-four evaluation rank: {rank56} of 56")
    print("S56 relation basis: parity times M1, parity times M2")
    print(f"opposite-label antipodal pairs: {exceptional_pairs}")
    print("verified repaired-support degree-four relations")


if __name__ == "__main__":
    main()
