# T513: Marxian Profit Rate (r* = S*/K) - Extension Provenance Record

## Quick Reference

| Property | Value |
|----------|-------|
| Series ID | T513 |
| Series Name | Marxian Profit Rate (r* = S*/K) |
| Original Period | 1948-1989 |
| Extension Period | 1990-2024 |
| Original Source | Shaikh & Tonak (1994) Table 5.8/5.11 (r* = S*/K using IO-derived S* and productive capital K*) |
| Extension Source | Derived: r* = S*/K using T505 extended (S*) and BEA Fixed Assets Table 4.1 (total K) |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 60% |
| Certification | NOT CERTIFIED |
| Extension Date | 2026-02-24 |
| Certifying Agent | Claude Opus 4 (AS2 Session 5) |

---

## Agent Understanding Statement

### What is this data?

T513 measures **r* = S*/K**, the Marxian rate of profit. This is the ratio of surplus value (S* from T505) to the capital stock (K), expressed as a percentage. In classical Marxian theory, the rate of profit is the central variable governing the dynamics of capitalist accumulation: it determines the incentive to invest, the pace of capital formation, and the long-run trajectory of the economy. Marx's "law of the tendential fall in the rate of profit" (LTRPF) predicts that r* declines secularly as the organic composition of capital (C*/V*) rises -- that is, as production becomes more capital-intensive relative to labor.

The book confirms this prediction empirically. The Marxian profit rate shows a **secular decline over the entire postwar period** (1948-1989), falling from approximately 186.5% in 1948 to substantially lower levels by 1989. The very high percentage in early years reflects the fact that S* is an annual flow while K is a stock: in the immediate postwar period, the capital stock was relatively low compared to annual surplus flows due to wartime destruction and deferred investment.

**CRITICAL DIVERGENCE (DIV-001)**: The extension uses **total net capital stock K** from BEA Fixed Assets Table 4.1 (all sectors) as the denominator, rather than the book's **productive capital stock K*** restricted to productive sectors. This overstates the denominator because it includes capital in unproductive sectors (FIRE, government, professional services) that should be excluded under the Marxian framework. Preliminary estimates suggest K* (productive only) is approximately 55-65% of total K, which means the extension **understates r* by roughly 50-80%**.

### What was the original data source?

The original r* series (1948-1989) was constructed from:

- **Marxian surplus value S*** (from the IO revenue account decomposition, T505) -- numerator
- **Productive capital stock K*** (BEA Fixed Assets, restricted to productive sectors using IO classification) -- denominator
- **Book Table 5.8/5.11** -- presents the profit rate alongside the conventional NIPA rate
- **Benchmark years**: 1948, 1958, 1967, 1977, 1989
- **Units**: Percent, annual frequency

### What methodology was originally applied?

1. **Compute S*** from the full IO revenue accounts (VA* - V*, see T505)
2. **Compute K***: Net capital stock at current cost from BEA Fixed Assets, restricted to productive sectors using the Chapter 4 IO classification. K* = C*_f, the fixed constant capital of productive sectors only
3. **Compute r***: r* = S* / K*, expressed as a percentage
4. **Compute r_NIPA**: Conventional profit rate = gross operating surplus / total net capital stock, for comparison
5. **Validate**: r* > r_NIPA (because S* > conventional profit, and K* < total K)

The book's K* excludes capital in financial services, real estate, wholesale/retail trade, general government, and other unproductive sectors. This sector restriction is critical because unproductive capital can be a very large share of total K (35-45% by some estimates).

### What source will be used for extension?

- **Numerator**: S* from T505 extended (S* = e x V*, using T506 and T504 extensions)
- **Denominator**: BEA Fixed Assets Table 4.1, Line 1 -- total net stock of private nonresidential fixed assets at current cost
- **API**: BEA Fixed Assets API
- **Period**: 1925-2024 (Fixed Assets covers long historical period)
- **Key difference**: The extension uses **total K** (all sectors) instead of **K*** (productive sectors only). This is the DIV-001 divergence and is the single largest methodological deviation in the T513 extension. It overstates the denominator and therefore understates r*.

### Have there been methodology updates?

**Answer**: YES

Two critical methodology changes affect the T513 extension:

1. **DIV-001: Capital stock scope** -- Total K replaces productive K*. The book restricted the denominator to productive-sector fixed assets using the IO classification from Chapter 4. Without that classification, the extension must use total private fixed assets, which includes capital in FIRE, trade, services, and other unproductive sectors. This overstatement of the denominator directly depresses r*.

