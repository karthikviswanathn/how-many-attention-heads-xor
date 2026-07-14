#!/usr/bin/env python3
"""Build exact finite H4 coverage archives for residual degree-four families.

The fixed-space shattering search leaves a few affine-cocircuit families.
This script covers each finite boundary-extension family with a deterministic
dictionary. Floating point selects candidate witnesses only. Every stored
coefficient vector is checked against the integer cleared matrix before it is
written, and every stored integer must fit in signed 64-bit arithmetic.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

import screen_n5_degree4_cocircuit_families as families
import search_n5_degree4_face_residual as face
import search_n5_degree4_family_shattering as shattering
import search_uncovered_cubic_n6 as nonlinear


N = 5
HEADS = 4
WIDTH = N + 1
VERTICES = 1 << N
COEFFICIENT_COUNT = 1 + HEADS * WIDTH
DEFAULT_ORBITS = (8, 44, 63, 64)
HERE = Path(__file__).resolve().parent
INT64_LIMIT = 1 << 63


def archive_path(orbit: int) -> Path:
    return HERE / f"n5_degree4_orbit_{orbit}_exact_coverage.npz"


def ratio_decomposition(
    denominators: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    affine = nonlinear.core.affine_matrix(N).astype(float)
    values = affine @ denominators.astype(float).T
    raw = np.column_stack(
        [np.ones(VERTICES)]
        + [affine / values[:, head, None] for head in range(HEADS)]
    )
    left, singular, right = np.linalg.svd(raw, full_matrices=False)
    keep = singular > 1e-11 * singular[0]
    basis = left[:, keep]
    row_norms = np.linalg.norm(basis, axis=1)
    normalized_basis = basis / row_norms[:, None]
    coefficient_transform = right[keep].T / singular[keep]
    return raw, normalized_basis, coefficient_transform


def gilbert_candidates(
    signs: np.ndarray,
    denominators: np.ndarray,
    iterations: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return positive heuristic hits and coefficients in the ratio basis."""
    raw, features, transform = ratio_decomposition(denominators)
    labels = signs.astype(float)
    current = (labels @ features) / VERTICES
    active = np.ones(len(labels), dtype=bool)
    found_indices = []
    found_coordinates = []
    for _ in range(iterations):
        indices = np.flatnonzero(active)
        if not len(indices):
            break
        scores = labels[indices] * (current[indices] @ features.T)
        vertices = np.argmin(scores, axis=1)
        minima = scores[np.arange(len(indices)), vertices]
        found = minima > 1e-10
        if np.any(found):
            selected_indices = indices[found]
            found_indices.append(selected_indices)
            found_coordinates.append(current[selected_indices].copy())
            active[selected_indices] = False
        indices = indices[~found]
        vertices = vertices[~found]
        if not len(indices):
            break
        selected = labels[indices, vertices, None] * features[vertices]
        inner = np.sum(current[indices] * selected, axis=1)
        norm = np.sum(current[indices] * current[indices], axis=1)
        denominator = np.sum((current[indices] - selected) ** 2, axis=1)
        step = np.clip(
            (norm - inner) / np.maximum(denominator, 1e-30),
            0.0,
            1.0,
        )
        current[indices] = (
            (1.0 - step[:, None]) * current[indices]
            + step[:, None] * selected
        )
    if not found_indices:
        return (
            np.empty(0, dtype=np.int64),
            np.empty((0, COEFFICIENT_COUNT)),
            raw,
        )
    indices = np.concatenate(found_indices)
    coordinates = np.vstack(found_coordinates)
    coefficients = coordinates @ transform.T
    return indices, coefficients, raw


