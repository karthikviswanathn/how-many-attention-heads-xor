"""Portable integer certificates for threshold-degree linear alternatives."""

from __future__ import annotations

from typing import Any

import numpy as np

from .boolean_cube import monomial_matrix, validate_signs


def _exact_integer(value: Any) -> int:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError("Boolean values are not certificate integers")
    integer = int(value)
    if value != integer:
        raise ValueError("certificate value is not exactly integral")
    return integer


def verify_threshold_polynomial(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
    dimension: int,
) -> dict[str, Any]:
    """Verify an integer polynomial sign-representation certificate."""
    checked = validate_signs(signs, dimension).astype(object)
    try:
        degree = _exact_integer(certificate["degree"])
        coefficients = [
            _exact_integer(value)
            for value in certificate["integer_coefficients"]
        ]
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "malformed polynomial certificate"}
    if not 0 <= degree <= dimension:
        return {"valid": False, "reason": "invalid polynomial degree"}
    matrix, monomials = monomial_matrix(dimension, degree, object)
    if len(coefficients) != matrix.shape[1]:
        return {"valid": False, "reason": "coefficient count mismatch"}
    archived_monomials = certificate.get("monomials")
    if archived_monomials is not None:
        expected = [list(subset) for subset in monomials]
        if archived_monomials != expected:
            return {"valid": False, "reason": "monomial ordering mismatch"}
    values = matrix @ np.array(coefficients, dtype=object)
    signed_values = checked * values
    minimum = int(min(signed_values))
    archived_minimum = certificate.get("minimum_signed_value")
    if archived_minimum is not None:
        try:
            if _exact_integer(archived_minimum) != minimum:
                return {
                    "valid": False,
                    "reason": "archived polynomial margin mismatch",
                }
        except (TypeError, ValueError, OverflowError):
            return {"valid": False, "reason": "polynomial margin is not integral"}
    return {
        "valid": minimum > 0,
        "degree": degree,
        "minimum_signed_value": minimum,
        "maximum_absolute_value": int(max(abs(value) for value in values)),
    }


def verify_gordan_obstruction(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
    dimension: int,
) -> dict[str, Any]:
    """Verify that no polynomial of the archived degree strictly separates.

    For the signed monomial matrix ``A = diag(signs) M_d``, a nonzero vector
    ``q >= 0`` with ``A.T q = 0`` is Gordan's alternative to strict
    separation.  Integer weights make the verification fully portable.
    """
    checked = validate_signs(signs, dimension).astype(object)
    try:
        degree = _exact_integer(certificate["degree"])
        support = certificate["support"]
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "malformed Gordan certificate"}
    if not 0 <= degree <= dimension:
        return {"valid": False, "reason": "invalid obstruction degree"}
    if not isinstance(support, list):
        return {"valid": False, "reason": "Gordan support must be a list"}
    weights = np.zeros(1 << dimension, dtype=object)
    seen: set[int] = set()
    try:
        for item in support:
            vertex = _exact_integer(item["vertex"])
            weight = _exact_integer(item["weight"])
            if not 0 <= vertex < 1 << dimension:
                return {"valid": False, "reason": "support vertex is out of range"}
            if vertex in seen:
                return {"valid": False, "reason": "duplicate support vertex"}
            if weight <= 0:
                return {"valid": False, "reason": "support weight is not positive"}
            seen.add(vertex)
            weights[vertex] = weight
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "malformed Gordan support entry"}
    total = int(sum(weights))
    if total <= 0:
        return {"valid": False, "reason": "Gordan vector is zero"}
    archived_total = certificate.get("total_weight")
    if archived_total is not None:
        try:
            if _exact_integer(archived_total) != total:
                return {"valid": False, "reason": "archived Gordan total mismatch"}
        except (TypeError, ValueError, OverflowError):
            return {"valid": False, "reason": "Gordan total is not integral"}
    matrix, _ = monomial_matrix(dimension, degree, object)
    signed_matrix = checked[:, None] * matrix
    moments = signed_matrix.T @ weights
    nonzero = [
        {"column": column, "value": int(value)}
        for column, value in enumerate(moments)
        if value != 0
    ]
    return {
        "valid": not nonzero,
        "degree_ruled_out": degree,
        "support_size": len(seen),
        "total_weight": total,
        "nonzero_moments": nonzero,
    }
