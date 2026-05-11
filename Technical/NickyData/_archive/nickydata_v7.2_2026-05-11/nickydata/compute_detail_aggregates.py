"""Step 4: Compute detail-level TP*, C*m, GFP*, VA* for all years 1997-2024.

Uses:
- UnderlyingGDPbyIndustry TableID=237 (412-industry detail gross output)
- UnderlyingGDPbyIndustry TableID=229 (189-industry underlying intermediate inputs)
- UnderlyingGDPbyIndustry TableID=210 (189-industry underlying value added)
- naics_detail_classification.json (412-industry Appendix F classification)

Also fetches annual IO Use tables (1997-2024) from InputOutput dataset for comparison.
"""
import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / "data" / "user-inputs" / "api_keys.env")

BEA_KEY = os.environ.get("BEA_API_KEY", "")
BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = ROOT / "data" / "cache"


def fetch_underlying(table_id: int, year: int) -> list[dict]:
    """Fetch from UnderlyingGDPbyIndustry."""
    table_map = {237: "go_detail", 219: "go_underlying", 229: "ii_underlying", 210: "va_underlying"}
    label = table_map.get(table_id, str(table_id))
    cache = CACHE_DIR / f"bea_underlying_{label}_{year}.json"
    cache.parent.mkdir(parents=True, exist_ok=True)

    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        params = {
            "UserID": BEA_KEY,
            "method": "GetData",
            "DataSetName": "UnderlyingGDPbyIndustry",
            "TableID": str(table_id),
            "Frequency": "A",
            "Year": str(year),
            "Industry": "ALL",
            "ResultFormat": "JSON",
        }
        resp = requests.get(BASE_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)
        time.sleep(0.5)

    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list) and results:
        return results[0].get("Data", [])
    elif isinstance(results, dict):
        return results.get("Data", [])
    return []


def records_to_series(records: list[dict]) -> dict[str, float]:
    """Convert API records to {industry_code: value} dict."""
    data = {}
    for r in records:
        ind = r.get("Industry", "").strip()
        val_str = str(r.get("DataValue", "")).replace(",", "").strip()
        if not ind or not val_str:
            continue
        try:
            data[ind] = float(val_str)
        except ValueError:
            continue
    return data