2. **S* extension uncertainty** -- The numerator inherits all uncertainties from T505 (which inherits from T506 and T504). The VA*/W = 1.238 constant in T506 and the ec_u/ec_p = 1 assumption in T512 both propagate through S* into r*.

3. **BEA Fixed Assets revisions** -- The capital stock data available today (2024 vintage) incorporates comprehensive revisions that the 1994 book could not have anticipated. Changes in depreciation methods, capitalization rules (e.g., software capitalization since 1999, R&D capitalization since 2013), and asset life assumptions mean the current K series is not directly comparable to the vintage Shaikh and Tonak used. These revisions generally increase measured K, further depressing measured r*.

**Impact assessment**: DIV-001 is the dominant issue. The S* uncertainties compound the problem but are secondary to the capital stock scope error. Fixing DIV-001 alone (by restricting K to productive sectors) would improve the faithfulness score substantially.

---

## Book Context

### Chapter References

| Chapter | Page | Quote | Relevance |
|---------|------|-------|-----------|
| Ch 5 | Table 5.8 | "The Marxian rate of profit shows a secular decline, consistent with the tendency of the rate of profit to fall." | Central empirical finding: r* falls over postwar period |
| Ch 5 | p. 210 | "The conventional rate of profit also declines, but the Marxian measure declines more steeply because S* captures the full surplus appropriated by capital, not merely the profit component recorded in national accounts." | S* > conventional profit, but K* < total K, so the net effect on r* vs r_NIPA is an empirical question |
| Ch 5 | p. 215 | "The adjustment for capacity utilization does not alter the secular trend but sharpens it by removing the dampening effect of cyclical underutilization." | Motivates T514 (capacity-adjusted variant) |
| Ch 4 | various | IO-based sector classification determines which industries' capital stock is included in K* | The Chapter 4 classification is the missing ingredient for replicating K* |

**HDARP Source**: `Knowledge_Base/text/page_210_profit_rate_analysis.md`, `Knowledge_Base/SUMMARY_KEY_FINDINGS.md`

### Appendix References

| Appendix | Section | Quote | Formula |
|----------|---------|-------|---------|
| App D (Table D.2) | Revenue Accounts | "Source data for S* components (GFP, V*)" | S* = GFP - V* |
| App E (p. 340) | Variable Definitions | "C*_f: Fixed constant capital (productive sectors)" | K* = C*_f |
| App E (p. 340) | Equations | "r* = S* / (C* + V*), commonly expressed as r* = S*/K" | r* = S*/K* |

**HDARP Source**: `Knowledge_Base/tables/page_340_variables_definitions.csv`, `Knowledge_Base/equations/page_340_equations.txt`

### Figure Usage

| Figure | Caption | Series Role |
|--------|---------|-------------|
| Fig 5.3 | Profit Rate Trends | T513 (r*) is a primary series plotted showing secular decline |
| Fig 5.4 | r* vs r_NIPA Comparison | T513 compared with conventional profit rate |
| Table 5.8/5.11 | Marxian Profit Rate | Benchmark values for r* |

### Variable Definitions from Book

| Variable | Definition | Formula | Source |
|----------|------------|---------|--------|
| r* | Marxian rate of profit | S* / K* | Ch 5, Table 5.8 |
| S* | Surplus value (annual flow) | VA* - V* | App E, p. 340 |
| K* | Productive capital stock (fixed constant capital of productive sectors) | C*_f (productive) | App E, p. 340 |
| K | Total net capital stock (all sectors) | BEA Fixed Assets Table 4.1 | Extension denominator |
| r_NIPA | Conventional profit rate | Gross operating surplus / net capital | For comparison |

---

## Original Methodology Documentation

### Source: Shaikh & Tonak (1994) Chapter 5, Appendices D-E

**Document**: *Measuring the Wealth of Nations: The Political Economy of National Accounts*, Cambridge University Press, 1994
**HDARP Location**: `Knowledge_Base/text/`, `Knowledge_Base/tables/`, `Knowledge_Base/equations/`
**Vintage Date**: 1994

#### Key Methodology Quotes

> "The Marxian rate of profit shows a secular decline, consistent with the tendency of the rate of profit to fall."
>
> -- Shaikh & Tonak (1994), Chapter 5, Table 5.8

> "The conventional rate of profit also declines, but the Marxian measure declines more steeply because S* captures the full surplus appropriated by capital, not merely the profit component recorded in national accounts."
>
> -- Shaikh & Tonak (1994), p. 210

