# T603: Property Tax on Workers (T_w_property) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T603 |
| Type | derived |
| Time Period | 1952-1989 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | millions of current dollars |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-25 |

---

## Context

> "Property taxes are allocated to workers proportional to their share of total housing expenditure, reflecting the fact that property taxes are primarily levied on residential and commercial real estate."
> -- Derived from Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

Property tax on workers (T_w_property) captures the portion of state and local property taxes attributable to the working class. The allocation key is the worker share of total housing expenditure, which proxies for worker ownership of taxable real estate. Property taxes are overwhelmingly a state/local revenue source (NIPA 3.3), with negligible federal property taxation. This is typically the smallest of the three tax components (T601-T603), reflecting the fact that property ownership is concentrated among the capitalist class. The allocation methodology parallels the income-proportional approach used for personal taxes but uses a housing-specific denominator.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T603A | Book Table 6.1 | 1952-1989 | N/A (book) | academic_research | Property tax component of T_w |
| T603B | NIPA Table 3.3 (State/Local Government) | 1952-2025 | BEA NIPA API | official_statistics | Property taxes (line 9) |
| T603C | NIPA Table 2.1 (Personal Income) | 1952-2025 | BEA NIPA API | official_statistics | Housing expenditure and compensation data |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull state/local government receipts | BEA API (NIPA 3.3) | nipa_3_3_state_local_govt.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 2 | Pull personal income data | BEA API (NIPA 2.1) | nipa_2_1_personal_income.csv | pull_bea_nipa_ch06.py | XFORM-062 |
| 3 | Compute worker housing share | W_p, housing expenditure data | beta_w = worker housing / total housing | calculate_ch06.py | XFORM-063 |
| 4 | Allocate property taxes to workers | beta_w, NIPA 3.3 line 9 | T603 = property_tax x beta_w | calculate_ch06.py | XFORM-063 |

### Transformation Details

#### XFORM-063: Property Tax Allocation

**Formula**:
```
T_w_property = PT_sl x beta_w

where:
  PT_sl  = State/local property taxes (NIPA 3.3 line 9)
  beta_w = Worker share of housing expenditure
         = (worker housing expenditure) / (total housing expenditure)

The worker housing share is approximated using the ratio of worker
compensation to total personal income as a proxy, unless direct housing
expenditure data by class is available from the Consumer Expenditure Survey.
```

**Notes**: Property taxes at the federal level are negligible and excluded. The housing-share proxy assumes that workers and capitalists consume housing in proportion to their incomes, which may understate the worker share given that housing is a larger fraction of expenditure for lower-income households.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| T603 > 0 for all years | Positive throughout | Validated 2026-03-22 | PASS |
| T603 < total property tax | Less than 100% of state/local property tax | Validated 2026-03-22 | PASS |
| T603 smallest component | Smaller than T601 and T602 | Validated 2026-03-22 | PASS |
| Year coverage | 1952-1989 | 1952-1989 | PASS |

---

## Known Issues

- [ ] **Housing share proxy**: Using income share as a proxy for housing share may introduce bias; direct housing data would improve accuracy
- [ ] **Renters vs owners**: Property taxes on rental housing are passed through to renters; the allocation method should capture this but the mechanism is indirect
- [ ] **NIPA 3.3 line mapping**: Property tax line numbers may shift across NIPA comprehensive revisions
- [ ] **Commercial property**: Some property taxes fall on commercial/industrial property, which is not directly allocable to workers as housing

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.3-F.4 | State/local tax decomposition including property taxes |

---

## Related Content

- **Figures**: 6.3 (Tax decomposition by type)
- **Derived Series**: T604 (Total Tax on Workers = T601 + T602 + T603)
- **Upstream Dependencies**: None (allocation uses NIPA inputs directly)
- **Module**: Chapter 6 -- Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
