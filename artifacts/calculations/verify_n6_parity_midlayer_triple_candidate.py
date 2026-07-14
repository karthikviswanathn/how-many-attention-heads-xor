#!/usr/bin/env python3
"""Verify the exact degree-four middle-layer parity-flip candidate."""

from __future__ import annotations

import itertools


N = 6
EXCEPTIONAL = (21, 38, 41)
EXPECTED_MASK = 0x96696BD669B69669

# Monomial order: all subsets of sizes zero through four, lexicographically
# within each size.
DEGREE_FOUR_COEFFICIENTS = (
    1,
    -2,
    -2,
    -2,
    -2,
    -2,
    -2,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    4,
    -8,
    -8,
    -8,
    -24,
    -24,
    40,
    -40,
    -8,
    40,
    -8,
    -8,
    -8,
    40,
    -8,
    -8,
    -8,
    -8,
    -8,
    -24,
    -8,
    32,
    -32,
    16,
    16,
    -16,
    32,
    -16,
    16,
    16,
    -32,
    16,
    -32,
    -16,
    16,
    32,
)

DEGREE_THREE_GORDAN_SUPPORT = (
    1,
    2,
    3,
    4,
    7,
    8,
    10,
    12,
    13,
    14,
    15,
    19,
    20,
    24,
    25,
    26,
    28,
    29,
    30,
    31,
    33,
    34,
    35,
    39,
    40,
    41,
    44,
    45,
    46,
    49,
    50,
    51,
    52,
    55,
    56,
    58,
    60,
    61,
    62,
    63,
)

DEGREE_THREE_GORDAN_WEIGHTS = (
    1,
    1,
    4,
    1,
    1,
    3,
    1,
    8,
    3,
    4,
    1,
    2,
    2,
    5,
    1,
    2,
    11,
    5,
    6,
    2,
    2,
    2,
    6,
    2,
    1,
    1,
    5,
    1,
    2,
    1,
    1,
    4,
    1,
    1,
    3,
    1,
    8,
    3,
    4,
    1,
)


def bit_tuple(code: int) -> tuple[int, ...]:
    return tuple((code >> coordinate) & 1 for coordinate in range(N))


def sign_tuple(code: int) -> tuple[int, ...]:
    return tuple(1 - 2 * bit for bit in bit_tuple(code))


def parity_sign(code: int) -> int:
    return 1 if bin(code).count("1") % 2 == 0 else -1


def target_sign(code: int) -> int:
    parity = parity_sign(code)
    return -parity if code in EXCEPTIONAL else parity


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def monomial(code: int, subset: tuple[int, ...]) -> int:
    return int(all((code >> coordinate) & 1 for coordinate in subset))


def monomial_subsets(degree: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        subset
        for size in range(degree + 1)
        for subset in itertools.combinations(range(N), size)
    )


def polynomial_value(code: int) -> int:
    subsets = monomial_subsets(4)
    assert len(subsets) == len(DEGREE_FOUR_COEFFICIENTS)
    return sum(
        coefficient * monomial(code, subset)
        for coefficient, subset in zip(DEGREE_FOUR_COEFFICIENTS, subsets)
    )


def verify_threshold_degree() -> None:
    truth_mask = 0
    signed_values = []
    for code in range(64):
        if target_sign(code) > 0:
            truth_mask |= 1 << code
        signed_values.append(target_sign(code) * polynomial_value(code))
    assert truth_mask == EXPECTED_MASK
    assert min(signed_values) == 1

    assert len(DEGREE_THREE_GORDAN_SUPPORT) == len(
        DEGREE_THREE_GORDAN_WEIGHTS
    )
    assert all(weight > 0 for weight in DEGREE_THREE_GORDAN_WEIGHTS)
    for subset in monomial_subsets(3):
        moment = sum(
            weight * target_sign(code) * monomial(code, subset)
            for code, weight in zip(
                DEGREE_THREE_GORDAN_SUPPORT,
                DEGREE_THREE_GORDAN_WEIGHTS,
            )
        )
        assert moment == 0


def cosets(subspace: set[int]) -> tuple[frozenset[int], ...]:
    unseen = set(range(64))
    answer = []
    while unseen:
        representative = min(unseen)
        current = frozenset(representative ^ value for value in subspace)
        answer.append(current)
        unseen.difference_update(current)
    return tuple(answer)


def verify_fourier_rigidity_identities() -> None:
    first, second, third = EXCEPTIONAL
    assert all(
        bin(a ^ b).count("1") == 4
        for a, b in itertools.combinations(EXCEPTIONAL, 2)
    )
    difference_1 = first ^ second
    difference_2 = first ^ third
    subspace = {0, difference_1, difference_2, difference_1 ^ difference_2}
    exceptional_coset = frozenset(first ^ value for value in subspace)
    assert exceptional_coset == frozenset((*EXCEPTIONAL, 26))

    parity_twist_values = [
        parity_sign(code) * polynomial_value(code) for code in range(64)
    ]
    assert all(
        value < 0 if code in EXCEPTIONAL else value > 0
        for code, value in enumerate(parity_twist_values)
    )
    assert sum(parity_twist_values) == 0
    for coordinate in range(N):
        assert sum(
            value * sign_tuple(code)[coordinate]
            for code, value in enumerate(parity_twist_values)
        ) == 0

    exceptional_magnitudes = [-parity_twist_values[code] for code in EXCEPTIONAL]
    total_exceptional_mass = sum(exceptional_magnitudes)
    assert all(
        4 * magnitude < 3 * total_exceptional_mass
        for magnitude in exceptional_magnitudes
    )

    annihilator = tuple(
        mask
        for mask in range(64)
        if all(character(mask, value) == 1 for value in subspace)
    )
    assert len(annihilator) == 16

    quotient_cosets = cosets(subspace)
    assert exceptional_coset in quotient_cosets
    beta = {
        current: sum(parity_twist_values[code] for code in current)
        for current in quotient_cosets
        if current != exceptional_coset
    }
    assert len(beta) == 15
    assert all(value > 0 for value in beta.values())

    cut_weights = {}
    for mask in annihilator:
        if mask == 0:
            continue
        eta = character(mask, first)
        fourier_sum = sum(
            value * character(mask, code)
            for code, value in enumerate(parity_twist_values)
        )
        cut_weight = -(eta * fourier_sum) // 2
        assert -eta * fourier_sum > 0
        assert -eta * fourier_sum % 2 == 0
        direct = sum(
            value
            for current, value in beta.items()
            if eta * character(mask, min(current)) == -1
        )
        assert cut_weight == direct
        cut_weights[mask] = cut_weight

    for current, mass in beta.items():
        representative = min(current)
        inverse_numerator = -sum(
            character(mask, first)
            * character(mask, representative)
            * cut_weight
            for mask, cut_weight in cut_weights.items()
        )
        assert inverse_numerator % 8 == 0
        assert inverse_numerator // 8 == mass


def main() -> None:
    verify_threshold_degree()
    verify_fourier_rigidity_identities()
    print(f"truth mask: {EXPECTED_MASK:#018x}")
    print("threshold degree: 4")
    print(f"degree-three Gordan support: {len(DEGREE_THREE_GORDAN_SUPPORT)}")
    print("Fourier cut-cone identities: verified")


if __name__ == "__main__":
    main()
