#!/usr/bin/env python3
"""MILP active learner for degree-two sign cells outside an H2 dictionary.

For each fixed denominator pair, Gordan's alternative says that a sign pattern
is not linearly separable in its cleared two-head feature space exactly when a
nonnegative positive circuit exists.  Binary truth signs gate one positive and
one negative copy of each circuit weight.  A single MILP therefore asks for a
degree-two threshold sign pattern with such an obstruction for every pair in a
finite dictionary.

MILP feasibility and infeasibility are numerical search results.  A returned
mask is rechecked with exact integer sign certificates and fixed-dictionary LPs.
An infeasible solve is not promoted to a universal theorem without an exact
branch-and-bound or oriented-matroid certificate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

import search_adversarial_low_dimension as core


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "uncovered_cell_milp_results.json"


def active_dictionary(n: int, size: int, seed: int) -> list[np.ndarray]:
    candidates = []
    if n == 5:
        for filename in (
            "mixed_dnf_n5_results.json",
            "uncovered_cell_milp_n5_active_results.json",
            "adversarial_n5_broad_results.json",
            "adversarial_n5_results.json",
        ):
            path = HERE / filename
            if path.exists():
                payload = json.loads(path.read_text())
                stored_dictionary = payload.get(
                    "dictionary", payload.get("final_dictionary", [])
                )
                candidates.extend(
                    np.array(pair, dtype=np.int64)
                    for pair in stored_dictionary
                )
    if n == 6:
        for filename in (
            "adversarial_n6_broad_results.json",
            "uncovered_cell_milp_n6_active_results.json",
        ):
            path = HERE / filename
            if not path.exists():
                continue
            payload = json.loads(path.read_text())
            stored_dictionary = payload.get(
                "dictionary", payload.get("final_dictionary", [])
            )
            candidates.extend(
                np.array(pair, dtype=np.int64) for pair in stored_dictionary
            )
        for pair in (
            (
                (35, -1, -15, -8, -1, -1, -1),
                (33, -1, -17, -1, -8, -4, -1),
            ),
            (
                (33, -1, -8, -9, -4, -1, -9),
                (32, -15, -6, -1, -2, -1, -1),
            ),
            (
                (33, -18, -3, -1, -1, -1, -1),
                (35, -20, -1, -3, -1, -1, -8),
            ),
            (
                (34, -1, -2, -1, -1, -14, -3),
                (33, -6, -1, -7, -13, -1, -4),
            ),
            (
                (34, -1, -1, -6, -1, -16, -8),
                (32, -13, -1, -10, -2, -1, -1),
            ),
        ):
            candidates.append(np.array(pair, dtype=np.int64))
    candidates.extend(core.build_dictionary(n, 3 * size, seed))
    answer = []
    seen = set()
    for pair in candidates:
        key = core.canonical_denominator_pair(pair)
        if key in seen:
            continue
        seen.add(key)
        answer.append(np.array(key, dtype=np.int64))
        if len(answer) >= size:
            break
    return answer


def append_entry(
    rows: list[int],
    columns: list[int],
    data: list[float],
    row: int,
    column: int,
    value: float,
) -> None:
    rows.append(row)
    columns.append(column)
    data.append(float(value))


def build_model(
    n: int,
    dictionary: list[np.ndarray],
    excluded_masks: list[int],
    coefficient_bound: float,
) -> tuple[np.ndarray, np.ndarray, Bounds, LinearConstraint, dict[str, int]]:
    vertices = 1 << n
    evaluation = core.monomial_matrix(n, 2).astype(float)
    degree_dimension = evaluation.shape[1]
    truth_start = 0
    coefficient_start = vertices
    circuit_start = coefficient_start + degree_dimension
    variable_count = circuit_start + len(dictionary) * 2 * vertices

    objective = np.zeros(variable_count)
    integrality = np.zeros(variable_count, dtype=np.uint8)
    integrality[truth_start : truth_start + vertices] = 1
    lower_bounds = np.zeros(variable_count)
    upper_bounds = np.ones(variable_count)
    lower_bounds[coefficient_start:circuit_start] = -coefficient_bound
    upper_bounds[coefficient_start:circuit_start] = coefficient_bound
    upper_bounds[0] = 0.0

    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []
    constraint_lower = []
    constraint_upper = []
    row = 0

    big_m = coefficient_bound * float(np.max(np.sum(np.abs(evaluation), axis=1))) + 1.0
    for vertex in range(vertices):
        append_entry(rows, columns, data, row, truth_start + vertex, -big_m)
        for column, value in enumerate(evaluation[vertex]):
            if value:
                append_entry(
                    rows,
                    columns,
                    data,
                    row,
                    coefficient_start + column,
                    value,
                )
        constraint_lower.append(1.0 - big_m)
        constraint_upper.append(-1.0)
        row += 1

    maximum_dual_residual_scale = 1.0
    for dictionary_index, denominators in enumerate(dictionary):
        features = core.whitened_feature_space(n, denominators)
        rank = features.shape[1]
        first = circuit_start + dictionary_index * 2 * vertices
        second = first + vertices
        for vertex in range(vertices):
            append_entry(rows, columns, data, row, first + vertex, 1.0)
            append_entry(rows, columns, data, row, second + vertex, 1.0)
        constraint_lower.append(1.0)
        constraint_upper.append(1.0)
        row += 1
        for feature in range(rank):
            for vertex in range(vertices):
                value = features[vertex, feature]
                append_entry(rows, columns, data, row, first + vertex, value)
                append_entry(rows, columns, data, row, second + vertex, -value)
            constraint_lower.append(0.0)
            constraint_upper.append(0.0)
            row += 1
        for vertex in range(vertices):
            append_entry(rows, columns, data, row, first + vertex, 1.0)
            append_entry(rows, columns, data, row, truth_start + vertex, -1.0)
            constraint_lower.append(-np.inf)
            constraint_upper.append(0.0)
            row += 1

            append_entry(rows, columns, data, row, second + vertex, 1.0)
            append_entry(rows, columns, data, row, truth_start + vertex, 1.0)
            constraint_lower.append(-np.inf)
            constraint_upper.append(1.0)
            row += 1

    for mask in excluded_masks:
        positive = [vertex for vertex in range(vertices) if (mask >> vertex) & 1]
        for vertex in range(vertices):
            coefficient = -1.0 if vertex in positive else 1.0
            append_entry(rows, columns, data, row, truth_start + vertex, coefficient)
        constraint_lower.append(1.0 - len(positive))
        constraint_upper.append(np.inf)
        row += 1

    matrix = coo_matrix(
        (data, (rows, columns)), shape=(row, variable_count)
    ).tocsr()
    metadata = {
        "vertices": vertices,
        "degree_dimension": degree_dimension,
        "truth_start": truth_start,
        "coefficient_start": coefficient_start,
        "circuit_start": circuit_start,
        "variables": variable_count,
        "constraints": row,
    }
    return (
        objective,
        integrality,
        Bounds(lower_bounds, upper_bounds),
        LinearConstraint(
            matrix,
            np.array(constraint_lower),
            np.array(constraint_upper),
        ),
        metadata,
    )


def solve_uncovered(
    n: int,
    dictionary: list[np.ndarray],
    excluded_masks: list[int],
    coefficient_bound: float,
    time_limit: float,
) -> tuple[object, dict[str, int]]:
    objective, integrality, bounds, constraints, metadata = build_model(
        n, dictionary, excluded_masks, coefficient_bound
    )
    print(
        f"MILP with {metadata['variables']} variables, "
        f"{metadata['constraints']} constraints, "
        f"{len(dictionary)} denominator pairs",
        flush=True,
    )
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=constraints,
        options={
            "time_limit": time_limit,
            "mip_rel_gap": 0.0,
            "presolve": True,
        },
    )
    return result, metadata


def verify_payload(payload: dict[str, object]) -> None:
    n = int(payload["n"])
    dictionary = [
        np.array(pair, dtype=np.int64) for pair in payload["final_dictionary"]
    ]
    affine = core.affine_matrix(n).astype(object)
    for pair in dictionary:
        for denominator in pair:
            assert np.all(denominator[1:] > 0) or np.all(denominator[1:] < 0)
            assert np.all(affine @ denominator.astype(object) > 0)
    for record in payload["records"]:
        if "truth_mask_hex" not in record:
            continue
        mask = int(record["truth_mask_hex"], 16)
        signs = core.signs_from_mask(mask, n)
        if record.get("exact_degree_two"):
            coefficients = np.array(
                record["degree_two_coefficients"], dtype=object
            )
            assert np.all(
                signs
                * (core.monomial_matrix(n, 2).astype(object) @ coefficients)
                > 0
            )
        dictionary_size = int(record["dictionary_size"])
        hits = core.exact_dictionary_hits(
            mask, n, dictionary[:dictionary_size]
        )
        assert len(hits) == record["exact_fixed_dictionary_hit_count"]
        search = record.get("orientation_cycle_search")
        if not search or not search["found"]:
            continue
        denominators = np.array(search["denominators"], dtype=np.int64)
        coefficients = np.array(
            search["cleared_score_coefficients"], dtype=object
        )
        matrix = core.cleared_two_head_matrix(n, denominators).astype(object)
        signed_scores = signs * (matrix @ coefficients)
        assert np.all(signed_scores > 0)
        assert min(map(int, signed_scores)) == search["minimum_signed_cleared_score"]
    print(
        f"verified {len(payload['records'])} MILP active-learning records on n={n}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(5, 6), default=5)
    parser.add_argument("--dictionary-size", type=int, default=64)
    parser.add_argument("--iterations", type=int, default=8)
    parser.add_argument("--coefficient-bound", type=float, default=10000.0)
    parser.add_argument("--time-limit", type=float, default=300.0)
    parser.add_argument("--orientation-trials", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=20260716)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_payload(json.loads(arguments.output.read_text()))
        return

    dictionary = active_dictionary(
        arguments.n, arguments.dictionary_size, arguments.seed
    )
    excluded = []
    records = []
    for iteration in range(arguments.iterations):
        result, metadata = solve_uncovered(
            arguments.n,
            dictionary,
            excluded,
            arguments.coefficient_bound,
            arguments.time_limit,
        )
        record: dict[str, object] = {
            "iteration": iteration + 1,
            "milp_status": int(result.status),
            "milp_message": str(result.message),
            "dictionary_size": len(dictionary),
            "model": metadata,
        }
        if result.x is None:
            records.append(record)
            print(json.dumps(record), flush=True)
            break
        vertices = 1 << arguments.n
        truth = np.rint(result.x[:vertices]).astype(np.int64)
        raw_mask = sum(
            1 << vertex for vertex, value in enumerate(truth) if value == 1
        )
        mask = core.complement_canonical(raw_mask, arguments.n)
        exact_polynomial = core.exact_integer_separator(
            core.signs_from_mask(mask, arguments.n),
            core.monomial_matrix(arguments.n, 2),
        )
        fixed_hits = core.exact_dictionary_hits(
            mask, arguments.n, dictionary
        )
        record["truth_mask_hex"] = (
            f"0x{mask:0{1 << (arguments.n - 2)}x}"
        )
        record["exact_degree_two"] = exact_polynomial is not None
        record["exact_fixed_dictionary_hits"] = fixed_hits[:16]
        record["exact_fixed_dictionary_hit_count"] = len(fixed_hits)
        if exact_polynomial is not None:
            record["degree_two_coefficients"] = [
                int(value) for value in exact_polynomial[0]
            ]
        if exact_polynomial is None or fixed_hits:
            excluded.append(raw_mask)
            records.append(record)
            print(json.dumps(record), flush=True)
            continue

        search = core.orientation_cycle_search(
            mask,
            arguments.n,
            arguments.seed + 100003 * iteration,
            arguments.orientation_trials,
            64,
        )
        record["orientation_cycle_search"] = search
        if search["found"]:
            key = core.canonical_denominator_pair(search["denominators"])
            if key not in {
                core.canonical_denominator_pair(pair) for pair in dictionary
            }:
                dictionary.append(np.array(key, dtype=np.int64))
        else:
            excluded.append(raw_mask)
        records.append(record)
        print(
            json.dumps(
                {
                    "iteration": iteration + 1,
                    "mask": record["truth_mask_hex"],
                    "h2_found": search["found"],
                    "trial": search.get("trial"),
                }
            ),
            flush=True,
        )

    payload = {
        "status": (
            "MILP outcomes are numerical search evidence.  Exact degree-two "
            "and H2 successes are integer-verified."
        ),
        "n": arguments.n,
        "parameters": {
            "initial_dictionary_size": arguments.dictionary_size,
            "coefficient_bound": arguments.coefficient_bound,
            "time_limit": arguments.time_limit,
            "orientation_trials": arguments.orientation_trials,
        },
        "final_dictionary": [pair.tolist() for pair in dictionary],
        "records": records,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
