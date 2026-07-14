#!/usr/bin/env python3
"""Verify exact H4 certificates for both five-bit cofactor types and all orientations."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import search_gated_single_flip as exact
import search_n5_parity_exception_orientation_counts as search


HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "n5_parity_exception_orientation_counts.json"


def verify() -> None:
    payload = json.loads(ARCHIVE.read_text())
    assert payload["dimension"] == search.N
    assert payload["heads"] == search.HEADS
    expected_masks = {
        "one_flip": "0x69969661",
        "two_flips": "0x69968661",
    }
    affine = exact.affine_matrix(search.N, object)

    for name, exceptions in search.TARGETS.items():
        record = payload["targets"][name]
        signs = search.target_signs(exceptions).astype(object)
        assert record["exceptions"] == list(exceptions)
        assert record["truth_mask_hex"] == expected_masks[name]
        assert search.truth_mask(signs) == int(expected_masks[name], 16)
        attempts = record["attempts"]
        assert [item["positive_heads"] for item in attempts] == list(range(5))
        for item in attempts:
            positive_heads = item["positive_heads"]
            certificate = item["certificate"]
            assert certificate is not None
            denominators = np.array(certificate["denominators"], dtype=object)
            assert denominators.shape == (search.HEADS, search.N + 1)
            assert np.all(affine @ denominators.T > 0)
            orientations = []
            for row in denominators:
                if all(value > 0 for value in row[1:]):
                    orientations.append(1)
                elif all(value < 0 for value in row[1:]):
                    orientations.append(0)
                else:
                    raise AssertionError("mixed denominator orientation")
            assert sum(orientations) == positive_heads

            coefficients = np.array(
                certificate["score_coefficients"], dtype=object
            )
            matrix = exact.cleared_matrix(search.N, denominators)
            assert coefficients.shape == (matrix.shape[1],)
            signed = signs * (matrix @ coefficients)
            minimum = int(min(signed))
            assert minimum > 0
            assert minimum == certificate["minimum_signed_cleared_score"]


def main() -> None:
    verify()
    print("one-flip mask: 0x69969661")
    print("two-flip mask: 0x69968661")
    print("one-flip exact H4 orientation counts: 0, 1, 2, 3, 4")
    print("two-flip exact H4 orientation counts: 0, 1, 2, 3, 4")


if __name__ == "__main__":
    main()
