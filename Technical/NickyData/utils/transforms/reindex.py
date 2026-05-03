"""Reindexing transformations for economic time-series data.

Reindexing rescales a series so that a chosen base year equals 100.
"""

from __future__ import annotations

import pandas as pd


def reindex(series: pd.Series, base_year: int) -> pd.Series:
    """Rescale *series* so that the value at *base_year* equals 100."""
    idx = _year_index(series)
    if base_year not in idx.values:
        raise KeyError(
            f"Base year {base_year} not found in series index.  "
            f"Available range: {idx.min()}\u2013{idx.max()}"
        )
    base_val = series[idx == base_year].iloc[0]
    if base_val == 0:
        raise ValueError(f"Base year {base_year} has value 0; cannot reindex.")
    return (series / base_val) * 100.0


def reindex_to_match(
    series: pd.Series,
    target: pd.Series,
    at_year: int,
) -> pd.Series:
    """Rescale *series* so its value at *at_year* matches *target* at the same year."""
    s_idx = _year_index(series)
    t_idx = _year_index(target)

    if at_year not in s_idx.values:
        raise KeyError(f"Year {at_year} not in source series.")
    if at_year not in t_idx.values:
        raise KeyError(f"Year {at_year} not in target series.")

    s_val = series[s_idx == at_year].iloc[0]
    t_val = target[t_idx == at_year].iloc[0]

    if s_val == 0:
        raise ValueError(f"Source value at {at_year} is 0; cannot reindex.")

    scale = t_val / s_val
    return series * scale


def _year_index(series: pd.Series) -> pd.Index:
    """Extract integer years from the series index."""
    if pd.api.types.is_datetime64_any_dtype(series.index):
        return series.index.year
    return series.index
