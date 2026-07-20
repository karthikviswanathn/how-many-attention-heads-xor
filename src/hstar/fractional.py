"""Exact certificates and numerical searches for linear-fractional heads."""

from __future__ import annotations

import math
from typing import Any, Sequence

import numpy as np
from scipy.optimize import linprog

from .boolean_cube import VERTEX_ORDER, affine_matrix, validate_signs


POSITIVE = 1
NEGATIVE = -1
CONSTANT = 0


def _exact_integer(value: Any) -> int:
    """Convert a numeric value only if it is exactly integral."""
    if isinstance(value, (bool, np.bool_)):
        raise ValueError("Boolean values are not certificate integers")
    integer = int(value)
    if value != integer:
        raise ValueError("certificate value is not exactly integral")
    return integer


def literal_weights_to_affine(
    literal_weights: Sequence[int], orientation: int
) -> np.ndarray:
    """Convert positive literal weights to affine denominator coefficients."""
    weights = [_exact_integer(value) for value in literal_weights]
    if not weights or any(value <= 0 for value in weights):
        raise ValueError("every literal weight must be a positive integer")
    if orientation == POSITIVE:
        return np.array(weights, dtype=object)
    if orientation == NEGATIVE:
        return np.array(
            [sum(weights)] + [-value for value in weights[1:]],
            dtype=object,
        )
    raise ValueError("orientation must be +1 or -1")


def denominator_report(
    coefficients: Sequence[int], orientation: int, dimension: int
) -> dict[str, Any]:
    """Check positivity and strict model-faithful orientation exactly."""
    try:
        row = [_exact_integer(value) for value in coefficients]
    except (TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "denominator coefficients are not integers"}
    if len(row) != dimension + 1:
        return {"valid": False, "reason": "wrong denominator width"}
    slopes = row[1:]
    if orientation == POSITIVE:
        oriented = all(value > 0 for value in slopes) and row[0] > 0
    elif orientation == NEGATIVE:
        oriented = all(value < 0 for value in slopes) and sum(row) > 0
    elif orientation == CONSTANT:
        oriented = all(value == 0 for value in slopes) and row[0] > 0
    else:
        return {"valid": False, "reason": "invalid orientation"}

    affine = affine_matrix(dimension, object)
    values = affine @ np.array(row, dtype=object)
    positive = min(values) > 0
    return {
        "valid": bool(oriented and positive and orientation != CONSTANT),
        "strictly_oriented": bool(oriented),
        "strictly_positive": bool(positive),
        "model_faithful_certificate": orientation != CONSTANT,
        "minimum": int(min(values)),
        "maximum": int(max(values)),
    }


def cleared_matrix(dimension: int, denominators: np.ndarray) -> np.ndarray:
    """Build exact cleared-score features for fixed denominators.

    Columns are the global constant followed by one affine numerator block per
    head.  Python integers are used throughout to avoid overflow.
    """
    raw_denominators = np.asarray(denominators, dtype=object)
    try:
        denominator_array = np.array(
            [
                [_exact_integer(value) for value in row]
                for row in raw_denominators.tolist()
            ],
            dtype=object,
        )
    except (TypeError, ValueError, OverflowError):
        raise ValueError("denominators must have integer coefficients") from None
    if denominator_array.ndim != 2 or denominator_array.shape[1] != dimension + 1:
        raise ValueError("denominators must have shape (heads, dimension + 1)")
    affine = affine_matrix(dimension, object)
    values = affine @ denominator_array.T
    if values.shape[1] == 0:
        return np.ones((1 << dimension, 1), dtype=object)
    if min(values.ravel()) <= 0:
        raise ValueError("every denominator must be positive on the cube")
    full_product = np.prod(values, axis=1)
    columns: list[np.ndarray] = [full_product]
    for head in range(len(denominator_array)):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(dimension + 1)
        )
    return np.column_stack(columns).astype(object)


