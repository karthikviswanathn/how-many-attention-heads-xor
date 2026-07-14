#!/usr/bin/env python3
"""Stress-test fixed pointwise subsystems for the six-bit H4 candidate.

The full 64 signed evaluation rows obstruct every denominator tuple tested so
far.  This diagnostic asks whether the structured 40-vertex support from the
exact degree-three Gordan witness already suffices after pullback through a
four-head tangent map.  Sampling is evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np

import analyze_n6_parity_triple_slice_subsystems as common


MASK = 0x96696BD669B69669
FULL = (1 << common.N) - 1

DEGREE_THREE_SUPPORT = (
    1, 2, 3, 4, 7, 8, 10, 12, 13, 14, 15, 19, 20, 24, 25, 26, 28, 29,
    30, 31, 33, 34, 35, 39, 40, 41, 44, 45, 46, 49, 50, 51, 52, 55, 56,
    58, 60, 61, 62, 63,
)

EXACT_TUPLES = (
    np.array(
        [
            [21, -1, -1, -15, -1, -1, -1],
            [40, -1, -1, -1, -6, -1, -29],
            [25, -12, -1, -4, -5, -1, -1],
            [46, 5, 3, 1, 27, 7, 2],
        ],
        dtype=float,
    ),
    np.array(
        [
            [135562, -131072, -256, -128, -4096, -1, -8],
            [794898, -524288, -8, -2, -8192, -262144, -8],
            [2433, -16, -1, -64, -256, -32, -2048],
            [1328512, -128, -262144, -1048576, -512, -512, -16384],
        ],
        dtype=float,
    ),
)


def character(mask: int, code: int) -> int:
    return common.character(mask, code)


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


SIGNED_EVALUATION_ROWS = np.array(
    [
        [target_sign(code) * character(mask, code) for mask in range(FULL + 1)]
        for code in range(FULL + 1)
    ],
    dtype=float,
)


def summarize(
    denominators: np.ndarray, support: tuple[int, ...]
) -> tuple[bool, int, float, int]:
    matrix = (
        SIGNED_EVALUATION_ROWS[list(support)]
        @ common.tangent_map(denominators)
    )
    column_scale = np.maximum(np.linalg.norm(matrix, axis=0), 1e-300)
    normalized = matrix / column_scale[None, :]
    # Positive row rescaling preserves both sides of Gordan's alternative.
    # It is essential for extreme denominator tuples: without it, HiGHS can
    # report a false infeasibility even when a well-interior dual exists.
    row_scale = np.maximum(np.max(np.abs(normalized), axis=1), 1e-300)
    normalized = normalized / row_scale[:, None]
    found, circuit_support = common.has_gordan_multiplier(normalized)
    margin = common.strict_gordan_margin(normalized)
    return (
        found,
        circuit_support,
        margin,
        int(np.linalg.matrix_rank(matrix)),
    )


def sample_denominators(
    rng: np.random.Generator, positive_heads: int, log_span: float
) -> np.ndarray:
    orientations = [-1] * (common.HEADS - positive_heads) + [1] * positive_heads
    rows = []
    for orientation in orientations:
        slopes = np.exp(rng.uniform(-log_span, log_span, size=common.N))
        slack = float(np.exp(rng.uniform(-log_span, log_span)))
        rows.append(
            np.concatenate([[np.sum(slopes) + slack], orientation * slopes])
        )
    return np.vstack(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--log-span", type=float, default=2.0)
    parser.add_argument("--only-complement", action="store_true")
    args = parser.parse_args()

    systems = (
        ("degree_three_support", DEGREE_THREE_SUPPORT),
        (
            "degree_three_support_plus_exceptions",
            tuple(sorted(set(DEGREE_THREE_SUPPORT) | {21, 38, 41})),
        ),
        (
            "degree_three_support_plus_exception_plane",
            tuple(sorted(set(DEGREE_THREE_SUPPORT) | {21, 26, 38, 41})),
        ),
        (
            "degree_three_support_plus_complement",
            tuple(
                sorted(
                    set(DEGREE_THREE_SUPPORT)
                    | {FULL ^ code for code in DEGREE_THREE_SUPPORT}
                )
            ),
        ),
        ("full", tuple(range(FULL + 1))),
    )
    if args.only_complement:
        systems = tuple(
            item
            for item in systems
            if item[0] in ("degree_three_support_plus_complement", "full")
        )
    for tuple_index, denominators in enumerate(EXACT_TUPLES):
        for name, support in systems:
            print(
                f"exact_tuple={tuple_index} system={name} ",
                summarize(denominators, support),
            )

    rng = np.random.default_rng(args.seed)
    for name, support in systems:
        print(f"system={name} rows={len(support)}")
        for positive_heads in range(3):
            successes = 0
            strict = 0
            minimum_margin = float("inf")
            first_failure = None
            for sample in range(args.samples):
                denominators = sample_denominators(
                    rng, positive_heads, args.log_span
                )
                found, _, margin, _ = summarize(denominators, support)
                successes += int(found)
                strict += int(margin > 1e-9)
                minimum_margin = min(minimum_margin, margin)
                if not found and first_failure is None:
                    first_failure = (sample, denominators.tolist())
            print(
                f"  positive_heads={positive_heads} gordan={successes}/{args.samples} "
                f"strict={strict}/{args.samples} minimum_margin={minimum_margin}"
            )
            if first_failure is not None:
                print("    first_failure=", first_failure)


if __name__ == "__main__":
    main()
