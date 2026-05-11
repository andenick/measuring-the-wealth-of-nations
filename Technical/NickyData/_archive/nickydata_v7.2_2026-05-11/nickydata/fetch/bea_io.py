"""BEA Input-Output benchmark table fetcher.

Fetches Use tables, Total Requirements tables, and Supply tables
for NAICS-era benchmarks (1997-2017) via BEA API.

SIC-era benchmarks (1947-1977) must be downloaded manually from
bea.gov/industry/historical-benchmark-input-output-tables and placed
in data/cache/io_sic/. The pipeline checks for these on startup.
"""

import json
import os
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"
SIC_DIR = CACHE_DIR / "io_sic"

NAICS_YEARS = [1997, 2002, 2007, 2012, 2017]

IO_TABLE_IDS = {
    "Use": 259,
    "Requirements": 262,
}


def _ensure_cache():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_naics_io(year: int, table_type: str, api_key: str) -> list[dict]:
    """Fetch a NAICS IO table from BEA API."""
    _ensure_cache()
    table_id = IO_TABLE_IDS.get(table_type, 259)
    cache = CACHE_DIR / f"bea_io_{table_type}_{year}.json"

    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "UserID": api_key,
            "method": "GetData",
            "DataSetName": "InputOutput",
            "TableID": str(table_id),
            "Year": str(year),
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    results = data.get("BEAAPI", {}).get("Results", [])
    if isinstance(results, list) and len(results) > 0:
        return results[0].get("Data", [])
    elif isinstance(results, dict):
        return results.get("Data", [])
    return []


def parse_use_matrix(records: list[dict]) -> tuple[pd.DataFrame, pd.Series]:
    """Parse Use table records into (A-matrix, gross_output)."""
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(), pd.Series(dtype=float)

    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")

    industry_codes = sorted(set(df["ColCode"]) - set(
        c for c in df["ColCode"] if c.startswith("F") or c.startswith("T") or c == ""
    ))

    commodity_rows = df[
        ~df["RowCode"].str.startswith("F") &
        ~df["RowCode"].str.startswith("T") &
        (df["RowCode"] != "")
    ]

    z = commodity_rows.pivot_table(
        index="RowCode", columns="ColCode", values="DataValue", aggfunc="first"
    ).fillna(0.0)
    z = z[[c for c in industry_codes if c in z.columns]]

    # T018 = "Total industry output (basic prices)" = gross output per industry
    # This is the correct denominator for the A-matrix computation
    x = pd.Series(dtype=float)
    for total_code in ["T018", "T005", "T00TOP"]:
        total_row = df[df["RowCode"] == total_code]
        if not total_row.empty:
            candidate = total_row.set_index("ColCode")["DataValue"]
            candidate = candidate[candidate.index.isin(industry_codes)]
            if candidate.sum() > 1e6:
                x = candidate
                break

    if x.empty or x.sum() < 1e6:
        x = z.sum(axis=0)

    common = z.columns.intersection(x.index)
    z = z[common]
    x = x[common]
    x_safe = x.replace(0, np.nan)

    A = z.div(x_safe, axis=1).fillna(0.0)
    return A, x


def parse_requirements_matrix(records: list[dict]) -> pd.DataFrame:
    """Parse Total Requirements records into Leontief inverse B-matrix."""
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame()

    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")

    industry = df[
        ~df["RowCode"].str.startswith("F") &
        ~df["RowCode"].str.startswith("T") &
        (df["RowCode"] != "") &
        ~df["ColCode"].str.startswith("F") &
        ~df["ColCode"].str.startswith("T") &
        (df["ColCode"] != "")
    ]

    B = industry.pivot_table(
        index="RowCode", columns="ColCode", values="DataValue", aggfunc="first"
    ).fillna(0.0)
    return B


def check_sic_availability() -> list[int]:
    """Check which SIC benchmark years have local data."""
    available = []
    if SIC_DIR.exists():
        for yr in [1947, 1958, 1963, 1967, 1972, 1977]:
            if (SIC_DIR / f"{yr}_A_matrix.csv").exists():
                available.append(yr)
    return available