def ratio_features(dimension: int, denominators: np.ndarray) -> np.ndarray:
    """Build floating features for the inner fixed-denominator LP."""
    denominator_array = np.asarray(denominators, dtype=float)
    affine = affine_matrix(dimension, float)
    values = affine @ denominator_array.T
    if values.shape[1] == 0 or not np.all(values > 0):
        raise ValueError("at least one positive denominator is required")
    return np.column_stack(
        [np.ones(len(affine))]
        + [affine / values[:, head, None] for head in range(len(denominator_array))]
    )


def verify_head_certificate(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
    dimension: int,
) -> dict[str, Any]:
    """Verify a head upper certificate using only exact integer arithmetic."""
    checked_signs = validate_signs(signs, dimension).astype(object)
    if certificate.get("dimension", dimension) != dimension:
        return {"valid": False, "reason": "certificate dimension mismatch"}
    if certificate.get("vertex_order", VERTEX_ORDER) != VERTEX_ORDER:
        return {"valid": False, "reason": "certificate vertex-order mismatch"}
    raw_orientations = certificate.get("orientations", [])
    try:
        orientations = [_exact_integer(value) for value in raw_orientations]
    except (TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "orientations are not integers"}
    if any(value not in (NEGATIVE, POSITIVE) for value in orientations):
        return {"valid": False, "reason": "certificates require strict +/- orientations"}
    heads = len(orientations)
    if certificate.get("head_count", heads) != heads:
        return {"valid": False, "reason": "certificate head-count mismatch"}
    raw_denominators = np.asarray(certificate.get("denominators", []), dtype=object)
    try:
        denominators = np.array(
            [
                [_exact_integer(value) for value in row]
                for row in raw_denominators.tolist()
            ],
            dtype=object,
        )
    except (TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "denominator coefficients are not integers"}
    if denominators.shape != (heads, dimension + 1):
        return {"valid": False, "reason": "denominator shape mismatch"}
    reports = [
        denominator_report(denominators[head], orientations[head], dimension)
        for head in range(heads)
    ]
    if not all(report["valid"] for report in reports):
        return {
            "valid": False,
            "reason": "a denominator is not strictly admissible",
            "denominator_reports": reports,
        }
    coefficients = np.asarray(certificate.get("score_coefficients", []), dtype=object)
    expected = 1 + heads * (dimension + 1)
    if coefficients.shape != (expected,):
        return {"valid": False, "reason": "score coefficient length mismatch"}
    try:
        coefficients = np.array(
            [_exact_integer(value) for value in coefficients],
            dtype=object,
        )
    except (TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "score coefficients are not integers"}
    matrix = cleared_matrix(dimension, denominators)
    signed_scores = checked_signs * (matrix @ coefficients)
    minimum = int(min(signed_scores))
    archived = certificate.get("minimum_signed_cleared_score")
    if archived is not None:
        try:
            archived_minimum = _exact_integer(archived)
        except (TypeError, ValueError, OverflowError):
            return {"valid": False, "reason": "archived minimum is not an integer"}
        if archived_minimum != minimum:
            return {
                "valid": False,
                "reason": "archived minimum does not match recomputation",
                "recomputed_minimum": minimum,
            }
    return {
        "valid": minimum > 0,
        "minimum_signed_cleared_score": minimum,
        "maximum_signed_cleared_score": int(max(signed_scores)),
        "denominator_reports": reports,
    }


