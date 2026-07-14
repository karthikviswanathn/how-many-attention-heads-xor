#!/usr/bin/env python3
"""Verify exact six-bit parity-with-one-flip data.

For a vertex v, let f_v agree with even parity except at v.  The script
proves exactly that every f_v has threshold degree five.  It also verifies
five-head certificates for the endpoint orbit |v|=0, the adjacent orbit
|v|=1, and both middle orbits |v|=2 and |v|=3.  Thus this family does not
give a strict head-complexity separation.
"""

from __future__ import annotations

import itertools


DIMENSION = 6
VERTICES = 1 << DIMENSION


ENDPOINT_DENOMINATORS = (
    (7, -1, -1, -1, -1, -1, -1),
    (2, 1, 1, 1, 1, 1, 1),
    (9, -1, -1, -1, -1, -1, -1),
    (4, 1, 1, 1, 1, 1, 1),
    (11, -1, -1, -1, -1, -1, -1),
)
ENDPOINT_SCORE = (
    -410,
    1647, -62, -62, -62, -62, -62, -62,
    -1725, 2168, 2168, 2168, 2168, 2168, 2168,
    -838, -2937, -2937, -2937, -2937, -2937, -2937,
    2600, -4240, -4240, -4240, -4240, -4240, -4240,
    3380, 4583, 4583, 4583, 4583, 4583, 4583,
)


ADJACENT_DENOMINATORS = (
    (7, -1, -1, -1, -1, -1, -1),
    (8, -1, -1, -1, -1, -1, -1),
    (3, 1, 1, 1, 1, 1, 1),
    (4, 1, 1, 1, 1, 1, 1),
    (11, -1, -1, -1, -1, -1, -1),
)
ADJACENT_SCORE = (
    -4763,
    19927, 6654, -4436, -4436, -4436, -4436, -4436,
    25129, -35183, 1783, 1783, 1783, 1783, 1783,
    -24394, 32851, -11508, -11508, -11508, -11508, -11508,
    29413, -49819, 12284, 12284, 12284, 12284, 12284,
    -4889, 43395, -5400, -5400, -5400, -5400, -5400,
)


MIDDLE_WEIGHT_TWO_DENOMINATORS = (
    (999, -58, -45, -187, -233, -201, -45),
    (1001, -151, -131, -185, -157, -217, -139),
    (1000, -182, -153, -53, -41, -50, -476),
    (61, 48, 632, 74, 45, 55, 86),
    (24, 700, 50, 52, 70, 39, 65),
)
MIDDLE_WEIGHT_TWO_SCORE = (
    -4282,
    -2985666, 1650462, 1690415, 2340496, 2096865, 3359362, 1775594,
    -384729, 2378438, 1989365, -1904682, -2896099, -2690987, 4114908,
    -2140410, 1910659, 1519154, -578691, -313593, -736204, -2612769,
    -792542, 1643551, -3515684, 467388, 378413, 368023, 459673,
    548958, -3583414, 245937, 449858, 856628, 357951, 538277,
)


MIDDLE_WEIGHT_THREE_DENOMINATORS = (
    (10001, -812, -728, -641, -2180, -1799, -2785),
    (10001, -1512, -1208, -2405, -1230, -1022, -1629),
    (2777, 741, 1887, 630, 1313, 1338, 1315),
    (495, 3136, 2974, 842, 851, 889, 813),
    (1508, 1031, 782, 3674, 998, 1028, 978),
)
MIDDLE_WEIGHT_THREE_SCORE = (
    173482,
    865163298, -70488423, -69663382, -79121347, -191449813, -155187227,
    -252175825,
    755870331, -141179789, -93608922, -202842977, -62473854, -52024237,
    -84246861,
    1113812922, -37307456, 93691807, -1396443680, -12666750, -5841690,
    -20423386,
    -123128468, -677650068, -1269584779, -284142175, -270402926,
    -282930957, -258633563,
    -734434735, -329258848, 288105245, 1031371447, -56317364, -62613384,
    -46413172,
)


def point(code: int) -> tuple[int, ...]:
    return tuple((code >> coordinate) & 1 for coordinate in range(DIMENSION))


def sign_point(code: int) -> tuple[int, ...]:
    return tuple(1 - 2 * bit for bit in point(code))


def parity_sign(code: int) -> int:
    return 1 if sum(point(code)) % 2 == 0 else -1


def target_sign(code: int, flipped: int) -> int:
    value = parity_sign(code)
    return -value if code == flipped else value


def explicit_degree_five_value(code: int, flipped: int) -> int:
    """Evaluate chi(z)-chi(v) product_i(1+v_i z_i)."""
    z = sign_point(code)
    v = sign_point(flipped)
    chi_z = 1
    chi_v = 1
    product = 1
    for current, exceptional in zip(z, v):
        chi_z *= current
        chi_v *= exceptional
        product *= 1 + exceptional * current
    return chi_z - chi_v * product


def subsets(maximum_degree: int):
    for degree in range(maximum_degree + 1):
        yield from itertools.combinations(range(DIMENSION), degree)


