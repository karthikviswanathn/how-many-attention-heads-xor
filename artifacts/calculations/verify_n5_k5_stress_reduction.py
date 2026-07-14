#!/usr/bin/env python3
"""Verify the finite algebra in the five-bit K5 stress reduction.

This script does not prove the remaining affine existence claim. It checks the
exact rank counts, harmonic identities, exceptional four-factor
classification, stress signs, one exact oriented Schur certificate, and
coefficient expansion used in
n5_universal_h2_theorem_lead.md.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product


DIMENSION = 5
VERTICES = tuple(range(DIMENSION))
EDGES = tuple(combinations(VERTICES, 2))
ZERO_EXPONENT = (0,) * DIMENSION


def clean(polynomial: dict[tuple[int, ...], int]) -> dict[tuple[int, ...], int]:
    return {monomial: coefficient for monomial, coefficient in polynomial.items()
            if coefficient}


def multiply(
    first: dict[tuple[int, ...], int],
    second: dict[tuple[int, ...], int],
) -> dict[tuple[int, ...], int]:
    result: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for first_monomial, first_coefficient in first.items():
        for second_monomial, second_coefficient in second.items():
            monomial = tuple(
                first_monomial[index] + second_monomial[index]
                for index in VERTICES
            )
            result[monomial] += first_coefficient * second_coefficient
    return clean(dict(result))


def difference(edge: tuple[int, int]) -> dict[tuple[int, ...], int]:
    first, second = edge
    first_monomial = [0] * DIMENSION
    second_monomial = [0] * DIMENSION
    first_monomial[first] = 1
    second_monomial[second] = 1
    return {tuple(first_monomial): 1, tuple(second_monomial): -1}


def edge_product(edges: tuple[tuple[int, int], ...]) -> dict[tuple[int, ...], int]:
    result = {ZERO_EXPONENT: 1}
    for edge in edges:
        result = multiply(result, difference(edge))
    return result


def laplacian(
    polynomial: dict[tuple[int, ...], int],
) -> dict[tuple[int, ...], int]:
    result: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for monomial, coefficient in polynomial.items():
        for index, exponent in enumerate(monomial):
            if exponent < 2:
                continue
            derivative = list(monomial)
            derivative[index] -= 2
            result[tuple(derivative)] += coefficient * exponent * (exponent - 1)
    return clean(dict(result))


def complementary_triangle(edge: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    remaining = tuple(index for index in VERTICES if index not in edge)
    return tuple(combinations(remaining, 2))


def basis_polynomial(edge: tuple[int, int]) -> dict[tuple[int, ...], int]:
    return edge_product((edge,) + complementary_triangle(edge))


def rational_rank(matrix: list[list[int | Fraction]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def evaluate_difference(values: tuple[int, ...], edge: tuple[int, int]) -> int:
    return values[edge[0]] - values[edge[1]]


def evaluate_basis(values: tuple[int, ...], edge: tuple[int, int]) -> int:
    result = evaluate_difference(values, edge)
    for triangle_edge in complementary_triangle(edge):
        result *= evaluate_difference(values, triangle_edge)
    return result


def verify_harmonic_classification() -> None:
    basis = [basis_polynomial(edge) for edge in EDGES]
    assert all(not laplacian(polynomial) for polynomial in basis)

    monomials = sorted({monomial for polynomial in basis for monomial in polynomial})
    coefficient_matrix = [
        [polynomial.get(monomial, 0) for polynomial in basis]
        for monomial in monomials
    ]
    assert rational_rank(coefficient_matrix) == 5

    additive_edges = []
    for vertex in VERTICES:
        additive_edges.append([
            int(vertex in edge) for edge in EDGES
        ])
    assert rational_rank(additive_edges) == 5
    for additive_table in additive_edges:
        combined: defaultdict[tuple[int, ...], int] = defaultdict(int)
        for edge, coefficient, polynomial in zip(EDGES, additive_table, basis):
            signed_coefficient = coefficient * (-1) ** (edge[0] + edge[1])
            for monomial, value in polynomial.items():
                combined[monomial] += signed_coefficient * value
        assert not clean(dict(combined))

    harmonic_products: set[tuple[tuple[int, int], ...]] = set()
    for edge_indices in combinations_with_replacement(range(len(EDGES)), 4):
        edges = tuple(EDGES[index] for index in edge_indices)
        if not laplacian(edge_product(edges)):
            harmonic_products.add(tuple(sorted(edges)))

    expected = {
        tuple(sorted((edge,) + complementary_triangle(edge))) for edge in EDGES
    }
    assert harmonic_products == expected
    print("edge-triangle span: rank 5 with the additive-edge kernel")
    print("harmonic four-collision products: exactly 10 complementary edge-triangles")


def verify_pair_stress() -> None:
    values = (0, 1, 3, 7, 12)
    barycentric = []
    for index in VERTICES:
        denominator = 1
        for other in VERTICES:
            if other != index:
                denominator *= values[index] - values[other]
        barycentric.append(Fraction(1, denominator))

    stresses: dict[tuple[int, int], Fraction] = {}
    for first, second in EDGES:
        stresses[(first, second)] = (
            barycentric[first]
            * barycentric[second]
            * (values[first] - values[second]) ** 2
        )

    for index in VERTICES:
        row_sum = Fraction(0)
        moment_sum = Fraction(0)
        for other in VERTICES:
            if other == index:
                continue
            edge = tuple(sorted((index, other)))
            weight = stresses[edge]
            row_sum += weight
            moment_sum += weight * (values[other] - values[index])
        assert row_sum == 0
        assert moment_sum == 0

    vandermonde = 1
    for edge in EDGES:
        vandermonde *= evaluate_difference(values, edge)
    for first, second in EDGES:
        expected = (-1) ** (first + second) * evaluate_basis(
            values, (first, second)
        )
        assert vandermonde * stresses[(first, second)] == expected

    pair_matrix: list[list[int]] = []
    for first, second in EDGES:
        row = [0] * 10
        row[first] = 1
        row[second] = 1
        row[5 + first] = values[second] - values[first]
        row[5 + second] = values[first] - values[second]
        pair_matrix.append(row)
    assert rational_rank(pair_matrix) == 9

    exceptional_t = (2, 3, 5, 5, 5)
    exceptional_u = (Fraction(-7, 2), 0, 0, 0, 0)
    exceptional_r = (Fraction(21, 2), 0, 0, 0, 0)
    exceptional_values = {}
    for first, second in EDGES:
        exceptional_values[(first, second)] = (
            exceptional_r[first]
            + exceptional_r[second]
            + (exceptional_u[first] - exceptional_u[second])
            * (exceptional_t[second] - exceptional_t[first])
        )
    assert exceptional_values[(0, 1)] == 7
    assert all(
        value == 0 for edge, value in exceptional_values.items()
        if edge != (0, 1)
    )
    print("K5 pair map: rank 9 with the stated exact stress")
    print("exceptional single-edge pair construction: verified")


def affine(coefficients: tuple[int, ...], point: tuple[int, ...]) -> int:
    return coefficients[0] + sum(
        coefficients[index + 1] * point[index] for index in range(5)
    )


def symmetric_product(
    first: tuple[int, ...], second: tuple[int, ...]
) -> list[list[Fraction]]:
    return [
        [
            Fraction(
                first[row] * second[column]
                + second[row] * first[column],
                2,
            )
            for column in range(6)
        ]
        for row in range(6)
    ]


def add_matrices(
    first: list[list[Fraction]], second: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [left + right for left, right in zip(first_row, second_row)]
        for first_row, second_row in zip(first, second)
    ]


def quadratic_value(matrix: list[list[Fraction]], vector: tuple[int, ...]) -> Fraction:
    return sum(
        matrix[row][column] * vector[row] * vector[column]
        for row in range(6)
        for column in range(6)
    )


def matrix_vector_product(
    matrix: list[list[Fraction]], vector: tuple[int, ...]
) -> tuple[Fraction, ...]:
    return tuple(
        sum(entry * coordinate for entry, coordinate in zip(row, vector))
        for row in matrix
    )


def verify_dual_isotropic_factor_criterion() -> None:
    matrix = [
        [Fraction(int(row == column) * sign) for column in range(6)]
        for row, sign in enumerate((1, 1, -1, -1, 0, 0))
    ]
    factor = (1, 0, 1, 0, 0, 0)
    dual_factor = (1, 0, -1, 0, 0, 0)
    first = (0, 1, 0, 1, 0, 0)
    second = (0, 1, 0, -1, 0, 0)

    inverse_on_image = matrix
    inverse_times_factor = matrix_vector_product(inverse_on_image, factor)
    assert inverse_times_factor == dual_factor
    assert sum(
        left * right for left, right in zip(factor, inverse_times_factor)
    ) == 0

    reconstructed = add_matrices(
        symmetric_product(dual_factor, factor),
        symmetric_product(first, second),
    )
    assert reconstructed == matrix
    assert rational_rank(matrix) == 4
    print("rank-four dual-isotropic criterion: exact rational reconstruction verified")


def verify_schur_rank_four_completion() -> None:
    core_diagonal = (20, -10, -10, 2)
    first_cross = (1, 2, 3, 4)
    second_cross = (5, 6, 7, 8)
    inverse_diagonal = tuple(Fraction(1, value) for value in core_diagonal)

    outside_cross = sum(
        Fraction(first_cross[index] * second_cross[index])
        * inverse_diagonal[index]
        for index in range(4)
    )
    first_outside_diagonal = sum(
        Fraction(value * value) * inverse_diagonal[index]
        for index, value in enumerate(first_cross)
    )
    second_outside_diagonal = sum(
        Fraction(value * value) * inverse_diagonal[index]
        for index, value in enumerate(second_cross)
    )

    matrix = [[Fraction(0) for _ in range(6)] for _ in range(6)]
    for index, value in enumerate(core_diagonal):
        matrix[index][index] = Fraction(value)
    for index in range(4):
        matrix[index][4] = matrix[4][index] = Fraction(first_cross[index])
        matrix[index][5] = matrix[5][index] = Fraction(second_cross[index])
    matrix[4][4] = first_outside_diagonal
    matrix[5][5] = second_outside_diagonal
    matrix[4][5] = matrix[5][4] = outside_cross

    assert rational_rank(matrix) == 4
    for outside_column, cross in ((4, first_cross), (5, second_cross)):
        dependence = [
            -Fraction(cross[index], core_diagonal[index]) for index in range(4)
        ] + [Fraction(int(index == outside_column)) for index in (4, 5)]
        assert all(
            value == 0 for value in matrix_vector_product(matrix, tuple(dependence))
        )
    assert sum(core_diagonal) == 2
    assert sum(value > 0 for value in core_diagonal) == 2
    assert sum(value < 0 for value in core_diagonal) == 2
    print("generic Schur completion: exact rank-four block certificate verified")


def verify_monochromatic_triangle_orientation() -> None:
    core_diagonal = (
        Fraction(-10000),
        Fraction(20000),
        Fraction(-10000),
        Fraction(32, 33),
    )
    first_cross = (Fraction(0), Fraction(0), Fraction(0), Fraction(8))
    second_cross = first_cross
    inverse_diagonal = tuple(Fraction(1, value) for value in core_diagonal)

    matrix = [[Fraction(0) for _ in range(6)] for _ in range(6)]
    for index, value in enumerate(core_diagonal):
        matrix[index][index] = value
    for index in range(4):
        matrix[index][4] = matrix[4][index] = first_cross[index]
        matrix[index][5] = matrix[5][index] = second_cross[index]

    first_outside_diagonal = sum(
        first_cross[index] * first_cross[index] * inverse_diagonal[index]
        for index in range(4)
    )
    outside_cross = sum(
        first_cross[index] * second_cross[index] * inverse_diagonal[index]
        for index in range(4)
    )
    second_outside_diagonal = sum(
        second_cross[index] * second_cross[index] * inverse_diagonal[index]
        for index in range(4)
    )
    matrix[4][4] = first_outside_diagonal
    matrix[4][5] = matrix[5][4] = outside_cross
    matrix[5][5] = second_outside_diagonal

    assert matrix[3][4] == 8
    assert matrix[3][5] == 8
    assert matrix[4][5] == 66
    assert rational_rank(matrix) == 4
    assert sum(value > 0 for value in core_diagonal) == 2
    assert sum(value < 0 for value in core_diagonal) == 2

    core_factor = (
        Fraction(1),
        Fraction(1, 4),
        Fraction(1, 4),
        Fraction(1, 100),
    )
    core_preimage = tuple(
        core_factor[index] * inverse_diagonal[index] for index in range(4)
    )
    preimage = core_preimage + (Fraction(0), Fraction(0))
    factor = matrix_vector_product(matrix, preimage)

    assert factor == (
        Fraction(1),
        Fraction(1, 4),
        Fraction(1, 4),
        Fraction(1, 100),
        Fraction(33, 400),
        Fraction(33, 400),
    )
    assert factor[0] > sum(factor[1:])
    assert all(value > 0 for value in factor[1:])
    assert sum(
        preimage[index] * factor[index] for index in range(6)
    ) == 0
    print("monochromatic slope triangle: exact admissible dual-isotropic factor verified")


def dot(first: tuple[int, ...], second: tuple[int, ...]) -> int:
    return sum(left * right for left, right in zip(first, second))


def verify_endpoint_boundary_reduction() -> None:
    q_zero = 2
    t = (-8, 1, 3, -1, 5)
    boundary_factor = (1, 1, 1, 1, 1)
    boundary_numerator = (1, -1, 0, 0, 0)
    residual_vector = (0, 0, 1, -1, 0)

    spatial_matrix = add_matrices(
        symmetric_product(
            (0,) + boundary_numerator,
            (0,) + boundary_factor,
        ),
        [
            [
                Fraction(-2 * residual_vector[row - 1] * residual_vector[column - 1])
                if row and column else Fraction(0)
                for column in range(6)
            ]
            for row in range(6)
        ],
    )
    reduced_spatial = [row[1:] for row in spatial_matrix[1:]]
    assert rational_rank(reduced_spatial) == 3

    image_of_numerator = matrix_vector_product(
        reduced_spatial, boundary_numerator
    )
    assert image_of_numerator == boundary_factor
    assert dot(boundary_factor, boundary_numerator) == 0
    assert dot(boundary_factor, residual_vector) == 0
    assert dot(boundary_numerator, residual_vector) == 0
    assert dot(boundary_factor, boundary_factor) == 5
    assert dot(boundary_numerator, boundary_numerator) == 2
    assert dot(residual_vector, residual_vector) == 2

    linear = tuple(
        q_zero * (2 * t[index] + t[index] * t[index])
        - 2 * residual_vector[index] * residual_vector[index]
        + boundary_numerator[index] * boundary_factor[index]
        for index in range(5)
    )
    pairs = {
        (first, second): (
            2 * q_zero * t[first] * t[second]
            - 4 * residual_vector[first] * residual_vector[second]
            + boundary_numerator[first] * boundary_factor[second]
            + boundary_numerator[second] * boundary_factor[first]
        )
        for first, second in EDGES
    }
    recovered_spatial = [[Fraction(0) for _ in range(5)] for _ in range(5)]
    for index in range(5):
        recovered_spatial[index][index] = (
            linear[index] - q_zero * (2 * t[index] + t[index] * t[index])
        )
    for (first, second), coefficient in pairs.items():
        value = Fraction(coefficient, 2) - q_zero * t[first] * t[second]
        recovered_spatial[first][second] = value
        recovered_spatial[second][first] = value
    assert recovered_spatial == reduced_spatial

    first_factor = (1,) + tuple(
        t[index] + residual_vector[index] for index in range(5)
    )
    second_factor = (q_zero,) + tuple(
        q_zero * (t[index] - residual_vector[index]) for index in range(5)
    )
    numerator = (0,) + boundary_numerator
    boundary = (0,) + boundary_factor
    epsilon = Fraction(1, 2)
    perturbed_boundary = (epsilon,) + boundary_factor
    shift = 17
    shifted_factor = tuple(
        Fraction(value) + shift * added
        for value, added in zip(second_factor, perturbed_boundary)
    )
    shifted_numerator = tuple(
        Fraction(value) - shift * subtracted
        for value, subtracted in zip(numerator, first_factor)
    )
    assert all(value > 0 for value in shifted_factor)
    assert all(value > 0 for value in shifted_factor[1:])

    original_values = []
    perturbed_values = []
    for point in product((0, 1), repeat=5):
        original = (
            affine(first_factor, point) * affine(second_factor, point)
            + affine(numerator, point) * affine(boundary, point)
        )
        expanded = q_zero
        expanded += sum(
            linear[index] * point[index] for index in range(5)
        )
        expanded += sum(
            coefficient * point[first] * point[second]
            for (first, second), coefficient in pairs.items()
        )
        assert original == expanded
        perturbed = Fraction(original) + epsilon * affine(numerator, point)
        reconstructed = (
            affine(first_factor, point) * affine(shifted_factor, point)
            + affine(shifted_numerator, point)
            * affine(perturbed_boundary, point)
        )
        assert perturbed == reconstructed
        original_values.append(Fraction(original))
        perturbed_values.append(perturbed)
    assert all(value for value in original_values)
    assert all(
        (original > 0) == (perturbed > 0)
        for original, perturbed in zip(original_values, perturbed_values)
    )
    print("endpoint-boundary reduction: rank-three criterion and inward perturbation verified")


def verify_canonical_complementary_cycle_cell() -> None:
    cycle_edges = {
        tuple(sorted((index, (index + 1) % 5))) for index in range(5)
    }
    canonical_positive_vertices = {0}
    canonical_positive_vertices.update(
        (1 << first) | (1 << second) for first, second in cycle_edges
    )

    first_numerator = (-1, -29, -51, 57, -24, -29)
    free_factor = (-1, -2, 2, 2, 1, 0)
    boundary_numerator = (-34, -57, 51, -24, 32, 3)
    boundary_factor = (0, 1, 1, 1, 1, 1)

    boundary_scores = []
    boundary_numerator_values = []
    canonical_values = []
    for code in range(32):
        point = tuple((code >> index) & 1 for index in range(5))
        support_size = sum(point)
        induced_edges = sum(
            point[first] * point[second] for first, second in cycle_edges
        )
        canonical_value = 1 - 2 * support_size * support_size + 8 * induced_edges
        expected_positive = code in canonical_positive_vertices
        assert (canonical_value > 0) == expected_positive

        boundary_value = (
            affine(first_numerator, point) * affine(free_factor, point)
            + affine(boundary_numerator, point)
            * affine(boundary_factor, point)
        )
        assert (boundary_value > 0) == expected_positive
        canonical_values.append(canonical_value)
        boundary_scores.append(boundary_value)
        boundary_numerator_values.append(affine(boundary_numerator, point))

    signed_boundary_values = [
        value if code in canonical_positive_vertices else -value
        for code, value in enumerate(boundary_scores)
    ]
    assert min(signed_boundary_values) == 1
    assert max(abs(value) for value in boundary_numerator_values) == 115

    for first, second in EDGES:
        if (first, second) in cycle_edges:
            base = 0
            expected_pattern = (True, False, False, True)
        else:
            common_neighbors = [
                index for index in VERTICES
                if tuple(sorted((index, first))) in cycle_edges
                and tuple(sorted((index, second))) in cycle_edges
            ]
            assert len(common_neighbors) == 1
            base = 1 << common_neighbors[0]
            expected_pattern = (False, True, True, False)
        face = (
            base,
            base | (1 << first),
            base | (1 << second),
            base | (1 << first) | (1 << second),
        )
        assert tuple(code in canonical_positive_vertices for code in face) == expected_pattern

    epsilon = Fraction(1, 256)
    perturbed_boundary = (epsilon, 1, 1, 1, 1, 1)
    shift = 257
    shifted_factor = tuple(
        Fraction(value) + shift * added
        for value, added in zip(free_factor, perturbed_boundary)
    )
    shifted_numerator = tuple(
        Fraction(value) - shift * subtracted
        for value, subtracted in zip(boundary_numerator, first_numerator)
    )
    assert shifted_factor == (
        Fraction(1, 256),
        Fraction(255),
        Fraction(259),
        Fraction(259),
        Fraction(258),
        Fraction(257),
    )
    assert all(value > 0 for value in perturbed_boundary)
    assert all(value > 0 for value in shifted_factor)

    for code in range(32):
        point = tuple((code >> index) & 1 for index in range(5))
        genuine_score = (
            affine(first_numerator, point) * affine(shifted_factor, point)
            + affine(shifted_numerator, point)
            * affine(perturbed_boundary, point)
        )
        expected_score = (
            Fraction(boundary_scores[code])
            + epsilon * boundary_numerator_values[code]
        )
        assert genuine_score == expected_score
        assert (genuine_score > 0) == (code in canonical_positive_vertices)
    print("canonical complementary-cycle cell: exact positive-endpoint H2 certificate verified")


def verify_boolean_matrix_completion() -> None:
    monomials = tuple(combinations_with_replacement(range(6), 2))
    monomial_index = {monomial: index for index, monomial in enumerate(monomials)}
    evaluation = []
    for signs in product((-1, 1), repeat=5):
        vector = (1,) + signs
        evaluation.append([
            vector[first] * vector[second] for first, second in monomials
        ])
    assert rational_rank(evaluation) == 16

    relations = []
    for index in range(1, 6):
        row = [0] * len(monomials)
        row[monomial_index[(index, index)]] = 1
        row[monomial_index[(0, 0)]] = -1
        relations.append(row)
    assert rational_rank(relations) == 5
    for relation in relations:
        assert all(
            sum(coefficient * value for coefficient, value in zip(relation, row)) == 0
            for row in evaluation
        )

    first_numerator = (2, -1, 3, 0, 4, -2)
    free_factor = (-3, 5, 1, -4, 2, 6)
    second_numerator = (1, 2, -2, 5, -1, 3)
    oriented_factor = (10, 1, 2, 1, 1, 1)
    assert oriented_factor[0] > sum(abs(value) for value in oriented_factor[1:])
    assert all(value > 0 for value in oriented_factor[1:])

    matrix = add_matrices(
        symmetric_product(first_numerator, free_factor),
        symmetric_product(second_numerator, oriented_factor),
    )
    assert rational_rank(matrix) <= 4

    lambdas = [matrix[index][index] for index in range(1, 6)]
    constant = matrix[0][0] + sum(lambdas)
    linear = [2 * matrix[0][index] for index in range(1, 6)]
    pairs = {
        (first, second): 2 * matrix[first][second]
        for first, second in combinations(range(1, 6), 2)
    }

    completion = [[Fraction(0) for _ in range(6)] for _ in range(6)]
    completion[0][0] = constant - sum(lambdas)
    for index in range(1, 6):
        completion[0][index] = linear[index - 1] / 2
        completion[index][0] = linear[index - 1] / 2
        completion[index][index] = lambdas[index - 1]
    for (first, second), coefficient in pairs.items():
        completion[first][second] = coefficient / 2
        completion[second][first] = coefficient / 2
    assert completion == matrix

    for signs in product((-1, 1), repeat=5):
        vector = (1,) + signs
        reduced = constant
        reduced += sum(
            linear[index] * signs[index] for index in range(5)
        )
        reduced += sum(
            coefficient * signs[first - 1] * signs[second - 1]
            for (first, second), coefficient in pairs.items()
        )
        assert quadratic_value(completion, vector) == reduced

    print("sign-cube quadratic kernel: exactly five trace-preserving diagonal shifts")
    print("admissible-factor matrix completion: exact factor and reduction verified")


def verify_full_expansion_and_rank() -> None:
    b = (3, 2, 5, 1, 4, 6)
    t_zero = 2
    t = (1, 3, 4, 7, 11)
    u_zero = -2
    u = (3, -1, 5, 2, -4)
    v_zero = 4
    v = (-5, 6, 1, -3, 2)
    r_zero = u_zero * t_zero + v_zero
    r = tuple(u[index] * t[index] + v[index] for index in range(5))

    q_zero = b[0] * b[0] * r_zero
    q_linear = tuple(
        b[0]
        * b[index + 1]
        * (
            r_zero
            + r[index]
            + (u_zero - u[index]) * (t[index] - t_zero)
        )
        + b[index + 1] * b[index + 1] * r[index]
        for index in range(5)
    )
    q_pairs = {
        (first, second): b[first + 1] * b[second + 1] * (
            r[first]
            + r[second]
            + (u[first] - u[second]) * (t[second] - t[first])
        )
        for first, second in EDGES
    }

    first_denominator = b
    second_denominator = (b[0] * t_zero,) + tuple(
        b[index + 1] * t[index] for index in range(5)
    )
    first_numerator = (b[0] * u_zero,) + tuple(
        b[index + 1] * u[index] for index in range(5)
    )
    second_numerator = (b[0] * v_zero,) + tuple(
        b[index + 1] * v[index] for index in range(5)
    )
    for point in product((0, 1), repeat=5):
        cleared = (
            affine(first_numerator, point) * affine(second_denominator, point)
            + affine(second_numerator, point) * affine(first_denominator, point)
        )
        expanded = q_zero
        expanded += sum(q_linear[index] * point[index] for index in range(5))
        expanded += sum(
            coefficient * point[first] * point[second]
            for (first, second), coefficient in q_pairs.items()
        )
        assert cleared == expanded

    loop_matrix: list[list[Fraction]] = []
    for index in range(5):
        row = [Fraction(0)] * 11
        row[index] = 1 + Fraction(b[index + 1], b[0])
        row[5] = t[index] - t_zero
        row[6 + index] = t_zero - t[index]
        loop_matrix.append(row)
    for first, second in EDGES:
        row = [Fraction(0)] * 11
        row[first] = 1
        row[second] = 1
        row[6 + first] = t[second] - t[first]
        row[6 + second] = t[first] - t[second]
        loop_matrix.append(row)
    assert rational_rank(loop_matrix) == 10
    assert len(loop_matrix) - rational_rank(loop_matrix) == 5
    print("full Boolean loop map: rank 10 with a five-dimensional stress space")
    print("full diagonally scaled coefficient expansion: verified on all 32 inputs")


def main() -> None:
    verify_harmonic_classification()
    verify_pair_stress()
    verify_boolean_matrix_completion()
    verify_dual_isotropic_factor_criterion()
    verify_schur_rank_four_completion()
    verify_monochromatic_triangle_orientation()
    verify_endpoint_boundary_reduction()
    verify_canonical_complementary_cycle_cell()
    verify_full_expansion_and_rank()
    print("five-bit K5 stress reduction: finite algebra verified")


if __name__ == "__main__":
    main()
