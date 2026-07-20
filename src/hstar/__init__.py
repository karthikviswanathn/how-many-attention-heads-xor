"""Experimental utilities for head-complexity searches."""

from .config import SearchConfig, TrainingConfig
from .certified import estimate_certified_hstar


def estimate_h_star(*args, **kwargs):
    """Load the optional Torch training path only when it is requested."""
    from .search import estimate_h_star as implementation

    return implementation(*args, **kwargs)


def run_representative_search(*args, **kwargs):
    """Load the optional Torch training path only when it is requested."""
    from .search import run_representative_search as implementation

    return implementation(*args, **kwargs)

__all__ = [
    "SearchConfig",
    "TrainingConfig",
    "estimate_certified_hstar",
    "estimate_h_star",
    "run_representative_search",
]
