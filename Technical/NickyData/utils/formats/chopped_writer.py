"""Write Anu Chopped CSV format (Row 1 metadata, Row 2 IDs, Row 3+ data)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd


def write_chopped(
    data_dict: dict[str, pd.Series],
    registry: dict[str, Any],
    series_id: str,
    output_dir: str | Path,
) -> Path:
    """Write a single series to Anu Chopped CSV.

    Parameters
    ----------
    data_dict : dict[str, pd.Series]
        Mapping from subseries ID to a pandas Series with integer year index.
    registry : dict
        Full registry dict (output of ``load_registry()``).
    series_id : str
        Top-level series key, e.g. ``"T506"``.
    output_dir : Path
        Directory to write the chopped CSV into.
    """
    series_config = registry["series"][series_id]
    subseries = series_config["subseries"]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    registry_cols = sorted(subseries.keys())
    extra_cols = [k for k in sorted(data_dict.keys()) if k not in subseries]
    columns = registry_cols + extra_cols

    output_path = output_dir / f"{series_id}_chopped.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Row 1: Metadata (Anu Chopped Standard: col 1 = "Year")
        row1: list[str] = ["Year"]
        for col_id in columns:
            sub = subseries.get(col_id, {})
            row1.append(_metadata_label(sub, col_id) if sub else "Composite final series")
        writer.writerow(row1)

        # Row 2: Column IDs (Anu Chopped Standard: col 1 = empty)
        writer.writerow([""] + columns)

        # Row 3+: Data rows
        all_years: set[int] = set()
        for col_id in columns:
            if col_id in data_dict:
                all_years.update(int(y) for y in data_dict[col_id].index)

        for year in sorted(all_years):
            row: list[Any] = [year]
            for col_id in columns:
                if col_id in data_dict and year in data_dict[col_id].index:
                    val = data_dict[col_id][year]
                    if isinstance(val, pd.Series):
                        val = val.iloc[0]
                    try:
                        row.append(val if pd.notna(val) else "")
                    except (ValueError, TypeError):
                        row.append("")
                else:
                    row.append("")
            writer.writerow(row)

    return output_path.resolve()


def _metadata_label(sub: dict[str, Any], col_id: str) -> str:
    """Build the Row-1 metadata cell for a subseries."""
    if sub.get("derived_from"):
        meta = f"Derived from {sub['derived_from']}"
        transform = sub.get("transform")
        if transform:
            meta += f", {transform['type']}"
            if transform.get("formula"):
                meta += f". Formula: {transform['formula']}"
        return meta

    if sub.get("source"):
        parts = [sub["source"]]
        if sub.get("units"):
            parts.append(sub["units"])
        return ", ".join(parts)

    return sub.get("name", col_id)
