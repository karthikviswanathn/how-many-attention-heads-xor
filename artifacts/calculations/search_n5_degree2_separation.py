#!/usr/bin/env python
"""Search five-bit quadratic thresholds for a two-head mismatch.

This is a deterministic candidate search, not an impossibility verifier.  Every
reported H2 success is converted to an exact integer cleared-score certificate.
A reported failure means only that none of the sampled valid denominator
dictionaries worked.  Proving H*(f) > 2 would require an additional global
infeasibility certificate for the denominator variables.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from scipy.optimize import differential_evolution, linprog


HERE = Path(__file__).resolve().parent
DIAGNOSTIC = HERE / "n5_mask_0x99c105ad_exact_refutation.json"


def cube(n: int) -> np.ndarray:
    return ((np.arange(1 << n)[:, None] >> np.arange(n)) & 1).astype(np.int64)


def affine_matrix(n: int) -> np.ndarray:
    return np.column_stack([np.ones(1 << n, dtype=np.int64), cube(n)])


def monomial_subsets(n: int, degree: int) -> list[tuple[int, ...]]:
    return [
        subset
        for size in range(degree + 1)
        for subset in itertools.combinations(range(n), size)
    ]


def monomial_matrix(n: int, degree: int) -> np.ndarray:
    x = cube(n)
    columns = []
    for subset in monomial_subsets(n, degree):
        if subset:
            columns.append(np.prod(x[:, subset], axis=1))
        else:
            columns.append(np.ones(1 << n, dtype=np.int64))
    return np.column_stack(columns).astype(np.int64)


def labels_from_values(values: np.ndarray) -> np.ndarray:
    assert np.all(values != 0)
    return np.where(values > 0, 1, -1).astype(np.int64)


def truth_mask(signs: np.ndarray) -> int:
    return sum(1 << index for index, sign in enumerate(signs) if sign > 0)


def signs_from_truth_mask(mask: int) -> np.ndarray:
    return np.array(
        [1 if (mask >> index) & 1 else -1 for index in range(32)],
        dtype=np.int64,
    )


def is_ltf(signs: np.ndarray, affine: np.ndarray) -> bool:
    result = linprog(
        np.zeros(affine.shape[1]),
        A_ub=-(signs[:, None] * affine),
        b_ub=-np.ones(len(signs)),
        bounds=[(None, None)] * affine.shape[1],
        method="highs",
    )
    return bool(result.success)


def one_dimensional_null_vector(matrix: np.ndarray) -> list[int]:
    """Compute a primitive integer null vector when the nullity is one."""
    rows = [list(map(Fraction, row)) for row in matrix.tolist()]
    row_count = len(rows)
    column_count = len(rows[0])
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
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


def affine_positive_circuit(signs: np.ndarray, affine: np.ndarray) -> np.ndarray:
    """Give an exact Gordan obstruction showing that the target is not an LTF."""
    signed = (signs[:, None] * affine).T
    equality = np.vstack([signed.astype(float), np.ones(len(signs))])
    target = np.concatenate([np.zeros(affine.shape[1]), [1.0]])
    result = linprog(
        np.zeros(len(signs)),
        A_eq=equality,
        b_eq=target,
        bounds=[(0.0, None)] * len(signs),
        method="highs",
    )
    if not result.success:
        raise RuntimeError("target unexpectedly passed the affine obstruction LP")
    for tolerance in (1e-7, 1e-9, 1e-11):
        support = np.flatnonzero(result.x > tolerance).tolist()
        try:
            integers = one_dimensional_null_vector(signed[:, support])
        except RuntimeError:
            continue
        if all(value < 0 for value in integers):
            integers = [-value for value in integers]
        if not all(value > 0 for value in integers):
            continue
        answer = np.zeros(len(signs), dtype=np.int64)
        answer[support] = integers
        if np.all(signed @ answer == 0):
            return answer
    raise RuntimeError("could not recover an exact affine positive circuit")


def random_quadratic(
    rng: np.random.Generator, evaluation: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return integer coefficients and odd nonzero values on the cube."""
    coefficients = rng.integers(-8, 9, size=evaluation.shape[1], dtype=np.int64)
    while not np.any(coefficients[6:] != 0):
        coefficients[6:] = rng.integers(-8, 9, size=len(coefficients) - 6)
    coefficients[0] = 0
    raw = evaluation @ coefficients
    threshold = int(np.sort(raw)[15])
    coefficients *= 2
    coefficients[0] -= 2 * threshold + 1
    values = evaluation @ coefficients
    assert np.all(values % 2 != 0)
    return coefficients, values


