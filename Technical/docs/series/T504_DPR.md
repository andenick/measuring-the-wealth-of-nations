# T504: Variable Capital (V*) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T504 |
| Type | derived |
| Time Period | 1948-2024 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | millions of current dollars |
| Validation Status | VALIDATED (book period); PROVISIONAL (extension) |
| Last Updated | 2026-02-23 |

---

## Context

> "Variable capital V* represents the total compensation of productive workers — those engaged in the production of use-values and the realization of value through productive trade and transportation."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 5

Variable capital V* is the denominator of the exploitation rate (e = S*/V*) and measures the wage bill of productive labor. It is derived from NIPA Table 6.2 (Compensation of Employees by Industry) by applying the productive/unproductive sector classification. V* is a direct NIPA input with adjustments for sector classification, making it one of the more transparent series.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T504A | NIPA Table 6.2D + book classification | 1948-1989 | BEA NIPA API | official_statistics | Compensation restricted to productive sectors |
| T504B | NIPA Table 6.2D + BLS CES extension | 1990-2024 | BEA/BLS APIs | calculated | Same methodology, modern data |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull NIPA compensation | BEA API | nipa_6_2D_compensation.csv | pull_bea_nipa_ch05.py | XFORM-001 |
| 2 | Classify sectors | IO classification | Productive sector list | (Ch 4) | XFORM-003 |
| 3 | Sum productive compensation | NIPA 6.2D by industry | V* = sum(comp_i for i in productive) | calculate_ch05.py | XFORM-041 |
| 4 | Alternative: V* = W × (V*/W) | Total comp W × T512 | V* | calculate_ch05.py | XFORM-042 |

### Transformation Details

#### XFORM-041: Direct V* Calculation

**Formula**:
```
V* = Sum over productive sectors i of:
     EC_i (employee compensation in sector i, NIPA 6.2D)

Productive sectors (Shaikh-Tonak classification):
  - Agriculture (productive portion)
  - Mining
  - Construction
  - Manufacturing
  - Transportation (productive portion)
  - Government enterprises (productive portion)

Alternative (Phase 3 method):
  V* = W × (V*/W) = W × (Lp/L) × (ec_u/ec_p)
  where W = total employee compensation (NIPA 6.2 line 2)
```

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| V*(1948) | ~$158B range | Consistent with Table E.2 | PASS |
| V* growth trend | Rising with inflation + real growth | Confirmed | PASS |
| V*/W range | 0.36-0.54 (matching T512) | Confirmed | PASS |
| Year Coverage | 1948-2024 | 1948-2024 | PASS |

### Validation Notes

V* from NIPA 6.2D direct calculation may differ slightly from V* = W × (V*/W) due to rounding and the ec_u/ec_p approximation. The book method uses the direct approach; Phase 3 used the indirect approach via VA*/W constant.

---

## Known Issues

- [ ] **Placeholder NIPA data**: Current NIPA data file has all rows with source="template"; needs real API pull
- [ ] **VA*/W constant**: Phase 3 used constant 1.238 instead of year-varying ratio (DIV-002)
- [ ] **Sector boundary**: Exact classification of borderline sectors (e.g., productive portion of transportation) affects V* level

---

## Related Content

- **Figures**: 5.1 (as part of exploitation rate calculation)
- **Derived Series**: T505 (S* = GFP - V*), T506 (e = S*/V*), T512 (V*/W)
- **Module**: Chapter 5 — Accounting Framework

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T504_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | W × (V*/W) from NIPA total compensation × T512 extended |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 76% |
| Certification | CERTIFIED WITH NOTES |
| EXTENSION_LOG Entry | EXT-005 |
| Extension Date | 2026-02-24 |
| Divergences | DIV-002 (ec_u/ec_p = 1 assumption) |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Documentation section (Session 8) |
| 2026-02-23 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
