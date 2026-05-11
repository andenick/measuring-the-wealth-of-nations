---
name: anu-extension
description: Apply Anu Extension Standard for maximally faithful data series extension. Use when extending time series data from historical to current periods. Requires HDARP extractions as inputs. Builds on anu-standard.
argument-hint: [action] [series_id]
allowed-tools: Read, Write, Grep, Glob, LS, WebSearch
requires: anu-standard
---

# Anu Extension Standard: Maximum Faithfulness Data Extension Framework

A rigorous framework for extending economic data series with complete fidelity to original construction methodology. Every extension must be traceable, documented, and validated.

---

## Core Philosophy

The Anu Extension Standard ensures that extended data is **EXACTLY** what would have been produced if the original methodology were applied to new data. This requires:

1. **Complete Understanding** - Know exactly what data was used originally
2. **Methodology Fidelity** - Apply identical transformations
3. **Source Verification** - Confirm data sources match
4. **Transition Validation** - Verify seamless connection at splice points

---

## Ten Principles of Extension Faithfulness

1. **UNDERSTAND BEFORE EXTENDING** - Read all source documentation (HDARP extracts)
2. **DOCUMENT AGENT REASONING** - Write detailed explanation of understanding
3. **SOURCE MATCH VERIFICATION** - Confirm original and extension sources are identical
4. **METHODOLOGY COMPARISON** - Quote old vs new methodology documentation
5. **BOOK CONTEXT INTEGRATION** - Include source quotes from chapters and appendices
6. **TRANSFORMATION REPLICATION** - Apply exact same transformations
7. **TRANSITION ANALYSIS** - Validate splice points with statistical tests
8. **VINTAGE TRACKING** - Record all data vintage dates
9. **QUOTE EVERYTHING** - Include actual quotes from all documentation
10. **FAIL ON UNCERTAINTY** - Stop if methodology unclear, do not guess

---

## Prerequisites

Before using this skill, ensure:

1. **Anu Standard Documentation Exists**
   - DPR file for the series (`S###_DPR.md`)
   - Series registered in `DEFINITIVE_SERIES_CATALOG.json`

2. **HDARP Extractions Available**
   - Book chapters and appendices (full text)
   - Original methodology PDFs (BEA, BLS, etc.)
   - Current methodology PDFs
   - All source quotes must come from HDARP extractions
   - **NO DIRECT PDF READING** - All content via HDARP

3. **Transition Analysis Capability**
   - Access to `transition_analysis.py` or equivalent
   - Historical baseline data for comparison

---

## Commands

### Planning Commands

```
/anu-extension plan [series_id]
```
Create comprehensive extension plan for a series. Outputs:
- Prerequisite checklist
- Source identification
- Methodology comparison plan
- Transformation replication plan
- Validation test plan

```
/anu-extension understand [series_id]
```
Document agent's understanding of the series. Outputs:
- What the data represents
- Original source documentation
- How it was constructed
- What figures use this data
- Relevant book quotes

### Research Commands

```
/anu-extension compare-methodology [series_id]
```
Compare original vs current methodology. Outputs:
- Old methodology quotes (from HDARP extractions)
- Current methodology quotes (from HDARP extractions)
- Web research findings on methodology changes
- Impact assessment

```
/anu-extension book-context [series_id]
```
Extract all relevant book context. Outputs:
- Chapter references with quotes
- Appendix references with quotes
- Variable definitions
- Formulas
- Figure usage

### Execution Commands

```
/anu-extension extend [series_id]
```
Execute the extension with full documentation. Outputs:
- Extended data file
- TRANSFORMATION_LOG entries
- Intermediate validation results

```
/anu-extension transition-analysis [series_id]
```
Run transition analysis at splice points. Outputs:
- Overlap period metrics
- Connection ratio
- Growth rate continuity
- Trend alignment
- Transition visualization reference

### Validation Commands

```
/anu-extension validate [series_id]
```
Run full validation suite. Outputs:
- Range validation results
- Cross-reference validation
- Automated test results
- Issue identification

```
/anu-extension certify [series_id]
```
Generate final certification. Outputs:
- Faithfulness score calculation
- EPR file generation
- EXTENSION_LOG.json entry
- DPR update with extension info

### Divergence Tracking Commands

```
/anu-extension log-divergence [series_id]
```
Document a methodology divergence discovered during extension. Outputs:
- New entry in DIVERGENCE_REGISTER.json
- ADR-### identifier assigned
- Linked to affected EPR files

```
/anu-extension list-divergences
```
Show all divergences in the project. Outputs:
- Summary of pending decisions
- Resolved divergences
- Statistics by category

```
/anu-extension resolve-divergence [ADR-###]
```
Record resolution decision for a divergence. Outputs:
- Updated DIVERGENCE_REGISTER.json
- Updated EPR files with resolution
- Decision documentation

---

## 10-Step Extension Workflow (with Divergence Tracking)

### Step 1: Prerequisite Check

Before any extension work:

- [ ] Verify DPR exists for series
- [ ] Verify HDARP extractions exist for book content
- [ ] Verify HDARP extractions exist for methodology PDFs
- [ ] If missing, document what is needed and STOP

