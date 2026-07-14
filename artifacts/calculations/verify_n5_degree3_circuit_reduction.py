#!/usr/bin/env python3
"""Verify exact data for the five-bit degree-three circuit reduction."""

from __future__ import annotations

import itertools

import numpy as np

import verify_n5_high_degree_candidate_refutations as samples


N = 5
VERTICES = 1 << N
PRIME = 101


def sign_cube() -> np.ndarray:
    bits = (
        (np.arange(VERTICES)[:, None] >> np.arange(N)) & 1
    ).astype(np.int64)
    return 1 - 2 * bits


def quadratic_fourier_features() -> np.ndarray:
    cube = sign_cube()
    columns = []
    for degree in range(3):
        for subset in itertools.combinations(range(N), degree):
            if subset:
                columns.append(np.prod(cube[:, subset], axis=1))
            else:
                columns.append(np.ones(VERTICES, dtype=np.int64))
    return np.column_stack(columns)


def modular_rank(matrix: np.ndarray, prime: int = PRIME) -> int:
    work = np.array(matrix, dtype=np.int64) % prime
    rows, columns = work.shape
    rank = 0
    for column in range(columns):
        candidates = np.flatnonzero(work[rank:, column])
        if len(candidates) == 0:
            continue
        pivot = rank + int(candidates[0])
        work[[rank, pivot]] = work[[pivot, rank]]
        inverse = pow(int(work[rank, column]), prime - 2, prime)
        work[rank] = work[rank] * inverse % prime
        for row in range(rows):
            if row == rank or work[row, column] == 0:
                continue
            multiplier = int(work[row, column])
            work[row] = (work[row] - multiplier * work[rank]) % prime
        rank += 1
        if rank == rows:
            break
    return rank


def verify_gale_self_duality() -> tuple[np.ndarray, np.ndarray]:
    features = quadratic_fourier_features()
    parity = np.prod(sign_cube(), axis=1)
    assert features.shape == (32, 16)
    assert modular_rank(features) == 16
    dual = parity[:, None] * features
    assert modular_rank(dual) == 16
    assert np.all(features.T @ dual == 0)
    combined = np.column_stack([features, dual])
    assert modular_rank(combined) == 32
    return features, parity


def verify_archived_circuits(
    features: np.ndarray, parity: np.ndarray
) -> None:
    sizes = []
    for certificate in samples.CERTIFICATES:
        if int(certificate["degree"]) != 3:
            continue
        signs = samples.signs_from_mask(int(certificate["mask"])).astype(
            np.int64
        )
        support = np.array(
            certificate["degree_lower_support"], dtype=np.int64
        )
        dependency = np.zeros(VERTICES, dtype=np.int64)
        dependency[support] = signs[support]
        assert np.all(features.T @ dependency == 0)
        assert modular_rank(features[support]) == len(support) - 1

        quadratic_values = parity * dependency
        scaled_coefficients = features.T @ quadratic_values
        assert np.all(features @ scaled_coefficients == 32 * quadratic_values)
        twisted = parity * signs
        weak_products = twisted * quadratic_values
        assert np.all(weak_products >= 0)
        assert np.all(weak_products[support] > 0)
        sizes.append(len(support))
    assert sorted(sizes) == [8, 12]


def verify_coordinate_face_circuits(features: np.ndarray) -> None:
    cube = sign_cube()
    count = 0
    for free in itertools.combinations(range(N), 3):
        fixed = tuple(index for index in range(N) if index not in free)
        for fixed_signs in itertools.product((-1, 1), repeat=2):
            active = np.all(
                cube[:, fixed] == np.array(fixed_signs)[None, :], axis=1
            )
            dependency = np.zeros(VERTICES, dtype=np.int64)
            dependency[active] = np.prod(cube[active][:, free], axis=1)
            support = np.flatnonzero(active)
            assert len(support) == 8
            assert np.all(features.T @ dependency == 0)
            assert modular_rank(features[support]) == 7
            count += 1
    assert count == 40


def main() -> None:
    features, parity = verify_gale_self_duality()
    verify_archived_circuits(features, parity)
    verify_coordinate_face_circuits(features)
    print("quadratic Fourier rank: 16")
    print("parity-reoriented Gale dual rank: 16")
    print("archived circuit support sizes: 8, 12")
    print("coordinate-face minimum circuits: 40")
    print("verified five-bit degree-three circuit reduction data")


if __name__ == "__main__":
    main()
