#!/usr/bin/env python3
"""Search stronger two-affine-factor relaxations of two-head sign scores."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import search_adversarial_low_dimension as core


def random_positive_affine(
    n: int, rng: np.random.Generator, maximum: int
) -> np.ndarray:
    weights = rng.integers(1, maximum + 1, size=n, dtype=np.int64)
    signs = rng.choice(np.array([-1, 1], dtype=np.int64), size=n)
    slopes = signs * weights
    constant = int(rng.integers(1, maximum + 1)) + int(
        np.sum(weights[signs < 0])
    )
    return np.concatenate([[constant], slopes]).astype(np.int64)


def random_unrestricted_affine(
    n: int, rng: np.random.Generator, maximum: int
) -> np.ndarray:
    denominator = rng.integers(
        -maximum, maximum + 1, size=n + 1, dtype=np.int64
    )
    while not np.any(denominator):
        denominator = rng.integers(
            -maximum, maximum + 1, size=n + 1, dtype=np.int64
        )
    return denominator


def search(
    n: int,
    mask: int,
    relaxation: str,
    trials: int,
    maximum: int,
    seed: int,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    signs = core.signs_from_mask(mask, n)
    affine = core.affine_matrix(n)
    for trial in range(trials):
        if relaxation == "arbitrary-positive":
            denominators = np.array(
                [
                    random_positive_affine(n, rng, maximum),
                    random_positive_affine(n, rng, maximum),
                ]
            )
        elif relaxation == "one-positive-factor":
            denominators = np.array(
                [
                    random_positive_affine(n, rng, maximum),
                    random_unrestricted_affine(n, rng, maximum),
                ]
            )
        else:
            denominators = np.array(
                [
                    random_unrestricted_affine(n, rng, maximum),
                    random_unrestricted_affine(n, rng, maximum),
                ]
            )
        matrix = core.cleared_two_head_matrix(n, denominators)
        result = core.exact_integer_separator(signs, matrix)
        if result is None:
            continue
        coefficients, margin = result
        signed_scores = signs.astype(object) * (
            matrix.astype(object) @ coefficients.astype(object)
        )
        denominator_values = affine @ denominators.T
        return {
            "found": True,
            "dimension": n,
            "truth_mask_hex": hex(mask),
            "relaxation": relaxation,
            "trial": trial,
            "denominators": denominators.tolist(),
            "denominator_value_ranges": [
                [int(np.min(denominator_values[:, head])),
                 int(np.max(denominator_values[:, head]))]
                for head in range(2)
            ],
            "cleared_score_coefficients": [int(value) for value in coefficients],
            "minimum_signed_cleared_score": min(map(int, signed_scores)),
            "floating_margin": margin,
        }
    return {
        "found": False,
        "dimension": n,
        "truth_mask_hex": hex(mask),
        "relaxation": relaxation,
        "trials": trials,
        "warning": "A random search failure is not an impossibility certificate.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, required=True)
    parser.add_argument("--mask", type=lambda value: int(value, 0), required=True)
    parser.add_argument(
        "--relaxation",
        choices=("arbitrary-positive", "one-positive-factor", "unrestricted"),
        required=True,
    )
    parser.add_argument("--trials", type=int, default=100000)
    parser.add_argument("--maximum", type=int, default=32)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = search(
        arguments.dimension,
        arguments.mask,
        arguments.relaxation,
        arguments.trials,
        arguments.maximum,
        arguments.seed,
    )
    rendered = json.dumps(result, indent=2) + "\n"
    if arguments.output is not None:
        arguments.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
