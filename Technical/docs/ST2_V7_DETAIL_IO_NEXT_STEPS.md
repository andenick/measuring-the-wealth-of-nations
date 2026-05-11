# ST2 NickyData v7.0 — Next Steps Implementation Plan

**Date**: 2026-05-10
**Current state**: 26 computed series, 77-year TP* from detail IO, but V* trajectory inverted
**Central problem**: e falls (2.01→1.46) over 1948-1989 when book shows e rising (1.70→2.44)
**Root cause**: Fallback V* formula uses near-constant T512 ratio instead of sector-level declining comp shares

---

## Phase A: Fix V* (Critical — Single Highest-Leverage Change)

### A1. Extend Sector V* Method to 1948 (2 hours)

**Goal**: Eliminate the fallback formula entirely. Use NIPA T60200D (compensation by industry) for ALL years.

**Discovery**: NIPA Table 6.2D has compensation by industry starting from **1948**. The current code only uses it for 1998+ because that's when the "D" (detailed) variant starts. But the older T60200B and T60200A have the same structure at lower granularity, covering 1948-1997.

**Implementation**:

```python
# In variable_capital.py:
# 1. Fetch T60200A/B (compensation by industry, 1948-1997)
#    - These use broader NAICS/SIC groupings but cover productive sectors
# 2. For each year 1948-2024:
#    V* = sum(EC_j * pw_ratio_j * sep_j) for productive sectors
# 3. pw_ratio from BLS CES (manufacturing, mining, construction)
#    and proxy ratios for services
# 4. NO fallback formula at all
```

**Key insight**: The book's V* declines relative to GFP* because:
- Productive sectors' share of TOTAL compensation declines (structural shift to FIRE)
- This is captured automatically when we sum productive-sector comp × pw_fraction
- No need for any aggregate Lp/L ratio — the sector composition does the work

**Steps**:
1. Check what NIPA tables cover compensation by industry pre-1998:
   - BEA API: `T60200A` (annual, 1929-1997), `T60200B` (broader)
   - Identify available industry lines for 1948-1997
2. Fetch these tables in the pipeline (add to `bea_nipa.py` fetch list)
3. Rewrite `variable_capital.py`:
   - Remove the fallback formula entirely
   - Use sector method for ALL years with available NIPA by-industry comp
   - For years where T60200D isn't available, use T60200A (coarser but same concept)
4. Verify: V*(1948) should be ~88B, and V*/GFP* should DECLINE from 0.36 (1948) to lower values

**Expected outcome**: e now RISES from ~1.70 (1948) to higher values (1989), matching book trajectory.

### A2. Apply Production Worker Wages (ec_p) Not Average (1 hour)

**Goal**: V* should use production-worker-specific compensation, not sector averages.

**Current**: `ecp = ec_j / fee_j * 1000` → sector average comp per FTE.
**Correct**: `ecp = BLS_production_worker_hourly * hours * 52 * supplements_ratio`

**Implementation**:
```python
# For sectors with BLS CES production worker data:
#   manufacturing (CES3000000008 * CES3000000007 * 52)
#   mining (similar)
#   construction (similar)
# Apply supplements ratio: ec_p = ws_p * (EC_sector / WS_sector)
#
# For service sectors without CES production worker data:
#   Use sector average * 0.85 (production workers earn ~85% of average)
#   This 0.85 factor should itself come from data where available
```

**Expected impact**: V* drops ~10-15%, e rises correspondingly.

### A3. Apply PEP/FEE Self-Employed Correction (30 min)

**Goal**: Include proprietors' imputed compensation in V* (book's Appendix G method).

**Current**: `pep_fee = 1.0` (no correction).
**Correct**: PEP (persons engaged in production) / FEE (full-time equivalent employees) from NIPA T61000D / T60500D.

**Implementation**:
```python
# Per sector per year:
sep_j = nipa_pep[j] / nipa_fee[j]  # typically 1.05-1.30
# V* = sum(ecp_j * lp_j * sep_j) for productive sectors
```

**Expected impact**: V* increases ~5-15% (restores the 88.4B for 1948, up from 76.7B).

### A4. Fix Year Range Guard (15 min)

Remove the spurious 2025 data point. Add `if yr > 2024: continue` to the sector loop.

### A5. Validate V* Trajectory (30 min)