def exactify_floating_coefficients(
    signs: np.ndarray,
    floating_coefficients: np.ndarray,
    ratio_matrix: np.ndarray,
    cleared_matrix: np.ndarray,
) -> np.ndarray | None:
    coefficients = floating_coefficients.copy()
    maximum = float(np.max(np.abs(coefficients)))
    if not np.isfinite(maximum) or maximum == 0.0:
        return None
    coefficients /= maximum
    ratio_scores = ratio_matrix @ coefficients
    margin = float(np.min(signs * ratio_scores))
    if not np.isfinite(margin) or margin <= 0.0:
        return None
    row_l1 = float(np.max(np.sum(np.abs(ratio_matrix), axis=1)))
    scale = max(1, int(math.ceil(row_l1 / (2.0 * margin))) + 1)
    signs_object = signs.astype(object)
    matrix_object = cleared_matrix.astype(object)
    for _ in range(16):
        integers = [int(round(scale * value)) for value in coefficients]
        maximum_integer = max(abs(value) for value in integers)
        if maximum_integer >= INT64_LIMIT:
            return None
        common = 0
        for value in integers:
            common = math.gcd(common, abs(value))
        if common > 1:
            integers = [value // common for value in integers]
        array = np.array(integers, dtype=object)
        if min(signs_object * (matrix_object @ array)) > 0:
            return np.array(integers, dtype=np.int64)
        scale *= 2
    return None


def exactify_nonlinear_certificate(
    signs: np.ndarray,
    denominators: np.ndarray,
) -> np.ndarray | None:
    certificate = nonlinear.exact_head_certificate(signs, denominators)
    if certificate is None:
        return None
    integers = [int(value) for value in certificate["score_coefficients"]]
    common = 0
    for value in integers:
        common = math.gcd(common, abs(value))
    if common > 1:
        integers = [value // common for value in integers]
    if max(abs(value) for value in integers) >= INT64_LIMIT:
        return None
    matrix = shattering.cleared_matrix(denominators)
    signed = signs.astype(object) * (
        matrix @ np.array(integers, dtype=object)
    )
    if min(signed) <= 0:
        return None
    return np.array(integers, dtype=np.int64)


def scan_denominator(
    signs: np.ndarray,
    target_indices: np.ndarray,
    denominators: np.ndarray,
    iterations: int,
    chunk_size: int,
) -> list[tuple[int, np.ndarray]]:
    if not len(target_indices):
        return []
    matrix = shattering.cleared_matrix(denominators)
    exact_hits = []
    for start in range(0, len(target_indices), chunk_size):
        chunk = target_indices[start : start + chunk_size]
        local_hits, floating, ratio_matrix = gilbert_candidates(
            signs[chunk], denominators, iterations
        )
        for local_index, current in zip(local_hits, floating):
            target_index = int(chunk[int(local_index)])
            exact = exactify_floating_coefficients(
                signs[target_index], current, ratio_matrix, matrix
            )
            if exact is None:
                exact = exactify_nonlinear_certificate(
                    signs[target_index], denominators
                )
            if exact is not None:
                exact_hits.append((target_index, exact))
    return exact_hits


def masks_from_signs(signs: np.ndarray) -> np.ndarray:
    powers = np.array([1 << vertex for vertex in range(VERTICES)], dtype=np.uint64)
    return ((signs > 0).astype(np.uint64) @ powers).astype(np.uint32)


def build_archive(
    orbit: int,
    dictionary_size: int,
    expanded_dictionary_size: int,
    iterations: int,
    refinement_iterations: int,
    chunk_size: int,
    seed: int,
    restarts: int,
    max_iterations: int,
    output: Path,
) -> None:
    face.configure_nonlinear_search()
    normals = families.orbit_normals()
    normal = normals[orbit]
    signs = families.extension_signs(normal)
    full_dictionary = families.denominator_dictionary(
        expanded_dictionary_size, seed
    )
    dictionary = list(full_dictionary[:dictionary_size])
    witnesses = -np.ones(len(signs), dtype=np.int16)
    coefficients = np.zeros(
        (len(signs), COEFFICIENT_COUNT), dtype=np.int64
    )

    def store(hits: list[tuple[int, np.ndarray]], index: int) -> None:
        for target_index, exact in hits:
            if witnesses[target_index] >= 0:
                continue
            witnesses[target_index] = index
            coefficients[target_index] = exact

    for dictionary_index, denominators in enumerate(dictionary):
        active = np.flatnonzero(witnesses < 0)
        store(
            scan_denominator(
                signs, active, denominators, iterations, chunk_size
            ),
            dictionary_index,
        )
        if (dictionary_index + 1) % 32 == 0 or not np.any(witnesses < 0):
            print(
                f"orbit={orbit} dictionary={dictionary_index + 1} "
                f"exact_misses={int(np.sum(witnesses < 0))}",
                flush=True,
            )
        if not np.any(witnesses < 0):
            break

    for denominators in full_dictionary[dictionary_size:]:
        active = np.flatnonzero(witnesses < 0)
        if not len(active):
            break
        dictionary_index = len(dictionary)
        dictionary.append(denominators)
        store(
            scan_denominator(
                signs, active, denominators, iterations, chunk_size
            ),
            dictionary_index,
        )
        if (dictionary_index + 1) % 256 == 0:
            print(
                f"orbit={orbit} expanded={dictionary_index + 1} "
                f"exact_misses={int(np.sum(witnesses < 0))}",
                flush=True,
            )

    if refinement_iterations > iterations and np.any(witnesses < 0):
        for dictionary_index, denominators in enumerate(dictionary):
            active = np.flatnonzero(witnesses < 0)
            if not len(active):
                break
            store(
                scan_denominator(
                    signs,
                    active,
                    denominators,
                    refinement_iterations,
                    chunk_size,
                ),
                dictionary_index,
            )
            if (dictionary_index + 1) % 32 == 0 or not np.any(
                witnesses < 0
            ):
                print(
                    f"orbit={orbit} refinement={dictionary_index + 1} "
                    f"exact_misses={int(np.sum(witnesses < 0))}",
                    flush=True,
                )

    round_index = 0
    while np.any(witnesses < 0):
        target_index = int(np.flatnonzero(witnesses < 0)[0])
        exact = None
        dictionary_index = -1
        for index, denominators in enumerate(dictionary):
            exact = exactify_nonlinear_certificate(
                signs[target_index], denominators
            )
            if exact is not None:
                dictionary_index = index
                break
        if exact is None:
            certificate = face.nonlinear_denominator_search(
                signs[target_index],
                seed + 100_003 * orbit + 10_007 * round_index,
                restarts,
                max_iterations,
            )
            if certificate is None:
                raise RuntimeError(
                    f"nonlinear search failed for orbit {orbit}, "
                    f"target {target_index}"
                )
            denominators = np.array(
                certificate["denominators"], dtype=np.int64
            )
            exact = exactify_nonlinear_certificate(
                signs[target_index], denominators
            )
            if exact is None:
                raise RuntimeError("new nonlinear certificate did not exactify")
            dictionary_index = len(dictionary)
            dictionary.append(denominators)
        witnesses[target_index] = dictionary_index
        coefficients[target_index] = exact
        active = np.flatnonzero(witnesses < 0)
        if len(active):
            store(
                scan_denominator(
                    signs,
                    active,
                    dictionary[dictionary_index],
                    iterations,
                    chunk_size,
                ),
                dictionary_index,
            )
        round_index += 1
        print(
            f"orbit={orbit} active_round={round_index} "
            f"dictionary={len(dictionary)} "
            f"exact_misses={int(np.sum(witnesses < 0))}",
            flush=True,
        )

    used = np.unique(witnesses)
    remap = -np.ones(len(dictionary), dtype=np.int64)
    remap[used] = np.arange(len(used))
    compact_dictionary = np.array(
        [dictionary[int(index)] for index in used], dtype=np.int64
    )
    witnesses = remap[witnesses].astype(np.int16)
    np.savez_compressed(
        output,
        orbit=np.array(orbit, dtype=np.int16),
        normal=np.array(normal, dtype=np.int64),
        masks=masks_from_signs(signs),
        denominators=compact_dictionary,
        witness_indices=witnesses,
        score_coefficients=coefficients,
    )
    print(
        f"wrote {output}: targets={len(signs)} "
        f"dictionary={len(compact_dictionary)}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, choices=DEFAULT_ORBITS, required=True)
    parser.add_argument("--dictionary-size", type=int, default=256)
    parser.add_argument("--expanded-dictionary-size", type=int, default=4096)
    parser.add_argument("--gilbert-iterations", type=int, default=160)
    parser.add_argument("--refinement-iterations", type=int, default=160)
    parser.add_argument("--chunk-size", type=int, default=4096)
    parser.add_argument("--restarts", type=int, default=24)
    parser.add_argument("--max-iterations", type=int, default=2200)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    build_archive(
        arguments.orbit,
        arguments.dictionary_size,
        arguments.expanded_dictionary_size,
        arguments.gilbert_iterations,
        arguments.refinement_iterations,
        arguments.chunk_size,
        arguments.seed,
        arguments.restarts,
        arguments.max_iterations,
        arguments.output or archive_path(arguments.orbit),
    )


if __name__ == "__main__":
    main()
