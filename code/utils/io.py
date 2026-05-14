"""IO helpers shared by loaders, processors, and validators."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def read_book_table(path: Path) -> pd.DataFrame:
    """Read a digitized book-table CSV, skipping any leading '#' header comment."""
    with path.open("r", encoding="utf-8") as f:
        first = f.readline()
        skip = 1 if first.startswith("#") else 0
    return pd.read_csv(path, skiprows=skip)


def load_registry() -> dict:
    """Load the canonical series registry."""
    from .paths import REGISTRY
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def get_series_entry(series_id: str) -> dict:
    """Return the registry entry for one series, raising if absent."""
    reg = load_registry()
    if series_id not in reg["series"]:
        raise KeyError(f"Series {series_id} not in registry")
    return reg["series"][series_id]


def write_series_csv(df: pd.DataFrame, series_id: str, *, stage: str = "intermediate") -> Path:
    """Write a single-series CSV to data/{stage}/{series_id}.csv. Returns the path."""
    from .paths import DATA_INTERMEDIATE, DATA_FINAL
    out_dir = {"intermediate": DATA_INTERMEDIATE, "final": DATA_FINAL}[stage]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{series_id}.csv"
    df.to_csv(out_path, index=False)
    return out_path


def write_validation_result(series_id: str, result: dict) -> Path:
    """Write a per-series validation result for S03 to roll up."""
    from .paths import VALIDATION_DIR
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    out_path = VALIDATION_DIR / f"{series_id}.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return out_path
