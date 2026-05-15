"""L01 helper — load Moos 2017 reconciled NSW dataset."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MOOS_CSV = ROOT / "data" / "source" / "external_studies" / "Moos_nsw_reconciled.csv"


def load_moos() -> pd.DataFrame:
    """Returns Moos's reconciled NSW data. Columns: year, labor_share, nsw1, nsw2,
    personal_income, compensation, plus adjusted_labor_share variants."""
    df = pd.read_csv(MOOS_CSV)
    return df


if __name__ == "__main__":
    df = load_moos()
    print(f"    [L01_moos] {len(df)} rows {df['year'].min()}-{df['year'].max()}; "
          f"NSW1 1959={df.iloc[0]['nsw1']:.2f}B, last={df.iloc[-1]['nsw1']:.2f}B")
