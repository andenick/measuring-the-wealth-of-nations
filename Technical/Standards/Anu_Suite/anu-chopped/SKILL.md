---
name: anu-chopped
description: Convert raw source data (Excel, CSV) into the Anu Chopped self-documenting CSV format. Use when ingesting new data sources, standardizing existing datasets, or building input databases for replication projects.
argument-hint: [action] [source_file_or_directory]
allowed-tools: Read, Write, Grep, Glob, LS, Shell
---

# Anu Chopped Standard: Self-Documenting CSV Database Format

A format specification and toolchain for converting raw data sources into structured, self-documenting CSV files where every column carries its own metadata and unique subseries identifier.

---

## Core Philosophy

The Anu Chopped Standard ensures that **every data column is self-documenting**. Any researcher opening an Anu Chopped CSV can immediately understand:

1. **What** each column contains (Row 1: metadata)
2. **Which** series/subseries it belongs to (Row 2: ID)
3. **When** the data covers (Row 3+: dated values)

This eliminates the need for external codebooks or README files to understand the data -- though those are still generated for discoverability.

---

## Format Specification (v1.0)

### Row Structure

Every Anu Chopped CSV has exactly this structure:

| Row | Purpose | Content |
|-----|---------|---------|
| 1 | **Metadata** | Per-column description: source citation, methodology, base year, units, coverage |
| 2 | **Subseries ID** | Unique identifier per column (e.g., `S001A`, `S001B`, `S001`) |
| 3+ | **Data** | Date/index in column 1, numeric values in remaining columns |

### Column Layout

| Position | Content | Row 1 | Row 2 | Row 3+ |
|----------|---------|-------|-------|--------|
| Column 1 | Date/Index | `"Year"` or `"Date"` or `"Index"` | _(empty)_ | Year/date/index values |
| Column 2 | First subsource | Source description | `S###A` | Numeric data |
| Column 3 | Second subsource or transform | Source description | `S###B` | Numeric data |
| ... | ... | ... | ... | ... |
| Last column | Final published series | Splice/derivation description | `S###` (no letter) | Final values |

### Concrete Example

Industrial Production (S001), 6 columns:

```csv
"Year","HS series, BEA Long Term Eco Growth 1973, TA15 p.185, 1913=100, 1860-1918","HS reindexed to 1958=100","FRB G-17 Industrial Production, 1919-2010","FRB reindexed to 1958=100","Final spliced series, reindexed to 1958=100"
"","S001A","S001B","S001C","S001D","S001"
1860,2.3,1.52,,,1.52
1861,3.1,2.05,,,2.05
1919,19.0,12.55,12.55,12.55,12.55
2010,,,494.39,494.39,494.39
```

---

## Rules

### R1: Column Identity

- Every data column MUST have a metadata description in Row 1
- Every data column MUST have a unique subseries ID in Row 2
- The date/index column MUST have an empty ID cell in Row 2
- Column 1 is ALWAYS the date/index column

### R2: Subseries ID Format

Follow the Anu Standard identity system:

| Pattern | Meaning | Example |
|---------|---------|---------|
| `S###A` | First raw subsource | `S001A` (HS series from BEA 1973) |
| `S###B` | Second raw subsource or first transform | `S001B` (reindexed to 1958) |
| `S###C` | Third subsource or second transform | `S001C` (FRB G-17) |
| `S###` | Final published series (no letter) | `S001` (spliced final) |
| `S###_CALC` | Derived/calculated series | `S026_CALC` |
| `S###_EXT` | Robin extension data (raw) | `S001_EXT` |
| `S###_COMBINED` | Spliced Shaikh + Robin | `S001_COMBINED` |
| `FPR###_C#` | Cross-sectional column | `FPR009_C1` |

### R3: Column Ordering

Columns MUST appear in this order (left to right):
1. Date/index column
2. Raw subsources in chronological order of their coverage period
3. Transformations of those subsources (reindex, adjust, etc.)
4. The final published/spliced series as the rightmost column

### R4: Missing Values

