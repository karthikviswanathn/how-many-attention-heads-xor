#!/usr/bin/env python3
"""Search five-bit XORs of incompatible affine threshold pairs.

For two odd-valued affine forms L and M, XOR of their positive halfspaces is
sign-represented exactly by -L M.  The sampled pairs have mixed coordinatewise
slope agreement, so no coordinate flip makes both factor slope patterns
one-sided at once.  Every retained cell has an exact quadratic polynomial and
an exact affine Farkas witness.  Every reported H2 success is reparameterized
from one admissible factor and checked with integer arithmetic.
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
import search_continuous_one_oriented_factor as one_factor


DIMENSION = 5
FULL_MASK = (1 << (1 << DIMENSION)) - 1


def random_ltf(rng: np.random.Generator) -> tuple[int, ...]:
    slopes = rng.integers(1, 10, size=DIMENSION)
    slopes *= rng.choice(np.array([-1, 1]), size=DIMENSION)
    values = core.cube(DIMENSION) @ slopes
    threshold = int(np.sort(values)[int(rng.integers(1, len(values) - 1))])
    return (1 - 2 * threshold, *(2 * slopes).tolist())


def affine_values(coefficients: tuple[int, ...]) -> np.ndarray:
    return core.affine_matrix(DIMENSION) @ np.array(coefficients, dtype=np.int64)


def product_coefficients(
    first: tuple[int, ...], second: tuple[int, ...], sign: int = -1
) -> list[int]:
    answer = [sign * first[0] * second[0]]
    answer.extend(
        sign
        * (
            first[0] * second[index]
            + second[0] * first[index]
            + first[index] * second[index]
        )
        for index in range(1, DIMENSION + 1)
    )
    for first_index in range(1, DIMENSION + 1):
        for second_index in range(first_index + 1, DIMENSION + 1):
            answer.append(
                sign
                * (
                    first[first_index] * second[second_index]
                    + first[second_index] * second[first_index]
                )
            )
    return answer


def mask_from_signs(signs: np.ndarray) -> int:
    return sum(1 << index for index in np.flatnonzero(signs > 0))


def degree_one_witness(mask: int) -> dict[str, object] | None:
    signs = core.signs_from_mask(mask, DIMENSION)
    affine = core.affine_matrix(DIMENSION)
    signed_rows = signs[:, None] * affine
    equalities = np.vstack([signed_rows.T, np.ones(1 << DIMENSION)])
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
        Fraction(float(result.x[index])).limit_denominator(10**6)
        for index in support
    ]
    denominator = 1
    for value in fractions:
        denominator = math.lcm(denominator, value.denominator)
    weights = [
        value.numerator * (denominator // value.denominator)
        for value in fractions
    ]
    moment = signed_rows[support].T.astype(object) @ np.array(
        weights, dtype=object
    )
    if any(int(value) for value in moment) or min(weights) <= 0:
        return None
    common = 0
    for weight in weights:
        common = math.gcd(common, abs(int(weight)))
    return {
        "vertices": [int(index) for index in support],
        "weights": [int(weight // common) for weight in weights],
    }


def continuous_search(mask: int, restarts: int, seed: int) -> dict[str, object]:
    arguments = argparse.Namespace(
        dimension=DIMENSION,
        mask=mask,
        restarts=restarts,
        max_iterations=3000,
        seed=seed,
        scales=(10, 30, 100, 300, 1000, 3000),
        output=None,
    )
    return one_factor.search(arguments)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=20000)
    parser.add_argument("--retain", type=int, default=1024)
    parser.add_argument("--dictionary-prefix", type=int, default=48)
    parser.add_argument("--finalists", type=int, default=48)
    parser.add_argument("--quick-restarts", type=int, default=12)
    parser.add_argument("--deep-finalists", type=int, default=8)
    parser.add_argument("--deep-restarts", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "ltf_pair_xor_n5_results.json",
    )
    arguments = parser.parse_args()
    rng = np.random.default_rng(arguments.seed)
    evaluation = core.monomial_matrix(DIMENSION, 2).astype(object)

    pool: dict[int, dict[str, object]] = {}
    for sample in range(arguments.samples):
        first = random_ltf(rng)
        second = random_ltf(rng)
        relative = [
            int(np.sign(first[index] * second[index]))
            for index in range(1, DIMENSION + 1)
        ]
        if len(set(relative)) < 2:
            continue
        first_values = affine_values(first)
        second_values = affine_values(second)
        if len(set(first_values > 0)) < 2 or len(set(second_values > 0)) < 2:
            continue
        coefficients = product_coefficients(first, second)
        values = np.array(evaluation @ np.array(coefficients, dtype=object))
        assert all(int(value) != 0 for value in values)
        mask = mask_from_signs(values)
        if (FULL_MASK ^ mask) < mask:
            mask = FULL_MASK ^ mask
            coefficients = [-value for value in coefficients]
        imbalance = abs(sum(relative))
        previous = pool.get(mask)
        if previous is None or imbalance < int(previous["relative_sign_imbalance"]):
            pool[mask] = {
                "truth_mask_hex": f"0x{mask:08x}",
                "first_affine_factor": list(first),
                "second_affine_factor": list(second),
                "relative_slope_signs": relative,
                "relative_sign_imbalance": imbalance,
                "degree_two_coefficients": coefficients,
                "minimum_signed_polynomial_value": int(
                    min(abs(int(value)) for value in values)
                ),
            }
        if len(pool) > 4 * arguments.retain:
            best = sorted(
                pool.items(),
                key=lambda item: (
                    int(item[1]["relative_sign_imbalance"]), item[0]
                ),
            )[: 2 * arguments.retain]
            pool = dict(best)
        if (sample + 1) % 5000 == 0:
            print(f"sampled {sample + 1}; unique cells={len(pool)}", flush=True)

    best_pool = sorted(
        pool.items(),
        key=lambda item: (int(item[1]["relative_sign_imbalance"]), item[0]),
    )[: arguments.retain]
    pool = dict(best_pool)

    dictionary_path = (
        Path(__file__).resolve().parent / "adversarial_n5_broad_results.json"
    )
    dictionary_payload = json.loads(dictionary_path.read_text())
    dictionary = [
        np.array(pair, dtype=np.int64)
        for pair in dictionary_payload["dictionary"][: arguments.dictionary_prefix]
    ]
    ranked = []
    for index, (mask, record) in enumerate(pool.items(), 1):
        hits = core.exact_dictionary_hits(mask, DIMENSION, dictionary)
        record["fixed_dictionary_hit_count"] = len(hits)
        record["fixed_dictionary_first_hits"] = hits[:8]
        ranked.append(
            (
                len(hits),
                int(record["relative_sign_imbalance"]),
                mask,
            )
        )
        if index % 128 == 0:
            print(f"dictionary scan {index}/{len(pool)}", flush=True)
    ranked.sort()

    quick_survivors = []
    refutations = []
    for index, (_, _, mask) in enumerate(ranked[: arguments.finalists]):
        record = pool[mask]
        witness = degree_one_witness(mask)
        if witness is None:
            continue
        record["degree_one_farkas_witness"] = witness
        search = continuous_search(
            mask, arguments.quick_restarts, arguments.seed + 100003 * index
        )
        record["one_oriented_search"] = search
        if search["found"]:
            refutations.append(record)
        else:
            quick_survivors.append(record)
            print(
                f"quick survivor {len(quick_survivors)}: "
                f"accuracy={search['best_accuracy']} mask={record['truth_mask_hex']}",
                flush=True,
            )

    quick_survivors.sort(
        key=lambda record: (
            int(record["one_oriented_search"]["best_accuracy"]),
            int(record["relative_sign_imbalance"]),
        )
    )
    final_survivors = []
    for index, record in enumerate(quick_survivors[: arguments.deep_finalists]):
        record.setdefault("search_history", []).append(
            record["one_oriented_search"]
        )
        mask = int(str(record["truth_mask_hex"]), 16)
        search = continuous_search(
            mask, arguments.deep_restarts, arguments.seed + 700001 + 100003 * index
        )
        record["one_oriented_search"] = search
        if search["found"]:
            refutations.append(record)
        else:
            final_survivors.append(record)

    payload = {
        "status": (
            "Polynomial, Farkas, and H2 success certificates are exact. "
            "Continuous failures are not H2 lower bounds."
        ),
        "dimension": DIMENSION,
        "parameters": vars(arguments) | {"output": str(arguments.output)},
        "sampled_unique_cells": len(pool),
        "quick_survivor_count": len(quick_survivors),
        "exact_refutation_count": len(refutations),
        "final_survivors": final_survivors,
        "refutations": refutations,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        f"saved {len(final_survivors)} survivors and {len(refutations)} "
        f"exact refutations to {arguments.output}",
        flush=True,
    )


if __name__ == "__main__":
    main()
