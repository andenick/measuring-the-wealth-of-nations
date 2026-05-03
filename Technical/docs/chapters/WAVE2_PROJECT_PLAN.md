# Wave 2 Project Plan — IO-Dependent Series Extension

## Overview

Wave 2 extends 7 book-period-only series (T501-T503, T507-T510) from 1948-1989 to 1948-2024 using Input-Output benchmark methodology from Chapter 4.

These series require IO benchmark tables for productive/unproductive sector classification, which cannot be constructed until Chapter 4's IO framework is complete.

---

## Series Priority Order

Extensions should proceed in dependency order:

| Priority | Series | Name | Dependency | Rationale |
|----------|--------|------|------------|-----------|
| 1 | T501 | Total Product (TP*) | IO benchmarks → productive-sector gross output | Foundation series; all others depend on TP* |
| 2 | T502 | Constant Capital — Materials (C*_m) | IO benchmarks → productive-sector intermediate inputs | Required for C* and VA* |
| 3 | T503 | Value Added (VA*) | T501, T502 | Derived: VA* = TP* - C*_m |
| 4 | T507 | Surplus Ratio (S*/Y) | T504, T505 (already extended) + IO validation | Derivable once IO validation complete |
| 5 | T510 | Value Composition (C*/V*) | T502, T504 (already extended) | Requires C* from T502 extension |
| 6 | T508 | Productive Consumption (CON*) | IO sector classification for consumption components | Revenue-side adjustment |
| 7 | T509 | Productive Investment (IG*) | IO sector classification for investment components | Revenue-side adjustment |

---

## Dependencies

### Chapter 4 Prerequisites
- IO benchmark tables for years: 1947, 1958, 1963, 1967, 1972, 1977, 1982, 1987, 1992, 1997, 2002, 2007, 2012, 2017
- SIC-NAICS concordance (already created: `concordance/SIC_NAICS_concordance.csv`)
- Productive/unproductive sector classification rules
- BEA IO Use Tables (annual, post-1997)

### Wave 1 Inputs Available
- T504 (V*) — extended to 2024 (EXT-005)
- T505 (S*) — extended to 2024 (EXT-006)
- T506 (e) — extended to 2024 (EXT-007)
- T511 (Lp/L) — extended to 2024 (EXT-001)
- T512 (V*/W) — extended to 2024 (EXT-002)
- T513 (r*) — extended to 2024 (EXT-008)
- T514 (r* adj) — extended to 2024 (EXT-009)
- T515 (Lp) — extended to 2024 (EXT-003)
- T516 (Lu) — extended to 2024 (EXT-004)

---

## SIC-NAICS Transition Complexity

The most significant methodological challenge for Wave 2 is the SIC-to-NAICS transition (1997):

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Sector reclassification | Services sectors reorganized; FIRE split into Finance and Real Estate | Use concordance table with probability weights |
| IO table format changes | Pre-1997: SIC-based benchmarks; post-1997: NAICS annual tables | Bridge using 1997 dual-coded year |
| Productive/unproductive boundary | Some borderline sectors reclassified | Document boundary decisions in DPRs |
| Data frequency | Pre-1997: benchmark years only (5-year gaps); post-1997: annual | Interpolation for inter-benchmark years |

---

## Estimated Scope

| Metric | Value |
|--------|-------|
| Series to extend | 7 (T501-T503, T507-T510) |
| IO benchmark tables needed | 14 (1947-2017) |
| New DPR updates required | 7 |
| New EPR files required | 7 |
| Key methodology documents | IO sector classification rules, interpolation methodology |
| Predecessor chapter | Chapter 4 (IO Framework) |

---

## Gap Resolution

| Property | Value |
|----------|-------|
| Gap ID | G014 |
| Gap Description | Book-period-only series extension timeline undefined |
| Resolution | Created this Wave 2 Project Plan with dependency analysis |
| Resolution Date | 2026-02-25 |
| Session | Session 8 |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation (Session 8 — G014 resolution) |

---

*Wave 2 Project Plan following Anu Standard v2.0*
