"""L01_ES1502 — Load Managerial Unproductive Labor (Mohun 2013).

Source: Mohun_unproductive_decomposition_1948_1989.csv, column `Lum_mohun`.
Units: thousands of workers under Mohun's narrow productive classification.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader

LOADER = BookColumnLoader(
    series_id="ES1502", subseries_id="ES1502-A",
    source_file=EXTERNAL_STUDIES / "Mohun_unproductive_decomposition_1948_1989.csv",
    source_column="Lum_mohun",
    units="thousands", unit_scale=1.0,
)

def run():
    df = LOADER.load()
    print(f"    [L01_ES1502] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.0f}, last={df.iloc[-1]['value']:.0f}")
    return df

if __name__ == "__main__":
    run()
