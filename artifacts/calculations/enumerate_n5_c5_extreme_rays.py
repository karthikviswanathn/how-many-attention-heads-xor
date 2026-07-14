#!/usr/bin/env python3
"""Enumerate exact extreme rays incident to known locked C5 cells.

Qhull is used only to discover active sets.  Every returned ray is rebuilt
from integer Fourier rows and is then checked exactly.  The resulting ray
set is therefore independent of Qhull's approximate coordinates once the
finite candidate list has been discovered.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from functools import reduce
import json
from math import gcd, lcm
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection

import screen_n5_c5_two_scale as c5
import survey_n5_c5_locked_cells as survey
import verify_n5_c5_fixed_chord_extremizer as verify


def primitive_null_vector(matrix: np.ndarray) -> tuple[int, ...]:
    """Return the primitive null vector of an integer rank-(n-1) matrix."""
    rows = [[Fraction(int(value)) for value in row] for row in matrix]
    row_count = len(rows)
    column_count = matrix.shape[1]
    pivot_row = 0
    pivot_columns: list[int] = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    assert len(pivot_columns) == column_count - 1
    free_column = next(
        column for column in range(column_count) if column not in pivot_columns
    )
    answer = [Fraction(0) for _ in range(column_count)]
    answer[free_column] = Fraction(1)
    for row, column in reversed(list(enumerate(pivot_columns))):
        answer[column] = -sum(
            rows[row][other] * answer[other]
            for other in range(column + 1, column_count)
        )
    denominator = reduce(lcm, (value.denominator for value in answer), 1)
    integers = [
        value.numerator * (denominator // value.denominator) for value in answer
    ]
    divisor = reduce(gcd, (abs(value) for value in integers if value))
    integers = [value // divisor for value in integers]
    first = next(value for value in integers if value)
    if first < 0:
        integers = [-value for value in integers]
    result = tuple(integers)
    assert np.all(matrix.astype(object) @ np.array(result, dtype=object) == 0)
    return result


def ell_slice() -> tuple[np.ndarray, np.ndarray]:
    """Return theta = offset + basis x for the signed-edge-sum-one slice."""
    basis = np.zeros((16, 15), dtype=np.int64)
    offset = np.zeros(16, dtype=np.int64)
    basis[:15, :15] = np.eye(15, dtype=np.int64)
    edge_signs = c5.EDGE_SIGNS.astype(np.int64)
    assert edge_signs[-1] in (-1, 1)
    offset[15] = edge_signs[-1]
    for coordinate in range(6, 15):
        basis[15, coordinate] = -edge_signs[coordinate - 6] * edge_signs[-1]
    return offset, basis


def exact_extreme_rays(mask: int, interior: np.ndarray) -> set[tuple[int, ...]]:
    """Enumerate and exactly reconstruct every extreme ray of one locked cone."""
    signs = verify.target_signs(mask)
    offset, basis = ell_slice()
    signed = signs[:, None] * c5.FOURIER.astype(np.int64)
    halfspaces = np.column_stack((-signed @ basis, -signed @ offset))
    ell = sum(
        int(c5.EDGE_SIGNS[index]) * float(interior[6 + index])
        for index in range(10)
    )
    assert ell > 0
    point = (interior / ell)[:15]
    assert np.max(halfspaces[:, :-1] @ point + halfspaces[:, -1]) < -1e-9
    vertices = HalfspaceIntersection(
        halfspaces.astype(float), point, qhull_options="Qx"
    ).intersections

    rays: set[tuple[int, ...]] = set()
    for vertex in vertices:
        approximate = offset.astype(float) + basis.astype(float) @ vertex
        values = c5.FOURIER @ approximate
        scale = max(1.0, float(np.max(np.abs(values))))
        zero_vertices = np.flatnonzero(np.abs(values) <= 1e-7 * scale)
        assert verify.modular_rank(c5.FOURIER[zero_vertices]) == 15
        ray = primitive_null_vector(c5.FOURIER[zero_vertices].astype(np.int64))
        ray_values = c5.FOURIER.astype(np.int64) @ np.array(ray, dtype=np.int64)
        if np.any(signs * ray_values < 0):
            ray = tuple(-value for value in ray)
            ray_values = -ray_values
        assert np.all(signs * ray_values >= 0)
        assert verify.modular_rank(c5.FOURIER[ray_values == 0]) == 15
        for edge_index, edge_sign in enumerate(c5.EDGE_SIGNS.astype(np.int64)):
            assert edge_sign * ray[6 + edge_index] >= 0
        rays.add(ray)
    return rays


def incident_tangent_topes(
    ray: tuple[int, ...], seed_mask: int, limit: int
) -> tuple[set[int], bool]:
    """Walk tangent topes at one ray inside the fixed C5 edge orthant."""
    fourier = c5.FOURIER.astype(np.int64)
    values = fourier @ np.array(ray, dtype=np.int64)
    zero_vertices = tuple(int(value) for value in np.flatnonzero(values == 0))
    zero_edges = tuple(
        index for index in range(10) if ray[6 + index] == 0
    )
    fixed_mask = sum(
        (int(value) > 0) << vertex
        for vertex, value in enumerate(values)
        if value
    )
    variable_mask = sum(1 << vertex for vertex in zero_vertices)
    assert (seed_mask & ~variable_mask) == fixed_mask

    def feasible(mask: int) -> bool:
        signs = verify.target_signs(mask)
        inequalities = [signs[vertex] * fourier[vertex] for vertex in zero_vertices]
        inequalities.extend(
            int(c5.EDGE_SIGNS[index]) * np.eye(16, dtype=np.int64)[6 + index]
            for index in zero_edges
        )
        result = linprog(
            np.zeros(16),
            A_ub=-np.array(inequalities, dtype=float),
            b_ub=-np.ones(len(inequalities)),
            bounds=[(None, None)] * 16,
            method="highs",
        )
        return bool(result.success)

    queue = deque([seed_mask])
    topes = {seed_mask}
    rejected: set[int] = set()
    while queue and len(topes) < limit:
        mask = queue.popleft()
        for vertex in zero_vertices:
            neighbor = mask ^ (1 << vertex)
            if neighbor in topes or neighbor in rejected:
                continue
            if feasible(neighbor):
                topes.add(neighbor)
                queue.append(neighbor)
                if len(topes) >= limit:
                    break
            else:
                rejected.add(neighbor)
    return topes, not queue


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-limit", type=int, default=1000)
    parser.add_argument("--tangent-limit", type=int, default=0)
    parser.add_argument("--extra-seed", type=lambda value: int(value, 0), action="append", default=[])
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.input:
        payload = json.loads(arguments.input.read_text())
        incidence = {
            tuple(record["ray"]): set(record["masks"])
            for record in payload["incidence"]
        }
        cells = {mask: np.empty(0) for masks in incidence.values() for mask in masks}
        ray_sizes = Counter(payload["ray_sizes"])
    else:
        cells, exhausted = survey.locked_class_walk(arguments.class_limit)
        assert exhausted
        for seed in arguments.extra_seed:
            extra, exhausted = survey.locked_class_walk_from_mask(seed, arguments.class_limit)
            assert exhausted
            cells.update(extra)

        incidence: dict[tuple[int, ...], set[int]] = {}
        ray_sizes = Counter()
        for index, (mask, interior) in enumerate(sorted(cells.items())):
            rays = exact_extreme_rays(mask, interior)
            ray_sizes[len(rays)] += 1
            for ray in rays:
                incidence.setdefault(ray, set()).add(mask)
            if (index + 1) % 50 == 0:
                print(f"locked classes processed: {index + 1}")
        if arguments.output:
            arguments.output.write_text(
                json.dumps(
                    {
                        "incidence": [
                            {"ray": list(ray), "masks": sorted(masks)}
                            for ray, masks in sorted(incidence.items())
                        ],
                        "ray_sizes": dict(sorted(ray_sizes.items())),
                    },
                    separators=(",", ":"),
                )
                + "\n"
            )
    print(f"locked quotient classes: {len(cells)}")
    print(f"exact extreme rays: {len(incidence)}")
    print(f"extreme ray order-40 orbits: {len({verify.ray_orbit_key(ray) for ray in incidence})}")
    print(f"rays per locked class: {dict(sorted(ray_sizes.items()))}")
    zero_sizes = Counter(
        int(np.sum(c5.FOURIER @ np.array(ray) == 0)) for ray in incidence
    )
    print(
        "zero-set sizes: "
        f"{dict(sorted(zero_sizes.items()))}"
    )

    if arguments.tangent_limit:
        tangent_locked: set[int] = set()
        tangent_counts = Counter()
        incomplete = 0
        for index, (ray, masks) in enumerate(sorted(incidence.items())):
            seed = next(iter(masks))
            topes, complete = incident_tangent_topes(ray, seed, arguments.tangent_limit)
            tangent_counts[len(topes)] += 1
            incomplete += not complete
            for mask in topes:
                signs = verify.target_signs(mask).astype(float)
                if survey.fully_locked(signs):
                    tangent_locked.add(survey.canonical_mask(mask))
            if (index + 1) % 50 == 0:
                print(f"ray tangent arrangements processed: {index + 1}")
        print(f"distinct tangent locked classes: {len(tangent_locked)}")
        print(f"new tangent locked classes: {len(tangent_locked - set(cells))}")
        print(f"incomplete tangent walks: {incomplete}")
        print(f"tangent tope counts: {dict(sorted(tangent_counts.items()))}")


if __name__ == "__main__":
    main()
