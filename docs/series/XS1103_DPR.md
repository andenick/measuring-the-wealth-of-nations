# XS1103 — Social Tax Rate (Shaikh & Tonak 1987)

## Series

- **SID**: XS1103
- **Name**: Social Tax Rate (ST 1987)
- **Study**: `study_02_st_1987` — Shaikh & Tonak (1987) "The Welfare State and the Myth of the Social Wage" in Cherry et al. eds., *The Imperiled Economy*, Book I, pp.184-194
- **Chapter**: ES-prefix follow-up study (registry chapter index 11; book equivalent is the 1987 ST paper, not the 1994 book)
- **Status**: book_period_validated
- **Status note**: (1952-1985 annual; Wave-2 / Stage-4 extension to 1986-2024 pending NIPA Group I/II reconstruction)
- **Units**: ratio (dimensionless)

## Methodology

XS1103 implements the comprehensive social tax rate defined in Shaikh & Tonak (1987). The construction divides total taxes paid by workers (`S604 = T_w`) by total employee compensation (`S617 = EC`), yielding a dimensionless rate. The verbatim primary anchor for the numerator is **"Taxes (from workers): = Group I (Social Security contributions from employee compensation) + Labor's share of Group II (personal taxes)"** (Shaikh & Tonak 1987, Empirical Methodology, p.187). The data source is the book's Appendix Table 1 (p.191, the 1964 illustration) and Table 2 (p.192, the full 1952-1985 annual taxes-paid-by-labor column), cross-checked against BEA *Survey of Current Business* 1981 tables at pp.121, 123, 129, 134, and 170.

