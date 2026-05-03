"""Shiny export writer -- produces chapter-level CSVs and a series catalog
JSON that the ST2 Shiny app can read directly.

Column names in the chapter CSVs use the ``shiny_column`` alias from the
registry so they match the Shiny app's data loader.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def _get_alias(registry: dict, series_id: str, sub_id: str) -> str | None:
    """Look up the shiny_column alias for a subseries."""
    entry = registry["series"].get(series_id, {})
    sub_entry = entry.get("subseries", {}).get(sub_id, {})
    if sub_entry.get("shiny_column"):
        return sub_entry["shiny_column"]
    if sub_id == series_id and entry.get("shiny_column"):
        return entry["shiny_column"]
    return None


def write_chapter_csv(
    chapter: int,
    process_results: list[dict],
    registry: dict,
    output_dir: Path,
) -> Path:
    """Combine all processed series for *chapter* into a single wide CSV."""
    all_series: dict[str, pd.Series] = {}

    for result in process_results:
        sid = result["series_id"]
        entry = registry["series"].get(sid, {})
        if entry.get("chapter") != chapter:
            continue
        data_dict: dict = result.get("data_dict", {})
        if not data_dict:
            continue

        for sub_id, series_data in data_dict.items():
            alias = _get_alias(registry, sid, sub_id)
            if alias is None:
                continue
            if alias in all_series:
                continue
            s = series_data.copy()
            s = s[~s.index.duplicated(keep="first")]
            all_series[alias] = s

    if not all_series:
        return output_dir / f"chapter_{chapter:02d}.csv"

    df = pd.DataFrame(all_series)
    df.index.name = "Year"
    df = df.sort_index()
    df = df.dropna(how="all")

    out = output_dir / f"chapter_{chapter:02d}.csv"
    df.to_csv(out, index=True)
    print(f"  [shiny-export] chapter_{chapter:02d}.csv: "
          f"{len(df)} rows, {len(df.columns)} columns")
    return out


def write_series_catalog(
    registry: dict,
    process_results: list[dict],
    output_dir: Path,
    existing_catalog_path: Path | None = None,
) -> Path:
    """Generate a series catalog JSON from the registry."""
    existing: dict = {}
    if existing_catalog_path and existing_catalog_path.exists():
        with open(existing_catalog_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        cat_series = raw.get("series", raw)
        if isinstance(cat_series, list):
            existing = {s.get("series_id", s.get("id")): s for s in cat_series}
        elif isinstance(cat_series, dict):
            existing = cat_series

    processed_ids = {r["series_id"] for r in process_results}
    catalog: dict[str, Any] = {}

    for sid in sorted(processed_ids):
        entry = registry["series"].get(sid, {})
        yr = entry.get("year_range", [None, None])

        subseries_keys = list(entry.get("subseries", {}).keys())
        shiny_cols = []
        for sk in subseries_keys:
            alias = _get_alias(registry, sid, sk)
            if alias:
                shiny_cols.append(alias)
        if entry.get("shiny_column"):
            shiny_cols.append(entry["shiny_column"])

        ext = entry.get("extension", {})
        if ext:
            ext_status = "extended"
        else:
            ext_status = "original"

        cat_entry: dict[str, Any] = {
            "series_id": sid,
            "name": entry.get("name", sid),
            "chapter": entry.get("chapter"),
            "figure_ids": entry.get("figures", []),
            "time_period_start": yr[0] if yr else None,
            "time_period_end": yr[1] if len(yr) > 1 else None,
            "extension_status": ext_status,
            "subsource_ids": subseries_keys,
            "subsource_count": len(subseries_keys),
            "shiny_columns": shiny_cols,
        }

        old = existing.get(sid, {})
        for preserve_key in (
            "methodology_note", "methodology_decision",
            "source_verified", "is_key_series",
        ):
            if preserve_key in old and preserve_key not in cat_entry:
                cat_entry[preserve_key] = old[preserve_key]

        catalog[sid] = cat_entry

    out = output_dir / "series_catalog.json"
    payload = {
        "generated_by": "anu_replicator_shiny_export_as2",
        "series": catalog,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"  [shiny-export] series_catalog.json: {len(catalog)} series")
    return out


def write_figure_column_map(
    registry: dict,
    output_dir: Path,
) -> Path:
    """Generate a JSON mapping of figure-to-column references."""
    figures = registry.get("figures", {})
    if not figures:
        return output_dir / "figure_column_map.json"

    col_map: dict[str, Any] = {}

    for fig_id, fig_spec in sorted(figures.items()):
        cols = list(fig_spec.get("columns", {}).keys())
        if len(cols) == 1:
            col_map[fig_id] = cols[0]
        else:
            col_map[fig_id] = cols

    payload = {
        "generated_by": "anu_replicator_shiny_export_as2",
        "figure_column_map": col_map,
    }

    out = output_dir / "figure_column_map.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"  [shiny-export] figure_column_map.json: {len(col_map)} figures")
    return out
