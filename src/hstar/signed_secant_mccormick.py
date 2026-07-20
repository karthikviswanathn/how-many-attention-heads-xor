"""Exact rational McCormick leaves for signed-secant parameter cells.

The verifier in this module reconstructs the relaxation from model metadata.
It never trusts solver-supplied matrices, derived variable bounds, or a claimed
linear-program value.  A certificate is accepted only when nonnegative
inequality multipliers and free equality multipliers reproduce the weighted
signed objective exactly and give a nonpositive rational upper bound.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Mapping, Sequence

import numpy as np

from .boolean_cube import VERTEX_ORDER, mask_from_signs, validate_signs


Rational = Fraction


def _rational(value: Any) -> Rational:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError("Boolean values are not rational certificate values")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("rational certificate values must be integers or strings")


def _bound(raw: Any, name: str) -> tuple[Rational, Rational]:
    if not isinstance(raw, list) or len(raw) != 2:
        raise ValueError(f"{name} must be a two-element bound")
    lower, upper = (_rational(raw[0]), _rational(raw[1]))
    if lower > upper:
        raise ValueError(f"{name} has lower bound above upper bound")
    return lower, upper


def _clean_form(coefficients: Mapping[str, Rational]) -> dict[str, Rational]:
    return {
        name: coefficient
        for name, coefficient in coefficients.items()
        if coefficient
    }


def _add_scaled(
    target: dict[str, Rational],
    source: Mapping[str, Rational],
    scale: Rational,
) -> None:
    for name, coefficient in source.items():
        updated = target.get(name, Fraction(0)) + scale * coefficient
        if updated:
            target[name] = updated
        else:
            target.pop(name, None)


@dataclass(frozen=True)
class LinearConstraint:
    name: str
    coefficients: dict[str, Rational]
    rhs: Rational


class RationalMcCormickRelaxation:
    """Build a factorable LP relaxation with exact interval propagation."""

    def __init__(self) -> None:
        self.bounds: dict[str, tuple[Rational, Rational]] = {}
        self.inequalities: dict[str, LinearConstraint] = {}
        self.equalities: dict[str, LinearConstraint] = {}
        self.objective: dict[str, Rational] = {}
        self.objective_constant = Fraction(0)
        self.product_count = 0
        self.affine_count = 0

    def _add_constraint(
        self,
        destination: dict[str, LinearConstraint],
        name: str,
        coefficients: Mapping[str, Rational],
        rhs: Rational,
    ) -> None:
        if name in self.inequalities or name in self.equalities:
            raise ValueError(f"duplicate constraint name: {name}")
        cleaned = _clean_form(coefficients)
        unknown = set(cleaned).difference(self.bounds)
        if unknown:
            raise ValueError(f"constraint {name} uses unknown variables: {unknown}")
        destination[name] = LinearConstraint(name, cleaned, rhs)

    def add_inequality(
        self,
        name: str,
        coefficients: Mapping[str, Rational],
        rhs: Rational | int,
    ) -> None:
        self._add_constraint(
            self.inequalities,
            name,
            coefficients,
            _rational(rhs),
        )

    def add_equality(
        self,
        name: str,
        coefficients: Mapping[str, Rational],
        rhs: Rational | int,
    ) -> None:
        self._add_constraint(
            self.equalities,
            name,
            coefficients,
            _rational(rhs),
        )

    def add_base(
        self,
        name: str,
        lower: Rational | int,
        upper: Rational | int,
    ) -> str:
        if name in self.bounds:
            raise ValueError(f"duplicate variable name: {name}")
        checked_lower = _rational(lower)
        checked_upper = _rational(upper)
        if checked_lower > checked_upper:
            raise ValueError(f"invalid bounds for {name}")
        self.bounds[name] = (checked_lower, checked_upper)
        self.add_inequality(
            f"bound_lower::{name}",
            {name: Fraction(-1)},
            -checked_lower,
        )
        self.add_inequality(
            f"bound_upper::{name}",
            {name: Fraction(1)},
            checked_upper,
        )
        return name

    def add_affine(
        self,
        name: str,
        constant: Rational | int,
        terms: Mapping[str, Rational | int],
        *,
        certified_bounds: tuple[Rational, Rational] | None = None,
    ) -> str:
        checked_constant = _rational(constant)
        checked_terms = {
            variable: _rational(coefficient)
            for variable, coefficient in terms.items()
            if _rational(coefficient)
        }
        unknown = set(checked_terms).difference(self.bounds)
        if unknown:
            raise ValueError(f"affine node {name} uses unknown variables: {unknown}")
        lower = checked_constant
        upper = checked_constant
        for variable, coefficient in checked_terms.items():
            source_lower, source_upper = self.bounds[variable]
            if coefficient >= 0:
                lower += coefficient * source_lower
                upper += coefficient * source_upper
            else:
                lower += coefficient * source_upper
                upper += coefficient * source_lower
        if certified_bounds is not None:
            certified_lower, certified_upper = certified_bounds
            if (
                certified_lower < lower
                or certified_upper > upper
                or certified_lower > certified_upper
            ):
                raise ValueError(f"invalid certified affine bounds for {name}")
            lower, upper = certified_lower, certified_upper
        self.add_base(name, lower, upper)
        equality = {name: Fraction(1)}
        for variable, coefficient in checked_terms.items():
            equality[variable] = equality.get(variable, Fraction(0)) - coefficient
        self.add_equality(f"affine::{name}", equality, checked_constant)
        self.affine_count += 1
        return name

    def add_product(self, name: str, left: str, right: str) -> str:
        if left not in self.bounds or right not in self.bounds:
            raise ValueError(f"product node {name} uses an unknown variable")
        if left == right:
            raise ValueError("square nodes require a dedicated convex envelope")
        left_lower, left_upper = self.bounds[left]
        right_lower, right_upper = self.bounds[right]
        corners = (
            left_lower * right_lower,
            left_lower * right_upper,
            left_upper * right_lower,
            left_upper * right_upper,
        )
        self.add_base(name, min(corners), max(corners))
        self.add_inequality(
            f"mccormick_ll::{name}",
            {
                name: Fraction(-1),
                right: left_lower,
                left: right_lower,
            },
            left_lower * right_lower,
        )
        self.add_inequality(
            f"mccormick_uu::{name}",
            {
                name: Fraction(-1),
                right: left_upper,
                left: right_upper,
            },
            left_upper * right_upper,
        )
        self.add_inequality(
            f"mccormick_ul::{name}",
            {
                name: Fraction(1),
                right: -left_upper,
                left: -right_lower,
            },
            -left_upper * right_lower,
        )
        self.add_inequality(
            f"mccormick_lu::{name}",
            {
                name: Fraction(1),
                right: -left_lower,
                left: -right_upper,
            },
            -left_lower * right_upper,
        )
        self.product_count += 1
        return name

    def set_objective(
        self,
        coefficients: Mapping[str, Rational],
        constant: Rational | int = 0,
    ) -> None:
        unknown = set(coefficients).difference(self.bounds)
        if unknown:
            raise ValueError(f"objective uses unknown variables: {unknown}")
        self.objective = _clean_form(coefficients)
        self.objective_constant = _rational(constant)

    def verify_dual(self, raw_dual: Any) -> dict[str, Any]:
        if not isinstance(raw_dual, dict):
            raise ValueError("dual certificate must be an object")
        raw_inequality = raw_dual.get("inequality_multipliers", {})
        raw_equality = raw_dual.get("equality_multipliers", {})
        if not isinstance(raw_inequality, dict) or not isinstance(raw_equality, dict):
            raise ValueError("dual multiplier collections must be objects")
        inequality_multipliers: dict[str, Rational] = {}
        for name, value in raw_inequality.items():
            if name not in self.inequalities:
                raise ValueError(f"unknown inequality multiplier: {name}")
            multiplier = _rational(value)
            if multiplier < 0:
                raise ValueError(f"negative inequality multiplier: {name}")
            if multiplier:
                inequality_multipliers[name] = multiplier
        equality_multipliers: dict[str, Rational] = {}
        for name, value in raw_equality.items():
            if name not in self.equalities:
                raise ValueError(f"unknown equality multiplier: {name}")
            multiplier = _rational(value)
            if multiplier:
                equality_multipliers[name] = multiplier

        reconstructed: dict[str, Rational] = {}
        upper_bound = self.objective_constant
        for name, multiplier in inequality_multipliers.items():
            constraint = self.inequalities[name]
            _add_scaled(reconstructed, constraint.coefficients, multiplier)
            upper_bound += multiplier * constraint.rhs
        for name, multiplier in equality_multipliers.items():
            constraint = self.equalities[name]
            _add_scaled(reconstructed, constraint.coefficients, multiplier)
            upper_bound += multiplier * constraint.rhs

        if reconstructed != self.objective:
            missing = {
                name: self.objective.get(name, Fraction(0))
                - reconstructed.get(name, Fraction(0))
                for name in set(self.objective) | set(reconstructed)
                if self.objective.get(name, Fraction(0))
                != reconstructed.get(name, Fraction(0))
            }
            raise ValueError(f"dual stationarity mismatch: {missing}")
        claimed = _rational(raw_dual.get("claimed_upper_bound"))
        if claimed != upper_bound:
            raise ValueError("claimed upper bound does not match the exact dual value")
        if upper_bound > 0:
            raise ValueError("dual upper bound is positive")
        return {
            "upper_bound": str(upper_bound),
            "nonzero_inequality_multipliers": len(inequality_multipliers),
            "nonzero_equality_multipliers": len(equality_multipliers),
        }


def _literal_value(
    code: int,
    dimension: int,
    orientation: int,
    literal_index: int,
) -> Rational:
    if literal_index == 0:
        return Fraction(1)
    bit = (code >> (literal_index - 1)) & 1
    if orientation == 1:
        return Fraction(bit)
    if orientation == -1:
        return Fraction(1 - bit)
    raise ValueError("orientation must be +1 or -1")


def _bound_grid(
    raw: Any,
    outer: int,
    inner: int,
    name: str,
) -> list[list[tuple[Rational, Rational]]]:
    if not isinstance(raw, list) or len(raw) != outer:
        raise ValueError(f"{name} has the wrong number of blocks")
    result = []
    for block_index, block in enumerate(raw):
        if not isinstance(block, list) or len(block) != inner:
            raise ValueError(f"{name}[{block_index}] has the wrong width")
        result.append(
            [
                _bound(value, f"{name}[{block_index}][{index}]")
                for index, value in enumerate(block)
            ]
        )
    return result


def linear_box_sum_bounds(
    coefficients: Sequence[Rational],
    bounds: Sequence[tuple[Rational, Rational]],
    total: Rational,
) -> tuple[Rational, Rational]:
    """Optimize a linear form over one box intersected with one sum equality."""
    if len(coefficients) != len(bounds):
        raise ValueError("linear box-sum data have inconsistent lengths")
    lower_sum = sum(lower for lower, _ in bounds)
    upper_sum = sum(upper for _, upper in bounds)
    if not lower_sum <= total <= upper_sum:
        raise ValueError("cell box is incompatible with its block-sum equality")
    baseline = sum(
        coefficient * lower
        for coefficient, (lower, _) in zip(coefficients, bounds)
    )
    remainder = total - lower_sum

    def optimized(reverse: bool) -> Rational:
        value = baseline
        unallocated = remainder
        order = sorted(
            range(len(coefficients)),
            key=lambda index: coefficients[index],
            reverse=reverse,
        )
        for index in order:
            lower, upper = bounds[index]
            increase = min(unallocated, upper - lower)
            value += coefficients[index] * increase
            unallocated -= increase
            if not unallocated:
                break
        if unallocated:
            raise RuntimeError("box-sum optimizer failed to allocate the total")
        return value

    return optimized(False), optimized(True)


def build_signed_secant_mccormick_relaxation(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
) -> tuple[RationalMcCormickRelaxation, dict[str, Any]]:
    """Reconstruct the exact factor-graph relaxation for one certificate leaf."""
    if certificate.get("schema_version") != 1:
        raise ValueError("unsupported schema version")
    if certificate.get("certificate_type") != "signed-secant-mccormick-leaf":
        raise ValueError("wrong certificate type")
    raw_dimension = certificate.get("dimension")
    if isinstance(raw_dimension, bool) or not isinstance(raw_dimension, int):
        raise ValueError("invalid dimension")
    dimension = raw_dimension
    if dimension < 1:
        raise ValueError("invalid dimension")
    checked = validate_signs(signs, dimension)
    if certificate.get("vertex_order") != VERTEX_ORDER:
        raise ValueError("vertex-order mismatch")
    if certificate.get("truth_mask_hex") != hex(mask_from_signs(checked, dimension)):
        raise ValueError("truth-mask mismatch")

    raw_orientations = certificate.get("orientations")
    if not isinstance(raw_orientations, list) or not raw_orientations:
        raise ValueError("orientations must be a nonempty list")
    orientations = []
    for value in raw_orientations:
        if (
            isinstance(value, (bool, np.bool_))
            or not isinstance(value, int)
            or value not in (-1, 1)
        ):
            raise ValueError("orientations must contain only +1 and -1")
        orientations.append(int(value))
    head_count = len(orientations)
    if certificate.get("head_count") != head_count:
        raise ValueError("head count does not match orientations")

    raw_cell = certificate.get("cell")
    if not isinstance(raw_cell, dict):
        raise ValueError("cell must be an object")
    theta_bounds = _bound_grid(
        raw_cell.get("theta_bounds"),
        head_count,
        dimension + 1,
        "theta_bounds",
    )
    direction_bounds = _bound_grid(
        raw_cell.get("direction_bounds"),
        head_count,
        dimension + 1,
        "direction_bounds",
    )
    scalar_bounds = _bound(
        raw_cell.get("scalar_direction_bounds"),
        "scalar_direction_bounds",
    )
    t_bounds = _bound(raw_cell.get("t_bounds"), "t_bounds")
    for block in theta_bounds:
        if any(lower < 0 or upper > 1 for lower, upper in block):
            raise ValueError("theta cell leaves the simplex coordinate box")
    for block in direction_bounds:
        if any(lower < -1 or upper > 1 for lower, upper in block):
            raise ValueError("direction cell leaves the normalized box")
    if scalar_bounds[0] < -1 or scalar_bounds[1] > 1:
        raise ValueError("scalar direction cell leaves the normalized box")
    if t_bounds[0] < 0 or t_bounds[1] > 1:
        raise ValueError("t cell leaves the unit interval")

    chart = certificate.get("chart")
    if (
        not isinstance(chart, dict)
        or isinstance(chart.get("value"), bool)
        or not isinstance(chart.get("value"), int)
        or chart.get("value") not in (-1, 1)
    ):
        raise ValueError("malformed signed-direction chart")
    chart_value = Fraction(int(chart["value"]))
    if chart.get("kind") == "scalar-direction":
        if scalar_bounds != (chart_value, chart_value):
            raise ValueError("scalar chart coordinate is not fixed by the cell")
    elif chart.get("kind") == "direction-coordinate":
        head = chart.get("head")
        literal = chart.get("literal")
        if (
            isinstance(head, bool)
            or isinstance(literal, bool)
            or not isinstance(head, int)
            or not isinstance(literal, int)
            or not (0 <= head < head_count)
            or not (0 <= literal <= dimension)
        ):
            raise ValueError("direction chart coordinate is out of range")
        if direction_bounds[head][literal] != (chart_value, chart_value):
            raise ValueError("direction chart coordinate is not fixed by the cell")
    else:
        raise ValueError("unknown chart kind")

    raw_lambda = certificate.get("lambda")
    if not isinstance(raw_lambda, list) or not raw_lambda:
        raise ValueError("lambda must be a nonempty list")
    weights: list[tuple[int, Rational]] = []
    previous_vertex = -1
    for entry in raw_lambda:
        if not isinstance(entry, dict):
            raise ValueError("lambda entries must be objects")
        vertex = entry.get("vertex")
        if (
            isinstance(vertex, bool)
            or not isinstance(vertex, int)
            or not (0 <= vertex < (1 << dimension))
            or vertex <= previous_vertex
        ):
            raise ValueError("lambda vertices must be strictly ordered and in range")
        weight = _rational(entry.get("weight"))
        if weight <= 0:
            raise ValueError("stored lambda weights must be positive")
        weights.append((vertex, weight))
        previous_vertex = vertex
    if sum(weight for _, weight in weights) != 1:
        raise ValueError("lambda weights must sum to one")

    relaxation = RationalMcCormickRelaxation()
    theta_names: list[list[str]] = []
    direction_names: list[list[str]] = []
    for head in range(head_count):
        theta_block = []
        direction_block = []
        for literal in range(dimension + 1):
            theta_lower, theta_upper = theta_bounds[head][literal]
            direction_lower, direction_upper = direction_bounds[head][literal]
            theta_block.append(
                relaxation.add_base(
                    f"theta_{head}_{literal}",
                    theta_lower,
                    theta_upper,
                )
            )
            direction_block.append(
                relaxation.add_base(
                    f"v_{head}_{literal}",
                    direction_lower,
                    direction_upper,
                )
            )
        theta_names.append(theta_block)
        direction_names.append(direction_block)
    a_name = relaxation.add_base("a", *scalar_bounds)
    t_name = relaxation.add_base("t", *t_bounds)

    z_names: list[list[str]] = []
    for head in range(head_count):
        relaxation.add_equality(
            f"simplex_theta::{head}",
            {name: Fraction(1) for name in theta_names[head]},
            1,
        )
        relaxation.add_equality(
            f"tangent_sum::{head}",
            {name: Fraction(1) for name in direction_names[head]},
            0,
        )
        z_block = []
        for literal in range(dimension + 1):
            z_name = relaxation.add_product(
                f"z_{head}_{literal}",
                t_name,
                direction_names[head][literal],
            )
            z_block.append(z_name)
            relaxation.add_inequality(
                f"endpoint_lower::{head}::{literal}",
                {
                    theta_names[head][literal]: Fraction(-1),
                    z_name: Fraction(-1),
                },
                0,
            )
            relaxation.add_inequality(
                f"endpoint_upper::{head}::{literal}",
                {
                    theta_names[head][literal]: Fraction(1),
                    z_name: Fraction(1),
                },
                1,
            )
        z_names.append(z_block)
        relaxation.add_equality(
            f"rlt_sum_z::{head}",
            {name: Fraction(1) for name in z_block},
            0,
        )

    objective: dict[str, Rational] = {}
    signed_forms: dict[int, dict[str, Rational]] = {}
    for code, weight in weights:
        prefix = f"x{code}"
        b_names = []
        d_names = []
        c_names = []
        for head, orientation in enumerate(orientations):
            literals = [
                _literal_value(code, dimension, orientation, literal)
                for literal in range(dimension + 1)
            ]
            b_bounds = linear_box_sum_bounds(
                literals,
                theta_bounds[head],
                Fraction(1),
            )
            d_bounds = linear_box_sum_bounds(
                literals,
                direction_bounds[head],
                Fraction(0),
            )
            z_block_bounds = [
                relaxation.bounds[name]
                for name in z_names[head]
            ]
            e_bounds = linear_box_sum_bounds(
                literals,
                z_block_bounds,
                Fraction(0),
            )
            b_name = relaxation.add_affine(
                f"{prefix}_b_{head}",
                0,
                {
                    theta_names[head][literal]: literals[literal]
                    for literal in range(dimension + 1)
                    if literals[literal]
                },
                certified_bounds=b_bounds,
            )
            d_name = relaxation.add_affine(
                f"{prefix}_d_{head}",
                0,
                {
                    direction_names[head][literal]: literals[literal]
                    for literal in range(dimension + 1)
                    if literals[literal]
                },
                certified_bounds=d_bounds,
            )
            endpoint_change = relaxation.add_affine(
                f"{prefix}_e_{head}",
                0,
                {
                    z_names[head][literal]: literals[literal]
                    for literal in range(dimension + 1)
                    if literals[literal]
                },
                certified_bounds=e_bounds,
            )
            c_lower = max(Fraction(0), b_bounds[0] + e_bounds[0])
            c_upper = min(Fraction(1), b_bounds[1] + e_bounds[1])
            c_name = relaxation.add_affine(
                f"{prefix}_c_{head}",
                0,
                {b_name: Fraction(1), endpoint_change: Fraction(1)},
                certified_bounds=(c_lower, c_upper),
            )
            b_names.append(b_name)
            d_names.append(d_name)
            c_names.append(c_name)

        p_name = relaxation.add_affine(f"{prefix}_P_0", 1, {})
        r_name = relaxation.add_affine(f"{prefix}_R_0", 0, {})
        c_product_name = relaxation.add_affine(f"{prefix}_C_0", 1, {})
        for head in range(head_count):
            previous_p = p_name
            p_name = relaxation.add_product(
                f"{prefix}_P_{head + 1}",
                previous_p,
                b_names[head],
            )
            r_left = relaxation.add_product(
                f"{prefix}_Rleft_{head + 1}",
                r_name,
                c_names[head],
            )
            r_right = relaxation.add_product(
                f"{prefix}_Rright_{head + 1}",
                previous_p,
                d_names[head],
            )
            r_name = relaxation.add_affine(
                f"{prefix}_R_{head + 1}",
                0,
                {r_left: Fraction(1), r_right: Fraction(1)},
            )
            c_product_name = relaxation.add_product(
                f"{prefix}_C_{head + 1}",
                c_product_name,
                c_names[head],
            )

        t_r_name = relaxation.add_product(f"{prefix}_tR", t_name, r_name)
        relaxation.add_equality(
            f"rlt_endpoint_identity::{prefix}",
            {
                c_product_name: Fraction(1),
                p_name: Fraction(-1),
                t_r_name: Fraction(-1),
            },
            0,
        )
        a_c_name = relaxation.add_product(f"{prefix}_aC", a_name, c_product_name)
        a_p_name = relaxation.add_product(f"{prefix}_aP", a_name, p_name)
        signed_coefficient = Fraction(int(checked[code]), 2)
        signed_form: dict[str, Rational] = {}
        for terminal in (r_name, a_c_name, a_p_name):
            signed_form[terminal] = signed_coefficient
            objective[terminal] = (
                objective.get(terminal, Fraction(0))
                + weight * signed_coefficient
            )
        signed_forms[code] = signed_form

    relaxation.set_objective(objective)
    metadata = {
        "dimension": dimension,
        "head_count": head_count,
        "active_vertices": len(weights),
        "raw_chart_count": 2 * head_count * (dimension + 1) + 2,
        "_signed_forms": signed_forms,
    }
    return relaxation, metadata


def _matrix_data(
    relaxation: RationalMcCormickRelaxation,
) -> tuple[list[str], list[str], list[str]]:
    return (
        list(relaxation.bounds),
        list(relaxation.inequalities),
        list(relaxation.equalities),
    )


def _denominator_limits(max_denominator: int) -> list[int]:
    if max_denominator < 1:
        raise ValueError("max_denominator must be positive")
    limits = []
    current = min(16, max_denominator)
    while True:
        limits.append(current)
        if current == max_denominator:
            break
        current = min(4 * current, max_denominator)
    return limits


def _discover_fixed_objective_dual(
    relaxation: RationalMcCormickRelaxation,
    *,
    support_tolerance: float,
    max_denominator: int,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix

    variable_names, inequality_names, equality_names = _matrix_data(relaxation)
    variable_index = {name: index for index, name in enumerate(variable_names)}
    column_count = len(inequality_names) + len(equality_names)
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    costs = np.zeros(column_count, dtype=float)
    for column, name in enumerate(inequality_names):
        constraint = relaxation.inequalities[name]
        costs[column] = float(constraint.rhs)
        for variable, coefficient in constraint.coefficients.items():
            rows.append(variable_index[variable])
            columns.append(column)
            entries.append(float(coefficient))
    equality_offset = len(inequality_names)
    for local_column, name in enumerate(equality_names):
        column = equality_offset + local_column
        constraint = relaxation.equalities[name]
        costs[column] = float(constraint.rhs)
        for variable, coefficient in constraint.coefficients.items():
            rows.append(variable_index[variable])
            columns.append(column)
            entries.append(float(coefficient))
    stationarity = coo_matrix(
        (entries, (rows, columns)),
        shape=(len(variable_names), column_count),
        dtype=float,
    ).tocsc()
    objective = np.array(
        [float(relaxation.objective.get(name, 0)) for name in variable_names],
        dtype=float,
    )
    result = linprog(
        costs,
        A_eq=stationarity,
        b_eq=objective,
        bounds=(
            [(0.0, None)] * len(inequality_names)
            + [(None, None)] * len(equality_names)
        ),
        method="highs",
    )
    diagnostics: dict[str, Any] = {
        "floating_status": int(result.status),
        "floating_message": str(result.message),
        "floating_objective_upper_bound": (
            None
            if result.fun is None
            else float(result.fun + float(relaxation.objective_constant))
        ),
        "floating_failures_are_lower_bounds": False,
    }
    if not result.success or result.x is None:
        diagnostics["status"] = "floating-dual-failed"
        return None, diagnostics

    last_error = "no rationalization attempted"
    for denominator_limit in _denominator_limits(max_denominator):
        inequality_multipliers: dict[str, Rational] = {}
        equality_multipliers: dict[str, Rational] = {}
        for index, name in enumerate(inequality_names):
            value = float(result.x[index])
            if value > support_tolerance:
                candidate = Fraction(value).limit_denominator(denominator_limit)
                if candidate > 0:
                    inequality_multipliers[name] = candidate
        for local_index, name in enumerate(equality_names):
            value = float(result.x[equality_offset + local_index])
            if abs(value) > support_tolerance:
                candidate = Fraction(value).limit_denominator(denominator_limit)
                if candidate:
                    equality_multipliers[name] = candidate
        upper_bound = relaxation.objective_constant
        for name, multiplier in inequality_multipliers.items():
            upper_bound += multiplier * relaxation.inequalities[name].rhs
        for name, multiplier in equality_multipliers.items():
            upper_bound += multiplier * relaxation.equalities[name].rhs
        raw_dual = {
            "inequality_multipliers": {
                name: str(value)
                for name, value in inequality_multipliers.items()
            },
            "equality_multipliers": {
                name: str(value)
                for name, value in equality_multipliers.items()
            },
            "claimed_upper_bound": str(upper_bound),
        }
        try:
            report = relaxation.verify_dual(raw_dual)
        except ValueError as error:
            last_error = str(error)
            continue
        diagnostics.update(
            {
                "status": "exact-rational-dual-found",
                "rational_denominator_limit": denominator_limit,
                "exact_upper_bound": report["upper_bound"],
                "dual_inequality_support": report[
                    "nonzero_inequality_multipliers"
                ],
                "dual_equality_support": report[
                    "nonzero_equality_multipliers"
                ],
            }
        )
        return raw_dual, diagnostics
    diagnostics.update(
        {
            "status": "rational-dual-reconstruction-failed",
            "last_exact_error": last_error,
        }
    )
    return None, diagnostics


def _floating_common_margin_weights(
    relaxation: RationalMcCormickRelaxation,
    signed_forms: Mapping[int, Mapping[str, Rational]],
) -> tuple[Any, list[int]]:
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix

    variable_names, inequality_names, equality_names = _matrix_data(relaxation)
    vertex_names = sorted(signed_forms)
    variable_index = {name: index for index, name in enumerate(variable_names)}
    inequality_count = len(inequality_names)
    equality_count = len(equality_names)
    equality_offset = inequality_count
    lambda_offset = inequality_count + equality_count
    column_count = lambda_offset + len(vertex_names)
    rows: list[int] = []
    columns: list[int] = []
    entries: list[float] = []
    costs = np.zeros(column_count, dtype=float)
    for column, name in enumerate(inequality_names):
        constraint = relaxation.inequalities[name]
        costs[column] = float(constraint.rhs)
        for variable, coefficient in constraint.coefficients.items():
            rows.append(variable_index[variable])
            columns.append(column)
            entries.append(float(coefficient))
    for local_column, name in enumerate(equality_names):
        column = equality_offset + local_column
        constraint = relaxation.equalities[name]
        costs[column] = float(constraint.rhs)
        for variable, coefficient in constraint.coefficients.items():
            rows.append(variable_index[variable])
            columns.append(column)
            entries.append(float(coefficient))
    for local_column, vertex in enumerate(vertex_names):
        column = lambda_offset + local_column
        for variable, coefficient in signed_forms[vertex].items():
            rows.append(variable_index[variable])
            columns.append(column)
            entries.append(-float(coefficient))
        rows.append(len(variable_names))
        columns.append(column)
        entries.append(1.0)
    equations = coo_matrix(
        (entries, (rows, columns)),
        shape=(len(variable_names) + 1, column_count),
        dtype=float,
    ).tocsc()
    rhs = np.zeros(len(variable_names) + 1, dtype=float)
    rhs[-1] = 1.0
    result = linprog(
        costs,
        A_eq=equations,
        b_eq=rhs,
        bounds=(
            [(0.0, None)] * inequality_count
            + [(None, None)] * equality_count
            + [(0.0, None)] * len(vertex_names)
        ),
        method="highs",
    )
    if result.x is not None:
        result.lambda_values = result.x[lambda_offset:]
    return result, vertex_names


def discover_signed_secant_mccormick_leaf(
    skeleton: dict[str, Any],
    signs: np.ndarray | list[int],
    *,
    active_vertices: Sequence[int] | None = None,
    support_tolerance: float = 1e-8,
    optimum_tolerance: float = 1e-9,
    max_denominator: int = 4096,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Discover a floating common-margin dual and exactify it if possible.

    Every success is passed through the independent exact leaf verifier.
    Failure, a positive relaxation margin, or failed rational reconstruction
    has no lower-bound meaning.
    """
    if support_tolerance <= 0 or optimum_tolerance < 0:
        raise ValueError("invalid floating discovery tolerances")
    raw_dimension = skeleton.get("dimension")
    if isinstance(raw_dimension, bool) or not isinstance(raw_dimension, int):
        raise ValueError("invalid dimension in discovery skeleton")
    vertex_count = 1 << raw_dimension
    if active_vertices is None:
        vertices = list(range(vertex_count))
    else:
        vertices = list(active_vertices)
        if (
            not vertices
            or any(
                isinstance(vertex, bool)
                or not isinstance(vertex, int)
                or not (0 <= vertex < vertex_count)
                for vertex in vertices
            )
            or vertices != sorted(set(vertices))
        ):
            raise ValueError("active vertices must be sorted, unique, and in range")

    working = deepcopy(skeleton)
    uniform_weight = str(Fraction(1, len(vertices)))
    working["lambda"] = [
        {"vertex": vertex, "weight": uniform_weight}
        for vertex in vertices
    ]
    working.pop("dual", None)
    relaxation, metadata = build_signed_secant_mccormick_relaxation(
        working,
        signs,
    )
    signed_forms = metadata.pop("_signed_forms")
    margin_result, ordered_vertices = _floating_common_margin_weights(
        relaxation,
        signed_forms,
    )
    diagnostics: dict[str, Any] = {
        "status": "floating-common-margin-failed",
        "active_vertices": len(vertices),
        "working_variables": len(relaxation.bounds),
        "working_inequalities": len(relaxation.inequalities),
        "working_equalities": len(relaxation.equalities),
        "working_product_nodes": relaxation.product_count,
        "floating_status": int(margin_result.status),
        "floating_message": str(margin_result.message),
        "floating_margin_upper_bound": (
            None if margin_result.fun is None else float(margin_result.fun)
        ),
        "floating_failures_are_lower_bounds": False,
    }
    if not margin_result.success or margin_result.x is None:
        return None, diagnostics
    if float(margin_result.fun) > optimum_tolerance:
        diagnostics["status"] = "relaxed-common-margin-positive"
        return None, diagnostics

    raw_lambda = []
    for vertex, value in zip(ordered_vertices, margin_result.lambda_values):
        if float(value) > support_tolerance:
            rational_value = Fraction(float(value)).limit_denominator(
                max_denominator
            )
            if rational_value > 0:
                raw_lambda.append((vertex, rational_value))
    if not raw_lambda:
        diagnostics["status"] = "lambda-rationalization-empty"
        return None, diagnostics
    lambda_total = sum(weight for _, weight in raw_lambda)
    rational_lambda = [
        (vertex, weight / lambda_total)
        for vertex, weight in raw_lambda
    ]
    candidate = deepcopy(skeleton)
    candidate["lambda"] = [
        {"vertex": vertex, "weight": str(weight)}
        for vertex, weight in rational_lambda
    ]
    candidate.pop("dual", None)
    support_relaxation, support_metadata = (
        build_signed_secant_mccormick_relaxation(candidate, signs)
    )
    support_metadata.pop("_signed_forms")
    dual, dual_diagnostics = _discover_fixed_objective_dual(
        support_relaxation,
        support_tolerance=support_tolerance,
        max_denominator=max_denominator,
    )
    diagnostics.update(
        {
            "candidate_lambda_support": len(rational_lambda),
            "fixed_objective_dual": dual_diagnostics,
        }
    )
    if dual is None:
        diagnostics["status"] = "exact-fixed-objective-dual-not-found"
        return None, diagnostics
    candidate["dual"] = dual
    report = verify_signed_secant_mccormick_leaf(candidate, signs)
    if not report["valid"]:
        diagnostics.update(
            {
                "status": "independent-verification-failed",
                "verification": report,
            }
        )
        return None, diagnostics
    candidate["discovery"] = {
        "method": "floating common-margin dual plus exact rational reconstruction",
        "floating_margin_upper_bound": float(margin_result.fun),
        "floating_failures_are_lower_bounds": False,
    }
    diagnostics.update(
        {
            "status": "verified-exact-leaf-found",
            "exact_upper_bound": report["upper_bound"],
            "verification": report,
        }
    )
    return candidate, diagnostics


