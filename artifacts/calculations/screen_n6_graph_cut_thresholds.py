#!/usr/bin/env python3
"""Screen every six-vertex graph cut threshold for an H2 survivor.

The graph atlas supplies the 156 unlabeled simple graphs on six vertices.  We
deduplicate threshold truth tables under coordinate permutations and output
complement, discard inessential tables, use a fixed exact denominator
dictionary as a fast first pass, and send every dictionary miss to the
one-oriented-factor learner.  Every reported hit has an exact integer H2
certificate.  A search survivor is not a lower bound.

This script requires NetworkX for ``graph_atlas_g``.
"""

from __future__ import annotations

import argparse
import itertools
import json
from argparse import Namespace
from pathlib import Path

import networkx as nx

import search_adversarial_low_dimension as core
import search_continuous_one_oriented_factor as learner
import verify_two_head_candidate_refutations as archived


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "n6_graph_cut_threshold_screen.json"
FULL_MASK = (1 << 64) - 1
PERMUTATIONS = tuple(itertools.permutations(range(6)))


def vertex_maps() -> tuple[tuple[int, ...], ...]:
    answer = []
    for permutation in PERMUTATIONS:
        image = []
        for vertex in range(64):
            transformed = 0
            for source, target in enumerate(permutation):
                transformed |= ((vertex >> source) & 1) << target
            image.append(transformed)
        answer.append(tuple(image))
    return tuple(answer)


VERTEX_MAPS = vertex_maps()


def canonical_mask(mask: int) -> int:
    best = min(mask, FULL_MASK ^ mask)
    support = tuple(vertex for vertex in range(64) if (mask >> vertex) & 1)
    for image in VERTEX_MAPS:
        transformed = sum(1 << image[vertex] for vertex in support)
        best = min(best, transformed, FULL_MASK ^ transformed)
    return best


def all_variables_essential(mask: int) -> bool:
    return all(
        any(
            ((mask >> vertex) & 1)
            != ((mask >> (vertex ^ (1 << coordinate))) & 1)
            for vertex in range(64)
        )
        for coordinate in range(6)
    )


def graph_cut_mask(edges: tuple[tuple[int, int], ...], threshold: int) -> int:
    mask = 0
    for vertex in range(64):
        cut = sum(
            ((vertex >> first) & 1) ^ ((vertex >> second) & 1)
            for first, second in edges
        )
        if cut >= threshold:
            mask |= 1 << vertex
    return mask


def candidate_inventory() -> dict[int, list[dict[str, object]]]:
    inventory: dict[int, list[dict[str, object]]] = {}
    graphs = [graph for graph in nx.graph_atlas_g() if len(graph) == 6]
    assert len(graphs) == 156
    for atlas_index, graph in enumerate(graphs):
        edges = tuple(sorted(tuple(sorted(edge)) for edge in graph.edges()))
        cut_values = [
            sum(
                ((vertex >> first) & 1) ^ ((vertex >> second) & 1)
                for first, second in edges
            )
            for vertex in range(64)
        ]
        for threshold in range(1, max(cut_values, default=0) + 1):
            raw_mask = graph_cut_mask(edges, threshold)
            if not all_variables_essential(raw_mask):
                continue
            mask = canonical_mask(raw_mask)
            inventory.setdefault(mask, []).append(
                {
                    "atlas_index": atlas_index,
                    "edges": [list(edge) for edge in edges],
                    "threshold": threshold,
                    "raw_truth_mask_hex": f"0x{raw_mask:016x}",
                }
            )
    return inventory


def write_checkpoint(
    path: Path,
    records: list[dict[str, object]],
    excluded: list[str],
    inventory_size: int,
    restarts: int,
    max_iterations: int,
) -> None:
    survivors = sorted(
        (
            record
            for record in records
            if not record["h2_search"]["found"]
        ),
        key=lambda record: (
            record["h2_search"]["best_accuracy"],
            record["h2_search"]["best_minimum_signed_score"],
        ),
        reverse=True,
    )
    payload = {
        "status": (
            "Every H2 success is exact. A search survivor is not an H2 lower "
            "bound."
        ),
        "unlabeled_graphs": 156,
        "essential_canonical_truth_tables": inventory_size,
        "excluded_archived_masks": excluded,
        "one_oriented_restarts_per_orientation": restarts,
        "max_iterations": max_iterations,
        "records": records,
        "survivor_masks_ranked": [
            record["truth_mask_hex"] for record in survivors
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dictionary-size", type=int, default=128)
    parser.add_argument("--restarts", type=int, default=20)
    parser.add_argument("--max-iterations", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=202607146)
    arguments = parser.parse_args()

    inventory = candidate_inventory()
    archived_masks = {
        canonical_mask(archived.N6_TRUTH_MASK),
        canonical_mask(archived.N6_SMALL_DIM_TRUTH_MASK),
        canonical_mask(archived.N6_BROAD_TRUTH_MASK),
        canonical_mask(0x724E7FFE7FFE724E),
    }
    excluded = [
        f"0x{mask:016x}"
        for mask in sorted(inventory.keys() & archived_masks)
    ]
    masks = sorted(inventory.keys() - archived_masks)
    dictionary = core.build_dictionary(6, arguments.dictionary_size, arguments.seed)

    records: list[dict[str, object]] = []
    for index, mask in enumerate(masks):
        signs = core.signs_from_mask(mask, 6)
        dictionary_hit = None
        for dictionary_index, denominators in enumerate(dictionary):
            certificate = core.exact_pair_certificate(
                mask,
                6,
                denominators,
                method="fixed-dictionary",
                dictionary_index=dictionary_index,
            )
            if certificate is not None:
                dictionary_hit = certificate
                break

        if dictionary_hit is not None:
            result = dictionary_hit
        else:
            result = learner.search(
                Namespace(
                    dimension=6,
                    mask=mask,
                    restarts=arguments.restarts,
                    max_iterations=arguments.max_iterations,
                    seed=arguments.seed + 100003 * index,
                    scales=(10, 30, 100, 300, 1000, 3000, 10000),
                )
            )

        ltf = core.exact_integer_separator(signs, core.affine_matrix(6))
        records.append(
            {
                "truth_mask_hex": f"0x{mask:016x}",
                "representatives": inventory[mask],
                "exact_affine_separator": (
                    None if ltf is None else [int(value) for value in ltf[0]]
                ),
                "h2_search": result,
            }
        )
        print(
            f"{index + 1}/{len(masks)}: found={result['found']} "
            f"method={result.get('method', 'one-oriented-factor')} "
            f"mask=0x{mask:016x}",
            flush=True,
        )
        write_checkpoint(
            arguments.output,
            records,
            excluded,
            len(inventory),
            arguments.restarts,
            arguments.max_iterations,
        )

    survivors = [record for record in records if not record["h2_search"]["found"]]
    print(
        f"exact H2 hits: {len(records) - len(survivors)}/{len(records)}; "
        f"survivors: {len(survivors)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
