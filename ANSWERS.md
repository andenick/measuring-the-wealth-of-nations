# Measuring the Wealth of Nations — The Best Answers

**Replication of Shaikh & Tonak (1994) · answers as of v2.1 · every number verified against the canonical build**

This is the answers-first layer. Each question gets the direct answer, then the basis in two or three sentences, then a pointer into the package apparatus. Nothing here is asserted without a verified artifact behind it.

---

## 1. Did the rate of exploitation keep rising after the book ended in 1989?

**Yes — on the book's own concept, e rises from 2.44 (1989) to ≈4.46 (2024), with an honest range of ≈3.6–4.9.**

The extension uses the Shaikh–Tonak formula with the input-output uplift factor now *measured annually* from BEA benchmark and supply-use tables (not assumed): it reproduces the book's 1989 value exactly, passes the frozen assumption's 1.571 in the mid-1990s, and rises thereafter as trade margins grew. The conservative lower-bound arm (uplift frozen at its 1989 value) still reaches 3.95. The "strange drop to 1.27" in earlier versions was a splice artifact, now removed and registered.
*See `DIVERGENCE_REGISTER.json` (DIV-028, DIV-071) and the S506 series documentation + band sidecar.*

## 2. How faithful is the replication to the printed book?

**Of the 882 printed data cells the project targets, 82.7% reproduce at the book's printed precision, the rest are registered divergences, and — after the final adjudication — exactly 0 cells book-wide remain unexplained.**

Every printed column of the book's 76 tables was diffed cell-by-cell against the build. Zero targeted cells are missing. The two cells that were previously "unexplained" — the 1964 tax entries S601/S603 vs Appendix N.1 (+1.8% and +11.8%) — were adjudicated as *chosen* divergences (S601: BEA vintage + labor-share; S603: basket breadth without the homeowner property filter) and registered as DIV-072/DIV-073, so the book-wide unexplained count is now zero. Excluding the 72 Appendix-C matrix cells (the model's *inputs*, not printed outputs) is disclosed: counted as failures they'd move the headline to 76.4%.
*See `DIVERGENCE_REGISTER.json` and the per-series documentation.*

## 3. Was the book right that the profit rate fell?

**Yes — and the replication now reproduces the book's own profit rate essentially exactly: the book-faithful gross-capital variant matches the printed r\* with mean error 0.0025, 42/42 years at printed precision, falling over 1948–89 with the trough in 1982.**

The headline shipped series (net capital basis) shows the same turning points with a damped fall (−5.7% vs the book-faithful −10.1%); the review proved the near-match of the old series to the book was a lucky cancellation, so the book-faithful gross arm (S513/S514/S517-GROSS-A) was added rather than pretending. Post-1997 a current-cost gross capital stock genuinely cannot be built (BEA discontinued it) — that limit is real and registered.
*See `DIVERGENCE_REGISTER.json` (DIV-058, DIV-070) and the S513/S514/S517 series documentation.*

## 4. What did the replication find wrong in the book itself?

**Two printed errata (1954 C\*_m should be 261.36; 1958 e should be 2.01) and a 14-year digitization misalignment risk in the labor appendix — all corrected and now matching exactly; nothing that disturbs the book's conclusions.**

*See `DIVERGENCE_REGISTER.json` (73 entries — every deliberate deviation, book erratum, and data-vintage break, each with rationale).*

## 5. What is genuinely uncertain or not knowable?

**Four things, all disclosed:** (i) the royalties term of the Marxian gross product is not observable annually after 1992 — it is carried from the 1992 benchmark measurement and dominates the uncertainty band; (ii) the SIC→NAICS classification change adds a small (+3.7%) calibrated jump at 1997; (iii) gross capital stock in current dollars ends in the mid-1990s (BEA discontinuation), so book-basis r\* is book-period-only; (iv) four external-study series (XS1101/1201/1202/1602) honestly FAIL validation pending paywalled source data. Nothing is interpolated synthetically; gaps are `nan`, never filled.
*See `DIVERGENCE_REGISTER.json` and the per-series documentation.*

## 6. How good is the project overall?

**Adversarially-audited scores: Completeness 96/100, Replication grade A, Thoughtfulness A−.** All 64 series carry full documentation, independent validation anchors, and gates (anu-doctor 0/0; pytest 95/2/2; per-series validators 60 PASS / 4 honest registered FAILs). Validator honesty is complete — two series gained genuine book anchors, and every remaining echo-the-output anchor is explicitly labeled as such with an independent range backstop — and the release engineering was rebuilt. The one-line verdict: *the numbers are sound*.
*See `CHANGELOG.md` and the package README.*

## 7. Where do I get the data?

- **Interactive**: shaikh.heterodata.org (explore + CSV/XLSX/Parquet downloads, 60 published series, 1948–2024/25).
- **Package**: github.com/andenick/measuring-the-wealth-of-nations (v2.1 — data, per-series documentation, provenance chains, divergence register). **New in v2.1**: the book-faithful gross-capital profit-rate variants (S513/S514/S517-GROSS-A) and the reconstructed time-varying-kIO rate-of-exploitation series (S506-EXT-MARX-KIO, with its uncertainty-band sidecar), alongside honest λ precision bands and the restored per-series author quotes.

---

## How this document works (the method behind the answers)

Every campaign in this project ends in three layers, and this brief is the top one:
1. **Answers** (this file): the direct claim, one caveat, one pointer.
2. **Verdicts and memos**: the reasoned documents where each claim is argued and scored.
3. **Workpapers**: the scripts, cell ledgers, and raw-source provenance (sha256-manifested) that let anyone recompute any number from government files.

A claim may only appear in layer 1 if it survived layer 3.