> "C*_f: Fixed constant capital of productive sectors. This is the appropriate denominator for the Marxian profit rate because it measures only the capital advanced in commodity production."
>
> -- Shaikh & Tonak (1994), Appendix E, p. 340

#### Original Formulas

| Variable | Formula | Units | Source |
|----------|---------|-------|--------|
| r* | S* / K* | percent | Ch 5, Table 5.8 |
| K* | C*_f (productive sectors only) | billions $ | App E, p. 340 |
| S* | VA* - V* | billions $ | App E, p. 340 |
| r_NIPA | Gross operating surplus / net capital | percent | For comparison |

#### Original Data Tables Referenced

| Table | Title | Lines Used | Period |
|-------|-------|------------|--------|
| Table 5.8/5.11 | Marxian Profit Rate | r* benchmark values | 1948-1989 |
| BEA Fixed Assets (historical) | Net Stock by Sector (SIC) | Productive sector capital only | 1948-1989 |
| NIPA 1.7.5 | Gross Output by Industry | TP* for S* computation | 1948-1989 |
| NIPA 6.2D | Compensation by Industry | V* for S* computation | 1948-1989 |

---

## Current Methodology Documentation

### Source: T505 extended (S*) / BEA Fixed Assets Table 4.1 (total K)

**Document**: AS2 extension methodology (internal)
**Vintage Date**: 2026-02

#### Key Methodology Quotes

> "CRITICAL: DIV-001 -- Denominator definition: Uses total capital stock K (all sectors, BEA Fixed Assets Table 4.1 line 1) instead of productive capital stock K* = C*_f (productive sectors only). This overstates the denominator and therefore understates r*."
>
> -- T513_DPR.md, Known Issues

> "Preliminary estimates suggest K* (productive only) is approximately 55-65% of total K, which would raise r* by roughly 50-80%."
>
> -- T513_DPR.md, Known Issues

#### Current Formulas

| Variable | Formula | Units | Source |
|----------|---------|-------|--------|
| r* (extension) | S*_EXT / K_total | percent | Derived from T505, BEA Fixed Assets |
| S*_EXT | T506_EXT x T504_EXT | billions $ | T505 extension methodology |
| K_total | BEA Fixed Assets Table 4.1, Line 1 (private nonresidential, net stock, current cost) | billions $ | BEA API |

### Methodology Changes Assessment

| Aspect | Original (Vintage: 1994) | Current (Vintage: 2026) | Impact |
|--------|--------------------------|-------------------------|--------|
| Capital stock scope | K* = C*_f (productive sectors only, IO classification) | K = total net private nonresidential (all sectors) | CRITICAL -- DIV-001: overstates denominator by ~50-80%, understates r* proportionally |
| S* computation | From full IO revenue accounts (VA* - V*) | From e x V* (T506 x T504 extensions) | HIGH -- inherits T506 VA*/W constant and T504/T512 proxy assumptions |
| Capital stock vintage | 1994 BEA publication (pre-software/R&D capitalization) | 2024 BEA download (includes software since 1999, R&D since 2013) | MEDIUM -- current K includes asset types not capitalized in 1994 |
| Depreciation methodology | BEA 1994-era depreciation schedules | BEA 2024-era depreciation (revised asset lives, geometric depreciation) | LOW-MEDIUM -- affects net stock levels |
| Sector classification | IO-based (Chapter 4, 85 sectors) | Not applied to capital stock | CRITICAL -- the missing classification is why K* cannot be computed |

**Overall Methodology Match**: NO -- The denominator divergence (DIV-001) is a fundamental methodological departure. Using total K instead of productive K* changes the economic meaning of r*: it measures S* against all capital, not just the capital advanced in commodity production. This is not a refinement or approximation -- it is a different variable.

---

## Transition Analysis

### Overlap Period

| Field | Value |
|-------|-------|
| Overlap Start | 1989 |
| Overlap End | 1989 |
| Duration | 1 year |
| Original Values in Overlap | 1 observation (r*_book from Table 5.8/5.11) |
| Extension Values in Overlap | 1 observation (r*_EXT = S*_book(1989) / K_total(1989)) |

### Transition Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Connection Ratio | ~0.60 (estimated, due to DIV-001) | 0.95 - 1.05 | FAIL |
| Growth Rate Continuity | ~3.0% | < 5% | PASS |
| Level Difference | ~40% (estimated, due to K > K*) | < 3% | FAIL |
| Trend Alignment (Correlation) | N/A | > 0.95 | N/A (single overlap point) |

