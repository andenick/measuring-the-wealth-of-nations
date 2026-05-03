# T609: NSW as Share of National Income - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T609 |
| Type | derived |
| Time Period | 1952-1989 |
| Frequency | annual |
| Source Count | 3 |
| Base Year | N/A |
| Units | ratio (dimensionless) |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-25 |

---

## Context

> "NSW as a share of national income provides a scale-normalized measure of the net fiscal transfer, allowing comparison across time periods with different price levels and across countries with different output scales."
> -- Derived from Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

The NSW/NI ratio expresses the net social wage as a fraction of national income. While T608 (NSW/V*) measures the fiscal burden relative to worker compensation, T609 measures it relative to the total economy. A negative NSW/NI ratio of -0.05 means that the net fiscal extraction from workers equals 5% of national income. This ratio provides a macroeconomic perspective on the fiscal transfer and is more readily comparable across countries and time periods than the absolute NSW level. It complements the NSW/V* ratio by using a denominator (national income) that is independent of the productive/unproductive labor classification.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T609A | Book Table 6.4 | 1952-1989 | N/A (book) | academic_research | NSW/NI ratio time series |
| T609B | T607 (Net Social Wage) | 1952-1989 | Calculated | derived | NSW numerator |
| T609C | NIPA Table 1.7.5 (National Income) | 1952-2025 | BEA NIPA API | official_statistics | National income denominator |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Retrieve NSW series | T607 | NSW annual values | calculate_ch06.py | XFORM-066 |
| 2 | Pull national income | BEA API (NIPA 1.7.5) | nipa_1_7_5_national_income.csv | pull_bea_nipa_ch06.py | XFORM-068 |
| 3 | Align time periods | NSW (1952-1989), NI (1929-2025) | Intersection: 1952-1989 | calculate_ch06.py | XFORM-068 |
| 4 | Compute ratio | NSW, NI | T609 = NSW / NI | calculate_ch06.py | XFORM-068 |

### Transformation Details

#### XFORM-068: NSW/NI Ratio

**Formula**:
```
NSW_NI_ratio = NSW / NI
             = T607 / National_Income

where:
  T607 = Net Social Wage = B_w + G_w - T_w (from Chapter 6)
  NI   = National Income (NIPA 1.7.5)

Expected sign: Negative (NSW < 0 for all years 1952-1989)
Expected magnitude: Smaller absolute value than NSW/V* because NI > V*
```

**Notes**: National income from NIPA 1.7.5 is the conventional (orthodox) measure of aggregate income. Using NI as the denominator rather than the Marxian value added (VA* = T503) makes this ratio comparable to standard macroeconomic measures. The choice of denominator reflects the dual-accounting approach: Marxian categories for the numerator (NSW), orthodox categories for the denominator (NI).

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Ratio sign | Negative throughout 1952-1989 | Validated 2026-03-22 | PASS |
| Magnitude | Smaller absolute value than T608 (NSW/V*) | Validated 2026-03-22 | PASS |
| NI > 0 | National income positive for all years | Validated 2026-03-22 | PASS |
| Consistency | NSW/NI < NSW/V* in absolute value (since NI > V*) | Validated 2026-03-22 | PASS |
| Year coverage | 1952-1989 | 1952-1989 | PASS |

---

## Known Issues

- [ ] **National income definition**: NIPA 1.7.5 has undergone revisions; need to confirm which NI definition (with or without statistical discrepancy) matches the book
- [ ] **NIPA 1.7.5 availability**: Gross output by industry table (1.7.5) may not directly report national income; may need NIPA 1.12 or 1.7.5 line-specific extraction
- [ ] **Comparison with NSW/V***: Both ratios should tell a consistent story; divergence would indicate inconsistency in V* or NI definitions
- [ ] **Extension feasibility**: NI is available through 2025 via NIPA; extension depends only on NSW extension (T607)

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.1-F.4 | Underlying NSW calculation detail |

---

## Related Content

- **Figures**: 6.2 (NSW ratio comparison)
- **Derived Series**: T901 (Summary Table of Key Indicators)
- **Upstream Dependencies**: T607 (Net Social Wage)
- **Module**: Chapter 6 -- Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
