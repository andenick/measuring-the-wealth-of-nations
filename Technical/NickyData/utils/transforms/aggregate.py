"""Frequency-conversion helpers for time-series data."""

from __future__ import annotations

import pandas as pd


def monthly_to_annual(
    series: pd.Series,
    method: str = "average",
) -> pd.Series:
    """Convert a monthly series to annual frequency.

    Parameters
    ----------
    series : pd.Series
        Must have a ``DatetimeIndex`` at monthly (or finer) frequency.
    method : str
        ``"average"`` (default), ``"sum"``, or ``"last"``.

    Returns
    -------
    pd.Series
        Annual series indexed by integer year.
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError(
            "monthly_to_annual requires a DatetimeIndex.  "
            f"Got {type(series.index).__name__}."
        )

    grouped = series.groupby(series.index.year)

    if method == "average":
        result = grouped.mean()
    elif method == "sum":
        result = grouped.sum()
    elif method == "last":
        result = grouped.last()
    else:
        raise ValueError(
            f"Unknown aggregation method '{method}'.  Use average | sum | last."
        )

    result.index.name = "year"
    return result
