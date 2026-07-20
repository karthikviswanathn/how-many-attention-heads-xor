#!/usr/bin/env python3
"""Screen the cycle-adapted two-scale Schur criterion.

For a fixed coefficient table, both the positive-orientation and
negative-orientation versions reduce to linear programs in three shape
variables and a strict-margin variable.  A success is a valid numerical
witness for the sufficient criterion.  A failure is not an obstruction to
two heads.

The representative-level experiment samples other quadratic representatives
inside the same strict sign cell and the same complementary-cycle coefficient
orthant.  Its output is search evidence, not a universal proof.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import linprog


INPUT_BITS = 5
VERTICES = (
    (np.arange(1 << INPUT_BITS)[:, None] >> np.arange(INPUT_BITS)) & 1
).astype(float)
SIGN_VERTICES = 2 * VERTICES - 1
EDGES = tuple(itertools.combinations(range(INPUT_BITS), 2))
CYCLE_EDGES = frozenset(
    {
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (0, 4),
    }
)
EDGE_SIGNS = np.array(
    [1 if edge in CYCLE_EDGES else -1 for edge in EDGES], dtype=float
)
FOURIER_SUBSETS = (
    ((),)
    + tuple((index,) for index in range(INPUT_BITS))
    + EDGES
)
FOURIER = np.column_stack(
    [
        np.prod(SIGN_VERTICES[:, subset], axis=1)
        if subset
        else np.ones(1 << INPUT_BITS)
        for subset in FOURIER_SUBSETS
    ]
)
EDGE_SELECTOR = np.zeros((len(EDGES), len(FOURIER_SUBSETS)))
EDGE_SELECTOR[np.arange(len(EDGES)), np.arange(6, 16)] = EDGE_SIGNS


def coefficient_matrix(coefficients: np.ndarray) -> dict[tuple[int, int], float]:
    matrix = {
        (-1, index): float(coefficients[1 + index]) / 2
        for index in range(INPUT_BITS)
    }
    matrix.update(
        {
            edge: float(value) / 2
            for edge, value in zip(EDGES, coefficients[6:])
        }
    )
    return matrix


def entry(
    matrix: dict[tuple[int, int], float], first: int, second: int
) -> float:
    if first == -1:
        return matrix[(-1, second)]
    return matrix[tuple(sorted((first, second)))]


def criterion_witness(
    coefficients: np.ndarray,
) -> dict[str, object] | None:
    """Return the strongest LP witness among all index and orientation choices."""
    matrix = coefficient_matrix(coefficients)
    best = None
    for negative_orientation in (False, True):
        for pivot in range(INPUT_BITS):
            remaining = [index for index in range(INPUT_BITS) if index != pivot]
            for outside_p, outside_q in itertools.combinations(remaining, 2):
                large = [
                    index
                    for index in remaining
                    if index not in (outside_p, outside_q)
                ]
                for large_a, large_b in (large, large[::-1]):
                    alpha = entry(matrix, outside_p, outside_q)
                    pivot_p = entry(matrix, pivot, outside_p)
                    pivot_q = entry(matrix, pivot, outside_q)
                    if abs(alpha * pivot_p * pivot_q) < 1e-14:
                        continue
                    sigma = np.sign(alpha * pivot_p * pivot_q)
                    shape_sign = 1 if negative_orientation else -1
                    triples = []
                    for target in (pivot, outside_p, outside_q):
                        triples.append(
                            (
                                sigma * entry(matrix, -1, target),
                                sigma
                                * shape_sign
                                * entry(matrix, large_a, target),
                                sigma
                                * shape_sign
                                * entry(matrix, large_b, target),
                            )
                        )
                    h_value, p_value, q_value = triples
                    alpha_over_pivot_q = alpha / pivot_q
                    alpha_over_pivot_p = alpha / pivot_p

                    # Variables are R, S, Z, epsilon.  The first three
                    # inequalities impose 0 < R < 1 < S with margin epsilon.
                    greater_equal = [
                        ([1, 0, 0, -1], 0),
                        ([-1, 0, 0, -1], -1),
                        ([0, 1, 0, -1], 1),
                    ]
                    if not negative_orientation:
                        # Z + H > 0, P + (alpha / s_k) Z > 0,
                        # Q + (alpha / r_k) Z > 0.
                        greater_equal.extend(
                            [
                                (
                                    [h_value[1], h_value[2], 1, -1],
                                    -h_value[0],
                                ),
                                (
                                    [
                                        p_value[1],
                                        p_value[2],
                                        alpha_over_pivot_q,
                                        -1,
                                    ],
                                    -p_value[0],
                                ),
                                (
                                    [
                                        q_value[1],
                                        q_value[2],
                                        alpha_over_pivot_p,
                                        -1,
                                    ],
                                    -q_value[0],
                                ),
                            ]
                        )
                    else:
                        # Z - H > 0, (alpha / s_k) Z - P > 0,
                        # (alpha / r_k) Z - Q > 0.
                        greater_equal.extend(
                            [
                                (
                                    [-h_value[1], -h_value[2], 1, -1],
                                    h_value[0],
                                ),
                                (
                                    [
                                        -p_value[1],
                                        -p_value[2],
                                        alpha_over_pivot_q,
                                        -1,
                                    ],
                                    p_value[0],
                                ),
                                (
                                    [
                                        -q_value[1],
                                        -q_value[2],
                                        alpha_over_pivot_p,
                                        -1,
                                    ],
                                    q_value[0],
                                ),
                            ]
                        )

                    result = linprog(
                        np.array([0.0, 0.0, 0.0, -1.0]),
                        A_ub=-np.array(
                            [row for row, _ in greater_equal], dtype=float
                        ),
                        b_ub=-np.array(
                            [bound for _, bound in greater_equal], dtype=float
                        ),
                        bounds=[
                            (0.0, 1.0),
                            (1.0, None),
                            (None, None),
                            (0.0, 1.0),
                        ],
                        method="highs",
                    )
                    if not result.success or result.x[3] <= 1e-8:
                        continue
                    record = {
                        "margin": float(result.x[3]),
                        "negative_orientation": negative_orientation,
                        "pivot": pivot,
                        "outside": [outside_p, outside_q],
                        "large": [large_a, large_b],
                        "R": float(result.x[0]),
                        "S": float(result.x[1]),
                        "Z": float(result.x[2]),
                    }
                    if best is None or record["margin"] > best["margin"]:
                        best = record
    return best


def alternative_representative(
    target_signs: np.ndarray,
    rng: np.random.Generator,
    trials: int,
) -> tuple[np.ndarray, dict[str, object]] | None:
    constraints = np.vstack(
        [
            -(target_signs[:, None] * FOURIER),
            -EDGE_SELECTOR,
        ]
    )
    bounds = np.concatenate(
        [
            -np.ones(1 << INPUT_BITS),
            -0.05 * np.ones(len(EDGES)),
        ]
    )
    for _ in range(trials):
        objective = rng.normal(size=len(FOURIER_SUBSETS))
        for direction in (objective, -objective):
            result = linprog(
                direction,
                A_ub=constraints,
                b_ub=bounds,
                bounds=[(-2000.0, 2000.0)] * len(FOURIER_SUBSETS),
                method="highs",
            )
            if not result.success:
                continue
            witness = criterion_witness(result.x)
            if witness is not None:
                return result.x, witness
    return None


def canonical_coefficients() -> np.ndarray:
    return np.array(
        [-4, -1, -1, -1, -1, -1]
        + [1 if edge in CYCLE_EDGES else -1 for edge in EDGES],
        dtype=float,
    )


def canonical_boundary_coefficients() -> np.ndarray:
    affine = np.column_stack([np.ones(1 << INPUT_BITS), VERTICES])
    first_numerator = np.array([-1, -29, -51, 57, -24, -29])
    free_factor = np.array([-1, -2, 2, 2, 1, 0])
    second_numerator = np.array([-34, -57, 51, -24, 32, 3])
    boundary_factor = np.array([0, 1, 1, 1, 1, 1])
    values = (affine @ first_numerator) * (affine @ free_factor) + (
        affine @ second_numerator
    ) * (affine @ boundary_factor)
    return FOURIER.T @ values / (1 << INPUT_BITS)


def locked_cell_coefficients() -> np.ndarray:
    return np.array(
        [
            988,
            -12,
            -979,
            997,
            -15,
            -15,
            6,
            -1003,
            -6,
            1009,
            497,
            -973,
            -491,
            500,
            -997,
            488,
        ],
        dtype=float,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--representatives", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260714)
    arguments = parser.parse_args()

    rng = np.random.default_rng(arguments.seed)
    named = (
        ("canonical symmetric", canonical_coefficients()),
        ("canonical boundary", canonical_boundary_coefficients()),
        ("locked cell", locked_cell_coefficients()),
    )
    for name, coefficients in named:
        direct = criterion_witness(coefficients)
        target_signs = np.sign(FOURIER @ coefficients)
        alternative = alternative_representative(
            target_signs, rng, arguments.representatives
        )
        print(
            f"{name}: direct={direct is not None}, "
            f"alternative={alternative is not None}"
        )

    direct_count = 0
    rescued_count = 0
    unresolved_masks = []
    for _ in range(arguments.samples):
        coefficients = rng.normal(size=len(FOURIER_SUBSETS))
        coefficients[6:] = EDGE_SIGNS * np.exp(rng.uniform(-5, 5, len(EDGES)))
        values = FOURIER @ coefficients
        if np.min(np.abs(values)) < 1e-8:
            continue
        if criterion_witness(coefficients) is not None:
            direct_count += 1
            continue
        alternative = alternative_representative(
            np.sign(values), rng, arguments.representatives
        )
        if alternative is not None:
            rescued_count += 1
            continue
        mask = sum(
            (int(value) > 0) << vertex for vertex, value in enumerate(values)
        )
        unresolved_masks.append(f"0x{mask:08x}")

    print(
        f"random C5 tables: direct={direct_count}, rescued={rescued_count}, "
        f"unresolved={len(unresolved_masks)}"
    )
    if unresolved_masks:
        print("unresolved masks:", ", ".join(unresolved_masks))
    print("warning: an unresolved sample is only a search failure")


if __name__ == "__main__":
    main()
