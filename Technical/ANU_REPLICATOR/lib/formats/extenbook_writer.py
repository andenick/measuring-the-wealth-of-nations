"""Write Anu Extenbook Excel with 4 sheets: Data, Provenance, Research, Construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def write_extenbook(
    data_dict: dict[str, pd.Series],
    registry: dict[str, Any],
    research_data: dict[str, Any] | None,
    series_id: str,
    output_dir: str | Path,
) -> Path:
    """Generate a 4-sheet Extenbook Excel workbook for a series."""
    series_config = registry["series"][series_id]
    subseries_defs = series_config["subseries"]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{series_id}_extenbook.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        _write_data_sheet(writer, data_dict, subseries_defs, series_id)
        _write_provenance_sheet(writer, subseries_defs)
        _write_research_sheet(writer, research_data)
        _write_construction_sheet(writer, series_config)

    return output_path.resolve()


def _write_data_sheet(writer, data_dict, subseries_defs, series_id):
    columns = sorted(subseries_defs.keys())
    all_years: set[int] = set()
    for col_id in columns:
        if col_id in data_dict:
            all_years.update(int(y) for y in data_dict[col_id].index)

    if not all_years:
        pd.DataFrame({"Year": []}).to_excel(writer, sheet_name="Data", index=False)
        return

    years = sorted(all_years)
    records = []
    for year in years:
        row: dict[str, Any] = {"Year": int(year)}
        for col_id in columns:
            if col_id in data_dict and year in data_dict[col_id].index:
                val = data_dict[col_id][year]
                if isinstance(val, pd.Series):
                    val = val.iloc[0]
                try:
                    row[col_id] = val if pd.notna(val) else None
                except (ValueError, TypeError):
                    row[col_id] = None
            else:
                row[col_id] = None
        records.append(row)

    df = pd.DataFrame(records)
    df["Year"] = df["Year"].astype(int)
    df.to_excel(writer, sheet_name="Data", index=False)


def _write_provenance_sheet(writer, subseries_defs):
    rows = []
    for sub_id in sorted(subseries_defs.keys()):
        sub = subseries_defs[sub_id]
        period = sub.get("period", [None, None])
        rows.append({
            "subseries_id": sub_id,
            "name": sub.get("name", ""),
            "source": sub.get("source", ""),
            "period": f"{period[0]}\u2013{period[1]}" if period and len(period) == 2 else "",
            "units": sub.get("units", ""),
            "derived_from": sub.get("derived_from", ""),
            "color": sub.get("color", ""),
        })
    pd.DataFrame(rows).to_excel(writer, sheet_name="Provenance", index=False)


def _write_research_sheet(writer, research_data):
    if not research_data or "entries" not in research_data:
        pd.DataFrame(columns=[
            "entry_id", "type", "source_location", "quote",
            "subseries_affected", "confidence",
        ]).to_excel(writer, sheet_name="Research", index=False)
        return

    rows = []
    for entry in research_data["entries"]:
        affected = entry.get("subseries_affected", [])
        rows.append({
            "entry_id": entry.get("entry_id", ""),
            "type": entry.get("type", ""),
            "source_location": entry.get("source_location", ""),
            "quote": entry.get("quote", ""),
            "subseries_affected": ", ".join(affected) if isinstance(affected, list) else str(affected),
            "confidence": entry.get("confidence", ""),
        })
    pd.DataFrame(rows).to_excel(writer, sheet_name="Research", index=False)


def _write_construction_sheet(writer, series_config):
    steps = series_config.get("construction", [])
    if not steps:
        pd.DataFrame(columns=["step", "op", "input", "output", "parameters"]).to_excel(
            writer, sheet_name="Construction", index=False,
        )
        return

    rows = []
    for s in steps:
        input_val = (
            s.get("input")
            or ", ".join(s.get("inputs", s.get("subseries", [])))
        )
        params = []
        for key in ("base_year", "at_year", "method", "match_to", "desc"):
            if key in s:
                params.append(f"{key}={s[key]}")
        rows.append({
            "step": str(s.get("step", "")),
            "op": s.get("op", ""),
            "input": input_val,
            "output": s.get("output", ""),
            "parameters": "; ".join(params),
        })
    pd.DataFrame(rows).to_excel(writer, sheet_name="Construction", index=False)
