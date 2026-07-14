#!/usr/bin/env python3
"""Exactly sweep simple rank-16 rays for one 13-vertex residual pocket.

This is deliberately separate from the active five-bit cubic checkpoint.  It
enumerates all 15-row zero sets containing the fixed 13-vertex pocket face in
each of the 480 asymmetric near-literal denominator spaces.  Only exact
integer null vectors and exact sign tests can enter the result archive.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
import math
from pathlib import Path

import numpy as np
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

import search_n5_cubic_dictionary_milp as search


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n5_cubic_pocket13_cocircuit_sweep.json"
POCKET_MASKS = (
    0x95563FFC,
    0xFDD6BEE8,
    0xEDD63EEC,
    0xE156BEEE,
    0xE9D73FE8,
    0xE957BEE8,
    0x69D63EFE,
    0x6956BFFC,
)
SOURCE_MASK = POCKET_MASKS[-1]
EXPECTED_VARYING_MASK = 0xFC818116


def pocket_varying_mask() -> int:
    varying = 0
    for mask in POCKET_MASKS[1:]:
        varying |= mask ^ POCKET_MASKS[0]
    assert varying == EXPECTED_VARYING_MASK
    assert varying.bit_count() == 13
    return varying


def denominator_spaces() -> list[np.ndarray]:
    spaces = []
    seen = set()
    for representative in search.asymmetric_near_literal_representatives(10):
        for denominators in search.denominator_orbit(representative):
            key = search.canonical_triple(denominators)
            if key in seen:
                continue
            seen.add(key)
            spaces.append(np.array(key, dtype=np.int64))
    assert len(spaces) == 480
    assert all(search.valid_denominators(item) for item in spaces)
    return spaces


def exact_null_vector(matrix: np.ndarray) -> tuple[int, ...] | None:
    rows = [[int(value) for value in row] for row in matrix.tolist()]
    domain = DomainMatrix.from_list_sympy(len(rows), len(rows[0]), rows).convert_to(ZZ)
    nullspace = domain.nullspace()
    vectors = nullspace.to_list()
    if len(vectors) != 1:
        return None
    vector = [int(value) for value in vectors[0]]
    common = 0
    for value in vector:
        common = math.gcd(common, abs(value))
    assert common
    vector = [value // common for value in vector]
    first = next(value for value in vector if value)
    if first < 0:
        vector = [-value for value in vector]
    return tuple(vector)


def orient_for_source(
    basis: np.ndarray, coefficients: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    values = tuple(
        int(value)
        for value in basis @ np.array(coefficients, dtype=object)
    )
    signs = tuple(int(value) for value in search.signs_from_mask(SOURCE_MASK))
    signed = tuple(sign * value for sign, value in zip(signs, values))
    if all(value >= 0 for value in signed) and any(value > 0 for value in signed):
        return coefficients, values
    if all(value <= 0 for value in signed) and any(value < 0 for value in signed):
        return tuple(-value for value in coefficients), tuple(-value for value in values)
    return None


def family_from_ray(
    denominators: np.ndarray,
    basis_columns: tuple[int, ...],
    coefficients: tuple[int, ...],
    values: tuple[int, ...],
    zero_vertices: tuple[int, ...],
) -> dict[str, object]:
    positive = sum((value > 0) << vertex for vertex, value in enumerate(values))
    negative = sum((value < 0) << vertex for vertex, value in enumerate(values))
    family: dict[str, object] = {
        "source_mask_hex": f"0x{SOURCE_MASK:08x}",
        "denominators": [
            list(row) for row in search.canonical_triple(denominators)
        ],
        "score_basis_columns": list(basis_columns),
        "ray_coefficients": list(coefficients),
        "zero_vertices": list(zero_vertices),
        "fixed_positive_mask_hex": f"0x{positive:08x}",
        "fixed_negative_mask_hex": f"0x{negative:08x}",
        "score_space_rank": 16,
        "zero_restriction_rank": 15,
        "symmetry_orbit": "S5 x global input complement x output complement",
        "targeted_face": {
            "pocket_masks_hex": [f"0x{mask:08x}" for mask in POCKET_MASKS],
            "forced_zero_vertices": [
                vertex
                for vertex in range(search.VERTICES)
                if (EXPECTED_VARYING_MASK >> vertex) & 1
            ],
        },
    }
    search.verify_family(family)
    for mask in POCKET_MASKS:
        assert positive & mask == positive
        assert negative & (search.FULL_MASK ^ mask) == negative
    return family


def verify_result(payload: dict[str, object]) -> None:
    assert payload["schema_version"] == 1
    assert payload["pocket_masks_hex"] == [
        f"0x{mask:08x}" for mask in POCKET_MASKS
    ]
    assert int(payload["varying_mask_hex"], 16) == pocket_varying_mask()
    assert payload["denominator_space_count"] == 480
    assert payload["zero_set_completions_per_space"] == 171
    assert payload["candidate_zero_set_count"] == 480 * 171
    assert payload["unique_family_orbit_count"] == len(payload["families"])
    seen = set()
    for record in payload["families"]:
        family = record["family"]
        search.verify_family(family)
        positive = int(family["fixed_positive_mask_hex"], 16)
        negative = int(family["fixed_negative_mask_hex"], 16)
        for mask in POCKET_MASKS:
            assert positive & mask == positive
            assert negative & (search.FULL_MASK ^ mask) == negative
        orbit = tuple(search.family_clauses(family))
        assert orbit not in seen
        seen.add(orbit)


def sweep(output: Path) -> dict[str, object]:
    varying = pocket_varying_mask()
    forced = tuple(
        vertex for vertex in range(search.VERTICES) if (varying >> vertex) & 1
    )
    fixed = tuple(
        vertex for vertex in range(search.VERTICES) if not (varying >> vertex) & 1
    )
    completions = tuple(combinations(fixed, 2))
    assert len(forced) == 13
    assert len(fixed) == 19
    assert len(completions) == 171

    statistics = {
        "forced_rank_deficient_spaces": 0,
        "rank_deficient_zero_sets": 0,
        "nonsimple_zero_sets": 0,
        "sign_compatible_rays": 0,
    }
    families = []
    seen_orbits = set()
    spaces = denominator_spaces()
    for space_index, denominators in enumerate(spaces):
        basis, basis_columns = search.independent_score_basis(denominators)
        assert basis.shape == (search.VERTICES, 16)
        forced_rank = search.modular_rank(basis[list(forced)])
        if forced_rank != 13:
            statistics["forced_rank_deficient_spaces"] += 1
            continue
        for completion in completions:
            zero_vertices = tuple(sorted(forced + completion))
            coefficients = exact_null_vector(basis[list(zero_vertices)])
            if coefficients is None:
                statistics["rank_deficient_zero_sets"] += 1
                continue
            oriented = orient_for_source(basis, coefficients)
            if oriented is None:
                continue
            coefficients, values = oriented
            actual_zeros = tuple(
                vertex for vertex, value in enumerate(values) if value == 0
            )
            if actual_zeros != zero_vertices:
                statistics["nonsimple_zero_sets"] += 1
                continue
            statistics["sign_compatible_rays"] += 1
            family = family_from_ray(
                denominators,
                basis_columns,
                coefficients,
                values,
                zero_vertices,
            )
            orbit = tuple(search.family_clauses(family))
            if orbit in seen_orbits:
                continue
            seen_orbits.add(orbit)
            families.append(
                {
                    "denominator_space_index": space_index,
                    "completion_vertices": list(completion),
                    "family": family,
                }
            )
        if (space_index + 1) % 20 == 0:
            print(
                f"spaces={space_index + 1}/480 "
                f"compatible={statistics['sign_compatible_rays']} "
                f"unique_orbits={len(families)}",
                flush=True,
            )

    payload: dict[str, object] = {
        "schema_version": 1,
        "status": (
            "Exact enumeration of every simple rank-16 cocircuit ray whose "
            "15-row zero set contains the 13-vertex residual pocket face."
        ),
        "pocket_masks_hex": [f"0x{mask:08x}" for mask in POCKET_MASKS],
        "source_mask_hex": f"0x{SOURCE_MASK:08x}",
        "varying_mask_hex": f"0x{varying:08x}",
        "denominator_space_count": len(spaces),
        "zero_set_completions_per_space": len(completions),
        "candidate_zero_set_count": len(spaces) * len(completions),
        **statistics,
        "unique_family_orbit_count": len(families),
        "families": families,
    }
    verify_result(payload)
    output.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.verify_only:
        payload = json.loads(arguments.output.read_text())
        verify_result(payload)
        print(
            f"verified {payload['unique_family_orbit_count']} exact family orbits",
            flush=True,
        )
        return
    payload = sweep(arguments.output)
    print(json.dumps({key: value for key, value in payload.items() if key != "families"}, indent=2))
    print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
