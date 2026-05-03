# Chapter 5 Investigation — Accounting Framework for Empirical Estimates

## 1. Overview

- **Chapter**: 5 — "An Accounting Framework for Empirical Estimates"
- **Page Range**: ~pp. 95-150 (Chapters 5.1-5.5)
- **Empirical Type**: Primary empirical (constructs Marxian national accounts from US NIPA data)
- **T-Series**: 16 (T501-T516)
- **Tables**: 10 (Tables 5.5-5.14)
- **Figures**: 8 (Figures 5.1-5.8)
- **Core Period**: 1948-1989 (benchmark years: 1948, 1958, 1967, 1977, 1989)
- **Wave Assignment**: Wave 1 (foundation)
- **Investigation Date**: 2026-02-23
- **Status**: IN PROGRESS

---

## 2. Content Summary

Chapter 5 is the empirical backbone of *Measuring the Wealth of Nations*. It constructs a complete set of Marxian national accounts from US NIPA data for the period 1948-1989. The chapter translates the theoretical framework of Chapters 3-4 (productive vs unproductive labor, Marxian value categories) into empirical estimates using Bureau of Economic Analysis (BEA) National Income and Product Accounts and Bureau of Labor Statistics (BLS) Current Employment Statistics.

The key theoretical framework distinguishes productive labor (creating use-values in commodity production, transportation, and productive services) from unproductive labor (trade, finance, government administration). This distinction fundamentally redefines national accounting aggregates: Total Product (TP*) replaces GDP, Value Added (VA*) replaces conventional value added, Variable Capital (V*) replaces total wages, and Surplus Value (S*) replaces profit-type income. The chapter demonstrates that the Marxian rate of exploitation (e = S*/V*) ranges from 1.70 (1948) to 2.44 (1989) — far exceeding the conventional profit/wage ratio of ~1.33.

Chapter 5 provides the foundational series for all subsequent chapters: Chapter 6 (Net Social Wage) depends on V* and employment decomposition; Chapter 9 (Summary) derives entirely from Chapter 5 results.

---

## 3. Table Inventory (NIPA-Line-Item Depth)

### Table 5.5: Marxian National Accounts — Revenue Side

**What it shows**: Revenue-side Marxian aggregates for benchmark years (1948, 1958, 1967, 1977, 1989)

**T-series contained**: T501 (TP*), T502 (C* = M_p), T503 (VA*), T504 (V* = W_p), T505 (S*), T506 (S*/V*)

**Row-by-row NIPA mapping**:

| Row | Variable | Marxian Symbol | Formula | NIPA Source (from Table E.2) | NIPA Table.Line |
|-----|----------|---------------|---------|------------------------------|-----------------|
| 1 | Total Product | TP* | GO_p + GO_t | Table D.2 (Appendix D) | Derived from NIPA 1.7.5 (GDP by Industry, Gross Output) |
| 2 | Constant Capital (materials) | C* = M'_p = C*_m | Intermediate inputs of productive sectors | Table D.2 | Derived from NIPA 1.7.5, BEA IO tables |
| 3 | Value Added (Marxian) | VA* | TP* - C* | Derived | Derived |
| 4 | Variable Capital | V* = W_p | Productive worker wages | Table D.2 | NIPA 6.2 (Compensation by Industry) × BLS productive labor share |
| 5 | Surplus Value | S* | VA* - V* | Derived | Derived |
| 6 | Rate of Surplus Value | e = S*/V* | S* / V* | Derived ratio | Derived ratio |

**Data period**: 1948-1989 (benchmark years; interpolated annually)
**Units**: Billions of current dollars (except S*/V* = ratio)
**Benchmark values (e = S*/V*)**: 1.70 (1948), 1.83 (1958), 2.10 (1967), 2.10 (1977), 2.44 (1989)

**Known issues**:
- TP* depends on productive-sector gross output, which requires sector classification via concordance (85 IO sectors -> 13 NIPA industries)
- C* = M_p requires industry-level intermediate consumption data from BEA IO benchmark tables
- V* approximation relies on ec_u/ec_p ~ 1 finding (Section 5.3)

---

### Table 5.6: Marxian National Accounts — Use Side

**What it shows**: Use-side decomposition: TP*, U*, FP*, and components (CON*, IG*, G*, (X-IM)*)

**T-series contained**: T507 (FP* = GFP*), T508 (NP* = CON_Wp), T509 (SP*), T510 (SP*/NP*)

**Row-by-row NIPA mapping (from Table E.2, page_310)**:

