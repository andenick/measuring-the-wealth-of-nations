"""L01_S504 — Load Variable Capital (V*).

Book-period (1948-1989): Appendix H.1 column V_star (productive wage bill, $bn).

Extension (1998-2024): V* is derived as V*/W × W:
  - V*/W from S512 extension (P02_S512 must run first).
  - W (total compensation) from BEA NIPA T20100 (1929-2025 annual compensation
    in $millions); converted to $billions.

This module exposes load_extension_components() so P02_S504 can splice the
derived extension onto the book series.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.bea_cache import BEA_CACHE  # noqa: E402
from utils.paths import BOOK_TABLES  # noqa: E402
from utils.series import BookColumnLoader  # noqa: E402


LOADER = BookColumnLoader(
    series_id     = "S504",
    subseries_id  = "S504-A",
    source_file   = BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column = "V_star",
    units         = "billions_usd",
)


def load_total_compensation() -> pd.DataFrame:
    """Read BEA NIPA T20100 annual compensation, returning year + value in $billions."""
    path = BEA_CACHE / "nipa_T20100_compensation_1929_2025.csv"
    if not path.exists():
        raise FileNotFoundError(f"BEA compensation cache missing: {path}")
    df = pd.read_csv(path)
    out = pd.DataFrame({
        "year":  df["year"].astype(int),
        "value": df["compensation_millions"].astype(float) / 1000.0,  # millions → billions
    })
    return out.sort_values("year").reset_index(drop=True)


def run():
    df = LOADER.load()
    print(f"    [L01_S504] book loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.2f}, last={df.iloc[-1]['value']:.2f}")
    try:
        w = load_total_compensation()
        print(f"    [L01_S504] BEA T20100 W loaded: {len(w)} rows "
              f"({w['year'].min()}-{w['year'].max()}); "
              f"W_1989={w.loc[w['year']==1989, 'value'].iloc[0]:.1f}, "
              f"W_2024={w.loc[w['year']==2024, 'value'].iloc[0] if (w['year']==2024).any() else float('nan'):.1f}")
    except Exception as exc:
        print(f"    [L01_S504] WARNING: total compensation unavailable: {exc}")
    return df


if __name__ == "__main__":
    run()
