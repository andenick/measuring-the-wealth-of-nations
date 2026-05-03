# Fig_5_1: IO Accounts and Marxian Categories — Figure Provenance Record

## Anu Standard Compliance: v2.0

| Property | Value |
|----------|-------|
| Standard | Anu Standard v2.0 |
| Record Type | Figure Provenance Record (FPR) |
| Created | 2026-02-25 |
| Session | Session 8 — Score Elevation |

---

## Quick Reference

| Property | Value |
|----------|-------|
| Figure ID | Fig_5_1 |
| Chapter | 5 |
| Page | 110 |
| Title | IO Accounts and Marxian Categories |
| Type | Theoretical / Conceptual |
| is_empirical | false |
| Data Required | None (conceptual mapping) |

---

## Description

Figure 5.1 presents the conceptual mapping from standard Input-Output (IO) national accounts to Marxian economic categories. It shows how conventional IO categories (gross output, intermediate inputs, value added, compensation of employees, gross operating surplus) are reclassified into Marxian categories:

- **TP*** (Total Product) — productive-sector gross output
- **C*** (Constant Capital) — productive-sector intermediate inputs + depreciation
- **VA*** (Value Added) — TP* minus C*
- **V*** (Variable Capital) — productive-worker compensation
- **S*** (Surplus Value) — VA* minus V*

This is a **non-empirical figure** — it establishes the theoretical framework used throughout Chapter 5 rather than displaying time-series data.

---

## Source Material

| Property | Value |
|----------|-------|
| Book Reference | Shaikh & Tonak (1994), Chapter 5, p. 110 |
| Knowledge Base | `Knowledge_Base/figures/page_110_io_marxian_mapping.md` |
| HDARP Source | Page 110 extraction via density-aware chunking |
| Extraction Quality | HIGH — conceptual diagram, text-based mapping |

---

## IO-to-Marxian Category Mapping

| IO Category | Marxian Category | Series ID | Transformation |
|-------------|-----------------|-----------|----------------|
| Gross Output (productive sectors) | TP* (Total Product) | T501 | Sector classification via IO benchmarks |
| Intermediate Inputs (productive) | C*_m (Materials) | T502 | Productive-sector intermediate consumption |
| Value Added (productive) | VA* (Gross Final Product) | T503 | TP* - C*_m |
| Compensation of Employees (productive) | V* (Variable Capital) | T504 | Productive-worker wages + benefits |
| Gross Operating Surplus + mixed income | S* (Surplus Value) | T505 | VA* - V* |
| Employment (production workers) | Lp (Productive Labor) | T515 | BLS CES production/nonsupervisory |
| Employment (nonproduction workers) | Lu (Unproductive Labor) | T516 | L - Lp residual |

---

## Catalog Reference

| Property | Value |
|----------|-------|
| FIGURE_SERIES_CATALOG Entry | Fig_5_1 |
| is_empirical | false |
| series_ids | T501, T502, T503, T504, T505 |
| chart_type | conceptual_mapping |
| Related Figures | Fig 5.2 (exploitation rate), Fig 5.3 (profit rate) |

---

## Reproduction Notes

This figure is a **conceptual diagram** and does not require data reproduction. The mapping it describes is implemented computationally in:

- `ShinyApp/R/data_loader.R` — CH5_SERIES_MAPPING metadata
- `ShinyApp/R/chart_builder.R` — build_revenue_chart() for T501-T505
- Transformation chain documented in T501_DPR.md through T505_DPR.md

The IO benchmark tables underlying the productive/unproductive sector classification are documented in:
- `Knowledge_Base/chapters/ch05_accounting_framework.md`
- Appendix D (IO classifications) and Appendix E (data tables)

---

## Gap Resolution

| Property | Value |
|----------|-------|
| Gap ID | G011 |
| Gap Description | Figure 5.1 needs FPR not DPR |
| Resolution | Created this FPR with conceptual mapping documentation |
| Resolution Date | 2026-02-25 |
| Session | Session 8 |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation (Session 8 — G011 resolution) |

---

*Figure Provenance Record following Anu Standard v2.0*
