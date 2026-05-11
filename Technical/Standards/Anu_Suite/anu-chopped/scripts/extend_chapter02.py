#!/usr/bin/env python3
"""
Chapter 2 Extension Script
===========================

Extends Chapter 2 Anu Chopped CSVs with Robin data by adding 3 columns:
    S###_EXT      : Raw Robin extension data in Robin's native units
    S###_COMBINED : Spliced series (Shaikh through overlap, then re-indexed Robin)

For each file, the splice works by:
1. Finding the last year where both Shaikh final (S###) and Robin have data
2. Computing the re-index ratio: shaikh_value / robin_value at that year
3. For years after Shaikh ends: COMBINED = robin_value * ratio
4. For years where Shaikh has data: COMBINED = shaikh_value

Also trims empty leading/trailing rows and enriches metadata.

Usage:
    python extend_chapter02.py <chopped_dir> <robin_dir>

Created: 2026-02-11
"""

import csv
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


def read_chopped_csv(filepath: Path) -> Tuple[List[str], List[str], List[List]]:
    """Read an Anu Chopped CSV. Returns (meta_row, id_row, data_rows)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    if len(rows) < 3:
        return [], [], []
    return rows[0], rows[1], rows[2:]


def write_chopped_csv(filepath: Path, meta_row: List, id_row: List, data_rows: List):
    """Write an Anu Chopped CSV."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(meta_row)
        writer.writerow(id_row)
        for row in data_rows:
            writer.writerow(row)


def read_robin_csv(filepath: Path, year_col: str = 'year', value_col: str = None,
                   skip_header_rows: int = 0) -> Dict[int, float]:
    """Read a Robin extension CSV. Returns {year: value}."""
    data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        # Skip non-header rows (like MeasuringWorth notes)
        for _ in range(skip_header_rows):
            next(f)
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        if value_col is None:
            # Use second column
            value_col = cols[1] if len(cols) > 1 else None
        if value_col is None:
            return data
        for row in reader:
            try:
                yr_str = row.get(year_col, '').strip().strip('"')
                yr = int(float(yr_str))
                val_str = row.get(value_col, '').strip().strip('"').replace(',', '')
                if val_str:
                    data[yr] = float(val_str)
            except (ValueError, TypeError):
                continue
    return data


def read_mw_csv(filepath: Path, value_col_idx: int = 1) -> Dict[int, float]:
    """Read a MeasuringWorth CSV with header rows to skip."""
    data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the header row (the one starting with "Year")
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('"Year"'):
            header_idx = i
            break

    if header_idx is None:
        return data

    # Parse from header onwards
    reader = csv.reader(lines[header_idx:])
    headers = next(reader)

    for row in reader:
        try:
            yr = int(row[0].strip().strip('"'))
            val_str = row[value_col_idx].strip().strip('"').replace(',', '')
            if val_str:
                data[yr] = float(val_str)
        except (ValueError, TypeError, IndexError):
            continue
    return data


def safe_float(val) -> Optional[float]:
    """Convert to float or None."""
    if val is None or val == '':
        return None
    try:
        f = float(val)
        return None if f != f else f  # NaN check
    except (ValueError, TypeError):
        return None


def get_final_col_idx(id_row: List[str], series_base: str) -> Optional[int]:
    """Find the index of the final series column (S### without suffix)."""
    for i, sid in enumerate(id_row):
        if sid.strip() == series_base:
            return i
    return None


def find_splice_year(data_rows: List[List], final_idx: int,
                     robin_data: Dict[int, float]) -> Optional[int]:
    """Find the last year where both Shaikh and Robin have data."""
    best_year = None
    for row in data_rows:
        try:
            yr = int(float(row[0]))
        except (ValueError, TypeError, IndexError):
            continue
        shaikh_val = safe_float(row[final_idx] if final_idx < len(row) else None)
        robin_val = robin_data.get(yr)
        if shaikh_val is not None and robin_val is not None:
            best_year = yr
    return best_year


