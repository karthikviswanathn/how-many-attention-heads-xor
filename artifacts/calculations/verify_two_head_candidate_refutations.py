#!/usr/bin/env python3
"""Verify exact two-head certificates that refute numerical candidates.

Every coefficient below is an integer.  Numerator coefficients are scaled by
10^6 and positive-denominator coefficients by 10^10.  The common positive
scale does not affect any sign.
"""

from itertools import product


NUMERATOR_SCALE = 10**6
DENOMINATOR_SCALE = 10**10


def affine(coefficients, point):
    return coefficients[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(coefficients[1:], point)
    )


def verify_certificate(name, dimension, labels, numerator_1, denominator_1,
                       numerator_2, denominator_2):
    assert len(numerator_1) == dimension + 1
    assert len(numerator_2) == dimension + 1
    assert len(denominator_1) == dimension + 1
    assert len(denominator_2) == dimension + 1
    for denominator in (denominator_1, denominator_2):
        slopes = denominator[1:]
        assert all(coefficient > 0 for coefficient in slopes) or all(
            coefficient < 0 for coefficient in slopes
        )

    minimum_signed_score = None
    positive_count = 0
    for index, point in enumerate(product((0, 1), repeat=dimension)):
        a = affine(numerator_1, point)
        b = affine(denominator_1, point)
        c = affine(numerator_2, point)
        d = affine(denominator_2, point)
        assert b > 0
        assert d > 0

        cleared_score = a * d + c * b
        expected_sign = 1 if labels(index, point) else -1
        signed_score = expected_sign * cleared_score
        assert signed_score > 0, (name, index, point, cleared_score)
        minimum_signed_score = (
            signed_score
            if minimum_signed_score is None
            else min(minimum_signed_score, signed_score)
        )
        positive_count += expected_sign > 0

    print(f"{name}: inputs={1 << dimension}, positives={positive_count}")
    print(f"{name}: minimum signed cleared score={minimum_signed_score}")


N6_TRUTH_MASK = 0xDE5F3A0A5C5D1400
N6_NUMERATOR_1 = (
    -235863157,
    -165272368,
    281249082,
    -73975175,
    -127250628,
    3571152,
    187158647,
)
N6_DENOMINATOR_1 = (
    10000000,
    825630589,
    10000000,
    10000000,
    2030274020,
    3554129430,
    3589965940,
)
N6_NUMERATOR_2 = (
    430000032,
    352540555,
    -182007613,
    198074846,
    -145401525,
    81481861,
    -585863808,
)
N6_DENOMINATOR_2 = (
    1775755580,
    1934404180,
    10000000,
    10000000,
    10000000,
    6289840230,
    10000000,
)


INT4_NUMERATOR_1 = (
    1497405603,
    216559672,
    -138951628,
    99271044,
    82351247,
    3283337,
    -140444914,
    -1670864246,
    78845080,
)
INT4_DENOMINATOR_1 = (
    1539852674,
    5998501025,
    1228492995,
    1000000,
    1000000,
    1000000,
    1233153306,
    1000000,
    1000000,
)
INT4_NUMERATOR_2 = (
    -304746927,
    -462532138,
    177140653,
    -40242821,
    -78268291,
    41233531,
    177918138,
    675802754,
    -74069020,
)
INT4_DENOMINATOR_2 = (
    1000000,
    3208615020,
    1000000,
    1000000,
    289798742,
    1000000,
    1000000,
    6221047282,
    280538956,
)


Z_AND_DISJ2_NUMERATOR_1 = (
    -29059,
    -31489,
    -50807,
    -46759,
    25313,
    52281,
)
Z_AND_DISJ2_DENOMINATOR_1 = (100, 59, 64, 35, 50, 66)
Z_AND_DISJ2_NUMERATOR_2 = (24380, 46107, 34910, 42660, -38706, -48315)
Z_AND_DISJ2_DENOMINATOR_2 = (86, 64, 42, 52, 15, 78)


