from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


def is_constant(truth_table: np.ndarray) -> bool:
    return bool(np.all(truth_table == truth_table[0]))


def is_linear_threshold(inputs: np.ndarray, truth_table: np.ndarray) -> bool:
    """Check linear-threshold representability exactly via LP feasibility."""
    signs = np.where(truth_table > 0.5, 1.0, -1.0)
    augmented_inputs = np.concatenate(
        [inputs, np.ones((inputs.shape[0], 1), dtype=np.float64)], axis=1
    )
    a_ub = -(signs[:, None] * augmented_inputs)
    b_ub = -np.ones(inputs.shape[0], dtype=np.float64)
    objective = np.zeros(inputs.shape[1] + 1, dtype=np.float64)

    result = linprog(
        c=objective,
        A_ub=a_ub,
        b_ub=b_ub,
        bounds=[(None, None)] * (inputs.shape[1] + 1),
        method="highs",
    )
    return bool(result.success)
