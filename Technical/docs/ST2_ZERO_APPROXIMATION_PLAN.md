# ST2 Zero-Approximation Plan — Every Number From Data

**Date**: 2026-05-09
**Principle**: No hardcoded constants. No "methodology defaults." No magic numbers. Every value in the pipeline comes from a public API fetch, computed from a formula, or interpolated from data. The formulas come from the book. The data comes from APIs. Nothing else.

---

## Current Approximations to Eliminate

| # | What | Current | Replace With | Source |
|---|------|---------|-------------|--------|
| 1 | TP*/GDP ratio | Hardcoded {1947:1.65, 1972:1.35, ...} | Sum of GDP-by-Industry gross output for productive+trading sectors | BEA GDPbyIndustry TableID=15 |
| 2 | C*m/GDP ratio | Hardcoded {1947:0.72, 1972:0.56, ...} | Sum of intermediate inputs for productive sectors from IO Use tables | BEA IO Use tables (already fetched) |
| 3 | Production worker fraction per sector | Hardcoded (mining=0.71, construction=0.65, ...) | BLS CES production workers / total workers per sector | FRED CES*0006 / CES*0001 per sector |
| 4 | ec_p/ec_avg ratio | Hardcoded 0.95 | BLS production worker annual wage / NIPA sector avg compensation | FRED CES*0008×CES*0007×52 / (NIPA 6.2D EC / NIPA 6.5D FEE) |
| 5 | PEP/FEE ratio (self-employed scaling) | Hardcoded 1.16 | NIPA 6.10D (persons engaged) / NIPA 6.5D (FTE) per sector | BEA NIPA T61000D / T60500D |
| 6 | Productive services GNP ratio | Hardcoded 0.587 | NIPA 6.1D GVA of productive service industries / total services GVA | BEA NIPA T60100D |
| 7 | Depreciation (Dp) | MISSING | Consumption of fixed capital × productive ratio | FRED COFC + IO productive ratio |
| 8 | hu/hp hours ratio | Hardcoded 0.99 | BLS total private avg weekly hours / production worker avg weekly hours | FRED CES0500000007 (prod) vs BLS total hours |
| 9 | ecu/ecp wage ratio | Hardcoded 1.01 | Unproductive sector avg compensation / productive sector avg compensation from NIPA 6.2D | BEA NIPA T60200D classified by sector |
| 10 | NSW Group II labor share | Hardcoded via methodology | EC/PI from NIPA 2.1 (already data-driven, OK) | Already correct |

---

## Data Requirements — Complete API Fetch List

### FRED Series (11 series)

| # | Series ID | Description | Used To Eliminate |
|---|-----------|-------------|-------------------|
| 1 | PAYEMS | Total nonfarm employment | Already fetched |
| 2 | GDPDEF | GDP deflator | Already fetched |
| 3 | TCU | Capacity utilization | Already fetched |
| 4 | USTRADE | Trade employment | Already fetched |
| 5 | CEU5500000001 | FIRE employment | Already fetched |
| 6 | CEU9000000001 | Government employment | Already fetched |
| 7 | **COFC** | **Consumption of fixed capital (billions)** | **Approximation #7** |
| 8 | CES0500000008 | Total private production worker hourly earnings | Approximation #4 |
| 9 | CES0500000007 | Total private production worker weekly hours | Approximation #4, #8 |
| 10 | CES3000000008 | Manufacturing production worker hourly earnings | Already fetched |
| 11 | CES3000000007 | Manufacturing production worker weekly hours | Already fetched |

### BEA NIPA Tables (14 tables)

| # | Table | Description | Used To Eliminate |
|---|-------|-------------|-------------------|
| 1 | T10105 | GDP components | Already fetched |
| 2 | T10705 | GDP-GNP-NNP-NI-PI relations | Already fetched |
| 3 | T20100 | Personal income, compensation | Already fetched |
| 4 | T30100 | Govt receipts/expenditures | Already fetched |
| 5 | T30200 | Federal government | Already fetched |
| 6 | T30300 | State/local government | Already fetched |
| 7 | T30700 | Social insurance contributions | Already fetched |
| 8 | T31200 | Social benefits | Already fetched |
| 9 | T31600 | Govt consumption by function | Already fetched |
| 10 | T60200D | Compensation by industry | Already fetched |
| 11 | T60500D | FTE by industry | Already fetched |
| 12 | T60600D | Wages and salaries by industry | Already fetched |
| 13 | **T60100D** | **GDP (value added) by industry** | **Approximation #6** |
| 14 | **T61000D** | **Persons engaged in production by industry** | **Approximation #5** |