def random_denominator(n: int, rng: np.random.Generator) -> np.ndarray:
    orientation = int(rng.choice([-1, 1]))
    slopes = orientation * rng.integers(1, 33, size=n, dtype=np.int64)
    if orientation > 0:
        constant = int(rng.integers(1, 33))
    else:
        constant = int(-slopes.sum() + rng.integers(1, 33))
    return np.concatenate([[constant], slopes]).astype(np.int64)


def random_denominator_with_orientation(
    n: int, rng: np.random.Generator, orientation: int
) -> np.ndarray:
    """Sample a valid denominator with a prescribed monotone orientation."""
    weights = rng.integers(1, 33, size=n, dtype=np.int64)
    if orientation > 0:
        return np.concatenate([[rng.integers(1, 33)], weights]).astype(np.int64)
    return np.concatenate(
        [[weights.sum() + rng.integers(1, 33)], -weights]
    ).astype(np.int64)


def cleared_two_head_matrix(denominators: np.ndarray) -> np.ndarray:
    affine = affine_matrix(5)
    first = affine @ denominators[0]
    second = affine @ denominators[1]
    return np.column_stack(
        [first * second, affine * second[:, None], affine * first[:, None]]
    ).astype(np.int64)


def cleared_two_head_matrix_big(denominators: list[list[int]]) -> np.ndarray:
    affine = affine_matrix(5).astype(object)
    denominator_array = np.array(denominators, dtype=object)
    first = affine @ denominator_array[0]
    second = affine @ denominator_array[1]
    return np.column_stack(
        [first * second, affine * second[:, None], affine * first[:, None]]
    ).astype(object)


def exact_integer_score(
    signs: np.ndarray, matrix: np.ndarray
) -> Optional[Tuple[np.ndarray, float]]:
    variables = matrix.shape[1]
    constraints = np.zeros((len(signs), variables + 1), dtype=float)
    constraints[:, :variables] = -(signs[:, None] * matrix)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(signs)),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
    )
    if not result.success or -result.fun <= 1e-9:
        return None

    floating = result.x[:variables]
    margin = float(np.min(signs * (matrix @ floating)))
    if margin <= 1e-10:
        return None
    row_l1 = int(np.max(np.sum(np.abs(matrix), axis=1)))
    scale = max(1, int(np.ceil((row_l1 + 1) / (2.0 * margin))))
    matrix_object = matrix.astype(object)
    signs_object = signs.astype(object)
    for _ in range(80):
        exact = np.rint(scale * floating).astype(object)
        signed_scores = signs_object * (matrix_object @ exact)
        if all(int(value) > 0 for value in signed_scores):
            maximum = max(abs(int(value)) for value in exact)
            if maximum >= (1 << 63):
                raise OverflowError(maximum)
            return np.array([int(value) for value in exact], dtype=np.int64), margin
        scale *= 2
    raise RuntimeError("could not quantize a positive-margin score")


def exact_integer_score_big(
    signs: np.ndarray, matrix: np.ndarray
) -> Optional[Tuple[list[int], float]]:
    floating_matrix = np.array(matrix, dtype=float)
    norms = np.linalg.norm(floating_matrix, axis=0)
    normalized = floating_matrix / np.where(norms > 0, norms, 1.0)
    variables = normalized.shape[1]
    constraints = np.zeros((len(signs), variables + 1), dtype=float)
    constraints[:, :variables] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(signs)),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
    )
    if not result.success or -result.fun <= 1e-12:
        return None
    unnormalized = result.x[:variables] / norms
    margin = float(np.min(signs * (normalized @ result.x[:variables])))
    row_l1 = max(sum(abs(int(value)) for value in row) for row in matrix.tolist())
    scale = max(1, int(math.ceil((row_l1 + 1) / (2.0 * margin))))
    signs_object = signs.astype(object)
    for _ in range(120):
        exact = [int(round(scale * float(value))) for value in unnormalized]
        signed_scores = signs_object * (matrix @ np.array(exact, dtype=object))
        if all(int(value) > 0 for value in signed_scores):
            return exact, margin
        scale *= 2
    return None


