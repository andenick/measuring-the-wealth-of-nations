# Phase 0 Method Contract

**Purpose**: Define the exact rules, thresholds, and provenance requirements for every data operation in AS2. Two different agents given this contract and the same source data should produce identical results.

**Version**: 1.0
**Date**: February 23, 2026

---

## 1. Data Loading Rules

### 1.1 Source Priority

When loading a series, follow this source hierarchy:
1. **Book Tables** (`Inputs/BookTables/`) -- authoritative baseline for book period (1948-1989)
2. **Tonak Benchmarks** (`Inputs/ExternalSources/Tonak_Benchmarks/`) -- validation reference from Prof. Tonak
3. **BEA NIPA** (`Inputs/NIPA/` and `Inputs/API_Data/BEA/`) -- primary extension source for national accounts
4. **BEA IO** (`Inputs/IO_Matrices/` and `Inputs/API_Data/BEA/`) -- IO analysis extension
5. **BLS** (`Inputs/BLS/` and `Inputs/API_Data/BLS/`) -- employment and production worker data
6. **Robin APIs** (`Inputs/API_Data/`) -- FRED, additional BEA, additional BLS for extension period

### 1.2 Parsing Standards
- All data files follow Anu Chopped format: Row 0 = metadata (source citations, methods, base years). Row 1 = column headers. Row 2+ = data rows.
- Year column is always first or clearly labeled.
- **No silent type coercion.** If a cell contains text in a numeric column, flag it; do not convert to NA silently.
- **No silent NA fill.** Missing values must be preserved as NA, not interpolated unless explicitly documented.

### 1.3 Encoding
- All CSV files: UTF-8 encoding.
- All JSON files: UTF-8 encoding, 2-space indentation.
- All Excel files: .xlsx format (not .xls), one sheet per file.

---

## 2. Replication Rules

### 2.1 Value Match Tolerance

| Data Type | Tolerance | Example |
|-----------|-----------|---------|
| Rates (exploitation, profit) | <= 0.1% relative difference | e(t) = s/v: book says 1.85, we accept 1.8482-1.8518 |
| Absolute values (output, surplus, wages) | <= 1% relative difference | GFP = $2,451B: we accept $2,427B-$2,475B |
| Integer data (employment counts, years) | Exact match | Production workers = 14,523,000: must be exact |
| Percentage data (shares, ratios as %) | 0.01 percentage points absolute | Share = 34.5%: we accept 34.49%-34.51% |

### 2.2 Replication Procedure

For each T-series:
1. Load from `Inputs/BookTables/` (identify correct chapter and table).
2. Parse metadata row for source citation and base year.
3. Extract time series data.
4. Compare against Shaikh Tonak authoritative data for cross-validation.
5. Store in Anu Chopped CSV format.
6. Create DPR in `Technical/docs/series/T###_DPR.md`.
7. Create automated test in `Technical/tests/`.

### 2.3 Table Reproduction

For each empirical table:
1. Identify T-series IDs from table structure.
2. Load series data.
3. Apply any transformations documented in the book's methodology.
4. Render in Shiny app.
5. Compare with book table values.
6. Create FPR in `Technical/docs/figures/`.

---

## 3. Extension Rules

### 3.1 Splice Method Selection

| Condition | Method | Formula |
|-----------|--------|---------|
| Same agency, same concept, same methodology continues | `level_match` | Use API values directly |
| Different source or methodology change; good overlap (>= 3 years) | `growth_rate_splice` | `Ext[t] = Book[splice_yr] * (API[t] / API[splice_yr])` |
| No overlap; low risk of level shift | `direct_append` | Append new years |
| Different base years | `rebase_and_splice` | Rebase both to common year, then splice |
| Cannot determine method with confidence | `BLOCKED` | Flag as needs_method_decision |

### 3.2 Splice Year Selection

- Default splice year: last year of book's original data (typically 1989).
- If overlap exists: use last year where both sources agree within 1%.
- If sources diverge in overlap: document divergence; use growth_rate_splice.
- **Never splice at**: 1992 (SIC->NAICS transition), 2003 (BEA comprehensive revision), 2013 (BEA comprehensive revision), 2020 (COVID disruption).

### 3.3 Transition Quality Thresholds

