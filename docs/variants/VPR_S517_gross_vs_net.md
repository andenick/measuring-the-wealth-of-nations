# VPR: S517 Gross vs Net Stock

**Series**: S517 (Productive Capital Stock K*)
**Variant ID**: VPR_S517_gross_vs_net
**Date**: 2026-05-24
**Author**: anu-rebuild v1.1 Phase 3 (Agent 2)
**Status**: BLOCKED — see Constraint section. Recommendation: retain net stock as primary.

## Problem

S517 (Productive Capital Stock K*) is constructed from BEA Fixed Assets
**Table 4.1, Line 1, Current-Cost Net Stock of Private Nonresidential Fixed Assets**.
The book's Table 5.8 / Appendix H references K* as **gross** stock of fixed capital,
following the Marxian convention of valuing constant capital at its full reproduction
cost without netting out accumulated depreciation. The current S517 implementation
therefore embeds a net-stock methodology that — taken literally — diverges from the
book's nominal specification.

The first-order question this VPR was meant to answer:
> *How much does using net stock instead of gross stock bias the r\* denominator?*

## Variants Considered

| Variant | BEA Table | Form | Units | Status |
|---------|-----------|------|-------|--------|
| Net (current) | FAAt401, Line 1 | Current-Cost Net Stock | Billions current $ | Implemented |
| Gross — current-cost | n/a | Current-Cost Gross Stock | Billions current $ | **Not published by BEA** |
| Gross — real | FAAt402, Line 1 | Chain-type Fisher Quantity Index | Dimensionless | Fetched; not directly comparable |
| Gross — historical-cost | FAAt403, Line 1 | Historical-Cost Net Stock | Billions historical $ | Different vintage (net, not gross) |

## Constraint Discovered

**BEA Fixed Assets does not publish a current-cost gross stock series for private
nonresidential fixed assets.** Verification: queried BEA API
`GetParameterValues` on `FixedAssets / TableName` (127 tables) on 2026-05-24.
No table whose description matches "Current-Cost Gross Stock". The closest
gross-form series is Table 4.2 (Fisher chain-type quantity indexes for
**gross** stock), but this is dimensionless and uses a chained real-quantity
methodology incompatible with the book's nominal current-dollar K\*.

A faithful current-cost gross-stock reconstruction would require:
1. Pulling investment flows (Table 4.7 or Table 1 of the Fixed Assets accounts);
2. Applying the perpetual inventory method (PIM) with assumed service lives
   and a no-depreciation retirement schedule;
3. Independently estimating retirement (Winfrey or similar distribution).

This is a Stage-5-replicator-level construction project, not a v1.1 quick fix.

## Results — Net vs Real-Gross-Index (Fisher) at book endpoints

| Year | Net stock (bn $) | Gross quantity index (FAAt402) | Implied gross stock anchored to net at 1948 (bn $) | Book reference (net) |
|------|------------------|--------------------------------|----------------------------------------------------|----------------------|
| 1948 | 291.56 | 12.24 | 291.56 | 291.557 |
| 1958 | 551.36 | 16.94 | 403.63 | 551.356 |
| 1967 | 871.19 | 23.72 | 565.03 | 871.188 |
| 1980 | 3,800.29 | 38.86 | 925.90 | 3,800.29 |
| 1989 | 6,699.84 | 51.48 | 1,226.63 | 6,699.84 |

**Net stock matches book reference values exactly** (0.00% deviation at all
benchmark years). The "implied-gross-bn" column is illustrative only and should
NOT be interpreted as a competing K\* estimate: it conflates a nominal anchor
with a chained-real quantity index. The 1948→1989 ratio of net to implied-gross
(1.0 → 5.46) is overwhelmingly **price inflation** in the net (current-dollar)
series, not a genuine gross-vs-net wedge.

## Recommendation

**Retain net stock (BEA Table 4.1 Line 1) as primary S517 source.** Rationale:

1. **Literal book practice vs. literal book text diverge.** While the book's
   prose calls K\* "gross", the published Table 5.8 / Appendix H values match
   BEA Table 4.1 Line 1 (net stock) to within rounding (0.00% pct_diff at 5
   benchmark years — see scratch CSV). The book's *implemented* methodology
   is net stock; only the *labelling* uses "gross".

2. **Current-cost gross stock is unavailable from BEA.** No published series
   meets the Marxian "current reproduction cost of total fixed capital ever
   purchased and still in service" definition. Any "gross" variant would
   require agent-side PIM reconstruction (Stage-5-replicator scope, out of
   v1.1 quick-fix budget).

3. **Downstream impact is bounded.** S513 (r\* = S\*/(C\*+V\*)) does NOT depend
   on S517: r\* is built from S502, S504, S505 flows. Only the *stock-form*
   variant of r\* (see VPR_S513_stock_vs_flow, sibling VPR) would propagate a
   net-vs-gross choice, and that variant is itself a recommendation document
   pending decision.

4. **Reference-value tolerance is satisfied.** S517's `validation.reference_values`
   in `series_registry.json` are themselves Table 4.1 (net) endpoints, so the
   series passes its own validation gate definitionally. Switching to a
   reconstructed gross series would invalidate the reference values and require
   a coordinated registry update.

## Disclosure Required (per Anti-Proxy Rule)

A footnote of the form below should be added to the S517 EPR / DPR and to any
methodology document mentioning K\*:

> **Note on net vs. gross K\*.** The book's prose describes K\* as the *gross*
> stock of productive fixed capital, but its tabulated values (Table 5.8 /
> Appendix H) match BEA Fixed Assets Table 4.1 Line 1 (Current-Cost **Net**
> Stock of Private Nonresidential Fixed Assets) to four significant figures
> at all benchmark years. We retain net stock for fidelity to the book's
> realized values. BEA does not publish a current-cost gross stock series,
> so a gross-stock alternative would require investigator-side perpetual-
> inventory reconstruction, which is out of scope for this replication.

## Impact on Downstream Series

- **S513** r\* = S\*/(C\*+V\*) — uses S502, S504, S505. **Independent of S517.**
- **S512** s\* = S\*/V\* — independent of S517.
- **Any stock-form r\* variant** (VPR_S513_stock_vs_flow) — uses S517 directly.
  Inherits this VPR's net-stock recommendation.
- **No re-build required** for current registry state; this is a disclosure-only
  divergence.

## References

- `code/E08_exploration/E_S517_gross_vs_net.py` — comparison script
- `data/scratch/S517_gross_vs_net.csv` — year-by-year side-by-side, 1925-2024
- `data/raw/bea/fixed_assets_4_2_gross_stock.csv` — Table 4.2 fetch (Fisher quantity index)
- `data/raw/bea/provenance_fixed_assets_4_2.json` — fetch provenance
- `code/E08_exploration/fetch_bea_table_4_2.py` — fetch script
- `series_registry.json` — S517 entry (status: validated_book_and_extension)
- Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, Appendix H
- BEA Fixed Assets Methodology: https://www.bea.gov/resources/methodologies/fixed-assets-accounts