After A1-A4, verify:
```
Year   V*      V*/GFP*   Book V*   Book V*/GFP*
1948   ~88     ~0.36     88.4      0.357
1958   ~128    ~0.32     127.7     0.316
1967   ~216    ~0.31     216.3     0.309
1972   ~324    ~0.32     324.3     0.320
1977   ~516    ~0.31     515.8     0.305
1989   ~1206   ~0.28     1206.4    0.276
```

The key check: V*/GFP* should DECLINE over time (production workers get a shrinking share of productive value added).

---

## Phase B: Fix Transition and Validate (1.5 hours)

### B1. Eliminate 1997/1998 Discontinuity (30 min)

With Phase A complete, the sector method covers 1948-2024 continuously. Verify:
- V*(1997) from sector method ~ V*(1998) from sector method (continuous)
- No jump in e at the transition

If a small gap remains (due to NIPA table version change A→D), apply a level-shift correction:
```python
# If V*_A(1997) != V*_D(1998) by more than 5%:
# Compute ratio = V*_D(1998) / V*_A(1998) [same year, different table]
# Apply ratio to all A-table years: V*_corrected = V*_A * ratio
```

### B2. Verify GFP* Continuity at 1989→1990 Transition (30 min)

GFP*/GDP drops from 0.77 (1989, book) to 0.54 (1997, data). Is this:
- Real structural change (FIRE growth 1990-1997)?
- Classification artifact (SIC→NAICS)?

**Test**: Compute GFP*(1997) using the book's BROADER productive definition (all of NAICS 51 as productive, matching SIC 48). If the gap closes significantly, document as classification effect.

### B3. Mark Interpolated Years as Uncertain (15 min)

In the integrated_tp_series output, add a `confidence` column:
- `book_H1` years: "high" (direct measurement)
- `detail_412` years: "high" (direct measurement)
- `interpolated` years: "low" (model-based)

### B4. Cross-Validate Against Mohun (2013) (15 min)

Load `data/user-inputs/mohun_2013/mohun_2013_published_data.csv` and compare:
- Mohun's e trajectory for US
- Our e trajectory for overlapping years
- Document deviations > 10% and hypothesize causes

---

## Phase C: Depreciation and Profit Rate (2 hours)

### C1. Sector-Level Depreciation from NIPA (45 min)

**Current**: `Dp = COFC * productive_ratio` (one aggregate number * fraction).
**Better**: NIPA T60700D or Fixed Assets by industry → sum depreciation for productive sectors only.

**Implementation**:
```python
# Fetch BEA Fixed Assets Table 4.4 (depreciation by industry)
# Or use NIPA Table 6.22D (capital consumption allowances by industry)
# Dp = sum(CCA_j) for j in productive sectors
```

### C2. Compute Profit Rate r* = S*/K* (1 hour)

**K***: Net capital stock of productive sectors from BEA Fixed Assets.
- TableName: `FAAt201` (current-cost net stock) or `FAAt101` (chain-weighted)
- Classify by industry → sum productive sectors → K*

**r***: S* / K* annually.

**Expected trajectory**: r* should decline secularly (a key Marxian prediction). Compare with Dumenil & Levy's published US profit rate series.

### C3. Validate S* = VA* - V* Identity (15 min)

Verify for all years:
```python
assert abs(t505[yr] - (t503[yr] - dp[yr] - t504[yr])) < 0.1  # within rounding
```

---

## Phase D: Labor Values and IO Analysis (2 hours)

### D1. Compute Direct Requirements A-Matrix for All Annual Tables (45 min)

We have IO Use tables for 1997-2024 (annually!). Compute the A-matrix for each year:
```python
A[yr] = Z[yr] / x[yr]  # intermediate flows / gross output per industry
```

Store as annual A-matrices in `data/computed/io_matrices/`.

### D2. Compute Leontief Inverse B = (I - A)^(-1) (15 min)

For each year:
```python
B[yr] = np.linalg.inv(np.eye(n) - A[yr])
```

### D3. Compute Labor Values (30 min)

```python
# hp* = hours of productive labor per $ of output, per industry
# lambda* = hp* @ B  (labor values = direct+indirect labor per unit output)
```

Requires: BLS hours by industry / gross output = labor coefficient vector.

### D4. Compute Prices of Production (30 min)

```python
# p* = (1 + r*) * (c + v)  where c = materials cost, v = labor cost
# Deviation: |p* - market_price| shows transfer of surplus between sectors
```

