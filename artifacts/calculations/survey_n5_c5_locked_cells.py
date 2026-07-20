#!/usr/bin/env python3
"""Survey fully locked complementary-C5 quadratic sign cells on five bits.

This is a diagnostic sampler, not an exhaustive classification.  For each
sampled C5-orthant quadratic threshold, it checks the ten cone memberships
that characterize sign-cell locking, reduces locked masks by the full
order-40 symmetry group of the fixed C5 coefficient orthant, and tests the
cycle-adapted two-scale sufficient criterion.
"""

from __future__ import annotations

import argparse
from collections import deque
from functools import lru_cache

import numpy as np
from scipy.optimize import linprog

import screen_n5_c5_two_scale as c5


FULL_MASK = (1 << (1 << c5.INPUT_BITS)) - 1


def mask_from_signs(signs: np.ndarray) -> int:
    return sum(
        (int(value) > 0) << vertex
        for vertex, value in enumerate(signs)
    )


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for vertex in range(1 << c5.INPUT_BITS):
        image = 0
        for source, target in enumerate(permutation):
            image |= ((vertex >> source) & 1) << target
        if (mask >> vertex) & 1:
            answer |= 1 << image
    return answer


def fixed_orthant_symmetries() -> tuple[tuple[tuple[int, ...], bool], ...]:
    """Return coordinate maps and whether they exchange cycle and chord colors."""
    answer = []
    for multiplier in (1, 4, 2, 3):
        exchanges_colors = multiplier in (2, 3)
        for shift in range(5):
            permutation = tuple(
                (multiplier * index + shift) % 5 for index in range(5)
            )
            answer.append((permutation, exchanges_colors))
    return tuple(answer)


def global_input_complement(mask: int) -> int:
    answer = 0
    complement_vertex = (1 << c5.INPUT_BITS) - 1
    for vertex in range(1 << c5.INPUT_BITS):
        if (mask >> (vertex ^ complement_vertex)) & 1:
            answer |= 1 << vertex
    return answer


@lru_cache(maxsize=None)
def canonical_mask(mask: int) -> int:
    images = []
    for permutation, exchanges_colors in fixed_orthant_symmetries():
        image = permute_mask(mask, permutation)
        if exchanges_colors:
            image = FULL_MASK ^ image
        images.append(image)
        flipped = global_input_complement(image)
        images.append(flipped)
    return min(images)


def fully_locked(signs: np.ndarray) -> bool:
    signed_features = signs[:, None] * c5.FOURIER
    equality = signed_features.T
    for edge_index, edge_sign in enumerate(c5.EDGE_SIGNS):
        target = np.zeros(len(c5.FOURIER_SUBSETS))
        target[6 + edge_index] = edge_sign
        result = linprog(
            np.zeros(1 << c5.INPUT_BITS),
            A_eq=equality,
            b_eq=target,
            bounds=[(0.0, None)] * (1 << c5.INPUT_BITS),
            method="highs",
        )
        if not result.success or np.max(
            np.abs(equality @ result.x - target)
        ) > 1e-7:
            return False
    return True


def ell_bounded(signs: np.ndarray) -> bool:
    """Return whether the signed edge sum is positive on every closed-cell ray."""
    signed_features = signs[:, None] * c5.FOURIER
    normalizer = np.sum(signed_features, axis=0, keepdims=True)
    edge_sum = np.zeros(len(c5.FOURIER_SUBSETS))
    edge_sum[6:] = c5.EDGE_SIGNS
    result = linprog(
        edge_sum,
        A_ub=-signed_features,
        b_ub=np.zeros(1 << c5.INPUT_BITS),
        A_eq=normalizer,
        b_eq=np.ones(1),
        bounds=[(None, None)] * len(c5.FOURIER_SUBSETS),
        method="highs",
    )
    return bool(result.success and result.fun > 1e-9)


def cell_representative(signs: np.ndarray) -> np.ndarray | None:
    constraints = np.vstack(
        [-(signs[:, None] * c5.FOURIER), -c5.EDGE_SELECTOR]
    )
    bounds = -np.ones((1 << c5.INPUT_BITS) + len(c5.EDGES))
    result = linprog(
        np.zeros(len(c5.FOURIER_SUBSETS)),
        A_ub=constraints,
        b_ub=bounds,
        bounds=[(None, None)] * len(c5.FOURIER_SUBSETS),
        method="highs",
    )
    if not result.success:
        return None
    return result.x


def locked_neighbor_walk(limit: int) -> dict[int, np.ndarray]:
    start_coefficients = c5.locked_cell_coefficients()
    start_signs = np.sign(c5.FOURIER @ start_coefficients)
    start_mask = mask_from_signs(start_signs)
    queue = deque([start_mask])
    representatives = {start_mask: start_coefficients}
    rejected = set()
    while queue and len(representatives) < limit:
        mask = queue.popleft()
        for vertex in range(1 << c5.INPUT_BITS):
            neighbor = mask ^ (1 << vertex)
            if neighbor in representatives or neighbor in rejected:
                continue
            signs = np.array(
                [1 if (neighbor >> code) & 1 else -1 for code in range(32)],
                dtype=float,
            )
            coefficients = cell_representative(signs)
            if coefficients is None or not fully_locked(signs):
                rejected.add(neighbor)
                continue
            representatives[neighbor] = coefficients
            queue.append(neighbor)
            if len(representatives) >= limit:
                break
    return representatives


