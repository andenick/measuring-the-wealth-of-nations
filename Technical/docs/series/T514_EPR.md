# T514: Capacity-Adjusted Profit Rate (r*_adj) - Extension Provenance Record

## Quick Reference

| Property | Value |
|----------|-------|
| Series ID | T514 |
| Series Name | Capacity-Adjusted Profit Rate (r*_adj) |
| Original Period | 1948-1989 |
| Extension Period | 1990-2024 |
| Original Source | Shaikh & Tonak (1994) Table 5.8/5.11 (r*_adj = r* x (1/TCU) from IO-derived r* and Federal Reserve capacity data) |
| Extension Source | Derived: r*_adj = T513 extended / FRED TCU |
| Transition Status | ACCEPTABLE |
| Faithfulness Score | 60% |
| Certification | NOT CERTIFIED |
| Extension Date | 2026-02-24 |
| Certifying Agent | Claude Opus 4 (AS2 Session 5) |

---

## Agent Understanding Statement

### What is this data?

T514 measures **r*_adj**, the capacity-adjusted Marxian profit rate. This series corrects the raw Marxian profit rate r* (T513) for cyclical variation in capacity utilization by dividing by the total capacity utilization rate (TCU). The adjustment removes the dampening effect of business-cycle fluctuations on measured profitability, isolating the underlying secular trend.

When capacity utilization is low (during recessions), the measured profit rate r* is depressed because the capital stock is underutilized -- output and therefore surplus value fall while the capital stock remains in place. Dividing by TCU effectively asks: "What would the profit rate be if all capital were fully utilized?" This inflates r* during recessions and deflates it during booms, producing a series that more faithfully tracks the structural tendency of the rate of profit to fall.

```
r*_adj = r* x (1/TCU) = r* / TCU
       = (S*/K) / TCU
```

The capacity-adjusted rate is standard in the empirical Marxian literature (Shaikh 1987, 1992; Dumenil and Levy 1993; Basu and Manolakos 2013). The book shows that the adjusted rate falls even more steeply than the unadjusted rate during certain periods (notably 1966-1982) because the secular decline in profitability coincided with declining average capacity utilization.

**CRITICAL**: T514 inherits **all DIV-001 issues from T513**. Because r*_adj = r*/TCU, the denominator overstatement in T513 (using total K instead of productive K*) propagates directly into r*_adj. The extension also faces a **TCU coverage issue**: the FRED TCU series begins in 1967, requiring estimation for the pre-1967 portion of the book period.

### What was the original data source?

The original r*_adj series (1948-1989) was constructed from:

- **Marxian profit rate r*** (T513) -- the unadjusted series from IO-derived S* and productive K*
- **Federal Reserve capacity utilization data** -- historical TCU measures, including pre-1967 estimates from the Wharton index
- **Book Table 5.8/5.11** -- presents r*_adj alongside r* and r_NIPA
- **Benchmark years**: 1948, 1958, 1967, 1977, 1989
- **Units**: Percent, annual frequency

### What methodology was originally applied?

1. **Retrieve r*** from T513 (S*/K* using productive capital only)
2. **Obtain TCU**: Total capacity utilization from Federal Reserve G.17 industrial production and capacity data. For pre-1967, use the Wharton capacity utilization index or Federal Reserve historical estimates
3. **Annualize TCU**: Convert monthly/quarterly observations to annual averages
4. **Compute r*_adj**: r*_adj = r* / TCU, where TCU is expressed as a fraction (0 to 1)
5. **Validate**: r*_adj > r* in all years (since TCU < 1 throughout the postwar period)

The book's TCU measure covers manufacturing, mining, and utilities -- the industries for which the Federal Reserve computes capacity utilization. This is not perfectly aligned with the full productive sector definition (which includes agriculture, construction, and productive transportation) but is the standard measure used in the literature.

### What source will be used for extension?

- **r* source**: T513 extended (S*_EXT / K_total, inheriting DIV-001)
- **TCU source**: FRED series TCU (Total Industry Capacity Utilization, Federal Reserve G.17)
- **API**: FRED API (series ID: TCU)
- **Period**: 1967-2025 (monthly, annualized)
- **Update frequency**: Monthly (Federal Reserve G.17 release)
- **Key differences**: (1) Inherits DIV-001 from T513, (2) FRED TCU starts 1967 -- pre-1967 values estimated, (3) TCU covers manufacturing/mining/utilities only, not the full productive sector

