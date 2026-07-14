#!/usr/bin/env python3
"""Find exact H4 shattering certificates for degree-four cocircuit families.

Fix an affine normal with cube zero set Z.  Away from Z, the parity-twisted
target signs are forced; on Z they are arbitrary.  A fixed four-head tangent
space covers the whole family if its restriction to Z is surjective and its
kernel on Z contains one score with the forced strict signs away from Z.
Indeed, interpolate any requested values on Z and add a sufficiently large
multiple of the kernel score to preserve all off-Z signs.

The search uses floating point only to choose promising denominator tuples.
Every emitted record contains an integer kernel score, and the verifier checks
surjectivity by an exact modular rank computation.  Dictionary misses are not
lower bounds.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

import screen_n5_degree4_cocircuit_families as families
import search_adversarial_low_dimension as core
import verify_n5_degree4_reduction as reduction


N = 5
HEADS = 4
WIDTH = N + 1
VERTICES = 1 << N
PRIME = 1_000_003
HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n5_degree4_family_shattering_certificates.json"
TARGET_LOG_SPANS = (4.0, 7.0, 10.0, 14.0)
STRUCTURALLY_OBSTRUCTED_ORBITS = frozenset({62})


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


def valid_denominators(denominators: np.ndarray) -> bool:
    if denominators.shape != (HEADS, WIDTH):
        return False
    affine = core.affine_matrix(N).astype(object)
    values = affine @ denominators.astype(object).T
    return bool(
        np.all(values > 0)
        and all(
            np.all(row[1:] > 0) or np.all(row[1:] < 0)
            for row in denominators
        )
    )


def forced_data(
    normal: tuple[int, ...]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    features = reduction.affine_features().astype(np.int64)
    values = features @ np.array(normal, dtype=np.int64)
    zero = np.flatnonzero(values == 0)
    off_zero = np.flatnonzero(values != 0)
    parity = np.array(
        [
            1 if bin(vertex).count("1") % 2 == 0 else -1
            for vertex in range(VERTICES)
        ],
        dtype=np.int64,
    )
    forced = np.sign(values[off_zero]).astype(np.int64) * parity[off_zero]
    return zero, off_zero, forced


def column_basis(denominators: np.ndarray) -> np.ndarray:
    affine = core.affine_matrix(N).astype(float)
    values = affine @ denominators.astype(float).T
    raw = np.column_stack(
        [np.ones(VERTICES)]
        + [affine / values[:, head, None] for head in range(HEADS)]
    )
    left, singular, _ = np.linalg.svd(raw, full_matrices=False)
    keep = singular > 1e-11 * singular[0]
    return left[:, keep]


def numerical_shattering_margin(
    normal: tuple[int, ...], denominators: np.ndarray
) -> float | None:
    zero, off_zero, forced = forced_data(normal)
    basis = column_basis(denominators)
    _, singular, right = np.linalg.svd(
        basis[zero], full_matrices=True
    )
    if len(zero):
        rank = int(np.sum(singular > 1e-10 * singular[0]))
    else:
        rank = 0
    if rank != len(zero):
        return None
    kernel = right[rank:].T
    signed = forced[:, None] * (basis[off_zero] @ kernel)
    variables = kernel.shape[1]
    constraints = np.zeros((len(off_zero), variables + 1))
    constraints[:, :variables] = -signed
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(off_zero)),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
    )
    if not result.success or -float(result.fun) <= 1e-9:
        return None
    return -float(result.fun)


def integer_nullspace_basis(matrix: np.ndarray) -> np.ndarray:
    """Return integer columns spanning the rational right nullspace."""
    rows = [list(map(Fraction, row)) for row in matrix.tolist()]
    row_count = len(rows)
    column_count = len(rows[0])
    pivots: list[int] = []
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
    basis = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(column_count)]
        vector[free_column] = Fraction(1)
        for row, pivot in reversed(list(enumerate(pivots))):
            vector[pivot] = -sum(
                rows[row][column] * vector[column]
                for column in range(pivot + 1, column_count)
            )
        denominator_lcm = 1
        for value in vector:
            denominator_lcm = math.lcm(
                denominator_lcm, value.denominator
            )
        integers = [int(value * denominator_lcm) for value in vector]
        common = 0
        for value in integers:
            common = math.gcd(common, abs(value))
        basis.append([value // common for value in integers])
    answer = np.array(basis, dtype=object).T
    assert np.all(matrix.astype(object) @ answer == 0)
    return answer


def modular_rank(matrix: np.ndarray, prime: int = PRIME) -> int:
    rows = [
        [int(value) % prime for value in row]
        for row in matrix.astype(object).tolist()
    ]
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], prime - 2, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for row in range(row_count):
            if row == rank or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                (rows[row][index] - factor * rows[rank][index]) % prime
                for index in range(column_count)
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def exact_integer_separator_all_columns(
    signs: np.ndarray, matrix: np.ndarray
) -> tuple[np.ndarray, float] | None:
    """Find an integer separator without dropping small exact columns.

    Exact nullspace bases can have wildly different integer column scales.
    Relative floating thresholds would incorrectly discard small but essential
    columns, so every exactly nonzero column is normalized separately.
    """
    exact_matrix = matrix.astype(object)
    exact_scales = np.array(
        [
            max(abs(int(value)) for value in exact_matrix[:, column])
            for column in range(exact_matrix.shape[1])
        ],
        dtype=object,
    )
    keep = np.array([scale > 0 for scale in exact_scales], dtype=bool)
    kept_columns = np.flatnonzero(keep)
    normalized = np.column_stack(
        [
            np.array(
                [
                    float(Fraction(int(value), int(exact_scales[column])))
                    for value in exact_matrix[:, column]
                ]
            )
            for column in kept_columns
        ]
    )
    variables = normalized.shape[1]
    constraints = np.zeros((len(signs), variables + 1))
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
    if not result.success or -float(result.fun) <= 1e-12:
        return None
    floating_coefficients = result.x[:variables]
    margin = float(
        np.min(signs * (normalized @ floating_coefficients))
    )
    if margin <= 1e-12:
        return None
    exact_signs = signs.astype(object)
    for maximum_denominator in (10, 100, 1_000, 10_000, 100_000, 1_000_000):
        rational_coefficients = [Fraction(0) for _ in range(matrix.shape[1])]
        for index, column in enumerate(kept_columns):
            numerator = Fraction(
                float(floating_coefficients[index])
            ).limit_denominator(maximum_denominator)
            if numerator:
                rational_coefficients[column] = numerator / int(
                    exact_scales[column]
                )
        common_denominator = 1
        for coefficient in rational_coefficients:
            common_denominator = math.lcm(
                common_denominator, coefficient.denominator
            )
        integers = np.array(
            [
                int(coefficient * common_denominator)
                for coefficient in rational_coefficients
            ],
            dtype=object,
        )
        common = 0
        for value in integers:
            common = math.gcd(common, abs(int(value)))
        if common > 1:
            integers //= common
        if min(exact_signs * (exact_matrix @ integers)) > 0:
            return integers, margin
    return None


def exact_shattering_certificate(
    normal: tuple[int, ...], denominators: np.ndarray
) -> dict[str, object] | None:
    if not valid_denominators(denominators):
        return None
    zero, off_zero, forced = forced_data(normal)
    matrix = cleared_matrix(denominators)
    if modular_rank(matrix[zero]) != len(zero):
        return None
    kernel = integer_nullspace_basis(matrix[zero])
    kernel_values = matrix @ kernel
    assert np.all(kernel_values[zero] == 0)
    separator = exact_integer_separator_all_columns(
        forced, kernel_values[off_zero]
    )
    if separator is None:
        return None
    kernel_coefficients, floating_margin = separator
    score_coefficients = kernel @ kernel_coefficients
    values = matrix @ score_coefficients
    assert np.all(values[zero] == 0)
    signed = forced.astype(object) * values[off_zero]
    minimum = int(min(signed))
    assert minimum > 0
    return {
        "normal": list(normal),
        "normal_orbit_key": list(reduction.normal_orbit_key(normal)),
        "zero_vertices": [int(vertex) for vertex in zero],
        "denominators": denominators.tolist(),
        "kernel_score_coefficients": [
            int(value) for value in score_coefficients
        ],
        "minimum_signed_off_zero_score": minimum,
        "restriction_rank_prime": PRIME,
        "floating_kernel_margin": float(floating_margin),
    }


def targeted_random_denominators(
    rng: np.random.Generator, trial: int
) -> tuple[np.ndarray, int, float]:
    """Draw one deterministic log-uniform tuple for a prescribed orientation count."""
    positive_heads = trial % (HEADS + 1)
    log_span = TARGET_LOG_SPANS[(trial // (HEADS + 1)) % len(TARGET_LOG_SPANS)]
    orientations = np.array(
        [1] * positive_heads + [-1] * (HEADS - positive_heads),
        dtype=np.int64,
    )
    rng.shuffle(orientations)
    literal_weights = np.exp(
        rng.uniform(0.0, log_span, size=(HEADS, WIDTH))
    )
    denominators = np.vstack(
        [
            families.oriented_denominator(
                literal_weights[head], int(orientations[head])
            )
            for head in range(HEADS)
        ]
    )
    canonical = np.array(
        families.canonical_tuple(denominators), dtype=np.int64
    )
    assert valid_denominators(canonical)
    return canonical, positive_heads, log_span


def targeted_random_certificate(
    normal: tuple[int, ...],
    orbit: int,
    seed: int,
    trials: int,
) -> tuple[dict[str, object] | None, dict[str, object]]:
    """Exactify every numerical hit while recording the best observed margin."""
    rng = np.random.default_rng(
        np.random.SeedSequence([seed, orbit, 0x48345F544152474554])
    )
    best_margin: float | None = None
    numerical_hits = 0
    exact_attempts = 0
    for trial in range(trials):
        denominators, positive_heads, log_span = targeted_random_denominators(
            rng, trial
        )
        margin = numerical_shattering_margin(normal, denominators)
        if margin is None:
            continue
        numerical_hits += 1
        if best_margin is None or margin > best_margin:
            best_margin = margin
        exact_attempts += 1
        certificate = exact_shattering_certificate(normal, denominators)
        if certificate is not None:
            certificate.update(
                {
                    "orbit_index": orbit,
                    "search_source": "targeted_random",
                    "targeted_trial": trial,
                    "targeted_positive_heads": positive_heads,
                    "targeted_log_span": log_span,
                    "targeted_numerical_margin": margin,
                }
            )
            return certificate, {
                "trials_run": trial + 1,
                "numerical_hits": numerical_hits,
                "exact_attempts": exact_attempts,
                "best_numerical_margin": best_margin,
            }
    return None, {
        "trials_run": trials,
        "numerical_hits": numerical_hits,
        "exact_attempts": exact_attempts,
        "best_numerical_margin": best_margin,
    }


def verify_record(record: dict[str, object]) -> None:
    normal = tuple(int(value) for value in record["normal"])
    assert list(reduction.normal_orbit_key(normal)) == record[
        "normal_orbit_key"
    ]
    denominators = np.array(record["denominators"], dtype=object)
    assert valid_denominators(denominators)
    zero, off_zero, forced = forced_data(normal)
    assert [int(vertex) for vertex in zero] == record["zero_vertices"]
    matrix = cleared_matrix(denominators)
    prime = int(record["restriction_rank_prime"])
    assert modular_rank(matrix[zero], prime) == len(zero)
    coefficients = np.array(
        record["kernel_score_coefficients"], dtype=object
    )
    values = matrix @ coefficients
    assert np.all(values[zero] == 0)
    signed = forced.astype(object) * values[off_zero]
    minimum = int(min(signed))
    assert minimum > 0
    assert minimum == int(record["minimum_signed_off_zero_score"])


def verify_payload(payload: dict[str, object]) -> None:
    keys = set()
    for record in payload["records"]:
        verify_record(record)
        key = tuple(record["normal_orbit_key"])
        assert key not in keys
        keys.add(key)
    assert len(keys) == int(payload["exact_family_count"])
    print(
        f"verified exact H4 shattering for {len(keys)} cocircuit families",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary-size", type=int, default=256)
    parser.add_argument("--targeted-trials", type=int, default=5_000)
    parser.add_argument(
        "--targeted-size16-trials",
        type=int,
        default=4_000,
        help=(
            "Fixed-space trials for size-16 families other than the known "
            "structural obstruction at orbit 62."
        ),
    )
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_payload(json.loads(arguments.output.read_text()))
        return

    normals = families.orbit_normals()
    dictionary = families.denominator_dictionary(
        arguments.dictionary_size, arguments.seed
    )
    records = []
    misses = []
    for orbit, normal in enumerate(normals):
        candidates = []
        for index, denominators in enumerate(dictionary):
            margin = numerical_shattering_margin(normal, denominators)
            if margin is not None:
                candidates.append((margin, index, denominators))
        candidates.sort(key=lambda item: item[0], reverse=True)
        certificate = None
        for _, dictionary_index, denominators in candidates:
            certificate = exact_shattering_certificate(normal, denominators)
            if certificate is not None:
                certificate["orbit_index"] = orbit
                certificate["dictionary_index"] = dictionary_index
                certificate["search_source"] = "shared_dictionary"
                break
        targeted_statistics = None
        zero_size = len(forced_data(normal)[0])
        if orbit in STRUCTURALLY_OBSTRUCTED_ORBITS:
            targeted_trials = 0
        elif zero_size == 16:
            targeted_trials = arguments.targeted_size16_trials
        else:
            targeted_trials = arguments.targeted_trials
        if certificate is None and targeted_trials:
            certificate, targeted_statistics = targeted_random_certificate(
                normal,
                orbit,
                arguments.seed,
                targeted_trials,
            )
        if certificate is None:
            miss = {
                "orbit_index": orbit,
                "normal": list(normal),
                "normal_orbit_key": list(
                    reduction.normal_orbit_key(normal)
                ),
                "zero_size": zero_size,
                "numerical_candidate_count": len(candidates),
                "targeted_trials_requested": targeted_trials,
            }
            if targeted_statistics is not None:
                miss["targeted_statistics"] = targeted_statistics
            misses.append(miss)
            print(
                f"orbit={orbit} exact family miss zero={zero_size} "
                f"targeted={targeted_trials}",
                flush=True,
            )
        else:
            records.append(certificate)
            if certificate["search_source"] == "shared_dictionary":
                search_detail = f"dictionary={certificate['dictionary_index']}"
            else:
                search_detail = (
                    f"targeted_trial={certificate['targeted_trial']} "
                    f"positive_heads={certificate['targeted_positive_heads']}"
                )
            print(
                f"orbit={orbit} exact family hit "
                f"zero={len(certificate['zero_vertices'])} "
                f"{search_detail}",
                flush=True,
            )

    payload = {
        "status": (
            "Every listed family is covered exactly by one fixed H4 tangent "
            "space via restriction surjectivity and an off-zero kernel "
            "separator. Dictionary misses are not lower bounds."
        ),
        "dictionary_size": len(dictionary),
        "targeted_trials_per_non_size16_miss": arguments.targeted_trials,
        "targeted_trials_per_size16_miss": arguments.targeted_size16_trials,
        "targeted_log_spans": list(TARGET_LOG_SPANS),
        "structurally_obstructed_orbits": sorted(
            STRUCTURALLY_OBSTRUCTED_ORBITS
        ),
        "seed": arguments.seed,
        "exact_family_count": len(records),
        "total_normal_orbits": len(normals),
        "records": records,
        "misses": misses,
    }
    verify_payload(payload)
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