def exact_score_from_big_denominators(
    signs: np.ndarray, denominators: list[list[int]]
) -> Optional[Tuple[list[int], float]]:
    """Solve in direct ratio coordinates, then verify the cleared score exactly."""
    affine_float = affine_matrix(5).astype(float)
    denominator_float = np.array(denominators, dtype=float)
    values = affine_float @ denominator_float.T
    features = np.column_stack(
        [
            np.ones(32),
            affine_float / values[:, 0, None],
            affine_float / values[:, 1, None],
        ]
    )
    norms = np.linalg.norm(features, axis=0)
    normalized = features / norms
    variables = normalized.shape[1]
    constraints = np.zeros((len(signs), variables + 1), dtype=float)
    constraints[:, :variables] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(signs)),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
    )
    if not result.success or -result.fun <= 1e-12:
        return None
    unnormalized = result.x[:variables] / norms
    margin = float(np.min(signs * (features @ unnormalized)))
    if margin <= 1e-12:
        return None
    matrix = cleared_two_head_matrix_big(denominators)
    row_l1 = max(sum(abs(int(value)) for value in row) for row in matrix.tolist())
    scale = max(1, int(math.ceil((row_l1 + 1) / (2.0 * margin))))
    signs_object = signs.astype(object)
    for _ in range(160):
        exact = [int(round(scale * float(value))) for value in unnormalized]
        signed_scores = signs_object * (matrix @ np.array(exact, dtype=object))
        if all(int(value) > 0 for value in signed_scores):
            return exact, margin
        scale *= 2
    return None


def floating_margin(signs: np.ndarray, features: np.ndarray) -> float:
    norms = np.linalg.norm(features, axis=0)
    normalized = features / np.where(norms > 0, norms, 1.0)
    variables = normalized.shape[1]
    constraints = np.zeros((len(signs), variables + 1), dtype=float)
    constraints[:, :variables] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(signs)),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
    )
    return float(-result.fun) if result.success else -1.0


def denominators_from_log_weights(
    log_weights: np.ndarray, orientations: tuple[int, int]
) -> tuple[np.ndarray, np.ndarray]:
    x = cube(5).astype(float)
    values = []
    for h, orientation in enumerate(orientations):
        weights = np.exp(np.clip(log_weights[5 * h : 5 * (h + 1)], -12, 12))
        if orientation > 0:
            values.append(1.0 + x @ weights)
        else:
            values.append(1.0 + (1.0 - x) @ weights)
    return values[0], values[1]


def continuous_features(
    log_weights: np.ndarray, orientations: tuple[int, int]
) -> np.ndarray:
    affine = affine_matrix(5).astype(float)
    first, second = denominators_from_log_weights(log_weights, orientations)
    return np.column_stack(
        [np.ones(32), affine / first[:, None], affine / second[:, None]]
    )


def integer_denominators_from_log_weights(
    log_weights: np.ndarray,
    orientations: tuple[int, int],
    scale: int,
) -> np.ndarray:
    denominators = []
    for h, orientation in enumerate(orientations):
        weights = np.exp(np.clip(log_weights[5 * h : 5 * (h + 1)], -12, 12))
        slopes = np.maximum(1, np.rint(scale * weights).astype(np.int64))
        if orientation > 0:
            denominators.append(np.concatenate([[scale], slopes]))
        else:
            denominators.append(np.concatenate([[scale + int(slopes.sum())], -slopes]))
    return np.array(denominators, dtype=np.int64)


