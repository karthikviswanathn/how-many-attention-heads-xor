#!/usr/bin/env python3
"""Verify the four minimum-support quadratic circuit types on five bits."""

from __future__ import annotations

import itertools

import numpy as np

import sample_n5_quadratic_circuit_orbits as orbits
import verify_n5_degree3_circuit_reduction as reduction


N = 5
VERTICES = 1 << N


def minimum_affine_factors() -> list[tuple[str, np.ndarray]]:
    cube = reduction.sign_cube()
    factors = []
    for coordinate in range(N):
        for sign in (-1, 1):
            factors.append(
                (
                    f"1 {sign:+d} z{coordinate + 1}",
                    1 + sign * cube[:, coordinate],
                )
            )
    for first, second in itertools.combinations(range(N), 2):
        for sign in (-1, 1):
            factors.append(
                (
                    f"z{first + 1} {sign:+d} z{second + 1}",
                    cube[:, first] + sign * cube[:, second],
                )
            )
    assert len(factors) == 30
    assert all(np.count_nonzero(values) == 16 for _, values in factors)
    return factors


def main() -> None:
    features = reduction.quadratic_fourier_features()
    parity = np.prod(reduction.sign_cube(), axis=1)
    full_automorphisms = orbits.cube_automorphisms()
    head_automorphisms = orbits.head_symmetry_automorphisms()
    full_orbits: dict[int, tuple[str, str]] = {}
    head_orbits = set()
    qualifying_pairs = 0
    for (first_name, first), (second_name, second) in itertools.combinations(
        minimum_affine_factors(), 2
    ):
        product = first * second
        if np.count_nonzero(product) != 8:
            continue
        assert np.all(product % 4 == 0)
        quadratic = product // 4
        dependency = parity * quadratic
        circuit_signs = np.sign(dependency).astype(np.int8)
        support = np.flatnonzero(circuit_signs)
        assert len(support) == 8
        assert np.all(features.T @ dependency == 0)
        assert reduction.modular_rank(features[support]) == 7
        full_key = orbits.canonical_key(
            circuit_signs, full_automorphisms
        )
        head_key = orbits.canonical_key(
            circuit_signs, head_automorphisms
        )
        full_orbits.setdefault(full_key, (first_name, second_name))
        head_orbits.add(head_key)
        qualifying_pairs += 1

    expected_types = {
        ("z1 -1 z2", "z1 -1 z3"),
        ("z1 -1 z2", "z3 -1 z4"),
        ("1 -1 z1", "z2 -1 z3"),
        ("1 -1 z1", "1 -1 z2"),
    }
    assert set(full_orbits.values()) == expected_types
    assert len(full_orbits) == 4
    assert len(head_orbits) == 9
    assert qualifying_pairs == 420
    print("minimum affine factors: 30")
    print("qualifying factor pairs: 420")
    print("full-cube support-eight circuit orbits: 4")
    print("head-symmetry support-eight circuit orbits: 9")
    for index, pair in enumerate(full_orbits.values()):
        print(f"type {index + 1}: ({pair[0]})({pair[1]})")
    print("verified five-bit support-eight circuit classification data")


if __name__ == "__main__":
    main()
