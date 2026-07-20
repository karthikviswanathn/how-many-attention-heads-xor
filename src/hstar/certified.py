"""Anytime certified interval estimation for Boolean head complexity.

The public estimator never interprets a failed numerical search as a lower
bound.  It combines exact or theorem-backed lower bounds, theorem-backed upper
bounds, exactly verified numerical upper certificates, and an optional exact
QF_NRA decision layer.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from .boolean_cube import (
    VERTEX_ORDER,
    cube,
    mask_from_signs,
    monomial_matrix,
    validate_signs,
)
from .fractional import (
    exact_fixed_denominator_certificate,
    literal_weights_to_affine,
    random_denominator_search,
    verify_head_certificate,
)
from .exact_linear import verify_gordan_obstruction, verify_threshold_polynomial
from .sparse_ptf import (
    FourierTailBudgetExceeded,
    SparsePTFColumnGenerationConfig,
    column_generation_sparse_ptf_portfolio,
    optimal_fourier_tail_upper_bound,
    verify_sparse_ptf_certificate,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _z3_module():
    try:
        import z3  # type: ignore
    except ImportError:
        return None
    return z3


def largest_parity_restriction(
    signs: np.ndarray | list[int], dimension: int
) -> dict[str, Any]:
    """Find the largest subcube on which the function is parity or its negation."""
    checked = validate_signs(signs, dimension)
    coordinates = tuple(range(dimension))
    for free_count in range(dimension, 0, -1):
        for free in itertools.combinations(coordinates, free_count):
            free_set = set(free)
            fixed = tuple(value for value in coordinates if value not in free_set)
            for fixed_code in range(1 << len(fixed)):
                base_code = sum(
                    ((fixed_code >> position) & 1) << coordinate
                    for position, coordinate in enumerate(fixed)
                )
                common = None
                valid = True
                for free_code in range(1 << free_count):
                    code = base_code + sum(
                        ((free_code >> position) & 1) << coordinate
                        for position, coordinate in enumerate(free)
                    )
                    parity_sign = -1 if free_code.bit_count() % 2 else 1
                    current = int(checked[code]) * parity_sign
                    if common is None:
                        common = current
                    elif current != common:
                        valid = False
                        break
                if valid:
                    fixed_values = {
                        str(coordinate): (fixed_code >> position) & 1
                        for position, coordinate in enumerate(fixed)
                    }
                    return {
                        "dimension": free_count,
                        "free_coordinates": list(free),
                        "fixed_coordinates": fixed_values,
                        "parity_sign_at_free_zero": int(common),
                    }
    return {"dimension": 0}


def _canonical_partition_coordinates(
    dimension: int,
) -> list[tuple[int, ...]]:
    """List nontrivial coordinate bipartitions once, balanced first."""
    candidates = []
    for size in range(1, dimension // 2 + 1):
        for subset in itertools.combinations(range(dimension), size):
            if 2 * size == dimension and 0 not in subset:
                continue
            candidates.append(subset)
    candidates.sort(key=lambda subset: (abs(dimension - 2 * len(subset)), subset))
    return candidates


def _embedded_local_codes(
    local_codes: np.ndarray,
    coordinates: tuple[int, ...],
) -> np.ndarray:
    result = np.zeros(len(local_codes), dtype=np.int64)
    for position, coordinate in enumerate(coordinates):
        result |= ((local_codes >> position) & 1) << coordinate
    return result


def _evenly_spaced_codes(count: int, limit: int) -> np.ndarray:
    if count <= limit:
        return np.arange(count, dtype=np.int64)
    return np.array(
        [(index * count) // limit for index in range(limit)],
        dtype=np.int64,
    )


def _partition_submatrix(
    signs: np.ndarray,
    dimension: int,
    row_coordinates: tuple[int, ...],
    row_codes: np.ndarray,
    column_codes: np.ndarray,
) -> np.ndarray:
    row_set = set(row_coordinates)
    column_coordinates = tuple(
        coordinate for coordinate in range(dimension) if coordinate not in row_set
    )
    embedded_rows = _embedded_local_codes(row_codes, row_coordinates)
    embedded_columns = _embedded_local_codes(column_codes, column_coordinates)
    return signs[embedded_rows[:, None] | embedded_columns[None, :]]


def _ceil_square_root_ratio(numerator: int, denominator: int) -> int:
    if numerator <= 0 or denominator <= 0:
        raise ValueError("square-root ratio must be positive")
    result = math.isqrt(numerator // denominator)
    if result * result * denominator < numerator:
        result += 1
    return max(1, result)


def _head_lower_bound_from_sign_rank(sign_rank: int) -> int:
    if sign_rank < 1:
        raise ValueError("sign-rank must be positive")
    ceiling_log = (sign_rank + 1).bit_length()
    return max(1, ceiling_log - 1)


def _forster_witness_for_partition(
    signs: np.ndarray,
    dimension: int,
    row_coordinates: tuple[int, ...],
    max_side: int,
) -> dict[str, Any]:
    row_count = 1 << len(row_coordinates)
    column_count = 1 << (dimension - len(row_coordinates))
    row_codes = _evenly_spaced_codes(row_count, max_side)
    column_codes = _evenly_spaced_codes(column_count, max_side)
    matrix = _partition_submatrix(
        signs,
        dimension,
        row_coordinates,
        row_codes,
        column_codes,
    ).astype(np.int64)
    if matrix.shape[0] <= matrix.shape[1]:
        gram = matrix @ matrix.T
        gram_side = "rows"
    else:
        gram = matrix.T @ matrix
        gram_side = "columns"
    spectral_squared_upper = int(np.max(np.sum(np.abs(gram), axis=1)))
    forster_numerator = int(matrix.shape[0] * matrix.shape[1])
    sign_rank_lower = _ceil_square_root_ratio(
        forster_numerator,
        spectral_squared_upper,
    )
    return {
        "head_lower_bound": _head_lower_bound_from_sign_rank(sign_rank_lower),
        "sign_rank_lower_bound": sign_rank_lower,
        "row_coordinates": list(row_coordinates),
        "column_coordinates": [
            coordinate
            for coordinate in range(dimension)
            if coordinate not in set(row_coordinates)
        ],
        "full_matrix_shape": [row_count, column_count],
        "submatrix_shape": list(matrix.shape),
        "submatrix_row_codes": [int(value) for value in row_codes],
        "submatrix_column_codes": [int(value) for value in column_codes],
        "gram_side": gram_side,
        "spectral_norm_squared_upper_bound": spectral_squared_upper,
        "forster_numerator": forster_numerator,
        "theorem": (
            "Forster spectral sign-rank bound plus the tangential "
            "rank cap 2^(H+1)-2"
        ),
    }


def partition_forster_lower_bound(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    partition_limit: int = 64,
    max_side: int = 128,
) -> dict[str, Any]:
    """Search coordinate partitions for a portable spectral lower bound.

    The spectral norm is bounded using an exact Gershgorin row sum on a Gram
    matrix.  When a partition side is larger than ``max_side``, the witness
    uses a deterministic submatrix, whose sign-rank still lower-bounds that of
    the full partition matrix.
    """
    checked = validate_signs(signs, dimension)
    if partition_limit < 0:
        raise ValueError("partition_limit must be nonnegative")
    if max_side < 1:
        raise ValueError("max_side must be positive")
    candidates = _canonical_partition_coordinates(dimension)
    selected = candidates[:partition_limit]
    if not selected:
        return {
            "head_lower_bound": 0,
            "sign_rank_lower_bound": 0,
            "partitions_checked": 0,
            "total_canonical_partitions": len(candidates),
            "partition_search_exhaustive": not candidates,
        }
    witnesses = [
        _forster_witness_for_partition(
            checked,
            dimension,
            row_coordinates,
            max_side,
        )
        for row_coordinates in selected
    ]
    best = max(
        witnesses,
        key=lambda witness: (
            int(witness["head_lower_bound"]),
            int(witness["sign_rank_lower_bound"]),
            -int(witness["spectral_norm_squared_upper_bound"]),
        ),
    )
    return {
        **best,
        "partitions_checked": len(selected),
        "total_canonical_partitions": len(candidates),
        "partition_search_exhaustive": len(selected) == len(candidates),
        "max_submatrix_side": max_side,
    }


def verify_partition_forster_witness(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
    dimension: int,
) -> dict[str, Any]:
    """Verify a Forster and exact-Gram partition witness from integers only."""
    checked = validate_signs(signs, dimension)
    try:
        row_coordinates = tuple(int(value) for value in certificate["row_coordinates"])
        if (
            not row_coordinates
            or len(row_coordinates) >= dimension
            or len(set(row_coordinates)) != len(row_coordinates)
            or any(value < 0 or value >= dimension for value in row_coordinates)
        ):
            raise ValueError
        row_codes = np.array(certificate["submatrix_row_codes"], dtype=np.int64)
        column_codes = np.array(
            certificate["submatrix_column_codes"],
            dtype=np.int64,
        )
        if (
            row_codes.ndim != 1
            or column_codes.ndim != 1
            or len(row_codes) == 0
            or len(column_codes) == 0
            or len(set(int(value) for value in row_codes)) != len(row_codes)
            or len(set(int(value) for value in column_codes)) != len(column_codes)
            or np.any(row_codes < 0)
            or np.any(row_codes >= 1 << len(row_coordinates))
            or np.any(column_codes < 0)
            or np.any(column_codes >= 1 << (dimension - len(row_coordinates)))
        ):
            raise ValueError
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "malformed partition witness"}

    matrix = _partition_submatrix(
        checked,
        dimension,
        row_coordinates,
        row_codes,
        column_codes,
    ).astype(np.int64)
    if matrix.shape[0] <= matrix.shape[1]:
        gram = matrix @ matrix.T
        gram_side = "rows"
    else:
        gram = matrix.T @ matrix
        gram_side = "columns"
    spectral_squared_upper = int(np.max(np.sum(np.abs(gram), axis=1)))
    forster_numerator = int(matrix.shape[0] * matrix.shape[1])
    sign_rank_lower = _ceil_square_root_ratio(
        forster_numerator,
        spectral_squared_upper,
    )
    head_lower = _head_lower_bound_from_sign_rank(sign_rank_lower)
    expected = {
        "submatrix_shape": list(matrix.shape),
        "gram_side": gram_side,
        "spectral_norm_squared_upper_bound": spectral_squared_upper,
        "forster_numerator": forster_numerator,
        "sign_rank_lower_bound": sign_rank_lower,
        "head_lower_bound": head_lower,
    }
    for key, value in expected.items():
        if certificate.get(key) != value:
            return {"valid": False, "reason": f"partition witness mismatch: {key}"}
    return {
        "valid": True,
        "head_lower_bound": head_lower,
        "sign_rank_lower_bound": sign_rank_lower,
        "submatrix_shape": list(matrix.shape),
        "spectral_norm_squared_upper_bound": spectral_squared_upper,
    }


def projection_sign_change_upper_bound(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    permutation_limit: int = 720,
    seed: int = 0,
) -> dict[str, Any]:
    """Optimize the rigorous positive-projection sign-change construction."""
    checked = validate_signs(signs, dimension)
    points = cube(dimension)

    def evaluate_weights(weights: list[int]) -> tuple[int, int] | None:
        level_labels: dict[int, int] = {}
        levels = points @ np.array(weights, dtype=np.int64)
        for code, level in enumerate(levels):
            integer_level = int(level)
            label = int(checked[code])
            previous = level_labels.get(integer_level)
            if previous is not None and previous != label:
                return None
            level_labels[integer_level] = label
        profile = [level_labels[level] for level in sorted(level_labels)]
        changes = sum(left != right for left, right in zip(profile, profile[1:]))
        return changes, len(profile)

    identity = tuple(range(dimension))
    factorial = math.factorial(dimension)
    if factorial <= max(1, permutation_limit):
        permutations: Iterable[tuple[int, ...]] = itertools.permutations(range(dimension))
        exhaustive = True
        planned = factorial
    else:
        rng = np.random.default_rng(seed)
        selected = {identity}
        target = max(1, permutation_limit)
        while len(selected) < target:
            selected.add(tuple(int(value) for value in rng.permutation(dimension)))
        permutations = sorted(selected)
        exhaustive = False
        planned = len(selected)
    permutation_list = list(permutations)

    equal_weights = [1] * dimension
    equal_result = evaluate_weights(equal_weights)
    best_count = equal_result[0] if equal_result is not None else 1 << dimension
    best_permutation = identity
    best_weights = (
        equal_weights
        if equal_result is not None
        else [1 << i for i in range(dimension)]
    )
    best_levels = equal_result[1] if equal_result is not None else 1 << dimension
    best_family = "equal weights" if equal_result is not None else "binary weights"
    checked_count = 0
    candidate_count = 1
    layered_offset = 1 << dimension
    for permutation in permutation_list:
        perturbations = [0] * dimension
        for position, coordinate in enumerate(permutation):
            perturbations[coordinate] = 1 << position
        candidates = (
            ("binary weights", perturbations),
            (
                "Hamming-layered binary weights",
                [layered_offset + value for value in perturbations],
            ),
        )
        checked_count += 1
        for family, weights in candidates:
            result = evaluate_weights(weights)
            if result is None:
                raise RuntimeError(f"injective {family} failed to factor the truth table")
            changes, levels = result
            candidate_count += 1
            if changes < best_count:
                best_count = changes
                best_permutation = permutation
                best_weights = weights
                best_levels = levels
                best_family = family
        if best_count == 1:
            break
    return {
        "upper_bound": best_count,
        "positive_integer_weights": best_weights,
        "projection_family": best_family,
        "distinct_projection_levels": best_levels,
        "coordinate_permutation": list(best_permutation),
        "permutations_checked": checked_count,
        "projection_candidates_checked": candidate_count,
        "planned_permutations": planned,
        "permutation_search_exhaustive": exhaustive and checked_count == factorial,
        "theorem": "positive projection sign changes",
    }


def verify_projection_witness(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
    dimension: int,
) -> dict[str, Any]:
    """Verify a positive-projection sign-change witness with integer arithmetic."""
    checked = validate_signs(signs, dimension)
    try:
        raw_weights = certificate["positive_integer_weights"]
        archived_bound = int(certificate["upper_bound"])
        if archived_bound != certificate["upper_bound"]:
            raise ValueError
        if not isinstance(raw_weights, list) or len(raw_weights) != dimension:
            raise ValueError
        weights = []
        for value in raw_weights:
            if isinstance(value, (bool, np.bool_)):
                raise ValueError
            integer = int(value)
            if integer != value or integer <= 0:
                raise ValueError
            weights.append(integer)
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"valid": False, "reason": "malformed projection certificate"}

    level_labels: dict[int, int] = {}
    for code, point in enumerate(cube(dimension)):
        level = sum(int(point[index]) * weights[index] for index in range(dimension))
        label = int(checked[code])
        previous = level_labels.get(level)
        if previous is not None and previous != label:
            return {
                "valid": False,
                "reason": "opposite labels collide at one projection level",
                "collision_level": level,
            }
        level_labels[level] = label
    ordered_levels = sorted(level_labels)
    profile = [level_labels[level] for level in ordered_levels]
    transitions = [
        index
        for index, (left, right) in enumerate(zip(profile, profile[1:]), start=1)
        if left != right
    ]
    changes = len(transitions)
    archived_levels = certificate.get("distinct_projection_levels")
    if archived_levels is not None and archived_levels != len(ordered_levels):
        return {"valid": False, "reason": "archived projection level count mismatch"}
    if archived_bound != changes:
        return {"valid": False, "reason": "archived sign-change count mismatch"}
    return {
        "valid": True,
        "upper_bound": changes,
        "distinct_projection_levels": len(ordered_levels),
        "transition_positions": transitions,
        "ordered_levels": ordered_levels,
        "ordered_labels": profile,
    }


def exact_threshold_degree(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    timeout_milliseconds: int = 30_000,
    export_directory: str | Path | None = None,
) -> dict[str, Any]:
    """Compute threshold degree through exact QF_LRA decisions in Z3.

    Every unsatisfiable lower-degree instance is an exact solver decision.
    The first satisfiable instance is also converted to an independently
    checkable integer sign-polynomial certificate.
    """
    checked = validate_signs(signs, dimension)
    z3 = _z3_module()
    if z3 is None:
        return {
            "status": "backend-unavailable",
            "backend": "z3 QF_LRA",
            "degree_lower_bound": 0,
            "degree_upper_bound": dimension,
            "checks": [],
        }
    export_path = Path(export_directory) if export_directory is not None else None
    if export_path is not None:
        export_path.mkdir(parents=True, exist_ok=True)

    lower = 0
    checks: list[dict[str, Any]] = []
    unknown_degrees: list[int] = []
    lower_certificates: list[dict[str, Any]] = []
    first_upper = dimension
    upper_certificate = None
    for degree in range(dimension + 1):
        matrix, monomials = monomial_matrix(dimension, degree)
        variables = [
            z3.Real(f"threshold_d{degree}_c{column}")
            for column in range(matrix.shape[1])
        ]
        solver = z3.SolverFor("QF_LRA")
        if timeout_milliseconds > 0:
            solver.set(timeout=timeout_milliseconds)
        for row in range(len(checked)):
            polynomial = z3.Sum(
                [int(matrix[row, column]) * variables[column] for column in range(matrix.shape[1])]
            )
            solver.add(int(checked[row]) * polynomial >= 1)
        exported = None
        if export_path is not None:
            exported_path = export_path / f"threshold_degree_{degree}.smt2"
            exported_path.write_text(solver.sexpr() + "\n")
            exported = str(exported_path)
        result = solver.check()
        entry: dict[str, Any] = {"degree": degree, "result": str(result)}
        if exported is not None:
            entry["smt2"] = exported
        if result == z3.unsat:
            dual_weights = [
                z3.Real(f"threshold_d{degree}_q{row}")
                for row in range(len(checked))
            ]
            dual = z3.SolverFor("QF_LRA")
            if timeout_milliseconds > 0:
                dual.set(timeout=timeout_milliseconds)
            dual.add(*(weight >= 0 for weight in dual_weights))
            dual.add(z3.Sum(dual_weights) == 1)
            for column in range(matrix.shape[1]):
                dual.add(
                    z3.Sum(
                        [
                            int(checked[row])
                            * int(matrix[row, column])
                            * dual_weights[row]
                            for row in range(len(checked))
                        ]
                    )
                    == 0
                )
            dual_result = dual.check()
            if dual_result != z3.sat:
                raise RuntimeError(
                    "primal threshold system was unsatisfiable but its exact "
                    "Gordan alternative was not satisfiable"
                )
            dual_model = dual.model()
            rational_weights = [
                dual_model.eval(weight, model_completion=True)
                for weight in dual_weights
            ]
            if not all(z3.is_rational_value(value) for value in rational_weights):
                raise RuntimeError("QF_LRA returned a non-rational dual value")
            weight_scale = math.lcm(
                *[value.denominator_as_long() for value in rational_weights]
            )
            integer_weights = [
                value.numerator_as_long()
                * (weight_scale // value.denominator_as_long())
                for value in rational_weights
            ]
            positive_weights = [value for value in integer_weights if value > 0]
            divisor = math.gcd(*positive_weights)
            integer_weights = [value // divisor for value in integer_weights]
            gordan_certificate = {
                "degree": degree,
                "support": [
                    {"vertex": row, "weight": int(weight)}
                    for row, weight in enumerate(integer_weights)
                    if weight > 0
                ],
                "total_weight": int(sum(integer_weights)),
            }
            gordan_report = verify_gordan_obstruction(
                gordan_certificate,
                checked,
                dimension,
            )
            if not gordan_report["valid"]:
                raise RuntimeError("failed to verify the extracted Gordan certificate")
            entry["gordan_certificate"] = gordan_certificate
            entry["gordan_verification"] = gordan_report
            lower_certificates.append(gordan_certificate)
            lower = max(lower, degree + 1)
        elif result == z3.unknown:
            entry["reason"] = solver.reason_unknown()
            unknown_degrees.append(degree)
        else:
            first_upper = degree
            model = solver.model()
            rationals = [model.eval(variable, model_completion=True) for variable in variables]
            if not all(z3.is_rational_value(value) for value in rationals):
                raise RuntimeError("QF_LRA returned a non-rational model value")
            denominators = [value.denominator_as_long() for value in rationals]
            scale = math.lcm(*denominators)
            coefficients = [
                value.numerator_as_long() * (scale // value.denominator_as_long())
                for value in rationals
            ]
            divisor = math.gcd(*[abs(value) for value in coefficients if value != 0])
            if divisor > 1:
                coefficients = [value // divisor for value in coefficients]
            signed_values = checked.astype(object) * (
                matrix.astype(object) @ np.array(coefficients, dtype=object)
            )
            if min(signed_values) <= 0:
                raise RuntimeError("failed to verify the extracted threshold polynomial")
            upper_certificate = {
                "degree": degree,
                "monomials": [list(subset) for subset in monomials],
                "integer_coefficients": coefficients,
                "minimum_signed_value": int(min(signed_values)),
            }
            polynomial_report = verify_threshold_polynomial(
                upper_certificate,
                checked,
                dimension,
            )
            if not polynomial_report["valid"]:
                raise RuntimeError(
                    "failed to independently verify the threshold polynomial"
                )
            entry["polynomial_verification"] = polynomial_report
            checks.append(entry)
            break
        checks.append(entry)

    exact = lower == first_upper
    return {
        "status": "exact" if exact else "interval",
        "backend": "z3 QF_LRA",
        "degree_lower_bound": lower,
        "degree_upper_bound": first_upper,
        "exact_degree": first_upper if exact else None,
        "unknown_degrees": unknown_degrees,
        "checks": checks,
        "lower_certificates": lower_certificates,
        "upper_certificate": upper_certificate,
    }


def _orientation_solver(
    signs: np.ndarray,
    dimension: int,
    heads: int,
    positive_heads: int,
    timeout_milliseconds: int,
):
    z3 = _z3_module()
    if z3 is None:
        raise RuntimeError("z3-solver is required for exact QF_NRA decisions")
    orientations = tuple([-1] * (heads - positive_heads) + [1] * positive_heads)
    points = cube(dimension)
    beta = [
        [z3.Real(f"h{heads}_p{positive_heads}_b{head}_{index}") for index in range(dimension + 1)]
        for head in range(heads)
    ]
    numerators = [
        [z3.Real(f"h{heads}_p{positive_heads}_a{head}_{index}") for index in range(dimension + 1)]
        for head in range(heads)
    ]
    solver = z3.SolverFor("QF_NRA")
    if timeout_milliseconds > 0:
        solver.set(timeout=timeout_milliseconds)
    denominator_values = [[] for _ in range(heads)]
    numerator_values = [[] for _ in range(heads)]
    for head, orientation in enumerate(orientations):
        solver.add(z3.Sum(beta[head]) == 1)
        solver.add(*(value >= 0 for value in beta[head]))
        for point in points:
            literals = point if orientation > 0 else 1 - point
            denominator_values[head].append(
                beta[head][0]
                + z3.Sum(
                    [beta[head][index + 1] * int(literals[index]) for index in range(dimension)]
                )
            )
            numerator_values[head].append(
                numerators[head][0]
                + z3.Sum(
                    [numerators[head][index + 1] * int(point[index]) for index in range(dimension)]
                )
            )
    for row in range(1 << dimension):
        cleared_terms = []
        for head in range(heads):
            product = numerator_values[head][row]
            for other in range(heads):
                if other != head:
                    product *= denominator_values[other][row]
            cleared_terms.append(product)
        solver.add(int(signs[row]) * z3.Sum(cleared_terms) >= 1)
    return solver, orientations, beta


def _model_value_as_float(z3, value) -> float:
    """Convert a rational or real-algebraic Z3 model value to a safe approximation."""
    if z3.is_rational_value(value):
        return value.numerator_as_long() / value.denominator_as_long()
    if z3.is_algebraic_value(value):
        approximation = value.approx(80)
        return approximation.numerator_as_long() / approximation.denominator_as_long()
    rendered = value.as_decimal(50)
    if rendered.endswith("?"):
        rendered = rendered[:-1]
    if rendered.endswith(".0"):
        rendered = rendered[:-2]
    return float(rendered)


def _recover_sat_certificate(
    z3,
    model,
    beta,
    orientations,
    signs: np.ndarray,
    dimension: int,
) -> dict[str, Any] | None:
    """Strictify a solver model, rationalize denominators, and solve the inner LP."""
    theta = np.array(
        [
            [
                _model_value_as_float(
                    z3,
                    model.eval(beta[head][index], model_completion=True),
                )
                for index in range(dimension + 1)
            ]
            for head in range(len(orientations))
        ],
        dtype=float,
    )
    theta = np.maximum(theta, 0.0)
    row_sums = np.sum(theta, axis=1, keepdims=True)
    if np.any(row_sums <= 0):
        return None
    theta /= row_sums
    for epsilon in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        interior = (1.0 - epsilon) * theta + epsilon / (dimension + 1)
        for scale in (10**3, 10**5, 10**7, 10**9):
            weights = np.maximum(1, np.rint(scale * interior)).astype(object)
            denominators = np.vstack(
                [
                    literal_weights_to_affine(weights[head], orientations[head])
                    for head in range(len(orientations))
                ]
            )
            certificate = exact_fixed_denominator_certificate(
                signs,
                dimension,
                denominators,
                orientations,
            )
            if certificate is not None:
                certificate["recovery"] = {
                    "source": "exact QF_NRA model",
                    "strictification_epsilon": epsilon,
                    "denominator_scale": scale,
                }
                return certificate
    return None


def decide_head_feasibility(
    signs: np.ndarray | list[int],
    dimension: int,
    heads: int,
    *,
    timeout_milliseconds: int = 60_000,
    export_directory: str | Path | None = None,
) -> dict[str, Any]:
    """Decide all ``H + 1`` orientation counts as QF_NRA instances.

    ``unsat`` is a global lower certificate relative to the exact solver.  A
    ``sat`` result is a global upper proof.  ``unknown`` changes neither end of
    a certified interval.
    """
    if heads < 1:
        raise ValueError("heads must be positive")
    checked = validate_signs(signs, dimension)
    if _z3_module() is None:
        return {"status": "backend-unavailable", "backend": "z3 QF_NRA", "checks": []}
    export_path = Path(export_directory) if export_directory is not None else None
    if export_path is not None:
        export_path.mkdir(parents=True, exist_ok=True)
    checks = []
    saw_unknown = False
    z3 = _z3_module()
    for positive_heads in range(heads + 1):
        solver, orientations, beta = _orientation_solver(
            checked,
            dimension,
            heads,
            positive_heads,
            timeout_milliseconds,
        )
        exported = None
        if export_path is not None:
            path = export_path / f"heads_{heads}_positive_{positive_heads}.smt2"
            path.write_text(solver.sexpr() + "\n")
            exported = str(path)
        result = solver.check()
        entry: dict[str, Any] = {
            "positive_heads": positive_heads,
            "orientations": list(orientations),
            "result": str(result),
        }
        if exported is not None:
            entry["smt2"] = exported
        if result == z3.sat:
            model = solver.model()
            entry["model"] = model.sexpr()
            certificate = _recover_sat_certificate(
                z3,
                model,
                beta,
                orientations,
                checked,
                dimension,
            )
            if certificate is not None:
                entry["strict_integer_certificate"] = certificate
            checks.append(entry)
            return {
                "status": "sat",
                "backend": "z3 QF_NRA",
                "heads": heads,
                "checks": checks,
                "closure_note": (
                    "every closed-simplex solution with positive cleared margin "
                    "strictifies by finite-cube perturbation"
                ),
                "strict_integer_certificate": certificate,
            }
        if result == z3.unknown:
            saw_unknown = True
            entry["reason"] = solver.reason_unknown()
        checks.append(entry)
    return {
        "status": "unknown" if saw_unknown else "unsat",
        "backend": "z3 QF_NRA",
        "heads": heads,
        "checks": checks,
    }


def _eight_bit_hamming_signs() -> np.ndarray:
    answer = []
    for point in cube(8):
        distance = sum(int(point[index] != point[index + 4]) for index in range(4))
        answer.append(1 if distance >= 2 else -1)
    return np.array(answer, dtype=np.int64)


def known_bound_entries(
    signs: np.ndarray | list[int], dimension: int
) -> dict[str, list[dict[str, Any]]]:
    """Load repository theorems and independently verify archived upper data."""
    checked = validate_signs(signs, dimension)
    lower: list[dict[str, Any]] = []
    upper: list[dict[str, Any]] = []
    if dimension == 6:
        universal_lemma = REPOSITORY_ROOT / (
            "lemmas/01_foundations_and_normal_form/"
            "019_six_bit_universal_upper_bound.md"
        )
        upper.append(
            {
                "bound": 11,
                "method": "six-bit universal determinant-span theorem",
                "proof": str(universal_lemma),
            }
        )

        truth_mask = mask_from_signs(checked, dimension)
        target_mask = 0x96696BD669B69669
        complement_mask = ((1 << (1 << dimension)) - 1) ^ target_mask
        if truth_mask in (target_mask, complement_mask):
            import json

            archive = REPOSITORY_ROOT / (
                "artifacts/calculations/"
                "n6_parity_midlayer_triple_h6_certificate.json"
            )
            if archive.exists():
                raw = json.loads(archive.read_text())
                score_coefficients = raw["score_coefficients"]
                if truth_mask == complement_mask:
                    score_coefficients = [-value for value in score_coefficients]
                certificate = {
                    "schema_version": 1,
                    "dimension": 6,
                    "vertex_order": VERTEX_ORDER,
                    "head_count": 6,
                    "orientations": raw["orientations"],
                    "denominators": raw["denominators"],
                    "score_coefficients": score_coefficients,
                    "minimum_signed_cleared_score": raw[
                        "minimum_signed_cleared_score"
                    ],
                }
                report = verify_head_certificate(certificate, checked, dimension)
                if not report["valid"]:
                    raise RuntimeError(
                        "the archived six-bit certificate failed generic verification"
                    )
                upper.append(
                    {
                        "bound": 6,
                        "method": "exact integer head certificate",
                        "archive": str(archive),
                        "verification": report,
                        "certificate": certificate,
                    }
                )
    if dimension == 8 and np.array_equal(checked, _eight_bit_hamming_signs()):
        lemma = REPOSITORY_ROOT / (
            "lemmas/06_strict_separations/"
            "189_eight_bit_hamming_threshold_strict_separation.md"
        )
        lower.append(
            {
                "bound": 3,
                "method": "proved two-head impossibility",
                "proof": str(lemma),
            }
        )
        archive = REPOSITORY_ROOT / "artifacts/calculations/f8_three_head_upper_search.json"
        if archive.exists():
            import json

            payload = json.loads(archive.read_text())
            raw = payload["certificate"]
            certificate = {
                "schema_version": 1,
                "dimension": 8,
                "vertex_order": VERTEX_ORDER,
                "head_count": 3,
                "orientations": raw["orientations"],
                "denominators": raw["denominators"],
                "score_coefficients": raw["score_coefficients"],
                "minimum_signed_cleared_score": raw["minimum_signed_cleared_score"],
            }
            report = verify_head_certificate(certificate, checked, dimension)
            if not report["valid"]:
                raise RuntimeError(
                    "the archived eight-bit certificate failed generic verification"
                )
            upper.append(
                {
                    "bound": 3,
                    "method": "exact integer head certificate",
                    "archive": str(archive),
                    "verification": report,
                    "certificate": certificate,
                }
            )
    return {"lower": lower, "upper": upper}


def estimate_certified_hstar(
    signs: np.ndarray | list[int],
    dimension: int,
    *,
    use_z3_threshold_degree: bool = True,
    threshold_timeout_milliseconds: int = 30_000,
    use_known_bounds: bool = True,
    projection_permutation_limit: int = 720,
    partition_spectral_limit: int = 64,
    partition_spectral_max_side: int = 128,
    use_optimal_fourier_tail: bool = False,
    optimal_fourier_tail_max_transitions: int | None = 50_000_000,
    optimal_fourier_tail_max_vertices: int = 4096,
    use_sparse_ptf_column_generation: bool = False,
    sparse_ptf_max_iterations: int = 32,
    sparse_ptf_batch_size: int = 8,
    sparse_ptf_max_columns: int = 256,
    sparse_ptf_max_vertices: int = 4096,
    heuristic_restarts: int = 0,
    heuristic_max_heads: int | None = None,
    exact_nra: bool = False,
    nra_timeout_milliseconds: int = 60_000,
    nra_max_heads: int | None = None,
    seed: int = 0,
    export_directory: str | Path | None = None,
) -> dict[str, Any]:
    """Return a mathematically valid interval containing ``H^*(f)``."""
    checked = validate_signs(signs, dimension)
    truth_mask = mask_from_signs(checked, dimension)
    base: dict[str, Any] = {
        "schema_version": 1,
        "dimension": dimension,
        "vertex_order": VERTEX_ORDER,
        "truth_mask_hex": hex(truth_mask),
    }
    if np.all(checked == checked[0]):
        return {
            **base,
            "status": "exact",
            "certified_interval": [0, 0],
            "lower_bounds": [{"bound": 0, "method": "constant function"}],
            "upper_bounds": [{"bound": 0, "method": "constant function"}],
            "guarantee": "unconditional exact classification",
        }

    lower = 1
    lower_entries: list[dict[str, Any]] = [
        {"bound": 1, "method": "nonconstant functions require at least one head"}
    ]
    parity = largest_parity_restriction(checked, dimension)
    if parity["dimension"] > lower:
        lower = int(parity["dimension"])
        lower_entries.append(
            {
                "bound": lower,
                "method": "parity restriction plus threshold degree",
                "witness": parity,
            }
        )

    partition_spectral = partition_forster_lower_bound(
        checked,
        dimension,
        partition_limit=partition_spectral_limit,
        max_side=partition_spectral_max_side,
    )
    spectral_lower = int(partition_spectral["head_lower_bound"])
    if spectral_lower > lower:
        verification = verify_partition_forster_witness(
            partition_spectral,
            checked,
            dimension,
        )
        if not verification["valid"]:
            raise RuntimeError("failed to verify the partition spectral witness")
        lower = spectral_lower
        lower_entries.append(
            {
                "bound": lower,
                "method": (
                    "Forster partition sign-rank plus tangential rank cap"
                ),
                "witness": partition_spectral,
                "verification": verification,
            }
        )

    threshold = None
    threshold_export = (
        Path(export_directory) / "threshold"
        if export_directory is not None
        else None
    )
    if use_z3_threshold_degree:
        threshold = exact_threshold_degree(
            checked,
            dimension,
            timeout_milliseconds=threshold_timeout_milliseconds,
            export_directory=threshold_export,
        )
        threshold_lower = int(threshold["degree_lower_bound"])
        if threshold_lower > lower:
            lower = threshold_lower
            lower_entries.append(
                {
                    "bound": lower,
                    "method": "exact threshold-degree lower bound",
                    "backend": threshold["backend"],
                }
            )

    projection = projection_sign_change_upper_bound(
        checked,
        dimension,
        permutation_limit=projection_permutation_limit,
        seed=seed,
    )
    upper = int(projection["upper_bound"])
    upper_entries: list[dict[str, Any]] = [
        {"bound": upper, "method": "positive projection sign changes", "witness": projection}
    ]
    if projection["projection_family"] == "equal weights":
        symmetric_value = int(projection["upper_bound"])
        lower = max(lower, symmetric_value)
        upper = symmetric_value
        symmetric_proof = REPOSITORY_ROOT / (
            "lemmas/01_foundations_and_normal_form/"
            "012_symmetric_sign_changes.md"
        )
        lower_entries.append(
            {
                "bound": symmetric_value,
                "method": "symmetric sign-change characterization",
                "proof": str(symmetric_proof),
            }
        )
        upper_entries.append(
            {
                "bound": symmetric_value,
                "method": "symmetric sign-change characterization",
                "proof": str(symmetric_proof),
            }
        )
    minority = int(min(np.sum(checked > 0), np.sum(checked < 0)))
    sparse_upper = 1 if minority == 1 else 2 * minority
    if sparse_upper < upper:
        upper = sparse_upper
        upper_entries.append(
            {
                "bound": upper,
                "method": "sparse support upper bound",
                "minority_size": minority,
            }
        )
    if threshold is not None and threshold.get("exact_degree") == 1:
        upper = 1
        upper_entries.append(
            {"bound": 1, "method": "one head if and only if linear threshold"}
        )
    if (
        threshold is not None
        and threshold.get("exact_degree") is not None
        and dimension <= 4
    ):
        small_value = int(threshold["exact_degree"])
        upper = min(upper, small_value)
        small_proof = REPOSITORY_ROOT / (
            "lemmas/06_strict_separations/"
            "183_small_dimension_exact_classification.md"
        )
        upper_entries.append(
            {
                "bound": small_value,
                "method": "exact equality with threshold degree through four bits",
                "proof": str(small_proof),
            }
        )

    if use_known_bounds:
        known = known_bound_entries(checked, dimension)
        for entry in known["lower"]:
            if int(entry["bound"]) > lower:
                lower = int(entry["bound"])
            lower_entries.append(entry)
        for entry in known["upper"]:
            if int(entry["bound"]) < upper:
                upper = int(entry["bound"])
            upper_entries.append(entry)

    if lower > upper:
        raise RuntimeError(f"inconsistent certified bounds: lower {lower} exceeds upper {upper}")

    optimal_fourier_tail_diagnostics: dict[str, Any] | None = None
    if use_optimal_fourier_tail:
        vertex_count = 1 << dimension
        if optimal_fourier_tail_max_vertices < 1:
            raise ValueError("optimal_fourier_tail_max_vertices must be positive")
        if (
            optimal_fourier_tail_max_transitions is not None
            and optimal_fourier_tail_max_transitions < 1
        ):
            raise ValueError(
                "optimal_fourier_tail_max_transitions must be positive or None"
            )
        if vertex_count > optimal_fourier_tail_max_vertices:
            optimal_fourier_tail_diagnostics = {
                "status": "skipped-vertex-budget",
                "vertex_count": vertex_count,
                "max_vertices": optimal_fourier_tail_max_vertices,
                "floating_failures_are_lower_bounds": False,
            }
        else:
            try:
                tail_certificate, tail_search = optimal_fourier_tail_upper_bound(
                    checked,
                    dimension,
                    max_dp_transitions=optimal_fourier_tail_max_transitions,
                )
            except FourierTailBudgetExceeded as error:
                optimal_fourier_tail_diagnostics = {
                    "status": "skipped-transition-budget",
                    "estimated_dp_transitions": error.estimated_transitions,
                    "max_dp_transitions": error.max_transitions,
                    "floating_failures_are_lower_bounds": False,
                }
            else:
                tail_report = verify_sparse_ptf_certificate(
                    tail_certificate,
                    checked,
                    dimension,
                )
                if not tail_report["valid"]:
                    raise RuntimeError(
                        "failed to verify the optimal Fourier-tail certificate"
                    )
                tail_bound = int(tail_certificate["head_count"])
                improved_upper_bound = tail_bound < upper
                optimal_fourier_tail_diagnostics = {
                    **tail_search,
                    "improved_upper_bound": improved_upper_bound,
                    "certificate": tail_certificate,
                    "verification": tail_report,
                }
                if improved_upper_bound:
                    upper = tail_bound
                    upper_entries.append(
                        {
                            "bound": tail_bound,
                            "method": (
                                "optimal absolute Fourier-tail knapsack plus exact "
                                "theorem-backed compilation"
                            ),
                            "certificate": tail_certificate,
                            "verification": tail_report,
                        }
                    )
        if lower > upper:
            raise RuntimeError(
                f"inconsistent certified bounds after optimal Fourier tail: "
                f"lower {lower} exceeds upper {upper}"
            )

    sparse_ptf_diagnostics: dict[str, Any] | None = None
    if use_sparse_ptf_column_generation:
        vertex_count = 1 << dimension
        if sparse_ptf_max_vertices < 1:
            raise ValueError("sparse_ptf_max_vertices must be positive")
        if vertex_count > sparse_ptf_max_vertices:
            sparse_ptf_diagnostics = {
                "status": "skipped-vertex-budget",
                "vertex_count": vertex_count,
                "max_vertices": sparse_ptf_max_vertices,
                "floating_failures_are_lower_bounds": False,
            }
        else:
            sparse_certificate, sparse_ptf_diagnostics = (
                column_generation_sparse_ptf_portfolio(
                    checked,
                    dimension,
                    config=SparsePTFColumnGenerationConfig(
                        max_iterations=sparse_ptf_max_iterations,
                        batch_size=sparse_ptf_batch_size,
                        max_columns=sparse_ptf_max_columns,
                    ),
                )
            )
            sparse_report = verify_sparse_ptf_certificate(
                sparse_certificate,
                checked,
                dimension,
            )
            if not sparse_report["valid"]:
                raise RuntimeError("failed to verify the sparse PTF certificate")
            sparse_bound = int(sparse_certificate["head_count"])
            if sparse_bound < upper:
                upper = sparse_bound
                upper_entries.append(
                    {
                        "bound": sparse_bound,
                        "method": (
                            "transform-priced sparse PTF plus exact "
                            "theorem-backed compilation"
                        ),
                        "certificate": sparse_certificate,
                        "verification": sparse_report,
                    }
                )
        if lower > upper:
            raise RuntimeError(
                f"inconsistent certified bounds after sparse PTF: "
                f"lower {lower} exceeds upper {upper}"
            )

    heuristic_diagnostics = []
    if heuristic_restarts > 0 and lower < upper:
        maximum = upper - 1
        if heuristic_max_heads is not None:
            maximum = min(maximum, heuristic_max_heads)
        for heads in range(lower, maximum + 1):
            certificate, diagnostic = random_denominator_search(
                checked,
                dimension,
                heads,
                restarts=heuristic_restarts,
                seed=seed + 1009 * heads,
            )
            heuristic_diagnostics.append({"heads": heads, **diagnostic})
            if certificate is not None:
                upper = heads
                upper_entries.append(
                    {
                        "bound": heads,
                        "method": "numerically discovered, exactly verified integer certificate",
                        "certificate": certificate,
                    }
                )
                break

    nra_decisions = []
    if exact_nra and lower < upper:
        maximum = upper - 1
        if nra_max_heads is not None:
            maximum = min(maximum, nra_max_heads)
        frontier = lower
        for heads in range(lower, maximum + 1):
            nra_export = (
                Path(export_directory) / "nra" / f"heads_{heads}"
                if export_directory is not None
                else None
            )
            decision = decide_head_feasibility(
                checked,
                dimension,
                heads,
                timeout_milliseconds=nra_timeout_milliseconds,
                export_directory=nra_export,
            )
            nra_decisions.append(decision)
            if decision["status"] == "unsat" and heads == frontier:
                frontier += 1
                lower = frontier
                lower_entries.append(
                    {
                        "bound": lower,
                        "method": "all orientation counts QF_NRA unsatisfiable",
                        "heads_ruled_out": heads,
                        "backend": decision["backend"],
                    }
                )
            elif decision["status"] == "sat":
                upper = min(upper, heads)
                entry = {
                    "bound": heads,
                    "method": "QF_NRA satisfiable closure, strictified by perturbation",
                    "backend": decision["backend"],
                }
                if decision.get("strict_integer_certificate") is not None:
                    entry["certificate"] = decision["strict_integer_certificate"]
                    entry["method"] = "QF_NRA discovery plus strict integer verification"
                upper_entries.append(entry)
                break

    exact = lower == upper
    solver_endpoint = any(
        entry["method"] in {
            "exact threshold-degree lower bound",
            "all orientation counts QF_NRA unsatisfiable",
            "QF_NRA satisfiable closure, strictified by perturbation",
        }
        for entry in lower_entries + upper_entries
        if int(entry["bound"]) in {lower, upper}
    )
    return {
        **base,
        "status": "exact" if exact else "certified-interval",
        "certified_interval": [lower, upper],
        "lower_bounds": lower_entries,
        "upper_bounds": upper_entries,
        "threshold_degree": threshold,
        "largest_parity_restriction": parity,
        "partition_spectral_bound": partition_spectral,
        "optimal_fourier_tail": optimal_fourier_tail_diagnostics,
        "sparse_ptf_column_generation": sparse_ptf_diagnostics,
        "heuristic_diagnostics": heuristic_diagnostics,
        "exact_nra_decisions": nra_decisions,
        "guarantee": (
            "portable exact theorem or integer-certificate classification"
            if exact and not solver_endpoint
            else "exact, conditional only on the cited exact solver decisions"
            if exact and solver_endpoint
            else (
                "both endpoints are rigorous; heuristic failures did not affect "
                "the lower endpoint"
            )
        ),
    }
