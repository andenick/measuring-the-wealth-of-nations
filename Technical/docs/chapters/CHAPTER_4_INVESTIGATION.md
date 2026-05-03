# Chapter 4 Investigation: The Input-Output Framework

## Quick Reference

| Property | Value |
|----------|-------|
| Chapter | 4 — Marxian Categories in Input-Output Terms |
| Book Pages | pp.67-94 |
| Series | T401 (A-matrix), T402 (Leontief inverse B) |
| Wave | Wave 2 (prerequisite for all Wave 2 series) |
| Status | IN PROGRESS — infrastructure built, narrative documentation needed |
| Key Figures | Fig 4.1 (condensed form), Fig 4.2 (numerical example), Fig 4.3 (IO coefficients) |

---

## Chapter Summary

Chapter 4 establishes the mathematical framework for computing Marxian economic categories from standard Input-Output tables. It is the **methodological bridge** between the theoretical categories defined in Chapters 2-3 and the empirical measures computed in Chapters 5-9.

### Core Problem

Standard national accounts (BEA IO tables) report data in **money/producer prices**. Marxian categories require data in **labor values**. Chapter 4 shows how to transform one into the other using the IO table structure.

### Key Relationships

**Ideal case** (quantity IO tables):
```
lambda = hp * (I - app)^{-1}
```
Where:
- `lambda` = row vector of unit labor values
- `hp` = row vector of direct labor hours per unit output
- `app` = IO coefficients matrix (productive sectors only)

**Actual case** (money IO tables at producer prices):
```
lambda* = hp* * (I - app*)^{-1}
```
Where:
- `lambda*` = labor-value / producer-price ratios
- `hp*` = labor coefficients in price terms (hpj / pj)
- `app*` = money-value IO coefficients (pi * appij / pj)

### Critical Principle (p.81)

> "Since the lambda*s are ratios of labor values to producer prices, we must be careful to apply them only to the producer-price components of commodity flows."

This means:
- **Labor value of C**: multiply only producer-price component of inputs by lambda*
- **Money value of C***: use full purchaser prices (producer + trading margin)
- **Labor value of V**: multiply producer-price component of worker consumption by lambda*
- **Money value of V***: use full purchaser prices of worker consumption

---

## Sector Classification

### The Productive/Unproductive/Trading Taxonomy

Shaikh & Tonak classify all IO sectors into three categories:

| Category | Definition | Examples | Count (85-sector) |
|----------|-----------|----------|-------------------|
| **Productive** | Sectors producing material use-values | Agriculture, Mining, Manufacturing, Construction, Transportation (productive portion) | 75 |
| **Unproductive** | Sectors not producing material use-values | FIRE, Real Estate, Legal, Government, Business Services | 7 |
| **Trading** | Sectors involved in circulation/exchange | Wholesale Trade, Retail Trade | 3 |

### Classification in ST2

The classification is implemented in `Inputs/Concordances/io_85_to_nipa_13_concordance.csv`:
- 85 IO sectors mapped to 13 NIPA industries
- Each sector labeled as "productive", "unproductive", or "trading" (in `classification` column)
- Based on SIC codes (pre-1997) and NAICS codes (post-1997)

### Current Classification Results (from P13)

| Year | Productive | Unproductive | Trading | Total |
|------|-----------|--------------|---------|-------|
| 1947 | 75 | 7 | 3 | 85 |
| 1958 | 75 | 7 | 3 | 85 |
| 1963 | 75 | 7 | 3 | 85 |
| 1967 | 75 | 7 | 3 | 85 |
| 1972 | 75 | 7 | 3 | 85 |
| 1977 | 75 | 7 | 3 | 85 |

---

## IO Table Structure (Figure 5.2, p.91)

The 8x11 summary IO table has the structure:

```
Rows: Production, Trading, Royalties sectors
Columns: Intermediate demand (by sector) + Final demand (CON, IG, X-IM, G)

Key aggregates:
  TV* = GOp + GOtt           (Total Value = productive + trading gross output)
  C*m = M'p                   (Constant capital = productive intermediate inputs, net of depreciation)
  GFP* = TV* - C*m            (Gross Final Product)
  GVA* = GFP* (for sectors)  (Gross Value Added, Marxian)
```

### Derivation Steps (p.91)

1. Create consistent 82x88 tables from BEA published benchmark IO tables
2. Adjust for industry classification and secondary products
3. Ensure imports are comparable across years
4. Aggregate to 8x11 summary following Figure 5.1 structure

---

## Data Availability

### Currently Available (SIC era, 1947-1977)

