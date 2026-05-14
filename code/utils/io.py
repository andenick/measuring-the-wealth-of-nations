"""IO helpers shared by loaders, processors, and validators."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def read_book_table(path: Path) -> pd.DataFrame:
    """Read a digitized book-table CSV.

    Handles three header conventions seen in the project's source CSVs:
      1. Leading `#`-prefixed comment row (Ch5 tables: H.1, E.2, 5.7, E.3)
      2. Multi-row title headers ending in a column row starting with `year`
         (Ch6 tables: 6.1, 6.2, 6.3 — first row is title, second is source,
         third is column header)
      3. No header preamble — first row is the column header

    Returns a DataFrame with the column-header row as columns.
    """
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    skip = 0
    for i, line in enumerate(lines):
        first_cell = line.split(",", 1)[0].strip().strip('"').lower()
        if first_cell == "year":
            skip = i
            break
        # Legacy convention: leading `#` comment row, next row IS the header
        if i == 0 and line.startswith("#"):
            skip = 1
            break
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
