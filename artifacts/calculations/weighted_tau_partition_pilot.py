#!/usr/bin/env python3
"""Standalone weighted-tau sign-rank certificate pilot.

This research script deliberately does not modify or depend on the public
certified estimator.  It has three layers:

1. A numerical outer-approximation search for the weighted tau SDP, using
   HiGHS and cuts from negative eigenvectors.
2. A numerical-to-rational conversion that adds an exact diagonally dominant
   residual to a rational Gram factor.
3. An exact verifier that uses only Python integer and Fraction arithmetic.

For rational probability vectors p and q, the weighted tau problem is

    minimize  sum(z)
    subject to S .* W >= p q^T
               Diag(z) - [[0, W/2], [W^T/2, 0]] >= 0.

A rational feasible point of value U proves sign-rank(S) >= ceil(1 / U).
The numerical search is only a candidate generator.  Every reported bound is
recomputed by ``verify_weighted_tau_certificate`` using exact arithmetic.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Sequence

import numpy as np
from scipy import sparse
from scipy.optimize import linprog


@dataclass(frozen=True)
class WeightedTauDiscovery:
    """Untrusted floating-point output of the eigenvector-cut search."""

    w: np.ndarray
    z: np.ndarray
    objective: float
    minimum_eigenvalue: float
    rounds: int
    cut_count: int
    elapsed_seconds: float
    converged: bool


def sylvester_matrix(order: int) -> np.ndarray:
    """Return the Sylvester Hadamard matrix of power-of-two order."""
    if order < 1 or order & (order - 1):
        raise ValueError("Sylvester order must be a positive power of two")
    result = np.array([[1]], dtype=np.int64)
    while result.shape[0] < order:
        result = np.block([[result, result], [result, -result]])
    return result


def _validate_sign_matrix(signs: np.ndarray | Sequence[Sequence[int]]) -> np.ndarray:
    matrix = np.asarray(signs)
    if matrix.ndim != 2 or 0 in matrix.shape:
        raise ValueError("sign matrix must be nonempty and two-dimensional")
    if not np.all(np.isin(matrix, (-1, 1))):
        raise ValueError("sign matrix entries must all be -1 or 1")
    return matrix.astype(np.int64, copy=False)


def _validate_probability_vector(
    values: Sequence[float], expected_length: int, name: str
) -> np.ndarray:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (expected_length,):
        raise ValueError(f"{name} must have length {expected_length}")
    if np.any(vector < 0.0) or not np.isfinite(vector).all():
        raise ValueError(f"{name} must be finite and nonnegative")
    if not math.isclose(float(np.sum(vector)), 1.0, abs_tol=1e-12):
        raise ValueError(f"{name} must sum to one")
    return vector


def discover_weighted_tau(
    signs: np.ndarray | Sequence[Sequence[int]],
    p: Sequence[float],
    q: Sequence[float],
    *,
    maximum_rounds: int = 160,
    eigenvalue_tolerance: float = 1e-7,
    cuts_per_round: int = 12,
    magnitude_penalty: float = 1e-6,
) -> WeightedTauDiscovery:
    """Numerically search the weighted tau SDP by eigenvector cuts.

    The finite LP is an outer approximation to the PSD cone.  Consequently,
    this function never returns a certificate.  Its output must be passed to
    ``rationalize_discovery`` and then to the exact verifier.
    """
    matrix = _validate_sign_matrix(signs)
    row_count, column_count = matrix.shape
    row_weights = _validate_probability_vector(p, row_count, "p")
    column_weights = _validate_probability_vector(q, column_count, "q")
    if maximum_rounds < 1:
        raise ValueError("maximum_rounds must be positive")
    if eigenvalue_tolerance <= 0.0:
        raise ValueError("eigenvalue_tolerance must be positive")
    if cuts_per_round < 1:
        raise ValueError("cuts_per_round must be positive")

    entry_count = row_count * column_count
    psd_order = row_count + column_count
    required_margins = row_weights[:, None] * column_weights[None, :]

    initial_w = matrix.astype(float) * required_margins
    initial_diagonal = float(np.linalg.norm(initial_w, ord=2)) / 2.0 + 1e-8
    incumbent_objective = psd_order * initial_diagonal
    magnitude_bound = max(1.0, incumbent_objective)

    objective = np.concatenate(
        [magnitude_penalty * matrix.ravel(), np.ones(psd_order)]
    )
    bounds: list[tuple[float, float]] = []
    for sign, margin in zip(matrix.ravel(), required_margins.ravel()):
        if sign > 0:
            bounds.append((float(margin), magnitude_bound))
        else:
            bounds.append((-magnitude_bound, -float(margin)))
    bounds.extend([(0.0, incumbent_objective)] * psd_order)

    # Every PSD 2 by 2 row-column principal submatrix obeys
    # z_i + z_j >= |W_ij|.  These cuts also keep the first LP bounded well.
    pair_rows = []
    for row in range(row_count):
        for column in range(column_count):
            indices = [
                row * column_count + column,
                entry_count + row,
                entry_count + row_count + column,
            ]
            values = [float(matrix[row, column]), -1.0, -1.0]
            pair_rows.append(
                sparse.csr_matrix(
                    (values, ([0, 0, 0], indices)),
                    shape=(1, entry_count + psd_order),
                )
            )
    cut_rows = pair_rows
    start = time.perf_counter()
    last_w = initial_w
    last_z = np.full(psd_order, initial_diagonal, dtype=float)
    last_minimum = 0.0

    for round_index in range(maximum_rounds):
        inequality_matrix = sparse.vstack(cut_rows, format="csc")
        result = linprog(
            objective,
            A_ub=inequality_matrix,
            b_ub=np.zeros(inequality_matrix.shape[0]),
            bounds=bounds,
            method="highs",
            options={
                "primal_feasibility_tolerance": 1e-9,
                "dual_feasibility_tolerance": 1e-9,
            },
        )
        if not result.success:
            raise RuntimeError(f"weighted tau LP failed: {result.message}")

        last_w = result.x[:entry_count].reshape(row_count, column_count)
        last_z = result.x[entry_count:]
        candidate = np.block(
            [
                [np.diag(last_z[:row_count]), -last_w / 2.0],
                [-last_w.T / 2.0, np.diag(last_z[row_count:])],
            ]
        )
        eigenvalues, eigenvectors = np.linalg.eigh(candidate)
        last_minimum = float(eigenvalues[0])
        negative = np.flatnonzero(eigenvalues < -eigenvalue_tolerance)
        if len(negative) == 0:
            return WeightedTauDiscovery(
                w=last_w,
                z=last_z,
                objective=float(np.sum(last_z)),
                minimum_eigenvalue=last_minimum,
                rounds=round_index + 1,
                cut_count=len(cut_rows),
                elapsed_seconds=time.perf_counter() - start,
                converged=True,
            )

        for eigen_index in negative[:cuts_per_round]:
            vector = eigenvectors[:, eigen_index]
            left = vector[:row_count]
            right = vector[row_count:]
            dense_cut = np.concatenate(
                [
                    (left[:, None] * right[None, :]).ravel(),
                    -(left * left),
                    -(right * right),
                ]
            )
            cut_rows.append(sparse.csr_matrix(dense_cut.reshape(1, -1)))

    return WeightedTauDiscovery(
        w=last_w,
        z=last_z,
        objective=float(np.sum(last_z)),
        minimum_eigenvalue=last_minimum,
        rounds=maximum_rounds,
        cut_count=len(cut_rows),
        elapsed_seconds=time.perf_counter() - start,
        converged=False,
    )


def _ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def _is_certificate_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _head_lower_from_sign_rank(signs: np.ndarray, sign_rank_lower: int) -> int:
    # The partition rank cap is stated for nonconstant targets.  A constant
    # submatrix alone cannot certify that premise, so return zero there.
    if np.all(signs == signs.flat[0]):
        return 0
    return max(1, (sign_rank_lower + 1).bit_length() - 1)


def _pack_rationals(values: Sequence[Fraction]) -> dict[str, Any]:
    denominator = 1
    for value in values:
        denominator = math.lcm(denominator, value.denominator)
    return {
        "denominator": denominator,
        "numerators": [
            value.numerator * (denominator // value.denominator)
            for value in values
        ],
    }


def _pack_rational_matrix(values: Sequence[Sequence[Fraction]]) -> dict[str, Any]:
    row_count = len(values)
    column_count = len(values[0]) if row_count else 0
    if any(len(row) != column_count for row in values):
        raise ValueError("rational matrix must be rectangular")
    flat = [value for row in values for value in row]
    packed = _pack_rationals(flat)
    packed["shape"] = [row_count, column_count]
    return packed


def _unpack_rationals(data: Any, expected_length: int) -> list[Fraction]:
    if not isinstance(data, dict):
        raise ValueError("rational vector must be a dictionary")
    denominator = data.get("denominator")
    numerators = data.get("numerators")
    if not _is_certificate_integer(denominator) or denominator <= 0:
        raise ValueError("rational denominator must be a positive integer")
    if not isinstance(numerators, list) or len(numerators) != expected_length:
        raise ValueError("rational vector has the wrong length")
    if any(not _is_certificate_integer(value) for value in numerators):
        raise ValueError("rational numerators must be integers")
    return [Fraction(value, denominator) for value in numerators]


def _unpack_rational_matrix(
    data: Any, expected_shape: tuple[int, int] | None = None
) -> list[list[Fraction]]:
    if not isinstance(data, dict):
        raise ValueError("rational matrix must be a dictionary")
    shape = data.get("shape")
    if (
        not isinstance(shape, list)
        or len(shape) != 2
        or any(not _is_certificate_integer(value) or value < 0 for value in shape)
    ):
        raise ValueError("rational matrix shape is malformed")
    row_count, column_count = shape
    if expected_shape is not None and (row_count, column_count) != expected_shape:
        raise ValueError("rational matrix has the wrong shape")
    flat = _unpack_rationals(data, row_count * column_count)
    return [
        flat[row * column_count : (row + 1) * column_count]
        for row in range(row_count)
    ]


def _certificate_from_rationals(
    signs: np.ndarray,
    p: Sequence[Fraction],
    q: Sequence[Fraction],
    w: Sequence[Sequence[Fraction]],
    z: Sequence[Fraction],
    gram_factor: Sequence[Sequence[Fraction]],
    *,
    source: str,
) -> dict[str, Any]:
    matrix = _validate_sign_matrix(signs)
    objective = sum(z, Fraction(0))
    if objective <= 0:
        raise ValueError("certificate objective must be positive")
    sign_rank_lower = _ceil_fraction(Fraction(1, 1) / objective)
    head_lower = _head_lower_from_sign_rank(matrix, sign_rank_lower)
    return {
        "schema_version": 1,
        "method": "weighted-tau-rational-gram-dd",
        "source": source,
        "matrix_shape": list(matrix.shape),
        "p": _pack_rationals(p),
        "q": _pack_rationals(q),
        "w": _pack_rational_matrix(w),
        "z": _pack_rationals(z),
        "gram_factor": _pack_rational_matrix(gram_factor),
        "claimed_objective": str(objective),
        "claimed_sign_rank_lower_bound": sign_rank_lower,
        "claimed_head_lower_bound": head_lower,
    }


def rationalize_discovery(
    signs: np.ndarray | Sequence[Sequence[int]],
    p: Sequence[Fraction],
    q: Sequence[Fraction],
    discovery: WeightedTauDiscovery,
    *,
    value_denominator: int = 1 << 12,
    factor_denominator: int = 1 << 16,
) -> dict[str, Any]:
    """Convert a numerical candidate into an exact Gram-plus-DD certificate."""
    matrix = _validate_sign_matrix(signs)
    row_count, column_count = matrix.shape
    psd_order = row_count + column_count
    if len(p) != row_count or len(q) != column_count:
        raise ValueError("rational probability vectors have the wrong size")
    if any(value < 0 for value in p) or sum(p, Fraction(0)) != 1:
        raise ValueError("p must be a rational probability vector")
    if any(value < 0 for value in q) or sum(q, Fraction(0)) != 1:
        raise ValueError("q must be a rational probability vector")
    if discovery.w.shape != matrix.shape or discovery.z.shape != (psd_order,):
        raise ValueError("discovery arrays have the wrong shape")
    if value_denominator < 1 or factor_denominator < 1:
        raise ValueError("rounding denominators must be positive")

    rational_w: list[list[Fraction]] = []
    for row in range(row_count):
        current_row = []
        for column in range(column_count):
            required = p[row] * q[column]
            required_numerator = _ceil_fraction(required * value_denominator)
            signed_value = float(matrix[row, column] * discovery.w[row, column])
            approximate_numerator = math.ceil(
                signed_value * value_denominator - 1e-12
            )
            magnitude_numerator = max(
                0, required_numerator, approximate_numerator
            )
            current_row.append(
                Fraction(
                    int(matrix[row, column]) * magnitude_numerator,
                    value_denominator,
                )
            )
        rational_w.append(current_row)

    rational_z0 = [
        Fraction(
            max(0, math.ceil(float(value) * value_denominator - 1e-12)),
            value_denominator,
        )
        for value in discovery.z
    ]

    q0 = [[Fraction(0) for _ in range(psd_order)] for _ in range(psd_order)]
    for index, value in enumerate(rational_z0):
        q0[index][index] = value
    for row in range(row_count):
        for column in range(column_count):
            value = -rational_w[row][column] / 2
            q0[row][row_count + column] = value
            q0[row_count + column][row] = value

    q0_float = np.array(
        [[float(value) for value in row] for row in q0], dtype=float
    )
    eigenvalues, eigenvectors = np.linalg.eigh(q0_float)
    positive = np.flatnonzero(eigenvalues > 1e-12)
    numerical_factor = (
        eigenvectors[:, positive] * np.sqrt(eigenvalues[positive])[None, :]
    )
    gram_factor = [
        [
            Fraction(int(round(value * factor_denominator)), factor_denominator)
            for value in numerical_factor[row]
        ]
        for row in range(psd_order)
    ]

    residual = [
        [q0[row][column] for column in range(psd_order)]
        for row in range(psd_order)
    ]
    for row in range(psd_order):
        for column in range(psd_order):
            residual[row][column] -= sum(
                (
                    gram_factor[row][factor_index]
                    * gram_factor[column][factor_index]
                    for factor_index in range(len(positive))
                ),
                Fraction(0),
            )

    corrections = []
    for row in range(psd_order):
        off_diagonal = sum(
            (
                abs(residual[row][column])
                for column in range(psd_order)
                if column != row
            ),
            Fraction(0),
        )
        corrections.append(max(Fraction(0), off_diagonal - residual[row][row]))
    rational_z = [
        rational_z0[index] + corrections[index]
        for index in range(psd_order)
    ]
    return _certificate_from_rationals(
        matrix,
        p,
        q,
        rational_w,
        rational_z,
        gram_factor,
        source="eigenvector-cut discovery followed by rational Gram plus DD residual",
    )


def verify_weighted_tau_certificate(
    certificate: dict[str, Any],
    signs: np.ndarray | Sequence[Sequence[int]],
) -> dict[str, Any]:
    """Verify a weighted tau certificate using exact rational arithmetic."""
    try:
        matrix = _validate_sign_matrix(signs)
        row_count, column_count = matrix.shape
        psd_order = row_count + column_count
        if not _is_certificate_integer(certificate.get("schema_version")):
            raise ValueError("schema version must be an integer")
        if certificate.get("schema_version") != 1:
            raise ValueError("unsupported schema version")
        if certificate.get("method") != "weighted-tau-rational-gram-dd":
            raise ValueError("unexpected certificate method")
        if certificate.get("matrix_shape") != [row_count, column_count]:
            raise ValueError("matrix shape mismatch")

        p = _unpack_rationals(certificate.get("p"), row_count)
        q = _unpack_rationals(certificate.get("q"), column_count)
        w = _unpack_rational_matrix(
            certificate.get("w"), (row_count, column_count)
        )
        z = _unpack_rationals(certificate.get("z"), psd_order)
        factor_data = certificate.get("gram_factor")
        if not isinstance(factor_data, dict):
            raise ValueError("missing Gram factor")
        factor_shape = factor_data.get("shape")
        if (
            not isinstance(factor_shape, list)
            or len(factor_shape) != 2
            or factor_shape[0] != psd_order
            or not _is_certificate_integer(factor_shape[1])
            or factor_shape[1] < 0
        ):
            raise ValueError("Gram factor shape mismatch")
        gram_factor = _unpack_rational_matrix(
            factor_data, (psd_order, factor_shape[1])
        )

        if any(value < 0 for value in p) or sum(p, Fraction(0)) != 1:
            raise ValueError("p is not a probability vector")
        if any(value < 0 for value in q) or sum(q, Fraction(0)) != 1:
            raise ValueError("q is not a probability vector")
        if any(value < 0 for value in z):
            raise ValueError("z has a negative entry")
        for row in range(row_count):
            for column in range(column_count):
                signed_value = int(matrix[row, column]) * w[row][column]
                if signed_value < p[row] * q[column]:
                    raise ValueError("weighted sign-margin constraint failed")

        residual = [
            [Fraction(0) for _ in range(psd_order)]
            for _ in range(psd_order)
        ]
        for index, value in enumerate(z):
            residual[index][index] = value
        for row in range(row_count):
            for column in range(column_count):
                value = -w[row][column] / 2
                residual[row][row_count + column] = value
                residual[row_count + column][row] = value
        factor_columns = factor_shape[1]
        for row in range(psd_order):
            for column in range(psd_order):
                residual[row][column] -= sum(
                    (
                        gram_factor[row][factor_index]
                        * gram_factor[column][factor_index]
                        for factor_index in range(factor_columns)
                    ),
                    Fraction(0),
                )

        slacks = []
        for row in range(psd_order):
            off_diagonal = sum(
                (
                    abs(residual[row][column])
                    for column in range(psd_order)
                    if column != row
                ),
                Fraction(0),
            )
            slack = residual[row][row] - off_diagonal
            if slack < 0:
                raise ValueError("Gram residual is not diagonally dominant")
            slacks.append(slack)

        objective = sum(z, Fraction(0))
        if objective <= 0:
            raise ValueError("objective must be positive")
        sign_rank_lower = _ceil_fraction(Fraction(1, 1) / objective)
        head_lower = _head_lower_from_sign_rank(matrix, sign_rank_lower)
        if certificate.get("claimed_objective") != str(objective):
            raise ValueError("claimed objective mismatch")
        claimed_sign_rank = certificate.get("claimed_sign_rank_lower_bound")
        if not _is_certificate_integer(claimed_sign_rank):
            raise ValueError("claimed sign-rank bound must be an integer")
        if claimed_sign_rank != sign_rank_lower:
            raise ValueError("claimed sign-rank lower bound mismatch")
        claimed_head = certificate.get("claimed_head_lower_bound")
        if not _is_certificate_integer(claimed_head):
            raise ValueError("claimed head bound must be an integer")
        if claimed_head != head_lower:
            raise ValueError("claimed head lower bound mismatch")
        return {
            "valid": True,
            "objective": str(objective),
            "sign_rank_lower_bound": sign_rank_lower,
            "head_lower_bound": head_lower,
            "minimum_dd_slack": str(min(slacks)),
            "gram_factor_columns": factor_columns,
        }
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        return {"valid": False, "reason": str(error)}


def padded_sylvester_hard_core_certificate(
    full_order: int = 16,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Return an exact rank-three certificate for a padded 8 by 8 core.

    The sign matrix is all positive outside its leading Sylvester block.
    The product weights are uniform on that block and zero elsewhere.  The
    exact Gram factor uses a = 3/20 and b = -5/96.  Its residual is diagonal:
    3/3200 on active row coordinates and 1/576 on active column coordinates.
    """
    core_order = 8
    if full_order < core_order:
        raise ValueError("full order must be at least eight")
    core = sylvester_matrix(core_order)
    signs = np.ones((full_order, full_order), dtype=np.int64)
    signs[:core_order, :core_order] = core
    p = [
        Fraction(1, core_order) if index < core_order else Fraction(0)
        for index in range(full_order)
    ]
    q = list(p)
    w = [
        [Fraction(0) for _ in range(full_order)]
        for _ in range(full_order)
    ]
    for row in range(core_order):
        for column in range(core_order):
            w[row][column] = Fraction(int(core[row, column]), 64)
    z = [
        Fraction(3, 128) if index < core_order else Fraction(0)
        for index in range(full_order)
    ] + [
        Fraction(3, 128) if index < core_order else Fraction(0)
        for index in range(full_order)
    ]
    gram_factor = [
        [Fraction(0) for _ in range(core_order)]
        for _ in range(2 * full_order)
    ]
    for row in range(core_order):
        gram_factor[row][row] = Fraction(3, 20)
    for column in range(core_order):
        for factor_index in range(core_order):
            gram_factor[full_order + column][factor_index] = (
                Fraction(-5, 96) * int(core[factor_index, column])
            )
    certificate = _certificate_from_rationals(
        signs,
        p,
        q,
        w,
        z,
        gram_factor,
        source="exact padded Sylvester 8 by 8 hard-core construction",
    )
    return signs, certificate


