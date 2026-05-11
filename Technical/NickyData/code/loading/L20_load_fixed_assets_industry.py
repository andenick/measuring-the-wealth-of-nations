#!/usr/bin/env python3
"""L06b - Load BEA Fixed Assets by industry and compute K* (productive capital stock).

K* = Σ K_j for j in productive sectors, using the NIPA 6.5 classification.
This replaces the total-K approximation (K × productive_output_ratio) with
actual industry-level data.

BEA Fixed Assets Table FAAt401 provides current-cost net stock of private
fixed assets by industry. We classify industries and sum productive sectors.

Inputs:  BEA API (FixedAssets dataset, FAAt401)
         nipa_65_to_io_classification.json
Outputs: final-data/series/K_star_by_industry.csv
Dependencies: None
"""

import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT, CONFIG, ensure_dirs

SERIES_IDS = []
PRIORITY = 6

BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cache"

# FAAt401 LineNumber → sector mapping (top-level industry lines)
# These are the BEA Fixed Assets industry lines that map to NIPA 6.5D classifications
FA_PRODUCTIVE_LINES = {
    3: "Agriculture, forestry, fishing, and hunting",
    4: "Mining",
    5: "Utilities",
    6: "Construction",
    7: "Manufacturing",
    14: "Transportation and warehousing",
    21: "Educational services",
    22: "Health care and social assistance",
    24: "Arts, entertainment, and recreation",
    25: "Accommodation and food services",
    26: "Other services, except government",
}

FA_TRADING_LINES = {
    10: "Wholesale trade",
    11: "Retail trade",
}

FA_UNPRODUCTIVE_LINES = {
    15: "Information",  # Mixed — but info sector K is mostly telecom/media infra
    16: "Finance and insurance",
    17: "Real estate and rental and leasing",
    18: "Professional, scientific, and technical services",
    19: "Management of companies and enterprises",
    20: "Administrative and waste management services",
}


def _get_api_key() -> str:
    api_key = os.environ.get("BEA_API_KEY", "")
    if not api_key:
        from dotenv import load_dotenv
        env_paths = [
            Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env",
        ]
        for p in env_paths:
            if p.exists():
                load_dotenv(p)
                api_key = os.environ.get("BEA_API_KEY", "")
                if api_key:
                    break
    return api_key


def _fetch_fa(api_key: str) -> list[dict]:
    """Fetch Fixed Assets Table FAAt401."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"bea_fa_FAAt401_{date.today().isoformat()}.json"

    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "UserID": api_key,
            "method": "GetData",
            "DataSetName": "FixedAssets",
            "TableName": "FAAt401",
            "Year": "ALL",
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    return data.get("BEAAPI", {}).get("Results", {}).get("Data", [])


def _parse_by_industry(records: list[dict], line_map: dict[int, str],
                       min_year: int = 1947) -> pd.DataFrame:
    """Parse FA records into year × industry DataFrame (billions $)."""
    result = {}
    for ln, name in line_map.items():
        vals = {}
        for rec in records:
            try:
                rec_ln = int(rec.get("LineNumber", 0))
                yr = int(rec.get("TimePeriod", 0))
                val_str = str(rec.get("DataValue", "")).replace(",", "")
                if rec_ln == ln and yr >= min_year:
                    vals[yr] = float(val_str)
            except (ValueError, TypeError):
                continue
        if vals:
            result[name] = pd.Series(vals)
    df = pd.DataFrame(result)
    df.index.name = "year"
    return df


def load():
    """Load Fixed Assets, classify industries, compute K*."""
    ensure_dirs()
    steps = []

    api_key = _get_api_key()
    if not api_key:
        print("    [L06b] SKIP: BEA_API_KEY not found")
        return {"series_id": "L06b", "status": "skip", "steps": ["No API key"], "outputs": []}

    records = _fetch_fa(api_key)
    if not records:
        print("    [L06b] FAIL: No Fixed Assets data")
        return {"series_id": "L06b", "status": "fail", "steps": ["No data"], "outputs": []}

    steps.append(f"FAAt401: {len(records)} records")

    # Parse by sector classification
    k_prod = _parse_by_industry(records, FA_PRODUCTIVE_LINES)
    k_trade = _parse_by_industry(records, FA_TRADING_LINES)
    k_unprod = _parse_by_industry(records, FA_UNPRODUCTIVE_LINES)

    # Also get total private (line 2)
    k_total_df = _parse_by_industry(records, {2: "Total_private"})
    k_total = k_total_df["Total_private"] if "Total_private" in k_total_df.columns else pd.Series(dtype=float)

    # K* = productive + trading capital stock
    k_star = k_prod.sum(axis=1) + k_trade.sum(axis=1)
    k_star_bn = k_star / 1e3  # millions → billions (FA data is in millions)

    # Compute productive share of total K
    if not k_total.empty:
        common = k_star.index.intersection(k_total.index)
        prod_share = k_star[common] / k_total[common]
        steps.append(f"K* productive share: {prod_share.iloc[0]:.1%} ({int(common[0])}) → "
                     f"{prod_share.iloc[-1]:.1%} ({int(common[-1])})")

    # Save K* series
    out = pd.DataFrame({
        "K_star_bn": k_star_bn,
        "K_total_bn": k_total / 1e3 if not k_total.empty else None,
        "productive_share": prod_share if not k_total.empty else None,
    })
    out.index.name = "year"
    out_path = SERIES_OUT / "K_star_by_industry.csv"
    out.to_csv(out_path)

    steps.append(f"K*: {len(k_star_bn)} years ({int(k_star_bn.index.min())}-{int(k_star_bn.index.max())})")
    print(f"    [L06b] K*: {len(k_star_bn)} years, "
          f"{k_star_bn.iloc[0]:.0f} → {k_star_bn.iloc[-1]:.0f} bn")

    return {
        "series_id": "L06b",
        "status": "ok",
        "steps": steps,
        "outputs": [str(out_path)],
    }
