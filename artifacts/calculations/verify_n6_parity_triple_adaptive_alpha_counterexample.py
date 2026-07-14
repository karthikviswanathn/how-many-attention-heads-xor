#!/usr/bin/env python3
"""Exactly verify a counterexample to the adaptive-alpha pair ansatz.

For an ordinary antipodal pair {x, -x}, the ansatz ties the two Farkas
weights in the ratio D(x)^alpha : D(-x)^alpha, where D is the product of
the four positive affine denominators.  The six endpoints in the three
exceptional pairs remain independent.

The verifier constructs rational separating numerators on a finite dyadic
cover of the real alpha line.  Numerical linear programming only discovers
candidate numerators.  Every accepted interval and tail is subsequently
checked with exact rational arithmetic.  Thus solver error can make the
script fail to find the certificate, but cannot make an invalid certificate
pass.
"""

from __future__ import annotations

from fractions import Fraction
import math

import numpy as np
from scipy.optimize import linprog


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
EXCEPTIONAL = frozenset((21, 38, 41))
EXCEPTIONAL_PAIRS = frozenset(
    frozenset((code, FULL ^ code)) for code in EXCEPTIONAL
)
PAIRS = tuple(
    (code, FULL ^ code)
    for code in range(1 << N)
    if code < (FULL ^ code)
)

# Every row has a positive intercept and six strictly negative slopes.
DENOMINATORS = (
    (78, -3, -12, -13, -20, -2, -13),
    (95, -28, -2, -29, -2, -29, -2),
    (95, -17, -1, -27, -11, -7, -4),
    (63, -10, -6, -16, -7, -16, -6),
)

ROUNDING_SCALE = 10**14
TAIL_BOUND = 8
EXPECTED_INTERVALS = 58
EXPECTED_MAX_DYADIC_DENOMINATOR = 4096


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def denominator_values() -> tuple[tuple[int, ...], ...]:
    values = []
    for code in range(1 << N):
        row = []
        for denominator in DENOMINATORS:
            value = denominator[0] + sum(
                denominator[coordinate + 1]
                * character(1 << coordinate, code)
                for coordinate in range(N)
            )
            assert value > 0
            row.append(value)
        values.append(tuple(row))
    return tuple(values)


VALUES = denominator_values()
PRODUCTS = tuple(math.prod(row) for row in VALUES)
LOG_PRODUCTS = np.log(np.array(PRODUCTS, dtype=float))


def signed_feature(code: int) -> np.ndarray:
    sign = target_sign(code)
    entries = [float(sign)]
    for head in range(4):
        for coordinate in range(N):
            entries.append(
                sign
                * character(1 << coordinate, code)
                / VALUES[code][head]
            )
    return np.array(entries, dtype=float)


SIGNED_FEATURES = np.vstack(
    [signed_feature(code) for code in range(1 << N)]
)


def grouped_rows(alpha: float) -> np.ndarray:
    """Return the projectively normalized rows at one finite alpha."""
    rows = []
    for left, right in PAIRS:
        if frozenset((left, right)) in EXCEPTIONAL_PAIRS:
            rows.extend((SIGNED_FEATURES[left], SIGNED_FEATURES[right]))
            continue
        left_log = alpha * LOG_PRODUCTS[left]
        right_log = alpha * LOG_PRODUCTS[right]
        shift = max(left_log, right_log)
        rows.append(
            math.exp(left_log - shift) * SIGNED_FEATURES[left]
            + math.exp(right_log - shift) * SIGNED_FEATURES[right]
        )
    matrix = np.vstack(rows)
    return matrix / np.maximum(np.linalg.norm(matrix, axis=1), 1e-300)[:, None]


def endpoint_rows(positive_infinity: bool) -> np.ndarray:
    """Return the alpha to positive or negative infinity limiting rows."""
    rows = []
    for left, right in PAIRS:
        if frozenset((left, right)) in EXCEPTIONAL_PAIRS:
            rows.extend((SIGNED_FEATURES[left], SIGNED_FEATURES[right]))
            continue
        if PRODUCTS[left] == PRODUCTS[right]:
            rows.append(SIGNED_FEATURES[left] + SIGNED_FEATURES[right])
            continue
        choose_left = (PRODUCTS[left] > PRODUCTS[right]) == positive_infinity
        rows.append(SIGNED_FEATURES[left if choose_left else right])
    matrix = np.vstack(rows)
    return matrix / np.maximum(np.linalg.norm(matrix, axis=1), 1e-300)[:, None]


def separating_numerator(parts: tuple[np.ndarray, ...]) -> tuple[float, tuple[int, ...]]:
    """Discover an integer numerator positive on all supplied row systems."""
    matrix = np.vstack(parts)
    columns = matrix.shape[1]

    # Write v = v_plus - v_minus, impose ||v||_1 <= 1, and maximize the
    # common signed margin t.
    objective = np.zeros(2 * columns + 1, dtype=float)
    objective[-1] = -1.0
    inequalities = np.zeros(
        (matrix.shape[0] + 1, 2 * columns + 1), dtype=float
    )
    inequalities[:-1, :columns] = -matrix
    inequalities[:-1, columns : 2 * columns] = matrix
    inequalities[:-1, -1] = 1.0
    inequalities[-1, : 2 * columns] = 1.0
    bounds = [(0.0, None)] * (2 * columns) + [(None, None)]
    result = linprog(
        objective,
        A_ub=inequalities,
        b_ub=np.concatenate([np.zeros(matrix.shape[0]), [1.0]]),
        bounds=bounds,
        method="highs-ds",
    )
    if not result.success:
        return float("-inf"), ()
    numerator = result.x[:columns] - result.x[columns : 2 * columns]
    integers = tuple(int(round(ROUNDING_SCALE * value)) for value in numerator)
    return float(result.x[-1]), integers