def big_integer_denominators_from_log_weights(
    log_weights: np.ndarray,
    orientations: tuple[int, int],
    scale: int,
) -> list[list[int]]:
    denominators = []
    for h, orientation in enumerate(orientations):
        weights = np.exp(np.clip(log_weights[5 * h : 5 * (h + 1)], -12, 12))
        slopes = [max(1, int(round(scale * float(weight)))) for weight in weights]
        if orientation > 0:
            denominators.append([scale] + slopes)
        else:
            denominators.append([scale + sum(slopes)] + [-value for value in slopes])
    return denominators


def continuous_search_target(
    signs: np.ndarray,
    seed: int,
    max_iterations: int = 120,
) -> dict[str, object]:
    """Optimize denominator weights, then rationalize any successful result."""
    orientation_pairs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    best_margin = -1.0
    best_record = None
    for index, orientations in enumerate(orientation_pairs):
        def objective(log_weights: np.ndarray) -> float:
            return -floating_margin(
                signs, continuous_features(log_weights, orientations)
            )

        result = differential_evolution(
            objective,
            bounds=[(-8.0, 8.0)] * 10,
            seed=seed + index,
            maxiter=max_iterations,
            popsize=8,
            polish=False,
            updating="immediate",
            workers=1,
        )
        margin = -float(result.fun)
        if margin > best_margin:
            best_margin = margin
            best_record = (result.x.copy(), orientations)
        if margin <= 1e-9:
            continue
        for scale in (100, 1_000, 10_000, 100_000, 1_000_000):
            denominators = integer_denominators_from_log_weights(
                result.x, orientations, scale
            )
            exact = exact_integer_score(
                signs, cleared_two_head_matrix(denominators)
            )
            if exact is None:
                continue
            coefficients, exact_margin = exact
            return {
                "found": True,
                "method": "continuous-denominator-optimization",
                "orientations": list(orientations),
                "scale": scale,
                "denominators": denominators.tolist(),
                "cleared_score_coefficients": coefficients.tolist(),
                "floating_margin": exact_margin,
                "optimized_normalized_margin": margin,
            }
        for scale in (10**8, 10**10, 10**12, 10**14):
            denominators = big_integer_denominators_from_log_weights(
                result.x, orientations, scale
            )
            exact = exact_score_from_big_denominators(signs, denominators)
            if exact is None:
                continue
            coefficients, exact_margin = exact
            return {
                "found": True,
                "method": "continuous-denominator-optimization-bigint",
                "orientations": list(orientations),
                "scale": scale,
                "denominators": denominators,
                "cleared_score_coefficients": coefficients,
                "floating_margin": exact_margin,
                "optimized_normalized_margin": margin,
            }
    return {
        "found": False,
        "method": "continuous-denominator-optimization",
        "max_iterations": max_iterations,
        "best_normalized_margin": best_margin,
        "best_log_weights": best_record[0].tolist() if best_record else None,
        "best_orientations": list(best_record[1]) if best_record else None,
    }


def search_target(
    signs: np.ndarray,
    rng: np.random.Generator,
    trials: int,
) -> dict[str, object]:
    best_margin = -1.0
    for trial in range(trials):
        denominators = np.array(
            [random_denominator(5, rng), random_denominator(5, rng)],
            dtype=np.int64,
        )
        matrix = cleared_two_head_matrix(denominators)
        result = exact_integer_score(signs, matrix)
        if result is None:
            continue
        coefficients, margin = result
        best_margin = max(best_margin, margin)
        return {
            "found": True,
            "trial": trial,
            "denominators": denominators.tolist(),
            "cleared_score_coefficients": coefficients.tolist(),
            "floating_margin": margin,
        }
    return {"found": False, "trials": trials, "best_certified_margin": best_margin}


def search_target_orientation_cycle(
    signs: np.ndarray,
    rng: np.random.Generator,
    trials: int,
) -> dict[str, object]:
    """Search while cycling deterministically through all orientation pairs."""
    orientation_pairs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    for trial in range(trials):
        orientations = orientation_pairs[trial % len(orientation_pairs)]
        denominators = np.array(
            [
                random_denominator_with_orientation(5, rng, orientations[0]),
                random_denominator_with_orientation(5, rng, orientations[1]),
            ],
            dtype=np.int64,
        )
        result = exact_integer_score(
            signs, cleared_two_head_matrix(denominators)
        )
        if result is None:
            continue
        coefficients, margin = result
        return {
            "found": True,
            "method": "orientation-cycle-random-search",
            "trial": trial,
            "orientations": list(orientations),
            "denominators": denominators.tolist(),
            "cleared_score_coefficients": coefficients.tolist(),
            "floating_margin": margin,
        }
    return {
        "found": False,
        "method": "orientation-cycle-random-search",
        "trials": trials,
    }


