# EPR: S514 - Capacity-Adjusted Profit Rate (r*_adj = r* x TCU/100)

**Series**: S514
**Generated**: 2026-05-23T00:00:00Z
**Updated**: 2026-05-24 (v1.2 Iter 3 stock-form lockstep)
**Status**: validated_book_and_extension (stock-form primary)

## 1. shaikh_source

"Since we are concerned here with the long-term tendencies of the rates of profit, all measured ratios are adjusted for cyclical fluctuations by means of a measure of capacity utilization developed in Shaikh (1987, 1992a). The rate of profit may be thought of as responding to long-term structural changes in the rate of surplus value and the organic composition of capital, and to short-term fluctuations in capacity utilization." -- Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5, p. 124. See also p. 129 for the empirical decomposition of the cyclical and structural components.

## 2. shaikh_appendix_ref

Table 5.11, r*_adj column (1967-1989; coverage starts in 1967 because the Federal Reserve G.17 capacity-utilization series begins in 1967); Figure 5.11. Underlying TCU series: Federal Reserve Statistical Release G.17 (Industrial Production and Capacity Utilization), 1967-present.

## 3. extension_source

DERIVED formula series. Extension is computed each year as:

    r*_adj = S513 x TCU / 100

where S513 is the (derived, extended) Marxian profit rate and TCU is total capacity utilization from FRED. Specifically, the cached FRED series at `data/raw/fred/fred_tcu_capacity_utilization.csv` (mirrored from `Inputs/ST2/Inputs/API_Data/FRED/fred_tcu_capacity_utilization.csv`; provenance in `Inputs/ST2/Inputs/API_Data/FRED/provenance.json`) supplies the TCU multiplier. Primary FRED identifier: `TCU` (Total Capacity Utilization, all industries); the manufacturing alternative `CAPUTLB00004S` is retained as a variant for the Shaikh (1987, 1992a) manufacturing-centric construction.

### Form choice (v1.2 Iter 3 stock-form lockstep with S513)

S514 is derived from S513 via TCU multiplication. Its form choice is therefore not independent: it follows S513's form choice exactly. As of v1.2 Iter 3, S513 adopts **stock-form r* = S*/(K*+V*)** as primary across the entire 1948-2024 span (per book Table 5.11 verbatim definition at p.122 §5.5; see `VPR_S513_stock_vs_flow_DECISION_BRIEF.md`, recommendation HIGH-confidence). S514 mirrors this:

- **S514-A** (1948-1989): S513-A (stock-form book r*) x TCU/100. NaN pre-1967.
- **S514-EXT** (1998-2024): S513-EXT (stock-form extended r* = S505-COMBINED / (S517-COMBINED + S504-COMBINED)) x TCU/100. Coverage gap 1990-1997 inherited from S513-EXT.
- **S514-COMBINED**: S514-A 1948-1989 concatenated with S514-EXT post-1989.
- **S514-FLOW** (SECONDARY, _secondary: true, stage=secondary_variant): S513-FLOW (flow-form r* = S505-COMBINED / (S502-COMBINED + S504-COMBINED)) x TCU/100. Retained as reference variant for cross-check against the v1.1 published flow-form, **not used in S514-COMBINED**. See DIV-012 for the cross-version disclosure.

v1.1 carried a stock-form 1948-1989 plus flow-form 1998-2024 splice that produced a wrong-sign trend artifact (+24% over 76 years vs the book's documented -59% decline). v1.2 closure restores book canonical form across the full range.

## 4. extension_url

- FRED TCU (all industries): https://fred.stlouisfed.org/series/TCU
- FRED CAPUTLB00004S (manufacturing alternative): https://fred.stlouisfed.org/series/CAPUTLB00004S
- Underlying Federal Reserve G.17: https://www.federalreserve.gov/releases/g17/

For the S513 input, see `S513_EPR.md`.

## 5. conceptual_continuity

Shaikh & Tonak define the capacity-adjusted Marxian profit rate as r*_adj = r* x TCU, separating long-run structural movements of profitability from short-run swings in capital usage (Ch. 5, p. 124; Table 5.11). The modern FRED TCU series is the direct successor to the Federal Reserve G.17 utilization measure that Shaikh & Tonak themselves used; conceptual continuity for the TCU factor is therefore near-perfect within the 1967-onward window. The full construct's continuity reduces to (a) the continuity of S513 (see `S513_EPR.md`) and (b) the continuity of FRED TCU. Coverage gap 1948-1966 is intrinsic to the data source, not a methodological defect: the book's r*_adj also begins in 1967. Anti-lazy-splice safeguard: the V03 validator rejects any direct splice of r*_adj and requires formula recomputation from S513 x TCU/100. Form continuity (v1.2 onward) is full stock-form across 1948-2024, matching the book's Ch.5 §5.5 stock-form definition; the flow-form secondary subseries is retained only for reference and is not used in any headline construct.

## 6. vintage_note

Book vintage: Federal Reserve G.17 capacity-utilization series as of the late 1980s, applied to a 1989-vintage stock-form r*. Modern vintage: FRED TCU was substantively revised in 2002 (G.17 Industrial Production redesign), so pre-2002 TCU values are not strictly comparable level-by-level to post-2002 values; FRED's published series carries the revised methodology back through the entire history, so the revision shows up as a level shift in the historical reconstruction rather than as a break in the published series. Vintage divergence of r*_adj is dominated by S513's own vintage issues (notably the BEA 2013 R&D/IPP capitalization through S517 in the stock-form denominator). Last cached fetch of TCU: see `Inputs/ST2/Inputs/API_Data/FRED/provenance.json`.

## 7. v1.2 Iter 3 form-switch references

- `Technical/docs/variants/VPR_S513_stock_vs_flow.md`
- `Technical/docs/variants/VPR_S513_stock_vs_flow_DECISION_BRIEF.md`
- `Technical/_v1.2_patches/S514_stockform_patch.json`
- `Technical/_v1.2_patches/DIVERGENCE_REGISTER_DIV012_patch.json` (S513 + S514 form-change disclosure)
- DIV-012 (supersedes DIV-009)
