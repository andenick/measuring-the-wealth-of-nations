"""Vintage impact analysis — compares current vs historical NIPA data.

Uses ALFRED API to fetch 1994-vintage NIPA data (earliest available)
and quantify how much NIPA revisions affect Marxian measures.

The book used BEA (1986) data. ALFRED starts at ~1994. The 1994 vintage
is pre-1996/1999/2003/2009/2013/2018/2023 comprehensive revisions,
making it the closest available proxy for the book's data.
"""

import json
import pandas as pd
from pathlib import Path
from .helpers import save_series

DEPENDS_ON = []

# Key FRED series that mirror NIPA data
VINTAGE_SERIES = {
    "GDP": "Gross Domestic Product (billions)",
    "COE": "Compensation of Employees (billions)",
    "A576RC1": "Compensation of employees (alt FRED ID, billions)",
    "W209RC1": "Personal Income (alt FRED ID, billions)",
}

BENCHMARK_YEARS = [1948, 1958, 1967, 1972, 1977, 1980, 1989]
# Note: ALFRED doesn't support annual-frequency NIPA series with realtime parameters.
# We document the vintage gap qualitatively instead of computing it empirically.
VINTAGE_YEARS = []  # Empty — ALFRED comparison not available for annual NIPA

BOOK_VALUES = {
    "GDP": {1948: 274.5, 1958: 467.8, 1972: 1280.0, 1989: 5484.0},
    "V_star": {1948: 88.41, 1958: 127.72, 1972: 324.30, 1989: 1206.40},
    "e_star": {1948: 1.70, 1958: 2.01, 1972: 1.99, 1989: 2.44},
}


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    """Run vintage comparison analysis."""
    import os
    from dotenv import load_dotenv

    env_paths = [
        Path(__file__).resolve().parent.parent / "api_keys.env",
        Path(__file__).resolve().parent.parent.parent / "data" / "user-inputs" / "api_keys.env",
    ]
    for p in env_paths:
        if p.exists():
            load_dotenv(p)
            break

    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key:
        print("    [vintage] No FRED API key, skipping")
        return {}

    from nickydata.fetch.fred import compare_vintages, fetch_vintage, fetch

    results = {}
    all_comparisons = {}

    print("  Vintage Analysis:")

    for series_id, desc in VINTAGE_SERIES.items():
        print(f"    {series_id} ({desc}):")
        try:
            comparison = compare_vintages(series_id, api_key, VINTAGE_YEARS, BENCHMARK_YEARS)
            all_comparisons[series_id] = comparison

            if "current" in comparison.columns and "v1994" in comparison.columns:
                for yr in BENCHMARK_YEARS:
                    if yr in comparison.index:
                        cur = comparison.loc[yr, "current"]
                        v94 = comparison.loc[yr, "v1994"]
                        if pd.notna(cur) and pd.notna(v94) and v94 != 0:
                            pct = (cur - v94) / v94 * 100
                            print(f"      {yr}: 1994={v94:,.0f}  current={cur:,.0f}  revision={pct:+.1f}%")
            elif "current" in comparison.columns:
                print(f"      1994 vintage not available for {series_id}")
                for yr in BENCHMARK_YEARS:
                    if yr in comparison.index:
                        print(f"      {yr}: current={comparison.loc[yr, 'current']:,.0f}")

        except Exception as e:
            print(f"      FAIL: {e}")

    # Compare with book values
    print("\n    Book comparison (V* and e at benchmark years):")
    comp_series = all_comparisons.get("A576RC1")  # Compensation of employees
    if comp_series is not None and "v1994" in comp_series.columns:
        for yr in [1948, 1972, 1989]:
            if yr in comp_series.index:
                ec_1994 = comp_series.loc[yr, "v1994"]
                ec_current = comp_series.loc[yr, "current"]
                v_star_book = BOOK_VALUES["V_star"].get(yr, 0)
                if v_star_book > 0 and ec_1994 > 0:
                    # Book V*/EC ratio
                    vw_book = v_star_book / (ec_1994 / 1e3) if ec_1994 > 100 else v_star_book / ec_1994
                    print(f"      {yr}: EC_1994={ec_1994:,.0f}  V*_book={v_star_book:.1f}bn  implied V*/EC={vw_book:.3f}")

    # Save analysis with current values + book comparison
    out_dir = Path(__file__).resolve().parent.parent / "data" / "computed"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Current-vintage values at benchmark years
    current_values = {}
    for series_id, comparison in all_comparisons.items():
        if "current" in comparison.columns:
            vals = {}
            for yr in BENCHMARK_YEARS:
                if yr in comparison.index:
                    v = comparison.loc[yr, "current"]
                    if pd.notna(v):
                        vals[str(yr)] = round(float(v), 1)
            if vals:
                current_values[series_id] = vals

    # Book comparison at key years
    book_comparison = {}
    for yr in [1948, 1972, 1989]:
        entry = {"year": yr}
        if "GDP" in current_values:
            entry["GDP_current"] = current_values["GDP"].get(str(yr))
            entry["GDP_book"] = BOOK_VALUES["GDP"].get(yr)
            if entry["GDP_current"] and entry["GDP_book"]:
                entry["GDP_revision_pct"] = round((entry["GDP_current"] - entry["GDP_book"]) / entry["GDP_book"] * 100, 1)
        entry["V_star_book"] = BOOK_VALUES["V_star"].get(yr)
        entry["e_star_book"] = BOOK_VALUES["e_star"].get(yr)
        book_comparison[yr] = entry

    analysis_path = out_dir / "vintage_analysis.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump({
            "description": "NIPA vintage comparison: current vs book (1986) data",
            "current_vintage": "2025-2026 (post-2023 comprehensive revision)",
            "book_vintage": "BEA (1986) publication",
            "alfred_status": "ALFRED does not support annual-frequency NIPA series with realtime parameters. Historical vintage comparison not available via API.",
            "current_values": current_values,
            "book_comparison": book_comparison,
            "known_revisions": [
                "1991: Computer investment capitalized",
                "1996: Chain-type price indexes",
                "1999: Software as investment, SIC to NAICS",
                "2003: Government investment capitalized",
                "2009: R&D as investment (+3% GDP)",
                "2013: Entertainment originals, pension accounting",
                "2018: Methodological updates",
                "2023: Latest comprehensive revision"
            ],
        }, f, indent=2)

    print(f"\n    Saved vintage analysis to {analysis_path.name}")
    return results
