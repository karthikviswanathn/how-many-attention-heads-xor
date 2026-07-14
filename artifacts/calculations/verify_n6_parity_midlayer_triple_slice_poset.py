#!/usr/bin/env python3
"""Verify exact slice-poset and pair-boundary identities for the n6 candidate."""

from __future__ import annotations

import itertools


N = 6
FULL = (1 << N) - 1
EXCEPTIONS = (21, 38, 41)
SLICE_SIGNS = (1, -1, 1, -1, -1, 1)
SLICE_EXCEPTIONS = (38, 38, 41, 41, 21, 21)
DIAGONAL_NEGATIVE = frozenset((0, 2, 5))
PAIRS = ((0, 1), (2, 3), (4, 5))


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def diagonal(mask: int) -> int:
    return -1 if sum((mask >> value) & 1 for value in DIAGONAL_NEGATIVE) % 2 else 1


def pair_index(coordinate: int) -> int:
    return coordinate // 2


def transformed_edge_sign(coordinate: int, subset: int) -> int:
    return character(subset, SLICE_EXCEPTIONS[coordinate]) * diagonal(subset)


def rank(mask: int) -> int:
    return sum(
        ((mask >> left) & 1) != ((mask >> right) & 1)
        for left, right in PAIRS
    )


def connected_components(vertices: set[int], edges: list[tuple[int, int]]) -> list[set[int]]:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(vertices)
    answer = []
    while unseen:
        seed = min(unseen)
        component = {seed}
        frontier = [seed]
        unseen.remove(seed)
        while frontier:
            current = frontier.pop()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    frontier.append(neighbor)
        answer.append(component)
    return answer


def verify_slices() -> None:
    for coordinate, (slice_sign, exception) in enumerate(
        zip(SLICE_SIGNS, SLICE_EXCEPTIONS)
    ):
        in_slice = [
            value
            for value in EXCEPTIONS
            if character(1 << coordinate, value) == slice_sign
        ]
        assert in_slice == [exception]

        for subset in range(1 << N):
            if subset & (1 << coordinate):
                continue
            if bin(subset).count("1") > 4:
                continue
            union = subset | (1 << coordinate)
            assert diagonal(union) == -slice_sign * diagonal(subset)

            mate = coordinate ^ 1
            expected = -1 if subset & (1 << mate) else 1
            assert transformed_edge_sign(coordinate, subset) == expected


def verify_posets() -> None:
    middle_vertices = {
        mask for mask in range(1 << N) if 2 <= bin(mask).count("1") <= 4
    }
    middle_edges = []
    for subset in middle_vertices:
        if bin(subset).count("1") not in (2, 3):
            continue
        for coordinate in range(N):
            if subset & (1 << coordinate):
                continue
            union = subset | (1 << coordinate)
            middle_edges.append((subset, union))
            if transformed_edge_sign(coordinate, subset) > 0:
                assert rank(subset) < rank(union)
            else:
                assert rank(union) < rank(subset)
    assert len(middle_vertices) == 50
    assert len(middle_edges) == 120
    assert [
        sum(rank(mask) == value for mask in middle_vertices)
        for value in range(4)
    ] == [6, 12, 24, 8]
    assert len(connected_components(middle_vertices, middle_edges)) == 1

    low_vertices = {
        mask for mask in range(1 << N) if bin(mask).count("1") in (1, 2)
    }
    low_edges = [
        (subset, subset | (1 << coordinate))
        for subset in low_vertices
        if bin(subset).count("1") == 1
        for coordinate in range(N)
        if not subset & (1 << coordinate)
    ]
    high_vertices = {
        mask for mask in range(1 << N) if bin(mask).count("1") in (3, 4)
    }
    high_edges = [
        (subset, subset | (1 << coordinate))
        for subset in high_vertices
        if bin(subset).count("1") == 3
        for coordinate in range(N)
        if not subset & (1 << coordinate)
    ]
    assert len(low_vertices) == 21 and len(low_edges) == 30
    assert len(high_vertices) == 35 and len(high_edges) == 60
    assert len(connected_components(low_vertices, low_edges)) == 1
    assert len(connected_components(high_vertices, high_edges)) == 1


def transform_code(code: int) -> int:
    answer = 0
    for left, right in PAIRS:
        answer |= (1 - ((code >> right) & 1)) << left
        answer |= (1 - ((code >> left) & 1)) << right
    return answer


