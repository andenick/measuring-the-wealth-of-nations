"""L01_S617 — Load Employee Compensation (EC) from Appendix H.1.

EC is the total wage bill (productive + unproductive labor) — the denominator
for ST 1987 and ST 2002 NSW ratios (ES1101-1103, ES1201-1202).
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.paths import BOOK_TABLES
from utils.series import BookColumnLoader

LOADER = BookColumnLoader(
    series_id="S617", subseries_id="S617-A",
    source_file=BOOK_TABLES / "book_tableH1_1948_1989.csv",
    source_column="EC",
    units="billions_usd", unit_scale=1.0,
)

def run():
    df = LOADER.load()
    print(f"    [L01_S617] loaded {len(df)} rows; "
          f"period {df['year'].min()}-{df['year'].max()}; "
          f"first={df.iloc[0]['value']:.2f}, last={df.iloc[-1]['value']:.2f}")
    return df

if __name__ == "__main__":
    run()
