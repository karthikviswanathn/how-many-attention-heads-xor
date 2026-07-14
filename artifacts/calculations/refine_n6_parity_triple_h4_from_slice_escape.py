#!/usr/bin/env python3
"""Refine H4 search from a tuple escaping the 90-row slice subsystem.

The starting denominators satisfy all admissibility inequalities and admit a
tangent numerator satisfying the slice Fourier levels one and three.  They do
not escape the stronger level-two-and-three subsystem.  This script uses the
exact inner-numerator LP and searches every coefficient normalization branch
near that tuple.  Any success is rounded and verified over the integers.  A
failure is only search evidence.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import minimize

import search_gated_single_flip as exact
import search_n6_h4_inner_lp as inner


SIGN_DENOMINATORS = np.array(
    [
        [
            22.78718002238036,
            -3.5139954010967656,
            -0.17302043130558298,
            -6.8734336559397216,
            -4.804875962403327,
            -0.15223001879580095,
            -0.3045946795811433,
        ],
        [
            14.964422775120239,
            -3.7443885925961613,
            -0.15918249946508356,
            -3.8576427496965024,
            -6.193683788655042,
            -0.2655119379011769,
            -0.5657062309699218,
        ],
        [
            7.593582793761379,
            -5.061680841369399,
            -0.4461672942946222,
            -0.4256010148579883,
            -0.15331588103525748,
            -0.1404819878992763,
            -1.1661402356555535,
        ],
        [
            18.31194600992425,
            -0.2549659944451859,
            -2.4713286198852162,
            -4.275837325748056,
            -3.272575385255975,
            -6.131780710063287,
            -0.8718417476609722,
        ],
    ],
    dtype=float,
)


def literal_weights() -> np.ndarray:
    slopes = -SIGN_DENOMINATORS[:, 1:]
    slack = SIGN_DENOMINATORS[:, 0] - np.sum(slopes, axis=1)
    assert np.all(slopes > 0.0)
    assert np.all(slack > 0.0)
    weights = np.column_stack([slack, 2.0 * slopes])
    return weights / np.sum(weights, axis=1, keepdims=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jitters", type=int, default=4)
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--seed", type=int, default=20260714)
    args = parser.parse_args()

    signs = inner.signs_from_mask(0x96696BD669B69669)
    orientations = (1, 1, 1, 1)
    rng = np.random.default_rng(args.seed)
    start = np.log(literal_weights())
    best_margin = float("-inf")
    best_record = None
    attempt = 0

    for anchor_index in range(1 + inner.HEADS * inner.N):
        for anchor_value in (-1, 1):
            for jitter in range(args.jitters):
                attempt += 1
                initial = start + rng.normal(
                    scale=0.05 * jitter, size=start.shape
                )

                def objective(current: np.ndarray) -> tuple[float, np.ndarray]:
                    value, gradient, _ = inner.inner_lp(
                        current,
                        signs,
                        orientations,
                        0.0,
                        anchor_index,
                        anchor_value,
                    )
                    return value, gradient

                result = minimize(
                    objective,
                    initial.ravel(),
                    jac=True,
                    method="L-BFGS-B",
                    bounds=[(-20.0, 20.0)] * (inner.HEADS * inner.WIDTH),
                    options={
                        "maxiter": args.iterations,
                        "maxfun": 8 * args.iterations,
                        "ftol": 1e-14,
                        "gtol": 1e-9,
                        "maxls": 40,
                    },
                )
                _, _, diagnostics = inner.inner_lp(
                    result.x,
                    signs,
                    orientations,
                    0.0,
                    anchor_index,
                    anchor_value,
                )
                margin = float(diagnostics["margin"])
                theta = np.array(diagnostics["theta"], dtype=float)
                if margin > best_margin:
                    best_margin = margin
                    best_record = (
                        anchor_index,
                        anchor_value,
                        jitter,
                        theta.copy(),
                    )
                    print(
                        f"attempt={attempt} anchor={anchor_index}:"
                        f"{anchor_value} jitter={jitter} margin={margin}",
                        flush=True,
                    )

                for scale in (
                    100,
                    300,
                    1000,
                    3000,
                    10000,
                    30000,
                    100000,
                    300000,
                    1000000,
                ):
                    denominators = np.vstack(
                        [
                            exact.oriented_integer_denominator(
                                np.maximum(
                                    1, np.rint(scale * theta[head])
                                ),
                                1,
                            )
                            for head in range(inner.HEADS)
                        ]
                    )
                    certificate = exact.exact_fixed_certificate(
                        signs.astype(np.int64), inner.N, denominators
                    )
                    if certificate is not None:
                        print(
                            {
                                "anchor_index": anchor_index,
                                "anchor_value": anchor_value,
                                "jitter": jitter,
                                "rounding_scale": scale,
                                "continuous_margin": margin,
                                "certificate": certificate,
                            },
                            flush=True,
                        )
                        return

    print(f"best_margin={best_margin}")
    if best_record is not None:
        print(
            {
                "anchor_index": best_record[0],
                "anchor_value": best_record[1],
                "jitter": best_record[2],
                "literal_weights": best_record[3].tolist(),
            }
        )
    print("No exact H4 certificate found. This is only search evidence.")


if __name__ == "__main__":
    main()
