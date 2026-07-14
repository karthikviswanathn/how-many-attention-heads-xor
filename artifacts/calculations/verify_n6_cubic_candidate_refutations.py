#!/usr/bin/env python3
"""Verify three exact refutations from the six-bit cubic search.

For each truth table, an integer cubic sign polynomial and a positive Gordan
circuit prove threshold degree three.  Positive affine denominators and an
integer cleared-score certificate prove three-head realizability.  Thus both
tables satisfy threshold degree equal to head complexity equal to three, so
neither table is a strict separation.

All checks below use integer arithmetic only.
"""

from __future__ import annotations

import itertools

import numpy as np


INPUT_BITS = 6

# Monomial order is degree first, then lexicographic combinations of 0-based
# variable indices, exactly as produced by itertools.combinations.
CERTIFICATES = (
    {
        "truth_mask": 0x12244880218A8110,
        "cubic_coefficients": (
            -22,
            -62,
            -149,
            43,
            130,
            -62,
            -149,
            210,
            -173,
            -69,
            166,
            210,
            -167,
            -26,
            210,
            206,
            -173,
            -210,
            106,
            -26,
            -161,
            119,
            297,
            -79,
            -76,
            -268,
            -38,
            297,
            -172,
            -79,
            100,
            -224,
            297,
            -283,
            110,
            -297,
            148,
            -134,
            297,
            -172,
            153,
            148,
        ),
        "minimum_signed_cubic_value": 19,
        "quadratic_circuit_support": (
            1,
            2,
            4,
            8,
            11,
            14,
            17,
            20,
            21,
            23,
            26,
            29,
            32,
            38,
            39,
            43,
            45,
            50,
            51,
            53,
            56,
            60,
            63,
        ),
        "quadratic_circuit_weights": (
            18,
            12,
            65,
            7,
            40,
            2,
            65,
            56,
            100,
            56,
            2,
            37,
            13,
            45,
            23,
            76,
            41,
            61,
            83,
            57,
            41,
            38,
            32,
        ),
        "orientations": (-1, -1, 1),
        "denominators": (
            (1001, -1, -73, -155, -162, -168, -441),
            (1005, -1, -1, -445, -1, -1, -1),
            (1, 271, 416, 1, 61, 252, 1),
        ),
        "head_score_coefficients": (
            1310595802438,
            9374582430256,
            -4397455792178,
            -8022202440815,
            -2319264222624,
            -4453593735898,
            -8111946123858,
            9374846063356,
            903054221356531,
            6358142319481,
            9794298708478,
            -406590961847031,
            5445675168587,
            11419009995047,
            -1732107491853,
            -2218884709113,
            -603164606318571,
            -925183450557764,
            -2191344654349,
            -135414806513970,
            -560276966367163,
            -12535072433288,
        ),
        "minimum_signed_cleared_score": 343262974918480,
    },
    {
        "truth_mask": 0x02180C8160822150,
        "cubic_coefficients": (
            -22,
            -103,
            -103,
            43,
            43,
            0,
            43,
            -52,
            60,
            60,
            146,
            -52,
            103,
            60,
            8,
            60,
            -146,
            -43,
            -86,
            -104,
            -138,
            -43,
            52,
            -207,
            104,
            207,
            86,
            -164,
            -69,
            -43,
            147,
            9,
            0,
            -8,
            -60,
            -17,
            77,
            -181,
            207,
            -207,
            129,
            77,
        ),
        "minimum_signed_cubic_value": 20,
        "quadratic_circuit_support": (
            4,
            5,
            6,
            8,
            11,
            13,
            14,
            17,
            20,
            23,
            25,
            26,
            29,
            30,
            33,
            34,
            39,
            42,
            44,
            51,
            52,
            55,
            56,
        ),
        "quadratic_circuit_weights": (
            4,
            7,
            6,
            5,
            3,
            4,
            9,
            5,
            10,
            2,
            6,
            1,
            5,
            5,
            1,
            9,
            7,
            8,
            5,
            5,
            9,
            11,
            3,
        ),
        "orientations": (-1, -1, -1),
        "denominators": (
            (100000, -40408, -13617, -28, -21020, -24917, -2),
            (100000, -6, -5, -8, -58797, -3, -41175),
            (100002, -99953, -1, -1, -1, -41, -1),
        ),
        "head_score_coefficients": (
            39577070602295184,
            -3946916077876322238464,
            -2085397372491901173760,
            -314151615133667491840,
            4050636478611933102080,
            1660826086268629155840,
            -360102325374157258752,
            1644501906376417345536,
            -2147520064516005560320,
            917439109644128640,
            744416566126720640,
            -2440728154315922866176,
            1486310000546047852544,
            439597283644516032,
            659690433604886200320,
            924558194782240374784,
            -921604795789289455616,
            697961512897204736,
            -1178897389006759936,
            318635212005185344,
            -1552334674863855872,
            -546152843809208192,
        ),
        "minimum_signed_cleared_score": 778259917397545395552,
    },
    {
        "truth_mask": 0x3047010D090EA030,
        "cubic_coefficients": (
            -22,
            -23,
            -45,
            43,
            0,
            0,
            56,
            68,
            81,
            -99,
            66,
            -33,
            -77,
            -41,
            99,
            99,
            -99,
            -99,
            -99,
            43,
            -13,
            -13,
            -47,
            140,
            -122,
            -79,
            140,
            -140,
            -81,
            13,
            15,
            61,
            2,
            79,
            23,
            -56,
            -140,
            -134,
            74,
            111,
            111,
            -74,
        ),
        "minimum_signed_cubic_value": 19,
        "quadratic_circuit_support": (
            0,
            1,
            4,
            6,
            11,
            15,
            17,
            19,
            20,
            24,
            29,
            35,
            36,
            39,
            40,
            44,
            45,
            51,
            54,
            56,
            59,
            61,
        ),
        "quadratic_circuit_weights": (
            5,
            5,
            14,
            6,
            3,
            5,
            5,
            4,
            7,
            4,
            6,
            9,
            2,
            5,
            4,
            5,
            1,
            8,
            6,
            3,
            2,
            7,
        ),
        "orientations": (-1, -1, -1),
        "denominators": (
            (10003, -1, -2642, -1, -3007, -4350, -1),
            (10005, -14, -1, -9986, -1, -1, -1),
            (10003, -1, -1, -3385, -170, -1, -6444),
        ),
        "head_score_coefficients": (
            1705048167471576,
            -88598069730232860672,
            13521422956200212,
            29814785281744752640,
            -44681498307435634688,
            26820462384107712512,
            31908770524005957632,
            -102249127728735928320,
            74774042760944271360,
            1270359162301501696,
            -1735910819607265792,
            -74197599253301051392,
            -21548994706237600,
            -1743872071289519872,
            -911858232296809984,
            -52156723536364822528,
            -1371260536342266368,
            23556843492388855808,
            -71721566281783975936,
            12239505760800821248,
            62384105495889297408,
            88592555988231389184,
        ),
        "minimum_signed_cleared_score": 104594294173425664,
    },
)


