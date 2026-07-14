#!/usr/bin/env python3
"""Pack GF(3^6) evaluation files as a row-major two-plane GF3 matrix."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import search_n5_collision_degree7_gf3 as gf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--append", action="store_true")
    parser.add_argument("inputs", type=Path, nargs="+")
    arguments = parser.parse_args()

    records = []
    orbit_count = None
    for path in arguments.inputs:
        payload = np.load(path)
        current_count = int(payload["orbit_count"])
        if orbit_count is None:
            orbit_count = current_count
        assert current_count == orbit_count
        records.append(
            (
                int(payload["start"]),
                int(payload["end"]),
                payload["evaluations"],
            )
        )
    records.sort()
    assert records[0][0] == 0
    assert records[-1][1] == orbit_count
    assert all(
        records[index][1] == records[index + 1][0]
        for index in range(len(records) - 1)
    )
    evaluations = np.concatenate([record[2] for record in records], axis=1)
    samples, columns = evaluations.shape
    assert columns == orbit_count

    coefficients = gf.coefficient_table()
    words = (columns + 63) // 64
    planes = np.zeros(
        (samples * gf.FIELD_DEGREE, 2, words), dtype=np.uint64
    )
    padded_bytes = words * 8
    for coordinate in range(gf.FIELD_DEGREE):
        digits = coefficients[evaluations, coordinate]
        for plane, value in enumerate((1, 2)):
            packed = np.packbits(
                digits == value, axis=1, bitorder="little"
            )
            if packed.shape[1] < padded_bytes:
                packed = np.pad(
                    packed,
                    ((0, 0), (0, padded_bytes - packed.shape[1])),
                )
            planes[
                coordinate * samples : (coordinate + 1) * samples,
                plane,
                :,
            ] = packed.view(np.uint64)
        print(
            f"packed coordinate={coordinate + 1}/{gf.FIELD_DEGREE}",
            flush=True,
        )
    mode = "ab" if arguments.append else "wb"
    with arguments.output.open(mode) as output_file:
        planes.tofile(output_file)
    print(
        f"wrote rows={len(planes)} columns={columns} words={words} "
        f"to {arguments.output}"
    )


if __name__ == "__main__":
    main()
