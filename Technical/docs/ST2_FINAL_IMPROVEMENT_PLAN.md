# ST2 Final Improvement Plan — Closing the Replication Gap

**Date**: 2026-05-09
**Current state**: nickydata v7.0 from-scratch pipeline, 24 series in 4.9s, V*(1948) within 0.7% of book, e(1948) within 9.1% (pre-fix)
**Diagnosed root causes**: (1) Missing depreciation in S*, (2) V* trajectory doesn't decline with Lp/L, (3) TP* approximated by ratio instead of data
**Target**: e within 3-5% of book at all benchmark years, correct rising trajectory

---

## Fix 1: Add Depreciation to S* Computation (1.5 hours)

### 1.1 Fetch Depreciation Data (30 min)

**What**: Capital consumption of productive fixed capital (Dp) from BEA.

**Sources** (two options):
- **BEA NIPA Table 1.7.5** line for "Consumption of fixed capital" — total economy Dp
- **BEA Fixed Assets Table FAAt401** — has depreciation by type (equipment, structures, IP)

The book's Dp comes from Table E.2 (Appendix E): "Depreciation of productive fixed capital." This is depreciation restricted to PRODUCTIVE sectors only (not trade, not FIRE, not government). For the from-scratch pipeline, use total economy depreciation × productive output ratio as approximation.

**Implementation**:
```python
# In nickydata/fetch/bea_nipa.py or run.py fetch phase:
# Add to NIPA fetch list:
"T10705": "GDP-GNP-NNP-NI-PI relations"  # Line for consumption of fixed capital

# Or fetch from Fixed Assets:
# FAAt401 Line 2 or 3 = Depreciation (capital consumption allowances)
```

**Alternative**: FRED series `COFC` (Consumption of Fixed Capital, billions, annual) — simplest fetch.

### 1.2 Modify S* Computation (30 min)

**Current** (in `compute/variable_capital.py`):
```python
s_star = t503 - v_star  # S* = GFP* - V* (WRONG: no depreciation)
```

**Corrected**:
```python
# VA* = GFP* - Dp (net value added = gross final product - depreciation)
# S* = VA* - V* (surplus value = net value added - variable capital)
dp = fetch("COFC", api_key) / 1e3  # billions
dp_productive = dp * productive_ratio  # restrict to productive sectors
va_star = t503 - dp_productive
s_star = va_star - v_star
```

