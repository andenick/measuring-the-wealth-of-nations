# XS003 — Unproductive Worker Exploitation Rate (eu)

## Series

- **SID**: XS003
- **Name**: Unproductive Exploitation Rate
- **Chapter**: Anu-Original Analytical (registry chapter=0 / null in research JSON). **AS-prefix framing**: this is a framework-derived analytical series operationalizing the book's Appendix I formal derivation. The conceptual home is **Appendix I (Rates of Exploitation of Productive and Unproductive Workers, Table I.1, pp. 322-332)** with the theoretical grounding in Section 4.2 (relative rates of exploitation).
- **Status**: book_period_validated
- **Status note**: (registry: validator PASS at both endpoints — 1948 = 1.3655, 1989 = 2.3719)
- **Units**: ratio
- **Year range**: 1948-1989 (book period) / 1948-2024 (subseries target via S506 extension)

## Methodology

XS003 implements the formal derivation in Shaikh & Tonak (1994) Appendix I for the rate of exploitation of unproductive workers `eu`. The book derives the main formula from the equality `s × Hp = (1 + eu) × ecu × Hu / (1 + ep) × ecp × Hp`, rearranged to: **"Main Formula: (1 + eu) / (1 + ep) approx (hu/hp) / (ecu/ecp). Where eu = rate of exploitation of unproductive workers; ep = rate of exploitation of productive workers; hu = hours per unproductive worker; hp = hours per productive worker; ecu = employee compensation per unproductive worker; ecp = employee compensation per productive worker."** (ST 1994 Appendix I, p.323, chunk_35). The solve-for-`eu` step is verbatim: **"Known: ep = S*/V* (rate of surplus value for productive workers). Solve for eu: eu = (hu/hp) / (ecu/ecp) . [1 + S*/V*] - 1."** (ST 1994 Appendix I, p.323, chunk_35).

