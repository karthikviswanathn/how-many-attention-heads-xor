#!/usr/bin/env python3
"""Search exact H3 shattering certificates for sampled circuit families.

A signed quadratic circuit C forces the target signs on C and leaves its
complement F free.  A fixed three-head score space shatters all extensions if
its restriction to F is surjective and its kernel on F contains a score with
the forced signs on C.

The three-head score space has dimension at most 16.  Consequently this
criterion is structurally impossible unless |F| <= 15, hence unless |C| = 17.
Even for |C| = 17, the family cannot be shattered if the forced parity twist
on C admits a weak affine separator, because such a separator produces a
threshold-degree-at-least-four extension.

This script samples support-17 circuit families modulo the symmetries that
preserve head complexity.  Exact positive dual weights decide which families
have no weak affine extension.  A differentiable search then proposes
denominators for those exact-degree-three-only families, and every hit is
rechecked with integer arithmetic.  Sampling and search misses are not
classification results.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import torch
from scipy.optimize import least_squares, linprog

import sample_n5_quadratic_circuit_orbits as circuits
import search_adversarial_low_dimension as core
import search_n5_cubic_exact_factorization as factorization
import search_n5_degree4_family_shattering as exact
import verify_n5_degree3_circuit_reduction as reduction


N = 5
HEADS = 3
WIDTH = N + 1
VERTICES = 1 << N
PRIME = 1_000_003
ORIENTATION_PATTERNS = (
    (-1, -1, -1),
    (-1, -1, 1),
    (-1, 1, 1),
    (1, 1, 1),
)
ROUNDING_SCALES = (
    30,
    100,
    300,
    1_000,
    3_000,
    10_000,
    100_000,
    1_000_000,
    10_000_000,
)


def sampled_support17_orbits(samples: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    integer_features = reduction.quadratic_fourier_features()
    features = integer_features.astype(float)
    parity = np.prod(reduction.sign_cube(), axis=1)
    automorphisms = circuits.head_symmetry_automorphisms()
    representatives: dict[int, np.ndarray] = {}
    accepted = 0
    while accepted < samples:
        zero = np.sort(rng.choice(VERTICES, size=15, replace=False))
        _, singular, right = np.linalg.svd(
            features[zero], full_matrices=True
        )
        if singular[-1] < 1e-9:
            continue
        quadratic = features @ right[-1]
        scale = max(1.0, float(np.max(np.abs(quadratic))))
        zero_mask = np.abs(quadratic) < 1e-8 * scale
        if reduction.modular_rank(integer_features[zero_mask]) != 15:
            continue
        signs = np.zeros(VERTICES, dtype=np.int8)
        signs[~zero_mask] = (
            parity[~zero_mask] * np.sign(quadratic[~zero_mask])
        ).astype(np.int8)
        support_size = int(np.count_nonzero(signs))
        if not 8 <= support_size <= 17:
            continue
        if support_size == 17:
            key = circuits.canonical_key(signs, automorphisms)
            representatives.setdefault(key, signs.copy())
        accepted += 1

    answer = []
    for key in sorted(representatives):
        signs = representatives[key]
        dependency = circuits.exact_dependency(signs, integer_features)
        answer.append(np.sign(dependency).astype(np.int8))
    return answer


def exact_positive_null_vector(matrix: np.ndarray) -> np.ndarray | None:
    """Find an exact strictly positive vector in the right nullspace."""
    kernel = exact.integer_nullspace_basis(matrix.astype(object))
    if kernel.shape[1] == 0:
        return None
    separator = exact.exact_integer_separator_all_columns(
        np.ones(kernel.shape[0], dtype=np.int64), kernel
    )
    if separator is None:
        return None
    vector = kernel @ separator[0]
    assert np.all(vector > 0)
    assert np.all(matrix.astype(object) @ vector == 0)
    return vector


def rationalize_affine_separator(
    values: np.ndarray, signed_features: np.ndarray
) -> np.ndarray | None:
    for maximum_denominator in (10, 100, 1_000, 10_000, 1_000_000):
        rationals = [
            Fraction(float(value)).limit_denominator(maximum_denominator)
            for value in values
        ]
        denominator_lcm = 1
        for value in rationals:
            denominator_lcm = math.lcm(
                denominator_lcm, value.denominator
            )
        integers = np.array(
            [int(value * denominator_lcm) for value in rationals],
            dtype=object,
        )
        common = 0
        for value in integers:
            common = math.gcd(common, abs(int(value)))
        if common > 1:
            integers //= common
        products = signed_features.astype(object) @ integers
        if max(products) > 0 and min(products) >= 0:
            return integers
    return None


def exact_affine_extension_dichotomy(
    circuit_signs: np.ndarray,
) -> dict[str, object]:
    support = np.flatnonzero(circuit_signs)
    parity = np.prod(reduction.sign_cube(), axis=1)
    twisted = circuit_signs[support].astype(np.int64) * parity[support]
    affine = np.column_stack(
        [np.ones(VERTICES, dtype=np.int64), reduction.sign_cube()]
    )
    signed_features = twisted[:, None] * affine[support]
    assert reduction.modular_rank(signed_features) == WIDTH

    positive_dual = exact_positive_null_vector(signed_features.T)
    if positive_dual is not None:
        return {
            "affine_extendible": False,
            "positive_dual_weights": [int(value) for value in positive_dual],
        }

    objective = -np.sum(signed_features, axis=0).astype(float)
    result = linprog(
        objective,
        A_ub=-signed_features.astype(float),
        b_ub=np.zeros(len(support)),
        bounds=[(-1.0, 1.0)] * WIDTH,
        method="highs",
    )
    if not result.success or -float(result.fun) <= 1e-9:
        raise AssertionError("failed to realize the exact affine dichotomy")
    affine_separator = rationalize_affine_separator(
        result.x, signed_features
    )
    if affine_separator is None:
        raise AssertionError("failed to exactify a weak affine separator")
    return {
        "affine_extendible": True,
        "affine_separator": [int(value) for value in affine_separator],
    }


def valid_denominators(denominators: np.ndarray) -> bool:
    if denominators.shape != (HEADS, WIDTH):
        return False
    affine = core.affine_matrix(N).astype(object)
    values = affine @ denominators.astype(object).T
    return bool(
        np.all(values > 0)
        and all(
            np.all(row[1:] > 0) or np.all(row[1:] < 0)
            for row in denominators
        )
    )


def cleared_matrix(denominators: np.ndarray) -> np.ndarray:
    affine = core.affine_matrix(N).astype(object)
    values = affine @ denominators.astype(object).T
    full_product = np.prod(values, axis=1)
    columns = [full_product]
    for head in range(HEADS):
        other_product = np.prod(np.delete(values, head, axis=1), axis=1)
        columns.extend(
            affine[:, coordinate] * other_product
            for coordinate in range(WIDTH)
        )
    return np.column_stack(columns).astype(object)


def exact_shattering_certificate(
    circuit_signs: np.ndarray, denominators: np.ndarray
) -> dict[str, object] | None:
    if not valid_denominators(denominators):
        return None
    support = np.flatnonzero(circuit_signs)
    free = np.flatnonzero(circuit_signs == 0)
    if len(support) != 17 or len(free) != 15:
        return None
    matrix = cleared_matrix(denominators)
    if exact.modular_rank(matrix[free], PRIME) != len(free):
        return None
    kernel = exact.integer_nullspace_basis(matrix[free])
    kernel_values = matrix @ kernel
    assert np.all(kernel_values[free] == 0)
    if not any(
        any(int(value) != 0 for value in kernel_values[:, column])
        for column in range(kernel_values.shape[1])
    ):
        return None
    separator = exact.exact_integer_separator_all_columns(
        circuit_signs[support].astype(np.int64), kernel_values[support]
    )
    if separator is None:
        return None
    score_coefficients = kernel @ separator[0]
    score = matrix @ score_coefficients
    signed = circuit_signs[support].astype(object) * score[support]
    minimum = int(min(signed))
    assert minimum > 0
    assert np.all(score[free] == 0)
    return {
        "denominators": denominators.tolist(),
        "kernel_score_coefficients": [
            int(value) for value in score_coefficients
        ],
        "minimum_signed_support_score": minimum,
        "restriction_rank_prime": PRIME,
    }


def integer_denominators(
    literal_weights: np.ndarray,
    orientations: tuple[int, int, int],
    scale: int,
) -> np.ndarray:
    weights = np.maximum(1, np.rint(scale * literal_weights)).astype(
        np.int64
    )
    answer = []
    for head, orientation in enumerate(orientations):
        if orientation > 0:
            answer.append(weights[head])
        else:
            answer.append(
                np.concatenate(
                    [[int(np.sum(weights[head]))], -weights[head, 1:]]
                )
            )
    return np.vstack(answer)


def quantized_float_denominators(
    denominators: np.ndarray,
    orientations: tuple[int, int, int],
    scale: int,
) -> np.ndarray:
    answer = np.rint(scale * denominators).astype(np.int64)
    for head, orientation in enumerate(orientations):
        if orientation > 0:
            answer[head] = np.maximum(answer[head], 1)
        else:
            answer[head, 1:] = np.minimum(answer[head, 1:], -1)
            slope_sum = int(np.sum(np.abs(answer[head, 1:])))
            answer[head, 0] = max(int(answer[head, 0]), slope_sum + 1)
    assert valid_denominators(answer)
    return answer


def cubic_kernel_target(circuit_signs: np.ndarray) -> np.ndarray:
    support = np.flatnonzero(circuit_signs)
    free = np.flatnonzero(circuit_signs == 0)
    evaluation = core.monomial_matrix(N, 3).astype(float)
    result = linprog(
        np.zeros(evaluation.shape[1]),
        A_ub=-(circuit_signs[support, None] * evaluation[support]),
        b_ub=-np.ones(len(support)),
        A_eq=evaluation[free],
        b_eq=np.zeros(len(free)),
        bounds=[(None, None)] * evaluation.shape[1],
        method="highs",
    )
    if not result.success:
        raise AssertionError("exact-degree-three-only family lacks a cubic kernel score")
    target = evaluation @ result.x
    assert np.max(np.abs(target[free])) < 1e-8
    assert np.min(circuit_signs[support] * target[support]) > 1 - 1e-8
    return target / np.linalg.norm(target)


def factorization_search(
    circuit_signs: np.ndarray,
    seed: int,
    restarts: int,
    maximum_evaluations: int,
) -> tuple[dict[str, object] | None, dict[str, object]]:
    target = cubic_kernel_target(circuit_signs)
    rng = np.random.default_rng(seed)
    best_residual = float("inf")
    exact_attempts = 0
    for orientations in ORIENTATION_PATTERNS:
        for restart in range(restarts):
            initial = rng.normal(scale=2.0, size=HEADS * WIDTH)
            result = least_squares(
                factorization.projection_residual,
                initial,
                args=(orientations, target),
                max_nfev=maximum_evaluations,
                ftol=1e-12,
                xtol=1e-12,
                gtol=1e-12,
            )
            residual = float(np.linalg.norm(result.fun))
            best_residual = min(best_residual, residual)
            if residual > 1e-7:
                continue
            floating_denominators = factorization.denominators_from_logits(
                result.x, orientations
            )
            for scale in ROUNDING_SCALES:
                denominators = quantized_float_denominators(
                    floating_denominators, orientations, scale
                )
                exact_attempts += 1
                certificate = exact_shattering_certificate(
                    circuit_signs, denominators
                )
                if certificate is None:
                    continue
                certificate.update(
                    {
                        "search_source": "cubic_kernel_factorization",
                        "orientations": list(orientations),
                        "restart": restart,
                        "rounding_scale": scale,
                        "factorization_residual": residual,
                    }
                )
                return certificate, {
                    "best_factorization_residual": best_residual,
                    "factorization_exact_attempts": exact_attempts,
                }
    return None, {
        "best_factorization_residual": best_residual,
        "factorization_exact_attempts": exact_attempts,
    }


def independent_ratio_features(
    literal_weights: torch.Tensor,
    orientations: tuple[int, int, int],
    inputs: torch.Tensor,
) -> torch.Tensor:
    denominators = []
    for head, orientation in enumerate(orientations):
        literals = inputs if orientation > 0 else 1.0 - inputs
        denominators.append(
            literal_weights[head, 0]
            + literals @ literal_weights[head, 1:]
        )
    columns = [torch.ones((VERTICES, 1), dtype=torch.float64)]
    columns.extend(
        inputs / denominators[head][:, None] for head in range(HEADS)
    )
    return torch.cat(columns, dim=1)


def numerical_kernel_margins(
    logits: torch.Tensor,
    orientations: tuple[int, int, int],
    inputs: torch.Tensor,
    support: torch.Tensor,
    free: torch.Tensor,
    forced: torch.Tensor,
    pivot: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    literal_weights = torch.softmax(logits, dim=1)
    features = independent_ratio_features(
        literal_weights, orientations, inputs
    )
    other_columns = [column for column in range(16) if column != pivot]
    coefficients = torch.linalg.solve(
        features[free][:, other_columns], -features[free][:, pivot]
    )
    null_vector = torch.zeros(16, dtype=torch.float64)
    null_vector[other_columns] = coefficients
    null_vector[pivot] = 1.0
    signed = forced * (features[support] @ null_vector)
    signed = signed / torch.sqrt(torch.mean(signed * signed) + 1e-24)
    orientation = torch.sign(torch.sum(signed)).detach()
    if float(orientation) == 0.0:
        orientation = torch.tensor(1.0, dtype=torch.float64)
    return orientation * signed, literal_weights


def search_one_family(
    circuit_signs: np.ndarray,
    seed: int,
    factorization_restarts: int,
    factorization_evaluations: int,
    restarts: int,
    steps: int,
) -> tuple[dict[str, object] | None, dict[str, object]]:
    factor_certificate, factor_statistics = factorization_search(
        circuit_signs,
        seed,
        factorization_restarts,
        factorization_evaluations,
    )
    if factor_certificate is not None:
        return factor_certificate, factor_statistics

    support_array = np.flatnonzero(circuit_signs)
    free_array = np.flatnonzero(circuit_signs == 0)
    inputs = torch.tensor(core.cube(N).astype(float), dtype=torch.float64)
    support = torch.tensor(support_array, dtype=torch.long)
    free = torch.tensor(free_array, dtype=torch.long)
    forced = torch.tensor(
        circuit_signs[support_array].astype(float), dtype=torch.float64
    )
    best_margin = float("-inf")
    exact_attempts = 0

    for orientation_index, orientations in enumerate(ORIENTATION_PATTERNS):
        for restart in range(restarts):
            generator = torch.Generator()
            generator.manual_seed(
                int(
                    np.random.SeedSequence(
                        [seed, orientation_index, restart]
                    ).generate_state(1)[0]
                )
            )
            logits = 2.0 * torch.randn(
                (HEADS, WIDTH), generator=generator, dtype=torch.float64
            )
            logits.requires_grad_()
            with torch.no_grad():
                initial_features = independent_ratio_features(
                    torch.softmax(logits, dim=1), orientations, inputs
                )
                _, _, right = torch.linalg.svd(
                    initial_features[free], full_matrices=True
                )
                pivot = int(torch.argmax(torch.abs(right[-1])))
            optimizer = torch.optim.Adam([logits], lr=0.03)
            final_weights = None
            final_margin = float("-inf")
            for _ in range(steps):
                optimizer.zero_grad()
                try:
                    margins, literal_weights = numerical_kernel_margins(
                        logits,
                        orientations,
                        inputs,
                        support,
                        free,
                        forced,
                        pivot,
                    )
                except torch.linalg.LinAlgError:
                    break
                loss = torch.mean(torch.nn.functional.softplus(-20 * margins))
                loss = loss + 1e-7 * torch.sum(logits * logits)
                loss.backward()
                optimizer.step()
                final_margin = float(torch.min(margins).detach())
                if final_margin > best_margin:
                    best_margin = final_margin
                if final_margin > 1e-4:
                    final_weights = literal_weights.detach().numpy()
                    break
            if final_weights is None:
                continue
            for scale in ROUNDING_SCALES:
                denominators = integer_denominators(
                    final_weights, orientations, scale
                )
                exact_attempts += 1
                certificate = exact_shattering_certificate(
                    circuit_signs, denominators
                )
                if certificate is None:
                    continue
                certificate.update(
                    {
                        "orientations": list(orientations),
                        "restart": restart,
                        "rounding_scale": scale,
                        "numerical_margin": final_margin,
                    }
                )
                certificate["search_source"] = "direct_kernel_optimization"
                return certificate, {
                    **factor_statistics,
                    "best_numerical_margin": best_margin,
                    "exact_attempts": exact_attempts,
                }
    return None, {
        **factor_statistics,
        "best_numerical_margin": best_margin,
        "exact_attempts": exact_attempts,
    }


def verify_record(record: dict[str, object]) -> None:
    circuit_signs = np.zeros(VERTICES, dtype=np.int8)
    support = np.array(record["support_vertices"], dtype=np.int64)
    circuit_signs[support] = np.array(
        record["support_signs"], dtype=np.int8
    )
    dependency = circuits.exact_dependency(
        circuit_signs, reduction.quadratic_fourier_features()
    )
    assert np.array_equal(np.sign(dependency), circuit_signs)
    dichotomy = exact_affine_extension_dichotomy(circuit_signs)
    assert not dichotomy["affine_extendible"]
    certificate = exact_shattering_certificate(
        circuit_signs, np.array(record["denominators"], dtype=np.int64)
    )
    assert certificate is not None
    assert certificate["minimum_signed_support_score"] == record[
        "minimum_signed_support_score"
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--factorization-restarts", type=int, default=4)
    parser.add_argument(
        "--factorization-evaluations", type=int, default=1_500
    )
    parser.add_argument("--restarts", type=int, default=6)
    parser.add_argument("--steps", type=int, default=1_200)
    parser.add_argument("--max-families", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    arguments = parser.parse_args()

    if arguments.verify_only:
        if arguments.output is None:
            raise ValueError("--verify-only requires --output")
        payload = json.loads(arguments.output.read_text())
        for record in payload["records"]:
            verify_record(record)
        print(
            f"verified {len(payload['records'])} exact H3 family certificates"
        )
        return

    representatives = sampled_support17_orbits(
        arguments.samples, arguments.seed
    )
    if arguments.max_families is not None:
        representatives = representatives[: arguments.max_families]
    records = []
    affine_extendible = []
    misses = []
    exact_degree_three_only = 0
    for orbit, circuit_signs in enumerate(representatives):
        support = np.flatnonzero(circuit_signs)
        dichotomy = exact_affine_extension_dichotomy(circuit_signs)
        common = {
            "orbit_index": orbit,
            "support_vertices": [int(value) for value in support],
            "support_signs": [int(circuit_signs[value]) for value in support],
        }
        if dichotomy["affine_extendible"]:
            common.update(dichotomy)
            affine_extendible.append(common)
            print(f"orbit={orbit} affine-extendible", flush=True)
            continue
        exact_degree_three_only += 1
        certificate, statistics = search_one_family(
            circuit_signs,
            arguments.seed ^ (orbit * 0x9E3779B1),
            arguments.factorization_restarts,
            arguments.factorization_evaluations,
            arguments.restarts,
            arguments.steps,
        )
        if certificate is None:
            common.update(dichotomy)
            common.update(statistics)
            misses.append(common)
            print(
                f"orbit={orbit} exact-degree-three-only miss "
                f"best={statistics['best_numerical_margin']}",
                flush=True,
            )
            continue
        common.update(dichotomy)
        common.update(certificate)
        records.append(common)
        print(
            f"orbit={orbit} exact H3 family hit "
            f"orientation={certificate['orientations']} "
            f"restart={certificate['restart']} "
            f"scale={certificate['rounding_scale']}",
            flush=True,
        )

    payload = {
        "status": (
            "Every listed hit is an exact fixed-space shattering "
            "certificate. Sampling and search misses are not classification "
            "results."
        ),
        "samples": arguments.samples,
        "seed": arguments.seed,
        "factorization_restarts": arguments.factorization_restarts,
        "factorization_evaluations": arguments.factorization_evaluations,
        "restarts": arguments.restarts,
        "steps": arguments.steps,
        "sampled_support17_orbits": len(representatives),
        "affine_extendible_families": len(affine_extendible),
        "exact_degree_three_only_families": exact_degree_three_only,
        "exact_h3_shattered_families": len(records),
        "records": records,
        "affine_extendible": affine_extendible,
        "misses": misses,
    }
    for record in records:
        verify_record(record)
    print(
        f"support17={len(representatives)} "
        f"affine_extendible={len(affine_extendible)} "
        f"degree3_only={exact_degree_three_only} "
        f"exact_h3_shattered={len(records)} misses={len(misses)}",
        flush=True,
    )
    if arguments.output is not None:
        arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
        print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
