#!/usr/bin/env python3
"""Representation-complete degree-eight collision search over GF(3^6).

This reuses the exact odd-characteristic evaluator and two-plane GF3 bitset
elimination from the degree-seven search.  There are 21,135 invariant and
16,809 alternating S5 relative-orbit columns.  The extension-field sample
counts provide at least 17,280 exact scalar GF3 equations in either
character.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import search_n5_collision_degree7_relative_invariant as base
import search_n5_collision_degree7_gf3 as search


DEGREE = 8
SEED = 8_729
SAMPLES_BY_CHARACTER = {
    "invariant": 3_600,
    "alternating": 2_880,
}


def configure(character: str) -> None:
    base.DEGREE = DEGREE
    search.SAMPLES = SAMPLES_BY_CHARACTER[character]
    search.SEED = SEED


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", type=int)
    parser.add_argument("--blocks", type=int, default=4)
    parser.add_argument(
        "--character",
        choices=("invariant", "alternating"),
        default="invariant",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--combine", type=Path, nargs="+")
    arguments = parser.parse_args()

    configure(arguments.character)
    if arguments.combine is not None:
        search.combine(arguments.combine)
        return
    if arguments.block is None or arguments.output is None:
        raise ValueError("block mode requires --block and --output")
    search.evaluate_block(
        arguments.block,
        arguments.blocks,
        arguments.character,
        arguments.output,
    )


if __name__ == "__main__":
    main()