def _canonical_cell(
    raw_cell: Any,
    head_count: int,
    dimension: int,
) -> dict[str, Any]:
    if not isinstance(raw_cell, dict):
        raise ValueError("cell must be an object")
    theta_bounds = _bound_grid(
        raw_cell.get("theta_bounds"),
        head_count,
        dimension + 1,
        "theta_bounds",
    )
    direction_bounds = _bound_grid(
        raw_cell.get("direction_bounds"),
        head_count,
        dimension + 1,
        "direction_bounds",
    )
    scalar_bounds = _bound(
        raw_cell.get("scalar_direction_bounds"),
        "scalar_direction_bounds",
    )
    t_bounds = _bound(raw_cell.get("t_bounds"), "t_bounds")

    def rendered(pair: tuple[Rational, Rational]) -> list[str]:
        return [str(pair[0]), str(pair[1])]

    return {
        "theta_bounds": [
            [rendered(pair) for pair in block]
            for block in theta_bounds
        ],
        "direction_bounds": [
            [rendered(pair) for pair in block]
            for block in direction_bounds
        ],
        "scalar_direction_bounds": rendered(scalar_bounds),
        "t_bounds": rendered(t_bounds),
    }


def _split_bound_slot(
    cell: dict[str, Any],
    coordinate: Any,
    head_count: int,
    dimension: int,
) -> list[str]:
    if not isinstance(coordinate, dict):
        raise ValueError("split coordinate must be an object")
    kind = coordinate.get("kind")
    if kind in {"theta", "direction"}:
        head = coordinate.get("head")
        literal = coordinate.get("literal")
        if (
            isinstance(head, bool)
            or isinstance(literal, bool)
            or not isinstance(head, int)
            or not isinstance(literal, int)
            or not (0 <= head < head_count)
            or not (0 <= literal <= dimension)
        ):
            raise ValueError("split coordinate is out of range")
        key = "theta_bounds" if kind == "theta" else "direction_bounds"
        return cell[key][head][literal]
    if kind == "scalar-direction":
        return cell["scalar_direction_bounds"]
    if kind == "t":
        return cell["t_bounds"]
    raise ValueError("unknown split-coordinate kind")


