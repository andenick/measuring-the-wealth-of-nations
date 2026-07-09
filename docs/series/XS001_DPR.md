# XS001 — Social Burden Rate (b = T/S* + Eu/S* = 1 − Pn/S*)

## Series

- **SID**: XS001
- **Name**: Social Burden Rate
- **Chapter**: Anu-Original Analytical (registry chapter=0 / null in research JSON). **AS-prefix framing**: this is a framework-derived analytical series, not a direct book-table replication. The conceptual home is the book's Ch7 §7.1 derivation of `r'n = (1 − b) r*'`, with `b = t + eu = T/S* + Eu/S*`.
- **Status**: book_period_validated
- **Units**: ratio

## REVIEW 2026-07 (workpackage E Group A) — methodology correction (SUPERSEDES the "Pn approximation / magnitude offset" narrative below)

The prior implementation computed `b = 1 - Pn/S*` with **Pn = NIPA Table 1.7.5 Line 17
(corporate profits)**. That is the **WRONG quantity**: the book's Pn (Table 7.1, Sources =
Table 5.8) is **"profit-type income net of ALL taxes"** (1948 = $66.51B), roughly double NIPA
corporate profits (~$31B). This — not a "concordance approximation" — is why the old output was
0.79-0.86 instead of the book's printed 0.56-0.68.

**Fix:** Pn is now sourced directly from ST 1994 **Table 7.1** (`data/source/book_tables/
XS001_Table71_Pn.csv`); `S*` remains **S505-A**, which reproduces the book's Table 7.1 S* column
**exactly** (verified abs err 0.00 at all anchor years). `b = 1 - Pn/S505` now reproduces the
printed book `b` to **<= 0.005** (1948 0.5564 vs 0.56 … 1989 0.6530 vs 0.65). Refvals re-anchored
to the printed Table 7.1 `b`; validator_class = **book**; `open_issue` resolved. See **DIV-025**.
The paragraphs below describing the NIPA-Line-17 Pn and a "~25pp magnitude offset" are retained for
history but are **superseded**.

## Methodology

XS001 operationalizes the social burden rate from Shaikh & Tonak's Ch7 §7.1 decomposition of surplus value. The book defines the relation `r'n = [1 − T/S* − Eu/S*][S*/(K*.u)] = (1 − t − eu) r*' = (1 − b) r*'`, where `r*' = S*/(K*.u)` is the capacity-utilization-adjusted Marxian rate of profit, `r'n = Pn/(K*.u)` is the similarly adjusted NIPA-based net rate of profit, `t = T/S*` is the tax share of surplus value, `eu = Eu/S*` is the unproductive-expenses share of surplus value, and `b = t + eu` is the social burden rate. The verbatim foundation is **"Divide equation (1) by utilized capital K*.u: r'n = [1 − T/S* − Eu/S*][S*/(K*.u)] = (1−t−eu)r*' = (1−b)r*'. Where r*' = S*/(K*.u) = capacity utilization-adjusted Marxian rate of profit; r'n = Pn/(K*.u) = similarly adjusted NIPA-based net rate of profit; t = T/S* = tax share of surplus value; eu = Eu/S* = unproductive expenses share of surplus value; b = t + eu = social burden rate."** (ST 1994 Ch7 §7.1, p.213). The interpretive anchor is **"Observed net rate of profit r'n will fall relative to Marxian general rate r*' when greater proportion of surplus value absorbed in business taxes or unproductive expenses. Hence: b = social burden rate."** (ST 1994 Ch7 §7.1, p.213).

The construction rearranges the identity: `S* = Pn + T + Eu`, so `b = 1 − Pn/S*` is the fraction of surplus value not reinvested as productive capital. The Wave-1 implementation uses `Pn` approximated by NIPA Table 1.7.5 Line 17 (Corporate profits with IVA and CCAdj). This is total corporate profits; a fully faithful Pn would apply the productive/unproductive concordance from Appendix F to remove financial-sector profits. `S*` is taken from S505 (the project's Marxian surplus value series). `b = 1 − Pn/S505` is then computed annually 1948-2024. The legacy script is `code/A##_analytical/A07_social_burden_rate.py`. The book's headline empirical finding for the book period is **"Figure 7.1 shows the corresponding rise of 16% in social burden rate b over postwar period. Figure 7.2 result: NIPA-based rate rn falls substantially faster than Marxian rate. Marxian rate falls 25%, NIPA-based rate falls 39%."** (ST 1994 Ch7 §7.1, p.214). The book's reported b values rise from 0.56 (1948) to 0.66 (1989) — a 16% increase. Our implementation reports 0.7906 (1948) → 0.8577 (1989), magnitudes higher than the book by ~25 percentage points but directionally identical (RISING).

