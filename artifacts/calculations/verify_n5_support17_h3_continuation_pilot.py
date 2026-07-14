#!/usr/bin/env python3
"""Verify the exact support-17 H3 adjacency-continuation pilot.

The graph joins two canonical exact-degree-three-only circuit families when
their 15-point free sets differ by one exchanged cube vertex.  Starting from
the exact global-dictionary seed at family 16737, a deterministic search pilot
attempted every one of its 12 graph neighbors.  The first pass exactified nine
hits.  A stronger second pass exactified the remaining three.  The script
archives and exactly verifies all 12 hits while retaining the precise first-
pass miss list.

A search miss is not a head lower bound.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np

import search_n5_support17_global_dictionary as global_search


HERE = Path(__file__).resolve().parent
CODES = HERE / "n5_support17_exact_degree3_only_codes.tsv"
VERTICES = 32
SEED = 16_737

SEED_DENOMINATORS = np.array(
    [
        [999999, -1101, -8721, -206419, -868, -780890],
        [1023341, -844279, -1, -1, -67592, -111467],
        [1039074, -791803, -1, -50224, -45368, -56119],
    ],
    dtype=np.int64,
)

NEIGHBORS = (
    14_950,
    16_404,
    16_454,
    16_725,
    16_735,
    16_738,
    16_739,
    16_741,
    16_809,
    16_846,
    16_856,
    16_857,
)

CERTIFICATES = {
    14_950: (
        (1000, -163, -27, -620, -63, -93),
        (1000, -26, -2, -813, -1, -153),
        (26, 133, 33, 466, 270, 72),
    ),
    16_404: (
        (300, -145, -27, -123, -1, -1),
        (302, -1, -82, -4, -103, -1),
        (301, -28, -87, -41, -101, -28),
    ),
    16_454: (
        (10000, -917, -1000, -486, -2073, -3751),
        (9999, -5641, -732, -1639, -1458, -92),
        (10000, -125, -205, -1, -7526, -1547),
    ),
    16_725: (
        (300, -1, -70, -21, -14, -6),
        (298, -108, -30, -1, -6, -134),
        (299, -51, -53, -44, -31, -67),
    ),
    16_735: (
        (100, -19, -1, -71, -6, -2),
        (101, -61, -9, -1, -16, -1),
        (41, 22, 6, 17, 5, 10),
    ),
    16_738: (
        (3000, -825, -409, -211, -58, -1369),
        (3000, -102, -322, -18, -186, -1995),
        (3000, -51, -222, -1022, -54, -1105),
    ),
    16_739: (
        (1000001, -372266, -51260, -192103, -149401, -62635),
        (1000001, -17275, -10031, -43973, -7564, -40018),
        (1000000, -999475, -32, -239, -77, -1),
    ),
    16_741: (
        (32, 399, 22, 6576, 2928, 43),
        (3836, 610, 91, 2247, 3021, 196),
        (2264, 2653, 600, 91, 2683, 1709),
    ),
    16_809: (
        (999, -4, -67, -874, -12, -20),
        (1001, -15, -126, -1, -48, -792),
        (999, -220, -212, -81, -2, -11),
    ),
    16_846: (
        (999, -532, -1, -6, -3, -19),
        (1000, -507, -188, -126, -30, -129),
        (999, -202, -44, -656, -37, -54),
    ),
    16_856: (
        (299, -52, -44, -188, -3, -3),
        (300, -1, -8, -153, -30, -2),
        (301, -42, -113, -1, -24, -110),
    ),
    16_857: (
        (10000, -43, -26, -38, -3089, -5249),
        (10000, -2826, -2402, -489, -1080, -2197),
        (10001, -958, -502, -8139, -104, -136),
    ),
}

# These are exact misses for four direct-optimization restarts of 900 steps
# with the archived deterministic family seeds.  They are not mathematical
# nonexistence statements.
FIRST_PASS_SEARCH_MISSES = {
    16_404: -0.0064282195412597365,
    16_735: -0.001743462401583931,
    16_857: -0.0029634910999581346,
}


def zero_mask(signs: np.ndarray) -> int:
    answer = 0
    for vertex in np.flatnonzero(signs == 0):
        answer |= 1 << int(vertex)
    return answer


def adjacency(signs: np.ndarray) -> list[set[int]]:
    masks = [zero_mask(row) for row in signs]
    lookup = {mask: index for index, mask in enumerate(masks)}
    assert len(lookup) == len(masks)
    graph = [set() for _ in masks]
    for family, mask in enumerate(masks):
        free = [
            vertex for vertex in range(VERTICES) if (mask >> vertex) & 1
        ]
        support = [
            vertex
            for vertex in range(VERTICES)
            if not ((mask >> vertex) & 1)
        ]
        for removed in free:
            partial = mask ^ (1 << removed)
            for added in support:
                neighbor = lookup.get(partial ^ (1 << added))
                if neighbor is not None and neighbor != family:
                    graph[family].add(neighbor)
                    graph[neighbor].add(family)
    return graph


def component_sizes(graph: list[set[int]]) -> list[int]:
    seen = set()
    answer = []
    for start in range(len(graph)):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        size = 0
        while stack:
            family = stack.pop()
            size += 1
            for neighbor in graph[family]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        answer.append(size)
    return answer


def main() -> None:
    codes = global_search.load_codes(CODES)
    signs = global_search.decode_codes(codes)
    graph = adjacency(signs)

    edges = sum(len(neighbors) for neighbors in graph) // 2
    nonisolated = sum(bool(neighbors) for neighbors in graph)
    sizes = component_sizes(graph)
    distribution = Counter(sizes)
    assert edges == 50_569
    assert nonisolated == 22_243
    assert len(sizes) == 1_282
    assert max(sizes) == 20_896
    assert distribution[1] == 873
    assert tuple(sorted(graph[SEED])) == NEIGHBORS

    seed_hit, seed_margin = global_search.exact_family_hit(
        signs[SEED], SEED_DENOMINATORS
    )
    assert seed_hit and seed_margin > 0

    exact_margins = {}
    for family, denominators in sorted(CERTIFICATES.items()):
        hit, margin = global_search.exact_family_hit(
            signs[family], np.array(denominators, dtype=np.int64)
        )
        assert hit and margin > 0
        exact_margins[family] = margin

    assert set(CERTIFICATES) == set(NEIGHBORS)
    assert set(FIRST_PASS_SEARCH_MISSES) < set(CERTIFICATES)

    print("verified exact support-17 H3 continuation pilot")
    print(
        f"graph vertices={len(graph)} edges={edges} "
        f"components={len(sizes)} giant={max(sizes)}"
    )
    print(
        f"seed={SEED} attempted_neighbors={len(NEIGHBORS)} "
        f"exact_hits={len(CERTIFICATES)} final_search_misses=0"
    )
    print(f"hit families={tuple(sorted(CERTIFICATES))}")
    print(
        "first pass miss families="
        f"{tuple(sorted(FIRST_PASS_SEARCH_MISSES))}"
    )


if __name__ == "__main__":
    main()