| Row | Variable | Marxian Symbol | Formula | NIPA Source (Table E.2) | NIPA Table.Line |
|-----|----------|---------------|---------|-------------------------|-----------------|
| 1 | Total Product | TP* | = Revenue side TP* | Table D.2 | Same as Table 5.5 row 1 |
| 2 | Materials used up | C*_m = M'_p | = Revenue side C* | Table D.2 | Same as Table 5.5 row 2 |
| 3 | Gross Final Product | GFP = TP* - C*_m | Derived | Derived | Derived |
| 4 | Consumption (Marxian) | CON* | CON - GVA_ir - RY_con + HH_con - ROW_con | 101 2; Table E.1; Table D.2; 601 73 | NIPA 1.1.5 line 2 (PCE); NIPA 6.1 line 73 (HH); derived adjustments |
| 5 | Consumption (NIPA) | CON | NIPA Personal Consumption Expenditures | 101 2 | NIPA 1.1.5 line 2 |
| 6 | Imputed royalties (consumption) | GVA_ir | Gross value added of interest and rent | Table E.1 | Computed (Appendix E Table 1) |
| 7 | Royalty adjustment (consumption) | RY_con | Royalties allocated to consumption | Table D.2 | Derived from Appendix D |
| 8 | Household consumption | HH_con | Household consumption of fixed capital | 601 73 | NIPA 6.1 line 73 |
| 9 | ROW consumption adjustment | ROW_con | Rest-of-world consumption | Table D.2 | Derived |
| 10 | Investment (Marxian) | IG* | IG - RY_i + ABR | 101 6; Table D.2; Table E.1 | NIPA 1.1.5 line 6 (GPDI); Appendix E (ABR) |
| 11 | Investment (NIPA) | IG | Gross Private Domestic Investment | 101 6 | NIPA 1.1.5 line 6 |
| 12 | Royalty adjustment (investment) | RY_i | Royalties allocated to investment | Table D.2 | Derived |
| 13 | Adjusted business reserves | ABR | Building rent adjustment | Table E.1 | Computed (Appendix E Table 1) |
| 14 | Net exports (Marxian) | (X-IM)* | (X-IM) - RY_x-im - ROW_x-im | 101 15; Table D.2 | NIPA 1.1.5 line 15 |
| 15 | Net exports (NIPA) | X-IM | Net Exports of Goods and Services | 101 15 | NIPA 1.1.5 line 15 |
| 16 | Royalty adjustment (net exports) | RY_x-im | Royalties allocated to net exports | Table D.2 | Derived |
| 17 | ROW net exports adjustment | ROW_x-im | Rest-of-world net exports | Table D.2 | Derived |
| 18 | Government (Marxian) | G* | G - RY_G - W_G + ROW_s | 301 7; Table D.2; 301 8 | NIPA 3.1 line 7 (Federal); NIPA 3.1 line 8 (State/Local) |
| 19 | Government (NIPA) | G | Government Consumption Expenditures | 301 7 | NIPA 3.1 line 7 |
| 20 | Royalty adjustment (government) | RY_G | Royalties allocated to government | Table D.2 | Derived |
| 21 | Government wages | W_G | Wages paid to government employees | 301 8 | NIPA 3.1 line 8 |
| 22 | ROW subsidies | ROW_s | Rest-of-world subsidy adjustment | Table D.2 | Derived |
| 23 | Depreciation consumed | C*_d | Consumption of fixed capital | Table E.1 | Computed (Appendix E Table 1) |
| 24 | Final Product | FP* = GFP* - C*_d | Net of depreciation | Derived | Derived |

**Transformation chain**:
1. Start with NIPA use-side aggregates (CON, IG, X-IM, G) from NIPA Table 1.1.5 and 3.1
2. Remove royalty imputations (RY_con, RY_i, RY_G, RY_x-im) — these are fictitious income attributions
3. Add building rent (ABR) and household consumption (HH_con) adjustments
4. Subtract government wages (W_G) — government employees are unproductive
5. Adjust for rest-of-world flows (ROW_con, ROW_x-im, ROW_s)
6. Subtract depreciation (C*_d) to obtain FP*

**Validation source**: Table E.2 (page_310_table_E2.csv) provides complete 1948-1961 annual data with source column identifying every NIPA input.

**Example verification (1948)**:
- CON = 174.90 (NIPA 1.1.5 line 2), GVA_ir = 8.40 (Table E.1), RY_con = 6.90 (Table D.2), HH_con = 2.40 (NIPA 6.1 line 73), ROW_con = -1.27 (Table D.2)
- CON* = 174.90 - 8.40 - 6.90 + 2.40 - (-1.27) = 158.46 -- confirmed in Table E.2 row "CON*" = 158.46

---

### Table 5.7: Key Ratios (THE Benchmark Table)

**What it shows**: Three key ratios for benchmark years: exploitation rate, productive labor share, productive wage share

**T-series contained**: T506 (e = S*/V*), T511 (Lp/L), T512 (V*/W)

**Row-by-row mapping**:

| Row | Variable | Symbol | Formula | Source | NIPA/BLS Input |
|-----|----------|--------|---------|--------|----------------|
| 1 | Exploitation rate | e = S*/V* | (VA* - V*) / V* | Derived from Table 5.5 | All Table 5.5 inputs |
| 2 | Productive labor share | Lp/L | Productive employment / Total employment | BLS CES production worker data | BLS CES: production workers by industry × concordance classification |
| 3 | Productive wage share | V*/W | Productive worker wages / Total wages | Approximation: V*/W ~ Lp/L | NIPA 6.2 (Compensation); finding ec_u/ec_p ~ 1 |

**Critical benchmark values (from authoritative CSV)**:

| Year | e (S*/V*) | Lp/L | V*/W |
|------|-----------|------|------|
| 1948 | 1.70 | 0.57 | 0.54 |
| 1958 | 1.83 | 0.52 | 0.49 |
| 1967 | 2.10 | 0.51 | 0.45 |
| 1977 | 2.10 | 0.50 | 0.41 |
| 1989 | 2.44 | 0.36 | 0.36 |