def extend_file(chopped_path: Path, robin_data: Dict[int, float],
                series_base: str, ext_metadata: str,
                combined_metadata: str) -> bool:
    """
    Extend a single Anu Chopped CSV with Robin data.
    Adds S###_EXT and S###_COMBINED columns.
    Returns True if successful.
    """
    meta_row, id_row, data_rows = read_chopped_csv(chopped_path)
    if not data_rows:
        print(f"  SKIP: {chopped_path.name} - no data")
        return False

    final_idx = get_final_col_idx(id_row, series_base)
    if final_idx is None:
        print(f"  SKIP: {chopped_path.name} - no column {series_base}")
        return False

    # Check if already extended
    ext_id = f"{series_base}_EXT"
    comb_id = f"{series_base}_COMBINED"
    if ext_id in [s.strip() for s in id_row]:
        print(f"  SKIP: {chopped_path.name} - already extended")
        return False

    # Find splice year
    splice_year = find_splice_year(data_rows, final_idx, robin_data)
    if splice_year is None:
        print(f"  SKIP: {chopped_path.name} - no overlap year found")
        return False

    # Get Shaikh and Robin values at splice year
    shaikh_at_splice = None
    robin_at_splice = robin_data.get(splice_year)
    for row in data_rows:
        try:
            yr = int(float(row[0]))
        except (ValueError, TypeError, IndexError):
            continue
        if yr == splice_year:
            shaikh_at_splice = safe_float(row[final_idx] if final_idx < len(row) else None)
            break

    if shaikh_at_splice is None or robin_at_splice is None or robin_at_splice == 0:
        print(f"  SKIP: {chopped_path.name} - cannot compute ratio at {splice_year}")
        return False

    ratio = shaikh_at_splice / robin_at_splice
    print(f"  {chopped_path.name}: splice at {splice_year}, ratio = {ratio:.6f}")
    print(f"    Shaikh({splice_year}) = {shaikh_at_splice}, Robin({splice_year}) = {robin_at_splice}")

    # Determine full year range (union of Shaikh and Robin)
    shaikh_years = set()
    for row in data_rows:
        try:
            yr = int(float(row[0]))
            shaikh_years.add(yr)
        except (ValueError, TypeError, IndexError):
            pass
    robin_years = set(robin_data.keys())
    all_years = sorted(shaikh_years | robin_years)

    # Find the actual data range (trim empty leading/trailing)
    first_data_year = None
    last_data_year = None
    for yr in all_years:
        # Check if any column has data for this year
        has_shaikh = False
        for row in data_rows:
            try:
                row_yr = int(float(row[0]))
            except (ValueError, TypeError, IndexError):
                continue
            if row_yr == yr:
                for ci in range(1, len(row)):
                    if safe_float(row[ci]) is not None:
                        has_shaikh = True
                        break
                break
        has_robin = yr in robin_data
        if has_shaikh or has_robin:
            if first_data_year is None:
                first_data_year = yr
            last_data_year = yr

    if first_data_year is None:
        first_data_year = min(all_years)
    if last_data_year is None:
        last_data_year = max(all_years)

    # Build lookup for existing data rows
    existing_rows = {}
    for row in data_rows:
        try:
            yr = int(float(row[0]))
            existing_rows[yr] = row
        except (ValueError, TypeError, IndexError):
            pass

    # Build new data rows
    n_existing_cols = len(meta_row)
    new_data_rows = []
    for yr in range(first_data_year, last_data_year + 1):
        if yr in existing_rows:
            base_row = list(existing_rows[yr])
            # Pad if needed
            while len(base_row) < n_existing_cols:
                base_row.append('')
        else:
            base_row = [yr] + [''] * (n_existing_cols - 1)

        # Extension value
        robin_val = robin_data.get(yr)
        ext_val = robin_val if robin_val is not None else ''

        # Combined value
        shaikh_val = safe_float(base_row[final_idx] if final_idx < len(base_row) else None)
        if shaikh_val is not None:
            combined_val = shaikh_val
        elif robin_val is not None:
            combined_val = round(robin_val * ratio, 6)
        else:
            combined_val = ''

        base_row.append(ext_val)
        base_row.append(combined_val)
        new_data_rows.append(base_row)

    # Update metadata and ID rows
    new_meta = list(meta_row) + [ext_metadata, combined_metadata]
    new_ids = list(id_row) + [ext_id, comb_id]

    write_chopped_csv(chopped_path, new_meta, new_ids, new_data_rows)
    print(f"    -> {len(new_data_rows)} rows, years {first_data_year}-{last_data_year}")
    return True


# =============================================================================
# EXTENSION CONFIGURATIONS
# =============================================================================

