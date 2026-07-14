#!/usr/bin/env python3
"""Exact verifier for the five-bit finite H3 dictionary cover.

The archive contains three kinds of exact data:

1. 6,508 Boolean clauses excluding every parity-twisted weak affine
   extension, exactly characterizing degree-at-most-three sign patterns.
2. Integer H3 certificates and all symmetry-expanded singleton clauses.
3. Simple tangent-family rays. If the score space has rank r, a stored ray
   has r - 1 zero rows and the restriction to those rows has rank r - 1.
   Therefore arbitrary signs can be prescribed on the zero set while a large
   positive multiple of the ray fixes every remaining sign.

All matrix products, signs, ranks, symmetry transforms, and Boolean clauses
are rechecked. No cubic coefficient bound or floating-point feasibility claim
is used in the final decision.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

import search_n5_cubic_dictionary_milp as cover


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "n5_cubic_dictionary_cover.json"


def verify_archive(
    payload: dict[str, object],
    node_limit: int,
    allow_incomplete: bool,
) -> None:
    if cover.upgrade_payload(payload):
        raise AssertionError("archive uses an obsolete or incomplete schema")
    assert payload["schema_version"] == 3
    parameters = payload["parameters"]
    assert parameters["input_bits"] == 5
    assert parameters["heads"] == 3
    assert parameters["degree_clause_count"] == 6_508
    assert parameters["cubic_coefficient_bound"] is None
    assert parameters["symmetric_near_literal_seed_count"] == 80
    assert parameters["asymmetric_near_literal_representative_count"] == 2
    assert parameters["asymmetric_near_literal_orbit_count"] == 480

    dictionary = payload["base_dictionary"]
    assert len(dictionary) == len(
        {cover.canonical_triple(item) for item in dictionary}
    )
    assert all(cover.valid_denominators(item) for item in dictionary)

    learned = payload["learned_certificates"]
    for record in learned:
        cover.verify_head_record(record)

    singleton_clause_total = 0
    for singleton in payload["singleton_covers"]:
        index = int(singleton["learned_certificate_index"])
        assert 0 <= index < len(learned)
        record = learned[index]
        assert singleton["source_mask_hex"] == record["truth_mask_hex"]
        clauses = cover.singleton_clauses(singleton)
        assert len(clauses) == int(singleton["orbit_clause_count"])
        singleton_clause_total += len(clauses)
        cover.verify_head_symmetry_orbit(record)

    rank_histogram: Counter[int] = Counter()
    family_clause_total = 0
    for family in payload["families"]:
        cover.verify_family(family)
        rank = int(family["score_space_rank"])
        assert int(family["zero_restriction_rank"]) == rank - 1
        clauses = cover.family_clauses(family)
        family_clause_total += len(clauses)
        rank_histogram[rank] += 1

    degree = cover.degree_clauses()
    assert len(degree) == 6_508
    clauses = cover.all_search_clauses(
        payload["families"], payload["singleton_covers"]
    )
    candidate, summary = cover.dpll_candidate(clauses, node_limit)
    final = payload.get("final_dpll")
    assert final is not None
    assert int(final["clause_count"]) == len(clauses)
    assert final["status"] == summary["status"]
    if candidate is None:
        assert final["status"] == "UNSAT"
    else:
        if not allow_incomplete:
            raise AssertionError(
                f"cover is incomplete; exact survivor is 0x{candidate:08x}"
            )
        assert final["status"] == "candidate"
        archived_candidate = int(final["candidate_mask_hex"], 16)
        assert cover.satisfies_clauses(archived_candidate, clauses)
        cover.exact_degree_certificate(archived_candidate)

    print(
        json.dumps(
            {
                "status": summary["status"],
                "exact_clause_count": len(clauses),
                "degree_clause_count": len(degree),
                "family_count": len(payload["families"]),
                "family_rank_histogram": dict(sorted(rank_histogram.items())),
                "raw_family_orbit_clause_count": family_clause_total,
                "singleton_count": len(payload["singleton_covers"]),
                "raw_singleton_orbit_clause_count": singleton_clause_total,
                "dpll_nodes": summary["nodes"],
                "dpll_max_depth": summary["max_depth"],
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, nargs="?", default=DEFAULT_INPUT)
    parser.add_argument("--dpll-node-limit", type=int, default=10_000_000)
    parser.add_argument("--allow-incomplete", action="store_true")
    arguments = parser.parse_args()
    payload = json.loads(arguments.input.read_text())
    verify_archive(payload, arguments.dpll_node_limit, arguments.allow_incomplete)


if __name__ == "__main__":
    main()
