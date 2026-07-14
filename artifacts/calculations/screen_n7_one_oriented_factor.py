#!/usr/bin/env python3
"""Screen fresh seven-bit quadratic cells with the exact H2 relaxation.

The learner is the one-oriented-factor search.  Every success is converted to
two admissible denominators and checked with integer arithmetic by the imported
search routine.  A surviving record is only a search survivor.
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

import search_continuous_one_oriented_factor as learner
import verify_two_head_candidate_refutations as archived


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "adversarial_n7_pilot_results.json"
DEFAULT_OUTPUT = HERE / "adversarial_n7_one_oriented_screen.json"

ARCHIVED_MASKS = {
    archived.N7_POSITIVE_ORIENTATION_TRUTH_MASK,
    archived.N7_NEGATIVE_ORIENTATION_TRUTH_MASK,
    archived.N7_MAIN_TRUTH_MASK,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--restarts", type=int, default=20)
    parser.add_argument("--max-iterations", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=202607147)
    arguments = parser.parse_args()

    source = json.loads(arguments.input.read_text())
    records = []
    excluded = []
    for source_index, record in enumerate(source["final_records"]):
        if record["orientation_cycle_search"]["found"]:
            continue
        mask = int(record["truth_mask_hex"], 16)
        if mask in ARCHIVED_MASKS:
            excluded.append(record["truth_mask_hex"])
            continue
        result = learner.search(
            Namespace(
                dimension=7,
                mask=mask,
                restarts=arguments.restarts,
                max_iterations=arguments.max_iterations,
                seed=arguments.seed + 100003 * source_index,
                scales=(10, 30, 100, 300, 1000, 3000, 10000),
            )
        )
        records.append(
            {
                "truth_mask_hex": record["truth_mask_hex"],
                "degree_two_coefficients": record["degree_two_coefficients"],
                "one_oriented_factor_search": result,
            }
        )
        print(
            f"record {len(records)}: found={result['found']} "
            f"mask={record['truth_mask_hex']}",
            flush=True,
        )

    survivors = sorted(
        (
            record
            for record in records
            if not record["one_oriented_factor_search"]["found"]
        ),
        key=lambda record: (
            record["one_oriented_factor_search"]["best_accuracy"],
            record["one_oriented_factor_search"]["best_minimum_signed_score"],
        ),
        reverse=True,
    )
    payload = {
        "status": (
            "Every success is exact. A search survivor is not an H2 lower "
            "bound."
        ),
        "dimension": 7,
        "source": arguments.input.name,
        "restarts_per_orientation": arguments.restarts,
        "max_iterations": arguments.max_iterations,
        "excluded_archived_masks": excluded,
        "records": records,
        "survivor_masks_ranked": [
            record["truth_mask_hex"] for record in survivors
        ],
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        f"exact H2 hits: {len(records) - len(survivors)}/{len(records)}; "
        f"survivors: {len(survivors)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