def locked_class_walk_from_mask(
    seed_mask: int, limit: int
) -> tuple[dict[int, np.ndarray], bool]:
    """Walk one fully locked component in the order-40 symmetry quotient."""
    start_mask = canonical_mask(seed_mask)
    canonical_signs = np.array(
        [1 if (start_mask >> code) & 1 else -1 for code in range(32)],
        dtype=float,
    )
    start_coefficients = cell_representative(canonical_signs)
    assert start_coefficients is not None and fully_locked(canonical_signs)

    queue = deque([start_mask])
    representatives = {start_mask: start_coefficients}
    rejected = set()
    while queue and len(representatives) < limit:
        mask = queue.popleft()
        for vertex in range(1 << c5.INPUT_BITS):
            neighbor = canonical_mask(mask ^ (1 << vertex))
            if neighbor in representatives or neighbor in rejected:
                continue
            signs = np.array(
                [1 if (neighbor >> code) & 1 else -1 for code in range(32)],
                dtype=float,
            )
            coefficients = cell_representative(signs)
            if coefficients is None or not fully_locked(signs):
                rejected.add(neighbor)
                continue
            representatives[neighbor] = coefficients
            queue.append(neighbor)
            if len(representatives) >= limit:
                break
    return representatives, not queue


def locked_class_walk(limit: int) -> tuple[dict[int, np.ndarray], bool]:
    """Walk the component containing the explicit rigid locked cell."""
    start_signs = np.sign(c5.FOURIER @ c5.locked_cell_coefficients())
    start_mask = mask_from_signs(start_signs)
    return locked_class_walk_from_mask(start_mask, limit)


def c5_class_walk(limit: int) -> tuple[dict[int, np.ndarray], bool]:
    """Walk every sign cell meeting the fixed complementary-C5 orthant."""
    start_signs = np.sign(c5.FOURIER @ c5.locked_cell_coefficients())
    start_mask = canonical_mask(mask_from_signs(start_signs))
    canonical_signs = np.array(
        [1 if (start_mask >> code) & 1 else -1 for code in range(32)],
        dtype=float,
    )
    start_coefficients = cell_representative(canonical_signs)
    assert start_coefficients is not None

    queue = deque([start_mask])
    representatives = {start_mask: start_coefficients}
    rejected = set()
    while queue and len(representatives) < limit:
        mask = queue.popleft()
        for vertex in range(1 << c5.INPUT_BITS):
            neighbor = canonical_mask(mask ^ (1 << vertex))
            if neighbor in representatives or neighbor in rejected:
                continue
            signs = np.array(
                [1 if (neighbor >> code) & 1 else -1 for code in range(32)],
                dtype=float,
            )
            coefficients = cell_representative(signs)
            if coefficients is None:
                rejected.add(neighbor)
                continue
            representatives[neighbor] = coefficients
            queue.append(neighbor)
            if len(representatives) >= limit:
                break
    return representatives, not queue


