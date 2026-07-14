#!/usr/bin/env python3
"""Active exact-clause search for a universal five-bit H3 dictionary.

The six-bit uncovered-cell MILP bounds the coefficients of a cubic separator.
That bound is unsuitable for a universal statement because normalized cubic
cells can approach the boundary with arbitrarily large coefficient ratios.
On five bits the parity-twist alternative removes the issue completely:
degree at most three is equivalent to disagreement with both orientations of
each of the 3,254 primitive affine covectors.  This script encodes those 6,508
conditions as exact Boolean clauses and never introduces cubic coefficients.

For a fixed denominator triple, a three-head hit is verified over the integers.
It is then strengthened, when possible, to a simple family certificate.  If
the score space has rank r, the certificate consists of an extreme ray with
exactly r - 1 zero rows and a rank-(r - 1) restriction to those rows.
Surjectivity on the zero set shows that all 2^(r - 1) tangent assignments are
covered.  Coordinate permutations,
global input complement, and output complement expand each stored family.

The exact DPLL layer searches for a degree-at-most-three truth table outside
all certified families.  A fixed-dictionary hit or a newly learned exact H3
certificate adds another family and checkpoints the result.  A nonlinear
failure is only survivor evidence.  DPLL unsatisfiability, in contrast, is an
exact finite universal cover once independently reverified.
"""

from __future__ import annotations

import argparse
import functools
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import pycosat
from scipy.optimize import linprog, minimize
from scipy.special import expit

import search_adversarial_low_dimension as core
import search_n6_h4_inner_lp as inner_lp_core
import verify_n5_degree4_reduction as degree_four


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n5_cubic_dictionary_active_checkpoint.json"
DEFAULT_FINAL_OUTPUT = HERE / "n5_cubic_dictionary_cover.json"
CPP_DPLL_SOURCE = HERE / "solve_n5_clause_cnf.cpp"
CPP_DPLL_BINARY = Path("/tmp/how_many_attention_heads_n5_clause_dpll")
N = 5
HEADS = 3
WIDTH = N + 1
VERTICES = 1 << N
FULL_MASK = (1 << VERTICES) - 1
PARITY = np.array(
    [1 if bin(vertex).count("1") % 2 == 0 else -1 for vertex in range(VERTICES)],
    dtype=np.int64,
)


LEARNED_SEEDS: tuple[dict[str, object], ...] = (
    {
        "mask": 0xA995E996,
        "denominators": (
            (105, -1, -1, -1, -1, -1),
            (103, -1, -29, -1, -29, -14),
            (102, -28, -26, -20, -26, -1),
        ),
    },
    {
        "mask": 0x6343941C,
        "denominators": (
            (104, -95, -1, -1, -5, -1),
            (104, -1, -77, -1, -1, -23),
            (105, -1, -1, -100, -1, -1),
        ),
    },
    {
        "mask": 0x04639041,
        "denominators": (
            (1003, -2, -290, -1, -1, -708),
            (1003, -1, -1, -1, -2, -997),
            (1004, -1, -1, -1, -1, -1),
        ),
    },
    {
        "mask": 0x177E7EE9,
        "denominators": (
            (101, -20, -1, -1, -16, -15),
            (103, -36, -1, -1, -32, -32),
            (105, -1, -1, -1, -1, -1),
        ),
    },
    {
        "mask": 0x0761300F,
        "denominators": (
            (1000001, -284, -220, -5, -1, -999490),
            (1000003, -1, -4, -1, -999995, -1),
            (1000003, -1, -1, -7, -999992, -1),
        ),
    },
    {
        "mask": 0x2D8B4E14,
        "denominators": (
            (1000003, -6, -1, -641731, -1, -358263),
            (1000004, -999998, -1, -1, -1, -2),
            (1000004, -1, -1, -1, -999998, -1),
        ),
    },
    {
        "mask": 0x6A83833C,
        "denominators": (
            (23, 9168, 316, 379, 26, 88),
            (97, 91, 4504, 4989, 79, 241),
            (135, 6344, 81, 139, 229, 3071),
        ),
    },
)


def signs_from_mask(mask: int) -> np.ndarray:
    return core.signs_from_mask(mask, N)


def mask_from_signs(signs: np.ndarray) -> int:
    return core.mask_from_signs(signs)


def complement_canonical(mask: int) -> int:
    return min(mask, FULL_MASK ^ mask)


def canonical_triple(denominators: object) -> tuple[tuple[int, ...], ...]:
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


def valid_denominators(denominators: object) -> bool:
    exact = np.array(denominators, dtype=object)
    if exact.shape != (HEADS, WIDTH):
        return False
    affine = core.affine_matrix(N).astype(object)
    if not np.all(affine @ exact.T > 0):
        return False
    return all(
        all(int(value) > 0 for value in row[1:])
        or all(int(value) < 0 for value in row[1:])
        for row in exact
    )


def oriented_denominator(weights: list[int], orientation: int) -> tuple[int, ...]:
    assert len(weights) == N
    if orientation > 0:
        return (1, *weights)
    return (sum(weights) + 1, *(-value for value in weights))


def near_literal_dictionary(scale: int = 10) -> list[np.ndarray]:
    answer = []
    seen = set()
    for coordinates in itertools.combinations(range(N), HEADS):
        for orientations in itertools.product((-1, 1), repeat=HEADS):
            rows = []
            for coordinate, orientation in zip(coordinates, orientations):
                weights = [1] * N
                weights[coordinate] = scale
                rows.append(oriented_denominator(weights, orientation))
            key = canonical_triple(rows)
            if key not in seen:
                seen.add(key)
                answer.append(np.array(key, dtype=np.int64))
    assert len(answer) == 80
    assert all(valid_denominators(item) for item in answer)
    return answer


def asymmetric_near_literal_representatives(scale: int = 10) -> list[np.ndarray]:
    """Two generic perturbations whose symmetry orbits cover both orientation types."""
    if scale < 2:
        raise ValueError("the asymmetric near-literal scale must be at least two")
    dominant = 100 * scale
    weights = (
        (dominant + 3, 97, 101, 105, 94),
        (96, dominant - 5, 104, 99, 107),
        (102, 95, dominant + 7, 106, 98),
    )
    margins = (103, 97, 101)
    answer = []
    for orientations in ((-1, -1, -1), (-1, -1, 1)):
        rows = []
        for row_weights, margin, orientation in zip(
            weights, margins, orientations
        ):
            if orientation > 0:
                rows.append((margin, *row_weights))
            else:
                rows.append(
                    (
                        sum(row_weights) + margin,
                        *(-value for value in row_weights),
                    )
                )
        denominators = np.array(canonical_triple(rows), dtype=np.int64)
        assert valid_denominators(denominators)
        assert modular_rank(cleared_matrix(denominators)) == 16
        answer.append(denominators)
    assert len({canonical_triple(item) for item in answer}) == 2
    assert sum(len(denominator_orbit(item)) for item in answer) == 480
    return answer


def transform_denominators(
    denominators: object,
    permutation: tuple[int, ...],
    global_complement: bool,
) -> tuple[tuple[int, ...], ...]:
    answer = []
    for row_object in denominators:
        row = [int(value) for value in row_object]
        slopes = [0] * N
        for source in range(N):
            slopes[permutation[source]] = row[1 + source]
        constant = row[0]
        if global_complement:
            constant += sum(slopes)
            slopes = [-value for value in slopes]
        answer.append((constant, *slopes))
    result = canonical_triple(answer)
    assert valid_denominators(result)
    return result


def transform_affine_row(
    row_object: object,
    permutation: tuple[int, ...],
    global_complement: bool,
) -> tuple[int, ...]:
    """Pull an affine form through the selected cube automorphism."""
    row = [int(value) for value in row_object]
    slopes = [0] * N
    for source in range(N):
        slopes[permutation[source]] = row[1 + source]
    constant = row[0]
    if global_complement:
        constant += sum(slopes)
        slopes = [-value for value in slopes]
    return (constant, *slopes)


def denominator_orbit(denominators: object) -> list[np.ndarray]:
    images = {
        transform_denominators(denominators, permutation, global_complement)
        for permutation in itertools.permutations(range(N))
        for global_complement in (False, True)
    }
    return [np.array(key, dtype=np.int64) for key in sorted(images)]


def ratio_features(denominators: object) -> np.ndarray:
    affine = core.affine_matrix(N).astype(float)
    exact = np.array(denominators, dtype=float)
    values = affine @ exact.T
    assert np.all(values > 0)
    return np.column_stack(
        [np.ones(VERTICES)]
        + [affine / values[:, head, None] for head in range(HEADS)]
    )


def cleared_matrix(denominators: object) -> np.ndarray:
    affine = core.affine_matrix(N).astype(object)
    exact = np.array(denominators, dtype=object)
    values = affine @ exact.T
    assert np.all(values > 0)
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(HEADS):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product for coordinate in range(WIDTH)
        )
    return np.column_stack(columns).astype(object)


