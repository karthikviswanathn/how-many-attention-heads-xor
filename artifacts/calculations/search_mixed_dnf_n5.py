#!/usr/bin/env python3
"""Exhaustive mixed-literal two-term and three-term DNF search on five bits.

There are 242 nonempty mixed-literal cubes.  This script enumerates every
union of two or three distinct cubes, includes CNFs through output
complementation, deduplicates truth tables, and classifies degree at most two
with exact integer sign certificates.  Degree-two masks are screened against
the learned two-head denominator dictionary, then rare misses receive exact
orientation-cycle searches.

As elsewhere, failure of the final randomized search is not an H2 lower bound.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import multiprocessing as mp
import os
from pathlib import Path
from typing import Iterable

os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np

import search_adversarial_low_dimension as core


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "mixed_dnf_n5_results.json"
DEFAULT_ARCHIVE = HERE / "mixed_dnf_n5_degree_masks.npz"


def literal_cube_masks() -> list[int]:
    masks = []
    for code in range(1, 3**5):
        digits = []
        value = code
        for _ in range(5):
            digits.append(value % 3)
            value //= 3
        mask = 0
        for vertex in range(32):
            if all(
                literal == 0
                or ((vertex >> coordinate) & 1) == literal - 1
                for coordinate, literal in enumerate(digits)
            ):
                mask |= 1 << vertex
        masks.append(mask)
    assert len(masks) == len(set(masks)) == 242
    return masks


def enumerate_dnf_masks() -> tuple[np.ndarray, dict[str, int]]:
    terms = literal_cube_masks()
    full = (1 << 32) - 1
    pair_masks = set()
    for first, second in itertools.combinations(terms, 2):
        mask = first | second
        pair_masks.add(min(mask, full ^ mask))
    all_masks = set(pair_masks)
    for first, second, third in itertools.combinations(terms, 3):
        mask = first | second | third
        all_masks.add(min(mask, full ^ mask))
    diagnostics = {
        "nonempty_literal_cubes": len(terms),
        "raw_two_term_combinations": math_comb(242, 2),
        "raw_three_term_combinations": math_comb(242, 3),
        "deduplicated_two_term_masks_mod_output_complement": len(pair_masks),
        "deduplicated_all_masks_mod_output_complement": len(all_masks),
    }
    return np.array(sorted(all_masks), dtype=np.uint32), diagnostics


def math_comb(n: int, k: int) -> int:
    answer = 1
    for value in range(1, k + 1):
        answer = answer * (n - value + 1) // value
    return answer


def classify_chunk(chunk: Iterable[int]) -> tuple[list[int], list[int]]:
    evaluation = core.monomial_matrix(5, 2)
    degree_two = []
    higher = []
    for raw_mask in chunk:
        mask = int(raw_mask)
        result = core.exact_integer_separator(
            core.signs_from_mask(mask, 5), evaluation
        )
        if result is None:
            higher.append(mask)
        else:
            degree_two.append(mask)
    return degree_two, higher


def certificate_chunk(chunk: Iterable[int]) -> tuple[list[int], list[list[int]]]:
    evaluation = core.monomial_matrix(5, 2)
    masks = []
    coefficients = []
    for raw_mask in chunk:
        mask = int(raw_mask)
        result = core.exact_integer_separator(
            core.signs_from_mask(mask, 5), evaluation
        )
        if result is None:
            raise RuntimeError(f"stored degree-two mask lost its certificate: {mask:#x}")
        masks.append(mask)
        coefficients.append([int(value) for value in result[0]])
    return masks, coefficients


def exact_degree_classification(
    masks: np.ndarray, workers: int, chunk_size: int
) -> tuple[np.ndarray, np.ndarray]:
    chunks = [
        masks[index : index + chunk_size].tolist()
        for index in range(0, len(masks), chunk_size)
    ]
    degree_two = []
    higher = []
    completed = 0
    if workers == 1:
        iterator = map(classify_chunk, chunks)
        pool = None
    else:
        pool = mp.get_context("spawn").Pool(processes=workers)
        iterator = pool.imap_unordered(classify_chunk, chunks)
    try:
        for low, high in iterator:
            degree_two.extend(low)
            higher.extend(high)
            completed += len(low) + len(high)
            if completed % (20 * chunk_size) == 0 or completed == len(masks):
                print(
                    f"exact degree classification {completed}/{len(masks)}; "
                    f"degree<=2={len(degree_two)} higher={len(higher)}",
                    flush=True,
                )
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return (
        np.array(sorted(degree_two), dtype=np.uint32),
        np.array(sorted(higher), dtype=np.uint32),
    )


def load_active_dictionary(limit: int, seed: int) -> list[np.ndarray]:
    candidates = []
    for filename in (
        "adversarial_n5_broad_results.json",
        "adversarial_n5_results.json",
    ):
        path = HERE / filename
        if path.exists():
            payload = json.loads(path.read_text())
            candidates.extend(
                np.array(pair, dtype=np.int64) for pair in payload["dictionary"]
            )
    candidates.extend(core.build_dictionary(5, 3 * limit, seed))
    answer = []
    seen = set()
    for pair in candidates:
        key = core.canonical_denominator_pair(pair)
        if key in seen:
            continue
        seen.add(key)
        answer.append(np.array(key, dtype=np.int64))
        if len(answer) >= limit:
            break
    return answer


def batch_heuristic_screen(
    masks: np.ndarray,
    dictionary: list[np.ndarray],
    pairs: int,
    iterations: int,
    batch_size: int,
) -> np.ndarray:
    shifts = np.arange(32, dtype=np.uint32)
    signs = (
        2 * ((masks[:, None] >> shifts[None, :]) & 1).astype(np.int8) - 1
    )
    coverage = np.zeros(len(masks), dtype=np.int16)
    for dictionary_index, denominators in enumerate(dictionary[:pairs]):
        features = core.whitened_feature_space(5, denominators)
        for start in range(0, len(masks), batch_size):
            stop = min(start + batch_size, len(masks))
            coverage[start:stop] += core.gilbert_cover(
                signs[start:stop], features, iterations
            ).astype(np.int16)
        print(
            f"DNF heuristic pair {dictionary_index + 1}/{pairs}: "
            f"zero-count={int(np.sum(coverage == 0))}",
            flush=True,
        )
    return coverage


def archive_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def augment_certificate_archive(
    archive: Path, workers: int, chunk_size: int
) -> None:
    data = np.load(archive)
    degree_two = data["degree_two_masks"]
    higher = data["higher_degree_masks"]
    data.close()
    chunks = [
        degree_two[index : index + chunk_size].tolist()
        for index in range(0, len(degree_two), chunk_size)
    ]
    all_masks = []
    all_coefficients = []
    completed = 0
    if workers == 1:
        iterator = map(certificate_chunk, chunks)
        pool = None
    else:
        pool = mp.get_context("spawn").Pool(processes=workers)
        iterator = pool.imap_unordered(certificate_chunk, chunks)
    try:
        for masks, coefficients in iterator:
            all_masks.extend(masks)
            all_coefficients.extend(coefficients)
            completed += len(masks)
            if completed % (20 * chunk_size) == 0 or completed == len(degree_two):
                print(
                    f"archiving exact quadratic certificates "
                    f"{completed}/{len(degree_two)}",
                    flush=True,
                )
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    order = np.argsort(np.array(all_masks, dtype=np.uint32))
    sorted_masks = np.array(all_masks, dtype=np.uint32)[order]
    coefficients = np.array(all_coefficients, dtype=np.int64)[order]
    assert np.array_equal(sorted_masks, degree_two)
    np.savez_compressed(
        archive,
        degree_two_masks=degree_two,
        degree_two_coefficients=coefficients,
        higher_degree_masks=higher,
    )


def verify_payload(payload: dict[str, object], archive: Path) -> None:
    data = np.load(archive)
    degree_two = data["degree_two_masks"]
    higher = data["higher_degree_masks"]
    assert len(np.intersect1d(degree_two, higher)) == 0
    assert len(degree_two) == payload["degree_classification"]["degree_at_most_two"]
    assert len(higher) == payload["degree_classification"]["degree_at_least_three"]
    assert archive_digest(archive) == payload["archive_sha256"]
    if "degree_two_coefficients" in data.files:
        coefficients = data["degree_two_coefficients"]
        assert coefficients.shape == (len(degree_two), 16)
        evaluation = core.monomial_matrix(5, 2)
        for start in range(0, len(degree_two), 10000):
            stop = min(start + 10000, len(degree_two))
            scores = coefficients[start:stop] @ evaluation.T
            shifts = np.arange(32, dtype=np.uint32)
            signs = (
                2
                * (
                    (degree_two[start:stop, None] >> shifts[None, :]) & 1
                ).astype(np.int64)
                - 1
            )
            assert np.all(signs * scores > 0)
    affine = core.affine_matrix(5).astype(object)
    for record in payload["final_records"]:
        mask = int(record["truth_mask_hex"], 16)
        signs = core.signs_from_mask(mask, 5)
        polynomial = np.array(record["degree_two_coefficients"], dtype=object)
        assert np.all(
            signs
            * (core.monomial_matrix(5, 2).astype(object) @ polynomial)
            > 0
        )
        search = record["h2_certificate_or_search"]
        if not search["found"]:
            continue
        denominators = np.array(search["denominators"], dtype=np.int64)
        for denominator in denominators:
            assert np.all(denominator[1:] > 0) or np.all(denominator[1:] < 0)
            assert np.all(affine @ denominator.astype(object) > 0)
        coefficients = np.array(search["cleared_score_coefficients"], dtype=object)
        matrix = core.cleared_two_head_matrix(5, denominators).astype(object)
        signed_scores = signs * (matrix @ coefficients)
        assert np.all(signed_scores > 0)
        assert min(map(int, signed_scores)) == search["minimum_signed_cleared_score"]
    print(
        f"verified mixed-DNF archive and {len(payload['final_records'])} finalists",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 1)))
    parser.add_argument("--chunk-size", type=int, default=1000)
    parser.add_argument("--dictionary-size", type=int, default=320)
    parser.add_argument("--heuristic-pairs", type=int, default=32)
    parser.add_argument("--heuristic-iterations", type=int, default=160)
    parser.add_argument("--heuristic-retain", type=int, default=2048)
    parser.add_argument("--prefix-pairs", type=int, default=24)
    parser.add_argument("--full-scan-retain", type=int, default=128)
    parser.add_argument("--finalists", type=int, default=32)
    parser.add_argument("--orientation-trials", type=int, default=100000)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--augment-certificates", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_payload(json.loads(arguments.output.read_text()), arguments.archive)
        return

    if arguments.augment_certificates:
        augment_certificate_archive(
            arguments.archive, arguments.workers, arguments.chunk_size
        )
        payload = json.loads(arguments.output.read_text())
        payload["archive_sha256"] = archive_digest(arguments.archive)
        payload["archive_contains_all_quadratic_coefficients"] = True
        arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
        verify_payload(payload, arguments.archive)
        return

    masks, enumeration = enumerate_dnf_masks()
    print(json.dumps(enumeration), flush=True)
    if arguments.limit:
        masks = masks[: arguments.limit]
        enumeration["debug_limit"] = arguments.limit
    degree_two, higher = exact_degree_classification(
        masks, arguments.workers, arguments.chunk_size
    )
    np.savez_compressed(
        arguments.archive,
        degree_two_masks=degree_two,
        higher_degree_masks=higher,
    )

    dictionary = load_active_dictionary(arguments.dictionary_size, arguments.seed)
    print(f"active dictionary size={len(dictionary)}", flush=True)
    heuristic = batch_heuristic_screen(
        degree_two,
        dictionary,
        min(arguments.heuristic_pairs, len(dictionary)),
        arguments.heuristic_iterations,
        batch_size=4096,
    )
    order = np.lexsort((degree_two, heuristic))
    retained = [
        int(degree_two[index])
        for index in order[: min(arguments.heuristic_retain, len(order))]
    ]
    prefix_ranked = []
    for index, mask in enumerate(retained):
        hits = core.exact_dictionary_hits(
            mask, 5, dictionary[: arguments.prefix_pairs]
        )
        prefix_ranked.append((len(hits), mask))
        if (index + 1) % 256 == 0:
            print(
                f"DNF exact prefix scan {index + 1}/{len(retained)}",
                flush=True,
            )
    prefix_ranked.sort()
    full_pool = [
        mask for _, mask in prefix_ranked[: arguments.full_scan_retain]
    ]

    fully_ranked = []
    for index, mask in enumerate(full_pool):
        hits = core.exact_dictionary_hits(mask, 5, dictionary)
        fully_ranked.append((len(hits), mask, hits))
        print(
            f"DNF full scan {index + 1}/{len(full_pool)}: "
            f"hits={len(hits)} mask=0x{mask:08x}",
            flush=True,
        )
    fully_ranked.sort()

    cache: dict[int, list[int] | None] = {}
    initial_dictionary_size = len(dictionary)
    records = []
    for index, (hit_count, mask, hits) in enumerate(
        fully_ranked[: arguments.finalists]
    ):
        search = None
        if hits:
            search = core.exact_pair_certificate(
                mask,
                5,
                dictionary[hits[0]],
                "fixed-dictionary",
                hits[0],
            )
        else:
            for dictionary_index in range(initial_dictionary_size, len(dictionary)):
                search = core.exact_pair_certificate(
                    mask,
                    5,
                    dictionary[dictionary_index],
                    "active-dictionary-reuse",
                    dictionary_index,
                )
                if search is not None:
                    break
        if search is None:
            search = core.orientation_cycle_search(
                mask,
                5,
                arguments.seed + 100003 * index,
                arguments.orientation_trials,
                64,
            )
        if search["found"]:
            key = core.canonical_denominator_pair(search["denominators"])
            if key not in {
                core.canonical_denominator_pair(pair) for pair in dictionary
            }:
                dictionary.append(np.array(key, dtype=np.int64))
        polynomial = core.degree_two_certificate(mask, 5, cache)
        assert polynomial is not None
        records.append(
            {
                "truth_mask_hex": f"0x{mask:08x}",
                "degree_two_coefficients": polynomial,
                "fixed_dictionary_hit_count": hit_count,
                "h2_certificate_or_search": search,
            }
        )
        print(
            f"DNF finalist {index + 1}: method={search['method']} "
            f"found={search['found']} mask=0x{mask:08x}",
            flush=True,
        )

    payload = {
        "status": (
            "Exact degree-two and H2 successes are verified.  A randomized H2 "
            "search failure is not a head-complexity lower bound."
        ),
        "enumeration": enumeration,
        "degree_classification": {
            "degree_at_most_two": len(degree_two),
            "degree_at_least_three": len(higher),
        },
        "archive": arguments.archive.name,
        "archive_sha256": archive_digest(arguments.archive),
        "parameters": {
            "dictionary_size": arguments.dictionary_size,
            "heuristic_pairs": arguments.heuristic_pairs,
            "heuristic_iterations": arguments.heuristic_iterations,
            "heuristic_retained": len(retained),
            "full_scan_pool": len(full_pool),
            "orientation_trials": arguments.orientation_trials,
        },
        "heuristic_zero_count": int(np.sum(heuristic == 0)),
        "dictionary": [pair.tolist() for pair in dictionary],
        "higher_degree_masks_sample": [f"0x{int(mask):08x}" for mask in higher[:128]],
        "final_records": records,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    verify_payload(payload, arguments.archive)


if __name__ == "__main__":
    main()
