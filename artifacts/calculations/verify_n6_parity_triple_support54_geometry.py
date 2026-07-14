#!/usr/bin/env python3
"""Verify the hyperplane and moment structure of the 54-vertex dual support."""

from __future__ import annotations

import itertools


N = 6
FULL = (1 << N) - 1
EXCEPTIONAL = frozenset((21, 38, 41))
SUPPORT40 = (
    1, 2, 3, 4, 7, 8, 10, 12, 13, 14, 15, 19, 20, 24, 25, 26, 28,
    29, 30, 31, 33, 34, 35, 39, 40, 41, 44, 45, 46, 49, 50, 51, 52,
    55, 56, 58, 60, 61, 62, 63,
)
WEIGHTS40 = (
    1, 1, 4, 1, 1, 3, 1, 8, 3, 4, 1, 2, 2, 5, 1, 2, 11, 5, 6, 2,
    2, 2, 6, 2, 1, 1, 5, 1, 2, 1, 1, 4, 1, 1, 3, 1, 8, 3, 4, 1,
)
HYPERPLANE_NORMAL = (2, 1, -2, -3, -1, 1)
EXPECTED_OMITTED = frozenset((6, 9, 16, 21, 27, 36, 42, 47, 54, 57))


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def parity(code: int) -> int:
    return character(FULL, code)


def target_sign(code: int) -> int:
    return -parity(code) if code in EXCEPTIONAL else parity(code)


def hyperplane_value(code: int) -> int:
    return sum(
        coefficient * character(1 << coordinate, code)
        for coordinate, coefficient in enumerate(HYPERPLANE_NORMAL)
    )


def transform(code: int, permutation: tuple[int, ...], complement: int) -> int:
    answer = 0
    for source, target in enumerate(permutation):
        bit = ((code >> source) & 1) ^ ((complement >> target) & 1)
        answer |= bit << target
    return answer


def signed_measure() -> tuple[int, ...]:
    answer = [0] * (1 << N)
    for code, weight in zip(SUPPORT40, WEIGHTS40):
        answer[code] = weight * target_sign(code)
    return tuple(answer)


def verify() -> None:
    support = frozenset(SUPPORT40)
    antipodal = frozenset(FULL ^ code for code in support)
    support54 = support | antipodal
    omitted = frozenset(range(1 << N)) - support54
    assert len(support54) == 54
    assert omitted == EXPECTED_OMITTED
    assert omitted == frozenset(
        code for code in range(1 << N) if hyperplane_value(code) == 0
    )
    assert all((FULL ^ code) in omitted for code in omitted)

    representatives = (6, 9, 16, 21, 27)
    sign_rows = tuple(
        tuple(character(1 << coordinate, code) for coordinate in range(N))
        for code in representatives
    )
    # A nonzero 5 by 5 minor proves that the five projective representatives
    # have rank five, so their common central hyperplane is unique.
    minor = tuple(tuple(row[column] for column in range(5)) for row in sign_rows)
    determinant = 0
    for permutation in itertools.permutations(range(5)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(5)
            for right in range(left + 1, 5)
        )
        term = (-1) ** inversions
        for row, column in enumerate(permutation):
            term *= minor[row][column]
        determinant += term
    assert determinant != 0
    assert all(
        sum(left * right for left, right in zip(row, HYPERPLANE_NORMAL)) == 0
        for row in sign_rows
    )

    # The hyperplane section has 24 signed-coordinate symmetries.
    stabilizers = []
    for permutation in itertools.permutations(range(N)):
        for complement in range(1 << N):
            image = frozenset(
                transform(code, permutation, complement) for code in omitted
            )
            if image == omitted:
                stabilizers.append((permutation, complement))
    assert len(stabilizers) == 24

    measure = signed_measure()
    for mask in range(1 << N):
        if bin(mask).count("1") <= 3:
            assert sum(
                measure[code] * character(mask, code)
                for code in range(1 << N)
            ) == 0

    reflected = tuple(measure[FULL ^ code] for code in range(1 << N))
    even = tuple(left + right for left, right in zip(measure, reflected))
    odd = tuple(left - right for left, right in zip(measure, reflected))
    assert frozenset(code for code, value in enumerate(even) if value) == support54
    assert frozenset(code for code, value in enumerate(odd) if value) == support54
    assert all(even[code] == even[FULL ^ code] for code in range(1 << N))
    assert all(odd[code] == -odd[FULL ^ code] for code in range(1 << N))
    for current in (even, odd):
        for mask in range(1 << N):
            if bin(mask).count("1") <= 3:
                assert sum(
                    current[code] * character(mask, code)
                    for code in range(1 << N)
                ) == 0
    bad_even = frozenset(
        code
        for code, value in enumerate(even)
        if value and value * target_sign(code) < 0
    )
    assert bad_even == frozenset((22, 38))


def main() -> None:
    verify()
    print("antipodal support size: 54")
    print("omitted hyperplane vertices: 10")
    print("hyperplane normal: (2, 1, -2, -3, -1, 1)")
    print("signed-coordinate stabilizer size: 24")
    print("even symmetrized moment mismatches: (22, 38)")


if __name__ == "__main__":
    main()
