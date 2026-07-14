#!/usr/bin/env python3
"""Search the two interior six-bit parity-single-flip orbits at five heads.

The representatives flip vertices 000011 and 000111.  Both have exact
threshold degree five.  For five heads there are only six orientation types,
up to permutation of the heads.  This script searches every type.  Every
optimized denominator tuple is tested by a fixed-denominator linear program,
regardless of the accuracy of the jointly optimized smooth numerators.  Any
success is rounded and verified with integer arithmetic.

For each best failed tuple, the script also extracts an exact positive Gordan
circuit.  Such a circuit proves failure for that fixed tuple only.  Neither a
finite search nor these fixed-tuple circuits prove a global five-head lower
bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize
from scipy.special import expit

import verify_n6_parity_single_flip_candidates as exact


N = 6
HEADS = 5
WIDTH = N + 1
VERTICES = 1 << N
HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n6_parity_single_flip_h5_search.json"
ORIENTATION_COUNTS = (2, 3, 1, 4, 0, 5)


def cube() -> np.ndarray:
    return ((np.arange(VERTICES)[:, None] >> np.arange(N)) & 1).astype(
        np.int64
    )


def affine_matrix(dtype: type = np.int64) -> np.ndarray:
    return np.column_stack([np.ones(VERTICES, dtype=np.int64), cube()]).astype(
        dtype
    )


def target_signs(flipped: int) -> np.ndarray:
    return np.array(
        [exact.target_sign(code, flipped) for code in range(VERTICES)],
        dtype=np.int64,
    )


def valid_denominators(denominators: np.ndarray) -> bool:
    values = affine_matrix(object) @ denominators.astype(object).T
    if denominators.shape != (HEADS, WIDTH) or not np.all(values > 0):
        return False
    return all(
        np.all(row[1:] > 0) or np.all(row[1:] < 0)
        for row in denominators
    )


def ratio_features(denominators: np.ndarray) -> np.ndarray:
    affine = affine_matrix(float)
    values = affine @ denominators.astype(float).T
    assert np.all(values > 0)
    return np.column_stack(
        [np.ones(VERTICES)]
        + [affine / values[:, head, None] for head in range(HEADS)]
    )


def cleared_matrix(denominators: np.ndarray) -> np.ndarray:
    affine = affine_matrix(object)
    values = affine @ denominators.astype(object).T
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(HEADS):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(WIDTH)
        )
    return np.column_stack(columns).astype(object)


def floating_cleared_matrix(denominators: np.ndarray) -> np.ndarray:
    """Return a safely rescaled cleared matrix with the same column span."""
    affine = affine_matrix(float)
    scaled = denominators.astype(float)
    scaled /= np.max(np.abs(scaled), axis=1, keepdims=True)
    values = affine @ scaled.T
    assert np.all(values > 0)
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(HEADS):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(WIDTH)
        )
    return np.column_stack(columns)


def floating_fixed_margin(
    signs: np.ndarray, denominators: np.ndarray
) -> float:
    """LP-test a tuple after harmless row and column rescaling."""
    if not valid_denominators(denominators):
        return float("-inf")
    matrix = floating_cleared_matrix(denominators)
    norms = np.linalg.norm(matrix, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = matrix[:, keep] / norms[keep]
    variables = normalized.shape[1]
    constraints = np.zeros((VERTICES, variables + 1))
    constraints[:, :variables] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(VERTICES),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
        options={"time_limit": 0.2},
    )
    if not result.success:
        return float("-inf")
    return -float(result.fun)


@lru_cache(maxsize=None)
def signed_reoriented_fourier_matrix(flipped: int) -> np.ndarray:
    """Map cube values to the 63 forced proper coefficient signs."""
    inputs = cube()
    sign_coordinates = 1 - 2 * inputs
    exceptional = np.array(
        [1 - 2 * ((flipped >> coordinate) & 1) for coordinate in range(N)],
        dtype=np.int64,
    )
    reoriented = sign_coordinates * exceptional
    common_sign = -int(np.prod(exceptional))
    rows = []
    for size in range(N + 1):
        for subset in itertools.combinations(range(N), size):
            if size == N:
                continue
            if subset:
                character_values = np.prod(reoriented[:, subset], axis=1)
            else:
                character_values = np.ones(VERTICES, dtype=np.int64)
            rows.append(common_sign * character_values / VERTICES)
    return np.array(rows, dtype=float)


@lru_cache(maxsize=None)
def weighted_cut_matrix(flipped: int) -> np.ndarray:
    """Map the 63 nonexceptional margins to shifted Fourier magnitudes.

    Rows use the same proper-subset order as
    ``signed_reoriented_fourier_matrix``.  The row for a proper subset S is
    the weighted cut indexed by its nonempty complement T.  Columns are the
    vertices other than ``flipped``, in increasing code order.
    """
    nonexceptional = [
        code for code in range(VERTICES) if code != flipped
    ]
    rows = []
    full = VERTICES - 1
    for size in range(N + 1):
        for subset in itertools.combinations(range(N), size):
            if size == N:
                continue
            subset_mask = sum(1 << coordinate for coordinate in subset)
            cut_mask = full ^ subset_mask
            rows.append(
                [
                    (
                        1.0 / 32.0
                        if bin((code ^ flipped) & cut_mask).count("1") % 2
                        else 0.0
                    )
                    for code in nonexceptional
                ]
            )
    matrix = np.array(rows, dtype=float)

    # The canonical degree-five polynomial has margin 1 away from the
    # exceptional vertex.  Both sides of the weighted-cut identity are then
    # the all-ones vector, which also checks the row ordering and signs.
    canonical_values = np.array(
        [
            exact.explicit_degree_five_value(code, flipped)
            for code in range(VERTICES)
        ],
        dtype=float,
    )
    fourier_magnitudes = (
        signed_reoriented_fourier_matrix(flipped) @ canonical_values
    )
    assert np.allclose(fourier_magnitudes, matrix @ np.ones(VERTICES - 1))
    assert np.allclose(fourier_magnitudes, np.ones(VERTICES - 1))
    return matrix


def cut_cone_projection(
    flipped: int,
    theta: np.ndarray,
    orientations: tuple[int, ...],
    minimum_margin: float = 0.0,
) -> dict[str, object] | None:
    """Project a fixed tangent space toward the exact weighted-cut cone.

    The coefficient-orthant condition is only necessary.  The full target
    signs require the shifted coefficient magnitudes to equal a positive
    weighted cut.  With the 63 nonexceptional margins normalized to sum to
    one, this LP minimizes the L1 residual from the closed cut cone.  A zero
    residual only shows contact with its boundary unless all margins are
    positive.  A positive residual still gives a graded, target-aware
    numerator seed.  The direct sign LP remains the certificate gate.
    """
    denominators = np.vstack(
        [
            theta[head]
            if orientations[head] > 0
            else np.concatenate(
                [[np.sum(theta[head])], -theta[head, 1:]]
            )
            for head in range(HEADS)
        ]
    )
    coefficient_matrix = (
        signed_reoriented_fourier_matrix(flipped)
        @ floating_cleared_matrix(denominators)
    )
    norms = np.linalg.norm(coefficient_matrix, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = coefficient_matrix[:, keep] / norms[keep]
    coefficient_variables = normalized.shape[1]
    cut = weighted_cut_matrix(flipped)
    margin_variables = VERTICES - 1
    residual_variables = VERTICES - 1
    variables = (
        coefficient_variables + margin_variables + residual_variables
    )
    coefficient_slice = slice(0, coefficient_variables)
    margin_slice = slice(
        coefficient_variables,
        coefficient_variables + margin_variables,
    )
    residual_slice = slice(
        coefficient_variables + margin_variables,
        variables,
    )

    constraints = np.zeros((2 * (VERTICES - 1), variables))
    constraints[: VERTICES - 1, coefficient_slice] = normalized
    constraints[: VERTICES - 1, margin_slice] = -cut
    constraints[: VERTICES - 1, residual_slice] = -np.eye(
        residual_variables
    )
    constraints[VERTICES - 1 :, coefficient_slice] = -normalized
    constraints[VERTICES - 1 :, margin_slice] = cut
    constraints[VERTICES - 1 :, residual_slice] = -np.eye(
        residual_variables
    )
    equality = np.zeros((1, variables))
    equality[0, margin_slice] = 1.0
    objective = np.zeros(variables)
    objective[residual_slice] = 1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(2 * (VERTICES - 1)),
        A_eq=equality,
        b_eq=np.ones(1),
        bounds=(
            [(None, None)] * coefficient_variables
            + [(minimum_margin, None)] * margin_variables
            + [(0.0, None)] * residual_variables
        ),
        method="highs",
        options={"time_limit": 0.2},
    )
    if not result.success:
        return None
    coefficients = np.zeros(1 + HEADS * WIDTH)
    coefficients[keep] = result.x[coefficient_slice] / norms[keep]
    return {
        "denominators": denominators,
        "coefficients": coefficients,
        "normalized_margins": result.x[margin_slice],
        "l1_residual": float(result.fun),
    }


def cut_cone_numerator_initialization(
    flipped: int,
    theta: np.ndarray,
    orientations: tuple[int, ...],
) -> tuple[np.ndarray, float] | None:
    projection = cut_cone_projection(flipped, theta, orientations)
    if projection is None:
        return None
    denominators = np.array(projection["denominators"], dtype=float)
    coefficients = np.array(projection["coefficients"], dtype=float)
    numerators = coefficients[1:].reshape(HEADS, WIDTH)
    row_scales = np.max(np.abs(denominators), axis=1)
    numerators *= row_scales[:, None]
    numerators[0] += coefficients[0] * denominators[0]

    affine = affine_matrix(float)
    values = affine @ denominators.T
    score = np.sum((affine @ numerators.T) / values, axis=1)
    scale = max(1e-8, float(np.sqrt(np.mean(score * score))))
    return numerators / scale, float(projection["l1_residual"])


def cut_cone_dual_separation(
    flipped: int,
    theta: np.ndarray,
    orientations: tuple[int, ...],
    minimum_margin: float = 0.0,
) -> dict[str, object] | None:
    """Return a Fourier functional separating a fixed tangent from cuts.

    For the proper-coefficient matrix B and cut-generator matrix C, the dual
    searches for y with B^T y=0, |y| at most one, and C^T y at least delta.
    A positive delta proves that this fixed tangent space misses even the
    closed nonzero cut cone.  The functional is numerical and applies only to
    this denominator tuple.
    """
    denominators = np.vstack(
        [
            theta[head]
            if orientations[head] > 0
            else np.concatenate(
                [[np.sum(theta[head])], -theta[head, 1:]]
            )
            for head in range(HEADS)
        ]
    )
    coefficient_matrix = (
        signed_reoriented_fourier_matrix(flipped)
        @ floating_cleared_matrix(denominators)
    )
    norms = np.linalg.norm(coefficient_matrix, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = coefficient_matrix[:, keep] / norms[keep]
    cut = weighted_cut_matrix(flipped)

    variables = (VERTICES - 1) + 1
    constraints = np.zeros((VERTICES - 1, variables))
    constraints[:, : VERTICES - 1] = -cut.T
    constraints[:, -1] = 1.0
    equality = np.zeros((normalized.shape[1], variables))
    equality[:, : VERTICES - 1] = normalized.T
    if not 0.0 <= minimum_margin < 1.0 / (VERTICES - 1):
        raise ValueError("minimum margin is outside the normalized simplex")
    objective = np.zeros(variables)
    objective[: VERTICES - 1] = -minimum_margin
    objective[-1] = -(1.0 - (VERTICES - 1) * minimum_margin)
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(VERTICES - 1),
        A_eq=equality,
        b_eq=np.zeros(normalized.shape[1]),
        bounds=[(-1.0, 1.0)] * (VERTICES - 1) + [(None, None)],
        method="highs",
        options={"time_limit": 0.2},
    )
    if not result.success:
        return None
    functional = result.x[: VERTICES - 1]
    generator_values = cut.T @ functional
    annihilator_residual = float(
        np.max(np.abs(normalized.T @ functional))
    )
    return {
        "separation_margin": -float(result.fun),
        "minimum_cut_generator_value": float(np.min(generator_values)),
        "maximum_cut_generator_value": float(np.max(generator_values)),
        "annihilator_residual": annihilator_residual,
        "proper_fourier_functional": functional.tolist(),
        "cut_generator_values": generator_values.tolist(),
    }


def cut_cone_residual_gradient(
    flipped: int,
    logits: np.ndarray,
    orientations: tuple[int, ...],
    minimum_margin: float = 0.0,
) -> tuple[float, np.ndarray, dict[str, object]]:
    """Differentiate the fixed-space cut distance with an LP subgradient.

    The primal supplies a closest tangent polynomial and the dual supplies a
    Fourier functional annihilating the tangent space.  The envelope theorem
    then differentiates only the cleared polynomial with the primal
    coefficients held fixed.  Column and denominator rescalings are changes
    of tangent-space coordinates, so the calculation converts back to the
    unscaled denominator basis first.
    """
    theta = softmax(logits.reshape(HEADS, WIDTH))
    projection = cut_cone_projection(
        flipped, theta, orientations, minimum_margin
    )
    dual = cut_cone_dual_separation(
        flipped, theta, orientations, minimum_margin
    )
    if projection is None or dual is None:
        return 10.0, np.zeros_like(logits), {"lp_failure": True}

    residual = float(projection["l1_residual"])
    dual_residual = float(dual["separation_margin"])
    denominators = np.array(projection["denominators"], dtype=float)
    coefficients = np.array(projection["coefficients"], dtype=float)
    row_scales = np.max(np.abs(denominators), axis=1)
    scale_product = float(np.prod(row_scales))
    raw_constant = coefficients[0] / scale_product
    raw_numerators = coefficients[1:].reshape(HEADS, WIDTH).copy()
    for head in range(HEADS):
        raw_numerators[head] /= scale_product / row_scales[head]

    affine = affine_matrix(float)
    denominator_values = affine @ denominators.T
    numerator_values = affine @ raw_numerators.T
    functional = np.array(
        dual["proper_fourier_functional"], dtype=float
    )
    value_functional = (
        signed_reoriented_fourier_matrix(flipped).T @ functional
    )
    theta_gradient = np.zeros((HEADS, WIDTH))
    inputs = cube().astype(float)
    literals = [
        literal_matrix(inputs, orientation)
        for orientation in orientations
    ]
    for differentiated_head in range(HEADS):
        other_product = np.prod(
            np.delete(denominator_values, differentiated_head, axis=1),
            axis=1,
        )
        derivative_values = raw_constant * other_product
        for numerator_head in range(HEADS):
            if numerator_head == differentiated_head:
                continue
            remaining = np.prod(
                np.delete(
                    denominator_values,
                    [differentiated_head, numerator_head],
                    axis=1,
                ),
                axis=1,
            )
            derivative_values += (
                numerator_values[:, numerator_head] * remaining
            )
        # The explicit dual uses the opposite sign from the L1 residual
        # subgradient, since its cut-generator values are positive.
        theta_gradient[differentiated_head] = -(
            literals[differentiated_head].T
            @ (value_functional * derivative_values)
        )
    logit_gradient = theta * (
        theta_gradient
        - np.sum(theta * theta_gradient, axis=1, keepdims=True)
    )
    diagnostics = {
        "dual_residual": dual_residual,
        "primal_dual_gap": residual - dual_residual,
        "annihilator_residual": dual["annihilator_residual"],
    }
    return residual, logit_gradient.ravel(), diagnostics


def exact_head_certificate(
    signs: np.ndarray, denominators: np.ndarray
) -> dict[str, object] | None:
    if floating_fixed_margin(signs, denominators) <= 1e-11:
        return None
    matrix = cleared_matrix(denominators)
    floating_matrix = np.array(matrix, dtype=float)
    norms = np.linalg.norm(floating_matrix, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = floating_matrix[:, keep] / norms[keep]
    variables = normalized.shape[1]
    constraints = np.zeros((VERTICES, variables + 1))
    constraints[:, :variables] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(VERTICES),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
        options={"time_limit": 1.0},
    )
    if not result.success or -float(result.fun) <= 1e-13:
        return None

    floating = np.zeros(floating_matrix.shape[1])
    floating[keep] = result.x[:variables] / norms[keep]
    floating_margin = float(np.min(signs * (floating_matrix @ floating)))
    if floating_margin <= 1e-13:
        return None
    row_norm = max(
        sum(abs(int(value)) for value in row) for row in matrix.tolist()
    )
    scale = max(1, int(math.ceil((row_norm + 1) / (2 * floating_margin))))
    signs_object = signs.astype(object)
    for _ in range(180):
        coefficients = np.array(
            [int(round(scale * value)) for value in floating], dtype=object
        )
        signed = signs_object * (matrix @ coefficients)
        if min(signed) > 0:
            return {
                "denominators": denominators.tolist(),
                "score_coefficients": [int(value) for value in coefficients],
                "minimum_signed_cleared_score": int(min(signed)),
                "floating_normalized_cleared_margin": floating_margin,
            }
        scale *= 2
    return None


def verify_head_certificate(
    flipped: int, certificate: dict[str, object]
) -> int:
    denominators = np.array(certificate["denominators"], dtype=object)
    assert valid_denominators(denominators)
    coefficients = np.array(certificate["score_coefficients"], dtype=object)
    assert len(coefficients) == 1 + HEADS * WIDTH
    signs = target_signs(flipped).astype(object)
    signed = signs * (cleared_matrix(denominators) @ coefficients)
    minimum = int(min(signed))
    assert minimum > 0
    assert minimum == int(certificate["minimum_signed_cleared_score"])
    return minimum


def literal_matrix(inputs: np.ndarray, orientation: int) -> np.ndarray:
    literals = inputs if orientation > 0 else 1.0 - inputs
    return np.column_stack([np.ones(VERTICES), literals])


def softmax(rows: np.ndarray) -> np.ndarray:
    shifted = rows - np.max(rows, axis=1, keepdims=True)
    exponentials = np.exp(np.maximum(shifted, -700.0))
    raw = exponentials / np.sum(exponentials, axis=1, keepdims=True)
    epsilon = 1e-12
    return (1.0 - WIDTH * epsilon) * raw + epsilon


def oriented_integer_denominator(
    literal_weights: np.ndarray, orientation: int
) -> np.ndarray:
    weights = [max(1, int(value)) for value in literal_weights]
    if orientation > 0:
        return np.array(weights, dtype=np.int64)
    return np.array(
        [sum(weights)] + [-value for value in weights[1:]],
        dtype=np.int64,
    )


def literal_weights_from_denominator(
    denominator: tuple[int, ...]
) -> tuple[int, np.ndarray]:
    slopes = denominator[1:]
    if all(value > 0 for value in slopes):
        return 1, np.array(denominator, dtype=float)
    assert all(value < 0 for value in slopes)
    intercept = denominator[0] + sum(slopes)
    return -1, np.array([intercept] + [-value for value in slopes], dtype=float)


def template_logits(orientations: tuple[int, ...]) -> np.ndarray | None:
    templates = []
    for denominator in exact.ADJACENT_DENOMINATORS:
        orientation, weights = literal_weights_from_denominator(denominator)
        templates.append((orientation, weights))
    rows = []
    unused = list(templates)
    for orientation in orientations:
        selected = next(
            (index for index, item in enumerate(unused) if item[0] == orientation),
            None,
        )
        if selected is None:
            return None
        _, weights = unused.pop(selected)
        rows.append(np.log(weights / np.sum(weights)))
    return np.vstack(rows)


def search_orientation(
    flipped: int,
    signs: np.ndarray,
    positive_heads: int,
    seed: int,
    restarts: int,
    max_iterations: int,
    scales: tuple[int, ...],
) -> tuple[dict[str, object] | None, dict[str, object]]:
    orientations = tuple([-1] * (HEADS - positive_heads) + [1] * positive_heads)
    inputs = cube().astype(float)
    affine = affine_matrix(float)
    literals = [literal_matrix(inputs, value) for value in orientations]
    template = template_logits(orientations)
    rng = np.random.default_rng(seed)
    best_accuracy = -1
    best_minimum = float("-inf")
    best: dict[str, object] = {}

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
        if template is not None and restart % 8 == 0:
            logits = template + rng.normal(scale=1.0, size=(HEADS, WIDTH))
        else:
            logit_scale = float(rng.choice((2.0, 4.0, 7.0, 11.0)))
            logits = rng.normal(scale=logit_scale, size=(HEADS, WIDTH))
        theta_initial = softmax(logits)
        cut_cone_initial = None
        if restart % 2 == 0:
            cut_cone_initial = cut_cone_numerator_initialization(
                flipped, theta_initial, orientations
            )
        if cut_cone_initial is None:
            numerators = rng.normal(scale=0.7, size=HEADS * WIDTH)
            cut_cone_residual = None
        else:
            initial_numerators, cut_cone_residual = cut_cone_initial
            numerators = (
                initial_numerators
                + rng.normal(scale=0.03, size=(HEADS, WIDTH))
            ).ravel()
        variables = np.concatenate([numerators, logits.ravel()])
        regularization = 10 ** rng.uniform(-13.0, -6.0)
        result = minimize(
            lambda current: objective_gradient(current, regularization),
            variables,
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": max_iterations,
                "maxfun": 5 * max_iterations,
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
            dual_separation = cut_cone_dual_separation(
                flipped, theta, orientations
            )
            best = {
                "positive_heads": positive_heads,
                "orientations": list(orientations),
                "restart": restart,
                "accuracy": accuracy,
                "minimum_signed_smooth_score": minimum,
                "literal_weights": theta.tolist(),
                "wrong_vertices": [
                    int(index) for index in np.flatnonzero(signed <= 1e-8)
                ],
                "cut_cone_initial_l1_residual": cut_cone_residual,
                "cut_cone_dual_separation": dual_separation,
            }
            print(
                f"positive_heads={positive_heads} restart={restart} "
                f"accuracy={accuracy}/{VERTICES} minimum={minimum}",
                flush=True,
            )

        # This LP screen is intentionally unconditional.  The optimized
        # numerators can miss rows even when the denominators support the cell.
        for scale in scales:
            denominators = np.vstack(
                [
                    oriented_integer_denominator(
                        np.maximum(1, np.rint(scale * theta[head])),
                        orientations[head],
                    )
                    for head in range(HEADS)
                ]
            )
            certificate = exact_head_certificate(signs, denominators)
            if certificate is not None:
                certificate["positive_heads"] = positive_heads
                certificate["continuous_restart"] = restart
                certificate["rounding_scale"] = scale
                certificate["seed"] = seed
                return certificate, best
    return None, best


def random_denominator_tuple(
    rng: np.random.Generator, positive_heads: int
) -> np.ndarray:
    orientations = [-1] * (HEADS - positive_heads) + [1] * positive_heads
    rows = []
    for orientation in orientations:
        weights = np.maximum(
            1, np.rint(np.exp(rng.uniform(0.0, 16.0, size=WIDTH)))
        ).astype(np.int64)
        rows.append(oriented_integer_denominator(weights, orientation))
    return np.vstack(rows)


def random_fixed_screen(
    unresolved: dict[int, np.ndarray],
    trials: int,
    seed: int,
) -> tuple[dict[int, dict[str, object]], dict[int, int]]:
    rng = np.random.default_rng(seed)
    found: dict[int, dict[str, object]] = {}
    tested = {flipped: 0 for flipped in unresolved}
    for trial in range(trials):
        positive_heads = ORIENTATION_COUNTS[trial % len(ORIENTATION_COUNTS)]
        denominators = random_denominator_tuple(rng, positive_heads)
        for flipped, signs in unresolved.items():
            if flipped in found:
                continue
            tested[flipped] += 1
            certificate = exact_head_certificate(signs, denominators)
            if certificate is not None:
                certificate["positive_heads"] = positive_heads
                certificate["random_trial"] = trial
                certificate["seed"] = seed
                found[flipped] = certificate
        if len(found) == len(unresolved):
            break
        if (trial + 1) % 2000 == 0:
            print(f"random fixed tuples tested: {trial + 1}", flush=True)
    return found, tested


def one_dimensional_null_vector(matrix: np.ndarray) -> list[int]:
    rows = [list(map(Fraction, row)) for row in matrix.tolist()]
    row_count = len(rows)
    column_count = len(rows[0])
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][index] - factor * rows[pivot_row][index]
                for index in range(column_count)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free = [column for column in range(column_count) if column not in pivots]
    if len(free) != 1:
        raise RuntimeError(f"expected nullity one, got {len(free)}")
    vector = [Fraction(0) for _ in range(column_count)]
    vector[free[0]] = Fraction(1)
    for row, pivot in reversed(list(enumerate(pivots))):
        vector[pivot] = -sum(
            rows[row][column] * vector[column]
            for column in range(pivot + 1, column_count)
        )
    denominator_lcm = 1
    for value in vector:
        denominator_lcm = math.lcm(denominator_lcm, value.denominator)
    integers = [int(value * denominator_lcm) for value in vector]
    common = 0
    for value in integers:
        common = math.gcd(common, abs(value))
    return [value // common for value in integers]


def modular_rank(matrix: np.ndarray, prime: int = 1000003) -> int:
    rows = [
        [int(value) % prime for value in row]
        for row in matrix.astype(object).tolist()
    ]
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], prime - 2, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for row in range(row_count):
            if row == rank or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                (rows[row][index] - factor * rows[rank][index]) % prime
                for index in range(column_count)
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def exact_fixed_gordan_circuit(
    signs: np.ndarray, denominators: np.ndarray
) -> dict[str, object]:
    exact_matrix = cleared_matrix(denominators)
    floating = np.array(exact_matrix, dtype=float)
    norms = np.linalg.norm(floating, axis=0)
    normalized = floating / norms
    rank = modular_rank(exact_matrix)
    left, _, _ = np.linalg.svd(normalized, full_matrices=False)
    basis = left[:, :rank]
    signed_basis = signs[:, None] * basis
    equality = np.vstack(
        [signed_basis.T, np.ones(VERTICES, dtype=float)]
    )
    target = np.concatenate([np.zeros(rank), [1.0]])
    signed_cleared = (signs[:, None].astype(object) * exact_matrix).T
    rng = np.random.default_rng(50620260714)
    objectives = [np.zeros(VERTICES)] + [
        1e-7 * rng.standard_normal(VERTICES) for _ in range(32)
    ]
    feasible = False
    for objective in objectives:
        result = linprog(
            objective,
            A_eq=equality,
            b_eq=target,
            bounds=[(0.0, None)] * VERTICES,
            method="highs",
        )
        if not result.success:
            continue
        feasible = True
        for tolerance in (1e-6, 1e-8, 1e-10, 1e-12, 1e-14):
            support = np.flatnonzero(result.x > tolerance).tolist()
            try:
                weights = one_dimensional_null_vector(
                    signed_cleared[:, support]
                )
            except RuntimeError:
                continue
            if all(value < 0 for value in weights):
                weights = [-value for value in weights]
            if not all(value > 0 for value in weights):
                continue
            if np.all(
                signed_cleared[:, support]
                @ np.array(weights, dtype=object)
                == 0
            ):
                return {"support": support, "weights": weights}
    if not feasible:
        raise RuntimeError("fixed tuple is unexpectedly separable")
    raise RuntimeError("could not recover an exact fixed-tuple circuit")


def best_tuple_obstruction(
    signs: np.ndarray, best: dict[str, object], scale: int = 1000000
) -> dict[str, object]:
    theta = np.array(best["literal_weights"], dtype=float)
    orientations = tuple(int(value) for value in best["orientations"])
    denominators = np.vstack(
        [
            oriented_integer_denominator(
                np.maximum(1, np.rint(scale * theta[head])),
                orientations[head],
            )
            for head in range(HEADS)
        ]
    )
    assert exact_head_certificate(signs, denominators) is None
    circuit = exact_fixed_gordan_circuit(signs, denominators)
    return {
        "denominators": denominators.tolist(),
        "gordan_support": circuit["support"],
        "gordan_weights": circuit["weights"],
    }


def verify_payload(payload: dict[str, object]) -> None:
    for flipped_hex, record in payload["candidates"].items():
        flipped = int(flipped_hex, 16)
        exact.verify_threshold_degree(flipped)
        certificate = record.get("five_head_certificate")
        if certificate is not None:
            verify_head_certificate(flipped, certificate)
        signs = target_signs(flipped).astype(object)
        for attempt in record.get("continuous_attempts", []):
            obstruction = attempt.get("best_fixed_tuple_obstruction")
            if obstruction is None:
                continue
            denominators = np.array(obstruction["denominators"], dtype=object)
            signed = (signs[:, None] * cleared_matrix(denominators)).T
            weights = np.zeros(VERTICES, dtype=object)
            weights[obstruction["gordan_support"]] = np.array(
                obstruction["gordan_weights"], dtype=object
            )
            assert all(
                int(value) > 0 for value in obstruction["gordan_weights"]
            )
            assert np.all(signed @ weights == 0)
    print("verified parity-single-flip H5 search payload", flush=True)


def write_checkpoint(output: Path, payload: dict[str, object]) -> None:
    output.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--continuous-seeds", type=int, default=3)
    parser.add_argument("--restarts", type=int, default=96)
    parser.add_argument("--max-iterations", type=int, default=7000)
    parser.add_argument("--random-fixed-trials", type=int, default=20000)
    parser.add_argument("--exact-fixed-obstructions", action="store_true")
    parser.add_argument("--seed", type=int, default=65320260714)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        verify_payload(json.loads(arguments.output.read_text()))
        return

    payload: dict[str, object] = {
        "status": (
            "Every reported H5 success and fixed-tuple obstruction is exact. "
            "Continuous and random search failures are not a global H5 lower "
            "bound."
        ),
        "parameters": {
            "continuous_seeds": arguments.continuous_seeds,
            "restarts_per_orientation_type": arguments.restarts,
            "max_iterations": arguments.max_iterations,
            "random_fixed_trials": arguments.random_fixed_trials,
            "seed": arguments.seed,
            "fixed_lp_tested_for_every_continuous_restart": True,
            "exact_fixed_obstructions": arguments.exact_fixed_obstructions,
            "orientation_types_up_to_head_permutation": list(
                ORIENTATION_COUNTS
            ),
        },
        "known_certificate_self_check": {
            "endpoint_margin": exact.verify_head_certificate(
                0, exact.ENDPOINT_DENOMINATORS, exact.ENDPOINT_SCORE
            ),
            "adjacent_margin": exact.verify_head_certificate(
                1, exact.ADJACENT_DENOMINATORS, exact.ADJACENT_SCORE
            ),
        },
        "candidates": {
            "0x03": {
                "flip_weight": 2,
                "threshold_degree": 5,
                "continuous_attempts": [],
                "five_head_certificate": None,
            },
            "0x07": {
                "flip_weight": 3,
                "threshold_degree": 5,
                "continuous_attempts": [],
                "five_head_certificate": None,
            },
        },
    }
    for flipped in (3, 7):
        exact.verify_threshold_degree(flipped)

    scales = tuple(10**exponent for exponent in range(2, 11))
    for flipped_hex, record in payload["candidates"].items():
        flipped = int(flipped_hex, 16)
        signs = target_signs(flipped)
        for seed_index in range(arguments.continuous_seeds):
            if record["five_head_certificate"] is not None:
                break
            for positive_heads in ORIENTATION_COUNTS:
                seed = (
                    arguments.seed
                    + 1000003 * seed_index
                    + 10007 * flipped
                    + 101 * positive_heads
                )
                certificate, best = search_orientation(
                    flipped,
                    signs,
                    positive_heads,
                    seed,
                    arguments.restarts,
                    arguments.max_iterations,
                    scales,
                )
                attempt: dict[str, object] = {
                    "seed_index": seed_index,
                    "positive_heads": positive_heads,
                    "best": best,
                }
                if (
                    certificate is None
                    and best
                    and arguments.exact_fixed_obstructions
                ):
                    attempt["best_fixed_tuple_obstruction"] = (
                        best_tuple_obstruction(signs, best)
                    )
                record["continuous_attempts"].append(attempt)
                if certificate is not None:
                    record["five_head_certificate"] = certificate
                    record["outcome"] = "exact H5 certificate found"
                    break
                write_checkpoint(arguments.output, payload)

    unresolved = {
        int(flipped_hex, 16): target_signs(int(flipped_hex, 16))
        for flipped_hex, record in payload["candidates"].items()
        if record["five_head_certificate"] is None
    }
    if unresolved and arguments.random_fixed_trials > 0:
        found, tested = random_fixed_screen(
            unresolved,
            arguments.random_fixed_trials,
            arguments.seed + 999983,
        )
        for flipped, signs in unresolved.items():
            record = payload["candidates"][f"0x{flipped:02x}"]
            record["random_fixed_tuples_tested"] = tested[flipped]
            if flipped in found:
                record["five_head_certificate"] = found[flipped]
                record["outcome"] = "exact random fixed-tuple H5 certificate"
            else:
                record["outcome"] = "uncertified search survivor"
    for record in payload["candidates"].values():
        record.setdefault("outcome", "exact H5 certificate found")

    write_checkpoint(arguments.output, payload)
    verify_payload(payload)
    print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
