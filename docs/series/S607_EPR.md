# EPR: S607 — Net Social Wage (NSW = B_w + G_w − T_w)

**Series**: S607
**Generated**: 2026-05-23T00:00:00Z
**Status**: book_period_validated (extension block populated; pre-computed extension table exists; extension execution pending in L01/P02)

## 1. shaikh_source

Operational definition from the research dossier (verbatim, derived from Chapter 5 §5.9 and Tonak 1984): "NSW = B_w + G_w − T_w, where B_w is government benefits to workers (S605), G_w is government services to workers (S606), and T_w is total taxes paid by workers (S604). A negative NSW means workers pay more in taxes than they receive in benefits and services — the state extracts net revenue from the working class." Empirical headline: "NSW is predominantly NEGATIVE for 1952–1989: 35 of 38 years show workers paying more in taxes than receiving in benefits and services. Only 3 years show positive NSW: 1975, 1976, and 1983 — all deep recessions with countercyclical benefit spikes and falling tax receipts." — Shaikh & Tonak (1994), *Measuring the Wealth of Nations*, Chapter 5 §5.9 ("The net transfer between workers and the state", pp.137–142, Figures 5.21–5.24) with detailed calculations in Appendix N (Tables N.1, N.2); methodology imported from Tonak (1984) PhD dissertation. (The book has no Chapter 6 on the net social wage — a prior "Chapter 6, Table 6.3" citation here was fabricated and is corrected.)

## 2. shaikh_appendix_ref

Appendix N (Table N.1 = 1964 benchmark mapping; Table N.2 = 1952–1989 rates) — the project-internal reconstruction file `Table6_3_NetSocialWage.csv` is named after an internal label, NOT a book table. Identity NSW = S605 + S606 − S604 (benefits-to-workers plus services-to-workers minus taxes-from-workers). Appendix N details the NIPA tables that feed B_w, G_w, and T_w (Tables 3.4, 3.6, 3.12, 3.15 of the then-current NIPA).

## 3. extension_source

DIRECT-splice composite. The predecessor build has already produced a faithful continuation through 2024: `data/source/book_tables/Table6_3_Extended.csv` (path canonical to the predecessor-build data tree). Table6_3_Extended is constructed by re-applying Tonak's exact NIPA-component decomposition to post-1989 BEA NIPA Tables 3.4, 3.6, 3.12, and 3.15, with cached BEA inputs at `data/raw/bea/nipa_3_1_govt_receipts_expenditures.csv`, `nipa_3_2_federal_govt.csv`, `nipa_3_3_state_local_govt.csv`, `nipa_2_1_personal_income.csv`, `nipa_T20100_compensation_1929_2025.csv`, and `nipa_6_10D_employer_contributions.csv` (provenance in `data/raw/bea/provenance_ch06.json`). The 1989 overlap value in Table6_3_Extended matches the book value identically (verified at the 1952 and 1989 endpoints). Methodologically the extension series IS the same construction continued, not a proxy or growth-rate splice.

## 4. extension_url

- BEA NIPA iTable (live interface for the underlying NIPA tables 3.4, 3.6, 3.12, 3.15): https://apps.bea.gov/iTable/iTable.cfm?reqid=19&step=2
- BEA Data Application API (programmatic NIPA pulls): https://apps.bea.gov/api/signup/
- For the dependent component EPRs, see `S604_EPR.md` (T_w), `S605_EPR.md` (B_w), `S606_EPR.md` (G_w).

## 5. conceptual_continuity

Shaikh & Tonak define NSW as the net fiscal balance between what workers receive from the state (cash benefits B_w plus imputed services G_w) and what they pay to it in taxes T_w (Ch. 6, Table 6.3). The construct is identity-defined and modern-NIPA-observable. The predecessor-build extension preserves the methodology *exactly*: same NIPA decomposition, same worker/non-worker tax allocation rules (with the Moos 2017 / Mohun 2005 cross-check showing 99.996% formula-reconstruction accuracy from component values per the research entry), same treatment of imputed services. The substantive *headline* of the extension — that NSW turns persistently positive in the early 1990s after being predominantly negative 1952–1989 — is an empirical finding, not a methodological divergence: classification rules and component formulas are identical book-period and extension-period. Cross-study sensitivity is documented (AS2 vs Moos r = 0.697; AS2 vs Tonak r = 0.611; Moos vs Tonak r = 0.876), and Moos's exact-component reconstruction validates the formula. Conceptual continuity is therefore the highest of any extending series in the Chapter 6 cluster.

## 6. vintage_note

Book vintage: NIPA tables 3.4, 3.6, 3.12, 3.15 as of approximately 1989–1992. Modern vintage: post-comprehensive-revision BEA NIPA (current through 2024 in `Table6_3_Extended.csv`). Vintage differences on pre-1990 values are negligible at the 1952 and 1989 endpoint-overlap (verified identical), so the splice is treated as `direct` rather than `level`. Major *level* shifts post-1989 — ACA expansion, Medicare Part D, TANF, multiple UI extensions, payroll tax changes, 1996 welfare reform — change the underlying components but not the construction methodology; the 1996 welfare-reform structural break is flagged in the research dossier as a known regime change. Last cached fetch of feeding BEA NIPA components: see `data/raw/bea/provenance_ch06.json`. Pre-computed predecessor-build extension table (`Table6_3_Extended.csv`) is the canonical extension input; raw BEA pulls are retained for re-validation.
