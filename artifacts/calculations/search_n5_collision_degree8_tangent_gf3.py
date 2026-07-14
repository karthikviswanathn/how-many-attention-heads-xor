#!/usr/bin/env python3
"""Search degree-eight collision relations using exact tangent constraints.

The fixed-center high-coefficient image is a hypersurface in twenty
coordinates.  At a smooth sampled image point, the gradient of every
vanishing polynomial is proportional to the one-dimensional normal vector.
Thus one sample supplies nineteen gradient constraints, instead of just one
value constraint.  Evaluations take place over GF(3^6), and the final rank is
computed exactly over GF3 by two-plane bitset elimination.

Use block calls followed by one combine call.  Both the invariant and
alternating S5 characters are supported.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy import sparse

import search_n5_collision_degree7_relative_invariant as base
import search_n5_collision_degree7_gf3 as gf


DEGREE = 8
SAMPLES = 190
SEED = 8_308
PARAMETERS = 24
VARIABLES = 20


def field_inverses(products: np.ndarray) -> np.ndarray:
    answer = np.zeros(gf.FIELD_SIZE, dtype=np.uint16)
    for value in range(1, gf.FIELD_SIZE):
        locations = np.flatnonzero(products[value] == 1)
        assert len(locations) == 1
        answer[value] = locations[0]
    return answer


def field_negatives(coefficients: np.ndarray) -> np.ndarray:
    return (((2 * coefficients.astype(np.int16)) % 3) @ gf.POWERS).astype(
        np.uint16
    )


def field_sum(
    values: np.ndarray, coefficients: np.ndarray, axis: int
) -> np.ndarray:
    digits = np.sum(
        coefficients[values].astype(np.int64), axis=axis
    ) % 3
    return (digits @ gf.POWERS).astype(np.uint16)


def affine_basis(index: int) -> np.ndarray:
    answer = np.zeros(1 << base.N, dtype=np.uint16)
    answer[[0, 1, 2, 4, 8, 16][index]] = 1
    return answer


def high_value_and_jacobian(
    parameter_rows: np.ndarray,
    sums: np.ndarray,
    products: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    variable_masks, _ = base.variable_permutations()
    left, right, multiplier, numerator = [
        gf.affine_polynomial(row) for row in parameter_rows
    ]
    left_right = gf.boolean_product(left, right, sums, products)
    cubic = gf.boolean_product(left_right, multiplier, sums, products)
    quadratic = gf.boolean_product(numerator, multiplier, sums, products)
    value = sums[cubic, quadratic][variable_masks]

    jacobian = np.empty((VARIABLES, PARAMETERS), dtype=np.uint16)
    bases = [affine_basis(index) for index in range(base.N + 1)]
    for index, basis in enumerate(bases):
        derivative = gf.boolean_product(
            basis,
            gf.boolean_product(right, multiplier, sums, products),
            sums,
            products,
        )
        jacobian[:, index] = derivative[variable_masks]
    for index, basis in enumerate(bases):
        derivative = gf.boolean_product(
            basis,
            gf.boolean_product(left, multiplier, sums, products),
            sums,
            products,
        )
        jacobian[:, 6 + index] = derivative[variable_masks]
    multiplier_source = sums[left_right, numerator]
    for index, basis in enumerate(bases):
        derivative = gf.boolean_product(
            basis, multiplier_source, sums, products
        )
        jacobian[:, 12 + index] = derivative[variable_masks]
    for index, basis in enumerate(bases):
        derivative = gf.boolean_product(
            basis, multiplier, sums, products
        )
        jacobian[:, 18 + index] = derivative[variable_masks]
    return value, jacobian


def normal_vector(
    jacobian: np.ndarray,
    coefficients: np.ndarray,
    sums: np.ndarray,
    products: np.ndarray,
    inverses: np.ndarray,
    negatives: np.ndarray,
) -> np.ndarray | None:
    matrix = jacobian.T.copy()
    row_count, column_count = matrix.shape
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        locations = np.flatnonzero(matrix[pivot_row:, column])
        if not len(locations):
            continue
        source = pivot_row + int(locations[0])
        if source != pivot_row:
            matrix[[pivot_row, source]] = matrix[[source, pivot_row]]
        matrix[pivot_row] = products[
            matrix[pivot_row], inverses[matrix[pivot_row, column]]
        ]
        for row in range(row_count):
            if row == pivot_row or matrix[row, column] == 0:
                continue
            multiple = products[
                matrix[pivot_row], negatives[matrix[row, column]]
            ]
            matrix[row] = sums[matrix[row], multiple]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    if len(pivot_columns) != VARIABLES - 1:
        return None
    free_columns = [
        column
        for column in range(column_count)
        if column not in pivot_columns
    ]
    assert len(free_columns) == 1
    free = free_columns[0]
    normal = np.zeros(column_count, dtype=np.uint16)
    normal[free] = 1
    for row, column in enumerate(pivot_columns):
        normal[column] = negatives[matrix[row, free]]
    check = field_sum(
        products[jacobian, normal[:, None]], coefficients, axis=0
    )
    assert not np.any(check)
    pivot = int(np.flatnonzero(normal)[0])
    normal = products[normal, inverses[normal[pivot]]]
    return normal


def sampled_smooth_points(
    coefficients: np.ndarray,
    sums: np.ndarray,
    products: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    inverses = field_inverses(products)
    negatives = field_negatives(coefficients)
    rng = np.random.default_rng(SEED)
    values = []
    normals = []
    pivots = []
    attempts = 0
    while len(values) < SAMPLES:
        attempts += 1
        parameters = rng.integers(
            0,
            gf.FIELD_SIZE,
            size=(4, base.N + 1),
            dtype=np.uint16,
        )
        value, jacobian = high_value_and_jacobian(
            parameters, sums, products
        )
        if np.any(value == 0):
            continue
        normal = normal_vector(
            jacobian,
            coefficients,
            sums,
            products,
            inverses,
            negatives,
        )
        if normal is None or normal[0] == 0:
            continue
        values.append(value)
        normals.append(normal)
        pivots.append(0)
    print(f"accepted {SAMPLES} smooth nonzero points in {attempts} attempts")
    return (
        np.array(values, dtype=np.uint16),
        np.array(normals, dtype=np.uint16),
        np.array(pivots, dtype=np.int8),
    )


def derivative_matrix(
    selected: np.ndarray, weights: np.ndarray
) -> sparse.csr_matrix:
    rows = []
    columns = []
    data = []
    for term_index, monomial in enumerate(selected):
        counts = np.bincount(monomial, minlength=VARIABLES) % 3
        for variable in np.flatnonzero(counts):
            coefficient = int(counts[variable] * weights[term_index]) % 3
            if coefficient:
                rows.append(term_index)
                columns.append(int(variable))
                data.append(coefficient)
    return sparse.csr_matrix(
        (np.array(data, dtype=np.int16), (rows, columns)),
        shape=(len(selected), VARIABLES),
        dtype=np.int16,
    )


def orbit_constraints(
    selected: np.ndarray,
    weights: np.ndarray,
    values: np.ndarray,
    normals: np.ndarray,
    pivots: np.ndarray,
    coefficients: np.ndarray,
    sums: np.ndarray,
    products: np.ndarray,
    inverses: np.ndarray,
    negatives: np.ndarray,
) -> np.ndarray:
    terms = values[:, selected[:, 0]]
    for factor in range(1, DEGREE):
        terms = products[terms, values[:, selected[:, factor]]]
    term_digits = coefficients[terms].astype(np.int16)

    weighted_digits = (
        term_digits * weights[None, :, None].astype(np.int16)
    ) % 3
    value_digits = np.sum(weighted_digits, axis=1, dtype=np.int64) % 3
    orbit_values = (value_digits @ gf.POWERS).astype(np.uint16)

    derivative = derivative_matrix(selected, weights)
    flat_digits = term_digits.transpose(0, 2, 1).reshape(
        SAMPLES * gf.FIELD_DEGREE, len(selected)
    )
    numerator_digits = (flat_digits @ derivative) % 3
    numerator_digits = numerator_digits.reshape(
        SAMPLES, gf.FIELD_DEGREE, VARIABLES
    ).transpose(0, 2, 1)
    numerators = (numerator_digits @ gf.POWERS).astype(np.uint16)
    gradients = products[numerators, inverses[values]]

    constraints = np.empty((SAMPLES, VARIABLES), dtype=np.uint16)
    constraints[:, 0] = orbit_values
    assert not np.any(pivots)
    correction = products[
        normals[:, 1:], gradients[:, 0, None]
    ]
    constraints[:, 1:] = sums[
        gradients[:, 1:], negatives[correction]
    ]
    return constraints.reshape(SAMPLES * VARIABLES)


def evaluate_block(
    block: int,
    blocks: int,
    character: str,
    output: Path,
) -> None:
    if not 0 <= block < blocks:
        raise ValueError("block must be in range(blocks)")
    base.DEGREE = DEGREE
    coefficients, sums, products = gf.field_tables()
    inverses = field_inverses(products)
    negatives = field_negatives(coefficients)
    monomials, orbits = gf.relative_orbits(character)
    values, normals, pivots = sampled_smooth_points(
        coefficients, sums, products
    )
    start = len(orbits) * block // blocks
    end = len(orbits) * (block + 1) // blocks
    evaluations = np.empty(
        (SAMPLES * VARIABLES, end - start), dtype=np.uint16
    )
    for output_column, orbit_index in enumerate(range(start, end)):
        indices, weights = orbits[orbit_index]
        evaluations[:, output_column] = orbit_constraints(
            monomials[indices],
            weights,
            values,
            normals,
            pivots,
            coefficients,
            sums,
            products,
            inverses,
            negatives,
        )
        if output_column and output_column % 500 == 0:
            print(
                f"character={character} block={block}/{blocks} "
                f"evaluated={output_column}/{end - start}",
                flush=True,
            )
    np.savez_compressed(
        output,
        character=np.array(character),
        orbit_count=np.array(len(orbits), dtype=np.int64),
        start=np.array(start, dtype=np.int64),
        end=np.array(end, dtype=np.int64),
        evaluations=evaluations,
    )
    print(
        f"wrote character={character} block={block}/{blocks} "
        f"columns=[{start},{end}) to {output}"
    )


def packed_ternary_column(
    column: np.ndarray, coefficients: np.ndarray
) -> tuple[int, int]:
    digits = coefficients[column]
    one = 0
    two = 0
    row_count = len(column)
    for coordinate in range(gf.FIELD_DEGREE):
        packed_one = np.packbits(
            digits[:, coordinate] == 1, bitorder="little"
        ).tobytes()
        packed_two = np.packbits(
            digits[:, coordinate] == 2, bitorder="little"
        ).tobytes()
        one |= int.from_bytes(packed_one, "little") << (
            coordinate * row_count
        )
        two |= int.from_bytes(packed_two, "little") << (
            coordinate * row_count
        )
    return one, two


def combine(paths: list[Path]) -> None:
    coefficients = gf.coefficient_table()
    records = []
    character = None
    orbit_count = None
    for path in paths:
        payload = np.load(path)
        current_character = str(payload["character"])
        current_count = int(payload["orbit_count"])
        if character is None:
            character = current_character
            orbit_count = current_count
        assert current_character == character
        assert current_count == orbit_count
        records.append(
            (
                int(payload["start"]),
                int(payload["end"]),
                payload["evaluations"],
            )
        )
    records.sort()
    assert records[0][0] == 0
    assert records[-1][1] == orbit_count
    assert all(
        records[index][1] == records[index + 1][0]
        for index in range(len(records) - 1)
    )
    evaluations = np.concatenate([record[2] for record in records], axis=1)
    assert evaluations.shape == (SAMPLES * VARIABLES, orbit_count)

    row_count = SAMPLES * VARIABLES * gf.FIELD_DEGREE
    row_mask = (1 << row_count) - 1
    column_mask = (1 << orbit_count) - 1
    basis: dict[int, tuple[int, int]] = {}
    combination_basis: dict[int, tuple[int, int]] = {}
    dependencies = []
    rank = 0
    for column_index in range(orbit_count):
        column = packed_ternary_column(
            evaluations[:, column_index], coefficients
        )
        combination = (1 << column_index, 0)
        while column[0] | column[1]:
            pivot = (column[0] | column[1]).bit_length() - 1
            pivot_digit = gf.digit_at(column, pivot)
            if pivot not in basis:
                if pivot_digit == 2:
                    column = gf.ternary_negate(column)
                    combination = gf.ternary_negate(combination)
                basis[pivot] = column
                combination_basis[pivot] = combination
                rank += 1
                break
            if pivot_digit == 1:
                column = gf.ternary_add(
                    column, gf.ternary_negate(basis[pivot]), row_mask
                )
                combination = gf.ternary_add(
                    combination,
                    gf.ternary_negate(combination_basis[pivot]),
                    column_mask,
                )
            else:
                column = gf.ternary_add(column, basis[pivot], row_mask)
                combination = gf.ternary_add(
                    combination, combination_basis[pivot], column_mask
                )
        if not (column[0] | column[1]):
            dependencies.append(combination)
        if column_index and column_index % 1_000 == 0:
            print(
                f"combined={column_index}/{orbit_count} rank={rank}",
                flush=True,
            )

    print(f"degree={DEGREE} character={character} columns={orbit_count}")
    print(f"exact GF3 tangent-evaluation rank={rank}")
    print(f"dependency dimension={len(dependencies)}")
    for index, dependency in enumerate(dependencies[:5]):
        support = dependency[0] | dependency[1]
        entries = [
            (column, gf.digit_at(dependency, column))
            for column in range(orbit_count)
            if (support >> column) & 1
        ]
        print(
            f"dependency={index} support_size={len(entries)} "
            f"entries={entries}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", type=int)
    parser.add_argument("--blocks", type=int, default=4)
    parser.add_argument(
        "--character",
        choices=("invariant", "alternating"),
        default="invariant",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--combine", type=Path, nargs="+")
    arguments = parser.parse_args()
    if arguments.combine is not None:
        combine(arguments.combine)
        return
    if arguments.block is None or arguments.output is None:
        raise ValueError("block mode requires --block and --output")
    evaluate_block(
        arguments.block,
        arguments.blocks,
        arguments.character,
        arguments.output,
    )


if __name__ == "__main__":
    main()