N6_SMALL_DIM_TRUTH_MASK = 0x057D779F13FF7FFF
N6_SMALL_DIM_NUMERATOR_1 = (
    34560,
    19410,
    -26888,
    21066,
    35560,
    22394,
    -19541,
)
N6_SMALL_DIM_DENOMINATOR_1 = (35, -1, -15, -8, -1, -1, -1)
N6_SMALL_DIM_NUMERATOR_2 = (
    -13375,
    -24302,
    30773,
    -35800,
    -14913,
    -17116,
    6535,
)
N6_SMALL_DIM_DENOMINATOR_2 = (33, -1, -17, -1, -8, -4, -1)


N6_BROAD_TRUTH_MASK = 0x000018184C0C6FDF
N6_BROAD_NUMERATOR_1 = (
    -144019,
    40552,
    103964,
    -90683,
    22710,
    28303,
    -70791,
)
N6_BROAD_DENOMINATOR_1 = (14, -2, -7, -1, -1, -1, -1)
N6_BROAD_NUMERATOR_2 = (
    154481,
    -23630,
    41408,
    98438,
    -23422,
    -51533,
    -49164,
)
N6_BROAD_DENOMINATOR_2 = (15, -1, -1, -1, -1, -1, -6)


N7_POSITIVE_ORIENTATION_TRUTH_MASK = 0x2A2F2E3F2F2FBF3F022A00372F2A3724
N7_POSITIVE_ORIENTATION_NUMERATOR_1 = (
    -1232116,
    1266287,
    301778,
    31710398,
    1424014,
    2751292,
    47276561,
    8276328,
)
N7_POSITIVE_ORIENTATION_DENOMINATOR_1 = (1, 1, 3, 112, 3, 5, 149, 28)
N7_POSITIVE_ORIENTATION_NUMERATOR_2 = (
    3067490,
    -11025776,
    -172151,
    -45976249,
    -895399,
    -24161859,
    -4551653,
    -8713095,
)
N7_POSITIVE_ORIENTATION_DENOMINATOR_2 = (4, 35, 1, 155, 1, 76, 1, 30)


N7_NEGATIVE_ORIENTATION_TRUTH_MASK = 0x511555517555FDD05114DDD1FFFFFFF
N7_NEGATIVE_ORIENTATION_NUMERATOR_1 = (
    -22273585,
    -1313926,
    932013,
    6761680,
    5509508,
    -20719942,
    9574757,
    106930,
)
N7_NEGATIVE_ORIENTATION_DENOMINATOR_1 = (
    306,
    -1,
    -1,
    -97,
    -80,
    -1,
    -124,
    -1,
)
N7_NEGATIVE_ORIENTATION_NUMERATOR_2 = (
    25629037,
    -829980,
    -822552,
    960395,
    894572,
    -18800560,
    -3661514,
    -2055711,
)
N7_NEGATIVE_ORIENTATION_DENOMINATOR_2 = (
    304,
    -1,
    -1,
    -1,
    -1,
    -267,
    -23,
    -8,
)


N7_MAIN_TRUTH_MASK = 0x3351C040FAFF01010341CFD5EFFF
N7_MAIN_NUMERATOR_1 = (
    -26493822,
    28087797,
    -2374569,
    -29589088,
    10262392,
    30769161,
    31533652,
    27533956,
)
N7_MAIN_DENOMINATOR_1 = (1, 61, 1, 1, 14, 25, 1, 1)
N7_MAIN_NUMERATOR_2 = (
    507586406,
    -532180738,
    52300855,
    556213918,
    -193217378,
    -586584887,
    -607999235,
    -518451637,
)
N7_MAIN_DENOMINATOR_2 = (10, 1157, 1, 27, 267, 472, 36, 11)


def n6_label(index, _point):
    return bool((N6_TRUTH_MASK >> index) & 1)


def int4_label(_index, point):
    return any(point[index] * point[4 + index] for index in range(4))


