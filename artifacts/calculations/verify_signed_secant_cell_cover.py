#!/usr/bin/env python3
"""Verify a rational binary cover tree of signed-secant subcells."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from hstar.boolean_cube import signs_from_mask
from hstar.signed_secant_mccormick import verify_signed_secant_cell_cover


HERE = Path(__file__).resolve().parent


def main() -> None:
    certificate = json.loads(
        (HERE / "signed_secant_subcell_cover_xor1.json").read_text()
    )
    signs = signs_from_mask(0x2, 1)
    report = verify_signed_secant_cell_cover(certificate, signs)
    assert report["valid"], report
    assert report["nodes"] == 3
    assert report["splits"] == 1
    assert report["leaves"] == 2
    assert report["maximum_depth"] == 1
    assert not report["root_is_full_chart_box"]
    assert not report["chart_infeasible"]
    assert not report["global_head_lower_bound"]

    f8_certificate = json.loads(
        (HERE / "f8_h2_pp_scalar_plus_chart_cover.json").read_text()
    )
    from hstar.certified import _eight_bit_hamming_signs

    f8_report = verify_signed_secant_cell_cover(
        f8_certificate,
        _eight_bit_hamming_signs(),
    )
    assert f8_report["valid"], f8_report
    assert f8_report["root_is_full_chart_box"]
    assert f8_report["chart_infeasible"]
    assert not f8_report["global_head_lower_bound"]
    assert f8_report["leaves"] == 1

    bad_pivot = deepcopy(certificate)
    bad_pivot["tree"]["split"]["value"] = "0"
    assert not verify_signed_secant_cell_cover(bad_pivot, signs)["valid"]

    missing_child = deepcopy(certificate)
    missing_child["tree"].pop("right")
    assert not verify_signed_secant_cell_cover(missing_child, signs)["valid"]

    bad_dual = deepcopy(certificate)
    bad_dual["tree"]["right"]["leaf"]["dual"][
        "claimed_upper_bound"
    ] = "0"
    assert not verify_signed_secant_cell_cover(bad_dual, signs)["valid"]

    print(
        json.dumps(
            {
                "one_bit_subcell_cover": report,
                "eight_bit_full_chart_cover": f8_report,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