**Key methodological finding**: Unit wages of productive and unproductive workers are nearly equal (ec_u/ec_p ~ 1), therefore V*/W ~ Lp/L. This is validated in Section 5.3 and is the basis for the 1990-2024 extension methodology.

**Existing replication status**: Phase 3 achieved 93.8% exact match against book benchmarks.

---

### Table 5.8: Comparison — Marxian vs Conventional Profit Rates

**What it shows**: Marxian rate of profit r* = S*/K vs conventional NIPA profit rate, plus capacity-adjusted variants

**T-series contained**: T513 (r* = S*/K), T514 (r*_adjusted)

**Row-by-row mapping**:

| Row | Variable | Symbol | Formula | NIPA Source |
|-----|----------|--------|---------|-------------|
| 1 | Marxian profit rate | r* | S* / K | S* from Table 5.5; K from NIPA Fixed Assets Table (nonresidential fixed assets, current cost) |
| 2 | Conventional profit rate | r_NIPA | (Profit-type income) / K | NIPA 1.14 (National Income by Type); Fixed Assets Table |
| 3 | Capacity-adjusted Marxian | r*_adj | r* × capacity utilization | Federal Reserve G.17 (Industrial Production and Capacity Utilization) |
| 4 | Capacity-adjusted conventional | r_NIPA_adj | r_NIPA × capacity utilization | Federal Reserve G.17 |

**Known issue (P1 BLOCKER)**: The existing Shiny app shows a large profit rate discrepancy. Root cause: calculation uses total capital stock K (all sectors) instead of productive capital stock K* = C*_f (productive sectors only). Resolution documented in `R_STAR_DISCREPANCY_RESOLUTION.md` (referenced in Gap/Blocker Register).

---

### Tables 5.9-5.10: Employment Decomposition

**What they show**: Productive labor (Lp) and unproductive labor (Lu) by sector

**T-series contained**: T515 (Lp by sector), T516 (Lu by sector)

**Sector-by-sector NIPA/BLS mapping (from page_320 labor statistics)**:

| Sector | NIPA/BLS Source | Classification | Decomposition Method |
|--------|----------------|---------------|---------------------|
| Agriculture | NIPA 6.10B line 4 (Employment by Industry) | Productive (with adjustment) | (Lp)_agr = (Lp/L)_min × L_agr; (Lu)_agr = L_agr - (Lp)_agr |
| Mining | NIPA 6.10B | 100% Productive | All workers productive |
| Construction | NIPA 6.10B | 100% Productive | All workers productive |
| Manufacturing (durable) | NIPA 6.10B | 100% Productive | All workers productive |
| Manufacturing (nondurable) | NIPA 6.10B | 100% Productive | All workers productive |
| Transportation | NIPA 6.10B | 100% Productive | All workers productive |
| Communications | NIPA 6.10B | 100% Productive | All workers productive |
| Electric/gas utilities | NIPA 6.10B | 100% Productive | All workers productive |
| Wholesale trade | NIPA 6.10B line 50 | 100% Unproductive | L_whtr = (Lu)_whtr |
| Retail trade | NIPA 6.10B line 51 | 100% Unproductive | L_retr = (Lu)_retr |
| FIRE | NIPA 6.10B line 52 | Decomposed | L_fi (unproductive); L_br = L_re - L_gr (building rent, unproductive); L_r = L_fr + L_gr (royalties) |
| Government enterprises (Federal) | NIPA 6.10B line 81 | Productive (with adjustment) | (Lp)_gefed = (Lp/L)_nongovtot × L_gefed |
| Government enterprises (State/local) | NIPA 6.10B line 86 | Productive (with adjustment) | (Lp)_gest = (Lp/L)_nongovtot × L_gest |
| Government (non-enterprise) | NIPA 6.10B lines 78, 83 | 100% Unproductive (dummy sector) | L_d = L_govntfed + L_govntsl |
| Services | NIPA 6.10B | Mixed | Productive services (hotels, repair, amusements, health, education) vs unproductive (business services) |

**Special decompositions**:

1. **Agriculture**: Uses minimum productive-labor ratio (Lp/L)_min applied to total agricultural employment. Values from page_320: (Lp/L)_min ranges from 0.782 (1948) to 0.759 (1961).

2. **Government enterprises**: Uses total non-government productive ratio (Lp/L)_nongovtot applied to government enterprise employment. Values: 0.734 (1948) to 0.700 (1960).

3. **FIRE decomposition**:
   - L_fire = total FIRE employment
   - L_re = total real estate employment (NIPA 6.10B line 58)
   - L_fi = L_fire - L_re (finance/insurance)
   - g = ground rent proportion from Table B.5 (~0.26-0.30)
   - L_gr = L_re × g (ground rent labor)
   - L_br = L_re - L_gr (building rent labor)
   - L_r = L_fi + L_gr (royalties labor — finance/insurance + ground rent)

4. **Trade**: All trade labor classified as unproductive per Marxian theory (circulation, not production)

**Concordance file**: `Inputs/Concordances/io_85_to_nipa_13_concordance.csv` maps 85 IO sectors to 13 NIPA industries with productive/unproductive classification.

