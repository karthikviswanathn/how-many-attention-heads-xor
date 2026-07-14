#!/usr/bin/env python3
"""Extract complementarity data on support54 denominator boundaries.

Every positive affine denominator is written, up to positive scale, as

    B(z) = slack + sum_i slope_i (1 + orientation * z_i).

The admissible region has positive slack and nonnegative slopes.  This
diagnostic sends selected slacks to zero, computes the cleared 54 by 25
tangent matrix W, and applies both sides of Stiemke's alternative.  When a
boundary separator exists, it reports its nonzero zero set and tests whether
that set carries a complementary positive circuit.

All floating-point output is diagnostic.  It is intended to identify stable
supports for later exact reconstruction.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import itertools
import math

import numpy as np
from scipy.optimize import linprog

import verify_n6_parity_triple_support54_geometry as geometry


N = 6
HEADS = 4
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
SUPPORT54 = tuple(
    code for code in range(1 << N)
    if code not in geometry.EXPECTED_OMITTED
)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def denominators_from_parameters(
    orientations: tuple[int, ...],
    slacks: np.ndarray,
    slopes: np.ndarray,
) -> np.ndarray:
    rows = []
    for head in range(HEADS):
        rows.append(
            np.concatenate(
                [
                    [float(slacks[head] + np.sum(slopes[head]))],
                    orientations[head] * slopes[head],
                ]
            )
        )
    return np.vstack(rows)


def cleared_matrix(denominators: np.ndarray) -> np.ndarray:
    values = np.array(
        [
            [
                denominators[head, 0]
                + sum(
                    denominators[head, coordinate + 1]
                    * character(1 << coordinate, code)
                    for coordinate in range(N)
                )
                for head in range(HEADS)
            ]
            for code in SUPPORT54
        ],
        dtype=float,
    )
    product = np.prod(values, axis=1)
    rows = []
    for row, code in enumerate(SUPPORT54):
        sign = target_sign(code)
        entries = [sign * product[row]]
        for head in range(HEADS):
            partial = math.prod(
                values[row, other]
                for other in range(HEADS)
                if other != head
            )
            entries.extend(
                sign * character(1 << coordinate, code) * partial
                for coordinate in range(N)
            )
        rows.append(entries)
    return np.array(rows, dtype=float)


def normalized_nonzero_rows(
    matrix: np.ndarray,
) -> tuple[np.ndarray, tuple[int, ...], tuple[int, ...]]:
    row_norms = np.linalg.norm(matrix, axis=1)
    scale = max(float(np.max(row_norms)), 1.0)
    zero_indices = tuple(
        index for index, norm in enumerate(row_norms) if norm <= 1e-13 * scale
    )
    nonzero_indices = tuple(
        index for index in range(len(row_norms)) if index not in zero_indices
    )
    normalized = matrix[list(nonzero_indices)] / row_norms[
        list(nonzero_indices), None
    ]
    column_norms = np.linalg.norm(normalized, axis=0)
    column_norms = np.maximum(column_norms, 1e-14)
    return normalized / column_norms[None, :], nonzero_indices, zero_indices


def positive_kernel(
    matrix: np.ndarray,
) -> tuple[bool, tuple[int, ...], np.ndarray | None]:
    row_count = matrix.shape[0]
    equalities = np.vstack([matrix.T, np.ones((1, row_count))])
    target = np.zeros(equalities.shape[0])
    target[-1] = 1.0
    rng = np.random.default_rng(938475)
    result = linprog(
        rng.normal(size=row_count),
        A_eq=equalities,
        b_eq=target,
        bounds=[(0.0, None)] * row_count,
        method="highs-ds",
    )
    if not result.success:
        return False, (), None
    weights = np.maximum(np.array(result.x, dtype=float), 0.0)
    threshold = 1e-9 * max(float(np.max(weights)), 1.0)
    support = tuple(np.flatnonzero(weights > threshold).tolist())
    return True, support, weights


def separator(
    matrix: np.ndarray,
) -> tuple[bool, np.ndarray | None, np.ndarray | None]:
    """Find x with W x >= 0 and sum(W x)=1, if one exists."""
    column_sum = np.sum(matrix, axis=0)
    result = linprog(
        np.zeros(matrix.shape[1]),
        A_ub=-matrix,
        b_ub=np.zeros(matrix.shape[0]),
        A_eq=column_sum[None, :],
        b_eq=np.ones(1),
        bounds=[(None, None)] * matrix.shape[1],
        method="highs-ds",
    )
    if not result.success:
        return False, None, None
    vector = np.array(result.x, dtype=float)
    values = matrix @ vector
    scale = max(float(np.max(np.abs(values))), 1.0)
    values[np.abs(values) <= 2e-8 * scale] = 0.0
    if float(np.min(values)) < -2e-7 * scale:
        return False, None, None
    return True, vector, values


def complementary_kernel(
    matrix: np.ndarray, zero_set: tuple[int, ...]
) -> tuple[bool, tuple[int, ...], int]:
    if not zero_set:
        return False, (), 0
    restricted = matrix[list(zero_set)]
    rank = int(np.linalg.matrix_rank(restricted, tol=1e-9))
    found, local_support, _ = positive_kernel(restricted)
    if not found:
        return False, (), rank
    return True, tuple(zero_set[index] for index in local_support), rank


def sample_slopes(
    rng: np.random.Generator, sample: int, log_span: float
) -> np.ndarray:
    if sample == 0:
        return np.ones((HEADS, N), dtype=float)
    return np.exp(rng.uniform(-log_span, log_span, size=(HEADS, N)))


def orientation_tuple(positive_heads: int) -> tuple[int, ...]:
    return tuple([-1] * (HEADS - positive_heads) + [1] * positive_heads)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=20)
    parser.add_argument("--log-span", type=float, default=8.0)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--positive-heads", type=int, choices=range(3))
    parser.add_argument("--boundary-size", type=int, choices=range(1, 5))
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    orientation_counts = (
        range(3) if args.positive_heads is None else (args.positive_heads,)
    )
    boundary_masks = tuple(
        mask
        for mask in range(1, 1 << HEADS)
        if args.boundary_size is None
        or bin(mask).count("1") == args.boundary_size
    )

    for positive_heads in orientation_counts:
        orientations = orientation_tuple(positive_heads)
        statistics: Counter[tuple[int, int, bool, int]] = Counter()
        zero_sets: defaultdict[tuple[int, ...], int] = defaultdict(int)
        records = []
        for sample in range(args.samples):
            slopes = sample_slopes(rng, sample, args.log_span)
            for boundary_mask in boundary_masks:
                slacks = np.ones(HEADS, dtype=float)
                for head in range(HEADS):
                    if boundary_mask & (1 << head):
                        slacks[head] = 0.0
                denominators = denominators_from_parameters(
                    orientations, slacks, slopes
                )
                raw = cleared_matrix(denominators)
                matrix, row_indices, vanished = normalized_nonzero_rows(raw)
                kernel_found, circuit, _ = positive_kernel(matrix)
                separator_found, _, values = separator(matrix)
                nonzero_zero_set: tuple[int, ...] = ()
                complementary_found = False
                complementary_support: tuple[int, ...] = ()
                zero_rank = 0
                if separator_found:
                    assert values is not None
                    local_zero_set = tuple(
                        index for index, value in enumerate(values) if value == 0
                    )
                    nonzero_zero_set = tuple(
                        SUPPORT54[row_indices[index]] for index in local_zero_set
                    )
                    (
                        complementary_found,
                        local_complementary_support,
                        zero_rank,
                    ) = complementary_kernel(matrix, local_zero_set)
                    complementary_support = tuple(
                        SUPPORT54[row_indices[index]]
                        for index in local_complementary_support
                    )
                    zero_sets[nonzero_zero_set] += 1
                statistics[
                    (
                        len(vanished),
                        len(circuit),
                        separator_found,
                        zero_rank,
                    )
                ] += 1
                if separator_found:
                    records.append(
                        (
                            len(vanished),
                            -zero_rank,
                            len(nonzero_zero_set),
                            sample,
                            boundary_mask,
                            tuple(SUPPORT54[index] for index in vanished),
                            nonzero_zero_set,
                            complementary_found,
                            complementary_support,
                            kernel_found,
                        )
                    )

        print(
            f"orientation={positive_heads} cases={args.samples * len(boundary_masks)} "
            f"statistics={dict(statistics)}"
        )
        print(
            "  recurring_zero_sets=",
            sorted(
                ((count, zero_set) for zero_set, count in zero_sets.items()),
                reverse=True,
            )[:10],
        )
        records.sort()
        for record in records[:20]:
            (
                vanished_count,
                negative_rank,
                zero_count,
                sample,
                boundary_mask,
                vanished,
                zero_set,
                complementary_found,
                complementary_support,
                kernel_found,
            ) = record
            print(
                f"  sample={sample} boundary={boundary_mask:04b} "
                f"vanished={vanished_count}:{vanished} "
                f"kernel={kernel_found} zeros={zero_count} "
                f"rank={-negative_rank} set={zero_set} "
                f"complementary={complementary_found}:{complementary_support}"
            )


if __name__ == "__main__":
    main()