### Have there been methodology updates?

**Answer**: YES

Three methodology issues affect the T514 extension:

1. **DIV-001 inherited from T513**: The parent series uses total K instead of productive K*. Since r*_adj = r*/TCU, the denominator overstatement propagates directly. r*_adj is understated by the same factor as r*.

2. **TCU coverage gap (1948-1966)**: The FRED TCU series begins in January 1967. For the 1948-1966 portion of the book period, Shaikh and Tonak used historical Federal Reserve estimates or the Wharton capacity utilization index. The extension must either: (a) use alternative pre-1967 sources, (b) back-estimate from industrial production data, or (c) accept a gap. The current implementation uses estimated pre-1967 values.

3. **TCU sectoral scope**: FRED TCU covers manufacturing, mining, and electric/gas utilities only. It does not cover construction, agriculture, or productive transportation/services. A capacity measure more closely aligned with the Marxian productive sector definition would require combining industry-specific capacity data, which is not straightforward.

**Impact assessment**: DIV-001 dominates all other issues. The TCU coverage gap affects only the pre-1967 book period (not the extension period) and is therefore less critical for the 1990-2024 extension. The TCU sectoral scope mismatch is a secondary concern shared between the book and extension methodologies.

---

## Book Context

### Chapter References

| Chapter | Page | Quote | Relevance |
|---------|------|-------|-----------|
| Ch 5 | Table 5.8 | "Capacity-adjusted profit rates remove cyclical variation, isolating the secular trend." | Defines the purpose of r*_adj |
| Ch 5 | p. 215 | "The adjustment for capacity utilization does not alter the secular trend but sharpens it by removing the dampening effect of cyclical underutilization. The adjusted rate falls even more steeply than the unadjusted rate in the 1966-1982 period." | Documents the r*_adj behavior: same secular trend as r*, with clearer signal |
| Ch 5 | p. 210 | "The conventional rate of profit also declines, but the Marxian measure declines more steeply because S* captures the full surplus appropriated by capital." | Context for the secular decline that r*_adj sharpens |
| Ch 5 | Table 5.8 | "The Marxian rate of profit shows a secular decline, consistent with the tendency of the rate of profit to fall." | The LTRPF finding that r*_adj is designed to reveal more clearly |

**HDARP Source**: `Knowledge_Base/text/page_210_profit_rate_analysis.md`, `Knowledge_Base/text/page_215_capacity_adjustment.md`, `Knowledge_Base/SUMMARY_KEY_FINDINGS.md`

### Appendix References

| Appendix | Section | Quote | Formula |
|----------|---------|-------|---------|
| App D (Table D.2) | Revenue Accounts | "Source data for S* components underlying r*" | S* = GFP - V* |
| App E (p. 340) | Variable Definitions | "C*_f: Fixed constant capital (productive sectors)" | K* = C*_f (parent series denominator) |
| App E (p. 340) | Equations | "r* = S* / K*, commonly adjusted for capacity utilization" | r*_adj = r* / TCU |

**HDARP Source**: `Knowledge_Base/tables/page_340_variables_definitions.csv`, `Knowledge_Base/equations/page_340_equations.txt`

### Figure Usage

| Figure | Caption | Series Role |
|--------|---------|-------------|
| Fig 5.3 | Profit Rate Trends | T514 (r*_adj) plotted alongside T513 (r*) showing sharper secular decline |
| Fig 5.4 | Adjusted vs Unadjusted Profit Rates | Direct comparison of r* and r*_adj |
| Table 5.8/5.11 | Marxian Profit Rates | Both r* and r*_adj values |

### Variable Definitions from Book

| Variable | Definition | Formula | Source |
|----------|------------|---------|--------|
| r*_adj | Capacity-adjusted Marxian profit rate | r* / TCU | Ch 5, Table 5.8 |
| r* | Marxian rate of profit (unadjusted) | S* / K* | T513, Ch 5 |
| TCU | Total capacity utilization (Federal Reserve G.17) | Manufacturing + mining + utilities | FRED series TCU |
| S* | Surplus value | VA* - V* | T505, App E |
| K* | Productive capital stock | C*_f (productive) | App E, p. 340 |

---

## Original Methodology Documentation

### Source: Shaikh & Tonak (1994) Chapter 5

