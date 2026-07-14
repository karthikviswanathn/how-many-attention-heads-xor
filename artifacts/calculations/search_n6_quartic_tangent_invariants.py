#!/usr/bin/env python3
"""Search low-degree equations of the six-bit quartic tangent image.

Coefficient monomials split into 64 blocks under coordinate sign changes.
Coordinate permutations identify blocks with character labels of equal
Hamming weight, so one representative of each weight suffices.  Full column
rank over F_101 proves that the corresponding equation block is zero.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from itertools import combinations_with_replacement

import numpy as np

import search_cubic_tangent_quartic_invariants as cubic_search
import verify_cubic_tangent_dimension as cubic
import verify_n6_quartic_tangent_dimension as tangent


PRIME = tangent.SAMPLE_PRIME


def character_blocks(
    degree: int, selected_characters: set[int] | None = None
) -> dict[int, list[tuple[int, ...]]]:
    blocks: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for monomial in combinations_with_replacement(
        range(len(tangent.OUTPUT_MONOMIALS)), degree
    ):
        character = 0
        for coordinate in monomial:
            character ^= tangent.OUTPUT_MONOMIALS[coordinate]
        if selected_characters is None or character in selected_characters:
            blocks[character].append(monomial)
    return blocks


def full_block_evaluation(
    samples: np.ndarray, block: list[tuple[int, ...]]
) -> np.ndarray:
    indices = np.array(block, dtype=np.int64)
    answer = np.empty((len(samples), len(block)), dtype=np.uint8)
    for row, coefficients in enumerate(samples):
        answer[row] = (
            np.prod(coefficients[indices], axis=1) % PRIME
        ).astype(np.uint8)
    return answer


def swap_bits(mask: int, first: int, second: int) -> int:
    first_bit = (mask >> first) & 1
    second_bit = (mask >> second) & 1
    if first_bit == second_bit:
        return mask
    return mask ^ (1 << first) ^ (1 << second)


def stabilizer_orbits(
    block: list[tuple[int, ...]], weight: int
) -> list[list[tuple[int, ...]]]:
    coordinate_index = {
        mask: index for index, mask in enumerate(tangent.OUTPUT_MONOMIALS)
    }
    generators = tuple(
        [(index, index + 1) for index in range(weight - 1)]
        + [(index, index + 1) for index in range(weight, 5)]
    )
    unseen = set(block)
    orbits: list[list[tuple[int, ...]]] = []
    while unseen:
        seed = unseen.pop()
        unseen_orbit = [seed]
        queue = deque([seed])
        while queue:
            current = queue.popleft()
            for first, second in generators:
                neighbor = tuple(
                    sorted(
                        coordinate_index[
                            swap_bits(
                                tangent.OUTPUT_MONOMIALS[coordinate],
                                first,
                                second,
                            )
                        ]
                        for coordinate in current
                    )
                )
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    unseen_orbit.append(neighbor)
                    queue.append(neighbor)
        orbits.append(unseen_orbit)
    return orbits


def orbit_evaluation(
    samples: np.ndarray, orbits: list[list[tuple[int, ...]]]
) -> np.ndarray:
    monomial_indices = np.array(
        [monomial for orbit in orbits for monomial in orbit], dtype=np.int64
    )
    orbit_indices = np.repeat(
        np.arange(len(orbits), dtype=np.int64),
        [len(orbit) for orbit in orbits],
    )
    answer = np.empty((len(samples), len(orbits)), dtype=np.uint8)
    for row, coefficients in enumerate(samples):
        monomial_values = (
            np.prod(coefficients[monomial_indices], axis=1) % PRIME
        )
        orbit_values = np.bincount(
            orbit_indices,
            weights=monomial_values,
            minlength=len(orbits),
        )
        answer[row] = (
            np.rint(orbit_values).astype(np.int64) % PRIME
        ).astype(np.uint8)
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--degree", type=int, choices=(2, 3, 4, 5), required=True
    )
    parser.add_argument("--weight", type=int, choices=range(7))
    parser.add_argument("--extra-samples", type=int, default=20)
    parser.add_argument("--block-size", type=int, default=32)
    parser.add_argument("--orbit-sums", action="store_true")
    arguments = parser.parse_args()

    weights = range(7) if arguments.weight is None else (arguments.weight,)
    if arguments.degree == 5 and arguments.weight is None:
        raise ValueError("degree five must be run one character weight at a time")
    characters = {(1 << weight) - 1 for weight in weights}
    blocks = character_blocks(arguments.degree, characters)
    selected: dict[int, tuple[list[tuple[int, ...]], object]] = {}
    maximum_columns = 0
    for weight in weights:
        block = blocks[(1 << weight) - 1]
        if arguments.orbit_sums:
            orbits = stabilizer_orbits(block, weight)
            selected[weight] = (block, orbits)
            maximum_columns = max(maximum_columns, len(orbits))
        else:
            selected[weight] = (block, block)
            maximum_columns = max(maximum_columns, len(block))
    sample_count = maximum_columns + arguments.extra_samples
    samples = np.empty(
        (sample_count, len(tangent.OUTPUT_MONOMIALS)), dtype=np.uint8
    )
    state = 0xF049
    for sample in range(sample_count):
        state, coefficients = tangent.tangent_sample_mod_prime(state)
        samples[sample] = coefficients.astype(np.uint8)

    for weight in weights:
        character = (1 << weight) - 1
        block, columns = selected[weight]
        if arguments.orbit_sums:
            assert isinstance(columns, list)
            evaluations = orbit_evaluation(samples, columns)
        else:
            evaluations = full_block_evaluation(samples, block)
        if evaluations.shape[1] < 1000:
            rank = cubic.modular_rank(evaluations, PRIME)
        else:
            rank = cubic_search.blocked_modular_rank(
                evaluations,
                PRIME,
                block_size=arguments.block_size,
                verbose=True,
            )
        print(
            f"degree={arguments.degree} weight={weight}: "
            f"block={len(block)} columns={evaluations.shape[1]} "
            f"rank={rank} nullity={evaluations.shape[1] - rank}",
            flush=True,
        )


if __name__ == "__main__":
    main()
