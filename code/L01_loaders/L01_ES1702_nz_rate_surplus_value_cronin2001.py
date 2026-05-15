"""L01_ES1702 — Load NZ Rate of Surplus Value (Cronin 2001), external study (Wave 4).

Source: external_studies/Cronin2001_cronin_table2_ratios_1972_1995.csv, column `rate_of_surplus_value_pct`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "ES1702",
    subseries_id  = "ES1702-A",
    source_file   = EXTERNAL_STUDIES / "Cronin2001_cronin_table2_ratios_1972_1995.csv",
    source_column = "rate_of_surplus_value_pct",
    units         = "percent",
    unit_scale    = 1.0,
)


def run():
    df = LOADER.load()
    print(f"    [L01_ES1702] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()
