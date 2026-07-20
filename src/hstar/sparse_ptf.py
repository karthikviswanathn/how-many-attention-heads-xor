"""Certified sparse polynomial-threshold upper bounds.

The searches in this module are deliberately one-sided.  Both retain an exact
full-basis interpolation as a safe fallback.  The deletion search refits after
removing columns from a materialized dictionary.  The column-generation search
instead prices an implicit dictionary with fast transforms and materializes
only its restricted master.  A proposed support changes the returned upper
bound only after its coefficients have been rounded and an independent integer
verifier has checked every Boolean input.

Two compiler bases are supported:

``monotone-01``
    The feature indexed by ``S`` is ``prod(x_i for i in S)``.  All singleton
    terms share one affine head and every active term of degree at least two
    costs one head.

``walsh``
    The feature indexed by ``S`` is ``(-1)^sum(x_i for i in S)``.  All
    singleton characters share one affine head and an active character of
    degree at least two costs ``len(S)`` heads.

The compiler costs are justified by Lemmas 048 and 045 in the repository.  A
certificate is therefore a compact theorem-backed head upper bound; it need
not expand every selected feature into explicit linear-fractional atoms.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import math
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
from scipy.optimize import linprog

from .boolean_cube import VERTEX_ORDER, mask_from_signs, validate_signs


MONOTONE_BASIS = "monotone-01"
WALSH_BASIS = "walsh"
SUPPORTED_BASES = (MONOTONE_BASIS, WALSH_BASIS)

_COMPILERS = {
    MONOTONE_BASIS: "affine-free-sparsity",
    WALSH_BASIS: "fourier-support-cost",
}

_COMPILER_LEMMAS = {
    MONOTONE_BASIS: (
        "lemmas/03_function_families_and_affine_geometry/"
        "048_affine_free_sparsity_upper_bound.md"
    ),
    WALSH_BASIS: (
        "lemmas/02_complexity_measure_upper_bounds/"
        "045_fourier_support_upper_bound.md"
    ),
}


class FourierTailBudgetExceeded(ValueError):
    """Report a predictable exact-knapsack budget miss without losing metadata."""

    def __init__(self, estimated_transitions: int, max_transitions: int) -> None:
        self.estimated_transitions = int(estimated_transitions)
        self.max_transitions = int(max_transitions)
        super().__init__(
            "the Fourier-tail dynamic program needs an estimated "
            f"{self.estimated_transitions} transitions, exceeding the budget "
            f"of {self.max_transitions}"
        )


@dataclass(frozen=True)
class SparsePTFSearchConfig:
    """Bound the floating support-reduction phase.

    ``max_prune_solves`` is applied separately to every ordering restart.  If
    the initial feature matrix would exceed ``max_matrix_entries``, the search
    skips pruning and returns the exact full-basis certificate.
    """

    max_prune_solves: int = 256
    ordering_restarts: int = 1
    max_matrix_entries: int = 4_000_000
    margin_tolerance: float = 1e-10
    rounding_attempts: int = 160
    seed: int = 0


@dataclass(frozen=True)
class SparsePTFColumnGenerationConfig:
    """Bound transform-priced sparse PTF column generation."""

    max_iterations: int = 64
    batch_size: int = 8
    max_columns: int = 256
    pricing_tolerance: float = 1e-7
    artificial_tolerance: float = 1e-8
    coefficient_tolerance: float = 1e-9
    margin_tolerance: float = 1e-10
    rounding_attempts: int = 160


def _exact_integer(value: Any) -> int:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError("Boolean values are not certificate integers")
    integer = int(value)
    if value != integer:
        raise ValueError("certificate value is not exactly integral")
    return integer


def _validate_basis(basis: str) -> str:
    if basis not in SUPPORTED_BASES:
        raise ValueError(f"basis must be one of {SUPPORTED_BASES}")
    return basis


def _fwht_in_place(values: list[int]) -> None:
    """Apply the unnormalized Walsh-Hadamard transform exactly."""
    block = 1
    length = len(values)
    while block < length:
        stride = 2 * block
        for start in range(0, length, stride):
            for offset in range(block):
                left_index = start + offset
                right_index = left_index + block
                left = values[left_index]
                right = values[right_index]
                values[left_index] = left + right
                values[right_index] = left - right
        block = stride


def _subset_zeta_in_place(values: list[int], dimension: int) -> None:
    """Replace coefficients by their evaluations on every subset."""
    for coordinate in range(dimension):
        bit = 1 << coordinate
        for mask in range(1 << dimension):
            if mask & bit:
                values[mask] += values[mask ^ bit]


def _subset_mobius_in_place(values: list[int], dimension: int) -> None:
    """Invert the subset-zeta transform exactly."""
    for coordinate in range(dimension):
        bit = 1 << coordinate
        for mask in range(1 << dimension):
            if mask & bit:
                values[mask] -= values[mask ^ bit]


def _initial_coefficients(
    signs: np.ndarray,
    dimension: int,
    basis: str,
) -> dict[int, int]:
    """Return an exact full-basis score with the requested signs."""
    values = [int(value) for value in signs]
    if basis == MONOTONE_BASIS:
        _subset_mobius_in_place(values, dimension)
    else:
        _fwht_in_place(values)
    return {mask: value for mask, value in enumerate(values) if value != 0}


def _evaluate_exact(
    coefficients: Mapping[int, int],
    dimension: int,
    basis: str,
) -> list[int]:
    """Evaluate a sparse coefficient mapping in ``O(n 2^n)`` arithmetic."""
    values = [0] * (1 << dimension)
    for mask, coefficient in coefficients.items():
        values[mask] = int(coefficient)
    if basis == MONOTONE_BASIS:
        _subset_zeta_in_place(values, dimension)
    else:
        _fwht_in_place(values)
    return values


def _compiler_cost(masks: Iterable[int], basis: str) -> int:
    degrees = [int(mask).bit_count() for mask in masks]
    affine = int(any(degree == 1 for degree in degrees))
    if basis == MONOTONE_BASIS:
        nonlinear = sum(degree >= 2 for degree in degrees)
    else:
        nonlinear = sum(degree for degree in degrees if degree >= 2)
    return affine + nonlinear


def _subset_from_mask(mask: int, dimension: int) -> list[int]:
    return [coordinate for coordinate in range(dimension) if mask & (1 << coordinate)]


def _mask_from_subset(raw_subset: Any, dimension: int) -> int:
    if not isinstance(raw_subset, list):
        raise ValueError("term subset must be a list")
    coordinates = [_exact_integer(value) for value in raw_subset]
    if coordinates != sorted(coordinates) or len(coordinates) != len(set(coordinates)):
        raise ValueError("term subset is not strictly ordered")
    if any(not 0 <= coordinate < dimension for coordinate in coordinates):
        raise ValueError("term subset coordinate is out of range")
    return sum(1 << coordinate for coordinate in coordinates)


def _certificate_from_coefficients(
    coefficients: Mapping[int, int],
    signs: np.ndarray,
    dimension: int,
    basis: str,
) -> dict[str, Any]:
    cleaned = {
        int(mask): int(coefficient)
        for mask, coefficient in coefficients.items()
        if int(coefficient) != 0
    }
    if not cleaned:
        raise ValueError("a sign certificate cannot have empty support")
    divisor = math.gcd(*[abs(value) for value in cleaned.values()])
    if divisor > 1:
        cleaned = {mask: value // divisor for mask, value in cleaned.items()}
    values = _evaluate_exact(cleaned, dimension, basis)
    signed_values = [int(signs[index]) * value for index, value in enumerate(values)]
    minimum = min(signed_values)
    if minimum <= 0:
        raise ValueError("the proposed integer coefficients do not separate")
    ordered_masks = sorted(cleaned)
    return {
        "schema_version": 1,
        "certificate_type": "sparse-ptf-upper",
        "dimension": dimension,
        "vertex_order": VERTEX_ORDER,
        "truth_mask_hex": hex(mask_from_signs(signs, dimension)),
        "basis": basis,
        "compiler": _COMPILERS[basis],
        "compiler_lemma": _COMPILER_LEMMAS[basis],
        "head_count": _compiler_cost(ordered_masks, basis),
        "terms": [
            {
                "subset": _subset_from_mask(mask, dimension),
                "coefficient": cleaned[mask],
            }
            for mask in ordered_masks
        ],
        "minimum_signed_value": minimum,
        "maximum_absolute_value": max(abs(value) for value in values),
    }


def verify_sparse_ptf_certificate(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
    dimension: int,
) -> dict[str, Any]:
    """Verify a sparse PTF upper certificate using integer arithmetic only."""
    try:
        checked = validate_signs(signs, dimension)
    except ValueError as error:
        return {"valid": False, "reason": str(error)}
    try:
        if _exact_integer(certificate["schema_version"]) != 1:
            raise ValueError("unsupported schema version")
        if certificate["certificate_type"] != "sparse-ptf-upper":
            raise ValueError("wrong certificate type")
        if _exact_integer(certificate["dimension"]) != dimension:
            raise ValueError("certificate dimension mismatch")
        if certificate["vertex_order"] != VERTEX_ORDER:
            raise ValueError("vertex-order mismatch")
        basis = _validate_basis(certificate["basis"])
        if certificate["compiler"] != _COMPILERS[basis]:
            raise ValueError("compiler does not match the basis")
        raw_terms = certificate["terms"]
        if not isinstance(raw_terms, list) or not raw_terms:
            raise ValueError("certificate terms must be a nonempty list")
        coefficients: dict[int, int] = {}
        archived_order: list[int] = []
        for raw_term in raw_terms:
            if not isinstance(raw_term, dict):
                raise ValueError("malformed certificate term")
            mask = _mask_from_subset(raw_term["subset"], dimension)
            coefficient = _exact_integer(raw_term["coefficient"])
            if coefficient == 0:
                raise ValueError("zero coefficients must be omitted")
            if mask in coefficients:
                raise ValueError("duplicate feature subset")
            coefficients[mask] = coefficient
            archived_order.append(mask)
        if archived_order != sorted(archived_order):
            raise ValueError("terms are not in canonical mask order")
        archived_head_count = _exact_integer(certificate["head_count"])
        archived_minimum = _exact_integer(certificate["minimum_signed_value"])
        archived_maximum = certificate.get("maximum_absolute_value")
        if archived_maximum is not None:
            archived_maximum = _exact_integer(archived_maximum)
        archived_mask = certificate.get("truth_mask_hex")
        if archived_mask is not None:
            if isinstance(archived_mask, str):
                parsed_mask = int(archived_mask, 0)
            else:
                parsed_mask = _exact_integer(archived_mask)
            if parsed_mask != mask_from_signs(checked, dimension):
                raise ValueError("truth mask mismatch")
    except (KeyError, TypeError, ValueError, OverflowError) as error:
        return {"valid": False, "reason": str(error) or "malformed certificate"}

    values = _evaluate_exact(coefficients, dimension, basis)
    signed_values = [int(checked[index]) * value for index, value in enumerate(values)]
    minimum = min(signed_values)
    head_count = _compiler_cost(coefficients, basis)
    maximum = max(abs(value) for value in values)
    if archived_minimum != minimum:
        return {
            "valid": False,
            "reason": "archived minimum signed value does not match",
            "recomputed_minimum_signed_value": minimum,
        }
    if archived_head_count != head_count:
        return {
            "valid": False,
            "reason": "archived head count does not match compiler cost",
            "recomputed_head_count": head_count,
        }
    if archived_maximum is not None and archived_maximum != maximum:
        return {
            "valid": False,
            "reason": "archived maximum absolute value does not match",
            "recomputed_maximum_absolute_value": maximum,
        }
    return {
        "valid": minimum > 0,
        "basis": basis,
        "head_count": head_count,
        "support_size": len(coefficients),
        "maximum_degree": max(mask.bit_count() for mask in coefficients),
        "minimum_signed_value": minimum,
        "maximum_absolute_value": maximum,
    }


def _feature_matrix(
    masks: Sequence[int],
    dimension: int,
    basis: str,
) -> np.ndarray:
    vertex_count = 1 << dimension
    codes = np.arange(vertex_count, dtype=np.int64)
    if basis == MONOTONE_BASIS:
        columns = [((codes & mask) == mask).astype(float) for mask in masks]
    else:
        parity = np.fromiter(
            (code.bit_count() & 1 for code in range(vertex_count)),
            dtype=np.int8,
            count=vertex_count,
        )
        columns = [1.0 - 2.0 * parity[codes & mask] for mask in masks]
    return np.column_stack(columns)


def _nonlinear_feature_cost(mask: int, basis: str) -> int:
    """Return the compiler cost of one nonlinear basis feature."""
    degree = int(mask).bit_count()
    if degree < 2:
        raise ValueError("column-generation costs are only for nonlinear features")
    return 1 if basis == MONOTONE_BASIS else degree


def _fwht_float(values: np.ndarray) -> np.ndarray:
    """Return all Walsh correlations without building a feature dictionary."""
    transformed = np.asarray(values, dtype=float).copy()
    block = 1
    while block < len(transformed):
        stride = 2 * block
        for start in range(0, len(transformed), stride):
            left = transformed[start : start + block].copy()
            right = transformed[start + block : start + stride].copy()
            transformed[start : start + block] = left + right
            transformed[start + block : start + stride] = left - right
        block = stride
    return transformed


def _superset_zeta_float(values: np.ndarray, dimension: int) -> np.ndarray:
    """Return all monotone-monomial correlations by a superset zeta transform."""
    transformed = np.asarray(values, dtype=float).copy()
    for coordinate in range(dimension):
        step = 1 << coordinate
        stride = 2 * step
        for start in range(0, len(transformed), stride):
            transformed[start : start + step] += transformed[
                start + step : start + stride
            ]
    return transformed


def _full_weighted_l1_bound(
    seed_coefficients: Mapping[int, int],
    dimension: int,
    basis: str,
) -> float:
    """Bound the full-master objective using exact label interpolation."""
    numerator = sum(
        _nonlinear_feature_cost(mask, basis) * abs(int(coefficient))
        for mask, coefficient in seed_coefficients.items()
        if int(mask).bit_count() >= 2
    )
    if basis == WALSH_BASIS:
        return float(numerator) / float(1 << dimension)
    return float(numerator)


def _solve_column_master(
    signs: np.ndarray,
    affine_features: np.ndarray,
    nonlinear_features: np.ndarray,
    active_masks: Sequence[int],
    basis: str,
    artificial_penalty: float,
) -> dict[str, Any] | None:
    """Solve one restricted weighted-L1 master with an artificial label column."""
    # With affine matrix A, generated nonlinear matrix Phi, and labels y, the
    # restricted Phase I primal is
    #
    #   min  sum_j c_j (u_j + v_j) + M a
    #   s.t. y_x [A_x alpha + Phi_x (u - v)] + a >= 1,
    #        alpha free, u,v,a >= 0.
    #
    # The artificial raw-score feature is y itself, hence its signed value is
    # one on every row.  For lambda >= 0, the corresponding dual conditions are
    #
    #   A^T (y * lambda) = 0,
    #   |Phi_j^T (y * lambda)| <= c_j,
    #   sum_x lambda_x <= M.
    #
    # SciPy reports nonpositive marginals for the <= form used below, so the
    # dual weights are their negations.
    vertex_count = len(signs)
    affine_count = affine_features.shape[1]
    nonlinear_count = len(active_masks)
    variable_count = affine_count + 2 * nonlinear_count + 1

    objective = np.zeros(variable_count, dtype=float)
    costs = np.fromiter(
        (_nonlinear_feature_cost(mask, basis) for mask in active_masks),
        dtype=float,
        count=nonlinear_count,
    )
    if nonlinear_count:
        objective[affine_count : affine_count + nonlinear_count] = costs
        objective[
            affine_count + nonlinear_count : affine_count + 2 * nonlinear_count
        ] = costs
    objective[-1] = artificial_penalty

    constraints = np.empty((vertex_count, variable_count), dtype=float)
    signed_affine = signs[:, None] * affine_features
    constraints[:, :affine_count] = -signed_affine
    if nonlinear_count:
        signed_nonlinear = signs[:, None] * nonlinear_features
        constraints[:, affine_count : affine_count + nonlinear_count] = (
            -signed_nonlinear
        )
        constraints[
            :, affine_count + nonlinear_count : affine_count + 2 * nonlinear_count
        ] = signed_nonlinear
    constraints[:, -1] = -1.0

    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=-np.ones(vertex_count, dtype=float),
        bounds=[(None, None)] * affine_count
        + [(0.0, None)] * (2 * nonlinear_count + 1),
        method="highs",
    )
    if not result.success:
        return None

    affine_coefficients = result.x[:affine_count]
    positive = result.x[affine_count : affine_count + nonlinear_count]
    negative = result.x[
        affine_count + nonlinear_count : affine_count + 2 * nonlinear_count
    ]
    nonlinear_coefficients = positive - negative
    artificial_value = float(result.x[-1])
    real_scores = affine_features @ affine_coefficients
    if nonlinear_count:
        real_scores = real_scores + nonlinear_features @ nonlinear_coefficients
    dual_weights = np.maximum(
        0.0,
        -np.asarray(result.ineqlin.marginals, dtype=float),
    )
    return {
        "objective": float(result.fun),
        "affine_coefficients": affine_coefficients,
        "nonlinear_coefficients": nonlinear_coefficients,
        "artificial_value": artificial_value,
        "real_margin": float(np.min(signs * real_scores)),
        "dual_weights": dual_weights,
        "dual_mass": float(np.sum(dual_weights)),
        "affine_dual_residual": float(
            np.max(np.abs(signed_affine.T @ dual_weights))
        ),
        "matrix_entries": int(constraints.size),
    }


def _price_nonlinear_columns(
    dual_weights: np.ndarray,
    signs: np.ndarray,
    dimension: int,
    basis: str,
    active_masks: set[int],
    batch_size: int,
    pricing_tolerance: float,
) -> dict[str, Any]:
    """Price every implicit nonlinear feature with one fast transform."""
    residual = np.asarray(dual_weights, dtype=float) * signs
    if basis == MONOTONE_BASIS:
        correlations = _superset_zeta_float(residual, dimension)
        method = "superset-zeta"
    else:
        correlations = _fwht_float(residual)
        method = "fwht"

    violating: list[tuple[float, float, int]] = []
    maximum_ratio = 0.0
    for mask, correlation in enumerate(correlations):
        if mask.bit_count() < 2 or mask in active_masks:
            continue
        cost = _nonlinear_feature_cost(mask, basis)
        ratio = abs(float(correlation)) / float(cost)
        maximum_ratio = max(maximum_ratio, ratio)
        if ratio > 1.0 + pricing_tolerance:
            violating.append((ratio, abs(float(correlation)), mask))
    violating.sort(key=lambda item: (-item[0], -item[1], item[2]))
    return {
        "method": method,
        "maximum_ratio": maximum_ratio,
        "violation_count": len(violating),
        "masks": [item[2] for item in violating[:batch_size]],
    }


def _refit_column_candidate(
    signs: np.ndarray,
    dimension: int,
    basis: str,
    affine_masks: Sequence[int],
    active_masks: Sequence[int],
    nonlinear_coefficients: np.ndarray,
    coefficient_tolerance: float,
    margin_tolerance: float,
    rounding_attempts: int,
) -> tuple[dict[str, Any] | None, int]:
    """Refit promising generated supports, then round and verify exactly."""
    used_masks = [
        mask
        for mask, coefficient in zip(active_masks, nonlinear_coefficients)
        if abs(float(coefficient)) > coefficient_tolerance
    ]
    nonlinear_supports = [used_masks]
    if used_masks != list(active_masks):
        nonlinear_supports.append(list(active_masks))

    best: dict[str, Any] | None = None
    refit_solves = 0
    seen: set[tuple[int, ...]] = set()
    for nonlinear_support in nonlinear_supports:
        masks = tuple(affine_masks) + tuple(nonlinear_support)
        if masks in seen:
            continue
        seen.add(masks)
        features = _feature_matrix(masks, dimension, basis)
        refit_solves += 1
        solution = _maximum_margin_separator(features, signs, margin_tolerance)
        if solution is None:
            continue
        candidate = _exactify_floating_separator(
            masks,
            features,
            solution[0],
            signs,
            dimension,
            basis,
            rounding_attempts,
        )
        if candidate is not None and (
            best is None or _certificate_key(candidate) < _certificate_key(best)
        ):
            best = candidate
    return best, refit_solves


def _maximum_margin_separator(
    features: np.ndarray,
    signs: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, float] | None:
    """Find a bounded floating separator on a fixed support."""
    if features.ndim != 2 or features.shape[1] == 0:
        return None
    norms = np.linalg.norm(features, axis=0)
    keep = norms > 1e-14 * max(1.0, float(np.max(norms)))
    if not np.all(keep):
        return None
    normalized = features / norms
    variable_count = normalized.shape[1]
    constraints = np.zeros((len(signs), variable_count + 1), dtype=float)
    constraints[:, :variable_count] = -(signs[:, None] * normalized)
    constraints[:, -1] = 1.0
    objective = np.zeros(variable_count + 1, dtype=float)
    objective[-1] = -1.0
    result = linprog(
        objective,
        A_ub=constraints,
        b_ub=np.zeros(len(signs), dtype=float),
        bounds=[(-1.0, 1.0)] * variable_count + [(None, None)],
        method="highs",
    )
    if not result.success:
        return None
    coefficients = result.x[:variable_count] / norms
    signed_values = signs * (features @ coefficients)
    margin = float(np.min(signed_values))
    if not math.isfinite(margin) or margin <= tolerance:
        return None
    return coefficients, margin


def _exactify_floating_separator(
    masks: Sequence[int],
    features: np.ndarray,
    floating_coefficients: np.ndarray,
    signs: np.ndarray,
    dimension: int,
    basis: str,
    attempts: int,
) -> dict[str, Any] | None:
    floating_scores = features @ floating_coefficients
    margin = float(np.min(signs * floating_scores))
    if not math.isfinite(margin) or margin <= 0:
        return None
    row_l1 = float(np.max(np.sum(np.abs(features), axis=1)))
    scale = max(1, int(math.ceil((row_l1 + 1.0) / margin)))
    for _ in range(attempts):
        try:
            rounded = {
                int(mask): int(round(scale * float(coefficient)))
                for mask, coefficient in zip(masks, floating_coefficients)
                if int(round(scale * float(coefficient))) != 0
            }
        except (OverflowError, ValueError):
            return None
        if rounded:
            try:
                certificate = _certificate_from_coefficients(
                    rounded,
                    signs,
                    dimension,
                    basis,
                )
            except ValueError:
                certificate = None
            if certificate is not None:
                report = verify_sparse_ptf_certificate(
                    certificate,
                    signs,
                    dimension,
                )
                if report["valid"]:
                    certificate["floating_margin"] = margin
                    certificate["rounding_scale"] = scale
                    return certificate
        scale *= 2
    return None


def _certificate_key(certificate: dict[str, Any]) -> tuple[int, int, int, int]:
    terms = certificate["terms"]
    return (
        int(certificate["head_count"]),
        len(terms),
        max(len(term["subset"]) for term in terms),
        max(abs(int(term["coefficient"])) for term in terms),
    )


def fourier_tail_upper_bound(
    signs: np.ndarray | list[int],
    dimension: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Greedily retain exact Walsh mass until the omitted tail is below one.

    The unnormalized Walsh coefficients evaluate to ``2^n * signs``.  If the
    omitted absolute coefficient mass is strictly below ``2^n``, the retained
    score has the same strict signs.  Constants are free, all singleton terms
    share one affine head, and a nonlinear character costs its degree.

    The support ordering is heuristic.  The returned certificate is exact and
    independently verified, but a more expensive subset search may improve it.
    """
    checked = validate_signs(signs, dimension)
    coefficients = _initial_coefficients(checked, dimension, WALSH_BASIS)
    vertex_count = 1 << dimension
    constant = {0: coefficients[0]} if coefficients.get(0, 0) != 0 else {}
    singleton_masks = sorted(
        mask for mask in coefficients if int(mask).bit_count() == 1
    )
    nonlinear_masks = [
        mask for mask in coefficients if int(mask).bit_count() >= 2
    ]
    total_mass = sum(abs(value) for value in coefficients.values())

    orderings = [
        sorted(
            nonlinear_masks,
            key=lambda mask: (
                -Fraction(abs(coefficients[mask]), mask.bit_count()),
                -abs(coefficients[mask]),
                mask.bit_count(),
                mask,
            ),
        ),
        sorted(
            nonlinear_masks,
            key=lambda mask: (
                -abs(coefficients[mask]),
                mask.bit_count(),
                mask,
            ),
        ),
    ]
    candidates: list[tuple[dict[str, Any], int, bool, str]] = []
    for retain_singletons in (False, True):
        base = dict(constant)
        if retain_singletons:
            base.update(
                {mask: coefficients[mask] for mask in singleton_masks}
            )
        for ordering_index, ordering in enumerate(orderings):
            selected = dict(base)
            retained_mass = sum(abs(value) for value in selected.values())
            for mask in ordering:
                if total_mass - retained_mass < vertex_count:
                    break
                selected[mask] = coefficients[mask]
                retained_mass += abs(coefficients[mask])
            if total_mass - retained_mass >= vertex_count:
                continue

            removable = sorted(
                [mask for mask in selected if mask.bit_count() >= 2],
                key=lambda mask: (
                    Fraction(abs(coefficients[mask]), mask.bit_count()),
                    -mask.bit_count(),
                    mask,
                ),
            )
            for mask in removable:
                mass = abs(selected[mask])
                if total_mass - retained_mass + mass < vertex_count:
                    retained_mass -= mass
                    del selected[mask]
            certificate = _certificate_from_coefficients(
                selected,
                checked,
                dimension,
                WALSH_BASIS,
            )
            candidates.append(
                (
                    certificate,
                    total_mass - retained_mass,
                    retain_singletons,
                    "mass-per-head" if ordering_index == 0 else "absolute-mass",
                )
            )

    if not candidates:
        raise RuntimeError("full Walsh support failed the exact tail criterion")
    certificate, omitted_mass, retained_singletons, ordering_name = min(
        candidates,
        key=lambda item: _certificate_key(item[0]),
    )
    diagnostics = {
        "status": "verified-fourier-tail-certificate",
        "basis": WALSH_BASIS,
        "ordering": ordering_name,
        "retained_singletons": retained_singletons,
        "unnormalized_omitted_mass": omitted_mass,
        "strict_tail_threshold": vertex_count,
        "support_size": len(certificate["terms"]),
        "head_count": int(certificate["head_count"]),
        "search_is_optimal": False,
        "floating_failures_are_lower_bounds": False,
    }
    certificate = dict(certificate)
    certificate["search"] = diagnostics.copy()
    report = verify_sparse_ptf_certificate(
        certificate,
        checked,
        dimension,
    )
    if not report["valid"]:
        raise RuntimeError("the Fourier-tail certificate failed verification")
    return certificate, diagnostics