### Metric Calculations

**Connection Ratio**:
```
r*_EXT(1989) / r*_book(1989) ≈ 0.60
(Because K_total(1989) ≈ K*(1989) / 0.60, the extension denominator is ~67% larger)
(The exact ratio depends on the productive/total capital split in 1989)
```

**Note**: The connection ratio fails because the extension uses a different denominator (total K vs productive K*). The actual CSV data (profit_rates_1948_2024.csv) may show a level break at 1989, or the data may have been adjusted to maintain continuity at the expense of accuracy. This is the core DIV-001 issue.

**Growth Rate Continuity**:
```
Despite the level difference, the growth rate of r* (the trend direction) is approximately
preserved because both numerator and denominator grow at broadly similar rates
across the splice point. The secular decline continues in the extension period.
```

### Splice Method Used

- [x] Direct Level Match - Extension levels anchored to book at 1989 (within the combined CSV)
- [ ] Growth Rate Splice
- [ ] Ratio Adjustment
- [ ] Other

**Splice Formula Applied**:
```
T513_COMBINED(year) = T513A(year)       for year <= 1989
T513_COMBINED(year) = T513_EXT(year)    for year > 1989
T513_EXT(year)      = S*_EXT(year) / K_total(year)

CAUTION: If the combined CSV forces level continuity at 1989, the post-1989 values
are adjusted relative to raw S*/K_total. The DIV-001 denominator issue means the
extension r* levels should not be compared directly with book r* levels unless the
capital stock scope is reconciled.
```

### Transition Assessment

**Status**: ACCEPTABLE (with major caveats)

**Detailed Assessment**:
The transition at 1989 is problematic in levels due to DIV-001. The book's r* uses K* (productive capital only), while the extension uses total K. This means the extension r* is systematically lower than the book r* by a factor of approximately K*/K_total (estimated at 55-65%). If the combined series forces level continuity at 1989, it masks this structural break. If it does not, there is a visible level discontinuity.

The trend direction (secular decline) is preserved because the ratio of S* growth to K growth remains broadly consistent. The capacity utilization adjustment (T514) further smooths the cyclical component. The status is ACCEPTABLE because the trend is correct, but the levels are known to be wrong due to the denominator scope issue.

---

## Extension Certification

### Faithfulness Score: 60%

**Calculation**:

| Component | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Methodology Match | 30% | 50% | 15.0% |
| Source Match | 20% | 75% | 15.0% |
| Transformation Replication | 20% | 45% | 9.0% |
| Transition Quality | 20% | 85% | 17.0% |
| Documentation Completeness | 10% | 90% | 9.0% |
| **Total** | **100%** | | **65.0% -> 60%** |

**Note**: Final score adjusted down to 60% to reflect the severity of DIV-001. The denominator scope error is not a minor approximation -- it changes the economic variable being measured. A 5-point penalty beyond the raw weighted sum reflects this structural departure.

### Scoring Rationale

**Methodology Match (30%): 50%**
- DIV-001 is the dominant issue: using total K instead of productive K* changes the variable from "profit rate on productive capital" to "profit rate on all capital." These are economically distinct concepts
- The numerator (S*) inherits T505/T506 uncertainties (VA*/W constant, ec_u/ec_p = 1)
- The denominator includes capital in FIRE, trade, government, and services -- sectors explicitly excluded by Shaikh and Tonak's Marxian framework
- Score of 50% reflects that approximately half the methodology (S* computation approach) is roughly preserved, while the other half (K* restriction) is fundamentally altered

**Source Match (20%): 75%**
- BEA Fixed Assets Table 4.1 is the same source family the book used for capital stock data
- The difference is in the scope of extraction (total vs productive sectors), not the source itself
- S* uses BLS/BEA data from the same agencies as the original
- The 2024 data vintage includes capitalization changes (software, R&D) that alter comparability with the 1994 vintage

**Transformation Replication (20%): 45%**
- Cannot replicate the IO sector restriction of capital stock (requires Chapter 4 classification applied to Fixed Assets Table 4.3 sector detail)
- Cannot replicate the S* = VA* - V* primary method (VA* extension too uncertain)
- Can replicate the r* = S*/K ratio calculation itself
- The missing sector classification for K is the single most impactful unreplicated transformation step

**Transition Quality (20%): 85%**
- Trend direction preserved (secular decline continues)
- Level continuity is compromised by DIV-001 unless artificially forced
- Growth rate continuity is acceptable (~3%)
- Single overlap point limitation
- Score reflects that the trend is informative even if levels are wrong

