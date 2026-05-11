"""FRED/ALFRED API fetcher with date-stamped caching and vintage support.

Fetches any FRED series as an annual pd.Series. Caches raw JSON to
data/cache/fred_{series_id}_{date}.json.

ALFRED support: pass realtime_start/realtime_end to fetch historical vintages.
This returns the data AS IT WAS PUBLISHED at the specified date, not the
current revised values. Critical for understanding NIPA revision impact.
"""

import json
import os
from datetime import date
from pathlib import Path
from typing import Optional

import pandas as pd

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"


def _ensure_cache():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def fetch(series_id: str, api_key: str, start: str = "1929-01-01",
          frequency: str = "a", min_year: int = 1929,
          realtime_start: str = None, realtime_end: str = None) -> pd.Series:
    """Fetch a FRED series. Returns annual pd.Series indexed by year.

    For ALFRED vintage access, pass realtime_start and realtime_end:
      fetch("GDP", key, realtime_start="1994-01-01", realtime_end="1994-12-31")
    returns GDP as published in 1994.
    """
    _ensure_cache()

    # Cache key includes vintage info if ALFRED parameters used
    if realtime_start:
        vintage_tag = f"_vintage_{realtime_start[:4]}"
    else:
        vintage_tag = ""
    cache = CACHE_DIR / f"fred_{series_id}{vintage_tag}_{date.today().isoformat()}.json"

    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "observation_start": start,
            "frequency": frequency,
            "aggregation_method": "avg",
        }
        if realtime_start:
            params["realtime_start"] = realtime_start
        if realtime_end:
            params["realtime_end"] = realtime_end

        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    rows = {}
    for o in data.get("observations", []):
        yr = int(o["date"][:4])
        if o["value"] != "." and yr >= min_year:
            rows[yr] = float(o["value"])

    return pd.Series(rows, name=series_id, dtype=float)


def fetch_vintage(series_id: str, api_key: str, vintage_year: int,
                  start: str = "1929-01-01", min_year: int = 1929) -> pd.Series:
    """Fetch a series as it was published in vintage_year (ALFRED)."""
    return fetch(series_id, api_key, start=start, min_year=min_year,
                 realtime_start=f"{vintage_year}-01-01",
                 realtime_end=f"{vintage_year}-12-31")


def fetch_deflator(api_key: str, base_year: int = 1982) -> pd.Series:
    """Fetch GDP deflator (GDPDEF) and rebase to base_year=100."""
    raw = fetch("GDPDEF", api_key, start="1929-01-01", min_year=1929)
    if base_year in raw.index and raw[base_year] > 0:
        return raw / raw[base_year] * 100
    return raw


def fetch_multiple(series_ids: list[str], api_key: str, **kwargs) -> pd.DataFrame:
    """Fetch multiple FRED series into a DataFrame."""
    result = {}
    for sid in series_ids:
        try:
            result[sid] = fetch(sid, api_key, **kwargs)
        except Exception as e:
            print(f"    [FRED] {sid} failed: {e}")
    return pd.DataFrame(result)


def compare_vintages(series_id: str, api_key: str, vintage_years: list[int],
                     benchmark_years: list[int] = None) -> pd.DataFrame:
    """Compare a series across multiple vintages at benchmark years.

    Returns DataFrame with vintages as columns and benchmark years as rows.
    """
    if benchmark_years is None:
        benchmark_years = [1948, 1958, 1967, 1972, 1977, 1980, 1989]

    result = {}
    # Current (latest) vintage
    current = fetch(series_id, api_key, min_year=1929)
    result["current"] = current

    for vy in vintage_years:
        try:
            vintage = fetch_vintage(series_id, api_key, vy, min_year=1929)
            result[f"v{vy}"] = vintage
        except Exception as e:
            print(f"    [ALFRED] {series_id} vintage {vy}: {e}")

    df = pd.DataFrame(result)
    if benchmark_years:
        df = df.reindex([y for y in benchmark_years if y in df.index])

    return df
