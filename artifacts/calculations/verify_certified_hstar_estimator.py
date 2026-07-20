#!/usr/bin/env python3
"""Smoke-test the certified interval and exact certificate infrastructure."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from hstar.boolean_cube import (
    VERTEX_ORDER,
    cube,
    mask_from_signs,
    signs_from_mask,
    signs_from_vertex_bitstring,
)
from hstar.certified import (
    _eight_bit_hamming_signs,
    decide_head_feasibility,
    estimate_certified_hstar,
    exact_threshold_degree,
    largest_parity_restriction,
    partition_forster_lower_bound,
    projection_sign_change_upper_bound,
    verify_partition_forster_witness,
    verify_projection_witness,
)
from hstar.exact_linear import verify_gordan_obstruction, verify_threshold_polynomial
from hstar.fractional import verify_head_certificate
from hstar.sparse_ptf import verify_sparse_ptf_certificate


HERE = Path(__file__).resolve().parent


def verify_cube_convention() -> None:
    assert VERTEX_ORDER == "integer-code-lsb-coordinate-0"
    assert cube(2).tolist() == [[0, 0], [1, 0], [0, 1], [1, 1]]
    signs = signs_from_mask(0x6, 2)
    assert signs.tolist() == [-1, 1, 1, -1]
    assert mask_from_signs(signs, 2) == 0x6
    assert np.array_equal(signs, signs_from_vertex_bitstring("0110", 2))


def verify_small_intervals() -> None:
    constant = signs_from_mask(0x0, 3)
    result = estimate_certified_hstar(
        constant,
        3,
        use_z3_threshold_degree=False,
        heuristic_restarts=0,
    )
    assert result["certified_interval"] == [0, 0]

    xor2 = signs_from_mask(0x6, 2)
    parity = largest_parity_restriction(xor2, 2)
    assert parity["dimension"] == 2
    result = estimate_certified_hstar(
        xor2,
        2,
        use_z3_threshold_degree=False,
        heuristic_restarts=0,
    )
    assert result["certified_interval"] == [2, 2]

    xor3_mask = sum(
        1 << code for code in range(8) if code.bit_count() % 2 == 1
    )
    xor3 = signs_from_mask(xor3_mask, 3)
    assert largest_parity_restriction(xor3, 3)["dimension"] == 3
    result = estimate_certified_hstar(
        xor3,
        3,
        use_z3_threshold_degree=False,
        heuristic_restarts=0,
    )
    assert result["certified_interval"] == [3, 3]


def verify_one_head_integer_certificate() -> None:
    and2 = signs_from_mask(0x8, 2)
    certificate = {
        "schema_version": 1,
        "dimension": 2,
        "vertex_order": VERTEX_ORDER,
        "head_count": 1,
        "orientations": [1],
        "denominators": [[1, 1, 1]],
        "score_coefficients": [0, -3, 2, 2],
        "minimum_signed_cleared_score": 1,
    }
    report = verify_head_certificate(certificate, and2, 2)
    assert report["valid"]
    assert report["minimum_signed_cleared_score"] == 1
    malformed = dict(certificate)
    malformed["score_coefficients"] = [0, -3, 2, 2.5]
    assert not verify_head_certificate(malformed, and2, 2)["valid"]


def verify_six_bit_layered_projection() -> None:
    signs = signs_from_mask(0x96696BD669B69669, 6)
    certificate = projection_sign_change_upper_bound(
        signs,
        6,
        permutation_limit=720,
    )
    assert certificate["upper_bound"] == 8
    assert certificate["positive_integer_weights"] == [65, 72, 96, 66, 80, 68]
    report = verify_projection_witness(certificate, signs, 6)
    assert report["valid"]
    assert report["transition_positions"] == [1, 7, 23, 37, 39, 42, 57, 63]
    result = estimate_certified_hstar(
        signs,
        6,
        use_z3_threshold_degree=False,
        heuristic_restarts=0,
    )
    assert result["certified_interval"] == [4, 6]
    complement = estimate_certified_hstar(
        -signs,
        6,
        use_z3_threshold_degree=False,
        heuristic_restarts=0,
    )
    assert complement["certified_interval"] == [4, 6]


def verify_partition_spectral_bound() -> None:
    dimension = 6
    signs = []
    for code in range(1 << dimension):
        left = [(code >> coordinate) & 1 for coordinate in range(3)]
        right = [(code >> (coordinate + 3)) & 1 for coordinate in range(3)]
        signs.append(1 if sum(a * b for a, b in zip(left, right)) % 2 == 0 else -1)
    witness = partition_forster_lower_bound(
        signs,
        dimension,
        partition_limit=64,
        max_side=8,
    )
    assert witness["head_lower_bound"] >= 2
    assert witness["sign_rank_lower_bound"] >= 3
    report = verify_partition_forster_witness(witness, signs, dimension)
    assert report["valid"]
    assert report["head_lower_bound"] == witness["head_lower_bound"]


def verify_sparse_ptf_estimator_backend() -> None:
    points = cube(6)
    signs = np.where(
        np.all(points[:, :3] == points[:, 3:], axis=1),
        1,
        -1,
    ).astype(np.int64)
    result = estimate_certified_hstar(
        signs,
        6,
        use_z3_threshold_degree=False,
        use_known_bounds=False,
        projection_permutation_limit=64,
        partition_spectral_limit=0,
        use_sparse_ptf_column_generation=True,
        sparse_ptf_max_iterations=8,
        sparse_ptf_batch_size=16,
        sparse_ptf_max_columns=128,
        sparse_ptf_max_vertices=64,
        heuristic_restarts=0,
        seed=19,
    )
    assert result["certified_interval"][1] == 4
    diagnostics = result["sparse_ptf_column_generation"]
    assert diagnostics["status"] == "verified-certificate-found"
    assert diagnostics["selected_basis"] == "monotone-01"
    entries = [
        entry
        for entry in result["upper_bounds"]
        if entry["method"].startswith("transform-priced sparse PTF")
    ]
    assert len(entries) == 1
    report = verify_sparse_ptf_certificate(entries[0]["certificate"], signs, 6)
    assert report["valid"]
    assert report["head_count"] == 4

    skipped = estimate_certified_hstar(
        signs,
        6,
        use_z3_threshold_degree=False,
        use_known_bounds=False,
        projection_permutation_limit=2,
        partition_spectral_limit=0,
        use_sparse_ptf_column_generation=True,
        sparse_ptf_max_vertices=32,
        heuristic_restarts=0,
    )
    assert skipped["sparse_ptf_column_generation"]["status"] == (
        "skipped-vertex-budget"
    )


def verify_optimal_fourier_tail_estimator_backend() -> None:
    dimension = 6
    signs = signs_from_mask(0xB1E41B4E278D72D8, dimension)
    archived_certificate = json.loads(
        (HERE / "six_bit_optimal_fourier_tail_h8_certificate.json").read_text()
    )
    archived_report = verify_sparse_ptf_certificate(
        archived_certificate,
        signs,
        dimension,
    )
    assert archived_report["valid"]
    assert archived_report["head_count"] == 8
    result = estimate_certified_hstar(
        signs,
        dimension,
        use_z3_threshold_degree=False,
        use_known_bounds=False,
        projection_permutation_limit=720,
        partition_spectral_limit=0,
        use_optimal_fourier_tail=True,
        optimal_fourier_tail_max_vertices=64,
        heuristic_restarts=0,
    )
    assert result["certified_interval"][1] == 8
    diagnostics = result["optimal_fourier_tail"]
    assert diagnostics["status"] == "verified-optimal-fourier-tail-certificate"
    assert diagnostics["head_count"] == 8
    assert diagnostics["improved_upper_bound"]
    report = verify_sparse_ptf_certificate(
        diagnostics["certificate"],
        signs,
        dimension,
    )
    assert report["valid"]
    assert report["head_count"] == 8
    entries = [
        entry
        for entry in result["upper_bounds"]
        if entry["method"].startswith("optimal absolute Fourier-tail knapsack")
    ]
    assert len(entries) == 1
    assert entries[0]["bound"] == 8

    transition_skip = estimate_certified_hstar(
        signs,
        dimension,
        use_z3_threshold_degree=False,
        use_known_bounds=False,
        projection_permutation_limit=2,
        partition_spectral_limit=0,
        use_optimal_fourier_tail=True,
        optimal_fourier_tail_max_transitions=1,
        optimal_fourier_tail_max_vertices=64,
        heuristic_restarts=0,
    )
    transition_diagnostics = transition_skip["optimal_fourier_tail"]
    assert transition_diagnostics["status"] == "skipped-transition-budget"
    assert transition_diagnostics["estimated_dp_transitions"] > 1
    assert not transition_diagnostics["floating_failures_are_lower_bounds"]

    vertex_skip = estimate_certified_hstar(
        signs,
        dimension,
        use_z3_threshold_degree=False,
        use_known_bounds=False,
        projection_permutation_limit=2,
        partition_spectral_limit=0,
        use_optimal_fourier_tail=True,
        optimal_fourier_tail_max_vertices=32,
        heuristic_restarts=0,
    )
    vertex_diagnostics = vertex_skip["optimal_fourier_tail"]
    assert vertex_diagnostics["status"] == "skipped-vertex-budget"
    assert not vertex_diagnostics["floating_failures_are_lower_bounds"]


def verify_optional_exact_backend() -> bool:
    xor2 = signs_from_mask(0x6, 2)
    degree = exact_threshold_degree(xor2, 2, timeout_milliseconds=5_000)
    if degree["status"] == "backend-unavailable":
        return False
    assert degree["status"] == "exact"
    assert degree["exact_degree"] == 2
    assert verify_threshold_polynomial(
        degree["upper_certificate"], xor2, 2
    )["valid"]
    for certificate in degree["lower_certificates"]:
        assert verify_gordan_obstruction(certificate, xor2, 2)["valid"]
    one_head = decide_head_feasibility(
        xor2,
        2,
        1,
        timeout_milliseconds=5_000,
    )
    assert one_head["status"] == "unsat"
    two_heads = decide_head_feasibility(
        xor2,
        2,
        2,
        timeout_milliseconds=5_000,
    )
    assert two_heads["status"] == "sat"
    certificate = two_heads["strict_integer_certificate"]
    assert certificate is not None
    assert verify_head_certificate(certificate, xor2, 2)["valid"]
    return True


def verify_archived_eight_bit_result() -> None:
    signs = _eight_bit_hamming_signs()
    archive = json.loads((HERE / "f8_three_head_upper_search.json").read_text())
    raw = archive["certificate"]
    certificate = {
        "orientations": raw["orientations"],
        "denominators": raw["denominators"],
        "score_coefficients": raw["score_coefficients"],
        "minimum_signed_cleared_score": raw["minimum_signed_cleared_score"],
    }
    report = verify_head_certificate(certificate, signs, 8)
    assert report["valid"]
    assert report["minimum_signed_cleared_score"] == 58
    result = estimate_certified_hstar(
        signs,
        8,
        use_z3_threshold_degree=False,
        projection_permutation_limit=2,
        heuristic_restarts=0,
    )
    assert result["certified_interval"] == [3, 3]


def main() -> None:
    verify_cube_convention()
    verify_small_intervals()
    verify_one_head_integer_certificate()
    verify_six_bit_layered_projection()
    verify_partition_spectral_bound()
    verify_sparse_ptf_estimator_backend()
    verify_optimal_fourier_tail_estimator_backend()
    verify_archived_eight_bit_result()
    exact_backend = verify_optional_exact_backend()
    print("cube convention: verified")
    print("small certified intervals: verified")
    print("strict integer head certificate: verified")
    print("six-bit parity triple-flip interval [4, 6]: verified")
    print("partition spectral lower bound: verified")
    print("sparse PTF estimator backend: verified")
    print("optimal Fourier-tail estimator backend: verified")
    print("eight-bit exact result H^*(f_8) = 3: verified")
    print(
        "optional exact real-arithmetic backend:",
        "verified" if exact_backend else "not installed",
    )


if __name__ == "__main__":
    main()
