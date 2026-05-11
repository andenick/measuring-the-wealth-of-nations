#!/usr/bin/env python3
"""AS2 NickyData v7.0 — Marxian National Accounts from Public Data.

Computes the complete Marxian national accounting framework for the US economy
(1947-2024) using only public BEA, BLS, and FRED data.

Methodology: Shaikh & Tonak (1994) "Measuring the Wealth of Nations"

Usage:
    python -m nickydata.run                 # Full pipeline
    python -m nickydata.run --fetch-only    # Fetch data only
    python -m nickydata.run --compute-only  # Compute only (using cached data)
    python -m nickydata.run --test          # Full + validation
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

VERSION = "7.0.0"


def _load_api_keys() -> dict:
    """Load API keys from environment or .env file."""
    from dotenv import load_dotenv
    for env_path in [
        ROOT / "api_keys.env",
        ROOT.parent / "data" / "user-inputs" / "api_keys.env",
    ]:
        if env_path.exists():
            load_dotenv(env_path)
            break

    return {
        "fred": os.environ.get("FRED_API_KEY", ""),
        "bea": os.environ.get("BEA_API_KEY", ""),
    }


def fetch_all_data(keys: dict) -> dict:
    """Phase 1: Fetch all public data from APIs."""
    print("\n  == FETCH ==")
    data = {}

    # FRED series
    from nickydata.fetch import fred, bls
    if keys["fred"]:
        print("  FRED:")
        data["payems"] = fred.fetch("PAYEMS", keys["fred"], start="1939-01-01", min_year=1939)
        print(f"    PAYEMS: {len(data['payems'])} years")

        data["gdp_deflator"] = fred.fetch_deflator(keys["fred"])
        print(f"    GDPDEF: {len(data['gdp_deflator'])} years (1982=100)")

        data["tcu"] = fred.fetch("TCU", keys["fred"], start="1967-01-01", min_year=1967)
        print(f"    TCU: {len(data['tcu'])} years")

        data["bls_ratios"] = bls.fetch_production_worker_ratios(keys["fred"])
        print(f"    BLS ratios: {len(data['bls_ratios'])} years x {len(data['bls_ratios'].columns)} sectors")

        data["bls_wages"] = bls.fetch_production_worker_wages(keys["fred"])
        print(f"    BLS wages: {len(data['bls_wages'])} years x {len(data['bls_wages'].columns)} sectors")

        data["bls_counts"] = bls.fetch_production_worker_counts(keys["fred"])
        print(f"    BLS counts: {len(data['bls_counts'])} years x {len(data['bls_counts'].columns)} sectors")

        data["employment"] = bls.fetch_employment_by_sector(keys["fred"])
        print(f"    Employment: {len(data['employment'])} years x {len(data['employment'].columns)} sectors")

        data["cofc"] = fred.fetch("COFC", keys["fred"], start="1929-01-01", min_year=1929)
        print(f"    COFC (depreciation): {len(data['cofc'])} years")

    # BEA NIPA
    from nickydata.fetch import bea_nipa
    if keys["bea"]:
        print("  BEA NIPA:")
        nipa_tables = {
            "T10105": "GDP components",
            "T10705": "Gross output by industry",
            "T20100": "Personal income",
            "T30100": "Govt receipts/expenditures",
            "T30200": "Federal government",
            "T30300": "State/local government",
            "T30700": "Social insurance contributions",
            "T31200": "Social benefits",
            "T31600": "Govt consumption by function",
            "T60200D": "Compensation by industry",
            "T60500D": "FTE by industry",
            "T60600D": "Wages and salaries by industry",
            "T60100D": "GDP (value added) by industry",
            "T61000D": "Persons engaged in production by industry",
        }
        data["nipa"] = {}
        for table_name, desc in nipa_tables.items():
            try:
                records = bea_nipa.fetch_table(table_name, keys["bea"])
                data["nipa"][table_name] = records
                print(f"    {table_name}: {len(records)} records ({desc})")
            except Exception as e:
                print(f"    {table_name}: FAIL ({e})")

    # BEA IO benchmarks
    from nickydata.fetch import bea_io
    if keys["bea"]:
        print("  BEA IO:")
        data["io"] = {}
        for year in bea_io.NAICS_YEARS:
            try:
                use = bea_io.fetch_naics_io(year, "Use", keys["bea"])
                req = bea_io.fetch_naics_io(year, "Requirements", keys["bea"])
                data["io"][year] = {"use": use, "requirements": req}
                print(f"    {year}: Use={len(use)} records, Req={len(req)} records")
            except Exception as e:
                print(f"    {year}: FAIL ({e})")

    # BEA Fixed Assets
    from nickydata.fetch import bea_fixed_assets
    if keys["bea"]:
        print("  BEA Fixed Assets:")
        try:
            fa_records = bea_fixed_assets.fetch(keys["bea"])
            data["fixed_assets"] = fa_records
            print(f"    FAAt401: {len(fa_records)} records")
        except Exception as e:
            print(f"    FAAt401: FAIL ({e})")

    return data


def compute_all(data: dict) -> dict:
    """Phase 2: Compute all Marxian series from fetched data."""
    print("\n  == COMPUTE ==")
    all_series = {}

    with open(ROOT / "config" / "methodology.json", encoding="utf-8") as f:
        methodology = json.load(f)

    # Import compute modules in dependency order
    from nickydata.compute import (
        total_product, employment, variable_capital,
        exploitation, profit_rate,
        taxes, benefits, nsw,
        analytical, io_matrices, period_analysis,
        vintage_analysis,
    )

    # Share in-memory series store so modules can read each other's output
    from nickydata.compute.helpers import set_series_store
    set_series_store(all_series)

    compute_order = [
        ("Revenue (T501-T503)", total_product),
        ("Employment (T511-T516)", employment),
        ("Variable Capital (T504-T505)", variable_capital),
        ("Exploitation (T506-T507)", exploitation),
        ("Profit Rate (T513-T514)", profit_rate),
        ("Taxes (T601-T604)", taxes),
        ("Benefits (T605-T606)", benefits),
        ("NSW (T607-T609)", nsw),
        ("Analytical (A07-A10)", analytical),
        ("IO Matrices", io_matrices),
        ("Period Analysis", period_analysis),
        ("Vintage Analysis", vintage_analysis),
    ]

    for name, module in compute_order:
        print(f"  {name}:")
        try:
            result = module.compute(data, methodology)
            all_series.update(result)
        except Exception as e:
            print(f"    FAIL: {e}")

    return all_series


def validate_all(series: dict) -> list:
    """Phase 3: Run validation checks."""
    print("\n  == VALIDATE ==")
    checks = []
    print("    (validation not yet implemented)")
    return checks


def output_all(series: dict):
    """Phase 4: Generate output files."""
    print("\n  == OUTPUT ==")
    out_dir = ROOT / "data" / "computed"
    out_dir.mkdir(parents=True, exist_ok=True)

    for sid, df in series.items():
        path = out_dir / f"{sid}.csv"
        df.to_csv(path)

    print(f"    {len(series)} series written to {out_dir}")


def main():
    parser = argparse.ArgumentParser(description=f"AS2 NickyData v{VERSION}")
    parser.add_argument("--fetch-only", action="store_true")
    parser.add_argument("--compute-only", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    print(f"\n  AS2 NickyData v{VERSION}")
    print(f"  Marxian National Accounts from Public Data")
    print(f"  Methodology: Shaikh & Tonak (1994)")
    print(f"  {'=' * 45}")

    start = time.time()
    keys = _load_api_keys()

    if not keys["fred"] and not keys["bea"] and not args.compute_only:
        print("\n  ERROR: No API keys found.")
        print("  Set FRED_API_KEY and BEA_API_KEY in environment or api_keys.env")
        sys.exit(1)

    if args.fetch_only:
        fetch_all_data(keys)
    elif args.compute_only:
        data = fetch_all_data(keys) if (keys["fred"] or keys["bea"]) else {}
        series = compute_all(data)
        output_all(series)
    else:
        data = fetch_all_data(keys)
        series = compute_all(data)
        output_all(series)
        if args.test:
            validate_all(series)

    elapsed = time.time() - start
    print(f"\n  Done in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
