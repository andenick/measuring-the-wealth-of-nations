"""Validation utilities for checking constructed series against references."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class RefCheckResult:
    """Outcome of a single reference-value check."""

    year: int
    expected: float
    actual: float
    abs_error: float
    rel_error: float
    within_tolerance: bool


def validate_reference(
    series: pd.Series,
    ref_values: dict[int, float],
    tolerance: float = 0.01,
) -> list[RefCheckResult]:
    """Compare *series* against known reference values.

    Parameters
    ----------
    series : pd.Series
        Constructed series (index should contain integer years).
    ref_values : dict[int, float]
        ``{year: expected_value}`` pairs.
    tolerance : float
        Maximum acceptable relative error (default 1 %).
    """
    results: list[RefCheckResult] = []
    idx = series.index

    for year, expected in sorted(ref_values.items()):
        if expected is None:
            continue
        if year not in idx:
            results.append(
                RefCheckResult(year, expected, float("nan"), float("nan"), float("nan"), False)
            )
            continue

        actual = float(series[year])
        abs_err = abs(actual - expected)
        rel_err = abs_err / abs(expected) if expected != 0 else float("inf")
        results.append(
            RefCheckResult(year, expected, actual, abs_err, rel_err, rel_err <= tolerance)
        )

    return results


def validate_range(
    series: pd.Series,
    min_val: float,
    max_val: float,
) -> bool:
    """Return ``True`` if every value in *series* is within [min_val, max_val]."""
    return bool((series >= min_val).all() and (series <= max_val).all())


def validate_transition(
    series_a: pd.Series,
    series_b: pd.Series,
    at_year: int,
) -> dict[str, Any]:
    """Check that two series join smoothly at *at_year*."""
    a_val = _get(series_a, at_year)
    b_val = _get(series_b, at_year)

    abs_diff = abs(a_val - b_val)
    rel_diff = abs_diff / abs(a_val) if a_val != 0 else float("inf")

    return {
        "year": at_year,
        "a_value": a_val,
        "b_value": b_val,
        "abs_difference": abs_diff,
        "rel_difference": rel_diff,
        "smooth": rel_diff < 0.01,
    }


def _get(s: pd.Series, year: int) -> float:
    if year not in s.index:
        raise KeyError(f"Year {year} not in series (range {s.index.min()}\u2013{s.index.max()}).")
    return float(s[year])
