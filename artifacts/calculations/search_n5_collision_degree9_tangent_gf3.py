#!/usr/bin/env python3
"""Degree-nine fixed-center relation search from exact tangent constraints.

At each smooth GF(3^6) image point, a vanishing polynomial has gradient in
the one-dimensional normal line.  The value and nineteen normal-line
constraints give twenty extension-field equations per sample.  This makes
the complete degree-nine S5 relative-invariant spaces tractable.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import search_n5_collision_degree8_tangent_gf3 as search


DEGREE = 9
SAMPLES_BY_CHARACTER = {
    "invariant": 540,
    "alternating": 460,
}
SEED = 9_729


def configure(character: str) -> None:
    search.DEGREE = DEGREE
    search.SAMPLES = SAMPLES_BY_CHARACTER[character]
    search.SEED = SEED


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", type=int)
    parser.add_argument("--blocks", type=int, default=6)
    parser.add_argument(
        "--character",
        choices=("invariant", "alternating"),
        default="alternating",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if arguments.block is None or arguments.output is None:
        raise ValueError("block mode requires --block and --output")
    configure(arguments.character)
    search.evaluate_block(
        arguments.block,
        arguments.blocks,
        arguments.character,
        arguments.output,
    )


if __name__ == "__main__":
    main()