The numerator `T_w` aggregates two groups. Group I (100% from workers — flows directly from employee compensation) comprises: Employer + Employee Contributions for Social Insurance, Other Labor Income (pension contributions), and the small net receipts from government-administered lotteries and parimutuels (treated as a positive net tax, sign-inverted from BEA's listing because the net receipts are consistently positive to the state). Group II (allocated by labor share = total labor income ÷ personal income) comprises: federal and state personal income taxes, motor vehicle licenses, the home-owner portion of property taxes, and miscellaneous other taxes and non-taxes. The 1964 illustration in Appendix Table 1 yields: Group I (28.66 + 0.002 = 28.662) plus Group II (36.51 + 2.60 + 0.78 + 5.99 = 45.88) = total `T_w = 74.52B` in 1964. Corporate profit taxes, indirect business taxes, and estate and gift taxes are excluded as not levied on workers. The denominator (`EC`) is computed at the cost-to-capitalists level — wages and benefits plus employer Social Security contributions plus Other Labor Income — so that the employer SS contribution appears in both numerator and denominator, correctly reflecting that it is a labor cost workers bear via reduced take-home pay. The verbatim trajectory anchor is **"Tax Rate: 1952: ~0.17 (17%) … Rises slowly and steadily throughout period … 1968: ~0.22 (22%) … 1975: ~0.24 (24%) … 1984: ~0.31 (31%) … By 1984: Reaches all-time high (41% higher than 1966)"** (Shaikh & Tonak 1987, Figure 2 description, p.188).

The transformation produces a monotonically rising rate over 1952-1985 (~17% → ~31%), driven primarily by Social Security expansion rather than income-tax policy. The Reagan-era income tax cuts were offset by continuing growth in social security contributions, so by 1985 the rate reached 41% above its 1966 level despite income-tax rate reductions — illustrating that the social-security component dominates the long-run trend. The substantive interpretive thrust the rising tax rate supports is the rebuttal of the Bowles & Gintis "rising social wage" thesis: **"Arguments such as those of Bowles and Gintis, which claim that 'there has been a substantial redistribution from capital to labor' over the postwar period, and which trace the current economic crisis back to a supposed increased social wage, appear to be quite ill-founded."** (Shaikh & Tonak 1987, p.187). Validation runs against book benchmarks in Figure 2 and Table 2 (1952 ≈ 0.17, 1966 ≈ 0.22, 1975 ≈ 0.24, 1984 ≈ 0.31) within the rate-series tolerance class; the V03 validator additionally enforces the expected range `[0.0, 0.3]`. Comparison with BLS spendable-earnings-derived series (Bowles & Gintis) is intentionally not used as validation because BLS omits state and local taxes — Bowles & Gintis's 1977 tax estimate was $10/week vs Tonak's $30.42/week, a two-thirds underestimate documented in note 5 (p.193).

## Sources

- KB chunks: `Technical/knowledge_base/external_papers/productive_labor/1987_Shaikh_Tonak_Social_Wage_Myth/full_transcription.md` (full ST 1987 paper extraction)
- Book tables: ST 1987 Appendix Table 1 (1964 illustration, p.191); ST 1987 Table 2 (taxes column, 1952-1985 annual, p.192); ST 1987 Figure 2 (tax rate trajectory, p.188); ST 1987 Figure 1 (broader social-wage decomposition)
- External sources: BEA Survey of Current Business 1981, tables at pp.121, 123, 129, 134 (tax data); BEA SCB 1981 p.170 (lotteries/parimutuels)
- Upstream series: S604 (taxes paid by workers T_w), S617 (employee compensation EC)
- Companion ES series in the same study: XS1101 (benefits to workers B_w), XS1102 (government transfers G_w), and XS1001/XS1002 (related)
- Related: Tonak (1984) PhD dissertation "A Conceptualization of State Revenues and Expenditures U.S.: 1952-1980", UMI Order #9414212 — the underlying comprehensive tax accounting framework

## Reference values

- 34 annual observations 1952-1985
- Figure 2 / Table 2 benchmark trajectory: 1952 ≈ 0.17, 1966 ≈ 0.22, 1975 ≈ 0.24, 1984 ≈ 0.31
- Absolute dollar values from Table 2: 1952=34.58B, 1964=74.52B, 1975=241.70B, 1985=705.27B
- 1984 peak is **41% higher than 1966** (the all-time high in the book period)
- Validator `expected_range`: **[0.0, 0.3]** (registry; share_series tolerance class)
- Direction: monotonically rising throughout 1952-1985 (PASS)
- 1964 illustration breakdown (Appendix Table 1): Group I = 28.662B, Group II = 45.88B, total T_w = 74.52B

## Known issues

- **Property tax coverage restricted to home-owner portion only** — renters' indirect tax burden (paid via rent) is excluded by framework design (the framework excludes tax shifting); XS1103 therefore likely understates the full property-tax burden on workers who rent
- **BLS spendable-earnings comparison will show XS1103 much higher** — BLS omits state and local taxes (Bowles & Gintis's $10/week 1977 estimate vs Tonak's $30.42/week, a two-thirds underestimate per note 5)
- **Employer social security contribution is counted in both EC (denominator) and T_w (numerator)** — this is methodologically correct per Note 8 (pp.193-194) but may appear to inflate the rate to readers unfamiliar with the cost-to-capitalists EC definition
- **Lotteries/parimutuels is a very small Group I addition** treated as net tax (sign-inverted from BEA listing — BEA lists as expenditure but net is consistently positive)
- **Extension to 1986-2024 pending** Stage-4 NIPA Group I/II reconstruction (would require building a continuous concordance from current BEA NIPA tables to the 1987 paper's tax classification)
- **No EPR yet authored** for XS1103 (Stage 4 work)
- **Inherits S604 status**: if S604 contains synthetic or estimated rows, XS1103 inherits that status — [internal-decision-record] (No Synthetic Data Policy, 2026-05-03) does not currently list XS1103 among the five series requiring remediation, but the dependency should be re-checked after any S604 revision

## Cross-references

- Upstream: S604 (taxes paid by workers), S617 (employee compensation)
- Companion ES series (same study): XS1101 (benefits B_w), XS1102 (government transfers G_w), XS1001, XS1002
- Downstream: S607 (Net Social Wage NSW = B_w + G_w − T_w; XS1103's numerator is the T_w component); S608 (NSW/V* ratio) — both used in S901 summary table
- Related external: Tonak (1984) PhD dissertation (underlying tax accounting framework); BEA Survey of Current Business 1981; Bowles & Gintis (1985) — the "rising social wage" thesis XS1103's rising tax-rate finding refutes; Miller (1986) — the tax-incidence / tax-shifting framework ST 1987 explicitly distinguishes itself from
- Related project DPRs: XS1101 (benefits side of the same NSW decomposition); XS001 (social burden rate — different decomposition of the same fiscal-burden question)

## Provenance trail

- **Original research**: `Technical/research/XS1103_research.json`, researcher `agent`, 2026-05-06; ported from `predecessor-build/research/N1103_research.json` on 2026-05-14; verbatim quotes added 2026-05-19 by `D4_es_ch10_13_backfill`
- **DPR enriched**: 2026-05-23 by Stage-3 cohort-1 ingestion agent (cohort agent 4); prior version of this DPR (pre-cohort-1) was a short stub with one methodology paragraph; this enrichment adds full 7-section structure with sources, reference values, known issues, cross-references; sources read = research JSON + ST 1987 full transcription + registry entry
- **Anu Framework stage**: Stage 3 INGESTION (cohort 1, failing chapters); ingestion gate IDs P31/P32


---

## D3 book-faithful adoption (2026-07-02)

**XS1103-A is now book Table N.2 T1/EC verbatim** (V03 5/5; was reconstruction 0/5). The excluded indirect/sales-excise tax term now lives ONLY in the **XS1103-RECON-A** / S604 comparison arm (resolves workpackage B-DIV-S604-INDIRECT on the primary).

> Decision: ADOPT NSW Candidate A (Appendix N Tables N.1/N.2 verbatim, 1952-1989) as book-period primary; BEA-API reconstruction becomes the labeled comparison/extension arm. Nothing deleted (.pre_d3 backups + -RECON subseries). See internal-review-notes_2026-07/D3_REGISTRY_PATCHES.json + D3_DIV_PATCHES.json.
