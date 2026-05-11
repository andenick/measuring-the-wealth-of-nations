"""Generic API data fetcher for FRED and BEA.

Reads api_sources.json for series definitions. Caches raw JSON responses
to raw-data/api/. Parses to annual DataFrames.
"""

import json
import os
from datetime import date
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from .paths import API_RAW, PARSED_RAW, API_DATA, CONFIG_DIR, ensure_dirs

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
BEA_BASE = "https://apps.bea.gov/api/data"


def _get_api_keys() -> dict:
    env_path = Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env"
    load_dotenv(env_path)
    return {
        "fred": os.environ.get("FRED_API_KEY", ""),
        "bea": os.environ.get("BEA_API_KEY", ""),
    }


def _load_api_config() -> dict:
    path = CONFIG_DIR / "api_sources.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _fetch_fred_series(series_id: str, api_key: str, start: str = "1948-01-01",
                        frequency: str = "a") -> pd.Series:
    cache = API_RAW / f"fred_{series_id}_{date.today().isoformat()}.json"
    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {
            "series_id": series_id, "api_key": api_key, "file_type": "json",
            "observation_start": start, "frequency": frequency,
            "aggregation_method": "avg",
        }
        resp = requests.get(FRED_BASE, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    rows = {}
    for o in data.get("observations", []):
        yr = int(o["date"][:4])
        if o["value"] != ".":
            rows[yr] = float(o["value"])
    return pd.Series(rows, name=series_id)


def _fetch_bea_dataset(dataset_config: dict, api_key: str) -> list[dict]:
    cache_name = f"bea_{dataset_config['TableName']}_{date.today().isoformat()}.json"
    cache = API_RAW / cache_name
    if cache.exists():
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        import requests
        params = {"UserID": api_key, "method": "GetData", "ResultFormat": "JSON"}
        params.update({k: v for k, v in dataset_config.items() if k not in ("description", "output")})
        resp = requests.get(BEA_BASE, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return data.get("BEAAPI", {}).get("Results", {}).get("Data", [])


def fetch_all():
    """Fetch all FRED and BEA data defined in api_sources.json."""
    ensure_dirs()
    config = _load_api_config()
    keys = _get_api_keys()

    if keys["fred"]:
        fred_config = config.get("fred", {}).get("series", {})
        sector_data = {}

        for series_id, spec in fred_config.items():
            try:
                s = _fetch_fred_series(series_id, keys["fred"],
                                        spec.get("start", "1948-01-01"),
                                        spec.get("frequency", "a"))
                if "output_group" in spec:
                    sector_data[spec.get("name", series_id)] = s
                elif "output" in spec:
                    df = s.to_frame(name="value")
                    df.index.name = "year"
                    if "rebase_year" in spec:
                        base_yr = spec["rebase_year"]
                        if base_yr in df.index:
                            df["deflator_1982"] = df["value"] / df.loc[base_yr, "value"] * 100
                    out = PARSED_RAW / spec["output"]
                    df.to_csv(out)
                print(f"    [fetch] FRED {series_id}: {len(s)} years")
            except Exception as e:
                print(f"    [fetch] FRED {series_id} failed: {e}")

        if sector_data:
            df = pd.DataFrame(sector_data)
            df.index.name = "year"
            df.columns = [c.lower().replace(" ", "_") for c in df.columns]
            df.to_csv(PARSED_RAW / "sector_employment.csv")
            print(f"    [fetch] Sector employment: {len(df)} years")

    if keys["bea"]:
        for ds_name, ds_config in config.get("bea", {}).get("datasets", {}).items():
            try:
                records = _fetch_bea_dataset(ds_config, keys["bea"])
                print(f"    [fetch] BEA {ds_name}: {len(records)} records")
            except Exception as e:
                print(f"    [fetch] BEA {ds_name} failed: {e}")


def load_nipa_csv(filename: str, line_filter: str = None) -> pd.DataFrame:
    """Load a pre-fetched NIPA CSV from Inputs/API_Data/BEA/."""
    path = API_DATA / "BEA" / filename
    if not path.exists():
        return pd.DataFrame()
    raw = pd.read_csv(path)
    if line_filter and "LineDescription" in raw.columns:
        raw = raw[raw["LineDescription"].str.contains(line_filter, case=False, na=False)]
    if "TimePeriod" in raw.columns and "DataValue" in raw.columns:
        rows = {}
        for _, r in raw.iterrows():
            yr = int(r["TimePeriod"])
            val_str = str(r["DataValue"]).replace(",", "")
            try:
                rows[yr] = float(val_str)
            except ValueError:
                continue
        return pd.Series(rows).to_frame(name="value")
    return raw


def load_parsed(filename: str) -> pd.DataFrame:
    """Load a parsed CSV from raw-data/parsed/."""
    path = PARSED_RAW / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, index_col="year")
