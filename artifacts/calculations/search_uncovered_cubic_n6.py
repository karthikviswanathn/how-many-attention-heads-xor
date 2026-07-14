#!/usr/bin/env python3
"""Active search for a six-bit degree-three versus three-head gap.

For fixed denominator triples, three-head scores form a linear feature space.
Gordan's alternative gives a positive circuit exactly when a truth pattern is
not separable in that space.  A mixed-integer model asks for a degree-three
threshold truth table carrying such a circuit for every triple in a finite
dictionary.  Each returned cell is then attacked by a continuous all-
orientation search.  Every success is rounded to integer denominators, solved
again by linear programming, and verified with integer arithmetic.

The MILP and continuous searches are candidate generators.  A surviving mask
is not a lower bound on head complexity until a global infeasibility proof is
supplied.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp, minimize
from scipy.special import expit
from scipy.sparse import coo_matrix

import search_adversarial_low_dimension as core


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "uncovered_cubic_n6_results.json"
N = 6
HEADS = 3
WIDTH = N + 1
VERTICES = 1 << N


def signs_from_mask(mask: int) -> np.ndarray:
    return core.signs_from_mask(mask, N)


def mask_from_truth(truth: np.ndarray) -> int:
    return sum(1 << vertex for vertex, value in enumerate(truth) if value)


def canonical_triple(denominators: np.ndarray) -> tuple[tuple[int, ...], ...]:
    rows = []
    for row in denominators:
        values = [int(value) for value in row]
        common = 0
        for value in values:
            common = math.gcd(common, abs(value))
        if common > 1:
            values = [value // common for value in values]
        rows.append(tuple(values))
    return tuple(sorted(rows))


def oriented_denominator(
    literal_weights: np.ndarray, orientation: int
) -> np.ndarray:
    weights = [max(1, int(value)) for value in literal_weights]
    if orientation > 0:
        return np.array(weights, dtype=np.int64)
    return np.array(
        [sum(weights)] + [-value for value in weights[1:]], dtype=np.int64
    )


def random_denominator(rng: np.random.Generator) -> np.ndarray:
    orientation = int(rng.choice((-1, 1)))
    # Log-uniform weights make both dense and almost-literal factors common.
    weights = np.maximum(
        1, np.rint(np.exp(rng.uniform(0.0, 8.0, size=WIDTH)))
    ).astype(np.int64)
    return oriented_denominator(weights, orientation)


def random_dictionary(size: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    answer = []
    seen = set()
    while len(answer) < size:
        triple = np.vstack([random_denominator(rng) for _ in range(HEADS)])
        key = canonical_triple(triple)
        if key in seen:
            continue
        seen.add(key)
        answer.append(np.array(key, dtype=np.int64))
    return answer


def ratio_features(denominators: np.ndarray) -> np.ndarray:
    affine = core.affine_matrix(N).astype(float)
    values = affine @ denominators.astype(float).T
    assert np.all(values > 0)
    return np.column_stack(
        [np.ones(VERTICES)]
        + [affine / values[:, head, None] for head in range(HEADS)]
    )


def whitened_features(denominators: np.ndarray) -> np.ndarray:
    features = ratio_features(denominators)
    left, singular_values, _ = np.linalg.svd(features, full_matrices=False)
    tolerance = 1e-11 * max(1.0, float(singular_values[0]))
    return left[:, singular_values > tolerance]


def cleared_matrix(denominators: np.ndarray) -> np.ndarray:
    affine = core.affine_matrix(N).astype(object)
    values = affine @ denominators.astype(object).T
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(HEADS):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(WIDTH)
        )
    return np.column_stack(columns).astype(object)


def exact_head_certificate(
    signs: np.ndarray, denominators: np.ndarray
) -> dict[str, object] | None:
    features = ratio_features(denominators)
    norms = np.linalg.norm(features, axis=0)
    normalized = features / norms
    variable_count = normalized.shape[1]
    constraints = np.zeros((VERTICES, variable_count + 1))
    constraints[:, :variable_count] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variable_count + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(VERTICES),
        bounds=[(-1.0, 1.0)] * variable_count + [(None, None)],
        method="highs",
    )
    if not result.success or -float(result.fun) <= 1e-11:
        return None

    floating = result.x[:variable_count] / norms
    matrix = cleared_matrix(denominators)
    floating_margin = float(
        np.min(signs * (features @ floating))
    )
    if floating_margin <= 1e-12:
        return None
    row_norm = max(
        sum(abs(int(value)) for value in row) for row in matrix.tolist()
    )
    scale = max(1, int(math.ceil((row_norm + 1) / (2 * floating_margin))))
    signs_object = signs.astype(object)
    for _ in range(180):
        integers = np.array(
            [int(round(scale * value)) for value in floating], dtype=object
        )
        signed_scores = signs_object * (matrix @ integers)
        if min(signed_scores) > 0:
            return {
                "denominators": denominators.tolist(),
                "score_coefficients": [int(value) for value in integers],
                "minimum_signed_cleared_score": int(min(signed_scores)),
                "floating_ratio_margin": floating_margin,
            }
        scale *= 2
    return None


def literal_matrix(inputs: np.ndarray, orientation: int) -> np.ndarray:
    literals = inputs if orientation > 0 else 1.0 - inputs
    return np.column_stack([np.ones(VERTICES), literals])


def softmax(rows: np.ndarray) -> np.ndarray:
    shifted = rows - np.max(rows, axis=1, keepdims=True)
    exponentials = np.exp(np.maximum(shifted, -700.0))
    raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
    # Keep every literal weight in the strict interior.  This avoids numerical
    # division by zero while still resolving denominator ratios down to 1e-12.
    epsilon = 1e-12
    return (1.0 - WIDTH * epsilon) * raw + epsilon


def continuous_search(
    signs: np.ndarray,
    seed: int,
    restarts: int,
    max_iterations: int,
    scales: tuple[int, ...],
    orientation_filter: tuple[int, int, int] | None = None,
    lp_accuracy_threshold: int = VERTICES - 4,
) -> tuple[dict[str, object] | None, dict[str, object]]:
    inputs = core.cube(N).astype(float)
    affine = np.column_stack([np.ones(VERTICES), inputs])
    rng = np.random.default_rng(seed)
    best_accuracy = 0
    best_minimum = float("-inf")
    best: dict[str, object] = {}

    orientation_tuples = (
        (orientation_filter,)
        if orientation_filter is not None
        else itertools.product((-1, 1), repeat=HEADS)
    )
    for orientations in orientation_tuples:
        literals = [literal_matrix(inputs, value) for value in orientations]

        def objective_gradient(
            variables: np.ndarray, regularization: float
        ) -> tuple[float, np.ndarray]:
            numerators = variables[: HEADS * WIDTH].reshape(HEADS, WIDTH)
            logits = variables[HEADS * WIDTH :].reshape(HEADS, WIDTH)
            theta = softmax(logits)
            denominator_values = np.column_stack(
                [literals[head] @ theta[head] for head in range(HEADS)]
            )
            numerator_values = affine @ numerators.T
            score = np.sum(numerator_values / denominator_values, axis=1)
            arguments = -signs * score
            score_gradient = -signs * expit(arguments) / VERTICES
            loss = float(np.mean(np.logaddexp(0.0, arguments)))
            loss += regularization * (
                np.sum(numerators * numerators)
                + 0.001 * np.sum(logits * logits)
            )

            numerator_gradient = (
                affine.T @ (score_gradient[:, None] / denominator_values)
            ).T
            numerator_gradient += 2 * regularization * numerators
            theta_gradient = np.vstack(
                [
                    literals[head].T
                    @ (
                        -score_gradient
                        * numerator_values[:, head]
                        / denominator_values[:, head] ** 2
                    )
                    for head in range(HEADS)
                ]
            )
            logit_gradient = theta * (
                theta_gradient
                - np.sum(theta * theta_gradient, axis=1, keepdims=True)
            )
            logit_gradient += 0.002 * regularization * logits
            return loss, np.concatenate(
                [numerator_gradient.ravel(), logit_gradient.ravel()]
            )

        for restart in range(restarts):
            variables = np.concatenate(
                [
                    rng.normal(scale=0.7, size=HEADS * WIDTH),
                    rng.normal(scale=3.0, size=HEADS * WIDTH),
                ]
            )
            regularization = 10 ** rng.uniform(-12.0, -6.0)
            result = minimize(
                lambda current: objective_gradient(current, regularization),
                variables,
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": max_iterations,
                    "ftol": 1e-14,
                    "gtol": 1e-9,
                    "maxls": 60,
                },
            )
            numerators = result.x[: HEADS * WIDTH].reshape(HEADS, WIDTH)
            theta = softmax(
                result.x[HEADS * WIDTH :].reshape(HEADS, WIDTH)
            )
            denominator_values = np.column_stack(
                [literals[head] @ theta[head] for head in range(HEADS)]
            )
            signed = signs * np.sum(
                (affine @ numerators.T) / denominator_values, axis=1
            )
            accuracy = int(np.sum(signed > 1e-8))
            minimum = float(np.min(signed))
            if (accuracy, minimum) > (best_accuracy, best_minimum):
                best_accuracy, best_minimum = accuracy, minimum
                best = {
                    "orientations": list(orientations),
                    "restart": restart,
                    "accuracy": accuracy,
                    "minimum_signed_score": minimum,
                    "literal_weights": theta.tolist(),
                    "numerators": numerators.tolist(),
                    "wrong_vertices": [
                        int(index) for index in np.flatnonzero(signed <= 1e-8)
                    ],
                }
                print(
                    f"orientations={orientations} restart={restart} "
                    f"accuracy={accuracy}/{VERTICES} minimum={minimum}",
                    flush=True,
                )
            # The nonlinear objective can optimize the numerators poorly even
            # when its denominators already support the target sign cell.  A
            # fixed-denominator LP is decisive, so run it for every near fit,
            # not only when the current floating numerators classify all rows.
            if accuracy < lp_accuracy_threshold:
                continue

            for scale in scales:
                denominators = np.vstack(
                    [
                        oriented_denominator(
                            np.maximum(1, np.rint(scale * theta[head])),
                            orientations[head],
                        )
                        for head in range(HEADS)
                    ]
                )
                certificate = exact_head_certificate(signs, denominators)
                if certificate is not None:
                    certificate["orientations"] = list(orientations)
                    certificate["continuous_restart"] = restart
                    certificate["rounding_scale"] = scale
                    return certificate, best
    return None, best


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


def build_milp(
    dictionary: list[np.ndarray],
    excluded_masks: list[int],
    coefficient_bound: float,
    maximize_uniform_circuit_floor: bool = False,
    minimum_uniform_circuit_floor: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, Bounds, LinearConstraint, dict[str, int]]:
    evaluation = core.monomial_matrix(N, 3).astype(float)
    degree_dimension = evaluation.shape[1]
    truth_start = 0
    coefficient_start = VERTICES
    circuit_start = coefficient_start + degree_dimension
    circuit_end = circuit_start + len(dictionary) * 2 * VERTICES
    use_uniform_circuit_floor = (
        maximize_uniform_circuit_floor or minimum_uniform_circuit_floor > 0.0
    )
    floor_index = circuit_end if use_uniform_circuit_floor else -1
    variable_count = circuit_end + int(use_uniform_circuit_floor)

    objective = np.zeros(variable_count)
    if maximize_uniform_circuit_floor:
        objective[floor_index] = -1.0
    integrality = np.zeros(variable_count, dtype=np.uint8)
    integrality[:VERTICES] = 1
    lower_bounds = np.zeros(variable_count)
    upper_bounds = np.ones(variable_count)
    lower_bounds[coefficient_start:circuit_start] = -coefficient_bound
    upper_bounds[coefficient_start:circuit_start] = coefficient_bound
    upper_bounds[0] = 0.0
    if use_uniform_circuit_floor:
        lower_bounds[floor_index] = minimum_uniform_circuit_floor
        upper_bounds[floor_index] = 1.0 / VERTICES

    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []
    lower = []
    upper = []
    row = 0
    big_m = coefficient_bound * float(
        np.max(np.sum(np.abs(evaluation), axis=1))
    ) + 1.0

    for vertex in range(VERTICES):
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
        lower.append(1.0 - big_m)
        upper.append(-1.0)
        row += 1

    for dictionary_index, denominators in enumerate(dictionary):
        features = whitened_features(denominators)
        first = circuit_start + dictionary_index * 2 * VERTICES
        second = first + VERTICES
        for vertex in range(VERTICES):
            append_entry(rows, columns, data, row, first + vertex, 1.0)
            append_entry(rows, columns, data, row, second + vertex, 1.0)
        lower.append(1.0)
        upper.append(1.0)
        row += 1
        for feature in range(features.shape[1]):
            for vertex in range(VERTICES):
                value = features[vertex, feature]
                append_entry(rows, columns, data, row, first + vertex, value)
                append_entry(rows, columns, data, row, second + vertex, -value)
            lower.append(0.0)
            upper.append(0.0)
            row += 1
        for vertex in range(VERTICES):
            append_entry(rows, columns, data, row, first + vertex, 1.0)
            append_entry(rows, columns, data, row, truth_start + vertex, -1.0)
            lower.append(-np.inf)
            upper.append(0.0)
            row += 1
            append_entry(rows, columns, data, row, second + vertex, 1.0)
            append_entry(rows, columns, data, row, truth_start + vertex, 1.0)
            lower.append(-np.inf)
            upper.append(1.0)
            row += 1
            if use_uniform_circuit_floor:
                append_entry(rows, columns, data, row, first + vertex, 1.0)
                append_entry(rows, columns, data, row, second + vertex, 1.0)
                append_entry(rows, columns, data, row, floor_index, -1.0)
                lower.append(0.0)
                upper.append(np.inf)
                row += 1

    for mask in excluded_masks:
        positive = [vertex for vertex in range(VERTICES) if (mask >> vertex) & 1]
        for vertex in range(VERTICES):
            append_entry(
                rows,
                columns,
                data,
                row,
                truth_start + vertex,
                -1.0 if vertex in positive else 1.0,
            )
        lower.append(1.0 - len(positive))
        upper.append(np.inf)
        row += 1

    matrix = coo_matrix(
        (data, (rows, columns)), shape=(row, variable_count)
    ).tocsr()
    metadata = {
        "variables": variable_count,
        "constraints": row,
        "degree_dimension": degree_dimension,
        "dictionary_size": len(dictionary),
        "circuit_floor_index": floor_index,
        "minimum_uniform_circuit_floor": minimum_uniform_circuit_floor,
    }
    return (
        objective,
        integrality,
        Bounds(lower_bounds, upper_bounds),
        LinearConstraint(matrix, np.array(lower), np.array(upper)),
        metadata,
    )


def verify_payload(payload: dict[str, object]) -> None:
    evaluation = core.monomial_matrix(N, 3).astype(object)
    affine = core.affine_matrix(N).astype(object)
    for triple in payload["final_dictionary"]:
        denominators = np.array(triple, dtype=object)
        assert np.all(affine @ denominators.T > 0)
        for denominator in denominators:
            slopes = denominator[1:]
            assert all(value > 0 for value in slopes) or all(
                value < 0 for value in slopes
            )
    for record in payload["records"]:
        if "truth_mask_hex" not in record:
            continue
        mask = int(record["truth_mask_hex"], 16)
        signs = signs_from_mask(mask).astype(object)
        coefficients = np.array(record["degree_three_coefficients"], dtype=object)
        assert min(signs * (evaluation @ coefficients)) > 0
        certificate = record.get("three_head_certificate")
        if certificate is None:
            continue
        denominators = np.array(certificate["denominators"], dtype=object)
        score_coefficients = np.array(
            certificate["score_coefficients"], dtype=object
        )
        signed_scores = signs * (
            cleared_matrix(denominators) @ score_coefficients
        )
        assert min(signed_scores) == certificate["minimum_signed_cleared_score"]
    print(f"verified {len(payload['records'])} records", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary-size", type=int, default=24)
    parser.add_argument("--iterations", type=int, default=8)
    parser.add_argument("--coefficient-bound", type=float, default=1000.0)
    parser.add_argument("--time-limit", type=float, default=180.0)
    parser.add_argument("--restarts", type=int, default=24)
    parser.add_argument("--max-iterations", type=int, default=2500)
    parser.add_argument("--seed", type=int, default=60320260714)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_payload(json.loads(arguments.output.read_text()))
        return

    dictionary = random_dictionary(arguments.dictionary_size, arguments.seed)
    excluded_masks: list[int] = []
    records = []
    scales = (1000, 10000, 100000, 1000000, 10000000)

    for iteration in range(arguments.iterations):
        objective, integrality, bounds, constraints, metadata = build_milp(
            dictionary, excluded_masks, arguments.coefficient_bound
        )
        print(
            f"iteration={iteration + 1} MILP variables={metadata['variables']} "
            f"constraints={metadata['constraints']} "
            f"dictionary={len(dictionary)}",
            flush=True,
        )
        result = milp(
            objective,
            integrality=integrality,
            bounds=bounds,
            constraints=constraints,
            options={
                "time_limit": arguments.time_limit,
                "mip_rel_gap": 0.0,
                "presolve": True,
            },
        )
        record: dict[str, object] = {
            "iteration": iteration + 1,
            "milp_status": int(result.status),
            "milp_message": str(result.message),
            "model": metadata,
        }
        if result.x is None:
            records.append(record)
            break

        truth = np.rint(result.x[:VERTICES]).astype(np.int64)
        raw_mask = mask_from_truth(truth)
        mask = core.complement_canonical(raw_mask, N)
        signs = signs_from_mask(mask)
        degree_certificate = core.exact_integer_separator(
            signs, core.monomial_matrix(N, 3)
        )
        if degree_certificate is None:
            record["exact_degree_three"] = False
            excluded_masks.append(raw_mask)
            records.append(record)
            continue
        record["truth_mask_hex"] = f"0x{mask:016x}"
        record["exact_degree_three"] = True
        record["degree_three_coefficients"] = [
            int(value) for value in degree_certificate[0]
        ]

        certificate, best = continuous_search(
            signs,
            arguments.seed + 100003 * iteration,
            arguments.restarts,
            arguments.max_iterations,
            scales,
        )
        record["continuous_best"] = best
        if certificate is not None:
            record["three_head_certificate"] = certificate
            key = canonical_triple(
                np.array(certificate["denominators"], dtype=np.int64)
            )
            if key not in {canonical_triple(item) for item in dictionary}:
                dictionary.append(np.array(key, dtype=np.int64))
        else:
            record["three_head_certificate"] = None
            excluded_masks.append(raw_mask)
        records.append(record)
        print(
            json.dumps(
                {
                    "iteration": iteration + 1,
                    "mask": record["truth_mask_hex"],
                    "h3_found": certificate is not None,
                    "best": best,
                }
            ),
            flush=True,
        )

    payload = {
        "status": (
            "Degree-three and reported H3 certificates are exact. MILP and "
            "continuous failures are candidate-search evidence only."
        ),
        "parameters": {
            "initial_dictionary_size": arguments.dictionary_size,
            "iterations": arguments.iterations,
            "coefficient_bound": arguments.coefficient_bound,
            "time_limit": arguments.time_limit,
            "restarts": arguments.restarts,
            "max_iterations": arguments.max_iterations,
            "seed": arguments.seed,
        },
        "final_dictionary": [item.tolist() for item in dictionary],
        "records": records,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    verify_payload(payload)
    print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
