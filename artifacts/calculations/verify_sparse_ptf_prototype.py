#!/usr/bin/env python3
"""Focused smoke checks for the certified sparse PTF prototype."""

from __future__ import annotations

from copy import deepcopy
import json
import time

import numpy as np

from hstar.boolean_cube import cube, signs_from_mask
from hstar.sparse_ptf import (
    MONOTONE_BASIS,
    WALSH_BASIS,
    SparsePTFColumnGenerationConfig,
    SparsePTFSearchConfig,
    _feature_matrix,
    _fwht_float,
    _initial_coefficients,
    _superset_zeta_float,
    column_generation_sparse_ptf_upper_bound,
    fourier_tail_upper_bound,
    optimal_fourier_tail_upper_bound,
    sparse_ptf_portfolio,
    sparse_ptf_upper_bound,
    verify_sparse_ptf_certificate,
)


def parity_signs(dimension: int) -> np.ndarray:
    points = cube(dimension)
    return np.where(np.sum(points, axis=1) % 2 == 1, 1, -1).astype(np.int64)


def equality_signs(block_size: int) -> np.ndarray:
    dimension = 2 * block_size
    points = cube(dimension)
    equal = np.all(
        points[:, :block_size] == points[:, block_size:],
        axis=1,
    )
    return np.where(equal, 1, -1).astype(np.int64)


def checked_summary(
    name: str,
    signs: np.ndarray,
    dimension: int,
    certificate: dict,
    diagnostics: dict,
) -> dict:
    report = verify_sparse_ptf_certificate(certificate, signs, dimension)
    assert report["valid"], report
    return {
        "name": name,
        "dimension": dimension,
        "basis": certificate["basis"],
        "head_count": certificate["head_count"],
        "support_size": report["support_size"],
        "maximum_degree": report["maximum_degree"],
        "minimum_signed_value": report["minimum_signed_value"],
        "search_status": diagnostics["status"],
        "lp_solves": diagnostics.get("lp_solves", 0),
    }


def verify_all_three_bit_full_basis() -> None:
    config = SparsePTFSearchConfig(
        max_prune_solves=0,
        max_matrix_entries=1,
    )
    for mask in range(1 << (1 << 3)):
        signs = signs_from_mask(mask, 3)
        for basis in (MONOTONE_BASIS, WALSH_BASIS):
            certificate, diagnostics = sparse_ptf_upper_bound(
                signs,
                3,
                basis=basis,
                config=config,
            )
            assert diagnostics["status"] == "pruning-disabled"
            report = verify_sparse_ptf_certificate(certificate, signs, 3)
            assert report["valid"], (mask, basis, report)


def verify_all_three_bit_fourier_tails() -> None:
    for mask in range(1 << (1 << 3)):
        signs = signs_from_mask(mask, 3)
        certificate, diagnostics = fourier_tail_upper_bound(signs, 3)
        report = verify_sparse_ptf_certificate(certificate, signs, 3)
        assert report["valid"], (mask, report)
        assert diagnostics["unnormalized_omitted_mass"] < 1 << 3


def brute_force_fourier_tail_cost(signs: np.ndarray, dimension: int) -> int:
    coefficients = _initial_coefficients(signs, dimension, WALSH_BASIS)
    singleton_mass = sum(
        abs(coefficient)
        for mask, coefficient in coefficients.items()
        if mask.bit_count() == 1
    )
    items = []
    if singleton_mass:
        items.append((1, singleton_mass))
    items.extend(
        (mask.bit_count(), abs(coefficient))
        for mask, coefficient in coefficients.items()
        if mask.bit_count() >= 2
    )
    item_mass = sum(value for _, value in items)
    best = sum(cost for cost, _ in items)
    for selection in range(1 << len(items)):
        cost = 0
        retained_mass = 0
        for index, (item_cost, item_value) in enumerate(items):
            if selection & (1 << index):
                cost += item_cost
                retained_mass += item_value
        if item_mass - retained_mass < 1 << dimension:
            best = min(best, cost)
    return best


def verify_all_three_bit_optimal_fourier_tails() -> None:
    for mask in range(1 << (1 << 3)):
        signs = signs_from_mask(mask, 3)
        certificate, diagnostics = optimal_fourier_tail_upper_bound(signs, 3)
        report = verify_sparse_ptf_certificate(certificate, signs, 3)
        assert report["valid"], (mask, report)
        assert diagnostics["optimal_within_absolute_tail_criterion"]
        assert report["head_count"] == brute_force_fourier_tail_cost(signs, 3)
        greedy, _ = fourier_tail_upper_bound(signs, 3)
        assert report["head_count"] <= int(greedy["head_count"])


def verify_optimal_tail_improvement() -> dict:
    signs = signs_from_mask(0xCC4B244F3C92D063, 6)
    greedy, _ = fourier_tail_upper_bound(signs, 6)
    optimal, diagnostics = optimal_fourier_tail_upper_bound(signs, 6)
    assert verify_sparse_ptf_certificate(optimal, signs, 6)["valid"]
    assert int(greedy["head_count"]) == 119
    assert int(optimal["head_count"]) == 117
    return {
        "dimension": 6,
        "truth_mask_hex": "0xcc4b244f3c92d063",
        "greedy_head_count": int(greedy["head_count"]),
        "optimal_tail_head_count": int(optimal["head_count"]),
        "actual_dp_transitions": diagnostics["actual_dp_transitions"],
    }


