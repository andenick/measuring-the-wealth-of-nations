# T602: Social Insurance Tax on Workers (T_w_social) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T602 |
| Type | extracted |
| Time Period | 1952-1989 |
| Frequency | annual |
| Source Count | 2 |
| Base Year | N/A |
| Units | millions of current dollars |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-25 |

---

## Context

> "Social insurance contributions from workers are directly identifiable in NIPA accounts, unlike other tax types which require allocation between workers and capitalists."
> -- Derived from Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

Social insurance tax on workers (T_w_social) captures the employee-side contributions for government social insurance programs (Social Security, Medicare, unemployment insurance). Unlike personal income taxes (T601) or property taxes (T603), which require allocation between workers and capitalists using income or housing shares, social insurance contributions from employees are directly reported in NIPA tables. The employee portion is unambiguously a tax on workers because it is withheld from wages. This makes T602 the most cleanly extracted component of the total tax on workers.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T602A | Book Table 6.1 | 1952-1989 | N/A (book) | academic_research | Social insurance component of T_w |
| T602B | NIPA Table 3.1 (Government Receipts) | 1952-2025 | BEA NIPA API | official_statistics | Contributions for government social insurance (line 8) |
| T602C | NIPA Table 3.2 (Federal Government) | 1952-2025 | BEA NIPA API | official_statistics | Federal employee contributions (lines 10-11) |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull government receipts | BEA API (NIPA 3.1) | nipa_3_1_govt_receipts_expenditures.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 2 | Pull federal government detail | BEA API (NIPA 3.2) | nipa_3_2_federal_govt.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 3 | Extract employee social insurance contributions | NIPA 3.1 line 8 (persons) | T602 = employee SI contributions | calculate_ch06.py | XFORM-062 |

### Transformation Details

#### XFORM-062: Social Insurance Extraction

**Formula**:
```
T_w_social = SI_employee

where:
  SI_employee = Employee contributions for government social insurance
              = NIPA 3.1 line 8 (contributions from persons)

Note: Employer contributions are NOT included — they are part of the
capitalist tax burden and are captured separately.
```

**Notes**: The distinction between employee and employer contributions is critical. NIPA 3.1 line 7 reports total social insurance contributions; line 8 isolates the personal (employee) portion. Only the employee portion is allocated to workers.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| T602 > 0 for all years | Positive throughout | Validated 2026-03-22 | PASS |
| T602 < total SI contributions | Less than total (line 7) | Validated 2026-03-22 | PASS |
| Rising trend | SI contributions rose steadily | Validated 2026-03-22 | PASS |
| Year coverage | 1952-1989 | 1952-1989 | PASS |

---

## Known Issues

- [ ] **Employee vs personal contributions**: NIPA reporting of "personal" vs "employee" contributions may vary across revisions; need to confirm correct line references
- [ ] **Self-employed contributions**: Self-employment tax (SECA) combines employee and employer portions; allocation to workers requires separate treatment
- [ ] **Medicare introduction**: Medicare contributions begin in 1966, creating a structural break in the series

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.1-F.2 | Social insurance contribution detail |

---

## Related Content

- **Figures**: 6.3 (Tax decomposition by type)
- **Derived Series**: T604 (Total Tax on Workers = T601 + T602 + T603)
- **Upstream Dependencies**: None (directly extracted from NIPA)
- **Module**: Chapter 6 -- Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
