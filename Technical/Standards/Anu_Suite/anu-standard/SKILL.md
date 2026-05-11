---
name: anu-standard
description: Apply rigorous data provenance and quality standards to data projects. Use when creating data pipelines, documenting datasets, reviewing data quality, setting up replication projects, or auditing data transformations.
argument-hint: [action] [target]
allowed-tools: Read, Write, Grep, Glob, LS
---

# The Anu Standard: Data Provenance and Quality Framework

A rigorous framework for ensuring complete provenance tracking, quality assurance, and reproducibility for ALL data research projects.

---

## Quick Reference

### Five Core Principles

1. **EXPLICIT PARSING** - Never rely on implicit defaults when loading data
2. **VALIDATE ON LOAD** - Every data structure must be validated immediately after loading
3. **FAIL LOUDLY** - Never fall through to silent defaults; throw diagnostic errors
4. **DOCUMENT EVERYTHING** - Every series, figure, and transformation must have provenance
5. **TEST DATA PATHS** - Every data-to-output mapping must have automated tests

### When to Use This Skill

Apply the Anu Standard when:
- Setting up a new data research project
- Documenting existing datasets for reproducibility
- Creating data pipelines with multiple sources
- Reviewing data quality and provenance
- Preparing replication packages
- Auditing transformation chains

---

## Content Type Classification

All data content falls into one of five types:

| Type | Description | Documentation Required |
|------|-------------|------------------------|
| `time_series` | Historical data with time dimension | DPR (Data Provenance Record) |
| `theoretical` | Conceptual diagrams, no underlying data | FPR (Figure Provenance Record) |
| `cross_sectional` | Point-in-time empirical studies | FPR + Source Documentation |
| `simulation` | Computational model outputs | FPR + Methodology Documentation |
| `derived` | Calculated/transformed from other series | DPR with transformation chain |

### Decision Tree

```
Does the content have underlying data?
├── YES: Is it time-indexed?
│   ├── YES → time_series → Create DPR
│   └── NO → cross_sectional → Create FPR + Source Doc
└── NO: What type of content?
    ├── Conceptual/theoretical diagram → theoretical → Create FPR
    ├── Computational model output → simulation → Create FPR + Methodology
    └── Calculated from other data → derived → Create DPR with chain
```

---

## Identity Systems

### Series/Dataset Identifiers

```
IDENTIFIER FORMAT (customize prefix per project):
  - Series:     [PREFIX]_S###       (e.g., PROJ_S001, ECON_S042)
  - Subseries:  [PREFIX]_S###X      (e.g., PROJ_S001A, PROJ_S001B)
  - Reindexed:  [PREFIX]_S###X-R### (e.g., PROJ_S001B-R2010)
  - Derived:    [PREFIX]_S###_CALC  (e.g., PROJ_S026_CALC)
```

### Figure/Output Identifiers

```
FIGURE FORMAT:
  - Figure:     [PREFIX]_FIG_###    (e.g., PROJ_FIG_001)
  - Panel:      [PREFIX]_FIG_###X   (e.g., PROJ_FIG_001A)
```

### File Naming Conventions

| Content | File Name Format | Example |
|---------|------------------|---------|
| Data Provenance Record | `[ID]_DPR.md` | `PROJ_S001_DPR.md` |
| Figure Provenance Record | `[ID]_FPR.md` | `PROJ_FIG_001_FPR.md` |
| Module Investigation | `[MODULE]_INVESTIGATION.md` | `CHAPTER_2_INVESTIGATION.md` |
| Validation Report | `[MODULE]_VALIDATION.md` | `CHAPTER_2_VALIDATION.md` |
| Transformation Log | `TRANSFORMATION_LOG.json` | N/A |

---

## Documentation Requirements

### Data Provenance Record (DPR)

Required for all `time_series` and `derived` content:

```markdown
# [ID]: [Dataset Name] - Data Provenance Record

## Quick Reference
| Property | Value |
|----------|-------|
| Dataset ID | [ID] |
| Type | time_series / derived |
| Time Period | YYYY-YYYY |
| Source Count | # |
| Validation Status | VALIDATED / PENDING |
| Last Updated | YYYY-MM-DD |

## Source Documentation
[For each source: name, URL, download date, quality assessment]

## Transformation Chain
[Step-by-step operations with formulas, scripts, input/output files]

## Validation Record
[Value range checks, coverage checks, cross-references]

## Known Issues
[Any data quality issues or limitations]
```

### Figure Provenance Record (FPR)

Required for all `theoretical`, `cross_sectional`, and `simulation` content:

