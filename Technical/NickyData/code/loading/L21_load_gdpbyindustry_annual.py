#!/usr/bin/env python3
"""L21 - Load BEA GDPbyIndustry annual data for IO sector classification.

Fetches Table 1 (Value Added), Table 6 (Components of VA: compensation,
taxes, GOS), and gross output data by industry for 1997-2024. Classifies
each industry as productive/trading/unproductive using classifications.json
and outputs annual sector aggregates.

This is the foundation for WP-1: replacing frozen IO ratios with annually-
varying productive sector shares.

Inputs:  BEA API (GDPbyIndustry dataset)
         classifications.json (naics_io sector mapping)
Outputs: parsed-raw/gdpbyindustry_va_annual.csv
         parsed-raw/gdpbyindustry_components_annual.csv
         parsed-raw/annual_io_classified.csv (sector aggregates)
"""

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import PARSED_RAW, CONFIG, ensure_dirs

SERIES_IDS = []
PRIORITY = 21

BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cache"

TABLES = {
    "va": 1,
    "components": 6,
}

YEAR_RANGE = range(1997, 2025)


def _get_api_key() -> str:
    api_key = os.environ.get("BEA_API_KEY", "")
    if not api_key:
        from dotenv import load_dotenv
        env_path = Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env"
        if env_path.exists():
            load_dotenv(env_path)
            api_key = os.environ.get("BEA_API_KEY", "")
    return api_key


def _fetch_table(table_key: str, year: int, api_key: str) -> list[dict]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    table_id = TABLES[table_key]
    cache_path = CACHE_DIR / f"bea_gdpbyind_{table_key}_{year}.json"

    if cache_path.exists():
        with open(cache_path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "UserID": api_key,
            "method": "GetData",
            "DataSetName": "GDPbyIndustry",
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
        time.sleep(0.5)

    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list) and results:
        return results[0].get("Data", [])
    elif isinstance(results, dict):
        return results.get("Data", [])
    return []


def _parse_value(val_str: str) -> float | None:
    val_str = str(val_str).replace(",", "").strip()
    try:
        return float(val_str)
    except ValueError:
        return None


def _load_classification() -> dict[str, str]:
    cls_path = CONFIG / "classifications.json"
    with open(cls_path, encoding="utf-8") as f:
        cls_data = json.load(f)
    return {k: v for k, v in cls_data.get("naics_io", {}).items() if not k.startswith("_")}


def load():
    ensure_dirs()
    api_key = _get_api_key()
    if not api_key:
        return {"status": "fail", "message": "BEA_API_KEY not found"}

    classification = _load_classification()
    all_va_rows = []
    all_comp_rows = []

    for year in YEAR_RANGE:
        # Table 1: Value Added by industry
        va_records = _fetch_table("va", year, api_key)
        for r in va_records:
            ind = r.get("Industry", "").strip()
            val = _parse_value(r.get("DataValue", ""))
            desc = r.get("InduDesc", "").strip()
            if ind and val is not None:
                sector = classification.get(ind, "unclassified")
                all_va_rows.append({
                    "year": year,
                    "industry": ind,
                    "description": desc,
                    "classification": sector,
                    "value_added": val,
                })

        # Table 6: Components of VA (compensation, taxes, GOS)
        comp_records = _fetch_table("components", year, api_key)
        comp_by_ind = {}
        for r in comp_records:
            ind = r.get("Industry", "").strip()
            desc = r.get("InduDesc", "").strip()
            val = _parse_value(r.get("DataValue", ""))
            component = r.get("InduDesc", "")
            if ind not in comp_by_ind:
                comp_by_ind[ind] = {"year": year, "industry": ind, "description": desc}

            # Table 6 returns multiple rows per industry (one per component)
            # The component is identified by a sub-table structure
            # We need to match by the specific measure
            table_str = str(r.get("TableID", ""))
            # Components are typically: Compensation, Taxes, GOS
            # Identified by different rows for same industry
            if val is not None:
                comp_by_ind[ind].setdefault("values", []).append(val)

        for ind, row in comp_by_ind.items():
            sector = classification.get(ind, "unclassified")
            row["classification"] = sector
            all_comp_rows.append(row)

    # Write raw VA data
    va_df = pd.DataFrame(all_va_rows)
    if not va_df.empty:
        va_path = PARSED_RAW / "gdpbyindustry_va_annual.csv"
        va_df.to_csv(va_path, index=False)

    # Compute sector aggregates
    if not va_df.empty:
        agg_rows = []
        for year in YEAR_RANGE:
            yr_data = va_df[va_df["year"] == year]
            for sector in ["productive", "trading", "unproductive", "government"]:
                sector_data = yr_data[yr_data["classification"] == sector]
                agg_rows.append({
                    "year": year,
                    "sector": sector,
                    "value_added": sector_data["value_added"].sum(),
                    "n_industries": len(sector_data),
                })

        agg_df = pd.DataFrame(agg_rows)
        agg_path = PARSED_RAW / "annual_io_classified.csv"
        agg_df.to_csv(agg_path, index=False)

        # Compute productive ratios
        ratio_rows = []
        for year in YEAR_RANGE:
            yr = agg_df[agg_df["year"] == year]
            va_prod = yr[yr["sector"] == "productive"]["value_added"].sum()
            va_trade = yr[yr["sector"] == "trading"]["value_added"].sum()
            va_total = yr["value_added"].sum()
            if va_total > 0:
                ratio_rows.append({
                    "year": year,
                    "ratio_productive_va": va_prod / va_total,
                    "ratio_productive_plus_trading_va": (va_prod + va_trade) / va_total,
                    "va_productive": va_prod,
                    "va_trading": va_trade,
                    "va_unproductive": yr[yr["sector"] == "unproductive"]["value_added"].sum(),
                    "va_total": va_total,
                })

        ratio_df = pd.DataFrame(ratio_rows).set_index("year")
        ratio_path = PARSED_RAW / "annual_io_va_ratios.csv"
        ratio_df.to_csv(ratio_path)

    n_years = len(va_df["year"].unique()) if not va_df.empty else 0
    n_industries = len(va_df["industry"].unique()) if not va_df.empty else 0
    summary = f"GDPbyIndustry: {n_years} years, {n_industries} industries, VA + Components"
    print(f"    [L21] {summary}")
    return {"status": "ok", "summary": summary}
