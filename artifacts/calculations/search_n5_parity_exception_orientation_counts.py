#!/usr/bin/env python3
"""Search exact H4 certificates by orientation count for two five-bit cofactors.

The six-bit parity-triple candidate has two cofactor types: five-bit parity
with one flipped vertex, and five-bit parity with two weight-two vertices at
distance four flipped.  Restriction preserves the orientation of every
nonconstant denominator.  This diagnostic samples denominator tuples for
each of the five orientation counts and exactifies every success.  A miss is
only search evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import search_gated_single_flip as exact
import search_n6_h4_inner_lp as inner


N = 5
HEADS = 4
VERTICES = 1 << N
TARGETS = {
    "one_flip": (3,),
    "two_flips": (3, 12),
}


def parity_sign(code: int) -> int:
    return 1 if bin(code).count("1") % 2 == 0 else -1


def target_signs(exceptions: tuple[int, ...]) -> np.ndarray:
    return np.array(
        [
            -parity_sign(code) if code in exceptions else parity_sign(code)
            for code in range(VERTICES)
        ],
        dtype=np.int64,
    )


def truth_mask(signs: np.ndarray) -> int:
    return sum(
        (1 << code) for code, value in enumerate(signs) if int(value) > 0
    )


def random_denominators(
    rng: np.random.Generator, positive_heads: int
) -> np.ndarray:
    orientations = tuple(
        [-1] * (HEADS - positive_heads) + [1] * positive_heads
    )
    weights = np.maximum(
        1,
        np.rint(np.exp(rng.uniform(0.0, 9.0, size=(HEADS, N + 1)))),
    )
    return np.vstack(
        [
            exact.oriented_integer_denominator(weights[head], orientation)
            for head, orientation in enumerate(orientations)
        ]
    )


def orientation_count(denominators: np.ndarray) -> int:
    counts = []
    affine = exact.affine_matrix(N, object)
    assert np.all(affine @ denominators.astype(object).T > 0)
    for row in denominators:
        if np.all(row[1:] > 0):
            counts.append(1)
        elif np.all(row[1:] < 0):
            counts.append(0)
        else:
            raise AssertionError("denominator has mixed orientation")
    return sum(counts)


def search(
    signs: np.ndarray,
    positive_heads: int,
    rng: np.random.Generator,
    trials: int,
) -> tuple[dict[str, object] | None, int]:
    for trial in range(1, trials + 1):
        denominators = random_denominators(rng, positive_heads)
        assert orientation_count(denominators) == positive_heads
        certificate = exact.exact_fixed_certificate(signs, N, denominators)
        if certificate is not None:
            certificate["trial"] = trial
            certificate["positive_heads"] = positive_heads
            return certificate, trial
    return None, trials


def configure_inner_search() -> None:
    inner.N = N
    inner.HEADS = HEADS
    inner.WIDTH = N + 1
    inner.VERTICES = VERTICES
    inner.AFFINE = np.column_stack(
        [np.ones(VERTICES), inner.cube()]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--restarts", type=int, default=42)
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    configure_inner_search()
    rng = np.random.default_rng(args.seed)
    payload: dict[str, object] = {
        "status": "Every success is exact. A miss is only search evidence.",
        "dimension": N,
        "heads": HEADS,
        "targets": {},
    }
    for name, exceptions in TARGETS.items():
        signs = target_signs(exceptions)
        mask = truth_mask(signs)
        attempts = []
        print(
            f"target={name} exceptions={exceptions} mask=0x{mask:08x}",
            flush=True,
        )
        for positive_heads in range(HEADS + 1):
            certificate, attempted = search(
                signs, positive_heads, rng, args.trials
            )
            method = "random_fixed_denominators"
            best = None
            if certificate is None and args.restarts > 0:
                certificate, best = inner.search_orientation(
                    signs.astype(float),
                    positive_heads,
                    args.seed + 1009 * positive_heads,
                    args.restarts,
                    args.max_iterations,
                    (30, 100, 300, 1000, 3000, 10000, 30000),
                )
                method = "continuous_inner_lp"
            attempts.append(
                {
                    "positive_heads": positive_heads,
                    "trials": attempted,
                    "method": method,
                    "continuous_best": best,
                    "certificate": certificate,
                }
            )
            print(
                f"  positive_heads={positive_heads} "
                f"exact_hit={certificate is not None} trials={attempted} "
                f"method={method}",
                flush=True,
            )
        payload["targets"][name] = {
            "exceptions": list(exceptions),
            "truth_mask_hex": f"0x{mask:08x}",
            "attempts": attempts,
        }

    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
        print(f"wrote {args.output}", flush=True)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
