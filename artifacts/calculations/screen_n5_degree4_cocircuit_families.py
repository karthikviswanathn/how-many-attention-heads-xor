#!/usr/bin/env python3
"""Screen the 65 five-bit degree-four affine-cocircuit families for H4.

For one affine-normal orbit, labels away from the hyperplane are fixed after
the parity twist, while the labels on the zero set are arbitrary.  This
diagnostic enumerates that small extension cube, then screens it against a
finite dictionary of admissible four-head denominator tuples.  A fixed-space
hit is valid numerical evidence; a miss is not a head lower bound.
"""

from __future__ import annotations

import argparse
import itertools
import math

import numpy as np

import search_adversarial_low_dimension as core
import verify_n5_degree4_reduction as reduction
import verify_n5_high_degree_candidate_refutations as samples


N = 5
HEADS = 4
WIDTH = N + 1
VERTICES = 1 << N


def canonical_tuple(denominators: np.ndarray) -> tuple[tuple[int, ...], ...]:
    rows = []
    for denominator in denominators:
        values = [int(value) for value in denominator]
        common = 0
        for value in values:
            common = math.gcd(common, abs(value))
        if common > 1:
            values = [value // common for value in values]
        rows.append(tuple(values))
    return tuple(sorted(rows))


def oriented_denominator(weights: np.ndarray, orientation: int) -> np.ndarray:
    integers = np.maximum(1, np.rint(weights)).astype(np.int64)
    if orientation > 0:
        return integers
    return np.concatenate(
        [[int(np.sum(integers))], -integers[1:]]
    ).astype(np.int64)


def global_complement_denominator(denominator: np.ndarray) -> np.ndarray:
    constant = int(denominator[0] + np.sum(denominator[1:]))
    return np.concatenate([[constant], -denominator[1:]])


def denominator_dictionary(size: int, seed: int) -> list[np.ndarray]:
    degree_four = next(
        certificate
        for certificate in samples.CERTIFICATES
        if certificate["degree"] == 4
    )
    base = np.array(degree_four["denominators"], dtype=np.int64)
    candidates = []
    for permutation in itertools.permutations(range(N)):
        current = np.column_stack(
            [base[:, 0], base[:, 1 + np.array(permutation)]]
        )
        candidates.append(current)
        candidates.append(
            np.vstack(
                [global_complement_denominator(row) for row in current]
            )
        )

    rng = np.random.default_rng(seed)
    while len(candidates) < 4 * size:
        orientations = rng.choice((-1, 1), size=HEADS)
        literal_weights = np.exp(
            rng.uniform(0.0, 9.0, size=(HEADS, WIDTH))
        )
        candidates.append(
            np.vstack(
                [
                    oriented_denominator(literal_weights[head], orientation)
                    for head, orientation in enumerate(orientations)
                ]
            )
        )

    answer = []
    seen = set()
    affine = core.affine_matrix(N).astype(object)
    for denominators in candidates:
        key = canonical_tuple(denominators)
        if key in seen:
            continue
        array = np.array(key, dtype=np.int64)
        if not np.all(affine @ array.astype(object).T > 0):
            continue
        seen.add(key)
        answer.append(array)
        if len(answer) >= size:
            break
    return answer


def whitened_features(denominators: np.ndarray) -> np.ndarray:
    affine = core.affine_matrix(N).astype(float)
    values = affine @ denominators.astype(float).T
    raw = np.column_stack(
        [np.ones(VERTICES)]
        + [affine / values[:, head, None] for head in range(HEADS)]
    )
    left, singular, _ = np.linalg.svd(raw, full_matrices=False)
    keep = singular > 1e-11 * singular[0]
    basis = left[:, keep]
    return basis / np.linalg.norm(basis, axis=1, keepdims=True)


def orbit_normals() -> list[tuple[int, ...]]:
    features = reduction.affine_features()
    normals = reduction.enumerate_rank_five_normals(features)
    representatives: dict[tuple[int, ...], tuple[int, ...]] = {}
    for normal in normals:
        key = reduction.normal_orbit_key(normal)
        representatives.setdefault(key, normal)
    return sorted(representatives.values(), key=lambda normal: (
        int(np.count_nonzero(features @ np.array(normal) == 0)),
        reduction.normal_orbit_key(normal),
    ))


def extension_signs(normal: tuple[int, ...]) -> np.ndarray:
    features = reduction.affine_features().astype(np.int64)
    values = features @ np.array(normal, dtype=np.int64)
    zero = np.flatnonzero(values == 0)
    choices = np.arange(1 << len(zero), dtype=np.uint32)
    twisted = np.sign(values)[None, :].astype(np.int8).repeat(
        len(choices), axis=0
    )
    for coordinate, vertex in enumerate(zero):
        twisted[:, vertex] = np.where(
            (choices >> coordinate) & 1, 1, -1
        )
    # Constant twisted tables give parity or its complement, whose threshold
    # degree is five.  They occur for supporting-hyperplane representatives
    # and are not part of the exact degree-four class.
    twisted = twisted[np.any(twisted != twisted[:, :1], axis=1)]
    parity = np.array(
        [1 if bin(vertex).count("1") % 2 == 0 else -1 for vertex in range(32)],
        dtype=np.int8,
    )
    signs = twisted * parity[None, :]
    # Output complement preserves head complexity.  Canonicalize each target
    # independently without discarding any zero-set assignment.
    signs[signs[:, 0] > 0] *= -1
    return signs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary-size", type=int, default=256)
    parser.add_argument("--iterations", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--zero-size", type=int)
    arguments = parser.parse_args()

    normals = orbit_normals()
    selected = arguments.orbit or list(range(len(normals)))
    dictionary = denominator_dictionary(arguments.dictionary_size, arguments.seed)
    spaces = [whitened_features(denominators) for denominators in dictionary]
    features = reduction.affine_features()
    print(f"dictionary size: {len(dictionary)}")
    for orbit in selected:
        normal = normals[orbit]
        zero_count = int(
            np.count_nonzero(features @ np.array(normal) == 0)
        )
        if arguments.zero_size is not None and zero_count != arguments.zero_size:
            continue
        signs = extension_signs(normal)
        covered = np.zeros(len(signs), dtype=bool)
        for space in spaces:
            active = np.flatnonzero(~covered)
            if not len(active):
                break
            covered[active] = core.gilbert_cover(
                signs[active], space, arguments.iterations
            )
        print(
            f"orbit={orbit} zero={zero_count} extensions={len(signs)} "
            f"covered={int(np.sum(covered))} "
            f"uncovered={int(np.sum(~covered))} normal={normal}"
        )
    print("warning: dictionary misses are only search evidence")


if __name__ == "__main__":
    main()
