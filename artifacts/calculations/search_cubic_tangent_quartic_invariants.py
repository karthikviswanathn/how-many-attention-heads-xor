#!/usr/bin/env python3
"""Search stabilizer-invariant quartic equations for the n=6 tangent map.

The 42 coefficient coordinates are indexed by subsets of [6] of size at
most three.  Coordinate sign changes by cube characters give every
homogeneous coefficient monomial an F_2^6 character, namely the symmetric
difference of its four coordinate subsets.  We inspect one representative
of each character weight.  Inside that block, we average over the character
stabilizer S_k times S_{6-k} and test whether any averaged quartic vanishes
on random tangent forms over F_101.

This is a search diagnostic, not an exact characteristic-zero certificate.
If a rank defect appears, its nullspace vector is a compact candidate for a
subsequent symbolic identity check.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from itertools import combinations_with_replacement

import numpy as np

import verify_cubic_tangent_dimension as tangent


PRIME = tangent.QUADRATIC_PRIME
DEGREE = 4


def tangent_sample_fourier_mod_prime(
    state: int,
) -> tuple[int, np.ndarray]:
    """Sample the tangent map in the Fourier quotient y_i^2 = 1."""
    dimension = 6
    output_monomials = tangent.monomials(dimension)
    output_index = {
        monomial: index for index, monomial in enumerate(output_monomials)
    }
    parameters = np.empty((6, dimension + 1), dtype=np.int64)
    for factor in range(6):
        for coordinate in range(dimension + 1):
            state, value = tangent.lcg(state)
            parameters[factor, coordinate] = value % PRIME

    answer = np.zeros(len(output_monomials), dtype=np.int64)
    denominators = parameters[:3]
    numerators = parameters[3:]
    for factor in range(3):
        other = [index for index in range(3) if index != factor]
        for first in range(dimension + 1):
            first_monomial = 0 if first == 0 else 1 << (first - 1)
            for second in range(dimension + 1):
                second_monomial = 0 if second == 0 else 1 << (second - 1)
                for third in range(dimension + 1):
                    third_monomial = 0 if third == 0 else 1 << (third - 1)
                    monomial = first_monomial ^ second_monomial ^ third_monomial
                    answer[output_index[monomial]] += (
                        numerators[factor, first]
                        * denominators[other[0], second]
                        * denominators[other[1], third]
                    )
    return state, answer % PRIME


def character_blocks(
    degree: int = DEGREE,
) -> dict[int, list[tuple[int, ...]]]:
    coordinate_masks = tangent.monomials(6)
    blocks: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for monomial in combinations_with_replacement(
        range(len(coordinate_masks)), degree
    ):
        character = 0
        for coordinate in monomial:
            character ^= coordinate_masks[coordinate]
        blocks[character].append(monomial)
    return blocks


def swap_bits(mask: int, first: int, second: int) -> int:
    first_bit = (mask >> first) & 1
    second_bit = (mask >> second) & 1
    if first_bit == second_bit:
        return mask
    return mask ^ (1 << first) ^ (1 << second)


def stabilizer_generators(weight: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        [(index, index + 1) for index in range(weight - 1)]
        + [(index, index + 1) for index in range(weight, 5)]
    )


def stabilizer_orbits(
    block: list[tuple[int, ...]], weight: int
) -> tuple[list[list[tuple[int, ...]]], dict[tuple[int, ...], int]]:
    coordinate_masks = tangent.monomials(6)
    coordinate_index = {
        mask: index for index, mask in enumerate(coordinate_masks)
    }
    generators = stabilizer_generators(weight)
    unseen = set(block)
    orbits: list[list[tuple[int, ...]]] = []
    orbit_index: dict[tuple[int, ...], int] = {}
    while unseen:
        seed = unseen.pop()
        orbit = [seed]
        queue = deque([seed])
        while queue:
            current = queue.popleft()
            for first, second in generators:
                neighbor = tuple(
                    sorted(
                        coordinate_index[
                            swap_bits(
                                coordinate_masks[coordinate], first, second
                            )
                        ]
                        for coordinate in current
                    )
                )
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    orbit.append(neighbor)
                    queue.append(neighbor)
        index = len(orbits)
        for monomial in orbit:
            orbit_index[monomial] = index
        orbits.append(orbit)
    return orbits, orbit_index


def orbit_evaluation(
    coefficients: np.ndarray,
    orbits: list[list[tuple[int, ...]]],
) -> np.ndarray:
    values = np.zeros(len(orbits), dtype=np.int64)
    for orbit_index, orbit in enumerate(orbits):
        value = 0
        for monomial in orbit:
            product = 1
            for coordinate in monomial:
                product = product * int(coefficients[coordinate]) % PRIME
            value += product
        values[orbit_index] = value % PRIME
    return values


def right_nullspace(
    matrix: np.ndarray, prime: int
) -> list[np.ndarray]:
    work = np.array(matrix, dtype=np.int64) % prime
    rows, columns = work.shape
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(columns):
        candidates = np.flatnonzero(work[pivot_row:, column])
        if len(candidates) == 0:
            continue
        pivot = pivot_row + int(candidates[0])
        work[[pivot_row, pivot]] = work[[pivot, pivot_row]]
        inverse = pow(int(work[pivot_row, column]), prime - 2, prime)
        work[pivot_row] = work[pivot_row] * inverse % prime
        for row in range(rows):
            if row == pivot_row or work[row, column] == 0:
                continue
            multiplier = int(work[row, column])
            work[row] = (work[row] - multiplier * work[pivot_row]) % prime
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break

    free_columns = [
        column for column in range(columns) if column not in pivot_columns
    ]
    answer = []
    for free in free_columns:
        vector = np.zeros(columns, dtype=np.int64)
        vector[free] = 1
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[row, free] % prime
        answer.append(vector)
    return answer


def modular_inverse(matrix: np.ndarray, prime: int) -> np.ndarray:
    size = len(matrix)
    work = np.column_stack(
        [np.array(matrix, dtype=np.int64) % prime,
         np.eye(size, dtype=np.int64)]
    )
    for column in range(size):
        candidates = np.flatnonzero(work[column:, column])
        assert len(candidates)
        pivot = column + int(candidates[0])
        work[[column, pivot]] = work[[pivot, column]]
        inverse = pow(int(work[column, column]), prime - 2, prime)
        work[column] = work[column] * inverse % prime
        for row in range(size):
            if row == column or work[row, column] == 0:
                continue
            multiplier = int(work[row, column])
            work[row] = (work[row] - multiplier * work[column]) % prime
    assert np.array_equal(work[:, :size], np.eye(size, dtype=np.int64))
    return work[:, size:]


def blocked_modular_rank(
    matrix: np.ndarray,
    prime: int,
    block_size: int = 32,
    verbose: bool = False,
) -> int:
    """Compute exact rank, using exact float matrix products for speed.

    Each floating matrix product has inner dimension at most block_size and
    residue entries below prime.  With the present constants, all intermediate
    integer sums are far below 2^53, so binary64 represents them exactly.
    """
    work = (np.array(matrix, dtype=np.int64) % prime).astype(np.uint8)
    answer = 0
    rng = np.random.default_rng(0xB10C)
    while min(work.shape) > block_size:
        rows, columns = work.shape
        size = block_size
        selected_rows: np.ndarray | None = None
        selected_columns: np.ndarray | None = None
        while size:
            for attempt in range(40):
                if attempt == 0:
                    row_choice = np.arange(size)
                    column_choice = np.arange(size)
                else:
                    row_choice = rng.choice(rows, size=size, replace=False)
                    column_choice = rng.choice(
                        columns, size=size, replace=False
                    )
                corner = work[np.ix_(row_choice, column_choice)]
                if tangent.modular_rank(corner, prime) == size:
                    selected_rows = row_choice
                    selected_columns = column_choice
                    break
            if selected_rows is not None:
                break
            size //= 2
        if not size:
            break
        remaining_rows = np.setdiff1d(
            np.arange(rows), selected_rows, assume_unique=True
        )
        remaining_columns = np.setdiff1d(
            np.arange(columns), selected_columns, assume_unique=True
        )
        row_order = np.concatenate([selected_rows, remaining_rows])
        column_order = np.concatenate(
            [selected_columns, remaining_columns]
        )
        work = work[np.ix_(row_order, column_order)]
        corner = work[:size, :size]
        upper_right = work[:size, size:]
        lower_left = work[size:, :size]
        lower_right = work[size:, size:]
        inverse = modular_inverse(corner, prime)
        left_factor = (np.rint(
            lower_left.astype(float) @ inverse.astype(float)
        ).astype(np.int64) % prime).astype(np.uint8)
        next_work = np.empty(lower_right.shape, dtype=np.uint8)
        upper_float = upper_right.astype(float)
        for row_start in range(0, len(lower_right), 512):
            row_stop = min(row_start + 512, len(lower_right))
            update = np.rint(
                left_factor[row_start:row_stop].astype(float) @ upper_float
            ).astype(np.int64) % prime
            next_work[row_start:row_stop] = (
                lower_right[row_start:row_stop].astype(np.int64) - update
            ) % prime
        work = next_work
        answer += size
        if verbose:
            print(
                f"    eliminated={answer} remaining={work.shape}",
                flush=True,
            )
    return answer + tangent.modular_rank(work, prime)


def full_block_evaluation(
    samples: np.ndarray, block: list[tuple[int, ...]]
) -> np.ndarray:
    indices = np.array(block, dtype=np.int64)
    answer = np.empty((len(samples), len(block)), dtype=np.int64)
    for row, coefficients in enumerate(samples):
        answer[row] = np.prod(coefficients[indices], axis=1) % PRIME
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-blocks", action="store_true")
    parser.add_argument("--degree", type=int, choices=(2, 3, 4), default=4)
    parser.add_argument("--weight", type=int, choices=range(7))
    arguments = parser.parse_args()
    blocks = character_blocks(arguments.degree)
    state = 0x51A71E
    weights = range(7) if arguments.weight is None else (arguments.weight,)
    if arguments.full_blocks:
        sample_count = max(
            len(blocks[(1 << weight) - 1]) for weight in weights
        ) + 25
        samples = np.empty((sample_count, 42), dtype=np.int64)
        for sample in range(sample_count):
            state, samples[sample] = tangent_sample_fourier_mod_prime(state)
    for weight in weights:
        character = (1 << weight) - 1
        block = blocks[character]
        if arguments.full_blocks:
            evaluations = full_block_evaluation(samples, block)
            rank = blocked_modular_rank(evaluations, PRIME)
            print(
                f"weight={weight}: full block={len(block)} rank={rank} "
                f"nullity={len(block) - rank}"
            )
            continue
        orbits, _ = stabilizer_orbits(block, weight)
        sample_count = len(orbits) + 25
        evaluations = np.empty(
            (sample_count, len(orbits)), dtype=np.int64
        )
        for sample in range(sample_count):
            state, coefficients = tangent_sample_fourier_mod_prime(state)
            evaluations[sample] = orbit_evaluation(coefficients, orbits)
        rank = tangent.modular_rank(evaluations, PRIME)
        nullity = len(orbits) - rank
        print(
            f"weight={weight}: block={len(block)} orbits={len(orbits)} "
            f"rank={rank} nullity={nullity}"
        )
        if nullity:
            vectors = right_nullspace(evaluations, PRIME)
            assert len(vectors) == nullity
            for index, vector in enumerate(vectors):
                support = np.flatnonzero(vector)
                print(
                    f"  candidate={index} support={len(support)} "
                    f"vector={vector.tolist()}"
                )


if __name__ == "__main__":
    main()
