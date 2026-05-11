# [DATASET_ID]: [Dataset Name] - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | [DATASET_ID] |
| Type | time_series / derived |
| Time Period | [START_YEAR]-[END_YEAR] |
| Frequency | annual / quarterly / monthly / daily |
| Source Count | [#] |
| Base Year | [YEAR or N/A] |
| Units | [units] |
| Validation Status | PENDING |
| Last Updated | [YYYY-MM-DD] |

---

## Context

> "[Optional: Quote from source author about this data or its significance]"
> — [Author], [Source], p. [page]

[Brief description of what this dataset represents and why it matters for the project.]

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| [ID]A | [Source Name] | [YYYY-YYYY] | [URL or API] | [quality_category] | [notes] |
| [ID]B | [Source Name] | [YYYY-YYYY] | [URL or API] | [quality_category] | [notes] |

### Quality Categories
- `official_statistics` - Government/central bank data (HIGH reliability)
- `academic_research` - Peer-reviewed sources (HIGH reliability)
- `institutional` - IMF, World Bank, etc. (HIGH reliability)
- `historical_reconstruction` - Reconstructed from archives (MEDIUM reliability)
- `calculated` - Derived from formulas (VARIES)
- `estimated` - Third-party estimates (MEDIUM reliability)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | [operation] | [input] | [output] | [script.py] | T### |
| 2 | [operation] | [input] | [output] | [script.py] | T### |

### Transformation Details

#### T###: [Operation Name]

**Formula**: 
```
[Mathematical formula or pseudocode]
```

**Parameters**:
- [param1]: [value]
- [param2]: [value]

**Notes**: [Any important notes about this transformation]

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Value Range | [min-max] | [actual range] | PASS/FAIL |
| Year Coverage | [start-end] | [actual coverage] | PASS/FAIL |
| Missing Values | [expected %] | [actual %] | PASS/FAIL |
| Cross-reference | [reference] | [matches?] | PASS/FAIL |

### Validation Notes

[Any notes about validation results, edge cases, or known discrepancies]

---

## Known Issues

- [ ] **[Issue 1]**: [Description and impact]
- [ ] **[Issue 2]**: [Description and impact]

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App X.Y | [Title from source book] | [Table IDs] | [How this appendix informs series construction] |

### Key Appendix Variables
- **[Variable Name]**: [Formula/definition from appendix]
- **[Variable Name]**: [Formula/definition from appendix]

### Appendix Methodology Notes
[Key methodology points from appendix that inform series construction]

---

## Data Revision History

| Source | Revision | Date | Impact | Series Affected |
|--------|----------|------|--------|-----------------|
| BEA | [Comprehensive/Annual] | [YYYY] | [HIGH/MEDIUM/LOW] | [Series IDs] |
| BLS | [Methodology Update] | [YYYY] | [HIGH/MEDIUM/LOW] | [Series IDs] |

### Original Data Vintage
- **Shaikh Data Vintage**: [YYYY]
- **Current Data Vintage**: [YYYY]

### Extension Implications
[Document how revisions affect data extensions and methodology updates]

### Methodology URLs
- [Source 1]: [URL to methodology documentation]
- [Source 2]: [URL to methodology documentation]

---

## Related Content

- **Figures**: [List of figures using this dataset]
- **Derived Series**: [List of series derived from this one]
- **Module**: [Module/chapter this belongs to]
- **Appendices**: [List of appendices informing this series]

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| [YYYY-MM-DD] | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
