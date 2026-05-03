# T601: Personal Tax on Workers (T_w_personal) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T601 |
| Type | derived |
| Time Period | 1952-1989 |
| Frequency | annual |
| Source Count | 3 |
| Base Year | N/A |
| Units | millions of current dollars |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-25 |

---

## Context

> "The allocation of personal income taxes between workers and capitalists follows the income-proportional method: each class pays taxes in proportion to its share of total personal income."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

Personal tax on workers (T_w_personal) captures the portion of federal and state/local personal income taxes attributable to the working class. The allocation key is the ratio of worker compensation (W_p, from variable capital V*) to total personal income. This is the largest component of the total tax burden on workers (T604) and reflects the progressive structure of income taxation filtered through the Marxian class lens. Because worker compensation is a declining share of personal income over the postwar period, the worker share of income taxes also declines relative to total tax collections.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T601A | Book Table 6.1 | 1952-1989 | N/A (book) | academic_research | Personal tax component of T_w |
| T601B | NIPA Table 3.2 (Federal Government) | 1952-2025 | BEA NIPA API | official_statistics | Federal personal current taxes (line 3) |
| T601C | NIPA Table 3.3 (State/Local Government) | 1952-2025 | BEA NIPA API | official_statistics | State/local personal current taxes (line 3) |
| T601D | NIPA Table 2.1 (Personal Income) | 1952-2025 | BEA NIPA API | official_statistics | Total personal income and compensation |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull federal government receipts | BEA API (NIPA 3.2) | nipa_3_2_federal_govt.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 2 | Pull state/local government receipts | BEA API (NIPA 3.3) | nipa_3_3_state_local_govt.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 3 | Pull personal income and compensation | BEA API (NIPA 2.1) | nipa_2_1_personal_income.csv | pull_bea_nipa_ch06.py | XFORM-062 |
| 4 | Compute worker share of personal income | W_p (from T504), PI (NIPA 2.1 line 1) | alpha_w = W_p / PI | calculate_ch06.py | XFORM-063 |
| 5 | Allocate personal taxes to workers | alpha_w, personal taxes (3.2 + 3.3) | T601 = (federal + state/local personal tax) x alpha_w | calculate_ch06.py | XFORM-063 |

### Transformation Details

#### XFORM-063: Personal Tax Allocation

**Formula**:
```
T_w_personal = (PT_fed + PT_sl) x (W_p / PI)

where:
  PT_fed = Federal personal current taxes (NIPA 3.2 line 3)
  PT_sl  = State/local personal current taxes (NIPA 3.3 line 3)
  W_p    = Worker compensation (V* from T504)
  PI     = Total personal income (NIPA 2.1 line 1)
```

**Notes**: The income-proportional allocation assumes that workers and capitalists face the same effective tax rate on personal income. This is a simplification — progressive rate structures would allocate proportionally less to workers — but it provides a consistent and reproducible baseline.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| T601 > 0 for all years | Positive throughout | Validated 2026-03-22 | PASS |
| T601 < total personal tax | Less than 100% of personal tax | Validated 2026-03-22 | PASS |
| Worker share declining | alpha_w declining over time | Validated 2026-03-22 | PASS |
| Year coverage | 1952-1989 | 1952-1989 | PASS |

---

## Known Issues

- [ ] **Allocation method sensitivity**: Income-proportional method may overstate worker tax burden relative to statutory or incidence-based approaches
- [ ] **V* dependency**: Requires validated T504 (Variable Capital) for worker compensation share
- [ ] **NIPA line mapping**: Federal and state/local tables use different line numbering conventions across NIPA revisions
- [ ] **Pre-1959 state/local data**: NIPA 3.3 coverage may be limited for earliest years of the series

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.1-F.2 | Tax decomposition by type and level of government |

---

## Related Content

- **Figures**: 6.3 (Tax decomposition by type)
- **Derived Series**: T604 (Total Tax on Workers = T601 + T602 + T603)
- **Upstream Dependencies**: T504 (Variable Capital V*)
- **Module**: Chapter 6 -- Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
