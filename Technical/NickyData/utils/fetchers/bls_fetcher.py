"""Fetch time-series data from the BLS (Bureau of Labor Statistics) API v2.

Used primarily for CES (Current Employment Statistics) production worker
series needed to extend Shaikh & Tonak labor share ratios (Lp/L, V*/W).

Caches raw JSON responses under ``data/raw-data/api/``.
"""

from __future__ import annotations

import json
import os
from datetime import date
from typing import Any

import requests

from ..paths import api_path, ensure_dirs

BLS_BASE = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get("BLS_API_KEY")
    if not key:
        raise EnvironmentError(
            "No BLS API key provided.  Set the BLS_API_KEY environment "
            "variable or pass api_key= explicitly."
        )
    return key


def fetch_bls(
    series_ids: list[str],
    *,
    api_key: str | None = None,
    start_year: int = 1948,
    end_year: int | None = None,
    annual_average: bool = True,
) -> dict[str, Any]:
    """Download one or more BLS time series.

    Parameters
    ----------
    series_ids : list[str]
        BLS series IDs (e.g. ["CES0500000006", "CES0500000001"]).
        Maximum 50 per request.
    start_year, end_year : int
        Year range (BLS API allows 20-year spans per request with a key).
    annual_average : bool
        Whether to include annual average values.
    """
    key = _resolve_api_key(api_key)
    ensure_dirs()

    if end_year is None:
        end_year = date.today().year

    payload = {
        "seriesid": series_ids[:50],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": key,
        "annualaverage": annual_average,
    }

    headers = {"Content-type": "application/json"}

    try:
        resp = requests.post(BLS_BASE, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {
            "series_ids": series_ids,
            "data": {},
            "error": str(exc),
        }

    data = resp.json()
    status = data.get("status", "")
    results = data.get("Results", {}).get("series", [])

    parsed: dict[str, list[dict]] = {}
    for series_result in results:
        sid = series_result.get("seriesID", "")
        observations = series_result.get("data", [])
        parsed[sid] = observations

    date_str = date.today().isoformat()
    tag = "_".join(series_ids[:3])
    if len(series_ids) > 3:
        tag += f"_plus{len(series_ids) - 3}"
    cache_file = api_path("bls", tag, date_str)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    return {
        "series_ids": series_ids,
        "status": status,
        "data": parsed,
        "obs_count": sum(len(v) for v in parsed.values()),
        "cached_path": str(cache_file),
    }
