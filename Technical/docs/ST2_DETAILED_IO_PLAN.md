# ST2 Detailed IO Matrices Plan — Maximum Sector Resolution

**Date**: 2026-05-10
**Problem**: Summary-level IO tables (71 NAICS sectors) give TP*/GDP = 0.97 because intra-industry flows are netted out. The book used detailed 82-sector SIC tables giving TP*/GDP = 1.62. We need more sector detail to close the gap.
**Goal**: Fetch the most detailed IO tables available from BEA, for all available years, and recompute all Marxian aggregates at maximum resolution.

---

## BEA IO Data Levels

BEA provides IO tables at 4 levels of detail:

| Level | Industries | Available Years | API Access |
|-------|-----------|-----------------|------------|
| **Sector** | 15 | Annual 1997-2024 | Yes (InputOutput dataset) |
| **Summary** | 71 | Annual 1997-2024 | Yes (InputOutput dataset, what we currently use) |
| **Underlying Summary** | 138 | Benchmark years only (2007, 2012, 2017) | Uncertain |
| **Detail** | 402 | Benchmark years only (2007, 2012, 2017) | Uncertain |

Plus historical:

| Level | Industries | Available Years | API Access |
|-------|-----------|-----------------|------------|
| **SIC Benchmarks** | 85 | 1947, 1958, 1963, 1967, 1972, 1977 | No (downloadable ZIP) |
| **NAICS Benchmarks (detailed)** | 400+ | 1997, 2002, 2007, 2012, 2017 | Yes (benchmark IO dataset) |
| **1992 Bridge** | Both SIC and NAICS | 1992 | Download from bea.gov |

The `TableID` parameter was deprecated in 2018. The current API uses `TableName`. Important: the IO Interactive Data Application has MORE tables than the API.

---

## What We Need to Fetch

### Priority 1: Detail-Level NAICS Benchmarks (1997-2017)

The BEA API InputOutput dataset should have detailed (~400 sector) Use tables for benchmark years. These have MUCH less intra-industry netting, giving gross output that's closer to the true economy-wide GO.

**API discovery call**:
```
GET https://apps.bea.gov/api/data
  ?UserID={key}
  &method=GetParameterValuesFiltered
  &DataSetName=InputOutput
  &TargetParameter=TableName
  &Year=2017
  &ResultFormat=JSON
```

This returns all available TableName values, which should include:
- Use_Detail, Use_Summary, Use_Sector
- Supply_Detail, Supply_Summary, Supply_Sector
- Requirements_Detail, Requirements_Summary, Requirements_Sector

### Priority 2: Underlying Summary Level (138 sectors)

If 402-sector detail is too large or unavailable via API, the 138-sector "underlying summary" is a good middle ground. More than 2× the sector detail of our current 71.

### Priority 3: Annual Summary (71 sectors, all years 1997-2024)

We already have benchmark years (1997, 2002, 2007, 2012, 2017). Fetching ALL years gives annual resolution without interpolation for 1997-2024.

### Priority 4: SIC Historical Benchmarks

