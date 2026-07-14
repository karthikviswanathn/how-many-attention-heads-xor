#!/usr/bin/env python3
"""Verify an exact limit of the positive-quartic support54 ansatz.

For the six-bit parity-triple candidate, consider tangent multipliers of the
form

    lambda(z) = D(z) q(z),

where D is the product of four positive affine denominators and q is a
Fourier polynomial of degree at most four that is positive on support54.

For one integer denominator tuple, this file verifies two complementary
facts using exact rational arithmetic:

* a 26-point affine functional forces every normalized positive tangent
  kernel vector to violate the unique degree-four evaluation relation;
* a different 26-point positive circuit annihilates all tangent columns.

Thus the unrestricted support54 obstruction survives at this tuple, while
positive quartic q is not a universal parameterization of that obstruction.
"""

from __future__ import annotations

from fractions import Fraction
import math


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
OMITTED = frozenset((6, 9, 16, 21, 27, 36, 42, 47, 54, 57))
SUPPORT54 = tuple(code for code in range(1 << N) if code not in OMITTED)

DENOMINATORS = (
    (323384, -45582, -3, -74, -8850, -268810, -55),
    (10469, -245, -58, -145, -2843, -7092, -76),
    (135697804, -17211, -19850000, -45, -262047, -75713338, -39855153),
    (3423, -1788, -1498, -1, -1, -1, -124),
)

# Rows on which G(z) y + beta = R(z) determines the exact separating
# functional.  The inequality is then checked on all 54 support points.
SEPARATOR_ACTIVE_SUPPORT = (
    4, 5, 7, 8, 12, 13, 14, 15, 18, 20, 22, 23, 24,
    25, 28, 30, 35, 38, 39, 44, 49, 51, 53, 56, 59, 60,
)

# A one-dimensional exact left-null support for the unrestricted tangent
# matrix.  Its weights are reconstructed below instead of stored.
FREE_CIRCUIT_SUPPORT = (
    4, 5, 7, 8, 12, 13, 14, 18, 20, 22, 23, 24, 25,
    28, 30, 35, 38, 39, 44, 49, 51, 53, 56, 59, 60, 62,
)

MONOMIALS4 = tuple(
    mask for mask in range(1 << N) if bin(mask).count("1") <= 4
)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def parity(code: int) -> int:
    return character(FULL, code)


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def linear_form(code: int) -> int:
    coefficients = (2, 1, -2, -3, -1, 1)
    return sum(
        coefficient * character(1 << coordinate, code)
        for coordinate, coefficient in enumerate(coefficients)
    )


def relation_weight(code: int) -> int:
    return parity(code) * linear_form(code)


def denominator_values(code: int) -> tuple[int, ...]:
    return tuple(
        denominator[0]
        + sum(
            denominator[coordinate + 1]
            * character(1 << coordinate, code)
            for coordinate in range(N)
        )
        for denominator in DENOMINATORS
    )


def cleared_row(code: int) -> tuple[int, ...]:
    values = denominator_values(code)
    product = math.prod(values)
    sign = target_sign(code)
    return tuple(
        [sign * product]
        + [
            sign
            * character(1 << coordinate, code)
            * (product // values[head])
            for head in range(4)
            for coordinate in range(N)
        ]
    )


ROWS = {code: cleared_row(code) for code in SUPPORT54}


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


def solve_square(matrix: list[list[Fraction]]) -> tuple[Fraction, ...]:
    size = len(matrix)
    assert all(len(row) == size + 1 for row in matrix)
    work = [row[:] for row in matrix]
    for column in range(size):
        chosen = next(
            row for row in range(column, size) if work[row][column]
        )
        work[column], work[chosen] = work[chosen], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[column])
            ]
    return tuple(work[row][-1] for row in range(size))