def _full_chart_box(
    chart: dict[str, Any],
    head_count: int,
    dimension: int,
) -> dict[str, Any]:
    theta = [
        [["0", "1"] for _ in range(dimension + 1)]
        for _ in range(head_count)
    ]
    direction = [
        [["-1", "1"] for _ in range(dimension + 1)]
        for _ in range(head_count)
    ]
    scalar = ["-1", "1"]
    value = str(int(chart["value"]))
    if chart["kind"] == "scalar-direction":
        scalar = [value, value]
    elif chart["kind"] == "direction-coordinate":
        direction[chart["head"]][chart["literal"]] = [value, value]
    else:
        raise ValueError("unknown chart kind")
    return {
        "theta_bounds": theta,
        "direction_bounds": direction,
        "scalar_direction_bounds": scalar,
        "t_bounds": ["0", "1"],
    }


def verify_signed_secant_cell_cover(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
) -> dict[str, Any]:
    """Verify a binary subdivision tree whose leaves are exact cell duals."""
    try:
        if certificate.get("schema_version") != 1:
            raise ValueError("unsupported schema version")
        if certificate.get("certificate_type") != "signed-secant-cell-cover":
            raise ValueError("wrong certificate type")
        raw_dimension = certificate.get("dimension")
        if isinstance(raw_dimension, bool) or not isinstance(raw_dimension, int):
            raise ValueError("invalid dimension")
        dimension = raw_dimension
        raw_orientations = certificate.get("orientations")
        if not isinstance(raw_orientations, list) or not raw_orientations:
            raise ValueError("orientations must be a nonempty list")
        head_count = len(raw_orientations)
        if certificate.get("head_count") != head_count:
            raise ValueError("head count does not match orientations")
        chart = certificate.get("chart")
        root_cell = _canonical_cell(
            certificate.get("root_cell"),
            head_count,
            dimension,
        )
        common = {
            "schema_version": 1,
            "certificate_type": "signed-secant-mccormick-leaf",
            "dimension": dimension,
            "vertex_order": certificate.get("vertex_order"),
            "truth_mask_hex": certificate.get("truth_mask_hex"),
            "head_count": head_count,
            "orientations": raw_orientations,
            "chart": chart,
        }
        root_probe = {
            **common,
            "cell": root_cell,
            "lambda": [{"vertex": 0, "weight": "1"}],
        }
        root_relaxation, root_metadata = (
            build_signed_secant_mccormick_relaxation(root_probe, signs)
        )
        root_metadata.pop("_signed_forms")
        del root_relaxation

        node_count = 0
        split_count = 0
        leaf_count = 0
        maximum_depth = 0
        total_dual_support = 0

        def recurse(node: Any, expected_cell: dict[str, Any], depth: int) -> None:
            nonlocal node_count
            nonlocal split_count
            nonlocal leaf_count
            nonlocal maximum_depth
            nonlocal total_dual_support
            node_count += 1
            maximum_depth = max(maximum_depth, depth)
            if not isinstance(node, dict):
                raise ValueError("cover nodes must be objects")
            has_leaf = "leaf" in node
            has_split = "split" in node
            if has_leaf == has_split:
                raise ValueError("each cover node must be exactly one leaf or split")
            if has_leaf:
                payload = node["leaf"]
                if not isinstance(payload, dict):
                    raise ValueError("leaf payload must be an object")
                leaf_certificate = {
                    **common,
                    "cell": expected_cell,
                    "lambda": payload.get("lambda"),
                    "dual": payload.get("dual"),
                }
                report = verify_signed_secant_mccormick_leaf(
                    leaf_certificate,
                    signs,
                )
                if not report["valid"]:
                    raise ValueError(f"invalid cover leaf: {report['reason']}")
                leaf_count += 1
                total_dual_support += int(
                    report["nonzero_inequality_multipliers"]
                ) + int(report["nonzero_equality_multipliers"])
                return

            split = node["split"]
            if not isinstance(split, dict):
                raise ValueError("split payload must be an object")
            if "left" not in node or "right" not in node:
                raise ValueError("split nodes need left and right children")
            left_cell = deepcopy(expected_cell)
            right_cell = deepcopy(expected_cell)
            left_slot = _split_bound_slot(
                left_cell,
                split.get("coordinate"),
                head_count,
                dimension,
            )
            right_slot = _split_bound_slot(
                right_cell,
                split.get("coordinate"),
                head_count,
                dimension,
            )
            lower = _rational(left_slot[0])
            upper = _rational(left_slot[1])
            pivot = _rational(split.get("value"))
            if not lower < pivot < upper:
                raise ValueError("split pivot must be strictly inside its interval")
            left_slot[1] = str(pivot)
            right_slot[0] = str(pivot)
            split_count += 1
            recurse(node["left"], left_cell, depth + 1)
            recurse(node["right"], right_cell, depth + 1)

        recurse(certificate.get("tree"), root_cell, 0)
        canonical_full = _canonical_cell(
            _full_chart_box(chart, head_count, dimension),
            head_count,
            dimension,
        )
        full_chart = root_cell == canonical_full
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        return {"valid": False, "reason": str(error)}
    return {
        "valid": True,
        "dimension": dimension,
        "head_count": head_count,
        "nodes": node_count,
        "splits": split_count,
        "leaves": leaf_count,
        "maximum_depth": maximum_depth,
        "total_dual_support": total_dual_support,
        "root_is_full_chart_box": full_chart,
        "chart_infeasible": full_chart,
        "global_head_lower_bound": False,
        "conclusion": (
            "the entire normalized chart is infeasible"
            if full_chart
            else "the declared chart subcell is infeasible; no global lower bound follows"
        ),
    }


def verify_signed_secant_mccormick_leaf(
    certificate: dict[str, Any],
    signs: np.ndarray | list[int],
) -> dict[str, Any]:
    """Verify one rational cell leaf independently of any floating LP solver."""
    try:
        relaxation, metadata = build_signed_secant_mccormick_relaxation(
            certificate,
            signs,
        )
        metadata.pop("_signed_forms")
        dual_report = relaxation.verify_dual(certificate.get("dual"))
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        return {"valid": False, "reason": str(error)}
    return {
        "valid": True,
        **metadata,
        "variables": len(relaxation.bounds),
        "linear_inequalities": len(relaxation.inequalities),
        "linear_equalities": len(relaxation.equalities),
        "affine_nodes": relaxation.affine_count,
        "product_nodes": relaxation.product_count,
        **dual_report,
        "conclusion": "the signed-secant chart cell has no strictly feasible point",
    }


__all__ = [
    "RationalMcCormickRelaxation",
    "build_signed_secant_mccormick_relaxation",
    "discover_signed_secant_mccormick_leaf",
    "linear_box_sum_bounds",
    "verify_signed_secant_cell_cover",
    "verify_signed_secant_mccormick_leaf",
]