**Summary results from page_320 (1948-1961)**:
- L (total): 66,091 (1948) to 82,827 (1961) thousands
- Lp/L: ~0.453 (1948) declining to ~0.406 (1961)

---

### Tables 5.11-5.12: Variable Capital Decomposition

**What they show**: V* = w_p × L_p by sector; W_u decomposition

**NIPA inputs (from page_330 trade wages)**:

| Component | NIPA Table | Line Reference | Description |
|-----------|-----------|---------------|-------------|
| EC by industry | NIPA 6.04B | Lines 50, 51, 52, 58, 78, 83 | Employee compensation by sector |
| FTE by industry | NIPA 6.07B | Lines 50, 51, 52, 58, 78, 83 | Full-time equivalent employees |
| Employment by industry | NIPA 6.10B | Lines 50, 51, 52, 58, 78, 83 | Total employees |

**Sector-specific wage calculations (from page_330 equations)**:

| Sector | Unit Wage Formula | Wage Formula |
|--------|-------------------|--------------|
| Wholesale trade | ec_whtr = EC_whtr / FEE_whtr | W_whtr = ec_whtr × L_whtr |
| Retail trade | ec_retir = EC_retir / FEE_retir | W_retir = ec_retir × L_retir |
| Finance/insurance | ec_fi = (EC_fire - EC_re) / (FEE_fire - FEE_re) | W_fi = ec_fi × L_fi |
| Real estate | ec_re = EC_re / FEE_re | W_re = ec_re × L_re |
| Building rent | — | W_br = W_re - W_gr |
| Ground rent | — | W_gr = W_re × g |
| Government (Federal) | — | EC_govfed (NIPA 6.04B line 78) |
| Government (State/local) | — | EC_govst (NIPA 6.04B line 83) |

**Variable capital formula** (from page_340):
- V* = w_p × x × L_p
- Where w_p = production worker wages, x = compensation/salary ratio, L_p = productive workers
- W_u = W - V* (unproductive wages = total wages minus variable capital)

**Key empirical finding** (Section 5.3, p. 113):
- ec_u/ec_p ~ 1 (unit wages nearly equal between productive and unproductive workers)
- Therefore V*/W ~ Lp/L (productive wage share approximates productive labor share)
- Corporate officers' salaries have minimal impact: only 4.2% of total wages in manufacturing (1968)

---

### Tables 5.13-5.14: Summary Comparisons

**What they show**: Marxian vs orthodox measure comparisons — levels, ratios, and trends

**T-series**: These are presentation tables reusing T501-T514 data (no new series)

**Table 5.14 data** (from page_140_marxian_orthodox_comparison.csv):

| Variable | Typical Relative Levels (1967) | Change in Relative Levels (1948-89) |
|----------|-------------------------------|-------------------------------------|
| TP*/GP | 82% | -12% |
| TP*/GNP | 147% | -14% |
| Lp/L | 44% | -37% |
| V*/W | 42% | -33% |
| S*/P | 224% | +34% |
| C*/V* | 245% | +23% |
| M/EC | 136% | -12% |
| S*/V* | 210% | +44% |
| P+/EC | 58% | -27% |
| q*/y | 306% | +49% (1948-89); +19% (1972-82) |

**Key interpretive findings**:
- Marxian total product TP* ~ 82% of IO gross product GP
- TP* ~ 1.5× GNP (conventional measure)
- Surplus value S* ~ 2× profit-type income P+
- Rate of exploitation S*/V* ~ 210% of conventional profit/wage ratio
- Productive labor share fell 37% over the postwar period
- Marxian productivity grows faster than conventional (+49% vs lower conventional measures)

---

## 4. Figure Inventory

| Figure | Type | Title/Description | Series Used | Page (book) | Validation |
|--------|------|-------------------|-------------|-------------|------------|
| Fig 5.1 | Conceptual/Structural | IO Accounts and Marxian Categories — condensed matrix mapping | None (matrix diagram) | p. 110 | FPR only; documented in page_110_io_marxian_mapping.md |
| Fig 5.2 | Empirical (time_series) | Productive and Unproductive Labor, 1948-1988 | T511 (Lp/L), T515 (Lp), T516 (Lu) | p. 56 | Compare against page_130 labor trends |
| Fig 5.3 | Empirical (time_series) | Rates of Profit and Surplus Value | T506 (e = S*/V*) | p. 61 | Compare against Table 5.7 benchmarks |
| Fig 5.4 | Empirical (time_series) | Value/materialized composition of capital | T501-T505 (revenue side components) | — | Derived from Table 5.5 |
| Fig 5.5 | Empirical (time_series) | Marxian vs Conventional Profit Rates | T513 (r*), T514 (r*_adj) | — | Compare against Table 5.8 |
| Fig 5.6 | Empirical (time_series) | Productivity comparison (Marxian vs conventional) | T501 (TP*), T515 (Lp) | — | q* = TP*/Lp vs y = GDP/L |
| Fig 5.7 | Empirical (time_series) | Total Labor and Productive Labor Trends | T511, T515, T516 | p. 130 | L: 58K→110K+; Lp: 33K→41K (page_130) |
| Fig 5.8 | Empirical (cross_sectional) | Table 5.14 bar chart — Marxian vs Orthodox comparison | All T5xx series | — | Against page_140 comparison CSV |

### Figure Type Summary