def one_dimensional_nullspace(
    rows: list[list[int]],
) -> list[Fraction] | None:
    if not rows:
        return None
    matrix = [[Fraction(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        chosen = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if chosen is None:
            continue
        matrix[pivot_row], matrix[chosen] = matrix[chosen], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                left - multiplier * right
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free_columns = [
        column for column in range(column_count)
        if column not in pivot_columns
    ]
    if len(free_columns) != 1:
        return None
    free = free_columns[0]
    vector = [Fraction(0) for _ in range(column_count)]
    vector[free] = Fraction(1)
    for row, column in enumerate(pivot_columns):
        vector[column] = -matrix[row][free]
    return vector


def primitive_integer_vector(vector: list[Fraction]) -> tuple[int, ...]:
    scale = math.lcm(*(value.denominator for value in vector))
    integers = [
        value.numerator * (scale // value.denominator) for value in vector
    ]
    divisor = math.gcd(*(abs(value) for value in integers))
    assert divisor > 0
    integers = [value // divisor for value in integers]
    if sum(integers) < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def verify() -> tuple[Fraction, tuple[int, ...], tuple[Fraction, ...]]:
    assert len(SUPPORT54) == 54
    assert set(code for code in range(1 << N) if linear_form(code) == 0) == OMITTED
    for denominator in DENOMINATORS:
        assert all(value < 0 for value in denominator[1:])
        assert denominator[0] == sum(abs(value) for value in denominator[1:]) + 10
    assert all(
        min(denominator_values(code)) > 0 for code in range(1 << N)
    )

    evaluation4 = [
        [character(mask, code) for mask in MONOMIALS4]
        for code in SUPPORT54
    ]
    assert len(MONOMIALS4) == 57
    assert modular_rank(evaluation4) == 53
    for mask in MONOMIALS4:
        assert sum(
            relation_weight(code) * character(mask, code)
            for code in SUPPORT54
        ) == 0

    separator_system = [
        [Fraction(value) for value in ROWS[code]]
        + [Fraction(1), Fraction(relation_weight(code))]
        for code in SEPARATOR_ACTIVE_SUPPORT
    ]
    separator = solve_square(separator_system)
    tangent_functional = separator[:-1]
    beta = separator[-1]
    assert beta < 0
    slacks = tuple(
        sum(
            Fraction(value) * multiplier
            for value, multiplier in zip(ROWS[code], tangent_functional)
        )
        + beta
        - relation_weight(code)
        for code in SUPPORT54
    )
    assert all(slack >= 0 for slack in slacks)
    assert tuple(
        code for code, slack in zip(SUPPORT54, slacks) if slack == 0
    ) == SEPARATOR_ACTIVE_SUPPORT

    circuit_matrix = [
        [ROWS[code][column] for code in FREE_CIRCUIT_SUPPORT]
        for column in range(25)
    ]
    circuit_vector = one_dimensional_nullspace(circuit_matrix)
    assert circuit_vector is not None
    circuit_weights = primitive_integer_vector(circuit_vector)
    assert all(weight > 0 for weight in circuit_weights)
    for column in range(25):
        assert sum(
            weight * ROWS[code][column]
            for code, weight in zip(FREE_CIRCUIT_SUPPORT, circuit_weights)
        ) == 0

    normalized_relation = Fraction(
        sum(
            weight * relation_weight(code)
            for code, weight in zip(FREE_CIRCUIT_SUPPORT, circuit_weights)
        ),
        sum(circuit_weights),
    )
    assert normalized_relation <= beta < 0
    return beta, circuit_weights, slacks


def main() -> None:
    beta, circuit_weights, slacks = verify()
    print("quartic evaluation rank on support54: 53 of 54")
    print("unique quartic relation: verified on all 57 monomials")
    print("separator active support: 26")
    print(f"separator beta: {float(beta):.16f}")
    print(f"strict separator slacks: {sum(slack > 0 for slack in slacks)} of 54")
    print("positive unrestricted circuit support: 26")
    print(
        "largest unrestricted circuit weight digits: "
        f"{max(len(str(weight)) for weight in circuit_weights)}"
    )
    print("verified positive-quartic ansatz limitation")


if __name__ == "__main__":
    main()
