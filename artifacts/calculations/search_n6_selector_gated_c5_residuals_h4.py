#!/usr/bin/env python3
"""Screen selector gates between hard five-bit cubic residual cells.

For two five-bit truth tables g0 and g1, form the six-bit selector table

    F(x, z) = g0(x) when z = 0, and g1(x) when z = 1.

The second cofactor is deliberately transformed by coordinate permutations
and input complements. Each table is classified exactly by threshold degree,
then every four-head orientation count is searched. Every H4 success is
verified with integer arithmetic. A search failure is not a lower bound.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import search_gated_single_flip as h4
from search_n6_parity_flip_triples_h4 import exact_degree_four_record


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n6_selector_gated_c5_residuals_h4_screen.json"

BASE_MASKS = (
    ("a", 0x6956BFE8),
    ("b", 0x69D73FE8),
    ("c", 0xBC83833C),
)

TRANSFORMS = (
    {
        "name": "identity",
        "permutation": (0, 1, 2, 3, 4),
        "input_xor": 0,
        "output_complement": False,
    },
    {
        "name": "shuffle_xor_21",
        "permutation": (2, 4, 1, 3, 0),
        "input_xor": 21,
        "output_complement": False,
    },
    {
        "name": "reverse_xor_7",
        "permutation": (4, 3, 2, 1, 0),
        "input_xor": 7,
        "output_complement": False,
    },
    {
        "name": "cross_xor_11_output_complement",
        "permutation": (3, 0, 4, 1, 2),
        "input_xor": 11,
        "output_complement": True,
    },
)


def permute_code(code: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for source, target in enumerate(permutation):
        answer |= ((code >> source) & 1) << target
    return answer


def transform_mask(
    mask: int,
    permutation: tuple[int, ...],
    input_xor: int,
    output_complement: bool,
) -> int:
    answer = 0
    for code in range(32):
        source = permute_code(code, permutation) ^ input_xor
        value = (mask >> source) & 1
        if output_complement:
            value ^= 1
        answer |= value << code
    return answer


def selector_signs(low_mask: int, high_mask: int) -> np.ndarray:
    return np.array(
        [
            1
            if (
                (low_mask >> code) & 1
                if code < 32
                else (high_mask >> (code - 32)) & 1
            )
            else -1
            for code in range(64)
        ],
        dtype=np.int64,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--max-iterations", type=int, default=1600)
    parser.add_argument("--seed", type=int, default=202607141)
    parser.add_argument(
        "--scales", type=int, nargs="+", default=(30, 100, 300, 1000, 3000)
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--transform-index",
        type=int,
        action="append",
        choices=range(len(TRANSFORMS)),
        help="screen only selected transform indices; may be repeated",
    )
    arguments = parser.parse_args()

    transforms = (
        TRANSFORMS
        if arguments.transform_index is None
        else tuple(TRANSFORMS[index] for index in arguments.transform_index)
    )
    records = []
    candidate_index = 0
    for low_name, low_mask in BASE_MASKS:
        for high_name, high_base_mask in BASE_MASKS:
            for transform in transforms:
                high_mask = transform_mask(
                    high_base_mask,
                    transform["permutation"],
                    transform["input_xor"],
                    transform["output_complement"],
                )
                signs = selector_signs(low_mask, high_mask)
                degree = exact_degree_four_record(signs)
                six_bit_mask = low_mask | (high_mask << 32)
                record: dict[str, object] = {
                    "low_name": low_name,
                    "low_mask_hex": f"0x{low_mask:08x}",
                    "high_base_name": high_name,
                    "high_base_mask_hex": f"0x{high_base_mask:08x}",
                    "high_transform": transform,
                    "high_transformed_mask_hex": f"0x{high_mask:08x}",
                    "truth_mask_hex": f"0x{six_bit_mask:016x}",
                    **degree,
                    "attempts": [],
                    "h4_certificate": None,
                }
                if degree["threshold_degree"] == 4:
                    for positive_heads in range(5):
                        certificate, best = h4.search_orientation(
                            signs,
                            5,
                            positive_heads,
                            arguments.seed
                            + 100003 * candidate_index
                            + 1009 * positive_heads,
                            arguments.restarts,
                            arguments.max_iterations,
                            tuple(arguments.scales),
                        )
                        record["attempts"].append(
                            {"positive_heads": positive_heads, "best": best}
                        )
                        print(
                            f"candidate={candidate_index} low={low_name} "
                            f"high={high_name} transform={transform['name']} "
                            f"positive_heads={positive_heads} "
                            f"found={certificate is not None} best={best}",
                            flush=True,
                        )
                        if certificate is not None:
                            record["h4_certificate"] = certificate
                            break
                else:
                    print(
                        f"candidate={candidate_index} low={low_name} "
                        f"high={high_name} transform={transform['name']} "
                        f"degree={degree['threshold_degree']}",
                        flush=True,
                    )
                records.append(record)
                candidate_index += 1
                payload = {
                    "status": (
                        "Every threshold-degree statement and H4 success is "
                        "exact. An H4 search failure is not a lower bound."
                    ),
                    "base_masks": {
                        name: f"0x{mask:08x}" for name, mask in BASE_MASKS
                    },
                    "records": records,
                }
                arguments.output.write_text(json.dumps(payload, indent=2) + "\n")

    exact_degree_four = [
        record for record in records if record["threshold_degree"] == 4
    ]
    survivors = [
        record
        for record in exact_degree_four
        if record["h4_certificate"] is None
    ]
    print(f"exact degree-four targets: {len(exact_degree_four)}")
    print(f"H4 search survivors: {len(survivors)}")


if __name__ == "__main__":
    main()
