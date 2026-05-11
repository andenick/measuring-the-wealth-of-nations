# ST2 Comprehensive Review — What We Have, What We're Missing, What Comes Next

**Date**: 2026-05-08
**Author**: Claude Opus 4.6 (Session 23)
**Context**: Pipeline at 98% Druck completion, 0 UNJUSTIFIED, 0 UNKNOWN, 60 series, 17/40 KB chunks read

---

## Part I: What the Book Actually Argues

The pipeline replicates the book's DATA but not yet its ARGUMENT. Shaikh & Tonak (1994) is not just a collection of empirical series — it builds a theoretical case in three steps:

### Step 1: Marxian categories differ fundamentally from orthodox ones (Chapters 2-4)
- TP* ≈ 82% of IO gross product, but ≈ 1.5× GNP
- S* ≈ 2× the most inclusive profit measure (P+)
- S*/V* ≈ 4× P+/EC (exploitation rate vs profit/wage ratio)
- The profit/wage ratio **falls** while the rate of exploitation **rises** — "P+/EC grossly understates the level, and falsifies the trend, of S*/V*" (Section 5.4)

**Our coverage**: T201 (GFP/GDP comparison), T506 vs P+/EC comparison in figures. Adequate.

### Step 2: The rate of exploitation rose, driving rising surplus value (Chapter 5)
- e = S*/V*: 1.70 (1948) → 2.44 (1989), +43%
- Driven by declining Lp/L (0.57 → 0.36) not by wage differentials (ec_p/ec_u stable)
- The net social wage is negative — workers pay more in taxes than they receive in benefits (Chapter 5 Section 5.9)
- Price-value deviations are small (6-9%), validating the money-form approximation

**Our coverage**: T501-T516 (complete), T601-T609 (complete), N-series (8 external studies). Strong.

### Step 3: Rising unproductive activity causes the rate of profit to fall (Chapter 7) — THE CENTRAL ARGUMENT

This is where the book's analytical contribution lives. The key decomposition:

```
r'_n = (1 - b) × r*'

where:
  r*' = S* / (K* × u)           = Marxian general profit rate (capacity-adjusted)
  r'_n = P_n / (K* × u)         = NIPA-based net profit rate
  b = (T + E_u) / S*            = social burden rate
  T = business taxes
  E_u = expenses of unproductive sectors (trade wages + materials)
```

And the accumulation equation:

```
g_K = s' × u × r*'

where:
  s' = 1 - c'                   = social savings rate
  c' = (CON_C + G + E_u) / S*  = social consumption rate
```

