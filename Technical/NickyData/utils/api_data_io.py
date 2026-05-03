"""Parsers for pre-downloaded API data files (BEA, BLS, FRED).

No network calls — all data already exists in Inputs/API_Data/.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger("api_data_io")


def load_bea_nipa(filepath: str | Path, line_filter: str | list[str] | None = None) -> pd.DataFrame:
    """Load a BEA NIPA long-format CSV into a year-indexed DataFrame.

    Handles the 10-column BEA format: strips commas from DataValue,
    applies UNIT_MULT scaling, and pivots by TimePeriod.

    Parameters
    ----------
    filepath : path to the BEA CSV
    line_filter : if given, keep only rows where LineDescription matches
                  (string or list of strings)
    """
    filepath = Path(filepath)
    df = pd.read_csv(filepath, dtype={"DataValue": str, "UNIT_MULT": str})

    # Clean DataValue: strip commas and quotes, convert to float
    df["DataValue"] = df["DataValue"].str.replace(",", "", regex=False)
    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")

    # Apply UNIT_MULT scaling (usually 6 = millions)
    df["UNIT_MULT"] = pd.to_numeric(df["UNIT_MULT"], errors="coerce").fillna(0)
    df["scaled_value"] = df["DataValue"] * (10 ** df["UNIT_MULT"])

    # Convert TimePeriod to integer year
    df["year"] = pd.to_numeric(df["TimePeriod"], errors="coerce")
    df = df[df["year"].notna()]
    df["year"] = df["year"].astype(int)

    # Optional line filter
    if line_filter is not None:
        if isinstance(line_filter, str):
            line_filter = [line_filter]
        df = df[df["LineDescription"].isin(line_filter)]

    # Pivot: rows=year, columns=LineDescription, values=scaled_value
    if df["LineDescription"].nunique() == 1:
        result = df.set_index("year")[["scaled_value"]].copy()
        result.columns = [df["LineDescription"].iloc[0]]
    else:
        result = df.pivot_table(index="year", columns="LineDescription",
                                values="scaled_value", aggfunc="first")

    result = result.sort_index()
    return result


def load_bls_csv(filepath: str | Path) -> pd.DataFrame:
    """Load a BLS CES year-indexed CSV directly."""
    filepath = Path(filepath)
    df = pd.read_csv(filepath, index_col=0)
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index = df.index.astype(int)
    df.index.name = "year"
    return df.sort_index()


def load_fred_csv(filepath: str | Path) -> pd.Series:
    """Load a 3-column (date, year, value) FRED export as a year-indexed Series."""
    filepath = Path(filepath)
    df = pd.read_csv(filepath)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df[df["year"].notna()]
    df["year"] = df["year"].astype(int)
    s = df.set_index("year")["value"]
    s = s.sort_index()
    s.name = filepath.stem
    return s
