"""Steps 6-9: Build integrated TP*/GDP series 1948-2024.

Combines:
- Book Table H.1 (1948-1989): TP* from Shaikh & Tonak's 82-sector SIC IO tables
- Detail-level data (1997-2024): TP* from 412-industry UnderlyingGDPbyIndustry
- Interpolation (1990-1996): between book's 1989 endpoint and data's 1997 start

Produces the complete TP*/GDP, C*m, GFP* trajectories showing how the productive
sector's share has evolved across the entire postwar period.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / "data" / "user-inputs" / "api_keys.env")


def load_book_h1() -> pd.DataFrame:
    """Load digitized Table H.1 from book (1948-1989)."""
    h1_path = ROOT.parent / "data" / "final-data" / "book" / "series" / "book_tableH1_1948_1989.csv"
    df = pd.read_csv(h1_path, comment="#")
    df = df.set_index("year")
    return df


def load_detail_aggregates() -> pd.DataFrame:
    """Load computed detail-level aggregates (1997-2024)."""
    path = ROOT / "data" / "computed" / "detail_io_aggregates.csv"
    df = pd.read_csv(path, index_col="year")
    return df


def get_fred_gdp() -> pd.Series:
    """Get GDP from FRED cache or hardcode."""
    # Current-vintage GDP in billions of dollars (FRED series GDP, annual)
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
    return pd.Series(gdp, name="GDP")


def main():
    print("=" * 80)
    print("INTEGRATED TP*/GDP SERIES 1948-2024")
    print("=" * 80)

    # Load sources
    h1 = load_book_h1()
    detail = load_detail_aggregates()
    gdp = get_fred_gdp()

    print(f"\nSource data:")
    print(f"  Book H.1: 1948-1989 ({len(h1)} years)")
    print(f"  Detail:   1997-2024 ({len(detail)} years)")
    print(f"  GDP:      1948-2024 ({len(gdp)} years)")

    # Build integrated series
    years = range(1948, 2025)
    integrated = pd.DataFrame(index=years, columns=[
        "tp_star", "cm_star", "gfp_star", "va_star", "gdp", "tp_gdp_ratio",
        "source", "productive_go_share", "go_total"
    ])
    integrated.index.name = "year"

    # 1948-1989: From book Table H.1
    for yr in range(1948, 1990):
        if yr in h1.index:
            row = h1.loc[yr]
            tp = row["TP_star"]
            gfp = row["GFP_star"]
            cm = tp - gfp  # C*m = TP* - GFP* = Mp
            va = row["VA_star"]
            g = gdp.get(yr, 0)
            integrated.loc[yr, "tp_star"] = tp
            integrated.loc[yr, "cm_star"] = cm
            integrated.loc[yr, "gfp_star"] = gfp
            integrated.loc[yr, "va_star"] = va
            integrated.loc[yr, "gdp"] = g
            integrated.loc[yr, "tp_gdp_ratio"] = tp / g if g > 0 else np.nan
            integrated.loc[yr, "source"] = "book_H1"

    # 1997-2024: From detail-level computation
    for yr in range(1997, 2025):
        if yr in detail.index:
            row = detail.loc[yr]
            integrated.loc[yr, "tp_star"] = row["tp_star"]
            integrated.loc[yr, "cm_star"] = row["cm_star"]
            integrated.loc[yr, "gfp_star"] = row["gfp_star"]
            integrated.loc[yr, "gdp"] = row["gdp"]
            integrated.loc[yr, "tp_gdp_ratio"] = row["tp_gdp_ratio"]
            integrated.loc[yr, "source"] = "detail_412"
            integrated.loc[yr, "productive_go_share"] = row["productive_go_share"]
            integrated.loc[yr, "go_total"] = row["go_total"]
            # VA* = GFP* - Dp (we'll add depreciation later)
            integrated.loc[yr, "va_star"] = row["gfp_star"]  # placeholder

    # 1990-1996: Interpolate between book 1989 endpoint and data 1997 start
    tp_1989 = float(integrated.loc[1989, "tp_star"])
    tp_1997 = float(integrated.loc[1997, "tp_star"])
    cm_1989 = float(integrated.loc[1989, "cm_star"])
    cm_1997 = float(integrated.loc[1997, "cm_star"])
    gfp_1989 = float(integrated.loc[1989, "gfp_star"])
    gfp_1997 = float(integrated.loc[1997, "gfp_star"])
    ratio_1989 = float(integrated.loc[1989, "tp_gdp_ratio"])
    ratio_1997 = float(integrated.loc[1997, "tp_gdp_ratio"])

    for yr in range(1990, 1997):
        t = (yr - 1989) / (1997 - 1989)  # 0 at 1989, 1 at 1997
        g = gdp.get(yr, 0)
        # Interpolate TP*/GDP ratio (log-linear for smooth decline)
        ratio = ratio_1989 * (ratio_1997 / ratio_1989) ** t
        tp = ratio * g
        # Interpolate C*m/TP* ratio
        cm_tp_1989 = cm_1989 / tp_1989
        cm_tp_1997 = cm_1997 / tp_1997
        cm_tp = cm_tp_1989 + t * (cm_tp_1997 - cm_tp_1989)
        cm = tp * cm_tp
        gfp = tp - cm

        integrated.loc[yr, "tp_star"] = tp
        integrated.loc[yr, "cm_star"] = cm
        integrated.loc[yr, "gfp_star"] = gfp
        integrated.loc[yr, "gdp"] = g
        integrated.loc[yr, "tp_gdp_ratio"] = ratio
        integrated.loc[yr, "source"] = "interpolated"

    # Convert to numeric
    for col in ["tp_star", "cm_star", "gfp_star", "va_star", "gdp", "tp_gdp_ratio",
                "productive_go_share", "go_total"]:
        integrated[col] = pd.to_numeric(integrated[col], errors="coerce")

    # Print summary
    print("\n" + "=" * 80)
    print("TP*/GDP RATIO TRAJECTORY 1948-2024")
    print("=" * 80)
    print(f"{'Year':<6} {'TP*':>10} {'C*m':>10} {'GFP*':>10} {'GDP':>10} {'TP*/GDP':>8} {'Source':>12}")
    print("-" * 70)
    # Print every 5 years + key years
    key_years = list(range(1948, 2025, 5)) + [1989, 1997, 2007, 2017, 2024]
    key_years = sorted(set(key_years))
    for yr in key_years:
        if yr in integrated.index:
            r = integrated.loc[yr]
            tp = r["tp_star"]
            cm = r["cm_star"]
            gfp = r["gfp_star"]
            g = r["gdp"]
            ratio = r["tp_gdp_ratio"]
            src = r["source"]
            if pd.notna(tp):
                print(f"{yr:<6} {tp:>10,.1f} {cm:>10,.1f} {gfp:>10,.1f} {g:>10,.1f} "
                      f"{ratio:>8.3f} {str(src):>12}")

    # Key period analysis
    print("\n" + "=" * 80)
    print("PERIOD ANALYSIS")
    print("=" * 80)
    periods = [
        ("Golden Age", 1948, 1973),
        ("Stagflation", 1973, 1980),
        ("Reagan Era", 1980, 1989),
        ("Transition (interp)", 1990, 1996),
        ("Clinton/Bush", 1997, 2007),
        ("GFC+Recovery", 2008, 2015),
        ("Late Expansion", 2016, 2019),
        ("COVID+Post", 2020, 2024),
    ]
    for name, start, end in periods:
        subset = integrated.loc[start:end, "tp_gdp_ratio"].dropna()
        if len(subset) > 0:
            print(f"  {name:<25} ({start}-{end}): mean TP*/GDP = {subset.mean():.3f} "
                  f"(start={subset.iloc[0]:.3f}, end={subset.iloc[-1]:.3f})")

    # Structural shift: productive share of GO
    print("\n" + "=" * 80)
    print("STRUCTURAL SHIFT: Productive Sector's Share of Total GO")
    print("=" * 80)
    prod_shares = integrated.loc[1997:2024, "productive_go_share"].dropna()
    if len(prod_shares) > 0:
        print(f"  1997: {prod_shares.iloc[0]:.1%}")
        print(f"  2007: {prod_shares.get(2007, np.nan):.1%}")
        print(f"  2017: {prod_shares.get(2017, np.nan):.1%}")
        print(f"  2024: {prod_shares.iloc[-1]:.1%}")
        print(f"  Decline 1997->2024: {(prod_shares.iloc[-1] - prod_shares.iloc[0]):.1%} percentage points")

    # Save
    out_path = ROOT / "data" / "computed" / "integrated_tp_series.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    integrated.to_csv(out_path)
    print(f"\n[SAVED] {out_path}")

    # Also save as JSON for pipeline consumption
    json_path = ROOT / "data" / "computed" / "integrated_tp_series.json"
    integrated_clean = integrated.where(pd.notna(integrated), None)
    records = []
    for yr in integrated_clean.index:
        row = integrated_clean.loc[yr].to_dict()
        row["year"] = int(yr)
        records.append(row)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    print(f"[SAVED] {json_path}")


if __name__ == "__main__":
    main()
