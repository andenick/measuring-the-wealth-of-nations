# T505: Surplus Value (S*) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T505 |
| Type | derived |
| Time Period | 1948-1989 (extended 1948-2024) |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | billions of current dollars |
| Validation Status | VALIDATED (book period); PROVISIONAL (extension) |
| Last Updated | 2026-02-24 |

---

## Context

> "Surplus value S* is the portion of value added that accrues to capital after paying variable capital. In the Marxian accounts, S* is approximately twice conventional profit-type income, because it includes not only profits but also the compensation of unproductive workers and various forms of property income that are funded out of the social surplus."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 5, Table 5.14, p. 140

Surplus value S* is the central measure of capitalist appropriation in the Marxian framework. It represents the difference between the total value added by productive labor (VA* = T503) and the wages paid to productive workers (V* = T504). Equivalently, S* = e x V*, where e is the rate of exploitation (T506). The secular rise in S* reflects both the growth of total output and the increasing rate of exploitation as employment shifts from productive to unproductive sectors. S* is approximately 224% of conventional profit-type income (Table 5.14, p. 140), because the conventional measure excludes the compensation of unproductive labor that the Marxian framework counts as part of surplus.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T505A | Derived from T503 (VA*) and T504 (V*) | 1948-1989 | N/A (derived) | calculated | S* = VA* - V* = T503 - T504 |
| T505B | Extended series from T503, T504 extensions | 1990-2024 | N/A (derived) | calculated | Inherits extension methodology from parent series |

### Quality Categories
- `calculated` - Derived from formulas (VARIES -- depends on inputs T503, T504)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Compute VA* (value added) | NIPA-derived gross output | T503 series | calculate_ch05.py | XFORM-050 |
| 2 | Compute V* (variable capital) | NIPA 6.2D by sector | T504 series | calculate_ch05.py | XFORM-041 |
| 3 | Compute S* = VA* - V* | T503, T504 | T505 series | calculate_ch05.py | XFORM-051 |
| 4 | Cross-check: S* = e x V* | T506, T504 | T505 (verify) | validate_ch05.py | XFORM-052 |

### Transformation Details

#### XFORM-051: Surplus Value Calculation

**Formula**:
```
S* = VA* - V*
   = T503 - T504

Equivalently:
  S* = e × V*
  where e = rate of exploitation (T506)

Components of S*:
  - Compensation of unproductive workers (largest component)
  - Corporate profits (before tax)
  - Net interest income
  - Rental income
  - Indirect business taxes (portion)
  - Capital consumption allowances (portion)

Cross-check identity:
  S* / V* = e  (must equal T506 values)
```

**Parameters**:
- VA* (T503): Marxian value added (gross final product of productive sectors)
- V* (T504): Variable capital (total compensation of productive workers)

**Notes**: S* rises secularly because VA* grows faster than V* -- a direct consequence of the falling share of productive employment (Lp/L, T511) combined with rising labor productivity.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| S*/P ratio | ~224% (Table 5.14) | Consistent with book benchmark | PASS |
| S* > 0 | Positive for all years | Confirmed 1948-1989 | PASS |
| S* = VA* - V* identity | T505 = T503 - T504 | Confirmed (exact) | PASS |
| S*/V* = e cross-check | Must equal T506 | Matches T506 benchmarks | PASS |
| S*(1948) growth direction | Rising with nominal GDP | Confirmed | PASS |
| Year Coverage | 1948-1989 (book); 1948-2024 (extended) | 1948-2024 | PASS |

### Validation Notes

S* can be independently validated two ways: (1) as the residual VA* - V*, and (2) via e x V* where e is the book exploitation rate. Both methods must agree. The ratio S*/P (surplus value to conventional profit) of approximately 224% is a key diagnostic: if S*/P deviates significantly from this range, it signals a classification error in either S* or P. The conventional profit measure P excludes unproductive worker compensation and certain property income flows that the Marxian framework attributes to surplus.

---

## Known Issues

- [ ] **VA* extension uncertain**: S* extension depends on both VA* (T503) and V* (T504) extended series, each carrying their own provisional status
- [ ] **S* extension depends on both VA* and V* extended series**: Any errors in the parent extensions compound in S*
- [ ] **Conventional profit comparison**: The S*/P ~ 224% benchmark needs verification with NIPA corporate profit data (Table 1.12) for each year, not just the aggregate ratio
- [ ] **Pre-1948 unavailable**: No book data before 1948; S* cannot be computed without both VA* and V*

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App D | National Accounts Detail | D.2 | Source data for VA* components (TP*, C*_m) |
| App E | Revenue Accounts | E.2 | Row-by-row construction of Marxian value added and surplus decomposition |

### Key Appendix Variables
- **VA***: Value added of productive sectors (= TP* - C*_m, Table D.2)
- **V***: Variable capital (productive worker compensation, NIPA 6.2D adjusted)
- **S***: Surplus value (residual: VA* - V*)
- **P**: Conventional profit-type income (NIPA-based, for comparison)

---

## Related Content

- **Book Table**: 5.5, 5.14 (comparison with conventional measures)
- **Figures**: 5.1 (as part of exploitation rate calculation), 5.3 (surplus ratio)
- **Derived Series**: T506 (e = S*/V*), T507 (S*/(S*+V*)), T513 (profit rate)
- **Dependencies**: T503 (VA*), T504 (V*)
- **Module**: Chapter 5 -- Accounting Framework

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T505_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | S* = e × V* from T506 extended × T504 extended |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 70% |
| Certification | NOT CERTIFIED |
| EXTENSION_LOG Entry | EXT-006 |
| Extension Date | 2026-02-24 |
| Divergences | DIV-002 (ec_u/ec_p = 1 assumption) |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Documentation section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation with book period validated against Table 5.14 benchmarks |

---

*Data Provenance Record following Anu Standard v2.0*
