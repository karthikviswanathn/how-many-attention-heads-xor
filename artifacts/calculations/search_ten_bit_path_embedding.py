#!/usr/bin/env python3
"""Search for a ten-bit quadratic embedding of the compact path obstruction.

The 35 target row signs are the exact path-hitting codes used by the eleven-bit
separation.  Six x bits encode the 35 rows.  This search samples injections of
the eight sign coordinates into the four-bit y cube and asks whether one
quadratic polynomial in (x,y) realizes all 280 selected signs.  A success is
rounded and verified with exact integer arithmetic.  A failure is only search
evidence.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Optional

import numpy as np
from scipy.optimize import linear_sum_assignment, minimize

import search_adversarial_low_dimension as core


X_BITS = 6
Y_BITS = 4
TOTAL_BITS = X_BITS + Y_BITS
ROW_CODES = (
    0,
    3,
    5,
    10,
    12,
    15,
    18,
    20,
    23,
    30,
    34,
    36,
    39,
    46,
    54,
    65,
    72,
    75,
    77,
    80,
    83,
    85,
    90,
    92,
    95,
    96,
    99,
    101,
    106,
    108,
    111,
    114,
    116,
    119,
    126,
)


def bits(value: int, width: int) -> tuple[int, ...]:
    return tuple((value >> index) & 1 for index in range(width))


def feature_rows(inputs: np.ndarray) -> np.ndarray:
    columns = [np.ones(len(inputs), dtype=np.int64)]
    columns.extend(inputs[:, index] for index in range(TOTAL_BITS))
    columns.extend(
        inputs[:, first] * inputs[:, second]
        for first, second in combinations(range(TOTAL_BITS), 2)
    )
    return np.column_stack(columns)


def target_signs() -> np.ndarray:
    return np.array(
        [
            [-1 if (row_code >> coordinate) & 1 else 1 for coordinate in range(8)]
            for row_code in ROW_CODES
        ],
        dtype=np.int64,
    )


def selected_system(
    y_codes: tuple[int, ...],
    x_codes: Optional[tuple[int, ...]] = None,
) -> tuple[np.ndarray, np.ndarray]:
    if x_codes is None:
        x_codes = tuple(row_code & 63 for row_code in ROW_CODES)
    rows = []
    signs = []
    for row_index, x_code in enumerate(x_codes):
        x = bits(x_code, X_BITS)
        for coordinate, y_code in enumerate(y_codes):
            rows.append(x + bits(y_code, Y_BITS))
            signs.append(target_signs()[row_index, coordinate])

    inputs = np.array(rows, dtype=np.int64)
    return np.array(signs, dtype=np.int64), feature_rows(inputs)


def all_pair_scores(
    x_codes: tuple[int, ...], y_codes: tuple[int, ...], coefficients: np.ndarray
) -> np.ndarray:
    rows = [
        bits(x_code, X_BITS) + bits(y_code, Y_BITS)
        for x_code in x_codes
        for y_code in y_codes
    ]
    values = feature_rows(np.array(rows, dtype=np.int64)).astype(float) @ coefficients
    return values.reshape(len(x_codes), len(y_codes))


def logistic_fit(
    signs: np.ndarray,
    matrix: np.ndarray,
    initial: np.ndarray,
    regularization: float,
) -> np.ndarray:
    signed_matrix = signs[:, None] * matrix.astype(float)

    def objective(coefficients: np.ndarray) -> tuple[float, np.ndarray]:
        margins = signed_matrix @ coefficients
        loss = float(np.mean(np.logaddexp(0.0, -margins)))
        loss += 0.5 * regularization * float(coefficients @ coefficients)
        weights = -1.0 / (1.0 + np.exp(np.clip(margins, -60.0, 60.0)))
        gradient = signed_matrix.T @ weights / len(margins)
        gradient += regularization * coefficients
        return loss, gradient

    result = minimize(
        objective,
        initial,
        jac=True,
        method="L-BFGS-B",
        options={"maxiter": 1000, "ftol": 1e-14, "gtol": 1e-10},
    )
    return np.array(result.x)


def alternating_search(
    restarts: int, iterations: int, rng: np.random.Generator
) -> Optional[dict[str, object]]:
    targets = target_signs()
    all_x = tuple(range(1 << X_BITS))
    all_y = tuple(range(1 << Y_BITS))
    coefficient_count = 1 + TOTAL_BITS + TOTAL_BITS * (TOTAL_BITS - 1) // 2

    for restart in range(restarts):
        if restart == 0:
            x_codes = tuple(row_code & 63 for row_code in ROW_CODES)
        else:
            x_codes = tuple(int(value) for value in rng.choice(64, size=35, replace=False))
        y_codes = tuple(int(value) for value in rng.choice(16, size=8, replace=False))
        coefficients = rng.normal(scale=0.1, size=coefficient_count)

        for iteration in range(iterations):
            signs, matrix = selected_system(y_codes, x_codes)
            regularization = 10.0 ** (-3.0 - 4.0 * iteration / max(1, iterations - 1))
            coefficients = logistic_fit(
                signs, matrix, coefficients, regularization
            )
            signed_values = signs * (matrix.astype(float) @ coefficients)
            accuracy = int(np.sum(signed_values > 0))
            if accuracy == len(signs):
                exact = core.exact_integer_separator(signs, matrix)
                if exact is not None:
                    integers, normalized_margin = exact
                    exact_signed = signs.astype(object) * (
                        matrix.astype(object) @ integers
                    )
                    return {
                        "method": "alternating-matching",
                        "restart": restart,
                        "iteration": iteration,
                        "selected_x_codes": list(x_codes),
                        "selected_y_codes": list(y_codes),
                        "quadratic_coefficients": [int(value) for value in integers],
                        "minimum_signed_selected_value": int(min(exact_signed)),
                        "normalized_margin": normalized_margin,
                    }

            row_scores = all_pair_scores(all_x, y_codes, coefficients)
            row_cost = np.empty((len(ROW_CODES), len(all_x)))
            for target_index in range(len(ROW_CODES)):
                margins = targets[target_index][None, :] * row_scores
                row_cost[target_index] = np.sum(
                    np.logaddexp(0.0, -margins), axis=1
                )
            row_indices, x_assignment = linear_sum_assignment(row_cost)
            assert tuple(row_indices) == tuple(range(len(ROW_CODES)))
            x_codes = tuple(int(value) for value in x_assignment)

            column_scores = all_pair_scores(x_codes, all_y, coefficients)
            column_cost = np.empty((8, len(all_y)))
            for coordinate in range(8):
                margins = targets[:, coordinate][:, None] * column_scores
                column_cost[coordinate] = np.sum(
                    np.logaddexp(0.0, -margins), axis=0
                )
            column_indices, y_assignment = linear_sum_assignment(column_cost)
            assert tuple(column_indices) == tuple(range(8))
            y_codes = tuple(int(value) for value in y_assignment)

            if iteration % 10 == 0:
                print(
                    f"restart {restart} iteration {iteration}: "
                    f"accuracy={accuracy}/{len(signs)}",
                    flush=True,
                )
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--alternating-restarts", type=int, default=0)
    parser.add_argument("--alternating-iterations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent
        / "ten_bit_path_embedding_search.json",
    )
    arguments = parser.parse_args()
    rng = np.random.default_rng(arguments.seed)

    tested = set()
    result_record = None
    if arguments.alternating_restarts:
        result_record = alternating_search(
            arguments.alternating_restarts,
            arguments.alternating_iterations,
            rng,
        )
    else:
        for trial in range(1, arguments.trials + 1):
            y_codes = tuple(int(value) for value in rng.choice(16, size=8, replace=False))
            if y_codes in tested:
                continue
            tested.add(y_codes)
            signs, matrix = selected_system(y_codes)
            if not core.floating_separable(signs, matrix):
                if trial % 1000 == 0:
                    print(f"trial {trial}: no embedding", flush=True)
                continue
            exact = core.exact_integer_separator(signs, matrix)
            if exact is None:
                print(f"trial {trial}: floating-only candidate", flush=True)
                continue
            coefficients, normalized_margin = exact
            signed_values = signs.astype(object) * (
                matrix.astype(object) @ coefficients
            )
            result_record = {
                "method": "random-column-injection",
                "trial": trial,
                "selected_x_codes": [row_code & 63 for row_code in ROW_CODES],
                "selected_y_codes": list(y_codes),
                "quadratic_coefficients": [int(value) for value in coefficients],
                "minimum_signed_selected_value": int(min(signed_values)),
                "normalized_margin": normalized_margin,
            }
            print(json.dumps(result_record), flush=True)
            break

    payload = {
        "status": "Exact integer success, or numerical search failure only.",
        "x_bits": X_BITS,
        "y_bits": Y_BITS,
        "row_codes": list(ROW_CODES),
        "parameters": {
            "trials": arguments.trials,
            "alternating_restarts": arguments.alternating_restarts,
            "alternating_iterations": arguments.alternating_iterations,
            "seed": arguments.seed,
        },
        "tested_injections": len(tested),
        "result": result_record,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()
