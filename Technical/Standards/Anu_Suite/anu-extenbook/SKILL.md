# Anu Extenbook Skill

## Overview

| Property | Value |
|----------|-------|
| Skill Name | Anu Extenbook |
| Version | 1.0 |
| Part Of | Anu Suite |
| Created | 2026-01-30 |
| Purpose | Generate series-level Excel workbooks showing complete data construction |

---

## Purpose

Generate **series-level Excel workbooks** that expose every subcomponent, transformation, and provenance detail of a data series. Each workbook is a complete, self-contained visualization of data construction.

### Key Differentiators

| Aspect | Previous Extenbooks | Anu Extenbooks |
|--------|---------------------|----------------|
| Unit | Chapter or Figure | **Series** |
| Data Content | Limited or none | **All subcomponents visible** |
| Transformations | Described in text | **Visible as columns** |
| Splice Points | Documented | **Visible in data rows** |
| Provenance | Separate files | **Integrated Sheet 2** |

---

## When to Use

Use the Anu Extenbook skill when:

- After completing DPR/EPR for a series
- During chapter review to visualize all subcomponents
- For quality assurance and validation of extended data
- To provide reviewers with transparent data construction
- Complementing Anu Shiny Standard with spreadsheet visualization

---

## Prerequisites

Before generating an Anu Extenbook:

1. **DPR Exists**: Data Provenance Record for the series (`S###_DPR.md`)
2. **EPR Exists** (if extended): Extension Provenance Record (`S###_EPR.md`)
3. **Subsource Data**: Shaikh Absorbed data available
4. **Series Catalog**: Entry in `DEFINITIVE_SERIES_CATALOG.json`

---

## Workflow

### Step 1: Verify Prerequisites

```bash
# Check DPR exists
ls docs/series/S###_DPR.md

# Check EPR exists (for extendable series)
ls docs/series/S###_EPR.md

# Verify subsource catalog
cat catalogs/SERIES_SUBSOURCES.json | grep "S###"
```

### Step 2: Generate Extenbook

```bash
python create_anu_extenbooks.py --series S###
```

Or for entire chapter:

```bash
python create_anu_extenbooks.py --chapter 2
```

### Step 3: Review Output

Open generated file:
```
Outputs/Anu_Extenbooks/Chapter_##/Anu_Extenbook_S###.xlsx
```

Verify:
- All subsources appear as separate columns
- Splice points highlighted
- Final series matches known values
- Provenance sheet is complete

### Step 4: Validate Against Original

Compare with Shaikh Chopped source:
```
Inputs/ShaikhChoppedTables/Appendix#_*.xlsx
```

---

## Workbook Structure

### Sheet 1: Data

**Purpose**: Show all subcomponents and transformations laid out plain.

**Structure**:

| Row | Content |
|-----|---------|
| 0 | Metadata (column-specific source citations) |
| 1 | Headers (subsource IDs and descriptions) |
| 2+ | Data (year-indexed values) |

**Columns**:

| Column | Content | Color |
|--------|---------|-------|
| A | Year | White |
| B-N | Subsources (S###A, S###B, etc.) | Light Yellow (original) / Light Blue (extension) |
| O+ | Transformations (Rebased, Spliced) | Light Orange |
| Last | FINAL (extended series) | Light Green |

**Visual Indicators**:
- Splice years: Yellow row background
- Empty cells (NaN): Light gray
- Active ranges: Column-specific coloring

### Sheet 2: Provenance

**Purpose**: Complete DPR/EPR documentation in structured format.

**Sections**:

| Rows | Section | Content |
|------|---------|---------|
| 1-3 | Series Overview | ID, Title, Chapter, Figures, Period, Status |
| 5-12 | Theoretical Context | Shaikh quotes, relevance |
| 14-25 | Subsources | Table with ID, Source, Period, API, Quality |
| 27-40 | Transformation Chain | Step, Operation, Formula, Input, Output |
| 42-55 | Extension Details | Sources, Splice Method, Transition Metrics |
| 57-65 | Validation | Range checks, correlations, test results |
| 67-75 | Certification | Faithfulness score, status, notes |
| 77-85 | Divergences | ADR entries affecting this series |
| 87-95 | References | DPR, EPR, data file locations |

---

## File Naming Convention

```
Anu_Extenbook_S###.xlsx
```

Examples:
- `Anu_Extenbook_S001.xlsx` - US Industrial Production Index
- `Anu_Extenbook_S013.xlsx` - US Corporate Rate of Profit
- `Anu_Extenbook_S047.xlsx` - Market Prices vs Direct Prices

---

## Output Location

```
Outputs/Anu_Extenbooks/
├── Chapter_02\
│   ├── Anu_Extenbook_S001.xlsx
│   ├── Anu_Extenbook_S002.xlsx
│   └── ...
├── Chapter_09\
│   └── ...
└── SUMMARY\
    └── Anu_Extenbook_Master_Index.xlsx
```

---

## Color Coding Standard

| Element | Hex Color | Usage |
|---------|-----------|-------|
| Header Row | #4472C4 | Column headers (Row 1) |
| Metadata Row | #D9E2F3 | Row 0 metadata |
| Subsource Original | #FFF2CC | Shaikh's original subsources |
| Subsource Extension | #E6F2FF | API extension data |
| Transformation | #FCE4D6 | Intermediate calculations |
| Final Series | #E6FFE6 | Final spliced series |
| Splice Row | #FFFF00 | Splice point highlight |
| NaN/Empty | #F2F2F2 | Inactive ranges |

---

## Integration with Anu Suite

| Component | Relationship |
|-----------|-------------|
| Anu Standard | Extenbook visualizes DPR documentation |
| Anu Extension Standard | Extenbook visualizes EPR methodology |
| Anu Review | Extenbook aids quality review |
| Anu Shiny Standard | Complements interactive visualization |

---

## Validation Checklist

For each generated Anu Extenbook:

- [ ] All subsources visible as separate columns
- [ ] Splice points clearly marked with yellow highlighting
- [ ] Final series matches known values from DPR/EPR
- [ ] Provenance sheet contains complete DPR/EPR information
- [ ] Color coding applied correctly per standard
- [ ] Links to source files accurate in references section
- [ ] Comparison with Shaikh Chopped original validates accuracy

---

## Troubleshooting

### Missing Subsource Data

```
Error: Subsource S###A not found in Shaikh Absorbed
```

**Solution**: Run absorption script for the chapter:
```bash
python absorb_shaikh_chopped_v3.py --chapter ##
```

### DPR/EPR Not Found

```
Error: DPR file not found for S###
```

**Solution**: Create DPR first using Anu Standard skill.

### Splice Point Mismatch

If splice point values don't match between subsources:

1. Check transition analysis in EPR
2. Verify splice year is correct
3. Review rebasing methodology

---

## Templates

Templates location: `Council/Druck/.claude/skills/anu-extenbook/templates/`

- `EXTENBOOK_DATA_TEMPLATE.md` - Sheet 1 structure guide
- `EXTENBOOK_PROVENANCE_TEMPLATE.md` - Sheet 2 structure guide

---

## Related Documentation

- Full standard: `Council/Druck/docs/ANU_EXTENBOOK_STANDARD.md`
- Rules file: `Council/Druck/.cursor/rules/anu-extenbook.md`
- Script: `Technical/scripts/create_anu_extenbooks.py`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-30 | Initial release |

---

*Part of the Anu Suite - Data Construction Visualization*
