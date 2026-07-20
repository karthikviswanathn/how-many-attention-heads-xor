#!/usr/bin/env python3
"""Verify the first exact rational signed-secant McCormick cell leaf."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from hstar.boolean_cube import signs_from_mask
from hstar.signed_secant_mccormick import (
    discover_signed_secant_mccormick_leaf,
    verify_signed_secant_mccormick_leaf,
)


HERE = Path(__file__).resolve().parent


def main() -> None:
    certificate = json.loads(
        (HERE / "signed_secant_mccormick_leaf_xor1.json").read_text()
    )
    signs = signs_from_mask(0x2, 1)
    report = verify_signed_secant_mccormick_leaf(certificate, signs)
    assert report["valid"], report
    assert report["upper_bound"] == "0"
    assert report["nonzero_inequality_multipliers"] == 3
    assert report["nonzero_equality_multipliers"] == 0

    skeleton = deepcopy(certificate)
    skeleton.pop("lambda")
    skeleton.pop("dual")
    discovered, diagnostics = discover_signed_secant_mccormick_leaf(
        skeleton,
        signs,
        active_vertices=[0, 1],
        max_denominator=256,
    )
    assert diagnostics["status"] == "verified-exact-leaf-found", diagnostics
    assert discovered is not None
    assert discovered["lambda"] == [{"vertex": 0, "weight": "1"}]
    discovered_report = verify_signed_secant_mccormick_leaf(discovered, signs)
    assert discovered_report["valid"], discovered_report
    assert discovered_report["upper_bound"] == "0"

    negative_dual = deepcopy(certificate)
    negative_dual["dual"]["inequality_multipliers"][
        "bound_lower::x0_R_1"
    ] = "-1/2"
    assert not verify_signed_secant_mccormick_leaf(negative_dual, signs)["valid"]

    wrong_chart = deepcopy(certificate)
    wrong_chart["cell"]["scalar_direction_bounds"] = ["0", "1"]
    assert not verify_signed_secant_mccormick_leaf(wrong_chart, signs)["valid"]

    wrong_stationarity = deepcopy(certificate)
    wrong_stationarity["dual"]["inequality_multipliers"].pop(
        "bound_lower::x0_aP"
    )
    assert not verify_signed_secant_mccormick_leaf(
        wrong_stationarity,
        signs,
    )["valid"]

    wrong_truth_table = signs_from_mask(0x1, 1)
    assert not verify_signed_secant_mccormick_leaf(
        certificate,
        wrong_truth_table,
    )["valid"]

    print(
        json.dumps(
            {
                "archived_leaf": report,
                "discovery": diagnostics,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
