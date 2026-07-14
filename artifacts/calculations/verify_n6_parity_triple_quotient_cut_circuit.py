#!/usr/bin/env python3
"""Verify an exact slice-edge plus quotient-cut Gordan circuit.

This is a fixed-denominator diagnostic for the six-bit parity-triple target.
It is not a parameter-uniform four-head obstruction.
"""

from __future__ import annotations

import itertools
import math

import verify_n6_parity_triple_slice_cone_limit as base


MIDDLE_ROW_COUNT = 120
CUT_ROW_COUNT = 15
SUPPORT_INDICES = (
    15,
    25,
    26,
    27,
    35,
    37,
    54,
    58,
    59,
    61,
    66,
    67,
    70,
    71,
    72,
    76,
    79,
    82,
    84,
    86,
    92,
    93,
    96,
    112,
    120,
    127,
)

# Primitive positive integer null vector in SUPPORT_INDICES order.
GORDAN_WEIGHTS = (
    709774956900548220167874366471210809228254829294056250386842637577041904422018780,
    1824717508559842145867532142832644519598008270801432516601647286190353292417650934,
    94757698514344823883773645768228490969858491834845115866744071071744088588791452,
    1113775451711576837765289548681535530959473216936152709260683717917866459190373680,
    1434690600592807707957913926684027143742657714160820297412607667717829151876566952,
    345125680096767207734776330700985162593421437183759784858659174008006702671124170,
    657639141215098080548389749999098840665695635611437004357519154114540258667392478,
    4374809951756209511418267428701551576006672002520466452143939381630214278117786788,
    83509681277432861066680674008785337807834433054726278750466931099968113989424452,
    213181330960466824356388600684498814224231519165566381010491457947553679920983136,
    2673898015883137636444993755429206021220674309922960558984026626987085549922432172,
    531644701958360069427649342422404990536706136289018955736662762351714425996340228,
    8809501773220772930731021283307182086782974616024272200535352580388457271338413136,
    4753257649536554763683197802301340387764709572238454806745042153694012122458141358,
    2151253905985577779609735378676270107731460378404324515180060510433758611598438278,
    25987604040491746868812279587502794865933862887542025595985001852514869073293527388,
    2187314934231794350091228298321004006677879643357194417060256737117313089394987284,
    181752138780764192553824210017572895336946366412446746460807286656878768404505736,
    2936529844908505273424449608103370314299036959361594958872739711716583275895504506,
    2245492352020462984983627664827841594180509142200683381079536855829466950506491904,
    2071951476988926370203188010964163236700740608445309193370230134828619889394551842,
    917641686084428835769400092700871486245522122358116342360550624805217797655642530,
    5812092683111847974259028706140369351468160173848859084377461795718366505442778728,
    9280956007874965654511967662363611214751148021697134929098726426357412417620425200,
    87323577054519614175412812585814558391377517149205781160183001552173117600953562,
    76062709248234335760112305351508779641788375363401332529483961356354030488755237,
)

EXPECTED_SLICE_SUPPORT = (
    (0, 50, 3),
    (1, 20, 2),
    (1, 36, 2),
    (1, 24, 2),
    (1, 49, 3),
    (1, 44, 3),
    (2, 41, 3),
    (2, 50, 3),
    (2, 56, 3),
    (3, 5, 2),
    (3, 34, 2),
    (3, 20, 2),
    (3, 7, 3),
    (3, 19, 3),
    (3, 35, 3),
    (3, 22, 3),
    (3, 52, 3),
    (4, 9, 2),
    (4, 6, 2),
    (4, 34, 2),
    (4, 35, 3),
    (4, 13, 3),
    (4, 14, 3),
    (5, 19, 3),
)
EXPECTED_CUT_SUPPORT = ((0, 15, 51, 60), (7, 8, 52, 59))


def tangent_columns() -> tuple[tuple[int, ...], ...]:
    factors = tuple(
        base.affine_coefficients(row) for row in base.DENOMINATORS
    )
    columns = []
    for omitted in range(4):
        product = (1,) + (0,) * (base.VERTICES - 1)
        for head, factor in enumerate(factors):
            if head != omitted:
                product = base.xor_convolution(product, factor)
        columns.append(product)
        columns.extend(
            tuple(product[mask ^ (1 << coordinate)] for mask in range(64))
            for coordinate in range(base.N)
        )
    return tuple(columns)


