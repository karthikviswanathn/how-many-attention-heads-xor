#!/usr/bin/env python3
"""Verify an exact limit of the positive-cubic support54 ansatz.

The ansatz writes a support54 tangent multiplier as

    lambda(z) = D(z) q(z),

where D is the product of four positive affine denominators and q is a
Fourier polynomial of degree at most three that is positive on support54.

For one small integer denominator tuple, this file verifies two exact and
complementary certificates:

* an 18-point theorem-of-alternatives functional excludes every positive
  cubic q in the tangent kernel;
* a 23-point positive circuit annihilates the unrestricted tangent rows.

Thus the unrestricted support54 obstruction survives, but cubic q is not a
universal parameterization of it.
"""

from __future__ import annotations

from fractions import Fraction
import math


N = 6
FULL = (1 << N) - 1
MASK = 0x96696BD669B69669
OMITTED = frozenset((6, 9, 16, 21, 27, 36, 42, 47, 54, 57))
SUPPORT54 = tuple(code for code in range(1 << N) if code not in OMITTED)

DENOMINATORS = (
    (12, -2, -2, -1, -1, -2, -2),
    (10, -2, -1, -1, -1, -2, -1),
    (9, -1, -2, -2, -1, -1, -1),
    (11, 2, 2, 2, 1, 2, 1),
)

CUBIC_OBSTRUCTION_SUPPORT = (
    2, 5, 11, 14, 15, 19, 20, 25, 26,
    29, 30, 31, 35, 38, 40, 45, 50, 61,
)
CUBIC_OBSTRUCTION_WEIGHTS = (
    802595562101293972593845201550825827842391520,
    1175783545648287976321183066921163073889880640,
    2245484646137007472880079942442180008957141120,
    1839082319327361576289129720002240815376015840,
    1872326224113797630233972851379711165650441600,
    3840307735739513760698531412528231745323837600,
    405320677108910679067781862979721552379215040,
    5055982766032178099495017249096057621969553280,
    1149917180890071573661552631172827818781898240,
    719464478295917264962255768246517801702225280,
    1599587282056087210202123076222937467293537280,
    1819767883184525138776880913662851177229556000,
    2369875898069052367268368349246760850452934080,
    8404847075182837792634538953338514856842550720,
    3025973140667644398217291897349978137166907840,
    455874830168038991617511776427435945201996160,
    1274308432822116468049841037977408660277691200,
    5596295144344383075080918019684642077754729600,
)

# One multiplier for the global cleared column, followed by six multipliers
# for each of the four heads.
TANGENT_MULTIPLIERS = (
    86216930052784297393800601603267688514968,
    -14236862552211805636160437291078564674223080,
    -97261411682149164406273396658478389247018240,
    73736319978549353748284508605623694990894160,
    21446689804492340417430940713780470809628040,
    21325083804624885552876282965454083159826720,
    19326938701143505285371401720710483958747280,
    18097259001214777014456008698800449800914516,
    32870781427895790521866218033007827214414098,
    2455940711859168509327891203110150321355758,
    -19441974070005726218001967268213215966110702,
    -8651941676397194214060817393844695682383164,
    -20893270828713136096913235898342169885401662,
    -8253542894859225698449750205605991467545088,
    44093216065354294363838296407361909721201200,
    -54904624741848552186072158473576918595357360,
    6066105619894306577354767358104432016192810,
    -7826212382116621643639758349264057782740832,
    3498016552519666012969784699698717977612080,
    -1536189218884277727842361541983140748792888,
    -2456014232240512331778541938610827151490655,
    2134221589710343843396224586132012272842265,
    2301160573203010226389214930538654530530905,
    2291854109573089772392730539520738503895688,
    -1283732282209426168867701459005127423019455,
)

