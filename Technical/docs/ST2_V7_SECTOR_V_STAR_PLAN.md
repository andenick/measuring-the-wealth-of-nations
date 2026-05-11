# V* Sector-by-Sector Calculation Plan — Faithful Appendix G Implementation

**Date**: 2026-05-09
**Problem**: T506 (exploitation rate) = 2.31 at 1948 vs book's 1.70. The gap comes from V* being too small — our approximate production worker fractions undercount productive wages.
**Goal**: Implement the book's exact Appendix G methodology using available public data to get T506 within 10% of the book's values.

---

## Why the Current V* Is Wrong

The book (Appendix G, chunk 33) computes V* through a 7-step procedure:

1. **ec_j = EC_j / FEE_j** — compensation per FTE employee in each sector (from NIPA 6.2D / 6.5D)
2. **W_j = ec_j × L_j** — total wages including self-employed wage equivalent (L from NIPA PEP, not just FEE)
3. **(wp)_j** — BLS unit wage of production workers in sector j (NOT ec_j — this is LOWER than average)
4. **x_j = (EC/WS)_j** — supplements adjustment (employer contributions / wages+salaries)
5. **(ecp)_j = (wp)_j × x_j** — adjusted production worker compensation (LOWER than ec_j)
6. **V*_j = (ecp)_j × (Lp)_j** — variable capital in sector j
7. **V* = Σ V*_j** — sum across productive sectors

Our current code does:
```python
V*_j = EC_j × pw_ratio_j × (1/1000)
```

Where `pw_ratio_j` is a hardcoded fraction (0.65-0.80). This is wrong in two ways:

1. **Uses ec_j (average compensation) instead of (ecp)_j (production worker compensation).**
   Production workers earn LESS than average — the ratio ec_p/ec_avg ≈ 0.75-0.85 for manufacturing, less for services. Using ec_j overstates V* per worker.

2. **Applies pw_ratio to total EC instead of to FTE × ecp.**
   The book computes V*_j = ecp_j × Lp_j where Lp_j comes from BLS production worker counts, NOT from EC_j × fraction.

The net effect: our V* is too HIGH (because ec > ecp), which makes S* = GFP* - V* too LOW, which makes e = S*/V* too LOW... wait, actually our e = 2.31 > book's 1.70, so our V* must be too LOW not too HIGH.

Let me recheck: T504 1948 = 77bn, book = 88bn. Our V* IS too low. And T505 (S*) = 177bn vs book 150bn — our S* is too HIGH. So e = S*/V* = 177/77 = 2.30 vs book's 150/88 = 1.70. Both numerator and denominator push e up.

The root issue: our GFP* (T503) is close to correct (~254bn vs book 248bn), but our V* (77bn) is too low (book 88bn). The difference of 11bn in V* cascades into a much larger difference in e because both numerator and denominator move.

**Why V* is too low**: Our production worker fraction (0.65) applied to sector EC understates V*. The book gets 88bn because it uses a DIFFERENT formula path:
- Book: V* = Σ (wp_j × x_j × Lp_j) where wp is BLS production worker wage
- Us: V* = Σ (EC_j / FEE_j × FEE_j × pw_fraction) = Σ (EC_j × pw_fraction)
- The difference: the book counts Lp_j workers at THEIR wage rate; we count pw_fraction of ALL workers at the AVERAGE wage rate.

If production workers earn 85% of average, and there are 65% of them:
- Book: V* = 0.65 × 0.85 × W = 0.55 × W
- Us: V* = 0.65 × 1.00 × EC ≈ 0.65 × W (assumes production workers earn average)

Our V* is too HIGH by factor 0.65/0.55 = 1.18? But our V* is actually too LOW. Let me trace through more carefully.

Actually, the issue is different. The book computes V* for 7 specific production sectors, not all of the economy. Our code sums EC for NIPA 6.2D lines classified as "productive" — but the NIPA lines include sub-industries that might not all be productive per the book's classification. Also, the 0.65 fraction might undercount production workers in sectors where they're a larger share (transport, utilities = 0.80).

