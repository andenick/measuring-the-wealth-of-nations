"""Compute Marxian aggregates from BEA GDP-by-Industry data using NAICS classification.

Uses the sector classification from naics_classification.py to split
BEA gross output data into productive, trading, and unproductive components.

Key formulas (from IO_METHODOLOGY_EXTRACTION.md):
  TV* = GO_p + GO_t  (Total Value = productive + trading gross output)
  C*m = M'_p         (Constant capital = productive intermediate inputs)
  GFP* = TV* - C*m   (Gross Final Product)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from lib.io.naics_classification import NAICS_CLASSIFICATION


def load_gdp_by_industry_go(csv_path: Path | str) -> pd.DataFrame:
    """Load BEA GDP-by-Industry gross output data.

    Returns DataFrame with columns: Year, Industry (NAICS code), GO (billions).
    """
    df = pd.read_csv(csv_path)
    # Standardize columns
    result = pd.DataFrame({
        "year": df["Year"].astype(int),
        "industry": df["Industry"].astype(str),
        "industry_name": df["IndustrYDescription"].astype(str),
        "go": pd.to_numeric(df["DataValue"], errors="coerce"),
    })
    return result.dropna(subset=["go"])


def compute_marxian_aggregates(go_data: pd.DataFrame) -> pd.DataFrame:
    """Compute productive/trading/unproductive gross output by year.

    Parameters
    ----------
    go_data : DataFrame with columns year, industry, go

    Returns
    -------
    DataFrame indexed by year with columns:
        GO_productive, GO_trading, GO_unproductive, GO_govt_enterprise,
        TV_star (= GO_p + GO_t), GO_total
    """
    records = []

    for year, group in go_data.groupby("year"):
        go_p = 0.0
        go_t = 0.0
        go_u = 0.0
        go_ge = 0.0
        go_ga = 0.0
        go_other = 0.0
        n_matched = 0

        for _, row in group.iterrows():
            code = str(row["industry"]).strip()
            go_val = float(row["go"])

            cls = NAICS_CLASSIFICATION.get(code)
            if cls == "productive":
                go_p += go_val
                n_matched += 1
            elif cls == "trading":
                go_t += go_val
                n_matched += 1
            elif cls == "unproductive":
                go_u += go_val
                n_matched += 1
            elif cls == "govt_enterprise":
                go_ge += go_val
                n_matched += 1
            elif cls == "govt_admin":
                go_ga += go_val
                n_matched += 1
            # Skip aggregate/summary codes (11, 21, 31G, etc.) to avoid double-counting

        # TV* = GO_productive + GO_trading (book formula)
        tv_star = go_p + go_t

        records.append({
            "year": int(year),
            "GO_productive": round(go_p, 2),
            "GO_trading": round(go_t, 2),
            "GO_unproductive": round(go_u, 2),
            "GO_govt_enterprise": round(go_ge, 2),
            "GO_govt_admin": round(go_ga, 2),
            "TV_star": round(tv_star, 2),
            "n_sectors_matched": n_matched,
        })

    result = pd.DataFrame(records).set_index("year").sort_index()
    return result
