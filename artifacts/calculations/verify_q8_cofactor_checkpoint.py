#!/usr/bin/env python3
"""Verify the exact finite claims in q8_cofactor_checkpoint.md."""

from __future__ import annotations

from itertools import combinations, product


POINTS = tuple(product((-1, 1), repeat=4))


def score(x: tuple[int, ...], y: tuple[int, ...], lam: int) -> int:
    return (1 + sum(x)) * (1 + sum(y)) - lam * (
        1 + sum(left * right for left, right in zip(x, y))
    )


def target_sign(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return 1 if score(x, y, 3) > 0 else -1


def rank_mod_prime(rows: list[tuple[int, ...]], prime: int) -> int:
    matrix = [[value % prime for value in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (index for index in range(rank, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(inverse * value) % prime for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or matrix[index][column] == 0:
                continue
            scale = matrix[index][column]
            matrix[index] = [
                (left - scale * right) % prime
                for left, right in zip(matrix[index], matrix[rank])
            ]
        rank += 1
    return rank


def verify_lambda_interval() -> None:
    signed_at_two = []
    signed_at_five = []
    for x in POINTS:
        for y in POINTS:
            sign = target_sign(x, y)
            signed_at_two.append(sign * score(x, y, 2))
            signed_at_five.append(sign * score(x, y, 5))

    assert min(signed_at_two) > 0
    assert min(signed_at_five) == 0
    assert all(value >= 0 for value in signed_at_five)
    assert sum(value == 0 for value in signed_at_five) == 31

    # The score is affine in lambda.  Strict positivity at lambda = 2 and
    # weak positivity at lambda = 5 prove strict positivity on [2, 5).
    print("lambda endpoints:", min(signed_at_two), min(signed_at_five))
    print("lambda-five boundary zeros:", signed_at_five.count(0))


def verify_special_columns() -> None:
    all_negative = (-1, -1, -1, -1)
    for x in POINTS:
        assert score(x, all_negative, 3) == -6
        for index in range(4):
            y = tuple(-1 if coordinate == index else 1 for coordinate in range(4))
            assert score(x, y, 3) == 6 * x[index]
    print("special columns: exact")


def verify_singular_mixed_block() -> None:
    mixed = tuple(
        tuple(1 - 4 * (row == column) for column in range(4))
        for row in range(4)
    )
    assert all(sum(row) == 0 for row in mixed)
    leading_three = tuple(tuple(mixed[i][j] for j in range(3)) for i in range(3))
    determinant = (
        leading_three[0][0]
        * (leading_three[1][1] * leading_three[2][2] - leading_three[1][2] * leading_three[2][1])
        - leading_three[0][1]
        * (leading_three[1][0] * leading_three[2][2] - leading_three[1][2] * leading_three[2][0])
        + leading_three[0][2]
        * (leading_three[1][0] * leading_three[2][1] - leading_three[1][1] * leading_three[2][0])
    )
    assert determinant == -16
    print("lambda-four mixed block: rank three with null vector (1,1,1,1)")


def verify_checkerboard_cone() -> None:
    normals: set[tuple[int, ...]] = set()
    for first_x, second_x in combinations(POINTS, 2):
        difference_x = tuple(left - right for left, right in zip(first_x, second_x))
        for first_y, second_y in combinations(POINTS, 2):
            signs = (
                target_sign(first_x, first_y),
                target_sign(first_x, second_y),
                target_sign(second_x, first_y),
                target_sign(second_x, second_y),
            )
            if not (
                signs[0] == signs[3]
                and signs[1] == signs[2]
                and signs[0] == -signs[1]
            ):
                continue
            difference_y = tuple(
                left - right for left, right in zip(first_y, second_y)
            )
            normals.add(
                tuple(
                    signs[0] * difference_x[row] * difference_y[column]
                    for row in range(4)
                    for column in range(4)
                )
            )

    mixed_three = tuple(1 - 3 * (row == column) for row in range(4) for column in range(4))
    margins = [
        sum(left * right for left, right in zip(normal, mixed_three))
        for normal in normals
    ]
    assert len(normals) == 571
    assert min(margins) == 8
    assert rank_mod_prime(list(normals), 127) == 16
    print("checkerboard normals:", len(normals))
    print("checkerboard normal rank:", 16)
    print("minimum exact margin at J - 3I:", min(margins))


def main() -> None:
    verify_lambda_interval()
    verify_special_columns()
    verify_singular_mixed_block()
    verify_checkerboard_cone()
    print("q8 cofactor checkpoint: verified")


if __name__ == "__main__":
    main()