EXTENSIONS = [
    {
        'csv_name': 'Appendix2_IndustrialProduction.csv',
        'series_base': 'S001',
        'robin_file': 'FRED/INDPRO.csv',
        'robin_type': 'fred',
        'ext_meta': 'FRED INDPRO, Industrial Production Total Index, 2017=100, monthly avg, 2000-2025. Source: https://fred.stlouisfed.org/series/INDPRO',
        'comb_meta': 'Combined: Shaikh (1860-2010) + FRED INDPRO (2011-2025), re-indexed to 1958=100 at splice year 2010',
    },
    {
        'csv_name': 'Appendix2_RealInvestmentUS_1832-2010.csv',
        'series_base': 'S002',
        'robin_file': 'FRED/GPDI.csv',
        'robin_type': 'fred',
        'ext_meta': 'FRED GPDI, Gross Private Domestic Investment, Billions of $, quarterly avg, 2000-2025. Source: https://fred.stlouisfed.org/series/GPDI. NOTE: Nominal dollars (Shaikh uses real)',
        'comb_meta': 'Combined: Shaikh (1832-2010) + FRED GPDI (2011-2025), re-indexed to 1958=100 at splice year 2010. WARNING: nominal/real mismatch',
    },
    {
        'csv_name': 'Appendix2_MeasuringWorthGDP_1889-2010.csv',
        'series_base': 'S003',
        'robin_file': 'MeasuringWorth/USGDP_1790-2025.csv',
        'robin_type': 'mw_gdp',
        'mw_col_idx': 6,  # "Real GDP per capita (year 2017 dollars)"
        'ext_meta': 'MeasuringWorth, Real GDP per capita (2017 dollars), 1790-2024. Citation: Williamson 2025',
        'comb_meta': 'Combined: Shaikh (1780-2000) + MeasuringWorth (2001-2024), re-indexed at splice year 2000',
    },
    {
        'csv_name': 'Appendix2_ManufacturingProductivityAndRealWages1889-2010.csv',
        'series_base': 'S007',
        'robin_file': 'FRED/OUTNFB.csv',
        'robin_type': 'fred',
        'ext_meta': 'FRED OUTNFB, Nonfarm Business Output Index 2017=100, quarterly avg, 2000-2025. NOTE: Nonfarm output, not manufacturing-specific. Source: https://fred.stlouisfed.org/series/OUTNFB',
        'comb_meta': 'Combined: Shaikh (1889-2009) + FRED OUTNFB (2010-2025), re-indexed at splice year 2009. Proxy: nonfarm for manufacturing',
    },
    {
        'csv_name': 'Appendix2_ManufacturingProductivity.csv',
        'series_base': 'S008',
        'robin_file': 'MeasuringWorth/USCPI_1774-2025.csv',
        'robin_type': 'mw_cpi',
        'ext_meta': 'MeasuringWorth, US CPI 1982-84=100, 1774-2024. Citation: Officer & Williamson 2025. Extends S008 CPI component only',
        'comb_meta': 'Combined: Shaikh (1780-2010) + MeasuringWorth CPI (2011-2024), re-indexed at splice year 2010',
    },
    {
        'csv_name': 'Appendix2_Unemployment.csv',
        'series_base': 'S009',
        'robin_file': 'FRED/UNRATE.csv',
        'robin_type': 'fred',
        'ext_meta': 'FRED UNRATE, Unemployment Rate %, monthly avg, 2000-2025. Source: https://fred.stlouisfed.org/series/UNRATE',
        'comb_meta': 'Combined: Shaikh (1890-2010) + FRED UNRATE (2011-2025), direct splice (same units, same series)',
    },
]


def main():
    if len(sys.argv) < 3:
        print("Usage: python extend_chapter02.py <chopped_dir> <robin_dir>")
        sys.exit(1)

    chopped_dir = Path(sys.argv[1])
    robin_dir = Path(sys.argv[2])

    ch02_dir = chopped_dir / 'ch02'
    if not ch02_dir.exists():
        print(f"ERROR: {ch02_dir} not found")
        sys.exit(1)

    print("Chapter 2 Extension Script")
    print(f"Chopped: {ch02_dir}")
    print(f"Robin:   {robin_dir}")
    print("=" * 60)

    results = []
    for ext in EXTENSIONS:
        csv_path = ch02_dir / ext['csv_name']
        robin_path = robin_dir / ext['robin_file']

        if not csv_path.exists():
            print(f"  MISSING: {csv_path}")
            continue
        if not robin_path.exists():
            print(f"  MISSING: {robin_path}")
            continue

        # Load Robin data
        if ext['robin_type'] == 'fred':
            robin_data = read_robin_csv(robin_path)
        elif ext['robin_type'] == 'mw_gdp':
            robin_data = read_mw_csv(robin_path, value_col_idx=ext.get('mw_col_idx', 1))
        elif ext['robin_type'] == 'mw_cpi':
            robin_data = read_mw_csv(robin_path, value_col_idx=1)
        else:
            robin_data = read_robin_csv(robin_path)

        if not robin_data:
            print(f"  NO DATA: {robin_path}")
            continue

        print(f"\nExtending {ext['csv_name']}:")
        print(f"  Robin: {ext['robin_file']} ({len(robin_data)} years, {min(robin_data)}-{max(robin_data)})")

        ok = extend_file(
            csv_path, robin_data,
            ext['series_base'],
            ext['ext_meta'],
            ext['comb_meta'],
        )
        results.append((ext['csv_name'], ok))

    print("\n" + "=" * 60)
    for name, ok in results:
        status = "OK" if ok else "SKIP"
        print(f"  [{status}] {name}")
    print(f"\nExtended: {sum(1 for _, ok in results if ok)}/{len(results)}")


if __name__ == '__main__':
    main()
