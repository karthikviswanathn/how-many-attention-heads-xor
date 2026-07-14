#!/usr/bin/env python3
"""Search exact small hitting sets for projective coordinate-flip cycles.

The sign-rank obstruction in Theorems 181 and 184 uses antipodal classes in
the eight-dimensional sign cube.  A valid row set must meet every generic
two-dimensional tope cycle, equivalently every projective coordinate-flip
cycle.  There are 322,560 distinct cycles, each containing eight of the 128
antipodal classes.

This script uses exact cycle enumeration and MILP row generation.  Any
reported hitting set is independently checked against every cycle.  Solver
failure or a time limit is only search evidence.  An infeasible result is
reported only when HiGHS proves infeasibility for the accumulated exact cuts.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, vstack


DIMENSION = 8
CLASS_COUNT = 1 << (DIMENSION - 1)
FULL_MASK = (1 << DIMENSION) - 1


def projective_class(vertex: int) -> int:
    """Return the representative whose eighth bit is zero."""
    return vertex if vertex < CLASS_COUNT else vertex ^ FULL_MASK


def enumerate_cycles() -> tuple[tuple[int, ...], ...]:
    """Enumerate every distinct projective coordinate-flip cycle exactly."""
    cycle_masks: set[int] = set()
    for start in range(CLASS_COUNT):
        for order in itertools.permutations(range(DIMENSION)):
            vertex = start
            mask = 0
            for coordinate in order:
                mask |= 1 << projective_class(vertex)
                vertex ^= 1 << coordinate
            assert bin(mask).count("1") == DIMENSION
            cycle_masks.add(mask)

    cycles = tuple(
        tuple(index for index in range(CLASS_COUNT) if mask >> index & 1)
        for mask in sorted(cycle_masks)
    )
    assert len(cycles) == 322_560
    return cycles


def incidence(cycles: tuple[tuple[int, ...], ...]):
    rows = np.repeat(np.arange(len(cycles), dtype=np.int32), DIMENSION)
    columns = np.fromiter(
        (vertex for cycle in cycles for vertex in cycle),
        dtype=np.int32,
        count=len(cycles) * DIMENSION,
    )
    data = np.ones(len(rows), dtype=float)
    return coo_matrix(
        (data, (rows, columns)),
        shape=(len(cycles), CLASS_COUNT),
    ).tocsr()


def verify_hitting_set(
    selected: tuple[int, ...], cycles: tuple[tuple[int, ...], ...]
) -> None:
    selected_mask = sum(1 << vertex for vertex in selected)
    for cycle in cycles:
        assert any(selected_mask >> vertex & 1 for vertex in cycle), cycle


def solve_with_row_generation(
    cycles: tuple[tuple[int, ...], ...],
    target_size: int,
    seed: int,
    initial_cuts: int,
    cuts_per_round: int,
    time_limit: float,
    maximum_rounds: int,
) -> dict[str, object]:
    matrix = incidence(cycles)
    rng = np.random.default_rng(seed)
    active = set(
        int(value)
        for value in rng.choice(
            len(cycles), size=min(initial_cuts, len(cycles)), replace=False
        )
    )

    # Translation of the sign cube acts transitively on projective classes and
    # preserves all cycles.  Therefore some target-size hitting set exists if
    # and only if one exists that contains class zero.
    lower = np.zeros(CLASS_COUNT)
    upper = np.ones(CLASS_COUNT)
    lower[0] = 1.0
    bounds = Bounds(lower, upper)
    integrality = np.ones(CLASS_COUNT, dtype=np.int8)

    for round_index in range(1, maximum_rounds + 1):
        active_indices = np.array(sorted(active), dtype=np.int64)
        active_matrix = matrix[active_indices]
        total_row = coo_matrix(np.ones((1, CLASS_COUNT), dtype=float)).tocsr()
        constraint_matrix = vstack([active_matrix, total_row], format="csr")
        lower_bounds = np.concatenate(
            [np.ones(len(active_indices)), np.array([-np.inf])]
        )
        upper_bounds = np.concatenate(
            [np.full(len(active_indices), np.inf), np.array([target_size])]
        )

        # This is a pure feasibility problem.  A nonzero tie-breaking
        # objective can make HiGHS spend substantial time proving an
        # irrelevant optimum before returning a feasible target-size set.
        objective = np.zeros(CLASS_COUNT)
        result = milp(
            c=objective,
            integrality=integrality,
            bounds=bounds,
            constraints=LinearConstraint(
                constraint_matrix, lower_bounds, upper_bounds
            ),
            options={
                "time_limit": time_limit,
                "mip_rel_gap": 0.0,
                "presolve": True,
            },
        )

        print(
            f"round {round_index}: cuts={len(active)} "
            f"status={result.status} message={result.message}",
            flush=True,
        )
        if result.x is None:
            return {
                "status": "infeasible" if result.status == 2 else "no_solution",
                "solver_status": int(result.status),
                "solver_message": str(result.message),
                "round": round_index,
                "active_cuts": len(active),
            }

        selected = tuple(
            int(index) for index in np.flatnonzero(result.x > 0.5)
        )
        selected_mask = sum(1 << vertex for vertex in selected)
        uncovered = [
            index
            for index, cycle in enumerate(cycles)
            if not any(selected_mask >> vertex & 1 for vertex in cycle)
        ]
        print(
            f"round {round_index}: selected={len(selected)} "
            f"uncovered={len(uncovered)}",
            flush=True,
        )
        if not uncovered:
            verify_hitting_set(selected, cycles)
            return {
                "status": "verified_hitting_set",
                "round": round_index,
                "active_cuts": len(active),
                "selected_classes": list(selected),
            }

        if len(uncovered) <= cuts_per_round:
            active.update(uncovered)
        else:
            active.update(
                int(value)
                for value in rng.choice(
                    uncovered, size=cuts_per_round, replace=False
                )
            )

    return {
        "status": "round_limit",
        "round": maximum_rounds,
        "active_cuts": len(active),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--initial-cuts", type=int, default=4000)
    parser.add_argument("--cuts-per-round", type=int, default=4000)
    parser.add_argument("--time-limit", type=float, default=120.0)
    parser.add_argument("--maximum-rounds", type=int, default=40)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().with_suffix(".json"),
    )
    arguments = parser.parse_args()
    if not 1 <= arguments.target_size <= CLASS_COUNT:
        raise ValueError("target size must belong to [1, 128]")

    cycles = enumerate_cycles()
    print(f"distinct projective cycles: {len(cycles)}", flush=True)
    result = solve_with_row_generation(
        cycles=cycles,
        target_size=arguments.target_size,
        seed=arguments.seed,
        initial_cuts=arguments.initial_cuts,
        cuts_per_round=arguments.cuts_per_round,
        time_limit=arguments.time_limit,
        maximum_rounds=arguments.maximum_rounds,
    )
    payload = {
        "dimension": DIMENSION,
        "projective_classes": CLASS_COUNT,
        "distinct_projective_cycles": len(cycles),
        "target_size": arguments.target_size,
        "parameters": {
            "seed": arguments.seed,
            "initial_cuts": arguments.initial_cuts,
            "cuts_per_round": arguments.cuts_per_round,
            "time_limit": arguments.time_limit,
            "maximum_rounds": arguments.maximum_rounds,
        },
        "result": result,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)
    print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
