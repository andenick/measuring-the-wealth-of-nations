"""Shared data I/O for the AS2 Anu Replicator processing scripts.

Provides a single canonical ``load_parsed()`` that correctly reads the
year-indexed parsed CSVs produced by the L## loading phase, plus helpers
for loading multi-column chapter tables.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from utils.paths import CHOPPED_IN, ST_CHOPPED, PARSED_RAW, ensure_dirs
from utils.config_loader import load_registry
from utils.registry_reader import get_series

log = logging.getLogger("data_io")


def load_parsed(series_id: str) -> tuple[pd.DataFrame | None, str]:
    """Load a parsed CSV and return a DataFrame with integer year index.

    The L## loaders write CSVs whose first column is the year (with an
    empty header).  Using ``index_col=0`` ensures pandas treats that
    column as the index rather than data.
    """
    path = PARSED_RAW / f"{series_id}_parsed.csv"
    if not path.exists():
        return None, str(path)

    df = pd.read_csv(path, index_col=0)
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index = df.index.astype(int)
    df.index.name = "year"
    df = df.sort_index()
    return df, str(path)


def _detect_header_row(lines: list[str]) -> int:
    """Detect which row contains column headers.

    Format A: row 0 = ``# source=...``, headers at row 1
    Format B: row 0 = ``source,...`` CSV metadata, headers at row 1
    Format C: row 0 = ``Table 6.x: ...``, row 1 = ``Source: ...``, headers at row 2
    """
    if len(lines) < 2:
        return 0
    row0 = lines[0].strip().strip('"')
    row1 = lines[1].strip().strip('"')
    # Format C: title line followed by Source line
    if row0.startswith("Table ") and (row1.startswith("Source") or row1.startswith('"Source')):
        return 2
    # Formats A and B: headers at row 1
    return 1


def _parse_chopped_csv(chopped_file: Path, out_file: Path) -> dict:
    """Read an Anu Chopped CSV (multi-format header), write parsed CSV."""
    with open(chopped_file, "r", encoding="utf-8-sig") as fh:
        raw_lines = list(fh)

    if len(raw_lines) < 3:
        return {"status": "fail", "error": "CSV has fewer than 3 rows"}

    header_row = _detect_header_row(raw_lines)
    reader = csv.reader(raw_lines[header_row:])
    headers = next(reader)
    headers = [h.strip() for h in headers]

    expected_cols = len(headers)
    rows = []
    row_warnings = 0
    for line_num, row in enumerate(reader, start=3):
        stripped = [c.strip() for c in row]
        if not any(stripped):
            continue
        if len(stripped) != expected_cols:
            row_warnings += 1
            while len(stripped) < expected_cols:
                stripped.append("")
            stripped = stripped[:expected_cols]
        rows.append(stripped)

    with open(out_file, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)

    result = {"rows_written": len(rows), "columns": headers}
    if row_warnings:
        result["row_warnings"] = row_warnings
    return result


def load_chopped_table(series_id: str, source_file: str, script_label: str) -> dict:
    """Shared loader for multi-column chopped tables.

    Parses the Anu Chopped CSV from Inputs/ST_Chopped/ and writes a
    parsed CSV to data/raw-data/parsed/.
    """
    ensure_dirs()
    registry = load_registry()
    series = get_series(registry, series_id)

    result = {
        "series_id": series_id,
        "status": "ok",
        "message": series["name"],
        "outputs": [],
    }

    chopped_file = ST_CHOPPED / source_file
    if not chopped_file.exists():
        result["status"] = "fail"
        result["message"] = f"Chopped CSV not found: {chopped_file.name}"
        log.error("[%s/%s] FAILED: %s", script_label, series_id, result["message"])
        return result

    out_file = PARSED_RAW / f"{series_id}_parsed.csv"
    parse_info = _parse_chopped_csv(chopped_file, out_file)
    if parse_info.get("status") == "fail":
        result["status"] = "fail"
        result["message"] = parse_info["error"]
        log.error("[%s/%s] FAILED: %s", script_label, series_id, result["message"])
        return result

    n_cols = len(parse_info["columns"]) - 1
    result["outputs"].append(str(out_file))
    result["obs_count"] = parse_info["rows_written"]
    result["message"] += f" | {parse_info['rows_written']} rows, {n_cols} columns"

    if parse_info.get("row_warnings"):
        log.warning("[%s/%s] %d rows had mismatched column counts",
                    script_label, series_id, parse_info["row_warnings"])

    log.info("[%s/%s] OK: %s", script_label, series_id, result["message"])
    return result


def load_chopped_direct(filepath: str | Path, columns: list[str] | None = None) -> pd.DataFrame:
    """Load a chopped CSV directly into a year-indexed DataFrame.

    Auto-detects the header format (A/B/C) and returns a clean DataFrame
    with integer year index.  Optionally selects only *columns*.
    """
    filepath = Path(filepath)
    with open(filepath, "r", encoding="utf-8-sig") as fh:
        raw_lines = fh.readlines()

    header_row = _detect_header_row(raw_lines)
    # Build a single string starting from the header row for pandas
    text = "".join(raw_lines[header_row:])

    from io import StringIO
    df = pd.read_csv(StringIO(text), index_col=0)
    df.index = pd.to_numeric(df.index, errors="coerce")
    df = df[df.index.notna()]
    df.index = df.index.astype(int)
    df.index.name = "year"
    df = df.sort_index()

    # Drop fully-empty columns
    df = df.dropna(axis=1, how="all")

    if columns:
        missing = [c for c in columns if c not in df.columns]
        if missing:
            log.warning("load_chopped_direct: columns %s not found in %s", missing, filepath.name)
        present = [c for c in columns if c in df.columns]
        df = df[present]

    return df
