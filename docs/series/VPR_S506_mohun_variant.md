# Variant Provenance Record — S506 / S504 Mohun rate-of-surplus-value variant

**Variant ID:** VAR-S506-MOHUN
**Parent series:** S506 (rate of exploitation e = S*/V*), with knock-on S504 (variable capital V*) variant
**Author:** workpackage A, RMWND comprehensive review, 2026-07-01
**Status:** documented + quantified (extension-era implementation; registry-patch-level integration proposed, not pipeline-wired to protect the build)

## Motivation

Task T3: implement Mohun (2005) SM/V "Marxian variable capital" as an anu-variant and quantify it
against the workpackage A primary S506 extension. Mohun's rate of surplus value differs from Shaikh–Tonak's
by definitional latitude in the productive/unproductive split (Mohun treats **Information entirely
productive** and uses a broader productive perimeter). The forensic (`P1_FORENSIC_REPORT.md`) records
Mohun's faithful US 1989 rate at **1.87** — between the book's 2.44 and the naïve BEA rate (~0.80) —
which is why a Mohun variant is a useful triangulation point.

> **Provenance caveat (workpackage E finding):** `research/XS1401_research.json`–`XS1403_research.json` are
> **book-period ST-method reconstructions, NOT Mohun's own published figures** (workpackage E DIV-C01). This
> VPR is therefore the **extension-era implementation** of Mohun's *method*, not a transcription of
> Mohun's tables. The equations are taken from `research/XS1403_research.json` (Mohun 2005 SM = net
> value added − productive-worker compensation; V = productive-worker compensation).

## Construction (extension-era Mohun-style rate)

Over the broader Mohun productive perimeter **partition B = A + Information(51) + Professional(54)**
(NAICS top-level), using BEA GDP-by-Industry `va_components`:

```
e_mohun_t = (VA_partB_t − comp_partB_t) / comp_partB_t
```

This is a *sector-compensation-denominator* lower bound (Mohun's own SM/V uses production-worker-only
V, which is smaller, so Mohun's published rate is higher — ~1.87 rising). The variant here isolates
the **partition-width sensitivity** (A → B) at extension-era data.

## Quantification vs the workpackage A primary (at the seam and beyond)

| year | e_mohun (partB, sector-comp denom) | primary S506-EXT (partA) | book-concept S506-EXT-MARX |
|---|---|---|---|
| 1998 | 0.782 | 0.789 | 2.971 |
| 2005 | 0.925 | 0.939 | 3.437 |
| 2010 | 1.051 | 1.087 | 3.895 |
| 2020 | 0.922 | 0.986 | 3.586 |
| 2024 | 1.033 | 1.147 | 3.952 |

**Finding:** widening the productive perimeter A → B (Mohun's Information-productive choice) moves the
consistent BEA rate by only **−0.01 to −0.11** — near-neutral for the *ratio* (consistent with the
forensic's scope-neutrality result, DIV-A13). The large gap to the book concept (~2.4×) is the I-O
reallocation (DIV-A10), NOT the productive-perimeter choice. Mohun's published 1.87→ level is reached
only when V is restricted to **production-worker** compensation (a smaller denominator than sector
compensation); that restriction, not partition width, is what lifts the level.

## Relation to XS1403 (Mohun external-study series)

XS1403 (`research/XS1403_research.json`) carries the Mohun 2005 equations but is a book-period
ST-method reconstruction (workpackage E DIV-C01, rebuild-vs-reclassify decision pending). This VPR's
extension-era numbers should feed that decision: the extension-era Mohun-style rate is constructible
from BEA `va_components` and lands as a lower bound to Mohun's production-worker-denominator rate.

## Registry integration (proposed, not wired)

Proposed as `S504-MOHUN` (variable capital on Mohun's production-worker basis) + `S506-MOHUN`
(knock-on e), emitted as variant subseries. NOT wired into P02 in this pass to avoid perturbing the
64-series build; queued as a registry patch for P5/P7. See `WP-A_REGISTRY_PATCHES.json`.