def cube() -> np.ndarray:
    return (
        (np.arange(1 << INPUT_BITS)[:, None] >> np.arange(INPUT_BITS)) & 1
    ).astype(object)


def affine_matrix() -> np.ndarray:
    return np.column_stack(
        [np.ones(1 << INPUT_BITS, dtype=object), cube()]
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


def signs(truth_mask: int) -> np.ndarray:
    return np.array(
        [
            1 if (truth_mask >> vertex) & 1 else -1
            for vertex in range(1 << INPUT_BITS)
        ],
        dtype=object,
    )


def cleared_head_matrix(denominators: tuple[tuple[int, ...], ...]) -> np.ndarray:
    affine = affine_matrix()
    denominator_values = affine @ np.array(denominators, dtype=object).T
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


def verify(certificate: dict[str, object]) -> tuple[int, int]:
    target = signs(int(certificate["truth_mask"]))

    cubic_values = monomial_matrix(3) @ np.array(
        certificate["cubic_coefficients"], dtype=object
    )
    signed_cubic_values = target * cubic_values
    cubic_minimum = int(min(signed_cubic_values))
    assert cubic_minimum == certificate["minimum_signed_cubic_value"]
    assert cubic_minimum > 0

    support = certificate["quadratic_circuit_support"]
    circuit_weights = certificate["quadratic_circuit_weights"]
    assert len(support) == len(circuit_weights)
    assert all(int(weight) > 0 for weight in circuit_weights)
    weights = np.zeros(1 << INPUT_BITS, dtype=object)
    weights[list(support)] = np.array(circuit_weights, dtype=object)
    signed_quadratic_features = target[:, None] * monomial_matrix(2)
    assert np.all(signed_quadratic_features.T @ weights == 0)

    denominators = np.array(certificate["denominators"], dtype=object)
    orientations = certificate["orientations"]
    assert denominators.shape == (3, INPUT_BITS + 1)
    for denominator, orientation in zip(denominators, orientations):
        assert all(
            int(orientation) * int(slope) > 0 for slope in denominator[1:]
        )
    denominator_values = affine_matrix() @ denominators.T
    assert np.all(denominator_values > 0)

    signed_head_values = target * (
        cleared_head_matrix(certificate["denominators"])
        @ np.array(certificate["head_score_coefficients"], dtype=object)
    )
    head_minimum = int(min(signed_head_values))
    assert head_minimum == certificate["minimum_signed_cleared_score"]
    assert head_minimum > 0
    return cubic_minimum, head_minimum


def main() -> None:
    for certificate in CERTIFICATES:
        cubic_minimum, head_minimum = verify(certificate)
        truth_mask = int(certificate["truth_mask"])
        support = certificate["quadratic_circuit_support"]
        weights = certificate["quadratic_circuit_weights"]
        print(f"truth mask: 0x{truth_mask:016x}")
        print(f"minimum signed cubic value: {cubic_minimum}")
        print(
            "quadratic Gordan circuit: "
            f"support={len(support)}, weight sum={sum(weights)}"
        )
        print(f"minimum signed cleared H3 score: {head_minimum}")
        print("threshold degree and head complexity: exactly 3")


if __name__ == "__main__":
    main()