### BEA GDP-by-Industry (1 dataset)

| # | Dataset | TableID | Description | Used To Eliminate |
|---|---------|---------|-------------|-------------------|
| 1 | **GDPbyIndustry** | **15** | **Gross output by industry (NAICS, 1997+)** | **Approximation #1** |

### BEA IO Benchmark Tables (already fetched)

5 NAICS years (1997-2017), Use + Requirements tables. Used for approximation #2 (C*m from IO intermediate inputs).

### BEA Fixed Assets (already fetched)

FAAt401. Used for K and K*.

---

## Implementation Steps — Zero Approximation

### Step Z1: Fetch Missing Data (1 hour)

Add 4 new fetches to the pipeline:

```python
# In nickydata/run.py fetch phase:

# FRED
data["cofc"] = fred.fetch("COFC", keys["fred"], min_year=1929)  # depreciation

# BEA NIPA
"T60100D": "GDP by industry (value added)"  # for productive services ratio
"T61000D": "Persons engaged in production by industry"  # for PEP/FEE

# BEA GDP-by-Industry
data["gdp_by_industry"] = bea_gdpbi.fetch(keys["bea"], table_id=15)  # gross output
```

Write `nickydata/fetch/bea_gdpbi.py`:
```python
def fetch(api_key, table_id=15, frequency="A", year="ALL", industry="ALL"):
    """Fetch BEA GDP-by-Industry gross output data."""
    params = {
        "UserID": api_key, "method": "GetData",
        "DataSetName": "GDPbyIndustry",
        "TableID": str(table_id),
        "Frequency": frequency, "Year": year,
        "Industry": industry, "ResultFormat": "JSON",
    }
    ...
```

### Step Z2: Replace TP* Approximation with GDP-by-Industry Data (1.5 hours)

**Current**: `tp_star = gdp × hardcoded_ratio`

**New**: For 1997-2024:
```python
# Parse GDP-by-Industry gross output
# Classify each industry using methodology.json NAICS classification
# TP* = sum of gross_output[j] for j in productive + trading
# C*m = sum of intermediate_inputs[j] for j in productive
#       (intermediate = gross_output - value_added, from same dataset)

for industry in gdp_by_industry:
    code = industry["IndustrySortOrder"]  # or IndustryDescription
    cls = classify_naics(code)
    if cls in ("productive", "trading"):
        tp_star[yr] += industry["DataValue"]  # gross output
    if cls == "productive":
        # intermediate inputs = gross output - value added
        # value added from Table T60100D
        va = nipa_61[industry][yr]
        cm_star[yr] += industry["DataValue"] - va
```

For 1947-1996: interpolate TP*/GDP and C*m/GDP ratios from IO benchmarks (1947-1977 SIC + 1997 NAICS). NO hardcoded constants — the ratios come from actual IO data at each benchmark year, linearly interpolated between them.

### Step Z3: Replace Depreciation Approximation with FRED COFC (30 min)

```python
cofc = data["cofc"]  # FRED COFC, billions, annual
productive_ratio = io_productive_ratios  # from IO benchmarks (data, not constant)

dp = cofc * productive_ratio  # depreciation of productive capital
va_star = gfp_star - dp
s_star = va_star - v_star
```

### Step Z4: Replace PEP/FEE Ratio with NIPA Data (30 min)

**Current**: `total_wages = total_comp * 1.16`

**New**:
```python
# NIPA T61000D: Persons engaged in production (PEP) by industry
# NIPA T60500D: Full-time equivalent employees (FEE) by industry
# PEP/FEE ratio varies by sector and year

pep = parse_by_industry(nipa_T61000D)
fee = parse_by_industry(nipa_T60500D)

for yr in years:
    pep_yr = sum(pep[yr][j] for j in productive_sectors)
    fee_yr = sum(fee[yr][j] for j in productive_sectors)
    pep_fee_ratio[yr] = pep_yr / fee_yr  # typically 1.10-1.20

total_wages[yr] = total_comp[yr] * pep_fee_ratio[yr]
```

