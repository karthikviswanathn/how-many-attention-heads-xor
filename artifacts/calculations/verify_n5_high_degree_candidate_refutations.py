#!/usr/bin/env python3
"""Verify exact refutations of two hard five-bit separation candidates.

Both truth tables survived broad random denominator screening.  The first has
threshold degree three and the second has threshold degree four.  This script
checks exact threshold-degree certificates and exact matching head
certificates using only integer arithmetic.
"""

from itertools import combinations

import numpy as np


INPUT_BITS = 5


def cube() -> np.ndarray:
    return ((np.arange(1 << INPUT_BITS)[:, None] >> np.arange(INPUT_BITS)) & 1).astype(
        object
    )


def affine_matrix() -> np.ndarray:
    return np.column_stack(
        [np.ones(1 << INPUT_BITS, dtype=object), cube()]
    ).astype(object)


def monomial_matrix(degree: int) -> np.ndarray:
    inputs = cube()
    columns = []
    for size in range(degree + 1):
        for subset in combinations(range(INPUT_BITS), size):
            if subset:
                columns.append(np.prod(inputs[:, subset], axis=1))
            else:
                columns.append(np.ones(1 << INPUT_BITS, dtype=object))
    return np.column_stack(columns).astype(object)


def signs_from_mask(mask: int) -> np.ndarray:
    return np.array(
        [1 if (mask >> vertex) & 1 else -1 for vertex in range(1 << INPUT_BITS)],
        dtype=object,
    )


def cleared_head_matrix(denominators: list[list[int]]) -> np.ndarray:
    affine = affine_matrix()
    denominator_values = affine @ np.array(denominators, dtype=object).T
    full_product = np.prod(denominator_values, axis=1)
    columns = [full_product]
    for head in range(len(denominators)):
        other_product = np.prod(
            np.delete(denominator_values, head, axis=1), axis=1
        )
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(INPUT_BITS + 1)
        )
    return np.column_stack(columns).astype(object)


CERTIFICATES = (
    {
        "name": "degree-three random hard case",
        "mask": 0x149AC934,
        "degree": 3,
        "degree_coefficients": (
            -14,
            0,
            27,
            27,
            27,
            0,
            -27,
            0,
            -217,
            27,
            -217,
            -54,
            -27,
            -54,
            217,
            -27,
            190,
            271,
            190,
            -217,
            -271,
            -271,
            271,
            -108,
            81,
            -163,
        ),
        "degree_lower_support": (2, 3, 8, 10, 12, 15, 18, 19, 24, 26, 28, 31),
        "denominators": (
            (10, 10, 63, 1, 2, 603),
            (10, 142669, 20638, 158, 4, 1),
            (69, -15, -1, -3, -39, -1),
        ),
        "head_coefficients": (
            18599034,
            2412033861,
            -740129806,
            4707511674,
            188133455,
            -3750823618,
            80375242678,
            -2876615747,
            -18839205001351,
            -3087788971798,
            -18849944858,
            3239557461,
            -2466314610,
            1879100956,
            -300183884,
            445294424,
            -278483493,
            150944385,
            -2247966980,
        ),
        "minimum_signed_head_score": 3154067748,
    },
    {
        "name": "parity with one weight-two vertex flipped",
        "mask": 0x966B6996,
        "degree": 4,
        "degree_coefficients": (
            -16,
            32,
            32,
            32,
            32,
            224,
            -64,
            -64,
            -64,
            449,
            -64,
            -64,
            -257,
            -64,
            -257,
            -257,
            128,
            128,
            -385,
            128,
            -385,
            -385,
            128,
            321,
            321,
            321,
            -257,
            257,
            257,
            257,
            -449,
        ),
        "degree_lower_support": tuple(range(8, 16)) + tuple(range(24, 32)),
        "denominators": (
            (375, -88, -18, -48, -47, -85),
            (3, 88, 56, 11, 8, 72),
            (279, -45, -2, -27, -99, -45),
            (250, -52, -20, -87, -6, -84),
        ),
        "head_coefficients": (
            3017091,
            582109133,
            -129717950,
            -63648939,
            -126580760,
            -247103952,
            -92990250,
            -18023867,
            -532296032,
            -336069685,
            -65994303,
            -47902469,
            -434905377,
            396388403,
            -55936488,
            22294069,
            -27933628,
            -47295032,
            -65436910,
            4288936,
            -4318215,
            634546,
            16852481,
            -356212,
            -16852753,
        ),
        "minimum_signed_head_score": 866538115,
    },
    {
        "name": "parity-near degree-three hard case",
        "mask": 0x96E86B96,
        "degree": 3,
        "degree_coefficients": (
            -14,
            109,
            27,
            27,
            27,
            -190,
            -136,
            -136,
            190,
            -81,
            -54,
            -54,
            163,
            -54,
            163,
            163,
            190,
            -136,
            136,
            -136,
            136,
            -109,
            109,
            -109,
            -109,
            -109,
        ),
        "degree_lower_support": (2, 3, 12, 13, 18, 19, 28, 29),
        "denominators": (
            (498, -67, -172, -101, -25, -98),
            (883, -190, -122, -60, -187, -131),
            (709, -49, -139, -70, -195, -59),
        ),
        "head_coefficients": (
            -1077,
            910135,
            2627809,
            -1381869,
            -437769,
            -1679063,
            1256958,
            7753312,
            -631811,
            -7438168,
            -5504428,
            9190471,
            -8018945,
            -6769705,
            -4708320,
            7982091,
            5040066,
            -4345442,
            3818038,
        ),
        "minimum_signed_head_score": 156296498,
    },
)


def verify_certificate(certificate: dict[str, object]) -> None:
    signs = signs_from_mask(int(certificate["mask"]))
    degree = int(certificate["degree"])

    degree_coefficients = np.array(
        certificate["degree_coefficients"], dtype=object
    )
    signed_polynomial_values = signs * (
        monomial_matrix(degree) @ degree_coefficients
    )
    assert min(signed_polynomial_values) > 0

    lower_weights = np.zeros(1 << INPUT_BITS, dtype=object)
    lower_weights[list(certificate["degree_lower_support"])] = 1
    signed_lower_features = signs[:, None] * monomial_matrix(degree - 1)
    assert np.all(signed_lower_features.T @ lower_weights == 0)

    denominators = [list(row) for row in certificate["denominators"]]
    denominator_values = affine_matrix() @ np.array(denominators, dtype=object).T
    assert np.all(denominator_values > 0)
    for denominator in denominators:
        slopes = denominator[1:]
        assert all(slope > 0 for slope in slopes) or all(
            slope < 0 for slope in slopes
        )

    head_coefficients = np.array(certificate["head_coefficients"], dtype=object)
    signed_head_values = signs * (
        cleared_head_matrix(denominators) @ head_coefficients
    )
    assert min(signed_head_values) == certificate["minimum_signed_head_score"]

    print(
        f"{certificate['name']}: degree={degree}, heads={len(denominators)}, "
        f"minimum signed cleared score={min(signed_head_values)}"
    )


def main() -> None:
    for certificate in CERTIFICATES:
        verify_certificate(certificate)
    print("certificates: verified")


if __name__ == "__main__":
    main()
