#!/usr/bin/env python3
"""
Anu Chopped Catalog Generator v1.0
===================================

Generates ANU_CHOPPED_CATALOG.json from a folder of Anu Chopped CSV files.
Reads Row 1 (metadata), Row 2 (subseries IDs), and scans data rows for
year ranges and row counts.

Usage:
    python generate_catalog.py <chopped_dir> [--output catalog.json]
"""

import sys
import csv
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


def parse_csv_catalog_entry(filepath: Path, base_dir: Path) -> Optional[Dict]:
    """Parse a single Anu Chopped CSV and return a catalog entry."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return None

    if len(rows) < 3:
        return None

    meta_row = rows[0]
    id_row = rows[1]
    data_rows = rows[2:]

    # Extract chapter from path
    rel = filepath.relative_to(base_dir)
    parts = rel.parts
    chapter = None
    if parts and parts[0].startswith('ch'):
        try:
            chapter = int(parts[0][2:])
        except ValueError:
            pass

    # Source Excel name
    source_excel = filepath.stem + '.xlsx'

    # Parse columns
    columns = {}
    for i in range(1, len(id_row)):
        sid = id_row[i].strip() if i < len(id_row) else ''
        if not sid:
            continue
        desc = meta_row[i].strip() if i < len(meta_row) else ''

        # Determine type
        is_final = bool(re.match(r'^S\d{3}$', sid))
        col_type = 'final' if is_final else 'raw'
        if 'reindex' in desc.lower():
            col_type = 'reindex'
        elif 'splice' in desc.lower():
            col_type = 'splice'
        elif 'calculated' in desc.lower() or 'derived' in desc.lower():
            col_type = 'calculated'
        elif is_final:
            col_type = 'final'

        # Coverage from actual data
        col_idx = i
        col_years = []
        for dr in data_rows:
            if col_idx < len(dr) and dr[col_idx].strip():
                try:
                    year = float(dr[0])
                    col_years.append(int(year))
                except (ValueError, IndexError):
                    pass

        coverage = [min(col_years), max(col_years)] if col_years else None

        columns[sid] = {
            'name': sid,
            'description': desc[:300],
            'type': col_type,
            'coverage': coverage,
        }

    # Year range from data
    years = []
    for dr in data_rows:
        if dr:
            try:
                years.append(int(float(dr[0])))
            except (ValueError, TypeError):
                pass

    # Detect format
    fmt = 'time_series'
    if sid.startswith('FPR'):
        fmt = 'cross_sectional'

    final_ids = [sid for sid in columns if re.match(r'^S\d{3}$', sid)]

    return {
        'source_excel': source_excel,
        'chapter': chapter,
        'format': fmt,
        'year_range': [min(years), max(years)] if years else None,
        'row_count': len(data_rows),
        'columns': columns,
        'linked_figures': [],
        'linked_series': final_ids,
    }


def generate_catalog(chopped_dir: Path, output_path: Path):
    """Generate catalog from all CSVs in directory."""
    csv_files = sorted(chopped_dir.rglob('*.csv'))

    print(f"Anu Chopped Catalog Generator v1.0")
    print(f"Source: {chopped_dir}")
    print(f"Files:  {len(csv_files)}")
    print("=" * 60)

    catalog = {
        'version': '1.0',
        'standard': 'Anu Chopped v1.0',
        'project': 'CD2',
        'generated': datetime.now().strftime('%Y-%m-%d'),
        'source_location': str(chopped_dir),
        'total_files': 0,
        'total_columns': 0,
        'files': {},
    }

    for csv_file in csv_files:
        rel = csv_file.relative_to(chopped_dir)
        entry = parse_csv_catalog_entry(csv_file, chopped_dir)
        if entry:
            key = str(rel).replace('\\', '/')
            catalog['files'][key] = entry
            catalog['total_files'] += 1
            catalog['total_columns'] += len(entry['columns'])
            print(f"  {key}: {len(entry['columns'])} columns, {entry['row_count']} rows")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"Catalog: {output_path}")
    print(f"Files: {catalog['total_files']}, Columns: {catalog['total_columns']}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_catalog.py <chopped_dir> [--output catalog.json]")
        sys.exit(1)

    src = Path(sys.argv[1])
    out = Path(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == '--output' else src.parent / 'ANU_CHOPPED_CATALOG.json'
    generate_catalog(src, out)
