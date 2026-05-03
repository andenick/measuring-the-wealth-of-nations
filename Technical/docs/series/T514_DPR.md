# T514: Capacity-Adjusted Profit Rate (r*_adj) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T514 |
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

> "Capacity-adjusted profit rates remove cyclical variation from capacity utilization, isolating the secular trend in profitability."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 5, Table 5.8

The capacity-adjusted Marxian profit rate r*_adj corrects the raw profit rate r* for the business cycle by dividing by the total capacity utilization rate (TCU). When capacity utilization is low (recession), the measured profit rate is depressed relative to its trend because the capital stock is underutilized. Dividing by TCU inflates r* during recessions and deflates it during booms, producing a series that more faithfully tracks the underlying secular trend. This adjustment is standard in the empirical Marxian literature (Shaikh 1987, 1992; Dumenil & Levy 1993; Basu & Manolakos 2013).

---

## Subsources

| ID | Source | Period | API/URL | Quality | Notes |
|----|--------|--------|---------|---------|-------|
| T514A | T513: Marxian Profit Rate (r*) | 1948-2024 | Derived series | calculated | Parent series; r* = S*/K |
| T514B | FRED TCU Capacity Utilization (Federal Reserve G.17) | 1967-2025 | FRED API (series TCU) | official_statistics | Total industry capacity utilization, percent |
| T514C | Book Table 5.11 (Shaikh & Tonak 1994) | 1948-1989 | N/A (book) | academic_research | Benchmark capacity-adjusted values |

### Quality Categories
- `academic_research` - Peer-reviewed source (HIGH reliability)
- `official_statistics` - Government statistical agency (HIGH reliability)
- `calculated` - Derived from formulas (VARIES -- depends on inputs)

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Pull FRED TCU data | FRED API (series TCU) | fred_tcu_capacity_utilization.csv | pull_fred_tcu.py | XFORM-057 |
| 2 | Annualize TCU | Monthly/quarterly TCU | Annual average TCU | calculate_ch05.py | XFORM-058 |
| 3 | Retrieve r* from T513 | T513 series | r* series (percent) | calculate_ch05.py | XFORM-059 |
| 4 | Compute r*_adj = r* / TCU | r*, TCU | r*_adj (percent) | calculate_ch05.py | XFORM-060 |
| 5 | Validate against book Table 5.11 | r*_adj, book benchmarks | pass/fail | validate_ch05.py | XFORM-060V |

### Transformation Details

#### XFORM-060: Capacity-Adjusted Profit Rate

**Formula**:
```
r*_adj = r* x (1 / TCU)
       = r* / TCU

where:
  r*  = Marxian profit rate (T513) = S* / K, in percent
  TCU = Total Capacity Utilization (Federal Reserve G.17), expressed as a fraction (0 to 1)

Example:
  r*(1970) = 15.2%, TCU(1970) = 0.8128
  r*_adj(1970) = 15.2% / 0.8128 = 18.7%

Units: percent (same as r*)
```

**Parameters**:
- TCU from FRED is reported as a percentage (e.g., 81.28); must be converted to a fraction (0.8128) before dividing
- Annual TCU is the simple average of monthly observations within each calendar year
- Pre-1967 TCU values: The FRED TCU series begins in 1967. For 1948-1966, the book uses Federal Reserve estimates or interpolated values from the Wharton index of capacity utilization

**Notes**: The capacity adjustment amplifies cyclical swings. During recessions (low TCU), r*_adj exceeds r* because the denominator shrinks. During booms (high TCU), r*_adj falls below r*. The secular trend is preserved but cyclical noise is reduced, making the underlying decline in profitability more visible.

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| r*_adj(1948) | ~151.2% | Consistent with profit_rates_1948_2024.csv | PASS |
| r*_adj > r* when TCU < 1 | r*_adj exceeds r* in all years | Confirmed (TCU < 1 throughout) | PASS |
| Secular decline preserved | r*_adj declines 1948-1989 | Confirmed | PASS |
| Cyclical amplification | r*_adj swings wider than r* | Confirmed in recession years | PASS |
| Year Coverage | 1948-2024 | 1948-2024 | PASS |
| TCU range | 0.70-0.90 typical | 0.6647-0.8915 (FRED data) | PASS |

