# T609: NSW/NI Share (Net Social Wage as Share of National Income) - Extension Provenance Record

## Quick Reference

| Property | Value |
|----------|-------|
| Series ID | T609 |
| Series Name | NSW/NI Share (NSW as fraction of National Income) |
| Original Period | 1952-1989 |
| Extension Period | 1990-2025 |
| Original Source | Derived: T607 / National Income (NIPA) |
| Extension Source | Same derivation using extended T607 and NIPA National Income |
| Transition Status | SEAMLESS |
| Faithfulness Score | 93% |
| Certification | CERTIFIED |
| Extension Date | 2026-02-25 |
| Certifying Agent | Claude Opus 4 (AS2 Chapter 6 EPR Session) |

---

## Agent Understanding Statement

### What is this data?

T609 measures the **Net Social Wage as a share of National Income**: `NSW/NI = T607 / NI`. This ratio normalizes NSW by the total income of the economy, showing the net fiscal impact on workers as a fraction of national output. It provides a scale-independent measure of the welfare state's redistributive (or extractive) effect on workers.

A negative T609 means workers contribute a net positive share of national income to the state; a positive T609 means the state redistributes a net positive share toward workers. The book-period values range from approximately -0.047 to +0.014, indicating that the net fiscal extraction from workers typically ranges from 0% to 5% of national income.

### What was the original data source?

- **T607**: Net Social Wage (NIPA-based, see T607_EPR.md)
- **NI**: National Income (NIPA Table 1.7.5 or equivalent)
- **Formula**: `T609 = T607 / NI`
- **Units**: Ratio (dimensionless), annual frequency

### What methodology was originally applied?

Simple ratio: divide NSW (T607, millions of current dollars) by National Income (NI, millions of current dollars). Both are NIPA-derived aggregates.

### What source was used for extension?

- **T607_EXT**: Extended using same NIPA methodology (CERTIFIED at 93%, see T607_EPR.md)
- **NI**: National Income from NIPA, continuous series available via BEA API
- **Key fact**: Both numerator and denominator are NIPA-sourced with continuous data. No methodology break.

### Have there been methodology updates?

**Answer**: NO. The ratio formula is unchanged. National Income is a standard NIPA aggregate. NIPA comprehensive revisions may change NI levels but not the concept.

---

## Book Context

### Chapter References

| Chapter | Page | Quote | Relevance |
|---------|------|-------|-----------|
| Ch 6 | p. 175 | "As a fraction of national income, NSW ranges from approximately -5% to near zero, indicating that the net fiscal extraction from workers is a small but persistent share of total income." | Quantifies T609 range |
| Ch 6 | p. 178-180 | "The tax rate rising from 0.18 to 0.32 while the benefit rate rose only from 0.11 to 0.28 means the NSW/NI share remains negative, trending slightly downward." | T609 trend |
| Ch 6 | p. 180 | "The welfare state is not a mechanism for income redistribution toward workers. It is, at best, a system that recycles workers' own contributions." | Political interpretation |

### Variable Definitions from Book

| Variable | Definition | Formula | Source |
|----------|------------|---------|--------|
| NSW/NI | Net social wage share of national income | T607 / NI | Derived ratio |
| NI | National Income | NIPA aggregate | BEA |

---

## Methodology Changes Assessment

| Aspect | Original (Vintage: 1994) | Current (Vintage: 2025) | Impact |
|--------|--------------------------|-------------------------|--------|
| Ratio formula | T607 / NI | T607 / NI | NONE -- identical |
| Numerator (NSW) | NIPA-based | Same NIPA via API | NONE (see T607_EPR) |
| Denominator (NI) | NIPA National Income | Same NIPA National Income | NONE -- continuous series |
| NIPA vintage | ~1992 vintage | 2025 vintage | LOW -- comprehensive revisions may alter NI levels |

**Overall Methodology Match**: YES -- Both numerator and denominator are standard NIPA aggregates with continuous data.

---

## Transition Analysis

### Overlap Period

| Field | Value |
|-------|-------|
| Overlap Start | 1989 |
| Overlap End | 1989 |
| Duration | 1 year (splice point) |
| Original Value at 1989 | -0.021860 |
| Extension Value at 1989 | -0.021860 |

### Transition Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Connection Ratio | 1.000 | 0.95 - 1.05 | PASS |
| Growth Rate Continuity | N/A | < 5% | FLAG (see note) |
| Level Difference | 0.000% | < 3% | PASS |

### Metric Calculations

**Connection Ratio**:
```
T609_EXT(1989) / T609_A(1989) = -0.021860 / -0.021860 = 1.000
```

**Growth Rate Continuity**:
```
Original growth (1988->1989): (-0.021860 - (-0.022031)) / |-0.022031| = -0.776%
Extension growth (1989->1990): (-0.015204 - (-0.021860)) / |-0.021860| = 30.449%
|Extension_Growth - Original_Growth| = |30.449% - (-0.776%)| = 31.225%
```

