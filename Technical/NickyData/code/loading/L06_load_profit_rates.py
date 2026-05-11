#!/usr/bin/env python3
"""L06 - Load Profit Rates: T513, T514.

Inputs:
  - ch05/ProfitRates_1948_1989.csv (Format B, 1948-1989) — book values
  - ch05/ProfitRates_Extended.csv (Format B, 1948-2024) — pre-extended
Column map: T513←T513_r_star_pct (÷100), T514←T514_r_star_adj_pct (÷100)
Outputs: parsed-raw/T513_parsed.csv, T514_parsed.csv, *_ext_parsed.csv,
         plus T513_capacity_utilization_parsed.csv etc. (cross-validation)
Dependencies: None
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from utils.paths import ST_CHOPPED, PARSED_RAW, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T513", "T514"]

COLUMN_MAP = {
    "T513": "T513_r_star_pct",
    "T514": "T514_r_star_adj_pct",
}


def _fetch_k_star_industry(outputs: list):
    """Fetch BEA Fixed Assets Table 4.1 and compute K* = K × IO productive ratio."""
    import json, os
    from datetime import date
    from dotenv import load_dotenv

    env_path = Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env"
    load_dotenv(env_path)
    api_key = os.environ.get("BEA_API_KEY")
    if not api_key:
        return

    from utils.paths import API_RAW, SERIES_OUT
    import pandas as pd

    cache = API_RAW / f"bea_fixed_assets_by_industry_{date.today().isoformat()}.json"
    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {"UserID": api_key, "method": "GetData", "DataSetName": "FixedAssets",
                  "TableName": "FAAt403", "Year": "ALL", "ResultFormat": "JSON"}
        resp = requests.get("https://apps.bea.gov/api/data", params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)

    records = data.get("BEAAPI", {}).get("Results", {}).get("Data", [])
    k_total_dict = {}
    for rec in records:
        yr = int(rec.get("TimePeriod", 0))
        ln = int(rec.get("LineNumber", 0))
        val_str = str(rec.get("DataValue", "")).replace(",", "")
        if ln == 1 and yr >= 1948:
            try:
                k_total_dict[yr] = float(val_str)
            except ValueError:
                continue

    if not k_total_dict:
        return

    k_total = pd.Series(k_total_dict)
    io_path = SERIES_OUT / "IO_productive_ratios.csv"
    if io_path.exists():
        io = pd.read_csv(io_path, index_col="year")
        prod_ratio = io.get("ratio_productive_output", pd.Series(0.55, index=k_total.index))
    else:
        prod_ratio = pd.Series(0.55, index=k_total.index)

    k_total_bn = k_total / 1e3
    avg_ratio = prod_ratio.mean() if len(prod_ratio) > 0 else 0.55
    k_star_bn = k_total_bn.copy()
    for yr in k_total_bn.index:
        r = prod_ratio.get(yr, avg_ratio)
        k_star_bn[yr] = k_total_bn[yr] * r

    out = pd.DataFrame({"K_star_bn": k_star_bn, "K_total_bn": k_total_bn})
    out["K_star_ratio"] = out["K_star_bn"] / out["K_total_bn"]
    out.index.name = "year"
    out_path = PARSED_RAW / "fixed_assets_by_industry.csv"
    out.to_csv(out_path)
    also_path = SERIES_OUT / "K_star_by_industry.csv"
    out.to_csv(also_path)
    outputs.extend([str(out_path), str(also_path)])
    print(f"    [L06] K*: {len(out)} years, K*/K={out['K_star_ratio'].mean():.3f}")


def load():
    """Load profit rates, converting percentage to ratio (÷100)."""
    ensure_dirs()
    outputs = []

    # Book data
    book_src = ST_CHOPPED / "ch05" / "ProfitRates_1948_1989.csv"
    if not book_src.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {book_src}", "outputs": []}

    book_df = load_chopped_direct(book_src)
    for sid, col in COLUMN_MAP.items():
        if col not in book_df.columns:
            print(f"    [L06] {sid}: column {col} not found in book")
            continue
        out = book_df[[col]].rename(columns={col: "value"}).dropna()
        out["value"] = out["value"] / 100.0  # pct -> ratio
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L06] {sid}: {len(out)} book rows (÷100 -> ratio)")

    # Also save cross-validation columns from book
    for extra_col in ["capacity_utilization", "S_star_bn", "K_bn"]:
        if extra_col in book_df.columns:
            out = book_df[[extra_col]].rename(columns={extra_col: "value"}).dropna()
            out_path = PARSED_RAW / f"T513_{extra_col}_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))

    # Extended data (pre-computed)
    ext_src = ST_CHOPPED / "ch05" / "ProfitRates_Extended.csv"
    if ext_src.exists():
        ext_df = load_chopped_direct(ext_src)
        for sid, col in COLUMN_MAP.items():
            if col not in ext_df.columns:
                continue
            out = ext_df[[col]].rename(columns={col: "value"}).dropna()
            out["value"] = out["value"] / 100.0
            out_path = PARSED_RAW / f"{sid}_ext_parsed.csv"
            out.to_csv(out_path)
            outputs.append(str(out_path))
            print(f"    [L06] {sid}: {len(out)} extended rows")
    else:
        print("    [L06] Extended file not found, book-only")

    # Fetch K* from BEA Fixed Assets × IO productive ratio
    try:
        _fetch_k_star_industry(outputs)
    except Exception as e:
        print(f"    [L06] K* fetch skipped: {e}")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Profit rates | {len(outputs)} files",
        "outputs": outputs,
    }
