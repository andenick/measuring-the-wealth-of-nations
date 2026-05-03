"""Splicing operations for combining overlapping time-series segments.

Three methods are supported:

* **growth_rate** -- use series_b's growth rates to extend series_a.
* **level_shift** -- shift series_b by the level difference at splice point.
* **direct** -- simply concatenate, preferring series_a in the overlap.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def splice(
    series_a: pd.Series,
    series_b: pd.Series,
    at_year: int,
    method: str = "growth_rate",
) -> pd.Series:
    """Splice two series at *at_year*.

    *series_a* is treated as the "preferred" series; *series_b* fills in
    where *series_a* has no coverage.
    """
    method = method.lower()
    if method == "growth_rate":
        return _splice_growth_rate(series_a, series_b, at_year)
    if method == "level_shift":
        return _splice_level_shift(series_a, series_b, at_year)
    if method == "direct":
        return _splice_direct(series_a, series_b)
    raise ValueError(f"Unknown splice method: '{method}'.  Use growth_rate | level_shift | direct.")


def _splice_growth_rate(a: pd.Series, b: pd.Series, at_year: int) -> pd.Series:
    """Extend *a* using *b*'s growth rates."""
    a_val = _val_at(a, at_year)
    b_val = _val_at(b, at_year)

    if b_val == 0:
        raise ValueError(f"series_b is 0 at splice year {at_year}; cannot compute growth rates.")

    scale = a_val / b_val
    b_scaled = b * scale

    combined = a.copy()
    for yr in b_scaled.index:
        if yr not in combined.index:
            combined[yr] = b_scaled[yr]
    return combined.sort_index()


def _splice_level_shift(a: pd.Series, b: pd.Series, at_year: int) -> pd.Series:
    """Shift *b* by the level difference at *at_year*."""
    a_val = _val_at(a, at_year)
    b_val = _val_at(b, at_year)
    shift = a_val - b_val

    combined = a.copy()
    for yr in b.index:
        if yr not in combined.index:
            combined[yr] = b[yr] + shift
    return combined.sort_index()


def _splice_direct(a: pd.Series, b: pd.Series) -> pd.Series:
    """Concatenate, preferring *a* in the overlap."""
    combined = a.copy()
    for yr in b.index:
        if yr not in combined.index:
            combined[yr] = b[yr]
    return combined.sort_index()


def _val_at(s: pd.Series, year: int) -> float:
    """Get the value of *s* at *year*, raising on miss."""
    idx = s.index
    if pd.api.types.is_datetime64_any_dtype(idx):
        mask = idx.year == year
    else:
        mask = idx == year

    matches = s[mask]
    if matches.empty:
        raise KeyError(f"Year {year} not found in series (range {idx.min()}\u2013{idx.max()}).")
    return float(matches.iloc[0])
