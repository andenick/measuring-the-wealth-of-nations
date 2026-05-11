# The Anu Standard: Unified Data and Figure Provenance Framework

**Version**: 2.2 (Subsource Visualization Standard)  
**Created**: 2026-01-27  
**Updated**: 2026-01-31  
**Project**: CD2 (Shaikh Replication and Extension Package)

---

## Overview

The Anu Standard is the definitive framework for ensuring complete provenance tracking, quality assurance, and reproducibility for ALL content in the CD2 project. It covers:

- **Empirical time series** with full data lineage
- **Theoretical diagrams** with conceptual documentation
- **Simulation outputs** with methodology records
- **Cross-sectional studies** with source documentation

The standard is named after Anwar Shaikh, whose meticulous approach to economic data construction in "Capitalism: Competition, Conflict, Crises" (2016) serves as the model for this framework.

---

## Part I: Core Principles

### Principle 1: EXPLICIT PARSING

**Never rely on implicit defaults.** Every data load must specify exact parsing behavior.

```r
# BAD: Relies on default simplifyDataFrame = TRUE
data <- fromJSON(path)

# GOOD: Explicit about structure preservation
data <- fromJSON(path, simplifyDataFrame = FALSE)
```

### Principle 2: VALIDATE ON LOAD

**Every data structure must be validated immediately after loading.**

- Verify expected fields exist
- Check data types match expectations
- Confirm row/column counts are reasonable
- Log validation results

### Principle 3: FAIL LOUDLY

**Never fall through to defaults silently.** If expected data isn't found, throw an error with diagnostic information.

```r
# BAD: Silent fallback
if (is.null(data)) data <- default_value

# GOOD: Explicit failure with diagnostics
if (is.null(data)) {
    stop(sprintf("DATA_MISSING: Expected data for %s not found. Available: %s",
                 expected_id, paste(available_ids, collapse = ", ")))
}
```

### Principle 4: DOCUMENT EVERYTHING

**Every series, figure, and transformation must have complete provenance documentation.**

- Source file location
- Download date (for external data)
- Transformation steps
- Validation results
- Shaikh's theoretical context

### Principle 5: TEST DATA PATHS

**Every figure-to-data mapping must have an automated test.**

- Verify HDARP linkages resolve correctly
- Confirm expected series exist in chapter data
- Validate value ranges match expectations

### Principle 6: NO SYNTHETIC DATA

**Never generate fake, estimated, or placeholder data to fill gaps.**

- If annual data exists in an HDARP extraction, extract it — do not approximate
- If data is unavailable: mark as `data_unavailable`, leave CSV empty
- Acceptable sources: HDARP extractions, official APIs, published tables, digitized figures
- `np.random` in a data construction script is always wrong
- Every value in every CSV must trace to an identifiable real source

---

## Part II: Content Type Taxonomy

### Classification System

All figures in Shaikh's "Capitalism" fall into one of five content types:

| Type Code | Name | Description | Documentation |
|-----------|------|-------------|---------------|
| `empirical` | Empirical Time Series | Historical data with time dimension | DPR (Data Provenance Record) |
| `theoretical` | Theoretical Diagram | Conceptual illustration, no data | FPR (Figure Provenance Record) |
| `conceptual` | Conceptual Diagram | Explanatory diagram with stylized data | FPR |
| `simulation` | Simulation Output | Generated from computational model | FPR + Methodology Doc |
| `cross-sectional` | Cross-Sectional Data | Point-in-time empirical study | FPR + Source Doc |

### Decision Tree

```
Is there underlying time series data?
├── YES: Does it have a Series ID (S###)?
│   ├── YES → empirical → Create DPR
│   └── NO → Assign S### ID, then create DPR
└── NO: What type of content?
    ├── Conceptual/theoretical diagram → Create FPR
    ├── Computational model output → Create FPR + Methodology Doc
    └── Point-in-time empirical data → Create FPR + Source Doc
```

### Chapter Classification Summary