Download from [bea.gov/industry/historical-benchmark-input-output-tables](https://www.bea.gov/industry/historical-benchmark-input-output-tables):
- 1947 benchmark (85 sectors)
- 1958 benchmark
- 1963 benchmark
- 1967 benchmark
- 1972 benchmark
- 1977 benchmark
- 1982 benchmark (may have SIC-NAICS bridge)
- 1987 benchmark
- 1992 benchmark (both SIC and NAICS format!)

---

## Implementation Plan

### Step 1: API Discovery — Find All Available IO Tables (30 min)

```python
# nickydata/fetch/bea_io.py — add discovery function

def discover_tables(api_key: str, year: int = 2017) -> list[dict]:
    """List all available IO TableName values for a given year."""
    params = {
        "UserID": api_key,
        "method": "GetParameterValuesFiltered",
        "DataSetName": "InputOutput",
        "TargetParameter": "TableName",
        "Year": str(year),
        "ResultFormat": "JSON",
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    return resp.json()

def discover_years(api_key: str, table_name: str) -> list[int]:
    """List all available years for a given IO table."""
    params = {
        "UserID": api_key,
        "method": "GetParameterValuesFiltered",
        "DataSetName": "InputOutput",
        "TargetParameter": "Year",
        "TableName": table_name,
        "ResultFormat": "JSON",
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    return resp.json()
```

**Output**: Complete list of available table names and years. Expected to find Use tables at sector/summary/underlying/detail levels.

### Step 2: Fetch Detail-Level Use Tables (1 hour)

For each benchmark year (2007, 2012, 2017 at minimum):

```python
def fetch_detail_use(year: int, api_key: str) -> list[dict]:
    """Fetch detail-level (402 sector) Use table."""
    # TableName might be: "Use_Detail_Before_Redefinitions" or similar
    # Discovered in Step 1
    return fetch_naics_io(year, discovered_table_name, api_key)
```

Cache each response. The detail tables may be large (402 × 402 = 161,604 cells × multiple rows/columns = 500K+ records).

### Step 3: Build Detail-Level NAICS Classification (1 hour)

Map each of the ~402 detail industries to productive/trading/unproductive using the book's Appendix F rules:

```python
DETAIL_CLASSIFICATION = {
    # Agriculture
    "1111A0": "productive",  # Oilseed farming
    "1111B0": "productive",  # Grain farming
    ...
    # Manufacturing (100+ industries)
    "311111": "productive",  # Dog and cat food manufacturing
    ...
    # Wholesale trade (single industry)
    "420000": "trading",
    # Retail trade (12+ industries)
    "441000": "trading",     # Motor vehicle dealers
    ...
    # Finance, insurance (20+ industries)
    "521CI": "unproductive", # Federal Reserve and credit intermediation
    ...
    # Professional services
    "541100": "unproductive", # Legal services
    ...
    # Health care (5+ industries)
    "621100": "productive",  # Offices of physicians
    ...
}
```

This classification needs to be built from the BEA industry code descriptions, using the book's Appendix F rules (production = creation/transformation of use values).

### Step 4: Compute Detail-Level Marxian Aggregates (1 hour)

For each benchmark year with detail data:

```python
def compute_detail_aggregates(use_detail, classification):
    """Compute TP*, C*m, GFP* from detail-level IO."""
    A, gross_output = parse_use_matrix(use_detail)

    tp_star = sum(gross_output[j] for j in classification
                  if classification[j] in ("productive", "trading"))
    cm_star = sum(intermediate[j] for j in classification
                  if classification[j] == "productive")
    gfp_star = tp_star - cm_star

    return {"TP_star": tp_star, "C_star_m": cm_star, "GFP_star": gfp_star,
            "TP_GDP_ratio": tp_star / gdp, "n_sectors": len(classification)}
```

Compare with summary-level results to quantify the resolution gain:
- Summary (71 sectors): TP*/GDP ≈ 0.97
- Detail (402 sectors): TP*/GDP ≈ ? (expected 1.4-1.7)

### Step 5: Fetch ALL Annual Summary Tables (1997-2024) (30 min)

Instead of just 5 benchmark years, fetch the summary Use table for EVERY year:

```python
for year in range(1997, 2025):
    records = fetch_naics_io(year, "Use", api_key)
    # Parse and store
```

This eliminates interpolation entirely for 1997-2024.

### Step 6: Download SIC Historical Benchmarks (1 hour)

Manually download from BEA website (not available via API):

```
https://www.bea.gov/industry/historical-benchmark-input-output-tables
```

Files available as ZIP archives:
- 1947, 1958, 1963, 1967, 1972, 1977, 1982, 1987 benchmark IO tables

Store in `nickydata/data/cache/io_sic/`

Add parsing for the SIC format (different from NAICS API format — likely CSV or fixed-width):

```python
def parse_sic_use_table(filepath: Path) -> tuple[pd.DataFrame, pd.Series]:
    """Parse historical SIC benchmark Use table from downloaded file."""
```

### Step 7: Build SIC Sector Classification (30 min)

Map the 85 SIC sectors to productive/trading/unproductive using the book's own classification (which IS for SIC sectors — Appendix F Table F.1):

```python
SIC_CLASSIFICATION = {
    # Agriculture
    1: "productive",   # Livestock
    2: "productive",   # Other agriculture
    ...
    # Manufacturing
    14: "productive",  # Food products
    15: "productive",  # Tobacco
    ...
    # Trade
    69: "trading",     # Wholesale trade
    70: "trading",     # Retail trade
    ...
    # FIRE
    71: "unproductive", # Banking
    72: "unproductive", # Insurance
    ...
    # Services
    77: "productive",   # Health services
    78: "productive",   # Educational services
    ...
    # Government
    85: "government",   # Government
}
```

The book's Appendix F Table F.1 has the EXACT classification for all 85 SIC sectors. We already have this from the KB deep dive.

### Step 8: Compute TP*/GDP Ratios at All Detail Levels (30 min)

For each benchmark year, compute TP*/GDP at each available detail level:

```
Year  Sector(15) Summary(71) Underlying(138) Detail(402) SIC(85)
1947  —          —           —               —           xxx
1958  —          —           —               —           xxx
1967  —          —           —               —           xxx
1972  —          —           —               —           xxx
1977  —          —           —               —           xxx
1997  xxx        0.97        xxx             xxx         —
2002  xxx        0.95        xxx             xxx         —
2007  xxx        0.93        xxx             xxx         —
2012  xxx        0.95        xxx             xxx         —
2017  xxx        0.94        xxx             xxx         —
```

This shows exactly how much detail resolution matters.

### Step 9: Interpolate TP*/GDP Across All Years (30 min)

Using the maximum detail available at each year:
- 1947-1977: SIC 85-sector TP*/GDP ratios at each benchmark, interpolated annually
- 1978-1996: Interpolate between 1977 SIC and 1997 NAICS (using 1992 bridge if available)
- 1997-2024: Annual summary from Step 5, calibrated by detail/summary ratio from Step 8

### Step 10: Recompute All Marxian Series (1 hour)

With the corrected TP*/GDP ratios:
1. TP* = GDP × (detail-level TP*/GDP ratio)
2. C*m from IO intermediate inputs at maximum resolution
3. GFP* = TP* - C*m
4. VA* = GFP* - Dp (depreciation from COFC)
5. S* = VA* - V*
6. e = S*/V*

**Expected outcome**: e(1948) moves from 1.86 → ~1.70, matching the book.

---

## Effort Summary

| Step | What | Hours |
|------|------|-------|
| 1 | API discovery (table names, years) | 0.5 |
| 2 | Fetch detail Use tables (2007, 2012, 2017) | 1.0 |
| 3 | Build detail NAICS classification (402 sectors) | 1.0 |
| 4 | Compute detail-level aggregates | 1.0 |
| 5 | Fetch annual summary tables (1997-2024) | 0.5 |
| 6 | Download SIC historical benchmarks | 1.0 |
| 7 | Build SIC classification (85 sectors) | 0.5 |
| 8 | Compute TP*/GDP at all detail levels | 0.5 |
| 9 | Interpolate across all years | 0.5 |
| 10 | Recompute all Marxian series | 1.0 |
| **Total** | | **~7.5 hours** |

---

## What This Achieves

After this plan:
- **TP* from data at maximum resolution** — detail (402 sectors) for benchmarks, summary (71) for annual
- **C*m from data** — IO intermediate inputs at each benchmark
- **Complete year coverage** — SIC 1947-1977, bridge 1992, NAICS 1997-2024
- **No hardcoded ratios** — every ratio from IO data at the maximum available resolution
- **Documented resolution impact** — table showing how TP*/GDP changes with sector detail

The exploitation rate trajectory should then correctly RISE (as the book shows) because:
1. TP* is properly scaled (TP*/GDP ≈ 1.4-1.6 at detail level, not 0.97)
2. V* growth is properly modulated by declining Lp/L
3. S* = VA* - V* is positive and growing
4. e = S*/V* rises as V* share of VA* declines

---

Sources:
- [BEA Input-Output Accounts Data](https://www.bea.gov/industry/input-output-accounts-data)
- [BEA Benchmark Input-Output Data](https://www.bea.gov/industry/benchmark-input-output-data)
- [BEA Historical Benchmark IO Tables](https://www.bea.gov/industry/historical-benchmark-input-output-tables)
- [BEA API User Guide](https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf)
- [BEA Interactive IO Application](https://www.bea.gov/itable/input-output)

---

*Plan authored 2026-05-10. Based on IO parsing diagnostics (T018 = $15.1T total industry output at summary level), BEA data documentation, and the diagnosed TP*/GDP gap (0.97 summary vs 1.62 book).*