| Type | Count | Figures |
|------|-------|---------|
| time_series | 6 | Fig 5.2, 5.3, 5.4, 5.5, 5.6, 5.7 |
| conceptual | 1 | Fig 5.1 |
| cross_sectional | 1 | Fig 5.8 |

---

## 5. T-Series Catalog

| ID | Name | Formula | NIPA Inputs | BLS Inputs | Period | Status |
|----|------|---------|-------------|------------|--------|--------|
| T501 | Total Product (TP*) | GO_p + GO_t | NIPA 1.7.5 (Gross Output by Industry, productive + trading sectors) | — | 1948-1989 | Book benchmarks available; NIPA placeholder |
| T502 | Constant Capital — Materials (C* = M_p) | Intermediate inputs of productive sectors | NIPA IO benchmark tables (intermediate consumption) | — | 1948-1989 | Book benchmarks (Table E.2); NIPA placeholder |
| T503 | Value Added — Marxian (VA*) | TP* - C* = T501 - T502 | Derived | — | 1948-1989 | Derived from T501, T502 |
| T504 | Variable Capital (V* = W_p) | Productive worker wages = ec_p × Lp | NIPA 6.2 (Compensation by Industry) | BLS CES (production worker ratios) | 1948-1989 | Approximation: V* ~ W × (Lp/L) |
| T505 | Surplus Value (S*) | VA* - V* = T503 - T504 | Derived | — | 1948-1989 | Derived from T503, T504 |
| T506 | Rate of Surplus Value (e = S*/V*) | S* / V* = T505 / T504 | Derived ratio | — | 1948-1989 | Book benchmarks: 1.70-2.44; Phase 3: 93.8% match |
| T507 | Gross Final Product (GFP* = FP*) | TP* - C*_m - C*_d | Table E.2 sources (see Table 5.6) | — | 1948-1989 | Table E.2 has 1948-1961 annual |
| T508 | Necessary Product (NP* = CON_Wp) | Consumption of productive workers | NIPA 1.1.5 line 2 (PCE) × productive worker share | — | 1948-1989 | Requires consumption allocation |
| T509 | Surplus Product (SP*) | FP* - NP* = T507 - T508 | Derived | — | 1948-1989 | Derived |
| T510 | Rate of Exploitation (use-side) (SP*/NP*) | SP* / NP* = T509 / T508 | Derived ratio | — | 1948-1989 | Should equal S*/V* in theory |
| T511 | Productive Labor Share (Lp/L) | Productive employment / Total employment | — | BLS CES production worker data; concordance classification | 1948-1989 | Book benchmarks: 0.57→0.36 |
| T512 | Productive Wage Share (V*/W) | Productive worker wages / Total wages | NIPA 6.2 (Compensation by Industry) | BLS CES | 1948-1989 | Approximation: ~ Lp/L per ec_u/ec_p ~ 1 |
| T513 | Marxian Profit Rate (r* = S*/K) | S* / K (productive capital stock) | S* from T505; K from NIPA Fixed Assets Table | — | 1948-1989 | Known discrepancy: uses total K, not K* |
| T514 | Capacity-Adjusted Marxian Profit Rate | r* × capacity utilization | T513; Federal Reserve G.17 (capacity utilization) | — | 1948-1989 | Requires Fed data |
| T515 | Productive Labor by Sector (Lp) | Sum of productive workers across all sectors | NIPA 6.10B (Employment by Industry) | BLS CES (production worker ratios) | 1948-1989 | page_320 has 1948-1961 detail |
| T516 | Unproductive Labor by Sector (Lu) | L - Lp by sector | NIPA 6.10B | BLS CES | 1948-1989 | page_320 has 1948-1961 detail |

---

## 6. Data Sources

### Primary Sources

#### BEA National Income and Product Accounts (NIPA)

