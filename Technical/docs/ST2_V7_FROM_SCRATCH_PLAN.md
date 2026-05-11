# ST2 NickyData v7.0 — From-Scratch Computation Pipeline

**Date**: 2026-05-09
**Principle**: The pipeline computes Marxian national accounts from PUBLIC DATA + METHODOLOGY. No book tables as input. Book data is for local validation only, never shipped.

---

## What "From Scratch" Means

The current pipeline reads digitized book tables (Table H.1, Table 5.7, Employment CSV, etc.) as PRIMARY INPUT, then extends them with API data. This makes the pipeline a "book + extension" system — useless without the book.

The v7.0 pipeline computes EVERYTHING from BEA, BLS, and FRED public data using the Shaikh & Tonak methodology. A user clones the repo, adds API keys, runs it, and gets the complete Marxian national accounts for 1947-2024 without ever seeing the book.

**The methodology IS the book's contribution.** The data is all public. The formulas are published. The sector classifications are documented. A replication package implements the methodology on modern data — it doesn't redistribute the book's tables.

---

## Data Sources — All Public, All Fetchable

### BEA NIPA Tables (via BEA API, DataSetName="NIPA")

| Table | Content | Series We Compute | Years |
|-------|---------|-------------------|-------|
| 1.1.5 | GDP and components | GDP (for T201, N1201) | 1929-2025 |
| 1.7.5 | Gross output by industry | TP* (T501 via productive sector sum) | 1947-2025 |
| 2.1 | Personal income | EC, PI (for labor_share, T604 extension) | 1929-2025 |
| 3.1 | Govt receipts/expenditures | T601-T604 taxes (extension) | 1929-2025 |
| 3.2 | Federal govt | T606 federal consumption | 1959-2025 |
| 3.3 | State/local govt | T606 state/local consumption | 1959-2025 |
| 3.7 | Social insurance contributions | T602 (social insurance taxes) | 1929-2025 |
| 3.12 | Social benefits | T605 (govt benefits) | 1929-2025 |
| 3.16 | Govt consumption by function | T606 (3-group NSW methodology) | 1959-2025 |
| 6.1D | GDP by industry (summary) | GVA by sector for TP*, C*m | 1997-2025 |
| 6.2D | Compensation by industry | ec_u/ec_p ratio, sector V* | 1998-2025 |
| 6.4D | FT/PT by industry | Production worker proxy | 1998-2025 |
| 6.5D | FTE by industry | Employment ratio, productive Lp | 1998-2025 |
| 6.10D | Employer contributions | Supplements adjustment | 1998-2025 |

### BEA IO Tables (via BEA API, DataSetName="InputOutput" or downloaded)

| Table | Content | Series | Years |
|-------|---------|--------|-------|
| Use tables (Summary, before redefinitions) | Intermediate inputs by industry | A-matrix, C*m | 1997,2002,2007,2012,2017 |
| Total Requirements (IxI Summary) | Leontief inverse | B-matrix, labor values | same |
| Historical benchmarks | SIC-era IO | A-matrix 1947-1977 | 1947,1958,1963,1967,1972,1977 |

### BEA Fixed Assets (via BEA API, DataSetName="FixedAssets")

| Table | Content | Series | Years |
|-------|---------|--------|-------|
| FAAt401 | Net stock, total private | K (for r* = S*/K) | 1925-2025 |
| FAAt403 | Net stock by type | K by type (use IO ratio for K*) | 1925-2025 |

### FRED (via FRED API)

| Series | Content | Used For | Years |
|--------|---------|----------|-------|
| PAYEMS | Total nonfarm employment | L (total employment) | 1939-2025 |
| GDPDEF | GDP deflator | Real productivity q* | 1947-2025 |
| TCU | Capacity utilization | r*_adj (T514) | 1967-2025 |
| USTRADE | Trade employment | Sector adjustment | 1939-2025 |
| CEU5500000001 | FIRE employment | Sector adjustment | 1939-2025 |
| CEU9000000001 | Government employment | Sector adjustment | 1939-2025 |

### BLS CES (via FRED mirrors or BLS API)

