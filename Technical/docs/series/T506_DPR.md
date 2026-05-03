# T506: Rate of Exploitation (e = S*/V*) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T506 |
| Type | derived |
| Time Period | 1948-2024 |
| Frequency | annual |
| Source Count | 3 |
| Base Year | N/A |
| Units | ratio (dimensionless) |
| Validation Status | VALIDATED (book period); PROVISIONAL (extension) |
| Last Updated | 2026-02-23 |

---

## Context

> "The rate of exploitation e = S*/V* rose from 1.70 in 1948 to 2.44 in 1989, reflecting the increasing share of surplus value relative to the compensation of productive workers."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, p. 115, Table 5.7

The rate of exploitation is THE keystone series in AS2. It measures the ratio of surplus value (S*) to variable capital (V*), i.e., how much surplus labor is extracted relative to the compensation of productive workers. All validation gates ultimately reference this series because it synthesizes both the labor classification (who is productive) and the value decomposition (how output is divided).

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T506A | Book Table 5.7 (Shaikh & Tonak 1994) | 1948-1989 | N/A (book) | academic_research | 5 benchmark years: 1948, 1958, 1967, 1977, 1989 |
| T506B | NIPA-derived (Phase 3 calculation) | 1948-1989 | BEA NIPA 1.7.5, 6.2D | calculated | Uses VA*/W=1.238 constant; see DIV-002 |
| T506C | BLS CES extension | 1990-2024 | BLS CES | calculated | Production worker ratios + book methodology |

### Quality Categories
- `academic_research` - Peer-reviewed source (HIGH reliability)
- `calculated` - Derived from formulas (VARIES — depends on inputs)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull NIPA compensation data | BEA API | nipa_6_2D_compensation.csv | pull_bea_nipa_ch05.py | XFORM-001 |
| 2 | Pull NIPA gross output | BEA API | nipa_1_7_5_gross_output.csv | pull_bea_nipa_ch05.py | XFORM-002 |
| 3 | Classify sectors (p/u) | IO tables | sector_classification | (manual / Ch 4) | XFORM-003 |
| 4 | Compute V* = W × (V*/W) | NIPA 6.2D + BLS ratios | V* series | calculate_ch05.py | XFORM-004 |
| 5 | Compute S* = GFP - V* | T503, T504 | S* series | calculate_ch05.py | XFORM-005 |
| 6 | Compute e = S*/V* | T504, T505 | T506 series | calculate_ch05.py | XFORM-006 |
| 7 | Validate against benchmarks | T506, book values | pass/fail | validate_ch05.py | XFORM-007 |

### Transformation Details

#### XFORM-006: Exploitation Rate Calculation

**Formula**:
```
e = S* / V*
  = (GFP - V*) / V*
  = (GFP / V*) - 1

where:
  GFP = TP* - C*_m (Gross Final Product)
  V* = W × (Lp/L) × (ec_u/ec_p) ≈ W × (Lp/L) when ec_u/ec_p ≈ 1
  S* = GFP - V*
```

**Parameters**:
- ec_u/ec_p: Ratio of unproductive to productive employee compensation per worker (empirically ≈ 1)
- VA*/W: Value added ratio (Phase 3 used constant 1.238; to be replaced with year-varying)

**Notes**: The exploitation rate rises secularly from 1.70 (1948) to 2.44 (1989) because productive employment (Lp) falls as a share of total employment while output continues to grow.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| e(1948) | 1.70 | 1.70 | PASS |
| e(1958) | 1.83 | 1.83 | PASS |
| e(1967) | 2.10 | 2.10 | PASS |
| e(1977) | 2.10 | 2.10 | PASS |
| e(1989) | 2.44 | 2.44 | PASS |
| Monotonic trend | Generally increasing | Confirmed (plateau 1967-1977) | PASS |
| Value Range | 1.0-4.0 | 1.70-3.59 | PASS |
| Year Coverage | 1948-2024 | 1948-2024 | PASS |

### Validation Notes

The 1967-1977 plateau (e ≈ 2.10) is a genuine feature of the data, not an interpolation artifact. It reflects the offsetting effects of rising labor productivity and the shift of employment toward unproductive sectors during this period.

---

## Known Issues

- [x] **Benchmark match**: All 5 benchmark years match book values exactly
- [ ] **VA*/W constant**: Phase 3 used VA*/W = 1.238 constant; inter-benchmark values may differ from true book calculation (DIV-002)
- [ ] **Extension uses placeholder BLS**: Post-1989 extension uses placeholder BLS ratios; needs real API data
- [ ] **NIPA-derived e differs from authoritative e**: The NIPA-calculated exploitation rate (T506B ≈ 1.32-1.52) differs from authoritative book values (T506A ≈ 1.70-2.44) because Phase 3 NIPA data is placeholder

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App D | National Accounts Detail | D.2 | Source data for TP*, C*_m, GFP components |
| App E | Revenue Accounts | E.2 | Row-by-row construction of Marxian accounts |
| App E | Labor Statistics | E.3 | Sector employment decomposition for Lp/L |

### Key Appendix Variables
- **TP***: Total Product of productive sectors (Table D.2 / NIPA 1.7.5)
- **C*_m**: Material constant capital (intermediate inputs, Table D.2)
- **V***: Variable capital (productive worker compensation, NIPA 6.2D adjusted)
- **S***: Surplus value (residual: GFP - V*)

---

## Related Content

- **Figures**: 5.1 (Exploitation Rate), 5.2 (Exploitation Rate Extended), 5.3 (Surplus Ratio)
- **Derived Series**: T507 (Surplus Ratio), T513 (Profit Rate), T901 (Summary)
- **Module**: Chapter 5 — Accounting Framework
- **Appendices**: D, E

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T506_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | e = (VA*/W)/(V*/W) - 1 using VA*/W=1.238 constant × T512 |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 72% |
| Certification | NOT CERTIFIED |
| EXTENSION_LOG Entry | EXT-007 |
| Extension Date | 2026-02-24 |
| Divergences | DIV-002 (ec_u/ec_p = 1 assumption) |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Documentation section (Session 8) |
| 2026-02-23 | 1.0 | Initial creation with book benchmarks validated |

---

*Data Provenance Record following Anu Standard v2.0*