The book's central empirical finding: **b rises 16% over the postwar period, causing r'_n to fall 39% while r*' falls only 25%.** The accumulation rate g_K tracks r*' (not r'_n) because s' is stable.

**Our coverage**: WE DO NOT COMPUTE b, c', s', g_K, r*', OR r'_n AS SEPARATE SERIES. These are the book's most important analytical results. Table 7.1 has all of these annually for 1948-1989.

---

## Part II: Series Gap Analysis

### Series We Have (59 total, well-covered)

| Block | Series | Coverage | Faithfulness |
|-------|--------|----------|-------------|
| Revenue (Ch 5) | T501-T503 | Book + extended | Good (IO overlay 1997+) |
| Exploitation (Ch 5) | T504-T506 | Book (H.1) + extended | Good (V* from components) |
| Composition (Ch 5) | T507-T510 | Book only (most) | T510 needs extension |
| Employment (Ch 5) | T511-T516 | Book + IO-extended | Good (PAYEMS + IO ratio) |
| Profit rate (Ch 5) | T513-T514 | Book + K*-extended | Good (S*/K* from components) |
| NSW (Ch 6) | T601-T609 | Book + 3-group extended | Good (Appendix N methodology) |
| IO (Ch 4) | T401-T402, T701-T703 | SIC benchmarks + NAICS | Good (A06 Ochoa regression) |
| Cross-study (Ch 8) | T801 | Book period | Basic comparison table |
| Alt GFP (Ch 2) | T201 | Book + GDP extended | Unit-fixed |
| Summary (Ch 9) | T901 | Book period | Assembled from others |
| External studies | N1001-N1704 | 26 series, 8 papers | Mixed (some real data, some limited coverage) |

### Series We're MISSING (from book's tables, not yet in pipeline)

| Table | Series | Content | Importance |
|-------|--------|---------|-----------|
| **Table 7.1** | b, c', s', g_K, r*', r'_n | Social burden rate + accumulation dynamics (42 years) | **CRITICAL** — the book's central argument |
| **Table K.1** | G*_t/SP* | Government absorption of surplus value (42 years) | HIGH — unique measure |
| **Table I.1** | e_u, e_u/e_p | Exploitation rate of unproductive workers (42 years) | HIGH — 25-step calculation |
| **Table J.1** | q*, y*, y, y₂ | Marxian vs orthodox productivity (42 years) | HIGH — productivity slowdown analysis |
| **Table L.1** | v*', v", w' | Aglietta's exploitation index (42 years) | MEDIUM — cross-validation |
| **Table 5.8** | r*, r, r_corp, C*/V*, C*/(V*+S*) | Profit rates and compositions (42 years, capacity-adjusted) | HIGH — detailed profit analysis |
| **Table 5.10** | q*, y*, y, y₂ | Productivity measures (same as J.1, main text version) | Same as J.1 |
| **Table 5.11** | G*_E, G*_E/SP* | Government absorption (same as K.1, main text version) | Same as K.1 |

### What This Means

We've replicated the book's DATA (the building blocks) but not its ANALYSIS (the decompositions and relationships that constitute the actual argument). The missing Table 7.1 series are the analytical heart of the book.

---

## Part III: Methodological Investigations We Ought To Do

### Investigation A: The Social Burden Rate Decomposition

**What**: Compute b = (T + E_u) / S* annually for 1948-2024.

**Why**: This is THE mechanism that connects Marxian surplus value to observable profit rates. The book shows b rose from 0.56 to 0.66 (1948-1989). What happened after 1989? Did neoliberalism reverse the trend? Did financialization change the composition of unproductive expenses?

**Data needed**: We have S*, T (from T601-T604), but need E_u (expenses of unproductive sectors = trade sector wages + materials). This requires the IO decomposition of trade sector costs.

**Expected finding**: b likely continued rising through 2000s (financialization expanded FIRE), then may have shifted post-2008.

### Investigation B: The Accumulation Equation

**What**: Compute g_K = In/K*, s' = In/SP*, and verify g_K = s' × u × r*'.

**Why**: The book's empirical finding that g_K tracks r*' (because s' is stable) is a powerful test of classical/Marxian accumulation theory. Does this still hold post-1989?

**Data needed**: In (net investment) from BEA NIPA, K* (productive capital stock, partially available), u (capacity utilization, from FRED TCU).

### Investigation C: Productivity Slowdown Decomposition

**What**: Compute q* (Marxian: TP*/Hp) and y (orthodox: GDP/H) and compare their trends, especially post-1972.

**Why**: The book shows q* grows 2-3× faster than y over the postwar period. The "productivity slowdown" is an artifact of using GDP per worker-hour instead of total product per productive worker-hour. Does this extend to 2024?

**Data needed**: TP* (have), Hp (productive worker hours — need from BLS), GDP (have), total hours H (need from BLS/NIPA).

### Investigation D: SIC-Era Price-Value Regression

**What**: Run the Ochoa regression (log market prices on log labor values) on our existing 1958 SIC IO data.

**Why**: The book claims R² ≈ 0.98 for 1958. Our NAICS-era results show R² = 0.44-0.60. We need to verify the 1958 result to confirm whether the decline is genuine structural change or a specification error in our SIC data handling.

**Data needed**: Already available (L11 loads SIC IO matrices, L12 computes hp* vectors). Just need to run the regression on the SIC data.

### Investigation E: Khanjian Cross-Validation

**What**: Compare our S*/V* with Khanjian's (1989) labor-value-based estimates (Table 5.12).

**Why**: The book shows S*/V* (money rate) is 6-9% lower than S/V (labor value rate), and the two track closely. Our pipeline computes S*/V* (money rate). Cross-checking against Khanjian's numbers validates our methodology.

**Data available**: Table 5.12 (chunk 17) has Khanjian's estimates for 1958, 1963, 1967, 1972, 1977. Compare with our T506 at those years.

### Investigation F: Sensitivity Analysis on Key Assumptions

**What**: Test how results change under different assumptions:
1. VA*/W = constant 1.238 vs year-varying (how much does exploitation rate change?)
2. BLS CES production workers vs IO-classified Lp (how much does employment share change?)
3. 40% defense exclusion vs 3-group NSW methodology (how much does NSW change?)
4. Total K vs productive K* (how much does profit rate change?)

**Why**: Every extension involves assumptions documented in DEC-001 through DEC-020. A sensitivity analysis shows which assumptions matter most and which are robust.

### Investigation G: Structural Break Tests

**What**: Test for structural breaks in key series around:
- 1973 (oil shock)
- 1980 (Reagan/Volcker)
- 1996 (welfare reform)
- 2001 (dot-com)
- 2008 (GFC)
- 2020 (COVID)

**Why**: The book identifies two phases (1948-1980 falling profit rate, 1980-1989 partial recovery). Our extension covers 1990-2024 — three more potential phases. Formal break tests would identify structural shifts.

---

## Part IV: What Would Make This Publication-Quality

### Tier 1: Essential for a Working Paper

1. **Compute Table 7.1 series** (b, c', s', g_K, r*', r'_n) for 1948-2024
2. **Compute Table K.1** (government absorption ratio G*_t/SP*)
3. **LaTeX methodology paper** with every formula, book page reference, and KB verification
4. **Reproduce the SIC 1958 regression** (Investigation D)
5. **Khanjian cross-validation** (Investigation E)

### Tier 2: For a Journal Submission

6. **Compute Table I.1** (unproductive worker exploitation rate e_u)
7. **Compute Table J.1** (Marxian vs orthodox productivity q*, y*, y)
8. **Sensitivity analysis** (Investigation F)
9. **Structural break tests** (Investigation G)
10. **Social burden rate decomposition** extended to 2024 (Investigation A)
11. **Accumulation equation** verification post-1989 (Investigation B)

### Tier 3: For a Book-Length Treatment

12. **Full IO framework for all SIC+NAICS years** with proper bridge
13. **International comparisons** updated (Turkey, NZ, Greece data extended)
14. **Productivity slowdown** decomposition extended (Investigation C)
15. **Aglietta index** reproduction and comparison
16. **Real wage / real productivity** comparison as alternative exploitation indicator

---

## Part V: Cross-Check Against What We Know From Tonak

### What the Book's Data Tells Us (from KB)

| Year | S*/V* (H.1) | V* ($B) | S* ($B) | P+/EC | b (7.1) | r*' | Comment |
|------|------------|---------|---------|-------|---------|-----|---------|
| 1948 | 1.70 | 88.41 | 149.94 | 0.70 | ~0.56 | ~0.52 | Postwar peak profit rate |
| 1958 | 2.01 | 127.72 | 256.15 | 0.59 | — | — | Our old benchmark was WRONG (1.83) |
| 1967 | 2.10 | 216.26 | 454.40 | 0.58 | — | — | Vietnam War |
| 1972 | 1.99 | 324.30 | 645.98 | 0.52 | — | — | Note: e FELL from 1967 |
| 1980 | 2.07 | 706.53 | 1462.70 | 0.48 | ~0.66 | ~0.40 | Profit rate trough |
| 1989 | 2.44 | 1206.40 | 2943.35 | 0.51 | ~0.66 | ~0.44 | Reagan recovery |

### Critical Observations

1. **The exploitation rate is NOT monotonically rising.** S*/V* dips from 2.10 (1967) to 1.99 (1972) — a significant 5% decline during the late 1960s. This is obscured by our old linearly interpolated data (which showed a constant 2.10 for all of 1967-1977). The Table H.1 data reveals real year-to-year dynamics.

2. **The 1958 correction matters.** Our old benchmark (1.83) implied exploitation rose steadily from 1948 to 1958. The actual value (2.01) shows exploitation rose MUCH faster in the 1950s (from 1.70 to 2.01 in 10 years = +18%) then slowed in the 1960s. This changes the narrative about the postwar exploitation trajectory.

3. **P+/EC (orthodox) trends OPPOSITE to S*/V* (Marxian).** The orthodox profit/wage ratio FALLS from 0.70 to 0.51 while the Marxian exploitation rate RISES from 1.70 to 2.44. This is the book's key empirical finding — and it's driven entirely by the growing share of unproductive employment absorbing surplus value.

4. **The social burden rate b ≈ 0.56-0.66** means 56-66% of surplus value goes to taxes + unproductive expenses (not to capitalist profit). This is why Marxian surplus value (S*) is roughly 2× orthodox profit (P+).

---

## Part VI: Do We Have Everything?

### Data: YES, mostly
- Book-period data: Digitized Table H.1 (42 years, 14 columns) ✓
- Extension data: BEA NIPA, FRED, BLS CES ✓
- IO framework: SIC (6 benchmarks) + NAICS (5 benchmarks) ✓
- Employment: PAYEMS + sector data ✓

### Methodology: MOSTLY
- V* computation: Sector-by-sector infrastructure built, needs refinement ✓
- NSW: 3-group Appendix N methodology ✓
- Employment: IO productive ratio for extension ✓
- Profit rate: S*/K* from components ✓
- **MISSING**: Social burden rate decomposition (b, c', s')
- **MISSING**: Productivity measures (q*, y*)
- **MISSING**: Exploitation rate of unproductive workers (e_u)

### Analysis: NO — this is the biggest gap
- **The Chapter 7 analytical series are not computed**
- No social burden rate trend
- No accumulation equation verification
- No productivity decomposition
- No structural break analysis
- No Khanjian cross-validation

### Documentation: PARTIAL
- KB deep dive findings: Comprehensive (600+ lines) ✓
- Decision log: 20 entries ✓
- Methodology review: All verdicts finalized ✓
- **MISSING**: LaTeX paper with formulas + KB page references
- **MISSING**: Formal data provenance for every series extension

---

## Part VII: Recommended Next Phase

### Phase 4: "The Argument" (5-8 sessions)

Build the analytical series that constitute the book's central contribution:

1. **Table 7.1 series**: b, c', s', g_K, r*', r'_n (Investigations A + B)
2. **Table K.1 series**: G*_t/SP* government absorption
3. **Table I.1 series**: e_u, e_u/e_p unproductive worker exploitation
4. **Table J.1 series**: q*, y*, y productivity measures
5. **SIC-era regression**: Reproduce R² ≈ 0.98 for 1958
6. **Khanjian cross-validation**: Table 5.12 comparison
7. **LaTeX paper**: Complete methodology documentation

This would transform the project from "data replication" to "analytical replication" — not just reproducing the numbers but reproducing the ARGUMENT that those numbers support.

---

*Review authored 2026-05-08 (Session 23). Based on 17/40 KB chunks, 20 decision log entries, 60 pipeline series, and Chapter 7 analytical framework from chunk 24.*