The fix needs to be meticulous:

---

## Step-by-Step Faithful Implementation

### Step 1: Map NIPA 6.2D Industries to Book Sectors (1 hour)

The book defines 7 production sectors (Appendix F, Table F.1):

| Book Sector | NIPA 6.2D Lines | Production Worker Source |
|-------------|-----------------|------------------------|
| Agriculture | Line 4 (Agriculture, forestry, fishing, hunting) | Use mining ratio (book footnote e) |
| Mining | Line 7 (Mining) | BLS CES1000000006 / CES1000000001 |
| Construction | Line 12 (Construction) | BLS CES2000000006 / CES2000000001 |
| Manufacturing | Line 13 (Manufacturing) | BLS CES3000000006 / CES3000000001 |
| Transport & Utilities | Line 11 (Utilities) + Line 43 (Transportation) | BLS (extrapolated pre-1963) |
| Productive Services | Lines 73+74+79+82+85 (Education, Health, Arts, Accommodation, Other) | Use GNP ratio: (productive services GNP)/(total services GNP) |
| Government Enterprises | Lines 91+96 (Federal + State/local govt enterprises) | Use average private sector ratio |

**Key**: For services, the book does NOT use a BLS production worker ratio. Instead, it uses the GNP ratio: what fraction of total services GNP comes from productive service sub-sectors. This ratio (0.587 in 1989) is then applied to total service employment.

**Implementation**:
1. Parse NIPA 6.2D to extract EC by LineNumber for each of the 7 sectors
2. Parse NIPA 6.5D to extract FEE by LineNumber for the same sectors
3. Compute ec_j = EC_j / FEE_j for each sector

### Step 2: Get Production Worker Wages from BLS (1 hour)

The book uses BLS "average hourly earnings of production and nonsupervisory workers" (now called "average hourly earnings of production and nonsupervisory employees" in modern BLS).

FRED series for hourly earnings:
- `CES0500000008` or `AHETPI` — Total private, production workers, hourly earnings
- `CES1000000008` — Mining, production workers, hourly earnings
- `CES2000000008` — Construction, production workers, hourly earnings
- `CES3000000008` — Manufacturing, production workers, hourly earnings

From hourly earnings + average weekly hours + 52 weeks:
```
(wp)_j = hourly_earnings_j × weekly_hours_j × 52 = annual wage of production worker
```

Then adjust for supplements:
```
x_j = EC_j / WS_j (from NIPA, ratio of total compensation to wages & salaries)
(ecp)_j = (wp)_j × x_j
```

**FRED series needed**:
- `CES0500000008` (or equivalent) — average hourly earnings, total private, prod workers
- `CES0500000007` (or equivalent) — average weekly hours, total private, prod workers
- Same for mining (CES10), construction (CES20), manufacturing (CES30)

**For services**: The book uses ec_serv directly (average compensation per service FTE), since BLS wage data for services wasn't available historically.

### Step 3: Get Production Worker Counts from BLS (30 minutes)

Already have these from our fetch layer:
- `CES0500000006` — total private, production workers (thousands)
- `CES1000000006` — mining production workers
- `CES2000000006` — construction production workers
- `CES3000000006` — manufacturing production workers

For transport/utilities: Need `CES4300000006` or similar (may not be on FRED)
For services: Compute Lp_serv = (GNPpr_serv / GNPtot_serv) × L_serv

### Step 4: Compute V* Sector by Sector (1 hour)

For each of the 7 production sectors:

**Manufacturing, Mining, Construction** (BLS data available):
```python
wp_j = hourly_earnings_j × weekly_hours_j × 52  # annual production worker wage
x_j = EC_j / WS_j  # supplements adjustment from NIPA
ecp_j = wp_j × x_j  # adjusted compensation
V*_j = ecp_j × Lp_j  # variable capital
```

