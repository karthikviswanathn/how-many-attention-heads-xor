#!/usr/bin/env python3
"""Active-learn H4 denominator tuples for the degree-four face family.

Orbit 62 in the affine-cocircuit reduction has one four-bit face carrying an
arbitrary sign table and the opposite face carrying four-bit parity.  The one
constant extension is five-bit parity and is excluded.  A single tangent
space cannot shatter this entire family, so this diagnostic learns a finite
dictionary instead.  Every reported target success is checked exactly; a
remaining dictionary miss is not a lower bound.
"""

from __future__ import annotations

import argparse
import json

import numpy as np

import screen_n5_degree4_cocircuit_families as families
import search_adversarial_low_dimension as core
import search_uncovered_cubic_n6 as nonlinear


N = 5
HEADS = 4
WIDTH = N + 1
VERTICES = 1 << N
ORBIT = 62

# Exact denominator tuples learned from deterministic residual targets.  They
# are seed witnesses for later runs, not evidence about targets they miss.
KNOWN_ADDITIONAL_DENOMINATORS = (
    (
        (10002, -1, -2283, -1, -2292, -5424),
        (10003, -2, -2004, -2, -7993, -1),
        (10002, -1, -7152, -1, -2846, -1),
        (1, 5109, 1, 4735, 156, 1),
    ),
    (
        (34, -1, -1, -1, -1, -29),
        (33, -25, -1, -1, -3, -2),
        (32, -22, -1, -1, -5, -2),
        (35, -1, -1, -1, -1, -1),
    ),
    (
        (10001, -2, -9723, -1, -1, -23),
        (10001, -7752, -1340, -295, -310, -298),
        (10002, -29, -1, -627, -1297, -8047),
        (10001, -1, -4, -6369, -1898, -1726),
    ),
    (
        (35, -1, -1, -1, -1, -1),
        (34, -27, -1, -3, -1, -1),
        (33, -20, -1, -9, -1, -1),
        (33, -1, -10, -1, -10, -10),
    ),
)


def configure_nonlinear_search() -> None:
    nonlinear.N = N
    nonlinear.HEADS = HEADS
    nonlinear.WIDTH = WIDTH
    nonlinear.VERTICES = VERTICES


def heuristic_coverage(
    signs: np.ndarray,
    dictionary: list[np.ndarray],
    iterations: int,
) -> tuple[np.ndarray, np.ndarray]:
    covered = np.zeros(len(signs), dtype=bool)
    witnesses = -np.ones(len(signs), dtype=np.int64)
    for dictionary_index, denominators in enumerate(dictionary):
        active = np.flatnonzero(~covered)
        if not len(active):
            break
        hits = core.gilbert_cover(
            signs[active],
            families.whitened_features(denominators),
            iterations,
        )
        selected = active[hits]
        covered[selected] = True
        witnesses[selected] = dictionary_index
    return covered, witnesses


def exact_dictionary_hit(
    signs: np.ndarray, dictionary: list[np.ndarray]
) -> tuple[int, dict[str, object]] | None:
    for dictionary_index, denominators in enumerate(dictionary):
        certificate = nonlinear.exact_head_certificate(signs, denominators)
        if certificate is not None:
            return dictionary_index, certificate
    return None


def nonlinear_denominator_search(
    signs: np.ndarray,
    seed: int,
    restarts: int,
    max_iterations: int,
) -> dict[str, object] | None:
    for positive_heads in range(HEADS + 1):
        orientations = tuple(
            [-1] * (HEADS - positive_heads) + [1] * positive_heads
        )
        certificate, _ = nonlinear.continuous_search(
            signs,
            seed + 1009 * positive_heads,
            restarts,
            max_iterations,
            (10, 30, 100, 300, 1000, 3000, 10000),
            orientation_filter=orientations,
            lp_accuracy_threshold=VERTICES - 8,
        )
        if certificate is not None:
            certificate["positive_heads"] = positive_heads
            return certificate
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary-size", type=int, default=256)
    parser.add_argument("--gilbert-iterations", type=int, default=160)
    parser.add_argument("--rounds", type=int, default=16)
    parser.add_argument("--exact-probes", type=int, default=16)
    parser.add_argument("--restarts", type=int, default=24)
    parser.add_argument("--max-iterations", type=int, default=2200)
    parser.add_argument("--seed", type=int, default=20260714)
    arguments = parser.parse_args()
    configure_nonlinear_search()

    normal = families.orbit_normals()[ORBIT]
    signs = families.extension_signs(normal)
    dictionary = families.denominator_dictionary(
        arguments.dictionary_size, arguments.seed
    )
    dictionary.extend(
        np.array(denominators, dtype=np.int64)
        for denominators in KNOWN_ADDITIONAL_DENOMINATORS
    )
    additions = []
    exact_extra_covered: set[int] = set()

    for round_index in range(arguments.rounds + 1):
        covered, _ = heuristic_coverage(
            signs, dictionary, arguments.gilbert_iterations
        )
        if exact_extra_covered:
            covered[list(exact_extra_covered)] = True
        misses = np.flatnonzero(~covered)
        print(
            f"round={round_index} dictionary={len(dictionary)} "
            f"heuristic_misses={len(misses)}",
            flush=True,
        )
        if not len(misses) or round_index == arguments.rounds:
            break

        unresolved = []
        for target_index in misses[: arguments.exact_probes]:
            hit = exact_dictionary_hit(signs[target_index], dictionary)
            if hit is None:
                unresolved.append(int(target_index))
            else:
                exact_extra_covered.add(int(target_index))
        if not unresolved:
            continue

        target_index = unresolved[0]
        certificate = nonlinear_denominator_search(
            signs[target_index],
            arguments.seed + 100_003 * round_index,
            arguments.restarts,
            arguments.max_iterations,
        )
        if certificate is None:
            print(
                f"target={target_index} nonlinear search failed",
                flush=True,
            )
            continue
        denominators = np.array(certificate["denominators"], dtype=np.int64)
        dictionary.append(denominators)
        record = {
            "target_index": target_index,
            "denominators": certificate["denominators"],
            "positive_heads": certificate["positive_heads"],
            "minimum_signed_cleared_score": certificate[
                "minimum_signed_cleared_score"
            ],
        }
        additions.append(record)
        print("ADDITION " + json.dumps(record), flush=True)

    print(f"learned additions: {len(additions)}")
    print(json.dumps(additions, indent=2))
    print("warning: residual misses are only search evidence")


if __name__ == "__main__":
    main()