def optimal_fourier_tail_upper_bound(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    max_dp_transitions: int | None = 50_000_000,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Optimize the exact absolute Fourier-tail compiler criterion.

    All singleton coefficients form one cost-one item.  Within each nonlinear
    degree, equal compiler costs mean that an optimum retaining k terms keeps
    the k largest coefficient masses.  A grouped knapsack over these
    degree-prefix choices therefore finds the exact minimum compiler cost under
    the sufficient omitted-mass criterion.
    """
    checked = validate_signs(signs, dimension)
    if max_dp_transitions is not None and max_dp_transitions < 1:
        raise ValueError("max_dp_transitions must be positive or None")
    coefficients = _initial_coefficients(checked, dimension, WALSH_BASIS)
    vertex_count = 1 << dimension
    selected_coefficients = (
        {0: coefficients[0]} if coefficients.get(0, 0) != 0 else {}
    )

    groups: list[tuple[int, list[tuple[int, tuple[int, ...]]]]] = []
    singleton_masks = sorted(
        mask for mask in coefficients if int(mask).bit_count() == 1
    )
    if singleton_masks:
        groups.append(
            (
                1,
                [
                    (
                        sum(abs(coefficients[mask]) for mask in singleton_masks),
                        tuple(singleton_masks),
                    )
                ],
            )
        )
    for degree in range(2, dimension + 1):
        entries = [
            (abs(coefficients[mask]), (mask,))
            for mask in coefficients
            if int(mask).bit_count() == degree
        ]
        entries.sort(key=lambda item: (-item[0], item[1]))
        if entries:
            groups.append((degree, entries))

    item_mass = sum(
        abs(coefficient)
        for mask, coefficient in coefficients.items()
        if mask != 0
    )
    target_mass = max(0, item_mass - vertex_count + 1)
    maximum_cost = sum(cost * len(entries) for cost, entries in groups)
    estimated_transitions = sum(
        (maximum_cost + 1) * (len(entries) + 1)
        for _, entries in groups
    )
    if (
        max_dp_transitions is not None
        and estimated_transitions > max_dp_transitions
    ):
        raise FourierTailBudgetExceeded(
            estimated_transitions,
            max_dp_transitions,
        )

    unreachable = -1
    values = [unreachable] * (maximum_cost + 1)
    values[0] = 0
    choices: list[list[int]] = []
    current_maximum_cost = 0
    actual_transitions = 0
    for cost, entries in groups:
        prefix_mass = [0]
        for mass, _ in entries:
            prefix_mass.append(prefix_mass[-1] + mass)
        next_values = [unreachable] * (maximum_cost + 1)
        group_choices = [-1] * (maximum_cost + 1)
        for previous_cost in range(current_maximum_cost + 1):
            previous_value = values[previous_cost]
            if previous_value < 0:
                continue
            for retained_count, retained_mass in enumerate(prefix_mass):
                next_cost = previous_cost + retained_count * cost
                candidate_value = previous_value + retained_mass
                actual_transitions += 1
                if candidate_value > next_values[next_cost]:
                    next_values[next_cost] = candidate_value
                    group_choices[next_cost] = retained_count
        current_maximum_cost += cost * len(entries)
        values = next_values
        choices.append(group_choices)

    optimal_cost = next(
        cost
        for cost, retained_mass in enumerate(values)
        if retained_mass >= target_mass
    )
    retained_item_mass = values[optimal_cost]
    reconstruction_cost = optimal_cost
    for group_index in range(len(groups) - 1, -1, -1):
        cost, entries = groups[group_index]
        retained_count = choices[group_index][reconstruction_cost]
        if retained_count < 0:
            raise RuntimeError("Fourier-tail knapsack reconstruction failed")
        for _, masks in entries[:retained_count]:
            for mask in masks:
                selected_coefficients[mask] = coefficients[mask]
        reconstruction_cost -= retained_count * cost
    if reconstruction_cost != 0:
        raise RuntimeError("Fourier-tail knapsack cost did not reconstruct")
    omitted_mass = item_mass - retained_item_mass
    if omitted_mass >= vertex_count:
        raise RuntimeError("Fourier-tail knapsack did not meet the strict tail test")

    certificate = _certificate_from_coefficients(
        selected_coefficients,
        checked,
        dimension,
        WALSH_BASIS,
    )
    if int(certificate["head_count"]) != optimal_cost:
        raise RuntimeError("Fourier-tail compiler cost disagrees with the knapsack")
    diagnostics = {
        "status": "verified-optimal-fourier-tail-certificate",
        "basis": WALSH_BASIS,
        "unnormalized_omitted_mass": omitted_mass,
        "strict_tail_threshold": vertex_count,
        "target_retained_item_mass": target_mass,
        "retained_item_mass": retained_item_mass,
        "support_size": len(certificate["terms"]),
        "head_count": int(certificate["head_count"]),
        "maximum_knapsack_cost": maximum_cost,
        "estimated_dp_transitions": estimated_transitions,
        "actual_dp_transitions": actual_transitions,
        "optimal_within_absolute_tail_criterion": True,
        "floating_failures_are_lower_bounds": False,
    }
    certificate = dict(certificate)
    certificate["search"] = diagnostics.copy()
    report = verify_sparse_ptf_certificate(
        certificate,
        checked,
        dimension,
    )
    if not report["valid"]:
        raise RuntimeError("the optimal Fourier-tail certificate failed verification")
    return certificate, diagnostics


def _deletion_order(
    masks: Sequence[int],
    seed_coefficients: Mapping[int, int],
    basis: str,
    restart: int,
    rng: np.random.Generator,
) -> list[int]:
    nonlinear = [mask for mask in masks if mask.bit_count() >= 2]
    affine = [mask for mask in masks if mask.bit_count() <= 1]
    if restart == 0:
        # First challenge terms used by the exact value interpolation while
        # every initially zero dictionary feature is still available for the
        # LP refit.  This lets the search move to a different sign polynomial
        # rather than remaining trapped in the unique polynomial equal to the
        # labels.  Only then prune the extra nonlinear dictionary features.
        seeded = [mask for mask in nonlinear if seed_coefficients.get(mask, 0)]
        extra = [mask for mask in nonlinear if not seed_coefficients.get(mask, 0)]
        seeded.sort(
            key=lambda mask: (
                abs(seed_coefficients.get(mask, 0))
                / max(1, _compiler_cost([mask], basis)),
                -_compiler_cost([mask], basis),
                mask,
            )
        )
        extra.sort(key=lambda mask: (-_compiler_cost([mask], basis), mask))
        nonlinear = seeded + extra
        affine.sort(key=lambda mask: (abs(seed_coefficients.get(mask, 0)), mask))
    else:
        rng.shuffle(nonlinear)
        rng.shuffle(affine)
    return nonlinear + affine


def sparse_ptf_upper_bound(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    basis: str,
    config: SparsePTFSearchConfig | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Search for and exactly verify a sparse PTF head upper bound.

    The returned certificate is always valid.  When the matrix or LP budget is
    exhausted, the cheaper of the exact full-basis interpolation and the
    verified greedy Fourier-tail seed is returned.
    """
    checked = validate_signs(signs, dimension)
    checked_basis = _validate_basis(basis)
    selected = config or SparsePTFSearchConfig()
    if selected.max_prune_solves < 0:
        raise ValueError("max_prune_solves must be nonnegative")
    if selected.ordering_restarts < 1:
        raise ValueError("ordering_restarts must be positive")
    if selected.max_matrix_entries < 1:
        raise ValueError("max_matrix_entries must be positive")
    if selected.margin_tolerance <= 0:
        raise ValueError("margin_tolerance must be positive")
    if selected.rounding_attempts < 1:
        raise ValueError("rounding_attempts must be positive")

    seed_coefficients = _initial_coefficients(checked, dimension, checked_basis)
    seed_certificate = _certificate_from_coefficients(
        seed_coefficients,
        checked,
        dimension,
        checked_basis,
    )
    seed_report = verify_sparse_ptf_certificate(seed_certificate, checked, dimension)
    if not seed_report["valid"]:
        raise RuntimeError("the exact full-basis seed failed verification")
    tail_certificate: dict[str, Any] | None = None
    tail_diagnostics: dict[str, Any] | None = None
    if checked_basis == WALSH_BASIS:
        tail_certificate, tail_diagnostics = fourier_tail_upper_bound(
            checked,
            dimension,
        )
    initial_certificate = min(
        [
            candidate
            for candidate in (seed_certificate, tail_certificate)
            if candidate is not None
        ],
        key=_certificate_key,
    )
    initial_source = (
        "fourier-tail-seed"
        if tail_certificate is not None
        and _certificate_key(tail_certificate) < _certificate_key(seed_certificate)
        else "safe-full-basis-interpolation"
    )

    # Search the whole basis, not only the support of the unique polynomial
    # equal to the labels.  A much sparser sign polynomial may require features
    # whose exact-interpolation coefficient is zero.  The matrix budget below
    # keeps this full dictionary bounded.
    initial_masks = list(range(1 << dimension))
    diagnostics: dict[str, Any] = {
        "status": "verified-seed-certificate",
        "basis": checked_basis,
        "initial_support_size": len(seed_certificate["terms"]),
        "initial_dictionary_size": len(initial_masks),
        "initial_head_count": int(seed_certificate["head_count"]),
        "fourier_tail_seed": tail_diagnostics,
        "matrix_entries": (1 << dimension) * len(initial_masks),
        "ordering_restarts": selected.ordering_restarts,
        "max_prune_solves_per_restart": selected.max_prune_solves,
        "lp_solves": 0,
        "successful_deletions": 0,
        "exactified_candidates": 0,
        "floating_failures_are_lower_bounds": False,
    }
    matrix_entries = int(diagnostics["matrix_entries"])
    if selected.max_prune_solves == 0:
        diagnostics["status"] = "pruning-disabled"
        diagnostics["final_support_size"] = len(initial_certificate["terms"])
        diagnostics["final_head_count"] = int(initial_certificate["head_count"])
        diagnostics["certificate_source"] = initial_source
        selected_certificate = dict(initial_certificate)
        selected_certificate["search"] = diagnostics.copy()
        return selected_certificate, diagnostics
    if matrix_entries > selected.max_matrix_entries:
        diagnostics["status"] = "pruning-skipped-matrix-budget"
        diagnostics["final_support_size"] = len(initial_certificate["terms"])
        diagnostics["final_head_count"] = int(initial_certificate["head_count"])
        diagnostics["certificate_source"] = initial_source
        selected_certificate = dict(initial_certificate)
        selected_certificate["search"] = diagnostics.copy()
        return selected_certificate, diagnostics

    full_features = _feature_matrix(initial_masks, dimension, checked_basis)
    index_by_mask = {mask: index for index, mask in enumerate(initial_masks)}
    best = initial_certificate
    best_source = initial_source
    rng = np.random.default_rng(selected.seed)

    for restart in range(selected.ordering_restarts):
        active_indices = list(range(len(initial_masks)))
        active_masks = initial_masks.copy()
        current_solution: tuple[np.ndarray, float] | None = None
        deletions = 0
        order = _deletion_order(
            initial_masks,
            seed_coefficients,
            checked_basis,
            restart,
            rng,
        )
        for mask in order[: selected.max_prune_solves]:
            position = index_by_mask[mask]
            if position not in active_indices or len(active_indices) <= 1:
                continue
            trial_indices = [index for index in active_indices if index != position]
            trial_features = full_features[:, trial_indices]
            diagnostics["lp_solves"] += 1
            solution = _maximum_margin_separator(
                trial_features,
                checked.astype(float),
                selected.margin_tolerance,
            )
            if solution is None:
                continue
            active_indices = trial_indices
            active_masks = [initial_masks[index] for index in active_indices]
            current_solution = solution
            deletions += 1
            diagnostics["successful_deletions"] += 1

        if not deletions or current_solution is None:
            continue
        candidate = _exactify_floating_separator(
            active_masks,
            full_features[:, active_indices],
            current_solution[0],
            checked,
            dimension,
            checked_basis,
            selected.rounding_attempts,
        )
        if candidate is None:
            continue
        diagnostics["exactified_candidates"] += 1
        if _certificate_key(candidate) < _certificate_key(best):
            best = candidate
            best_source = "deletion-refit"

    diagnostics["final_support_size"] = len(best["terms"])
    diagnostics["final_head_count"] = int(best["head_count"])
    diagnostics["status"] = (
        "verified-pruned-certificate"
        if best_source == "deletion-refit"
        else "verified-seed-certificate"
    )
    diagnostics["certificate_source"] = best_source
    best = dict(best)
    best["search"] = diagnostics.copy()
    report = verify_sparse_ptf_certificate(best, checked, dimension)
    if not report["valid"]:
        raise RuntimeError("the selected sparse PTF certificate failed verification")
    return best, diagnostics


def column_generation_sparse_ptf_upper_bound(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    basis: str,
    config: SparsePTFColumnGenerationConfig | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Search an implicit basis by transform-priced column generation.

    The restricted master has a free affine block, split weighted-L1
    coefficients for generated nonlinear columns, and one artificial feature
    equal to the label vector.  A Walsh-Hadamard or superset-zeta transform
    prices every nonlinear basis feature without materializing the full square
    feature dictionary.  Floating search output is used only after support
    refitting, integer rounding, and exact certificate verification.

    The exact full-basis label interpolation is retained as a safe fallback.
    Failure to generate or exactify a better certificate is never interpreted
    as a lower bound.
    """
    checked = validate_signs(signs, dimension)
    checked_basis = _validate_basis(basis)
    selected = config or SparsePTFColumnGenerationConfig()
    if selected.max_iterations < 1:
        raise ValueError("max_iterations must be positive")
    if selected.batch_size < 1:
        raise ValueError("batch_size must be positive")
    if selected.max_columns < 0:
        raise ValueError("max_columns must be nonnegative")
    if selected.pricing_tolerance <= 0:
        raise ValueError("pricing_tolerance must be positive")
    if selected.artificial_tolerance <= 0:
        raise ValueError("artificial_tolerance must be positive")
    if selected.coefficient_tolerance <= 0:
        raise ValueError("coefficient_tolerance must be positive")
    if selected.margin_tolerance <= 0:
        raise ValueError("margin_tolerance must be positive")
    if selected.rounding_attempts < 1:
        raise ValueError("rounding_attempts must be positive")

    vertex_count = 1 << dimension
    seed_coefficients = _initial_coefficients(checked, dimension, checked_basis)
    seed_certificate = _certificate_from_coefficients(
        seed_coefficients,
        checked,
        dimension,
        checked_basis,
    )
    seed_report = verify_sparse_ptf_certificate(seed_certificate, checked, dimension)
    if not seed_report["valid"]:
        raise RuntimeError("the exact full-basis seed failed verification")
    tail_certificate: dict[str, Any] | None = None
    tail_diagnostics: dict[str, Any] | None = None
    if checked_basis == WALSH_BASIS:
        tail_certificate, tail_diagnostics = fourier_tail_upper_bound(
            checked,
            dimension,
        )

    full_weighted_l1_bound = _full_weighted_l1_bound(
        seed_coefficients,
        dimension,
        checked_basis,
    )
    artificial_penalty = full_weighted_l1_bound + 1.0
    diagnostics: dict[str, Any] = {
        "status": "not-started",
        "basis": checked_basis,
        "pricing_method": (
            "superset-zeta" if checked_basis == MONOTONE_BASIS else "fwht"
        ),
        "full_dictionary_size": vertex_count,
        "full_dictionary_entries": vertex_count * vertex_count,
        "full_dictionary_materialized": False,
        "initial_support_size": len(seed_certificate["terms"]),
        "initial_head_count": int(seed_certificate["head_count"]),
        "fourier_tail_seed": tail_diagnostics,
        "full_weighted_l1_bound": full_weighted_l1_bound,
        "phase_one_penalty": artificial_penalty,
        "restricted_master_solves": 0,
        "candidate_refit_lp_solves": 0,
        "pricing_passes": 0,
        "columns_added": 0,
        "exactified_candidates": 0,
        "max_restricted_matrix_entries": 0,
        "artificial_values": [],
        "maximum_pricing_ratios": [],
        "pricing_violation_counts": [],
        "floating_failures_are_lower_bounds": False,
    }
    if not math.isfinite(artificial_penalty):
        diagnostics["status"] = "phase-one-penalty-not-finite"
        diagnostics["active_columns"] = 0
        diagnostics["final_artificial_value"] = None
        diagnostics["final_support_size"] = len(seed_certificate["terms"])
        diagnostics["final_head_count"] = int(seed_certificate["head_count"])
        diagnostics["certificate_source"] = "safe-full-basis-interpolation"
        diagnostics["safe_full_basis_fallback_used"] = True
        best_fallback = min(
            [
                candidate
                for candidate in (seed_certificate, tail_certificate)
                if candidate is not None
            ],
            key=_certificate_key,
        )
        diagnostics["final_support_size"] = len(best_fallback["terms"])
        diagnostics["final_head_count"] = int(best_fallback["head_count"])
        diagnostics["certificate_source"] = (
            "fourier-tail-seed"
            if tail_certificate is not None
            and _certificate_key(tail_certificate) < _certificate_key(seed_certificate)
            else "safe-full-basis-interpolation"
        )
        diagnostics["safe_full_basis_fallback_used"] = (
            diagnostics["certificate_source"] == "safe-full-basis-interpolation"
        )
        best_fallback = dict(best_fallback)
        best_fallback["search"] = diagnostics.copy()
        return best_fallback, diagnostics

    affine_masks = [0] + [1 << coordinate for coordinate in range(dimension)]
    affine_features = _feature_matrix(affine_masks, dimension, checked_basis)
    active_masks: list[int] = []
    active_set: set[int] = set()
    if (
        tail_certificate is not None
        and _certificate_key(tail_certificate) < _certificate_key(seed_certificate)
    ):
        best = tail_certificate
        best_source = "fourier-tail-seed"
    else:
        best = seed_certificate
        best_source = "safe-full-basis-interpolation"
    last_artificial: float | None = None

    for solve_index in range(selected.max_iterations):
        nonlinear_features = (
            _feature_matrix(active_masks, dimension, checked_basis)
            if active_masks
            else np.empty((vertex_count, 0), dtype=float)
        )
        master = _solve_column_master(
            checked.astype(float),
            affine_features,
            nonlinear_features,
            active_masks,
            checked_basis,
            artificial_penalty,
        )
        diagnostics["restricted_master_solves"] += 1
        if master is None:
            diagnostics["status"] = "restricted-master-failed"
            break
        diagnostics["max_restricted_matrix_entries"] = max(
            int(diagnostics["max_restricted_matrix_entries"]),
            int(master["matrix_entries"]),
        )
        last_artificial = float(master["artificial_value"])
        diagnostics["artificial_values"].append(last_artificial)
        diagnostics.setdefault("real_margins", []).append(float(master["real_margin"]))
        diagnostics.setdefault("dual_masses", []).append(float(master["dual_mass"]))
        diagnostics.setdefault("affine_dual_residuals", []).append(
            float(master["affine_dual_residual"])
        )

        if float(master["real_margin"]) > selected.margin_tolerance:
            candidate, refit_solves = _refit_column_candidate(
                checked,
                dimension,
                checked_basis,
                affine_masks,
                active_masks,
                master["nonlinear_coefficients"],
                selected.coefficient_tolerance,
                selected.margin_tolerance,
                selected.rounding_attempts,
            )
            diagnostics["candidate_refit_lp_solves"] += refit_solves
            if candidate is not None:
                diagnostics["exactified_candidates"] += 1
                if _certificate_key(candidate) < _certificate_key(best):
                    best = candidate
                    best_source = "generated-support-refit"

        pricing = _price_nonlinear_columns(
            master["dual_weights"],
            checked.astype(float),
            dimension,
            checked_basis,
            active_set,
            selected.batch_size,
            selected.pricing_tolerance,
        )
        diagnostics["pricing_passes"] += 1
        diagnostics["maximum_pricing_ratios"].append(
            float(pricing["maximum_ratio"])
        )
        diagnostics["pricing_violation_counts"].append(
            int(pricing["violation_count"])
        )

        if int(pricing["violation_count"]) == 0:
            diagnostics["status"] = (
                "pricing-optimal-artificial-eliminated"
                if last_artificial <= selected.artificial_tolerance
                else "pricing-optimal-artificial-positive"
            )
            break
        if len(active_masks) >= selected.max_columns:
            diagnostics["status"] = "column-budget-exhausted"
            break
        if solve_index + 1 >= selected.max_iterations:
            diagnostics["status"] = "iteration-budget-exhausted"
            break

        available_slots = selected.max_columns - len(active_masks)
        additions = list(pricing["masks"][:available_slots])
        if not additions:
            diagnostics["status"] = "column-budget-exhausted"
            break
        active_masks.extend(additions)
        active_set.update(additions)
        diagnostics["columns_added"] += len(additions)
    else:
        diagnostics["status"] = "iteration-budget-exhausted"

    diagnostics["active_columns"] = len(active_masks)
    diagnostics["final_artificial_value"] = last_artificial
    diagnostics["final_support_size"] = len(best["terms"])
    diagnostics["final_head_count"] = int(best["head_count"])
    diagnostics["certificate_source"] = best_source
    diagnostics["safe_full_basis_fallback_used"] = (
        best_source == "safe-full-basis-interpolation"
    )
    best = dict(best)
    best["search"] = diagnostics.copy()
    report = verify_sparse_ptf_certificate(best, checked, dimension)
    if not report["valid"]:
        raise RuntimeError("the column-generation certificate failed verification")
    return best, diagnostics


def column_generation_sparse_ptf_portfolio(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    config: SparsePTFColumnGenerationConfig | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run transform-priced column generation in both compiler bases."""
    selected = config or SparsePTFColumnGenerationConfig()
    attempts = []
    certificates = []
    for basis in SUPPORTED_BASES:
        certificate, diagnostics = column_generation_sparse_ptf_upper_bound(
            signs,
            dimension,
            basis=basis,
            config=selected,
        )
        certificates.append(certificate)
        attempts.append(diagnostics)
    best = min(certificates, key=_certificate_key)
    portfolio = {
        "status": "verified-certificate-found",
        "selected_basis": best["basis"],
        "head_count": int(best["head_count"]),
        "attempts": attempts,
        "full_dictionary_materialized": False,
        "floating_failures_are_lower_bounds": False,
    }
    best = dict(best)
    best["portfolio"] = portfolio.copy()
    report = verify_sparse_ptf_certificate(best, signs, dimension)
    if not report["valid"]:
        raise RuntimeError(
            "the column-generation portfolio selected an invalid certificate"
        )
    return best, portfolio


def sparse_ptf_portfolio(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    config: SparsePTFSearchConfig | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run both compiler bases and return the cheaper exact certificate."""
    selected = config or SparsePTFSearchConfig()
    attempts = []
    certificates = []
    for offset, basis in enumerate(SUPPORTED_BASES):
        basis_config = replace(selected, seed=selected.seed + 1009 * offset)
        certificate, diagnostics = sparse_ptf_upper_bound(
            signs,
            dimension,
            basis=basis,
            config=basis_config,
        )
        certificates.append(certificate)
        attempts.append(diagnostics)
    best = min(certificates, key=_certificate_key)
    portfolio = {
        "status": "verified-certificate-found",
        "selected_basis": best["basis"],
        "head_count": int(best["head_count"]),
        "attempts": attempts,
        "floating_failures_are_lower_bounds": False,
    }
    best = dict(best)
    best["portfolio"] = portfolio.copy()
    report = verify_sparse_ptf_certificate(best, signs, dimension)
    if not report["valid"]:
        raise RuntimeError("the sparse PTF portfolio selected an invalid certificate")
    return best, portfolio


__all__ = [
    "MONOTONE_BASIS",
    "WALSH_BASIS",
    "SUPPORTED_BASES",
    "FourierTailBudgetExceeded",
    "SparsePTFColumnGenerationConfig",
    "SparsePTFSearchConfig",
    "fourier_tail_upper_bound",
    "optimal_fourier_tail_upper_bound",
    "column_generation_sparse_ptf_upper_bound",
    "column_generation_sparse_ptf_portfolio",
    "sparse_ptf_upper_bound",
    "sparse_ptf_portfolio",
    "verify_sparse_ptf_certificate",
]
