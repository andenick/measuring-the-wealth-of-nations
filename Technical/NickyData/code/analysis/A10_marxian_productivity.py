#!/usr/bin/env python3
"""A10 - Marxian vs Orthodox Productivity Measures (Table J.1).

q* = TPr / Hp  (Marxian: real total product per productive worker hour)
y* = GFPr / Hp (quasi-Marxian: real GFP per productive worker hour)
y  = GDPr / H  (orthodox: real GDP per total worker hour)

Book findings (1948-1989):
  q* grows 183% (2.83x), y grows only 90% (1.90x)
  Marxian productivity grows 2-3x faster than orthodox
  The "productivity slowdown" post-1972 is worse in y than in q*

Uses: GNP deflator (py) from FRED, TP* and GFP* from Table H.1/E.2,
      Hp from PAYEMS × (Lp/L ratio), GDP from NIPA

Outputs: outputs/analysis/marxian_productivity.json
         data/final-data/book/series/analytical_productivity.csv
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
import numpy as np
from utils.paths import SERIES_OUT, ANALYSIS_OUT, ensure_dirs


def generate():
    ensure_dirs()
    ANALYSIS_OUT.mkdir(parents=True, exist_ok=True)

    # Load TP* and GFP* from Table H.1
    h1_path = SERIES_OUT / "book_tableH1_1948_1989.csv"
    if not h1_path.exists():
        print("    [A10] Table H.1 not available")
        return {"status": "fail"}

    h1 = pd.read_csv(h1_path, comment="#", index_col="year")
    tp_star_book = h1["TP_star"]   # billions
    gfp_star_book = h1["GFP_star"] # billions

    # Extend with pipeline T501 (TP*) and T503 (GFP*) combined
    t501_path = SERIES_OUT / "T501.csv"
    t503_path = SERIES_OUT / "T503.csv"
    if t501_path.exists():
        t501 = pd.read_csv(t501_path, index_col="year")
        tp_ext = t501["combined"].dropna() if "combined" in t501.columns else pd.Series(dtype=float)
        tp_ext = tp_ext[tp_ext.index > 1989]
        tp_star = pd.concat([tp_star_book, tp_ext])
        tp_star = tp_star[~tp_star.index.duplicated(keep="first")].sort_index()
    else:
        tp_star = tp_star_book

    if t503_path.exists():
        t503 = pd.read_csv(t503_path, index_col="year")
        gfp_ext = t503["combined"].dropna() if "combined" in t503.columns else pd.Series(dtype=float)
        gfp_ext = gfp_ext[gfp_ext.index > 1989]
        gfp_star = pd.concat([gfp_star_book, gfp_ext])
        gfp_star = gfp_star[~gfp_star.index.duplicated(keep="first")].sort_index()
    else:
        gfp_star = gfp_star_book

    # Load GDP from T201 orthodox data
    t201_path = SERIES_OUT / "T201.csv"
    gdp = None
    if t201_path.exists():
        t201 = pd.read_csv(t201_path, index_col="year")
        if "GDP" in t201.columns:
            gdp = t201["GDP"]

    # Load productive labor share for Hp approximation
    t511_path = SERIES_OUT / "T511.csv"
    t511 = None
    if t511_path.exists():
        df = pd.read_csv(t511_path, index_col="year")
        t511 = df["combined"] if "combined" in df.columns else df.iloc[:, 0]

    # Load PAYEMS (total nonfarm employment, thousands)
    payems_path = Path(__file__).resolve().parents[2] / "data/raw-data/parsed/total_nonfarm_employment.csv")
    payems = None
    if payems_path.exists():
        pf = pd.read_csv(payems_path, index_col="year")
        payems = pf["value"]  # thousands

    # Approximate hours: average annual hours ≈ 2000 (stable per book)
    AVG_HOURS_PER_WORKER = 2000

    # GDP deflator from FRED GDPDEF (rebased to 1982=100, matching book's py)
    defl_path = Path(__file__).resolve().parents[2] / "data/raw-data/parsed/gdp_deflator.csv")
    deflator = None
    if defl_path.exists():
        defl_df = pd.read_csv(defl_path, index_col="year")
        if "deflator_1982" in defl_df.columns:
            deflator = defl_df["deflator_1982"] / 100.0  # convert to ratio (1982 = 1.0)

    results = {}
    out_data = {}

    common_years = sorted(tp_star.dropna().index)

    for yr in common_years:
        tp = tp_star.get(yr)
        gfp = gfp_star.get(yr)

        if tp is None or gfp is None:
            continue

        # Productive employment Lp (thousands)
        lp_l_ratio = t511.get(yr, 0.40) if t511 is not None else 0.40
        total_emp = payems.get(yr) if payems is not None else None
        if total_emp is None:
            continue

        lp = total_emp * lp_l_ratio  # thousands
        hp = lp * AVG_HOURS_PER_WORKER / 1e6  # millions of hours
        h_total = total_emp * AVG_HOURS_PER_WORKER / 1e6  # millions of hours

        if hp <= 0 or h_total <= 0:
            continue

        # Deflate to 1982 dollars if deflator available
        py = deflator.get(yr, 1.0) if deflator is not None else 1.0
        tp_real = tp / py if py > 0 else tp
        gfp_real = gfp / py if py > 0 else gfp

        # Productivity (1982$ billions / million hours = 1982$/hour)
        q_star = tp_real / hp      # Marxian: TPr/Hp
        y_star = gfp_real / hp     # quasi-Marxian: GFPr/Hp

        gdp_yr = gdp.get(yr) if gdp is not None else None
        y = (gdp_yr / py) / h_total if gdp_yr and gdp_yr > 0 and py > 0 else None

        out_data[yr] = {
            "q_star": q_star,
            "y_star": y_star,
            "y_orthodox": y,
            "Lp_thousands": lp,
            "Hp_million_hours": hp,
            "deflator_1982": py,
        }

        if yr in [1948, 1958, 1967, 1972, 1977, 1980, 1989]:
            results[yr] = {k: round(float(v), 2) if v else None for k, v in out_data[yr].items()}
            y_str = f", y={y:.2f}" if y else ""
            print(f"    [A10] {yr}: q*={q_star:.2f}, y*={y_star:.2f}{y_str} ($/hr)")

    if out_data:
        df = pd.DataFrame(out_data).T
        df.index.name = "year"
        out_path = SERIES_OUT / "analytical_productivity.csv"
        df.to_csv(out_path)

        # Growth rates
        if 1948 in out_data and 1989 in out_data:
            q48 = out_data[1948]["q_star"]
            q89 = out_data[1989]["q_star"]
            y48 = out_data[1948]["y_star"]
            y89 = out_data[1989]["y_star"]
            print(f"\n    [A10] Productivity growth 1948-1989:")
            print(f"    [A10]   q* (Marxian): {q48:.1f} -> {q89:.1f} = {(q89/q48-1)*100:.0f}% growth")
            print(f"    [A10]   y* (quasi-M): {y48:.1f} -> {y89:.1f} = {(y89/y48-1)*100:.0f}% growth")

        with open(ANALYSIS_OUT / "marxian_productivity.json", "w") as f:
            json.dump({"method": "Table J.1 methodology, nominal values (no deflator applied)",
                       "key_years": {str(k): v for k, v in results.items()},
                       "note": "Values are in nominal $/hr, not real. Book uses 1982=100 GNP deflator for real values."}, f, indent=2)

        print(f"    [A10] Saved {len(df)} years to analytical_productivity.csv")

    return {"status": "ok"}


if __name__ == "__main__":
    generate()
