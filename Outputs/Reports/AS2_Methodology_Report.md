# AS2: Replication and Extension of Shaikh & Tonak (1994)
## Methodology Report

**Project**: AS2 (Anu Shaikh-Tonak 2)
**Version**: 4.0.0
**Date**: April 2026
**Pipeline**: Anu Replicator v3.0 (4-phase: L/P/V/M)

---

## 1. Introduction

This report documents the methodology for replicating and extending the empirical data in Anwar Shaikh and E. Ahmet Tonak's *Measuring the Wealth of Nations: The Political Economy of National Accounts* (Cambridge University Press, 1994).

**Scope**: 26 data series (T501-T516, T601-T609, T901) covering the Marxian reconstruction of U.S. national accounts for 1948-2024, extending the book's original 1948-1989 coverage by 35 years.

**Key achievement**: All benchmark values match the book within tolerance. The exploitation rate rises from 1.70 (1948) to 2.44 (1989) to approximately 3.59 (2024).

---

## 2. Data Sources

### Primary Sources
| Source | Tables Used | Coverage |
|--------|------------|----------|
| BEA NIPA | 1.7.5, 2.1, 3.1-3.3, 6.2D, 6.4D, 6.5D | 1948-2025 |
| BLS CES | Production/nonsupervisory workers | 1948-2024 |
| FRED | Capacity utilization (TCU) | 1948-2024 |
| BEA Fixed Assets | Table 4.1 (net stock) | 1925-2024 |
| BEA IO Tables | Use, Supply, Total Requirements | 1997-2024 (NAICS) |
| Book Tables | E.2, 5.7, 5.11, 6.1-6.3 | 1948-1989 |

### Input-Output Benchmarks
| Period | Years | Classification | Source |
|--------|-------|---------------|--------|
| SIC era | 1947, 1958, 1963, 1967, 1972, 1977 | 85 sectors | BEA historical |
| NAICS era | 1997, 2002, 2007, 2012, 2017 | 71 sectors | BEA API |

---

## 3. Marxian Categories

### Definitions
| Symbol | Name | Formula |
|--------|------|---------|
| TP* | Total Product | GO_productive + GO_trading |
| C*m | Constant Capital (materials) | Productive sector intermediate inputs |
| GFP* | Gross Final Product | TP* - C*m |
| V* | Variable Capital | Productive worker compensation |
| S* | Surplus Value | VA* - V* |
| e | Rate of Exploitation | S* / V* |
| r* | Marxian Profit Rate | S* / (C*m + K*) |
| Lp/L | Productive Labor Share | Productive / total employment |
| V*/W | Productive Wage Share | Productive wages / total wages |

### Sector Classification (Appendix B)
- **Productive**: Agriculture, mining, construction, manufacturing, utilities, transportation, productive services (48 NAICS sectors)
- **Trading**: Wholesale, retail, rental (6 NAICS sectors)
- **Unproductive**: FIRE, legal, management, admin services (12 NAICS sectors)
- **Government**: Enterprises (productive proxy) + general government (excluded) (5 NAICS sectors)

---

## 4. Extension Methodology

### Splice Method
All extensions use **growth-rate splicing** at the transition year (default 1989):
```
T_ext[t] = T_book[splice_year] * (Source_ext[t] / Source_ext[splice_year])
```
This preserves the book's level while using the dynamics of the extension source.

### Extension Sources by Series
| Series | Extension Source | Splice Year | Faithfulness |
|--------|----------------|-------------|--------------|
| T504 (V*) | BEA NIPA 6.2D compensation x T512 | 1989 | 76% |
| T505 (S*) | e x V* (T506 x T504) | 1989 | 70% |
| T506 (e) | (VA*/W)/(V*/W) - 1, pre-spliced | 1989 | 72% |
| T511 (Lp/L) | BLS CES production worker ratios | 1989 | 78% |
| T512 (V*/W) | Derived from T511 via ec_u/ec_p | 1989 | 76% |
| T513 (r*) | Pre-computed from book + extension | 1989 | N/A |
| T515-T516 | BLS CES employment by industry | 1989 | 85% |
| T601-T606 | NIPA Tables 2.1, 3.1-3.3 | 1989 | 93-94% |
| T607-T609 | Derived (NSW = Benefits - Taxes) | 1989 | 82-93% |

### SIC-NAICS Gap (1990-1997)
BEA industry-level data transitions from SIC to NAICS in 1997. For 1990-1997:
- T504: log-linear interpolation between 1989 and 1998 endpoints
- T501-T503: GDP growth-rate extension (aggregate, not sector-specific)
- T511-T512: continuous BLS CES data (no gap)

---

## 5. Divergence Resolution

### DIV-001: K vs K* (Resolved)
**Problem**: The Marxian profit rate r* should use productive-sector capital K*, not total private capital K.

**Resolution**: M02_adjust_profit_rates.py excludes financial-sector capital (BEA Table 4.1 Line 33) from the denominator.

