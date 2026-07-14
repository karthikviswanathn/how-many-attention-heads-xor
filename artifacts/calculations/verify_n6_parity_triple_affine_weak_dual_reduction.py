#!/usr/bin/env python3
"""Verify an affine weak-dual reduction for the S56 repair.

The nonnegative affine weight

    Q(z) = 2 + z5 - z4

vanishes at the two exceptional vertices retained by S56.  Against every
degree-at-most-four polynomial, its target-signed moment on S56 is therefore
exactly the negative parity moment on the eight omitted vertices.  Two of
those omitted weights vanish, leaving a six-point residual.
"""

from __future__ import annotations

import verify_n6_parity_triple_repaired_degree4_relations as repaired


N = 6
FULL = (1 << N) - 1
MASK = repaired.MASK
SUPPORT56 = repaired.SUPPORT56
OMITTED8 = tuple(sorted(set(range(1 << N)) - set(SUPPORT56)))
MONOMIALS4 = tuple(
    mask for mask in range(1 << N) if bin(mask).count("1") <= 4
)
SURVIVING_EXCEPTIONS = (38, 41)
EXPECTED_RESIDUAL_SUPPORT = (6, 9, 21, 27, 54, 57)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def parity(code: int) -> int:
    return character(FULL, code)


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def affine_weight(code: int) -> int:
    return 2 + character(1 << 5, code) - character(1 << 4, code)


def verify() -> tuple[tuple[int, ...], tuple[int, ...]]:
    assert OMITTED8 == (6, 9, 21, 27, 36, 42, 54, 57)
    assert min(affine_weight(code) for code in range(1 << N)) == 0
    assert max(affine_weight(code) for code in range(1 << N)) == 4
    assert all(affine_weight(code) == 0 for code in SURVIVING_EXCEPTIONS)

    residual_support = tuple(
        code for code in OMITTED8 if affine_weight(code) != 0
    )
    assert residual_support == EXPECTED_RESIDUAL_SUPPORT

    for mask in MONOMIALS4:
        full_parity_moment = sum(
            parity(code) * affine_weight(code) * character(mask, code)
            for code in range(1 << N)
        )
        assert full_parity_moment == 0

        support_moment = sum(
            target_sign(code)
            * affine_weight(code)
            * character(mask, code)
            for code in SUPPORT56
        )
        omitted_moment = sum(
            parity(code) * affine_weight(code) * character(mask, code)
            for code in OMITTED8
        )
        assert support_moment == -omitted_moment

    for normal in (repaired.M1, repaired.M2):
        assert sum(
            repaired.relation(normal, (code,))[0] * affine_weight(code)
            for code in SUPPORT56
        ) == 0
    return OMITTED8, residual_support


def main() -> None:
    omitted, residual = verify()
    print(f"S56 omitted vertices: {omitted}")
    print(f"nonzero omitted residual support: {residual}")
    print("verified affine weak-dual reduction on all quartic monomials")


if __name__ == "__main__":
    main()
