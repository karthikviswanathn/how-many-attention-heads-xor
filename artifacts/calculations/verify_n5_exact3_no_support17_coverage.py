#!/usr/bin/env python3
"""Verify an exact-degree-three table with no exact-only support-17 circuit.

The truth table is specified by its 32-bit positive mask.  An integer cubic
separator proves degree at most three.  A positive 12-point dual annihilating
all quadratic monomials proves degree at least three.

For the coverage check, expand all 23116 exact-only support-17 head-symmetry
representatives through 120 coordinate permutations and simultaneous input
complementation.  Both output orientations are checked.  The resulting exact
packed-circuit set has no member conformal to the truth table.
"""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path

import numpy as np


N = 5
VERTICES = 1 << N
POSITIVE_MASK = 625_160_162
HERE = Path(__file__).resolve().parent
CODES = HERE / "n5_support17_exact_degree3_only_codes.tsv"

# Monomial order is degree first, then lexicographic combinations of the five
# coordinates, exactly as returned by monomial_subsets(3).
CUBIC_COEFFICIENTS = np.array(
    [
        -14,
        30,
        -15,
        0,
        27,
        27,
        -15,
        42,
        23,
        -30,
        42,
        37,
        -12,
        -42,
        -42,
        -18,
        -58,
        -60,
        -60,
        48,
        -27,
        -60,
        -60,
        27,
        -19,
        48,
    ],
    dtype=np.int64,
)

DUAL_SUPPORT = np.array(
    [2, 6, 7, 10, 11, 15, 16, 17, 21, 25, 28, 29],
    dtype=np.int64,
)
DUAL_WEIGHTS = np.array(
    [2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 3],
    dtype=np.int64,
)

EXPECTED_REPRESENTATIVES = 23_116
EXPECTED_AUTOMORPHISMS = 240
EXPECTED_TRANSFORMED_INCIDENCES = 5_547_840
EXPECTED_UNIQUE_PACKED_CIRCUITS = 5_286_336
EXPECTED_PACKED_SHA256 = (
    "6ecc8f5fbafe4768f7f8ec726af5d54a"
    "4468b9206f409f9cdec5e336389d187f"
)


def popcount(mask: int) -> int:
    return bin(mask).count("1")


def monomial_subsets(maximum_degree: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for degree in range(maximum_degree + 1)
        for subset in itertools.combinations(range(N), degree)
    )


def monomial_matrix(maximum_degree: int) -> np.ndarray:
    inputs = (
        (np.arange(VERTICES)[:, None] >> np.arange(N)) & 1
    ).astype(np.int64)
    columns = []
    for subset in monomial_subsets(maximum_degree):
        if subset:
            columns.append(np.prod(inputs[:, subset], axis=1))
        else:
            columns.append(np.ones(VERTICES, dtype=np.int64))
    return np.column_stack(columns)


def truth_signs() -> np.ndarray:
    return np.array(
        [
            1 if (POSITIVE_MASK >> vertex) & 1 else -1
            for vertex in range(VERTICES)
        ],
        dtype=np.int64,
    )


def verify_degree() -> None:
    signs = truth_signs()
    cubic = monomial_matrix(3)
    assert cubic.shape == (VERTICES, 26)
    scores = cubic @ CUBIC_COEFFICIENTS
    signed_scores = signs * scores
    assert int(np.min(signed_scores)) == 12

    quadratic = monomial_matrix(2)
    assert quadratic.shape == (VERTICES, 16)
    signed_dual = (
        DUAL_WEIGHTS[:, None]
        * signs[DUAL_SUPPORT, None]
        * quadratic[DUAL_SUPPORT]
    )
    assert np.all(np.sum(signed_dual, axis=0) == 0)
    assert np.all(DUAL_WEIGHTS > 0)
    assert popcount(POSITIVE_MASK) == 15


def load_signs() -> np.ndarray:
    lines = CODES.read_text().splitlines()
    assert lines[0] == "ternary_circuit_code"
    codes = [int(line) for line in lines[1:]]
    assert len(codes) == EXPECTED_REPRESENTATIVES
    signs = np.empty((len(codes), VERTICES), dtype=np.int8)
    for row, code in enumerate(codes):
        current = code
        for vertex in range(VERTICES):
            signs[row, vertex] = current % 3 - 1
            current //= 3
        assert current == 0
    assert np.all(np.count_nonzero(signs, axis=1) == 17)
    return signs


def head_automorphisms() -> list[np.ndarray]:
    vertices = np.arange(VERTICES, dtype=np.int64)
    answer = []
    for permutation in itertools.permutations(range(N)):
        permuted = np.zeros(VERTICES, dtype=np.int64)
        for target, source in enumerate(permutation):
            permuted |= ((vertices >> source) & 1) << target
        answer.append(permuted)
        answer.append(permuted ^ (VERTICES - 1))
    assert len(answer) == EXPECTED_AUTOMORPHISMS
    return answer


def packed_transformed_circuits(signs: np.ndarray) -> np.ndarray:
    bit_weights = np.uint64(1) << np.arange(VERTICES, dtype=np.uint64)
    chunks = []
    for automorphism in head_automorphisms():
        transformed = signs[:, automorphism]
        positive = np.sum(
            (transformed > 0) * bit_weights,
            axis=1,
            dtype=np.uint64,
        )
        negative = np.sum(
            (transformed < 0) * bit_weights,
            axis=1,
            dtype=np.uint64,
        )
        chunks.append(positive | (negative << np.uint64(32)))
    assert len(chunks) * len(signs) == EXPECTED_TRANSFORMED_INCIDENCES
    packed = np.unique(np.concatenate(chunks)).astype("<u8", copy=False)
    assert len(packed) == EXPECTED_UNIQUE_PACKED_CIRCUITS
    digest = hashlib.sha256(packed.tobytes()).hexdigest()
    assert digest == EXPECTED_PACKED_SHA256
    return packed


def verify_no_coverage(packed: np.ndarray) -> None:
    low_mask = np.uint64((1 << VERTICES) - 1)
    positive = packed & low_mask
    negative = packed >> np.uint64(32)
    support = positive | negative
    table = np.uint64(POSITIVE_MASK)

    # The stored orientation is conformal precisely when the table is positive
    # on every positive circuit entry and negative on every negative entry.
    # Comparing with negative also checks the output-complement orientation.
    compatible = ((table & support) == positive) | (
        (table & support) == negative
    )
    assert int(np.count_nonzero(compatible)) == 0


def main() -> None:
    verify_degree()
    packed = packed_transformed_circuits(load_signs())
    verify_no_coverage(packed)
    print("verified exact-degree-three circuit-coverage counterexample")
    print(f"positive mask={POSITIVE_MASK}")
    print("threshold degree=3, exact cubic margin=12")
    print(
        f"transformed incidences={EXPECTED_TRANSFORMED_INCIDENCES} "
        f"unique packed circuits={EXPECTED_UNIQUE_PACKED_CIRCUITS}"
    )
    print(f"packed SHA256={EXPECTED_PACKED_SHA256}")
    print("compatible exact-only support-17 circuits=0")


if __name__ == "__main__":
    main()