- Missing values MUST be empty cells (not `NA`, not `NaN`, not `0`, not `-`)
- A year row should exist if ANY column has data for that year
- The year range should span the full union of all subsource coverage periods

### R5: Metadata Content (Row 1)

Each metadata cell SHOULD include (when available):
- Source name and citation
- Table/series reference (e.g., "TA15, p.185")
- Base year and index value (e.g., "1913=100")
- Coverage period (e.g., "1860-1918")
- Units or measurement type
- Transformation applied (e.g., "reindexed to 1958=100")

### R6: One File Per Source

- Each original source file (e.g., one Excel workbook) maps to exactly one Anu Chopped CSV
- Multi-sheet workbooks produce one CSV per data sheet (documentation sheets are skipped)
- Files are organized into chapter subdirectories: `ch02/`, `ch05/`, `ch06/`, etc.

### R7: File Naming

```
Appendix{N}_{TableName}.csv
```

Matching the original Excel file name but with `.csv` extension.

### R8: Extension Columns (_EXT / _COMBINED)

When a series is extended with Robin data (FRED, MeasuringWorth, Maddison, etc.), two additional columns are appended **after** the Shaikh final column:

| Suffix | Meaning | Content |
|--------|---------|---------|
| `S###_EXT` | Extension raw data | Robin values in Robin's native units/base |
| `S###_COMBINED` | Spliced series | Shaikh values through overlap year, then Robin values re-indexed to Shaikh's base |

**Column order** (extends R3):
```
Year | S###A | S###B | ... | S### (Shaikh final) | S###_EXT (Robin raw) | S###_COMBINED (spliced)
```

**Splice method**:
1. Find the last year where both S### and Robin have data (the "splice year")
2. Compute ratio = S###(splice_year) / Robin(splice_year)
3. For years where Shaikh has data: COMBINED = Shaikh value
4. For years after Shaikh ends: COMBINED = Robin value * ratio

**Metadata requirements**:
- `S###_EXT` Row 1 must cite the Robin source, units, coverage period, and URL
- `S###_COMBINED` Row 1 must state splice year, source combination, and any caveats (e.g., "nominal/real mismatch")

**Validation**:
- `S###_EXT` and `S###_COMBINED` IDs must match pattern `S\d{3}_(EXT|COMBINED)`
- The `_COMBINED` column should have no gaps (continuous year coverage from first to last)

---

## Data Format Patterns

### Pattern A: Standard Time Series (most common)

Original Excel structure:
- Row 0: Metadata string (source citations, methods, base years)
- Row 1: Column headers (Year, Variable1, Variable2, ...)
- Row 2+: Year-indexed data

Conversion:
- Parse Row 0 metadata and distribute across columns in CSV Row 1
- Map column headers to subseries IDs in CSV Row 2
- Copy data rows as-is to CSV Row 3+

### Pattern B: Wide-Format Tables (Chapter 6)

Original Excel structure:
- Row 0: Table title
- Row 1: Table | Description | Source | Variable | 1947 | 1948 | ...
- Row 2+: Variable rows with years as columns

Conversion:
- Transpose: each variable/row becomes a column in the CSV
- Year headers become data rows
- Description and Source cells become CSV Row 1 metadata
- Variable codes become part of the subseries ID

### Pattern C: Cross-Sectional/Matrix (Chapter 9)

Original Excel structure:
- Row 0: Calculation metadata
- Row 1: Index | Column1 | Column2 | ...
- Row 2+: Industry/category-indexed data

Conversion:
- Keep the row structure (NOT transposed)
- Row 1: metadata for each column
- Row 2: FPR-linked identifiers (e.g., FPR009_C1, FPR009_C2)
- Row 3+: data with index column on the far left

### Pattern D: Documentation Only

Files containing only text descriptions (e.g., `Appendix5_Documentation.xlsx`):
- Skipped during CSV generation
- Referenced in the catalog with `"format": "documentation"`
- Content preserved in the manifest markdown file

---

## Catalog Specification

Every Anu Chopped dataset MUST have a companion catalog file (`ANU_CHOPPED_CATALOG.json`):

