#!/usr/bin/env python3
"""Screen nonsymmetric six-bit parity-flip triples at four heads.

The initial targets flip an antipodal pair and one further vertex of weight
one, two, or three. Each target receives exact threshold-degree certificates.
Every reported H4 success is also exact. Search failures are only candidates,
but this family has a useful Fourier-moment description for a possible exact
lower bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

import search_adversarial_low_dimension as core
import search_gated_single_flip as h4


N = 6
VERTICES = 1 << N
HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n6_parity_flip_triples_h4_screen.json"
EXCEPTIONAL_TRIPLES = (
    (0, 63, 1),
    (0, 63, 3),
    (0, 63, 7),
    (0, 61, 62),
    (0, 57, 62),
    (0, 49, 62),
    (0, 33, 62),
    (0, 1, 62),
    (0, 51, 60),
    (0, 35, 60),
    (0, 3, 60),
    (0, 7, 56),
)


def target_signs(exceptional: tuple[int, ...]) -> np.ndarray:
    exceptional_set = set(exceptional)
    return np.array(
        [
            (-1 if code in exceptional_set else 1)
            * (1 if bin(code).count("1") % 2 == 0 else -1)
            for code in range(VERTICES)
        ],
        dtype=np.int64,
    )


def truth_mask(signs: np.ndarray) -> int:
    answer = 0
    for code, sign in enumerate(signs):
        if sign > 0:
            answer |= 1 << code
    return answer


def one_dimensional_null_vector(matrix: np.ndarray) -> list[int]:
    rows = [list(map(Fraction, row)) for row in matrix.tolist()]
    row_count = len(rows)
    column_count = len(rows[0])
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][index] - factor * rows[pivot_row][index]
                for index in range(column_count)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free = [column for column in range(column_count) if column not in pivots]
    if len(free) != 1:
        raise RuntimeError(f"expected nullity one, got {len(free)}")
    vector = [Fraction(0) for _ in range(column_count)]
    vector[free[0]] = Fraction(1)
    for row, pivot in reversed(list(enumerate(pivots))):
        vector[pivot] = -sum(
            rows[row][column] * vector[column]
            for column in range(pivot + 1, column_count)
        )
    denominator_lcm = 1
    for value in vector:
        denominator_lcm = math.lcm(denominator_lcm, value.denominator)
    integers = [int(value * denominator_lcm) for value in vector]
    common = 0
    for value in integers:
        common = math.gcd(common, abs(value))
    return [value // common for value in integers]


def positive_gordan_circuit(
    signs: np.ndarray, degree: int
) -> dict[str, object]:
    evaluation = core.monomial_matrix(N, degree)
    signed = (signs[:, None] * evaluation).T
    equality = np.vstack(
        [signed.astype(float), np.ones(VERTICES, dtype=float)]
    )
    target = np.concatenate([np.zeros(signed.shape[0]), [1.0]])
    rng = np.random.default_rng(14072026 + degree)
    objectives = [np.zeros(VERTICES)] + [
        1e-7 * rng.standard_normal(VERTICES) for _ in range(48)
    ]
    for objective in objectives:
        result = linprog(
            objective,
            A_eq=equality,
            b_eq=target,
            bounds=[(0.0, None)] * VERTICES,
            method="highs",
        )
        if not result.success:
            continue
        for tolerance in (1e-7, 1e-9, 1e-11, 1e-13):
            support = np.flatnonzero(result.x > tolerance).tolist()
            try:
                weights = one_dimensional_null_vector(signed[:, support])
            except RuntimeError:
                continue
            if all(weight < 0 for weight in weights):
                weights = [-weight for weight in weights]
            if not all(weight > 0 for weight in weights):
                continue
            exact_moment = signed[:, support].astype(object) @ np.array(
                weights, dtype=object
            )
            if np.all(exact_moment == 0):
                return {"support": support, "weights": weights}
    raise RuntimeError("could not recover an exact positive Gordan circuit")


def exact_degree_four_record(signs: np.ndarray) -> dict[str, object]:
    degree_four = core.exact_integer_separator(
        signs, core.monomial_matrix(N, 4)
    )
    if degree_four is None:
        raise AssertionError("target is not degree at most four")
    degree_three = core.exact_integer_separator(
        signs, core.monomial_matrix(N, 3)
    )
    if degree_three is not None:
        return {
            "threshold_degree": "at most 3",
            "degree_three_coefficients": [
                int(value) for value in degree_three[0]
            ],
        }
    certificate = [int(value) for value in degree_four[0]]
    signed_values = signs.astype(object) * (
        core.monomial_matrix(N, 4).astype(object)
        @ np.array(certificate, dtype=object)
    )
    return {
        "threshold_degree": 4,
        "degree_four_coefficients": certificate,
        "degree_four_minimum_signed_value": int(min(signed_values)),
        "degree_three_gordan_circuit": positive_gordan_circuit(signs, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=24)
    parser.add_argument("--max-iterations", type=int, default=1600)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument(
        "--exceptional",
        type=int,
        nargs=3,
        action="append",
        help="search only the specified exceptional triple; may be repeated",
    )
    parser.add_argument(
        "--scales", type=int, nargs="+", default=(30, 100, 300, 1000, 3000)
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()

    exceptional_triples = (
        EXCEPTIONAL_TRIPLES
        if arguments.exceptional is None
        else tuple(tuple(values) for values in arguments.exceptional)
    )
    if any(
        len(set(exceptional)) != 3
        or any(code < 0 or code >= VERTICES for code in exceptional)
        for exceptional in exceptional_triples
    ):
        raise ValueError("each exceptional triple must contain three cube vertices")

    records = []
    for target_index, exceptional in enumerate(exceptional_triples):
        signs = target_signs(exceptional)
        degree = exact_degree_four_record(signs)
        record: dict[str, object] = {
            "exceptional_vertices": list(exceptional),
            "exceptional_vertex_bits": [f"{code:06b}" for code in exceptional],
            "truth_mask_hex": f"0x{truth_mask(signs):016x}",
            **degree,
            "attempts": [],
            "h4_certificate": None,
        }
        if degree["threshold_degree"] == 4:
            for positive_heads in range(5):
                certificate, best = h4.search_orientation(
                    signs,
                    5,
                    positive_heads,
                    arguments.seed
                    + 100003 * target_index
                    + 1009 * positive_heads,
                    arguments.restarts,
                    arguments.max_iterations,
                    tuple(arguments.scales),
                )
                record["attempts"].append(
                    {"positive_heads": positive_heads, "best": best}
                )
                print(
                    f"exceptional={exceptional} positive_heads={positive_heads} "
                    f"found={certificate is not None} best={best}",
                    flush=True,
                )
                if certificate is not None:
                    record["h4_certificate"] = certificate
                    break
        records.append(record)
        arguments.output.write_text(
            json.dumps(
                {
                    "status": (
                        "Every degree statement and H4 success is exact. "
                        "An H4 search failure is not a lower bound."
                    ),
                    "records": records,
                },
                indent=2,
            )
            + "\n"
        )

    survivors = [
        record
        for record in records
        if record["threshold_degree"] == 4
        and record["h4_certificate"] is None
    ]
    print(f"exact degree-four targets: {sum(record['threshold_degree'] == 4 for record in records)}")
    print(f"H4 search survivors: {len(survivors)}")


if __name__ == "__main__":
    main()
