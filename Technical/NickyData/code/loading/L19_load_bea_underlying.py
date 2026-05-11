#!/usr/bin/env python3
"""L19 - Load BEA UnderlyingGDPbyIndustry: detail-level gross output and value added.

Fetches 412-industry detail GO (TableID=237) and summary VA (TableID=210)
from the UnderlyingGDPbyIndustry dataset, applies Appendix F classification,
and computes Marxian aggregates (TP*, C*m, GFP*) for 1997-2024.

Inputs:  BEA API (UnderlyingGDPbyIndustry dataset)
         config/naics_detail_classification.json (412-industry classification)
         config/classifications.json (summary IO classification for VA)
Outputs: raw-data/parsed/detail_io_aggregates.csv
         raw-data/parsed/integrated_tp_series.csv
Dependencies: None (standalone data fetch + computation)
"""

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from utils.paths import PARSED_RAW, CONFIG, ensure_dirs

SERIES_IDS = []
PRIORITY = 19

BASE_URL = "https://apps.bea.gov/api/data"
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cache"

TABLES = {
    "go_detail": 237,
    "va_underlying": 210,
}


def _get_api_key() -> str:
    api_key = os.environ.get("BEA_API_KEY", "")
    if not api_key:
        from dotenv import load_dotenv
        env_paths = [
            Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env",
            Path(__file__).resolve().parent.parent.parent.parent / "data" / "user-inputs" / "api_keys.env",
        ]
        for p in env_paths:
            if p.exists():
                load_dotenv(p)
                api_key = os.environ.get("BEA_API_KEY", "")
                if api_key:
                    break
    return api_key