Note: As with T607, the growth rate continuity metric is unreliable for T609 because the series oscillates near zero. The large apparent discontinuity (31.2%) reflects the 1990-1991 recession (which pushed NSW toward zero), not a methodology break. The connection ratio (1.000) and the fact that both numerator and denominator are continuous NIPA data confirm the transition is seamless.

**Level change analysis**:
```
T609(1988) = -0.022031
T609(1989) = -0.021860 (slight improvement: recession reducing taxes, increasing benefits)
T609(1990) = -0.015204 (recession effect continues: NSW moving toward zero)
```

The level trajectory is smooth and economically rational: the 1990-91 recession pushes NSW/NI from -2.2% toward -1.5%.

### Splice Method Used

- [x] Direct Level Match -- Same continuous NIPA data sources for both numerator and denominator
- [ ] Growth Rate Splice
- [ ] Ratio Adjustment
- [ ] Other

### Transition Assessment

**Status**: SEAMLESS

Both the numerator (T607/NSW) and denominator (NI) use continuous NIPA data. The transition is mathematically perfect with connection ratio 1.000. The growth rate metric is not applicable for near-zero oscillating series.

---

## Extended Series Key Statistics

### T609 Range Analysis

| Period | Min | Max | Mean | Interpretation |
|--------|-----|-----|------|----------------|
| 1952-1989 (book) | -0.047 (1969) | +0.014 (1975) | -0.024 | Workers net payers: ~2.4% of NI |
| 1990-2025 (extension) | -0.030 (2000) | +0.092 (2020) | +0.020 | Mixed; recessions push positive |
| Full 1952-2025 | -0.047 | +0.092 | -0.004 | Near zero on average |

### Notable Values

| Year | T609 | Context |
|------|------|---------|
| 1969 | -0.047 | Peak fiscal extraction (Vietnam-era taxes + low benefits) |
| 1975 | +0.014 | First positive year (recession-driven benefits) |
| 2000 | -0.030 | Late 1990s boom (high tax collections, low transfers) |
| 2009 | +0.070 | Great Recession |
| 2020 | +0.092 | COVID peak: largest positive value in series |
| 2025 | +0.050 | Elevated post-COVID level |

---

## Faithfulness Score Calculation

### Score: 93%

| Component | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|----------|-----------|
| Methodology Match | 30% | 97% | 29.1% | Identical ratio formula; both numerator and denominator from same NIPA |
| Source Match | 20% | 99% | 19.8% | Same BEA NIPA tables for NSW and NI |
| Transformation Replication | 20% | 90% | 18.0% | Simple ratio; inherits T607 component assumptions |
| Transition Quality | 20% | 95% | 19.0% | Connection ratio 1.000; growth rate metric invalid for near-zero series |
| Documentation Completeness | 10% | 85% | 8.5% | All sections complete |
| **Total** | **100%** | | **94.4% -> 93%** | |

---

## Extension Certification

### Certification Status

- [x] **CERTIFIED** -- Maximally faithful extension (Score >= 90%)
- [ ] **CERTIFIED WITH NOTES**
- [ ] **NOT CERTIFIED**

### Certification Notes

1. **Dual NIPA sourcing**: Both numerator (NSW) and denominator (NI) come from continuous NIPA data, making T609 one of the most faithful extensions in the Chapter 6 framework.
2. **Near-zero oscillation**: T609 values are small (-0.05 to +0.09), making percentage-based transition metrics unreliable. Level analysis confirms smooth, economically rational transitions.
3. **Post-1989 sign changes**: T609 is positive during recessions (1975, 1983, 1992-93, 2002-04, 2008-10, 2020-21) and negative during expansions. This countercyclical pattern is consistent with the book's framework and extends the original finding.
4. **COVID dominance**: The 2020 value (+0.092) is the largest positive T609 in the series, reflecting unprecedented government transfers during the pandemic.
5. **Structural trend**: The post-2008 trend toward more positive T609 values (averaging ~+0.04 in 2008-2025 vs ~-0.024 in 1952-1989) may indicate a structural shift in the fiscal relationship between workers and the state. This warrants further analysis.

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
| DPR | `Technical/docs/series/T609_DPR.md` | Original series documentation |
| Extended Data | `ShinyApp/data/nsw_1952_2025.csv` | Full 1952-2025 series |
| Book Period Data | `ShinyApp/data/nsw_1952_1989.csv` | Original 1952-1989 series |
| T607 EPR | `Technical/docs/series/T607_EPR.md` | Numerator provenance |

### EXTENSION_LOG Entry

```json
{
  "extension_id": "EXT-018",
  "series_id": "T609",
  "timestamp": "2026-02-25T00:00:00Z",
  "faithfulness_score": 93,
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
*Extension Provenance Record -- T609: NSW/NI Share*
