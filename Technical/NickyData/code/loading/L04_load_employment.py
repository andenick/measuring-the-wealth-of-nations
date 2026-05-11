#!/usr/bin/env python3
"""L04 - Load Employment + FRED Data: T515, T516, PAYEMS, sector employment, GDP deflator.

Book data:  ch05/Employment_1948_1989.csv (T515=Lp thousands, T516=Lu thousands)
FRED data:  PAYEMS (total nonfarm employment, includes govt, for P06 extension)
            USTRADE/CEU5500000001/CEU9000000001 (trade/FIRE/govt for sector adjustment)
            GDPDEF (GDP deflator, rebased to 1982=100 for real productivity in A10)

Outputs:
  parsed-raw/T515_parsed.csv, T516_parsed.csv (book employment)
  parsed-raw/total_nonfarm_employment.csv (FRED PAYEMS)
  parsed-raw/sector_employment.csv (FRED trade/FIRE/govt)
  parsed-raw/gdp_deflator.csv (FRED GDPDEF, 1982=100)
Dependencies: None. Requires FRED_API_KEY in data/user-inputs/api_keys.env.
"""

import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from dotenv import load_dotenv

from utils.paths import ST_CHOPPED, PARSED_RAW, API_RAW, ensure_dirs
from utils.data_io import load_chopped_direct

SERIES_IDS = ["T515", "T516"]

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
SECTOR_SERIES = {
    "USTRADE": "trade_employment",
    "CEU5500000001": "fire_employment",
    "CEU9000000001": "government_employment",
}


def _get_fred_api_key() -> str:
    env_path = Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env"
    load_dotenv(env_path)
    return os.environ.get("FRED_API_KEY", "")


def _fetch_fred_annual(series_id: str, api_key: str, start: str = "1929-01-01") -> dict:
    cache = API_RAW / f"fred_{series_id}_{date.today().isoformat()}.json"
    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            return json.load(f)

    import requests
    params = {
        "series_id": series_id, "api_key": api_key, "file_type": "json",
        "observation_start": start, "frequency": "a", "aggregation_method": "avg",
    }
    resp = requests.get(FRED_BASE, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data


def _parse_fred_observations(data: dict, min_year: int = 1948) -> pd.Series:
    rows = {}
    for o in data.get("observations", []):
        yr = int(o["date"][:4])
        if o["value"] != "." and yr >= min_year:
            rows[yr] = float(o["value"])
    return pd.Series(rows)


def _fetch_payems(api_key: str, outputs: list):
    try:
        data = _fetch_fred_annual("PAYEMS", api_key, "1948-01-01")
        s = _parse_fred_observations(data)
        df = s.to_frame(name="value")
        df.index.name = "year"
        out_path = PARSED_RAW / "total_nonfarm_employment.csv"
        df.to_csv(out_path)
        outputs.append(str(out_path))
        cached = "cache" if (API_RAW / f"fred_PAYEMS_{date.today().isoformat()}.json").exists() else "FRED"
        print(f"    [L04] PAYEMS: {len(df)} years ({df.index.min()}-{df.index.max()}), thousands")
    except Exception as e:
        print(f"    [L04] PAYEMS fetch failed: {e}")


def _fetch_sector_employment(api_key: str, outputs: list):
    all_series = {}
    for fred_id, name in SECTOR_SERIES.items():
        try:
            data = _fetch_fred_annual(fred_id, api_key, "1948-01-01")
            all_series[name] = _parse_fred_observations(data)
            print(f"    [L04] {fred_id} -> {name}: {len(all_series[name])} years")
        except Exception as e:
            print(f"    [L04] {fred_id} failed: {e}")

    if all_series:
        df = pd.DataFrame(all_series)
        df.index.name = "year"
        out_path = PARSED_RAW / "sector_employment.csv"
        df.to_csv(out_path)
        outputs.append(str(out_path))


def _fetch_gdp_deflator(api_key: str, outputs: list):
    try:
        data = _fetch_fred_annual("GDPDEF", api_key, "1929-01-01")
        s = _parse_fred_observations(data, min_year=1929)
        df = s.to_frame(name="value")
        df.index.name = "year"
        if 1982 in df.index:
            base = df.loc[1982, "value"]
            df["deflator_1982"] = df["value"] / base * 100
        else:
            df["deflator_1982"] = df["value"]
        out_path = PARSED_RAW / "gdp_deflator.csv"
        df.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L04] GDPDEF: {len(df)} years, 1982 base")
    except Exception as e:
        print(f"    [L04] GDPDEF fetch failed: {e}")


def load():
    """Load book employment + fetch FRED data (PAYEMS, sectors, GDP deflator)."""
    ensure_dirs()

    # Book data
    source = ST_CHOPPED / "ch05" / "Employment_1948_1989.csv"
    if not source.exists():
        return {"series_id": SERIES_IDS[0], "status": "fail",
                "message": f"Source not found: {source}", "outputs": []}

    df = load_chopped_direct(source, columns=["T515", "T516"])
    outputs = []

    for sid in SERIES_IDS:
        if sid not in df.columns:
            print(f"    [L04] {sid}: column not found")
            continue
        out = df[[sid]].rename(columns={sid: "value"}).dropna()
        out_path = PARSED_RAW / f"{sid}_parsed.csv"
        out.to_csv(out_path)
        outputs.append(str(out_path))
        print(f"    [L04] {sid}: {len(out)} rows (thousands)")

    # FRED data
    api_key = _get_fred_api_key()
    if api_key:
        _fetch_payems(api_key, outputs)
        _fetch_sector_employment(api_key, outputs)
        _fetch_gdp_deflator(api_key, outputs)
    else:
        print("    [L04] FRED_API_KEY not found, skipping FRED fetches")

    return {
        "series_id": SERIES_IDS[0],
        "status": "ok",
        "message": f"Employment + FRED | {len(outputs)} files",
        "outputs": outputs,
    }
