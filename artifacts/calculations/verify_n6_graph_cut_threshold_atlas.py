#!/usr/bin/env python3
"""Replay the exact H2 certificates in the six-vertex graph-cut atlas.

This verifier uses only the Python standard library. It checks that every
stored representative is the stated graph-cut threshold, that canonical masks
are correct under coordinate permutations and output complement, and that all
256 essential canonical masks have exact two-head certificates. The one mask
excluded from the search archive is checked using its separate P4 disjoint K2
certificate.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "n6_graph_cut_threshold_screen.json"
FULL_MASK = (1 << 64) - 1

P4_K2_EDGES = ((0, 1), (0, 2), (1, 3), (4, 5))
P4_K2_RAW_MASK = 0x724E7FFE7FFE724E
P4_K2_DENOMINATORS = (
    (20, -3, -4, -3, -5, -2, -2),
    (34, -5, -7, -4, -6, -3, -8),
)
P4_K2_CLEARED_COEFFICIENTS = (
    -15,
    272,
    -205,
    -315,
    -21,
    203,
    90,
    764,
    32,
    295,
    473,
    -46,
    -499,
    -193,
    -1139,
)


def bits(vertex: int) -> tuple[int, ...]:
    return tuple((vertex >> coordinate) & 1 for coordinate in range(6))


VERTICES = tuple(bits(vertex) for vertex in range(64))


def affine_value(coefficients: tuple[int, ...], point: tuple[int, ...]) -> int:
    assert len(coefficients) == 7
    return coefficients[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(coefficients[1:], point)
    )


def graph_cut_mask(edges: tuple[tuple[int, int], ...], threshold: int) -> int:
    mask = 0
    for vertex, point in enumerate(VERTICES):
        cut = sum(point[first] ^ point[second] for first, second in edges)
        if cut >= threshold:
            mask |= 1 << vertex
    return mask


def all_variables_essential(mask: int) -> bool:
    return all(
        any(
            ((mask >> vertex) & 1)
            != ((mask >> (vertex ^ (1 << coordinate))) & 1)
            for vertex in range(64)
        )
        for coordinate in range(6)
    )


def transform_mask(mask: int, permutation: tuple[int, ...]) -> int:
    transformed = 0
    for vertex in range(64):
        if not ((mask >> vertex) & 1):
            continue
        image = 0
        for source, target in enumerate(permutation):
            image |= ((vertex >> source) & 1) << target
        transformed |= 1 << image
    return transformed


def canonical_mask(mask: int) -> int:
    best = min(mask, FULL_MASK ^ mask)
    for permutation in itertools.permutations(range(6)):
        transformed = transform_mask(mask, permutation)
        best = min(best, transformed, FULL_MASK ^ transformed)
    return best


def target_sign(mask: int, vertex: int) -> int:
    return 1 if (mask >> vertex) & 1 else -1


def verify_denominators(denominators: tuple[tuple[int, ...], ...]) -> None:
    assert len(denominators) == 2
    for denominator in denominators:
        slopes = denominator[1:]
        assert all(value > 0 for value in slopes) or all(
            value < 0 for value in slopes
        )
        assert all(affine_value(denominator, point) > 0 for point in VERTICES)


def verify_fixed_certificate(mask: int, certificate: dict[str, object]) -> None:
    denominators = tuple(
        tuple(int(value) for value in denominator)
        for denominator in certificate["denominators"]
    )
    verify_denominators(denominators)
    coefficients = tuple(
        int(value) for value in certificate["cleared_score_coefficients"]
    )
    assert len(coefficients) == 15
    constant = coefficients[0]
    numerator_1 = coefficients[1:8]
    numerator_2 = coefficients[8:15]
    signed_scores = []
    for vertex, point in enumerate(VERTICES):
        denominator_1 = affine_value(denominators[0], point)
        denominator_2 = affine_value(denominators[1], point)
        score = (
            constant * denominator_1 * denominator_2
            + affine_value(numerator_1, point) * denominator_2
            + affine_value(numerator_2, point) * denominator_1
        )
        signed_scores.append(target_sign(mask, vertex) * score)
    assert all(score > 0 for score in signed_scores)
    assert min(signed_scores) == certificate["minimum_signed_cleared_score"]


def vector_add(
    first: tuple[int, ...], second: tuple[int, ...], scale: int = 1
) -> tuple[int, ...]:
    return tuple(a + scale * b for a, b in zip(first, second))


def verify_learned_certificate(mask: int, certificate: dict[str, object]) -> None:
    denominators = tuple(
        tuple(int(value) for value in denominator)
        for denominator in certificate["denominators"]
    )
    numerators = tuple(
        tuple(int(value) for value in numerator)
        for numerator in certificate["numerators"]
    )
    verify_denominators(denominators)
    assert len(numerators) == 2

    factor_form = certificate["one_factor_form"]
    oriented = tuple(int(value) for value in factor_form["oriented_factor"])
    free = tuple(int(value) for value in factor_form["free_factor"])
    absorbed = tuple(
        tuple(int(value) for value in numerator)
        for numerator in factor_form["absorbed_numerators"]
    )
    shift = int(certificate["admissible_shift"])
    assert denominators[0] == oriented
    assert denominators[1] == vector_add(free, oriented, shift)
    assert numerators[0] == absorbed[0]
    assert numerators[1] == vector_add(absorbed[1], absorbed[0], -shift)

    value_ranges = [[], []]
    signed_scores = []
    for vertex, point in enumerate(VERTICES):
        denominator_1 = affine_value(denominators[0], point)
        denominator_2 = affine_value(denominators[1], point)
        value_ranges[0].append(denominator_1)
        value_ranges[1].append(denominator_2)
        score = (
            affine_value(numerators[0], point) * denominator_2
            + affine_value(numerators[1], point) * denominator_1
        )
        signed_scores.append(target_sign(mask, vertex) * score)
    assert all(score > 0 for score in signed_scores)
    assert min(signed_scores) == certificate["minimum_signed_cleared_score"]
    assert [[min(values), max(values)] for values in value_ranges] == certificate[
        "denominator_value_ranges"
    ]


def verify_p4_k2() -> int:
    assert graph_cut_mask(P4_K2_EDGES, 2) == P4_K2_RAW_MASK
    verify_fixed_certificate(
        P4_K2_RAW_MASK,
        {
            "denominators": P4_K2_DENOMINATORS,
            "cleared_score_coefficients": P4_K2_CLEARED_COEFFICIENTS,
            "minimum_signed_cleared_score": 1,
        },
    )
    return canonical_mask(P4_K2_RAW_MASK)


def main() -> None:
    payload = json.loads(ARCHIVE.read_text())
    assert payload["unlabeled_graphs"] == 156
    assert payload["essential_canonical_truth_tables"] == 256
    assert payload["survivor_masks_ranked"] == []
    assert len(payload["records"]) == 255

    canonical_masks = set()
    representative_count = 0
    fixed_count = 0
    learned_count = 0
    maximum_restart = -1
    for record in payload["records"]:
        mask = int(record["truth_mask_hex"], 16)
        assert all_variables_essential(mask)
        assert mask == canonical_mask(mask)
        assert mask not in canonical_masks
        canonical_masks.add(mask)

        for representative in record["representatives"]:
            representative_count += 1
            edges = tuple(tuple(edge) for edge in representative["edges"])
            raw_mask = graph_cut_mask(edges, int(representative["threshold"]))
            assert raw_mask == int(representative["raw_truth_mask_hex"], 16)
            assert canonical_mask(raw_mask) == mask

        certificate = record["h2_search"]
        assert certificate["found"] is True
        if certificate.get("method") == "fixed-dictionary":
            fixed_count += 1
            verify_fixed_certificate(mask, certificate)
        else:
            learned_count += 1
            maximum_restart = max(maximum_restart, int(certificate["restart"]))
            verify_learned_certificate(mask, certificate)

    excluded = {int(value, 16) for value in payload["excluded_archived_masks"]}
    p4_k2_canonical = verify_p4_k2()
    assert excluded == {p4_k2_canonical}
    canonical_masks.add(p4_k2_canonical)
    assert len(canonical_masks) == 256

    print(f"canonical essential masks: {len(canonical_masks)}")
    print(f"stored graph-threshold representatives: {representative_count}")
    print(f"fixed-dictionary certificates: {fixed_count}")
    print(f"learned certificates: {learned_count}")
    print(f"maximum successful learned restart: {maximum_restart}")
    print("verified exact H2 certificates for the complete atlas")


if __name__ == "__main__":
    main()