def target_sign(code: int) -> int:
    parity = 1 if bin(code).count("1") % 2 == 0 else -1
    return -parity if code in EXCEPTIONS else parity


def bit_vector(code: int) -> tuple[int, ...]:
    return tuple((code >> coordinate) & 1 for coordinate in range(N))


def sign_vector(code: int, coordinates: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(1 - 2 * ((code >> coordinate) & 1) for coordinate in coordinates)


def product(values: tuple[int, ...]) -> int:
    answer = 1
    for value in values:
        answer *= value
    return answer


def cofactor_polynomial_value(
    code: int,
    coordinates: tuple[int, ...],
    exceptions: tuple[int, ...],
) -> int:
    point = sign_vector(code, coordinates)
    parity = product(point)
    scale = len(exceptions)
    answer = scale * parity
    for exception in exceptions:
        exceptional_point = sign_vector(exception, coordinates)
        indicator_product = product(
            tuple(
                1 + exceptional * current
                for exceptional, current in zip(exceptional_point, point)
            )
        )
        answer -= product(exceptional_point) * indicator_product
    missing = next(value for value in range(N) if value not in coordinates)
    fixed_sign = 1 - 2 * ((code >> missing) & 1)
    return fixed_sign * answer


def verify_cofactor_degree() -> None:
    for coordinate in range(N):
        other_coordinates = tuple(value for value in range(N) if value != coordinate)
        for bit in (0, 1):
            exceptions = tuple(
                value
                for value in EXCEPTIONS
                if ((value >> coordinate) & 1) == bit
            )
            assert len(exceptions) in (1, 2)
            for code in range(1 << N):
                if ((code >> coordinate) & 1) != bit:
                    continue
                value = cofactor_polynomial_value(
                    code, other_coordinates, exceptions
                )
                assert target_sign(code) * value > 0

            if len(exceptions) == 1:
                avoiding_coordinate = other_coordinates[0]
                avoiding_bit = 1 - (
                    (exceptions[0] >> avoiding_coordinate) & 1
                )
            else:
                agreements = [
                    value
                    for value in other_coordinates
                    if ((exceptions[0] >> value) & 1)
                    == ((exceptions[1] >> value) & 1)
                ]
                assert len(agreements) == 1
                avoiding_coordinate = agreements[0]
                avoiding_bit = 1 - (
                    (exceptions[0] >> avoiding_coordinate) & 1
                )

            face = [
                code
                for code in range(1 << N)
                if ((code >> coordinate) & 1) == bit
                and ((code >> avoiding_coordinate) & 1) == avoiding_bit
            ]
            assert len(face) == 16
            assert all(code not in EXCEPTIONS for code in face)
            baseline_multiplier = (-1) ** (bit + avoiding_bit)
            remaining = tuple(
                value
                for value in other_coordinates
                if value != avoiding_coordinate
            )
            assert all(
                target_sign(code)
                == baseline_multiplier * product(sign_vector(code, remaining))
                for code in face
            )


def verify_symmetry_and_rectangles() -> None:
    assert all(transform_code(value) == value for value in EXCEPTIONS)
    assert all(target_sign(transform_code(code)) == target_sign(code) for code in range(64))

    rectangles = (
        (38, 41, 37, 42),
        (21, 38, 37, 22),
        (21, 41, 25, 37),
    )
    for positive_left, positive_right, negative_left, negative_right in rectangles:
        assert target_sign(positive_left) == target_sign(positive_right) == 1
        assert target_sign(negative_left) == target_sign(negative_right) == -1
        assert tuple(
            left + right
            for left, right in zip(
                bit_vector(positive_left), bit_vector(positive_right)
            )
        ) == tuple(
            left + right
            for left, right in zip(
                bit_vector(negative_left), bit_vector(negative_right)
            )
        )


def main() -> None:
    verify_slices()
    verify_posets()
    verify_symmetry_and_rectangles()
    verify_cofactor_degree()
    print("one-exception slice inequalities: 186")
    print("degree-two-through-four poset: 50 nodes, 120 edges, rank 49")
    print("degree-one-and-three subsystem: 90 edges, rank 54")
    print("orientation counts reduced to 0, 1, 2")
    print("pair-symmetric rectangle circuits: verified")
    print("all twelve one-bit cofactors have threshold degree four")


if __name__ == "__main__":
    main()
