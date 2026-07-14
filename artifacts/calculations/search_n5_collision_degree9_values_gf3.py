#!/usr/bin/env python3
"""Fresh value constraints for the characteristic-three degree-nine kernel."""

from __future__ import annotations

import argparse
from pathlib import Path

import search_n5_collision_degree7_relative_invariant as base
import search_n5_collision_degree7_gf3 as search


DEGREE = 9
SAMPLES = 300
SEED = 90_729


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", type=int, required=True)
    parser.add_argument("--blocks", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    base.DEGREE = DEGREE
    search.SAMPLES = SAMPLES
    search.SEED = SEED
    search.evaluate_block(
        arguments.block,
        arguments.blocks,
        "alternating",
        arguments.output,
    )


if __name__ == "__main__":
    main()
