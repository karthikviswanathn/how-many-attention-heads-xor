#!/usr/bin/env python3
"""Global denominator-dictionary search for support-17 H3 families.

Each admissible denominator triple determines one 16-dimensional score
space.  The numerical stage batch-tests that one space against every exact-
degree-three-only support-17 circuit orbit.  A selected hit is then rechecked
with an exact 32 by 16 integer cleared matrix.  The archive stores one tuple
index per covered orbit, and the verifier reconstructs every rank and kernel
sign certificate.

Dictionary misses are not head lower bounds.  They are a precise uncovered
set for the stated deterministic dictionary.
"""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
from collections import Counter
from pathlib import Path

import numpy as np

try:
    from threadpoolctl import threadpool_limits
except ModuleNotFoundError:
    def threadpool_limits(*, limits: int) -> None:
        """No-op fallback when the optional performance helper is absent."""
        del limits
        return None

import classify_n5_support17_affine_extensions as classification
import search_n5_degree4_family_shattering as exact


N = 5
HEADS = 3
WIDTH = N + 1
VERTICES = 1 << N
HERE = Path(__file__).resolve().parent
DEFAULT_CODES = HERE / "n5_support17_exact_degree3_only_codes.tsv"
DEFAULT_OUTPUT = HERE / "n5_support17_global_dictionary_coverage.npz"
DEFAULT_SUMMARY = HERE / "n5_support17_global_dictionary_summary.json"
PRIME = 1_000_003
LOG_SPANS = (4.0, 7.0, 10.0, 14.0)


_SIGNS: np.ndarray | None = None
_FREE: np.ndarray | None = None
_INPUTS: np.ndarray | None = None
_THREAD_LIMIT = None


def load_codes(path: Path) -> np.ndarray:
    lines = path.read_text().splitlines()
    assert lines[0] == "ternary_circuit_code"
    codes = np.array([int(line) for line in lines[1:]], dtype=np.uint64)
    assert len(codes) == 23_116
    return codes


def decode_codes(codes: np.ndarray) -> np.ndarray:
    return np.stack(
        [classification.decode_ternary_code(int(code)) for code in codes]
    )


def initialize_worker(codes_path: str) -> None:
    global _SIGNS, _FREE, _INPUTS, _THREAD_LIMIT
    _THREAD_LIMIT = threadpool_limits(limits=1)
    codes = load_codes(Path(codes_path))
    _SIGNS = decode_codes(codes)
    _FREE = np.stack(
        [np.flatnonzero(signs == 0) for signs in _SIGNS]
    )
    _INPUTS = (
        (np.arange(VERTICES)[:, None] >> np.arange(N)) & 1
    ).astype(float)


def canonical_denominators(
    denominators: np.ndarray,
) -> tuple[tuple[int, ...], ...]:
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


def normalized_integer_weights(
    logits: np.ndarray, scale: int = 1_000_000
) -> np.ndarray:
    shifted = logits - np.max(logits)
    probabilities = np.exp(shifted)
    probabilities /= np.sum(probabilities)
    return np.maximum(1, np.rint(scale * probabilities)).astype(np.int64)