| Metric | Formula | PASS | WARN | FAIL |
|--------|---------|------|------|------|
| Connection ratio | `API[splice_yr] / Book[splice_yr]` | 0.95 - 1.05 | 0.90-0.95 or 1.05-1.10 | <0.90 or >1.10 |
| Growth rate continuity | `abs(g_book - g_api)` in overlap window | < 3% | 3-5% | > 5% |
| Trend correlation | Pearson r over 5-year window around splice | > 0.98 | 0.95 - 0.98 | < 0.95 |
| Level difference | `max(abs(Book[t] - API[t]) / Book[t])` in overlap | < 1% | 1-3% | > 3% |

### 3.4 When Transition Fails

1. Log failure in `DIVERGENCE_REGISTER.json`.
2. Investigate: methodology change? Definition change? BEA revision?
3. Create ADR (Anu Divergence Report) documenting root cause.
4. If resolvable: apply correction, re-validate.
5. If not resolvable: escalate to user with options.

---

## 4. NIPA-Specific Rules

### 4.1 Key NIPA Tables for AS2

| NIPA Table | Content | AS2 Usage |
|------------|---------|-----------|
| 1.7.5 | GDP by sector (current $) | Gross output, intermediate consumption |
| 1.12 | National income by type | Compensation, proprietor's income, corporate profits |
| 2.1 | Personal income and outlays | NSW components |
| 3.1 | Government receipts and expenditures | NSW government transfers |
| 6.2-6.5 | Compensation by industry | Productive/unproductive labor wages |
| 7.1-7.5 | Fixed assets tables | Capital stock for profit rate |

### 4.2 BEA Revision Handling

- Always record the **vintage date** of any BEA data download.
- When a comprehensive revision occurs, re-download all affected tables and compare.
- Document pre-revision vs. post-revision differences in DIVERGENCE_REGISTER.json.
- Use **post-revision** data for extension period; note revision impact on book-period overlap.

### 4.3 Marxian Category Mappings

The core Marxian categories map to NIPA as follows (per Shaikh & Tonak 1994, Chapter 5):

| Marxian Category | Symbol | NIPA Mapping |
|-----------------|--------|--------------|
| Gross value of production | C + V + S | Gross output (Table 1.7.5) |
| Constant capital consumed | c | Intermediate inputs + depreciation |
| Variable capital | v | Wages of productive workers |
| Surplus value | s | Gross output - c - v |
| Rate of exploitation | e = s/v | Computed |
| Rate of surplus value | s/v | Same as exploitation rate |
| Organic composition | c/v | Computed |
| Rate of profit | s/(c+v) | Computed |

---

## 5. Provenance Requirements

### 5.1 DPR (Data Provenance Record) - Every Series

Required fields:
```
series_id: T###
name: [descriptive name]
chapter: [chapter number]
book_table: [Table #.# reference]
source_file: [exact filename in Inputs/]
time_period: [start_year - end_year]
base_year: [if applicable]
unit: [unit of measurement]
transformation: [none | log | index | ratio | difference | ...]
methodology_reference: [book page/section or methodology doc]
validation_status: [replicated | pending | failed]
validation_date: [YYYY-MM-DD]
notes: [any additional context]
```

### 5.2 EPR (Extension Provenance Record) - Every Extended Series

Required fields (in addition to DPR):
```
extension_source: [API name and series ID]
extension_period: [start_year - end_year]
splice_year: [year of connection]
splice_method: [level_match | growth_rate_splice | direct_append | rebase_and_splice]
transition_analysis:
  connection_ratio: [value]
  growth_rate_continuity: [value]
  trend_correlation: [value]
  level_difference: [value]
  pass_fail: [PASS | WARN | FAIL]
api_vintage_date: [date of API data pull]
methodology_comparison: [summary of old vs new methodology]
certification: [EXEMPLARY | COMPLETE | ADEQUATE | INCOMPLETE]
```

### 5.3 FPR (Figure Provenance Record) - Every Figure/Table

Required fields:
```
figure_id: [Table#.# or Fig#.#]
title: [title from book]
chapter: [chapter number]
type: [empirical | conceptual | composite]
series_ids: [list of T### IDs used]
data_source: [path to data file]
transformation: [description of any transforms applied]
rendering: [chart type or table format]
validation: [visual match confirmed | pending]
```

