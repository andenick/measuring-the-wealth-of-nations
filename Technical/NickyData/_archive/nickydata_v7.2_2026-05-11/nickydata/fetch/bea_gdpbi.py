"""BEA GDP-by-Industry fetcher.

Fetches gross output and value added by industry from the GDPbyIndustry dataset.
TableID=15 = Gross Output by Industry (NAICS, annual, 1997+).
TableID=1 = Value Added by Industry.
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


def fetch(api_key: str, table_id: int = 15, frequency: str = "A",
          year: str = "ALL", industry: str = "ALL") -> list[dict]:
    """Fetch GDP-by-Industry data from BEA API."""
    _ensure_cache()
    cache = CACHE_DIR / f"bea_gdpbi_{table_id}_{date.today().isoformat()}.json"

    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "UserID": api_key,
            "method": "GetData",
            "DataSetName": "GDPbyIndustry",
            "TableID": str(table_id),
            "Frequency": frequency,
            "Year": year,
            "Industry": industry,
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list):
        return results[0].get("Data", []) if results else []
    return results.get("Data", [])


def parse_by_industry(records: list[dict]) -> pd.DataFrame:
    """Parse GDP-by-Industry records into a year × industry DataFrame."""
    rows = []
    for rec in records:
        try:
            rows.append({
                "year": int(rec.get("Year", 0)),
                "industry": rec.get("Industry", ""),
                "industry_desc": rec.get("IndustrYDescription", rec.get("IndustryDescription", "")),
                "value": float(str(rec.get("DataValue", "0")).replace(",", "")),
            })
        except (ValueError, TypeError):
            continue
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def sum_by_classification(records: list[dict], classification: dict,
                          year: int = None) -> dict:
    """Sum gross output by productive/trading/unproductive classification.

    classification: dict mapping industry codes to "productive"/"trading"/"unproductive"
    Returns: {"productive": X, "trading": Y, "unproductive": Z, "total": T}
    """
    df = parse_by_industry(records)
    if df.empty:
        return {}

    if year:
        df = df[df["year"] == year]

    result = {"productive": 0, "trading": 0, "unproductive": 0, "government": 0, "total": 0}

    for _, row in df.iterrows():
        ind = row["industry"]
        val = row["value"]
        cls = classification.get(ind, None)
        if cls and cls in result:
            result[cls] += val
        result["total"] += val

    return result
