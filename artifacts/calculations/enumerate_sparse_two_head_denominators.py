#!/usr/bin/env python3
"""Enumerate sparse oriented denominator pairs for a fixed truth table.

Each positive oriented affine denominator is normalized to have minimum cube
value one.  Its seven slope magnitudes therefore form a positive weight
vector.  A support-k grid point has exactly k weights chosen from the supplied
grid and all remaining weights equal to one.  Every resulting fixed pair is
tested by linear programming.  A reported success is converted to an integer
separator and checked with exact integer arithmetic.

A search failure is finite-grid evidence only, not an H2 lower bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import numpy as np

from search_adversarial_low_dimension import (
    cleared_two_head_matrix,
    exact_integer_separator,
    floating_separable,
    oriented_denominator,
    signs_from_mask,
)


def denominator_class(
    dimension: int, support: int, grid: tuple[int, ...]
) -> list[tuple[int, tuple[int, ...], np.ndarray]]:
    if support < 0 or support > dimension:
        raise ValueError("support must lie between zero and the dimension")
    if any(weight <= 1 for weight in grid):
        raise ValueError("all nonbaseline grid weights must exceed one")

    answer = []
    for orientation in (-1, 1):
        for coordinates in itertools.combinations(range(dimension), support):
            for active_weights in itertools.product(grid, repeat=support):
                weights = [1] * dimension
                for coordinate, weight in zip(coordinates, active_weights):
                    weights[coordinate] = weight
                answer.append(
                    (
                        orientation,
                        tuple(weights),
                        np.array(
                            oriented_denominator(weights, orientation),
                            dtype=np.int64,
                        ),
                    )
                )
    return answer


def exact_minimum(
    signs: np.ndarray, matrix: np.ndarray, coefficients: np.ndarray
) -> int:
    signed = signs.astype(object) * (
        matrix.astype(object) @ coefficients.astype(object)
    )
    return int(min(signed))


def search(arguments: argparse.Namespace) -> dict[str, object]:
    signs = signs_from_mask(arguments.mask, arguments.dimension)
    grid = tuple(sorted(set(arguments.weights)))
    left = denominator_class(arguments.dimension, arguments.left_support, grid)
    right = denominator_class(arguments.dimension, arguments.right_support, grid)
    same_class = arguments.left_support == arguments.right_support

    if same_class:
        pairs = itertools.combinations_with_replacement(range(len(left)), 2)
        total = len(left) * (len(left) + 1) // 2
    else:
        pairs = itertools.product(range(len(left)), range(len(right)))
        total = len(left) * len(right)

    started = time.time()
    orientation_counts: Counter[tuple[int, int]] = Counter()
    for tested, (left_index, right_index) in enumerate(pairs, 1):
        first = left[left_index]
        second = right[right_index]
        orientation_counts[tuple(sorted((first[0], second[0])))] += 1
        denominators = np.vstack([first[2], second[2]])
        matrix = cleared_two_head_matrix(arguments.dimension, denominators)
        if floating_separable(signs, matrix):
            exact = exact_integer_separator(signs, matrix)
            if exact is None:
                raise RuntimeError(
                    "floating LP found a fit that integer verification could not certify"
                )
            coefficients, normalized_margin = exact
            width = arguments.dimension + 1
            constant = int(coefficients[0])
            numerator_1 = [int(value) for value in coefficients[1 : 1 + width]]
            numerator_2 = [int(value) for value in coefficients[1 + width :]]
            absorbed_numerator_1 = [
                numerator_1[index]
                + constant * int(denominators[0, index])
                for index in range(width)
            ]
            return {
                "found": True,
                "dimension": arguments.dimension,
                "truth_mask_hex": hex(arguments.mask),
                "support_pair": [arguments.left_support, arguments.right_support],
                "weight_grid": list(grid),
                "tested_pairs": tested,
                "total_pairs": total,
                "elapsed_seconds": time.time() - started,
                "orientations": [first[0], second[0]],
                "literal_weights": [list(first[1]), list(second[1])],
                "denominators": denominators.tolist(),
                "absorbed_numerators": [absorbed_numerator_1, numerator_2],
                "minimum_signed_cleared_score": exact_minimum(
                    signs, matrix, coefficients
                ),
                "fixed_denominator_normalized_margin": normalized_margin,
            }
        if arguments.progress_every and tested % arguments.progress_every == 0:
            print(
                f"tested {tested}/{total} pairs in {time.time() - started:.1f}s",
                flush=True,
            )

    return {
        "found": False,
        "dimension": arguments.dimension,
        "truth_mask_hex": hex(arguments.mask),
        "support_pair": [arguments.left_support, arguments.right_support],
        "weight_grid": list(grid),
        "denominators_per_class": [len(left), len(right)],
        "tested_pairs": total,
        "orientation_pair_counts": {
            f"{first},{second}": count
            for (first, second), count in sorted(orientation_counts.items())
        },
        "elapsed_seconds": time.time() - started,
        "warning": "A finite-grid search failure is not an H2 lower bound.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--mask", type=lambda value: int(value, 0), required=True)
    parser.add_argument("--left-support", type=int, required=True)
    parser.add_argument("--right-support", type=int, required=True)
    parser.add_argument(
        "--weights",
        type=int,
        nargs="+",
        default=(2, 3, 5, 10, 30, 100, 300, 1000, 10000),
    )
    parser.add_argument("--progress-every", type=int, default=100000)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = search(arguments)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if arguments.output is not None:
        arguments.output.write_text(rendered + "\n")


if __name__ == "__main__":
    main()
