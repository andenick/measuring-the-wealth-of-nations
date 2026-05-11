---
name: anu-review
description: Systematic audit tool for reviewing data chapter/module integration quality. Validates compliance with Anu Standard, Anu Extension Standard, and Anu Shiny Standard. Use when reviewing chapter implementations, auditing data construction projects, or validating integration completeness.
argument-hint: [chapter] or [action] [target]
allowed-tools: Read, Write, Grep, Glob, LS
---

# The Anu Review: Integration Quality Audit Framework

A systematic audit tool for reviewing how well data chapters/modules are integrated into a data construction project. Part of the Anu Suite of tools.

---

## Quick Reference

### Purpose

The Anu Review validates compliance with:
- **Anu Standard v2.1** - Data provenance and quality
- **Anu Extension Standard v1.0** - Maximum faithfulness data extension
- **Anu Shiny Standard v1.0** - Visualization application integration

### When to Use This Skill

Apply the Anu Review when:
- Completing a chapter integration
- Auditing existing data construction work
- Comparing implementation quality across chapters
- Identifying gaps in documentation or code
- Preparing for project milestones or handoffs

---

## Commands

```
/anu-review [chapter]           # Review single chapter (e.g., /anu-review 2)
/anu-review full [project]      # Review entire project
/anu-review compare [ch1] [ch2] # Compare two chapters
/anu-review gaps [chapter]      # Show only gaps
/anu-review score [chapter]     # Show only score
/anu-review checklist [chapter] # Show checklist with pass/fail
```

---

## Review Dimensions

The Anu Review evaluates 8 dimensions with weighted scoring:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **DPR Completeness** | 15% | Data Provenance Records for all series |
| **EPR Completeness** | 15% | Extension Provenance Records for extended series |
| **Data File Integrity** | 15% | CSV structure, column mapping, year ranges |
| **Series Mapping** | 15% | CH[X]_SERIES_MAPPING completeness in data_loader.R |
| **Chart Builder Integration** | 10% | Specialized builders and helper functions |
| **Test Coverage** | 10% | test_chapter_XX.R exists and covers all series |
| **Catalog Consistency** | 10% | FIGURE_SERIES_CATALOG.json accuracy |
| **Knowledge Base Integration** | 10% | Web research, source quotes documented |

---

## Scoring Methodology

### Integration Score Calculation

```
Integration Score = 
  (DPR_Score × 15%) +
  (EPR_Score × 15%) +
  (DataFile_Score × 15%) +
  (Mapping_Score × 15%) +
  (ChartBuilder_Score × 10%) +
  (TestCoverage_Score × 10%) +
  (Catalog_Score × 10%) +
  (KnowledgeBase_Score × 10%)
```

### Certification Levels

| Level | Score | Description |
|-------|-------|-------------|
| **EXEMPLARY** | ≥95% | Reference implementation, exceeds all standards |
| **COMPLETE** | ≥85% | Fully integrated, meets all core requirements |
| **ADEQUATE** | ≥70% | Functional with documented gaps |
| **INCOMPLETE** | <70% | Requires attention before production use |

---

## Dimension Checklists

### 1. DPR Completeness (15%)

For each series in the chapter:

- [ ] DPR file exists (`[SERIES_ID]_DPR.md`)
- [ ] Quick Reference table complete
- [ ] Shaikh context/quotes included
- [ ] Subsources documented with quality categories
- [ ] Transformation chain documented
- [ ] Validation record present
- [ ] HDARP linkage documented (if applicable)

**Scoring**: `(Complete DPRs / Total Series) × 100`

### 2. EPR Completeness (15%)

For each extended series:

- [ ] EPR file exists (`[SERIES_ID]_EPR.md`)
- [ ] Agent understanding statement present
- [ ] Book context with actual quotes
- [ ] Original methodology documented
- [ ] Current methodology documented
- [ ] Methodology changes assessment
- [ ] Transition analysis with metrics
- [ ] Faithfulness score calculated
- [ ] Certification status assigned

**Scoring**: `(Complete EPRs / Extended Series) × 100`

### 3. Data File Integrity (15%)

- [ ] `chapter_XX_data.csv` exists
- [ ] `chapter_XX_extended.csv` exists (if extended series present)
- [ ] All series have data columns
- [ ] Year ranges match DPR documentation
- [ ] No missing values in required columns
- [ ] Column names match mapping patterns

**Scoring**: Based on file existence and column coverage

### 4. Series Mapping (15%)

In `data_loader.R`:

- [ ] `CH[X]_SERIES_MAPPING` exists
- [ ] All series included in mapping
- [ ] `data_patterns` defined for each series
- [ ] `subsources` listed for each series
- [ ] `description` present for each series
- [ ] Special flags set correctly (`is_extended`, `is_conceptual`, etc.)
- [ ] `shaikh_finding` documented for each series

**Scoring**: `(Complete Mappings / Total Series) × 100`

### 5. Chart Builder Integration (10%)

In `chart_builder.R`:

