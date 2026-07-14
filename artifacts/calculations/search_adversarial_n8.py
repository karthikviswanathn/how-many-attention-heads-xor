#!/usr/bin/env python3
"""Search adversarial eight-bit degree-two cells for a two-head gap.

The candidate pool combines explicit random integer quadratics with sign cells
returned by an MILP that avoids a fixed denominator dictionary.  Every stored
candidate has an exact integer degree-two sign polynomial and an exact affine
Farkas witness excluding degree one.  Fixed-dictionary and continuous search
successes are integer-verified.  Continuous failures, including unrestricted
rank-(2,2) failures, are search evidence only.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

import search_adversarial_low_dimension as core
import search_continuous_one_oriented_factor as one_oriented
import search_continuous_rank4_relaxation as rank_four
import search_uncovered_cell_milp as uncovered


DIMENSION = 8
FULL_MASK = (1 << (1 << DIMENSION)) - 1


def mask_from_truth_row(row: np.ndarray) -> int:
    packed = np.packbits(row.astype(np.uint8), bitorder="little")
    return int.from_bytes(packed.tobytes(), byteorder="little")


def canonical_mask_and_coefficients(
    mask: int, coefficients: np.ndarray
) -> tuple[int, list[int]]:
    complement = FULL_MASK ^ mask
    if complement < mask:
        return complement, [-int(value) for value in coefficients]
    return mask, [int(value) for value in coefficients]


def random_quadratic_pool(
    samples: int, retain: int, seed: int, batch_size: int = 2000
) -> tuple[dict[int, dict[str, object]], dict[str, int]]:
    rng = np.random.default_rng(seed)
    evaluation = core.monomial_matrix(DIMENSION, 2).astype(np.int64)
    nonconstant = evaluation[:, 1:]
    retained: dict[int, dict[str, object]] = {}
    family_counts = {"dense": 0, "sparse": 0, "hierarchical": 0}

    generated = 0
    batch_index = 0
    while generated < samples:
        size = min(batch_size, samples - generated)
        family = ("dense", "sparse", "hierarchical")[batch_index % 3]
        if family == "dense":
            slopes = rng.integers(-7, 8, size=(size, nonconstant.shape[1]))
        elif family == "sparse":
            slopes = rng.integers(-15, 16, size=(size, nonconstant.shape[1]))
            slopes *= rng.random(size=slopes.shape) < 0.25
        else:
            exponents = rng.integers(0, 7, size=(size, nonconstant.shape[1]))
            slope_signs = rng.choice(np.array([-1, 1]), size=exponents.shape)
            slopes = slope_signs * np.left_shift(1, exponents)
            slopes *= rng.random(size=slopes.shape) < 0.60

        missing_quadratic = ~np.any(slopes[:, DIMENSION:] != 0, axis=1)
        for row in np.flatnonzero(missing_quadratic):
            column = int(rng.integers(DIMENSION, slopes.shape[1]))
            slopes[row, column] = 1

        raw_values = slopes @ nonconstant.T
        threshold_ranks = rng.integers(0, 1 << DIMENSION, size=size)
        thresholds = np.take_along_axis(
            np.sort(raw_values, axis=1), threshold_ranks[:, None], axis=1
        )[:, 0]
        coefficients = np.column_stack([1 - 2 * thresholds, 2 * slopes])
        values = coefficients @ evaluation.T
        assert np.all(values % 2 != 0)

        matrices = core.canonical_quadratic_matrix(coefficients, DIMENSION)
        singular = np.linalg.svd(matrices, compute_uv=False)
        tail = np.sqrt(np.sum(singular[:, 4:] ** 2, axis=1))
        total = np.sqrt(np.sum(singular**2, axis=1))
        cell_margin = np.min(np.abs(values), axis=1) / np.maximum(
            np.linalg.norm(coefficients, axis=1), 1.0
        )
        proxy = tail / np.maximum(total * cell_margin, 1e-14)

        local_count = min(size, max(4 * retain, 256))
        local = np.argpartition(proxy, -local_count)[-local_count:]
        for row in local:
            mask = mask_from_truth_row(values[row] > 0)
            mask, exact_coefficients = canonical_mask_and_coefficients(
                mask, coefficients[row]
            )
            score = float(proxy[row])
            previous = retained.get(mask)
            if previous is None or score > float(previous["rank_cell_proxy"]):
                retained[mask] = {
                    "truth_mask_hex": f"0x{mask:064x}",
                    "source": f"random-{family}",
                    "degree_two_coefficients": exact_coefficients,
                    "rank_cell_proxy": score,
                    "minimum_signed_polynomial_value": int(
                        np.min(np.abs(values[row]))
                    ),
                }

        if len(retained) > 8 * retain:
            best = sorted(
                retained.items(),
                key=lambda item: float(item[1]["rank_cell_proxy"]),
                reverse=True,
            )
            retained = dict(best[: 4 * retain])
        generated += size
        family_counts[family] += size
        batch_index += 1
        print(
            f"random quadratics {generated}/{samples}; pool={len(retained)}",
            flush=True,
        )

    best = sorted(
        retained.items(),
        key=lambda item: float(item[1]["rank_cell_proxy"]),
        reverse=True,
    )[:retain]
    return dict(best), family_counts


def exact_degree_one_witness(mask: int) -> dict[str, object] | None:
    signs = core.signs_from_mask(mask, DIMENSION)
    affine = core.affine_matrix(DIMENSION)
    signed_rows = signs[:, None] * affine
    equalities = np.vstack(
        [signed_rows.T.astype(float), np.ones(1 << DIMENSION)]
    )
    target = np.concatenate([np.zeros(DIMENSION + 1), [1.0]])
    result = linprog(
        np.zeros(1 << DIMENSION),
        A_eq=equalities,
        b_eq=target,
        bounds=(0.0, None),
        method="highs",
    )
    if not result.success:
        return None
    support = np.flatnonzero(result.x > 1e-9)
    fractions = [
        Fraction(float(result.x[index])).limit_denominator(10**7)
        for index in support
    ]
    common_denominator = 1
    for value in fractions:
        common_denominator = math.lcm(common_denominator, value.denominator)
    weights = [
        value.numerator * (common_denominator // value.denominator)
        for value in fractions
    ]
    moment = signed_rows[support].T.astype(object) @ np.array(
        weights, dtype=object
    )
    if any(int(value) != 0 for value in moment) or min(weights) <= 0:
        return None
    common = 0
    for weight in weights:
        common = math.gcd(common, abs(int(weight)))
    weights = [int(weight // common) for weight in weights]
    return {
        "vertices": [int(index) for index in support],
        "weights": weights,
    }


def verify_polynomial(record: dict[str, object]) -> None:
    mask = int(str(record["truth_mask_hex"]), 16)
    coefficients = np.array(record["degree_two_coefficients"], dtype=object)
    signed = core.signs_from_mask(mask, DIMENSION).astype(object) * (
        core.monomial_matrix(DIMENSION, 2).astype(object) @ coefficients
    )
    if min(signed) <= 0:
        raise AssertionError("stored quadratic does not represent its mask")
    record["minimum_signed_polynomial_value"] = int(min(signed))


def add_milp_candidates(
    pool: dict[int, dict[str, object]],
    dictionary: list[np.ndarray],
    count: int,
    time_limit: float,
    coefficient_bound: float,
) -> list[dict[str, object]]:
    outcomes = []
    excluded_raw: list[int] = []
    for iteration in range(count):
        result, metadata = uncovered.solve_uncovered(
            DIMENSION,
            dictionary,
            excluded_raw,
            coefficient_bound,
            time_limit,
        )
        outcome: dict[str, object] = {
            "iteration": iteration,
            "status": int(result.status),
            "message": str(result.message),
            "model": metadata,
        }
        if result.x is None:
            outcomes.append(outcome)
            break
        truth = np.rint(result.x[: 1 << DIMENSION]).astype(np.int64)
        raw_mask = sum(
            1 << vertex for vertex, value in enumerate(truth) if value == 1
        )
        excluded_raw.append(raw_mask)
        mask = core.complement_canonical(raw_mask, DIMENSION)
        exact = core.exact_integer_separator(
            core.signs_from_mask(mask, DIMENSION),
            core.monomial_matrix(DIMENSION, 2),
        )
        outcome["truth_mask_hex"] = f"0x{mask:064x}"
        outcome["exact_degree_two"] = exact is not None
        if exact is not None:
            coefficients = [int(value) for value in exact[0]]
            pool[mask] = {
                "truth_mask_hex": f"0x{mask:064x}",
                "source": "milp-dictionary-miss",
                "degree_two_coefficients": coefficients,
                "rank_cell_proxy": None,
            }
        outcomes.append(outcome)
        print(json.dumps(outcome), flush=True)
    return outcomes


def one_oriented_search(
    mask: int, restarts: int, seed: int, max_iterations: int
) -> dict[str, object]:
    arguments = argparse.Namespace(
        dimension=DIMENSION,
        mask=mask,
        restarts=restarts,
        max_iterations=max_iterations,
        seed=seed,
        scales=(10, 30, 100, 300, 1000, 3000),
        output=None,
    )
    return one_oriented.search(arguments)


def unrestricted_search(
    mask: int, restarts: int, seed: int, max_iterations: int
) -> dict[str, object]:
    arguments = argparse.Namespace(
        dimension=DIMENSION,
        mask=mask,
        restarts=restarts,
        max_iterations=max_iterations,
        seed=seed,
        scales=(10, 30, 100, 300, 1000, 3000),
        output=None,
    )
    return rank_four.search(arguments)


def hardness_key(record: dict[str, object]) -> tuple[int, int, int, float]:
    unrestricted = record["unrestricted_search"]
    oriented = record["one_oriented_search"]
    unrestricted_found = bool(unrestricted["found"])
    unrestricted_accuracy = int(unrestricted.get("best_accuracy", 1 << DIMENSION))
    oriented_accuracy = int(oriented.get("best_accuracy", 1 << DIMENSION))
    proxy = record.get("rank_cell_proxy")
    proxy_value = float(proxy) if proxy is not None else 0.0
    return (
        1 if unrestricted_found else 0,
        unrestricted_accuracy,
        oriented_accuracy,
        -proxy_value,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=20000)
    parser.add_argument("--retain", type=int, default=512)
    parser.add_argument("--dictionary-size", type=int, default=64)
    parser.add_argument("--dictionary-finalists", type=int, default=40)
    parser.add_argument("--milp-candidates", type=int, default=2)
    parser.add_argument("--milp-dictionary-size", type=int, default=12)
    parser.add_argument("--milp-time-limit", type=float, default=60.0)
    parser.add_argument("--coefficient-bound", type=float, default=10000.0)
    parser.add_argument("--quick-restarts", type=int, default=12)
    parser.add_argument("--deep-finalists", type=int, default=8)
    parser.add_argument("--deep-restarts", type=int, default=150)
    parser.add_argument("--max-iterations", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20260713)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "adversarial_n8_results.json",
    )
    arguments = parser.parse_args()

    pool, family_counts = random_quadratic_pool(
        arguments.samples, arguments.retain, arguments.seed
    )
    dictionary = core.build_dictionary(
        DIMENSION, arguments.dictionary_size, arguments.seed + 1
    )

    ranked = []
    for index, (mask, record) in enumerate(pool.items(), 1):
        hits = core.exact_dictionary_hits(mask, DIMENSION, dictionary)
        record["fixed_dictionary_hit_count"] = len(hits)
        record["fixed_dictionary_first_hits"] = hits[:8]
        ranked.append((len(hits), -float(record["rank_cell_proxy"]), mask))
        if index % 64 == 0:
            print(f"dictionary scan {index}/{len(pool)}", flush=True)
    ranked.sort()
    selected_masks = [
        mask for _, _, mask in ranked[: arguments.dictionary_finalists]
    ]

    milp_outcomes = add_milp_candidates(
        pool,
        dictionary[: arguments.milp_dictionary_size],
        arguments.milp_candidates,
        arguments.milp_time_limit,
        arguments.coefficient_bound,
    )
    selected_masks.extend(
        mask
        for mask, record in pool.items()
        if record["source"] == "milp-dictionary-miss"
    )
    selected_masks = list(dict.fromkeys(selected_masks))

    quick_survivors = []
    refuted_count = 0
    for index, mask in enumerate(selected_masks):
        record = pool[mask]
        verify_polynomial(record)
        witness = exact_degree_one_witness(mask)
        if witness is None:
            record["degree_one_farkas_witness"] = None
            continue
        record["degree_one_farkas_witness"] = witness
        oriented = one_oriented_search(
            mask,
            arguments.quick_restarts,
            arguments.seed + 100003 * index,
            arguments.max_iterations,
        )
        record["one_oriented_search"] = oriented
        if oriented["found"]:
            refuted_count += 1
            continue
        unrestricted = unrestricted_search(
            mask,
            arguments.quick_restarts,
            arguments.seed + 200003 * index,
            arguments.max_iterations,
        )
        record["unrestricted_search"] = unrestricted
        quick_survivors.append(record)
        print(
            f"quick survivor {len(quick_survivors)}: "
            f"unrestricted_found={unrestricted['found']} "
            f"mask={record['truth_mask_hex']}",
            flush=True,
        )

    quick_survivors.sort(key=hardness_key)
    deep_inputs = quick_survivors[: arguments.deep_finalists]
    final_survivors = []
    for index, record in enumerate(deep_inputs):
        mask = int(str(record["truth_mask_hex"]), 16)
        record.setdefault("search_history", []).append(
            {
                "one_oriented": record["one_oriented_search"],
                "unrestricted": record["unrestricted_search"],
            }
        )
        oriented = one_oriented_search(
            mask,
            arguments.deep_restarts,
            arguments.seed + 700001 + 100003 * index,
            arguments.max_iterations,
        )
        record["one_oriented_search"] = oriented
        if oriented["found"]:
            refuted_count += 1
            continue
        unrestricted = unrestricted_search(
            mask,
            arguments.deep_restarts,
            arguments.seed + 900001 + 100003 * index,
            arguments.max_iterations,
        )
        record["unrestricted_search"] = unrestricted
        final_survivors.append(record)
        print(
            f"deep survivor {len(final_survivors)}: "
            f"unrestricted_found={unrestricted['found']} "
            f"mask={record['truth_mask_hex']}",
            flush=True,
        )

    final_survivors.sort(key=hardness_key)
    payload = {
        "status": (
            "Exact polynomials, affine Farkas witnesses, and search successes "
            "are verified.  Search failures are not lower bounds."
        ),
        "dimension": DIMENSION,
        "seed": arguments.seed,
        "parameters": vars(arguments) | {"output": str(arguments.output)},
        "random_family_counts": family_counts,
        "dictionary": [pair.tolist() for pair in dictionary],
        "milp_outcomes": milp_outcomes,
        "selected_count": len(selected_masks),
        "quick_survivor_count": len(quick_survivors),
        "exactly_refuted_count": refuted_count,
        "final_survivors": final_survivors,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        f"saved {len(final_survivors)} deep survivors to {arguments.output}",
        flush=True,
    )


if __name__ == "__main__":
    main()