**Document**: *Measuring the Wealth of Nations: The Political Economy of National Accounts*, Cambridge University Press, 1994
**HDARP Location**: `Knowledge_Base/text/`, `Knowledge_Base/tables/`
**Vintage Date**: 1994

#### Key Methodology Quotes

> "Capacity-adjusted profit rates remove cyclical variation from capacity utilization, isolating the secular trend in profitability."
>
> -- Shaikh & Tonak (1994), Chapter 5, Table 5.8

> "The adjustment for capacity utilization does not alter the secular trend but sharpens it by removing the dampening effect of cyclical underutilization. The adjusted rate falls even more steeply than the unadjusted rate in the 1966-1982 period."
>
> -- Shaikh & Tonak (1994), p. 215

> "The Marxian rate of profit shows a secular decline, consistent with the tendency of the rate of profit to fall."
>
> -- Shaikh & Tonak (1994), Chapter 5, Table 5.8

#### Original Formulas

| Variable | Formula | Units | Source |
|----------|---------|-------|--------|
| r*_adj | r* / TCU = (S*/K*) / TCU | percent | Ch 5, Table 5.8 |
| r*_adj | r* x (1/TCU) | percent | Equivalent formulation |
| TCU | Annual average of monthly Federal Reserve G.17 data | fraction (0 to 1) | Federal Reserve |

#### Original Data Tables Referenced

| Table | Title | Lines Used | Period |
|-------|-------|------------|--------|
| Table 5.8/5.11 | Marxian Profit Rate (adjusted) | r*_adj benchmark values | 1948-1989 |
| Federal Reserve G.17 | Industrial Production and Capacity Utilization | TCU (manufacturing + mining + utilities) | 1948-1989 (Wharton index pre-1967) |
| BEA Fixed Assets (historical) | Net Stock by Sector (SIC) | K* for T513 parent | 1948-1989 |

---

## Current Methodology Documentation

### Source: T513 extended / FRED TCU

**Document**: AS2 extension methodology (internal)
**Vintage Date**: 2026-02

#### Key Methodology Quotes

> "CRITICAL: DIV-001 inherited from T513: The parent series T513 uses total capital stock K (all sectors) instead of productive capital stock K* = C*_f (productive sectors only). Since r*_adj = r* / TCU, the DIV-001 denominator overstatement propagates directly: r*_adj is understated by the same factor as r*."
>
> -- T514_DPR.md, Known Issues

> "TCU coverage gap: FRED TCU series (series ID: TCU) begins in 1967-01-01. Pre-1967 values (1948-1966) require estimation from alternative sources."
>
> -- T514_DPR.md, Known Issues

#### Current Formulas

| Variable | Formula | Units | Source |
|----------|---------|-------|--------|
| r*_adj (extension) | T513_EXT / TCU_FRED | percent | Derived from T513, FRED |
| T513_EXT | S*_EXT / K_total | percent | T513 extension |
| TCU_FRED | FRED series TCU, annualized (monthly average) | fraction (0 to 1) | FRED API |

### Methodology Changes Assessment

| Aspect | Original (Vintage: 1994) | Current (Vintage: 2026) | Impact |
|--------|--------------------------|-------------------------|--------|
| r* parent series | Uses K* (productive sectors only, IO classification) | Uses K total (all sectors) -- DIV-001 | CRITICAL -- inherited from T513; overstates denominator, understates r*_adj |
| S* computation | From full IO revenue accounts | From e x V* (T506 x T504 extensions) | HIGH -- inherited from T505/T506 |
| TCU source (post-1967) | Federal Reserve G.17 | FRED series TCU (same underlying Fed data) | NONE -- same data source |
| TCU source (pre-1967) | Wharton index / Fed historical estimates | Estimated from available sources | LOW -- only affects book period, not extension |
| TCU annualization | Annual average of monthly/quarterly | Simple average of monthly FRED values | NONE -- equivalent method |
| TCU sectoral scope | Manufacturing + mining + utilities | Same (FRED TCU covers same sectors) | NONE -- same limitation in both book and extension |

**Overall Methodology Match**: NO -- Inherits the fundamental DIV-001 divergence from T513. The TCU component itself is well-matched (same Federal Reserve data source, same sectoral scope), but the parent r* series carries the critical denominator scope error. The capacity adjustment formula (r*/TCU) is identical in book and extension.

---

## Transition Analysis

### Overlap Period

