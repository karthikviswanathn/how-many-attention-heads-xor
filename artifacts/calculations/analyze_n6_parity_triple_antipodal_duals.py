#!/usr/bin/env python3
"""Test antipodally structured full-evaluation Farkas witnesses.

The parity-triple target has equal labels on 29 antipodal pairs and opposite
labels on the three pairs containing an exceptional vertex.  This diagnostic
tests full truth-table Farkas multipliers that assign equal weights within the
29 ordinary pairs, while either tying or separating the six exceptional-pair
endpoints.  Every result is numerical evidence only.
"""

from __future__ import annotations

import argparse
from collections import Counter

import numpy as np

import analyze_n6_parity_triple_global_dual as global_dual
import analyze_n6_parity_triple_slice_subsystems as common
import search_n6_parity_triple_cut_bridge_minimal as bridge
import verify_n6_parity_triple_slice_cone_limit as slice_limit
import verify_n6_parity_triple_support54_geometry as support_geometry
import verify_n6_parity_triple_adaptive_alpha_counterexample as adaptive_limit


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
EXCEPTIONAL = frozenset((21, 38, 41))
EXCEPTIONAL_PAIRS = frozenset(
    frozenset((code, FULL ^ code)) for code in EXCEPTIONAL
)
PAIRS = tuple(
    (code, FULL ^ code) for code in range(1 << N) if code < (FULL ^ code)
)
SUPPORT54 = frozenset(range(1 << N)) - support_geometry.EXPECTED_OMITTED


def sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def evaluation_features(
    denominators: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    values = np.array(
        [
            [
                float(row[0])
                + sum(
                    float(row[coordinate + 1])
                    * common.character(1 << coordinate, code)
                    for coordinate in range(N)
                )
                for row in denominators
            ]
            for code in range(1 << N)
        ]
    )
    assert np.all(values > 0)
    affine = np.array(
        [
            [1.0]
            + [common.character(1 << coordinate, code) for coordinate in range(N)]
            for code in range(1 << N)
        ]
    )
    features = np.column_stack(
        [np.ones(1 << N)]
        + [affine[:, 1:] / values[:, head, None] for head in range(4)]
    )
    signed = np.array([sign(code) for code in range(1 << N)])[:, None] * features
    return signed, values


def grouped_rows(
    matrix: np.ndarray,
    exceptional_endpoints_separate: bool,
    vertex_weights: np.ndarray | None = None,
) -> np.ndarray:
    if vertex_weights is None:
        vertex_weights = np.ones(1 << N)
    rows = []
    for left, right in PAIRS:
        pair = frozenset((left, right))
        if exceptional_endpoints_separate and pair in EXCEPTIONAL_PAIRS:
            rows.append(vertex_weights[left] * matrix[left])
            rows.append(vertex_weights[right] * matrix[right])
        else:
            rows.append(
                vertex_weights[left] * matrix[left]
                + vertex_weights[right] * matrix[right]
            )
    return np.vstack(rows)


def ordinary_pair_rows(matrix: np.ndarray) -> np.ndarray:
    return np.vstack(
        [
            matrix[left] + matrix[right]
            for left, right in PAIRS
            if frozenset((left, right)) not in EXCEPTIONAL_PAIRS
        ]
    )


def support54_grouped_rows(
    matrix: np.ndarray, vertex_weights: np.ndarray
) -> np.ndarray:
    rows = []
    for left, right in PAIRS:
        if left not in SUPPORT54:
            assert right not in SUPPORT54
            continue
        assert right in SUPPORT54
        pair = frozenset((left, right))
        if pair in EXCEPTIONAL_PAIRS:
            rows.append(vertex_weights[left] * matrix[left])
            rows.append(vertex_weights[right] * matrix[right])
        else:
            rows.append(
                vertex_weights[left] * matrix[left]
                + vertex_weights[right] * matrix[right]
            )
    assert len(rows) == 29
    return np.vstack(rows)


def has_positive_dual(matrix: np.ndarray) -> tuple[bool, int, float]:
    row_scale = np.maximum(np.linalg.norm(matrix, axis=1), 1e-300)
    normalized = matrix / row_scale[:, None]
    column_scale = np.maximum(np.linalg.norm(normalized, axis=0), 1e-300)
    normalized = normalized / column_scale[None, :]
    found, support = common.has_gordan_multiplier(normalized)
    margin = common.strict_gordan_margin(normalized)
    return found, support, margin


def exact_bank() -> tuple[tuple[str, np.ndarray], ...]:
    return (
        ("old", np.array(global_dual.DENOMINATORS, dtype=float)),
        ("small_generic", np.array(global_dual.SMALL_DENOMINATORS, dtype=float)),
        ("slice_escape", np.array(slice_limit.DENOMINATORS, dtype=float)),
        ("aggregate_escape", bridge.AGGREGATE_ESCAPE_DENOMINATORS.copy()),
        ("full_cut_escape", bridge.FULL_CUT_ESCAPE_DENOMINATORS.copy()),
        (
            "adaptive_alpha_escape",
            np.array(adaptive_limit.DENOMINATORS, dtype=float),
        ),
    )


def product_power(values: np.ndarray, exponent: float) -> np.ndarray:
    logarithms = exponent * np.sum(np.log(values), axis=1)
    logarithms -= np.max(logarithms)
    return np.exp(np.maximum(logarithms, -700.0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--log-span", type=float, default=8.0)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument(
        "--alpha-grid",
        type=float,
        nargs="+",
        default=(-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0),
    )
    args = parser.parse_args()

    assert len(PAIRS) == 32
    assert len(EXCEPTIONAL_PAIRS) == 3
    for label, denominators in exact_bank():
        matrix, values = evaluation_features(denominators)
        product = np.prod(values, axis=1)
        systems = {
            "support54_free": matrix[sorted(SUPPORT54)],
            "all_pairs_tied": grouped_rows(matrix, False),
            "exception_pairs_split": grouped_rows(matrix, True),
            "cleared_pairs_tied": grouped_rows(matrix, False, product),
            "cleared_exception_split": grouped_rows(matrix, True, product),
            "inverse_pairs_tied": grouped_rows(matrix, False, 1.0 / product),
            "ordinary_pairs_only": ordinary_pair_rows(matrix),
        }
        print(label, {name: has_positive_dual(rows) for name, rows in systems.items()})
        power_hits = []
        support54_power_hits = []
        for exponent in args.alpha_grid:
            weights = product_power(values, exponent)
            if has_positive_dual(grouped_rows(matrix, True, weights))[0]:
                power_hits.append(exponent)
            if has_positive_dual(support54_grouped_rows(matrix, weights))[0]:
                support54_power_hits.append(exponent)
        print(f"  exceptional_split_power_hits={tuple(power_hits)}")
        print(f"  support54_power_hits={tuple(support54_power_hits)}")

    rng = np.random.default_rng(args.seed)
    for positive_heads in range(3):
        counts = {
            "support54_free": 0,
            "all_pairs_tied": 0,
            "exception_pairs_split": 0,
            "cleared_pairs_tied": 0,
            "cleared_exception_split": 0,
            "inverse_pairs_tied": 0,
            "ordinary_pairs_only": 0,
        }
        minimum_margins = {name: float("inf") for name in counts}
        power_counts = Counter()
        power_union = 0
        support54_power_counts = Counter()
        support54_power_union = 0
        for sample in range(args.samples):
            span = args.log_span * (0.2 + 0.8 * (sample + 1) / args.samples)
            denominators = bridge.sample_denominators_wide(
                rng, positive_heads, span
            )
            matrix, values = evaluation_features(denominators)
            product = np.prod(values, axis=1)
            systems = {
                "support54_free": matrix[sorted(SUPPORT54)],
                "all_pairs_tied": grouped_rows(matrix, False),
                "exception_pairs_split": grouped_rows(matrix, True),
                "cleared_pairs_tied": grouped_rows(matrix, False, product),
                "cleared_exception_split": grouped_rows(matrix, True, product),
                "inverse_pairs_tied": grouped_rows(matrix, False, 1.0 / product),
                "ordinary_pairs_only": ordinary_pair_rows(matrix),
            }
            for name, rows in systems.items():
                found, _, margin = has_positive_dual(rows)
                counts[name] += int(found)
                minimum_margins[name] = min(minimum_margins[name], margin)
            current_power_hit = False
            current_support54_hit = False
            for exponent in args.alpha_grid:
                weights = product_power(values, exponent)
                found, _, _ = has_positive_dual(
                    grouped_rows(matrix, True, weights)
                )
                power_counts[exponent] += int(found)
                current_power_hit = current_power_hit or found
                support_found, _, _ = has_positive_dual(
                    support54_grouped_rows(matrix, weights)
                )
                support54_power_counts[exponent] += int(support_found)
                current_support54_hit = current_support54_hit or support_found
            power_union += int(current_power_hit)
            support54_power_union += int(current_support54_hit)
        print(
            f"orientation={positive_heads} counts={counts} "
            f"minimum_margins={minimum_margins} "
            f"power_union={power_union}/{args.samples} "
            f"power_counts={dict(power_counts)} "
            f"support54_power_union={support54_power_union}/{args.samples} "
            f"support54_power_counts={dict(support54_power_counts)}"
        )


if __name__ == "__main__":
    main()
