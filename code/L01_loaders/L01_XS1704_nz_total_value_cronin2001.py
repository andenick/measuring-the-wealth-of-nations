"""L01_XS1704 — Load NZ Total Value (Cronin 2001), external study (Wave 4).

Source: external_studies/Cronin2001_cronin_table1_nzsna_classical_1972_1995.csv, column `total_value_mNZD`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "XS1704",
    subseries_id  = "XS1704-A",
    source_file   = EXTERNAL_STUDIES / "Cronin2001_cronin_table1_nzsna_classical_1972_1995.csv",
    source_column = "total_value_mNZD",
    units         = "millions_nzd",
    unit_scale    = 1.0,
)


def run():
    df = LOADER.load()
    print(f"    [L01_XS1704] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()