def verify_edge_cases_and_budget() -> None:
    points = cube(3)
    config = SparsePTFSearchConfig(
        max_prune_solves=8,
        max_matrix_entries=1_000,
        seed=17,
    )
    cases = (
        (np.ones(8, dtype=np.int64), 0),
        (-np.ones(8, dtype=np.int64), 0),
        (np.where(np.sum(points, axis=1) == 3, 1, -1), 1),
        (np.where(np.sum(points, axis=1) >= 2, 1, -1), 1),
    )
    for signs, expected in cases:
        for basis in (MONOTONE_BASIS, WALSH_BASIS):
            certificate, _ = sparse_ptf_upper_bound(
                signs,
                3,
                basis=basis,
                config=config,
            )
            report = verify_sparse_ptf_certificate(certificate, signs, 3)
            assert report["valid"], report
            assert report["head_count"] == expected

    signs = signs_from_mask(0x6996, 4)
    skipped, diagnostics = sparse_ptf_upper_bound(
        signs,
        4,
        basis=MONOTONE_BASIS,
        config=SparsePTFSearchConfig(
            max_prune_solves=16,
            max_matrix_entries=1,
        ),
    )
    assert diagnostics["status"] == "pruning-skipped-matrix-budget"
    assert verify_sparse_ptf_certificate(skipped, signs, 4)["valid"]


def verify_tamper_rejection(
    certificate: dict,
    signs: np.ndarray,
    dimension: int,
) -> None:
    round_trip = json.loads(json.dumps(certificate))
    assert verify_sparse_ptf_certificate(round_trip, signs, dimension)["valid"]

    changes = (
        ("head_count", int(certificate["head_count"]) + 1),
        (
            "minimum_signed_value",
            int(certificate["minimum_signed_value"]) + 1,
        ),
        (
            "maximum_absolute_value",
            int(certificate["maximum_absolute_value"]) + 1,
        ),
        ("truth_mask_hex", "0x0"),
    )
    for key, value in changes:
        tampered = deepcopy(certificate)
        tampered[key] = value
        assert not verify_sparse_ptf_certificate(
            tampered,
            signs,
            dimension,
        )["valid"]


def verify_pricing_transforms() -> None:
    dimension = 5
    vertex_count = 1 << dimension
    masks = list(range(vertex_count))
    residual = np.cos(np.arange(vertex_count, dtype=float) + 0.375)
    monotone_explicit = (
        _feature_matrix(masks, dimension, MONOTONE_BASIS).T @ residual
    )
    walsh_explicit = _feature_matrix(masks, dimension, WALSH_BASIS).T @ residual
    assert np.allclose(
        _superset_zeta_float(residual, dimension),
        monotone_explicit,
        atol=1e-12,
        rtol=1e-12,
    )
    assert np.allclose(
        _fwht_float(residual),
        walsh_explicit,
        atol=1e-12,
        rtol=1e-12,
    )


def verify_transform_priced_column_generation() -> list[dict]:
    summaries = []
    small_config = SparsePTFColumnGenerationConfig(
        max_iterations=16,
        batch_size=8,
        max_columns=64,
    )
    parity = parity_signs(6)
    parity_certificate, parity_diagnostics = (
        column_generation_sparse_ptf_upper_bound(
            parity,
            6,
            basis=WALSH_BASIS,
            config=small_config,
        )
    )
    parity_report = verify_sparse_ptf_certificate(parity_certificate, parity, 6)
    assert parity_report["valid"], parity_report
    assert parity_report["head_count"] == 6
    assert parity_report["support_size"] == 1
    assert parity_diagnostics["full_dictionary_materialized"] is False
    assert parity_diagnostics["columns_added"] > 0
    assert parity_diagnostics["pricing_passes"] >= 2
    assert parity_diagnostics["exactified_candidates"] > 0
    summaries.append(
        {
            "name": "six-bit parity column generation",
            "dimension": 6,
            "basis": WALSH_BASIS,
            "head_count": parity_report["head_count"],
            "support_size": parity_report["support_size"],
            "status": parity_diagnostics["status"],
            "columns_added": parity_diagnostics["columns_added"],
            "pricing_passes": parity_diagnostics["pricing_passes"],
            "certificate_source": parity_diagnostics["certificate_source"],
        }
    )

    # At n = 12 the full feature dictionary has 16,777,216 entries, which is
    # above the deletion prototype's default 4,000,000-entry matrix budget.
    # The restricted master below has at most 80 generated nonlinear columns.
    equality = equality_signs(6)
    large_config = SparsePTFColumnGenerationConfig(
        max_iterations=6,
        batch_size=16,
        max_columns=80,
    )
    start = time.perf_counter()
    equality_certificate, equality_diagnostics = (
        column_generation_sparse_ptf_upper_bound(
            equality,
            12,
            basis=MONOTONE_BASIS,
            config=large_config,
        )
    )
    elapsed_seconds = time.perf_counter() - start
    equality_report = verify_sparse_ptf_certificate(
        equality_certificate,
        equality,
        12,
    )
    assert equality_report["valid"], equality_report
    assert equality_report["head_count"] == 7
    assert equality_diagnostics["initial_head_count"] == 4084
    assert equality_diagnostics["certificate_source"] == "generated-support-refit"
    assert equality_diagnostics["full_dictionary_entries"] == 16_777_216
    assert equality_diagnostics["full_dictionary_entries"] > 4_000_000
    assert equality_diagnostics["full_dictionary_materialized"] is False
    assert (
        equality_diagnostics["max_restricted_matrix_entries"]
        < equality_diagnostics["full_dictionary_entries"]
    )
    assert elapsed_seconds < 30.0
    summaries.append(
        {
            "name": "six-bit-string equality column generation",
            "dimension": 12,
            "basis": MONOTONE_BASIS,
            "initial_head_count": equality_diagnostics["initial_head_count"],
            "head_count": equality_report["head_count"],
            "support_size": equality_report["support_size"],
            "status": equality_diagnostics["status"],
            "columns_added": equality_diagnostics["columns_added"],
            "restricted_master_solves": equality_diagnostics[
                "restricted_master_solves"
            ],
            "max_restricted_matrix_entries": equality_diagnostics[
                "max_restricted_matrix_entries"
            ],
            "full_dictionary_entries": equality_diagnostics[
                "full_dictionary_entries"
            ],
            "elapsed_seconds": elapsed_seconds,
        }
    )
    return summaries


