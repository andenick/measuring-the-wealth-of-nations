"""Read FRED cached JSON responses."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .paths import ROOT


FRED_CACHE = ROOT / "data" / "raw" / "fred"


def load_fred_annual(filename: str) -> pd.DataFrame:
    """Load a FRED JSON observation file, aggregate to annual averages.

    Returns DataFrame: year, value.
    """
    path = FRED_CACHE / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    obs = data.get("observations", [])
    df = pd.DataFrame(obs)
    df["year"] = pd.to_datetime(df["date"]).dt.year
    df = df[df["value"] != "."]
    df["value"] = df["value"].astype(float)
    annual = df.groupby("year")["value"].mean().reset_index()
    return annual
