#!/usr/bin/env python3
"""Strong active search for a six-bit cubic versus three-head gap.

The initial MILP dictionary contains every persisted exact three-head
denominator triple from earlier six-bit searches.  It also contains sampled
coordinate permutations of those triples, both historical active dictionaries,
and fresh random triples.  The MILP enforces a shared positive lower bound on
every active Gordan weight for every dictionary triple.  With the truth table
fixed, a follow-up LP maximizes and records that bound.  This favors sign cells
with robust, full-support fixed-dictionary obstructions.

Every returned truth table receives exact threshold-degree certificates and an
exact fixed-dictionary screen.  The nonlinear screen visits every orientation
separately and LP-tests every optimized denominator triple, even when the
smooth numerator fit is poor.  Exact three-head successes are fed back into
later MILPs.  A survivor remains candidate-search evidence only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, milp

import search_adversarial_low_dimension as core
import search_uncovered_cubic_n6 as cubic
import verify_n6_cubic_candidate_refutations as latest_refutations
import verify_n6_cubic_hard_candidate as hard_refutation


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "uncovered_cubic_n6_strong_results.json"
HISTORY_FILES = (
    HERE / "uncovered_cubic_n6_results.json",
    HERE / "uncovered_cubic_n6_lp_refined.json",
)

# This certificate was found while benchmarking the strong initial dictionary.
# It is kept here so its denominator triple cuts every subsequent campaign.
BOOTSTRAP_CERTIFICATES = (
    {
        "truth_mask_hex": "0x377e7bb3f9cfcdcd",
        "denominators": (
            (1000003, -363, -999632, -1, -4, -1, -1),
            (1000000, -23, -80, -305089, -1, -2, -694802),
            (1000001, -7, -999812, -1, -7, -172, -1),
        ),
        "score_coefficients": (
            -52813480134643900416,
            11350046307598304114900992,
            -8982049255404468116127744,
            11350046307675738080280576,
            -5238613426530024154988544,
            -178430655919523085942784,
            1327671260580239208611840,
            -13228513752124552273461248,
            34937266681768298856579072,
            11698679676646809162219520,
            -10741944297120140533694464,
            -10527527964635602953961472,
            4565313803028657648697344,
            -7131099909631842782806016,
            -17274497324502504787935232,
            8028590865293448595898368,
            -7852399035684170045063168,
            -13225388923062892768526336,
            2042887493798572832325632,
            -5388270515087276582633472,
            9933754257084873017655296,
            389782466354560590938112,
        ),
        "minimum_signed_cleared_score": 37939500396415617073152,
    },
)


def valid_denominators(denominators: np.ndarray) -> bool:
    affine = core.affine_matrix(cubic.N).astype(object)
    exact = denominators.astype(object)
    if exact.shape != (cubic.HEADS, cubic.WIDTH):
        return False
    if not np.all(affine @ exact.T > 0):
        return False
    return all(
        np.all(row[1:] > 0) or np.all(row[1:] < 0) for row in exact
    )


def verify_head_certificate(mask: int, certificate: dict[str, object]) -> int:
    denominators = np.array(certificate["denominators"], dtype=object)
    assert valid_denominators(denominators)
    coefficients = np.array(certificate["score_coefficients"], dtype=object)
    assert len(coefficients) == 1 + cubic.HEADS * cubic.WIDTH
    target = cubic.signs_from_mask(mask).astype(object)
    signed = target * (cubic.cleared_matrix(denominators) @ coefficients)
    minimum = int(min(signed))
    assert minimum > 0
    expected = certificate.get("minimum_signed_cleared_score")
    if expected is not None:
        assert minimum == int(expected)
    return minimum


def certified_seed_triples(
    prior_output: Path | None = None,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    seen: set[tuple[tuple[int, ...], ...]] = set()

    def add(
        source: str,
        mask: int,
        denominators: object,
        score_coefficients: object,
        minimum: int,
    ) -> None:
        certificate = {
            "denominators": denominators,
            "score_coefficients": score_coefficients,
            "minimum_signed_cleared_score": minimum,
        }
        verify_head_certificate(mask, certificate)
        key = cubic.canonical_triple(
            np.array(denominators, dtype=np.int64)
        )
        if key in seen:
            return
        seen.add(key)
        records.append(
            {
                "source": source,
                "truth_mask_hex": f"0x{mask:016x}",
                "denominators": [list(row) for row in key],
            }
        )

    for path in HISTORY_FILES + ((prior_output,) if prior_output else ()):
        if path is None or not path.exists():
            continue
        payload = json.loads(path.read_text())
        for record in payload.get("records", []):
            certificate = record.get("three_head_certificate")
            mask_hex = record.get("truth_mask_hex")
            if certificate is None or mask_hex is None:
                continue
            add(
                path.name,
                int(mask_hex, 16),
                certificate["denominators"],
                certificate["score_coefficients"],
                int(certificate["minimum_signed_cleared_score"]),
            )

    for certificate in latest_refutations.CERTIFICATES:
        add(
            "verify_n6_cubic_candidate_refutations.py",
            int(certificate["truth_mask"]),
            certificate["denominators"],
            certificate["head_score_coefficients"],
            int(certificate["minimum_signed_cleared_score"]),
        )

    add(
        "verify_n6_cubic_hard_candidate.py",
        hard_refutation.TRUTH_MASK,
        hard_refutation.DENOMINATORS,
        hard_refutation.HEAD_SCORE_COEFFICIENTS,
        hard_refutation.MINIMUM_SIGNED_CLEARED_SCORE,
    )

    for certificate in BOOTSTRAP_CERTIFICATES:
        add(
            "search_uncovered_cubic_n6_strong.py bootstrap",
            int(certificate["truth_mask_hex"], 16),
            certificate["denominators"],
            certificate["score_coefficients"],
            int(certificate["minimum_signed_cleared_score"]),
        )
    return records


def historical_dictionary(prior_output: Path | None = None) -> list[np.ndarray]:
    answer = []
    for path in HISTORY_FILES + ((prior_output,) if prior_output else ()):
        if path is None or not path.exists():
            continue
        payload = json.loads(path.read_text())
        for triple in payload.get("final_dictionary", []):
            answer.append(np.array(triple, dtype=np.int64))
        for campaign in payload.get("campaigns", []):
            for triple in campaign.get("final_dictionary", []):
                answer.append(np.array(triple, dtype=np.int64))
    return answer


def permute_coordinates(
    denominators: np.ndarray, permutation: tuple[int, ...]
) -> np.ndarray:
    columns = [0] + [coordinate + 1 for coordinate in permutation]
    return denominators[:, columns]


def active_dictionary(
    size: int,
    seed: int,
    certified: list[dict[str, object]],
    learned: list[np.ndarray],
    prior_output: Path | None,
) -> tuple[list[np.ndarray], dict[str, int]]:
    answer: list[np.ndarray] = []
    seen: set[tuple[tuple[int, ...], ...]] = set()
    source_counts: dict[str, int] = {}

    def add(triple: object, source: str) -> None:
        key = cubic.canonical_triple(np.array(triple, dtype=np.int64))
        if key in seen:
            return
        array = np.array(key, dtype=np.int64)
        assert valid_denominators(array)
        seen.add(key)
        answer.append(array)
        source_counts[source] = source_counts.get(source, 0) + 1

    for record in certified:
        add(record["denominators"], "exact certificates")
    for triple in learned:
        add(triple, "learned certificates")
    if len(answer) > size:
        raise ValueError(
            f"dictionary size {size} is smaller than {len(answer)} exact cuts"
        )

    rng = np.random.default_rng(seed)
    priority = list(answer)
    for _ in range(2):
        for triple in priority:
            permutation = tuple(int(value) for value in rng.permutation(cubic.N))
            add(permute_coordinates(triple, permutation), "coordinate orbits")
            if len(answer) >= size:
                return answer, source_counts

    for triple in historical_dictionary(prior_output):
        add(triple, "historical dictionaries")
        if len(answer) >= size:
            return answer, source_counts

    for triple in cubic.random_dictionary(4 * size, seed + 17):
        add(triple, "fresh random")
        if len(answer) >= size:
            return answer, source_counts
    raise RuntimeError("could not fill the requested active dictionary")


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


def quadratic_positive_circuit(signs: np.ndarray) -> dict[str, object]:
    evaluation = core.monomial_matrix(cubic.N, 2)
    signed = (signs[:, None] * evaluation).T
    equality = np.vstack(
        [signed.astype(float), np.ones(cubic.VERTICES, dtype=float)]
    )
    target = np.concatenate([np.zeros(signed.shape[0]), [1.0]])
    rng = np.random.default_rng(620260714)
    objectives = [np.zeros(cubic.VERTICES)] + [
        1e-7 * rng.standard_normal(cubic.VERTICES) for _ in range(24)
    ]
    for objective in objectives:
        result = linprog(
            objective,
            A_eq=equality,
            b_eq=target,
            bounds=[(0.0, None)] * cubic.VERTICES,
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
            if np.all(
                signed[:, support].astype(object)
                @ np.array(weights, dtype=object)
                == 0
            ):
                return {"support": support, "weights": weights}
    raise RuntimeError("could not recover an exact quadratic Gordan circuit")


def exact_fixed_dictionary_hit(
    signs: np.ndarray, dictionary: list[np.ndarray]
) -> dict[str, object] | None:
    for index, denominators in enumerate(dictionary):
        certificate = cubic.exact_head_certificate(signs, denominators)
        if certificate is not None:
            certificate["dictionary_index"] = index
            return certificate
    return None


def fixed_truth_uniform_circuit_floor(
    signs: np.ndarray, dictionary: list[np.ndarray]
) -> dict[str, object]:
    floors = []
    for denominators in dictionary:
        features = cubic.whitened_features(denominators)
        signed = signs[:, None].astype(float) * features
        variable_count = cubic.VERTICES + 1
        objective = np.zeros(variable_count)
        objective[-1] = -1.0
        equality = np.zeros((features.shape[1] + 1, variable_count))
        equality[: features.shape[1], : cubic.VERTICES] = signed.T
        equality[-1, : cubic.VERTICES] = 1.0
        target = np.zeros(features.shape[1] + 1)
        target[-1] = 1.0
        inequality = np.zeros((cubic.VERTICES, variable_count))
        inequality[:, : cubic.VERTICES] = -np.eye(cubic.VERTICES)
        inequality[:, -1] = 1.0
        result = linprog(
            objective,
            A_ub=inequality,
            b_ub=np.zeros(cubic.VERTICES),
            A_eq=equality,
            b_eq=target,
            bounds=[(0.0, None)] * cubic.VERTICES
            + [(0.0, 1.0 / cubic.VERTICES)],
            method="highs",
        )
        if not result.success:
            floors.append(0.0)
        else:
            floors.append(float(result.x[-1]))
    values = np.array(floors, dtype=float)
    return {
        "minimum": float(np.min(values)),
        "median": float(np.median(values)),
        "maximum": float(np.max(values)),
        "minimizing_dictionary_index": int(np.argmin(values)),
    }


def deep_screen(
    signs: np.ndarray,
    base_seed: int,
    screen_seeds: int,
    restarts_per_orientation: int,
    max_iterations: int,
    scales: tuple[int, ...],
) -> tuple[dict[str, object] | None, list[dict[str, object]]]:
    attempts = []
    orientations = list(itertools.product((-1, 1), repeat=cubic.HEADS))
    for seed_index in range(screen_seeds):
        seed = base_seed + 1000003 * seed_index
        shift = seed_index % len(orientations)
        ordered = orientations[shift:] + orientations[:shift]
        for orientation in ordered:
            certificate, best = cubic.continuous_search(
                signs,
                seed + sum((index + 11) * value for index, value in enumerate(orientation)),
                restarts_per_orientation,
                max_iterations,
                scales,
                orientation_filter=orientation,
                lp_accuracy_threshold=0,
            )
            attempts.append(
                {
                    "seed": seed,
                    "orientation": list(orientation),
                    "best": best,
                }
            )
            if certificate is not None:
                certificate["screen_seed"] = seed
                return certificate, attempts
    return None, attempts


def survivor_diagnostics(attempts: list[dict[str, object]]) -> dict[str, object]:
    orientation_best: dict[str, dict[str, object]] = {}
    wrong_sets = []
    for attempt in attempts:
        best = attempt["best"]
        if not best:
            continue
        key = "".join("+" if value > 0 else "-" for value in attempt["orientation"])
        previous = orientation_best.get(key)
        rank = (int(best["accuracy"]), float(best["minimum_signed_score"]))
        if previous is None or rank > (
            int(previous["accuracy"]),
            float(previous["minimum_signed_score"]),
        ):
            theta = np.array(best["literal_weights"], dtype=float)
            orientation_best[key] = {
                "accuracy": int(best["accuracy"]),
                "minimum_signed_score": float(best["minimum_signed_score"]),
                "wrong_vertices": best["wrong_vertices"],
                "smallest_literal_weight": float(np.min(theta)),
                "largest_literal_weight": float(np.max(theta)),
                "effective_literal_counts": [
                    int(np.sum(row > 1e-5)) for row in theta
                ],
            }
        wrong_sets.append(set(int(value) for value in best["wrong_vertices"]))
    common_wrong = sorted(set.intersection(*wrong_sets)) if wrong_sets else []
    return {
        "orientation_best": orientation_best,
        "vertices_missed_by_every_smooth_fit": common_wrong,
        "interpretation": (
            "Boundary concentration and persistent missed vertices are only "
            "diagnostics for a possible singular-flat obstruction. They are "
            "not a global three-head lower bound."
        ),
    }


def verify_payload(payload: dict[str, object]) -> None:
    cubic_evaluation = core.monomial_matrix(cubic.N, 3).astype(object)
    quadratic_evaluation = core.monomial_matrix(cubic.N, 2).astype(object)
    for seed_record in payload["certified_seed_triples"]:
        assert valid_denominators(
            np.array(seed_record["denominators"], dtype=object)
        )
    for campaign in payload["campaigns"]:
        for triple in campaign["final_dictionary"]:
            assert valid_denominators(np.array(triple, dtype=object))
    for record in payload["records"]:
        mask_hex = record.get("truth_mask_hex")
        if mask_hex is None:
            continue
        mask = int(mask_hex, 16)
        signs = cubic.signs_from_mask(mask).astype(object)
        coefficients = record.get("degree_three_coefficients")
        if coefficients is not None:
            assert min(
                signs
                * (
                    cubic_evaluation
                    @ np.array(coefficients, dtype=object)
                )
            ) > 0
        circuit = record.get("quadratic_gordan_circuit")
        if circuit is not None:
            weights = np.zeros(cubic.VERTICES, dtype=object)
            weights[circuit["support"]] = np.array(
                circuit["weights"], dtype=object
            )
            assert all(int(value) > 0 for value in circuit["weights"])
            assert np.all(
                (signs[:, None] * quadratic_evaluation).T @ weights == 0
            )
        for key in ("fixed_dictionary_hit", "three_head_certificate"):
            certificate = record.get(key)
            if certificate is not None:
                verify_head_certificate(mask, certificate)
    print(
        f"verified {len(payload['records'])} strong cubic-search records",
        flush=True,
    )


def write_checkpoint(output: Path, payload: dict[str, object]) -> None:
    output.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary-size", type=int, default=128)
    parser.add_argument("--campaigns", type=int, default=3)
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--coefficient-bound", type=float, default=1000.0)
    parser.add_argument("--minimum-circuit-floor", type=float, default=1e-7)
    parser.add_argument("--time-limit", type=float, default=90.0)
    parser.add_argument("--screen-seeds", type=int, default=3)
    parser.add_argument("--restarts-per-orientation", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=7000)
    parser.add_argument("--seed", type=int, default=620260714)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_payload(json.loads(arguments.output.read_text()))
        return

    prior_output = arguments.output if arguments.output.exists() else None
    certified = certified_seed_triples(prior_output)
    learned: list[np.ndarray] = []
    excluded_masks: list[int] = []
    scales = tuple(10**exponent for exponent in range(2, 11))
    payload: dict[str, object] = {
        "status": (
            "Cubic and reported H3 certificates are exact. MILP outcomes, "
            "nonlinear failures, and survivor diagnostics are search evidence "
            "only."
        ),
        "parameters": {
            "dictionary_size": arguments.dictionary_size,
            "campaigns": arguments.campaigns,
            "iterations_per_campaign": arguments.iterations,
            "coefficient_bound": arguments.coefficient_bound,
            "minimum_circuit_floor": arguments.minimum_circuit_floor,
            "time_limit": arguments.time_limit,
            "screen_seeds": arguments.screen_seeds,
            "restarts_per_orientation": arguments.restarts_per_orientation,
            "max_iterations": arguments.max_iterations,
            "seed": arguments.seed,
            "fixed_lp_accuracy_threshold": 0,
            "uniform_circuit_floor_strategy": (
                "enforce in the MILP, maximize with the truth table fixed"
            ),
        },
        "certified_seed_triples": certified,
        "campaigns": [],
        "records": [],
    }

    for campaign_index in range(arguments.campaigns):
        campaign_seed = arguments.seed + 10000019 * campaign_index
        dictionary, source_counts = active_dictionary(
            arguments.dictionary_size,
            campaign_seed,
            certified,
            learned,
            prior_output,
        )
        campaign_record: dict[str, object] = {
            "campaign": campaign_index + 1,
            "seed": campaign_seed,
            "initial_dictionary_size": len(dictionary),
            "source_counts": source_counts,
            "final_dictionary": [],
        }
        payload["campaigns"].append(campaign_record)

        for iteration in range(arguments.iterations):
            objective, integrality, bounds, constraints, metadata = (
                cubic.build_milp(
                    dictionary,
                    excluded_masks,
                    arguments.coefficient_bound,
                    maximize_uniform_circuit_floor=False,
                    minimum_uniform_circuit_floor=(
                        arguments.minimum_circuit_floor
                    ),
                )
            )
            print(
                f"campaign={campaign_index + 1} iteration={iteration + 1} "
                f"dictionary={len(dictionary)} variables={metadata['variables']} "
                f"constraints={metadata['constraints']}",
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
                "campaign": campaign_index + 1,
                "iteration": iteration + 1,
                "milp_status": int(result.status),
                "milp_message": str(result.message),
                "model": metadata,
            }
            payload["records"].append(record)
            if result.x is None:
                write_checkpoint(arguments.output, payload)
                break

            floor_index = int(metadata["circuit_floor_index"])
            record["milp_circuit_floor_variable"] = float(
                result.x[floor_index]
            )
            truth = np.rint(result.x[: cubic.VERTICES]).astype(np.int64)
            raw_mask = cubic.mask_from_truth(truth)
            mask = core.complement_canonical(raw_mask, cubic.N)
            record["milp_raw_mask_hex"] = f"0x{raw_mask:016x}"
            record["truth_mask_hex"] = f"0x{mask:016x}"
            excluded_masks.append(raw_mask)
            signs = cubic.signs_from_mask(mask)
            record["fixed_truth_uniform_circuit_floor"] = (
                fixed_truth_uniform_circuit_floor(signs, dictionary)
            )

            cubic_certificate = core.exact_integer_separator(
                signs, core.monomial_matrix(cubic.N, 3)
            )
            if cubic_certificate is None:
                record["exact_degree_at_most_three"] = False
                write_checkpoint(arguments.output, payload)
                continue
            record["exact_degree_at_most_three"] = True
            record["degree_three_coefficients"] = [
                int(value) for value in cubic_certificate[0]
            ]
            quadratic_certificate = core.exact_integer_separator(
                signs, core.monomial_matrix(cubic.N, 2)
            )
            if quadratic_certificate is not None:
                record["threshold_degree"] = "at most 2"
                record["degree_two_coefficients"] = [
                    int(value) for value in quadratic_certificate[0]
                ]
                write_checkpoint(arguments.output, payload)
                continue
            record["quadratic_gordan_circuit"] = quadratic_positive_circuit(
                signs
            )
            record["threshold_degree"] = 3

            fixed_hit = exact_fixed_dictionary_hit(signs, dictionary)
            record["fixed_dictionary_hit"] = fixed_hit
            if fixed_hit is not None:
                record["screen_outcome"] = "exact fixed-dictionary refutation"
                write_checkpoint(arguments.output, payload)
                continue

            certificate, attempts = deep_screen(
                signs,
                campaign_seed + 100003 * iteration,
                arguments.screen_seeds,
                arguments.restarts_per_orientation,
                arguments.max_iterations,
                scales,
            )
            record["deep_screen_attempts"] = attempts
            record["three_head_certificate"] = certificate
            if certificate is not None:
                record["screen_outcome"] = "exact nonlinear-search refutation"
                key = cubic.canonical_triple(
                    np.array(certificate["denominators"], dtype=np.int64)
                )
                known = {cubic.canonical_triple(item) for item in dictionary}
                if key not in known:
                    learned.append(np.array(key, dtype=np.int64))
                    dictionary.append(np.array(key, dtype=np.int64))
            else:
                record["screen_outcome"] = "uncertified robust survivor"
                record["obstruction_diagnostics"] = survivor_diagnostics(
                    attempts
                )
            write_checkpoint(arguments.output, payload)
            print(
                json.dumps(
                    {
                        "mask": record["truth_mask_hex"],
                        "floor": record["fixed_truth_uniform_circuit_floor"],
                        "outcome": record["screen_outcome"],
                    }
                ),
                flush=True,
            )

        campaign_record["final_dictionary"] = [
            item.tolist() for item in dictionary
        ]
        write_checkpoint(arguments.output, payload)

    verify_payload(payload)
    print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
