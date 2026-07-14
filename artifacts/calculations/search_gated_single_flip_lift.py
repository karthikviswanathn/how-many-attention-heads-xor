#!/usr/bin/env python3
"""Lift a known five-bit four-head certificate through a fresh AND bit.

The five-bit parity function with one weight-two vertex flipped has a known
exact four-head representation.  This diagnostic fixes its four denominator
directions on the active slice, varies only their fresh-bit slopes, and solves
the numerator problem globally by linear programming.  Every reported
success is rounded and checked by exact integer arithmetic.  Exhausting the
finite grid is not a lower-bound certificate.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np

from search_gated_single_flip import exact_fixed_certificate, target_signs
from verify_n5_high_degree_candidate_refutations import CERTIFICATES


BASE = next(
    certificate
    for certificate in CERTIFICATES
    if certificate["name"] == "parity with one weight-two vertex flipped"
)


def lifted_denominator(
    base: tuple[int, ...], scale: int, fresh_magnitude: int
) -> tuple[int, ...]:
    """Return a six-variable denominator agreeing with scale * base at y=1."""
    slopes = tuple(scale * value for value in base[1:])
    if all(value < 0 for value in base[1:]):
        return (
            scale * base[0] + fresh_magnitude,
            *slopes,
            -fresh_magnitude,
        )
    if all(value > 0 for value in base[1:]):
        assert fresh_magnitude < scale * base[0]
        return (
            scale * base[0] - fresh_magnitude,
            *slopes,
            fresh_magnitude,
        )
    raise ValueError("base denominator is not admissibly oriented")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=100)
    parser.add_argument(
        "--negative-ratios",
        type=float,
        nargs="+",
        default=(0.01, 0.05, 0.2, 1.0, 5.0, 20.0),
    )
    parser.add_argument(
        "--positive-fractions",
        type=float,
        nargs="+",
        default=(0.02, 0.1, 0.3, 0.6, 0.9),
    )
    arguments = parser.parse_args()
    if arguments.scale <= 0:
        raise ValueError("scale must be positive")

    signs = target_signs(5, 3, "and")
    bases = tuple(BASE["denominators"])
    choices = []
    for base in bases:
        if all(value < 0 for value in base[1:]):
            magnitudes = tuple(
                max(1, int(round(arguments.scale * ratio)))
                for ratio in arguments.negative_ratios
            )
        else:
            ceiling = arguments.scale * base[0]
            magnitudes = tuple(
                min(
                    ceiling - 1,
                    max(1, int(round(ceiling * fraction))),
                )
                for fraction in arguments.positive_fractions
            )
        choices.append(tuple(dict.fromkeys(magnitudes)))

    attempted = 0
    for magnitudes in itertools.product(*choices):
        attempted += 1
        denominators = np.array(
            [
                lifted_denominator(base, arguments.scale, magnitude)
                for base, magnitude in zip(bases, magnitudes)
            ],
            dtype=np.int64,
        )
        certificate = exact_fixed_certificate(signs, 6, denominators)
        if certificate is not None:
            print(f"grid points attempted: {attempted}")
            print(f"fresh magnitudes: {magnitudes}")
            print(certificate)
            print("certificate: exact four-head lift found")
            return

    print(f"grid points attempted: {attempted}")
    print("certificate: none on this finite lift grid")


if __name__ == "__main__":
    main()