FREE_CIRCUIT_SUPPORT = (
    1, 2, 3, 11, 12, 14, 15, 17, 28, 30, 31, 32,
    33, 34, 35, 37, 48, 49, 50, 51, 60, 62, 63,
)
FREE_CIRCUIT_WEIGHTS = (
    2607388535259283780065600,
    1717463720489081063602950,
    1538353693705866812775000,
    210158908573721091364800,
    360628177110892180767200,
    441998477268026002414650,
    326490577372442216762325,
    855680293692905594130756,
    772949836893885638572620,
    785836718603366121051525,
    465333469360689199112150,
    5032982118830864609426400,
    3496870317462190205641335,
    2162946113490750521984820,
    1809227826509539905059850,
    210158908573721091364800,
    1692989756705923558258761,
    1891355120040996311956650,
    769836493057948608918150,
    821498915313954422760600,
    647278296997028833440150,
    520071799945186026739740,
    233411425727471736960600,
)


def character(mask: int, code: int) -> int:
    return -1 if bin(mask & code).count("1") % 2 else 1


def target_sign(code: int) -> int:
    return 1 if (MASK >> code) & 1 else -1


def denominator_values(code: int) -> tuple[int, ...]:
    return tuple(
        denominator[0]
        + sum(
            denominator[coordinate + 1]
            * character(1 << coordinate, code)
            for coordinate in range(N)
        )
        for denominator in DENOMINATORS
    )


def cleared_row(code: int) -> tuple[int, ...]:
    values = denominator_values(code)
    product = math.prod(values)
    sign = target_sign(code)
    return tuple(
        [sign * product]
        + [
            sign
            * character(1 << coordinate, code)
            * (product // values[head])
            for head in range(4)
            for coordinate in range(N)
        ]
    )


ROWS = {code: cleared_row(code) for code in SUPPORT54}
MONOMIALS3 = tuple(mask for mask in range(1 << N) if bin(mask).count("1") <= 3)
MONOMIALS2 = tuple(mask for mask in MONOMIALS3 if bin(mask).count("1") <= 2)
MONOMIALS4 = tuple(mask for mask in range(1 << N) if bin(mask).count("1") <= 4)
QUARTIC_ACTIVE_VERTICES = (
    0, 4, 5, 10, 11, 17, 18, 20, 22, 25, 26, 29, 30, 31,
    32, 37, 39, 40, 41, 45, 46, 48, 52, 53, 56, 58, 62, 63,
)
QUARTIC_ZERO_COEFFICIENTS = (20, 27, 42, 52)


def cubic_equation(column: int, mask: int) -> int:
    return sum(
        ROWS[code][column] * character(mask, code) for code in SUPPORT54
    )


def modular_rank(matrix: list[list[int]], prime: int = 1000003) -> int:
    work = [[value % prime for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        chosen = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column] % prime
            ),
            None,
        )
        if chosen is None:
            continue
        work[pivot_row], work[chosen] = work[chosen], work[pivot_row]
        inverse = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [value * inverse % prime for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                (left - multiplier * right) % prime
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def solve_square(matrix: list[list[Fraction]]) -> tuple[Fraction, ...]:
    size = len(matrix)
    assert all(len(row) == size + 1 for row in matrix)
    work = [row[:] for row in matrix]
    for column in range(size):
        chosen = next(
            row for row in range(column, size) if work[row][column]
        )
        work[column], work[chosen] = work[chosen], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[column])
            ]
    return tuple(work[row][-1] for row in range(size))


