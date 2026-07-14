#!/usr/bin/env python3
"""Test the quotient-cut cone against admissible four-head tangent spaces.

For six-bit parity with the three vertices 21, 38, and 41 flipped, parity
twisting a quartic sign representative gives a signed value vector whose
sum on each nonexceptional coset of ``span_F2{51, 60}`` is positive.  These
15 inequalities couple all six one-bit slices.  This diagnostic pulls them
back through sampled admissible four-head tangent maps and asks for a
nonnegative Gordan multiplier.  Sampling is evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np

import analyze_n6_parity_triple_slice_subsystems as common
import analyze_n6_parity_triple_global_dual as global_dual


FULL = (1 << common.N) - 1
EXCEPTIONAL = frozenset((21, 38, 41))
SUBSPACE = frozenset((0, 51, 60, 51 ^ 60))
EXCEPTIONAL_COSET = frozenset(21 ^ value for value in SUBSPACE)


def parity(code: int) -> int:
    return common.character(FULL, code)


def quotient_cosets() -> tuple[frozenset[int], ...]:
    unseen = set(range(1 << common.N))
    answer = []
    while unseen:
        representative = min(unseen)
        coset = frozenset(representative ^ value for value in SUBSPACE)
        answer.append(coset)
        unseen.difference_update(coset)
    return tuple(answer)


COSETS = quotient_cosets()
NONEXCEPTIONAL_COSETS = tuple(
    coset for coset in COSETS if coset != EXCEPTIONAL_COSET
)


def cut_rows() -> np.ndarray:
    """Return rows acting on Boolean Fourier coefficients of the quartic."""
    rows = []
    for coset in NONEXCEPTIONAL_COSETS:
        row = np.array(
            [
                sum(
                    parity(code) * common.character(mask, code)
                    for code in coset
                )
                for mask in range(1 << common.N)
            ],
            dtype=float,
        )
        rows.append(row)
    return np.vstack(rows)


CUT_R = cut_rows()


def summarize(
    denominators: np.ndarray, rows: np.ndarray
) -> tuple[bool, int, float, int]:
    pulled_back = rows @ common.tangent_map(denominators.astype(float))
    column_scale = np.maximum(np.linalg.norm(pulled_back, axis=0), 1e-300)
    normalized = pulled_back / column_scale[None, :]
    found, support = common.has_gordan_multiplier(normalized)
    margin = common.strict_gordan_margin(normalized)
    rank = int(np.linalg.matrix_rank(pulled_back))
    return found, support, margin, rank


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20260714)
    args = parser.parse_args()

    assert len(COSETS) == 16
    assert len(NONEXCEPTIONAL_COSETS) == 15
    assert EXCEPTIONAL.issubset(EXCEPTIONAL_COSET)
    assert EXCEPTIONAL_COSET == frozenset((21, 26, 38, 41))
    assert np.linalg.matrix_rank(CUT_R) == 15

    middle_indices = tuple(
        index for index, label in enumerate(common.LABELS)
        if label[2] in (2, 3)
    )
    systems = (
        ("cut", CUT_R),
        ("middle_plus_cut", np.vstack([common.R[list(middle_indices)], CUT_R])),
        ("all_slices_plus_cut", np.vstack([common.R, CUT_R])),
    )
    fixed = np.array(global_dual.DENOMINATORS, dtype=float)
    for name, rows in systems:
        print(f"direct_exact_tuple {name}", summarize(fixed, rows))

    rng = np.random.default_rng(args.seed)
    for name, rows in systems:
        print(f"system={name}")
        for positive_heads in range(3):
            successes = 0
            strict_successes = 0
            supports = []
            ranks = []
            margins = []
            first_failure = None
            for sample in range(args.samples):
                denominators = common.sample_denominators(rng, positive_heads)
                found, support, margin, rank = summarize(denominators, rows)
                successes += int(found)
                strict_successes += int(margin > 1e-9)
                if found:
                    supports.append(support)
                elif first_failure is None:
                    first_failure = (sample, denominators.tolist())
                ranks.append(rank)
                margins.append(margin)
            print(
                f"  positive_heads={positive_heads} "
                f"gordan={successes}/{args.samples} "
                f"strict={strict_successes}/{args.samples} "
                f"rank={min(ranks)}..{max(ranks)} "
                f"support={min(supports, default=0)}..{max(supports, default=0)} "
                f"margin={min(margins)}..{max(margins)}"
            )
            if first_failure is not None:
                print("    first_failure=", first_failure)


if __name__ == "__main__":
    main()