def signed_scores(numerator: tuple[int, ...]) -> tuple[Fraction, ...]:
    assert len(numerator) == 25
    answer = []
    for code in range(1 << N):
        value = Fraction(numerator[0])
        index = 1
        for head in range(4):
            for coordinate in range(N):
                value += Fraction(
                    numerator[index] * character(1 << coordinate, code),
                    VALUES[code][head],
                )
                index += 1
        answer.append(target_sign(code) * value)
    return tuple(answer)


def two_term_positive_at(
    left_score: Fraction,
    right_score: Fraction,
    left_product: int,
    right_product: int,
    alpha: Fraction,
) -> bool:
    """Check a D_left^alpha + b D_right^alpha > 0 exactly."""
    if left_score >= 0 and right_score >= 0:
        return left_score > 0 or right_score > 0
    if left_score <= 0 and right_score <= 0:
        return False

    power = alpha.numerator
    root = alpha.denominator
    if left_score > 0:
        left = Fraction(left_product, right_product) ** power
        right = Fraction(-right_score, left_score) ** root
        return left > right
    left = Fraction(right_product, left_product) ** power
    right = Fraction(-left_score, right_score) ** root
    return left > right


def valid_at(numerator: tuple[int, ...], alpha: Fraction) -> bool:
    scores = signed_scores(numerator)
    for left, right in PAIRS:
        if frozenset((left, right)) in EXCEPTIONAL_PAIRS:
            if scores[left] <= 0 or scores[right] <= 0:
                return False
            continue
        if not two_term_positive_at(
            scores[left],
            scores[right],
            PRODUCTS[left],
            PRODUCTS[right],
            alpha,
        ):
            return False
    return True


def valid_at_limit(
    numerator: tuple[int, ...], positive_infinity: bool
) -> bool:
    scores = signed_scores(numerator)
    for left, right in PAIRS:
        if frozenset((left, right)) in EXCEPTIONAL_PAIRS:
            if scores[left] <= 0 or scores[right] <= 0:
                return False
            continue
        if PRODUCTS[left] == PRODUCTS[right]:
            if scores[left] + scores[right] <= 0:
                return False
            continue
        choose_left = (PRODUCTS[left] > PRODUCTS[right]) == positive_infinity
        if scores[left if choose_left else right] <= 0:
            return False
    return True


def interval_certificate(
    left: Fraction, right: Fraction
) -> tuple[float, tuple[int, ...]] | None:
    margin, numerator = separating_numerator(
        (grouped_rows(float(left)), grouped_rows(float(right)))
    )
    if (
        margin > 1e-10
        and numerator
        and valid_at(numerator, left)
        and valid_at(numerator, right)
    ):
        return margin, numerator
    return None


def dyadic_cover(
    left: Fraction,
    right: Fraction,
    depth: int = 0,
) -> list[tuple[Fraction, Fraction, tuple[int, ...]]]:
    certificate = interval_certificate(left, right)
    if certificate is not None:
        return [(left, right, certificate[1])]
    assert depth < 24, (left, right)
    middle = (left + right) / 2
    return dyadic_cover(left, middle, depth + 1) + dyadic_cover(
        middle, right, depth + 1
    )


def tail_certificate(positive_infinity: bool) -> tuple[int, ...]:
    finite = TAIL_BOUND if positive_infinity else -TAIL_BOUND
    margin, numerator = separating_numerator(
        (grouped_rows(float(finite)), endpoint_rows(positive_infinity))
    )
    assert margin > 1e-10
    assert valid_at(numerator, Fraction(finite))
    assert valid_at_limit(numerator, positive_infinity)
    return numerator


def verify() -> tuple[tuple[Fraction, Fraction, tuple[int, ...]], ...]:
    assert len(PAIRS) == 32
    assert len(EXCEPTIONAL_PAIRS) == 3
    for denominator in DENOMINATORS:
        assert all(value < 0 for value in denominator[1:])
        assert denominator[0] > sum(abs(value) for value in denominator[1:])

    cover = tuple(
        dyadic_cover(Fraction(-TAIL_BOUND), Fraction(TAIL_BOUND))
    )
    assert len(cover) == EXPECTED_INTERVALS
    assert cover[0][0] == -TAIL_BOUND
    assert cover[-1][1] == TAIL_BOUND
    assert all(
        left[1] == right[0] for left, right in zip(cover, cover[1:])
    )
    assert max(
        max(left.denominator, right.denominator)
        for left, right, _ in cover
    ) == EXPECTED_MAX_DYADIC_DENOMINATOR

    tail_certificate(False)
    tail_certificate(True)
    return cover


def main() -> None:
    cover = verify()
    print("admissible denominator heads: 4")
    print("ordinary antipodal pairs: 29")
    print("independent exceptional endpoints: 6")
    print(f"exact finite interval certificates: {len(cover)}")
    print("exact tail certificates: 2")
    print("verified adaptive-alpha grouped-dual counterexample")


if __name__ == "__main__":
    main()