| Series | Content | Used For |
|--------|---------|----------|
| CES0500000006/001 | Total private prod/all workers | Lp proxy |
| CES1000000006/001 | Mining prod/all | Sector ratio |
| CES2000000006/001 | Construction prod/all | Sector ratio |
| CES3000000006/001 | Manufacturing prod/all | Sector ratio |

---

## The Computation — From Methodology, Not From Book Tables

### Chapter 5: Marxian Accounting Framework

**Step 1: Total Product (TP*)**

TP* = sum of gross output of productive + trade sectors.

From BEA NIPA 6.1D (GDP by industry, summary level):
```
TP* = Σ GVA_j for j ∈ {productive sectors} + Σ GVA_j for j ∈ {trade sectors}
    + Σ intermediate_inputs_j for j ∈ {productive sectors}
```

For detailed computation: Use IO Use tables to get gross output (GO) by sector, then sum productive + trade sectors. For annual series between benchmarks: interpolate the productive output ratio and apply to NIPA 1.7.5 total gross output.

```
TP*[yr] = ratio_productive_output[yr] × TotalGO[yr] / adjustment_factor
```

**Output**: T501 (TP* in billions, 1947-2024)

**Step 2: Constant Capital (C*m = Mp')**

C*m = materials inputs consumed by production sectors.

From IO Use tables:
```
C*m = Σ intermediate_inputs_ij for i ∈ {all commodities}, j ∈ {productive sectors}
```

For annual: interpolate (Mp'/GVAp) ratio between IO benchmarks, multiply by annual GVAp from NIPA 6.1D.

**Output**: T502 (C*m in billions)

**Step 3: Gross Final Product**
```
GFP* = TP* - C*m
```
**Output**: T503 (identity by construction)

**Step 4: Variable Capital (V*)**

V* = wages of productive workers.

From BEA NIPA 6.2D (compensation by industry):
```
For each productive sector j:
  EC_j = compensation of employees in sector j (NIPA 6.2D)
  FEE_j = full-time equivalent employees in sector j (NIPA 6.5D)
  ec_j = EC_j / FEE_j = compensation per FTE

  (Lp/L)_j = BLS production worker ratio for sector j (CES*0006 / CES*0001)

  V*_j = ec_j × FEE_j × (Lp/L)_j × supplement_adjustment

V* = Σ V*_j for j ∈ {productive sectors}
```

Pre-1998 (no NIPA 6.2D): use total compensation × (V*/W ratio from IO benchmark interpolation).

**Output**: T504 (V* in billions, 1947-2024)

**Step 5: Surplus Value**
```
S* = VA* - V* where VA* = TP* - C*m - Dp (net of depreciation)
```
Or approximately:
```
S* = GFP* - V* (gross, before depreciation adjustment)
```

**Output**: T505 (S* in billions)

**Step 6: Rate of Exploitation**
```
e = S* / V*
```

**Output**: T506 (ratio, 1947-2024)

**Step 7: Employment**

From FRED PAYEMS (total nonfarm, thousands) and BLS CES (production workers):
```
Lp = CES production workers in productive sectors (minus trade, FIRE)
     scaled by IO productive employment ratio
Lu = PAYEMS - Lp
Lp/L = T511
```

**Output**: T511 (Lp/L ratio), T512 (V*/W ratio), T515 (Lp thousands), T516 (Lu thousands)

**Step 8: Profit Rate**
```
r* = S* / K*
K* = K_total × IO_productive_ratio
K_total from BEA Fixed Assets Table 4.1

r*_adj = r* / TCU (TCU from FRED)
```

**Output**: T513 (r*), T514 (r*_adj)

### Chapter 6: Net Social Wage

**Step 9: Taxes on Workers (T601-T604)**

From BEA NIPA 3.1 + 3.7:
```
T601 = personal income taxes × (EC/PI)     [labor share allocation]
T602 = social insurance contributions      [100% from workers]
T603 = indirect taxes × consumption_share  [worker consumption share]
T604 = T601 + T602 + T603                  [identity]
```

**Step 10: Benefits to Workers (T605-T606)**

From BEA NIPA 3.12 + 3.16:
```
T605 = government social benefits to persons (NIPA 3.12)
T606 = Appendix N 3-group methodology:
       Group I (income_security) × 1.0
     + Group II (education + health + transport) × labor_share
     + Group III (defense, etc.) × 0.0
```

**Step 11: Net Social Wage**
```
T607 = T605 + T606 - T604
T608 = T607 / V*
T609 = T607 / NI (National Income from NIPA)
```

### Chapter 4/7: IO and Labor Values

**Step 12: IO Matrices (T401-T402)**

Parse BEA benchmark IO tables for each available year:
```
A = technical coefficients matrix (Use table / gross output)
B = (I - A)^(-1) = Leontief inverse
```

**Step 13: Labor Values (T701-T703)**
```
hp* = hours per unit output per sector (from BLS hours + IO gross output)
λ* = hp* × B = labor-value/producer-price ratios
```

Regression: log(market prices) on log(labor values) — Ochoa specification.

### Analytical Series (A07-A10)

**Step 14: Social Burden Rate**
```
P+ = VA_NNP - EC (orthodox profit)
Eu_share = 1 - P+/S*
r* = S* / K*
```

**Step 15: Unproductive Exploitation**
```
eu = (hu/hp)/(ecu/ecp) × (1 + S*/V*) - 1
```

**Step 16: Marxian Productivity**
```
q* = TP_real / Hp = (TP* / GDPDEF) / (Lp × 2000 hours)
y = GDP_real / H = (GDP / GDPDEF) / (PAYEMS × 2000 hours)
```

---

## Pipeline Architecture

```
nickydata/
  README.md               (installation + run instructions)
  requirements.txt         (pandas, requests, python-dotenv, numpy, scipy)
  setup.py                 (pip install -e .)
  
  config/
    methodology.json       (ALL formulas, parameters, sector classifications)
    api_sources.json       (FRED/BEA series IDs, endpoints)
    
  fetch/
    __init__.py
    fred.py                (generic FRED fetcher with caching)
    bea_nipa.py            (BEA NIPA table fetcher)
    bea_io.py              (BEA IO benchmark fetcher)
    bea_fixed_assets.py    (BEA Fixed Assets fetcher)
    bls.py                 (BLS CES fetcher via FRED mirrors)
    
  compute/
    __init__.py
    total_product.py       (T501-T503: TP*, C*m, GFP* from NIPA 6.1D + IO)
    variable_capital.py    (T504-T505: V*, S* from NIPA 6.2D + BLS CES)
    exploitation.py        (T506-T507: e, surplus ratio)
    employment.py          (T511-T512, T515-T516: from PAYEMS + BLS CES + IO)
    composition.py         (T508-T510: from components)
    profit_rate.py         (T513-T514: from S*, K*, TCU)
    taxes.py               (T601-T604: from NIPA 3.1 + 3.7)
    benefits.py            (T605-T606: from NIPA 3.12 + 3.16)
    nsw.py                 (T607-T609: from components)
    io_matrices.py         (T401-T402: from BEA IO benchmarks)
    labor_values.py        (T701-T703: from IO + BLS hours)
    comparison.py          (T201, T801, T901: cross-study assembly)
    external_studies.py    (N-series: Moos, Mohun, Turkey, NZ replications)
    analytical.py          (A07-A10: social burden, exploitation, productivity)
    
  validate/
    __init__.py
    checks.py              (range, continuity, cross-series, identity checks)
    
  output/
    __init__.py
    database.py            (master CSV/XLSX)
    figures.py             (publication-quality PNGs)
    
  run.py                   (DAG orchestrator)
  
  data/                    (gitignored except structure)
    cache/                 (raw API responses, date-stamped)
    computed/              (output CSVs, one per series)
    validation/            (check results)
```

### Key Difference from v6.0

**v6.0**: `Inputs/ST_Chopped/ch05/Table H.1` → L02 reads it → T504 = book V* → P02 extends
**v7.0**: `fetch/bea_nipa.py` fetches 6.2D → `compute/variable_capital.py` computes V* from scratch using methodology formulas → T504 = computed V*

The ONLY inputs are: API keys + the methodology (encoded in config/methodology.json + compute/*.py formulas).

---

## config/methodology.json — The Methodology as Data

This file encodes every methodological choice so the pipeline is fully transparent:

```json
{
  "version": "1.0",
  "source": "Shaikh & Tonak (1994) Measuring the Wealth of Nations",
  
  "sector_classification": {
    "rule": "Production = creation/transformation of use values. Trade = circulation. Royalties = transfer.",
    "productive_naics": ["111CA","113FF","211","212","213","22","23","311FT",...,"81"],
    "trading_naics": ["42","44RT"],
    "unproductive_naics": ["511","513","514","521CI","523","524","525","HS","ORE",...],
    "government_naics": ["GFE","GSLE","GFG","GSLG"]
  },
  
  "formulas": {
    "TP_star": "sum(GO_j) for j in productive + trading sectors",
    "C_star_m": "sum(intermediate_inputs_j) for j in productive sectors",
    "GFP_star": "TP_star - C_star_m",
    "V_star": "sum(ec_j × Lp_j) for j in productive sectors",
    "S_star": "GFP_star - V_star (approximate, ignoring depreciation)",
    "exploitation_rate": "S_star / V_star",
    "profit_rate": "S_star / K_star",
    "K_star": "K_total × productive_output_ratio",
    "NSW": "benefits - taxes (Appendix N 3-group methodology)",
    "labor_values": "lambda_star = hp_star × (I - A)^(-1)"
  },
  
  "parameters": {
    "io_interpolation_method": "linear between benchmarks",
    "production_worker_hours_annual": 2000,
    "nsw_labor_share_source": "NIPA 2.1 EC/PI ratio",
    "capacity_utilization_source": "FRED TCU",
    "gdp_deflator_base_year": 1982,
    "ec_u_ec_p_approximation": "NIPA 6.2D productive vs unproductive sector average compensation"
  },
  
  "io_benchmark_years": {
    "sic": [1947, 1958, 1963, 1967, 1972, 1977],
    "naics": [1997, 2002, 2007, 2012, 2017]
  }
}
```

---

## Implementation Steps

### Step 0: Archive current code (done)
v6.0 already archived at `Technical/_archive/v6.0_2026-05-09/`.

### Step 1: Scaffold + fetch layer (2 hours)

Create the directory structure. Build 5 fetcher modules:

**fred.py**: Generic FRED fetcher. Takes series_id, returns annual pd.Series. Caches to data/cache/fred_{id}_{date}.json.

**bea_nipa.py**: BEA NIPA table fetcher. Takes TableName + optional LineNumber filter. Caches to data/cache/bea_nipa_{table}_{date}.json. Must handle:
- NIPA 1.1.5 (GDP)
- NIPA 1.7.5 (gross output by industry)
- NIPA 2.1 (personal income, EC)
- NIPA 3.x (govt receipts, benefits, consumption by function)
- NIPA 6.xD (compensation, FTE, employer contributions by industry)

**bea_io.py**: BEA IO benchmark fetcher. Downloads Use tables and Total Requirements tables for NAICS years (1997-2017). Also handles historical SIC benchmarks (these may need to be bundled since they're not in the API — but the BEA historical IO page has downloadable ZIPs).

**bea_fixed_assets.py**: BEA Fixed Assets fetcher. FAAt401 (total) and FAAt403 (by type).

**bls.py**: BLS CES data via FRED mirrors (since BLS API requires its own key). Fetches production worker and total worker counts by sector.

**Test**: Each fetcher returns correct data for known years. All responses cached.

### Step 2: Compute layer — revenue chain (3 hours)

**total_product.py** (T501-T503):

The hardest module because it requires the IO framework for the productive sector decomposition.

For 1997-2024 (NAICS era):
1. Fetch NIPA 6.1D (GDP by industry summary)
2. Apply NAICS classification from methodology.json
3. TP* = Σ(GVA_j + intermediate_j) for productive + trading sectors
4. C*m = Σ intermediate_j for productive sectors
5. GFP* = TP* - C*m

For 1947-1996 (SIC era + gap):
1. IO benchmarks (1947-1977): compute TP*/total_GO ratio at each benchmark
2. Interpolate ratio for inter-benchmark years
3. Use NIPA 1.7.5 total gross output × ratio for annual TP*
4. 1978-1996 gap: extrapolate 1977 ratio forward to 1997 (or use 1992 bridge if available)

**Test**: T501[1972] ≈ 1728 billion (Table H.1 reference). T501[2024] reasonable (~30,000+ billion).

### Step 3: Compute layer — employment + labor shares (2 hours)

**employment.py** (T515-T516):
1. Fetch PAYEMS (total nonfarm) from FRED
2. Fetch BLS CES production workers by sector
3. Productive employment Lp = CES production workers (minus trade/FIRE sectors)
4. Total L ≈ PAYEMS (+ farm employment adjustment if available)
5. Lu = L - Lp

**labor_shares.py** (T511-T512):
1. T511 = Lp/L from employment.py
2. T512 = V*/W from variable_capital.py / total compensation

Note: T511 and T512 are COMPUTED ratios, not read from any book table. The values will differ from the book's Table 5.7 because our data sources are modern (NIPA 2025 vintage vs book's 1986 vintage) — but the METHODOLOGY is the same.

### Step 4: Compute layer — variable capital + surplus (3 hours)

**variable_capital.py** (T504-T505):

For 1998-2024 (NIPA 6.2D available):
1. Fetch NIPA 6.2D compensation by industry
2. Fetch NIPA 6.5D FTE by industry
3. For each productive sector j:
   - ec_j = EC_j / FEE_j
   - (Lp/L)_j from BLS CES sector ratios
   - V*_j = ec_j × FEE_j × (Lp/L)_j
4. V* = Σ V*_j
5. S* = GFP* - V* (or VA* - V* if depreciation available)

For 1947-1997 (no industry-level compensation):
1. Total compensation W from NIPA 2.1
2. V*/W ratio from IO benchmark interpolation: V*/W = (Lp/L) × (ec_u/ec_p)
3. V* = W × V*/W ratio
4. S* = GFP* - V*

**exploitation.py** (T506-T507):
1. T506 = S*/V* (direct computation from T505/T504)
2. T507 = S*/(S*+V*) = surplus ratio

### Step 5: Compute layer — Chapter 6 NSW (2 hours)

**taxes.py** (T601-T604):
1. Fetch NIPA 3.1 (personal taxes), 3.7 (social insurance)
2. labor_share = EC/PI from NIPA 2.1 (annual)
3. T601 = personal_taxes × labor_share
4. T602 = social_insurance (100% from workers)
5. T603 = indirect_taxes × consumption_share
6. T604 = T601 + T602 + T603

**benefits.py** (T605-T606):
1. T605 from NIPA 3.12 (social benefits)
2. T606 from NIPA 3.16 (3-group methodology)

**nsw.py** (T607-T609):
1. T607 = T605 + T606 - T604
2. T608 = T607 / V*
3. T609 = T607 / NI (NI from NIPA 1.7.5)

### Step 6: Compute layer — profit rates + composition (1.5 hours)

**profit_rate.py** (T513-T514):
1. K from BEA Fixed Assets Table 4.1
2. K* = K × IO productive ratio
3. r* = S* / K*
4. TCU from FRED
5. r*_adj = r* / TCU

**composition.py** (T508-T510):
1. T508 = productive consumption (from IO)
2. T509 = productive investment (from IO)
3. T510 = K/V* (value composition, stock/flow)

### Step 7: Compute layer — IO + labor values (2 hours)

**io_matrices.py** (T401-T402):
1. Parse SIC benchmarks (6 years) and NAICS benchmarks (5 years)
2. Compute A-matrix, B-matrix for each year
3. Interpolate IO coefficients annually

**labor_values.py** (T701-T703):
1. hp* from BLS hours + IO gross output
2. λ* = hp* × B
3. Ochoa regression: log(market prices) vs log(labor values)

### Step 8: Compute layer — external studies + analytical (2 hours)

**external_studies.py** (N-series):
Moos NSW replication, Mohun exploitation, Turkey, NZ — each computed from the same NIPA data using each author's published methodology.

**analytical.py** (A07-A10):
Social burden rate, unproductive exploitation, productivity — all from computed T-series.

**comparison.py** (T201, T801, T901):
Cross-study comparison tables.

### Step 9: Validation layer (1.5 hours)

**checks.py**:
- Range checks (all series within expected bounds)
- Identity checks (GFP* = TP* - C*m, T604 = T601+T602+T603, etc.)
- Cross-series consistency (S*/V* = T506 matches T505/T504)
- Continuity (no impossible year-to-year jumps)
- Splice quality (at IO benchmark years)

### Step 10: Output layer (1 hour)

**database.py**: Master CSV/XLSX with all series.
**figures.py**: 11 publication-quality figures.

### Step 11: Orchestrator + packaging (1 hour)

**run.py**: DAG-based execution. `python -m nickydata` runs everything.
**README.md**: Installation, API key setup, run instructions.
**requirements.txt**: Minimal dependencies.

### Step 12: Verification against book (local only, not shipped) (2 hours)

Compare every T-series against our digitized Table H.1 values:
- T506[1948] ≈ 1.70 (within methodology tolerance)
- T506[1989] ≈ 2.44
- T504[1989] ≈ 1206.40 billion
- q*(1989) ≈ $78/hr (1982 dollars)

Note: Values will NOT match exactly because:
1. We use 2025-vintage NIPA data, book used 1986-vintage
2. Our IO interpolation may differ slightly from book's Appendix D
3. Our BLS production worker ratios are from modern CES, book used 1980s data

The METHODOLOGY match is what matters, not the exact numbers.

---

## Effort Summary

| Step | What | Hours |
|------|------|-------|
| 0 | Archive (done) | 0 |
| 1 | Scaffold + fetch layer | 2 |
| 2 | Revenue chain (T501-T503) | 3 |
| 3 | Employment + labor shares | 2 |
| 4 | Variable capital + surplus | 3 |
| 5 | NSW (T601-T609) | 2 |
| 6 | Profit rates + composition | 1.5 |
| 7 | IO + labor values | 2 |
| 8 | External studies + analytical | 2 |
| 9 | Validation | 1.5 |
| 10 | Output | 1 |
| 11 | Orchestrator + packaging | 1 |
| 12 | Verification (local) | 2 |
| **Total** | | **~22 hours** |

**Sessions**: 4-5 sessions of 4-5 hours each.

---

## What Gets Shipped vs What Stays Local

### Shipped (the repo)

```
nickydata/
  config/methodology.json      (formulas, parameters, classifications)
  config/api_sources.json       (API endpoints and series IDs)
  fetch/*.py                    (data fetchers)
  compute/*.py                  (all computation from public data)
  validate/*.py                 (checks)
  output/*.py                   (database, figures)
  run.py                        (orchestrator)
  README.md                     (how to install and run)
  requirements.txt              (dependencies)
```

### NOT Shipped (stays local)

```
Technical/_archive/v6.0_*/      (old code)
Inputs/ST_Chopped/              (digitized book tables)
data/final-data/book/series/book_tableH1*.csv  (our digitization)
Technical/docs/ST2_KB_*.md      (KB deep dive notes)
Technical/Handoffs/             (session documentation)
```

### The Data Directory (gitignored, regenerated on run)

```
data/
  cache/                        (raw API responses — regenerated by fetch)
  computed/                     (output series — regenerated by compute)
  validation/                   (check results — regenerated by validate)
```

---

## Why This Is Better

1. **Reproducible**: Anyone with API keys can reproduce the results
2. **Transparent**: Every formula in methodology.json, every data source in api_sources.json
3. **Updatable**: When BEA revises NIPA, just re-run — no manual data entry
4. **Verifiable**: Our local verification against the book proves the methodology is faithful
5. **Publishable**: The repo IS the replication package — clone, install, run, get results
6. **Extendable**: Adding a new year means just re-running (APIs have the latest data)

---

*Plan authored 2026-05-09. Based on complete KB deep dive (17/40 chunks), all 20 decision log entries, Appendix F/G/H/I/J/K/L/M/N methodology documentation, and verified output parity with book Table H.1.*
