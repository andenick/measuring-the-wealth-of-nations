# Table F.1 (Productive-Share Filter) — Provenance

**File**: `Table_F_1.csv`
**Created**: 2026-05-23
**Agent**: v1.1 Phase 4 Ch7 real-fix extraction (agent 2)

---

## What this table is (and is not)

**This is** an 85-sector BEA 1967 I-O productive-share filter for Ch7 (S701, S702, S703) labor-coefficient real-fix work. Each row maps one I-O sector to a productive_share value in [0,1].

**This is NOT** a verbatim transcription of Shaikh-Tonak (1994) Appendix F Table F.1. Per KB Master Index and chunk_32 of the 1994 book extraction (pages 292-301), the book's actual Table F.1 is an annual labor-force decomposition (1948-1989, 42 years x 67+ variables in aggregated groups Lman, Lmin, Lcon, Ltrade, Lfin, Lgov, etc.), NOT a per-sector fractional productive-share filter.

---

## Why this substitution is defensible

Shaikh-Tonak's productive-share filter is implicitly defined by:
1. **Table 3.1** (book p. 60): Primary vs. Secondary sectoral structure (categorical)
2. **Section 3.3**: Productive labor methodology (categorical assignment)
3. **Table F.1**: Aggregate decomposition by sector group (consistent with the categorical assignment)

The 85-sector fractional table the user expected does not exist in the book. Shaikh-Tonak applied categorical sector classifications (productive=1.0, unproductive=0.0), with within-sector fractional adjustment handled separately via BLS production-worker ratios (Mohun 2005 sec. 3.3.2; ST 1994 Ch.5). So the 85-sector filter must be constructed.

---

## Construction

### Primary source

`Inputs/ST2/Inputs/Concordances/io_85_to_nipa_13_concordance.csv` and `CONCORDANCE_METHODOLOGY.md` (dated Nov 6 2025 in ST2 predecessor project).

That concordance maps all 85 BEA 1967 I-O sectors to:
- 13 NIPA industries
- SIC code ranges
- Productive/unproductive/mixed/n.a. classification (categorical)

The classification itself was built per ST2 methodology doc from:
- **BEA 1967 85-level Sectoring Plan**
- **Mohun (2013)** "Unproductive Labor in the U.S. Economy 1964-2010" Tables 2 & 3 (KB at `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/2013_Mohun_Unproductive_1964_2010/`)
- **Shaikh-Tonak (1994)** Chapter 3 and Chapter 5 productive/unproductive framework
- **NIPA Industry Structure (1948-1989)** 13-industry classification

### Conversion to productive_share

| Source classification | productive_share | uncertain |
|---|---|---|
| productive | 1.0 | false |
| unproductive | 0.0 | false |
| mixed (sector 85, govt industry) | 0.167 | true |
| n/a (sectors 81 imports, 84 scrap) | (blank) | true |

The sector-85 mixed value (0.167) is the NIPA-13 row of CONCORDANCE_METHODOLOGY.md (1 productive sub-sector / 6 government sub-sectors = 16.7%). It is an order-of-magnitude proxy only; users computing Ch7 series should refine sector-85 (and possibly sector 12 Services aggregate if used at NIPA level) with BLS production-worker ratios at compute time.

---

## Coverage

- 85 sectors total (matches BEA 1967 85-level plan exactly)
- 75 sectors: productive (productive_share=1.0)
- 7 sectors: unproductive (productive_share=0.0)
- 1 sector: mixed (sector 85, productive_share=0.167, uncertain=true)
- 2 sectors: n/a (sectors 81 imports, 84 scrap — uncertain=true, blank productive_share)

---

## Limitations and required follow-ups

1. **Fractional shares are not in the original book**. ST/Mohun handle within-sector productive ratios via BLS production-worker / total-worker series. Anyone using `productive_share=1.0` for, e.g., Manufacturing sector 11-64, should optionally multiply by BLS PW/TW ratio to get the actual productive-worker share.

2. **Mixed sector (85) is a proxy**. The 16.7% value is the unweighted count ratio from CONCORDANCE_METHODOLOGY. For real Ch7 use, replace with sector-specific BLS-derived ratio.

3. **NAICS extension** (post-1989): Use `Inputs/ST2/Inputs/Concordances/naics_71_to_classification.csv` (different scheme: productive / trading / unproductive / govt_admin / govt_enterprise). Trading is unproductive in ST framework.

4. **Not validated against actual book pages**. No agent has read the BEA 1967 sectoring plan source PDF or independently verified each sector-to-SIC mapping. The ST2 concordance is taken on faith as the predecessor project's research output.

---

## Recommended Sraffa OCR follow-up (optional)

If a higher-fidelity table is required, the following book pages can be OCR'd:
- `Inputs/Salvaged/book_text_1994/pages/page0004-292.png` through `page0004-301.png` (KB-confirmed Appendix F pages)
- Output would be the actual 1948-1989 labor decomposition (Lp/Lu/L by sector group, annual), NOT a productive-share filter

For a sectoral productive-share table at the 85-sector level, the only authoritative source would be:
- Mohun (2013) Tables 2 & 3 (SIC/NAICS classification, KB extraction available)
- Or manual transcription of the BEA 1967 sectoring plan + categorical assignment per ST Ch.3

Both are already encoded in the ST2 concordance used as primary source for this CSV.

---

## STEP_LOG

Logged as `v1.1-phase4-appendix-F-extract` with outcome `partial` — table built from defensible derived source (ST2 concordance, Mohun-derived) rather than book Appendix F (which does not contain this content).