---

## Phase E: Period Analysis and Write-Up (1.5 hours)

### E1. Compute Period Means Table (30 min)

For all key variables (e, r*, NSW/V*, productive share), compute:
```
Period              Years     Mean e    Mean r*   Prod GO%
Golden Age          1948-73   X.XX      X.XX      XX.X%
Stagflation         1973-80   X.XX      X.XX      XX.X%
Reagan Era          1980-89   X.XX      X.XX      XX.X%
Clinton/Bush        1997-07   X.XX      X.XX      XX.X%
GFC+Recovery        2008-15   X.XX      X.XX      XX.X%
Late Expansion      2016-19   X.XX      X.XX      XX.X%
COVID+Post          2020-24   X.XX      X.XX      XX.X%
```

### E2. Document TP*/GDP < 1.0 Finding (30 min)

Write up the structural finding:
- First time in postwar history: productive GO < GDP
- Quantify: productive share fell 54% -> 46% (1997-2024)
- Interpretation: more than half of US measured economic activity is now in sectors that don't produce use-values (Marxian definition)
- Implications for profit rate, accumulation, crisis theory

### E3. Comparison Table with Other Researchers (30 min)

| Source | Period | e (start) | e (end) | Method |
|--------|--------|-----------|---------|--------|
| Shaikh & Tonak (1994) | 1948-89 | 1.70 | 2.44 | 82 SIC sectors |
| Mohun (2013) | 1964-2010 | ? | ? | New NAICS |
| Moseley (1992) | 1947-87 | ? | ? | Modified |
| Our pipeline | 1948-2024 | X.XX | X.XX | 412 NAICS detail |

---

## Phase F: Fresh Environment Test and Package (1 hour)

### F1. Requirements File (15 min)

Verify `requirements.txt` includes all dependencies:
```
pandas>=2.0
numpy>=1.24
requests>=2.28
python-dotenv>=1.0
```

### F2. Fresh-Env Test (30 min)

```bash
python -m venv test_env
pip install -r requirements.txt
python -m nickydata.run
# Should produce all 26+ series from scratch with only API keys
```

### F3. README Update (15 min)

Update README with:
- Accuracy statement (V* within X% of book at benchmarks)
- Data sources (BEA UnderlyingGDPbyIndustry, FRED, BLS CES, NIPA)
- Key finding (TP*/GDP secular decline)

---

## Execution Order and Dependencies

```
Phase A (V* fix) ──────────────> Phase B (transition fix)
     |                                |
     └──> Phase C (profit rate) ──────┘──> Phase E (period analysis)
                                      |
Phase D (labor values) ───────────────┘──> Phase F (packaging)
```

**Phase A is blocking**: everything else depends on correct V* trajectory.

---

## Effort Summary

| Phase | What | Hours | Priority |
|-------|------|-------|----------|
| A | Fix V* trajectory (sector method all years) | 4.25 | CRITICAL |
| B | Transition fix + validation | 1.5 | HIGH |
| C | Depreciation + profit rate | 2.0 | HIGH |
| D | Labor values + IO analysis | 2.0 | MEDIUM |
| E | Period analysis + write-up | 1.5 | MEDIUM |
| F | Packaging + fresh test | 1.0 | LOW |
| **Total** | | **~12 hours** | |

---

## Success Criteria

After all phases:

| Metric | Current | Target | Book |
|--------|---------|--------|------|
| V*(1948) | 76.7B | ~88B | 88.4B |
| e(1948) | 2.01 | ~1.70 | 1.70 |
| e(1989) | 1.46 | ~2.3-2.5 | 2.44 |
| e trajectory 1948-89 | FALLING | RISING | RISING |
| e(1997-2024) | 0.65-1.23 | 1.2-1.8 | N/A |
| 1997/98 discontinuity | 2x jump | <5% gap | N/A |
| TP*/GDP (2024) | 0.993 | 0.993 | N/A (new finding) |

The central result we need: **e rises from ~1.7 (1948) to ~2.4 (1989), reflecting the declining share of productive-worker compensation in total value added.** Post-1989, e should continue at elevated levels or gradually decline as the productive sector shrinks.

---

*Plan authored 2026-05-10. Based on diagnostic analysis of pipeline output, code review of variable_capital.py, and comparison with book Table H.1.*
