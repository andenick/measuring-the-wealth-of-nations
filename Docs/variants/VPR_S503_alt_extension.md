# VPR: S503 Alternative Extension Variants

**Series**: S503 (Gross Final Product, GFP = TP* - C*_m)
**Variant ID**: VPR_S503_alt_extension
**Date**: 2026-05-24
**Author**: anu-rebuild v1.1 Phase 3
**Status**: exploratory (no methodology change committed)

## Status: DECLINED IN v1.2 — DEFERRED TO FUTURE COHORT

Per `VPR_S503_alt_extension_DECISION_BRIEF.md` (v1.2 Iter 1 examination), this VPR was evaluated and explicitly declined for v1.2 adoption.

**Decision rationale**:
- Retain Variant A: literal ST 1994 Appendix C SIC concordance preserved
- Variant B adoption requires coordinated S501/S502/S503 + 6 downstream series changes (cost ~1.5-2 cohorts)
- Only Mohun 2013 (ES1401) explicitly endorses NAICS 51 inclusion; other ES studies (Cronin, Moos, Tsoulfidis/Paitaridis, Karabacak/Tonak) retain narrow ST partition

**Future re-visit trigger**: when a coordinated multi-series concordance audit is in scope (likely v1.3 or later), specifically Variant B-prime (NAICS 51 only, Mohun-aligned) as the principled minimal adoption.

**Decision date**: 2026-05-24
**Decision authority**: v1.2 coordinator + Iter 1 examination agent recommendation

## Problem

S503's modern extension uses BEA GDP-by-Industry Value Added summed over a
narrow productive+trade NAICS partition:

```
A = [11 Agriculture, 21 Mining, 22 Utilities, 23 Construction,
     31G Manufacturing, 42 Wholesale, 44RT Retail, 48TW Transp./Warehousing]
```

