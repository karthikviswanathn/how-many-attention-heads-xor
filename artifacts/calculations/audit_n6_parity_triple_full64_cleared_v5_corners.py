#!/usr/bin/env python3
"""Audit literal corners of the full-cube cleared V5 multiplier cone.

Each admissible oriented affine denominator is an interior convex combination
of the constant form 1 and the six literals 1 + sigma z_i.  Up to head
permutation and the target symmetry reversing all orientations, there are
three orientation counts and 3 * 7**4 = 7203 literal-corner dictionaries.

For each dictionary this script maximizes the minimum coordinate of q subject
to G.T q = 0, parity.T q = 0, and sum(q) = 1.  The calculation is a numerical
boundary audit.  It is not, by itself, a proof for interior denominators.
"""

from __future__ import annotations

import itertools
from collections import Counter

import numpy as np
from scipy.optimize import linprog


N = 6
HEADS = 4
VERTICES = 1 << N
MASK = 0x96696BD669B69669
TOLERANCE = 1e-9
EXPECTED_COUNTS = {
    0: (25, 2376),
    1: (115, 2286),
    2: (97, 2304),
}
EXPECTED_RANK_COUNTS = {
    1: 66,
    6: 330,
    7: 150,
    8: 3,
    9: 840,
    11: 1320,
    13: 1434,
    14: 1080,
    16: 540,
    17: 1440,
}
EXPECTED_ZERO_RANK_COUNTS = {
    0: {8: 1, 13: 24},
    1: {8: 1, 13: 42, 14: 72},
    2: {8: 1, 13: 48, 14: 48},
}
EXPECTED_ZERO_TYPE_COUNTS = {
    0: {(0, ()): 1, (1, (1,)): 24},
    1: {
        (0, ()): 1,
        (1, (1,)): 24,
        (2, (2,)): 18,
        (4, (1, 1, 1, 1)): 72,
    },
    2: {
        (0, ()): 1,
        (1, (1,)): 24,
        (2, (2,)): 24,
        (4, (1, 1, 1, 1)): 48,
    },
}


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


Z = np.array(
    [
        [character(1 << coordinate, code) for coordinate in range(N)]
        for code in range(VERTICES)
    ],
    dtype=float,
)
SIGNS = np.array(
    [1.0 if (MASK >> code) & 1 else -1.0 for code in range(VERTICES)]
)
PARITY = np.array(
    [character(VERTICES - 1, code) for code in range(VERTICES)],
    dtype=float,
)


def literal_value(orientation: int, corner: int) -> np.ndarray:
    if corner == 0:
        return np.ones(VERTICES)
    return 1.0 + orientation * Z[:, corner - 1]


def augmented_rows(
    orientations: tuple[int, ...], corners: tuple[int, ...]
) -> np.ndarray:
    values = np.column_stack(
        [
            literal_value(orientation, corner)
            for orientation, corner in zip(orientations, corners)
        ]
    )
    product = np.prod(values, axis=1)
    columns = [SIGNS * product]
    for head in range(HEADS):
        partial = np.prod(
            values[:, [other for other in range(HEADS) if other != head]],
            axis=1,
        )
        columns.extend(
            SIGNS * Z[:, coordinate] * partial
            for coordinate in range(N)
        )
    columns.append(PARITY)
    return np.column_stack(columns)


def strict_margin(rows: np.ndarray) -> float:
    row_count, column_count = rows.shape
    scale = np.maximum(np.linalg.norm(rows, axis=0), 1.0)
    normalized = rows / scale

    equality = np.zeros((column_count + 1, row_count + 1))
    equality[:column_count, :row_count] = normalized.T
    equality[-1, :row_count] = 1.0
    target = np.zeros(column_count + 1)
    target[-1] = 1.0

    inequality = np.zeros((row_count, row_count + 1))
    inequality[:, :row_count] = -np.eye(row_count)
    inequality[:, -1] = 1.0
    objective = np.zeros(row_count + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=inequality,
        b_ub=np.zeros(row_count),
        A_eq=equality,
        b_eq=target,
        bounds=[(None, None)] * (row_count + 1),
        method="highs-ds",
    )
    if not result.success:
        raise RuntimeError(result.message)
    return float(result.x[-1])


def zero_type(corners: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    nonzero = [corner for corner in corners if corner]
    multiplicities = tuple(sorted(Counter(nonzero).values(), reverse=True))
    return len(nonzero), multiplicities


def audit() -> tuple[
    dict[int, tuple[int, int]],
    dict[int, int],
    dict[int, dict[int, int]],
    dict[int, dict[tuple[int, tuple[int, ...]], int]],
    float,
    float,
]:
    counts = {}
    rank_counts: dict[int, int] = {}
    zero_rank_counts = {}
    zero_type_counts = {}
    minimum_positive = float("inf")
    maximum = 0.0
    for positive_count in range(3):
        orientations = (1,) * positive_count + (-1,) * (
            HEADS - positive_count
        )
        zero_count = 0
        positive_count_local = 0
        local_zero_ranks: Counter[int] = Counter()
        local_zero_types: Counter[tuple[int, tuple[int, ...]]] = Counter()
        for corners in itertools.product(range(N + 1), repeat=HEADS):
            rows = augmented_rows(orientations, corners)
            rank = int(np.linalg.matrix_rank(rows, tol=1e-9))
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
            margin = strict_margin(rows)
            assert margin >= -TOLERANCE
            if margin <= TOLERANCE:
                zero_count += 1
                local_zero_ranks[rank] += 1
                local_zero_types[zero_type(corners)] += 1
            else:
                positive_count_local += 1
                minimum_positive = min(minimum_positive, margin)
                maximum = max(maximum, margin)
        counts[positive_count] = (zero_count, positive_count_local)
        zero_rank_counts[positive_count] = dict(local_zero_ranks)
        zero_type_counts[positive_count] = dict(local_zero_types)
    return (
        counts,
        rank_counts,
        zero_rank_counts,
        zero_type_counts,
        minimum_positive,
        maximum,
    )


def main() -> None:
    (
        counts,
        rank_counts,
        zero_rank_counts,
        zero_type_counts,
        minimum_positive,
        maximum,
    ) = audit()
    assert counts == EXPECTED_COUNTS
    assert rank_counts == EXPECTED_RANK_COUNTS
    assert zero_rank_counts == EXPECTED_ZERO_RANK_COUNTS
    assert zero_type_counts == EXPECTED_ZERO_TYPE_COUNTS
    assert abs(minimum_positive - 0.01) < 1e-10
    assert abs(maximum - 1.0 / 64.0) < 1e-10
    for orientation_count, (zero_count, positive_count) in counts.items():
        print(
            f"orientation count {orientation_count}: "
            f"zero={zero_count}, positive={positive_count}"
        )
        print(f"  zero ranks: {zero_rank_counts[orientation_count]}")
        print(f"  zero types: {zero_type_counts[orientation_count]}")
    print(f"rank counts: {rank_counts}")
    print(f"smallest positive margin: {minimum_positive:.12g}")
    print(f"largest margin: {maximum:.12g}")
    print("audited all 7203 literal corners")


if __name__ == "__main__":
    main()