def bounded_c5_class_walk(limit: int) -> tuple[dict[int, np.ndarray], bool]:
    """Walk the ell-bounded part of the fixed complementary-C5 chamber graph."""
    start_signs = np.sign(c5.FOURIER @ c5.locked_cell_coefficients())
    start_mask = canonical_mask(mask_from_signs(start_signs))
    canonical_signs = np.array(
        [1 if (start_mask >> code) & 1 else -1 for code in range(32)],
        dtype=float,
    )
    start_coefficients = cell_representative(canonical_signs)
    assert start_coefficients is not None and ell_bounded(canonical_signs)

    queue = deque([start_mask])
    representatives = {start_mask: start_coefficients}
    rejected = set()
    while queue and len(representatives) < limit:
        mask = queue.popleft()
        for vertex in range(1 << c5.INPUT_BITS):
            neighbor = canonical_mask(mask ^ (1 << vertex))
            if neighbor in representatives or neighbor in rejected:
                continue
            signs = np.array(
                [1 if (neighbor >> code) & 1 else -1 for code in range(32)],
                dtype=float,
            )
            coefficients = cell_representative(signs)
            if coefficients is None or not ell_bounded(signs):
                rejected.add(neighbor)
                continue
            representatives[neighbor] = coefficients
            queue.append(neighbor)
            if len(representatives) >= limit:
                break
    return representatives, not queue


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--locked-walk", type=int, default=0)
    parser.add_argument("--locked-class-walk", type=int, default=0)
    parser.add_argument("--c5-class-walk", type=int, default=0)
    parser.add_argument("--bounded-c5-class-walk", type=int, default=0)
    parser.add_argument("--representatives", type=int, default=64)
    arguments = parser.parse_args()
    rng = np.random.default_rng(arguments.seed)

    unique_masks: dict[int, np.ndarray] = {}
    for _ in range(arguments.samples):
        coefficients = rng.normal(scale=8.0, size=len(c5.FOURIER_SUBSETS))
        coefficients[6:] = c5.EDGE_SIGNS * np.exp(
            rng.uniform(-6.0, 6.0, len(c5.EDGES))
        )
        values = c5.FOURIER @ coefficients
        if np.min(np.abs(values)) < 1e-9:
            continue
        signs = np.sign(values)
        unique_masks.setdefault(mask_from_signs(signs), coefficients)

    locked: dict[int, tuple[int, np.ndarray]] = {}
    for mask, coefficients in unique_masks.items():
        signs = np.sign(c5.FOURIER @ coefficients)
        if not fully_locked(signs):
            continue
        canonical = canonical_mask(mask)
        locked.setdefault(canonical, (mask, coefficients))

    direct = 0
    unresolved = []
    for canonical, (mask, coefficients) in sorted(locked.items()):
        witness = c5.criterion_witness(coefficients)
        if witness is not None:
            direct += 1
        else:
            unresolved.append((canonical, mask))

    print(f"samples: {arguments.samples}")
    print(f"unique sampled masks: {len(unique_masks)}")
    print(f"fully locked symmetry classes: {len(locked)}")
    print(f"direct two-scale successes: {direct}")
    print(f"direct unresolved classes: {len(unresolved)}")
    for canonical, representative in unresolved[:64]:
        print(
            f"unresolved canonical=0x{canonical:08x} "
            f"sample=0x{representative:08x}"
        )
    known = c5.locked_cell_coefficients()
    known_signs = np.sign(c5.FOURIER @ known)
    print(f"known locked cell check: {fully_locked(known_signs)}")
    if arguments.locked_walk:
        walked = locked_neighbor_walk(arguments.locked_walk)
        walked_classes = {
            canonical_mask(mask) for mask in walked
        }
        direct_masks = []
        direct_failures = []
        for mask, coefficients in sorted(walked.items()):
            if c5.criterion_witness(coefficients) is not None:
                direct_masks.append(mask)
            else:
                direct_failures.append(mask)

        rescue_rng = np.random.default_rng(arguments.seed + 1)
        rescued_masks = []
        rescue_failures = []
        for mask in direct_failures:
            signs = np.array(
                [1 if (mask >> code) & 1 else -1 for code in range(32)],
                dtype=float,
            )
            alternative = c5.alternative_representative(
                signs,
                rescue_rng,
                arguments.representatives,
            )
            if alternative is None:
                rescue_failures.append(mask)
            else:
                rescued_masks.append(mask)

        print(f"locked neighbor-walk cells: {len(walked)}")
        print(f"locked neighbor-walk symmetry classes: {len(walked_classes)}")
        print(f"locked neighbor-walk direct successes: {len(direct_masks)}")
        print(
            "locked neighbor-walk alternative-representative successes: "
            f"{len(rescued_masks)}"
        )
        print(
            "locked neighbor-walk unresolved after representative search: "
            f"{len(rescue_failures)}"
        )
        for mask in rescue_failures[:64]:
            print(
                "walk unresolved "
                f"canonical=0x{canonical_mask(mask):08x} "
                f"sample=0x{mask:08x}"
            )
    if arguments.locked_class_walk:
        walked_classes, exhausted = locked_class_walk(arguments.locked_class_walk)
        print(f"locked quotient-walk classes: {len(walked_classes)}")
        print(f"locked quotient-walk component exhausted: {exhausted}")
    if arguments.c5_class_walk:
        walked_classes, exhausted = c5_class_walk(arguments.c5_class_walk)
        locked_count = 0
        for mask in walked_classes:
            signs = np.array(
                [1 if (mask >> code) & 1 else -1 for code in range(32)],
                dtype=float,
            )
            locked_count += int(fully_locked(signs))
        print(f"C5 quotient-walk classes: {len(walked_classes)}")
        print(f"C5 quotient-walk exhausted: {exhausted}")
        print(f"fully locked classes in C5 walk: {locked_count}")
    if arguments.bounded_c5_class_walk:
        walked_classes, exhausted = bounded_c5_class_walk(
            arguments.bounded_c5_class_walk
        )
        locked_count = 0
        for mask in walked_classes:
            signs = np.array(
                [1 if (mask >> code) & 1 else -1 for code in range(32)],
                dtype=float,
            )
            locked_count += int(fully_locked(signs))
        print(f"bounded C5 quotient-walk classes: {len(walked_classes)}")
        print(f"bounded C5 quotient-walk exhausted: {exhausted}")
        print(f"fully locked classes in bounded C5 walk: {locked_count}")
    print("warning: this survey is not exhaustive")


if __name__ == "__main__":
    main()