| Chapter | Primary Type | Series Count | Figure Count |
|---------|--------------|--------------|--------------|
| 2 | empirical | 18 | 19 |
| 3 | theoretical/simulation | 0 | 15 |
| 4 | theoretical | 1 | 23 |
| 5 | empirical | 6 | 6 |
| 6+ | mixed | varies | varies |

---

## Part III: Identity Systems

### Series Identifiers

```
SERIES IDENTIFIER FORMAT:
  - Series:     S###          (e.g., S026)
  - Subseries:  S###X         (e.g., S026A, S026B)
  - Reindexed:  S###X-R####   (e.g., S001B-R2010 = S001B reindexed to 2010)
  - Derived:    S###_CALC     (e.g., S026_CALC = calculated from components)
```

### Figure Identifiers

```
FIGURE IDENTIFIER FORMAT:
  - Figure:     Fig#.#        (e.g., Fig6.1)
  - Panel:      Fig#.#X       (e.g., Fig2.4A, Fig2.4B)
```

### Naming Conventions

| Content | File Name Format | Example |
|---------|------------------|---------|
| Data Provenance Record | `S###_DPR.md` | `S001_DPR.md` |
| Figure Provenance Record | `Fig#.#_FPR.md` | `Fig3.1_FPR.md` |
| Chapter Investigation | `CHAPTER_#_INVESTIGATION.md` | `CHAPTER_2_INVESTIGATION.md` |
| Validation Report | `CHAPTER_#_VALIDATION_REPORT.md` | `CHAPTER_2_VALIDATION_REPORT.md` |
| Methodology Document | `[NAME]_METHODOLOGY.md` | `ENGEL_CURVE_SIMULATIONS.md` |

---

## Part IV: Provenance Record Formats

### Data Provenance Record (DPR) - For Empirical Series

