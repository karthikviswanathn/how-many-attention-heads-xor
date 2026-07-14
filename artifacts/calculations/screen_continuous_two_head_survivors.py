#!/usr/bin/env python3
"""Run the boundary-aware continuous H2 solver on saved search survivors."""
from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

import numpy as np

import search_adversarial_low_dimension as core
import search_continuous_two_head as continuous


HERE = Path(__file__).resolve().parent


def verify_payload(payload: dict[str, object]) -> None:
    n = int(payload["dimension"])
    affine = core.affine_matrix(n).astype(object)
    for record in payload["records"]:
        mask = int(record["truth_mask_hex"], 16)
        signs = core.signs_from_mask(mask, n)
        polynomial = np.array(record["degree_two_coefficients"], dtype=object)
        assert np.all(
            signs * (core.monomial_matrix(n, 2).astype(object) @ polynomial) > 0
        )
        result = record["continuous_search"]
        if not result["found"]:
            continue
        denominators = np.array(result["denominators"], dtype=object)
        for denominator in denominators:
            assert np.all(denominator[1:] > 0) or np.all(denominator[1:] < 0)
            assert np.all(affine @ denominator > 0)
        coefficients = np.array(
            result["cleared_score_coefficients"], dtype=object
        )
        matrix = continuous.cleared_matrix(
            affine.astype(np.int64), denominators.tolist()
        )
        signed_scores = signs * (matrix @ coefficients)
        assert np.all(signed_scores > 0)
        assert min(map(int, signed_scores)) == result["minimum_signed_cleared_score"]
    print(
        f"verified {len(payload['records'])} continuous survivor screens",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--restarts", type=int, default=100)
    parser.add_argument("--max-iterations", type=int, default=2000)
    parser.add_argument("--max-records", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260720)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_payload(json.loads(arguments.output.read_text()))
        return

    source = json.loads(arguments.input.read_text())
    n = int(source["n"])
    survivors = [
        record
        for record in source["final_records"]
        if not record["orientation_cycle_search"]["found"]
    ]
    if arguments.max_records:
        survivors = survivors[: arguments.max_records]
    records = []
    payload = {
        "status": (
            "Every success is exact.  A continuous search failure is not "
            "an H2 lower bound."
        ),
        "dimension": n,
        "source": arguments.input.name,
        "restarts_per_orientation": arguments.restarts,
        "max_iterations": arguments.max_iterations,
        "records": records,
    }
    for index, record in enumerate(survivors):
        mask = int(record["truth_mask_hex"], 16)
        search_arguments = Namespace(
            dimension=n,
            mask=mask,
            restarts=arguments.restarts,
            max_iterations=arguments.max_iterations,
            seed=arguments.seed + 100003 * index,
            scales=(10, 30, 100, 300, 1000, 3000, 10000, 100000, 1000000),
        )
        result = continuous.search(search_arguments)
        records.append(
            {
                "truth_mask_hex": record["truth_mask_hex"],
                "degree_two_coefficients": record["degree_two_coefficients"],
                "fixed_dictionary_hit_count": record[
                    "fixed_dictionary_hit_count"
                ],
                "previous_search": record["orientation_cycle_search"],
                "continuous_search": result,
            }
        )
        arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
        print(
            f"continuous survivor {index + 1}/{len(survivors)}: "
            f"found={result['found']} mask={record['truth_mask_hex']}",
            flush=True,
        )
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    verify_payload(payload)


if __name__ == "__main__":
    main()
