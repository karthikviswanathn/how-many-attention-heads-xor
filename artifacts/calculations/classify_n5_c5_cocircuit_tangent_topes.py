#!/usr/bin/env python3
"""Build an exact-clause cover of all closed-C5 cocircuit tangent topes.

Discovery uses floating-point LPs, but every learned clause is reconstructed
over the rationals before it is retained.  There are two clause types:

* a wrong-edge quadratic weakly matching the sign pattern, which no fully
  locked cell can contain;
* a positive integer Gordan relation among signed evaluation rows and the ten
  prescribed edge rows, which forbids a strict complementary-C5 extension.

The companion verifier checks the finite Boolean cover using only the stored
integer certificates.  Archived locked masks are allowed as singleton leaves.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
import json
from math import gcd, lcm
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

import screen_n5_c5_two_scale as c5
import survey_n5_c5_locked_cells as survey
import verify_n5_c5_fixed_chord_extremizer as exact


RAY_PATH = Path(__file__).with_name("n5_c5_cocircuit_ray_orbits.csv")
KNOWN_PATH = Path(__file__).with_name("n5_c5_locked_extreme_ray_incidence.json")
FOURIER = c5.FOURIER.astype(np.int64)
EDGE_ROWS = c5.EDGE_SELECTOR.astype(np.int64)


def load_rays() -> list[tuple[int, ...]]:
    array = np.loadtxt(RAY_PATH, delimiter=",", skiprows=1, dtype=np.int64)
    return [tuple(int(value) for value in row) for row in array]


def known_raw_masks() -> set[int]:
    payload = json.loads(KNOWN_PATH.read_text())
    canonical = {mask for record in payload["incidence"] for mask in record["masks"]}
    assert len(canonical) == 380
    answer = set()
    for mask in canonical:
        for permutation, exchanges_colors in survey.fixed_orthant_symmetries():
            image = survey.permute_mask(mask, permutation)
            if exchanges_colors:
                image = survey.FULL_MASK ^ image
            answer.add(image)
            answer.add(survey.global_input_complement(image))
    return answer


def target(edge_index: int) -> tuple[int, ...]:
    answer = [0] * 16
    answer[6 + edge_index] = int(c5.EDGE_SIGNS[edge_index])
    return tuple(answer)


TARGETS = tuple(target(edge_index) for edge_index in range(10))


def rational_vector(values: np.ndarray) -> tuple[Fraction, ...]:
    return tuple(
        Fraction(float(value)).limit_denominator(1_000_000) for value in values
    )


def primitive_fractions(values: tuple[Fraction, ...]) -> tuple[int, ...]:
    denominator = reduce(lcm, (value.denominator for value in values), 1)
    integers = [
        value.numerator * (denominator // value.denominator) for value in values
    ]
    divisor = reduce(gcd, (abs(value) for value in integers if value))
    return tuple(value // divisor for value in integers)


def sign_clause(values: np.ndarray) -> tuple[int, int]:
    positive = sum((int(value) > 0) << vertex for vertex, value in enumerate(values))
    negative = sum((int(value) < 0) << vertex for vertex, value in enumerate(values))
    return positive, negative


def wrong_edge_separator(mask: int) -> tuple[int, ...] | None:
    signs = exact.target_signs(mask)
    signed = signs[:, None] * FOURIER
    for edge_index, edge_target in enumerate(TARGETS):
        result = linprog(
            np.zeros(16),
            A_ub=-signed.astype(float),
            b_ub=np.zeros(32),
            A_eq=np.array([edge_target], dtype=float),
            b_eq=np.array([-1.0]),
            bounds=[(None, None)] * 16,
            method="highs",
        )
        if not result.success:
            continue
        fractions = rational_vector(result.x)
        values = tuple(
            sum(Fraction(int(FOURIER[vertex, column])) * fractions[column] for column in range(16))
            for vertex in range(32)
        )
        edge_value = sum(
            Fraction(edge_target[column]) * fractions[column]
            for column in range(16)
        )
        assert edge_value == -1
        assert all(signs[vertex] * values[vertex] >= 0 for vertex in range(32))
        primitive = primitive_fractions(fractions)
        primitive_values = FOURIER @ np.array(primitive, dtype=np.int64)
        assert np.all(signs * primitive_values >= 0)
        assert any(
            int(c5.EDGE_SIGNS[index]) * primitive[6 + index] < 0
            for index in range(10)
        )
        return primitive
    return None


def strict_extension(mask: int) -> np.ndarray | None:
    signs = exact.target_signs(mask)
    constraints = np.vstack((-(signs[:, None] * FOURIER), -EDGE_ROWS))
    result = linprog(
        np.zeros(16),
        A_ub=constraints.astype(float),
        b_ub=-np.ones(42),
        bounds=[(None, None)] * 16,
        method="highs",
    )
    return result.x if result.success else None


def gordan_circuit(mask: int) -> tuple[int, ...]:
    signs = exact.target_signs(mask)
    rows = np.vstack((signs[:, None] * FOURIER, EDGE_ROWS)).astype(np.int64)
    equality = np.vstack((rows.T, np.ones((1, 42), dtype=np.int64)))
    rhs = np.zeros(17)
    rhs[-1] = 1
    result = linprog(
        np.zeros(42),
        A_eq=equality.astype(float),
        b_eq=rhs,
        bounds=[(0.0, None)] * 42,
        method="highs",
    )
    assert result.success
    support = [index for index, value in enumerate(result.x) if value > 1e-9]
    matrix = [
        [int(equality[row, index]) for index in support] for row in range(17)
    ]
    weights = exact.solve_exact(matrix, [Fraction(int(value)) for value in rhs])
    assert weights is not None and all(weight > 0 for weight in weights)
    common_denominator = reduce(lcm, (weight.denominator for weight in weights), 1)
    integers = [
        weight.numerator * (common_denominator // weight.denominator)
        for weight in weights
    ]
    divisor = reduce(gcd, integers)
    integers = [value // divisor for value in integers]
    answer = [0] * 42
    for index, value in zip(support, integers):
        answer[index] = value
    answer_array = np.array(answer, dtype=np.int64)
    assert np.all(answer_array >= 0) and np.any(answer_array > 0)
    assert np.all(rows.T @ answer_array == 0)
    return tuple(answer)


def circuit_clause(weights: tuple[int, ...], mask: int) -> tuple[int, int]:
    positive = 0
    negative = 0
    for vertex, weight in enumerate(weights[:32]):
        if not weight:
            continue
        if (mask >> vertex) & 1:
            positive |= 1 << vertex
        else:
            negative |= 1 << vertex
    assert positive | negative
    return positive, negative


def apply_local_clause(
    covered: np.ndarray,
    zero_vertices: tuple[int, ...],
    fixed_positive: int,
    fixed_negative: int,
    positive: int,
    negative: int,
) -> bool:
    if (positive & fixed_negative) or (negative & fixed_positive):
        return False
    zero_position = {vertex: index for index, vertex in enumerate(zero_vertices)}
    selector: list[object] = [slice(None)] * len(zero_vertices)
    local_support = False
    for vertex in zero_vertices:
        bit = 1 << vertex
        if positive & bit:
            selector[len(zero_vertices) - 1 - zero_position[vertex]] = 1
            local_support = True
        elif negative & bit:
            selector[len(zero_vertices) - 1 - zero_position[vertex]] = 0
            local_support = True
    if not local_support:
        covered[:] = True
    else:
        covered.reshape((2,) * len(zero_vertices))[tuple(selector)] = True
    return True


def exact_simple_forcing(
    ray: tuple[int, ...], zero_vertices: tuple[int, ...]
) -> dict[int, bool] | None:
    if len(zero_vertices) != 15:
        return {}
    matrix = [
        [int(FOURIER[vertex, column]) for vertex in zero_vertices]
        for column in range(16)
    ]
    forced: dict[int, bool] = {}
    for edge_index, edge_target in enumerate(TARGETS):
        if ray[6 + edge_index] != 0:
            continue
        coefficients = exact.solve_exact(
            matrix, [Fraction(value) for value in edge_target]
        )
        assert coefficients is not None
        for position, coefficient in enumerate(coefficients):
            if not coefficient:
                continue
            required = coefficient > 0
            if position in forced and forced[position] != required:
                return None
            forced[position] = required
    return forced


def next_uncovered(covered: np.ndarray, start: int) -> int | None:
    size = len(covered)
    while start < size:
        stop = min(size, start + 65_536)
        offsets = np.flatnonzero(~covered[start:stop])
        if len(offsets):
            return start + int(offsets[0])
        start = stop
    return None


def mask_at(ray_values: np.ndarray, zero_vertices: tuple[int, ...], local: int) -> int:
    mask = sum(
        (int(value) > 0) << vertex
        for vertex, value in enumerate(ray_values)
        if value
    )
    for position, vertex in enumerate(zero_vertices):
        mask |= ((local >> position) & 1) << vertex
    return mask


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-zero-size", type=int, default=24)
    parser.add_argument("--limit-rays", type=int, default=0)
    parser.add_argument("--input", type=Path)
    arguments = parser.parse_args()

    wrong_vectors: dict[tuple[int, int], tuple[int, ...]] = {}
    circuits: dict[tuple[int, int], tuple[int, ...]] = {}
    if arguments.input:
        payload = json.loads(arguments.input.read_text())
        for vector in payload["wrong_edge_vectors"]:
            vector_tuple = tuple(vector)
            wrong_vectors[sign_clause(FOURIER @ np.array(vector_tuple, dtype=np.int64))] = vector_tuple
        for record in payload["gordan_circuits"]:
            weights = tuple(record["weights"])
            circuits[(record["positive_mask"], record["negative_mask"])] = weights

    archive = known_raw_masks()
    survivor_masks: set[int] = set()
    counts: Counter[str] = Counter()
    rays = load_rays()
    rays.sort(key=lambda ray: (int(np.sum(FOURIER @ np.array(ray) == 0)), ray))
    selected = [
        ray for ray in rays
        if int(np.sum(FOURIER @ np.array(ray, dtype=np.int64) == 0)) <= arguments.max_zero_size
    ]
    if arguments.limit_rays:
        selected = selected[: arguments.limit_rays]

    for ray_index, ray in enumerate(selected):
        ray_array = np.array(ray, dtype=np.int64)
        ray_values = FOURIER @ ray_array
        zero_vertices = tuple(int(vertex) for vertex in np.flatnonzero(ray_values == 0))
        fixed_positive = sum(
            (int(value) > 0) << vertex
            for vertex, value in enumerate(ray_values)
            if value
        )
        fixed_negative = sum(
            (int(value) < 0) << vertex
            for vertex, value in enumerate(ray_values)
            if value
        )
        covered = np.zeros(1 << len(zero_vertices), dtype=bool)

        forcing = exact_simple_forcing(ray, zero_vertices)
        if forcing is None:
            covered[:] = True
            counts["simple_forcing_conflicts"] += 1
        else:
            view = covered.reshape((2,) * len(zero_vertices))
            for position, required in forcing.items():
                selector: list[object] = [slice(None)] * len(zero_vertices)
                selector[len(zero_vertices) - 1 - position] = int(not required)
                view[tuple(selector)] = True

        for positive, negative in wrong_vectors:
            apply_local_clause(
                covered, zero_vertices, fixed_positive, fixed_negative,
                positive, negative,
            )
        for positive, negative in circuits:
            apply_local_clause(
                covered, zero_vertices, fixed_positive, fixed_negative,
                positive, negative,
            )
        for mask in archive:
            if (mask & fixed_positive) != fixed_positive:
                continue
            if ((~mask) & fixed_negative) != fixed_negative:
                continue
            local = sum(((mask >> vertex) & 1) << position for position, vertex in enumerate(zero_vertices))
            covered[local] = True
            survivor_masks.add(mask)

        pointer = 0
        while True:
            local = next_uncovered(covered, pointer)
            if local is None:
                break
            mask = mask_at(ray_values, zero_vertices, local)
            representative = strict_extension(mask)
            if representative is None:
                weights = gordan_circuit(mask)
                clause = circuit_clause(weights, mask)
                circuits.setdefault(clause, weights)
                counts["learned_gordan"] += 1
                apply_local_clause(
                    covered, zero_vertices, fixed_positive, fixed_negative,
                    *clause,
                )
            else:
                separator = wrong_edge_separator(mask)
                if separator is not None:
                    clause = sign_clause(FOURIER @ np.array(separator, dtype=np.int64))
                    wrong_vectors.setdefault(clause, separator)
                    counts["learned_wrong_edge"] += 1
                    apply_local_clause(
                        covered, zero_vertices, fixed_positive, fixed_negative,
                        *clause,
                    )
                else:
                    canonical = survey.canonical_mask(mask)
                    if mask not in archive:
                        raise RuntimeError(
                            f"new fully locked tangent tope 0x{mask:08x}, canonical 0x{canonical:08x}"
                        )
                    survivor_masks.add(mask)
                    covered[local] = True
                    counts["locked_archive_leaves"] += 1
            assert covered[local]
            pointer = local + 1

        counts["rays"] += 1
        counts[f"zero_size_{len(zero_vertices)}"] += 1
        if (ray_index + 1) % 100 == 0:
            print(
                f"rays={ray_index + 1}, wrong={len(wrong_vectors)}, "
                f"gordan={len(circuits)}, survivors={len(survivor_masks)}"
            )

    payload = {
        "counts": dict(sorted(counts.items())),
        "processed_ray_count": len(selected),
        "max_zero_size": arguments.max_zero_size,
        "wrong_edge_vectors": [list(vector) for vector in sorted(wrong_vectors.values())],
        "gordan_circuits": [
            {
                "positive_mask": positive,
                "negative_mask": negative,
                "weights": list(weights),
            }
            for (positive, negative), weights in sorted(circuits.items())
        ],
        "survivor_masks": sorted(survivor_masks),
        "warning": "LPs discover clauses; every stored clause is reconstructed and checked exactly.",
    }
    arguments.output.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
    print(f"counts: {dict(sorted(counts.items()))}")
    print(f"wrong-edge clauses: {len(wrong_vectors)}")
    print(f"Gordan clauses: {len(circuits)}")
    print(f"survivor raw masks: {len(survivor_masks)}")
    print(f"output: {arguments.output}")


if __name__ == "__main__":
    main()