def verify_payload(payload: dict[str, object]) -> None:
    quadratic = monomial_matrix(5, 2)
    affine = affine_matrix(5)
    records = payload["records"]
    for record in records:
        polynomial = np.array(record["quadratic_coefficients"], dtype=np.int64)
        values = quadratic @ polynomial
        signs = labels_from_values(values)
        assert f"0x{truth_mask(signs):08x}" == record["truth_mask_hex"]
        obstruction = np.array(record["affine_obstruction"], dtype=np.int64)
        assert np.all(obstruction >= 0)
        assert np.any(obstruction > 0)
        assert np.all((signs * obstruction) @ affine == 0)

        search = record["h2_search"]
        if not search["found"]:
            continue
        denominators = np.array(search["denominators"], dtype=object)
        for denominator in denominators:
            slopes = denominator[1:]
            assert np.all(slopes > 0) or np.all(slopes < 0)
            assert np.all(affine.astype(object) @ denominator > 0)
        score = np.array(search["cleared_score_coefficients"], dtype=object)
        matrix = cleared_two_head_matrix_big(denominators.tolist())
        assert np.all(signs * (matrix @ score) > 0)
    print(
        f"verified {len(records)} exact degree-two targets; "
        f"{payload['successes']} have exact two-head certificates"
    )


