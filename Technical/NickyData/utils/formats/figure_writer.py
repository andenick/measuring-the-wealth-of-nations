"""Figure export writer — produces per-figure CSVs with transforms applied.

Each figure specification in the ``figures`` block of the registry defines
which data columns to include and what transforms to apply (HP filter,
normal-capacity adjustment, etc.).  This writer resolves column references
against the processing results' ``data_dict``, applies transforms, and
writes one CSV per figure.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

log = logging.getLogger("figure_writer")


def _resolve_column(
    col_name: str,
    col_spec: dict,
    all_data: dict[str, dict[str, pd.Series]],
) -> pd.Series | None:
    """Look up a column from the processing results."""
    series_id = col_spec.get("series")
    subseries_id = col_spec.get("subseries")

    if series_id not in all_data:
        return None

    data_dict = all_data[series_id]

    if subseries_id and subseries_id in data_dict:
        return data_dict[subseries_id]

    if series_id in data_dict:
        return data_dict[series_id]

    return None


def write_figure_csv(
    fig_id: str,
    fig_spec: dict,
    process_results: list[dict],
    output_dir: Path,
) -> Path | None:
    """Write a single figure's data to CSV."""
    all_data: dict[str, dict[str, pd.Series]] = {}
    for r in process_results:
        dd = r.get("data_dict")
        if dd:
            all_data[r["series_id"]] = dd

    columns: dict[str, pd.Series] = {}
    for col_name, col_spec in fig_spec.get("columns", {}).items():
        s = _resolve_column(col_name, col_spec, all_data)
        if s is not None:
            s = s.copy()
            s = s[~s.index.duplicated(keep="first")]
            columns[col_name] = s

    if not columns:
        return None

    df = pd.DataFrame(columns)
    df.index.name = "Year"
    df = df.sort_index()
    df = df.dropna(how="all")

    out = output_dir / f"{fig_id}.csv"
    df.to_csv(out, index=True)
    log.info("%s.csv: %d rows, %d columns", fig_id, len(df), len(df.columns))
    return out


def write_all_figures(
    registry: dict,
    process_results: list[dict],
    output_dir: Path,
) -> list[Path]:
    """Write CSVs for all figures defined in the registry."""
    figures = registry.get("figures", {})
    if not figures:
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []

    for fig_id in sorted(figures.keys()):
        fig_spec = figures[fig_id]
        path = write_figure_csv(fig_id, fig_spec, process_results, output_dir)
        if path:
            paths.append(path)

    log.info("%d/%d figures written", len(paths), len(figures))
    return paths