Required for all content with Series ID (S###).

```markdown
# S###: [Series Name] - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Series ID | S### |
| Figures | Fig#.# |
| Chapter | # |
| Time Period | YYYY-YYYY |
| Extension Status | [status] |
| Base Year | #### |
| Validation Status | [VALIDATED/PENDING] YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |

---

## Shaikh's Theoretical Context

> "[Quote from book]"
> — Shaikh (2016), p. ###

---

## Subsources

| ID | Source | Period | API | Quality |
|----|--------|--------|-----|---------|
| S###A | [Source] | YYYY-YYYY | [API] | [quality] |

---

## Transformation Chain

| Step | Operation | Input | Output |
|------|-----------|-------|--------|
| 1 | [operation] | [input] | [output] |

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Value Range | [range] | [range] | PASS/FAIL |
| Year Coverage | [years] | [years] | PASS/FAIL |

---

## Known Issues

- [Issue 1]

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| YYYY-MM-DD | 1.0 | Initial |
```

### Figure Provenance Record (FPR) - For Non-Series Figures

Required for theoretical, conceptual, simulation, and cross-sectional figures.

```markdown
# Fig#.#: [Figure Title] - Figure Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Figure ID | Fig#.# |
| Chapter | # |
| Page | ### |
| Type | [theoretical/conceptual/simulation/cross-sectional] |
| Linked Series | [S### or None] |
| Last Updated | YYYY-MM-DD |

---

## Shaikh's Caption

> "[Full caption from book]"

---

## Content Description

### Variables/Elements
- [Variable 1]: [Description]

### Key Features
- [Feature 1]

---

## Shaikh's Observations

> "[Quote]"
> — Shaikh (2016), p. ###

---

## Theoretical Significance

[Explanation of why this figure matters]

---

## Source Information

### For Theoretical/Conceptual
- **Source**: Author's construction
- **Data Required**: None

### For Simulation
- **Model**: [Platform]
- **Parameters**: [Key parameters]
- **Methodology**: See [doc]

### For Cross-Sectional
- **Original Source**: [Citation]
- **Year**: [Data year]
- **Sample**: [Description]

---

## Related Content

- **Previous Figure**: Fig#.#
- **Next Figure**: Fig#.#
- **Related Series**: [S### if any]
```

---

## Part V: Transformation Audit Trail

Every transformation must be recorded in `TRANSFORMATION_LOG.json`:

```json
{
  "transformations": [
    {
      "transform_id": "T001",
      "timestamp": "2026-01-26T12:00:00Z",
      "series_affected": ["S001", "S002"],
      "operation": "growth_rate_splice",
      "description": "Splice BEA growth rates onto Shaikh levels",
      "formula": "Extended[t] = Shaikh[2010] × (BEA[t] / BEA[2010])",
      "formula_reference": "Shaikh (2016), Appendix 2.1",
      "parameters": {
        "splice_year": 2010
      },
      "script": "scripts/splice_series.py",
      "script_hash": "sha256:abc123...",
      "input_files": ["shaikh_original.csv", "bea_2017_base.csv"],
      "output_files": ["chapter_02_extended.csv"],
      "validation_result": "PASS",
      "notes": "7.63pp discontinuity at splice point"
    }
  ]
}
```

---

## Part VI: Chapter Investigation Template

Every chapter must have an investigation document with these sections:

```markdown
# Chapter # Anu Standard Investigation

## Overview

- **Chapter**: # - [Title]
- **Figures**: ## (Fig#.#-Fig#.#)
- **Series**: ## (S###-S###)
- **Data File**: [filename or None]
- **Investigation Date**: YYYY-MM-DD
- **Status**: ANU STANDARD COMPLIANT

---

## Content Summary

[Brief chapter description]

---

## Figure Inventory

| Figure ID | Page | Caption | Type | Series | Documentation |
|-----------|------|---------|------|--------|---------------|
| Fig#.# | ### | [caption] | [type] | [S### or -] | [DPR/FPR link] |

---

## Series Inventory (if applicable)

| Series ID | Name | Extension Status | Documentation |
|-----------|------|------------------|---------------|
| S### | [name] | [status] | [DPR link] |

---

## Data Sources

### [Source Name]
- **Reference**: [Citation]
- **Coverage**: [Period]
- **Quality**: [Assessment]

---

## Unified Compliance Checklist

### Documentation
- [ ] All figures classified by type
- [ ] DPR files for all empirical series
- [ ] FPR files for all non-series figures
- [ ] Shaikh observations captured

### Data (if empirical)
- [ ] Data file exists and loads
- [ ] HDARP linkages verified
- [ ] Transformations logged

### Testing (if empirical)
- [ ] Automated tests exist
- [ ] Value ranges validated
- [ ] Year coverage verified

---

## Documentation Files

| Type | Count | Location |
|------|-------|----------|
| DPR Files | # | docs/series/ |
| FPR Files | # | docs/figures/ |
| Methodology | # | docs/methodology/ |
| Tests | # | tests/ |

---

## Changelog

| Date | Changes |
|------|---------|
| YYYY-MM-DD | [change] |

---

*Chapter # achieved Anu Standard Compliance on YYYY-MM-DD*
```

---

## Part VII: Testing and Validation

### Automated Test Requirements

Each empirical chapter must have a test file with:

1. **Series existence tests** - All series in catalog
2. **Chapter assignment tests** - Correct chapter number
3. **HDARP linkage tests** - Figures resolve to data
4. **Subsource completeness** - All subsources documented
5. **Data file existence** - CSV files present
6. **Value range validation** - Within expected bounds
7. **Year coverage checks** - No unexpected gaps
8. **DPR file existence** - All series documented

### Validation Report

Each empirical chapter should have `CHAPTER_#_VALIDATION_REPORT.md`:

```markdown
# Chapter # Validation Report

## Data Files Validated
- [file]: [rows] rows, [status]

## Value Range Checks
| Series | Expected | Actual | Status |
|--------|----------|--------|--------|

## Year Coverage
| Series | Start | End | Gaps |
|--------|-------|-----|------|

## Conclusion
[VALIDATED/ISSUES FOUND]
```

---

## Part VIII: Quality Assessment Categories

| Category | Description | Reliability |
|----------|-------------|-------------|
| `official_statistics` | Government agencies (BEA, BLS, FRED) | HIGH |
| `academic_research` | Peer-reviewed sources | HIGH |
| `historical_reconstruction` | Reconstructed historical data | MEDIUM |
| `calculated` | Derived from other series | VARIES |
| `interpolated` | Gap-filled data | LOW |
| `external_estimate` | Third-party estimates | MEDIUM |
| `simulation` | Computational model output | N/A |
| `theoretical` | Author construction | N/A |

---

## Part IX: File Organization

```
DOCUMENTATION/
├── ANU_STANDARD_UNIFIED.md          # This file
├── CHAPTER_#_INVESTIGATION.md       # Per-chapter status
└── FIGURE_INDEX_CH#-#.md            # Figure indices

docs/
├── series/                          # DPR files (S###_DPR.md)
│   └── CHAPTER_#_VALIDATION_REPORT.md
├── figures/                         # FPR files (Fig#.#_FPR.md)
└── methodology/                     # Simulation/source docs

data/ShaikhAbsorbed/catalogs/
├── DEFINITIVE_SERIES_CATALOG.json   # Master series catalog
├── HDARP_SERIES_LINKAGE.json        # Figure-to-series mappings
├── SERIES_SUBSOURCES.json           # Subsource details
└── TRANSFORMATION_LOG.json          # Audit trail

tests/
├── test_data_mappings.R             # Global tests
├── test_chapter_02.R                # Chapter-specific tests
└── test_chapter_05.R
```

---

## Part X: Compliance Checklist

### For Empirical Content (S### Series)

- [ ] Series ID assigned (S###)
- [ ] Entry in DEFINITIVE_SERIES_CATALOG.json
- [ ] Subsources documented in SERIES_SUBSOURCES.json
- [ ] HDARP linkage in HDARP_SERIES_LINKAGE.json
- [ ] DPR file in docs/series/
- [ ] Transformations in TRANSFORMATION_LOG.json
- [ ] Automated tests in tests/
- [ ] Value ranges validated
- [ ] Year coverage verified

### For Non-Empirical Content (Figures without Series)

- [ ] Figure type classified
- [ ] FPR file in docs/figures/
- [ ] Shaikh caption captured
- [ ] Shaikh observations documented
- [ ] Theoretical significance explained
- [ ] Source information provided (if applicable)
- [ ] Methodology documented (if simulation)

### For Chapter Investigation

- [ ] Investigation document exists
- [ ] All figures inventoried with types
- [ ] All series inventoried (if applicable)
- [ ] Unified compliance checklist completed
- [ ] Status shows "ANU STANDARD COMPLIANT"

---

## Part XI: Error Codes

### Data Errors

| Code | Description | Action |
|------|-------------|--------|
| `CHAPTER_NOT_FOUND` | Chapter key missing | Verify file exists |
| `HDARP_MAPPING_MISSING` | Figure not in linkage | Add to HDARP_SERIES_LINKAGE.json |
| `SERIES_NOT_FOUND` | Series not in data | Verify series_name |
| `VALIDATION_FAILED` | Values outside range | Investigate source |

### Documentation Errors

| Code | Description | Action |
|------|-------------|--------|
| `DPR_MISSING` | No DPR for series | Create S###_DPR.md |
| `FPR_MISSING` | No FPR for figure | Create Fig#.#_FPR.md |
| `TYPE_UNKNOWN` | Figure not classified | Add type to inventory |
| `CAPTION_MISSING` | Shaikh caption not captured | Add to FPR |

---

## Part XII: Success Metrics

The Anu Standard is successful when:

- **100%** of figures have type classification
- **100%** of empirical series have DPR files
- **100%** of non-series figures have FPR files
- **100%** of transformations are logged
- **100%** of HDARP linkages pass automated tests
- **0** silent fallbacks in data retrieval code
- **Every** data issue can be diagnosed in <5 minutes

---

## Part XIII: v2.1 Enhancements - Appendix and Data Revision Coverage

### Appendix Integration Requirements

For chapters with source appendices (Ch 2, 4, 5, 6, 9, 10, 11, 14):

1. **Reference all relevant appendices** in DATA_UPDATES review documents
2. **Link to appendix data tables** in DPR files
3. **Document appendix methodology** in investigation documents
4. **Map appendix variables to series** in provenance records

### Data Revision Tracking Requirements

For all empirical series:

1. **Document original data vintage** (e.g., "Shaikh 2011 vintage")
2. **Track major methodology revisions** from primary sources
3. **Include revision dates and impact assessment**
4. **Provide URLs to current official methodology**

### v2.1 Supporting Documents

| Document | Location | Purpose |
|----------|----------|---------|
| `APPENDIX_REFERENCE_MATRIX.md` | DOCUMENTATION/ | Maps all 13 Shaikh appendices to series |
| `DATA_REVISION_LOG.md` | DOCUMENTATION/ | Tracks BEA, BLS, Fed revisions |
| `METHODOLOGY_URL_INDEX.md` | DOCUMENTATION/ | Official methodology URLs |
| `DATA_UPDATES_TEMPLATE.md` | Druck templates/ | Standard format for reviews |

### Appendix Coverage by Chapter

| Chapter | Appendices | Status |
|---------|------------|--------|
| 2 | App 2.1 | INTEGRATED |
| 4 | App 4.1, 4.2 | INTEGRATED |
| 5 | App 5.1, 5.2 | INTEGRATED |
| 6 | App 6.1, 6.7 | INTEGRATED |
| 9 | App 9.1, 9.2 | INTEGRATED |
| 10 | App 10.1 | INTEGRATED |
| 11 | App 11.1 | INTEGRATED |
| 14 | App 14.1, 14.2 | INTEGRATED |

**Total: 13 appendices mapped, 39 BEA tables referenced, 120+ variables defined**

---

## Part XIV: Subsource Metadata and Visualization Standard (v2.2)

### Purpose

This section defines the enhanced metadata requirements for subsources and the visualization architecture for displaying subsource-specific data in the Shiny app.

### Required Metadata Fields in SERIES_SUBSOURCES.json

When absorbing data from Shaikh Chopped sheets, each subsource entry MUST include:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `subsource_id` | string | YES | Unique identifier (e.g., "S001A") |
| `source_name` | string | YES | Data source name (e.g., "BEA", "FRED") |
| `time_period_start` | integer | YES | First year of data coverage |
| `time_period_end` | integer | YES | Last year of data coverage |
| `is_shaikh_original` | boolean | YES | True if from Shaikh's original book data |
| `shaikh_end_year` | integer | YES | Last year of Shaikh's original data for this subsource |
| `splice_year` | integer/null | NO | Year where splice occurs (if applicable) |
| `splice_method` | string/null | NO | Splice method: "growth_rate_splice", "level_match", "direct_append" |
| `parent_series` | string | YES | Parent series ID (e.g., "S001") |

### Example Enhanced Subsource Entry

```json
{
  "S001B": {
    "subsource_id": "S001B",
    "source_name": "Federal Reserve",
    "time_period_start": 1919,
    "time_period_end": 2025,
    "is_shaikh_original": false,
    "shaikh_end_year": 2010,
    "splice_year": 2010,
    "splice_method": "growth_rate_splice",
    "parent_series": "S001",
    "note": "Extended via growth rate splice at 2010."
  }
}
```

### Visualization Architecture

Each subsource is rendered as a separate Plotly **trace** on the same chart:

- One `add_trace()` call per subsource
- Distinct color per subsource from the `subsource_colors` palette
- All traces overlap on the same chart (not separate charts)
- Legend shows: subsource_id, source_name, date range
- Interactive: hover, zoom, pan, legend toggle

### View Modes

The subsource selector UI supports these view modes:

| Mode | Selector Value | Filter Logic | Description |
|------|---------------|--------------|-------------|
| Full View | `"full_view"` | None | All subsources visible as overlapping traces |
| Shaikh Construction | `"shaikh_construction"` | `is_shaikh_original = true` | Only original Shaikh data |
| Final Extension | `"final_extension"` | `is_shaikh_original = false` | Only extension data |
| Individual | `subsource_id` (e.g., "S001A") | Match by ID | Single subsource visible |

### Shaikh Boundary Visualization

- Gold dashed vertical line at each unique `shaikh_end_year` value
- Label: "Shaikh ends: YYYY"
- Per-series boundaries (not a global 2010 assumption)
- Only displayed for extension subsources (where `is_shaikh_original = false`)

### Absorption Process Requirements

When absorbing data from Shaikh Chopped sheets:

1. **Extract start/end years** for each subsource from the source data
2. **Identify Shaikh original vs extensions** - set `is_shaikh_original` flag
3. **Document splice points** - extract `splice_year` from notes or DPR files
4. **Document splice methods** - set `splice_method` to describe how series were combined
5. **Populate all required metadata fields** in SERIES_SUBSOURCES.json

### Related Functions

| Function | File | Purpose |
|----------|------|---------|
| `filter_subsources_by_mode()` | `R/data_loader.R` | Filters subsources by view mode using `is_shaikh_original` |
| `filter_data_to_subsources()` | `R/data_loader.R` | Filters data to year ranges of filtered subsources |
| `add_shaikh_boundary_lines()` | `R/chart_builder.R` | Adds boundary lines using `shaikh_end_year` metadata |
| `build_subsource_colored_chart()` | `R/chart_builder.R` | Builds Plotly chart with overlapping traces |

---

## Part XV: Anu Chopped Standard - Self-Documenting CSV Database

The Anu Chopped Standard defines the canonical input data format for the CD2 project. It sits at the very beginning of the Anu Suite pipeline, converting raw Excel/PDF/API sources into structured, self-documenting CSV files.

### Format

Every Anu Chopped CSV has exactly this structure:

| Row | Purpose | Content |
|-----|---------|---------|
| 1 | **Metadata** | Per-column description: source citation, methodology, base year, units, coverage |
| 2 | **Subseries ID** | Unique identifier per column (e.g., `S001A`, `S001B`, `S001`) |
| 3+ | **Data** | Date/index in column 1, numeric values in remaining columns |

### Key Rules

1. **R1**: Every data column has metadata (Row 1) and a subseries ID (Row 2)
2. **R2**: IDs follow `S###A/B/C` for subsources, `S###` (no suffix) for final series
3. **R3**: Columns ordered: raw subsources → transformations → final series (left to right)
4. **R4**: Missing values are empty cells (not NA, not NaN, not 0)
5. **R5**: One CSV per original source file, organized in `ch##/` subdirectories
6. **R6**: The rightmost data column is always the final published series

### Integration

```
Raw Sources (Excel/PDF/API)
    → anu-chopped (standardize to CSV)
    → anu-standard (create DPR/EPR)
    → anu-extension (extend to 2025)
    → anu-extenbook (visualize)
    → anu-review (audit)
```

### Catalog

Every dataset has a companion `ANU_CHOPPED_CATALOG.json` linking files, columns, and subseries IDs with full column-level metadata.

### Full Specification

See `anu-chopped/SKILL.md` for complete format specification, validation rules, and conversion workflow.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-26 | Initial quantitative standard |
| 1.1 | 2026-01-27 | Added qualitative extension reference |
| 2.0 | 2026-01-27 | **Unified standard** - merged quantitative and qualitative into single definitive document |
| 2.1 | 2026-01-28 | **Appendix and Revision Enhanced** - added appendix integration requirements, data revision tracking |
| 2.2 | 2026-01-31 | **Subsource Visualization Standard** - added Part XIV with enhanced metadata fields (is_shaikh_original, shaikh_end_year, splice_year, splice_method), view mode filtering, overlapping Plotly traces, per-series boundary visualization |
| 2.3 | 2026-02-11 | **Anu Chopped Standard** - added Part XV defining canonical self-documenting CSV input format, pipeline integration |

---

*The Anu Standard ensures that every piece of content in the CD2 project - whether empirical data, theoretical diagram, or simulation output - can be fully traced, documented, and reproduced.*
