#!/usr/bin/env python3
"""Screen full-cube V5 multiplier cones on five exact hard tuples."""

from __future__ import annotations

import importlib

import numpy as np

import search_n6_parity_triple_repaired_quartic_multiplier as search


HARD_TUPLES = (
    (
        "support54 escape",
        "verify_n6_parity_triple_support54_counterexample",
    ),
    (
        "positive quartic limit",
        "verify_n6_parity_triple_quartic_positive_limit",
    ),
    (
        "S55 uncleared degree-four limit",
        "verify_n6_parity_triple_s55_uncleared_degree4_limit",
    ),
    (
        "S56 uncleared degree-four limit",
        "verify_n6_parity_triple_s56_uncleared_degree4_limit",
    ),
    (
        "S56 cleared degree-four limit",
        "verify_n6_parity_triple_s56_cleared_degree4_limit",
    ),
)
EXPECTED_CLEARED = (
    3.211795072312984e-7,
    0.010639952451704682,
    0.0090245447009682,
    0.008997347046933595,
    0.0079150209673504,
)


def margin(denominators: np.ndarray) -> float:
    logits, orientations = search.denominator_logits(denominators)
    _, _, diagnostics = search.strict_margin(logits.ravel(), orientations)
    return float(diagnostics["margin"])


def main() -> None:
    search.use_full_degree_five()
    search.MINIMUM_WEIGHT = 0.0
    denominators = tuple(
        np.asarray(importlib.import_module(module).DENOMINATORS, dtype=float)
        for _, module in HARD_TUPLES
    )

    search.USE_CLEARED = False
    uncleared = tuple(margin(current) for current in denominators)
    assert all(abs(value) < 1e-12 for value in uncleared)

    search.USE_CLEARED = True
    cleared = tuple(margin(current) for current in denominators)
    assert all(value > 0 for value in cleared)
    assert np.allclose(cleared, EXPECTED_CLEARED, rtol=1e-9, atol=1e-12)

    for (name, _), left, right in zip(HARD_TUPLES, uncleared, cleared):
        print(
            f"{name}: uncleared={left:.12g}, "
            f"cleared={right:.12g}"
        )
    print("screened five exact hard tuples")


if __name__ == "__main__":
    main()