**Output**: Prerequisite status report

### Step 2: Agent Understanding Document

Agent writes comprehensive explanation answering:

1. **What do I think this data is?**
   - Economic meaning and significance
   - How it fits in broader analysis

2. **What was the original data source?**
   - Exact source name, table, and line items
   - Time period covered
   - Units and frequency

3. **How was it constructed?**
   - Step-by-step transformation chain
   - Any splicing or adjustments

4. **What figures use this data?**
   - List all figures referencing this series
   - How series appears in each figure

5. **What does the source say about it?**
   - Relevant quotes from chapters
   - Relevant quotes from appendices

**Output**: Understanding statement in EPR file

### Step 3: Book Context Extraction

From HDARP book extractions, gather:

| Content | Source | Purpose |
|---------|--------|---------|
| Chapter quotes | `Knowledge_Base/HDARP_v3.3_Campaign/Body_Text/` | Context and interpretation |
| Appendix quotes | `Knowledge_Base/HDARP_v4.0_Figure_Metadata/Chapter_18_Appendices/` | Methodology details |
| Variable definitions | Appendix JSON files | Exact formulas |
| Formulas | `FORMULA_CHAINS.json` | Transformation specifications |
| Figure usage | `hdarp_v4/ch*_figures.json` | Visual representation |

**Output**: Book Context section in EPR file

### Step 4: Original Methodology Documentation

From HDARP methodology extractions:

1. **Identify Original Vintage**
   - Find methodology documentation from original data period
   - Example: BEA 2011 vintage for Shaikh's original data

2. **Extract Key Quotes**
   - Definition of series/table
   - Calculation methodology
   - Any special procedures

3. **Document Original Formulas**
   - Mathematical expressions
   - Variable definitions
   - Units and base years

**Source Location**: `Knowledge_Base/HDARP_Methodology_Sources_2025.12.22/`

**Output**: Original Methodology section in EPR file

### Step 5: Current Methodology Research

1. **Read Current HDARP Methodology Extractions**
   - Find latest methodology documentation
   - Example: BEA 2024 methodology

2. **Web Search for Changes**
   - Search for comprehensive revisions
   - Search for methodology updates
   - Document findings with URLs and dates

3. **Compare Old vs New**
   - Create side-by-side comparison
   - Quote both old and new methodology
   - Assess impact: HIGH / MEDIUM / LOW / NONE

**Output**: Current Methodology and Methodology Comparison sections in EPR file

### Step 5.5: Divergence Check (NEW)

After completing methodology research, assess whether any divergences require logging:

1. **Identify Divergences**
   - Did the source agency change their methodology?
   - Are there coverage, classification, or definition changes?
   - Is there a discontinuity that cannot be explained?

2. **Assess Significance**
   - Quantify the impact if possible (level discontinuity, %)
   - Determine if it affects the theoretical analysis
   - Consider if the original author was aware of this

3. **Log if Necessary**
   - If divergence is significant (>5% impact or methodological break):
     - Create entry in `DIVERGENCE_REGISTER.json`
     - Assign ADR-### identifier
     - Document options for resolution
   - If minor (<5% impact, same core methodology):
     - Note in EPR but do not log as formal divergence

4. **Continue Extension**
   - Divergences do NOT block extension
   - Extensions proceed with "CERTIFIED WITH NOTES" status
   - Decisions are made at end of chapter/project

**Divergence Categories**:
- `source_methodology_change` - Agency changed calculation/collection
- `coverage_change` - What's included/excluded changed
- `classification_change` - Industry/sector classification updated
- `base_year_change` - Reference period shifted
- `discontinuity` - Data break with no documented cause
- `definition_change` - Conceptual change in what's measured

**Output**: Entry in DIVERGENCE_REGISTER.json (if applicable), note in EPR file

### Step 6: Transformation Replication Plan

1. **List All Original Transformations**
   - From DPR transformation chain
   - From appendix methodology
   - From TRANSFORMATION_LOG.json

2. **Identify Equivalent Current Operations**
   - Map each original transform to current equivalent
   - Note any that differ

3. **Flag Non-Replicable Items**
   - Document any transformations that cannot be exactly replicated
   - Explain why and propose alternatives

4. **Document Rationale**
   - Justify each transformation choice
   - Reference methodology documentation

**Output**: Transformation Replication Plan in EPR file

### Step 7: Extension Execution

1. **Fetch New Data**
   - Use documented API endpoints
   - Record download timestamp and vintage date
   - Save raw data file

2. **Apply Transformations**
   - Execute each transformation from plan
   - Log in TRANSFORMATION_LOG.json
   - Use Transform IDs: T101, T102, ... for extensions

3. **Intermediate Validation**
   - Check value ranges at each step
   - Verify units and base years
   - Document any issues

**Output**: Extended data file, TRANSFORMATION_LOG entries

### Step 8: Transition Analysis

Run comprehensive transition analysis:

1. **Calculate Overlap Period Metrics**
   ```
   Connection Ratio = Extension_Value(overlap_start) / Original_Value(overlap_start)
   Target: 0.95 - 1.05
   ```

