#!/usr/bin/env python3
"""Verify an exact two-head certificate for a C5-locked five-bit cell.

The mask below has threshold degree exactly two.  More strongly, ten exact
dual identities force every strict quadratic sign representative to have the
same complementary-five-cycle signs on its ten quadratic Fourier
coefficients.  The final checks show that this sign cell nevertheless has an
exact two-head representation.
"""

from __future__ import annotations

from itertools import combinations
from fractions import Fraction

import numpy as np


INPUT_BITS = 5
TRUTH_MASK = 0x7B9AF0D7


def cube() -> np.ndarray:
    return ((np.arange(1 << INPUT_BITS)[:, None] >> np.arange(INPUT_BITS)) & 1).astype(
        object
    )


def signs() -> np.ndarray:
    return np.array(
        [1 if (TRUTH_MASK >> vertex) & 1 else -1 for vertex in range(1 << INPUT_BITS)],
        dtype=object,
    )


def affine_matrix() -> np.ndarray:
    return np.column_stack(
        [np.ones(1 << INPUT_BITS, dtype=object), cube()]
    ).astype(object)


FOURIER_SUBSETS = (
    ((),)
    + tuple((index,) for index in range(INPUT_BITS))
    + tuple(combinations(range(INPUT_BITS), 2))
)


def fourier_matrix() -> np.ndarray:
    sign_inputs = 2 * cube() - 1
    columns = []
    for subset in FOURIER_SUBSETS:
        if subset:
            columns.append(np.prod(sign_inputs[:, subset], axis=1))
        else:
            columns.append(np.ones(1 << INPUT_BITS, dtype=object))
    return np.column_stack(columns).astype(object)


# Coefficients are in the Fourier basis ordered by FOURIER_SUBSETS.  They are
# six times a smaller rational solution, solely to keep the verifier integral.
QUADRATIC_COEFFICIENTS = (
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
)


CYCLE_EDGES = frozenset(
    {
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (0, 4),
    }
)


# Each entry gives a nonnegative weight vector through its sparse support.
# Its signed Fourier moment is zero in every coordinate except the named edge,
# where it has the listed value.  The signs are the C5 coloring.
EDGE_DUALS = {
    (0, 1): ({20: 1, 21: 1, 22: 1, 23: 1}, 4),
    (0, 2): ({26: 1, 27: 1, 30: 1, 31: 1}, -4),
    (0, 3): ({22: 1, 23: 1, 30: 1, 31: 1}, -4),
    (0, 4): ({2: 1, 3: 1, 4: 1, 5: 1, 16: 1, 17: 1, 22: 1, 23: 1}, 8),
    (1, 2): (
        {
            1: 2,
            2: 1,
            3: 2,
            5: 1,
            8: 1,
            15: 1,
            18: 1,
            21: 1,
            23: 2,
            24: 1,
            31: 1,
        },
        8,
    ),
    (1, 3): ({2: 1, 5: 1, 10: 1, 13: 1, 16: 1, 23: 1, 24: 1, 31: 1}, -8),
    (1, 4): (
        {
            1: 1,
            2: 1,
            3: 1,
            5: 1,
            8: 1,
            15: 1,
            16: 1,
            20: 1,
            22: 1,
            23: 1,
            24: 1,
            31: 1,
        },
        -4,
    ),
    (2, 3): ({1: 1, 5: 1, 9: 1, 13: 1}, 4),
    (2, 4): ({3: 1, 7: 1, 9: 1, 13: 1, 17: 1, 21: 1, 27: 1, 31: 1}, -8),
    (3, 4): ({0: 1, 8: 1, 16: 1, 24: 1}, 4),
}


# Q = A D + C B is the one-admissible-factor form returned by the search.
ORIENTED_FACTOR = (15, -10, -1, -1, -1, -1)
FREE_FACTOR = (-5, 8, -5, -2, -6, 10)
FIRST_NUMERATOR = (-10841, 9502, 1103, -5699, 4965, 5363)
SECOND_NUMERATOR = (-2658, 3495, -4285, 648, -1971, 4603)
ADMISSIBLE_SHIFT = 11


def verify_threshold_degree_and_locked_cycle() -> None:
    target_signs = signs()
    fourier = fourier_matrix()
    coefficients = np.array(QUADRATIC_COEFFICIENTS, dtype=object)
    signed_values = target_signs * (fourier @ coefficients)
    assert min(signed_values) == 6

    edges = tuple(combinations(range(INPUT_BITS), 2))
    edge_indices = {edge: FOURIER_SUBSETS.index(edge) for edge in edges}
    for edge, (sparse_weights, expected_moment) in EDGE_DUALS.items():
        weights = np.zeros(1 << INPUT_BITS, dtype=object)
        for vertex, weight in sparse_weights.items():
            assert weight > 0
            weights[vertex] = weight
        moments = fourier.T @ (target_signs * weights)
        expected = np.zeros(len(FOURIER_SUBSETS), dtype=object)
        expected[edge_indices[edge]] = expected_moment
        assert np.array_equal(moments, expected)
        expected_sign = 1 if edge in CYCLE_EDGES else -1
        assert expected_moment * expected_sign > 0

    # Any one edge dual already annihilates all affine features and is a
    # positive Gordan obstruction to threshold degree one.
    first_weights = np.zeros(1 << INPUT_BITS, dtype=object)
    for vertex, weight in EDGE_DUALS[(0, 1)][0].items():
        first_weights[vertex] = weight
    assert np.all(fourier[:, : INPUT_BITS + 1].T @ (target_signs * first_weights) == 0)