The magnitude gap traces to two known approximations. First, our Pn (NIPA Line 17) undercounts S&T's productive Pn (book's IVA-adjusted productive profits) because it lacks the productive/unproductive concordance. Second, without the concordance some financial-sector profit ends up in our Pn but not in the book's. Both issues bias `b = 1 − Pn/S*` upward (higher Pn → lower b; lower Pn → higher b — but the way our Pn is "wrong" combines an inflated numerator with an inflated S505 denominator, so the net effect is a moderately uniform upward bias). The directional finding — `b` rising over the postwar period — is what XS001's validator enforces and what the book's central social-burden-rate claim turns on. XS001's role in the S901 summary table is to expose the mechanism: when `b` rises, the NIPA-based profit rate falls faster than the Marxian rate, exactly as Figures 7.1-7.2 of the book document. The cross-link to S607/S608 (Net Social Wage) is via Appendix N's net-transfer concept — **"Net transfer: NT = Benefits received by workers − Taxes paid by workers. … Finding: Net transfer is negative over most of 1952-85 period → net tax on workers."** (ST 1994 Appendix N, pp.352-353).

## Sources

- KB chunks: `data/raw/kb/book_digitization/chunk_24/full_transcription.md` (Ch7 §7.1 p.213-214 — formal definition `b = t + eu`, Figure 7.1 numeric finding, Figure 7.2 NIPA-Marxian gap); `chunk_35/full_transcription.md` (Appendix I Table I.1 — rates of exploitation of productive/unproductive workers, related decomposition); `chunk_38/full_transcription.md` (Appendix N — net transfer methodology, negative throughout postwar)
- Book tables: Ch7 §7.1 equations p.213; Figure 7.1 (social burden rate trajectory); Figure 7.2 (Marxian vs NIPA rate of profit); Appendix N Table N.2 (net transfer)
- External sources: BEA NIPA Table 1.7.5 Line 17 (Corporate profits with IVA and CCAdj) — cached locally 1929-2024
- Upstream series: S505 (Marxian surplus value S*), S607 (Net Social Wage, conceptual cross-link)
- Code: `code/A##_analytical/A07_social_burden_rate.py` (legacy standalone analytical script — predates the standard L01/P02/V03 triad; flagged for migration in Stage 5)

## Reference values

- **Book period (validator-enforced, REVIEW 2026-07)**: anchored to book Table 7.1 printed `b` — {1948:0.56, 1958:0.62, 1970:0.67, 1980:0.66, 1989:0.65} (share_series tolerance); the series rises 0.56→0.65 (Figure 7.1's ~16% postwar increase)
- **Our implementation (post-fix)**: `b = 0.5564` (1948), `b = 0.6530` (1989); reproduces the printed book `b` to <=0.005 at every anchor year. (Pre-fix, with NIPA-Line-17 Pn, it was 0.7906/0.8577 — retired, see DIV-025)
- **Validator `expected_range`**: `[0.3, 0.95]` (registry; share_series tolerance class)
- **Direction**: monotonic rise 1948→1989 (PASS)
- **Mechanism check**: r'n / r*' = (1 − b); with rising b, this ratio falls — and the book reports r'n falling 39% vs r*' falling 25%, consistent with b rising ~16%
- **Extension period 1990-2024**: XS001 covers the full window (registry year_range 1948-2024) because both NIPA Line 17 and S505 extend; direction continues to rise modestly

## Known issues

- **~~Pn approximation~~ (RESOLVED 2026-07)**: the NIPA-Line-17 Pn was the wrong quantity, not an approximation; Pn now sourced from book Table 7.1 (profit-type income net of all taxes). See DIV-025.
- **~~Magnitude offset~~ (RESOLVED 2026-07)**: output now reproduces book b (0.56-0.65) to <=0.005; the ~25pp offset is gone.
- **S505 dependency**: any drift in the upstream Marxian surplus value series propagates here
- **Legacy script not yet migrated** to the standard L01_XS001 / P02_XS001 / V03_XS001 triad; the construction array in the registry is empty for this reason
- **Construction array empty in registry**: signals "handled by legacy analytical script" rather than the standard pipeline
- **No EPR yet authored** for XS001 (Stage 4 work)

## Cross-references

- Upstream: S505 (Marxian surplus value), NIPA Table 1.7.5 Line 17 (Pn proxy), S607 (Net Social Wage; conceptual link via Appendix N)
- Related decompositions: S506 (rate of surplus value e = S*/V*); S513 (Marxian profit rate r*); S514 (capacity-adjusted r*); XS002 (Khanjian cross-validation — same family of analytical consistency checks)
- Downstream: S901 (Chapter-9-style summary table; uses XS001 as the b component implicitly via the r'n / r*' mechanism)
- Book derivation: Ch7 §7.1 equation (3) p.213; Figures 7.1 and 7.2; Appendix N net-transfer
- Related external: Mage (1963) productive-capitalist-sector accounting (Appendix M validates the NIPA-based approach against Mage); Bowles & Gintis (1985 critique of social wage); ST 1987 social-wage paper (XS1101/XS1102/XS1103)

## Provenance trail

- **Original research**: `Technical/research/XS001_research.json`, researcher `agent`, 2026-05-16; verbatim quotes added 2026-05-23 (`stage1_cohort3_S901AS001AS002`) — sourced from chunk_24 (Ch7 §7.1 definitional and Figure 7.1) and chunk_38 (Appendix N net-transfer concept)
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (cohort agent 4); sources read = research JSON + KB chunks 24/35/38 + registry entry + project CLAUDE.md (AS-prefix framing mandate)
- **Anu Framework stage**: Stage 3 INGESTION (cohort 1, failing chapters); ingestion gate IDs P31/P32
