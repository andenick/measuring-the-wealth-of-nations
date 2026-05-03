# T606: Government Expenditure on Workers (G_w) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T606 |
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

> "Government services consumed by workers include education, health, and general public services, allocated by worker share of population. Unlike transfer payments (B_w), these represent government consumption expenditures that benefit workers indirectly through public provision of services."
> -- Derived from Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

Government expenditure on workers (G_w) captures the portion of government consumption expenditure and gross investment that benefits the working class. This includes public education, public health services, housing assistance, social services, and the worker share of general public services (police, fire, infrastructure). G_w is conceptually distinct from B_w (transfer payments): B_w represents direct cash or in-kind transfers to workers, while G_w represents the consumption value of publicly provided services. Together, B_w + G_w forms the total benefit to workers from government fiscal activity.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T606A | Book Table 6.2 | 1952-1989 | N/A (book) | academic_research | Government expenditure component of NSW |
| T606B | NIPA Table 3.1 (Government Current Expenditures) | 1952-2025 | BEA NIPA API | official_statistics | Government consumption expenditures (line 21) |
| T606C | NIPA Table 3.3 (State/Local Government) | 1952-2025 | BEA NIPA API | official_statistics | State/local expenditures by function (line 24) |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull government expenditure data | BEA API (NIPA 3.1) | nipa_3_1_govt_receipts_expenditures.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 2 | Pull state/local expenditure detail | BEA API (NIPA 3.3) | nipa_3_3_state_local_govt.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 3 | Identify worker-benefiting expenditures | NIPA 3.1, 3.3 | education + health + housing + social | calculate_ch06.py | XFORM-065 |
| 4 | Allocate general expenditures by worker share | General expenditures, worker population share | G_w_general = general_exp x (Lw / L_total) | calculate_ch06.py | XFORM-065 |
| 5 | Compute total G_w | Worker-specific + allocated general | T606 = G_w | calculate_ch06.py | XFORM-065 |

### Transformation Details

#### XFORM-065: Government Expenditure on Workers

**Formula**:
```
G_w = G_education + G_health + G_housing + G_social + G_general_allocated

where:
  G_education = Public education expenditure (primarily state/local)
  G_health    = Public health expenditure (federal + state/local)
  G_housing   = Government housing programs
  G_social    = Social services administration
  G_general_allocated = General public services x (worker share of population)

Worker share of population is approximated by the ratio of workers
(and dependents) to total population, or by Lw/L from employment data.

Source: NIPA 3.1 line 21 (government consumption expenditures)
        NIPA 3.3 line 24 (state/local current expenditures)
```

**Notes**: Education is the single largest component of G_w and is overwhelmingly a state/local expenditure. The allocation of general public services (defense, administration, justice) requires an assumption about benefit incidence; Shaikh & Tonak use population share as the allocation key.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| G_w > 0 for all years | Positive throughout | Validated 2026-03-22 | PASS |
| G_w rising trend | Upward with government expansion | Validated 2026-03-22 | PASS |
| Education dominant | Education is largest component | Validated 2026-03-22 | PASS |
| B_w + G_w < T_w | Required for NSW < 0 | Validated 2026-03-22 | PASS |
| Year coverage | 1952-1989 | 1952-1989 | PASS |

---

## Known Issues

- [ ] **Expenditure classification**: Distinguishing worker-benefiting from capitalist-benefiting expenditures (e.g., infrastructure, defense) is inherently debatable
- [ ] **Population share allocation**: Using worker population share for general services assumes equal per-capita benefit, which may not hold for all categories
- [ ] **NIPA functional classification**: NIPA tables do not provide expenditure by function at the same granularity as Census of Governments; may need supplementary data
- [ ] **Federal vs state/local**: Federal expenditure is dominated by defense (not worker-benefiting); state/local is dominated by education (worker-benefiting)

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.3-F.4 | Government expenditure by function and level |

---

## Related Content

- **Figures**: 6.1 (NSW levels), 6.4 (Benefit decomposition)
- **Derived Series**: T607 (NSW = B_w + G_w - T_w)
- **Upstream Dependencies**: None (extracted and allocated from NIPA)
- **Module**: Chapter 6 -- Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