def verify_exact_two_head_certificate() -> None:
    target_signs = signs()
    affine = affine_matrix()
    oriented = np.array(ORIENTED_FACTOR, dtype=object)
    free = np.array(FREE_FACTOR, dtype=object)
    first = np.array(FIRST_NUMERATOR, dtype=object)
    second = np.array(SECOND_NUMERATOR, dtype=object)

    score = (affine @ first) * (affine @ free) + (affine @ second) * (
        affine @ oriented
    )
    assert min(target_signs * score) == 156

    shifted = free + ADMISSIBLE_SHIFT * oriented
    shifted_second = second - ADMISSIBLE_SHIFT * first
    shifted_score = (affine @ first) * (affine @ shifted) + (
        affine @ shifted_second
    ) * (affine @ oriented)
    assert np.array_equal(score, shifted_score)

    assert tuple(int(value) for value in shifted) == (160, -102, -16, -13, -17, -1)
    assert tuple(int(value) for value in shifted_second) == (
        116593,
        -101027,
        -16418,
        63337,
        -56586,
        -54390,
    )
    for denominator in (oriented, shifted):
        assert all(slope < 0 for slope in denominator[1:])
        assert min(affine @ denominator) > 0

    # The exact H2 score itself lies in the locked C5 coefficient orthant.
    fourier_coefficients = np.array(
        [sum(score * fourier_matrix()[:, column]) // (1 << INPUT_BITS) for column in range(16)],
        dtype=object,
    )
    for edge in combinations(range(INPUT_BITS), 2):
        expected_sign = 1 if edge in CYCLE_EDGES else -1
        assert expected_sign * fourier_coefficients[FOURIER_SUBSETS.index(edge)] > 0


def verify_two_scale_schur_inequalities() -> None:
    """Check the rational data used in the cycle-adapted Schur lemma."""
    coefficients = {
        subset: Fraction(value, 1)
        for subset, value in zip(FOURIER_SUBSETS, QUADRATIC_COEFFICIENTS)
    }

    def matrix_entry(first: int | None, second: int) -> Fraction:
        if first is None:
            return coefficients[(second,)] / 2
        return coefficients[tuple(sorted((first, second)))] / 2

    pivot = 0
    outside_p = 1
    outside_q = 2
    large_a = 3
    large_b = 4
    shape_a = Fraction(1, 10)
    shape_b = Fraction(6, 5)
    delta = Fraction(4, 13)
    slope_a = delta * shape_a
    slope_b = (1 - delta) * shape_b
    assert delta * shape_a**2 + (1 - delta) * shape_b**2 == 1
    assert slope_a == Fraction(2, 65)
    assert slope_b == Fraction(54, 65)
    assert slope_a + slope_b < 1

    alpha = matrix_entry(outside_p, outside_q)
    pivot_p = matrix_entry(pivot, outside_p)
    pivot_q = matrix_entry(pivot, outside_q)
    sigma = -1
    assert alpha * pivot_p * pivot_q < 0

    inverse_shape = (
        Fraction(sigma),
        -Fraction(sigma) * shape_a,
        -Fraction(sigma) * shape_b,
    )

    def large_dot(target: int) -> Fraction:
        entries = (
            matrix_entry(None, target),
            matrix_entry(large_a, target),
            matrix_entry(large_b, target),
        )
        return sum(value * entry for value, entry in zip(inverse_shape, entries))

    h_value = large_dot(pivot)
    p_value = large_dot(outside_p)
    q_value = large_dot(outside_q)
    assert h_value == Fraction(6111, 10)
    assert p_value == Fraction(585, 4)
    assert q_value == Fraction(-10717, 10)
    assert alpha / pivot_q == Fraction(-497, 1003)
    assert alpha / pivot_p == Fraction(497, 6)

    shifted_pivot = Fraction(3062379, 19880)
    pivot_component = shifted_pivot + h_value
    outside_p_limit = p_value + (alpha / pivot_q) * shifted_pivot
    outside_q_limit = q_value + (alpha / pivot_p) * shifted_pivot
    assert pivot_component == Fraction(15211047, 19880)
    assert outside_p_limit == Fraction(2805171, 40120)
    assert outside_q_limit == Fraction(935057, 80)
    assert min(pivot_component, outside_p_limit, outside_q_limit) > 0


def main() -> None:
    verify_threshold_degree_and_locked_cycle()
    verify_exact_two_head_certificate()
    verify_two_scale_schur_inequalities()
    print("C5-locked five-bit cell: exact degree-two and two-head certificates verified")


if __name__ == "__main__":
    main()
