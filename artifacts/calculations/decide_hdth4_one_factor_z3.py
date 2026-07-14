#!/usr/bin/env python3
"""Exact QF_NRA decision problem for a one-factor HDTH_4 certificate.

This is an exploratory exact solver, not a standalone impossibility
certificate.  A satisfiable result is independently checkable after rational
reconstruction.  An unknown result says nothing.  An unsatisfiable result
would still need a durable proof artifact before being used in a lemma.

The one-admissible-factor form is

    Q = A D + C B,

where A, C, and D are arbitrary affine forms and B has strictly positive
coefficients.  Such a form is equivalent to a genuine two-head score: for a
large enough k, both B and D + k B are admissible denominators, and

    A D + C B = A (D + k B) + (C - k A) B.

HDTH_4 is invariant under complementing all eight input bits, so a
negative-orientation denominator reduces to the positive-orientation case.
The gauges sum(B_i) = 1, D_0 = 0, D_1 = 1, and A_0 = 0 lose no non-LTF
solution.  Coordinate-pair symmetries move any nonzero slope of D to D_1.
"""

from __future__ import annotations

import argparse
import sys

import z3


DIMENSION = 8


def vertex(code: int) -> tuple[int, ...]:
    return tuple((code >> coordinate) & 1 for coordinate in range(DIMENSION))


def target_sign(point: tuple[int, ...]) -> int:
    distance = sum(point[index] != point[4 + index] for index in range(4))
    return 1 if distance >= 2 else -1


def affine_value(coefficients: list[z3.ArithRef], point: tuple[int, ...]):
    return coefficients[0] + sum(
        coefficient * bit
        for coefficient, bit in zip(coefficients[1:], point)
    )


def build_solver(timeout_milliseconds: int, vertex_limit: int):
    b = [z3.Real(f"b_{index}") for index in range(DIMENSION + 1)]
    d = [z3.Real(f"d_{index}") for index in range(DIMENSION + 1)]
    a = [z3.Real(f"a_{index}") for index in range(DIMENSION + 1)]
    c = [z3.Real(f"c_{index}") for index in range(DIMENSION + 1)]

    solver = z3.SolverFor("QF_NRA")
    if timeout_milliseconds > 0:
        solver.set(timeout=timeout_milliseconds)

    solver.add(sum(b) == 1)
    solver.add(*(coefficient > 0 for coefficient in b))
    solver.add(d[0] == 0)
    solver.add(d[1] == 1)
    solver.add(a[0] == 0)

    points = [vertex(code) for code in range(1 << DIMENSION)]
    for point in points[:vertex_limit]:
        score = (
            affine_value(a, point) * affine_value(d, point)
            + affine_value(c, point) * affine_value(b, point)
        )
        solver.add(target_sign(point) * score >= 1)

    return solver, (a, d, c, b)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--vertex-limit", type=int, default=1 << DIMENSION)
    arguments = parser.parse_args()
    if not 1 <= arguments.vertex_limit <= 1 << DIMENSION:
        raise ValueError("vertex limit must belong to [1, 256]")

    solver, factors = build_solver(
        1000 * arguments.timeout_seconds,
        arguments.vertex_limit,
    )
    result = solver.check()
    print(f"vertices: {arguments.vertex_limit}")
    print(f"result: {result}")
    if result == z3.sat:
        model = solver.model()
        for name, coefficients in zip(("A", "D", "C", "B"), factors):
            print(name, tuple(model.eval(value, model_completion=True) for value in coefficients))
    elif result == z3.unknown:
        print(f"reason: {solver.reason_unknown()}")
        sys.exit(2)


if __name__ == "__main__":
    main()