| Year | A-matrix | L-matrix (Leontief) | Z-matrix (Transactions) | Source |
|------|----------|---------------------|------------------------|--------|
| 1947 | 85x85 | 85x85 | 85x85 | BEA benchmark |
| 1958 | 85x85 | 85x85 | 85x85 | BEA benchmark |
| 1963 | 85x85 | 85x85 | 85x85 | BEA benchmark |
| 1967 | 85x85 | 85x85 | 85x85 | BEA benchmark |
| 1972 | 85x85 | 85x85 | 85x85 | BEA benchmark |
| 1977 | 85x85 | 85x85 | 85x85 | BEA benchmark |

All located in `Inputs/IO_Matrices/`.

### Needed for Wave 2 Extension (1982-2017)

| Year | SIC/NAICS | Status | Source |
|------|-----------|--------|--------|
| 1982 | SIC | NOT AVAILABLE | BEA benchmark (if obtainable) |
| 1987 | SIC | NOT AVAILABLE | BEA benchmark (if obtainable) |
| 1992 | SIC | NOT AVAILABLE | BEA benchmark (last SIC year) |
| 1997 | NAICS (dual-coded) | NOT AVAILABLE | BEA benchmark (bridge year) |
| 2002 | NAICS | NOT AVAILABLE | BEA benchmark (available online) |
| 2007 | NAICS | NOT AVAILABLE | BEA benchmark (available online) |
| 2012 | NAICS | NOT AVAILABLE | BEA benchmark (available online) |
| 2017 | NAICS | NOT AVAILABLE | BEA benchmark (available online) |

### SIC-NAICS Transition Challenge

The 1997 transition from SIC to NAICS sector classification is the primary methodological challenge:
- Pre-1997: 85 SIC-based sectors
- Post-1997: Different sector count and classification
- Bridge: 1997 dual-coded year allows concordance
- Concordance exists: `io_85_to_nipa_13_concordance.csv` maps SIC-era IO sectors to NIPA industries
- For NAICS-era IO tables, a new concordance (NAICS IO sectors -> productive/unproductive) will be needed

---

## Existing Infrastructure

### Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `L11_load_io_matrices.py` | Load A, L matrices for benchmark years, label with concordance | WORKING |
| `L12_load_labor_values.py` | Compute hp* vectors from employment data | WORKING |
| `P13_process_io.py` | Validate matrices, classify sectors, write summaries | WORKING |
| `P14_process_labor_values.py` | Compute labor values v = l x B | WORKING |

### Library

| Module | Functions | Status |
|--------|-----------|--------|
| `io_transforms.py` | `compute_technical_coefficients()`, `compute_leontief_inverse()`, `compute_labor_values()`, `classify_sectors()`, `load_matrix_csv()`, `recover_gross_output()`, `distribute_employment()` | WORKING |

### Pipeline Output

P13 currently produces per-year summary statistics:
- Matrix dimensions and sparsity
- Maximum eigenvalue and condition number
- Leontief inverse validation
- Sector classification counts

---

## Wave 2 Application: How IO Classification Enables Series Extension

### T501-T503 (Productive Output Aggregates)

**Current limitation**: T501 (TP*), T502 (C*_m), T503 (GFP*) are book-period only (1948-1989) because extending them requires knowing which sectors are productive in the NIPA post-1989 data.

**What IO classification provides**:
- Map of IO sector -> productive/unproductive for each benchmark year
- For inter-benchmark years: interpolate productive shares
- For extension years (1990+): use latest benchmark classification

**Extension procedure**:
1. For each benchmark year, compute productive-sector share of gross output: `share_p = GO_productive / GO_total`
2. Interpolate shares for inter-benchmark years
3. Apply shares to annual BEA GDP-by-industry data: `TP*_ext = GDP_total x share_p`

### DIV-001 Resolution (T513, T514)

**Current limitation**: Profit rate uses total K instead of productive K*.

**What IO classification provides**:
- Map of which sectors are productive
- Apply to BEA Fixed Assets Table 4.1 (net stock by industry)
- Restrict K to productive sectors: `K* = sum(K_i for i in productive_sectors)`
- Recompute: `r* = S* / K*`

---

## Gap Register

| Gap | Severity | Resolution |
|-----|----------|------------|
| No post-1977 IO matrices | HIGH | Source BEA benchmark tables for 1982-2017 |
| NAICS concordance needed | HIGH | Create productive/unproductive mapping for NAICS sectors |
| Inter-benchmark interpolation | MEDIUM | Apply interpolation methodology (already documented) |
| Annual IO tables (post-1997) | LOW | BEA publishes annual Make/Use tables; could replace benchmarks |

---

*Chapter 4 Investigation — ST2 Project*
*Created: 2026-03-30*