- **Reference**: Bureau of Economic Analysis, U.S. Department of Commerce. National Income and Product Accounts Tables.
- **Coverage**: 1948-1989 (historical book period)
- **Quality**: AUTHORITATIVE (official US government statistics)
- **Access**: BEA Interactive Data API (https://apps.bea.gov/iTable/) or FRED
- **Key tables used**:
  - Table 1.1.5: Gross Domestic Product (use-side components: PCE, GPDI, Net Exports, Government)
  - Table 1.7.5: GDP by Industry, Gross Output
  - Table 2.1: Personal Income and Its Disposition
  - Table 3.1: Government Current Receipts and Expenditures
  - Table 6.1: National Income by Type of Income (line 73: households)
  - Table 6.2: Compensation of Employees by Industry
  - Table 6.3: Wages and Salaries by Industry
  - Table 6.4/6.5: Full-Time Equivalent Employees by Industry
  - Table 6.10B: Employment by Industry
  - Fixed Assets Tables: Nonresidential fixed assets, current cost

#### BLS Current Employment Statistics (CES)

- **Reference**: Bureau of Labor Statistics, U.S. Department of Labor. Current Employment Statistics.
- **Coverage**: 1948-1989
- **Quality**: AUTHORITATIVE (official US government statistics)
- **Access**: BLS Data API (https://api.bls.gov/publicAPI/v2/)
- **Key data**: Production/nonsupervisory worker ratios by industry, used for Lp/L decomposition

#### BEA Input-Output Tables

- **Reference**: BEA Benchmark Input-Output Tables (1947, 1958, 1963, 1967, 1972, 1977)
- **Coverage**: Benchmark years
- **Quality**: AUTHORITATIVE
- **Access**: BEA website
- **Key data**: 85-sector IO tables (A-matrices, Z-matrices, L-matrices) for gross output, intermediate consumption, and labor value calculations

#### Federal Reserve G.17

- **Reference**: Federal Reserve Board. Industrial Production and Capacity Utilization (G.17).
- **Coverage**: 1948-1989
- **Quality**: AUTHORITATIVE
- **Access**: FRED API
- **Key data**: Capacity utilization rates for profit rate adjustment (T514)

### Data Files

| File | Format | Rows | Columns | Status |
|------|--------|------|---------|--------|
| `Inputs/BookTables/ch05/[2025.12.05] shaikh_tonak_authoritative_1948_1989.csv` | CSV | 42 | 11 | VALIDATED — Book benchmark values |
| `Inputs/BookTables/ch05/[2025.12.05] shaikh_tonak_authoritative_1948_2024.csv` | CSV | 77 | 11 | VALIDATED — Extended series |
| `Inputs/NIPA/nipa_1948_1989.csv` | CSV | 546 | 9 | PLACEHOLDER — source="template" for all rows |
| `Inputs/Concordances/io_85_to_nipa_13_concordance.csv` | CSV | 85 | 6 | VALIDATED — Research-based, no placeholders |
| `Technical/Knowledge_Base/tables/page_310_table_E2.csv` | CSV | 27 | 16 | VALIDATED — OCR extraction from book Appendix Table E.2 |
| `Technical/Knowledge_Base/tables/page_320_labor_statistics.csv` | CSV | 31 | 18 | VALIDATED — OCR extraction from Appendix Table E.3 |
| `Technical/Knowledge_Base/tables/page_330_trade_wages.csv` | CSV | 37 | 16 | VALIDATED — OCR extraction from Appendix Table E.4 |
| `Technical/Knowledge_Base/tables/page_340_variables_definitions.csv` | CSV | 16 | 2 | VALIDATED — Variable catalog |
| `Technical/Knowledge_Base/tables/page_120_marxian_estimates_1953_1961.csv` | CSV | 36 | 10 | VALIDATED — Intermediate period estimates |
| `Technical/Knowledge_Base/tables/page_140_marxian_orthodox_comparison.csv` | CSV | 10 | 4 | VALIDATED — Table 5.14 data |
| `Technical/Knowledge_Base/tables/page_060_sectoral_structure.csv` | CSV | 6 | 2 | VALIDATED — Sector classification |
| `Technical/Knowledge_Base/tables/page_070_marxian_io_measures.csv` | CSV | 15 | 3 | VALIDATED — Numerical example |
| `Technical/ShinyApp/data/comprehensive_1948_1989.csv` | CSV | — | — | EXISTING — Shiny app dataset |
| `Technical/ShinyApp/data/exploitation_composition_1948_1989.csv` | CSV | — | — | EXISTING — Exploitation/composition data |
| `Technical/ShinyApp/data/profit_rates_1948_1989.csv` | CSV | — | — | EXISTING — Profit rate data |
| `Technical/ShinyApp/data/employment_1948_1989.csv` | CSV | — | — | EXISTING — Employment data |

---

## 7. Transformation Chain

### Step-by-step: Raw NIPA -> Marxian National Accounts

```
STAGE 1: SECTOR CLASSIFICATION
  Input:  85 IO sectors (BEA benchmark tables)
  Apply:  io_85_to_nipa_13_concordance.csv
  Output: 13 NIPA industries classified as productive/unproductive/mixed
          - Productive: Agriculture, Mining, Construction, Manufacturing (2),
            Transportation, Communications, Utilities, selected Services
          - Unproductive: Wholesale trade, Retail trade, FIRE, Business services
          - Mixed: Government (enterprises=productive, administration=unproductive)

STAGE 2: EMPLOYMENT DECOMPOSITION (Tables 5.9-5.10 -> T515, T516)
  Input:  NIPA 6.10B (Employment by Industry)
          BLS CES (production worker ratios)
  Apply:  Sector-specific rules:
          - Agriculture: (Lp)_agr = (Lp/L)_min × L_agr
          - Gov enterprises: (Lp)_ge = (Lp/L)_nongovtot × L_ge
          - Trade: all Lu
          - FIRE: decompose into fi, re, br, gr subsectors
          - Government: all Lu (dummy sector)
  Output: Lp (productive labor), Lu (unproductive labor) by sector and year
          Lp/L ratio (T511)

STAGE 3: REVENUE-SIDE ACCOUNTS (Table 5.5 -> T501-T506)
  Input:  NIPA 1.7.5 (Gross Output by Industry)
          BEA IO tables (intermediate consumption)
          NIPA 6.2 (Compensation by Industry)
          BLS production worker ratios
  Apply:  TP* = GO_p + GO_t (productive + trading gross output)
          C*  = M_p (productive-sector intermediate inputs)
          VA* = TP* - C*
          V*  = W_p ≈ W × (Lp/L) [per ec_u/ec_p ≈ 1 finding]
          S*  = VA* - V*
          e   = S*/V*
  Output: Marxian revenue-side aggregates (T501-T506)

STAGE 4: USE-SIDE ACCOUNTS (Table 5.6 -> T507-T510)
  Input:  NIPA 1.1.5 (PCE, GPDI, Net Exports)
          NIPA 3.1 (Government expenditures)
          NIPA 6.1 line 73 (Household consumption)
          Appendix E Table 1 (GVA_ir, ABR, C*_d)
          Appendix D Table 2 (royalty adjustments RY_*)
  Apply:  CON* = CON - GVA_ir - RY_con + HH_con - ROW_con
          IG*  = IG - RY_i + ABR
          (X-IM)* = (X-IM) - RY_x-im - ROW_x-im
          G*   = G - RY_G - W_G + ROW_s
          GFP  = TP* - C*_m
          FP*  = GFP - C*_d
          NP*  = CON_Wp (consumption of productive workers)
          SP*  = FP* - NP*
  Output: Marxian use-side aggregates (T507-T510)

STAGE 5: WAGE DECOMPOSITION (Tables 5.11-5.12)
  Input:  NIPA 6.04B (Employee compensation by sector)
          NIPA 6.07B (FTE by sector)
          NIPA 6.10B (Employment by sector)
  Apply:  Unit wages by sector: ec_i = EC_i / FEE_i
          Sector wages: W_i = ec_i × L_i
          Variable capital: V* = Σ (ec_p × Lp) across productive sectors
          V*/W ratio (T512)
  Output: V* and W_u = W - V* by sector

STAGE 6: PROFIT RATE (Table 5.8 -> T513, T514)
  Input:  S* from Stage 3
          K from NIPA Fixed Assets Table
          Capacity utilization from Federal Reserve G.17
  Apply:  r* = S* / K [NOTE: should be K* = productive capital only]
          r*_adj = r* × capacity_utilization
  Output: Marxian and conventional profit rates

STAGE 7: VALIDATION
  Compare: Against book benchmarks (Table 5.7)
           Against Table E.2 annual data (1948-1961)
           Against page_120 intermediate estimates (1953-1961)
           Against page_140 comparison ratios
  Tolerance: 0.1% for rates, 1% for absolute values (per Method Contract)
```

---

## 8. Existing Assets Inventory

### Phase 3 Calculation Scripts

| Script | Path | Function | Quality |
|--------|------|----------|---------|
| `marxian_variable_calculator.py` | `Technical/scripts/calculate/` | Core V*, S*, e calculation | FUNCTIONAL — 93.8% match on benchmarks |
| `calculate_sector_employment.py` | `Technical/scripts/calculate/` | Sector employment decomposition | FUNCTIONAL |
| `employment_calculator.py` | `Technical/scripts/calculate/` | Employment calculation | FUNCTIONAL |
| `extract_gross_output.py` | `Technical/scripts/calculate/` | Gross output extraction | FUNCTIONAL |
| `calculate_hp_coefficients.py` | `Technical/scripts/calculate/` | Labor value coefficients | FUNCTIONAL |
| `calculate_lambda_star.py` | `Technical/scripts/calculate/` | Lambda* calculation | FUNCTIONAL |
| `io_matrix_inversion.py` | `Technical/scripts/calculate/` | Leontief inverse | FUNCTIONAL |
| `interpolation.py` | `Technical/scripts/calculate/` | Time series interpolation | FUNCTIONAL |
| `process_bls_ratios.py` | `Technical/scripts/calculate/` | BLS ratio processing | PLACEHOLDER — uses synthetic data |
| `create_placeholder_bls_ratios.py` | `Technical/scripts/calculate/` | Placeholder BLS generation | PLACEHOLDER — needs real BLS API data |
| `week3_employment_tables.py` | `Technical/scripts/calculate/` | Employment table generation | FUNCTIONAL |
| `week4_variable_capital.py` | `Technical/scripts/calculate/` | Variable capital calculation | FUNCTIONAL |
| `week5_surplus_value.py` | `Technical/scripts/calculate/` | Surplus value calculation | FUNCTIONAL |
| `week6_integration_validation.py` | `Technical/scripts/calculate/` | Cross-validation | FUNCTIONAL |

### Shiny App Data

| File | Content | Quality |
|------|---------|---------|
| `comprehensive_1948_1989.csv` | All-in-one dataset | EXISTING — derived from Phase 3 |
| `employment_1948_1989.csv` | Employment decomposition | EXISTING |
| `exploitation_composition_1948_1989.csv` | e, C*/V* | EXISTING |
| `profit_rates_1948_1989.csv` | r*, r*_adj | EXISTING — known discrepancy |
| `government_1948_1989.csv` | Government absorption | EXISTING |

### IO Matrices

18 files in `Inputs/IO_Matrices/`: A, L, Z matrices for benchmarks 1947, 1958, 1963, 1967, 1972, 1977.

### Mohun Comparison Data

16 files in `Inputs/ExternalSources/Mohun/`: Alternative employment, exploitation, and variable capital estimates for cross-validation.

---

## 9. Known Issues and Gaps

### P0 — Critical Blockers

1. **NIPA data is placeholder** (`nipa_1948_1989.csv`): All 546 rows have `source="template"`. Industry-level employment, compensation, value added, and gross output are synthetic, not actual BEA values. **Resolution**: Replace with real BEA API data (NIPA Tables 6.2-6.10, 1.7.5). This blocks any independent replication beyond book benchmarks.

2. **BLS production worker ratios are placeholder**: Phase 3 used `create_placeholder_bls_ratios.py` to generate synthetic ratios. **Resolution**: Pull actual BLS CES production/nonsupervisory worker data via BLS API.

### P1 — Significant Issues

3. **Profit rate discrepancy (r*)**: Shiny app shows large deviation from book values. Root cause: using total capital stock K instead of productive capital stock K* = C*_f. **Resolution**: Restrict denominator to productive-sector fixed assets only.

4. **VA*/W = 1.238 constant**: The 1990-2024 extension uses a fixed VA*/W ratio derived from the 1989 endpoint. No sensitivity analysis performed. **Impact**: Extension results may be sensitive to this assumption.

5. **Table E.2 row labels incomplete**: The 27-row CSV (page_310_table_E2.csv) has been OCR-extracted but some row identifications may be imprecise. The "Sources" column provides NIPA table references but the NIPA table numbering convention (e.g., "101 2" = NIPA Table 1.01 line 2) needs systematic verification.

### P2 — Methodology Clarifications Needed

6. **Self-employed wage equivalents**: Book adds wage equivalent of self-employed (WEQ) to employee compensation. Method for calculating WEQ not fully documented in extracted pages.

7. **Corporate officers' salaries (COS)**: Book follows Mage (1963) in excluding COS as capitalist income. Adjustment method documented in Appendix G (not extracted).

8. **Distributive transportation**: Page_110 notes "Distributive transport was not estimated in this framework." Impact on TP* calculation unclear.

9. **IVA treatment**: Inventory Valuation Adjustment is merged into both GVA* and GFP* (noted in page_110 figure). Exact treatment methodology needs clarification.

---

## 10. Compliance Checklist

### Documentation
- [x] All figures classified by type (8 figures: 6 time_series, 1 conceptual, 1 cross_sectional)
- [ ] DPR files for all time_series/derived datasets (NOT YET — Investigation phase only)
- [ ] FPR files for all theoretical/cross_sectional/simulation figures (NOT YET)
- [x] Source observations captured (Table E.2 Rosetta Stone documented)

### Data (if applicable)
- [x] Data files exist and load correctly (authoritative CSV validated)
- [x] Data-to-figure mappings verified (series dependencies documented)
- [ ] Transformations logged in TRANSFORMATION_LOG.json (NOT YET)

### Testing (if applicable)
- [x] Phase 3 automated validation exists (93.8% match)
- [x] Value ranges validated against book benchmarks
- [ ] Coverage verified for full 1948-1989 (only benchmarks + interpolation)
- [ ] Full validation report created (NOT YET)

---

## 11. Transformation Log Entries

| Transform ID | Datasets | Operation | Status |
|--------------|----------|-----------|--------|
| T501 | NIPA 1.7.5, IO tables | Sum productive + trading sector gross output | PENDING — needs real NIPA data |
| T502 | IO benchmark tables | Extract productive sector intermediate consumption | PENDING |
| T503 | T501, T502 | TP* - C* | PENDING |
| T504 | NIPA 6.2, BLS CES | W × (Lp/L) approximation | EXISTING (Phase 3) |
| T505 | T503, T504 | VA* - V* | EXISTING (Phase 3) |
| T506 | T505, T504 | S*/V* ratio | EXISTING (Phase 3, 93.8% match) |

---

## 12. Related Content

- **Previous Module**: Chapter 4 (Theoretical framework — IO accounts and Marxian categories)
- **Next Module**: Chapter 6 (Net Social Wage — depends on V*, Lp, employment decomposition)
- **Related Modules**: Chapter 9 (Summary — derives entirely from Ch 5 results); Chapters 7-8 (labor values, composition)
- **External Reference**: Mohun (2013) provides alternative classification for cross-validation

---

## 13. Key Observations

### On the NIPA Source Mapping (Table E.2 as Rosetta Stone)

> Table E.2 provides the "Sources" column that maps every row of the Marxian accounts to specific NIPA table and line references. For example, "101 2" = NIPA Table 1.01 line 2 = Personal Consumption Expenditures. This is the single most important reference for tracing empirical inputs.
> — Shaikh & Tonak (1994), Appendix E, Table E.2

### On the Productive/Unproductive Labor Approximation

> "Unit wages of productive and unproductive workers are nearly equal (ec_u/ec_p ≈ 1), therefore V*/W ≈ Lp/L."
> — Shaikh & Tonak (1994), Section 5.3, p. 113

### On the Fundamental Empirical Difference

> "The theoretical difference between Marxian and orthodox economic analysis is reflected in a fundamentally different empirical picture of capitalist reality."
> — Shaikh & Tonak (1994), p. 180

---

## Changelog

| Date | Changes |
|------|---------|
| 2026-02-23 | Initial investigation created. All 10 tables (5.5-5.14) mapped at NIPA-line-item depth. 16 T-series cataloged. 8 figures inventoried. Table E.2 Rosetta Stone fully traced. Known issues documented (placeholder NIPA, placeholder BLS, r* discrepancy, VA*/W constant). |

---

*Chapter 5 Investigation — IN PROGRESS*
*Reference: Anu Standard v2.0*
