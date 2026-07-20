#!/usr/bin/env python3
"""Benchmark sparse common-margin LPs and exact signed-secant leaf recovery."""

from __future__ import annotations

import json
from time import perf_counter

import numpy as np

from hstar.boolean_cube import VERTEX_ORDER, mask_from_signs, signs_from_mask
from hstar.certified import _eight_bit_hamming_signs
from hstar.signed_secant_mccormick import (
    discover_signed_secant_mccormick_leaf,
)


def skeleton(
    signs: np.ndarray,
    dimension: int,
    orientations: list[int],
    chart: dict,
) -> dict:
    head_count = len(orientations)
    direction_bounds = [
        [[-1, 1] for _ in range(dimension + 1)]
        for _ in range(head_count)
    ]
    scalar_bounds = [-1, 1]
    if chart["kind"] == "scalar-direction":
        scalar_bounds = [chart["value"], chart["value"]]
    else:
        direction_bounds[chart["head"]][chart["literal"]] = [
            chart["value"],
            chart["value"],
        ]
    return {
        "schema_version": 1,
        "certificate_type": "signed-secant-mccormick-leaf",
        "dimension": dimension,
        "vertex_order": VERTEX_ORDER,
        "truth_mask_hex": hex(mask_from_signs(signs, dimension)),
        "head_count": head_count,
        "orientations": orientations,
        "chart": chart,
        "cell": {
            "theta_bounds": [
                [[0, 1] for _ in range(dimension + 1)]
                for _ in range(head_count)
            ],
            "direction_bounds": direction_bounds,
            "scalar_direction_bounds": scalar_bounds,
            "t_bounds": [0, 1],
        },
    }


def run_case(signs: np.ndarray, candidate: dict) -> dict:
    start = perf_counter()
    certificate, diagnostics = discover_signed_secant_mccormick_leaf(
        candidate,
        signs,
        max_denominator=1024,
    )
    elapsed = perf_counter() - start
    return {
        "orientations": candidate["orientations"],
        "chart": candidate["chart"],
        "status": diagnostics["status"],
        "floating_margin_upper_bound": diagnostics.get(
            "floating_margin_upper_bound"
        ),
        "exact_upper_bound": diagnostics.get("exact_upper_bound"),
        "candidate_lambda_support": diagnostics.get(
            "candidate_lambda_support"
        ),
        "working_variables": diagnostics["working_variables"],
        "working_inequalities": diagnostics["working_inequalities"],
        "working_equalities": diagnostics["working_equalities"],
        "working_product_nodes": diagnostics["working_product_nodes"],
        "verified_certificate_found": certificate is not None,
        "elapsed_seconds": elapsed,
    }


def main() -> None:
    xor_signs = signs_from_mask(0x6, 2)
    xor_cases = []
    for orientation in (1, -1):
        charts = [
            {"kind": "scalar-direction", "value": value}
            for value in (1, -1)
        ]
        charts.extend(
            {
                "kind": "direction-coordinate",
                "head": 0,
                "literal": literal,
                "value": value,
            }
            for literal in range(3)
            for value in (1, -1)
        )
        xor_cases.extend(
            run_case(
                xor_signs,
                skeleton(xor_signs, 2, [orientation], chart),
            )
            for chart in charts
        )
    xor_verified = sum(
        case["status"] == "verified-exact-leaf-found"
        for case in xor_cases
    )
    xor_positive = sum(
        case["status"] == "relaxed-common-margin-positive"
        for case in xor_cases
    )
    assert (xor_verified, xor_positive) == (8, 8)

    f8_signs = _eight_bit_hamming_signs()
    f8_cases = []
    for orientations in ([1, 1], [1, -1], [-1, -1]):
        for value in (1, -1):
            chart = {"kind": "scalar-direction", "value": value}
            f8_cases.append(
                run_case(
                    f8_signs,
                    skeleton(f8_signs, 8, orientations, chart),
                )
            )
    f8_verified = sum(
        case["status"] == "verified-exact-leaf-found"
        for case in f8_cases
    )
    f8_positive = sum(
        case["status"] == "relaxed-common-margin-positive"
        for case in f8_cases
    )
    assert (f8_verified, f8_positive) == (2, 4)

    f6_signs = signs_from_mask(0x96696BD669B69669, 6)
    f6_cases = []
    for positive_count in range(5):
        orientations = [1] * positive_count + [-1] * (4 - positive_count)
        for value in (1, -1):
            chart = {"kind": "scalar-direction", "value": value}
            f6_cases.append(
                run_case(
                    f6_signs,
                    skeleton(f6_signs, 6, orientations, chart),
                )
            )
    f6_verified = sum(
        case["status"] == "verified-exact-leaf-found"
        for case in f6_cases
    )
    f6_positive = sum(
        case["status"] == "relaxed-common-margin-positive"
        for case in f6_cases
    )
    assert (f6_verified, f6_positive) == (2, 8)

    print(
        json.dumps(
            {
                "status": "verified-benchmark",
                "xor2_h1_raw_charts": {
                    "verified_root_leaves": xor_verified,
                    "positive_relaxations": xor_positive,
                    "cases": xor_cases,
                },
                "f8_h2_scalar_charts": {
                    "verified_full_chart_leaves": f8_verified,
                    "positive_relaxations": f8_positive,
                    "cases": f8_cases,
                },
                "f6_h4_scalar_charts": {
                    "verified_full_chart_leaves": f6_verified,
                    "positive_relaxations": f6_positive,
                    "cases": f6_cases,
                },
                "interpretation": (
                    "positive McCormick relaxations are unresolved outer "
                    "approximations, not feasible signed secants"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
