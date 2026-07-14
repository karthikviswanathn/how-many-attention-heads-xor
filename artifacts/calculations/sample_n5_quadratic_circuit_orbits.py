#!/usr/bin/env python3
"""Sample symmetry orbits of five-bit quadratic Fourier circuits.

Random rank-15 zero sets generate quadratic cocircuits.  Parity reorientation
turns them into circuits.  The output estimates orbit diversity and support
sizes only.  It is not an exhaustive enumeration.
"""

from __future__ import annotations

import argparse
import itertools
import math

import numpy as np
import sympy as sp

import verify_n5_degree3_circuit_reduction as reduction


N = 5
VERTICES = 1 << N


def cube_automorphisms() -> np.ndarray:
    vertices = np.arange(VERTICES, dtype=np.int64)
    answer = []
    for permutation in itertools.permutations(range(N)):
        permuted = np.zeros(VERTICES, dtype=np.int64)
        for target, source in enumerate(permutation):
            permuted |= ((vertices >> source) & 1) << target
        for flip in range(VERTICES):
            answer.append(permuted ^ flip)
    return np.array(answer, dtype=np.int64)


def head_symmetry_automorphisms() -> np.ndarray:
    """Return permutations and simultaneous input complementation only."""
    vertices = np.arange(VERTICES, dtype=np.int64)
    answer = []
    for permutation in itertools.permutations(range(N)):
        permuted = np.zeros(VERTICES, dtype=np.int64)
        for target, source in enumerate(permutation):
            permuted |= ((vertices >> source) & 1) << target
        answer.append(permuted)
        answer.append(permuted ^ (VERTICES - 1))
    return np.array(answer, dtype=np.int64)


def canonical_key(signs: np.ndarray, automorphisms: np.ndarray) -> int:
    digits = signs.astype(np.int64) + 1
    powers = np.array([3**index for index in range(VERTICES)], dtype=np.uint64)
    transformed = digits[automorphisms].astype(np.uint64)
    codes = transformed @ powers
    complement_codes = (2 - transformed) @ powers
    return int(min(np.min(codes), np.min(complement_codes)))


def exact_dependency(signs: np.ndarray, features: np.ndarray) -> np.ndarray:
    support = np.flatnonzero(signs)
    nullspace = sp.Matrix(features[support].T.tolist()).nullspace()
    assert len(nullspace) == 1
    vector = nullspace[0]
    denominator_lcm = 1
    for value in vector:
        denominator_lcm = math.lcm(denominator_lcm, int(value.q))
    integers = np.array(
        [int(value * denominator_lcm) for value in vector], dtype=np.int64
    )
    common = 0
    for value in integers:
        common = math.gcd(common, abs(int(value)))
    integers //= common
    if np.sign(integers[0]) != signs[support[0]]:
        integers *= -1
    assert np.array_equal(np.sign(integers), signs[support])
    dependency = np.zeros(VERTICES, dtype=np.int64)
    dependency[support] = integers
    assert np.all(features.T @ dependency == 0)
    return dependency


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument(
        "--head-symmetry",
        action="store_true",
        help=(
            "Canonicalize only by head-complexity symmetries: coordinate "
            "permutations, simultaneous input complementation, and output "
            "complementation."
        ),
    )
    parser.add_argument(
        "--show-support",
        type=int,
        help="Print exact representatives having this circuit support size.",
    )
    arguments = parser.parse_args()

    rng = np.random.default_rng(arguments.seed)
    integer_features = reduction.quadratic_fourier_features()
    features = integer_features.astype(float)
    parity = np.prod(reduction.sign_cube(), axis=1)
    if arguments.head_symmetry:
        automorphisms = head_symmetry_automorphisms()
        assert automorphisms.shape == (240, 32)
    else:
        automorphisms = cube_automorphisms()
        assert automorphisms.shape == (3840, 32)

    orbits: dict[int, np.ndarray] = {}
    accepted = 0
    attempts = 0
    while accepted < arguments.samples:
        attempts += 1
        zero = np.sort(rng.choice(VERTICES, size=15, replace=False))
        _, singular, right = np.linalg.svd(features[zero], full_matrices=True)
        if singular[-1] < 1e-9:
            continue
        normal = right[-1]
        values = features @ normal
        scale = max(1.0, float(np.max(np.abs(values))))
        zero_mask = np.abs(values) < 1e-8 * scale
        if int(np.sum(zero_mask)) < 15:
            continue
        if reduction.modular_rank(integer_features[zero_mask]) != 15:
            continue
        circuit_signs = np.zeros(VERTICES, dtype=np.int8)
        circuit_signs[~zero_mask] = (
            parity[~zero_mask] * np.sign(values[~zero_mask])
        ).astype(np.int8)
        support = int(np.count_nonzero(circuit_signs))
        if not 8 <= support <= 17:
            continue
        key = canonical_key(circuit_signs, automorphisms)
        orbits.setdefault(key, circuit_signs.copy())
        accepted += 1

    distribution: dict[int, int] = {}
    for signs in orbits.values():
        support = int(np.count_nonzero(signs))
        distribution[support] = distribution.get(support, 0) + 1
    print(f"accepted samples: {accepted}")
    print(f"attempts: {attempts}")
    print(f"observed symmetry orbits: {len(orbits)}")
    print(f"orbit support distribution: {dict(sorted(distribution.items()))}")
    if arguments.show_support is not None:
        selected = [
            (key, signs)
            for key, signs in orbits.items()
            if np.count_nonzero(signs) == arguments.show_support
        ]
        for index, (key, signs) in enumerate(sorted(selected)):
            dependency = exact_dependency(signs, integer_features)
            support = np.flatnonzero(signs)
            print(
                f"representative={index} key={key} "
                f"support={tuple(int(value) for value in support)} "
                f"weights={tuple(int(dependency[value]) for value in support)}"
            )
    print("warning: sampling is not exhaustive")


if __name__ == "__main__":
    main()
