#!/usr/bin/env python3
"""Search degree-four multiplier cones on repaired support U plus 47.

The 55-point support is support54 together with code 47.  Restrictions of
degree-at-most-four Fourier polynomials to this support have codimension one,
with relation R(z) = parity(z) L(z).  By default this diagnostic uses the
uncleared tangent matrix W = s(1, z_i / B_h) and maximizes the common lower
bound on y subject to

    W.T y = 0, R.T y = 0, sum(y) = 1.

The ``--cleared`` option instead uses G = s(F, z_i F / B_h), where F is the
denominator product.  This imposes degree at most four on q = y / F and is a
different cone.  All optimization output is numerical evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import linprog, minimize

import verify_n6_parity_triple_support54_geometry as geometry


N = 6
HEADS = 4
WIDTH = N + 1
VERTICES = 1 << N
MASK = 0x96696BD669B69669
SUPPORT = np.array(
    sorted(
        (set(range(VERTICES)) - set(geometry.EXPECTED_OMITTED)) | {47}
    ),
    dtype=int,
)
HYPERPLANE_NORMAL = np.array(geometry.HYPERPLANE_NORMAL, dtype=float)
MINIMUM_WEIGHT = 1e-7
USE_CLEARED = False


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


Z = np.array(
    [
        [character(1 << coordinate, code) for coordinate in range(N)]
        for code in range(VERTICES)
    ],
    dtype=float,
)
SIGNS = np.array(
    [1.0 if (MASK >> code) & 1 else -1.0 for code in range(VERTICES)]
)
RELATIONS = np.array(
    [
        [
            character((1 << N) - 1, code)
            * float(HYPERPLANE_NORMAL @ Z[code])
            for code in SUPPORT
        ]
    ],
    dtype=float,
)


def use_symmetric_support() -> None:
    global SUPPORT, RELATIONS
    SUPPORT = np.array(
        sorted(
            (set(range(VERTICES)) - set(geometry.EXPECTED_OMITTED))
            | {16, 47}
        ),
        dtype=int,
    )
    relation_normals = (
        np.array((0, 0, 1, 1, 0, 0), dtype=float),
        np.array((2, 1, 1, 0, -1, 1), dtype=float),
    )
    RELATIONS = np.array(
        [
            [
                character((1 << N) - 1, code)
                * float(normal @ Z[code])
                for code in SUPPORT
            ]
            for normal in relation_normals
        ],
        dtype=float,
    )


def use_full_degree_five() -> None:
    """Use the full cube and the sole degree-five evaluation relation."""
    global SUPPORT, RELATIONS
    SUPPORT = np.arange(VERTICES, dtype=int)
    RELATIONS = np.array(
        [
            [
                character((1 << N) - 1, code)
                for code in SUPPORT
            ]
        ],
        dtype=float,
    )


def literal_matrix(orientation: int) -> np.ndarray:
    return np.column_stack(
        [np.ones(VERTICES), 1.0 + orientation * Z]
    )


def softmax(logits: np.ndarray) -> np.ndarray:
    centered = logits - np.max(logits, axis=1, keepdims=True)
    exponentials = np.exp(np.maximum(centered, -700.0))
    raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
    epsilon = MINIMUM_WEIGHT
    return (1.0 - WIDTH * epsilon) * raw + epsilon


def cleared_matrix(
    theta: np.ndarray, orientations: tuple[int, ...]
) -> tuple[np.ndarray, np.ndarray, tuple[np.ndarray, ...]]:
    literals = tuple(literal_matrix(value) for value in orientations)
    values = np.column_stack(
        [literals[head] @ theta[head] for head in range(HEADS)]
    )
    rows = []
    for code in SUPPORT:
        current = values[code]
        sign = SIGNS[code]
        if USE_CLEARED:
            product = float(np.prod(current))
            row = [sign * product]
            for head in range(HEADS):
                partial = float(
                    np.prod(
                        [
                            current[other]
                            for other in range(HEADS)
                            if other != head
                        ]
                    )
                )
                row.extend(sign * Z[code] * partial)
        else:
            row = [sign]
            for head in range(HEADS):
                row.extend(sign * Z[code] / current[head])
        rows.append(row)
    return np.array(rows, dtype=float), values, literals


def strict_margin(
    logits_flat: np.ndarray,
    orientations: tuple[int, ...],
    regularization: float = 0.0,
) -> tuple[float, np.ndarray, dict[str, object]]:
    logits = logits_flat.reshape(HEADS, WIDTH)
    theta = softmax(logits)
    matrix, values, literals = cleared_matrix(theta, orientations)
    column_scale = np.maximum(np.linalg.norm(matrix, axis=0), 1e-100)
    normalized = matrix / column_scale[None, :]
    relation_scale = np.maximum(
        np.linalg.norm(RELATIONS, axis=1), 1.0
    )

    row_count = len(SUPPORT)
    variable_count = row_count + 1
    objective = np.zeros(variable_count)
    objective[-1] = -1.0
    relation_count = RELATIONS.shape[0]
    equalities = np.zeros((25 + relation_count + 1, variable_count))
    equalities[:25, :row_count] = normalized.T
    equalities[
        25 : 25 + relation_count, :row_count
    ] = RELATIONS / relation_scale[:, None]
    equalities[-1, :row_count] = 1.0
    target = np.zeros(25 + relation_count + 1)
    target[-1] = 1.0
    inequalities = np.zeros((row_count, variable_count))
    inequalities[:, :row_count] = -np.eye(row_count)
    inequalities[:, -1] = 1.0
    result = linprog(
        objective,
        A_ub=inequalities,
        b_ub=np.zeros(row_count),
        A_eq=equalities,
        b_eq=target,
        bounds=[(None, None)] * variable_count,
        method="highs-ds",
    )
    if not result.success:
        result = linprog(
            objective,
            A_ub=inequalities,
            b_ub=np.zeros(row_count),
            A_eq=equalities,
            b_eq=target,
            bounds=[(None, None)] * variable_count,
            method="highs-ipm",
        )
    if not result.success:
        raise RuntimeError(result.message)

    weights = np.array(result.x[:row_count], dtype=float)
    tangent_dual = np.array(result.eqlin.marginals[:25]) / column_scale
    value_gradient = np.zeros_like(values)
    for local, code in enumerate(SUPPORT):
        current = values[code]
        sign_weight = SIGNS[code] * weights[local]
        for changed in range(HEADS):
            if USE_CLEARED:
                derivative = tangent_dual[0] * np.prod(
                    [
                        current[other]
                        for other in range(HEADS)
                        if other != changed
                    ]
                )
                for omitted in range(HEADS):
                    if omitted == changed:
                        continue
                    start = 1 + omitted * N
                    numerator = float(
                        tangent_dual[start : start + N] @ Z[code]
                    )
                    derivative += numerator * np.prod(
                        [
                            current[other]
                            for other in range(HEADS)
                            if other not in (omitted, changed)
                        ]
                    )
            else:
                start = 1 + changed * N
                numerator = float(
                    tangent_dual[start : start + N] @ Z[code]
                )
                derivative = -numerator / (current[changed] ** 2)
            value_gradient[code, changed] = sign_weight * derivative

    theta_gradient = np.zeros_like(theta)
    for head in range(HEADS):
        theta_gradient[head] = literals[head].T @ value_gradient[:, head]
    movable = theta - MINIMUM_WEIGHT
    raw = movable / (1.0 - WIDTH * MINIMUM_WEIGHT)
    logit_gradient = movable * (
        theta_gradient
        - np.sum(raw * theta_gradient, axis=1, keepdims=True)
    )
    centered = logits - np.mean(logits, axis=1, keepdims=True)
    margin = float(result.x[-1])
    loss = margin + 0.5 * regularization * float(np.sum(centered * centered))
    logit_gradient += regularization * centered
    diagnostics: dict[str, object] = {
        "margin": margin,
        "theta": theta,
        "weights": weights,
        "active": int(np.sum(weights <= margin + 1e-9)),
        "tangent_residual": float(np.linalg.norm(normalized.T @ weights)),
        "relation_residual": float(np.max(np.abs(RELATIONS @ weights))),
    }
    return loss, logit_gradient.ravel(), diagnostics


def denominator_logits(denominators: np.ndarray) -> tuple[np.ndarray, tuple[int, ...]]:
    orientations = []
    parameters = []
    for row in denominators:
        slopes = np.array(row[1:], dtype=float)
        nonzero_signs = np.sign(slopes[np.abs(slopes) > 1e-14])
        if len(nonzero_signs) == 0 or not np.all(nonzero_signs == nonzero_signs[0]):
            raise ValueError("each denominator must have one slope orientation")
        orientation = int(nonzero_signs[0])
        magnitudes = np.abs(slopes)
        slack = float(row[0] - np.sum(magnitudes))
        if slack <= 0:
            raise ValueError("denominator is not strictly admissible")
        current = np.concatenate([[slack], magnitudes])
        current /= np.sum(current)
        orientations.append(orientation)
        parameters.append(current)
    logits = np.log(np.array(parameters))
    logits -= np.mean(logits, axis=1, keepdims=True)
    return logits, tuple(orientations)


def finite_difference_check(seed: int) -> float:
    rng = np.random.default_rng(seed)
    orientations = (-1, -1, 1, 1)
    logits = rng.normal(scale=0.8, size=(HEADS, WIDTH))
    loss, gradient, _ = strict_margin(logits.ravel(), orientations)
    direction = rng.normal(size=logits.size)
    direction /= np.linalg.norm(direction)
    epsilon = 2e-5
    plus = strict_margin(
        logits.ravel() + epsilon * direction, orientations
    )[0]
    minus = strict_margin(
        logits.ravel() - epsilon * direction, orientations
    )[0]
    numerical = (plus - minus) / (2.0 * epsilon)
    analytic = float(gradient @ direction)
    return abs(numerical - analytic) / max(
        1.0, abs(loss), abs(numerical), abs(analytic)
    )


def sample_denominators(
    rng: np.random.Generator, positive_heads: int, log_span: float
) -> np.ndarray:
    orientations = [-1] * (HEADS - positive_heads) + [1] * positive_heads
    rows = []
    for orientation in orientations:
        slopes = np.exp(rng.uniform(-log_span, log_span, size=N))
        slack = float(np.exp(rng.uniform(-log_span, log_span)))
        rows.append(
            np.concatenate([[np.sum(slopes) + slack], orientation * slopes])
        )
    return np.vstack(rows)


def main() -> None:
    global MINIMUM_WEIGHT, USE_CLEARED
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=30)
    parser.add_argument("--log-span", type=float, default=8.0)
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--search", action="store_true")
    parser.add_argument("--symmetric", action="store_true")
    parser.add_argument("--full-degree-five", action="store_true")
    parser.add_argument("--floor", type=float, default=1e-7)
    parser.add_argument("--cleared", action="store_true")
    args = parser.parse_args()

    if args.floor < 0 or WIDTH * args.floor >= 1:
        raise ValueError("floor must lie in [0, 1/7)")
    MINIMUM_WEIGHT = args.floor
    USE_CLEARED = args.cleared

    if args.symmetric and args.full_degree_five:
        raise ValueError("choose at most one support mode")
    if args.symmetric:
        use_symmetric_support()
    if args.full_degree_five:
        use_full_degree_five()

    print(f"tangent convention: {'cleared-q' if USE_CLEARED else 'uncleared-y'}")

    print(f"finite-difference relative error: {finite_difference_check(args.seed):.3e}")
    rng = np.random.default_rng(args.seed)
    bank = []
    for positive_heads in range(3):
        for sample in range(args.samples):
            span = args.log_span * (0.2 + 0.8 * (sample + 1) / args.samples)
            bank.append(sample_denominators(rng, positive_heads, span))

    records = []
    for index, denominators in enumerate(bank):
        logits, orientations = denominator_logits(denominators)
        _, _, diagnostics = strict_margin(logits.ravel(), orientations)
        records.append((float(diagnostics["margin"]), index, logits, orientations))
    records.sort(key=lambda item: item[0])
    print(
        f"sampled margins: min={records[0][0]:.12g} "
        f"median={records[len(records) // 2][0]:.12g} "
        f"max={records[-1][0]:.12g}"
    )

    if not args.search:
        return
    starts = records[: min(args.restarts, len(records))]
    best = (float("inf"), None)
    for restart, (_, _, logits, orientations) in enumerate(starts):
        regularization = 10 ** rng.uniform(-12.0, -8.0)

        def objective(current: np.ndarray) -> tuple[float, np.ndarray]:
            return strict_margin(current, orientations, regularization)[:2]

        result = minimize(
            objective,
            logits.ravel(),
            jac=True,
            method="L-BFGS-B",
            bounds=[(-24.0, 24.0)] * (HEADS * WIDTH),
            options={
                "maxiter": args.iterations,
                "maxfun": 8 * args.iterations,
                "ftol": 1e-14,
                "gtol": 1e-9,
                "maxls": 40,
            },
        )
        _, _, diagnostics = strict_margin(result.x, orientations)
        margin = float(diagnostics["margin"])
        if margin < best[0]:
            best = (margin, np.array(diagnostics["theta"]))
        print(
            f"restart={restart} orientations={orientations} "
            f"margin={margin:.12g} active={diagnostics['active']} "
            f"success={result.success}",
            flush=True,
        )
    print(f"best margin={best[0]:.12g}")
    print(f"best theta={best[1].tolist() if best[1] is not None else None}")


if __name__ == "__main__":
    main()
