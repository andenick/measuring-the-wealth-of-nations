"""Read BEA cached CSV responses (ported from predecessor-build API_Data).

BEA's NIPA-style CSVs have columns:
  TableName, SeriesCode, LineNumber, LineDescription, TimePeriod (year),
  METRIC_NAME, CL_UNIT, UNIT_MULT, DataValue (string with commas), NoteRef

DataValue is a string like "126,977" — strip commas and convert to float.
UNIT_MULT=6 means millions × 10^6 = billions (when multiplied), so the actual
value in billions current $ is DataValue / 1000 since DataValue is in millions.

This module is the read-from-cache fallback when the live BEA API is not
available. Live API client is in `bea.py` (Phase 1.C, deferred until API
key provisioned).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .paths import ROOT


BEA_CACHE = ROOT / "data" / "raw" / "bea"


def _parse_datavalue(v) -> float:
    """Strip thousands separators and convert to float."""
    if isinstance(v, float):
        return v
    s = str(v).replace(",", "").replace('"', "").strip()
    return float(s) if s and s != "..." else float("nan")


def load_bea_line(table_csv: str, line_number: int) -> pd.DataFrame:
    """Read a single line of a BEA NIPA-style cached table.

    Returns DataFrame: [year, value] in MILLIONS (the cache's native unit).
    Caller decides on conversion to billions etc.
    """
    path = BEA_CACHE / table_csv
    if not path.exists():
        raise FileNotFoundError(f"BEA cache file missing: {path}")
    df = pd.read_csv(path)
    sel = df[df["LineNumber"] == line_number]
    if sel.empty:
        raise ValueError(f"Line {line_number} not found in {table_csv}")
    out = pd.DataFrame({
        "year":  sel["TimePeriod"].astype(int).values,
        "value": [_parse_datavalue(v) for v in sel["DataValue"].values],
    }).sort_values("year").reset_index(drop=True)
    return out


def load_bea_line_summed(table_csv: str, line_numbers: list[int]) -> pd.DataFrame:
    """Sum across multiple lines of a BEA table, by year."""
    parts = [load_bea_line(table_csv, ln) for ln in line_numbers]
    merged = parts[0].rename(columns={"value": "L0"})
    for i, p in enumerate(parts[1:], start=1):
        merged = merged.merge(p.rename(columns={"value": f"L{i}"}), on="year")
    merged["value"] = sum(merged[f"L{i}"] for i in range(len(parts)))
    return merged[["year", "value"]].reset_index(drop=True)
