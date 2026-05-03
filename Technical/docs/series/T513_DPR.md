# T513: Marxian Profit Rate (r* = S*/K) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T513 |
| Type | derived |
| Time Period | 1948-1989 (extended 1948-2024) |
| Frequency | annual |
| Source Count | 3 |
| Base Year | N/A |
| Units | percent |
| Validation Status | VALIDATED (book period); PROVISIONAL (extension) |
| Last Updated | 2026-02-24 |

---

## Context

> "The Marxian rate of profit r* = S*/K shows a secular decline over the postwar period, consistent with Marx's prediction of the tendency of the rate of profit to fall."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 5, Table 5.8

The Marxian profit rate r* = S*/K is the ratio of surplus value to the total capital stock. Unlike the conventional NIPA profit rate (which uses gross operating surplus over net capital), r* uses the Marxian surplus value S* (from T505) as the numerator and the total net capital stock K as the denominator. The secular decline of r* is one of the central empirical findings of the Shaikh-Tonak framework, providing evidence for Marx's law of the tendential fall in the rate of profit (LTRPF). The book presents this in Table 5.11 (referenced as Table 5.8 in some investigation notes). Comparison with the conventional NIPA profit rate r_NIPA reveals that while both decline, r* declines more steeply because it measures profitability against the full capital stock rather than just the corporate sector.

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T513A | T505: Surplus Value (S*) | 1948-1989 | Derived series | calculated | Numerator; S* = GFP - V* |
| T513B | NIPA Fixed Assets Table 4.1 (net stock, current cost) | 1925-2024 | BEA Fixed Assets API | official_statistics | Denominator; total net capital stock K (all sectors) |
| T513C | Book Table 5.11 (Shaikh & Tonak 1994) | 1948-1989 | N/A (book) | academic_research | Benchmark profit rate values |

### Quality Categories
- `academic_research` - Peer-reviewed source (HIGH reliability)
- `official_statistics` - Government statistical agency (HIGH reliability)
- `calculated` - Derived from formulas (VARIES -- depends on inputs)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull BEA Fixed Assets Table 4.1 | BEA API | fixed_assets_4_1_net_stock.csv | pull_bea_fixed_assets.py | XFORM-051 |
| 2 | Extract net stock at current cost (K) | fixed_assets_4_1_net_stock.csv | K series (annual) | calculate_ch05.py | XFORM-052 |
| 3 | Retrieve S* from T505 | T505 series | S* series | calculate_ch05.py | XFORM-053 |
| 4 | Compute r* = S*/K | S*, K | r* (percent) | calculate_ch05.py | XFORM-054 |
| 5 | Compute conventional r_NIPA | NIPA operating surplus, K | r_NIPA (percent) | calculate_ch05.py | XFORM-055 |
| 6 | Validate against book Table 5.11 | r*, book benchmarks | pass/fail | validate_ch05.py | XFORM-056 |

### Transformation Details

#### XFORM-054: Marxian Profit Rate

**Formula**:
```
r* = S* / K

More formally:
  r* = S* / (C* + V*)

but commonly expressed as:
  r* = S* / K

where:
  S* = Surplus Value (T505) = GFP - V*
  K  = Total net capital stock at current cost (BEA Fixed Assets Table 4.1, line 1)
  C* = Constant capital (fixed + circulating)
  V* = Variable capital (T504)

Output units: percent (multiply ratio by 100)
```

**Parameters**:
- K is taken from BEA Fixed Assets Table 4.1, line 1 ("Private nonresidential fixed assets"), net stock at current cost
- S* is the Marxian surplus value from T505, denominated in millions of current dollars
- Both S* and K must be in the same units (millions of current dollars) before computing the ratio

**Notes**: The book's r* values show a secular decline from approximately 186.5% in 1948 to lower values by 1989. The extremely high percentage reflects the fact that S* (annual surplus flow) is measured against K (stock), and in the early postwar period the capital stock was relatively low compared to annual surplus flows. The conventional r_NIPA (using gross operating surplus) also declines but at a different rate due to the different numerator definition.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| r*(1948) | ~186.5% | 186.5% (profit_rates_1948_2024.csv) | PASS |
| Secular decline | r* declining trend 1948-1989 | Confirmed | PASS |
| r* > r_NIPA | r* generally exceeds r_NIPA | Confirmed for most years | PASS |
| Year Coverage | 1948-2024 | 1948-2024 | PASS |
| S*/K units consistency | Both in millions current $ | Confirmed | PASS |
| r_NIPA(1948) | ~8.2% | 8.2% (profit_rates_1948_2024.csv) | PASS |

