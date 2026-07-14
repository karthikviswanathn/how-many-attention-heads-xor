#!/usr/bin/env python3
"""Audit common full-cube cleared V5 kernels on literal-simplex edges.

The cleared tangent matrix is affine in one denominator when the other three
are fixed.  A multiplier common to both endpoints of a literal-simplex edge
therefore annihilates every denominator on that edge.  Head permutations
within one orientation class reduce the audit to five classes and 36015
inequivalent edges.

This script uses floating-point linear programming.  It is a reproducible
boundary diagnostic, not an exact proof for all interior dictionaries.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import linprog

import audit_n6_parity_triple_full64_cleared_v5_corners as corners


TOLERANCE = 1e-9
EDGE_CLASSES = (
    (0, 0),
    (1, 0),
    (1, 1),
    (2, 0),
    (2, 2),
)
EXPECTED_COUNTS = {
    (0, 0): (813, 6390),
    (1, 0): (1011, 6192),
    (1, 1): (1053, 6150),
    (2, 0): (1047, 6156),
    (2, 2): (1047, 6156),
}


def common_margin(left: np.ndarray, right: np.ndarray) -> float:
    stacked = np.column_stack((left, right))
    _, indices = np.unique(stacked, axis=1, return_index=True)
    stacked = stacked[:, np.sort(indices)]
    scale = np.maximum(np.linalg.norm(stacked, axis=0), 1.0)
    normalized = stacked / scale
    row_count, column_count = normalized.shape

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


def audit_class(
    orientation_count: int, changed_head: int
) -> tuple[int, int, float, float]:
    orientations = (1,) * orientation_count + (-1,) * (
        corners.HEADS - orientation_count
    )
    zero_count = 0
    positive_count = 0
    minimum_positive = float("inf")
    maximum = 0.0
    for fixed in itertools.product(
        range(corners.N + 1), repeat=corners.HEADS - 1
    ):
        current = [0] * corners.HEADS
        fixed_index = 0
        for head in range(corners.HEADS):
            if head != changed_head:
                current[head] = fixed[fixed_index]
                fixed_index += 1
        for left_corner in range(corners.N + 1):
            current[changed_head] = left_corner
            left = corners.augmented_rows(orientations, tuple(current))
            for right_corner in range(left_corner + 1, corners.N + 1):
                current[changed_head] = right_corner
                right = corners.augmented_rows(orientations, tuple(current))
                margin = common_margin(left, right)
                assert margin >= -TOLERANCE
                if margin <= TOLERANCE:
                    zero_count += 1
                else:
                    positive_count += 1
                    minimum_positive = min(minimum_positive, margin)
                    maximum = max(maximum, margin)
            current[changed_head] = left_corner
    return zero_count, positive_count, minimum_positive, maximum


def main() -> None:
    total_zero = 0
    total_positive = 0
    for edge_class in EDGE_CLASSES:
        result = audit_class(*edge_class)
        assert result[:2] == EXPECTED_COUNTS[edge_class]
        total_zero += result[0]
        total_positive += result[1]
        print(
            f"class {edge_class}: zero={result[0]}, "
            f"positive={result[1]}, min-positive={result[2]:.12g}, "
            f"max={result[3]:.12g}"
        )
    assert (total_zero, total_positive) == (4971, 31044)
    print(
        f"audited 36015 inequivalent edges: "
        f"zero={total_zero}, positive={total_positive}"
    )


if __name__ == "__main__":
    main()