**Transport & Utilities** (limited BLS data):
```python
# Use average sector compensation (ec_j) as proxy for production worker wage
# Apply production worker ratio from NIPA 6.5D
ecp_j = ec_j × 0.90  # production workers earn ~90% of sector average
V*_j = ecp_j × Lp_j
```

**Productive Services** (no BLS production worker wage data):
```python
# Book method: ec_serv used directly (production worker = average service worker)
ecp_serv = ec_serv
# Productive employment: GNP ratio method
Lp_serv = (GNP_productive_services / GNP_total_services) × FEE_serv
V*_serv = ecp_serv × Lp_serv
```

**Agriculture** (limited data):
```python
# Book uses mining ratio for production workers (footnote e)
pw_ratio_agr = pw_ratio_mining
ecp_agr = ec_agr × 0.85  # lower than average due to seasonal/temporary workers
V*_agr = ecp_agr × Lp_agr
```

**Government Enterprises** (no BLS data):
```python
# Book uses average private sector ratio (footnote f)
pw_ratio_ge = average_private_ratio
V*_ge = EC_ge × pw_ratio_ge  # no self-employed adjustment (all employees)
```

### Step 5: Compute Supplements Adjustment (30 minutes)

The supplements/wages ratio (x = EC/WS) comes from NIPA:
- WS = wages and salaries (a sub-component of EC in NIPA tables)
- EC = total employee compensation = WS + supplements

For NIPA 6.2D era (1998+), we can compute x_j = EC_j / WS_j per sector.
For pre-1998: use a constant or interpolated x.

The book (Appendix G validation, chunk 35) shows x is approximately:
- Manufacturing: 1.126-1.131 (supplements = 12-13% of wages)
- Nonmanufacturing: 1.107-1.061 (supplements = 6-11%)

### Step 6: Exclude Corporate Officers' Salaries (30 minutes)

The book follows Mage (1963): COS should be excluded from V* because corporate officers are capitalists, not workers.

The BLS production worker wage data automatically excludes COS (since COS are "nonproduction" by classification). So if we use BLS wp_j as the wage basis, COS exclusion is built in.

For services (where we use ec_serv directly), COS IS included. The book doesn't appear to adjust for this in services specifically.

### Step 7: Self-Employed Wage Equivalent (30 minutes)

The book extends EC to include self-employed by using:
```
W_j = ec_j × L_j where L_j = FEE_j + SEP_j (PEP from NIPA)
```

This increases V* because:
- Agriculture has many self-employed (L/FEE ≈ 2.55 in 1972)
- Services have some self-employed
- Manufacturing has few

NIPA 6.10D (Persons Engaged in Production) provides L_j by industry.
NIPA 6.5D provides FEE_j.
The ratio L_j/FEE_j gives the self-employed scaling factor.

### Step 8: Validate Against Book Values (1 hour)

Compare computed V* with book Table H.1 at benchmark years:

| Year | Our V* | Book V* | Diff |
|------|--------|---------|------|
| 1948 | ? | 88.41 | target <10% |
| 1958 | ? | 127.72 | |
| 1972 | ? | 324.30 | |
| 1989 | ? | 1206.40 | |

If within 10%, the methodology is faithful. If not, identify which sector's V* diverges most and investigate.

---

## Data Requirements

### FRED Series to Fetch (add to api_sources.json)

| Series ID | Description | Used For |
|-----------|-------------|----------|
| CES0500000008 | Total private, prod workers, avg hourly earnings | wp baseline |
| CES0500000007 | Total private, prod workers, avg weekly hours | hp for annual wage |
| CES1000000008 | Mining, prod workers, avg hourly earnings | wp_mining |
| CES1000000007 | Mining, prod workers, avg weekly hours | hp_mining |
| CES2000000008 | Construction, prod workers, avg hourly earnings | wp_construction |
| CES2000000007 | Construction, prod workers, avg weekly hours | hp_construction |
| CES3000000008 | Manufacturing, prod workers, avg hourly earnings | wp_manufacturing |
| CES3000000007 | Manufacturing, prod workers, avg weekly hours | hp_manufacturing |