def exact_head_certificate(
    signs: np.ndarray, denominators: object
) -> dict[str, object] | None:
    denominators = np.array(canonical_triple(denominators), dtype=np.int64)
    features = ratio_features(denominators)
    norms = np.linalg.norm(features, axis=0)
    keep = norms > 1e-13 * max(1.0, float(np.max(norms)))
    normalized = features[:, keep] / norms[keep]
    variable_count = normalized.shape[1]
    constraints = np.zeros((VERTICES, variable_count + 1))
    constraints[:, :variable_count] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variable_count + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(VERTICES),
        bounds=[(-1.0, 1.0)] * variable_count + [(None, None)],
        method="highs",
    )
    if not result.success or -float(result.fun) <= 1e-11:
        return None

    floating = np.zeros(features.shape[1])
    floating[keep] = result.x[:variable_count] / norms[keep]
    margin = float(np.min(signs * (features @ floating)))
    if margin <= 1e-12:
        return None
    matrix = cleared_matrix(denominators)
    row_norm = max(
        sum(abs(int(value)) for value in row) for row in matrix.tolist()
    )
    scale = max(1, int(math.ceil((row_norm + 1) / (2 * margin))))
    for _ in range(200):
        coefficients = np.array(
            [int(round(scale * value)) for value in floating], dtype=object
        )
        signed = signs.astype(object) * (matrix @ coefficients)
        if min(signed) > 0:
            return {
                "denominators": denominators.tolist(),
                "score_coefficients": [int(value) for value in coefficients],
                "minimum_signed_cleared_score": int(min(signed)),
                "floating_ratio_margin": margin,
            }
        scale *= 2
    return None


