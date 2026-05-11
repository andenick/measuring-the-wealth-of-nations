# ST2 Vintage Tracking and Historical Data Pull Plan

**Date**: 2026-05-09
**Problem**: Our pipeline uses 2025/2026-vintage NIPA data. The book used 1986-vintage NIPA data. The difference (NIPA comprehensive revisions in 1991, 1996, 1999, 2003, 2009, 2013, 2018, 2023) causes systematic divergences in computed Marxian series, particularly for the exploitation rate (e=1.86 vs book's 1.70 for 1948).
**Goal**: (1) Understand and document the vintage gap, (2) Optionally fetch historical vintages via ALFRED to quantify the impact, (3) Integrate vintage awareness into the v7.0 pipeline.

---

## The Vintage Problem

NIPA data is revised multiple times:
- **Annual revisions**: small adjustments each July (1-3 years back)
- **Comprehensive revisions**: major methodological changes every ~5 years (all years revised)

The book (published 1994, data through 1989) used **BEA (1986)** NIPA tables — the 1986 comprehensive revision. Since then, there have been 7 comprehensive revisions:

| Year | Key Changes | Impact on Marxian Measures |
|------|-------------|--------------------------|
| 1991 | Computer investment capitalized | Changes GDP, GVA, investment |
| 1996 | Chain-type price indexes | Changes real measures, deflators |
| 1999 | Software as investment, SIC→NAICS | Changes sector classifications, I* |
| 2003 | Government investment capitalized | Changes G, surplus allocation |
| 2009 | R&D as investment | Changes GDP by ~3%, shifts activity classification |
| 2013 | Entertainment originals, pension accounting | Changes capital stock measures |
| 2018 | Methodological updates | Various |
| 2023 | Latest comprehensive | Updates all historical data |

**Impact on our pipeline**: When we compute V*=89.0bn for 1948 (book says 88.4), the difference isn't a methodology error — it's because our EC for 1948 reflects the 2023 NIPA revision while the book's EC reflected the 1986 revision. The data for 1948 was literally CHANGED by BEA between 1986 and 2023.

---

## What We Currently Have

The `DATA_VINTAGE_LOG.json` tracks when each source was pulled:
- `nipa_6_2D`: pulled 2025-12-05 (Phase 3)
- `nipa_T20100`: pulled 2026-04-09 (BEA API live)
- `bls_ces`: pulled 2025-12-05 (Phase 3)
- `fixed_assets`: pulled 2025-12-05 (Phase 3)
- `klems`: pulled 2026-05-06 (Robin)
- `naics_io`: pulled 2026-04-08 (from Leontief.io, original 2025-10)

The v7.0 `nickydata/` pipeline caches all API responses with `{date}.json` filenames — so vintages are tracked by cache date. But we have NO ability to fetch HISTORICAL vintages.

The Anu Suite rules (python-data-quality.md) say: "Use ALFRED API (realtime_start/realtime_end) to compare vintages when validating extensions." We don't implement this.

---

## What ALFRED Can Do

The **ALFRED (Archival FRED)** API provides historical vintages of any FRED series. Same API endpoint, different parameters:

```
GET https://api.stlouisfed.org/fred/series/observations
  ?series_id=GDP
  &api_key=XXX
  &realtime_start=1986-01-01    ← what was published as of this date
  &realtime_end=1986-12-31
  &observation_start=1948-01-01
  &frequency=a
```

This returns GDP as it was published in 1986 — the EXACT data the book would have used.

**Available vintages for key NIPA series on FRED**:
- GDP (A191RC): vintages from 1991+ (not 1986)
- GDPC1 (Real GDP): vintages from 1991+
- A576RC1 (Compensation of employees): vintages from 1994+
- W209RC1 (Personal income): vintages from 1994+

**Limitation**: FRED/ALFRED mirrors of NIPA data only go back to 1991-1994. For the book's actual 1986 vintage, we'd need the BEA (1986) statistical tables publication directly (available as a government document but not via API).

---

## Plan

### Phase 1: Document Vintage Impact (1 hour)

Quantify how much NIPA revisions affect our Marxian measures.

**Method**: For 3 key FRED series (GDP, Compensation, Personal Income), fetch the 1994 vintage and 2025 vintage via ALFRED. Compare at benchmark years (1948, 1958, 1972, 1989).

```python
# 1994 vintage (earliest available, close to book)
gdp_1994 = fred.fetch("GDP", api_key, realtime_start="1994-01-01", realtime_end="1994-12-31")

# 2025 vintage (our current data)
gdp_2025 = fred.fetch("GDP", api_key)  # defaults to latest

# Compare
for yr in [1948, 1958, 1972, 1989]:
    diff_pct = (gdp_2025[yr] - gdp_1994[yr]) / gdp_1994[yr] * 100
    print(f"{yr}: 1994 vintage={gdp_1994[yr]}, 2025={gdp_2025[yr]}, diff={diff_pct:.1f}%")
```

**Output**: A table showing revision magnitude per year per series. Expected: 1-5% for most years, possibly larger for investment/capital series.

### Phase 2: Add ALFRED Support to Fetch Layer (1 hour)

Add `realtime_start` and `realtime_end` parameters to the FRED fetcher:

```python
# In nickydata/fetch/fred.py
def fetch(series_id, api_key, ..., realtime_start=None, realtime_end=None):
    params = {...}
    if realtime_start:
        params["realtime_start"] = realtime_start
    if realtime_end:
        params["realtime_end"] = realtime_end
    # Cache key includes vintage: fred_{id}_{vintage}_{date}.json
```

Add a convenience function:
```python
def fetch_vintage(series_id, api_key, vintage_year):
    """Fetch a series as it was published in vintage_year."""
    return fetch(series_id, api_key,
                 realtime_start=f"{vintage_year}-01-01",
                 realtime_end=f"{vintage_year}-12-31")
```

### Phase 3: Compute "Book-Vintage" Marxian Accounts (2 hours)

Fetch 1994-vintage data for all key NIPA series and recompute V*, S*, e using these historical values.

**Why 1994 not 1986**: ALFRED NIPA data starts ~1994. The 1994 vintage is post-1991 comprehensive revision but pre-1996/1999/2003/2009 revisions. It's the closest available to the book's data.

**Method**:
1. Fetch 1994-vintage: GDP, Compensation, Personal Income, Social Benefits
2. Compute V*, S*, e using the same v7.0 methodology but 1994 data
3. Compare: "1994 vintage e" should be closer to book's e than "2025 vintage e"

**Expected outcome**: e(1948) moves from 1.86 (2025 vintage) toward 1.70 (book), with ~50% of the gap explained by vintage differences. The remaining gap would be methodology (our sector-level computation vs the book's exact Appendix G procedure).

### Phase 4: Vintage-Aware Validation (1 hour)

Add a validator that flags when series are sensitive to vintage:

```python
def check_vintage_sensitivity(series, data):
    """Compare current-vintage vs historical-vintage for revision-sensitive series."""
    for sid in ["T504", "T505", "T506"]:
        current = series[sid]
        # Re-compute with 1994 vintage data
        historical = _recompute_with_vintage(sid, data, vintage=1994)
        max_diff = abs(current - historical).max()
        if max_diff > 0.05:  # >5% divergence
            yield Warning(f"{sid}: max vintage divergence {max_diff:.1%}")
```

### Phase 5: Update DATA_VINTAGE_LOG (30 min)

For the v7.0 pipeline:
- Every fetch records its vintage date in the cache filename (already done)
- Add a `data/vintages.json` manifest listing:
  - Current vintage date for each BEA/FRED series
  - Which NIPA comprehensive revisions are reflected
  - Which series are revision-sensitive (GDP, compensation, investment = YES; employment = less so)

### Phase 6: Document in methodology.json (15 min)

Add a vintage section:
```json
{
  "vintage_awareness": {
    "current_vintage": "2025-2026 (latest NIPA comprehensive revision: 2023)",
    "book_vintage": "BEA (1986) publication",
    "expected_divergence": "1-5% for most series, up to 10% for investment/capital",
    "revision_sensitive_series": ["T501", "T504", "T505", "T506", "T513"],
    "revision_insensitive_series": ["T511", "T515", "T516", "T601-T604"],
    "alfred_baseline_vintage": "1994 (earliest available on FRED/ALFRED)"
  }
}
```

---

## Effort Summary

| Phase | What | Hours |
|-------|------|-------|
| 1 | Document vintage impact (3 FRED comparisons) | 1.0 |
| 2 | Add ALFRED support to fetch layer | 1.0 |
| 3 | Compute book-vintage Marxian accounts | 2.0 |
| 4 | Vintage-aware validation | 1.0 |
| 5 | Update DATA_VINTAGE_LOG | 0.5 |
| 6 | Document in methodology.json | 0.25 |
| **Total** | | **~5.75 hours** |

---

## Integration with Anu Suite

The Anu Extension skill (Principle 8: VINTAGE TRACKING) requires:
1. Record all data vintage dates ✅ (cache filenames include date)
2. Compare vintages when validating extensions ❌ (no ALFRED implemented)
3. Document vintage in EPR ✅ (DATA_VINTAGE_LOG.json exists)

The python-data-quality rules require:
1. Log download date in cached filename ✅
2. Note vintage for revisable series ✅ (DATA_VINTAGE_LOG)
3. Use ALFRED for vintage comparison ❌ (not implemented)

**After this plan**: ALFRED support added, vintage comparison automated, all three Anu Suite requirements met.

---

## What This Explains About Our Results

The v7.0 pipeline's exploitation rate gap (e=1.86 vs book 1.70 for 1948) is likely 40-60% vintage-driven:

- **NIPA comprehensive revisions** changed GDP, EC, and sector classifications for ALL historical years
- The 2009 revision (R&D as investment) alone added ~3% to GDP, which changes GFP* and thus S*/V*
- The 1999 revision (SIC→NAICS) changed sector definitions, affecting our NAICS classification
- The remaining 40-60% of the gap is from methodology differences (our approximate production worker computation vs the book's exact Appendix G)

**The vintage comparison (Phase 3) will quantify this decomposition** — showing how much of the gap is "data changed" vs "methodology differs."

---

*Plan authored 2026-05-09. Based on DATA_VINTAGE_LOG.json, Anu Suite rules (python-data-quality.md), Anu Extension skill (Principle 8), FRED/ALFRED API documentation.*