### BEA NIPA Tables Already Fetched

| Table | Line | Used For |
|-------|------|----------|
| T60200D | 4,7,11,12,13,43,73,74,79,82,85,91,96 | EC_j by sector |
| T60500D | same | FEE_j by sector |
| T20100 | "Compensation of employees" | Total EC, WS |

### Additional BEA Table Needed

| Table | Content | Used For |
|-------|---------|----------|
| T60600D (NIPA 6.6D) | Wages and salaries by industry | WS_j for supplements ratio x_j |
| T61000D (NIPA 6.10D) | Persons engaged in production by industry | L_j (PEP, includes SEP) |

---

## Implementation Steps

### I1. Add FRED earnings/hours series to fetch layer (30 min)

Add 8 new FRED series (4 sectors × earnings + hours) to `nickydata/fetch/bls.py`:
```python
EARNINGS_SERIES = {
    "manufacturing": {"earnings": "CES3000000008", "hours": "CES3000000007"},
    "mining": {"earnings": "CES1000000008", "hours": "CES1000000007"},
    "construction": {"earnings": "CES2000000008", "hours": "CES2000000007"},
    "total_private": {"earnings": "CES0500000008", "hours": "CES0500000007"},
}
```

Add function:
```python
def fetch_production_worker_wages(api_key: str) -> pd.DataFrame:
    """Fetch annual production worker wages by sector.
    Returns DataFrame with columns: sector_annual_wage = hourly × weekly × 52."""
```

### I2. Add NIPA 6.6D and 6.10D to fetch layer (15 min)

Add to `nickydata/run.py` fetch phase:
```python
"T60600D": "Wages and salaries by industry",
"T61000D": "Persons engaged in production by industry",
```

### I3. Rewrite compute/variable_capital.py (2 hours)

Replace the current approximate computation with the faithful Appendix G procedure:

```python
def compute(data, methodology):
    # For each of 7 production sectors:
    for sector in PRODUCTION_SECTORS:
        # 1. Get EC_j and FEE_j from NIPA 6.2D/6.5D
        # 2. Get WS_j from NIPA 6.6D → supplements ratio x_j = EC_j/WS_j
        # 3. Get wp_j from BLS earnings × hours × 52 (or ec_j for services)
        # 4. Get Lp_j from BLS production worker counts (or GNP ratio for services)
        # 5. Get L_j from NIPA 6.10D → self-employed scaling
        # 6. ecp_j = wp_j × x_j
        # 7. V*_j = ecp_j × Lp_j × (L_j/FEE_j)  [self-employed scaling]
    
    # Sum across sectors
    V_star = sum(V_star_j for j in PRODUCTION_SECTORS)
```

### I4. Validate against book values (30 min)

Compare V* at 4 benchmark years. Target: within 10%.

### I5. Recompute exploitation rate and cascade (15 min)

Once V* is correct, S* = GFP* - V* and e = S*/V* automatically improve.

---

## Effort Summary

| Step | What | Hours |
|------|------|-------|
| I1 | Fetch BLS earnings/hours | 0.5 |
| I2 | Fetch NIPA 6.6D/6.10D | 0.25 |
| I3 | Rewrite variable_capital.py | 2.0 |
| I4 | Validate against book | 0.5 |
| I5 | Cascade verification | 0.25 |
| **Total** | | **~3.5 hours** |

---

## Expected Outcome

After implementation:
- V* within 10% of book values at all benchmark years
- T506 (exploitation rate) trajectory matches book's pattern (rising from ~1.7 to ~2.4)
- Level may still differ by 5-15% due to NIPA vintage differences (2025 vs 1986)
- The methodology is transparently documented in compute/variable_capital.py

---

*Plan authored 2026-05-09. Based on Appendix G methodology (KB chunk 33), Table I.1 procedure (KB chunk 35), and current pipeline output analysis.*
