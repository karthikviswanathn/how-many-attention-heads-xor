"""Exact Boolean-cube conventions used by certificate code.

Vertex ``code`` has coordinate ``i`` equal to bit ``i`` of ``code``.  Thus
coordinate zero is the least-significant bit and truth-mask bit ``code`` is
the value at that vertex.  This is the convention used by the exact artifacts
in this repository.  It intentionally differs from the legacy lexicographic
helpers in :mod:`hstar.truth_tables`.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np


VERTEX_ORDER = "integer-code-lsb-coordinate-0"


def cube(dimension: int, dtype: type = np.int64) -> np.ndarray:
    """Return all Boolean vertices in integer-code order."""
    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    codes = np.arange(1 << dimension, dtype=np.int64)
    points = (codes[:, None] >> np.arange(dimension, dtype=np.int64)) & 1
    return points.astype(dtype)


def affine_matrix(dimension: int, dtype: type = np.int64) -> np.ndarray:
    """Return rows ``(1, x_0, ..., x_{n-1})`` in integer-code order."""
    return np.column_stack(
        [np.ones(1 << dimension, dtype=np.int64), cube(dimension)]
    ).astype(dtype)


def validate_signs(signs: np.ndarray | list[int], dimension: int) -> np.ndarray:
    """Validate and return a sign vector with entries in ``{-1, +1}``."""
    result = np.asarray(signs, dtype=np.int64)
    if result.shape != (1 << dimension,):
        raise ValueError(f"expected {1 << dimension} signs")
    if not np.all((result == -1) | (result == 1)):
        raise ValueError("signs must all belong to {-1, +1}")
    return result


def signs_from_mask(mask: int, dimension: int) -> np.ndarray:
    """Decode a truth mask, where bit ``code`` is the positive-label bit."""
    if mask < 0 or mask >= 1 << (1 << dimension):
        raise ValueError("truth mask is outside the valid range")
    return np.array(
        [1 if (mask >> code) & 1 else -1 for code in range(1 << dimension)],
        dtype=np.int64,
    )


def mask_from_signs(signs: np.ndarray | list[int], dimension: int) -> int:
    """Encode signs in the repository truth-mask convention."""
    checked = validate_signs(signs, dimension)
    return sum(1 << code for code, sign in enumerate(checked) if sign > 0)


def signs_from_vertex_bitstring(text: str, dimension: int) -> np.ndarray:
    """Decode a string whose leftmost character is the value at vertex zero."""
    expected = 1 << dimension
    if len(text) != expected or any(character not in "01" for character in text):
        raise ValueError(f"bitstring must contain exactly {expected} binary digits")
    return np.array([1 if character == "1" else -1 for character in text], dtype=np.int64)


def monomial_subsets(dimension: int, degree: int) -> tuple[tuple[int, ...], ...]:
    """List squarefree monomials of degree at most ``degree``."""
    if not 0 <= degree <= dimension:
        raise ValueError("degree must belong to [0, dimension]")
    return tuple(
        subset
        for size in range(degree + 1)
        for subset in combinations(range(dimension), size)
    )


def monomial_matrix(
    dimension: int,
    degree: int,
    dtype: type = np.int64,
) -> tuple[np.ndarray, tuple[tuple[int, ...], ...]]:
    """Return the squarefree monomial evaluation matrix through ``degree``."""
    points = cube(dimension)
    subsets = monomial_subsets(dimension, degree)
    columns = []
    for subset in subsets:
        if not subset:
            columns.append(np.ones(1 << dimension, dtype=np.int64))
        else:
            columns.append(np.prod(points[:, subset], axis=1))
    return np.column_stack(columns).astype(dtype), subsets