def main():
    # Load classification
    cls_path = ROOT / "config" / "naics_detail_classification.json"
    with open(cls_path, encoding="utf-8") as f:
        cls_data = json.load(f)
    classification = cls_data["classification"]
    descriptions = cls_data["descriptions"]

    productive_codes = {c for c, v in classification.items() if v == "productive"}
    trading_codes = {c for c, v in classification.items() if v == "trading"}
    unproductive_codes = {c for c, v in classification.items() if v == "unproductive"}
    government_codes = {c for c, v in classification.items() if v == "government"}

    # ALSO load summary-level IO classification for VA computation
    # (Summary codes match the VA underlying data without double-counting)
    io_cls_path = ROOT / "config" / "classifications.json"
    with open(io_cls_path, encoding="utf-8") as f:
        io_cls_data = json.load(f)
    naics_io_cls = {k: v for k, v in io_cls_data["naics_io"].items() if not k.startswith("_")}
    io_productive = {c for c, v in naics_io_cls.items() if v == "productive"}
    io_trading = {c for c, v in naics_io_cls.items() if v == "trading"}

    print("=" * 80)
    print("DETAIL-LEVEL MARXIAN AGGREGATES — ALL YEARS 1997-2024")
    print("=" * 80)
    print(f"Detail classification: {len(productive_codes)} productive, {len(trading_codes)} trading, "
          f"{len(unproductive_codes)} unproductive, {len(government_codes)} government")
    print(f"Summary IO classification: {len(io_productive)} productive, {len(io_trading)} trading")

    # GDP series for ratio computation (from FRED, approximate)
    gdp_billions = {
        1997: 8577.6, 1998: 9062.8, 1999: 9631.2, 2000: 10252.3, 2001: 10581.9,
        2002: 10936.4, 2003: 11458.2, 2004: 12213.7, 2005: 13036.6, 2006: 13814.6,
        2007: 14451.9, 2008: 14712.8, 2009: 14448.9, 2010: 14992.1, 2011: 15542.6,
        2012: 16197.0, 2013: 16785.0, 2014: 17527.3, 2015: 18224.8, 2016: 18745.1,
        2017: 19485.4, 2018: 20533.1, 2019: 21381.0, 2020: 21060.5, 2021: 23315.1,
        2022: 25462.7, 2023: 27360.9, 2024: 28780.8,
    }

    # Fetch and compute for each year
    results = []
    for year in range(1997, 2025):
        print(f"\n--- {year} ---")

        # Fetch detail-level gross output
        go_records = fetch_underlying(237, year)
        go_data = records_to_series(go_records)
        print(f"  GO detail: {len(go_data)} industries")

        # Fetch underlying value added (for GFP* = VA of productive+trading)
        va_records = fetch_underlying(210, year)
        va_data = records_to_series(va_records)
        print(f"  VA underlying: {len(va_data)} industries")

        # Compute aggregates from detail GO
        go_productive = sum(v for c, v in go_data.items() if c in productive_codes)
        go_trading = sum(v for c, v in go_data.items() if c in trading_codes)
        go_unproductive = sum(v for c, v in go_data.items() if c in unproductive_codes)
        go_government = sum(v for c, v in go_data.items() if c in government_codes)
        go_total = go_productive + go_trading + go_unproductive + go_government

        tp_star = go_productive + go_trading

        # GFP* = VA of productive + trading sectors
        # Use IO summary codes (which match the VA underlying data without double-counting)
        va_productive = sum(va_data.get(c, 0) for c in io_productive if c in va_data)
        va_trading = sum(va_data.get(c, 0) for c in io_trading if c in va_data)
        gfp_star = va_productive + va_trading

        # C*m = TP* - GFP* (intermediate inputs = gross output - value added)
        cm_star = tp_star - gfp_star

        gdp = gdp_billions.get(year, 0)
        tp_gdp_ratio = tp_star / gdp if gdp > 0 else 0
        prod_share = go_productive / go_total if go_total > 0 else 0
        go_gdp_ratio = go_total / gdp if gdp > 0 else 0

        row = {
            "year": year,
            "gdp": gdp,
            "go_total": go_total,
            "go_productive": go_productive,
            "go_trading": go_trading,
            "go_unproductive": go_unproductive,
            "go_government": go_government,
            "tp_star": tp_star,
            "cm_star": cm_star,
            "gfp_star": gfp_star,
            "va_productive": va_productive,
            "va_trading": va_trading,
            "tp_gdp_ratio": tp_gdp_ratio,
            "go_gdp_ratio": go_gdp_ratio,
            "productive_go_share": prod_share,
        }
        results.append(row)

        print(f"  GO total: ${go_total:,.1f}B | prod: ${go_productive:,.1f}B | trade: ${go_trading:,.1f}B")
        print(f"  TP* = ${tp_star:,.1f}B | C*m = ${cm_star:,.1f}B | GFP* = ${gfp_star:,.1f}B")
        print(f"  TP*/GDP = {tp_gdp_ratio:.3f} | GO/GDP = {go_gdp_ratio:.3f} | prod share = {prod_share:.3f}")

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY: TP*/GDP TRAJECTORY 1997-2024")
    print("=" * 80)
    print(f"{'Year':<6} {'GDP':>10} {'GO total':>10} {'TP*':>10} {'C*m':>10} {'GFP*':>10} "
          f"{'TP*/GDP':>8} {'GO/GDP':>8} {'Prod%':>7}")
    print("-" * 80)
    for r in results:
        print(f"{r['year']:<6} {r['gdp']:>10,.0f} {r['go_total']:>10,.0f} {r['tp_star']:>10,.0f} "
              f"{r['cm_star']:>10,.0f} {r['gfp_star']:>10,.0f} {r['tp_gdp_ratio']:>8.3f} "
              f"{r['go_gdp_ratio']:>8.3f} {r['productive_go_share']:>7.1%}")

    # Save results
    out_path = ROOT / "data" / "computed" / "detail_io_aggregates.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[SAVED] {out_path}")

    # Also save as CSV
    df = pd.DataFrame(results).set_index("year")
    csv_path = ROOT / "data" / "computed" / "detail_io_aggregates.csv"
    df.to_csv(csv_path)
    print(f"[SAVED] {csv_path}")


if __name__ == "__main__":
    main()
