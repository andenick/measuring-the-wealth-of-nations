# T901: Summary Table (Key Indicators) - Data Provenance Record

## Anu Standard Compliance: v2.0

---

## Quick Reference

| Property | Value |
|----------|-------|
| Dataset ID | T901 |
| Type | derived |
| Time Period | 1948-1989 (book), 1948-2024 (extended) |
| Frequency | annual |
| Source Count | 0 (pure aggregator — all data from Ch5 + Ch6) |
| Base Year | N/A |
| Units | various (ratios, percentages, millions $) |
| Validation Status | PROVISIONAL |
| Last Updated | 2026-02-26 |

---

## Context

> "The theoretical difference between Marxian and orthodox economic analysis is reflected in a fundamentally different empirical picture of capitalist reality."
> -- Shaikh & Tonak, *Measuring the Wealth of Nations*, Chapter 9 (p. 240)

Chapter 9 is a pure summary chapter — it introduces no new data sources or calculations. T901 assembles the key indicators from Chapters 5 and 6 into a single reference table for cross-chapter comparison. This enables the book's concluding argument that Marxian categories reveal fundamentally different trends than orthodox measures.

---

## Subsources

| ID | Source Series | Chapter | Period | Notes |
|----|--------------|---------|--------|-------|
| T901A | T506 (e = S*/V*) | Ch 5, Table 5.7 | 1948-1989 | Rate of exploitation |
| T901B | T511 (Lp/L) | Ch 5, Table 5.7 | 1948-1989 | Productive labor share |
| T901C | T512 (V*/W) | Ch 5, Table 5.7 | 1948-1989 | Productive wage share |
| T901D | T513 (r* = S*/K) | Ch 5, Table 5.8 | 1948-1989 | Marxian profit rate |
| T901E | T514 (r*_adj) | Ch 5, Table 5.8 | 1948-1989 | Capacity-adjusted profit rate |
| T901F | T608 (NSW/V*) | Ch 6, Table 6.4 | 1952-1989 | Net social wage / variable capital |
| T901G | T501-T505 | Ch 5, Table 5.5 | 1948-1989 | Revenue accounts (TP*, C*, VA*, V*, S*) |

---

## Transformation Chain

| Step | Operation | Input | Output | Script | Transform ID |
|------|-----------|-------|--------|--------|--------------|
| 1 | Load Ch5 exploitation composition | exploitation_composition CSVs | T506, T511, T512 ratios | build_summary_table.py | XFORM-091 |
| 2 | Load Ch5 profit rates | profit_rates CSVs | T513, T514 rates | build_summary_table.py | XFORM-091 |
| 3 | Load Ch6 NSW ratios | nsw CSVs | T608 ratio | build_summary_table.py | XFORM-091 |
| 4 | Join on year | All loaded series | summary_indicators.csv | build_summary_table.py | XFORM-091 |

### Transformation Details

#### XFORM-091: Summary Table Assembly

**Formula**: No new calculations — pure join/assembly of existing series.

```
T901 = {
  year,
  T506: exploitation_rate (from Ch5),
  T511: Lp_L_ratio (from Ch5),
  T512: V_W_ratio (from Ch5),
  T513: r_star_pct (from Ch5),
  T514: r_star_adj_pct (from Ch5),
  T608: nsw_v_star_ratio (from Ch6)
}
```

---

## Validation Record

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| e(1948) | 1.70 | 1.70 | PASS |
| e(1989) | 2.44 | 2.44 | PASS |
| Lp/L(1948) | 0.57 | 0.57 | PASS |
| Lp/L(1989) | 0.36 | 0.36 | PASS |
| V*/W(1989) | 0.36 | 0.36 | PASS |
| NSW/V* sign | Predominantly negative | Negative 35/38 years | PASS (DIV-003) |
| Year coverage (book) | 1948-1989 | 1948-1989 | PASS |
| Year coverage (extended) | 1948-2024 | 1948-2024 | PASS |

### Benchmark Values (Book Table 9.1)

| Indicator | 1948 | 1958 | 1967 | 1977 | 1989 | Trend |
|-----------|------|------|------|------|------|-------|
| e = S*/V* | 1.70 | 1.83 | 2.10 | 2.10 | 2.44 | Rising (+44%) |
| Lp/L | 0.57 | 0.52 | 0.51 | 0.50 | 0.36 | Falling (-37%) |
| V*/W | 0.54 | 0.49 | 0.45 | 0.41 | 0.36 | Falling (-33%) |
| NSW/V* | — | — | — | — | <0 | Negative throughout |

---

## Known Issues

- [ ] **T608 post-1989 gap**: V* levels not yet computed for extended period, so T608 only available for 1952-1989
- [ ] **Chapters 7-8 not yet implemented**: Book Table 9.1 includes labor value and price composition data from Ch 7-8; these will be added in later waves
- [ ] **DIV-001 applies to T513/T514**: Profit rates use total K instead of productive K*

---

## Related Content

- **Figures**: 9.1-9.5 (summary charts)
- **Source Series**: T501-T516 (Ch5), T607-T608 (Ch6)
- **Module**: Chapter 9 — Summary of Results

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-26 | 1.0 | Initial creation (Session 10) |

---

*Data Provenance Record following Anu Standard v2.0*