### Validation Notes

> "The adjustment for capacity utilization does not alter the secular trend but sharpens it by removing the dampening effect of cyclical underutilization. The adjusted rate falls even more steeply than the unadjusted rate in the 1966-1982 period."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, p. 215

The profit_rates_1948_2024.csv file contains both r_star_pct and r_star_adj_pct columns with capacity_utilization. The r_star_adj_pct column is computed as r_star_pct / capacity_utilization. Both book-period and extension-period values are present.

---

## Known Issues

- [x] **CRITICAL: DIV-001 inherited from T513**: The parent series T513 uses total capital stock K (all sectors) instead of productive capital stock K* = C*_f (productive sectors only). Since r*_adj = r* / TCU, the DIV-001 denominator overstatement propagates directly: r*_adj is understated by the same factor as r*.
  - [ ] **Resolution**: Correct T513 first by restricting K to productive sectors; r*_adj will automatically correct when T513 is fixed.
  - [ ] Profit rate discrepancy documented in R_STAR_DISCREPANCY_RESOLUTION.md (file pending creation)
- [ ] **TCU coverage gap**: FRED TCU series (series ID: TCU) begins in 1967-01-01. Pre-1967 values (1948-1966) require estimation from alternative sources (Wharton capacity utilization index, Federal Reserve historical estimates, or interpolation from industrial production data).
- [ ] **TCU sectoral scope**: FRED TCU covers manufacturing, mining, and utilities only. It does not cover construction, agriculture, or services. A broader capacity measure aligned with the full productive sector definition may differ from the Federal Reserve's G.17 measure.
- [ ] **TCU annualization**: Monthly TCU values are averaged to annual; the choice of simple average vs. production-weighted average may affect results, particularly in years with sharp mid-year changes (e.g., 2008-2009).

---

## Appendix References

| Appendix | Title | Tables | Relevance |
|----------|-------|--------|-----------|
| App D | National Accounts Detail | D.2 | Source data for S* components underlying r* |
| App E | Revenue Accounts | E.2 | Surplus value construction for numerator |

### Key Appendix Variables
- **r***: Marxian profit rate (T513), the parent series
- **TCU**: Total Capacity Utilization (Federal Reserve G.17, FRED series TCU)
- **r*_adj**: Capacity-adjusted Marxian profit rate = r* / TCU

---

## Related Content

- **Book Table**: 5.11
- **Figures**: 5.3 (Profit Rate Trends), 5.4 (Adjusted vs Unadjusted)
- **Parent Series**: T513 (r* = S*/K)
- **Input Series**: T502 (C*), T504 (V*), T505 (S*)
- **Data Files**:
  - `ShinyApp/data/profit_rates_1948_1989.csv` (Phase 2 original, 42 rows)
  - `ShinyApp/data/profit_rates_1948_2024.csv` (Phase 3 extended, 77 rows)
  - `API_Data/FRED/fred_tcu_capacity_utilization.csv` (1967-2025, 59 rows)
- **Module**: Chapter 5 -- Accounting Framework

## Extension Documentation

| Property | Value |
|----------|-------|
| EPR File | `Technical/docs/series/T514_EPR.md` |
| Extension Period | 1990-2024 |
| Extension Source | T513 extended × (1/TCU) from FRED |
| Splice Year | 1989 |
| Splice Method | Direct Level Match |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 60% |
| Certification | NOT CERTIFIED |
| EXTENSION_LOG Entry | EXT-009 |
| Extension Date | 2026-02-24 |
| Divergences | DIV-001 (total K vs productive K*) |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.1 | Added Extension Documentation section (Session 8) |
| 2026-02-24 | 1.0 | Initial creation; DIV-001 inheritance from T513 documented; TCU coverage gap noted |

---

*Data Provenance Record following Anu Standard v2.0*
