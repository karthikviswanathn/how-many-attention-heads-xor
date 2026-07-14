#!/usr/bin/env python3
"""Verify the exact refutation of a natural six-bit gated candidate.

Let g be five-bit even parity with the vertex 00011 flipped, and set
F(x, y) = y AND g(x).  The one-bit gate theorem and restriction give
deg_pm(F) = 4.  This file checks an exact four-head representation, proving
H*(F) = deg_pm(F) = 4.
"""

from __future__ import annotations

import itertools

import numpy as np

from search_gated_single_flip import cleared_matrix, target_signs


DENOMINATORS = np.array(
    (
        (1003, -1, -6, -41, -952, -1, -1),
        (1002, -45, -1, -320, -215, -419, -1),
        (1003, -108, -1, -131, -112, -1, -649),
        (1003, -361, -634, -1, -1, -1, -1),
    ),
    dtype=object,
)


SCORE = np.array(
    (
        -2032686498817331,
        310360979757723008,
        1625798376317441,
        -13937478273641204,
        -20459418183163960,
        -310363272296784128,
        20595696603942008,
        24881321328574072,
        -185337283762376128,
        342727905093201472,
        -174768697973286080,
        -265749719158457408,
        -367989436628042048,
        367976416218402496,
        417845092150866432,
        368077591314396352,
        -312480445837363584,
        131093385585643680,
        -225018222712969888,
        -193246102323336416,
        -317887707248612352,
        368083196727720896,
        -669998025412958848,
        212081401776991168,
        318551468140794112,
        75716504928716992,
        77920879547851072,
        74426666803079680,
        55312440097606112,
    ),
    dtype=object,
)


def base_point(code: int) -> tuple[int, ...]:
    return tuple((code >> coordinate) & 1 for coordinate in range(5))


def sign_point(code: int) -> tuple[int, ...]:
    return tuple(1 - 2 * bit for bit in base_point(code))


def parity_sign(code: int) -> int:
    answer = 1
    for value in sign_point(code):
        answer *= value
    return answer


def base_sign(code: int) -> int:
    value = parity_sign(code)
    return -value if code == 3 else value


def degree_four_value(code: int) -> int:
    z = sign_point(code)
    v = sign_point(3)
    chi_z = parity_sign(code)
    chi_v = parity_sign(3)
    product = 1
    for current, exceptional in zip(z, v):
        product *= 1 + exceptional * current
    return chi_z - chi_v * product


def character(code: int, subset: tuple[int, ...]) -> int:
    answer = 1
    z = sign_point(code)
    for coordinate in subset:
        answer *= z[coordinate]
    return answer


def main() -> None:
    base_signs = np.array([base_sign(code) for code in range(32)])
    base_values = np.array(
        [degree_four_value(code) for code in range(32)], dtype=object
    )
    assert np.all(base_signs.astype(object) * base_values > 0)
    v = base_point(3)
    dual_weights = []
    for code in range(32):
        if code == 3:
            dual_weights.append(1)
        else:
            distance = sum(
                first != second
                for first, second in zip(base_point(code), v)
            )
            dual_weights.append(2 * distance - 1)
    for degree in range(4):
        for subset in itertools.combinations(range(5), degree):
            moment = sum(
                dual_weights[code]
                * base_sign(code)
                * character(code, subset)
                for code in range(32)
            )
            assert moment == 0

    bound = 1 + max(abs(int(value)) for value in base_values)
    gated_signs = target_signs(5, 3, "and").astype(object)
    gated_degree_values = np.concatenate(
        [base_values - bound, base_values]
    )
    assert np.all(gated_signs * gated_degree_values > 0)
    assert np.array_equal(base_signs.astype(object), gated_signs[32:])

    assert DENOMINATORS.shape == (4, 7)
    assert len(SCORE) == 1 + 4 * 7
    for denominator in DENOMINATORS:
        assert all(int(value) < 0 for value in denominator[1:])
    affine = np.column_stack(
        [
            np.ones(64, dtype=object),
            (
                (np.arange(64)[:, None] >> np.arange(6)) & 1
            ).astype(object),
        ]
    )
    assert np.min(affine @ DENOMINATORS.T) > 0

    matrix = cleared_matrix(6, DENOMINATORS)
    signed_scores = gated_signs * (matrix @ SCORE)
    minimum = min(int(value) for value in signed_scores)
    assert minimum == 1015078170392

    print("input bits: 6")
    print("threshold degree: 4")
    print("heads: 4")
    print(f"minimum signed cleared score: {minimum}")
    print("certificate: verified")


if __name__ == "__main__":
    main()
