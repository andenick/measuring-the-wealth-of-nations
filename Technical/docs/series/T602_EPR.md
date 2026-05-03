# T602: Social Insurance Tax (T_w_social) - Extension Provenance Record

## Quick Reference

| Property | Value |
|----------|-------|
| Series ID | T602 |
| Series Name | Social Insurance Tax (Employee Contributions) |
| Original Period | 1952-1989 |
| Extension Period | 1990-2025 |
| Original Source | NIPA Table 3.1 via book methodology |
| Extension Source | NIPA Table 3.1 via BEA API (identical table) |
| Transition Status | SEAMLESS |
| Faithfulness Score | 95% |
| Certification | CERTIFIED |
| Extension Date | 2026-02-25 |
| Certifying Agent | Claude Opus 4 (AS2 Chapter 6 EPR Session) |

---

## Agent Understanding Statement

### What is this data?

T602 measures **employee social insurance contributions** -- the payroll taxes paid directly by workers for Social Security (OASDI), Medicare (HI), and unemployment insurance. Unlike T601 (personal tax) which requires an allocation proxy, T602 is a direct extraction from NIPA Table 3.1 line 8 (employee contributions for government social insurance). These are taxes paid exclusively by workers and require no allocation between classes.

### What was the original data source?

The original T602 series (1952-1989) was constructed from:
- **NIPA Table 3.1**: Government Current Receipts and Expenditures -- line 8, employee contributions for government social insurance
- **Units**: Millions of current dollars, annual frequency

### What methodology was originally applied?

1. **Direct extraction**: Employee social insurance contributions are read directly from NIPA 3.1 line 8
2. **No allocation needed**: Unlike personal income taxes, social insurance contributions are explicitly classified as employee payments in the NIPA accounts
3. **Full attribution to workers**: 100% of employee SI contributions are attributed to workers (employer contributions are a separate category)

### What source was used for extension?

- **Source**: BEA NIPA API -- the exact same Table 3.1
- **Period**: 1929-2025 (continuous; 1990-2025 used for extension)
- **Key fact**: NIPA 3.1 is a continuous series from 1929 to 2025. There is NO source break at 1989.

### Have there been methodology updates?

**Answer**: NO (for the extraction methodology). Direct line item extraction is unchanged. However:
- **Social Security tax base changes**: The taxable wage base has been raised periodically (most recently to $168,600 in 2024), which affects the level of contributions but not the NIPA reporting methodology.
- **Medicare HI tax expansion** (1994): Medicare tax became uncapped, affecting revenue growth post-1993.
- **NIPA Comprehensive Revisions**: May slightly alter historical values.

---

## Book Context

### Chapter References

| Chapter | Page | Quote | Relevance |
|---------|------|-------|-----------|
| Ch 6 | p. 155 | "Social insurance contributions by employees represent a direct and unambiguous tax on workers -- no allocation is necessary." | Confirms T602 methodology |
| Ch 6 | p. 160 | "The tax rate on workers rose from 0.18 to 0.32, with social insurance taxes being the fastest-growing component." | T602 growth context |
| Ch 6 | p. 170-175 | "Social insurance taxes (OASDI, HI, UI) are regressive in structure, bearing most heavily on lower-wage workers." | Distributional context |

### Variable Definitions from Book

| Variable | Definition | Formula | Source |
|----------|------------|---------|--------|
| T_w_social | Employee social insurance contributions | Direct from NIPA 3.1 line 8 | BEA |
| OASDI | Old-Age, Survivors, and Disability Insurance | Component of T602 | SSA |
| HI | Hospital Insurance (Medicare Part A) | Component of T602 | CMS |

---

## Methodology Changes Assessment

| Aspect | Original (Vintage: 1994) | Current (Vintage: 2025) | Impact |
|--------|--------------------------|-------------------------|--------|
| Source table | NIPA 3.1 line 8 | NIPA 3.1 line 8 | NONE -- identical |
| Extraction method | Direct line item | Direct line item | NONE -- identical |
| Worker attribution | 100% employee SI | 100% employee SI | NONE -- identical |
| NIPA vintage | ~1992 vintage | 2025 vintage | LOW -- comprehensive revisions |
| Tax law changes | Pre-1990 rates | Post-1990 expansions (Medicare uncapping) | NONE for methodology; affects levels naturally |

**Overall Methodology Match**: YES -- Identical source table, identical extraction, identical attribution. The simplest series in the Chapter 6 framework.

---

## Transition Analysis