def random_denominator_tuple(
    index: int, seed: int, mode: str
) -> np.ndarray:
    rng = np.random.default_rng(
        np.random.SeedSequence([seed, index, 0x474C4F42414C])
    )
    selected_mode = mode
    if mode == "mixed":
        selected_mode = ("independent", "pair", "triple")[index % 3]
    if selected_mode == "independent":
        positive_heads = index % (HEADS + 1)
        orientations = np.array(
            [1] * positive_heads + [-1] * (HEADS - positive_heads),
            dtype=np.int64,
        )
        rng.shuffle(orientations)
        log_span = LOG_SPANS[(index // (HEADS + 1)) % len(LOG_SPANS)]
        weights = np.maximum(
            1,
            np.rint(
                np.exp(rng.uniform(0.0, log_span, size=(HEADS, WIDTH)))
            ),
        ).astype(np.int64)
    else:
        orientation = -1 if (index // 3) % 4 else 1
        orientations = np.full(HEADS, orientation, dtype=np.int64)
        base_logits = rng.normal(scale=2.5, size=WIDTH)
        base = normalized_integer_weights(base_logits)
        relative_scale = (0.003, 0.01, 0.03, 0.1)[(index // 12) % 4]
        perturbation = rng.normal(
            scale=relative_scale * 1_000_000,
            size=(HEADS, WIDTH),
        )
        weights = np.maximum(
            1, base[None, :] + np.rint(perturbation).astype(np.int64)
        )
        if selected_mode == "pair":
            weights[2] = normalized_integer_weights(
                rng.normal(scale=2.5, size=WIDTH)
            )
    rows = []
    for head, orientation in enumerate(orientations):
        if orientation > 0:
            rows.append(weights[head])
        else:
            rows.append(
                np.concatenate(
                    [[int(np.sum(weights[head]))], -weights[head, 1:]]
                )
            )
    return np.array(canonical_denominators(np.vstack(rows)), dtype=np.int64)


def numerical_cover_task(
    task: tuple[int, np.ndarray]
) -> tuple[int, np.ndarray, np.ndarray]:
    index, denominators = task
    assert _SIGNS is not None and _FREE is not None and _INPUTS is not None
    values = np.column_stack(
        [
            denominators[head, 0]
            + _INPUTS @ denominators[head, 1:].astype(float)
            for head in range(HEADS)
        ]
    )
    if np.any(values <= 0):
        return index, np.empty(0, dtype=np.int32), np.empty(0)
    matrix = np.column_stack(
        [np.ones(VERTICES)]
        + [
            _INPUTS[:, coordinate] / values[:, head]
            for head in range(HEADS)
            for coordinate in range(N)
        ]
    )
    matrix = matrix / np.linalg.norm(matrix, axis=0, keepdims=True)
    _, singular, right = np.linalg.svd(
        matrix[_FREE], full_matrices=True
    )
    null_vectors = right[:, -1, :]
    scores = null_vectors @ matrix.T
    scale = np.max(np.abs(scores), axis=1)
    products = _SIGNS * scores
    positive_margin = np.min(
        np.where(_SIGNS != 0, products, np.inf), axis=1
    )
    negative_margin = np.min(
        np.where(_SIGNS != 0, -products, np.inf), axis=1
    )
    margins = np.maximum(positive_margin, negative_margin) / scale
    rank_ok = singular[:, -1] > 1e-11 * singular[:, 0]
    covered = np.flatnonzero(rank_ok & (margins > 1e-8)).astype(np.int32)
    return index, covered, margins[covered]


def input_matrix() -> np.ndarray:
    inputs = (
        (np.arange(VERTICES)[:, None] >> np.arange(N)) & 1
    ).astype(object)
    return np.column_stack(
        [np.ones(VERTICES, dtype=object), inputs]
    )


def valid_denominators(denominators: np.ndarray) -> bool:
    affine = input_matrix()
    values = affine @ denominators.astype(object).T
    return bool(
        np.all(values > 0)
        and all(
            np.all(row[1:] > 0) or np.all(row[1:] < 0)
            for row in denominators
        )
    )


def independent_cleared_matrix(denominators: np.ndarray) -> np.ndarray:
    affine = input_matrix()
    values = affine @ denominators.astype(object).T
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(HEADS):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(1, WIDTH)
        )
    matrix = np.column_stack(columns).astype(object)
    assert matrix.shape == (VERTICES, 16)
    return matrix


def exact_family_hit(
    signs: np.ndarray, denominators: np.ndarray
) -> tuple[bool, int]:
    if not valid_denominators(denominators):
        return False, 0
    free = np.flatnonzero(signs == 0)
    support = np.flatnonzero(signs)
    matrix = independent_cleared_matrix(denominators)
    if exact.modular_rank(matrix[free], PRIME) != 15:
        return False, 0
    kernel = exact.integer_nullspace_basis(matrix[free])
    if kernel.shape != (16, 1):
        return False, 0
    score = matrix @ kernel[:, 0]
    assert np.all(score[free] == 0)
    products = signs[support].astype(object) * score[support]
    if min(products) > 0:
        return True, int(min(products))
    if max(products) < 0:
        return True, int(min(-products))
    return False, 0


def zero_layer_profile(signs: np.ndarray) -> tuple[int, ...]:
    counts = tuple(
        int(
            np.sum(
                (signs == 0)
                & np.array(
                    [vertex.bit_count() == weight for vertex in range(32)]
                )
            )
        )
        for weight in range(6)
    )
    return min(counts, tuple(reversed(counts)))


def verify_archive(
    codes: np.ndarray,
    denominators: np.ndarray,
    assignments: np.ndarray,
) -> None:
    signs = decode_codes(codes)
    assert assignments.shape == (len(codes),)
    assert np.all((assignments == -1) | (assignments < len(denominators)))
    for family in np.flatnonzero(assignments >= 0):
        hit, _ = exact_family_hit(
            signs[family], denominators[int(assignments[family])]
        )
        assert hit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codes", type=Path, default=DEFAULT_CODES)
    parser.add_argument("--dictionary-size", type=int, default=256)
    parser.add_argument(
        "--dictionary-mode",
        choices=("independent", "pair", "triple", "mixed"),
        default="mixed",
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    codes = load_codes(arguments.codes)
    if arguments.verify_only:
        payload = np.load(arguments.output)
        stored_codes = payload["codes"]
        denominators = payload["denominators"]
        assignments = payload["assignments"]
        assert np.array_equal(stored_codes, codes)
        verify_archive(codes, denominators, assignments)
        print(
            f"verified {int(np.count_nonzero(assignments >= 0))} exact "
            "support-17 H3 family assignments"
        )
        return

    dictionary = []
    seen = set()
    candidate_index = 0
    while len(dictionary) < arguments.dictionary_size:
        denominators = random_denominator_tuple(
            candidate_index, arguments.seed, arguments.dictionary_mode
        )
        candidate_index += 1
        key = canonical_denominators(denominators)
        if key in seen:
            continue
        seen.add(key)
        dictionary.append(denominators)

    tasks = list(enumerate(dictionary))
    context = mp.get_context("fork")
    with context.Pool(
        arguments.workers,
        initializer=initialize_worker,
        initargs=(str(arguments.codes),),
    ) as pool:
        results = list(
            pool.imap_unordered(numerical_cover_task, tasks, chunksize=1)
        )
    results.sort(key=lambda item: (-len(item[1]), item[0]))
    numerical_hits = sum(len(item[1]) for item in results)
    print(
        f"dictionary={len(dictionary)} numerical incidence hits={numerical_hits}",
        flush=True,
    )

    signs = decode_codes(codes)
    assignments = np.full(len(codes), -1, dtype=np.int32)
    selected_denominators = []
    selected_sources = []
    exact_margins = []
    for source, covered, _ in results:
        new_families = [
            int(family)
            for family in covered
            if assignments[int(family)] < 0
        ]
        if not new_families:
            continue
        exact_hits = []
        margins = []
        for family in new_families:
            hit, margin = exact_family_hit(
                signs[family], dictionary[source]
            )
            if hit:
                exact_hits.append(family)
                margins.append(margin)
        if not exact_hits:
            continue
        selected = len(selected_denominators)
        selected_denominators.append(dictionary[source])
        selected_sources.append(source)
        exact_margins.append(min(margins))
        assignments[exact_hits] = selected
        print(
            f"selected tuple={selected} source={source} "
            f"new_exact={len(exact_hits)} total={np.count_nonzero(assignments >= 0)}",
            flush=True,
        )

    denominator_array = np.array(selected_denominators, dtype=np.int64)
    if not len(selected_denominators):
        denominator_array = np.empty((0, HEADS, WIDTH), dtype=np.int64)
    np.savez_compressed(
        arguments.output,
        codes=codes,
        denominators=denominator_array,
        assignments=assignments,
        dictionary_source_indices=np.array(selected_sources, dtype=np.int32),
        minimum_exact_kernel_margins=np.array(exact_margins, dtype=object),
    )
    verify_archive(codes, denominator_array, assignments)

    uncovered = np.flatnonzero(assignments < 0)
    profiles = Counter(zero_layer_profile(signs[index]) for index in uncovered)
    summary = {
        "status": (
            "Every covered family has an exact rank-15 restriction and "
            "forced-sign kernel certificate. Uncovered families are exact "
            "misses for this finite dictionary only."
        ),
        "dictionary_size": len(dictionary),
        "dictionary_mode": arguments.dictionary_mode,
        "seed": arguments.seed,
        "workers": arguments.workers,
        "numerical_incidence_hits": numerical_hits,
        "selected_tuples": len(selected_denominators),
        "exact_covered_families": int(np.count_nonzero(assignments >= 0)),
        "uncovered_families": int(len(uncovered)),
        "top_uncovered_zero_layer_profiles": [
            {"profile": list(profile), "count": count}
            for profile, count in profiles.most_common(20)
        ],
    }
    arguments.summary.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    print(f"wrote {arguments.output}", flush=True)
    print(f"wrote {arguments.summary}", flush=True)


if __name__ == "__main__":
    main()