**Expected impact**: e(1948) drops from 1.855 to ~1.748 (within 2.8% of book's 1.70). At 1989: proportional improvement.

### 1.3 Add VA* as Separate Series (15 min)

Create T5035 or use the T503 slot for VA* (net, not gross):
```python
results["VA_star"] = build_series(va_star, ...)
```

Or keep T503 as GFP* (gross) and add VA* as a new analytical variable in A07.

### 1.4 Validate (15 min)

Check: VA*(1948) ≈ 238.35 (book Table H.1). Our value should be ~254.0 - 9.4×0.82 ≈ 246.3. Gap with book: +3.3% (from TP* being slightly high). Acceptable.

---

## Fix 2: V* Trajectory — Apply Declining Lp/L (2 hours)

### 2.1 Diagnose the Trajectory Inversion (30 min)

**The problem**:
- Book e RISES from 1.70 (1948) to 2.44 (1989): +43%
- Our e FALLS from 1.855 (1948) to 1.42 (1989): -23%
- This is a trajectory INVERSION — qualitatively wrong

**Root cause**: Our V* grows proportionally with EC (total compensation), but the book's V* grows SLOWER because V*/W = (Lp/L) × (ec_p/ec_avg) DECLINES as productive employment's share falls.

In the book:
- V*/W declines from 0.54 (1948) to 0.36 (1989): -33%
- This means V* grows at only ~67% of EC's growth rate
- S* = GFP* - V*, so when V* grows slower, S* grows faster, and e = S*/V* rises

In our pipeline:
- For 1998+ (NIPA 6.2D era): V* = Σ(EC_j × pw_fraction_j) for productive sectors
- The pw_fraction is roughly CONSTANT (~0.65-0.70)
- So V* grows at nearly the same rate as productive-sector EC
- This means V*/GFP* stays roughly constant → e stays roughly constant or declines

**The fix**: V* needs to be modulated by the DECLINING productive labor share (Lp/L).

### 2.2 Compute Lp/L Decline Trajectory (30 min)

From our existing employment.py, T511 = Lp/L shows the productive labor share. In the book, this declines from 0.57 to 0.36 (1948-1989).

For the V* computation:
```python
# For each year:
# V* = W_total × (V*/W)
# where V*/W = (Lp/L) × (ec_p/ec_avg)
#
# If ec_p/ec_avg ≈ 0.95 (production workers earn 95% of average):
# V*/W ≈ Lp/L × 0.95
#
# So V* = W_total × Lp/L × 0.95

# Using our T511 (Lp/L) and NIPA total compensation:
v_star[yr] = total_comp[yr] * t511[yr] * 0.95
```

This replaces the sector-by-sector computation with a simpler formula that captures the declining productive share.

### 2.3 Blend Sector and Ratio Methods (30 min)

For 1998+ where NIPA 6.2D is available:
- Compute V*_sector from sector-level data (current method)
- Compute V*_ratio from total_comp × Lp/L × 0.95
- Take the MINIMUM of the two (sector V* is an upper bound because it includes all compensation in productive sectors, not just production workers)

For pre-1998:
- Use V*_ratio = total_comp × Lp/L × 0.95 (same as current fallback but with the correct Lp/L trajectory)

### 2.4 Validate Trajectory (30 min)

Check that e now RISES from ~1.70 to ~2.44 (matching the book's trajectory):
```
Year  Book e   Our e (pre-fix)  Our e (post-fix)
1948  1.70     1.855            ~1.70-1.75
1967  2.10     1.410            ~1.90-2.00
1989  2.44     1.423            ~2.20-2.40
```

The rising trajectory comes from Lp/L declining (0.57→0.36), which makes V*/W decline, which makes V* grow slower than GFP*, which makes S* grow faster, which makes e rise.

---

## Fix 3: Fetch GDP-by-Industry Gross Output (1.5 hours)

### 3.1 Add BEA GDP-by-Industry Fetch (30 min)

**API call**:
```python
params = {
    "UserID": api_key,
    "method": "GetData",
    "DataSetName": "GDPbyIndustry",
    "TableID": "15",  # Gross output by industry
    "Frequency": "A",
    "Year": "ALL",
    "Industry": "ALL",
    "ResultFormat": "JSON",
}
```

This returns gross output for each NAICS industry, annually from 1997-2024. For pre-1997, continue using the TP*/GDP ratio methodology (book era uses IO benchmarks for these years anyway).

### 3.2 Parse and Classify (30 min)

Apply NAICS classification from methodology.json:
```python
for each industry in GDP-by-Industry:
    if classify(industry) in ["productive", "trading"]:
        tp_star += gross_output[industry]
    if classify(industry) == "productive":
        cm_star += intermediate_inputs[industry]  # if available
```

### 3.3 Replace TP* Ratio Approximation (15 min)

For 1997-2024: use actual GDP-by-Industry gross output sum.
For 1947-1996: keep current TP*/GDP ratio methodology (but calibrate the ratios to match the 1997 transition point).

### 3.4 Validate (15 min)

Check: TP*(1997) from GDP-by-Industry should match the IO-derived TP* at the 1997 benchmark. TP*(2024) should be ~$35-40 trillion.

---

## Fix 4: IO Benchmark Gross Output Parsing (1 hour)

### 4.1 Fix parse_use_matrix to Extract Total Industry Output (30 min)

The BEA IO API returns Use table data with various row codes. The total industry output row should be findable. Currently `parse_use_matrix` looks for "T00TOP", "T018", etc. but these codes may differ in the API format vs downloaded JSON format.

**Method**: Print all unique RowCode values from the API response. Identify the total output row. Update the parser.

### 4.2 Compute Actual Productive Ratios from IO (30 min)

Once total industry output is correctly parsed:
```python
tp_ratio = sum(GO[j] for j in productive+trading) / sum(GO[j] for j in all_industries)
cm_ratio = sum(intermediate[j] for j in productive) / sum(GO[j] for j in all_industries)
```

These replace the hardcoded methodology constants with data-driven ratios.

---

## Fix 5: Year-Varying ec_p/ec_avg from BLS (1 hour)

### 5.1 Compute Production Worker Wage Relative to Average (30 min)

From BLS CES data we already fetch:
```python
# Manufacturing production worker annual wage / average manufacturing wage
wp_mfg = bls_wages["manufacturing"]  # from CES3000000008 × CES3000000007 × 52
ec_mfg = nipa_6_2D[manufacturing_EC] / nipa_6_5D[manufacturing_FEE]

ecp_ec_ratio = wp_mfg / ec_mfg  # should be ~0.80-0.90
```

### 5.2 Apply to V* Formula (30 min)

Instead of hardcoded `0.95`:
```python
v_star[yr] = total_comp[yr] * t511[yr] * ecp_ec_ratio[yr]
```

This makes the formula fully data-driven: V* = W × (Lp/L) × (ec_p/ec_avg) where all three factors come from public data.

---

## Fix 6: Structural Break / Period Analysis (1.5 hours)

### 6.1 Compute Period Means for e (30 min)

After all fixes, compute exploitation rate by period:
```
Golden Age (1948-1973): mean e = ?
Stagflation (1973-1980): mean e = ?
Reagan (1980-1989): mean e = ?
Neoliberal (1989-2000): mean e = ?
Financialization (2000-2008): mean e = ?
Post-GFC (2008-2020): mean e = ?
COVID+ (2020-2024): mean e = ?
```

Compare with book's findings: e rising 1948-1989, with acceleration under Reagan.

### 6.2 Compute Social Burden Rate by Period (30 min)

```
b = (T + Eu) / S* ≈ 1 - P+/S*
```

By period, does b continue rising post-1989? The book shows b = 0.56 → 0.66 (1948-1989).

### 6.3 Compute Productivity Ratios by Period (30 min)

```
q*/y ratio by period: does the Marxian-orthodox productivity gap continue widening?
```

---

## Fix 7: Comprehensive Validation Suite (1 hour)

### 7.1 Identity Checks (15 min)

```python
assert GFP* == TP* - C*m  (within 0.01)
assert S* == VA* - V*      (within 0.01)
assert T604 == T601 + T602 + T603  (within 0.01)
assert T607 == T605 + T606 - T604  (within 0.01)
assert T506 == T505 / T504  (within 0.001)
```

### 7.2 Range Checks (15 min)

```python
assert 0 < TP* < 50000  # billions
assert 0 < V* < 20000
assert 0 < S*
assert 1.0 < e < 5.0  # exploitation rate
assert -0.15 < NSW/V* < 0.15  # net social wage ratio
```

### 7.3 Benchmark Cross-Check (15 min)

Compare with book Table H.1 at 1948, 1958, 1972, 1989. Report deviations.

### 7.4 Khanjian Cross-Validation (15 min)

Check: Our/Khanjian ratio should be ~0.80 (per Section 5.10, Table 5.12).

---

## Fix 8: Documentation and methodology.json Update (30 min)

### 8.1 Update methodology.json

Add:
```json
{
  "formulas": {
    "VA_star": "GFP_star - Dp (depreciation of productive capital)",
    "S_star": "VA_star - V_star (NOT GFP_star - V_star)",
    "Dp": "consumption of fixed capital × productive_ratio",
    "V_star_method": "W_total × (Lp/L) × (ec_p/ec_avg)",
    ...
  },
  "vintage_awareness": {
    "current_vintage": "2025-2026",
    "book_vintage": "BEA (1986)",
    "expected_divergence": "1-5% at benchmark years",
    "alfred_status": "ALFRED does not support annual NIPA. Vintage comparison done qualitatively."
  }
}
```

### 8.2 Update README.md

Add accuracy statement:
```
## Accuracy

At 1948 (the book's starting year):
- TP* within 1.0% of book (Table H.1)
- V* within 0.7% of book
- e (exploitation rate) within 3% after depreciation correction

Values use 2025-vintage NIPA data. The book used 1986-vintage data.
Level differences of 1-5% are expected due to 8 NIPA comprehensive
revisions between 1986 and 2023.
```

---

## Execution Order

```
Fix 1 (depreciation) ──────> Fix 2 (V* trajectory)
                                    |
Fix 3 (GDP-by-Industry) ──────────>|
                                    |
Fix 4 (IO gross output) ──────────>|──> Fix 6 (period analysis)
                                    |
Fix 5 (ec_p/ec_avg) ──────────────>|
                                    |
                                    └──> Fix 7 (validation)
                                              |
                                              └──> Fix 8 (documentation)
```

**Parallel**: Fixes 1, 3, 4, 5 are independent of each other. Fix 2 benefits from 5 (ec_p data). Fix 6 needs all preceding fixes. Fix 7 runs last.

---

## Effort Summary

| Fix | What | Hours | Impact on e Gap |
|-----|------|-------|-----------------|
| 1 | Add depreciation to S* | 1.5 | Closes 65% (9.1% → 3.1%) |
| 2 | V* trajectory (declining Lp/L) | 2.0 | Fixes trajectory inversion |
| 3 | GDP-by-Industry gross output | 1.5 | Improves TP* to <0.5% error |
| 4 | IO gross output parsing | 1.0 | Data-driven productive ratios |
| 5 | Year-varying ec_p/ec_avg | 1.0 | Fully data-driven V* |
| 6 | Period analysis | 1.5 | New empirical findings |
| 7 | Validation suite | 1.0 | Quality assurance |
| 8 | Documentation | 0.5 | Methodology transparency |
| **Total** | | **~10 hours** |

---

## Expected Final State

After all 8 fixes:

| Measure | Before Fixes | After Fixes | Book | Gap |
|---------|-------------|-------------|------|-----|
| V*(1948) | 89.0 | ~89.0 | 88.4 | <1% |
| S*(1948) | 165.0 | ~152 | 149.9 | ~1-2% |
| e(1948) | 1.855 | ~1.72 | 1.70 | ~1-2% |
| e(1989) | 1.42 | ~2.2-2.4 | 2.44 | ~5-10% |
| e trajectory | FALLING | RISING | RISING | Qualitatively correct |
| S*/V* at all years | Wrong trend | Correct trend | Book trend | ±5% |

The pipeline would then produce a qualitatively correct and quantitatively close replication of the book's central finding: the rate of exploitation RISES over the postwar period, driven by the declining share of productive employment.

---

*Plan authored 2026-05-09. Based on component decomposition analysis, vintage comparison, trajectory diagnosis, and 23+ sessions of project knowledge.*
