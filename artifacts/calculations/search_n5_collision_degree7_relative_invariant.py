#!/usr/bin/env python3
"""Search the complete degree-seven S5-relative collision invariant space.

At the symmetric collision center L = 1, retain the ten quadratic edge
coefficients and ten cubic triangle coefficients.  The fixed-center image is

    q = B U M + A M + E,

where E affects only degree zero and one.  Its irreducible hypersurface
equation transforms under either the trivial or sign character of S5.

There are 6650 S5 orbits of degree-seven monomials in the 20 high
coefficients.  In characteristic two, invariant and alternating orbit sums
coincide.  To avoid the false identities caused by evaluating only in F2,
this script evaluates over GF(256), then expands each equality into eight F2
equations.  Exact bitset elimination searches the full 6650-dimensional
relative-invariant space.

Use three block calls followed by one combine call.  Example:

    python3 SCRIPT --block 0 --blocks 3 --output /tmp/collision7_0.npz
    python3 SCRIPT --block 1 --blocks 3 --output /tmp/collision7_1.npz
    python3 SCRIPT --block 2 --blocks 3 --output /tmp/collision7_2.npz
    python3 SCRIPT --combine /tmp/collision7_0.npz /tmp/collision7_1.npz \
        /tmp/collision7_2.npz
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np


N = 5
DEGREE = 7
SAMPLES = 850
SEED = 707
EXPECTED_ORBITS = 6_650


def popcount(value: int) -> int:
    return bin(value).count("1")


def multiplication_table() -> np.ndarray:
    """Return GF(256) multiplication for x^8+x^4+x^3+x+1."""
    table = np.zeros((256, 256), dtype=np.uint8)
    for left in range(256):
        for right in range(256):
            current_left = left
            current_right = right
            product = 0
            for _ in range(8):
                if current_right & 1:
                    product ^= current_left
                high = current_left & 0x80
                current_left = (current_left << 1) & 0xFF
                if high:
                    current_left ^= 0x1B
                current_right >>= 1
            table[left, right] = product
    return table


def variable_permutations() -> tuple[list[int], list[list[int]]]:
    variables = [
        mask for mask in range(1 << N) if popcount(mask) in (2, 3)
    ]
    variable_index = {mask: index for index, mask in enumerate(variables)}
    permutations = []
    for permutation in itertools.permutations(range(N)):
        transformed = []
        for mask in variables:
            target = 0
            for source in range(N):
                if (mask >> source) & 1:
                    target |= 1 << permutation[source]
            transformed.append(variable_index[target])
        permutations.append(transformed)
    return variables, permutations


def monomial_orbits() -> tuple[np.ndarray, list[list[int]]]:
    _, permutations = variable_permutations()
    monomials = list(
        itertools.combinations_with_replacement(range(20), DEGREE)
    )
    lookup = {monomial: index for index, monomial in enumerate(monomials)}
    seen = set()
    orbits = []
    for index, monomial in enumerate(monomials):
        if index in seen:
            continue
        orbit = sorted(
            {
                lookup[
                    tuple(sorted(permutation[value] for value in monomial))
                ]
                for permutation in permutations
            }
        )
        seen.update(orbit)
        orbits.append(orbit)
    assert len(orbits) == EXPECTED_ORBITS
    return np.array(monomials, dtype=np.int8), orbits


def affine_polynomial(coefficients: np.ndarray) -> np.ndarray:
    answer = np.zeros(1 << N, dtype=np.uint8)
    answer[[0, 1, 2, 4, 8, 16]] = coefficients
    return answer


def boolean_product(
    left: np.ndarray, right: np.ndarray, table: np.ndarray
) -> np.ndarray:
    answer = np.zeros(1 << N, dtype=np.uint8)
    for left_mask in np.flatnonzero(left):
        for right_mask in np.flatnonzero(right):
            answer[left_mask | right_mask] ^= table[
                left[left_mask], right[right_mask]
            ]
    return answer


def sampled_high_coefficients(table: np.ndarray) -> np.ndarray:
    variables, _ = variable_permutations()
    rng = np.random.default_rng(SEED)
    parameters = rng.integers(
        0, 256, size=(SAMPLES, 4, N + 1), dtype=np.uint8
    )
    answer = np.empty((SAMPLES, 20), dtype=np.uint8)
    for sample in range(SAMPLES):
        denominator_left, denominator_right, multiplier, numerator = [
            affine_polynomial(row) for row in parameters[sample]
        ]
        cubic = boolean_product(
            denominator_left,
            boolean_product(denominator_right, multiplier, table),
            table,
        )
        quadratic = boolean_product(numerator, multiplier, table)
        answer[sample] = (cubic ^ quadratic)[variables]
    return answer


def evaluate_block(block: int, blocks: int, output: Path) -> None:
    if not 0 <= block < blocks:
        raise ValueError("block must be in range(blocks)")
    table = multiplication_table()
    monomials, orbits = monomial_orbits()
    values = sampled_high_coefficients(table)
    start = len(orbits) * block // blocks
    end = len(orbits) * (block + 1) // blocks
    evaluations = np.empty((SAMPLES, end - start), dtype=np.uint8)
    for output_column, orbit_index in enumerate(range(start, end)):
        orbit_monomials = monomials[orbits[orbit_index]]
        products = values[:, orbit_monomials[:, 0]]
        for factor in range(1, DEGREE):
            products = table[
                products, values[:, orbit_monomials[:, factor]]
            ]
        evaluations[:, output_column] = np.bitwise_xor.reduce(
            products, axis=1
        )
    np.savez_compressed(
        output,
        block=np.array(block, dtype=np.int64),
        blocks=np.array(blocks, dtype=np.int64),
        start=np.array(start, dtype=np.int64),
        end=np.array(end, dtype=np.int64),
        evaluations=evaluations,
    )
    print(f"wrote block={block}/{blocks} columns=[{start},{end}) to {output}")


def packed_binary_column(column: np.ndarray) -> int:
    answer = 0
    for bit in range(8):
        packed = np.packbits(
            (column >> bit) & 1, bitorder="little"
        ).tobytes()
        answer |= int.from_bytes(packed, "little") << (bit * SAMPLES)
    return answer


def combine(paths: list[Path]) -> None:
    records = []
    for path in paths:
        payload = np.load(path)
        records.append(
            (
                int(payload["start"]),
                int(payload["end"]),
                payload["evaluations"],
            )
        )
    records.sort()
    assert records[0][0] == 0
    assert records[-1][1] == EXPECTED_ORBITS
    assert all(
        records[index][1] == records[index + 1][0]
        for index in range(len(records) - 1)
    )
    evaluations = np.concatenate([record[2] for record in records], axis=1)
    assert evaluations.shape == (SAMPLES, EXPECTED_ORBITS)

    basis: dict[int, int] = {}
    combination_basis: dict[int, int] = {}
    rank = 0
    dependencies = []
    for column_index in range(EXPECTED_ORBITS):
        column = packed_binary_column(evaluations[:, column_index])
        combination = 1 << column_index
        while column:
            pivot = column.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = column
                combination_basis[pivot] = combination
                rank += 1
                break
            column ^= basis[pivot]
            combination ^= combination_basis[pivot]
        if column == 0:
            dependencies.append(combination)

    print(f"degree-seven relative-invariant columns={EXPECTED_ORBITS}")
    print(f"exact GF2 rank from GF256 evaluations={rank}")
    print(f"dependency dimension={len(dependencies)}")
    for index, dependency in enumerate(dependencies[:10]):
        support = [
            column
            for column in range(EXPECTED_ORBITS)
            if (dependency >> column) & 1
        ]
        print(
            f"dependency={index} support_size={len(support)} "
            f"orbit_indices={support}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", type=int)
    parser.add_argument("--blocks", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--combine", type=Path, nargs="+")
    arguments = parser.parse_args()
    if arguments.combine is not None:
        combine(arguments.combine)
        return
    if arguments.block is None or arguments.output is None:
        raise ValueError("block mode requires --block and --output")
    evaluate_block(
        arguments.block, arguments.blocks, arguments.output
    )


if __name__ == "__main__":
    main()
