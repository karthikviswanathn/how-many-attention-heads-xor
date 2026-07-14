#!/usr/bin/env python3
"""Adversarial low-dimensional search for degree-two versus two-head gaps.

The search has three deliberately separate levels of rigor.

1. A fast Gilbert convex-hull iteration scores many sign cells against a fixed
   dictionary of admissible denominator pairs.  This is only a screening
   heuristic.
2. Every retained sign cell is certified to have threshold degree at most two
   by an exact integer sign polynomial, and fixed-dictionary misses are checked
   by linear programming against every dictionary pair.
3. Every final miss receives a deterministic orientation-cycle search.  Any
   reported two-head success is quantized and rechecked with integer arithmetic.

Failure at levels 1 or 3 is not an H2 lower bound.  It only identifies a target
for a future global infeasibility proof.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
from scipy.optimize import linprog


HERE = Path(__file__).resolve().parent
CORPUS_N5 = HERE / "n5_degree2_search_results.json"
DEFAULT_OUTPUT = HERE / "adversarial_low_dimension_results.json"


def cube(n: int) -> np.ndarray:
    return ((np.arange(1 << n)[:, None] >> np.arange(n)) & 1).astype(np.int64)


def affine_matrix(n: int) -> np.ndarray:
    return np.column_stack([np.ones(1 << n, dtype=np.int64), cube(n)])


def monomial_matrix(n: int, degree: int = 2) -> np.ndarray:
    x = cube(n)
    columns = []
    for size in range(degree + 1):
        for subset in itertools.combinations(range(n), size):
            if subset:
                columns.append(np.prod(x[:, subset], axis=1))
            else:
                columns.append(np.ones(1 << n, dtype=np.int64))
    return np.column_stack(columns).astype(np.int64)


def signs_from_mask(mask: int, n: int) -> np.ndarray:
    return np.array(
        [1 if (mask >> index) & 1 else -1 for index in range(1 << n)],
        dtype=np.int64,
    )


def mask_from_signs(signs: np.ndarray) -> int:
    answer = 0
    for index in np.flatnonzero(signs > 0):
        answer |= 1 << int(index)
    return answer


def complement_canonical(mask: int, n: int) -> int:
    complement = ((1 << (1 << n)) - 1) ^ mask
    return min(mask, complement)


def coordinate_flip(mask: int, flip: int, n: int) -> int:
    answer = 0
    for vertex in range(1 << n):
        if (mask >> (vertex ^ flip)) & 1:
            answer |= 1 << vertex
    return answer


def cleared_two_head_matrix(n: int, denominators: np.ndarray) -> np.ndarray:
    affine = affine_matrix(n)
    values = affine @ denominators.T
    return np.column_stack(
        [
            values[:, 0] * values[:, 1],
            affine * values[:, 1, None],
            affine * values[:, 0, None],
        ]
    ).astype(np.int64)


def exact_integer_separator(
    signs: np.ndarray, matrix: np.ndarray
) -> Optional[tuple[np.ndarray, float]]:
    """Find and exactly verify an integer separator in the matrix column span."""
    floating = matrix.astype(float)
    norms = np.linalg.norm(floating, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = floating[:, keep] / norms[keep]
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
    if not result.success or -float(result.fun) <= 1e-10:
        return None

    coefficients = np.zeros(matrix.shape[1], dtype=float)
    coefficients[keep] = result.x[:variables] / norms[keep]
    margin = float(np.min(signs * (floating @ coefficients)))
    if margin <= 1e-12:
        return None
    row_l1 = max(sum(abs(int(value)) for value in row) for row in matrix.tolist())
    scale = max(1, int(math.ceil((row_l1 + 1) / (2.0 * margin))))
    matrix_object = matrix.astype(object)
    signs_object = signs.astype(object)
    for _ in range(160):
        exact = np.rint(scale * coefficients).astype(object)
        signed_scores = signs_object * (matrix_object @ exact)
        if all(int(value) > 0 for value in signed_scores):
            integers = [int(value) for value in exact]
            common = 0
            for value in integers:
                common = math.gcd(common, abs(value))
            if common > 1:
                integers = [value // common for value in integers]
            return np.array(integers, dtype=object), margin
        scale *= 2
    return None


def floating_separable(signs: np.ndarray, matrix: np.ndarray) -> bool:
    floating = matrix.astype(float)
    norms = np.linalg.norm(floating, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = floating[:, keep] / norms[keep]
    result = linprog(
        np.zeros(normalized.shape[1]),
        A_ub=-(signs[:, None] * normalized),
        b_ub=-np.ones(len(signs)),
        bounds=[(None, None)] * normalized.shape[1],
        method="highs",
    )
    return bool(result.success)


def canonical_denominator_pair(denominators: Iterable[Iterable[int]]) -> tuple:
    heads = []
    for denominator in denominators:
        values = [int(value) for value in denominator]
        common = 0
        for value in values:
            common = math.gcd(common, abs(value))
        if common > 1:
            values = [value // common for value in values]
        heads.append(tuple(values))
    return tuple(sorted(heads))


def oriented_denominator(weights: Iterable[int], orientation: int) -> list[int]:
    weights = [int(value) for value in weights]
    if orientation > 0:
        return [1] + weights
    return [sum(weights) + 1] + [-value for value in weights]


def simple_dictionary(n: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    patterns = [
        np.ones(n, dtype=np.int64),
        np.arange(1, n + 1, dtype=np.int64),
        np.arange(n, 0, -1, dtype=np.int64),
        np.array([1 << (index % 4) for index in range(n)], dtype=np.int64),
    ]
    for coordinate in range(n):
        weights = np.ones(n, dtype=np.int64)
        weights[coordinate] = 8
        patterns.append(weights)
        dominant = np.ones(n, dtype=np.int64)
        dominant[coordinate] = 4096
        patterns.append(dominant)
        near_face = np.full(n, 4096, dtype=np.int64)
        near_face[coordinate] = 1
        patterns.append(near_face)
    patterns.append(
        np.array([1 << (2 * index) for index in range(n)], dtype=np.int64)
    )
    patterns.append(
        np.array([1 << (2 * (n - 1 - index)) for index in range(n)], dtype=np.int64)
    )
    patterns.extend(
        rng.integers(1, 17, size=(64, n), dtype=np.int64)
    )
    pairs = []
    for index, first in enumerate(patterns):
        second = patterns[(17 * index + 7) % len(patterns)]
        for orientations in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            pairs.append(
                np.array(
                    [
                        oriented_denominator(first, orientations[0]),
                        oriented_denominator(second, orientations[1]),
                    ],
                    dtype=np.int64,
                )
            )
    return pairs


def corpus_dictionary_n5(limit: int, seed: int) -> list[np.ndarray]:
    payload = json.loads(CORPUS_N5.read_text())
    records = payload["records"]
    hard_masks = {
        "0xe5312872",
        "0x51bafc84",
        "0x179a43dc",
        "0x99c105ad",
    }
    selected = [
        record
        for record in records
        if record["truth_mask_hex"] in hard_masks
    ]
    candidates = []
    for record in records:
        search = record["h2_search"]
        denominators = search.get("denominators")
        if denominators is None:
            continue
        if max(abs(int(value)) for head in denominators for value in head) > 256:
            continue
        hardness = int(search.get("trial", 0))
        candidates.append((hardness, record))
    candidates.sort(key=lambda item: item[0], reverse=True)
    selected.extend(record for _, record in candidates[: max(32, limit // 2)])
    rng = np.random.default_rng(seed)
    remaining = [record for _, record in candidates]
    if remaining:
        indices = rng.choice(
            len(remaining), size=min(limit, len(remaining)), replace=False
        )
        selected.extend(remaining[int(index)] for index in indices)

    answer = []
    seen = set()
    for record in selected:
        denominators = record["h2_search"].get("denominators")
        if denominators is None:
            continue
        key = canonical_denominator_pair(denominators)
        if key in seen:
            continue
        seen.add(key)
        answer.append(np.array(key, dtype=np.int64))
        if len(answer) >= limit:
            break
    return answer


def build_dictionary(n: int, limit: int, seed: int) -> list[np.ndarray]:
    candidates = simple_dictionary(n, seed)
    if n == 5 and CORPUS_N5.exists():
        candidates = corpus_dictionary_n5(3 * limit, seed) + candidates
    if n == 6 and CORPUS_N5.exists():
        extensions = []
        for pair in corpus_dictionary_n5(2 * limit, seed):
            for new_weight in (1, 4, 16):
                extended = []
                for denominator in pair:
                    slopes = denominator[1:]
                    if np.all(slopes > 0):
                        extended.append(np.concatenate([denominator, [new_weight]]))
                    else:
                        extended.append(
                            np.concatenate(
                                [[denominator[0] + new_weight], slopes, [-new_weight]]
                            )
                        )
                extensions.append(np.array(extended, dtype=np.int64))
        candidates = extensions + candidates
    answer = []
    seen = set()
    affine = affine_matrix(n)
    for pair in candidates:
        key = canonical_denominator_pair(pair)
        if key in seen:
            continue
        array = np.array(key, dtype=np.int64)
        if not all(
            (np.all(head[1:] > 0) or np.all(head[1:] < 0))
            and np.all(affine @ head > 0)
            for head in array
        ):
            continue
        seen.add(key)
        answer.append(array)
        if len(answer) >= limit:
            break
    return answer


def order_dictionary_by_pilot(
    n: int,
    dictionary: list[np.ndarray],
    seed: int,
    iterations: int = 500,
) -> list[np.ndarray]:
    """Put broadly useful pairs first without changing the fixed dictionary."""
    if n == 5 and CORPUS_N5.exists():
        payload = json.loads(CORPUS_N5.read_text())
        pilot_masks = [int(record["truth_mask_hex"], 16) for record in payload["records"]]
    else:
        cache: dict[int, Optional[list[int]]] = {}
        pilot_masks = sorted(initial_masks(n, cache))
    rng = np.random.default_rng(seed)
    if len(pilot_masks) > 1024:
        indices = rng.choice(len(pilot_masks), size=1024, replace=False)
        pilot_masks = [pilot_masks[int(index)] for index in indices]
    signs = np.array(
        [signs_from_mask(mask, n) for mask in pilot_masks], dtype=np.int8
    )
    scores = []
    for index, denominators in enumerate(dictionary):
        hit_count = int(
            np.sum(
                gilbert_cover(
                    signs,
                    whitened_feature_space(n, denominators),
                    iterations,
                )
            )
        )
        scores.append((hit_count, index))
    scores.sort(reverse=True)
    print(
        "pilot dictionary coverage: "
        + ", ".join(str(score) for score, _ in scores[:8]),
        flush=True,
    )
    return [dictionary[index] for _, index in scores]


def whitened_feature_space(n: int, denominators: np.ndarray) -> np.ndarray:
    affine = affine_matrix(n).astype(float)
    values = affine @ denominators.astype(float).T
    features = np.column_stack(
        [
            np.ones(1 << n),
            affine / values[:, 0, None],
            affine / values[:, 1, None],
        ]
    )
    left, singular, _ = np.linalg.svd(features, full_matrices=False)
    keep = singular > singular[0] * 1e-11
    basis = left[:, keep]
    return basis / np.linalg.norm(basis, axis=1, keepdims=True)


def gilbert_cover(
    signs: np.ndarray, features: np.ndarray, iterations: int
) -> np.ndarray:
    """Return only positively certified heuristic hits, with no false hits."""
    labels = signs.astype(float)
    point_count = labels.shape[1]
    current = (labels @ features) / point_count
    active = np.ones(len(labels), dtype=bool)
    for _ in range(iterations):
        indices = np.flatnonzero(active)
        if not len(indices):
            break
        scores = labels[indices] * (current[indices] @ features.T)
        vertices = np.argmin(scores, axis=1)
        minima = scores[np.arange(len(indices)), vertices]
        found = minima > 1e-10
        active[indices[found]] = False
        indices = indices[~found]
        vertices = vertices[~found]
        if not len(indices):
            break
        selected = labels[indices, vertices, None] * features[vertices]
        inner = np.sum(current[indices] * selected, axis=1)
        norm = np.sum(current[indices] * current[indices], axis=1)
        denominator = np.sum((current[indices] - selected) ** 2, axis=1)
        step = np.clip(
            (norm - inner) / np.maximum(denominator, 1e-30), 0.0, 1.0
        )
        current[indices] = (
            (1.0 - step[:, None]) * current[indices]
            + step[:, None] * selected
        )
    return ~active


def screen_masks(
    masks: list[int],
    n: int,
    dictionary: list[np.ndarray],
    iterations: int,
) -> np.ndarray:
    signs = np.array([signs_from_mask(mask, n) for mask in masks], dtype=np.int8)
    coverage = np.zeros(len(masks), dtype=np.int32)
    for index, denominators in enumerate(dictionary):
        features = whitened_feature_space(n, denominators)
        coverage += gilbert_cover(signs, features, iterations).astype(np.int32)
        if (index + 1) % 32 == 0:
            print(
                f"  screened {index + 1}/{len(dictionary)} dictionary pairs; "
                f"heuristic zero-count={int(np.sum(coverage == 0))}",
                flush=True,
            )
    return coverage


def degree_two_certificate(
    mask: int, n: int, cache: dict[int, Optional[list[int]]]
) -> Optional[list[int]]:
    mask = complement_canonical(mask, n)
    if mask in cache:
        return cache[mask]
    result = exact_integer_separator(signs_from_mask(mask, n), monomial_matrix(n, 2))
    certificate = None if result is None else [int(value) for value in result[0]]
    cache[mask] = certificate
    return certificate


def canonical_quadratic_matrix(
    coefficients: np.ndarray, n: int
) -> np.ndarray:
    """Use the zero-diagonal affine homogenization as a rank proxy."""
    batch = len(coefficients)
    matrices = np.zeros((batch, n + 1, n + 1), dtype=float)
    matrices[:, 0, 0] = coefficients[:, 0]
    matrices[:, 0, 1:] = coefficients[:, 1 : n + 1] / 2.0
    matrices[:, 1:, 0] = coefficients[:, 1 : n + 1] / 2.0
    column = n + 1
    for first in range(n):
        for second in range(first + 1, n):
            value = coefficients[:, column] / 2.0
            matrices[:, first + 1, second + 1] = value
            matrices[:, second + 1, first + 1] = value
            column += 1
    return matrices


def sample_small_coefficient_cells(
    n: int,
    samples: int,
    retain: int,
    seed: int,
    batch_size: int = 20000,
) -> tuple[list[int], dict[int, list[int]], dict[str, object]]:
    """Sample many explicit quadratics and retain high-rank narrow-cell proxies."""
    rng = np.random.default_rng(seed)
    evaluation = monomial_matrix(n, 2)
    nonconstant = evaluation[:, 1:]
    retained: dict[int, tuple[float, list[int]]] = {}
    family_counts = {"dense": 0, "sparse": 0, "hierarchical": 0}
    generated = 0
    batch_index = 0
    while generated < samples:
        size = min(batch_size, samples - generated)
        family = ("dense", "sparse", "hierarchical")[batch_index % 3]
        if family == "dense":
            slopes = rng.integers(-5, 6, size=(size, nonconstant.shape[1]))
        elif family == "sparse":
            slopes = rng.integers(-9, 10, size=(size, nonconstant.shape[1]))
            slopes *= rng.random(size=slopes.shape) < 0.28
        else:
            exponents = rng.integers(0, 5, size=(size, nonconstant.shape[1]))
            signs = rng.choice(np.array([-1, 1]), size=exponents.shape)
            slopes = signs * (1 << exponents)
            slopes *= rng.random(size=slopes.shape) < 0.65
        empty = ~np.any(slopes[:, n:] != 0, axis=1)
        if np.any(empty):
            columns = rng.integers(n, slopes.shape[1], size=int(np.sum(empty)))
            slopes[np.flatnonzero(empty), columns] = 1

        raw = slopes @ nonconstant.T
        ranks = rng.integers(0, (1 << n), size=size)
        thresholds = np.take_along_axis(
            np.sort(raw, axis=1), ranks[:, None], axis=1
        )[:, 0]
        coefficients = np.column_stack([1 - 2 * thresholds, 2 * slopes])
        values = coefficients @ evaluation.T
        assert np.all(values % 2 != 0)
        truth = values > 0
        vertex_count = 1 << n
        if vertex_count <= 64:
            weights = np.left_shift(
                np.uint64(1), np.arange(vertex_count, dtype=np.uint64)
            )
            masks_low = truth.astype(np.uint64) @ weights
            masks_high = None
        else:
            assert vertex_count == 128
            weights = np.left_shift(
                np.uint64(1), np.arange(64, dtype=np.uint64)
            )
            truth_uint = truth.astype(np.uint64)
            masks_low = truth_uint[:, :64] @ weights
            masks_high = truth_uint[:, 64:] @ weights

        singular = np.linalg.svd(
            canonical_quadratic_matrix(coefficients, n),
            compute_uv=False,
        )
        tail = np.sqrt(np.sum(singular[:, 4:] ** 2, axis=1))
        total = np.sqrt(np.sum(singular**2, axis=1))
        cell_margin = np.min(np.abs(values), axis=1) / np.maximum(
            np.linalg.norm(coefficients, axis=1), 1.0
        )
        scores = tail / np.maximum(total * cell_margin, 1e-14)
        local_count = min(size, max(4 * retain, 256))
        local = np.argpartition(scores, -local_count)[-local_count:]
        for row in local:
            raw_mask = int(masks_low[row])
            if masks_high is not None:
                raw_mask |= int(masks_high[row]) << 64
            mask = complement_canonical(raw_mask, n)
            coefficients_row = [int(value) for value in coefficients[row]]
            if mask != raw_mask:
                coefficients_row = [-value for value in coefficients_row]
            score = float(scores[row])
            previous = retained.get(mask)
            if previous is None or score > previous[0]:
                retained[mask] = (score, coefficients_row)

        if len(retained) > 8 * retain:
            best = sorted(retained.items(), key=lambda item: item[1][0], reverse=True)
            retained = dict(best[: 4 * retain])
        generated += size
        family_counts[family] += size
        batch_index += 1
        if generated % (10 * batch_size) == 0 or generated == samples:
            print(
                f"coefficient sampling {generated}/{samples}; "
                f"proxy pool={len(retained)}",
                flush=True,
            )

    best = sorted(retained.items(), key=lambda item: item[1][0], reverse=True)
    best = best[:retain]
    masks = [mask for mask, _ in best]
    certificates = {mask: record[1] for mask, record in best}
    diagnostics = {
        "samples": samples,
        "families": family_counts,
        "unique_proxy_pool": len(retained),
        "retained": len(masks),
        "maximum_proxy_score": best[0][1][0] if best else None,
        "minimum_retained_proxy_score": best[-1][1][0] if best else None,
    }
    return masks, certificates, diagnostics


def rank_coefficient_sample(
    masks: list[int],
    n: int,
    dictionary: list[np.ndarray],
    scoring_pairs: int,
    keep: int,
) -> tuple[list[int], list[dict[str, int]]]:
    """Use a small exact dictionary prefix before the full finalist scan."""
    ranked = []
    prefix = dictionary[: min(scoring_pairs, len(dictionary))]
    for index, mask in enumerate(masks):
        hits = exact_dictionary_hits(mask, n, prefix)
        ranked.append((len(hits), mask))
        if (index + 1) % 256 == 0:
            print(
                f"exact coefficient-pool scoring {index + 1}/{len(masks)}",
                flush=True,
            )
    ranked.sort()
    selected = [mask for _, mask in ranked[:keep]]
    histogram: dict[int, int] = {}
    for hit_count, _ in ranked:
        histogram[hit_count] = histogram.get(hit_count, 0) + 1
    return selected, [
        {"exact_prefix_hits": hit_count, "count": count}
        for hit_count, count in sorted(histogram.items())
    ]


def initial_masks(n: int, cache: dict[int, Optional[list[int]]]) -> set[int]:
    if n == 5:
        seeds = [0xE5312872, 0x51BAFC84, 0x179A43DC, 0x99C105AD]
        masks = {
            complement_canonical(coordinate_flip(seed, flip, n), n)
            for seed in seeds
            for flip in range(1 << n)
        }
    else:
        rng = np.random.default_rng(90311)
        evaluation = monomial_matrix(n, 2)
        masks = set()
        for _ in range(512):
            coefficients = rng.integers(-4, 5, size=evaluation.shape[1])
            coefficients[0] = 0
            values = evaluation @ coefficients
            ordered = np.unique(values)
            if len(ordered) < 3:
                continue
            rank = int(rng.integers(1, len(ordered)))
            threshold = int(ordered[rank - 1] + ordered[rank])
            signs = np.where(2 * values > threshold, 1, -1)
            masks.add(complement_canonical(mask_from_signs(signs), n))
    return {
        mask
        for mask in masks
        if degree_two_certificate(mask, n, cache) is not None
    }


def hill_climb(
    n: int,
    dictionary: list[np.ndarray],
    rounds: int,
    beam_size: int,
    gilbert_iterations: int,
) -> tuple[list[int], dict[int, Optional[list[int]]], list[dict[str, int]]]:
    cache: dict[int, Optional[list[int]]] = {}
    beam = initial_masks(n, cache)
    visited = set(beam)
    history = []
    if len(beam) > beam_size:
        initial_list = sorted(beam)
        print(
            f"initial beam reduction: scoring {len(initial_list)} exact cells",
            flush=True,
        )
        initial_coverage = screen_masks(
            initial_list, n, dictionary, gilbert_iterations
        )
        initial_order = np.lexsort(
            (np.array(initial_list, dtype=object), initial_coverage)
        )
        beam = {
            initial_list[int(index)]
            for index in initial_order[:beam_size]
        }
        history.append(
            {
                "round": 0,
                "newly_visited": len(visited),
                "degree_two_candidates_scored": len(initial_list),
                "minimum_heuristic_coverage": int(np.min(initial_coverage)),
                "heuristic_zero_count": int(np.sum(initial_coverage == 0)),
            }
        )
    for round_index in range(rounds):
        candidates = set(beam)
        for mask in beam:
            for vertex in range(1 << n):
                neighbor = complement_canonical(mask ^ (1 << vertex), n)
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if degree_two_certificate(neighbor, n, cache) is not None:
                    candidates.add(neighbor)
        candidate_list = sorted(candidates)
        print(
            f"round {round_index + 1}: scoring {len(candidate_list)} exact "
            f"degree-two cells",
            flush=True,
        )
        coverage = screen_masks(
            candidate_list, n, dictionary, gilbert_iterations
        )
        order = np.lexsort((np.array(candidate_list, dtype=object), coverage))
        keep = order[: min(beam_size, len(order))]
        beam = {candidate_list[int(index)] for index in keep}
        history.append(
            {
                "round": round_index + 1,
                "newly_visited": len(visited),
                "degree_two_candidates_scored": len(candidate_list),
                "minimum_heuristic_coverage": int(np.min(coverage)),
                "heuristic_zero_count": int(np.sum(coverage == 0)),
            }
        )
        print(json.dumps(history[-1]), flush=True)
    return sorted(beam), cache, history


def exact_dictionary_hits(
    mask: int, n: int, dictionary: list[np.ndarray]
) -> list[int]:
    signs = signs_from_mask(mask, n)
    hits = []
    for index, denominators in enumerate(dictionary):
        matrix = cleared_two_head_matrix(n, denominators)
        if exact_integer_separator(signs, matrix) is not None:
            hits.append(index)
    return hits


def exact_pair_certificate(
    mask: int,
    n: int,
    denominators: np.ndarray,
    method: str,
    dictionary_index: Optional[int] = None,
) -> Optional[dict[str, object]]:
    signs = signs_from_mask(mask, n)
    matrix = cleared_two_head_matrix(n, denominators)
    result = exact_integer_separator(signs, matrix)
    if result is None:
        return None
    coefficients, margin = result
    signed_scores = signs.astype(object) * (
        matrix.astype(object) @ coefficients.astype(object)
    )
    answer = {
        "found": True,
        "method": method,
        "denominators": denominators.tolist(),
        "cleared_score_coefficients": [int(value) for value in coefficients],
        "minimum_signed_cleared_score": min(map(int, signed_scores)),
        "floating_margin": margin,
    }
    if dictionary_index is not None:
        answer["dictionary_index"] = dictionary_index
    return answer


def random_denominator(
    n: int, rng: np.random.Generator, orientation: int, weight_max: int
) -> np.ndarray:
    weights = rng.integers(1, weight_max + 1, size=n, dtype=np.int64)
    return np.array(oriented_denominator(weights, orientation), dtype=np.int64)


def orientation_cycle_search(
    mask: int,
    n: int,
    seed: int,
    trials: int,
    weight_max: int,
) -> dict[str, object]:
    signs = signs_from_mask(mask, n)
    rng = np.random.default_rng(seed)
    pairs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    for trial in range(trials):
        orientations = pairs[trial % 4]
        denominators = np.array(
            [
                random_denominator(n, rng, orientations[0], weight_max),
                random_denominator(n, rng, orientations[1], weight_max),
            ]
        )
        matrix = cleared_two_head_matrix(n, denominators)
        result = exact_integer_separator(signs, matrix)
        if result is None:
            continue
        coefficients, margin = result
        signed_scores = signs.astype(object) * (
            matrix.astype(object) @ coefficients.astype(object)
        )
        return {
            "found": True,
            "method": "orientation-cycle-random-search",
            "trial": trial,
            "orientations": list(orientations),
            "denominators": denominators.tolist(),
            "cleared_score_coefficients": [int(value) for value in coefficients],
            "minimum_signed_cleared_score": min(map(int, signed_scores)),
            "floating_margin": margin,
        }
    return {
        "found": False,
        "method": "orientation-cycle-random-search",
        "trials": trials,
        "weight_max": weight_max,
    }


def random_extreme_denominator(
    n: int,
    rng: np.random.Generator,
    orientation: int,
    trial: int,
    maximum_exponent: int,
) -> np.ndarray:
    """Sample near faces and vertices of the positive weight simplex."""
    exponents = rng.integers(0, maximum_exponent + 1, size=n)
    if trial % 3 == 1:
        exponents[:] = rng.integers(0, 3)
        exponents[int(rng.integers(0, n))] = maximum_exponent
    elif trial % 3 == 2:
        exponents[:] = maximum_exponent - rng.integers(0, 3)
        exponents[int(rng.integers(0, n))] = 0
    multipliers = rng.integers(1, 4, size=n, dtype=np.int64)
    weights = multipliers * np.left_shift(np.int64(1), exponents)
    baseline_exponent = int(rng.integers(0, maximum_exponent + 1))
    baseline = int(rng.integers(1, 4)) * (1 << baseline_exponent)
    if orientation > 0:
        return np.concatenate([[baseline], weights]).astype(np.int64)
    return np.concatenate([[baseline + int(weights.sum())], -weights]).astype(
        np.int64
    )


def orientation_cycle_extreme_search(
    mask: int,
    n: int,
    seed: int,
    trials: int,
    maximum_exponent: int = 20,
) -> dict[str, object]:
    signs = signs_from_mask(mask, n)
    rng = np.random.default_rng(seed)
    pairs = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    for trial in range(trials):
        orientations = pairs[trial % 4]
        denominators = np.array(
            [
                random_extreme_denominator(
                    n, rng, orientations[0], trial, maximum_exponent
                ),
                random_extreme_denominator(
                    n, rng, orientations[1], trial, maximum_exponent
                ),
            ],
            dtype=np.int64,
        )
        matrix = cleared_two_head_matrix(n, denominators)
        result = exact_integer_separator(signs, matrix)
        if result is None:
            continue
        coefficients, margin = result
        signed_scores = signs.astype(object) * (
            matrix.astype(object) @ coefficients.astype(object)
        )
        return {
            "found": True,
            "method": "orientation-cycle-extreme-simplex-search",
            "trial": trial,
            "orientations": list(orientations),
            "maximum_exponent": maximum_exponent,
            "denominators": denominators.tolist(),
            "cleared_score_coefficients": [int(value) for value in coefficients],
            "minimum_signed_cleared_score": min(map(int, signed_scores)),
            "floating_margin": margin,
        }
    return {
        "found": False,
        "method": "orientation-cycle-extreme-simplex-search",
        "trials": trials,
        "maximum_exponent": maximum_exponent,
    }


def verify_results(payload: dict[str, object]) -> None:
    n = int(payload["n"])
    dictionary = [
        np.array(pair, dtype=np.int64) for pair in payload["dictionary"]
    ]
    affine = affine_matrix(n)
    for pair in dictionary:
        for denominator in pair:
            assert np.all(denominator[1:] > 0) or np.all(denominator[1:] < 0)
            assert np.all(affine @ denominator > 0)
    for record in payload["final_records"]:
        mask = int(record["truth_mask_hex"], 16)
        signs = signs_from_mask(mask, n)
        polynomial = np.array(record["degree_two_coefficients"], dtype=object)
        assert np.all(signs * (monomial_matrix(n, 2).astype(object) @ polynomial) > 0)
        search = record["orientation_cycle_search"]
        if not search["found"]:
            continue
        denominators = np.array(search["denominators"], dtype=object)
        for denominator in denominators:
            assert np.all(denominator[1:] > 0) or np.all(denominator[1:] < 0)
            assert np.all(affine.astype(object) @ denominator > 0)
        coefficients = np.array(search["cleared_score_coefficients"], dtype=object)
        matrix = cleared_two_head_matrix(n, denominators.astype(np.int64)).astype(object)
        signed_scores = signs * (matrix @ coefficients)
        assert np.all(signed_scores > 0)
        assert min(map(int, signed_scores)) == search["minimum_signed_cleared_score"]
    print(
        f"verified {len(payload['final_records'])} adversarial records on n={n}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, choices=(5, 6, 7), default=5)
    parser.add_argument("--dictionary-size", type=int, default=192)
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--beam-size", type=int, default=48)
    parser.add_argument("--gilbert-iterations", type=int, default=160)
    parser.add_argument("--orientation-trials", type=int, default=20000)
    parser.add_argument("--extreme-orientation-trials", type=int, default=0)
    parser.add_argument("--extreme-maximum-exponent", type=int, default=20)
    parser.add_argument("--weight-max", type=int, default=48)
    parser.add_argument("--finalists", type=int, default=24)
    parser.add_argument("--coefficient-samples", type=int, default=0)
    parser.add_argument("--coefficient-retain", type=int, default=2048)
    parser.add_argument("--coefficient-finalists", type=int, default=96)
    parser.add_argument("--coefficient-scoring-pairs", type=int, default=24)
    parser.add_argument("--coordinate-variant-bases", type=int, default=32)
    parser.add_argument("--skip-dictionary-order", action="store_true")
    parser.add_argument("--seed", type=int, default=20260713)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--retry-extreme-failures", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_results(json.loads(arguments.output.read_text()))
        return

    if arguments.retry_extreme_failures:
        payload = json.loads(arguments.output.read_text())
        for index, record in enumerate(payload["final_records"]):
            previous = record["orientation_cycle_search"]
            if previous["found"]:
                continue
            mask = int(record["truth_mask_hex"], 16)
            result = orientation_cycle_extreme_search(
                mask,
                int(payload["n"]),
                arguments.seed + 100003 * index,
                arguments.extreme_orientation_trials,
                arguments.extreme_maximum_exponent,
            )
            record.setdefault("h2_search_history", []).append(previous)
            record["orientation_cycle_search"] = result
            print(
                f"extreme retry {index + 1}: found={result['found']} "
                f"mask={record['truth_mask_hex']}",
                flush=True,
            )
        payload["parameters"]["extreme_orientation_trials"] = (
            arguments.extreme_orientation_trials
        )
        payload["parameters"]["extreme_maximum_exponent"] = (
            arguments.extreme_maximum_exponent
        )
        arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
        verify_results(payload)
        return

    dictionary = build_dictionary(
        arguments.n, arguments.dictionary_size, arguments.seed
    )
    print(f"built dictionary with {len(dictionary)} pairs", flush=True)
    if not arguments.skip_dictionary_order:
        dictionary = order_dictionary_by_pilot(
            arguments.n, dictionary, arguments.seed
        )
    beam, cache, history = hill_climb(
        arguments.n,
        dictionary,
        arguments.rounds,
        arguments.beam_size,
        arguments.gilbert_iterations,
    )

    coefficient_diagnostics = None
    coefficient_histogram = None
    if arguments.coefficient_samples:
        sampled_masks, sampled_certificates, coefficient_diagnostics = (
            sample_small_coefficient_cells(
                arguments.n,
                arguments.coefficient_samples,
                arguments.coefficient_retain,
                arguments.seed + 731,
            )
        )
        cache.update(sampled_certificates)
        variant_masks = set(sampled_masks)
        for mask in sampled_masks[: arguments.coordinate_variant_bases]:
            for flip in range(1 << arguments.n):
                variant = complement_canonical(
                    coordinate_flip(mask, flip, arguments.n), arguments.n
                )
                if degree_two_certificate(variant, arguments.n, cache) is not None:
                    variant_masks.add(variant)
        sampled_masks = sorted(variant_masks)
        print(
            f"coefficient pool after coordinate variants: {len(sampled_masks)}",
            flush=True,
        )
        selected, coefficient_histogram = rank_coefficient_sample(
            sampled_masks,
            arguments.n,
            dictionary,
            arguments.coefficient_scoring_pairs,
            arguments.coefficient_finalists,
        )
        beam = sorted(set(beam) | set(selected))
        print(
            f"full exact finalist pool after merge: {len(beam)}",
            flush=True,
        )

    exact_ranked = []
    for index, mask in enumerate(beam):
        hits = exact_dictionary_hits(mask, arguments.n, dictionary)
        exact_ranked.append((len(hits), mask, hits))
        print(
            f"exact dictionary scan {index + 1}/{len(beam)}: "
            f"hits={len(hits)} mask=0x{mask:0{1 << (arguments.n - 2)}x}",
            flush=True,
        )
    exact_ranked.sort()

    initial_dictionary_size = len(dictionary)
    records = []
    for index, (hit_count, mask, hits) in enumerate(
        exact_ranked[: arguments.finalists]
    ):
        search = None
        if hits:
            search = exact_pair_certificate(
                mask,
                arguments.n,
                dictionary[hits[0]],
                method="fixed-dictionary",
                dictionary_index=hits[0],
            )
            assert search is not None
        else:
            for dictionary_index in range(initial_dictionary_size, len(dictionary)):
                search = exact_pair_certificate(
                    mask,
                    arguments.n,
                    dictionary[dictionary_index],
                    method="active-dictionary-reuse",
                    dictionary_index=dictionary_index,
                )
                if search is not None:
                    break
        if search is None:
            search = orientation_cycle_search(
                mask,
                arguments.n,
                seed=arguments.seed + 100003 * index,
                trials=arguments.orientation_trials,
                weight_max=arguments.weight_max,
            )
        if not search["found"] and arguments.extreme_orientation_trials:
            previous_search = search
            search = orientation_cycle_extreme_search(
                mask,
                arguments.n,
                seed=arguments.seed + 300007 * index,
                trials=arguments.extreme_orientation_trials,
                maximum_exponent=arguments.extreme_maximum_exponent,
            )
            search["previous_uniform_search"] = previous_search
        if search["found"]:
            pair = np.array(search["denominators"], dtype=np.int64)
            key = canonical_denominator_pair(pair)
            if key not in {
                canonical_denominator_pair(existing) for existing in dictionary
            }:
                dictionary.append(np.array(key, dtype=np.int64))
        records.append(
            {
                "truth_mask_hex": f"0x{mask:0{1 << (arguments.n - 2)}x}",
                "degree_two_coefficients": cache[mask],
                "fixed_dictionary_hit_count": hit_count,
                "fixed_dictionary_first_hits": hits[:8],
                "orientation_cycle_search": search,
            }
        )
        print(
            f"finalist {index + 1}: method={search['method']} "
            f"found={search['found']} "
            f"mask=0x{mask:0{1 << (arguments.n - 2)}x}",
            flush=True,
        )

    payload = {
        "status": (
            "Exact degree-two and H2 successes are verified.  An H2 search "
            "failure is not a head-complexity lower bound."
        ),
        "n": arguments.n,
        "seed": arguments.seed,
        "dictionary": [pair.tolist() for pair in dictionary],
        "parameters": {
            "initial_dictionary_size": arguments.dictionary_size,
            "rounds": arguments.rounds,
            "beam_size": arguments.beam_size,
            "gilbert_iterations": arguments.gilbert_iterations,
            "orientation_trials": arguments.orientation_trials,
            "extreme_orientation_trials": arguments.extreme_orientation_trials,
            "extreme_maximum_exponent": arguments.extreme_maximum_exponent,
            "weight_max": arguments.weight_max,
            "coefficient_samples": arguments.coefficient_samples,
            "coefficient_retain": arguments.coefficient_retain,
            "coefficient_finalists": arguments.coefficient_finalists,
        },
        "hill_climb_history": history,
        "coefficient_sampling_diagnostics": coefficient_diagnostics,
        "coefficient_prefix_hit_histogram": coefficient_histogram,
        "final_records": records,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    verify_results(payload)


if __name__ == "__main__":
    main()
