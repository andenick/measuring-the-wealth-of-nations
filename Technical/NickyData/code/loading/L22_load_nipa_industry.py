#!/usr/bin/env python3
"""L22 - Load NIPA industry-level employment and compensation data.

Fetches Table 6.5D (FTE by industry) and Table 6.2D (compensation by industry)
from BEA NIPA API. Classifies sectors using nipa_65_to_io_classification.json
and classifications.json to compute annual productive employment counts and
productive compensation (V*).

Inputs:  BEA API (NIPA dataset, Tables T60500D and T60200D)
         nipa_65_to_io_classification.json
         classifications.json
Outputs: parsed-raw/nipa_fte_by_industry.csv (annual FTE, 1998-2024)
         parsed-raw/nipa_compensation_by_industry.csv (annual comp, 1998-2024)
         parsed-raw/annual_productive_employment.csv (Lp, L, Lp/L)
         parsed-raw/annual_productive_compensation.csv (V*, W, V*/W)
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
PRIORITY = 22

BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cache"

YEAR_RANGE = range(1987, 2025)


def _get_api_key() -> str:
    api_key = os.environ.get("BEA_API_KEY", "")
    if not api_key:
        from dotenv import load_dotenv
        env_path = Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env"
        if env_path.exists():
            load_dotenv(env_path)
            api_key = os.environ.get("BEA_API_KEY", "")
    return api_key


def _fetch_nipa(table_name: str, api_key: str) -> list[dict]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"bea_nipa_{table_name}.json"

    if cache_path.exists():
        with open(cache_path, encoding="utf-8") as f:
            return json.load(f)

    import requests
    params = {
        "UserID": api_key,
        "method": "GetData",
        "DataSetName": "NIPA",
        "TableName": table_name,
        "Frequency": "A",
        "Year": "ALL",
        "ResultFormat": "JSON",
    }
    resp = requests.get(BASE_URL, params=params, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list) and results:
        records = results[0].get("Data", [])
    elif isinstance(results, dict):
        records = results.get("Data", [])
    else:
        records = []

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(records, f)
    time.sleep(1.0)
    return records


def _parse_nipa_records(records: list[dict]) -> pd.DataFrame:
    rows = []
    for r in records:
        line_num = r.get("LineNumber", "")
        line_desc = r.get("LineDescription", "").strip()
        year_str = r.get("TimePeriod", "")
        val_str = str(r.get("DataValue", "")).replace(",", "").strip()

        try:
            year = int(year_str)
            value = float(val_str)
            line_num = int(line_num) if line_num else 0
        except (ValueError, TypeError):
            continue

        if year < 1998:
            continue

        rows.append({
            "year": year,
            "line_number": line_num,
            "description": line_desc,
            "value": value,
        })

    return pd.DataFrame(rows)


def _load_fte_classification() -> dict[int, str]:
    cls_path = CONFIG / "nipa_65_to_io_classification.json"
    with open(cls_path, encoding="utf-8") as f:
        cls_data = json.load(f)
    return {int(k): v["sector"] for k, v in cls_data["classification"].items()}


def _load_comp_classification() -> dict[int, str]:
    cls_path = CONFIG / "classifications.json"
    with open(cls_path, encoding="utf-8") as f:
        cls_data = json.load(f)

    nipa_65 = cls_data.get("nipa_65_fte", {})
    return {int(k): v for k, v in nipa_65.items() if not k.startswith("_")}


def load():
    ensure_dirs()
    api_key = _get_api_key()
    if not api_key:
        return {"status": "fail", "message": "BEA_API_KEY not found"}

    outputs = []
    fte_cls = _load_fte_classification()
    comp_cls = _load_comp_classification()

    # --- Table 6.5D: FTE by industry ---
    fte_records = _fetch_nipa("T60500D", api_key)
    fte_df = _parse_nipa_records(fte_records)

    if not fte_df.empty:
        fte_df["classification"] = fte_df["line_number"].map(fte_cls).fillna("unclassified")
        fte_path = PARSED_RAW / "nipa_fte_by_industry.csv"
        fte_df.to_csv(fte_path, index=False)
        outputs.append(str(fte_path))

        # Compute annual Lp and L
        emp_rows = []
        for year in sorted(fte_df["year"].unique()):
            yr = fte_df[fte_df["year"] == year]
            lp = yr[yr["classification"] == "productive"]["value"].sum()
            l_trade = yr[yr["classification"] == "trading"]["value"].sum()
            l_total_classified = yr[yr["classification"].isin(
                ["productive", "trading", "unproductive"]
            )]["value"].sum()

            # Total L: use aggregate line (usually line 1 or 2)
            total_lines = yr[yr["line_number"].isin([1, 2])]
            l_total = total_lines["value"].max() if not total_lines.empty else l_total_classified

            if l_total > 0:
                emp_rows.append({
                    "year": year,
                    "Lp": lp,
                    "L_trading": l_trade,
                    "L_total": l_total,
                    "Lp_L": lp / l_total,
                })

        if emp_rows:
            emp_df = pd.DataFrame(emp_rows).set_index("year")
            emp_path = PARSED_RAW / "annual_productive_employment.csv"
            emp_df.to_csv(emp_path)
            outputs.append(str(emp_path))
            print(f"    [L22] FTE: {len(emp_rows)} years, Lp/L range [{emp_df['Lp_L'].min():.3f}, {emp_df['Lp_L'].max():.3f}]")

    # --- Table 6.2D: Compensation by industry ---
    comp_records = _fetch_nipa("T60200D", api_key)
    comp_df = _parse_nipa_records(comp_records)

    if not comp_df.empty:
        comp_df["classification"] = comp_df["line_number"].map(comp_cls).fillna("unclassified")
        comp_path = PARSED_RAW / "nipa_compensation_by_industry.csv"
        comp_df.to_csv(comp_path, index=False)
        outputs.append(str(comp_path))

        # Compute annual V* and W
        vstar_rows = []
        for year in sorted(comp_df["year"].unique()):
            yr = comp_df[comp_df["year"] == year]
            v_prod = yr[yr["classification"] == "productive"]["value"].sum()
            v_trade = yr[yr["classification"] == "trading"]["value"].sum()

            # Total W: aggregate line (line 1 or 2)
            total_lines = yr[yr["line_number"].isin([1, 2])]
            w_total = total_lines["value"].max() if not total_lines.empty else yr["value"].sum()

            if w_total > 0:
                vstar_rows.append({
                    "year": year,
                    "V_star": v_prod,
                    "V_trading": v_trade,
                    "W_total": w_total,
                    "V_star_W": v_prod / w_total,
                })

        if vstar_rows:
            vstar_df = pd.DataFrame(vstar_rows).set_index("year")
            vstar_path = PARSED_RAW / "annual_productive_compensation.csv"
            vstar_df.to_csv(vstar_path)
            outputs.append(str(vstar_path))
            print(f"    [L22] Compensation: {len(vstar_rows)} years, V*/W range [{vstar_df['V_star_W'].min():.3f}, {vstar_df['V_star_W'].max():.3f}]")

    summary = f"NIPA industry: {len(outputs)} files, FTE + Compensation classified"
    print(f"    [L22] {summary}")
    return {"status": "ok", "summary": summary, "outputs": outputs}