```json
{
  "version": "1.0",
  "standard": "Anu Chopped v1.0",
  "project": "CD2",
  "generated": "YYYY-MM-DD",
  "source_location": "Inputs/ShaikhChopped/",
  "total_files": 72,
  "total_columns": 0,
  "files": {
    "ch02/Appendix2_IndustrialProduction.csv": {
      "source_excel": "Appendix2_IndustrialProduction.xlsx",
      "chapter": 2,
      "format": "time_series",
      "year_range": [1860, 2010],
      "row_count": 251,
      "columns": {
        "S001A": {
          "name": "IndProdHS_BEA",
          "description": "HS series from BEA Long Term Eco Growth 1973",
          "source_type": "historical_book",
          "type": "raw",
          "coverage": [1860, 1918],
          "base_year": 1913,
          "base_value": 100
        }
      },
      "linked_figures": ["Fig2.1"],
      "linked_series": ["S001"]
    }
  }
}
```

Required fields per file entry:
- `source_excel`: Original filename
- `chapter`: Chapter number
- `format`: One of `time_series`, `wide_table`, `cross_sectional`, `documentation`
- `year_range`: `[start, end]` or `null` for non-time-series
- `row_count`: Number of data rows (excluding header rows)
- `columns`: Map of subseries ID to column metadata
- `linked_figures`: Array of figure IDs that use data from this file
- `linked_series`: Array of final series IDs (S### without letter suffix)

---

## Validation Rules

A valid Anu Chopped CSV must pass all of the following:

1. **V1**: Row 1 exists and contains non-empty strings for all data columns
2. **V2**: Row 2 exists and contains valid subseries IDs matching `S\d{3}[A-Z]?` or `FPR\d{3}_C\d+`
3. **V3**: Row 2 Column 1 is empty (date column has no ID)
4. **V4**: All data cells (Row 3+) are either empty or valid numbers
5. **V5**: Column 1 values are monotonically increasing (years/dates)
6. **V6**: No duplicate subseries IDs within a single file
7. **V7**: At least one data column has non-empty values
8. **V8**: File name matches `Appendix\d+_\w+\.csv` pattern
9. **V9**: The rightmost data column's ID has no letter suffix (final series)

---

## Workflow

### Converting a New Source

```
1. Identify the source format (Pattern A/B/C/D)
2. Read the Excel file with openpyxl (preserving Row 0 metadata)
3. Extract column-level metadata from Row 0
4. Map column names to subseries IDs using existing catalogs
5. Write the Anu Chopped CSV (Row 1: metadata, Row 2: IDs, Row 3+: data)
6. Add entry to ANU_CHOPPED_CATALOG.json
7. Run validate_chopped.py on the output
```

### Validating Existing Files

```
python scripts/validate_chopped.py path/to/file.csv
python scripts/validate_chopped.py path/to/directory/  # validate all CSVs
```

### Generating Catalog

```
python scripts/generate_catalog.py path/to/ShaikhChopped/ --output ANU_CHOPPED_CATALOG.json
```

---

## Integration with Anu Suite

The Anu Chopped Standard sits at the **beginning** of the Anu Suite pipeline:

```
Raw Sources (Excel/PDF/API)
    |
    v
anu-chopped (standardize into self-documenting CSV)
    |
    v
anu-standard (create DPR/EPR for each series)
    |
    v
anu-extension (extend series to current year)
    |
    v
anu-extenbook (visualize in Excel workbooks)
    |
    v
anu-review (audit all standards)
```

### Relationship to Other Components

| Component | Relationship |
|-----------|-------------|
| **anu-standard** | Chopped CSVs are the input; DPR/EPR document the series within |
| **anu-extension** | Extensions reference the Chopped CSV as the "original data" baseline |
| **anu-extenbook** | Extenbooks can import directly from Chopped CSV columns |
| **anu-review** | Review audits check Chopped format compliance as part of D2 (Data File Integrity) |

---

## Version History

- **v1.0** (2026-02-11): Initial specification based on Shaikh Chopped Tables format