- [ ] Specialized chart builder exists (if unique visualization needed)
- [ ] Helper functions defined (`is_chapter[X]_series`, etc.)
- [ ] Chart builder handles all series types
- [ ] Error handling for missing data
- [ ] Plotly configuration complete

**Scoring**: Based on builder coverage and functionality

### 6. Test Coverage (10%)

- [ ] `tests/test_chapter_XX.R` exists
- [ ] CHAPTER_METADATA tests present
- [ ] Series mapping tests present
- [ ] Data file tests present
- [ ] DPR/EPR existence tests present
- [ ] Figure catalog tests present
- [ ] Helper function tests present
- [ ] Thematic tests for Shaikh findings

**Scoring**: `(Test Sections Present / Required Sections) × 100`

### 7. Catalog Consistency (10%)

In `FIGURE_SERIES_CATALOG.json`:

- [ ] All chapter figures present
- [ ] `series_ids` correct for each figure
- [ ] `chapter` field correct
- [ ] `is_empirical` flag correct
- [ ] `year_start`/`year_end` populated
- [ ] `description` present

**Scoring**: `(Correct Figures / Total Figures) × 100`

### 8. Knowledge Base Integration (10%)

- [ ] Web research documented for key series
- [ ] Source quotes extracted and cited
- [ ] Methodology changes researched
- [ ] Data source URLs documented
- [ ] API endpoints documented (if applicable)

**Scoring**: Based on documentation completeness

---

## Review Process

### Step 1: Gather Information

1. Identify chapter number and expected series range
2. Load CHAPTER_METADATA for chapter details
3. List all series in CH[X]_SERIES_MAPPING
4. Identify which series are extended vs conceptual

### Step 2: Run Dimension Checks

For each dimension:
1. Execute checklist items
2. Record pass/fail for each item
3. Calculate dimension score
4. Note specific gaps

### Step 3: Calculate Overall Score

1. Apply dimension weights
2. Sum weighted scores
3. Determine certification level

### Step 4: Generate Report

1. Populate REVIEW_REPORT template
2. List all gaps in GAP_ANALYSIS
3. Prioritize action items
4. Provide specific recommendations

---

## Output Templates

### Review Report

See `templates/REVIEW_REPORT_TEMPLATE.md`

### Checklist

See `templates/CHECKLIST_TEMPLATE.md`

### Gap Analysis

See `templates/GAP_ANALYSIS_TEMPLATE.md`

---

## Integration with Other Anu Tools

The Anu Review complements:

- **`/anu-standard`** - Creates DPR/FPR documentation
- **`/anu-extension`** - Creates EPR documentation, runs extensions
- **Anu Shiny Standard** - Defines visualization requirements

### Recommended Workflow

1. Complete chapter integration work
2. Run `/anu-review [chapter]` to assess
3. Address gaps identified in report
4. Re-run review until COMPLETE or EXEMPLARY

---

## Example Review Output

```
=============================================================
                 ANU REVIEW REPORT: Chapter 2
=============================================================

Quick Reference:
  Chapter:           2
  Title:             Turbulent Macro Dynamics
  Series:            S001-S018 (18 total)
  Integration Score: 85%
  Status:            COMPLETE

Dimension Scores:
  DPR Completeness:        100% (18/18)
  EPR Completeness:        67%  (12/18 - 6 not extended)
  Data File Integrity:     90%  (extended CSV incomplete)
  Series Mapping:          100% (18/18)
  Chart Builder:           80%  (generic builders used)
  Test Coverage:           100% (comprehensive)
  Catalog Consistency:     100% (all correct)
  Knowledge Base:          70%  (partial documentation)

Gaps Identified:
  1. Extended CSV missing columns for S008, S011-S018
  2. S016 marked needs_source = TRUE
  3. No specialized chart builders for profit rate series

Action Items:
  [HIGH] Complete extended CSV with missing series
  [MED]  Investigate S016 source data
  [LOW]  Consider specialized builders for S013-S015

=============================================================
```

---

## File Locations (CD2 Project)

| Content | Location |
|---------|----------|
| DPR/EPR files | `Technical/ShinyApp/docs/series/` |
| Chapter data | `Technical/ShinyApp/data/ShaikhAbsorbed/chapter_XX_data.csv` |
| Extended data | `Technical/ShinyApp/data/ShaikhAbsorbed/chapter_XX_extended.csv` |
| Series mapping | `Technical/AnuShinyApp/R/data_loader.R` |
| Chart builders | `Technical/AnuShinyApp/R/chart_builder.R` |
| Tests | `Technical/AnuShinyApp/tests/test_chapter_XX.R` |
| Figure catalog | `Technical/ShinyApp/data/ShaikhAbsorbed/catalogs/FIGURE_SERIES_CATALOG.json` |

---

## Version History

- **v1.0** (January 2026) - Initial release as part of Anu Suite

---

*Part of the Anu Suite: Anu Standard | Anu Extension | Anu Shiny | **Anu Review***
