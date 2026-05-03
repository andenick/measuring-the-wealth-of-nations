# IO Methodology Extraction from HDARP Book Chunks
## Source: Shaikh & Tonak (1994) — Chapters 4-5, Appendices A-G

**Extracted**: 2026-04-08 from HDARP_Extractions/1994_Measuring_Wealth/ chunks 09-16, 27, 32-33
**Purpose**: Complete reference for Wave 2 IO framework implementation

---

## Core Formulas

### Labor Value Computation
```
λ* = hp* · (I - app*)^(-1)
```
Where:
- λ* = labor-value/producer-price ratios (hours per dollar)
- hp*j = hpj/pj (labor hours per dollar of producer-price output)
- app*ij = pi·appij/pj (producer-price IO coefficient matrix)

### Critical Principle (p.81)
Labor values apply ONLY to producer-price components:
```
C = λ* · (Mp)p        [NOT λ* · (Mp)]
V = λ* · (CONWp)p     [NOT λ* · (CONWp)]
```
Money values include both producer price AND trading margin:
```
C* = (Mp)p + (Mp)t
V* = (CONWp)p + (CONWp)t
```

### Variable Capital
```
V*j = (ecp)j × (Lp)j    [per sector]
V* = ΣV*j               [aggregate]
```
Where:
- (ecp)j = wpj × xj (BLS production worker wage × EC/WS supplement ratio)
- (Lp)j = (Lp/L)'j × Lj (BLS production ratio × NIPA total employment)

### Exploitation Rate
```
S*/V* = (VA* - V*) / V*
```
Book values: 1.70 (1948) → 2.44 (1989), +43%

### Value Composition
```
C*/V* = (M'p + Dp) / V*
```
Book values: 2.35 (1948) → 2.89 (1989), +23%

---

## 82×88 Sectoral Structure

| Row | Sectors | Classification |
|-----|---------|---------------|
| 1 Production | 1-64 + 68 + 70-75 | Productive |
| 2 Total Trade | 65 + (1-g)×67 | Trading |
| 3 Royalties | 66 + g×67 + 69 | Unproductive |
| 4 Household Industry | 79 | Noncapitalist |
| 5 Combined Dummy | 80 + 81 | Accounting |
| 6 Row Total | 82 | — |

g = ground rent proportion of building/equipment rental (0.25 benchmark)

---

## Productive Labor Classification (Appendix F)

| Sector | Lp Source | Production Ratio Source |
|--------|----------|----------------------|
| Manufacturing | BLS CES | 0.733 (1972) |
| Mining | BLS CES | 0.732 |
| Construction | BLS CES | 0.725 |
| Transport/Utilities | BLS CES | 0.870 |
| Agriculture | Mining proxy | 0.732 |
| Services | GNP-weighted | 0.668 × (GNPpr/GNP)serv |
| Govt Enterprises | Private average | (Lp/L)nongovtot |
| Trade | ALL unproductive | 0.0 |
| FIRE | ALL unproductive | 0.0 |
| Government | ALL unproductive | 0.0 |

### Key Finding: ec_u/ec_p Stability
- 1948: 1.13, 1989: 1.00 (range 0.96-1.14)
- V*/W decline (34%) driven almost entirely by Lp/L decline (37%), NOT wage differentials

---

## Interpolation Between Benchmark IO Years

**Method** (Section 5.2, p.96):
1. Compute ratios in each IO year: xp = (M'p/GVAp)_IO
2. Linearly interpolate ratios between benchmarks
3. Apply: (M'p)_annual = xp_interpolated × (GVAp)_NIPA

**Components interpolated**: M'p, RYp, M'tt, RYtt
**Components taken directly from NIPA**: GVAp, GVAtt, Dp, all final use items

---

## NIPA Table References

| Marxian Category | NIPA Series | Detail |
|-----------------|-------------|--------|
| Employee Compensation by sector | 604B | Lines 13(mfg), 7(mining), 12(const), 37(trans), 60(services), 4(agr), 81/86(govt ent), 50/51(trade), 52/58(FIRE), 78/83(govt) |
| FTE Employment | 607B | Same sector breakdown |
| Total Employment (PEP) | 610B | FEE + Self-Employed |
| Consumption detail | Table 2.4 line 4 | Eating/drinking services |
| Government | Tables 3.1-3.3 | Receipts and expenditures |
| Personal income | Table 2.1 | For worker share computation |
| GDP by industry | Table 1.7.5 | Gross output by industry |

---

## Data Source Requirements for Wave 2

### Already Available (1947-1977)
- 6 benchmark IO tables (A, L, Z matrices, 85×85)
- Concordance (85 IO → 13 NIPA)
- Employment data (Mohun comparison)

### Needed for Extension
- **Post-1977 IO benchmarks**: 1982, 1987, 1992 (SIC), 1997 (bridge), 2002-2017 (NAICS)
- **NAICS concordance**: Map ~71 NAICS industries → 85 SIC sectors
- **Modern BLS CES**: Production worker ratios by NAICS industry
- **BEA Fixed Assets**: Industry-level capital stock for K* restriction (DIV-001)

---

*Extracted from HDARP book chunks for ST2 Wave 2 implementation. See HDARP_BOOK_INDEX.md for chunk navigation.*
