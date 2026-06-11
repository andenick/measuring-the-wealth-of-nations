"""L01_XS1503 — Load Total Unproductive Labor (Mohun 2013).

Source: Mohun_unproductive_decomposition_1948_1989.csv, column `Lu_mohun`.
Units: thousands of workers under Mohun's narrow productive classification.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import EXTERNAL_STUDIES
from utils.series import BookColumnLoader

LOADER = BookColumnLoader(
    series_id="XS1503", subseries_id="XS1503-A",
    source_file=EXTERNAL_STUDIES / "Mohun_unproductive_decomposition_1948_1989.csv",
    source_column="Lu_mohun",
    units="thousands", unit_scale=1.0,
)

def run():
    df = LOADER.load()
    print(f"    [L01_XS1503] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.0f}, last={df.iloc[-1]['value']:.0f}")
    return df

if __name__ == "__main__":
    run()