def verify_diagnostic(payload: dict[str, object]) -> None:
    """Verify the compact exact record for the former hard candidate."""
    truth = payload["truth_table"]
    signs = signs_from_truth_mask(int(truth["mask_hex"], 16))
    assert np.flatnonzero(signs > 0).tolist() == truth["positive_vertex_indices"]

    degree_two = payload["degree_two_certificate"]
    polynomial = np.array(degree_two["coefficients"], dtype=np.int64)
    assert np.all(signs * (monomial_matrix(5, 2) @ polynomial) > 0)
    obstruction = np.array(
        degree_two["affine_non_ltf_gordan_dual"], dtype=np.int64
    )
    assert np.all(obstruction >= 0) and np.any(obstruction > 0)
    assert np.all((signs * obstruction) @ affine_matrix(5) == 0)

    h2 = payload["exact_two_head_certificate"]
    denominators = np.array(h2["denominators"], dtype=object)
    affine = affine_matrix(5).astype(object)
    for denominator in denominators:
        slopes = denominator[1:]
        assert np.all(slopes > 0) or np.all(slopes < 0)
        assert np.all(affine @ denominator > 0)
    coefficients = np.array(h2["cleared_score_coefficients"], dtype=object)
    matrix = cleared_two_head_matrix_big(denominators.tolist())
    signed_scores = signs * (matrix @ coefficients)
    assert np.all(signed_scores > 0)
    assert min(map(int, signed_scores)) == h2["minimum_signed_cleared_score"]
    print(
        "verified compact record: mask 0x99c105ad has exact degree two "
        "and an exact two-head certificate"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=200)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260713)
    parser.add_argument(
        "--sampling",
        choices=("uniform-truth", "coefficient"),
        default="uniform-truth",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / "n5_degree2_search_results.json",
    )
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--verify-diagnostic", action="store_true")
    parser.add_argument("--refine-failures", action="store_true")
    parser.add_argument("--retry-failures", action="store_true")
    parser.add_argument("--refine-iterations", type=int, default=120)
    arguments = parser.parse_args()

    if arguments.verify_only:
        payload = json.loads(arguments.output.read_text())
        verify_payload(payload)
        return

    if arguments.verify_diagnostic:
        verify_diagnostic(json.loads(DIAGNOSTIC.read_text()))
        return

    if arguments.retry_failures:
        payload = json.loads(arguments.output.read_text())
        failures = [
            record for record in payload["records"] if not record["h2_search"]["found"]
        ]
        for index, record in enumerate(failures):
            signs = signs_from_truth_mask(int(record["truth_mask_hex"], 16))
            previous_search = record["h2_search"]
            result = search_target_orientation_cycle(
                signs,
                rng=np.random.default_rng(arguments.seed + 1000 * index),
                trials=arguments.trials,
            )
            record.setdefault("h2_search_history", []).append(previous_search)
            record["h2_search"] = result
            print(
                f"retry {index + 1}/{len(failures)}: "
                f"found={result['found']} mask={record['truth_mask_hex']}",
                flush=True,
            )
        payload["successes"] = sum(
            bool(record["h2_search"]["found"]) for record in payload["records"]
        )
        payload["failures"] = len(payload["records"]) - payload["successes"]
        payload["orientation_cycle_retry_seed"] = arguments.seed
        payload["orientation_cycle_retry_trials"] = arguments.trials
        arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
        verify_payload(payload)
        return

    if arguments.refine_failures:
        payload = json.loads(arguments.output.read_text())
        failures = [
            record for record in payload["records"] if not record["h2_search"]["found"]
        ]
        for index, record in enumerate(failures):
            signs = signs_from_truth_mask(int(record["truth_mask_hex"], 16))
            result = continuous_search_target(
                signs,
                seed=arguments.seed + 1000 * index,
                max_iterations=arguments.refine_iterations,
            )
            record["h2_search"] = result
            print(
                f"refine {index + 1}/{len(failures)}: "
                f"found={result['found']} mask={record['truth_mask_hex']}",
                flush=True,
            )
        payload["successes"] = sum(
            bool(record["h2_search"]["found"]) for record in payload["records"]
        )
        payload["failures"] = len(payload["records"]) - payload["successes"]
        payload["continuous_refinement_iterations"] = arguments.refine_iterations
        arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
        verify_payload(payload)
        print(
            json.dumps(
                {
                    "successes": payload["successes"],
                    "failures": payload["failures"],
                    "continuous_refinement_iterations": arguments.refine_iterations,
                },
                indent=2,
            )
        )
        return

    rng = np.random.default_rng(arguments.seed)
    quadratic = monomial_matrix(5, 2)
    affine = affine_matrix(5)
    records = []
    attempts = 0
    while len(records) < arguments.samples:
        attempts += 1
        if arguments.sampling == "coefficient":
            polynomial, values = random_quadratic(rng, quadratic)
            signs = labels_from_values(values)
        else:
            sampled_mask = int(rng.integers(0, 1 << 32, dtype=np.uint64))
            signs = signs_from_truth_mask(sampled_mask)
            degree2_certificate = exact_integer_score(signs, quadratic)
            if degree2_certificate is None:
                continue
            polynomial = degree2_certificate[0]
        if is_ltf(signs, affine):
            continue
        affine_obstruction = affine_positive_circuit(signs, affine)
        result = search_target(signs, rng, arguments.trials)
        record = {
            "truth_mask_hex": f"0x{truth_mask(signs):08x}",
            "positive_inputs": int(np.sum(signs > 0)),
            "quadratic_coefficients": polynomial.tolist(),
            "affine_obstruction": affine_obstruction.tolist(),
            "h2_search": result,
        }
        records.append(record)
        print(
            f"sample {len(records)}/{arguments.samples}: "
            f"found={result['found']} mask={record['truth_mask_hex']}",
            flush=True,
        )

    payload = {
        "status": (
            "Every success is exact.  A failure is only a search failure and is not "
            "a lower bound on head complexity."
        ),
        "seed": arguments.seed,
        "sampling": arguments.sampling,
        "requested_samples": arguments.samples,
        "quadratic_draws": attempts,
        "denominator_trials_per_sample": arguments.trials,
        "successes": sum(bool(record["h2_search"]["found"]) for record in records),
        "failures": sum(not bool(record["h2_search"]["found"]) for record in records),
        "records": records,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({key: payload[key] for key in payload if key != "records"}, indent=2))


if __name__ == "__main__":
    main()
