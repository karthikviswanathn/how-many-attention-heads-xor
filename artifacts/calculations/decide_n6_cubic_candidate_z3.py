#!/usr/bin/env python3
"""Exact QF_NRA decision problem for the hard six-bit cubic candidate.

This is an exploratory solver, not a durable lower-bound certificate.  A
satisfiable result must be reconstructed and checked as an exact three-head
score.  An unknown result says nothing.  An unsatisfiable result should be
converted into a standalone proof artifact before it is cited as a theorem.

For fixed denominator orientations, the cleared three-head score is

    A1 B2 B3 + A2 B1 B3 + A3 B1 B2.

Each denominator is normalized in its positive literal basis.  Head
permutation reduces the eight orientation tuples to four representatives.
"""

from __future__ import annotations

import argparse
import sys

import z3


DIMENSION = 6
HEADS = 3
TRUTH_MASK = 0x20411408412A1432
ORIENTATION_REPRESENTATIVES = (
    (-1, -1, -1),
    (-1, -1, 1),
    (-1, 1, 1),
    (1, 1, 1),
)


def vertex(code: int) -> tuple[int, ...]:
    return tuple((code >> coordinate) & 1 for coordinate in range(DIMENSION))


def target_sign(code: int) -> int:
    return 1 if (TRUTH_MASK >> code) & 1 else -1


def affine_value(coefficients: list[z3.ArithRef], point: tuple[int, ...]):
    return coefficients[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(coefficients[1:], point)
    )


def denominator_value(
    weights: list[z3.ArithRef],
    orientation: int,
    point: tuple[int, ...],
):
    literals = point if orientation > 0 else tuple(1 - bit for bit in point)
    return weights[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(weights[1:], literals)
    )


def build_solver(
    orientations: tuple[int, int, int],
    timeout_milliseconds: int,
    vertex_limit: int,
):
    numerators = [
        [z3.Real(f"a_{head}_{index}") for index in range(DIMENSION + 1)]
        for head in range(HEADS)
    ]
    denominator_weights = [
        [z3.Real(f"b_{head}_{index}") for index in range(DIMENSION + 1)]
        for head in range(HEADS)
    ]

    solver = z3.SolverFor("QF_NRA")
    if timeout_milliseconds > 0:
        solver.set(timeout=timeout_milliseconds)

    for weights in denominator_weights:
        solver.add(sum(weights) == 1)
        solver.add(*(coefficient > 0 for coefficient in weights))

    # Adding a multiple of B_h to A_h adds a constant to the h-th ratio.
    # Move the constants of heads 2 and 3 into head 1.
    solver.add(numerators[1][0] == 0)
    solver.add(numerators[2][0] == 0)

    for code in range(vertex_limit):
        point = vertex(code)
        numerator_values = [
            affine_value(numerators[head], point) for head in range(HEADS)
        ]
        denominator_values = [
            denominator_value(
                denominator_weights[head], orientations[head], point
            )
            for head in range(HEADS)
        ]
        cleared_score = sum(
            numerator_values[head]
            * denominator_values[(head + 1) % HEADS]
            * denominator_values[(head + 2) % HEADS]
            for head in range(HEADS)
        )
        solver.add(target_sign(code) * cleared_score >= 1)

    return solver, (numerators, denominator_weights)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--vertex-limit", type=int, default=1 << DIMENSION)
    parser.add_argument("--orientation-index", type=int, choices=range(4))
    arguments = parser.parse_args()
    if not 1 <= arguments.vertex_limit <= 1 << DIMENSION:
        raise ValueError("vertex limit must belong to [1, 64]")

    if arguments.orientation_index is None:
        orientation_indices = range(len(ORIENTATION_REPRESENTATIVES))
    else:
        orientation_indices = (arguments.orientation_index,)

    saw_unknown = False
    for orientation_index in orientation_indices:
        orientations = ORIENTATION_REPRESENTATIVES[orientation_index]
        solver, variables = build_solver(
            orientations,
            1000 * arguments.timeout_seconds,
            arguments.vertex_limit,
        )
        result = solver.check()
        print(f"orientations: {orientations}")
        print(f"vertices: {arguments.vertex_limit}")
        print(f"result: {result}")
        if result == z3.sat:
            model = solver.model()
            numerators, denominator_weights = variables
            for head in range(HEADS):
                print(
                    f"A{head + 1}",
                    tuple(
                        model.eval(value, model_completion=True)
                        for value in numerators[head]
                    ),
                )
                print(
                    f"B{head + 1}",
                    tuple(
                        model.eval(value, model_completion=True)
                        for value in denominator_weights[head]
                    ),
                )
            return
        if result == z3.unknown:
            saw_unknown = True
            print(f"reason: {solver.reason_unknown()}")

    if saw_unknown:
        sys.exit(2)


if __name__ == "__main__":
    main()
