# Chapter 5 Data Interpolation Methodology

## Overview

Chapter 5 revenue-side accounts (T501-T503) require annual data from 1948 to 2024. The primary book source (Table E.2) covers 1948-1961, while BEA API data (NIPA tables) provides 1929-present for some series and 1998-present for industry-level detail. This document describes the interpolation strategy for bridging gaps.

---

## Data Coverage Map

| Source | Period | Series Covered | Resolution |
|--------|--------|---------------|------------|
| Book Table E.2 | 1948-1961 | T501-T509 (all revenue-side) | Annual |
| Authoritative CSV (benchmarks) | 1948, 1958, 1967, 1977, 1989 | T501-T509 | Benchmark years only |
| NIPA 1.7.5 (Gross Output) | 1929-2025 | T501 (TP*) | Annual, all industries |
| NIPA 6.2D (Compensation) | 1998-2024 | T504 (V*) | Annual, by industry |
| NIPA 6.4D (Employment FT/PT) | 1998-2024 | T511, T515, T516 | Annual, by industry |
| NIPA 6.5D (Employment FTE) | 1998-2024 | T511, T515, T516 | Annual, by industry |
| NIPA 6.10D (Employer Contributions) | 1998-2024 | T504, T512 | Annual, by industry |
| BLS CES | 1948-2024 | T515, T516 | Annual |
| FRED TCU | 1967-2025 | T514 | Annual |
| BEA Fixed Assets 4.1 | 1925-2024 | T513, T514 | Annual |

---

## Gap: 1962-1989 Revenue-Side Accounts

### Problem Statement

Table E.2 provides annual data for T501-T509 from 1948-1961. For 1962-1989, only IO benchmark years (1967, 1972, 1977, 1982, 1987) are available from the authoritative CSV. Post-1997, NIPA annual tables provide all needed series.

This creates a gap for **1962-1996** where annual data must be interpolated or estimated.

### Available Anchor Points

| Year | Source | Available Series |
|------|--------|-----------------|
| 1948 | Book Table E.2 / Authoritative CSV | All T501-T509 |
| 1958 | Book Table E.2 / Authoritative CSV | All T501-T509 |
| 1961 | Book Table E.2 (last year) | All T501-T509 |
| 1967 | IO Benchmark / Authoritative CSV | T501-T503 (via IO tables) |
| 1972 | IO Benchmark | T501-T503 |
| 1977 | IO Benchmark / Authoritative CSV | T501-T503 |
| 1982 | IO Benchmark | T501-T503 |
| 1987 | IO Benchmark | T501-T503 |
| 1989 | Authoritative CSV / Book Table 5.7 | All T501-T516 |
| 1998+ | NIPA API | T501-T505 (annual) |

### Interpolation Strategy

1. **TP* (T501)**: NIPA 1.7.5 provides gross output by industry from 1929-present. Apply productive-sector shares from IO benchmark years, interpolating shares linearly between benchmarks.

2. **C*_m (T502)**: IO benchmark tables provide intermediate input totals at benchmark years. Interpolate using NIPA gross output growth rates as proxy between benchmarks.

3. **VA* (T503)**: Derive from T501 - T502 after both are interpolated. Cross-validate against NIPA GDP by industry.

4. **V* (T504)**: Already extended independently via NIPA compensation data and T512 ratios (Wave 1, EXT-005).

5. **S* (T505)**: Already extended as VA* - V* (Wave 1, EXT-006). Note: extension uses approximation since VA* requires T503 which depends on IO data.

6. **Exploitation-derived (T506-T507)**: Already extended via Wave 1 methodology.

7. **Revenue adjustments (T508-T509)**: Require IO sector classification. Deferred to Wave 2.

### Quality Assessment

| Period | Method | Expected Accuracy |
|--------|--------|-------------------|
| 1948-1961 | Direct from book (Table E.2) | HIGH — primary source |
| 1962-1966 | Linear interpolation (1961→1967) | MEDIUM — short gap, stable economy |
| 1967-1989 | IO benchmark interpolation | MEDIUM-HIGH — benchmarks every 5 years |
| 1990-1997 | Backward extrapolation from 1998 | MEDIUM — structural break possible |
| 1998-2024 | NIPA annual data | HIGH — direct API source |

---

## NIPA 6.10B Note

NIPA Table 6.10B (Employment by Industry, FTE basis) has been added to the BEA fetch script (`pull_bea_nipa_ch05.py`) for cross-validation of employment decomposition. If the BEA API does not serve this table, the gap is documented here.

**Status**: Fetch script updated; execution pending. BLS CES data (1948-2024) serves as primary employment source for T515/T516 extensions.

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-25 | 1.0 | Initial creation (Session 8 — G008 partial resolution) |

---

*Interpolation Methodology following Anu Standard v2.0*
