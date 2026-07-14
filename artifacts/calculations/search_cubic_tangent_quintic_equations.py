#!/usr/bin/env python3
"""Search symmetric quintic equations for the n=6 cubic tangent image.

Only the two F_2^6 character blocks fixed by all coordinate permutations are
inspected: character zero and character [6].  For each block, the script
tests both S_6 orbit sums and S_5 orbit sums, where S_5 fixes coordinate zero.
The latter contains exactly the trivial and standard S_6 isotypic pieces.

Rank defects from random evaluation are candidate equations only.  A reported
candidate must still be checked by exact symbolic substitution before it is
called an equation of the tangent image.
"""

from __future__ import annotations

import argparse
from collections import deque
from itertools import combinations_with_replacement
import math

import numpy as np

import search_cubic_tangent_quartic_invariants as quartic
import verify_cubic_tangent_dimension as tangent


PRIME = tangent.QUADRATIC_PRIME
DEGREE = 5


def character_block(
    character: int, degree: int = DEGREE
) -> list[tuple[int, ...]]:
    coordinate_masks = tangent.monomials(6)
    block = []
    for monomial in combinations_with_replacement(
        range(len(coordinate_masks)), degree
    ):
        value = 0
        for coordinate in monomial:
            value ^= coordinate_masks[coordinate]
        if value == character:
            block.append(monomial)
    return block