def exact_fixed_denominator_certificate(
    signs: np.ndarray | list[int],
    dimension: int,
    denominators: np.ndarray,
    orientations: Sequence[int],
) -> dict[str, Any] | None:
    """Solve the inner LP, round it, and verify an integer certificate.

    Returning ``None`` is only a failure for this fixed tuple.  It is never a
    global lower bound.
    """
    checked_signs = validate_signs(signs, dimension)
    denominator_array = np.asarray(denominators, dtype=object)
    if denominator_array.shape != (len(orientations), dimension + 1):
        raise ValueError("denominator shape and orientations disagree")
    reports = [
        denominator_report(denominator_array[head], int(orientations[head]), dimension)
        for head in range(len(orientations))
    ]
    if not all(report["valid"] for report in reports):
        raise ValueError("the proposed denominators are not strictly admissible")

    features = ratio_features(dimension, denominator_array)
    norms = np.linalg.norm(features, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    normalized = features[:, keep] / norms[keep]
    variables = normalized.shape[1]
    constraints = np.zeros((len(checked_signs), variables + 1))
    constraints[:, :variables] = -(checked_signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variables + 1)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(checked_signs)),
        bounds=[(-1.0, 1.0)] * variables + [(None, None)],
        method="highs",
    )
    if not result.success or -float(result.fun) <= 1e-11:
        return None

    floating_coefficients = np.zeros(features.shape[1])
    floating_coefficients[keep] = result.x[:variables] / norms[keep]
    matrix = cleared_matrix(dimension, denominator_array)
    floating_matrix = np.asarray(matrix, dtype=float)
    floating_margin = float(
        np.min(checked_signs * (floating_matrix @ floating_coefficients))
    )
    if not math.isfinite(floating_margin) or floating_margin <= 1e-12:
        return None
    row_norm = max(sum(abs(int(value)) for value in row) for row in matrix.tolist())
    scale = max(1, int(math.ceil((row_norm + 1) / floating_margin)))
    for _ in range(200):
        integer_coefficients = np.array(
            [int(round(scale * value)) for value in floating_coefficients],
            dtype=object,
        )
        certificate = {
            "schema_version": 1,
            "dimension": dimension,
            "vertex_order": VERTEX_ORDER,
            "head_count": len(orientations),
            "orientations": [int(value) for value in orientations],
            "denominators": [
                [int(value) for value in row] for row in denominator_array.tolist()
            ],
            "score_coefficients": [int(value) for value in integer_coefficients],
            "floating_margin": floating_margin,
            "rounding_scale": scale,
        }
        signed = checked_signs.astype(object) * (matrix @ integer_coefficients)
        certificate["minimum_signed_cleared_score"] = int(min(signed))
        report = verify_head_certificate(certificate, checked_signs, dimension)
        if report["valid"]:
            return certificate
        scale *= 2
    return None


def random_denominator_search(
    signs: np.ndarray | list[int],
    dimension: int,
    heads: int,
    *,
    restarts: int = 250,
    seed: int = 0,
    maximum_weight: int = 64,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Search orientation-simplex interiors; verify every reported success."""
    if heads < 1:
        raise ValueError("heads must be positive")
    if restarts < 0 or maximum_weight < 1:
        raise ValueError("invalid search budget")
    checked_signs = validate_signs(signs, dimension)
    rng = np.random.default_rng(seed)
    attempts = 0
    for positive_heads in range(heads + 1):
        orientations = tuple(
            [NEGATIVE] * (heads - positive_heads) + [POSITIVE] * positive_heads
        )
        for restart in range(restarts):
            attempts += 1
            if restart == 0:
                literal_weights = np.ones((heads, dimension + 1), dtype=np.int64)
            else:
                logits = rng.uniform(
                    0.0,
                    math.log(maximum_weight),
                    size=(heads, dimension + 1),
                )
                literal_weights = np.maximum(1, np.rint(np.exp(logits))).astype(np.int64)
            denominators = np.vstack(
                [
                    literal_weights_to_affine(literal_weights[head], orientations[head])
                    for head in range(heads)
                ]
            )
            certificate = exact_fixed_denominator_certificate(
                checked_signs,
                dimension,
                denominators,
                orientations,
            )
            if certificate is not None:
                certificate["search"] = {
                    "method": "random-oriented-denominators-plus-inner-lp",
                    "seed": seed,
                    "restart": restart,
                    "positive_heads": positive_heads,
                }
                return certificate, {
                    "status": "verified-certificate-found",
                    "attempts": attempts,
                    "fixed_tuple_failures_are_global_lower_bounds": False,
                }
    return None, {
        "status": "not-found",
        "attempts": attempts,
        "fixed_tuple_failures_are_global_lower_bounds": False,
    }
