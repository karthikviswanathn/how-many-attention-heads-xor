#!/usr/bin/env python3
"""Classify all support-17 circuit families by affine extendibility.

The input contains one ternary signed-circuit code for each orbit under the
input symmetries that preserve head complexity.  A circuit family contains a
threshold-degree-at-least-four extension exactly when its forced parity twist
on the circuit support has a nonzero weak affine separator.

Every nonzero weak affine cone has an extreme ray vanishing on five
independent cube vertices.  The exact list of 3254 primitive affine normals is
therefore a complete finite test.  All comparisons below use integer and
32-bit mask arithmetic.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import verify_n5_degree4_reduction as affine_reduction


N = 5
VERTICES = 1 << N
FULL_MASK = (1 << VERTICES) - 1
HERE = Path(__file__).resolve().parent
DEFAULT_CODES = HERE / "n5_support17_head_orbit_codes.tsv"
DEFAULT_OUTPUT = HERE / "n5_support17_affine_dichotomy.npz"
DEFAULT_EXACT_CODES = HERE / "n5_support17_exact_degree3_only_codes.tsv"


def decode_ternary_code(code: int) -> np.ndarray:
    signs = np.empty(VERTICES, dtype=np.int8)
    current = int(code)
    for vertex in range(VERTICES):
        signs[vertex] = current % 3 - 1
        current //= 3
    assert current == 0
    assert np.count_nonzero(signs) == 17
    return signs


def sign_mask(values: np.ndarray, positive: bool) -> int:
    selected = values > 0 if positive else values < 0
    return sum(1 << int(vertex) for vertex in np.flatnonzero(selected))


def sorted_affine_normals() -> np.ndarray:
    features = affine_reduction.affine_features()
    normals = sorted(affine_reduction.enumerate_rank_five_normals(features))
    assert len(normals) == affine_reduction.EXPECTED_NORMAL_COUNT
    return np.array(normals, dtype=np.int64)


def affine_covector_masks(
    normals: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    features = affine_reduction.affine_features().astype(np.int64)
    positive = np.empty(len(normals), dtype=np.uint32)
    negative = np.empty(len(normals), dtype=np.uint32)
    for index, normal in enumerate(normals):
        values = features @ normal
        positive[index] = sign_mask(values, True)
        negative[index] = sign_mask(values, False)
    return positive, negative


def load_codes(path: Path) -> np.ndarray:
    lines = path.read_text().splitlines()
    assert lines[0] == "ternary_circuit_code"
    codes = np.array([int(line) for line in lines[1:]], dtype=np.uint64)
    assert len(codes) == 46_975
    assert np.all(codes[1:] > codes[:-1])
    return codes


def classify(
    codes: np.ndarray,
    normals: np.ndarray,
    positive_covectors: np.ndarray,
    negative_covectors: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    normal_indices = np.full(len(codes), -1, dtype=np.int16)
    orientations = np.zeros(len(codes), dtype=np.int8)
    parity = np.array(
        [1 if vertex.bit_count() % 2 == 0 else -1 for vertex in range(32)],
        dtype=np.int8,
    )
    for code_index, code in enumerate(codes):
        signs = decode_ternary_code(int(code))
        twisted = signs * parity
        twisted_positive = np.uint32(sign_mask(twisted, True))
        twisted_negative = np.uint32(sign_mask(twisted, False))

        forward_bad = (
            (positive_covectors & twisted_negative)
            | (negative_covectors & twisted_positive)
        )
        forward = np.flatnonzero(forward_bad == 0)
        if len(forward):
            normal_indices[code_index] = int(forward[0])
            orientations[code_index] = 1
            continue

        reverse_bad = (
            (positive_covectors & twisted_positive)
            | (negative_covectors & twisted_negative)
        )
        reverse = np.flatnonzero(reverse_bad == 0)
        if len(reverse):
            normal_indices[code_index] = int(reverse[0])
            orientations[code_index] = -1

    return normal_indices, orientations


def verify_classification(
    codes: np.ndarray,
    normals: np.ndarray,
    normal_indices: np.ndarray,
    orientations: np.ndarray,
) -> None:
    features = affine_reduction.affine_features().astype(np.int64)
    parity = np.array(
        [1 if vertex.bit_count() % 2 == 0 else -1 for vertex in range(32)],
        dtype=np.int8,
    )
    for index in np.flatnonzero(normal_indices >= 0):
        signs = decode_ternary_code(int(codes[index]))
        support = np.flatnonzero(signs)
        twisted = signs[support] * parity[support]
        values = features[support] @ normals[int(normal_indices[index])]
        products = int(orientations[index]) * twisted * values
        assert np.all(products >= 0)
        assert np.any(products > 0)
    assert np.all(orientations[normal_indices < 0] == 0)
    assert np.all(orientations[normal_indices >= 0] != 0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codes", type=Path, default=DEFAULT_CODES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--exact-codes", type=Path, default=DEFAULT_EXACT_CODES
    )
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    codes = load_codes(arguments.codes)
    normals = sorted_affine_normals()
    if arguments.verify_only:
        payload = np.load(arguments.output)
        stored_codes = payload["codes"]
        stored_normals = payload["affine_normals"]
        normal_indices = payload["affine_normal_indices"]
        orientations = payload["affine_orientations"]
        assert np.array_equal(stored_codes, codes)
        assert np.array_equal(stored_normals, normals)
    else:
        positive, negative = affine_covector_masks(normals)
        normal_indices, orientations = classify(
            codes, normals, positive, negative
        )
        np.savez_compressed(
            arguments.output,
            codes=codes,
            affine_normals=normals,
            affine_normal_indices=normal_indices,
            affine_orientations=orientations,
        )
        exact_codes = codes[normal_indices < 0]
        arguments.exact_codes.write_text(
            "ternary_circuit_code\n"
            + "\n".join(str(int(code)) for code in exact_codes)
            + "\n"
        )

    verify_classification(
        codes, normals, normal_indices, orientations
    )
    extendible = int(np.count_nonzero(normal_indices >= 0))
    exact_degree_three_only = len(codes) - extendible
    print(f"support-17 head-symmetry orbits: {len(codes)}")
    print(f"affine-extendible circuit families: {extendible}")
    print(f"exact-degree-three-only circuit families: {exact_degree_three_only}")
    print("verified exact affine-extension dichotomy")
    if not arguments.verify_only:
        print(f"wrote {arguments.output}")
        print(f"wrote {arguments.exact_codes}")


if __name__ == "__main__":
    main()
