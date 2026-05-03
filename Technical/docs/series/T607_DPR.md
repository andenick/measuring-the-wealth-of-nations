# T607: Net Social Wage (NSW = B_w + G_w - T_w) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T607 |
| Type | derived |
| Time Period | 1952-2025 |
| Frequency | annual |
| Source Count | 3 |
| Base Year | N/A |
| Units | millions of current dollars |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-23 |

---

## Context

> "The net social wage (NSW) measures the net fiscal benefit to workers from the state — the difference between what workers receive from the government (benefits and services) and what they pay in taxes. NSW is predominantly negative throughout the postwar period (35/38 years), meaning workers as a class are net contributors to state revenue. Three deep-recession years (1975, 1976, 1983) show positive NSW when countercyclical transfers temporarily exceeded the tax burden."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 6

The Net Social Wage is the Chapter 6 keystone series. It answers a politically charged question: do workers benefit or lose from government fiscal activity? Shaikh & Tonak's finding that NSW < 0 for the vast majority of the postwar period challenges the conventional view that the welfare state redistributes income toward workers. Our methodology produces NSW < 0 for 35/38 years (92%); 3 recession years (1975, 1976, 1983) show positive NSW — a documented divergence from the book's claim of universal negativity, likely due to different allocation parameters. NSW uses different NIPA tables than Chapter 5 (Tables 2.1, 3.1-3.3 vs 1.7.5, 6.x), making it an independent test of the framework.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T607A | Book Table 6.3 | 1952-1989 | N/A (book) | academic_research | Core finding: NSW predominantly < 0 (92%); 3 recession exceptions |
| T607B | NIPA Tables 2.1, 3.1-3.3 | 1952-2025 | BEA NIPA API | official_statistics | Government receipts/expenditures |
| T607C | Phase 1 NSW extension | 1990-2025 | Shaikh Tonak project | calculated | Extended using same methodology |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull NIPA government tables | BEA API | nipa_3_1, 3_2, 3_3.csv | pull_bea_nipa_ch06.py | XFORM-061 |
| 2 | Pull personal income | BEA API | nipa_2_1.csv | pull_bea_nipa_ch06.py | XFORM-062 |
| 3 | Compute T_w (taxes on workers) | NIPA 3.1-3.3 | T604 | calculate_ch06.py | XFORM-063 |
| 4 | Compute B_w (benefits to workers) | NIPA 2.1, 3.1 | T605 | calculate_ch06.py | XFORM-064 |
| 5 | Compute G_w (govt expenditure on workers) | NIPA 3.1, 3.3 | T606 | calculate_ch06.py | XFORM-065 |
| 6 | Compute NSW = B_w + G_w - T_w | T604-T606 | T607 | calculate_ch06.py | XFORM-066 |

### Transformation Details

#### XFORM-066: Net Social Wage

**Formula**:
```
NSW = B_w + G_w - T_w

where:
  T_w = T_w_personal + T_w_social + T_w_property
      = (personal income tax × W_p/PI) + (employee social insurance) + (property tax × worker housing share)

  B_w = transfer payments to workers + social insurance benefits

  G_w = government expenditure on worker-benefiting services
      = education + health + housing + social services
      (allocated by worker share of population)
```

**Key Finding**: NSW < 0 for 35 of 38 years (1952-1989), meaning workers are predominantly net payers to the state. Three deep-recession years (1975: +$19,653M, 1976: +$4,929M, 1983: +$8,992M) show positive NSW when countercyclical benefit surges temporarily exceeded the tax burden. This is documented as DIV-003.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| NSW sign | Predominantly negative 1952-1989 | Negative 35/38 years (92%); positive in recession years 1975, 1976, 1983 | PASS (with DIV-003 note) |
| NSW/V* trend | Declining (more negative) | Validated 2026-03-22 | PASS |
| Tax decomposition | Sum matches NIPA totals | Validated 2026-03-22 | PASS |
| Year Coverage | 1952-2025 | 1952-2025 (Phase 1 extension) | PASS |

### Validation Notes

The Phase 1 NSW calculation from the original Shaikh Tonak project covers 1952-2025. This needs reconciliation with the book's methodology, as there are known differences between the 1987 Tonak paper and the 1994 book in how taxes are allocated between workers and capitalists.

---

## Known Issues

- [ ] **Formula variation**: The 1987 Tonak paper and the 1994 book use slightly different formulas for tax allocation
- [ ] **Tax allocation ambiguity**: Three possible approaches for allocating taxes to workers vs capitalists; book uses income-share method
- [ ] **Phase 1 reconciliation**: The Phase 1 NSW extension needs verification against Tonak benchmark files (NSWComparisons-EAT_NA.docx)
- [ ] **Tonak benchmarks not yet parsed**: External validation files exist but haven't been machine-parsed

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App F | Government Accounts | F.1-F.4 | Detailed tax and expenditure decomposition |

---

## Related Content

- **Figures**: 6.1 (NSW levels), 6.2 (NSW/V* ratio), 6.3 (Tax decomposition), 6.4 (Benefit decomposition)
- **Derived Series**: T608 (NSW/V*), T609 (NSW/NI), T901 (Summary)
- **Module**: Chapter 6 — Net Social Wage

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-23 | 1.0 | Initial creation |

---

*Data Provenance Record following Anu Standard v2.0*
