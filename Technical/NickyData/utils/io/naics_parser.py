"""Parse BEA InputOutput API JSON files into pandas DataFrames.

Handles the BEA API JSON format for Use of Commodities, Supply of Commodities,
and Total Requirements (Leontief inverse) tables. Supports summary-level
(~71 industries) and sector-level (detailed) tables.

Data format: BEAAPI.Results[0].Data[] → list of dicts with keys:
  TableID, Year, RowCode, RowDescr, RowType, ColCode, ColDescr, ColType, DataValue
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# Codes to exclude from industry matrices (totals, value-added, special)
EXCLUDE_ROWS = {
    "T001", "T005", "T018", "T019",  # Totals
    "V001", "V003", "VABAS", "VAPRO",  # Value added rows
    "T00OTOP", "T00SUB", "T00TOP",  # Tax rows
    "Used", "Other",  # Special rows
}

EXCLUDE_COLS_INDUSTRY = {
    "T001", "T005", "T018", "T019",  # Totals
    "Used", "Other",
}

# Final demand column codes
FINAL_DEMAND_CODES = {
    "F010", "F02E", "F02N", "F02R", "F02S", "F030", "F040",
    "F06C", "F06E", "F06N", "F06S",
    "F07C", "F07E", "F07N", "F07S",
    "F10C", "F10E", "F10N", "F10S",
}


def _load_json(json_path: Path | str) -> list[dict]:
    """Load BEA API JSON and return the Data array."""
    with open(json_path, encoding="utf-8") as f:
        raw = json.load(f)

    results = raw.get("BEAAPI", {}).get("Results", [])
    if isinstance(results, list) and len(results) > 0:
        return results[0].get("Data", [])
    return []


def _parse_value(val_str: str) -> float:
    """Parse BEA DataValue string (may have commas) to float."""
    if not val_str or val_str == "---" or val_str == "...":
        return np.nan
    return float(str(val_str).replace(",", ""))


def parse_bea_io_json(
    json_path: Path | str,
    include_final_demand: bool = False,
    exclude_govt: bool = False,
) -> pd.DataFrame:
    """Parse BEA InputOutput API JSON into a pivot table (matrix).

    Returns DataFrame with RowCode as index, ColCode as columns, DataValue as values.
    Filters out totals, value-added rows, and special rows.

    Parameters
    ----------
    json_path : path to BEA IO JSON file
    include_final_demand : if True, include F-prefixed columns (PCE, investment, etc.)
    exclude_govt : if True, exclude government rows/cols (GFE, GFGD, GFGN, GSLE, GSLG)
    """
    data = _load_json(json_path)
    if not data:
        raise ValueError(f"No data found in {json_path}")

    records = []
    for entry in data:
        row_code = entry.get("RowCode", "")
        col_code = entry.get("ColCode", "")

        # Skip excluded rows
        if row_code in EXCLUDE_ROWS:
            continue

        # Skip excluded columns (industry matrix only)
        if not include_final_demand and col_code in FINAL_DEMAND_CODES:
            continue
        if col_code in EXCLUDE_COLS_INDUSTRY:
            continue

        # Skip government if requested
        govt_codes = {"GFE", "GFGD", "GFGN", "GSLE", "GSLG"}
        if exclude_govt and (row_code in govt_codes or col_code in govt_codes):
            continue

        val = _parse_value(entry.get("DataValue", ""))
        records.append({
            "row": row_code,
            "col": col_code,
            "value": val,
        })

    if not records:
        raise ValueError(f"No valid records after filtering in {json_path}")

    df = pd.DataFrame(records)
    matrix = df.pivot_table(index="row", columns="col", values="value", aggfunc="first")
    matrix = matrix.fillna(0.0)
    return matrix


def extract_use_matrix(json_path: Path | str) -> pd.DataFrame:
    """Extract industry-by-industry Use matrix (intermediate flows only).

    This is the Z-matrix from which A-matrix can be computed:
    A = Z × diag(1/GO) where GO = column sums of the full Use table.
    """
    return parse_bea_io_json(json_path, include_final_demand=False)


def extract_use_with_final_demand(json_path: Path | str) -> pd.DataFrame:
    """Extract full Use table including final demand columns."""
    return parse_bea_io_json(json_path, include_final_demand=True)


def extract_leontief(json_path: Path | str) -> pd.DataFrame:
    """Extract Total Requirements (Leontief inverse B = (I-A)^{-1}).

    The BEA pre-computes this from their detailed Make/Use framework.
    """
    data = _load_json(json_path)
    if not data:
        raise ValueError(f"No data found in {json_path}")

    records = []
    for entry in data:
        row_code = entry.get("RowCode", "")
        col_code = entry.get("ColCode", "")

        # Skip empty row code (total output requirement row)
        if not row_code:
            continue

        val = _parse_value(entry.get("DataValue", ""))
        records.append({"row": row_code, "col": col_code, "value": val})

    df = pd.DataFrame(records)
    matrix = df.pivot_table(index="row", columns="col", values="value", aggfunc="first")
    matrix = matrix.fillna(0.0)
    return matrix


def get_sector_labels(json_path: Path | str) -> list[str]:
    """Get ordered list of industry sector codes from a BEA IO JSON file."""
    data = _load_json(json_path)
    codes = set()
    for entry in data:
        rc = entry.get("RowCode", "")
        if rc and rc not in EXCLUDE_ROWS:
            codes.add(rc)
    return sorted(codes)


def get_sector_descriptions(json_path: Path | str) -> dict[str, str]:
    """Get mapping of sector code → descriptive name."""
    data = _load_json(json_path)
    desc = {}
    for entry in data:
        rc = entry.get("RowCode", "")
        rd = entry.get("RowDescr", "")
        if rc and rc not in EXCLUDE_ROWS and rc not in desc:
            desc[rc] = rd
    return desc


def compute_technical_coefficients_naics(
    use_matrix: pd.DataFrame,
    gross_output: Optional[pd.Series] = None,
) -> pd.DataFrame:
    """Compute A-matrix from Use table: a_ij = z_ij / GO_j.

    If gross_output not provided, uses column sums of the use matrix as proxy.
    """
    if gross_output is None:
        gross_output = use_matrix.sum(axis=0)

    go_safe = gross_output.replace(0, np.nan)
    a_matrix = use_matrix.div(go_safe, axis=1)
    return a_matrix.fillna(0.0)


def compute_leontief_inverse_naics(a_matrix: pd.DataFrame) -> pd.DataFrame:
    """Compute B = (I - A)^{-1} from A-matrix."""
    n = len(a_matrix)
    # Align to square
    common = a_matrix.index.intersection(a_matrix.columns)
    a_sq = a_matrix.loc[common, common]
    n = len(a_sq)

    identity = np.eye(n)
    i_minus_a = identity - a_sq.values
    b = np.linalg.inv(i_minus_a)
    return pd.DataFrame(b, index=a_sq.index, columns=a_sq.columns)
