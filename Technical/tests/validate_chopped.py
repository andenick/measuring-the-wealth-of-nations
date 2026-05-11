"""
Chopped CSV format validator for ST2.

Validates all T###_chopped.csv files against the expected format:
  Row 1: pipe-separated metadata fields (one per data column)
  Row 2: header row starting with 'year', followed by column IDs (dash-notation)
  Row 3+: numeric data rows (year + values, empty/NA allowed)

Cross-checks column IDs against SUBSOURCE_METADATA.json.

Usage:
    python validate_chopped.py
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative from tests/ directory)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
TECHNICAL = SCRIPT_DIR.parent
CHOPPED_DIR = TECHNICAL / "ANU_REPLICATOR" / "data" / "final-data" / "chopped"
METADATA_PATH = TECHNICAL / "ANU_REPLICATOR" / "data" / "final-data" / "shiny" / "SUBSOURCE_METADATA.json"

# Patterns
FILE_PATTERN = re.compile(r"^T\d+_chopped\.csv$")
COLUMN_ID_PATTERN = re.compile(r"^T\d+-[A-Z][A-Z0-9_]*$")
NUMERIC_PATTERN = re.compile(r"^-?\d+(\.\d+)?(e[+-]?\d+)?$", re.IGNORECASE)

MIN_DATA_ROWS = 10


def load_metadata_columns() -> set[str]:
    """Load the set of valid column IDs from SUBSOURCE_METADATA.json."""
    if not METADATA_PATH.exists():
        print(f"  WARNING: metadata file not found: {METADATA_PATH}")
        return set()
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return set(meta.get("columns", {}).keys())


def validate_file(filepath: Path, metadata_columns: set[str]) -> tuple[bool, list[str]]:
    """
    Validate a single chopped CSV file.

    Returns (passed: bool, errors: list[str]).
    """
    errors: list[str] = []
    name = filepath.name

    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = f.read().splitlines()

    # ---- Minimum line count (row 1 meta + row 2 header + 10 data) ----
    if len(raw_lines) < 2 + MIN_DATA_ROWS:
        errors.append(
            f"Too few lines: {len(raw_lines)} (need at least {2 + MIN_DATA_ROWS})"
        )
        return (False, errors)

    # ---- Row 1: pipe-separated metadata ----
    meta_row = raw_lines[0]
    meta_fields = meta_row.split(",")
    for i, field in enumerate(meta_fields):
        if not field.strip():
            errors.append(f"Row 1 metadata field {i} is empty")
        elif "|" not in field:
            errors.append(
                f"Row 1 metadata field {i} has no pipe-separated sub-fields: {field!r}"
            )

    # ---- Row 2: column IDs ----
    header_row = raw_lines[1]
    headers = header_row.split(",")

    if not headers or headers[0].strip().lower() != "year":
        errors.append(f"Row 2 first column should be 'year', got {headers[0]!r}")

    col_ids = [h.strip() for h in headers[1:]]
    expected_col_count = len(headers)

    # Extract table ID from filename for matching
    table_id = name.replace("_chopped.csv", "")

    for col_id in col_ids:
        if not COLUMN_ID_PATTERN.match(col_id):
            errors.append(f"Row 2 column ID does not match dash-notation: {col_id!r}")
        if not col_id.startswith(table_id + "-"):
            errors.append(
                f"Row 2 column ID {col_id!r} does not start with {table_id}-"
            )

    # ---- Metadata field count vs column count ----
    if len(meta_fields) != len(col_ids):
        errors.append(
            f"Row 1 has {len(meta_fields)} metadata fields but Row 2 has "
            f"{len(col_ids)} data columns (should match)"
        )

    # ---- Row 3+: data rows ----
    data_row_count = 0
    for line_idx, line in enumerate(raw_lines[2:], start=3):
        if not line.strip():
            continue
        data_row_count += 1
        cells = line.split(",")

        # Column count check
        if len(cells) != expected_col_count:
            errors.append(
                f"Row {line_idx}: expected {expected_col_count} columns, got {len(cells)}"
            )
            continue

        # Year column should be a 4-digit integer
        year_str = cells[0].strip()
        if not re.match(r"^\d{4}$", year_str):
            errors.append(f"Row {line_idx}: year column is not a 4-digit year: {year_str!r}")

        # Data columns should be numeric, empty, or NA
        for ci, val in enumerate(cells[1:], start=1):
            val = val.strip()
            if val == "" or val.upper() == "NA":
                continue
            if not NUMERIC_PATTERN.match(val):
                errors.append(
                    f"Row {line_idx}, col {ci} ({headers[ci] if ci < len(headers) else '?'}): "
                    f"non-numeric value {val!r}"
                )

    if data_row_count < MIN_DATA_ROWS:
        errors.append(
            f"Only {data_row_count} data rows (minimum {MIN_DATA_ROWS} required)"
        )

    # ---- Cross-check against SUBSOURCE_METADATA.json ----
    if metadata_columns:
        for col_id in col_ids:
            if col_id not in metadata_columns:
                errors.append(
                    f"Column {col_id!r} not found in SUBSOURCE_METADATA.json"
                )

    return (len(errors) == 0, errors)


def main() -> int:
    print(f"Chopped CSV Validator")
    print(f"  Chopped dir : {CHOPPED_DIR}")
    print(f"  Metadata    : {METADATA_PATH}")
    print()

    if not CHOPPED_DIR.exists():
        print(f"ERROR: chopped directory not found: {CHOPPED_DIR}")
        return 1

    # Discover files
    chopped_files = sorted(
        p for p in CHOPPED_DIR.iterdir()
        if p.is_file() and FILE_PATTERN.match(p.name)
    )

    if not chopped_files:
        print("ERROR: no T###_chopped.csv files found")
        return 1

    print(f"Found {len(chopped_files)} chopped CSV files\n")

    metadata_columns = load_metadata_columns()

    passed = 0
    failed = 0

    for fp in chopped_files:
        ok, errors = validate_file(fp, metadata_columns)
        if ok:
            print(f"  PASS  {fp.name}")
            passed += 1
        else:
            print(f"  FAIL  {fp.name}")
            for err in errors:
                print(f"        - {err}")
            failed += 1

    print()
    print(f"Summary: {passed} passed, {failed} failed out of {len(chopped_files)} files")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
