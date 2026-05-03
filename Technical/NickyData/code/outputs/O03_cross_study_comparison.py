#!/usr/bin/env python3
"""O03 - Cross-Study NSW Comparison: build multi-study comparison database.

Creates unified datasets comparing NSW estimates across methodologies and countries.

Output:
  - Outputs/Data/NSW_CROSS_STUDY/nsw_comparison.csv
  - Outputs/Data/EXPLOITATION_CROSS_STUDY/exploitation_comparison.csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from utils.paths import SERIES_OUT

NSW_OUTPUT = Path("D:/Arcanum/Projects/ST2/Outputs/Data/NSW_CROSS_STUDY")
EXPL_OUTPUT = Path("D:/Arcanum/Projects/ST2/Outputs/Data/EXPLOITATION_CROSS_STUDY")


def _load(sid):
    path = SERIES_OUT / f"{sid}.csv"
    if not path.exists():
        return pd.Series(dtype=float, name=sid)
    df = pd.read_csv(path, index_col=0)
    col = "combined" if "combined" in df.columns else df.columns[-1]
    return df[col].rename(sid)


def generate():
    NSW_OUTPUT.mkdir(parents=True, exist_ok=True)
    EXPL_OUTPUT.mkdir(parents=True, exist_ok=True)

    # === NSW Cross-Study Comparison ===
    nsw_series = {
        "T607_ST94_NSW": _load("T607"),           # Book Ch6 NSW (billions)
        "N1101_ST87_NetTransfer": _load("N1101"),  # ST 1987 net transfer rate
        "N1202_ST02_NSW_EC": _load("N1202"),       # ST 2002 NSW/EC
        "N1301_Moos_NSW_GDP": _load("N1301"),      # Moos NSW/GDP
        "N1302_Moos_NSW_EC": _load("N1302"),       # Moos NSW/EC
        "N1602_Turkey_NSW_GDP": _load("N1602"),    # Turkey NSW/GDP
    }

    nsw_df = pd.DataFrame(nsw_series)
    nsw_df.index.name = "year"
    nsw_path = NSW_OUTPUT / "nsw_comparison.csv"
    nsw_df.to_csv(nsw_path)

    n_years = len(nsw_df)
    n_studies = sum(1 for s in nsw_series.values() if len(s.dropna()) > 0)
    print(f"  NSW comparison: {n_years} years x {n_studies} studies")
    print(f"  Saved to {nsw_path}")

    # === Exploitation Cross-Study Comparison ===
    expl_series = {
        "T506_ST94_exploitation": _load("T506"),    # Book exploitation rate
        "N1401_Mohun_exploitation": _load("N1401"), # Mohun exploitation rate
        "N1404_ST_Mohun_ratio": _load("N1404"),     # ST/Mohun ratio
        "N1504_burden_ratio": _load("N1504"),       # Unproductive burden
    }

    expl_df = pd.DataFrame(expl_series)
    expl_df.index.name = "year"
    expl_path = EXPL_OUTPUT / "exploitation_comparison.csv"
    expl_df.to_csv(expl_path)

    n_years_e = len(expl_df)
    print(f"  Exploitation comparison: {n_years_e} years")
    print(f"  Saved to {expl_path}")

    # === Summary Statistics ===
    print("\n  === Cross-Study Summary ===")
    for name, s in nsw_series.items():
        s_clean = s.dropna()
        if len(s_clean) > 0:
            print(f"  {name}: {len(s_clean)} years, mean={float(s_clean.mean()):.4f}, range=[{float(s_clean.min()):.4f}, {float(s_clean.max()):.4f}]")

    return {"status": "ok", "nsw_path": str(nsw_path), "expl_path": str(expl_path)}


if __name__ == "__main__":
    generate()
