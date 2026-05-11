#!/usr/bin/env python3
"""
Anu Chopped Validator v1.0
==========================

Validates CSV files against the Anu Chopped Standard:
    V1: Row 1 has non-empty metadata for all data columns
    V2: Row 2 has valid subseries IDs
    V3: Row 2 Column 1 is empty
    V4: Data cells are empty or valid numbers
    V5: Column 1 values are monotonically increasing
    V6: No duplicate subseries IDs
    V7: At least one data column has values
    V8: Filename matches expected pattern
    V9: Rightmost data column ID has no letter suffix

Usage:
    python validate_chopped.py <file_or_directory>
"""

import sys
import csv
import re
from pathlib import Path
from typing import List, Tuple


def validate_file(filepath: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a single Anu Chopped CSV file.
    Returns: (passed, errors, warnings)
    """
    errors = []
    warnings = []

    # V8: Filename pattern
    if not re.match(r'Appendix\d+_\w+\.csv', filepath.name):
        warnings.append(f"V8: Filename '{filepath.name}' does not match Appendix#_Name.csv pattern")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        errors.append(f"Cannot read file: {e}")
        return False, errors, warnings

    if len(rows) < 3:
        errors.append(f"File has only {len(rows)} rows (minimum 3 required)")
        return False, errors, warnings

    row1 = rows[0]  # Metadata
    row2 = rows[1]  # IDs
    data_rows = rows[2:]

    n_cols = len(row1)

    # V1: Row 1 metadata
    for i in range(1, n_cols):
        if i < len(row1) and not row1[i].strip():
            warnings.append(f"V1: Column {i + 1} has empty metadata in Row 1")

    # V3: Row 2 Column 1 empty
    if row2 and row2[0].strip():
        errors.append(f"V3: Row 2 Column 1 should be empty, got '{row2[0]}'")

    # V2: Valid subseries IDs
    ids = []
    for i in range(1, min(n_cols, len(row2))):
        sid = row2[i].strip() if i < len(row2) else ''
        if not sid:
            warnings.append(f"V2: Column {i + 1} has empty subseries ID in Row 2")
        elif not re.match(r'^(S\d{3}[A-Z]{0,2}(_CALC)?|S\d{3}_(EXT|COMBINED)|FPR\d{3}_C\d+)$', sid):
            warnings.append(f"V2: Column {i + 1} ID '{sid}' does not match expected pattern")
        ids.append(sid)

    # V6: No duplicate IDs
    seen = set()
    for sid in ids:
        if sid and sid in seen:
            errors.append(f"V6: Duplicate subseries ID '{sid}'")
        seen.add(sid)

    # V9: Rightmost column ID should be a final series (no letter suffix, or _COMBINED)
    if ids:
        rightmost = ids[-1]
        if rightmost and re.match(r'^S\d{3}[A-Z]+$', rightmost) and '_' not in rightmost:
            warnings.append(f"V9: Rightmost data column ID '{rightmost}' has letter suffix (expected final series)")

    # V4 & V5: Data validation
    prev_index = None
    has_any_data = False
    for row_idx, row in enumerate(data_rows):
        # V5: Monotonic index
        if row:
            try:
                idx = float(row[0])
                if prev_index is not None and idx <= prev_index:
                    warnings.append(f"V5: Row {row_idx + 3} index {idx} not > previous {prev_index}")
                prev_index = idx
            except (ValueError, TypeError):
                pass

        # V4: Data cells numeric or empty
        for ci in range(1, min(n_cols, len(row))):
            val = row[ci].strip() if ci < len(row) else ''
            if val:
                try:
                    float(val)
                    has_any_data = True
                except ValueError:
                    errors.append(f"V4: Row {row_idx + 3} Col {ci + 1} non-numeric value '{val}'")

    # V7: At least one data column
    if not has_any_data:
        errors.append("V7: No data values found in any column")

    passed = len(errors) == 0
    return passed, errors, warnings


def validate_directory(dirpath: Path) -> Tuple[int, int, int]:
    """Validate all CSV files in a directory. Returns (total, passed, failed)."""
    csv_files = sorted(dirpath.rglob('*.csv'))
    total = len(csv_files)
    passed_count = 0
    failed_count = 0

    for f in csv_files:
        ok, errs, warns = validate_file(f)
        rel = f.relative_to(dirpath)
        if ok:
            passed_count += 1
            status = "PASS"
            if warns:
                status = f"PASS ({len(warns)} warnings)"
            print(f"  [{status}] {rel}")
        else:
            failed_count += 1
            print(f"  [FAIL] {rel}")
            for e in errs:
                print(f"    ERROR: {e}")
        for w in warns[:3]:
            print(f"    WARN:  {w}")
        if len(warns) > 3:
            print(f"    ... and {len(warns) - 3} more warnings")

    return total, passed_count, failed_count


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_chopped.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    print(f"Anu Chopped Validator v1.0")
    print(f"Target: {target}")
    print("=" * 60)

    if target.is_file():
        ok, errs, warns = validate_file(target)
        print(f"Result: {'PASS' if ok else 'FAIL'}")
        for e in errs:
            print(f"  ERROR: {e}")
        for w in warns:
            print(f"  WARN:  {w}")
        sys.exit(0 if ok else 1)
    elif target.is_dir():
        total, passed, failed = validate_directory(target)
        print("=" * 60)
        print(f"Total: {total}, Passed: {passed}, Failed: {failed}")
        sys.exit(0 if failed == 0 else 1)
    else:
        print(f"Not found: {target}")
        sys.exit(1)