def verify() -> Fraction:
    assert len(SUPPORT54) == 54
    for head, denominator in enumerate(DENOMINATORS):
        orientation = -1 if head < 3 else 1
        assert all(orientation * value > 0 for value in denominator[1:])
        assert denominator[0] > sum(abs(value) for value in denominator[1:])
    assert all(min(denominator_values(code)) > 0 for code in range(1 << N))

    equations3 = [
        [cubic_equation(column, mask) for mask in MONOMIALS3]
        for column in range(25)
    ]
    equations2 = [row[: len(MONOMIALS2)] for row in equations3]
    assert modular_rank(equations3) == 25
    assert modular_rank(equations2) == len(MONOMIALS2) == 22

    assert len(CUBIC_OBSTRUCTION_SUPPORT) == len(CUBIC_OBSTRUCTION_WEIGHTS) == 18
    assert len(TANGENT_MULTIPLIERS) == 25
    assert all(weight > 0 for weight in CUBIC_OBSTRUCTION_WEIGHTS)
    for mask_index, mask in enumerate(MONOMIALS3):
        left = sum(
            weight * character(mask, code)
            for code, weight in zip(
                CUBIC_OBSTRUCTION_SUPPORT, CUBIC_OBSTRUCTION_WEIGHTS
            )
        )
        right = sum(
            multiplier * equations3[column][mask_index]
            for column, multiplier in enumerate(TANGENT_MULTIPLIERS)
        )
        assert left == right

    assert len(FREE_CIRCUIT_SUPPORT) == len(FREE_CIRCUIT_WEIGHTS) == 23
    assert all(weight > 0 for weight in FREE_CIRCUIT_WEIGHTS)
    for column in range(25):
        assert sum(
            weight * ROWS[code][column]
            for code, weight in zip(FREE_CIRCUIT_SUPPORT, FREE_CIRCUIT_WEIGHTS)
        ) == 0

    obstruction = dict(zip(CUBIC_OBSTRUCTION_SUPPORT, CUBIC_OBSTRUCTION_WEIGHTS))
    free = dict(zip(FREE_CIRCUIT_SUPPORT, FREE_CIRCUIT_WEIGHTS))
    pairing = sum(
        Fraction(obstruction[code] * free[code], math.prod(denominator_values(code)))
        for code in set(obstruction) & set(free)
    )
    assert pairing > 0

    evaluation4 = [
        [character(mask, code) for mask in MONOMIALS4]
        for code in SUPPORT54
    ]
    assert len(MONOMIALS4) == 57
    assert modular_rank(evaluation4) == 53

    # The numerical discovery LP selected 28 tight vertex inequalities and
    # four zero coefficient gauges.  Solving those 57 rational equations
    # gives an exact quartic q with q >= 1 throughout support54.
    quartic_system = []
    for column in range(25):
        quartic_system.append(
            [Fraction(cubic_equation(column, mask)) for mask in MONOMIALS4]
            + [Fraction(0)]
        )
    for code in QUARTIC_ACTIVE_VERTICES:
        quartic_system.append(
            [Fraction(character(mask, code)) for mask in MONOMIALS4]
            + [Fraction(1)]
        )
    for coefficient in QUARTIC_ZERO_COEFFICIENTS:
        quartic_system.append(
            [
                Fraction(int(index == coefficient))
                for index in range(len(MONOMIALS4))
            ]
            + [Fraction(0)]
        )
    quartic = solve_square(quartic_system)
    assert all(
        sum(
            coefficient * cubic_equation(column, mask)
            for coefficient, mask in zip(quartic, MONOMIALS4)
        )
        == 0
        for column in range(25)
    )
    quartic_values = tuple(
        sum(
            coefficient * character(mask, code)
            for coefficient, mask in zip(quartic, MONOMIALS4)
        )
        for code in SUPPORT54
    )
    assert min(quartic_values) == 1
    assert all(value >= 1 for value in quartic_values)
    return pairing


def main() -> None:
    pairing = verify()
    print("cubic equation rank: 25 of 42")
    print("quadratic equation rank: 22 of 22")
    print("positive cubic-obstruction support: 18")
    print("positive unrestricted circuit support: 23")
    print("quartic evaluation rank on support54: 53 of 54")
    print("exact positive quartic kernel certificate: verified")
    print(f"positive obstruction pairing numerator digits: {len(str(pairing.numerator))}")
    print("verified positive-cubic ansatz limitation")


if __name__ == "__main__":
    main()