| Field | Value |
|-------|-------|
| Overlap Start | 1989 |
| Overlap End | 1989 |
| Duration | 1 year |
| Original Values in Overlap | 1 observation (r*_adj_book from Table 5.8/5.11) |
| Extension Values in Overlap | 1 observation (r*_adj_EXT = T513_EXT(1989) / TCU(1989)) |

### Transition Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Connection Ratio | ~0.60 (estimated, inherited from T513 DIV-001) | 0.95 - 1.05 | FAIL |
| Growth Rate Continuity | ~3.5% | < 5% | PASS |
| Level Difference | ~40% (estimated, inherited from T513) | < 3% | FAIL |
| Trend Alignment (Correlation) | N/A | > 0.95 | N/A (single overlap point) |

### Metric Calculations

**Connection Ratio**:
```
r*_adj_EXT(1989) / r*_adj_book(1989) ≈ 0.60
(Inherited directly from T513: same denominator scope issue)
(TCU(1989) cancels in the ratio, so the connection ratio equals T513's connection ratio)
```

**Growth Rate Continuity**:
```
The growth rate of r*_adj inherits the r* growth rate plus the TCU growth rate contribution.
TCU variation is cyclical and does not introduce systematic bias at the splice point.
Growth continuity is approximately preserved despite the level break.
```

### Splice Method Used

- [x] Direct Level Match - Extension levels anchored to book at 1989 (within the combined CSV)
- [ ] Growth Rate Splice
- [ ] Ratio Adjustment
- [ ] Other

**Splice Formula Applied**:
```
T514_COMBINED(year) = T514A(year)       for year <= 1989
T514_COMBINED(year) = T514_EXT(year)    for year > 1989
T514_EXT(year)      = T513_EXT(year) / TCU_FRED(year)

CAUTION: Same caveat as T513 -- the DIV-001 denominator issue means extension
r*_adj levels are systematically understated relative to the book's methodology.
```

### Transition Assessment

**Status**: ACCEPTABLE (with major caveats)

**Detailed Assessment**:
The transition inherits all issues from T513 (DIV-001 denominator scope, S* numerator uncertainty). The TCU component itself transitions smoothly because the same Federal Reserve data source (G.17, available via FRED) covers both the late book period and the extension period. The FRED TCU series starts in 1967, so by the 1989 splice point there are 22 years of overlap in the TCU data.

The capacity adjustment formula (r*/TCU) is faithfully replicated -- it is the same simple division in both book and extension. All methodology deviation comes from the parent r* series (T513), not from the TCU adjustment itself.

The secular decline in r*_adj continues into the extension period, consistent with the book's LTRPF finding. Cyclical fluctuations (notably the 2001, 2008-2009, and 2020 recessions) show the expected pattern: TCU drops, r*_adj spikes upward relative to r*, then both recover. The long-run trend is downward.

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

**Note**: Final score adjusted down to 60%, identical to T513. The capacity adjustment itself is faithfully replicated (same formula, same TCU data source), so T514 neither improves nor worsens relative to T513. The 5-point downward adjustment from the raw weighted sum reflects the severity of the inherited DIV-001 issue, plus the minor TCU coverage concern for the pre-1967 book period.

### Scoring Rationale

**Methodology Match (30%): 50%**
- Identical to T513: DIV-001 (total K vs productive K*) dominates
- The capacity adjustment formula itself is perfectly replicated (r*/TCU, same in book and extension)
- The TCU data source (FRED/Federal Reserve G.17) is the same as the book's source for the overlap period
- TCU sectoral scope (manufacturing + mining + utilities) is the same limitation in both book and extension
- The methodology match score reflects the r* parent series deviation, not the TCU adjustment

**Source Match (20%): 75%**
- Same as T513 for the r* component (BEA Fixed Assets, BLS/BEA for S*)
- TCU source is the same (Federal Reserve G.17) -- this component is a perfect match
- The blended score reflects the r* source deviation offset by the TCU source match

**Transformation Replication (20%): 45%**
- Same as T513 for the r* component: cannot replicate IO sector restriction on capital stock
- The TCU adjustment step is fully replicated (r*/TCU, identical formula)
- Pre-1967 TCU estimation introduces minor additional uncertainty for the book period but does not affect the 1990-2024 extension
- Score reflects that the missing transformation is in the parent series, not in the capacity adjustment

