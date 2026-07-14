#!/usr/bin/env python3
"""Rank selector gates built from recent hard five-bit cubic residuals.

Only the high selector slice is transformed, so the input complements and
coordinate permutations are not global symmetries of the six-bit table.
Every retained table has exact threshold degree four. Every reported H4 hit
has an exact integer certificate from the inner-LP denominator search. Search
survivors are ranked diagnostics, not head lower bounds.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import search_n6_h4_inner_lp as inner
from search_n6_parity_flip_triples_h4 import exact_degree_four_record
from search_n6_selector_gated_c5_residuals_h4 import (
    TRANSFORMS,
    selector_signs,
    transform_mask,
)


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n6_selector_residual_campaign.json"

BASE_MASKS = (
    ("bc83833c", 0xBC83833C),
    ("fcc3c33c", 0xFCC3C33C),
    ("4cc3c33c", 0x4CC3C33C),
    ("54c3c33c", 0x54C3C33C),
    ("4c83833c", 0x4C83833C),
    ("5483833c", 0x5483833C),
)

# Identity is omitted. Each transformation acts on only one selector slice.
TRANSFORM_INDICES = (1, 2, 3)


def checkpoint(path: Path, records: list[dict[str, object]]) -> None:
    degree_four = [
        record for record in records if record["threshold_degree"] == 4
    ]
    survivors = [
        record for record in degree_four if record["h4_certificate"] is None
    ]
    closest = sorted(
        survivors,
        key=lambda record: record["maximum_inner_lp_margin"],
        reverse=True,
    )
    strongest_negative = sorted(
        survivors,
        key=lambda record: record["maximum_inner_lp_margin"],
    )
    payload = {
        "status": (
            "Every threshold-degree statement and H4 success is exact. "
            "A finite inner-LP search survivor is not a lower bound."
        ),
        "base_masks": {name: f"0x{mask:08x}" for name, mask in BASE_MASKS},
        "high_slice_transform_indices": list(TRANSFORM_INDICES),
        "records": records,
        "persistent_survivors_by_closest_margin": [
            record["truth_mask_hex"] for record in closest
        ],
        "persistent_survivors_by_strongest_negative_margin": [
            record["truth_mask_hex"] for record in strongest_negative
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=2)
    parser.add_argument("--max-iterations", type=int, default=120)
    parser.add_argument("--seed", type=int, default=202607143)
    parser.add_argument(
        "--scales",
        type=int,
        nargs="+",
        default=(30, 100, 300, 1000, 3000, 10000),
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--limit",
        type=int,
        help="stop after this many raw selector specifications",
    )
    arguments = parser.parse_args()

    records: list[dict[str, object]] = []
    seen_masks: set[int] = set()
    raw_index = 0
    for low_name, low_mask in BASE_MASKS:
        for high_name, high_base_mask in BASE_MASKS:
            for transform_index in TRANSFORM_INDICES:
                if arguments.limit is not None and raw_index >= arguments.limit:
                    checkpoint(arguments.output, records)
                    return
                transform = TRANSFORMS[transform_index]
                high_mask = transform_mask(
                    high_base_mask,
                    transform["permutation"],
                    transform["input_xor"],
                    transform["output_complement"],
                )
                six_bit_mask = low_mask | (high_mask << 32)
                specification_index = raw_index
                raw_index += 1
                if six_bit_mask in seen_masks:
                    continue
                seen_masks.add(six_bit_mask)
                signs = selector_signs(low_mask, high_mask)
                degree = exact_degree_four_record(signs)
                record: dict[str, object] = {
                    "specification_index": specification_index,
                    "low_name": low_name,
                    "low_mask_hex": f"0x{low_mask:08x}",
                    "high_base_name": high_name,
                    "high_base_mask_hex": f"0x{high_base_mask:08x}",
                    "high_transform_index": transform_index,
                    "high_transform": transform,
                    "high_transformed_mask_hex": f"0x{high_mask:08x}",
                    "truth_mask_hex": f"0x{six_bit_mask:016x}",
                    **degree,
                    "orientation_attempts": [],
                    "maximum_inner_lp_margin": None,
                    "h4_certificate": None,
                }
                if degree["threshold_degree"] == 4:
                    margins = []
                    for positive_heads in range(5):
                        certificate, best = inner.search_orientation(
                            signs.astype(float),
                            positive_heads,
                            arguments.seed
                            + 100003 * specification_index
                            + 1009 * positive_heads,
                            arguments.restarts,
                            arguments.max_iterations,
                            tuple(arguments.scales),
                        )
                        margin = float(
                            best.get("continuous_inner_lp_margin", float("-inf"))
                        )
                        margins.append(margin)
                        record["orientation_attempts"].append(
                            {
                                "positive_heads": positive_heads,
                                "best": best,
                            }
                        )
                        print(
                            f"spec={specification_index} low={low_name} "
                            f"high={high_name} transform={transform['name']} "
                            f"positive_heads={positive_heads} "
                            f"found={certificate is not None} margin={margin}",
                            flush=True,
                        )
                        if certificate is not None:
                            record["h4_certificate"] = certificate
                            break
                    record["maximum_inner_lp_margin"] = max(margins)
                else:
                    print(
                        f"spec={specification_index} low={low_name} "
                        f"high={high_name} transform={transform['name']} "
                        f"degree={degree['threshold_degree']}",
                        flush=True,
                    )
                records.append(record)
                checkpoint(arguments.output, records)

    degree_four = [
        record for record in records if record["threshold_degree"] == 4
    ]
    survivors = [
        record
        for record in degree_four
        if record["h4_certificate"] is None
    ]
    print(f"unique selector tables: {len(records)}")
    print(f"exact degree-four tables: {len(degree_four)}")
    print(f"exact H4 hits: {len(degree_four) - len(survivors)}")
    print(f"persistent search survivors: {len(survivors)}")


if __name__ == "__main__":
    main()