### Step Z5: Replace Production Worker Fraction with BLS Data (30 min)

**Current**: `pw_default = {"mining": 0.71, "construction": 0.65, ...}`

**New**: For sectors with BLS data (mining, construction, manufacturing):
```python
pw_ratio[sector][yr] = bls_counts[sector][yr] / bls_total[sector][yr]
```

For sectors WITHOUT BLS data (services, transport, utilities, agriculture):
```python
# Use NIPA 6.1D to compute productive services fraction:
# productive_services_gva / total_services_gva
nipa_61 = parse_by_industry(nipa_T60100D)
productive_service_lines = [73, 74, 79, 82, 85]  # education, health, arts, accommodation, other
total_service_lines = [65, 69, 70, 73, 74, 79, 82, 85]  # all services including professional/admin

for yr in years:
    gva_productive_services = sum(nipa_61[yr][ln] for ln in productive_service_lines)
    gva_total_services = sum(nipa_61[yr][ln] for ln in total_service_lines)
    service_ratio[yr] = gva_productive_services / gva_total_services
```

For agriculture: use mining ratio (same as book footnote e — but from DATA, not constant).
For government enterprises: use weighted average of private sectors (same as book footnote f — from DATA).

### Step Z6: Replace ec_p/ec_avg with BLS Wage Data (30 min)

**Current**: hardcoded 0.95

**New**:
```python
# BLS production worker annual wage
wp = bls_wages["total_private"]  # CES0500000008 × CES0500000007 × 52

# NIPA average compensation per worker
ec_avg = nipa_T20100["Compensation of employees"] / payems  # dollars per worker per year

# Ratio (varies by year, typically 0.80-0.90)
ecp_ec_ratio = wp / ec_avg
```

### Step Z7: Replace hu/hp and ecu/ecp with Data (30 min)

**hu/hp** (hours ratio):
```python
# Total average weekly hours: NIPA T60400D or BLS CES total
# Production worker weekly hours: CES0500000007

h_total = ...  # from NIPA or BLS
h_prod = bls_hours["total_private"]  # CES0500000007

hu_hp = (h_total * L - h_prod * Lp) / ((L - Lp) * h_prod)
# This uses: H_total = hu*Lu + hp*Lp → hu = (H_total - hp*Lp)/Lu
```

**ecu/ecp** (wage ratio):
```python
# From NIPA 6.2D: classify sectors as productive vs unproductive
# Compute average compensation per worker for each class

ec_productive = sum(EC[j] for j in productive_sectors)
fee_productive = sum(FEE[j] for j in productive_sectors)
ec_unproductive = sum(EC[j] for j in unproductive_sectors)
fee_unproductive = sum(FEE[j] for j in unproductive_sectors)

ecp = ec_productive / fee_productive
ecu = ec_unproductive / fee_unproductive
ecu_ecp_ratio = ecu / ecp
```

### Step Z8: Compute V* with Zero Approximations (1 hour)

The final V* formula, fully data-driven:

```python
def compute_v_star(yr, data, methodology):
    # For each productive sector j:
    v_star_total = 0
    
    for j in productive_sectors:
        if j has BLS wage data:
            # BLS production worker annual wage × supplements adjustment
            wp_j = bls_earnings[j][yr] * bls_hours[j][yr] * 52  # $/year
            x_j = nipa_EC[j][yr] / nipa_WS[j][yr]  # supplements ratio (EC/WS)
            ecp_j = wp_j * x_j
            
            # BLS production worker count
            lp_j = bls_counts[j][yr]
            
        elif j is a service sector:
            # Services: average sector compensation (book methodology)
            ecp_j = nipa_EC[j][yr] / nipa_FEE[j][yr] * 1000  # $/year
            
            # Productive employment: GNP ratio (from NIPA 6.1D data, NOT constant)
            gva_productive = nipa_GVA[productive_service_lines][yr]
            gva_total = nipa_GVA[all_service_lines][yr]
            service_ratio = gva_productive / gva_total
            lp_j = nipa_FEE[j][yr] * service_ratio
            
        else:
            # Agriculture, utilities, transport, govt enterprises
            # Use sector average × production worker ratio from nearest sector with data
            ecp_j = nipa_EC[j][yr] / nipa_FEE[j][yr] * 1000
            lp_j = nipa_FEE[j][yr] * pw_ratio_from_bls_data[closest_sector][yr]
        
        # Self-employed scaling (from NIPA data, NOT constant)
        pep_j = nipa_PEP[j][yr]
        fee_j = nipa_FEE[j][yr]
        self_employed_factor = pep_j / fee_j if fee_j > 0 else 1.0
        
        v_star_j = ecp_j * lp_j * self_employed_factor / 1e6  # to billions
        v_star_total += v_star_j
    
    return v_star_total
```

