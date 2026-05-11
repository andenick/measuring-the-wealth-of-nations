"""BEA Underlying GDP-by-Industry fetcher — detail-level gross output and intermediate inputs.

Provides access to the UnderlyingGDPbyIndustry dataset which has:
- TableID=237: Gross output at 412-industry detail level (annual 1997-2024)
- TableID=219: Gross output at ~190-industry underlying summary level (annual 1997-2024)
- TableID=229: Intermediate inputs at ~190-industry underlying summary level (annual 1997-2024)
- TableID=210: Value added at ~190-industry underlying summary level (annual 1997-2024)

This is the key data source for computing TP* at maximum sector resolution.
The InputOutput dataset only provides sector (15) and summary (71) levels.
"""

import json
import os
import time
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"

TABLES = {
    "go_detail": 237,
    "go_underlying": 219,
    "ii_underlying": 229,
    "va_underlying": 210,
}


def _ensure_cache():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_underlying(table_key: str, year: int, api_key: str) -> list[dict]:
    """Fetch a single year from the UnderlyingGDPbyIndustry dataset.

    Args:
        table_key: One of "go_detail", "go_underlying", "ii_underlying", "va_underlying"
        year: Year to fetch (1997-2024)
        api_key: BEA API key
    """
    _ensure_cache()
    table_id = TABLES[table_key]
    cache_path = CACHE_DIR / f"bea_underlying_{table_key}_{year}.json"

    if cache_path.exists():
        with open(cache_path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        params = {
            "UserID": api_key,
            "method": "GetData",
            "DataSetName": "UnderlyingGDPbyIndustry",
            "TableID": str(table_id),
            "Frequency": "A",
            "Year": str(year),
            "Industry": "ALL",
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list) and results:
        return results[0].get("Data", [])
    elif isinstance(results, dict):
        return results.get("Data", [])
    return []


def fetch_all_years(table_key: str, api_key: str,
                    start_year: int = 1997, end_year: int = 2024) -> pd.DataFrame:
    """Fetch all years for a table and return as a DataFrame indexed by industry code.

    Returns DataFrame with columns = years, index = industry codes, values = billions $.
    """
    all_data = {}
    for year in range(start_year, end_year + 1):
        records = fetch_underlying(table_key, year, api_key)
        year_data = {}
        for r in records:
            ind = r.get("Industry", "")
            val_str = str(r.get("DataValue", "")).replace(",", "").strip()
            if not ind or not val_str:
                continue
            try:
                year_data[ind] = float(val_str)
            except ValueError:
                continue
        all_data[year] = year_data
        time.sleep(0.3)

    df = pd.DataFrame(all_data)
    df.index.name = "Industry"
    df.columns.name = "Year"
    return df


def get_industry_descriptions(records: list[dict]) -> dict[str, str]:
    """Extract industry code -> description mapping from API records."""
    descs = {}
    for r in records:
        ind = r.get("Industry", "")
        desc = r.get("IndustrYDescription", r.get("IndustryDescription", ""))
        if ind and desc:
            descs[ind] = desc
    return descs


def parse_detail_go(records: list[dict]) -> pd.Series:
    """Parse detail-level gross output records into a Series indexed by industry code."""
    data = {}
    for r in records:
        ind = r.get("Industry", "")
        val_str = str(r.get("DataValue", "")).replace(",", "").strip()
        if not ind or not val_str:
            continue
        try:
            data[ind] = float(val_str)
        except ValueError:
            continue
    s = pd.Series(data, name="GrossOutput")
    s.index.name = "Industry"
    return s