### 5.4 Transformation Log

Every data operation must be logged in `Technical/TRANSFORMATION_LOG.json`:
```json
{
  "timestamp": "ISO 8601",
  "series_id": "T###",
  "action": "extend | rebase | splice | calculate | correct",
  "parameters": { ... },
  "input_file": "path",
  "output_file": "path",
  "agent": "model name",
  "session": "session identifier"
}
```

---

## 6. Quality Gates by Stage

### 6.1 Pre-Extension Gate (per series)
- [ ] DPR exists and all required fields populated
- [ ] Original data loaded and value-matched (within tolerance)
- [ ] At least one automated test validates the data path
- [ ] Series appears correctly in Shiny app

### 6.2 Post-Extension Gate (per series)
- [ ] EPR exists and all required fields populated
- [ ] Transition quality: all metrics PASS or WARN (no FAIL)
- [ ] Extended CSV written to complete database
- [ ] Extenbook generated (Sheet 1: data, Sheet 2: provenance)
- [ ] Shiny app renders both original and extended with visual distinction
- [ ] Automated test updated to cover extension period

### 6.3 Chapter Completion Gate
- [ ] All empirical tables replicated
- [ ] All extendable series extended (or documented as blocked)
- [ ] All tables render in Shiny app
- [ ] Chapter investigation document complete
- [ ] Anu Review score >= 85%
- [ ] All DPR/EPR/FPR complete
- [ ] All tests passing

### 6.4 Wave Completion Gate
- [ ] All chapters in wave meet chapter completion gate
- [ ] Cross-chapter consistency check (shared variables agree)
- [ ] No unresolved FAIL-level divergences
- [ ] User review and sign-off

---

## 7. Naming Conventions

### 7.1 Series IDs
- Format: `T###` where first digit = chapter number
- T201 (Ch 2), T401-T402 (Ch 4), T501-T516 (Ch 5), T601-T609 (Ch 6), T701-T703 (Ch 7), T801 (Ch 8), T901 (Ch 9)
- Subsources: `T###A`, `T###B`, etc.

### 7.2 Figure/Table IDs
- Tables: `Table#.#` (e.g., Table5.7, Table6.3)
- Figures: `Fig#.#` (e.g., Fig5.1)

### 7.3 File Naming
- Data CSVs: `T###_[short_name].csv`
- DPRs: `T###_DPR.md`
- EPRs: `T###_EPR.md`
- FPRs: `Table#_#_FPR.md` or `Fig#_#_FPR.md`
- Scripts: `extend_T###.py`, `validate_ch##.py`
- Tests: `test_ch##.py` or `test_ch##.R`

### 7.4 Dates
- In filenames: `YYYYMMDD` (e.g., `20260223`)
- In documents: `YYYY-MM-DD` (e.g., `2026-02-23`)
- Handoffs: `HANDOFF_YYYYMMDD_HHMMSS.md`

---

## 8. Tool and Environment Requirements

### 8.1 R Environment
```r
install.packages(c(
  "shiny", "shinydashboard", "tidyverse", "plotly",
  "DT", "scales", "jsonlite", "here", "testthat", "readr"
))
```

### 8.2 Python Environment
```
pandas >= 1.5
numpy >= 1.24
scipy >= 1.10
openpyxl >= 3.1
requests >= 2.28
python-dotenv >= 1.0
pytest >= 7.0
```

### 8.3 API Keys Required
- BEA API key (for NIPA/IO table downloads)
- FRED API key (for supplementary series)

### 8.4 Path Configuration
All paths must resolve from the AS2 project root using `here()` (R) or `pathlib.Path` (Python). No hardcoded absolute paths.

---

## 9. Review Cadence

| Event | Frequency | Participants |
|-------|-----------|--------------|
| Series-level validation | After each series extension | Agent (automated) |
| Chapter-level Anu Review | After chapter completion | Agent + user review |
| Wave completion review | After each wave | User approval required |
| Cross-wave consistency check | After Wave 2 and Wave 3 | Agent (automated) + user review |
| Final deliverables review | After all waves complete | User sign-off |

---

*Method Contract v1.0 - February 23, 2026*
*This contract governs all data operations in AS2. Any deviation must be documented and approved.*
