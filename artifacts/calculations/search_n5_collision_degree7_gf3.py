#!/usr/bin/env python3
"""Representation-complete degree-seven collision search over GF(3^6).

This is the odd-characteristic companion to
search_n5_collision_degree7_relative_invariant.py.  GF(3^6) evaluations give
six GF3 equations each.  Exact two-plane bitset elimination then computes the
rank over GF3.  Both the invariant and alternating S5 characters are
supported.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np

import search_n5_collision_degree7_relative_invariant as base


FIELD_SIZE = 729
FIELD_DEGREE = 6
SAMPLES = 1_110
SEED = 3_707
POWERS = np.array([1, 3, 9, 27, 81, 243], dtype=np.int64)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(base.N)
        for right in range(left + 1, base.N)
    )
    return 1 if inversions % 2 == 0 else 2


def coefficient_table() -> np.ndarray:
    answer = np.empty((FIELD_SIZE, FIELD_DEGREE), dtype=np.int8)
    for value in range(FIELD_SIZE):
        current = value
        for degree in range(FIELD_DEGREE):
            answer[value, degree] = current % 3
            current //= 3
    return answer


def field_tables() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    coefficients = coefficient_table()
    sums = (
        (
            coefficients[:, None, :].astype(np.int16)
            + coefficients[None, :, :].astype(np.int16)
        )
        % 3
    ) @ POWERS
    sums = sums.astype(np.uint16)

    products = np.empty((FIELD_SIZE, FIELD_SIZE), dtype=np.uint16)
    # The modulus is x^6+x^5+2x^4+x^3+x+2 over GF3.
    modulus_tail = np.array([2, 1, 0, 1, 2, 1], dtype=np.int16)
    for left in range(FIELD_SIZE):
        left_coefficients = coefficients[left].astype(np.int16)
        for right in range(FIELD_SIZE):
            right_coefficients = coefficients[right].astype(np.int16)
            convolution = np.convolve(
                left_coefficients, right_coefficients
            ).astype(np.int16) % 3
            for degree in range(10, 5, -1):
                leading = int(convolution[degree])
                if leading:
                    convolution[degree - 6 : degree] = (
                        convolution[degree - 6 : degree]
                        - leading * modulus_tail
                    ) % 3
            products[left, right] = int(
                convolution[:FIELD_DEGREE] @ POWERS
            )
    return coefficients, sums, products


def relative_orbits(
    character: str,
) -> tuple[np.ndarray, list[tuple[np.ndarray, np.ndarray]]]:
    variables, _ = base.variable_permutations()
    variable_index = {mask: index for index, mask in enumerate(variables)}
    permutations = []
    for permutation in itertools.permutations(range(base.N)):
        transformed = []
        for mask in variables:
            target = 0
            for source in range(base.N):
                if (mask >> source) & 1:
                    target |= 1 << permutation[source]
            transformed.append(variable_index[target])
        permutations.append((transformed, permutation_sign(permutation)))

    monomials = list(
        itertools.combinations_with_replacement(range(20), base.DEGREE)
    )
    lookup = {monomial: index for index, monomial in enumerate(monomials)}
    seen = set()
    orbits = []
    for index, monomial in enumerate(monomials):
        if index in seen:
            continue
        transformed_signs: dict[int, int] = {}
        inconsistent = False
        for permutation, sign in permutations:
            transformed = lookup[
                tuple(sorted(permutation[value] for value in monomial))
            ]
            if (
                transformed in transformed_signs
                and transformed_signs[transformed] != sign
            ):
                inconsistent = True
            transformed_signs[transformed] = sign
        seen.update(transformed_signs)
        if character == "alternating" and inconsistent:
            continue
        indices = np.array(sorted(transformed_signs), dtype=np.int64)
        if character == "invariant":
            weights = np.ones(len(indices), dtype=np.int8)
        else:
            weights = np.array(
                [transformed_signs[value] for value in indices],
                dtype=np.int8,
            )
        orbits.append((indices, weights))
    return np.array(monomials, dtype=np.int8), orbits


def affine_polynomial(coefficients: np.ndarray) -> np.ndarray:
    answer = np.zeros(1 << base.N, dtype=np.uint16)
    answer[[0, 1, 2, 4, 8, 16]] = coefficients
    return answer


def boolean_product(
    left: np.ndarray,
    right: np.ndarray,
    sums: np.ndarray,
    products: np.ndarray,
) -> np.ndarray:
    answer = np.zeros(1 << base.N, dtype=np.uint16)
    for left_mask in np.flatnonzero(left):
        for right_mask in np.flatnonzero(right):
            target = left_mask | right_mask
            answer[target] = sums[
                answer[target], products[left[left_mask], right[right_mask]]
            ]
    return answer


def sampled_values(
    sums: np.ndarray, products: np.ndarray
) -> np.ndarray:
    variables, _ = base.variable_permutations()
    rng = np.random.default_rng(SEED)
    parameters = rng.integers(
        0,
        FIELD_SIZE,
        size=(SAMPLES, 4, base.N + 1),
        dtype=np.uint16,
    )
    answer = np.empty((SAMPLES, 20), dtype=np.uint16)
    for sample in range(SAMPLES):
        left, right, multiplier, numerator = [
            affine_polynomial(row) for row in parameters[sample]
        ]
        cubic = boolean_product(
            left,
            boolean_product(right, multiplier, sums, products),
            sums,
            products,
        )
        quadratic = boolean_product(numerator, multiplier, sums, products)
        answer[sample] = sums[cubic, quadratic][variables]
    return answer


def evaluate_block(
    block: int,
    blocks: int,
    character: str,
    output: Path,
) -> None:
    coefficients, sums, products = field_tables()
    monomials, orbits = relative_orbits(character)
    values = sampled_values(sums, products)
    start = len(orbits) * block // blocks
    end = len(orbits) * (block + 1) // blocks
    evaluations = np.empty((SAMPLES, end - start), dtype=np.uint16)
    for output_column, orbit_index in enumerate(range(start, end)):
        indices, weights = orbits[orbit_index]
        selected = monomials[indices]
        terms = values[:, selected[:, 0]]
        for factor in range(1, base.DEGREE):
            terms = products[terms, values[:, selected[:, factor]]]
        digits = coefficients[terms]
        weighted = (
            digits.astype(np.int16) * weights[None, :, None]
        ) % 3
        digit_sums = np.sum(weighted, axis=1, dtype=np.int64) % 3
        evaluations[:, output_column] = digit_sums @ POWERS
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
    for coordinate in range(FIELD_DEGREE):
        shift = coordinate * SAMPLES
        packed_one = np.packbits(
            digits[:, coordinate] == 1, bitorder="little"
        ).tobytes()
        packed_two = np.packbits(
            digits[:, coordinate] == 2, bitorder="little"
        ).tobytes()
        one |= int.from_bytes(packed_one, "little") << shift
        two |= int.from_bytes(packed_two, "little") << shift
    return one, two


def ternary_add(
    left: tuple[int, int],
    right: tuple[int, int],
    mask: int,
) -> tuple[int, int]:
    left_one, left_two = left
    right_one, right_two = right
    left_zero = mask ^ (left_one | left_two)
    right_zero = mask ^ (right_one | right_two)
    result_one = (
        (left_zero & right_one)
        | (left_one & right_zero)
        | (left_two & right_two)
    )
    result_two = (
        (left_zero & right_two)
        | (left_two & right_zero)
        | (left_one & right_one)
    )
    return result_one, result_two


def ternary_negate(value: tuple[int, int]) -> tuple[int, int]:
    return value[1], value[0]


def digit_at(value: tuple[int, int], position: int) -> int:
    if (value[0] >> position) & 1:
        return 1
    if (value[1] >> position) & 1:
        return 2
    return 0


def combine(paths: list[Path]) -> None:
    coefficients = coefficient_table()
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
    evaluations = np.concatenate([record[2] for record in records], axis=1)
    assert evaluations.shape == (SAMPLES, orbit_count)

    row_count = SAMPLES * FIELD_DEGREE
    row_mask = (1 << row_count) - 1
    column_mask = (1 << orbit_count) - 1
    basis: dict[int, tuple[int, int]] = {}
    combination_basis: dict[int, tuple[int, int]] = {}
    rank = 0
    dependencies = []
    for column_index in range(orbit_count):
        column = packed_ternary_column(
            evaluations[:, column_index], coefficients
        )
        combination = (1 << column_index, 0)
        while column[0] | column[1]:
            pivot = (column[0] | column[1]).bit_length() - 1
            pivot_digit = digit_at(column, pivot)
            if pivot not in basis:
                if pivot_digit == 2:
                    column = ternary_negate(column)
                    combination = ternary_negate(combination)
                basis[pivot] = column
                combination_basis[pivot] = combination
                rank += 1
                break
            if pivot_digit == 1:
                column = ternary_add(
                    column, ternary_negate(basis[pivot]), row_mask
                )
                combination = ternary_add(
                    combination,
                    ternary_negate(combination_basis[pivot]),
                    column_mask,
                )
            else:
                column = ternary_add(column, basis[pivot], row_mask)
                combination = ternary_add(
                    combination, combination_basis[pivot], column_mask
                )
        if not (column[0] | column[1]):
            dependencies.append(combination)

    print(f"character={character} columns={orbit_count}")
    print(f"exact GF3 rank from GF(3^6) evaluations={rank}")
    print(f"dependency dimension={len(dependencies)}")
    for index, dependency in enumerate(dependencies[:5]):
        support = dependency[0] | dependency[1]
        entries = [
            (column, digit_at(dependency, column))
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
    parser.add_argument("--blocks", type=int, default=3)
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