### Overlap Period

| Field | Value |
|-------|-------|
| Overlap Start | 1989 |
| Overlap End | 1989 |
| Duration | 1 year (splice point) |
| Original Value at 1989 | 385,231.0 |
| Extension Value at 1989 | 385,231.0 |

### Transition Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Connection Ratio | 1.000 | 0.95 - 1.05 | PASS |
| Growth Rate Continuity | 0.11% | < 5% | PASS |
| Level Difference | 0.000% | < 3% | PASS |

### Metric Calculations

**Connection Ratio**:
```
T602_EXT(1989) / T602_A(1989) = 385,231.0 / 385,231.0 = 1.000
```

**Growth Rate Continuity**:
```
Original growth (1988->1989): (385,231.0 - 361,482.0) / 361,482.0 = 6.571%
Extension growth (1989->1990): (410,108.0 - 385,231.0) / 385,231.0 = 6.457%
|Extension_Growth - Original_Growth| = |6.457% - 6.571%| = 0.114%
Growth rate continuity = 0.114% (excellent -- within 5% threshold)
```

**Level Difference**:
```
|T602_EXT(1989) - T602_A(1989)| / T602_A(1989) = 0 / 385,231.0 = 0.000%
```

### Splice Method Used

- [x] Direct Level Match -- Same continuous NIPA data source
- [ ] Growth Rate Splice
- [ ] Ratio Adjustment
- [ ] Other

### Transition Assessment

**Status**: SEAMLESS

T602 has the most seamless transition of any Chapter 6 series because it is a direct NIPA line item extraction with no allocation proxy. The growth rate continuity (0.11%) is nearly perfect, confirming no break in the underlying data. Social insurance contributions grew smoothly through the 1989-1990 transition.

---

## Faithfulness Score Calculation

### Score: 95%

| Component | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Methodology Match | 30% | 99% | 29.7% | Identical: direct NIPA line item extraction, no allocation needed |
| Source Match | 20% | 99% | 19.8% | Same BEA NIPA 3.1 line 8; only difference is API vs printed volume |
| Transformation Replication | 20% | 95% | 19.0% | Direct extraction -- minimal transformation, fully replicable |
| Transition Quality | 20% | 99% | 19.8% | Connection ratio 1.000, growth continuity 0.11%, same continuous source |
| Documentation Completeness | 10% | 85% | 8.5% | All sections complete; visualization pending |
| **Total** | **100%** | | **96.8% -> 95%** | Rounded conservatively |

---

## Extension Certification

### Certification Status

- [x] **CERTIFIED** -- Maximally faithful extension (Score >= 90%)
- [ ] **CERTIFIED WITH NOTES**
- [ ] **NOT CERTIFIED**

### Certification Notes

1. **Simplest extension**: T602 is a direct NIPA line item with no allocation. The extension is maximally faithful.
2. **Tax law evolution**: Post-1989 changes (Medicare uncapping 1994, rate increases) affect the level of contributions but are properly captured by the NIPA data -- these are real economic changes, not methodology breaks.
3. **Growth trajectory**: T602 grows from 385,231.0 (1989) to 2,015,518.0 (2025), a 5.2x increase reflecting expanding payroll tax base and rates.

### Certifying Agent

| Field | Value |
|-------|-------|
| Agent | Claude Opus 4 |
| Date | 2026-02-25 |
| Session | AS2 Chapter 6 EPR Session |
| Anu Extension Version | 1.0 |

---

## Related Documentation

### Associated Files

| File | Location | Purpose |
|------|----------|---------|
| DPR | `Technical/docs/series/T602_DPR.md` | Original series documentation |
| Extended Data | `ShinyApp/data/nsw_1952_2025.csv` | Full 1952-2025 series |
| Book Period Data | `ShinyApp/data/nsw_1952_1989.csv` | Original 1952-1989 series |
| NIPA Source | `Inputs/API_Data/BEA/nipa_3_1_govt_receipts_expenditures.csv` | Government receipts |

### EXTENSION_LOG Entry

```json
{
  "extension_id": "EXT-011",
  "series_id": "T602",
  "timestamp": "2026-02-25T00:00:00Z",
  "faithfulness_score": 95,
  "certification": "CERTIFIED"
}
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-25 | Claude Opus 4 (Ch6 EPR Session) | Initial EPR creation |

---

*Generated following Anu Extension Standard v1.0*
*Extension Provenance Record -- T602: Social Insurance Tax (Employee Contributions)*