def main() -> None:
    verify_all_three_bit_full_basis()
    verify_all_three_bit_fourier_tails()
    verify_all_three_bit_optimal_fourier_tails()
    optimal_tail_improvement = verify_optimal_tail_improvement()
    verify_edge_cases_and_budget()
    verify_pricing_transforms()
    column_generation_summaries = verify_transform_priced_column_generation()

    config = SparsePTFSearchConfig(
        max_prune_solves=256,
        ordering_restarts=1,
        max_matrix_entries=1_000_000,
        seed=20260717,
    )
    summaries = []

    parity = parity_signs(6)
    parity_certificate, parity_diagnostics = sparse_ptf_upper_bound(
        parity,
        6,
        basis=WALSH_BASIS,
        config=config,
    )
    assert parity_certificate["head_count"] == 6
    assert len(parity_certificate["terms"]) == 1
    summaries.append(
        checked_summary(
            "six-bit parity",
            parity,
            6,
            parity_certificate,
            parity_diagnostics,
        )
    )

    parity_triple = signs_from_mask(0x96696BD669B69669, 6)
    triple_certificate, triple_diagnostics = sparse_ptf_portfolio(
        parity_triple,
        6,
        config=config,
    )
    assert triple_certificate["head_count"] <= 14
    summaries.append(
        checked_summary(
            "six-bit parity triple flip",
            parity_triple,
            6,
            triple_certificate,
            triple_diagnostics,
        )
    )

    equality = equality_signs(3)
    equality_certificate, equality_diagnostics = sparse_ptf_upper_bound(
        equality,
        6,
        basis=MONOTONE_BASIS,
        config=config,
    )
    assert equality_certificate["head_count"] <= 4
    summaries.append(
        checked_summary(
            "three-bit-string equality",
            equality,
            6,
            equality_certificate,
            equality_diagnostics,
        )
    )

    random_signs = signs_from_mask(0xCC4B244F3C92D063, 6)
    random_certificate, random_diagnostics = sparse_ptf_portfolio(
        random_signs,
        6,
        config=config,
    )
    assert random_certificate["head_count"] <= min(
        int(attempt["initial_head_count"])
        for attempt in random_diagnostics["attempts"]
    )
    random_report = verify_sparse_ptf_certificate(
        random_certificate,
        random_signs,
        6,
    )
    assert random_report["valid"], random_report
    summaries.append(
        {
            "name": "fixed pseudorandom six-bit truth table",
            "dimension": 6,
            "truth_mask_hex": "0xcc4b244f3c92d063",
            "basis": random_certificate["basis"],
            "head_count": random_certificate["head_count"],
            "support_size": random_report["support_size"],
            "maximum_degree": random_report["maximum_degree"],
            "minimum_signed_value": random_report["minimum_signed_value"],
            "search_status": random_diagnostics["status"],
            "basis_attempts": random_diagnostics["attempts"],
        }
    )

    verify_tamper_rejection(parity_certificate, parity, 6)

    print(
        json.dumps(
            {
                "status": "verified",
                "exhaustive_three_bit_certificates": 512,
                "exhaustive_three_bit_fourier_tail_certificates": 256,
                "exhaustive_three_bit_optimal_tail_comparisons": 256,
                "optimal_tail_improvement": optimal_tail_improvement,
                "cases": summaries,
                "column_generation_cases": column_generation_summaries,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
