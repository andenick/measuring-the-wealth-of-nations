"""L01_ES1402 — Load Productive Labor Share — Mohun Classification (Mohun 2005), external study (Wave 4).

Source: external_studies/Mohun_mohun_employment_annual_1948_1989.csv, column `Lp_mohun_L_ratio`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "ES1402",
    subseries_id  = "ES1402-A",
    source_file   = EXTERNAL_STUDIES / "Mohun_mohun_employment_annual_1948_1989.csv",
    source_column = "Lp_mohun_L_ratio",
    units         = "share",
    unit_scale    = 1.0,
)


def run():
    df = LOADER.load()
    print(f"    [L01_ES1402] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()