### Step Z9: Full Pipeline Assembly (1 hour)

Wire all data-driven components into the pipeline:

1. `total_product.py`: TP* from GDP-by-Industry, C*m from IO intermediate inputs
2. `variable_capital.py`: V* from sector-by-sector with all-data formula (Step Z8)
3. S* = VA* - V* where VA* = GFP* - Dp (depreciation from FRED COFC × IO ratio)
4. e = S*/V* (all components data-driven)
5. Employment: Lp/L from BLS data, no hardcoded fractions
6. Analytical: eu computed from data-driven ecu/ecp and hu/hp

### Step Z10: Validation Against Book (1 hour)

Compare every series at every benchmark year:

```
Year  TP*_ours  TP*_book  gap    V*_ours  V*_book  gap    e_ours  e_book  gap
1948  xxx       446.2     x%     xxx      88.4     x%     x.xx    1.70    x%
1958  xxx       711.7     x%     xxx      127.7    x%     x.xx    2.01    x%
1972  xxx       1728.4    x%     xxx      324.3    x%     x.xx    1.99    x%
1989  xxx       7641.8    x%     xxx      1206.4   x%     x.xx    2.44    x%
```

Target: all within 5% at benchmark years, correct rising trajectory for e.

Document remaining gaps as "NIPA vintage differences" with the vintage_analysis.json evidence.

---

## What "Zero Approximation" Means

After this plan, the pipeline has:

- **ZERO hardcoded ratios** — every ratio computed from fetched data
- **ZERO "methodology constants"** — methodology.json has FORMULAS and CLASSIFICATIONS only, no numeric defaults
- **ZERO "calibration parameters"** — no 0.95, 0.587, 1.16, 0.71, 0.65 anywhere in code
- **Full data provenance** — every number traces to a specific FRED series, BEA NIPA line, or IO benchmark

The ONLY thing the pipeline takes as given:
1. **The sector classification** (which industries are productive/trading/unproductive) — this IS the book's methodology
2. **The formulas** (TP* = sum GO_productive, S* = VA* - V*, etc.) — this IS the book's contribution
3. **API keys** — the user's FRED and BEA credentials

Everything else is computed from public data.

---

## Effort Summary

| Step | What | Hours |
|------|------|-------|
| Z1 | Fetch COFC + NIPA 6.1D/6.10D + GDPbyIndustry | 1.0 |
| Z2 | TP*/C*m from GDP-by-Industry | 1.5 |
| Z3 | Depreciation from COFC | 0.5 |
| Z4 | PEP/FEE from NIPA 6.10D/6.5D | 0.5 |
| Z5 | Production worker fraction from BLS | 0.5 |
| Z6 | ec_p/ec_avg from BLS wages | 0.5 |
| Z7 | hu/hp and ecu/ecp from BLS/NIPA | 0.5 |
| Z8 | V* full data-driven assembly | 1.0 |
| Z9 | Pipeline assembly | 1.0 |
| Z10 | Validation | 1.0 |
| **Total** | | **~8 hours** |

---

## After This Plan

The `nickydata/` package is a ZERO-APPROXIMATION implementation of Shaikh & Tonak (1994):
- Clone → add keys → run → get Marxian national accounts from 1947-2024
- Every number from a public API
- Every formula from the published methodology
- Every sector classification from the book's Appendix F
- Zero hardcoded parameters
- Full vintage documentation
- Validation against the book's published values

This is what a replication package should be.

---

*Plan authored 2026-05-09.*