```markdown
# [ID]: [Figure Title] - Figure Provenance Record

## Quick Reference
| Property | Value |
|----------|-------|
| Figure ID | [ID] |
| Type | theoretical / cross_sectional / simulation |
| Page/Location | [reference] |
| Linked Dataset | [ID or None] |
| Last Updated | YYYY-MM-DD |

## Content Description
[What the figure shows, key variables, interpretation]

## Source Information
[For theoretical: "Author construction"
 For cross_sectional: Original source citation
 For simulation: Model details and parameters]

## Key Observations
[Author's insights about this figure]
```

---

## Transformation Audit Trail

All transformations must be logged in `TRANSFORMATION_LOG.json`:

```json
{
  "project": "[PROJECT_NAME]",
  "version": "1.0",
  "transformations": [
    {
      "transform_id": "T001",
      "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
      "datasets_affected": ["[ID1]", "[ID2]"],
      "operation": "[operation_type]",
      "description": "[What was done]",
      "formula": "[Mathematical formula if applicable]",
      "parameters": {},
      "script": "[script_path]",
      "input_files": ["[file1]", "[file2]"],
      "output_files": ["[output_file]"],
      "validation_result": "PASS / FAIL / WARN",
      "notes": "[Any additional notes]"
    }
  ]
}
```

### Standard Operation Types

- `direct_import` - Raw data imported without modification
- `splice` - Combining series with growth rate preservation
- `reindex` - Changing base year for index series
- `calculate` - Derived from formula
- `interpolate` - Gap filling
- `aggregate` - Combining multiple series
- `filter` - Subsetting data
- `transform` - Mathematical transformation

---

## Testing and Validation

### Required Tests

For each dataset/figure:

1. **Existence Test** - Required files exist
2. **Structure Test** - Expected fields/columns present
3. **Value Range Test** - Values within expected bounds
4. **Coverage Test** - Time/space coverage as expected
5. **Linkage Test** - References resolve correctly

### Validation Report Format

```markdown
# [Module] Validation Report

## Summary
| Metric | Value |
|--------|-------|
| Datasets Validated | # |
| Tests Passed | # |
| Tests Failed | # |
| Overall Status | PASS / FAIL |

## Individual Dataset Results
[For each dataset: tests run, results, issues]

## Recommendations
[Actions needed to resolve any failures]
```

---

## Compliance Checklist

### For Time Series Data

- [ ] Dataset ID assigned following naming convention
- [ ] DPR file created with all required sections
- [ ] All sources documented with download dates
- [ ] Transformations logged in TRANSFORMATION_LOG.json
- [ ] Validation tests written and passing
- [ ] Value ranges verified against expectations
- [ ] Time coverage documented

### For Theoretical/Conceptual Content

- [ ] Figure ID assigned following naming convention
- [ ] FPR file created with all required sections
- [ ] Content description complete
- [ ] Source observations documented
- [ ] Theoretical significance explained

### For Module/Component Investigation

- [ ] Investigation document exists
- [ ] All content classified by type
- [ ] All datasets have DPR files
- [ ] All figures have FPR files
- [ ] Compliance checklist completed
- [ ] Status shows "ANU STANDARD COMPLIANT"

---

## Quality Assessment Categories

| Category | Description | Reliability |
|----------|-------------|-------------|
| `official_statistics` | Government agencies, central banks | HIGH |
| `academic_research` | Peer-reviewed sources | HIGH |
| `institutional` | International organizations (IMF, WB) | HIGH |
| `historical_reconstruction` | Reconstructed from archives | MEDIUM |
| `calculated` | Derived from other series | VARIES |
| `interpolated` | Gap-filled data | LOW |
| `estimated` | Third-party estimates | MEDIUM |
| `simulation` | Model-generated | N/A |

---

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `ANU_FILE_NOT_FOUND` | Required file missing | Create the file |
| `ANU_VALIDATION_FAILED` | Structure validation failed | Check field names/types |
| `ANU_DPR_MISSING` | No DPR for time series | Create DPR file |
| `ANU_FPR_MISSING` | No FPR for figure | Create FPR file |
| `ANU_TRANSFORM_UNDOCUMENTED` | Transformation not logged | Add to TRANSFORMATION_LOG |
| `ANU_RANGE_VIOLATION` | Value outside expected range | Investigate data quality |
| `ANU_COVERAGE_GAP` | Unexpected gap in time series | Document or fill gap |
| `ANU_LINKAGE_BROKEN` | Reference doesn't resolve | Fix reference path |

---

## Project Setup

To apply the Anu Standard to a new project:

1. **Create directory structure**:
   ```
   [Project]/
   ├── Inputs/           # Raw data (read-only)
   ├── Technical/        # Processing, documentation
   │   ├── docs/
   │   │   ├── series/   # DPR files
   │   │   └── figures/  # FPR files
   │   └── TRANSFORMATION_LOG.json
   ├── Outputs/          # Final outputs
   └── tests/            # Validation tests
   ```