def character(code: int, subset: tuple[int, ...]) -> int:
    z = sign_point(code)
    answer = 1
    for coordinate in subset:
        answer *= z[coordinate]
    return answer


def dual_weight(code: int, flipped: int) -> int:
    if code == flipped:
        return 1
    distance = sum(
        first != second for first, second in zip(point(code), point(flipped))
    )
    return 2 * distance - 1


def affine_value(coefficients: tuple[int, ...], code: int) -> int:
    return coefficients[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(coefficients[1:], point(code))
    )


def verify_head_certificate(
    flipped: int,
    denominators: tuple[tuple[int, ...], ...],
    score_coefficients: tuple[int, ...],
) -> int:
    assert len(denominators) == 5
    assert len(score_coefficients) == 1 + 5 * (DIMENSION + 1)
    denominator_values = [
        [affine_value(denominator, code) for denominator in denominators]
        for code in range(VERTICES)
    ]
    for denominator in denominators:
        slopes = denominator[1:]
        assert all(value > 0 for value in slopes) or all(
            value < 0 for value in slopes
        )
    assert min(value for row in denominator_values for value in row) > 0

    minimum = None
    for code in range(VERTICES):
        values = denominator_values[code]
        full_product = 1
        for value in values:
            full_product *= value
        score = score_coefficients[0] * full_product
        offset = 1
        for head in range(5):
            other_product = full_product // values[head]
            numerator = affine_value(
                score_coefficients[offset:offset + DIMENSION + 1], code
            )
            score += numerator * other_product
            offset += DIMENSION + 1
        signed = target_sign(code, flipped) * score
        assert signed > 0
        minimum = signed if minimum is None else min(minimum, signed)
    assert minimum is not None
    return minimum


def verify_threshold_degree(flipped: int) -> None:
    signed_values = [
        target_sign(code, flipped)
        * explicit_degree_five_value(code, flipped)
        for code in range(VERTICES)
    ]
    assert min(signed_values) == 1

    weights = [dual_weight(code, flipped) for code in range(VERTICES)]
    assert min(weights) == 1
    for subset in subsets(4):
        moment = sum(
            weights[code]
            * target_sign(code, flipped)
            * character(code, subset)
            for code in range(VERTICES)
        )
        assert moment == 0


def verify_fourier_orthant(flipped: int) -> None:
    """Check the exact coefficient-sign identity on a generic positive ray."""
    exceptional_r = []
    for code in range(VERTICES):
        if code == flipped:
            exceptional_r.append(0)
        else:
            exceptional_r.append(1 + ((37 * code + 11 * flipped) % 23))
    exceptional_r[flipped] = -sum(exceptional_r)
    polynomial_values = [
        parity_sign(code) * exceptional_r[code]
        for code in range(VERTICES)
    ]

    top_coefficient = sum(
        parity_sign(code) * polynomial_values[code]
        for code in range(VERTICES)
    )
    assert top_coefficient == 0
    assert all(
        target_sign(code, flipped) * polynomial_values[code] > 0
        for code in range(VERTICES)
    )

    full_set = set(range(DIMENSION))
    common_reoriented_sign = -parity_sign(flipped)
    for subset in subsets(DIMENSION - 1):
        complement = tuple(sorted(full_set.difference(subset)))
        coefficient = sum(
            character(code, subset) * polynomial_values[code]
            for code in range(VERTICES)
        )
        expected_sign = -character(flipped, complement)
        assert expected_sign * coefficient > 0

        reoriented_coefficient = character(flipped, subset) * coefficient
        assert common_reoriented_sign * reoriented_coefficient > 0


def main() -> None:
    for flipped in (0, 1, 3, 7):
        verify_threshold_degree(flipped)
        verify_fourier_orthant(flipped)
        print(
            f"flip weight {sum(point(flipped))}: "
            "exact threshold degree five and Fourier orthant"
        )

    endpoint_margin = verify_head_certificate(
        0, ENDPOINT_DENOMINATORS, ENDPOINT_SCORE
    )
    adjacent_margin = verify_head_certificate(
        1, ADJACENT_DENOMINATORS, ADJACENT_SCORE
    )
    middle_weight_two_margin = verify_head_certificate(
        3, MIDDLE_WEIGHT_TWO_DENOMINATORS, MIDDLE_WEIGHT_TWO_SCORE
    )
    middle_weight_three_margin = verify_head_certificate(
        7, MIDDLE_WEIGHT_THREE_DENOMINATORS, MIDDLE_WEIGHT_THREE_SCORE
    )
    assert endpoint_margin == 11464
    assert adjacent_margin == 13400
    assert middle_weight_two_margin == 108571693319292
    assert middle_weight_three_margin == 5063509014022934970
    print(f"endpoint five-head margin: {endpoint_margin}")
    print(f"adjacent five-head margin: {adjacent_margin}")
    print(f"middle weight-two five-head margin: {middle_weight_two_margin}")
    print(
        "middle weight-three five-head margin: "
        f"{middle_weight_three_margin}"
    )
    print("all parity-single-flip orbits have exact five-head certificates")
    print("certificate: verified")


if __name__ == "__main__":
    main()
