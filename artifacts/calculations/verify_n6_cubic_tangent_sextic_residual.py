#!/usr/bin/env python3
"""Verify the five large residual blocks in the n=6 sextic audit.

The Young-subgroup detector used by the main invariant search mixes several
irreducible representations.  Five of its degree-six matrices are needlessly
large.  This verifier instead applies a primitive Young symmetrizer on every
stabilizer orbit.  The resulting column count is the multiplicity of the
requested Specht module, so all five exact modular rank tests fit in memory.

Full rank in these five pure blocks, together with the other sixty full Young
detectors, proves that the cubic tangent image has no sextic equation over
F_101.
"""

from __future__ import annotations

import argparse
import itertools
import math
import time

import numpy as np

import search_cubic_tangent_quartic_invariants as quartic
import search_cubic_tangent_quintic_equations as sextic
import verify_cubic_tangent_dimension as tangent


PRIME = sextic.PRIME
DIMENSION = 6
SPECS = {
    1: ((1,), (3, 1, 1), 8_087, 0x16002),
    2: ((2,), (2, 2), 7_618, 0x16003),
    3: ((2, 1), (2, 1), 18_538, 0x16001),
    4: ((2, 2), (2,), 7_597, 0x16004),
    5: ((3, 1, 1), (1,), 7_952, 0x16005),
}


def tableau_blocks(
    partition: tuple[int, ...], offset: int
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    rows = []
    cursor = offset
    for size in partition:
        rows.append(tuple(range(cursor, cursor + size)))
        cursor += size
    columns = tuple(
        tuple(row[column] for row in rows if len(row) > column)
        for column in range(partition[0] if partition else 0)
    )
    return tuple(rows), columns


def permutation_sign(values: tuple[int, ...]) -> int:
    inversions = sum(
        values[first] > values[second]
        for first in range(len(values))
        for second in range(first + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def block_group(
    blocks: tuple[tuple[int, ...], ...]
) -> list[tuple[tuple[int, ...], int]]:
    choices = [tuple(itertools.permutations(block)) for block in blocks]
    answer = []
    for images in itertools.product(*choices):
        permutation = list(range(DIMENSION))
        sign = 1
        for block, image in zip(blocks, images):
            for source, target in zip(block, image):
                permutation[source] = target
            sign *= permutation_sign(image)
        answer.append((tuple(permutation), sign))
    return answer


def compose(
    outer: tuple[int, ...], inner: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(outer[inner[index]] for index in range(DIMENSION))


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for source, target in enumerate(permutation):
        if (mask >> source) & 1:
            answer |= 1 << target
    return answer


def young_operator(
    first: tuple[int, ...], second: tuple[int, ...], weight: int
) -> tuple[list[np.ndarray], list[int]]:
    first_rows, first_columns = tableau_blocks(first, 0)
    second_rows, second_columns = tableau_blocks(second, weight)
    rows = block_group(first_rows + second_rows)
    columns = block_group(first_columns + second_columns)
    coordinate_masks = tangent.monomials(DIMENSION)
    coordinate_index = {
        mask: index for index, mask in enumerate(coordinate_masks)
    }
    maps = []
    signs = []
    for row, _ in rows:
        for column, column_sign in columns:
            permutation = compose(row, column)
            maps.append(
                np.array(
                    [
                        coordinate_index[permute_mask(mask, permutation)]
                        for mask in coordinate_masks
                    ],
                    dtype=np.int64,
                )
            )
            signs.append(column_sign)
    return maps, signs


def specht_dimension(partition: tuple[int, ...]) -> int:
    size = sum(partition)
    hooks = 1
    for row, row_size in enumerate(partition):
        for column in range(row_size):
            below = sum(
                other_size > column
                for other_size in partition[row + 1 :]
            )
            hooks *= row_size - column + below
    return math.factorial(size) // hooks


def projected_basis(
    full_orbits: list[list[tuple[int, ...]]],
    operator_maps: list[np.ndarray],
    operator_signs: list[int],
    maximum_orbit_rank: int,
) -> list[list[tuple[tuple[int, ...], int]]]:
    answer = []
    for orbit in full_orbits:
        orbit_index = {monomial: index for index, monomial in enumerate(orbit)}
        echelon_vectors: list[np.ndarray] = []
        pivots: list[int] = []
        for monomial in orbit:
            raw = np.zeros(len(orbit), dtype=np.int64)
            monomial_array = np.array(monomial, dtype=np.int64)
            for coordinate_map, sign in zip(operator_maps, operator_signs):
                image = tuple(sorted(coordinate_map[monomial_array].tolist()))
                raw[orbit_index[image]] += sign
            reduced = raw % PRIME
            for pivot, vector in zip(pivots, echelon_vectors):
                if reduced[pivot]:
                    reduced = (
                        reduced - int(reduced[pivot]) * vector
                    ) % PRIME
            support = np.flatnonzero(reduced)
            if not len(support):
                continue
            pivot = int(support[0])
            reduced = (
                reduced * pow(int(reduced[pivot]), PRIME - 2, PRIME)
            ) % PRIME
            pivots.append(pivot)
            echelon_vectors.append(reduced)
            answer.append(
                [
                    (orbit[index], int(coefficient))
                    for index, coefficient in enumerate(raw)
                    if coefficient
                ]
            )
            if len(pivots) == maximum_orbit_rank:
                break
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weight", type=int, required=True, choices=SPECS)
    parser.add_argument("--block-size", type=int, default=512)
    arguments = parser.parse_args()

    weight = arguments.weight
    first, second, expected_columns, seed = SPECS[weight]
    character = (1 << weight) - 1

    start = time.time()
    block = sextic.character_block(character, 6)
    full_orbits = sextic.group_orbits(
        block, quartic.stabilizer_generators(weight)
    )
    maps, signs = young_operator(first, second, weight)
    irreducible_dimension = (
        specht_dimension(first) * specht_dimension(second)
    )
    projected = projected_basis(
        full_orbits, maps, signs, irreducible_dimension
    )
    assert len(projected) == expected_columns
    print(
        f"weight={weight} irreps={first}x{second} "
        f"multiplicity={len(projected)} preparation_seconds={time.time() - start}",
        flush=True,
    )

    start = time.time()
    _, evaluations = sextic.signed_evaluation_matrix(
        projected, len(projected) + 50, seed
    )
    print(f"evaluation_seconds={time.time() - start}", flush=True)

    start = time.time()
    rank = quartic.blocked_modular_rank(
        evaluations, PRIME, block_size=arguments.block_size
    )
    assert rank == expected_columns
    print(
        f"rank={rank} nullity=0 rank_seconds={time.time() - start}",
        flush=True,
    )


if __name__ == "__main__":
    main()