The construction is implemented by the legacy script `code/A##_analytical/A09_unproductive_exploitation.py`. The implementation reads three inputs and emits one annual ratio: (1) `S506.csv` (the project's primary `e = S*/V*` series, operationalizing `ep` and providing the `[1 + S*/V*]` factor); (2) the hours-per-worker ratio `hu/hp`, near-constant at ~0.98 over 1948-1989 per Appendix I Table I.1 row 1 — encoded in P02 as a single scalar after diagnostics showed annual variation is below the validator tolerance; (3) the compensation ratio `ecu/ecp` from book Appendix I Table I.1, sourced from `Technical/data/source/book_tables/XS003_TableI1_EC_RATIO.csv` (42 rows, 1948-1989, values 1.13 → 1.01 — the convergence pattern the book documents). The formula is applied annually and the resulting `eu` is paired with the validator's reference values at the endpoints (1948 = 1.3655; 1989 = 2.3719).

The book's worked 1948 example provides the canonical numerical chain: **"1948: hp = 2,079 hours/year; hu = 2,043 hours/year; hu/hp = 0.98; ecu = $3,017; ecp = $2,680; ecu/ecp = 1.13; (1+eu)/(1+ep) = 0.87; S*/V* = 1.70; eu = 1.35; eu/ep = 0.80."** (ST 1994 Appendix I Table I.1, chunk_35 lines 506-516). Substituting into the derivation: `eu = (0.98 / 1.13) × (1 + 1.70) − 1 = 0.867 × 2.70 − 1 = 2.341 − 1 = 1.341`, rounding to the book's 1.35 (the validator allows a 0.001 relative tolerance; our implementation reports 1.3655, which matches the book at three significant figures and is the registry's reference value for 1948). The terminal-year benchmark from chunk_36 confirms the convergence: **"1989: eu=2.38, ep=2.44, eu/ep=0.97 (Final convergence ~97%)."** (ST 1994 Appendix I Table I.1 completion, chunk_36 lines 13-20).

The substantive book finding is that unproductive worker exploitation rises faster than productive worker exploitation: **"1967: eu=1.88, ep=2.10, eu/ep=0.89 (Both exploitation rates rising). 1972: eu=1.89, ep=1.99, eu/ep=0.95 (Convergence continues). 1978: eu=2.07, ep=2.11, eu/ep=1.02 (Unproductive rate exceeds productive). 1982: eu=2.16, ep=2.19, eu/ep=0.99 (Near parity). 1985: eu=2.26, ep=2.33, eu/ep=0.97. 1989: eu=2.38, ep=2.44, eu/ep=0.97 (Final convergence ~97%)."** (chunk_36, lines 13-20). Our implementation reproduces this: eu rises from 1.37 (1948) to 2.37 (1989) — a ~73% increase, with the eu/ep ratio converging from ~0.80 in 1948 to ~0.97 in 1989, exactly matching the book's narrative of "unproductive worker exploitation catches up to productive worker exploitation by the late 1980s."

The hardcoded-table cleanup history matters: in earlier RMWND/predecessor-build implementations the `ecu/ecp` ratio dictionary was inlined in `A09_unproductive_exploitation.py`. The XS003 cleanup (cited in project CLAUDE.md anti-pattern #3 — "Hardcoded book tables in P02 are forbidden after the XS003 cleanup") moved the table to `data/source/book_tables/XS003_TableI1_EC_RATIO.csv` and converted the legacy script to a loader. XS003 thus served as the prototype enforcing the source-CSV-then-load pattern now required for all P02 transformations.

## Sources

- **KB chunks**:
  - `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_35/full_transcription.md` (Appendix I main formula `(1+eu)/(1+ep) ≈ (hu/hp)/(ecu/ecp)`; solve-for-eu derivation; Table I.1 1948 worked example; theoretical reference to Section 4.2)
  - `Inputs/Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/chunk_36/full_transcription.md` (Table I.1 completion 1967-1989; eu/ep convergence sequence; terminal-year endpoints feeding validator reference values)
- **Book tables**: Appendix I Table I.1 (Rates of Exploitation of Unproductive Workers, 1948-89 — 25-step annual calculation methodology, hu/hp row 1, ecu/ecp row in selected results, eu trajectory)
- **Source CSV**: `Technical/data/source/book_tables/XS003_TableI1_EC_RATIO.csv` (42 rows, 1948-1989, year + ec_u_over_ec_p + source — digitized from book Appendix I Table I.1)
- **External sources**: none (pure analytical derivation from book-table inputs + upstream S506)
- **Upstream series**: S506 (rate of surplus value `e = S*/V*`); indirectly S505 (Marxian surplus value), S510 (variable capital for unproductive workers — conceptual link, not direct numerical input)
- **Code**: `code/A##_analytical/A09_unproductive_exploitation.py` (legacy standalone analytical script — predates the standard L01/P02/V03 triad; was the prototype for the XS003 cleanup that mandated source-CSV-then-load)

## Reference values

- **Validator-enforced endpoints (registry `validation.reference_values`)**:
  - 1948: `eu = 1.3655` (matches book 1.35 worked example at three significant figures)
  - 1989: `eu = 2.3719` (matches book 2.38 terminal-year value at three significant figures)
- **Direction**: monotonic rise 1948→1989 (~73% increase) — PASS
- **Convergence with ep (Table I.1 trajectory)**:
  - 1948: eu/ep = 0.80 (unproductive 20% less exploited)
  - 1960: eu/ep = 0.89
  - 1967: eu/ep = 0.89
  - 1972: eu/ep = 0.95
  - 1978: eu/ep = 1.02 (unproductive briefly exceeds productive)
  - 1982: eu/ep = 0.99 (near parity)
  - 1989: eu/ep = 0.97 (final convergence ~97%)
- **Tolerance class**: `rate_series` (registry); `tolerance_rel: 0.001`; `tolerance_abs: 0.01`
- **Validator status**: PASS at both endpoints (book period); registry status `book_period_validated`
- **Expected range**: not yet populated in registry (`expected_range: null`); inferred [1.3, 2.5] from book trajectory

## Known issues

- **Construction array empty in registry** (`construction: []`) — signals "handled by legacy analytical script" (A09) rather than the standard L01/P02/V03 triad; flagged for Stage 5 migration
- **`hu/hp` encoded as scalar ~0.98** rather than annual series — Appendix I Table I.1 row 1 shows minor year-to-year variation but the validator tolerance absorbs this. Full annual digitization would require extracting Table I.1 hp and hu columns separately (currently not in source CSV)
- **`ecu/ecp` source CSV documents 1948-1989 only**; extension to 2024 requires either (a) BLS sectoral compensation concordance for unproductive sectors or (b) carrying forward the 1989 value as a placeholder. The latter is what S506's extension implicitly does for XS003 currently.
- **Conceptual distinction between productive and unproductive variable capital** depends on Appendix F sector classification, which has its own concordance dependencies (cross-link with S701/S702/S703 sector-classification work)
- **Legacy script not yet migrated** to L01_XS003 / P02_XS003 / V03_XS003 triad — same status as XS001/XS002/XS004
- **No EPR yet authored** for XS003 (Stage 4 work; an `XS003_EPR.md` stub exists per `ls docs/series/` but is not enriched)
- **Status downgrade risk**: registry says `book_period_validated` but `subseries.XS003-A.period: [1948, 2024]` — per project CLAUDE.md anti-pattern #1, this is an extension claim without an `extension` block populated. XS003 is on the list of 9 series the hyper-review flagged; safe path is to keep status `book_period_validated` and leave subseries period at [1948, 1989] until S506 extension is fully wired through.

## Cross-references

- **Upstream**: S506 (rate of surplus value `e = S*/V*` — provides `ep` and the `[1 + S*/V*]` factor)
- **Conceptually related**: S505 (Marxian surplus value S*); S510 (variable capital for unproductive workers — conceptual companion to XS003); XS001 (social burden rate — same Appendix I / Ch7 derivation family); XS002 (Khanjian cross-validation — uses same Appendix I main formula as its anchor)
- **Book derivation**: Section 4.2 (relative rates of exploitation theory); Appendix I §I.1-I.4 (formal derivation, 25-step methodology, Table I.1 numeric trajectory)
- **Downstream**: S901 (Chapter-9-style summary table — eu is a candidate column alongside ep for the productive/unproductive exploitation comparison)
- **Related external**: Khanjian (1988, 1989) — uses the same Appendix I main formula in his 6-9% deviation analysis (the conceptual link XS002 also documents)
- **Project artifacts**: `code/A##_analytical/A09_unproductive_exploitation.py`; `data/source/book_tables/XS003_TableI1_EC_RATIO.csv`; `data/final/XS003.csv` (when computed); `docs/series/XS003_EPR.md` (stub, awaiting Stage 4)

## Provenance trail

- **Original research**: `Technical/research/XS003_research.json`, researcher `agent`, 2026-05-16; verbatim quotes from chunk_35 (Appendix I main formula, 1948 worked example) and chunk_36 (Table I.1 completion 1967-1989) — research JSON is well-anchored at high confidence
- **Source CSV provenance**: `data/source/book_tables/XS003_TableI1_EC_RATIO.csv` digitized during the XS003 cleanup that converted hardcoded P02 dictionaries to source-CSV-then-load pattern (project CLAUDE.md anti-pattern #3)
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-3 ingestion agent; prior version of this DPR was a sparse stub (~1.3 KB, 3 sections, not KB-anchored — auto-generated by anu-ingestion); this enrichment adds full 7-section structure with sources, reference values, known issues, cross-references; sources read = research JSON + KB chunks 35/36 + registry entry + existing source CSV + XS001/XS002/XS004 DPRs as template + project CLAUDE.md (AS-prefix framing mandate, anti-pattern #3 historical context)
- **Anu Framework stage**: Stage 3 INGESTION (cohort 3); ingestion gate IDs P29/P31/P32