def rational_pivot_columns(matrix: np.ndarray) -> list[int]:
    work = [[Fraction(int(value)) for value in row] for row in matrix.tolist()]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    pivots = []
    for column in range(columns):
        selected = next(
            (row for row in range(pivot_row, rows) if work[row][column]), None
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot
                for value, pivot in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivots


def modular_rank(matrix: np.ndarray, prime: int = 1_000_003) -> int:
    work = np.array(matrix, dtype=object)
    reduced = np.vectorize(lambda value: int(value) % prime)(work).astype(np.int64)
    rows, columns = reduced.shape
    rank = 0
    for column in range(columns):
        selected = next(
            (row for row in range(rank, rows) if reduced[row, column]), None
        )
        if selected is None:
            continue
        reduced[[rank, selected]] = reduced[[selected, rank]]
        inverse = pow(int(reduced[rank, column]), -1, prime)
        reduced[rank] = reduced[rank] * inverse % prime
        for row in range(rows):
            if row == rank or not reduced[row, column]:
                continue
            reduced[row] = (
                reduced[row] - reduced[row, column] * reduced[rank]
            ) % prime
        rank += 1
        if rank == rows:
            break
    return rank


def one_dimensional_null_vector(matrix: np.ndarray) -> tuple[int, ...]:
    rows = [[Fraction(int(value)) for value in row] for row in matrix.tolist()]
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
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                value - scale * pivot
                for value, pivot in zip(rows[row], rows[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
    free = [column for column in range(column_count) if column not in pivots]
    if len(free) != 1:
        raise ValueError(f"expected nullity one, got {len(free)}")
    vector = [Fraction(0) for _ in range(column_count)]
    vector[free[0]] = Fraction(1)
    for row, pivot in reversed(list(enumerate(pivots))):
        vector[pivot] = -sum(
            rows[row][column] * vector[column]
            for column in range(pivot + 1, column_count)
        )
    denominator = 1
    for value in vector:
        denominator = math.lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in vector]
    common = 0
    for value in integers:
        common = math.gcd(common, abs(value))
    integers = [value // common for value in integers]
    first = next(value for value in integers if value)
    if first < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def independent_score_basis(
    denominators: object,
) -> tuple[np.ndarray, tuple[int, ...]]:
    matrix = cleared_matrix(denominators)
    pivots = tuple(rational_pivot_columns(matrix))
    basis = matrix[:, pivots]
    assert len(pivots) == modular_rank(basis)
    return basis, pivots


def extreme_family_certificates(
    mask: int,
    denominators: object,
    seed: int,
    attempts: int = 96,
    max_families: int = 8,
) -> list[dict[str, object]]:
    signs = signs_from_mask(mask).astype(np.int64)
    basis, basis_columns = independent_score_basis(denominators)
    rank = basis.shape[1]
    if rank < 2:
        return []
    floating = np.array(basis, dtype=float)
    scales = np.linalg.norm(floating, axis=0)
    scaled = floating / scales
    signed = signs[:, None] * scaled
    normalizer = np.sum(signed, axis=0)
    rng = np.random.default_rng(seed)
    objectives = [rng.standard_normal(rank) for _ in range(attempts)]
    families: list[dict[str, object]] = []
    seen_orbits: set[tuple[Clause, ...]] = set()
    for objective in objectives:
        result = linprog(
            objective,
            A_ub=-signed,
            b_ub=np.zeros(VERTICES),
            A_eq=normalizer[None, :],
            b_eq=np.ones(1),
            bounds=[(None, None)] * rank,
            method="highs",
        )
        if not result.success:
            continue
        approximate_values = scaled @ result.x
        order = np.argsort(np.abs(approximate_values))
        selected: list[int] = []
        current_rank = 0
        for vertex_value in order[: min(VERTICES, rank + 7)]:
            vertex = int(vertex_value)
            candidate = basis[selected + [vertex]]
            candidate_rank = modular_rank(candidate)
            if candidate_rank > current_rank:
                selected.append(vertex)
                current_rank = candidate_rank
            if current_rank == rank - 1:
                break
        if current_rank != rank - 1:
            continue
        coefficients = one_dimensional_null_vector(basis[selected])
        values = basis @ np.array(coefficients, dtype=object)
        signed_values = signs.astype(object) * values
        if all(value <= 0 for value in signed_values):
            coefficients = tuple(-value for value in coefficients)
            values = -values
            signed_values = -signed_values
        if not all(value >= 0 for value in signed_values) or not any(signed_values):
            continue
        zero_vertices = tuple(
            int(vertex) for vertex in np.flatnonzero(np.array(values == 0, dtype=bool))
        )
        if len(zero_vertices) != rank - 1:
            continue
        if modular_rank(basis[list(zero_vertices)]) != rank - 1:
            continue
        positive_mask = sum(
            (int(value) > 0) << vertex for vertex, value in enumerate(values)
        )
        negative_mask = sum(
            (int(value) < 0) << vertex for vertex, value in enumerate(values)
        )
        assert positive_mask | negative_mask | sum(
            1 << vertex for vertex in zero_vertices
        ) == FULL_MASK
        family: dict[str, object] = {
            "source_mask_hex": f"0x{mask:08x}",
            "denominators": [list(row) for row in canonical_triple(denominators)],
            "score_basis_columns": list(basis_columns),
            "ray_coefficients": list(coefficients),
            "zero_vertices": list(zero_vertices),
            "fixed_positive_mask_hex": f"0x{positive_mask:08x}",
            "fixed_negative_mask_hex": f"0x{negative_mask:08x}",
            "score_space_rank": rank,
            "zero_restriction_rank": rank - 1,
            "symmetry_orbit": "S5 x global input complement x output complement",
        }
        orbit = tuple(family_clauses(family))
        if orbit in seen_orbits:
            continue
        seen_orbits.add(orbit)
        families.append(family)
        if len(families) >= max_families:
            break
    return families


def extreme_family_certificate(
    mask: int,
    denominators: object,
    seed: int,
    attempts: int = 96,
) -> dict[str, object] | None:
    families = extreme_family_certificates(
        mask, denominators, seed, attempts, max_families=1
    )
    return families[0] if families else None


def targeted_face_family_certificates(
    masks: list[int],
    denominators: object,
    seed: int,
    attempts: int = 96,
    max_families: int = 4,
) -> list[dict[str, object]]:
    """Find simple rays vanishing on every coordinate varying in a mask pocket."""
    assert masks
    shared_positive = FULL_MASK
    shared_negative = FULL_MASK
    for mask in masks:
        shared_positive &= mask
        shared_negative &= FULL_MASK ^ mask
    varying_mask = FULL_MASK ^ (shared_positive | shared_negative)
    forced_zeros = [
        vertex for vertex in range(VERTICES) if (varying_mask >> vertex) & 1
    ]
    source_mask = masks[-1]
    signs = signs_from_mask(source_mask).astype(np.int64)
    basis, basis_columns = independent_score_basis(denominators)
    rank = basis.shape[1]
    forced_rank = modular_rank(basis[forced_zeros]) if forced_zeros else 0
    if forced_rank != len(forced_zeros) or forced_rank >= rank:
        return []

    floating = np.array(basis, dtype=float)
    scales = np.linalg.norm(floating, axis=0)
    scaled = floating / scales
    signed = signs[:, None] * scaled
    fixed_vertices = [
        vertex for vertex in range(VERTICES) if not (varying_mask >> vertex) & 1
    ]
    normalizer = np.sum(signed[fixed_vertices], axis=0)
    equality_rows = [scaled[vertex] for vertex in forced_zeros]
    equality_rows.append(normalizer)
    equality_rhs = np.zeros(len(equality_rows))
    equality_rhs[-1] = 1.0
    rng = np.random.default_rng(seed)
    families: list[dict[str, object]] = []
    seen_orbits: set[tuple[Clause, ...]] = set()
    for _ in range(attempts):
        result = linprog(
            rng.standard_normal(rank),
            A_ub=-signed[fixed_vertices],
            b_ub=np.zeros(len(fixed_vertices)),
            A_eq=np.vstack(equality_rows),
            b_eq=equality_rhs,
            bounds=[(None, None)] * rank,
            method="highs",
        )
        if not result.success:
            continue
        approximate_values = scaled @ result.x
        selected = list(forced_zeros)
        current_rank = forced_rank
        for vertex_value in sorted(
            fixed_vertices, key=lambda vertex: abs(approximate_values[vertex])
        ):
            vertex = int(vertex_value)
            candidate_rank = modular_rank(basis[selected + [vertex]])
            if candidate_rank > current_rank:
                selected.append(vertex)
                current_rank = candidate_rank
            if current_rank == rank - 1:
                break
        if current_rank != rank - 1:
            continue
        coefficients = one_dimensional_null_vector(basis[selected])
        values = basis @ np.array(coefficients, dtype=object)
        signed_values = signs.astype(object) * values
        if all(value <= 0 for value in signed_values):
            coefficients = tuple(-value for value in coefficients)
            values = -values
            signed_values = -signed_values
        if not all(value >= 0 for value in signed_values) or not any(signed_values):
            continue
        zero_vertices = tuple(
            int(vertex) for vertex in np.flatnonzero(np.array(values == 0, dtype=bool))
        )
        if len(zero_vertices) != rank - 1:
            continue
        if not set(forced_zeros).issubset(zero_vertices):
            continue
        if modular_rank(basis[list(zero_vertices)]) != rank - 1:
            continue
        positive_mask = sum(
            (int(value) > 0) << vertex for vertex, value in enumerate(values)
        )
        negative_mask = sum(
            (int(value) < 0) << vertex for vertex, value in enumerate(values)
        )
        family: dict[str, object] = {
            "source_mask_hex": f"0x{source_mask:08x}",
            "denominators": [list(row) for row in canonical_triple(denominators)],
            "score_basis_columns": list(basis_columns),
            "ray_coefficients": list(coefficients),
            "zero_vertices": list(zero_vertices),
            "fixed_positive_mask_hex": f"0x{positive_mask:08x}",
            "fixed_negative_mask_hex": f"0x{negative_mask:08x}",
            "score_space_rank": rank,
            "zero_restriction_rank": rank - 1,
            "symmetry_orbit": "S5 x global input complement x output complement",
            "targeted_face": {
                "pocket_size": len(masks),
                "forced_zero_vertices": forced_zeros,
            },
        }
        orbit = tuple(family_clauses(family))
        if orbit in seen_orbits:
            continue
        seen_orbits.add(orbit)
        families.append(family)
        if len(families) >= max_families:
            break
    return families


def transform_vertex(
    vertex: int, permutation: tuple[int, ...], global_complement: bool
) -> int:
    image = 0
    for source in range(N):
        image |= ((vertex >> source) & 1) << permutation[source]
    if global_complement:
        image ^= (1 << N) - 1
    return image


def transform_mask(
    mask: int, permutation: tuple[int, ...], global_complement: bool
) -> int:
    answer = 0
    for vertex in range(VERTICES):
        if (mask >> vertex) & 1:
            answer |= 1 << transform_vertex(vertex, permutation, global_complement)
    return answer


Clause = tuple[int, int]


@functools.lru_cache(maxsize=1)
def degree_clauses() -> list[Clause]:
    features = degree_four.affine_features().astype(np.int64)
    normals = degree_four.enumerate_rank_five_normals(features)
    assert len(normals) == 3_254
    clauses: set[Clause] = set()
    for normal in normals:
        values = features @ np.array(normal, dtype=np.int64)
        for orientation in (-1, 1):
            desired = orientation * np.sign(values).astype(np.int64) * PARITY
            positive = sum(
                (int(value) < 0) << vertex
                for vertex, value in enumerate(desired)
                if value
            )
            negative = sum(
                (int(value) > 0) << vertex
                for vertex, value in enumerate(desired)
                if value
            )
            assert positive & negative == 0
            clauses.add((positive, negative))
    assert len(clauses) == 6_508
    answer = sorted(clauses)
    assert not satisfies_clauses(0x966B6996, answer)
    assert satisfies_clauses(0x149AC934, answer)
    assert satisfies_clauses(0x96E86B96, answer)
    return answer


def family_clauses(family: dict[str, object]) -> list[Clause]:
    positive = int(family["fixed_positive_mask_hex"], 16)
    negative = int(family["fixed_negative_mask_hex"], 16)
    return orbit_disagreement_clauses(positive, negative)


def orbit_disagreement_clauses(positive: int, negative: int) -> list[Clause]:
    clauses: set[Clause] = set()
    for permutation in itertools.permutations(range(N)):
        for global_complement in (False, True):
            transformed_positive = transform_mask(
                positive, permutation, global_complement
            )
            transformed_negative = transform_mask(
                negative, permutation, global_complement
            )
            for output_complement in (False, True):
                if output_complement:
                    current_positive = transformed_negative
                    current_negative = transformed_positive
                else:
                    current_positive = transformed_positive
                    current_negative = transformed_negative
                # To remain outside this covered family, the truth table must
                # disagree at one fixed-support vertex.
                clauses.add((current_negative, current_positive))
    return sorted(clauses)


def singleton_clauses(singleton: dict[str, object]) -> list[Clause]:
    mask = int(singleton["source_mask_hex"], 16)
    return orbit_disagreement_clauses(mask, FULL_MASK ^ mask)


def satisfies_clause(mask: int, clause: Clause) -> bool:
    positive, negative = clause
    return bool(mask & positive) or bool((FULL_MASK ^ mask) & negative)


def satisfies_clauses(mask: int, clauses: list[Clause]) -> bool:
    return all(satisfies_clause(mask, clause) for clause in clauses)


def dpll_candidate_naive(
    clauses: list[Clause], node_limit: int
) -> tuple[int | None, dict[str, int | str]]:
    occurrences = [0] * VERTICES
    for positive, negative in clauses:
        support = positive | negative
        for vertex in range(VERTICES):
            occurrences[vertex] += (support >> vertex) & 1
    nodes = 0
    max_depth = 0

    def search(assigned: int, values: int, depth: int) -> int | None:
        nonlocal nodes, max_depth
        nodes += 1
        max_depth = max(max_depth, depth)
        if nodes > node_limit:
            raise RuntimeError("DPLL node limit exceeded")

        while True:
            forced_vertex = None
            forced_value = None
            unresolved_support = 0
            for positive, negative in clauses:
                if (assigned & values & positive) or (
                    assigned & (FULL_MASK ^ values) & negative
                ):
                    continue
                unassigned = (positive | negative) & (FULL_MASK ^ assigned)
                if not unassigned:
                    return None
                unresolved_support |= unassigned
                if unassigned & (unassigned - 1) == 0:
                    vertex = unassigned.bit_length() - 1
                    value = 1 if positive & unassigned else 0
                    if forced_vertex is not None and forced_vertex == vertex:
                        if forced_value != value:
                            return None
                    forced_vertex, forced_value = vertex, value
                    break
            if forced_vertex is None:
                break
            bit = 1 << forced_vertex
            assigned |= bit
            if forced_value:
                values |= bit
            else:
                values &= FULL_MASK ^ bit

        if assigned == FULL_MASK:
            return values
        candidates = [
            vertex
            for vertex in range(VERTICES)
            if not (assigned >> vertex) & 1
            and (unresolved_support >> vertex) & 1
        ]
        if not candidates:
            return values
        vertex = max(candidates, key=lambda item: occurrences[item])
        bit = 1 << vertex
        preferred = 0 if vertex == 0 else 1
        for value in (preferred, 1 - preferred):
            result = search(
                assigned | bit,
                (values | bit) if value else (values & (FULL_MASK ^ bit)),
                depth + 1,
            )
            if result is not None:
                return result
        return None

    # Output complement preserves both degree and H3, so fix s(0)=-1.
    result = search(1, 0, 0)
    return result, {
        "status": "UNSAT" if result is None else "candidate",
        "nodes": nodes,
        "max_depth": max_depth,
        "clause_count": len(clauses),
    }


def dpll_candidate(
    clauses: list[Clause], node_limit: int
) -> tuple[int | None, dict[str, int | str]]:
    """Deterministic exact DPLL with two watched literals per clause."""
    literal_clauses: list[tuple[int, ...]] = []
    occurrences = [0] * VERTICES
    for positive, negative in clauses:
        assert positive & negative == 0
        literals = []
        for vertex in range(VERTICES):
            bit = 1 << vertex
            if positive & bit:
                literals.append(2 * vertex + 1)
                occurrences[vertex] += 1
            elif negative & bit:
                literals.append(2 * vertex)
                occurrences[vertex] += 1
        if not literals:
            return None, {
                "status": "UNSAT",
                "nodes": 1,
                "max_depth": 0,
                "clause_count": len(clauses),
                "solver": "watched-literal exact DPLL",
            }
        literal_clauses.append(tuple(literals))

    watched_positions: list[list[int]] = []
    watchers: list[list[int]] = [[] for _ in range(2 * VERTICES)]
    for clause_index, literals in enumerate(literal_clauses):
        second = 0 if len(literals) == 1 else 1
        watched_positions.append([0, second])
        watchers[literals[0]].append(clause_index)
        if second != 0:
            watchers[literals[second]].append(clause_index)

    assignments = [-1] * VERTICES
    trail: list[int] = []
    propagation_index = 0
    nodes = 0
    max_depth = 0

    def enqueue(vertex: int, value: int) -> bool:
        current = assignments[vertex]
        if current >= 0:
            return current == value
        assignments[vertex] = value
        trail.append(vertex)
        return True

    def literal_state(literal: int) -> int:
        value = assignments[literal // 2]
        if value < 0:
            return -1
        return 1 if value == literal % 2 else 0

    def propagate() -> bool:
        nonlocal propagation_index
        while propagation_index < len(trail):
            vertex = trail[propagation_index]
            propagation_index += 1
            false_literal = 2 * vertex + (1 - assignments[vertex])
            watch_list = watchers[false_literal]
            position = 0
            while position < len(watch_list):
                clause_index = watch_list[position]
                literals = literal_clauses[clause_index]
                first, second = watched_positions[clause_index]
                if literals[first] == false_literal:
                    slot = 0
                    current_position = first
                    other_position = second
                elif literals[second] == false_literal:
                    slot = 1
                    current_position = second
                    other_position = first
                else:
                    raise AssertionError("stale watched-literal entry")

                replacement = None
                for candidate_position, candidate_literal in enumerate(literals):
                    if candidate_position in (current_position, other_position):
                        continue
                    if literal_state(candidate_literal) != 0:
                        replacement = candidate_position
                        break
                if replacement is not None:
                    watched_positions[clause_index][slot] = replacement
                    watch_list[position] = watch_list[-1]
                    watch_list.pop()
                    watchers[literals[replacement]].append(clause_index)
                    continue

                other_literal = literals[other_position]
                other_state = literal_state(other_literal)
                if other_state == 0:
                    return False
                if other_state < 0 and not enqueue(
                    other_literal // 2, other_literal % 2
                ):
                    return False
                position += 1
        return True

    def backtrack(size: int) -> None:
        nonlocal propagation_index
        for vertex in trail[size:]:
            assignments[vertex] = -1
        del trail[size:]
        propagation_index = min(propagation_index, size)

    def search(depth: int) -> int | None:
        nonlocal nodes, max_depth
        nodes += 1
        max_depth = max(max_depth, depth)
        if nodes > node_limit:
            raise RuntimeError("DPLL node limit exceeded")
        if not propagate():
            return None
        if all(value >= 0 for value in assignments):
            mask = sum(value << vertex for vertex, value in enumerate(assignments))
            assert satisfies_clauses(mask, clauses)
            return mask
        vertex = max(
            (item for item in range(VERTICES) if assignments[item] < 0),
            key=lambda item: occurrences[item],
        )
        preferred = 0 if vertex == 0 else 1
        snapshot = len(trail)
        for value in (preferred, 1 - preferred):
            if enqueue(vertex, value):
                result = search(depth + 1)
                if result is not None:
                    return result
            backtrack(snapshot)
        return None

    for literals in literal_clauses:
        if len(literals) == 1 and not enqueue(literals[0] // 2, literals[0] % 2):
            return None, {
                "status": "UNSAT",
                "nodes": 1,
                "max_depth": 0,
                "clause_count": len(clauses),
                "solver": "watched-literal exact DPLL",
            }
    # Output complement preserves degree and H3, so fix s(0)=-1.
    initially_consistent = enqueue(0, 0)
    result = search(0) if initially_consistent else None
    return result, {
        "status": "UNSAT" if result is None else "candidate",
        "nodes": nodes,
        "max_depth": max_depth,
        "clause_count": len(clauses),
        "solver": "watched-literal exact DPLL",
    }


def dpll_candidate_cpp(
    clauses: list[Clause], node_limit: int
) -> tuple[int | None, dict[str, int | str]]:
    """Run the same exact watched-literal search in the compiled helper."""
    if (
        not CPP_DPLL_BINARY.exists()
        or CPP_DPLL_BINARY.stat().st_mtime < CPP_DPLL_SOURCE.stat().st_mtime
    ):
        subprocess.run(
            [
                "c++",
                "-O3",
                "-std=c++17",
                str(CPP_DPLL_SOURCE),
                "-o",
                str(CPP_DPLL_BINARY),
            ],
            check=True,
        )
    serialized = [f"{len(clauses)} {node_limit}\n"]
    serialized.extend(
        f"{positive} {negative}\n" for positive, negative in clauses
    )
    result = subprocess.run(
        [str(CPP_DPLL_BINARY)],
        input="".join(serialized),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 3:
        raise RuntimeError(f"DPLL node limit exceeded: {result.stdout.strip()}")
    if result.returncode != 0:
        raise RuntimeError(
            f"compiled DPLL failed with code {result.returncode}: "
            f"{result.stderr.strip()}"
        )
    fields = result.stdout.strip().split()
    status = fields[0]
    if status == "candidate":
        assert len(fields) == 4
        candidate = int(fields[1], 16)
        nodes = int(fields[2])
        max_depth = int(fields[3])
    else:
        assert status == "UNSAT"
        assert len(fields) == 3
        candidate = None
        nodes = int(fields[1])
        max_depth = int(fields[2])
    if candidate is not None:
        assert satisfies_clauses(candidate, clauses)
    return candidate, {
        "status": "UNSAT" if candidate is None else "candidate",
        "nodes": nodes,
        "max_depth": max_depth,
        "clause_count": len(clauses),
        "solver": "compiled watched-literal exact DPLL",
    }


def dpll_candidate_pycosat(
    clauses: list[Clause], node_limit: int
) -> tuple[int | None, dict[str, int | str]]:
    """Use PicoSAT for fast exact candidates and compiled DPLL to confirm UNSAT."""
    del node_limit

    def literal_clauses():
        # Output complement preserves degree and H3, so fix s(0)=-1.
        yield [-1]
        for positive, negative in clauses:
            literals = []
            for vertex in range(VERTICES):
                bit = 1 << vertex
                if positive & bit:
                    literals.append(vertex + 1)
                elif negative & bit:
                    literals.append(-(vertex + 1))
            assert literals
            yield literals

    result = pycosat.solve(literal_clauses(), vars=VERTICES)
    if result == "UNKNOWN":
        raise RuntimeError("PicoSAT returned UNKNOWN")
    if result == "UNSAT":
        candidate, summary = dpll_candidate_cpp(clauses, 50_000_000)
        assert candidate is None and summary["status"] == "UNSAT"
        summary["solver"] = "PicoSAT plus compiled watched-literal UNSAT confirmation"
        return None, summary
    assert isinstance(result, list)
    candidate = sum(1 << (literal - 1) for literal in result if literal > 0)
    assert not (candidate & 1)
    assert satisfies_clauses(candidate, clauses)
    return candidate, {
        "status": "candidate",
        "nodes": -1,
        "max_depth": -1,
        "clause_count": len(clauses),
        "solver": "PicoSAT exact candidate search",
    }


def literal_matrix(inputs: np.ndarray, orientation: int) -> np.ndarray:
    literals = inputs if orientation > 0 else 1.0 - inputs
    return np.column_stack([np.ones(VERTICES), literals])


def softmax(rows: np.ndarray) -> np.ndarray:
    shifted = rows - np.max(rows, axis=1, keepdims=True)
    exponentials = np.exp(np.maximum(shifted, -700.0))
    raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
    epsilon = 1e-12
    return (1.0 - WIDTH * epsilon) * raw + epsilon


def quantized_denominator(
    weights: np.ndarray, orientation: int
) -> np.ndarray:
    integers = [max(1, int(value)) for value in weights]
    if orientation > 0:
        return np.array(integers, dtype=np.int64)
    return np.array(
        [sum(integers)] + [-value for value in integers[1:]],
        dtype=np.int64,
    )


def continuous_inner_lp_search(
    signs: np.ndarray,
    seed: int,
    restarts: int,
    max_iterations: int,
) -> tuple[dict[str, object] | None, dict[str, object]]:
    """Optimize denominators with an exact numerator LP before logistic search."""
    inner_lp_core.N = N
    inner_lp_core.HEADS = HEADS
    inner_lp_core.WIDTH = WIDTH
    inner_lp_core.VERTICES = VERTICES
    inner_lp_core.AFFINE = core.affine_matrix(N).astype(float)
    scales = (
        30,
        100,
        300,
        1000,
        3000,
        10000,
        100000,
        1000000,
        10000000,
        100000000,
        1000000000,
    )
    attempts = []
    search_seeds = tuple(dict.fromkeys((202607142, seed)))
    for simplex_floor in (1e-6, 1e-9, 1e-12):
        def configured_softmax(logits: np.ndarray) -> np.ndarray:
            centered = logits - np.max(logits, axis=1, keepdims=True)
            exponentials = np.exp(np.maximum(centered, -700.0))
            raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
            return (1.0 - WIDTH * simplex_floor) * raw + simplex_floor

        inner_lp_core.softmax = configured_softmax
        for search_seed in search_seeds:
            for positive_heads in range(HEADS + 1):
                found, best = inner_lp_core.search_orientation(
                    signs.astype(float),
                    positive_heads,
                    search_seed + 1009 * positive_heads,
                    restarts,
                    max_iterations,
                    scales,
                )
                attempts.append(
                    {
                        "simplex_floor": simplex_floor,
                        "seed": search_seed,
                        "positive_heads": positive_heads,
                        "best": best,
                    }
                )
                if found is None:
                    continue
                certificate = exact_head_certificate(signs, found["denominators"])
                if certificate is None:
                    continue
                certificate["inner_lp_simplex_floor"] = simplex_floor
                certificate["inner_lp_seed"] = search_seed
                certificate["inner_lp_positive_heads"] = positive_heads
                certificate["inner_lp_restart"] = found["restart"]
                certificate["inner_lp_rounding_scale"] = found["rounding_scale"]
                return certificate, {
                    "status": "exact inner-LP H3 hit",
                    "attempts": attempts,
                }
    return None, {
        "status": "inner-LP search found no exact certificate",
        "attempts": attempts,
    }


def continuous_search(
    signs: np.ndarray,
    seed: int,
    restarts: int,
    max_iterations: int,
) -> tuple[dict[str, object] | None, dict[str, object]]:
    inputs = core.cube(N).astype(float)
    affine = np.column_stack([np.ones(VERTICES), inputs])
    rng = np.random.default_rng(seed)
    best_accuracy = 0
    best_minimum = float("-inf")
    best: dict[str, object] = {}
    scales = tuple(10**exponent for exponent in range(2, 11))
    for orientations in itertools.product((-1, 1), repeat=HEADS):
        literals = [literal_matrix(inputs, value) for value in orientations]

        def objective_gradient(
            variables: np.ndarray, regularization: float
        ) -> tuple[float, np.ndarray]:
            numerators = variables[: HEADS * WIDTH].reshape(HEADS, WIDTH)
            logits = variables[HEADS * WIDTH :].reshape(HEADS, WIDTH)
            theta = softmax(logits)
            denominator_values = np.column_stack(
                [literals[head] @ theta[head] for head in range(HEADS)]
            )
            numerator_values = affine @ numerators.T
            score = np.sum(numerator_values / denominator_values, axis=1)
            arguments = -signs * score
            score_gradient = -signs * expit(arguments) / VERTICES
            loss = float(np.mean(np.logaddexp(0.0, arguments)))
            loss += regularization * (
                np.sum(numerators * numerators)
                + 0.001 * np.sum(logits * logits)
            )
            numerator_gradient = (
                affine.T @ (score_gradient[:, None] / denominator_values)
            ).T
            numerator_gradient += 2 * regularization * numerators
            theta_gradient = np.vstack(
                [
                    literals[head].T
                    @ (
                        -score_gradient
                        * numerator_values[:, head]
                        / denominator_values[:, head] ** 2
                    )
                    for head in range(HEADS)
                ]
            )
            logit_gradient = theta * (
                theta_gradient
                - np.sum(theta * theta_gradient, axis=1, keepdims=True)
            )
            logit_gradient += 0.002 * regularization * logits
            return loss, np.concatenate(
                [numerator_gradient.ravel(), logit_gradient.ravel()]
            )

        for restart in range(restarts):
            variables = np.concatenate(
                [
                    rng.normal(scale=0.7, size=HEADS * WIDTH),
                    rng.normal(scale=3.0, size=HEADS * WIDTH),
                ]
            )
            regularization = 10 ** rng.uniform(-12.0, -6.0)
            result = minimize(
                lambda current: objective_gradient(current, regularization),
                variables,
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": max_iterations,
                    "ftol": 1e-14,
                    "gtol": 1e-9,
                    "maxls": 60,
                },
            )
            numerators = result.x[: HEADS * WIDTH].reshape(HEADS, WIDTH)
            theta = softmax(result.x[HEADS * WIDTH :].reshape(HEADS, WIDTH))
            denominator_values = np.column_stack(
                [literals[head] @ theta[head] for head in range(HEADS)]
            )
            signed = signs * np.sum(
                (affine @ numerators.T) / denominator_values, axis=1
            )
            accuracy = int(np.sum(signed > 1e-8))
            minimum = float(np.min(signed))
            if (accuracy, minimum) > (best_accuracy, best_minimum):
                best_accuracy, best_minimum = accuracy, minimum
                best = {
                    "orientations": list(orientations),
                    "restart": restart,
                    "accuracy": accuracy,
                    "minimum_signed_score": minimum,
                    "wrong_vertices": [
                        int(vertex) for vertex in np.flatnonzero(signed <= 1e-8)
                    ],
                }
            if accuracy < VERTICES - 6:
                continue
            for scale in scales:
                denominators = np.vstack(
                    [
                        quantized_denominator(
                            np.maximum(1, np.rint(scale * theta[head])),
                            orientations[head],
                        )
                        for head in range(HEADS)
                    ]
                )
                certificate = exact_head_certificate(signs, denominators)
                if certificate is not None:
                    certificate["orientations"] = list(orientations)
                    certificate["continuous_restart"] = restart
                    certificate["rounding_scale"] = scale
                    return certificate, best
    return None, best


def exact_degree_certificate(mask: int) -> list[int]:
    signs = signs_from_mask(mask)
    certificate = core.exact_integer_separator(
        signs, core.monomial_matrix(N, 3)
    )
    if certificate is None:
        raise AssertionError(f"degree clauses admitted non-cubic mask 0x{mask:08x}")
    return [int(value) for value in certificate[0]]


def verify_head_record(record: dict[str, object]) -> None:
    mask = int(record["truth_mask_hex"], 16)
    certificate = record["certificate"]
    denominators = np.array(certificate["denominators"], dtype=object)
    assert valid_denominators(denominators)
    coefficients = np.array(certificate["score_coefficients"], dtype=object)
    signed = signs_from_mask(mask).astype(object) * (
        cleared_matrix(denominators) @ coefficients
    )
    assert min(signed) == int(certificate["minimum_signed_cleared_score"])
    assert min(signed) > 0


def verify_head_symmetry_orbit(record: dict[str, object]) -> None:
    """Verify all 480 exact cube and output transforms of one H3 hit."""
    verify_head_record(record)
    mask = int(record["truth_mask_hex"], 16)
    certificate = record["certificate"]
    denominators = [tuple(int(value) for value in row) for row in certificate["denominators"]]
    coefficients = [int(value) for value in certificate["score_coefficients"]]
    assert len(coefficients) == 1 + HEADS * WIDTH
    constant = coefficients[0]
    numerators = [
        tuple(coefficients[1 + head * WIDTH : 1 + (head + 1) * WIDTH])
        for head in range(HEADS)
    ]
    original_values = cleared_matrix(denominators) @ np.array(coefficients, dtype=object)
    for permutation in itertools.permutations(range(N)):
        for global_complement in (False, True):
            transformed_denominators = [
                transform_affine_row(row, permutation, global_complement)
                for row in denominators
            ]
            transformed_numerators = [
                transform_affine_row(row, permutation, global_complement)
                for row in numerators
            ]
            assert valid_denominators(transformed_denominators)
            transformed_coefficients = np.array(
                [constant]
                + [value for row in transformed_numerators for value in row],
                dtype=object,
            )
            transformed_values = (
                cleared_matrix(transformed_denominators) @ transformed_coefficients
            )
            expected = np.zeros(VERTICES, dtype=object)
            for vertex in range(VERTICES):
                image = transform_vertex(vertex, permutation, global_complement)
                expected[image] = original_values[vertex]
            assert np.array_equal(transformed_values, expected)
            transformed_mask = transform_mask(mask, permutation, global_complement)
            for output_complement in (False, True):
                current_mask = (
                    FULL_MASK ^ transformed_mask
                    if output_complement
                    else transformed_mask
                )
                current_values = -transformed_values if output_complement else transformed_values
                signed = signs_from_mask(current_mask).astype(object) * current_values
                assert min(signed) > 0


def singleton_record(
    learned_certificate_index: int,
    learned_record: dict[str, object],
) -> dict[str, object]:
    singleton = {
        "source_mask_hex": learned_record["truth_mask_hex"],
        "learned_certificate_index": learned_certificate_index,
        "symmetry_orbit": "S5 x global input complement x output complement",
    }
    singleton["orbit_clause_count"] = len(singleton_clauses(singleton))
    return singleton


def upgrade_payload(payload: dict[str, object]) -> bool:
    """Migrate older checkpoints to the exact singleton-orbit fallback."""
    changed = False
    frozen_archive = bool(payload["parameters"].get("frozen_archive"))
    if not frozen_archive:
        known_learned = {
            (
                int(record["truth_mask_hex"], 16),
                canonical_triple(record["certificate"]["denominators"]),
            )
            for record in payload["learned_certificates"]
        }
        for index, seed_record in enumerate(LEARNED_SEEDS):
            mask = int(seed_record["mask"])
            denominators = canonical_triple(seed_record["denominators"])
            key = (mask, denominators)
            if key in known_learned:
                continue
            certificate = exact_head_certificate(
                signs_from_mask(mask), np.array(denominators, dtype=np.int64)
            )
            if certificate is None:
                raise AssertionError(f"learned seed T{index + 1} did not verify")
            payload["learned_certificates"].append(
                {
                    "source": f"curated exact seed T{index + 1}",
                    "truth_mask_hex": f"0x{mask:08x}",
                    "certificate": certificate,
                }
            )
            known_learned.add(key)
            changed = True
    singletons = payload.setdefault("singleton_covers", [])
    known_indices = {
        int(item["learned_certificate_index"])
        for item in singletons
    }
    for index, learned_record in enumerate(payload["learned_certificates"]):
        if index not in known_indices:
            singletons.append(singleton_record(index, learned_record))
            changed = True
    scale = int(payload["parameters"]["near_literal_scale"])
    known_dictionary = {
        canonical_triple(item) for item in payload["base_dictionary"]
    }
    for denominators in asymmetric_near_literal_representatives(scale):
        key = canonical_triple(denominators)
        if key not in known_dictionary:
            known_dictionary.add(key)
            payload["base_dictionary"].append([list(row) for row in key])
            changed = True
    if not frozen_archive:
        for seed_record in LEARNED_SEEDS:
            key = canonical_triple(seed_record["denominators"])
            if key not in known_dictionary:
                known_dictionary.add(key)
                payload["base_dictionary"].append([list(row) for row in key])
                changed = True
    parameter_updates = {
        "symmetric_near_literal_seed_count": 80,
        "asymmetric_near_literal_representative_count": 2,
        "asymmetric_near_literal_orbit_count": 480,
    }
    for key, value in parameter_updates.items():
        if payload["parameters"].get(key) != value:
            payload["parameters"][key] = value
            changed = True
    if payload.get("schema_version") != 3:
        payload["schema_version"] = 3
        changed = True
    if changed:
        payload["final_dpll"] = None
    return changed


def verify_family(family: dict[str, object]) -> None:
    denominators = np.array(family["denominators"], dtype=object)
    assert valid_denominators(denominators)
    basis, columns = independent_score_basis(denominators)
    assert list(columns) == family["score_basis_columns"]
    rank = int(family["score_space_rank"])
    assert basis.shape[1] == rank
    coefficients = np.array(family["ray_coefficients"], dtype=object)
    values = basis @ coefficients
    zeros = [int(vertex) for vertex in np.flatnonzero(np.array(values == 0))]
    assert zeros == family["zero_vertices"] and len(zeros) == rank - 1
    assert (
        modular_rank(basis[zeros])
        == int(family["zero_restriction_rank"])
        == rank - 1
    )
    positive = sum((int(value) > 0) << vertex for vertex, value in enumerate(values))
    negative = sum((int(value) < 0) << vertex for vertex, value in enumerate(values))
    assert positive == int(family["fixed_positive_mask_hex"], 16)
    assert negative == int(family["fixed_negative_mask_hex"], 16)
    source = int(family["source_mask_hex"], 16)
    assert (source & positive) == positive
    assert ((FULL_MASK ^ source) & negative) == negative


def all_search_clauses(
    families: list[dict[str, object]],
    singleton_covers: list[dict[str, object]] | None = None,
) -> list[Clause]:
    clauses = set(degree_clauses())
    family_source_masks = {
        int(family["source_mask_hex"], 16) for family in families
    }
    for family in families:
        clauses.update(family_clauses(family))
    for singleton in singleton_covers or []:
        # A tangent family contains its source truth table, so its orbit clause
        # subsumes the corresponding singleton-orbit clause.
        if int(singleton["source_mask_hex"], 16) not in family_source_masks:
            clauses.update(singleton_clauses(singleton))
    return sorted(clauses)


def verify_payload(payload: dict[str, object], dpll_node_limit: int) -> None:
    upgrade_payload(payload)
    assert payload["parameters"]["cubic_coefficient_bound"] is None
    assert payload["parameters"]["degree_clause_count"] == 6_508
    dictionary = payload["base_dictionary"]
    assert len({canonical_triple(item) for item in dictionary}) == len(dictionary)
    assert all(valid_denominators(item) for item in dictionary)
    for record in payload["learned_certificates"]:
        verify_head_record(record)
    for singleton in payload["singleton_covers"]:
        index = int(singleton["learned_certificate_index"])
        assert 0 <= index < len(payload["learned_certificates"])
        learned_record = payload["learned_certificates"][index]
        assert singleton["source_mask_hex"] == learned_record["truth_mask_hex"]
        clauses_for_singleton = singleton_clauses(singleton)
        assert len(clauses_for_singleton) == int(singleton["orbit_clause_count"])
        verify_head_symmetry_orbit(learned_record)
    for family in payload["families"]:
        verify_family(family)
    clauses = all_search_clauses(payload["families"], payload["singleton_covers"])
    candidate, summary = dpll_candidate(clauses, dpll_node_limit)
    final = payload.get("final_dpll")
    if final and final["status"] == "UNSAT":
        assert candidate is None
    elif final and final["status"] == "candidate":
        assert candidate is not None
        archived_candidate = int(final["candidate_mask_hex"], 16)
        assert satisfies_clauses(archived_candidate, clauses)
        exact_degree_certificate(archived_candidate)
    print(
        f"verified {len(payload['families'])} exact H3 families; "
        f"DPLL {summary['status']} in {summary['nodes']} nodes",
        flush=True,
    )


def write_checkpoint(output: Path, payload: dict[str, object]) -> None:
    output.write_text(json.dumps(payload, indent=2) + "\n")


def freeze_final_archive(payload: dict[str, object]) -> dict[str, object]:
    """Drop search-only history and redundant singleton witnesses after UNSAT."""
    final = payload.get("final_dpll")
    assert final is not None and final["status"] == "UNSAT"
    family_masks = {
        int(family["source_mask_hex"], 16) for family in payload["families"]
    }
    selected_singletons = []
    seen_singleton_orbits = set()
    for singleton in payload["singleton_covers"]:
        if int(singleton["source_mask_hex"], 16) in family_masks:
            continue
        orbit = tuple(singleton_clauses(singleton))
        if orbit in seen_singleton_orbits:
            continue
        seen_singleton_orbits.add(orbit)
        selected_singletons.append(singleton)

    learned_records = []
    remapped_singletons = []
    for singleton in selected_singletons:
        old_index = int(singleton["learned_certificate_index"])
        learned = payload["learned_certificates"][old_index]
        new_index = len(learned_records)
        learned_records.append(learned)
        remapped = dict(singleton)
        remapped["learned_certificate_index"] = new_index
        remapped_singletons.append(remapped)

    dictionary_keys = {
        canonical_triple(item)
        for item in asymmetric_near_literal_representatives(
            int(payload["parameters"]["near_literal_scale"])
        )
    }
    dictionary_keys.update(
        canonical_triple(family["denominators"])
        for family in payload["families"]
    )
    dictionary_keys.update(
        canonical_triple(record["certificate"]["denominators"])
        for record in learned_records
    )
    parameters = dict(payload["parameters"])
    parameters["frozen_archive"] = True
    return {
        "schema_version": 3,
        "status": (
            "Exact finite H3 tangent-family and singleton-orbit cover of every "
            "five-bit degree-at-most-three sign pattern."
        ),
        "parameters": parameters,
        "base_dictionary": [
            [list(row) for row in key] for key in sorted(dictionary_keys)
        ],
        "learned_certificates": learned_records,
        "singleton_covers": remapped_singletons,
        "families": payload["families"],
        "iterations": [],
        "search_summary": {
            "checkpoint_iteration_count": len(payload["iterations"]),
            "checkpoint_family_count": len(payload["families"]),
            "checkpoint_learned_certificate_count": len(
                payload["learned_certificates"]
            ),
            "retained_singleton_count": len(remapped_singletons),
        },
        "final_dpll": final,
    }


def initialize_payload(scale: int, seed: int) -> dict[str, object]:
    base = near_literal_dictionary(scale)
    base.extend(asymmetric_near_literal_representatives(scale))
    learned_records = []
    families = []
    seen_base = {canonical_triple(item) for item in base}
    for index, seed_record in enumerate(LEARNED_SEEDS):
        mask = int(seed_record["mask"])
        denominators = np.array(
            canonical_triple(seed_record["denominators"]), dtype=np.int64
        )
        certificate = exact_head_certificate(signs_from_mask(mask), denominators)
        if certificate is None:
            raise AssertionError(f"learned seed T{index + 1} did not verify")
        record = {
            "source": f"temporary active loop T{index + 1}",
            "truth_mask_hex": f"0x{mask:08x}",
            "certificate": certificate,
        }
        learned_records.append(record)
        key = canonical_triple(denominators)
        if key not in seen_base:
            seen_base.add(key)
            base.append(np.array(key, dtype=np.int64))
        family = extreme_family_certificate(
            mask, denominators, seed + 1009 * (index + 1)
        )
        if family is not None:
            families.append(family)
    return {
        "schema_version": 3,
        "status": (
            "Exact H3 certificates and simple tangent families are verified over the "
            "integers. The degree-at-most-three condition uses all 6,508 exact "
            "affine-covector clauses and has no cubic coefficient bound. Every "
            "exact H3 hit also contributes a formally verified singleton orbit. "
            "A nonlinear survivor is search evidence only."
        ),
        "parameters": {
            "input_bits": N,
            "heads": HEADS,
            "near_literal_scale": scale,
            "symmetric_near_literal_seed_count": 80,
            "asymmetric_near_literal_representative_count": 2,
            "asymmetric_near_literal_orbit_count": 480,
            "degree_clause_count": 6_508,
            "cubic_coefficient_bound": None,
            "seed": seed,
        },
        "base_dictionary": [item.tolist() for item in base],
        "learned_certificates": learned_records,
        "singleton_covers": [
            singleton_record(index, record)
            for index, record in enumerate(learned_records)
        ],
        "families": families,
        "iterations": [],
        "final_dpll": None,
    }


def expanded_dictionary(payload: dict[str, object]) -> list[np.ndarray]:
    answer = []
    seen = set()
    scale = int(payload["parameters"]["near_literal_scale"])
    asymmetric = {
        canonical_triple(item)
        for item in asymmetric_near_literal_representatives(scale)
    }
    base = sorted(
        payload["base_dictionary"],
        key=lambda item: canonical_triple(item) not in asymmetric,
    )
    for triple in base:
        for image in denominator_orbit(triple):
            key = canonical_triple(image)
            if key not in seen:
                seen.add(key)
                answer.append(image)
    return answer


def fixed_dictionary_hit(
    signs: np.ndarray, dictionary: list[np.ndarray]
) -> tuple[dict[str, object] | None, int | None]:
    for index, denominators in enumerate(dictionary):
        certificate = exact_head_certificate(signs, denominators)
        if certificate is not None:
            return certificate, index
    return None, None


def supplemental_rank16_space_hits(
    mask: int,
    dictionary: list[np.ndarray],
    excluded_denominators: object,
    seed: int,
    space_count: int,
    attempts: int,
    families_per_space: int,
) -> list[tuple[int, dict[str, object], list[dict[str, object]]]]:
    """Collect productive simple-ray bundles from distinct rank-16 spaces."""
    if space_count <= 0:
        return []
    signs = signs_from_mask(mask)
    excluded = canonical_triple(excluded_denominators)
    results = []
    seen_denominators = {excluded}
    seen_orbits: set[tuple[Clause, ...]] = set()
    for dictionary_index, denominators in enumerate(dictionary):
        key = canonical_triple(denominators)
        if key in seen_denominators:
            continue
        seen_denominators.add(key)
        certificate = exact_head_certificate(signs, denominators)
        if certificate is None:
            continue
        families = extreme_family_certificates(
            mask,
            certificate["denominators"],
            seed + 1000039 * (dictionary_index + 1),
            attempts,
            families_per_space,
        )
        productive = []
        for family in families:
            if int(family["score_space_rank"]) != 16:
                continue
            orbit = tuple(family_clauses(family))
            if orbit in seen_orbits:
                continue
            seen_orbits.add(orbit)
            productive.append(family)
        if not productive:
            continue
        results.append((dictionary_index, certificate, productive))
        if len(results) >= space_count:
            break
    return results


def rescue_singleton_fallbacks(
    payload: dict[str, object],
    seed: int,
    attempts: int,
) -> int:
    """Revisit old nonsimple hits with the generic rank-16 perturbation orbit."""
    scale = int(payload["parameters"]["near_literal_scale"])
    dictionary = []
    seen = set()
    for representative in asymmetric_near_literal_representatives(scale):
        for denominators in denominator_orbit(representative):
            key = canonical_triple(denominators)
            if key not in seen:
                seen.add(key)
                dictionary.append(denominators)
    assert len(dictionary) == 480
    rescued = 0
    for record in payload["iterations"]:
        if record.get("coverage_outcome") != "exact singleton-orbit fallback":
            continue
        if "asymmetric_rescue" in record:
            continue
        mask = int(record["candidate_mask_hex"], 16)
        certificate, dictionary_index = fixed_dictionary_hit(
            signs_from_mask(mask), dictionary
        )
        if certificate is None:
            continue
        family = extreme_family_certificate(
            mask,
            certificate["denominators"],
            seed + 1000033 * int(record["iteration"]),
            attempts,
        )
        if family is None:
            continue
        learned_record = {
            "source": "rank-16 asymmetric rescue",
            "truth_mask_hex": record["candidate_mask_hex"],
            "certificate": certificate,
        }
        verify_head_record(learned_record)
        verify_family(family)
        payload["learned_certificates"].append(learned_record)
        learned_index = len(payload["learned_certificates"]) - 1
        payload["singleton_covers"].append(
            singleton_record(learned_index, learned_record)
        )
        payload["families"].append(family)
        record["asymmetric_rescue"] = {
            "dictionary_index": dictionary_index,
            "learned_certificate_index": learned_index,
            "family_index": len(payload["families"]) - 1,
            "score_space_rank": family["score_space_rank"],
            "family_orbit_clause_count": len(family_clauses(family)),
        }
        rescued += 1
    if rescued:
        payload["final_dpll"] = None
    return rescued


def enrich_existing_rank16_hits(
    payload: dict[str, object],
    seed: int,
    attempts: int,
    families_per_hit: int,
) -> int:
    """Add several distinct simple-ray orbits from each archived rank-16 hit."""
    known_orbits = {
        tuple(family_clauses(family)) for family in payload["families"]
    }
    added = 0
    for index, record in enumerate(payload["learned_certificates"]):
        if "multi_ray_enrichment" in record:
            continue
        denominators = record["certificate"]["denominators"]
        basis, _ = independent_score_basis(denominators)
        rank = int(basis.shape[1])
        metadata: dict[str, object] = {
            "score_space_rank": rank,
            "requested_family_count": families_per_hit,
            "family_indices": [],
        }
        if rank == 16:
            mask = int(record["truth_mask_hex"], 16)
            candidates = extreme_family_certificates(
                mask,
                denominators,
                seed + 1000037 * (index + 1),
                attempts,
                families_per_hit,
            )
            metadata["found_family_count"] = len(candidates)
            for family in candidates:
                orbit = tuple(family_clauses(family))
                if orbit in known_orbits:
                    continue
                verify_family(family)
                known_orbits.add(orbit)
                payload["families"].append(family)
                metadata["family_indices"].append(len(payload["families"]) - 1)
                added += 1
        metadata["added_family_count"] = len(metadata["family_indices"])
        record["multi_ray_enrichment"] = metadata
    if added:
        payload["final_dpll"] = None
    return added


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--near-literal-scale", type=int, default=10)
    parser.add_argument("--dpll-node-limit", type=int, default=2_000_000)
    parser.add_argument(
        "--dpll-solver",
        choices=("pycosat", "cpp", "python"),
        default="pycosat",
    )
    parser.add_argument("--family-attempts", type=int, default=256)
    parser.add_argument("--families-per-hit", type=int, default=8)
    parser.add_argument("--spaces-per-hit", type=int, default=4)
    parser.add_argument("--existing-families-per-hit", type=int, default=4)
    parser.add_argument("--continuous-restarts", type=int, default=48)
    parser.add_argument("--continuous-max-iterations", type=int, default=6000)
    parser.add_argument("--inner-lp-restarts", type=int, default=12)
    parser.add_argument("--inner-lp-max-iterations", type=int, default=180)
    parser.add_argument("--seed", type=int, default=530260714)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--final-output", type=Path, default=DEFAULT_FINAL_OUTPUT)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()
    active_dpll_candidate = {
        "pycosat": dpll_candidate_pycosat,
        "cpp": dpll_candidate_cpp,
        "python": dpll_candidate,
    }[arguments.dpll_solver]

    if arguments.verify_only:
        verify_payload(
            json.loads(arguments.output.read_text()), arguments.dpll_node_limit
        )
        return

    if arguments.resume and arguments.output.exists():
        payload = json.loads(arguments.output.read_text())
    else:
        payload = initialize_payload(arguments.near_literal_scale, arguments.seed)
        write_checkpoint(arguments.output, payload)
    if upgrade_payload(payload):
        write_checkpoint(arguments.output, payload)
    rescued = rescue_singleton_fallbacks(
        payload,
        arguments.seed,
        max(512, arguments.family_attempts),
    )
    if rescued:
        write_checkpoint(arguments.output, payload)
        print(
            f"rescued {rescued} prior singleton fallbacks with exact "
            "rank-16 tangent families",
            flush=True,
        )
    enriched = enrich_existing_rank16_hits(
        payload,
        arguments.seed + 700000001,
        arguments.family_attempts,
        arguments.existing_families_per_hit,
    )
    if enriched:
        write_checkpoint(arguments.output, payload)
        print(
            f"added {enriched} deduplicated tangent families from archived "
            "rank-16 hits",
            flush=True,
        )

    clauses = all_search_clauses(
        payload["families"], payload["singleton_covers"]
    )
    clause_set = set(clauses)

    def add_active_clauses(new_clauses: list[Clause]) -> None:
        for clause in new_clauses:
            if clause not in clause_set:
                clause_set.add(clause)
                clauses.append(clause)

    for iteration in range(arguments.iterations):
        candidate, dpll = active_dpll_candidate(
            clauses, arguments.dpll_node_limit
        )
        if candidate is None:
            payload["final_dpll"] = dpll
            write_checkpoint(arguments.output, payload)
            print(
                f"exact DPLL UNSAT after {dpll['nodes']} nodes and "
                f"{len(clauses)} clauses",
                flush=True,
            )
            break
        dpll["candidate_mask_hex"] = f"0x{candidate:08x}"
        payload["final_dpll"] = dpll
        record: dict[str, object] = {
            "iteration": len(payload["iterations"]) + 1,
            "candidate_mask_hex": f"0x{candidate:08x}",
            "dpll": dpll,
            "degree_three_coefficients": exact_degree_certificate(candidate),
        }
        print(
            f"iteration={record['iteration']} candidate=0x{candidate:08x} "
            f"families={len(payload['families'])} clauses={len(clauses)}",
            flush=True,
        )

        dictionary = expanded_dictionary(payload)
        record["expanded_dictionary_size"] = len(dictionary)
        certificate, dictionary_index = fixed_dictionary_hit(
            signs_from_mask(candidate), dictionary
        )
        if certificate is not None:
            record["outcome"] = "exact fixed-dictionary hit"
            record["dictionary_index"] = dictionary_index
        else:
            certificate, inner_best = continuous_inner_lp_search(
                signs_from_mask(candidate),
                arguments.seed + 100003 * len(payload["iterations"]),
                arguments.inner_lp_restarts,
                arguments.inner_lp_max_iterations,
            )
            record["inner_lp_search"] = inner_best
            if certificate is not None:
                record["outcome"] = "exact learned inner-LP H3 hit"
            else:
                certificate, best = continuous_search(
                    signs_from_mask(candidate),
                    arguments.seed + 100003 * len(payload["iterations"]),
                    arguments.continuous_restarts,
                    arguments.continuous_max_iterations,
                )
                record["continuous_best"] = best
            if certificate is None:
                record["outcome"] = "uncertified robust survivor"
                payload["iterations"].append(record)
                write_checkpoint(arguments.output, payload)
                print(json.dumps(record, indent=2), flush=True)
                break
            if "outcome" not in record:
                record["outcome"] = "exact learned H3 hit"
            key = canonical_triple(certificate["denominators"])
            known = {canonical_triple(item) for item in payload["base_dictionary"]}
            if key not in known:
                payload["base_dictionary"].append([list(row) for row in key])

        learned_record = {
            "source": record["outcome"],
            "truth_mask_hex": f"0x{candidate:08x}",
            "certificate": certificate,
        }
        verify_head_record(learned_record)
        payload["learned_certificates"].append(learned_record)
        learned_index = len(payload["learned_certificates"]) - 1
        singleton = singleton_record(learned_index, learned_record)
        payload["singleton_covers"].append(singleton)
        record["singleton_orbit_clause_count"] = singleton["orbit_clause_count"]
        requested_family_count = max(
            arguments.families_per_hit,
            (
                32
                if int(dpll["nodes"]) < 0 or int(dpll["nodes"]) > 1_000
                else arguments.families_per_hit
            ),
        )
        primary_families = extreme_family_certificates(
            candidate,
            certificate["denominators"],
            arguments.seed + 1000003 * len(payload["iterations"]),
            arguments.family_attempts,
            requested_family_count,
        )
        bundles: list[
            tuple[int | None, dict[str, object], list[dict[str, object]]]
        ] = [(dictionary_index, learned_record, primary_families)]
        bundle_learned_indices = {id(learned_record): learned_index}
        supplemental = supplemental_rank16_space_hits(
            candidate,
            dictionary,
            certificate["denominators"],
            arguments.seed + 900000011 * len(payload["iterations"]),
            max(0, arguments.spaces_per_hit - (1 if primary_families else 0)),
            arguments.family_attempts,
            requested_family_count,
        )
        for supplemental_index, supplemental_certificate, families in supplemental:
            supplemental_record = {
                "source": "supplemental rank-16 multi-space hit",
                "truth_mask_hex": f"0x{candidate:08x}",
                "certificate": supplemental_certificate,
            }
            verify_head_record(supplemental_record)
            payload["learned_certificates"].append(supplemental_record)
            supplemental_learned_index = len(payload["learned_certificates"]) - 1
            payload["singleton_covers"].append(
                singleton_record(supplemental_learned_index, supplemental_record)
            )
            bundle_learned_indices[id(supplemental_record)] = (
                supplemental_learned_index
            )
            bundles.append((supplemental_index, supplemental_record, families))

        new_families = []
        seen_new_orbits: set[tuple[Clause, ...]] = set()
        supplemental_metadata = []
        productive_bundle_count = 0
        for bundle_index, bundle_record, bundle_families in bundles:
            family_indices = []
            for family in bundle_families:
                orbit = tuple(family_clauses(family))
                if orbit in seen_new_orbits:
                    continue
                seen_new_orbits.add(orbit)
                verify_family(family)
                payload["families"].append(family)
                family_indices.append(len(payload["families"]) - 1)
                new_families.append(family)
            if family_indices:
                productive_bundle_count += 1
            bundle_ranks = sorted(
                {
                    int(family["score_space_rank"])
                    for family in bundle_families
                }
            )
            bundle_record["multi_ray_enrichment"] = {
                "score_space_rank": (
                    bundle_ranks[0] if len(bundle_ranks) == 1 else bundle_ranks
                ),
                "requested_family_count": requested_family_count,
                "found_family_count": len(bundle_families),
                "added_family_count": len(family_indices),
                "family_indices": family_indices,
            }
            if bundle_record is not learned_record:
                supplemental_metadata.append(
                    {
                        "dictionary_index": bundle_index,
                        "learned_certificate_index": bundle_learned_indices[
                            id(bundle_record)
                        ],
                        "family_count_added": len(family_indices),
                    }
                )
        if supplemental_metadata:
            record["supplemental_space_hits"] = supplemental_metadata
        if not new_families:
            record["family_outcome"] = "no simple rank-(r-1) family found"
            record["coverage_outcome"] = "exact singleton-orbit fallback"
            payload["iterations"].append(record)
            payload["final_dpll"] = None
            add_active_clauses(singleton_clauses(singleton))
            write_checkpoint(arguments.output, payload)
            print(
                json.dumps(
                    {
                        "iteration": record["iteration"],
                        "mask": record["candidate_mask_hex"],
                        "outcome": record["outcome"],
                        "families": len(payload["families"]),
                        "singleton_orbit_clauses": record[
                            "singleton_orbit_clause_count"
                        ],
                    }
                ),
                flush=True,
            )
            continue
        ranks = sorted({int(family["score_space_rank"]) for family in new_families})
        record["family_count_added"] = len(new_families)
        record["denominator_space_count_added"] = productive_bundle_count
        record["family_outcome"] = (
            f"exact simple tangent families from score ranks {ranks}"
        )
        record["family_orbit_clause_count"] = sum(
            len(family_clauses(family)) for family in new_families
        )
        for family in new_families:
            add_active_clauses(family_clauses(family))
        payload["iterations"].append(record)
        payload["final_dpll"] = None
        write_checkpoint(arguments.output, payload)
        print(
            json.dumps(
                {
                    "iteration": record["iteration"],
                    "mask": record["candidate_mask_hex"],
                    "outcome": record["outcome"],
                    "families": len(payload["families"]),
                    "orbit_clauses": record["family_orbit_clause_count"],
                }
            ),
            flush=True,
        )

    if payload["final_dpll"] is None:
        candidate, summary = active_dpll_candidate(
            clauses, arguments.dpll_node_limit
        )
        if candidate is not None:
            summary["candidate_mask_hex"] = f"0x{candidate:08x}"
        payload["final_dpll"] = summary
        write_checkpoint(arguments.output, payload)
    verification_payload = payload
    if payload["final_dpll"]["status"] == "UNSAT":
        verification_payload = freeze_final_archive(payload)
        write_checkpoint(arguments.final_output, verification_payload)
    verify_payload(verification_payload, arguments.dpll_node_limit)
    print(f"wrote {arguments.output}", flush=True)
    if verification_payload is not payload:
        print(f"wrote {arguments.final_output}", flush=True)


if __name__ == "__main__":
    main()