def _fetch_underlying(table_key: str, year: int, api_key: str) -> list[dict]:
    """Fetch a single year from the UnderlyingGDPbyIndustry dataset."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    table_id = TABLES[table_key]
    cache_path = CACHE_DIR / f"bea_underlying_{table_key}_{year}.json"

    if cache_path.exists():
        with open(cache_path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "UserID": api_key,
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
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        time.sleep(0.3)

    results = data.get("BEAAPI", {}).get("Results", {})
    if isinstance(results, list) and results:
        return results[0].get("Data", [])
    elif isinstance(results, dict):
        return results.get("Data", [])
    return []


def _records_to_dict(records: list[dict]) -> dict[str, float]:
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


def _load_classification():
    """Load 412-industry NAICS detail classification."""
    cls_path = CONFIG / "naics_detail_classification.json"
    if not cls_path.exists():
        # Try nickydata config location
        alt = Path(__file__).resolve().parent.parent.parent / "nickydata" / "config" / "naics_detail_classification.json"
        if alt.exists():
            cls_path = alt
        else:
            return None, None
    with open(cls_path, encoding="utf-8") as f:
        cls_data = json.load(f)
    return cls_data["classification"], cls_data.get("descriptions", {})


def _load_io_classification():
    """Load summary-level IO classification for VA computation."""
    io_cls_path = CONFIG / "classifications.json"
    if not io_cls_path.exists():
        alt = Path(__file__).resolve().parent.parent.parent / "nickydata" / "config" / "classifications.json"
        if alt.exists():
            io_cls_path = alt
        else:
            return set(), set()
    with open(io_cls_path, encoding="utf-8") as f:
        io_cls_data = json.load(f)
    naics_io = {k: v for k, v in io_cls_data.get("naics_io", {}).items() if not k.startswith("_")}
    return (
        {c for c, v in naics_io.items() if v == "productive"},
        {c for c, v in naics_io.items() if v == "trading"},
    )


def _compute_detail_aggregates(api_key: str, classification: dict) -> pd.DataFrame:
    """Fetch and compute detail-level Marxian aggregates for 1997-2024."""
    productive_codes = {c for c, v in classification.items() if v == "productive"}
    trading_codes = {c for c, v in classification.items() if v == "trading"}
    io_productive, io_trading = _load_io_classification()

    results = []
    for year in range(1997, 2025):
        go_records = _fetch_underlying("go_detail", year, api_key)
        go_data = _records_to_dict(go_records)

        va_records = _fetch_underlying("va_underlying", year, api_key)
        va_data = _records_to_dict(va_records)

        go_productive = sum(v for c, v in go_data.items() if c in productive_codes)
        go_trading = sum(v for c, v in go_data.items() if c in trading_codes)
        tp_star = go_productive + go_trading

        va_productive = sum(va_data.get(c, 0) for c in io_productive if c in va_data)
        va_trading = sum(va_data.get(c, 0) for c in io_trading if c in va_data)
        gfp_star = va_productive + va_trading
        cm_star = tp_star - gfp_star

        go_total = sum(go_data.values())
        results.append({
            "year": year,
            "tp_star": tp_star,
            "cm_star": cm_star,
            "gfp_star": gfp_star,
            "go_productive": go_productive,
            "go_trading": go_trading,
            "go_total": go_total,
            "productive_go_share": go_productive / go_total if go_total > 0 else 0,
        })

    return pd.DataFrame(results).set_index("year")


def _build_integrated_series(detail_df: pd.DataFrame) -> pd.DataFrame:
    """Build integrated TP*/GDP series combining book H.1 + interpolation + detail data."""
    # Load book Table H.1
    project_root = Path(__file__).resolve().parent.parent.parent
    h1_path = project_root / "data" / "final-data" / "book" / "series" / "book_tableH1_1948_1989.csv"
    if not h1_path.exists():
        print(f"    [L19] Book Table H.1 not found at {h1_path}")
        return pd.DataFrame()

    h1 = pd.read_csv(h1_path, comment="#").set_index("year")

    # GDP series (hardcoded from FRED — current vintage)
    gdp = {
        1948: 274.8, 1949: 272.8, 1950: 300.2, 1951: 347.3, 1952: 367.7,
        1953: 389.7, 1954: 391.1, 1955: 426.2, 1956: 450.1, 1957: 474.9,
        1958: 482.0, 1959: 522.5, 1960: 543.3, 1961: 563.3, 1962: 605.1,
        1963: 638.6, 1964: 685.8, 1965: 743.7, 1966: 815.0, 1967: 861.7,
        1968: 942.5, 1969: 1019.9, 1970: 1075.9, 1971: 1167.8, 1972: 1282.4,
        1973: 1428.5, 1974: 1548.8, 1975: 1688.9, 1976: 1877.6, 1977: 2086.0,
        1978: 2356.6, 1979: 2632.1, 1980: 2862.5, 1981: 3211.0, 1982: 3345.0,
        1983: 3638.1, 1984: 4040.7, 1985: 4346.7, 1986: 4590.2, 1987: 4870.2,
        1988: 5252.6, 1989: 5657.7, 1990: 5979.6, 1991: 6174.0, 1992: 6539.3,
        1993: 6878.7, 1994: 7308.8, 1995: 7664.1, 1996: 8100.2,
        1997: 8577.6, 1998: 9062.8, 1999: 9631.2, 2000: 10252.3, 2001: 10581.9,
        2002: 10936.4, 2003: 11458.2, 2004: 12213.7, 2005: 13036.6, 2006: 13814.6,
        2007: 14451.9, 2008: 14712.8, 2009: 14448.9, 2010: 14992.1, 2011: 15542.6,
        2012: 16197.0, 2013: 16785.0, 2014: 17527.3, 2015: 18224.8, 2016: 18745.1,
        2017: 19485.4, 2018: 20533.1, 2019: 21381.0, 2020: 21060.5, 2021: 23315.1,
        2022: 25462.7, 2023: 27360.9, 2024: 28780.8,
    }

    years = range(1948, 2025)
    cols = ["tp_star", "cm_star", "gfp_star", "va_star", "gdp", "tp_gdp_ratio",
            "source", "productive_go_share", "go_total"]
    integrated = pd.DataFrame(index=years, columns=cols)
    integrated.index.name = "year"

    # Era 1: Book (1948-1989)
    for yr in range(1948, 1990):
        if yr in h1.index:
            row = h1.loc[yr]
            tp = row["TP_star"]
            gfp_val = row["GFP_star"]
            g = gdp.get(yr, 0)
            integrated.loc[yr, "tp_star"] = tp
            integrated.loc[yr, "cm_star"] = tp - gfp_val
            integrated.loc[yr, "gfp_star"] = gfp_val
            integrated.loc[yr, "va_star"] = row.get("VA_star", gfp_val)
            integrated.loc[yr, "gdp"] = g
            integrated.loc[yr, "tp_gdp_ratio"] = tp / g if g > 0 else np.nan
            integrated.loc[yr, "source"] = "book_H1"

    # Era 3: Detail data (1997-2024)
    for yr in range(1997, 2025):
        if yr in detail_df.index:
            row = detail_df.loc[yr]
            g = gdp.get(yr, 0)
            integrated.loc[yr, "tp_star"] = row["tp_star"]
            integrated.loc[yr, "cm_star"] = row["cm_star"]
            integrated.loc[yr, "gfp_star"] = row["gfp_star"]
            integrated.loc[yr, "gdp"] = g
            integrated.loc[yr, "tp_gdp_ratio"] = row["tp_star"] / g if g > 0 else np.nan
            integrated.loc[yr, "source"] = "detail_412"
            integrated.loc[yr, "productive_go_share"] = row["productive_go_share"]
            integrated.loc[yr, "go_total"] = row["go_total"]
            integrated.loc[yr, "va_star"] = row["gfp_star"]

    # Era 2: Log-linear interpolation (1990-1996)
    tp_1989 = float(integrated.loc[1989, "tp_star"])
    tp_1997 = float(integrated.loc[1997, "tp_star"])
    cm_1989 = float(integrated.loc[1989, "cm_star"])
    cm_1997 = float(integrated.loc[1997, "cm_star"])
    ratio_1989 = float(integrated.loc[1989, "tp_gdp_ratio"])
    ratio_1997 = float(integrated.loc[1997, "tp_gdp_ratio"])

    for yr in range(1990, 1997):
        t = (yr - 1989) / (1997 - 1989)
        g = gdp.get(yr, 0)
        ratio = ratio_1989 * (ratio_1997 / ratio_1989) ** t
        tp = ratio * g
        cm_tp_1989 = cm_1989 / tp_1989
        cm_tp_1997 = cm_1997 / tp_1997
        cm = tp * (cm_tp_1989 + t * (cm_tp_1997 - cm_tp_1989))
        integrated.loc[yr, "tp_star"] = tp
        integrated.loc[yr, "cm_star"] = cm
        integrated.loc[yr, "gfp_star"] = tp - cm
        integrated.loc[yr, "gdp"] = g
        integrated.loc[yr, "tp_gdp_ratio"] = ratio
        integrated.loc[yr, "source"] = "interpolated"

    for col in ["tp_star", "cm_star", "gfp_star", "va_star", "gdp", "tp_gdp_ratio",
                "productive_go_share", "go_total"]:
        integrated[col] = pd.to_numeric(integrated[col], errors="coerce")

    return integrated


def load():
    """Load detail-level BEA data, classify, compute aggregates, build integrated series."""
    ensure_dirs()
    steps = []

    classification, descriptions = _load_classification()
    if classification is None:
        msg = "naics_detail_classification.json not found"
        print(f"    [L19] FAIL: {msg}")
        return {"series_id": "L19", "status": "fail", "steps": [msg], "outputs": []}

    api_key = _get_api_key()
    if not api_key:
        msg = "BEA_API_KEY not found"
        print(f"    [L19] FAIL: {msg}")
        return {"series_id": "L19", "status": "fail", "steps": [msg], "outputs": []}

    counts = {}
    for v in classification.values():
        counts[v] = counts.get(v, 0) + 1
    steps.append(f"Classification: {counts}")

    # Compute detail aggregates
    detail_df = _compute_detail_aggregates(api_key, classification)
    detail_path = PARSED_RAW / "detail_io_aggregates.csv"
    detail_df.to_csv(detail_path)
    steps.append(f"Detail aggregates: {len(detail_df)} years ({detail_df.index.min()}-{detail_df.index.max()})")
    print(f"    [L19] Detail IO aggregates: {len(detail_df)} years")

    # Build integrated series
    integrated = _build_integrated_series(detail_df)
    integ_path = PARSED_RAW / "integrated_tp_series.csv"
    integrated.to_csv(integ_path)
    steps.append(f"Integrated series: {len(integrated)} years")
    tp_start = float(integrated.loc[1948, "tp_gdp_ratio"])
    tp_end = float(integrated.loc[2024, "tp_gdp_ratio"])
    print(f"    [L19] Integrated TP*/GDP: {tp_start:.3f} (1948) → {tp_end:.3f} (2024)")

    return {
        "series_id": "L19",
        "status": "ok",
        "steps": steps,
        "outputs": [str(detail_path), str(integ_path)],
    }