def middle_rows() -> tuple[
    tuple[tuple[int, ...], ...], tuple[tuple[str, int, int, int], ...]
]:
    rows = []
    labels = []
    for coordinate, (exceptional, slice_sign) in enumerate(
        base.unique_slice_data()
    ):
        remaining = tuple(
            index for index in range(base.N) if index != coordinate
        )
        for degree in (2, 3):
            for subset_tuple in itertools.combinations(remaining, degree):
                subset = sum(1 << index for index in subset_tuple)
                row = [0] * base.VERTICES
                row[subset] = base.character(subset, exceptional)
                row[subset | (1 << coordinate)] = (
                    row[subset] * slice_sign
                )
                rows.append(tuple(row))
                labels.append(("slice", coordinate, subset, degree))
    return tuple(rows), tuple(labels)


def quotient_cut_rows() -> tuple[
    tuple[tuple[int, ...], ...], tuple[tuple[str, tuple[int, ...]], ...]
]:
    subspace = {0, 51, 60, 51 ^ 60}
    exceptional_plane = {21 ^ value for value in subspace}
    unseen = set(range(base.VERTICES))
    rows = []
    labels = []
    while unseen:
        representative = min(unseen)
        current = tuple(
            sorted(representative ^ value for value in subspace)
        )
        unseen.difference_update(current)
        if set(current) == exceptional_plane:
            continue
        row = tuple(
            sum(
                base.character((base.VERTICES - 1) ^ mask, code)
                for code in current
            )
            for mask in range(base.VERTICES)
        )
        rows.append(row)
        labels.append(("cut", current))
    return tuple(rows), tuple(labels)


def verify() -> None:
    base.verify()
    middle, middle_labels = middle_rows()
    cuts, cut_labels = quotient_cut_rows()
    assert len(middle) == MIDDLE_ROW_COUNT
    assert len(cuts) == CUT_ROW_COUNT
    rows = middle + cuts
    labels = middle_labels + cut_labels

    supported_labels = tuple(labels[index] for index in SUPPORT_INDICES)
    assert tuple(label[1:] for label in supported_labels[:24]) == (
        EXPECTED_SLICE_SUPPORT
    )
    assert tuple(label[1] for label in supported_labels[24:]) == (
        EXPECTED_CUT_SUPPORT
    )

    assert len(GORDAN_WEIGHTS) == len(SUPPORT_INDICES) == 26
    assert all(weight > 0 for weight in GORDAN_WEIGHTS)
    assert math.gcd(*GORDAN_WEIGHTS) == 1

    columns = tangent_columns()
    assert len(columns) == 28
    for column in columns:
        pulled_values = tuple(
            sum(row[mask] * column[mask] for mask in range(base.VERTICES))
            for row in rows
        )
        moment = sum(
            weight * pulled_values[index]
            for index, weight in zip(SUPPORT_INDICES, GORDAN_WEIGHTS)
        )
        assert moment == 0

    endpoint_subgroup = {
        mask
        for mask in range(base.VERTICES)
        if all(
            bin(mask & value).count("1") % 2 == 0
            for value in (51, 60)
        )
    }
    expected_endpoints = {
        0,
        3,
        12,
        15,
        48,
        51,
        60,
        21,
        22,
        25,
        26,
        37,
        38,
        41,
        42,
        63,
    }
    assert endpoint_subgroup == expected_endpoints
    assert all(
        value == 0 or mask in endpoint_subgroup
        for row in cuts
        for mask, value in enumerate(row)
    )


def main() -> None:
    verify()
    print(f"middle rows: {MIDDLE_ROW_COUNT}")
    print(f"quotient-cut rows: {CUT_ROW_COUNT}")
    print(f"positive circuit support: {len(SUPPORT_INDICES)}")
    print("supported slice rows: 24")
    print(f"supported cut cosets: {EXPECTED_CUT_SUPPORT}")
    print(f"largest weight digits: {max(len(str(value)) for value in GORDAN_WEIGHTS)}")
    print("exact pulled-back Gordan relation: verified")


if __name__ == "__main__":
    main()
