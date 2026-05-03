# Fig_5_4: Value/Materialized Composition of Capital — Figure Provenance Record

## Anu Standard Compliance: v2.0

| Property | Value |
|----------|-------|
| Standard | Anu Standard v2.0 |
| Record Type | Figure Provenance Record (FPR) |
| Created | 2026-03-21 |

---

## Quick Reference

| Property | Value |
|----------|-------|
| Figure ID | Fig_5_4 |
| Chapter | 5 |
| Page | — |
| Title | Value/Materialized Composition of Capital |
| Type | time_series |
| is_empirical | true |
| Period | 1948-1989 |

---

## Description

Figure 5.4 traces the value composition of capital (VCC) and the materialized composition of capital over 1948-1989, drawing on the full set of Marxian aggregate accounts (T501-T505). The value composition of capital, defined as C*/V* (constant capital to variable capital), is the Marxian analogue of the capital-labor ratio but expressed in value terms. A rising composition of capital indicates increasing mechanization and capital-intensity in production, which in Marx's framework tends to exert downward pressure on the general rate of profit (the law of the tendential fall). This figure is central to evaluating whether the postwar US economy exhibited the rising organic composition that classical Marxian theory predicts.

---

## Data Sources

| Series | Name | Role in Figure |
|--------|------|---------------|
| T501 | Total Product (TP*) | Context for aggregate accounts |
| T502 | Constant Capital — Materials (C*_m) | Component of constant capital |
| T503 | Value Added (VA*) | Net product reference |
| T504 | Variable Capital (V*) | Denominator of VCC |
| T505 | Surplus Value (S*) | Numerator component via C* derivation |

---

## Data File

`Technical/ANU_REPLICATOR/data/final-data/figures/Fig_5_4.csv`

---

## Replication Notes

The value composition of capital is C*/V* where C* includes both materials (T502) and depreciation of fixed capital. The materialized composition uses stock measures of constant capital rather than flow measures. Reproduce by computing the ratio from the underlying T-series and plotting over time. Check whether the book uses flow-based or stock-based constant capital for each variant shown.

---

## Related

- **DPRs**: T501_DPR.md, T502_DPR.md, T503_DPR.md, T504_DPR.md, T505_DPR.md
- **Chapter Investigation**: CHAPTER_5_INVESTIGATION.md
- **Related Figures**: Fig_5_1 (definitions), Fig_5_5 (profit rate implications)

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-21 | 1.0 | Initial creation |

---

*Figure Provenance Record following Anu Standard v2.0*
