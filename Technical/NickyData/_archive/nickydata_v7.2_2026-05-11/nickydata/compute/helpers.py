"""Shared helpers for compute modules."""

import json
import numpy as np
import pandas as pd
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
COMPUTED_DIR = DATA_DIR / "computed"


def load_methodology() -> dict:
    with open(CONFIG_DIR / "methodology.json", encoding="utf-8") as f:
        return json.load(f)


def get_productive_naics(methodology: dict = None) -> list[str]:
    m = methodology or load_methodology()
    return m["sector_classification"]["productive_naics"]


def get_trading_naics(methodology: dict = None) -> list[str]:
    m = methodology or load_methodology()
    return m["sector_classification"]["trading_naics"]


def get_productive_nipa65(methodology: dict = None) -> list[int]:
    m = methodology or load_methodology()
    return m["sector_classification"]["productive_nipa65_lines"]


def build_series(book: pd.Series, ext: pd.Series, name: str = "") -> pd.DataFrame:
    """Combine book-period and extension into standard output DataFrame."""
    combined = pd.concat([book, ext])
    combined = combined[~combined.index.duplicated(keep="first")].sort_index()
    out = pd.DataFrame({"value": combined})
    out.index.name = "year"
    return out


def save_series(series_id: str, df: pd.DataFrame):
    """Save a computed series to data/computed/."""
    COMPUTED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(COMPUTED_DIR / f"{series_id}.csv")


_SERIES_STORE: dict = {}


def set_series_store(store: dict):
    """Set the in-memory series store from the orchestrator."""
    global _SERIES_STORE
    _SERIES_STORE = store


def load_computed(series_id: str) -> pd.Series:
    """Load a previously computed series. In-memory store first, then disk."""
    if series_id in _SERIES_STORE:
        df = _SERIES_STORE[series_id]
        if isinstance(df, pd.DataFrame):
            return df["value"].dropna() if "value" in df.columns else df.iloc[:, 0].dropna()
        return df if isinstance(df, pd.Series) else pd.Series(dtype=float)

    path = COMPUTED_DIR / f"{series_id}.csv"
    if not path.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(path, index_col="year")
    return df["value"].dropna() if "value" in df.columns else df.iloc[:, 0].dropna()


def interpolate_annual(benchmarks: dict, start: int = 1947, end: int = 2024) -> pd.Series:
    """Linearly interpolate between benchmark year values."""
    years = sorted(benchmarks.keys())
    vals = [benchmarks[y] for y in years]
    all_years = np.arange(start, end + 1)
    interp = np.interp(all_years, years, vals)
    return pd.Series(interp, index=all_years, dtype=float)