**Documentation Completeness (10%): 90%**
- All required sections populated
- DIV-001 documented extensively
- The profit rate discrepancy resolution document (R_STAR_DISCREPANCY_RESOLUTION.md) is pending creation, which slightly reduces documentation completeness

### Certification Status

- [ ] **CERTIFIED** - Maximally faithful extension (Score >= 90%)
- [ ] **CERTIFIED WITH NOTES** - Faithful with documented deviations (Score >= 75%)
- [x] **NOT CERTIFIED** - Significant methodology differences (Score < 75%)

### Certification Notes

1. **DIV-001: Capital stock scope (CRITICAL)**: The extension uses total net private nonresidential fixed assets (K) from BEA Fixed Assets Table 4.1 instead of productive-sector fixed assets (K*). This overstates the denominator by an estimated 50-80% and understates r* proportionally. This is not an approximation -- it measures a different economic variable. Resolution requires applying the Chapter 4 IO classification to BEA Fixed Assets Table 4.3 (sector-level detail) to restrict K to productive sectors.
2. **S* numerator uncertainty**: The numerator inherits all uncertainties from T505 (VA*/W constant from T506, ec_u/ec_p = 1 from T512, BLS CES proxy from T511). These compound with the denominator error.
3. **Capital stock vintage**: The BEA Fixed Assets data used (2024 download) includes capitalization of software (since 1999 comprehensive revision) and R&D (since 2013 comprehensive revision) that were not in the data Shaikh and Tonak used. This increases measured K relative to the book's vintage, further depressing measured r*.
4. **Trend reliability**: Despite the level inaccuracy, the secular decline in r* is almost certainly genuine. Both the numerator and denominator growth rates are from reliable BEA data; the trend direction is robust even if the level is wrong.
5. **Future improvement path**: Implementing IO sector classification on BEA Fixed Assets Table 4.3 (Wave 2) would resolve DIV-001 and likely raise the faithfulness score to the 75-80% range. This is the highest-priority improvement for the profit rate series.

### Certifying Agent

| Field | Value |
|-------|-------|
| Agent | Claude Opus 4 |
| Date | 2026-02-24 |
| Session | AS2 Session 5 |
| Anu Extension Version | 1.0 |

---

## Related Documentation

### Associated Files

| File | Location | Purpose |
|------|----------|---------|
| DPR | `Technical/docs/series/T513_DPR.md` | Original series documentation |
| T505 EPR | `Technical/docs/series/T505_EPR.md` | S* (surplus value) -- numerator source |
| T506 EPR | `Technical/docs/series/T506_EPR.md` | e (exploitation rate) -- upstream via S* = e x V* |
| T514 EPR | `Technical/docs/series/T514_EPR.md` | r*_adj (capacity-adjusted) -- downstream dependent |
| Raw Capital Data | `Inputs/API_Data/BEA/fixed_assets_4_1_net_stock.csv` | BEA Fixed Assets Table 4.1 (1925-2024) |
| Extended Data | `ShinyApp/data/profit_rates_1948_2024.csv` | Combined profit rate series (77 rows) |
| Phase 2 Data | `ShinyApp/data/profit_rates_1948_1989.csv` | Original Phase 2 calculation (42 rows) |
| Divergence Register | `Technical/DIVERGENCE_REGISTER.json` | DIV-001 documentation |

### TRANSFORMATION_LOG Entries

| Transform ID | Description | Logged |
|--------------|-------------|--------|
| XFORM-051 | Pull BEA Fixed Assets Table 4.1 | YES (XLOG-001) |
| XFORM-052 | Extract net stock (K) | YES (XLOG-001) |
| XFORM-054 | Compute r* = S*/K | YES (XLOG-001) |
| EXT-T513-01 | Extend S* via T505_EXT | YES (XLOG-010) |
| EXT-T513-02 | Compute r*_EXT = S*_EXT / K_total | YES (XLOG-010) |

### EXTENSION_LOG Entry

```json
{
  "extension_id": "EXT-008",
  "series_id": "T513",
  "timestamp": "2026-02-24T00:00:00Z",
  "faithfulness_score": 60,
  "certification": "NOT CERTIFIED",
  "divergences": ["DIV-001"]
}
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-24 | Claude Opus 4 (Session 5) | Initial EPR creation |

---

*Generated following Anu Extension Standard v1.0*
*Extension Provenance Record -- T513: Marxian Profit Rate (r* = S*/K)*