2. **Initialize transformation log**:
   ```json
   {
     "project": "[PROJECT_NAME]",
     "version": "1.0",
     "created": "YYYY-MM-DD",
     "transformations": []
   }
   ```

3. **Classify all content** by type using the decision tree

4. **Create documentation** (DPR/FPR) for each item

5. **Write validation tests** for all time series data

6. **Run compliance check** using `/anu-standard validate`

---

## Commands

Use this skill with arguments:

- `/anu-standard init [project]` - Initialize Anu Standard structure
- `/anu-standard classify [file]` - Classify content type
- `/anu-standard create-dpr [id]` - Create DPR for dataset
- `/anu-standard create-fpr [id]` - Create FPR for figure
- `/anu-standard validate [path]` - Check compliance
- `/anu-standard audit [path]` - Full audit report

---

## Supporting Files

Templates and scripts are available in the skill directory:

- `templates/DPR_TEMPLATE.md` - Data Provenance Record template
- `templates/FPR_TEMPLATE.md` - Figure Provenance Record template
- `templates/INVESTIGATION_TEMPLATE.md` - Module investigation template
- `scripts/validate_compliance.py` - Automated compliance checker

---

## Reference Implementation

See the CD2 project for a complete reference implementation:
`Technical/Standards/Anu_Suite/ANU_STANDARD_UNIFIED.md`

---

## Anu Standard v2.1 Enhancements

### Appendix Integration Requirements

For chapters/modules with source appendices (e.g., Shaikh appendices for Ch 2, 4, 5, 6, 9, 10, 11, 14):

1. **Reference all relevant appendices** in DATA_UPDATES review documents
2. **Link to appendix data tables** in DPR files (e.g., "See Appendix 6.7 Table references")
3. **Document appendix methodology** in investigation documents
4. **Map appendix variables to series** in provenance records

**Appendix Documentation Checklist:**
- [ ] Appendix ID and title referenced
- [ ] Related BEA/source tables documented
- [ ] Key variables and formulas extracted
- [ ] Methodology notes incorporated
- [ ] Extension implications assessed

### Data Revision Tracking Requirements

For all empirical series:

1. **Document original data vintage** (e.g., "Shaikh 2011 vintage")
2. **Track major methodology revisions** from primary sources:
   - BEA: Comprehensive revisions (2013, 2018, 2023)
   - BLS: Methodology updates (classification, sampling)
   - Federal Reserve: Series redefinitions
   - Census: Benchmark revisions
3. **Include revision dates and impact assessment**
4. **Provide URLs to current official methodology**

**Revision Documentation Format:**
```markdown
## Data Source Revisions

### [Source Name] Revisions
| Revision | Year | Series Affected | Impact |
|----------|------|-----------------|--------|
| [Name] | [Year] | [Series IDs] | [HIGH/MEDIUM/LOW] |

### Extension Implications
[Document how revisions affect data extensions and methodology updates]
```

### New v2.1 Documentation Assets

| Document | Purpose | Location |
|----------|---------|----------|
| `APPENDIX_REFERENCE_MATRIX.md` | Maps source appendices to series | DOCUMENTATION/ |
| `DATA_REVISION_LOG.md` | Tracks data source revisions | DOCUMENTATION/ |
| `METHODOLOGY_URL_INDEX.md` | Official methodology URLs | DOCUMENTATION/ |
| `DATA_UPDATES_TEMPLATE.md` | Standard format for reviews | templates/ |

---

## Integration with Anu Extension Standard

For **extending** data series from historical to current periods, use the **Anu Extension Standard** skill:

**Skill**: `/anu-extension`
**Location**: `Council/Druck/.claude/skills/anu-extension/SKILL.md`

### When to Use Anu Extension

Use the Anu Extension Standard when:
- Extending time series beyond original period
- Splicing old and new data sources
- Replicating historical constructions with current data
- Validating data transitions at splice points

### Extension Documentation

| Document | Purpose |
|----------|---------|
| EPR (Extension Provenance Record) | Documents extension methodology and certification |
| EXTENSION_LOG.json | Registry of all extensions |
| Transition Analysis | Statistical validation of splice points |

### Relationship to Anu Standard

- EPR files **complement** DPR files (do not replace them)
- Extensions use same series IDs (S###)
- Extensions add entries to TRANSFORMATION_LOG.json
- All source quotes must come from HDARP extractions

See: `Council/Druck/docs/ANU_EXTENSION_STANDARD.md` for full documentation.

---

*The Anu Standard ensures that every piece of data in a research project can be fully traced, documented, and reproduced.*