def group_orbits(
    block: list[tuple[int, ...]],
    generators: tuple[tuple[int, int], ...],
) -> list[list[tuple[int, ...]]]:
    coordinate_masks = tangent.monomials(6)
    coordinate_index = {
        mask: index for index, mask in enumerate(coordinate_masks)
    }
    unseen = set(block)
    orbits: list[list[tuple[int, ...]]] = []
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
                            quartic.swap_bits(
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
        orbits.append(orbit)
    return orbits


def signed_group_orbits(
    block: list[tuple[int, ...]],
    generators: tuple[tuple[int, int], ...],
) -> list[list[tuple[tuple[int, ...], int]]]:
    """Return orbit bases transforming by the sign of the subgroup."""
    coordinate_masks = tangent.monomials(6)
    coordinate_index = {
        mask: index for index, mask in enumerate(coordinate_masks)
    }
    unseen = set(block)
    answer: list[list[tuple[tuple[int, ...], int]]] = []
    while unseen:
        seed = unseen.pop()
        signs = {seed: 1}
        queue = deque([seed])
        valid = True
        while queue:
            current = queue.popleft()
            for first, second in generators:
                neighbor = tuple(
                    sorted(
                        coordinate_index[
                            quartic.swap_bits(
                                coordinate_masks[coordinate], first, second
                            )
                        ]
                        for coordinate in current
                    )
                )
                required_sign = -signs[current]
                if neighbor in signs:
                    if signs[neighbor] != required_sign:
                        valid = False
                    continue
                signs[neighbor] = required_sign
                unseen.remove(neighbor)
                queue.append(neighbor)
        if valid:
            answer.append(list(signs.items()))
    return answer


def twisted_group_orbits(
    block: list[tuple[int, ...]],
    generators: tuple[tuple[int, int, int], ...],
) -> list[list[tuple[tuple[int, ...], int]]]:
    """Return orbit bases for a specified one-dimensional character."""
    coordinate_masks = tangent.monomials(6)
    coordinate_index = {
        mask: index for index, mask in enumerate(coordinate_masks)
    }
    unseen = set(block)
    answer: list[list[tuple[tuple[int, ...], int]]] = []
    while unseen:
        seed = unseen.pop()
        signs = {seed: 1}
        queue = deque([seed])
        valid = True
        while queue:
            current = queue.popleft()
            for first, second, generator_sign in generators:
                neighbor = tuple(
                    sorted(
                        coordinate_index[
                            quartic.swap_bits(
                                coordinate_masks[coordinate], first, second
                            )
                        ]
                        for coordinate in current
                    )
                )
                required_sign = generator_sign * signs[current]
                if neighbor in signs:
                    if signs[neighbor] != required_sign:
                        valid = False
                    continue
                signs[neighbor] = required_sign
                unseen.remove(neighbor)
                queue.append(neighbor)
        if valid:
            answer.append(list(signs.items()))
    return answer


def evaluation_matrix(
    orbits: list[list[tuple[int, ...]]],
    sample_count: int,
    state: int,
) -> tuple[int, np.ndarray]:
    monomial_indices = np.array(
        [monomial for orbit in orbits for monomial in orbit],
        dtype=np.int64,
    )
    orbit_indices = np.repeat(
        np.arange(len(orbits), dtype=np.int64),
        [len(orbit) for orbit in orbits],
    )
    matrix = np.empty((sample_count, len(orbits)), dtype=np.uint8)
    for sample in range(sample_count):
        state, coefficients = quartic.tangent_sample_fourier_mod_prime(state)
        monomial_values = (
            np.prod(coefficients[monomial_indices], axis=1) % PRIME
        )
        orbit_values = np.bincount(
            orbit_indices,
            weights=monomial_values,
            minlength=len(orbits),
        )
        matrix[sample] = np.rint(orbit_values).astype(np.int64) % PRIME
    return state, matrix


def signed_evaluation_matrix(
    orbits: list[list[tuple[tuple[int, ...], int]]],
    sample_count: int,
    state: int,
) -> tuple[int, np.ndarray]:
    monomial_indices = np.array(
        [monomial for orbit in orbits for monomial, _ in orbit],
        dtype=np.int64,
    )
    monomial_signs = np.array(
        [sign for orbit in orbits for _, sign in orbit], dtype=np.int64
    )
    orbit_indices = np.repeat(
        np.arange(len(orbits), dtype=np.int64),
        [len(orbit) for orbit in orbits],
    )
    matrix = np.empty((sample_count, len(orbits)), dtype=np.uint8)
    for sample in range(sample_count):
        state, coefficients = quartic.tangent_sample_fourier_mod_prime(state)
        monomial_values = (
            np.prod(coefficients[monomial_indices], axis=1)
            * monomial_signs
        ) % PRIME
        orbit_values = np.bincount(
            orbit_indices,
            weights=monomial_values,
            minlength=len(orbits),
        )
        matrix[sample] = np.rint(orbit_values).astype(np.int64) % PRIME
    return state, matrix


def partitions(total: int, maximum: int | None = None) -> list[tuple[int, ...]]:
    if total == 0:
        return [()]
    if maximum is None:
        maximum = total
    answer = []
    for first in range(min(total, maximum), 0, -1):
        for rest in partitions(total - first, first):
            answer.append((first,) + rest)
    return answer


def young_generators(
    partition: tuple[int, ...], offset: int
) -> tuple[tuple[int, int], ...]:
    answer = []
    cursor = offset
    for part in partition:
        answer.extend((index, index + 1) for index in range(cursor, cursor + part - 1))
        cursor += part
    return tuple(answer)


def conjugate_partition(
    partition: tuple[int, ...]
) -> tuple[int, ...]:
    if not partition:
        return ()
    return tuple(
        sum(part >= column for part in partition)
        for column in range(1, partition[0] + 1)
    )


def young_subgroup_order(partition: tuple[int, ...]) -> int:
    answer = 1
    for part in partition:
        answer *= math.factorial(part)
    return answer


def representation_detector(
    partition: tuple[int, ...], offset: int
) -> tuple[str, tuple[tuple[int, int, int], ...]]:
    conjugate = conjugate_partition(partition)
    if young_subgroup_order(partition) >= young_subgroup_order(conjugate):
        return (
            f"trivial@{partition}",
            tuple(
                (first, second, 1)
                for first, second in young_generators(partition, offset)
            ),
        )
    return (
        f"sign@{conjugate}",
        tuple(
            (first, second, -1)
            for first, second in young_generators(conjugate, offset)
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-weights", action="store_true")
    parser.add_argument("--young", action="store_true")
    parser.add_argument("--complete-representations", action="store_true")
    parser.add_argument("--weight", type=int, choices=range(7))
    parser.add_argument("--degree", type=int, choices=(5, 6), default=5)
    parser.add_argument("--maximum-orbits", type=int, default=2500)
    parser.add_argument("--complete-maximum-orbits", type=int)
    arguments = parser.parse_args()
    state = 0x51517
    symmetric_generators = tuple((index, index + 1) for index in range(5))
    fixed_point_generators = tuple(
        (index, index + 1) for index in range(1, 5)
    )
    if arguments.weight is not None:
        weights = (arguments.weight,)
    else:
        weights = range(7) if arguments.all_weights else (0, 6)
    for weight in weights:
        character = (1 << weight) - 1
        block = character_block(character, arguments.degree)
        print(
            f"character={character}: coefficient monomials={len(block)}",
            flush=True,
        )
        if arguments.complete_representations:
            detector_groups = []
            for first_partition in partitions(weight):
                first_name, first_generators = representation_detector(
                    first_partition, 0
                )
                for second_partition in partitions(6 - weight):
                    second_name, second_generators = representation_detector(
                        second_partition, weight
                    )
                    detector_groups.append(
                        (
                            first_partition,
                            second_partition,
                            f"{first_name}x{second_name}",
                            first_generators + second_generators,
                        )
                    )
            for first_partition, second_partition, name, generators in detector_groups:
                orbits = twisted_group_orbits(block, generators)
                if (
                    arguments.complete_maximum_orbits is not None
                    and len(orbits) > arguments.complete_maximum_orbits
                ):
                    print(
                        f"  irreps={first_partition}x{second_partition} "
                        f"detector={name} orbits={len(orbits)} skipped",
                        flush=True,
                    )
                    continue
                sample_count = len(orbits) + 50
                state, evaluations = signed_evaluation_matrix(
                    orbits, sample_count, state
                )
                rank = (
                    quartic.blocked_modular_rank(
                        evaluations, PRIME, block_size=256
                    )
                    if len(orbits) > 256
                    else tangent.modular_rank(evaluations, PRIME)
                )
                nullity = len(orbits) - rank
                print(
                    f"  irreps={first_partition}x{second_partition} "
                    f"detector={name} orbits={len(orbits)} rank={rank} "
                    f"nullity={nullity}",
                    flush=True,
                )
                if nullity:
                    print("  found a quintic equation component", flush=True)
                    return
            continue
        if arguments.young:
            groups = []
            for first_partition in partitions(weight):
                for second_partition in partitions(6 - weight):
                    groups.append(
                        (
                            f"{first_partition}x{second_partition}",
                            young_generators(first_partition, 0)
                            + young_generators(second_partition, weight),
                        )
                    )
        else:
            groups = [
                (
                    f"S{weight}xS{6 - weight}",
                    quartic.stabilizer_generators(weight),
                )
            ]
        if weight in (0, 6) and not arguments.young:
            groups = [
                ("S6", symmetric_generators),
                ("S5", fixed_point_generators),
            ]
        for name, generators in groups:
            orbits = group_orbits(block, generators)
            if len(orbits) > arguments.maximum_orbits:
                print(
                    f"  {name}: orbits={len(orbits)} skipped",
                    flush=True,
                )
                continue
            sample_count = len(orbits) + 50
            state, evaluations = evaluation_matrix(
                orbits, sample_count, state
            )
            if len(orbits) > 256:
                rank = quartic.blocked_modular_rank(evaluations, PRIME)
            else:
                rank = tangent.modular_rank(evaluations, PRIME)
            nullity = len(orbits) - rank
            print(
                f"  {name}: orbits={len(orbits)} rank={rank} "
                f"nullity={nullity}",
                flush=True,
            )
            if nullity:
                if len(orbits) > 1000:
                    continue
                vectors = quartic.right_nullspace(evaluations, PRIME)
                assert len(vectors) == nullity
                for index, vector in enumerate(vectors):
                    support = np.flatnonzero(vector)
                    print(
                        f"    candidate={index} support={len(support)} "
                        f"vector={vector.tolist()}",
                        flush=True,
                    )


if __name__ == "__main__":
    main()
