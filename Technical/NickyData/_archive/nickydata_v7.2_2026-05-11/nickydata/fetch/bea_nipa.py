"""BEA NIPA table fetcher with caching.

Fetches NIPA tables via the BEA API. Each table is cached as a JSON file.
Provides parsing helpers to extract specific line items as annual series.
"""

import json
import os
from datetime import date
from pathlib import Path

import pandas as pd

BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"


def _ensure_cache():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_table(table_name: str, api_key: str, frequency: str = "A",
                year: str = "ALL") -> list[dict]:
    """Fetch a NIPA table from BEA API. Returns list of data records."""
    _ensure_cache()
    cache = CACHE_DIR / f"bea_nipa_{table_name}_{date.today().isoformat()}.json"

    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "UserID": api_key,
            "method": "GetData",
            "DataSetName": "NIPA",
            "TableName": table_name,
            "Frequency": frequency,
            "Year": year,
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    return data.get("BEAAPI", {}).get("Results", {}).get("Data", [])


def parse_line(records: list[dict], line_number: int = None,
               line_description: str = None) -> pd.Series:
    """Extract a single line item from NIPA records as annual pd.Series."""
    rows = {}
    for rec in records:
        match = True
        if line_number is not None and int(rec.get("LineNumber", 0)) != line_number:
            match = False
        if line_description is not None and line_description.lower() not in rec.get("LineDescription", "").lower():
            match = False
        if not match:
            continue

        yr_str = rec.get("TimePeriod", "")
        val_str = str(rec.get("DataValue", "")).replace(",", "")
        try:
            yr = int(yr_str)
            val = float(val_str)
            rows[yr] = val
        except (ValueError, TypeError):
            continue

    return pd.Series(rows, dtype=float)


def parse_by_industry(records: list[dict]) -> pd.DataFrame:
    """Parse an industry-detail NIPA table into a year × industry DataFrame."""
    rows = []
    for rec in records:
        yr_str = rec.get("TimePeriod", "")
        ln = rec.get("LineNumber", "")
        desc = rec.get("LineDescription", "")
        val_str = str(rec.get("DataValue", "")).replace(",", "")
        try:
            rows.append({
                "year": int(yr_str),
                "line": int(ln),
                "description": desc,
                "value": float(val_str),
            })
        except (ValueError, TypeError):
            continue

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    return df


def fetch_and_parse(table_name: str, api_key: str, line_number: int = None,
                    line_description: str = None) -> pd.Series:
    """Convenience: fetch a table and extract a specific line."""
    records = fetch_table(table_name, api_key)
    return parse_line(records, line_number=line_number, line_description=line_description)