def _uniform_fractions(length: int) -> list[Fraction]:
    return [Fraction(1, length) for _ in range(length)]


def run_smoke_tests() -> list[dict[str, Any]]:
    """Run numerical discovery and exact verification on small benchmarks."""
    cases = [
        ("all_ones_4", np.ones((4, 4), dtype=np.int64), 1),
        ("sylvester_4", sylvester_matrix(4), 2),
        ("sylvester_8", sylvester_matrix(8), 3),
    ]
    reports = []
    for name, signs, expected_rank in cases:
        p = _uniform_fractions(signs.shape[0])
        q = _uniform_fractions(signs.shape[1])
        discovery = discover_weighted_tau(
            signs,
            [float(value) for value in p],
            [float(value) for value in q],
        )
        if not discovery.converged:
            raise AssertionError(f"{name} numerical discovery did not converge")
        certificate = rationalize_discovery(signs, p, q, discovery)
        exact = verify_weighted_tau_certificate(certificate, signs)
        if not exact["valid"]:
            raise AssertionError(f"{name} exact verification failed: {exact}")
        if exact["sign_rank_lower_bound"] < expected_rank:
            raise AssertionError(f"{name} lost its expected integer rank bound")
        reports.append(
            {
                "name": name,
                "rounds": discovery.rounds,
                "cuts": discovery.cut_count,
                "numerical_objective": discovery.objective,
                "numerical_minimum_eigenvalue": discovery.minimum_eigenvalue,
                "exact": exact,
            }
        )

    padded_signs, padded_certificate = padded_sylvester_hard_core_certificate()
    padded = verify_weighted_tau_certificate(padded_certificate, padded_signs)
    if not padded["valid"]:
        raise AssertionError(f"padded hard-core certificate failed: {padded}")
    if padded["objective"] != "3/8" or padded["sign_rank_lower_bound"] != 3:
        raise AssertionError("padded hard-core certificate has unexpected value")
    reloaded = json.loads(json.dumps(padded_certificate))
    if not verify_weighted_tau_certificate(reloaded, padded_signs)["valid"]:
        raise AssertionError("JSON round trip invalidated the exact certificate")
    tampered = dict(padded_certificate)
    tampered_w = dict(padded_certificate["w"])
    tampered_numerators = list(tampered_w["numerators"])
    tampered_numerators[0] = 0
    tampered_w["numerators"] = tampered_numerators
    tampered["w"] = tampered_w
    if verify_weighted_tau_certificate(tampered, padded_signs)["valid"]:
        raise AssertionError("verifier accepted a tampered sign-margin entry")
    reports.append(
        {
            "name": "padded_sylvester_8_in_16",
            "rounds": 0,
            "cuts": 0,
            "numerical_objective": None,
            "numerical_minimum_eigenvalue": None,
            "exact": padded,
        }
    )
    return reports


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="run assertions without printing per-case reports",
    )
    arguments = parser.parse_args()
    reports = run_smoke_tests()
    if not arguments.quiet:
        for report in reports:
            exact = report["exact"]
            if report["numerical_objective"] is None:
                numerical = "analytic"
            else:
                numerical = (
                    f"numeric={report['numerical_objective']:.9f} "
                    f"lambda_min={report['numerical_minimum_eigenvalue']:.3e}"
                )
            print(
                f"{report['name']}: {numerical} rounds={report['rounds']} "
                f"cuts={report['cuts']} exact={exact['objective']} "
                f"rank>={exact['sign_rank_lower_bound']} "
                f"head>={exact['head_lower_bound']} "
                f"dd_slack={exact['minimum_dd_slack']}"
            )
        print("weighted tau partition pilot: verified")


if __name__ == "__main__":
    main()