def z_and_disj2_label(_index, point):
    z, x1, y1, x2, y2 = point
    return bool(z and not x1 * y1 and not x2 * y2)


def n6_small_dim_label(_index, point):
    code = sum(bit << coordinate for coordinate, bit in enumerate(point))
    return bool((N6_SMALL_DIM_TRUTH_MASK >> code) & 1)


def n6_broad_label(_index, point):
    code = sum(bit << coordinate for coordinate, bit in enumerate(point))
    return bool((N6_BROAD_TRUTH_MASK >> code) & 1)


def n7_positive_orientation_label(_index, point):
    code = sum(bit << coordinate for coordinate, bit in enumerate(point))
    return bool((N7_POSITIVE_ORIENTATION_TRUTH_MASK >> code) & 1)


def n7_negative_orientation_label(_index, point):
    code = sum(bit << coordinate for coordinate, bit in enumerate(point))
    return bool((N7_NEGATIVE_ORIENTATION_TRUTH_MASK >> code) & 1)


def n7_main_label(_index, point):
    code = sum(bit << coordinate for coordinate, bit in enumerate(point))
    return bool((N7_MAIN_TRUTH_MASK >> code) & 1)


def main():
    verify_certificate(
        "six-bit autoresearch candidate",
        6,
        n6_label,
        N6_NUMERATOR_1,
        N6_DENOMINATOR_1,
        N6_NUMERATOR_2,
        N6_DENOMINATOR_2,
    )
    verify_certificate(
        "INT_4",
        8,
        int4_label,
        INT4_NUMERATOR_1,
        INT4_DENOMINATOR_1,
        INT4_NUMERATOR_2,
        INT4_DENOMINATOR_2,
    )
    verify_certificate(
        "z AND DISJ_2",
        5,
        z_and_disj2_label,
        Z_AND_DISJ2_NUMERATOR_1,
        Z_AND_DISJ2_DENOMINATOR_1,
        Z_AND_DISJ2_NUMERATOR_2,
        Z_AND_DISJ2_DENOMINATOR_2,
    )
    verify_certificate(
        "six-bit small-dimension candidate",
        6,
        n6_small_dim_label,
        N6_SMALL_DIM_NUMERATOR_1,
        N6_SMALL_DIM_DENOMINATOR_1,
        N6_SMALL_DIM_NUMERATOR_2,
        N6_SMALL_DIM_DENOMINATOR_2,
    )
    verify_certificate(
        "six-bit broad-search candidate",
        6,
        n6_broad_label,
        N6_BROAD_NUMERATOR_1,
        N6_BROAD_DENOMINATOR_1,
        N6_BROAD_NUMERATOR_2,
        N6_BROAD_DENOMINATOR_2,
    )
    verify_certificate(
        "seven-bit positive-orientation candidate",
        7,
        n7_positive_orientation_label,
        N7_POSITIVE_ORIENTATION_NUMERATOR_1,
        N7_POSITIVE_ORIENTATION_DENOMINATOR_1,
        N7_POSITIVE_ORIENTATION_NUMERATOR_2,
        N7_POSITIVE_ORIENTATION_DENOMINATOR_2,
    )
    verify_certificate(
        "seven-bit negative-orientation candidate",
        7,
        n7_negative_orientation_label,
        N7_NEGATIVE_ORIENTATION_NUMERATOR_1,
        N7_NEGATIVE_ORIENTATION_DENOMINATOR_1,
        N7_NEGATIVE_ORIENTATION_NUMERATOR_2,
        N7_NEGATIVE_ORIENTATION_DENOMINATOR_2,
    )
    verify_certificate(
        "seven-bit main candidate",
        7,
        n7_main_label,
        N7_MAIN_NUMERATOR_1,
        N7_MAIN_DENOMINATOR_1,
        N7_MAIN_NUMERATOR_2,
        N7_MAIN_DENOMINATOR_2,
    )
    print("certificates: verified")


if __name__ == "__main__":
    main()