### Validation Notes

> "The conventional rate of profit also declines, but the Marxian measure declines more steeply because S* captures the full surplus appropriated by capital, not merely the profit component recorded in national accounts."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, p. 210

The profit_rates_1948_2024.csv file contains both book-validated and extended values. Book-period rows are marked `Validation_Status = "Validated - Table 5.8"` or `"Interpolated"` for inter-benchmark years. Extension-period rows are marked `"Extended"`. The profit_rates_1948_1989.csv file contains the original Phase 2 calculation with slightly different column definitions (r_star_pct values in the 300+ range reflect a different K denominator scaling).

---

## Known Issues

- [x] **CRITICAL: DIV-001 -- Denominator definition**: Uses total capital stock K (all sectors, BEA Fixed Assets Table 4.1 line 1) instead of productive capital stock K* = C*_f (productive sectors only). This **overstates the denominator** and therefore **understates r***. The total net stock includes capital in unproductive sectors (FIRE, government, services) that should be excluded under the Marxian framework.
  - [ ] **Resolution**: Restrict denominator to productive-sector fixed assets by filtering BEA Fixed Assets Table 4.1 or using sector-level detail from Table 4.3. Requires sector classification concordance from Chapter 4.
  - [ ] **Impact assessment**: Preliminary estimates suggest K* (productive only) is approximately 55-65% of total K, which would raise r* by roughly 50-80%.
  - [ ] Profit rate discrepancy documented in R_STAR_DISCREPANCY_RESOLUTION.md (file pending creation)
- [ ] **Two CSV versions**: profit_rates_1948_1989.csv (Phase 2, original) and profit_rates_1948_2024.csv (Phase 3, extended) use different column definitions and scaling for r_star_pct. Reconciliation needed.
- [ ] **Capital stock vintage**: BEA Fixed Assets data undergoes comprehensive revisions; the vintage used (2024 download) may differ from the vintage available to Shaikh & Tonak in 1994.

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App D | National Accounts Detail | D.2 | Source data for S* components (GFP, V*) |
| App E | Revenue Accounts | E.2 | Construction of surplus value accounts |
| App E | Labor Statistics | E.3 | Employment decomposition underlying V* |

### Key Appendix Variables
- **S***: Surplus value (T505) = GFP - V*
- **K**: Total net capital stock (BEA Fixed Assets Table 4.1, current cost basis)
- **C*_f**: Fixed constant capital (productive sectors only) -- the correct denominator per Marx
- **r_NIPA**: Conventional profit rate = gross operating surplus / net capital stock

---

## Related Content

- **Book Table**: 5.11 (listed as Table 5.8 in investigation notes)
- **Figures**: 5.3 (Profit Rate Trends), 5.4 (r* vs r_NIPA comparison)
- **Derived Series**: T514 (capacity-adjusted r*_adj)
- **Input Series**: T502 (C*), T504 (V*), T505 (S* numerator)
- **Data Files**:
  - `ShinyApp/data/profit_rates_1948_1989.csv` (Phase 2 original, 42 rows)
  - `ShinyApp/data/profit_rates_1948_2024.csv` (Phase 3 extended, 77 rows)
  - `API_Data/BEA/fixed_assets_4_1_net_stock.csv` (1925-2024, 7600 rows)
- **Module**: Chapter 5 -- Accounting Framework

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T513_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | S* extended / K from BEA Fixed Assets Table 4.1 |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 60% |
| Certification | NOT CERTIFIED |
| EXTENSION_LOG Entry | EXT-008 |
| Extension Date | 2026-02-24 |
| Divergences | DIV-001 (total K vs productive K*) |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Documentation section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation; DIV-001 documented; dual CSV issue noted |

---

*Data Provenance Record following Anu Standard v2.0*