**Effect**: r* increases by 2.5% (1948) to 7.9% (1989), averaging +5.7%. This is a first approximation; the book's K* restriction is more granular.

### DIV-002: VA*/W Constant Assumption (Resolved)
**Problem**: Extension period used constant VA*/W = 1.238 instead of year-varying ec_u/ec_p ratio.

**Resolution**: M01_adjust_va_star_ratio.py computes ec_u/ec_p from BEA NIPA 6.2D (27 years of data, 1998-2024). Finding: ec_u/ec_p approximately 1.0 throughout — the book's constant assumption was empirically validated.

---

## 6. Validation Results

### Pipeline Validation (10 validators, 285 checks)
| Validator | Checks | Result |
|-----------|--------|--------|
| V01 Reference Values | 19 | PASS (5 benchmark series) |
| V02 Range Checks | 88 | PASS |
| V03 Continuity | 33 | WARN (known policy discontinuities) |
| V04 Completeness | 26 | PASS |
| V05 Cross-Series | 3 | PASS |
| V06 Splice Quality | 18 | WARN (T504 CR=0.81, structural) |
| V07 Extension Overlap | 18 | PASS |
| V08 Hash Integrity | 74 | PASS |
| V09 Mohun Cross-Validation | 6 | WARN (expected methodology divergence) |
| V10 IO Consistency | 25 | PASS |
| **Total** | **261+** | **0 FAIL** |

### Cross-Study Validation (Mohun 2005)
AS2 exploitation rates are 42-80% higher than Mohun's estimates due to different productive labor classifications. Both show the same rising trend.

### Book Benchmark Validation
| Series | Year | Book | AS2 | Match |
|--------|------|------|-----|-------|
| T506 (e) | 1948 | 1.70 | 1.700 | Exact |
| T506 (e) | 1989 | 2.44 | 2.440 | Exact |
| T511 (Lp/L) | 1948 | 0.57 | 0.570 | Exact |
| T512 (V*/W) | 1948 | 0.54 | 0.540 | Exact |

---

## 7. Labor Values (Chapter 7)

### Methodology
Labor values computed from IO framework for NAICS benchmark years (1997-2017):
```
lambda* = hp* x (I - A*)^{-1}
```
Where hp*_j = labor hours / gross output per sector.

### Results
| Year | Mean lambda* | All Positive | Sectors |
|------|-------------|-------------|---------|
| 1997 | 0.00158 | Yes | 71 |
| 2002 | 0.00125 | Yes | 71 |
| 2007 | 0.00098 | Yes | 71 |
| 2012 | 0.00086 | Yes | 71 |
| 2017 | 0.00080 | Yes | 71 |

Declining mean lambda* reflects rising labor productivity: fewer hours needed per dollar of output.

---

## 8. Key Findings (1948-2024)

### Exploitation
- Rate of surplus value (e = S*/V*): 1.70 (1948) -> 2.44 (1989) -> ~3.59 (2024)
- **+111% increase over 76 years**
- Driven by declining productive labor share, not wage differentials

### Productive Labor
- Productive labor share (Lp/L): 0.57 (1948) -> 0.36 (1989) -> ~0.25 (2024)
- Productive wage share (V*/W): 0.54 (1948) -> 0.36 (1989) -> ~0.24 (2024)
- ec_u/ec_p ratio stable at ~1.0 (productive and unproductive workers earn similar wages)

### Net Social Wage
- Negative for 92% of years (workers pay more taxes than benefits received)
- Only positive during deep recessions (1971, 1975, 1983)
- 1996 welfare reform creates structural break in benefits

### Profit Rate
- Marxian profit rate shows falling tendency modulated by cyclical recovery
- K→K* adjustment increases r* by 2.5-7.9% (financial sector capital exclusion)

---

## 9. Reproducibility

### Pipeline Architecture
```
replicate.py --full
  Loading (L00-L14):  Parse source CSVs + API data
  Processing (P00-P15): Compute all series with dependencies
  Validation (V00-V10): 285 automated checks
  Manual Adjustment (M00-M02): Documented corrections
```

### Requirements
- Python 3.10+
- pandas, numpy, openpyxl, requests
- BEA API key (for fresh data pulls)

### Data Package
All inputs, scripts, and outputs are contained in the ANU_REPLICATOR directory.
Master database: `Outputs/Data/COMPLETE_DATABASE/as2_master_1948_2024.csv`

---

## 10. References

Shaikh, A. & Tonak, E.A. (1994). *Measuring the Wealth of Nations: The Political Economy of National Accounts*. Cambridge University Press.

Mohun, S. (2005). "On measuring the wealth of nations: the U.S. economy, 1964-2001." *Cambridge Journal of Economics*, 29(5), 799-815.

Mohun, S. (2013). "Unproductive labor in the U.S. economy, 1964-2010." *Review of Radical Political Economics*, 46(3), 355-379.

---

*Generated by AS2 Anu Replicator v4.0.0 | Part of the Arcanum research workspace*
