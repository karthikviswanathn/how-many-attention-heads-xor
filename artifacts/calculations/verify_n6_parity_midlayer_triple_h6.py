#!/usr/bin/env python3
"""Verify the six-head parity triple-flip certificate with Python integers."""

from __future__ import annotations

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE_PATH = HERE / "n6_parity_midlayer_triple_h6_certificate.json"
EXPECTED_MASK = 0x96696BD669B69669


def bits(code: int, dimension: int) -> tuple[int, ...]:
    return tuple((code >> coordinate) & 1 for coordinate in range(dimension))


def affine_value(coefficients: list[int], point: tuple[int, ...]) -> int:
    return coefficients[0] + sum(
        coefficient * value
        for coefficient, value in zip(coefficients[1:], point)
    )


def main() -> None:
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    dimension = certificate["dimension"]
    heads = certificate["head_count"]
    orientations = certificate["orientations"]
    denominators = certificate["denominators"]
    coefficients = certificate["score_coefficients"]

    assert dimension == 6
    assert certificate["vertex_order"] == "integer-code-lsb-coordinate-0"
    assert int(certificate["truth_mask_hex"], 16) == EXPECTED_MASK
    assert heads == 6
    assert len(orientations) == heads
    assert len(denominators) == heads
    assert len(coefficients) == 1 + heads * (dimension + 1)

    denominator_values: list[list[int]] = []
    for orientation, denominator in zip(orientations, denominators):
        assert len(denominator) == dimension + 1
        slopes = denominator[1:]
        if orientation == 1:
            assert denominator[0] > 0
            assert all(slope > 0 for slope in slopes)
        else:
            assert orientation == -1
            assert all(slope < 0 for slope in slopes)
            assert sum(denominator) > 0
        values = [
            affine_value(denominator, bits(code, dimension))
            for code in range(1 << dimension)
        ]
        assert min(values) > 0
        denominator_values.append(values)

    signed_scores = []
    for code in range(1 << dimension):
        point = bits(code, dimension)
        values = [denominator_values[head][code] for head in range(heads)]
        full_product = math.prod(values)
        cleared_score = coefficients[0] * full_product
        for head in range(heads):
            start = 1 + head * (dimension + 1)
            numerator = affine_value(
                coefficients[start : start + dimension + 1],
                point,
            )
            cleared_score += numerator * math.prod(
                values[other] for other in range(heads) if other != head
            )
        target_sign = 1 if (EXPECTED_MASK >> code) & 1 else -1
        signed_scores.append(target_sign * cleared_score)

    assert min(signed_scores) == certificate["minimum_signed_cleared_score"]
    assert max(signed_scores) == certificate["maximum_signed_cleared_score"]
    assert min(signed_scores) > 0

    print(f"certificate: {CERTIFICATE_PATH.name}")
    print("strict denominator orientations: verified")
    print(f"minimum signed cleared score: {min(signed_scores)}")
    print(f"maximum signed cleared score: {max(signed_scores)}")
    print("six-head upper bound: verified")


if __name__ == "__main__":
    main()
