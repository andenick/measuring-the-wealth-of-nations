# T604: Total Tax on Workers (T_w) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T604 |
| Type | derived |
| Time Period | 1952-1989 |
| Frequency | annual |
| Source Count | 4 |
| Base Year | N/A |
| Units | millions of current dollars |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-25 |

---

## Context

> "The total tax burden on workers T_w is the sum of personal income taxes, social insurance contributions, and property taxes allocated to the working class. This aggregate enters the net social wage calculation as the negative term: NSW = B_w + G_w - T_w."
> -- Derived from Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

Total tax on workers (T_w) is the aggregation of three tax components: personal income taxes allocated to workers (T601), employee social insurance contributions (T602), and property taxes allocated to workers (T603). This is the central tax variable in the net social wage framework. The key finding in Shaikh & Tonak is that T_w exceeds B_w + G_w for all years 1952-1989, making the net social wage consistently negative. T_w grows substantially over the postwar period, driven primarily by rising social insurance contributions and bracket creep in personal income taxes.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T604A | Book Table 6.1 | 1952-1989 | N/A (book) | academic_research | Total T_w with component breakdown |
| T604B | NIPA Table 3.1 (Government Receipts) | 1952-2025 | BEA NIPA API | official_statistics | Total government current receipts |
| T604C | NIPA Table 3.2 (Federal Government) | 1952-2025 | BEA NIPA API | official_statistics | Federal tax components |
| T604D | NIPA Table 3.3 (State/Local Government) | 1952-2025 | BEA NIPA API | official_statistics | State/local tax components |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull NIPA government tables | BEA API | nipa_3_1, 3_2, 3_3.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 2 | Pull personal income | BEA API | nipa_2_1.csv | pull_bea_nipa_ch06.py | XFORM-062 |
| 3 | Compute T601 (personal tax on workers) | NIPA 3.2, 3.3, 2.1 | T601 | calculate_ch06.py | XFORM-063 |
| 4 | Compute T602 (social insurance on workers) | NIPA 3.1 line 8 | T602 | calculate_ch06.py | XFORM-062 |
| 5 | Compute T603 (property tax on workers) | NIPA 3.3 line 9 | T603 | calculate_ch06.py | XFORM-063 |
| 6 | Aggregate total tax on workers | T601, T602, T603 | T604 = T601 + T602 + T603 | calculate_ch06.py | XFORM-063 |

### Transformation Details

#### XFORM-063: Total Tax Aggregation

**Formula**:
```
T_w = T_w_personal + T_w_social + T_w_property
    = T601 + T602 + T603

where:
  T601 = Personal income tax x (W_p / PI)         [income-proportional allocation]
  T602 = Employee social insurance contributions   [directly extracted]
  T603 = Property tax x (worker housing share)     [housing-proportional allocation]
```

**Decomposition**: Social insurance (T602) is typically the largest component by the late period, having grown rapidly with Social Security/Medicare expansion. Personal income taxes (T601) dominate in early years. Property taxes (T603) are the smallest component throughout.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| T604 = T601 + T602 + T603 | Exact additivity | Validated 2026-03-22 | PASS |
| T604 > 0 for all years | Positive throughout | Validated 2026-03-22 | PASS |
| T604 > B_w + G_w | NSW < 0 implies T_w > benefits | Validated 2026-03-22 | PASS |
| Rising trend | Taxes on workers rise over time | Validated 2026-03-22 | PASS |
| Year coverage | 1952-1989 | 1952-1989 | PASS |

---

## Known Issues

- [ ] **Component validation**: Each component (T601-T603) must be individually validated before T604 can be confirmed
- [ ] **Allocation method consistency**: All three components must use consistent definitions of the worker class (same V*/PI ratio)
- [ ] **Cross-check with NIPA totals**: Sum of worker taxes + capitalist taxes should equal total government receipts from persons
- [ ] **Phase 1 reconciliation**: The Phase 1 NSW project may have used slightly different allocation formulas

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.1-F.4 | Complete tax decomposition by type and level of government |

---

## Related Content

- **Figures**: 6.1 (NSW levels), 6.3 (Tax decomposition by type)
- **Derived Series**: T607 (NSW = B_w + G_w - T_w)
- **Upstream Dependencies**: T601 (Personal Tax), T602 (Social Insurance), T603 (Property Tax)
- **Module**: Chapter 6 -- Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