The book's 1989 endpoint (Table H.1, column `GFP_star`) is **4363.57 Bn USD**.
The BEA 1997 endpoint under partition A is **3462.40 Bn USD** — a level
discontinuity of **-20.7%** at the SIC→NAICS junction (or, framed the other
way, the book endpoint exceeds BEA 1997 by 26.0%, which matches the
registry's `vintage_note` wording).

The narrow partition may understate VA by excluding services whose
productive content is arguably non-trivial under modern Shaikh-tradition
readings (information, professional/scientific/technical). This VPR tests
whether a broader partition shrinks the discontinuity, and at what
methodological cost.

Per the registry's `vintage_note` (lines 372 of `series_registry.json`),
the existing methodology accepts this discontinuity as a known vintage
artefact and applies a growth-rate splice that preserves post-1997 growth
profile via a 1990-1996 log-linear bridge.

## Variants Tested

| Variant | Partition                              | Rationale |
|---------|----------------------------------------|-----------|
| **A** (current)  | `[11,21,22,23,31G,42,44RT,48TW]`        | Direct port of S501/S502 productive-trade partition; matches S&T 1994 SIC-based productive boundary as concorded in S501 EPR Appendix C. |
| **B** (broader) | A + `[51, 54]`                          | Add Information (51) and Professional/Scientific/Technical Services (54). Both have substantial productive-labor content under modern Shaikh-tradition readings (software production, R&D, technical services embodied in commodity production). |
| **C** (broadest)| A + `[51, 54, 53]`                      | Variant B plus Real Estate / Rental / Leasing (53). Controversial: rent on land/buildings is typically unproductive under Shaikh's framework, but operating leases of productive capital goods and rental of productive assets are borderline. Most of the 53 aggregate is owner-occupied housing imputations (unambiguously unproductive). |

## Results

### Level discontinuity at SIC→NAICS junction

| Variant | 1997 BEA endpoint (Bn USD) | Discontinuity vs book 1989 (4363.57) | Qualitative judgment |
|---------|---------------------------:|--------------------------------------:|----------------------|
| **A**   | 3462.40                    | **-20.7%** (downward step)            | Current methodology; visible jump; mitigated by growth-rate splice + 1990-1996 log-linear bridge. |
| **B**   | 4356.20                    | **-0.2%** (essentially continuous)    | Near-perfect level continuity. The bridge interval becomes nearly flat. |
| **C**   | 5391.40                    | **+23.6%** (upward step)              | Over-shoots in the other direction; Real Estate aggregate is dominated by owner-occupied housing imputations and rent, which Shaikh's framework treats as unproductive. Not recommended. |

### Full-series scratch output

Years 1948..2024 (77 rows). See `data/scratch/S503_alt_extension.csv` for the
combined-arm time series under each variant (book 1948-1989 unchanged; log-linear
bridge 1990-1996 sized to that variant's 1997 endpoint; BEA 1997-2024 under
that variant's NAICS sum).

## Methodological Analysis

**Variant B's near-perfect level continuity is suggestive but not dispositive.**

Two competing interpretations:

1. **B is right**: The book's GFP_star aggregate (SIC-based) naturally
   includes some of what NAICS 51/54 contain, because SIC's old "services"
   division had overlap with these activities, and the book's productive
   partition implicitly captured some of them via SIC 73 (business services)
   and similar codes. The NAICS 1997 reclassification moved them into 51/54.
   Under this reading, the level match at 1997 reflects conceptual continuity.

2. **B is coincidence**: The 1997 level match is artefactual. NAICS 51 includes
   publishing, broadcasting, telecom, data services — heterogeneous activities
   only partially productive in Shaikh's strict sense. NAICS 54 includes legal,
   accounting, advertising, management consulting — most of which are
   distribution/circulation activities, not productive labor. Including them
   simply because the level matches is curve-fitting.

The principled tie-breaker: **S501 EPR Appendix C** documents the SIC→NAICS
concordance used across S501/S502/S503 as a coherent productive partition.
S501 and S502 also use partition A. Adopting B unilaterally for S503 would
break the cross-series consistency (TP* vs Cp* vs GFP would no longer share
the same productive boundary, breaking the identity GFP = TP* - C*_m that V03_S503
checks).

## Recommendation

**Retain Variant A as the primary methodology.** Variant B is documented here as
a methodology variant per anu-variant, not as a replacement. Reasons:

1. **Cross-series consistency**: S501, S502, S503 all use partition A;
   adopting B only for S503 would break the productive-boundary identity
   GFP = TP* - C*_m (V03_S503 validation).
2. **Provenance of the original concordance**: S501 EPR Appendix C documents
   the SIC→NAICS concordance for partition A with explicit reasoning. No
   equivalent concordance work has been done for partition B.
3. **Risk of curve-fitting**: Variant B's near-perfect 1997 level match is
   striking, but adopting it because the levels match (rather than because
   the underlying concordance is principled) would be a form of methodological
   target-shooting — exactly the failure mode that anu-framework rules
   warn against ("No Lazy Splices on Derived Quantities", "No Proxies").
4. **Variant C is rejected**: Including Real Estate (53) over-shoots and
   pulls in owner-occupied housing imputations that Shaikh's framework
   unambiguously treats as unproductive.

**However**, Variant B is sufficiently striking that:

- A future cohort should attempt a full SIC→NAICS concordance audit
  spanning S501/S502/S503 with NAICS 51 and 54 explicitly evaluated for
  productive content per Shaikh's criteria (necessary-labor inclusion test).
- If the concordance work supports inclusion, partition B should be adopted
  uniformly across S501/S502/S503 in a single coordinated change, not
  series-by-series.

The existing DIVERGENCE_REGISTER entry DIV-003 documents the SIC→NAICS
discontinuity as a known vintage artefact, and DIV-007 (added with this VPR)
tracks the variant exploration. No PIPELINE_STATE, registry, ledger, or
manifest changes are made.

## References

- `code/E08_exploration/E_S503_alt_extension.py` — variant computation script
- `data/scratch/S503_alt_extension.csv` — 1948..2024 levels for variants A, B, C
- `series_registry.json` — entry `series.S503`, especially `extension.provenance.vintage_note`
- `DIVERGENCE_REGISTER.json` — DIV-003 (proxy disclosure, related context); DIV-007 (variant tracking, added with this VPR)
- `code/L01_loaders/L01_S503_gross_final_product.py` — current loader (PRODUCTIVE_TRADE_INDUSTRIES = partition A)
- `code/P02_processors/P02_S503_gross_final_product.py` — current processor (growth-rate splice at 1997)
- `docs/series/S501_EPR.md` Appendix C — SIC→NAICS concordance methodology (referenced)