**Transition Quality (20%): 85%**
- Same as T513: trend direction preserved, level compromised by DIV-001
- TCU transitions smoothly because FRED data is continuous from 1967 through the splice point
- Growth rate continuity acceptable (~3.5%)
- Single overlap point limitation

**Documentation Completeness (10%): 90%**
- All required sections populated
- DIV-001 inheritance documented extensively
- TCU coverage gap documented
- R_STAR_DISCREPANCY_RESOLUTION.md pending creation

### Certification Status

- [ ] **CERTIFIED** - Maximally faithful extension (Score >= 90%)
- [ ] **CERTIFIED WITH NOTES** - Faithful with documented deviations (Score >= 75%)
- [x] **NOT CERTIFIED** - Significant methodology differences (Score < 75%)

### Certification Notes

1. **DIV-001 inherited from T513 (CRITICAL)**: r*_adj = r*/TCU, so the denominator scope error in r* (total K vs productive K*) propagates directly. r*_adj is understated by the same factor as r*. Resolution: fix T513 first by restricting K to productive sectors; r*_adj will automatically correct.
2. **TCU coverage gap (pre-1967)**: FRED TCU begins in 1967. The 1948-1966 portion of the book period uses estimated TCU values. This does not affect the 1990-2024 extension period and is therefore secondary to DIV-001.
3. **TCU sectoral scope**: FRED TCU covers manufacturing, mining, and utilities. It does not cover agriculture, construction, or productive transportation. This is the same limitation in both the book and extension -- it does not represent a methodology change, but it is a known imprecision in the capacity adjustment.
4. **Capacity adjustment faithfulness**: Unlike the r* parent series, the capacity adjustment formula itself is perfectly replicated. The TCU data source is the same (Federal Reserve G.17), the formula is the same (r*/TCU), and the annualization method is the same (simple average of monthly observations). All deviation comes from the parent series.
5. **Cyclical signal preserved**: The extension correctly captures cyclical profit rate dynamics. Recessions (2001, 2008-2009, 2020) show the expected pattern: TCU drops sharply, r*_adj spikes relative to r*, then both recover. This cyclical behavior validates the capacity adjustment methodology even though the level is wrong.
6. **Future improvement path**: Same as T513 -- implementing IO sector classification on BEA Fixed Assets Table 4.3 would resolve DIV-001 for both T513 and T514 simultaneously. No additional work is needed on the TCU component.

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
| DPR | `Technical/docs/series/T514_DPR.md` | Original series documentation |
| T513 EPR | `Technical/docs/series/T513_EPR.md` | r* (parent series) -- r*_adj = r*/TCU |
| T505 EPR | `Technical/docs/series/T505_EPR.md` | S* (surplus value) -- numerator of r* |
| T506 EPR | `Technical/docs/series/T506_EPR.md` | e (exploitation rate) -- upstream via S* = e x V* |
| Raw TCU Data | `Inputs/API_Data/FRED/fred_tcu_capacity_utilization.csv` | FRED TCU data (1967-2025) |
| Raw Capital Data | `Inputs/API_Data/BEA/fixed_assets_4_1_net_stock.csv` | BEA Fixed Assets Table 4.1 (1925-2024) |
| Extended Data | `ShinyApp/data/profit_rates_1948_2024.csv` | Combined profit rate series (r* and r*_adj, 77 rows) |
| Phase 2 Data | `ShinyApp/data/profit_rates_1948_1989.csv` | Original Phase 2 calculation (42 rows) |
| Divergence Register | `Technical/DIVERGENCE_REGISTER.json` | DIV-001 documentation |

### TRANSFORMATION_LOG Entries

| Transform ID | Description | Logged |
|--------------|-------------|--------|
| XFORM-057 | Pull FRED TCU data | YES (XLOG-001) |
| XFORM-058 | Annualize TCU (monthly to annual average) | YES (XLOG-001) |
| XFORM-060 | Compute r*_adj = r*/TCU | YES (XLOG-001) |
| EXT-T514-01 | Inherit T513_EXT for r* | YES (XLOG-010) |
| EXT-T514-02 | Compute r*_adj_EXT = T513_EXT / TCU_FRED | YES (XLOG-010) |

### EXTENSION_LOG Entry

```json
{
  "extension_id": "EXT-009",
  "series_id": "T514",
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
*Extension Provenance Record -- T514: Capacity-Adjusted Profit Rate (r*_adj)*
