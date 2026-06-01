# RMWND Industry Concordances

**Last updated**: 2026-05-24 (v1.1 Phase 5)
**Maintainer**: RMWND project
**Scope**: Industry-classification crosswalks used in the Shaikh & Tonak (1994) replication and its 1990–2024 extension.

This directory documents every concordance file currently used (or considered for use) in RMWND's productive/unproductive partitioning, capital-stock decomposition, and sectoral labour-value calculations. It is **descriptive, not prescriptive**: it inventories what exists in the project today and what alternative concordances a future iteration might consider, without committing to any new bridge construction.

---

## Files actually used by RMWND

### `sic_naics_bridge.csv` (this directory)

| Field | Value |
|---|---|
| Purpose | Bridge BEA 85-sector I-O (1967 benchmark) to BEA 71-NAICS, carrying productive/unproductive classification through both classification systems. |
| Rows | 135 (covers all 85 I-O sectors, 64 unique NAICS-71 codes; one-to-many mappings represented as repeated rows) |
| Key columns | `bea_io_85_code`, `bea_io_85_name`, `sic_range`, `st_classification` (Shaikh-Tonak productive/unproductive partition for I-O), `bea_naics_71_code`, `naics_71_st_classification`, `bridge_quality`, `notes` |
| Source attribution | Manual construction (RMWND project); productive/unproductive flags follow Shaikh & Tonak (1994) Ch. 5 and are cross-checked against Mohun (2013) Tables 2–3. |
| Used by | (planned) Stage 5 Phase 2.A refinement of S517 (productive capital stock) and Ch. 7 labour-value coefficient redistribution. Not yet wired into any L## / P## script as of v1.1. |

### `../book_tables/`

The book-period historical concordance work that RMWND actively consumes is the **85-IO → 13-NIPA** mapping shipped under `Inputs/ST2/Inputs/Concordances/` (see below); the local `data/source/concordances/` directory currently only holds `sic_naics_bridge.csv` itself.

---

## Files inherited from `Inputs/ST2/Inputs/Concordances/`

These files were carried in from the Phase-3 historical replication project (the predecessor that fed RMWND's KB). They are **read-only inputs**; do not edit in-place. See `Inputs/ST2/Inputs/Concordances/CONCORDANCE_METHODOLOGY.md` for the original methodology write-up.

### `io_85_to_nipa_13_concordance.csv`

| Field | Value |
|---|---|
| Purpose | Map 85 BEA I-O sectors (1967 benchmark) to 13-industry NIPA classification, with Mohun (2013) productive/unproductive flags. Enables distribution of aggregate NIPA employment to detailed I-O sectors for labour-value coefficient calculations. |
| Rows | 85 (one row per I-O sector) |
| Period | 1948–1989 (book period) |
| Source attribution | BEA 1967 85-level Sectoring Plan; Mohun (2013) "Unproductive Labor in the U.S. Economy 1964–2010" Tables 2–3 (productive/unproductive); BEA NIPA 13-industry historical classification; Shaikh & Tonak (1994) Ch. 5 methodology. |
| Used by | Future Ch. 7 real-fix (per `Technical/Handoffs/CH7_REAL_FIX_PLAN.md`); currently the Ch. 7 proxy series (S701/S702/S703) bypass the concordance and use a Leontief-inverse mean column sum instead. |

### `naics_71_to_classification.csv`

| Field | Value |
|---|---|
| Purpose | Direct productive/unproductive labelling at the BEA 71-NAICS level (extension-era classification). |
| Rows | 71 |
| Period | 1997+ (NAICS era) |
| Source attribution | RMWND/predecessor manual classification following Mohun (2013) and Shaikh-Tonak Ch. 5. |
| Used by | Extension-era proxy for productive-sector aggregation when paired with BEA GDPbyIndustry. |

### `ISIC3_to_NAICS_crosswalk.csv` and `ISIC4_to_NAICS_crosswalk.csv`

| Field | Value |
|---|---|
| Purpose | WIOD 56-sector (ISIC Rev. 3/4) ↔ NAICS crosswalk for cross-national comparison. |
| Rows | many (one-to-many with Mapping_Quality scores) |
| Period | 1995–2014 (WIOD coverage) |
| Source attribution | WIOD documentation + manual ISIC↔NAICS mapping; quality scores carried in `Mapping_Quality` / `Coverage_Percentage` columns. |
| Used by | Not used by current RMWND series. Available for future international-comparison work (e.g., ES17xx Karabacak–Tonak 2022 cross-country profit-rate replication). |

### `classification_crosswalks.xlsx`

| Field | Value |
|---|---|
| Purpose | Multi-sheet workbook collecting the above CSVs plus auxiliary lookups (SIC↔NAICS bridge tables at multiple aggregation levels). |
| Source attribution | RMWND predecessor project (Phase-3 historical replication). |
| Used by | Reference only — the CSVs are the operational format. |

---

## Alternative variants to consider

The productive/unproductive partition is the most consequential methodological choice in any Shaikh-Tonak replication, and several published variants exist. RMWND v1.0/v1.1 has chosen the original Shaikh-Tonak partition; the variants below are documented here for transparency and for future variant-tracking work via `anu-variant`.

| Variant | Partition definition | Primary differences from ST 1994 | When to consider |
|---|---|---|---|
| **Shaikh & Tonak (1994) — current default** | Ch. 5 partition: trade (SIC 50–59), FIRE (60–67), business services (73–74), government = unproductive; rest productive | Baseline | Default for RMWND book-period and extension. |
| **Mohun (2005)** "Distributive shares in the US economy, 1964–2001" (Cambridge Journal of Economics) | Treats *all* of government as unproductive (matches ST); but reassigns parts of transportation/communications based on commodity-vs-service distinction | Moves marginal sectors; affects level of S*/V* by 2–5% | If replicating Mohun's 1964–2001 series exactly. |
| **Mohun (2013)** "Unproductive Labor in the U.S. Economy 1964–2010" (RRPE) | Adds explicit "occupational filter" within productive industries (supervisory labour reclassified as unproductive); SIC/NAICS partition itself is closer to ST | Reduces productive-sector V* by 10–15%; raises S/V | If incorporating supervisory-labour reclassification. Used internally for current productive/unproductive flags. |
| **Moos (2017)** "The implications of changes in industrial structure for the rate of profit" | Industry partition close to ST, but adds explicit FIRE-rents subtraction from K* | Mainly affects K* (denominator), not S* or V* | Future Stage 5 Phase 2.A refinement of S517. |
| **BEA-standard productive partition** (no Marxian filter) | Goods-producing vs services-producing, per BEA NIPA Table 6.1 | Not a Marxian concept — included for sensitivity comparison only | Reference benchmark; documents how non-Marxian the BEA aggregates are. |

A planned future iteration could implement these as named variants per `anu-variant` (VPRs at `Technical/docs/variants/`), with each variant's chopped output written under a versioned suffix (e.g., `S513_mohun2013.csv`) so the methodological choice is auditable per-series.

---

## Status

- **Stage**: Stage 3 (ingestion) for `sic_naics_bridge.csv` complete; no L## / P## script consumes the bridge file yet.
- **Decisions**: see `Council/Druck/docs/decisions/0002.md` for the Shaikh-Tonak partition decision in the book period.
- **No new concordance creation in v1.1 Phase 5** — this README is documentation only. New bridge construction (e.g., a NAICS-2007 ↔ NAICS-2017 update or a Moos K*-decomposition table) is deferred to a future stage.
