"""Fetch data from the BEA (Bureau of Economic Analysis) API.

Supports three datasets:
  - NIPA (National Income and Product Accounts)
  - FixedAssets (Fixed Assets tables)
  - GDPbyIndustry (Gross Output / Value Added by Industry)

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

BEA_BASE = "https://apps.bea.gov/api/data/"


def _resolve_api_key(api_key: str | None) -> str:
    key = api_key or os.environ.get("BEA_API_KEY")
    if not key:
        raise EnvironmentError(
            "No BEA API key provided.  Set the BEA_API_KEY environment "
            "variable or pass api_key= explicitly."
        )
    return key


def fetch_bea_nipa(
    table_name: str,
    *,
    api_key: str | None = None,
    frequency: str = "A",
    year: str = "ALL",
) -> dict[str, Any]:
    """Download a NIPA table from BEA.

    Parameters
    ----------
    table_name : str
        BEA NIPA table ID (e.g. "T10705", "T60200D").
    frequency : str
        "A" (annual), "Q" (quarterly), or "M" (monthly).
    year : str
        Comma-separated years or "ALL".
    """
    key = _resolve_api_key(api_key)
    ensure_dirs()

    params = {
        "UserID": key,
        "method": "GetData",
        "DataSetName": "NIPA",
        "TableName": table_name,
        "Frequency": frequency,
        "Year": year,
        "ResultFormat": "JSON",
    }

    try:
        resp = requests.get(BEA_BASE, params=params, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {
            "dataset": "NIPA",
            "table": table_name,
            "data": [],
            "error": str(exc),
        }

    data = resp.json()
    results = data.get("BEAAPI", {}).get("Results", {})
    observations = results.get("Data", [])

    date_str = date.today().isoformat()
    cache_file = api_path("bea", f"nipa_{table_name}", date_str)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    return {
        "dataset": "NIPA",
        "table": table_name,
        "data": observations,
        "obs_count": len(observations),
        "cached_path": str(cache_file),
    }


def fetch_bea_fixed_assets(
    table_name: str,
    *,
    api_key: str | None = None,
    year: str = "ALL",
) -> dict[str, Any]:
    """Download a Fixed Assets table from BEA.

    Parameters
    ----------
    table_name : str
        BEA Fixed Assets table ID (e.g. "FAAt401").
    """
    key = _resolve_api_key(api_key)
    ensure_dirs()

    params = {
        "UserID": key,
        "method": "GetData",
        "DataSetName": "FixedAssets",
        "TableName": table_name,
        "Year": year,
        "ResultFormat": "JSON",
    }

    try:
        resp = requests.get(BEA_BASE, params=params, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {
            "dataset": "FixedAssets",
            "table": table_name,
            "data": [],
            "error": str(exc),
        }

    data = resp.json()
    results = data.get("BEAAPI", {}).get("Results", {})
    observations = results.get("Data", [])

    date_str = date.today().isoformat()
    cache_file = api_path("bea", f"fixed_assets_{table_name}", date_str)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    return {
        "dataset": "FixedAssets",
        "table": table_name,
        "data": observations,
        "obs_count": len(observations),
        "cached_path": str(cache_file),
    }


def fetch_bea_gdp_by_industry(
    *,
    api_key: str | None = None,
    table_id: str = "1",
    frequency: str = "A",
    year: str = "ALL",
    industry: str = "ALL",
) -> dict[str, Any]:
    """Download GDP-by-Industry data from BEA.

    Parameters
    ----------
    table_id : str
        GDPbyIndustry table ID (1=Value Added, 5=Gross Output, etc.).
    industry : str
        Industry code or "ALL".
    """
    key = _resolve_api_key(api_key)
    ensure_dirs()

    params = {
        "UserID": key,
        "method": "GetData",
        "DataSetName": "GDPbyIndustry",
        "TableID": table_id,
        "Frequency": frequency,
        "Year": year,
        "Industry": industry,
        "ResultFormat": "JSON",
    }

    try:
        resp = requests.get(BEA_BASE, params=params, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return {
            "dataset": "GDPbyIndustry",
            "table_id": table_id,
            "data": [],
            "error": str(exc),
        }

    data = resp.json()
    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list):
        results = results[0] if results else {}
    observations = results.get("Data", [])

    date_str = date.today().isoformat()
    cache_file = api_path("bea", f"gdp_by_industry_{table_id}", date_str)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    return {
        "dataset": "GDPbyIndustry",
        "table_id": table_id,
        "data": observations,
        "obs_count": len(observations),
        "cached_path": str(cache_file),
    }
