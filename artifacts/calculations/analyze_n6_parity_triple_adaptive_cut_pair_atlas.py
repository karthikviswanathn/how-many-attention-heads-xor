#!/usr/bin/env python3
"""Build a diagnostic atlas of two-cut bridges for the n6 parity-triple target.

For each admissible denominator tuple, this diagnostic tests all 105 pairs of
nonexceptional quotient-cut rows together with the 120 middle slice-poset
rows.  It reports whether at least one pair gives a Gordan obstruction and
how frequently each pair works, split by denominator orientation count.
The bank includes a known exact tuple that escapes all 15 cut rows, so the
output explicitly demonstrates that no quotient-cut pair is universal.
"""

from __future__ import annotations

import argparse
from collections import Counter
import itertools

import numpy as np

import analyze_n6_parity_triple_global_dual as global_dual
import analyze_n6_parity_triple_quotient_cut_tangent as quotient
import analyze_n6_parity_triple_slice_subsystems as common
import search_n6_parity_triple_cut_bridge_minimal as bridge
import verify_n6_parity_triple_slice_cone_limit as slice_limit


PAIRS = tuple(itertools.combinations(range(15), 2))


def orientation_count(denominators: np.ndarray) -> int:
    return int(sum(np.all(row[1:] > 0) for row in denominators))


def sample_bank(
    rng: np.random.Generator, samples: int, log_span: float
) -> list[tuple[str, int, np.ndarray]]:
    exact_rows = (
        ("exact_old", np.array(global_dual.DENOMINATORS, dtype=float)),
        ("exact_small_generic", np.array(global_dual.SMALL_DENOMINATORS, dtype=float)),
        ("exact_slice_escape", np.array(slice_limit.DENOMINATORS, dtype=float)),
        ("exact_aggregate_escape", bridge.AGGREGATE_ESCAPE_DENOMINATORS.copy()),
        ("exact_full_cut_escape", bridge.FULL_CUT_ESCAPE_DENOMINATORS.copy()),
    )
    answer = [
        (label, orientation_count(denominators), denominators)
        for label, denominators in exact_rows
    ]
    for positive_heads in range(3):
        for sample in range(samples):
            span = log_span * (0.2 + 0.8 * (sample + 1) / samples)
            denominators = bridge.sample_denominators_wide(
                rng, positive_heads, span
            )
            answer.append(
                (f"random_r{positive_heads}_{sample}", positive_heads, denominators)
            )
    return answer


def working_pairs(tangent: np.ndarray) -> tuple[tuple[int, int], ...]:
    answer = []
    for pair in PAIRS:
        rows = np.vstack(
            [bridge.MIDDLE_R, quotient.CUT_R[list(pair)]]
        )
        if bridge.obstructs(rows, tangent):
            answer.append(pair)
    return tuple(answer)


def print_frequency(
    label: str,
    records: list[tuple[str, int, tuple[tuple[int, int], ...]]],
) -> None:
    counts = Counter(
        pair for _, _, pairs in records for pair in pairs
    )
    uncovered = [name for name, _, pairs in records if not pairs]
    sizes = [len(pairs) for _, _, pairs in records]
    print(
        f"{label}: tuples={len(records)} uncovered={len(uncovered)} "
        f"working_pairs={min(sizes, default=0)}..{max(sizes, default=0)}"
    )
    if uncovered:
        print("  uncovered_examples=", tuple(uncovered[:12]))
    for pair, count in counts.most_common(15):
        cosets = tuple(
            tuple(sorted(quotient.NONEXCEPTIONAL_COSETS[index]))
            for index in pair
        )
        print(f"  pair={pair} count={count}/{len(records)} cosets={cosets}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--log-span", type=float, default=8.0)
    parser.add_argument("--seed", type=int, default=20260714)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    bank = sample_bank(rng, args.samples, args.log_span)
    records = []
    for index, (label, positive_heads, denominators) in enumerate(bank):
        pairs = working_pairs(common.tangent_map(denominators))
        records.append((label, positive_heads, pairs))
        if label.startswith("exact_"):
            print(
                f"{label}: orientation={positive_heads} "
                f"working_pair_count={len(pairs)} pairs={pairs}"
            )
        if (index + 1) % 50 == 0:
            print(f"processed {index + 1}/{len(bank)}", flush=True)

    print_frequency("all", records)
    for positive_heads in range(3):
        selected = [
            record for record in records if record[1] == positive_heads
        ]
        print_frequency(f"orientation_{positive_heads}", selected)


if __name__ == "__main__":
    main()
