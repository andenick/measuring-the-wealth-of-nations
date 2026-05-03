# T507: Surplus Ratio (S*/Y) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T507 |
| Type | derived |
| Time Period | 1948-1989 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | ratio (dimensionless) |
| Validation Status | VALIDATED (book period) |
| Last Updated | 2026-02-24 |

---

## Context

> "The surplus ratio captures the share of total product accruing as surplus value, distinct from the conventional profit share. Where the conventional profit share (P/NI) averages roughly 25-30%, the Marxian surplus ratio S*/(S*+V*) ranges from 63% to 71% over 1948-1989, reflecting the much broader definition of surplus that includes unproductive worker compensation."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 5, Table 5.7, p. 115

The surplus ratio S*/(S*+V*) = S*/Y measures the share of gross final product (Y = S* + V*) that takes the form of surplus value. Unlike the conventional profit share, the surplus ratio is derived from the Marxian decomposition of output into its value components. The surplus ratio rises over time because the exploitation rate e = S*/V* rises, and S*/(S*+V*) = e/(1+e). This monotonic relationship with the exploitation rate makes the surplus ratio a useful alternative representation of the same underlying dynamics.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T507A | Derived from T504 (V*) and T505 (S*) | 1948-1989 | N/A (derived) | calculated | S*/(S*+V*) computed from T504, T505 |
| T507B | ExploitationComposition_1948_1989.csv | 1948-1989 | ST_Chopped/ch05/ExploitationComposition_1948_1989.csv | academic_research | Book data extracted from Table 5.7 |

### Quality Categories
- `academic_research` - Peer-reviewed source (HIGH reliability)
- `calculated` - Derived from formulas (VARIES -- depends on inputs)

### Chopped File Reference
- **File**: ST_Chopped/ch05/ExploitationComposition_1948_1989.csv
- **Content**: Contains surplus ratio alongside exploitation rate and composition of capital for benchmark and interpolated years
- **Columns**: Year, e (S*/V*), S*/(S*+V*), C*/V*, Lp/L, V*/W

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Load S* series | T505 | S* values 1948-1989 | calculate_ch05.py | XFORM-051 |
| 2 | Load V* series | T504 | V* values 1948-1989 | calculate_ch05.py | XFORM-041 |
| 3 | Compute Y = S* + V* | T504, T505 | Gross final product Y | calculate_ch05.py | XFORM-071 |
| 4 | Compute surplus ratio | S*, Y | T507 = S*/Y | calculate_ch05.py | XFORM-072 |
| 5 | Validate against Table 5.7 | T507, book values | pass/fail | validate_ch05.py | XFORM-073 |

### Transformation Details

#### XFORM-072: Surplus Ratio Calculation

**Formula**:
```
Surplus Ratio = S* / (S* + V*)
              = S* / Y
              = T505 / (T505 + T504)

Equivalently, in terms of exploitation rate:
  S*/(S*+V*) = e / (1 + e)
  where e = S*/V* = T506

Numerical range (book period):
  1948: e = 1.70 => surplus ratio = 1.70/2.70 = 0.630
  1989: e = 2.44 => surplus ratio = 2.44/3.44 = 0.709

The surplus ratio is bounded: 0 < S*/(S*+V*) < 1
  and is monotonically increasing in e.
```

**Parameters**:
- S* (T505): Surplus value (billions current dollars)
- V* (T504): Variable capital (billions current dollars)
- e (T506): Rate of exploitation (dimensionless)

**Notes**: The surplus ratio provides a complementary view to the exploitation rate. While e can exceed 1 (and does, rising from 1.70 to 2.44), the surplus ratio is bounded between 0 and 1, making it more intuitive as a "share" measure.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| SR(1948) | 0.630 (= 1.70/2.70) | 0.630 | PASS |
| SR(1958) | 0.647 (= 1.83/2.83) | 0.647 | PASS |
| SR(1967) | 0.677 (= 2.10/3.10) | 0.677 | PASS |
| SR(1977) | 0.677 (= 2.10/3.10) | 0.677 | PASS |
| SR(1989) | 0.709 (= 2.44/3.44) | 0.709 | PASS |
| Monotonic in e | Rising with e | Confirmed (plateau 1967-1977) | PASS |
| Value Range | 0.5-0.8 | 0.630-0.709 | PASS |
| Identity check | SR = e/(1+e) | Exact match for all years | PASS |

### Validation Notes

The surplus ratio mirrors the exploitation rate dynamics exactly, with the 1967-1977 plateau visible in both series. Because SR = e/(1+e) is a strictly monotonic transformation of e, any validation of T506 automatically validates T507. The surplus ratio values can also be cross-checked directly from Table 5.7 in the chopped file ExploitationComposition_1948_1989.csv.

---

## Known Issues

- [ ] **Dependent on T503/T504 accuracy**: The surplus ratio inherits all limitations from the VA* and V* series; any misclassification in productive/unproductive labor propagates directly
- [ ] **No extension computed**: T507 has not been extended beyond 1989; extension requires both T504 and T505 extended series to be finalized
- [ ] **Conventional comparison**: The ratio of S*/(S*+V*) to conventional profit share P/NI has not been systematically tabulated for all years

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App D | National Accounts Detail | D.2 | Source components for VA* entering S* |
| App E | Revenue Accounts | E.2 | Decomposition of value added into V* and S* |

### Key Appendix Variables
- **Y**: Gross final product = S* + V* (the denominator of the surplus ratio)
- **S***: Surplus value (Table E.2 residual)
- **V***: Variable capital (Table E.2, NIPA 6.2D adjusted)

---

## Related Content

- **Book Table**: 5.7 (Exploitation and Composition, five benchmark years)
- **Figures**: 5.3 (Surplus Ratio), 5.1 (Exploitation Rate -- same dynamics)
- **Derived Series**: T506 (e = S*/V*, equivalent representation), T513 (profit rate)
- **Dependencies**: T504 (V*), T505 (S*)
- **Module**: Chapter 5 -- Accounting Framework

## Extension Status

| Property | Value |
|----------|-------|
| Current Period | 1948-1989 (book only) |
| Extension Feasibility | BLOCKED — requires IO benchmark tables (Chapter 4) |
| Wave Assignment | Wave 2 |
| Dependency | Chapter 4 IO classification → sector-level decomposition |
| Estimated Extension Date | After Wave 2 IO chapter completion |
| Notes | Derived S*/(S*+V*); requires T504 and T505 extensions (already done) plus IO validation |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Status section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation with five benchmark years validated against Table 5.7 |

---

*Data Provenance Record following Anu Standard v2.0*