2. **Growth Rate Continuity**
   ```
   Growth_Difference = |Extension_Growth - Original_Growth| at transition
   Target: < 5%
   ```

3. **Trend Alignment**
   ```
   Correlation of original and extension in overlap period
   Target: > 0.95
   ```

4. **Level Difference**
   ```
   Percent difference at transition point
   Target: < 3%
   ```

5. **Generate Transition Plot**
   - Original series
   - Extended series
   - Overlap period highlighted

**Classification**:
- SEAMLESS: All metrics pass
- ACCEPTABLE: Minor deviations, documented
- PROBLEMATIC: Significant deviations, requires review
- FAILED: Cannot proceed, methodology mismatch

**Output**: Transition Analysis section in EPR file

### Step 9: Validation Suite

1. **Range Validation**
   - Check min/max against expected bounds
   - Flag outliers

2. **Cross-Reference Validation**
   - Compare to related series
   - Check correlations match historical patterns

3. **Automated Tests**
   - Run test suite for series
   - Document all results

4. **Documentation Completeness**
   - All EPR sections filled
   - All quotes documented
   - All transformations logged

**Output**: Validation Results section in EPR file

### Step 10: Certification

1. **Calculate Faithfulness Score**
   ```
   Faithfulness Score = 
     (Methodology_Match × 30%) +
     (Source_Match × 20%) +
     (Transformation_Replication × 20%) +
     (Transition_Quality × 20%) +
     (Documentation_Completeness × 10%)
   ```

2. **Determine Certification Status**
   - CERTIFIED: Score >= 90%, all criteria met
   - CERTIFIED WITH NOTES: Score >= 75%, documented deviations
   - NOT CERTIFIED: Score < 75% or critical failures

3. **Generate EPR File**
   - Complete all sections
   - Include all quotes and references
   - Sign with agent info

4. **Update Extension Log**
   - Add entry to EXTENSION_LOG.json
   - Link to EPR file

5. **Update DPR**
   - Add extension information to original DPR
   - Cross-reference EPR file

**Output**: Complete EPR file, EXTENSION_LOG entry, updated DPR

---

## Output Files

### Extension Provenance Record (EPR)

File naming: `[SERIES_ID]_EPR.md`
Location: Same as DPR files (e.g., `docs/series/S001_EPR.md`)

Template: `templates/EPR_TEMPLATE.md`

### Extension Log

File: `EXTENSION_LOG.json`
Location: With TRANSFORMATION_LOG.json

Schema:
```json
{
  "anu_extension_version": "1.0",
  "project": "[Project Name]",
  "extensions": [
    {
      "extension_id": "EXT001",
      "series_id": "S001",
      "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
      "agent": "[model-name]",
      "session": "[session-id]",
      "original_period": "YYYY-YYYY",
      "extension_period": "YYYY-YYYY",
      "methodology_match": true,
      "transition_status": "SEAMLESS",
      "faithfulness_score": 98,
      "certification": "CERTIFIED",
      "epr_file": "path/to/EPR.md",
      "transform_ids": ["T101", "T102"],
      "validation_result": "PASS",
      "notes": ""
    }
  ]
}
```

---

## Integration with Other Standards

### With Anu Standard

- EPR files complement DPR files
- Share series identity conventions (S###)
- Extend TRANSFORMATION_LOG.json format
- Reference same source catalogs

### With HDARP

- All quotes from HDARP extractions
- No direct PDF reading by agents
- Reference HDARP file paths in EPR
- Use HDARP table/equation extractions

### With Transition Analysis

- Use existing `transition_analysis.py`
- Apply splice validation metrics
- Generate transition visualizations
- Document in EPR file

---

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `EXT_NO_DPR` | No DPR exists for series | Create DPR first using anu-standard |
| `EXT_NO_HDARP` | HDARP extractions missing | Run HDARP on required documents |
| `EXT_METHODOLOGY_MISMATCH` | Cannot match methodology | Document difference, seek review |
| `EXT_TRANSITION_FAILED` | Transition analysis failed | Investigate data quality, methodology |
| `EXT_VALIDATION_FAILED` | Validation tests failed | Review extension, fix issues |
| `EXT_UNCERTAINTY` | Methodology unclear | Stop, do not guess, seek clarification |

---

## Templates

Available in `templates/`:

| Template | Purpose |
|----------|---------|
| `EPR_TEMPLATE.md` | Extension Provenance Record |
| `TRANSITION_ANALYSIS_TEMPLATE.md` | Transition analysis report |
| `METHODOLOGY_COMPARISON_TEMPLATE.md` | Old vs new methodology |
| `EXTENSION_CERTIFICATION_TEMPLATE.md` | Final certification |

---

## Reference Implementation

See CD2 project for reference:
- `Technical/ShinyApp/docs/series/` - EPR files
- `Technical/EXTENSION_LOG.json` - Extension log
- `Technical/scripts/transition_analysis.py` - Transition analysis

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-28 | Initial Anu Extension Standard |

---

*The Anu Extension Standard ensures that every data extension is maximally faithful to the original construction methodology, with complete documentation and validation.*
