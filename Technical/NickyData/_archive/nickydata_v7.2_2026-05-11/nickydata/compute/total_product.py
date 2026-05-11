"""T501 (TP*), T502 (C*m), T503 (GFP*) — From Detail-Level IO Data.

Sources:
- 1948-1989: Book Table H.1 (Shaikh & Tonak's 82-sector SIC IO computation)
- 1990-1996: Log-linear interpolation of TP*/GDP ratio between book and NAICS
- 1997-2024: 412-industry detail-level UnderlyingGDPbyIndustry (BEA API)

The integrated series is pre-computed by compute_integrated_tp.py and stored in
data/computed/integrated_tp_series.csv. This module loads it directly.

TP*/GDP trajectory:
  1948: 1.62  (Golden Age peak — productive sector dominant)
  1973: 1.39  (end of Golden Age)
  1989: 1.35  (book's final year)
  1997: 1.13  (start of NAICS era)
  2017: 1.02  (near unity)
  2024: 0.99  (below 1.0 — unproductive sector > productive sector)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from .helpers import build_series, save_series, load_methodology

DEPENDS_ON = []

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def compute(data: dict, methodology: dict) -> dict[str, pd.DataFrame]:
    integrated_path = DATA_DIR / "computed" / "integrated_tp_series.csv"

    if integrated_path.exists():
        df = pd.read_csv(integrated_path, index_col="year")
        tp_star = df["tp_star"].dropna()
        cm_star = df["cm_star"].dropna()
        gfp_star = df["gfp_star"].dropna()
        print(f"    Loaded integrated series: {len(tp_star)} years ({int(tp_star.index.min())}-{int(tp_star.index.max())})")
        if 1948 in tp_star.index:
            gdp_1948 = df.loc[1948, "gdp"] if "gdp" in df.columns else 274.8
            print(f"    TP*(1948) = {tp_star[1948]:.1f}B, TP*/GDP = {tp_star[1948]/gdp_1948:.3f}")
        if 2017 in tp_star.index:
            gdp_2017 = df.loc[2017, "gdp"] if "gdp" in df.columns else 19485.4
            print(f"    TP*(2017) = {tp_star[2017]:,.1f}B, TP*/GDP = {tp_star[2017]/gdp_2017:.3f}")
    else:
        print("    WARNING: integrated_tp_series.csv not found. Run compute_integrated_tp.py first.")
        print("    Falling back to GDP-by-Industry summary method...")
        tp_star, cm_star, gfp_star = _fallback_compute(data, methodology)

    results = {
        "T501": build_series(tp_star, pd.Series(dtype=float)),
        "T502": build_series(cm_star, pd.Series(dtype=float)),
        "T503": build_series(gfp_star, pd.Series(dtype=float)),
    }
    for sid, sdf in results.items():
        save_series(sid, sdf)
        print(f"    {sid}: {len(sdf)} years")
    return results


def _fallback_compute(data: dict, methodology: dict):
    """Fallback: old GDP-by-Industry method if integrated data unavailable."""
    from nickydata.fetch.bea_nipa import parse_line

    nipa_gdp = data.get("nipa", {}).get("T10105", [])
    gdp_raw = parse_line(nipa_gdp, line_description="Gross domestic product")
    gdp = gdp_raw / 1e3 if len(gdp_raw) > 0 and gdp_raw.iloc[0] > 1000 else gdp_raw

    params = methodology.get("parameters", {})
    tp_star = gdp * params.get("fallback_tp_gdp_ratio", 1.05)
    cm_star = tp_star * params.get("fallback_cm_tp_ratio", 0.65)
    gfp_star = tp_star - cm_star
    return tp_star, cm_star, gfp_star
