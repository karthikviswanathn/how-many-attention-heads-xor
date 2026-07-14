#!/usr/bin/env python3
"""Verify the exact refutation of a formerly hard six-bit H3 candidate.

The displayed cubic and positive Gordan circuit prove threshold degree three.
An exact integer three-head certificate proves that the candidate is not a
strict separation.
"""

from __future__ import annotations

import itertools

import numpy as np


INPUT_BITS = 6
TRUTH_MASK = 0x20411408412A1432

# Monomial order: degree first, then lexicographic combinations of 0-based
# variable indices, exactly as produced by itertools.combinations.
CUBIC_COEFFICIENTS = (
    -61,
    82,
    -79,
    82,
    39,
    39,
    39,
    36,
    -82,
    -122,
    12,
    -122,
    -86,
    122,
    32,
    79,
    -39,
    -122,
    -122,
    4,
    -39,
    4,
    -172,
    -172,
    -41,
    47,
    20,
    106,
    20,
    -16,
    161,
    -16,
    0,
    172,
    0,
    -118,
    -79,
    -75,
    36,
    122,
    118,
    -122,
)

QUADRATIC_CIRCUIT_SUPPORT = (
    0,
    4,
    6,
    9,
    10,
    15,
    19,
    20,
    21,
    24,
    27,
    30,
    34,
    35,
    37,
    44,
    48,
    51,
    54,
    60,
    61,
)

QUADRATIC_CIRCUIT_WEIGHTS = (
    6,
    13,
    6,
    2,
    3,
    2,
    6,
    8,
    1,
    2,
    3,
    2,
    5,
    10,
    6,
    1,
    6,
    11,
    6,
    8,
    7,
)

DENOMINATORS = (
    (10004, -1, -1, -1, -10, -9863, -127),
    (10002, -9965, -1, -1, -1, -1, -32),
    (10005, -1, -9887, -113, -1, -1, -1),
)

HEAD_SCORE_COEFFICIENTS = (
    -15269682346914856,
    61148231840350478336,
    19320576202811305984,
    -32818140812521627648,
    -11644544088780588,
    -37575756260891376,
    -60629109684220428288,
    -466534451470821760,
    52614269760819027968,
    -52261877506605776896,
    23322167980260556800,
    14264560445869776896,
    -14501218091098841088,
    -4834512581107000320,
    -14578687432838793216,
    38894684352617398272,
    -61887871906120515584,
    -52720040282216800256,
    -14450132198626377728,
    14561920969527498752,
    29232218103136743424,
    13732519175109126144,
)

MINIMUM_SIGNED_CLEARED_SCORE = 2072899260662880


def cube() -> np.ndarray:
    return (
        (np.arange(1 << INPUT_BITS)[:, None] >> np.arange(INPUT_BITS)) & 1
    ).astype(object)


def monomial_matrix(degree: int) -> np.ndarray:
    inputs = cube()
    columns = []
    for size in range(degree + 1):
        for subset in itertools.combinations(range(INPUT_BITS), size):
            if subset:
                columns.append(np.prod(inputs[:, subset], axis=1))
            else:
                columns.append(np.ones(1 << INPUT_BITS, dtype=object))
    return np.column_stack(columns).astype(object)


def signs() -> np.ndarray:
    return np.array(
        [
            1 if (TRUTH_MASK >> vertex) & 1 else -1
            for vertex in range(1 << INPUT_BITS)
        ],
        dtype=object,
    )


def affine_matrix() -> np.ndarray:
    return np.column_stack(
        [np.ones(1 << INPUT_BITS, dtype=object), cube()]
    ).astype(object)


def cleared_head_matrix() -> np.ndarray:
    affine = affine_matrix()
    denominator_values = affine @ np.array(DENOMINATORS, dtype=object).T
    full_product = np.prod(denominator_values, axis=1)
    columns = [full_product]
    for head in range(3):
        other_product = np.prod(
            np.delete(denominator_values, head, axis=1), axis=1
        )
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(INPUT_BITS + 1)
        )
    return np.column_stack(columns).astype(object)


def main() -> None:
    target = signs()
    cubic_values = monomial_matrix(3) @ np.array(
        CUBIC_COEFFICIENTS, dtype=object
    )
    signed_cubic_values = target * cubic_values
    assert min(signed_cubic_values) > 0

    weights = np.zeros(1 << INPUT_BITS, dtype=object)
    weights[list(QUADRATIC_CIRCUIT_SUPPORT)] = np.array(
        QUADRATIC_CIRCUIT_WEIGHTS, dtype=object
    )
    signed_quadratic_features = target[:, None] * monomial_matrix(2)
    assert np.all(signed_quadratic_features.T @ weights == 0)
    assert all(value > 0 for value in QUADRATIC_CIRCUIT_WEIGHTS)

    denominators = np.array(DENOMINATORS, dtype=object)
    denominator_values = affine_matrix() @ denominators.T
    assert np.all(denominator_values > 0)
    for denominator in denominators:
        assert all(value < 0 for value in denominator[1:])
    signed_head_values = target * (
        cleared_head_matrix()
        @ np.array(HEAD_SCORE_COEFFICIENTS, dtype=object)
    )
    assert min(signed_head_values) == MINIMUM_SIGNED_CLEARED_SCORE

    positive_vertices = [
        vertex for vertex in range(1 << INPUT_BITS) if target[vertex] > 0
    ]
    print(f"truth mask: 0x{TRUTH_MASK:016x}")
    print(f"positive vertices: {positive_vertices}")
    print(f"minimum signed cubic value: {min(signed_cubic_values)}")
    print(
        "quadratic Gordan circuit: "
        f"support={len(QUADRATIC_CIRCUIT_SUPPORT)}, "
        f"weight sum={sum(QUADRATIC_CIRCUIT_WEIGHTS)}"
    )
    print(f"minimum signed cleared H3 score: {min(signed_head_values)}")
    print("threshold degree and head complexity: exactly 3")


if __name__ == "__main__":
    main()
