#!/usr/bin/env python3
"""Map small quotient-cut bridges for the 120-row slice-poset system.

Exact extreme-anisotropy examples escape even the full collection of 15 cut
rows.  This diagnostic therefore does not search for a universal certificate.
It records which smaller cut subsets obstruct selected denominator tuples and
includes the known exact escapes in its bank.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np

import analyze_n6_parity_triple_global_dual as global_dual
import analyze_n6_parity_triple_quotient_cut_tangent as quotient
import analyze_n6_parity_triple_slice_subsystems as common
import verify_n6_parity_triple_slice_cone_limit as slice_limit


MIDDLE_INDICES = tuple(
    index for index, label in enumerate(common.LABELS)
    if label[2] in (2, 3)
)
MIDDLE_R = common.R[list(MIDDLE_INDICES)]
AGGREGATE_ESCAPE_DENOMINATORS = np.array(
    [
        [1572876, -524288, -8, -262144, -524288, -262144, -2],
        [853137, -16, -1024, -262144, -128, -65536, -524288],
        [2060, -2, -2, -2048, -2, -4, -1],
        [28993, 4096, 32, 32, 16384, 8192, 1],
    ],
    dtype=float,
)
FULL_CUT_ESCAPE_DENOMINATORS = np.array(
    [
        [135562, -131072, -256, -128, -4096, -1, -8],
        [794898, -524288, -8, -2, -8192, -262144, -8],
        [2433, -16, -1, -64, -256, -32, -2048],
        [1328512, -128, -262144, -1048576, -512, -512, -16384],
    ],
    dtype=float,
)


def sample_denominators_wide(
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


def bank(
    rng: np.random.Generator, samples: int, log_span: float
) -> list[np.ndarray]:
    answer = [
        np.array(global_dual.DENOMINATORS, dtype=float),
        np.array(global_dual.SMALL_DENOMINATORS, dtype=float),
        np.array(slice_limit.DENOMINATORS, dtype=float),
        AGGREGATE_ESCAPE_DENOMINATORS,
        FULL_CUT_ESCAPE_DENOMINATORS,
    ]
    for positive_heads in range(3):
        for sample in range(samples):
            span = log_span * (0.2 + 0.8 * (sample + 1) / samples)
            answer.append(
                sample_denominators_wide(rng, positive_heads, span)
            )
    return answer


def obstructs(rows: np.ndarray, tangent: np.ndarray) -> bool:
    pulled_back = rows @ tangent
    row_scales = np.maximum(np.linalg.norm(pulled_back, axis=1), 1e-300)
    pulled_back = pulled_back / row_scales[:, None]
    scales = np.maximum(np.linalg.norm(pulled_back, axis=0), 1e-300)
    found, _ = common.has_gordan_multiplier(
        pulled_back / scales[None, :]
    )
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=40)
    parser.add_argument("--log-span", type=float, default=8.0)
    parser.add_argument("--max-cuts", type=int, default=3)
    parser.add_argument("--cut", type=int, action="append")
    parser.add_argument("--greedy", action="store_true")
    parser.add_argument("--seed", type=int, default=20260714)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    denominators = bank(rng, args.samples, args.log_span)
    tangents = [common.tangent_map(item) for item in denominators]
    print(f"denominator bank: {len(tangents)}")
    if args.greedy:
        chosen: tuple[int, ...] = ()
        while True:
            rows = (
                MIDDLE_R
                if not chosen
                else np.vstack([MIDDLE_R, quotient.CUT_R[list(chosen)]])
            )
            failures = tuple(
                index
                for index, tangent in enumerate(tangents)
                if not obstructs(rows, tangent)
            )
            print(
                f"  greedy cuts={chosen} failures={len(failures)} "
                f"examples={failures[:12]}"
            )
            if not failures or len(chosen) == 15:
                return
            candidates = []
            for cut in range(15):
                if cut in chosen:
                    continue
                trial = tuple(sorted((*chosen, cut)))
                trial_rows = np.vstack(
                    [MIDDLE_R, quotient.CUT_R[list(trial)]]
                )
                remaining = sum(
                    not obstructs(trial_rows, tangents[index])
                    for index in failures
                )
                candidates.append((remaining, cut))
            remaining, cut = min(candidates)
            print(f"    add cut={cut} predicted_failures={remaining}")
            chosen = tuple(sorted((*chosen, cut)))

    for size in range(1, args.max_cuts + 1):
        records = []
        subsets = (
            [tuple(args.cut)]
            if args.cut is not None
            else itertools.combinations(range(15), size)
        )
        for subset in subsets:
            rows = np.vstack([MIDDLE_R, quotient.CUT_R[list(subset)]])
            failures = []
            for index, tangent in enumerate(tangents):
                if not obstructs(rows, tangent):
                    failures.append(index)
            records.append((len(failures), subset, tuple(failures[:8])))
        records.sort()
        print(f"cut_count={size} tested={len(records)}")
        for failures, subset, examples in records[:20]:
            cosets = tuple(
                tuple(sorted(quotient.NONEXCEPTIONAL_COSETS[index]))
                for index in subset
            )
            print(
                f"  failures={failures}/{len(tangents)} "
                f"cuts={subset} cosets={cosets} examples={examples}"
            )
        if args.cut is not None:
            break


if __name__ == "__main__":
    main()
