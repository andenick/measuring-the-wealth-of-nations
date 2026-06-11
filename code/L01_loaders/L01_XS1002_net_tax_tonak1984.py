"""L01_XS1002 — Load Net Tax on Labor (Tonak 1984), external study (Wave 4).

Source: external_studies/Tonak1984_table_X_net_tax_1952_1980.csv, column `net_tax`.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader


LOADER = BookColumnLoader(
    series_id     = "XS1002",
    subseries_id  = "XS1002-A",
    source_file   = EXTERNAL_STUDIES / "Tonak1984_table_X_net_tax_1952_1980.csv",
    source_column = "net_tax",
    units         = "billions_usd",
    unit_scale    = 1.0,
)


def run():
    df = LOADER.load()
    print(f"    [L01_XS1002] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.4f}, last={df.iloc[-1]['value']:.4f}")
    return df


if __name__ == "__main__":
    run()
