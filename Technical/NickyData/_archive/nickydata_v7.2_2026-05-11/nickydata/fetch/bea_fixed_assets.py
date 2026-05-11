"""BEA Fixed Assets fetcher.

Fetches Table FAAt401 (total private fixed assets) for K computation.
Uses IO productive output ratio to approximate K* (productive sector capital).
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


def fetch(api_key: str, table_name: str = "FAAt401") -> list[dict]:
    """Fetch Fixed Assets table from BEA API."""
    _ensure_cache()
    cache = CACHE_DIR / f"bea_fa_{table_name}_{date.today().isoformat()}.json"

    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "UserID": api_key,
            "method": "GetData",
            "DataSetName": "FixedAssets",
            "TableName": table_name,
            "Year": "ALL",
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    return data.get("BEAAPI", {}).get("Results", {}).get("Data", [])


def parse_total_k(records: list[dict], line_number: int = 1,
                  min_year: int = 1929) -> pd.Series:
    """Extract total K (private nonresidential fixed assets) in millions."""
    rows = {}
    for rec in records:
        ln = int(rec.get("LineNumber", 0))
        yr = int(rec.get("TimePeriod", 0))
        val_str = str(rec.get("DataValue", "")).replace(",", "")
        if ln == line_number and yr >= min_year:
            try:
                rows[yr] = float(val_str)
            except ValueError:
                continue
    return pd.Series(rows, name="K_total_millions", dtype=float)
