"""Fetch time-series observations from the FRED API.

Caches raw JSON responses under ``data/raw-data/api/`` so that repeated
runs do not hit the network.
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from typing import Any

import requests

from ..paths import api_path, ensure_dirs

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get("FRED_API_KEY")
    if not key:
        raise EnvironmentError(
            "No FRED API key provided.  Set the FRED_API_KEY environment "
            "variable or pass api_key= explicitly."
        )
    return key


def fetch_fred(
    series_id: str,
    *,
    api_key: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    file_type: str = "json",
) -> dict[str, Any]:
    """Download observations for *series_id* from FRED."""
    key = _resolve_api_key(api_key)
    ensure_dirs()

    params: dict[str, str] = {
        "series_id": series_id,
        "api_key": key,
        "file_type": file_type,
    }
    if start_date:
        params["observation_start"] = start_date
    if end_date:
        params["observation_end"] = end_date

    try:
        resp = requests.get(FRED_BASE, params=params, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {
            "observations": [],
            "vintage_date": None,
            "obs_count": 0,
            "series_id": series_id,
            "error": str(exc),
        }

    data = resp.json()
    observations = data.get("observations", [])

    vintage = datetime.utcnow().strftime("%Y-%m-%d")
    date_str = date.today().isoformat()
    cache_file = api_path("fred", series_id, date_str)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    return {
        "observations": observations,
        "vintage_date": vintage,
        "obs_count": len(observations),
        "series_id": series_id,
        "cached_path": str(cache_file),
    }
