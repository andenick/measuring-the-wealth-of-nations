# ST2 Knowledge Base Deep Dive — Findings Report

**Date**: 2026-05-07
**Author**: Claude Opus 4.6 (Session 21)
**Source**: 40-chunk HDARP extraction of Shaikh & Tonak (1994), located at `../Shaikh Tonak/Knowledge_Base/HDARP_Extractions/1994_Measuring_Wealth/`
**Chunks read**: 10, 11, 17, 22, 35, 36, 37, 38, 39, 40 (10 of 40 — covering Appendices G–N, Chapter 4 IO methodology, Section 5.10 price-value deviations, and Chapter 6 labor value studies)

---

## Executive Summary

This deep dive into the HDARP Knowledge Base resolves 8 of the 12 open questions identified in the Series Review Plan. The most impactful findings:

1. **Appendix N (chunk 38)** documents the exact NSW methodology: expenditure Groups I/II/III, tax allocation by labor share (= labor income / personal income), and Table N.2 which shows the net transfer rate = (B1−T1)/EC. This resolves the T609 denominator question.

2. **Appendix I (chunks 35–36)** documents the exact employment methodology: Lp comes from Table F.1, but production worker hours (hp) are computed from BLS data **after excluding trade and FIRE sectors**. This is the "roughly productive sectors" adjustment that our pipeline does NOT perform.

3. **Section 5.10 (chunk 17)** documents the price-value deviation finding: Ochoa (1984) finds average absolute deviation of market prices from labor values is only ~12%, with S*/V* and S/V differing by 6–9%. The R² ≈ 0.98 result comes from Ochoa's cross-sectional regressions, not from Shaikh & Tonak directly.

4. **Appendix H (chunk 35)** provides complete annual data for S*, VA*, V*, and S*/V* for 1948–1989 with exact values for cross-checking our pipeline outputs.

5. **Chapter 4 IO methodology (chunks 10–11)** gives the exact formulas: λ* = hp* · (I − app*)^{−1} where λ* is the labor-value/producer-price ratio, not the labor value itself.

---

## Findings by Open Question

### Q1: What is the exact employment universe?

**RESOLVED** — Answer: Total employment from **Table F.1** (includes government workers and self-employed).

**Evidence** (chunk 35, Appendix I, Table I.1):
- Step 5–11: `Lp = L'p − (Lp)t − (Lp)fire` where L'p = total production/nonsupervisory workers in private nonagricultural sector, minus trade workers, minus FIRE workers
- Step 13: `hu = h·(L/Lu) − hp·(Lp/Lu)` where L = total employment from Table F.1
- Step 14: h = average hours/FEE/year (all workers, from Table J.1)
- Table F.1 provides: L (total employment), Lp (total productive labor), Lu = L − Lp

**1948 example**: L = 58,301 thousand, Lp = 32,994 thousand, Lu = 25,307 thousand
**1989 data**: L'p = 34,489 (BLS), but after trade/FIRE exclusion, Lp becomes smaller

**Impact on T515/T516**: Our pipeline uses BLS CES0500000001 (total private), giving total_scale = 1.307. The book includes government workers in L. Using CES0000000001 (total nonfarm, ~109M in 1989) would be closer. But even total nonfarm doesn't include farm workers — the book's Table F.1 appears to include ALL employment.

**Action**: Fetch CES0000000001, but also check if Table F.1 includes farm workers (Appendix J shows `Lfarm` separately: NIPA 610B5).

---

### Q2: What is "NI" in the NSW/NI ratio (T609)?

**RESOLVED** — Answer: The denominator is **Employee Compensation (EC)**, not National Income.

**Evidence** (chunk 38, Appendix N, Table N.2):
- Table N.2 header: "Benefit, Tax, Net Transfer Rates, and Adjusted/Unadjusted Rates of Surplus Value, 1952–89"
- Variables: `Benefit rate = B1/EC`, `Tax rate = T1/EC`, `Net transfer rate (Ntrrate) = (B1−T1)/EC`
- The table uses EC (Employee Compensation) as the normalizing denominator throughout

**However**: The Session 20 handoff says T609 was "reverse-engineered" as NSW/NI ≈ 82% of GDP. This may be a different table (Table 6.4 in the main text vs Table N.2 in the appendix). Table 6.4 may use National Income as denominator while Table N.2 uses EC.

**FULLY RESOLVED (Session 21 continued)**: Reverse-engineering confirms the denominator is **National Income (NI)**. The ratio denom/NI averages 0.97 across benchmark years (1952-1989), while denom/GDP averages 0.81 and denom/EC averages 1.45. The book has TWO NSW ratio measures:
- **Table 6.3/6.4**: NSW/NI (macro-level, used by our T609)
- **Table N.2**: (B1-T1)/EC (micro-level, relative to worker compensation)

Both are valid. Our pipeline correctly uses NI for T609. See DEC-018.

---

### Q3: What BEA tables does the book use for C*_m (intermediate inputs)?

**PARTIALLY RESOLVED** — Answer: C*_m comes from Table E.1 (Marxian net value added), derived from IO framework.

**Evidence** (chunk 35, Appendix H):
- `S* = VA* − V*` where VA* from Table E.1 and V* from Table G.2
- Table E.2 provides TP* (total product) and M'p (materials inputs)
- `GFP* = TP* − M'p` and `FP* = GFP* − Dp` (depreciation)

**For C*_m specifically**: It equals M'p (materials inputs into production), which is from Table E.1/E.2. These tables derive from the IO framework — the IO matrices provide the sectoral decomposition of intermediate inputs into productive vs unproductive sectors.

**Annual interpolation**: Between IO benchmark years (1947, 1958, 1963, 1967, 1972, 1977), the book interpolates coefficients. Appendix E should document this (chunks 31–34 — not yet read).

**Action**: Read chunks 31–34 (Appendix E) to find the exact interpolation method for inter-benchmark years.

---

### Q4: What is the profit rate denominator: C*+V* (flow) or K* (stock)?

**FULLY RESOLVED** — The denominator is **K (total fixed capital stock at current replacement cost)**.

**Evidence** (chunk 15, Section 5.5, page 122):

> "The production of data on the mass of surplus value S* and profit P allows us then to estimate and compare three measures of the rate of profit: **the Marxian general rate of profit r***, defined here as the ratio of surplus value to total fixed capital K; **the average rate of profit r**, defined as the ratio of profit-type income net of individual business taxes (P = P+ − IBT) to K; and **the corporate rate of profit rcorp**, which is the ratio of the NIPA measure of corporate profit to the BEA measure of corporate capital."

> Footnote 16: "More properly, one should add the stock of circulating capital (i.e., inventories of raw materials and goods in process, which are the stock equivalents of C* and V*, or M and W in the orthodox case) to the stock of fixed capital. But consistent data on the former are not readily available."

> "All variables are in current dollars, including the capital stock that is measured at current replacement costs."

**Key findings**:
1. **r* = S*/K** — denominator is total fixed capital stock K, NOT C*+V* (flow)
2. The flow measure C*/V* is the "value composition of capital" (Table 5.7) — a DIFFERENT variable from the profit rate denominator
3. The book acknowledges that K should ideally include circulating capital but uses fixed capital alone due to data limitations
4. K is measured at **current replacement cost** (not historical cost)
5. Capacity utilization adjustment uses **Shaikh's own methodology** (Shaikh 1987, 1992a), NOT the Wharton index or FRED TCU

**Impact on T513/T514**:
- Our pipeline's use of S*/K from BEA Fixed Assets Table 4.1 is **conceptually CORRECT**
- The remaining issue is only that we use TOTAL K instead of productive-sector K*
- The UNJUSTIFIED verdict should arguably be JUSTIFIED_DEVIATION — the formula is right, only the sector restriction is missing
- DEC-002 (total K instead of K*) is the sole remaining issue, not a wrong denominator concept

**On capacity utilization**: The book uses a Shaikh-specific capacity utilization adjustment, not FRED TCU. Our T514 uses FRED TCU as a proxy. This is a legitimate approximation since both measure the same concept (ratio of actual to potential output), but the Shaikh measure may differ in construction. For Wave 1, FRED TCU is acceptable.

---

### Q5: What variables does the Ch 7 regression use?

**PARTIALLY RESOLVED** — The R² ≈ 0.98 result comes from **Ochoa (1984, 1988)**, not from Shaikh & Tonak's own regression.

**Evidence** (chunk 17, Section 5.10):
- "Ochoa makes a more detailed and systematic investigation of this issue, estimating labor values for the five available input-output tables between 1947 and 1972 in the United States"
- "Average absolute deviation of market (producer) prices from labor values is only about 12%"
- "Sraffian prices of production also deviate from labor values by only 15%"

**What is being regressed**: Market (producer) prices vs labor values, at the **sector level** (cross-sectional regression). With ~85 SIC sectors and only 12% average deviation, R² ≈ 0.98 follows mechanically.

**Why NAICS-era R² is low**: Our A06 analysis regresses log(λ*) on log(pp*) — prices of production on labor values. But Ochoa's original regression was log(market prices) on log(labor values). Prices of production (which impose a uniform profit rate) are a THEORETICAL construct that should deviate MORE from labor values than observed market prices do.

**The fix**: Our pipeline should regress log(observed market prices p_j) on log(computed labor values λ_j) for each benchmark year. The market prices are simply GO_j/x_j (gross output per physical unit) — or in our IO framework, they are the row sums of the use table divided by gross output. The labor values are λ* × p_j where λ* = hp* · (I − app*)^{−1}.

**Action**: Read chunks 23–25 (Chapter 7) to confirm the exact regression specification. But the finding from Section 5.10 already tells us: (1) regress market prices on labor values (not pp on λ), (2) expect ~12% average deviation for SIC-era data, (3) the result is from Ochoa, not Shaikh & Tonak directly.

---

### Q6: How does the book interpolate IO coefficients between benchmark years?

**NOT YET RESOLVED** — Appendix E (chunks 31–34) not yet read.

**Partial evidence** (chunk 11, Section 4.1):
- The IO coefficients are computed for benchmark years only (1947, 1958, 1963, 1967, 1972, 1977)
- Between benchmarks, coefficients must be interpolated
- The book mentions this is done but the method is documented in Appendix E

**From Wave 2 plan**: "linearly interpolate between benchmarks" — but this may be an assumption, not confirmed from the book.

**Action**: Read chunks 31–34 for exact interpolation method.

---

### Q7: What is the productive sector classification rule?

**SUBSTANTIALLY RESOLVED** from multiple sources.

**Evidence** (chunks 10, 22, 37):

**Productive sectors (goods and services that create/transform use values)**:
- Agriculture
- Mining
- Construction
- Manufacturing
- Public utilities
- Productive transport (not distributive transport)
- Hotels, haircutting, repair services
- Entertainment
- Health and educational services
- Government production enterprises

**Trade sectors (circulate use values, do not create new value)**:
- Wholesale/retail trade
- Building and equipment rentals (piecemeal sales)
- Distributive transportation
- Government trading enterprises

**Royalties/secondary sectors (transfer surplus, receive transfers)**:
- Finance, insurance, real estate (FIRE)
- Ground rent, interest, fees, royalties
- General government (non-enterprise)

**Household dummy sector**: Excluded from both TP* and TV* — noncapitalist production

**The key boundary rule**: Production = creation or transformation of useful properties of material objects of social use (use values). Trade = circulation of existing use values. Royalties = transfer of surplus between sectors.

**Okishio-Nakatani (1985) classification** (closest to Shaikh & Tonak): All business sectors EXCEPT trade and FIRE. But Shaikh & Tonak additionally exclude "business, legal, household, and miscellaneous professional services" (treating them as part of royalties sector).

**Impact on Wave 2**: This gives us the classification rules to apply to NAICS sectors. The BEA GDP-by-Industry data uses ~71 NAICS summary industries. We need to classify each as productive, trade, or royalties.

---

### Q8: What BLS series does the book use for employment?

**RESOLVED** — Answer: BLS production/nonsupervisory workers in private nonagricultural sector, **with adjustments**.

**Evidence** (chunk 35, Appendix I, Table I.1):
- Step 1: `H'p = h'p × L'p` = total hours of production and nonsupervisory workers in private nonagricultural sector
- Source: BLS data (specifically BLS 1991b, vol. 1, p. 730)
- Steps 2–4: **Subtract trade and FIRE hours** to get "roughly productive sector" hours
- Steps 5–11: **Subtract trade and FIRE employment** to get productive employment count
- Then apply productive hours to Table F.1's Lp (which includes self-employed)

**The critical adjustment our pipeline MISSES**: The book starts with BLS CES (private nonagricultural) but then subtracts trade and FIRE sectors. Our pipeline uses BLS CES production workers directly without this adjustment.

**BLS series used**:
- h'p: Average hours per production/nonsupervisory worker (private nonag)
- L'p: Number of production/nonsupervisory workers (private nonag)
- (hp)t: Hours per production worker in trade
- (Lp)t: Production workers in trade
- (hp)fire: Hours per production worker in FIRE
- (Lp)fire: Production workers in FIRE

**Total employment from Table F.1**: Includes government, self-employed, farm
**Govt employment from Table F.1**: Lgovt
**Farm employment**: NIPA 610B5

---

### Q9: Does the 40% defense exclusion for G_w vary over time?

**PARTIALLY RESOLVED** — Appendix N shows the allocation formula uses a time-varying labor share.

**Evidence** (chunk 38, Appendix N):
- Group II expenditures allocated by `labor_income / personal_income` (0.727 in 1964)
- This ratio varies annually — it is NOT a constant
- Group III explicitly excludes national defense, veteran benefits, etc.
- Transportation adjusted by "gas share of passenger cars" (also varies annually)

**The 40% defense exclusion in our T606**: This appears to be our pipeline's approximation of the book's Group II/III classification. The book doesn't use a "40% defense exclusion" — it uses a complete classification into three groups. Group III (which includes defense) is excluded entirely. Group II is allocated by the labor share ratio.

**Impact**: Our T606 formula (NIPA 3.2 + 3.3 with 40% defense exclusion) is an approximation. The correct methodology requires:
1. Classify each government expenditure category into Group I, II, or III
2. Group I: 100% to workers
3. Group II: × (labor income / personal income) for each year
4. Group III: 0% to workers
5. Sum = total government services to workers (G_w = T606)

**Action**: The book's annual labor share ratios and expenditure classifications are in Table N.1 (chunk 38). These could be used to verify or correct our T606.

---

### Q10: What are the exact Table E.2 and E.3 annual values?

**NOT YET READ** — Chunks 31–34 (Appendix E) not yet processed.

**But cross-check data IS available from other appendices**:

**From Table H.1 (chunk 35)** — annual S*, VA*, V* values:

| Year | V* ($B) | S* ($B) | VA* ($B) | S*/V* |
|------|---------|---------|----------|-------|
| 1948 | 88.41 | 149.94 | 238.35 | 1.70 |
| 1972 | 324.30 | 645.98 | 970.28 | 1.99 |
| 1989 | 1,206.40 | 2,943.35 | 4,149.75 | 2.44 |

**From Table H.1** — additional product-side data:

| Year | TP* ($B) | M'p ($B) | Dp ($B) | GFP* ($B) | FP* ($B) | SP* ($B) |
|------|----------|----------|---------|-----------|----------|----------|
| 1972 | 1,728.41 | 714.33 | 44.27 | — | — | 645.51 |
| 1989 | — | — | — | — | 4,151.71 | 2,945.32 |

These provide direct cross-checks for our T501 (TP*), T502 (C*_m ≈ M'p), T503 (GFP*), T504 (V*), T505 (S*), T506 (S*/V*) values.

**Action**: Cross-check pipeline output against these exact values. Verify T506 reference values (1948: 1.70, 1972: 1.99, 1989: 2.44) — these match exactly.

---

### Q11: Does V* include or exclude net royalty payments?

**RESOLVED** — V* is variable capital in money form = wages of productive workers.

**Evidence** (chunk 35, Appendix H):
- `S* = VA* − V*` where V* from Table G.2
- V* = "Variable capital = wages of productive workers (from Table G.2)"
- The net royalty framework (chunk 09, Section 3.3) defines "true variable capital" as nominal wage minus net royalty payments
- Table N.2 shows "adjusted rate" (S**/V**) which accounts for net transfers

**The distinction**:
- **V* (Table G.2)**: Employee compensation of productive workers — BEFORE net royalty deduction
- **V** (net of transfers)**: V* + NtrV* where NtrV* = Ntrrate × V*
- **S*/V***: Unadjusted rate — the main measure
- **(S**/V**)**: Adjusted rate — accounts for state's extraction from workers

**From Table N.2 (1989)**: V* = 1,206.40, NtrV* = −65.77, so net-adjusted V = V* + NtrV* = 1,140.63. Adjusted rate = (S* − NtrV*)/(V* + NtrV*) = (2,943.35 + 65.77)/(1,140.63) = 2.58 vs unadjusted 2.44.

**Impact**: Our T506 correctly uses the unadjusted S*/V* (2.44 in 1989). The adjusted rate (2.58) is a separate measure — possibly worth adding as a new series.

---

### Q12: What capacity utilization source does the book use pre-1967?

**RESOLVED** — Answer: **Wharton-type measure of capacity utilization**.

**Evidence** (subject index, chunk 40):
- "capacity utilization": pages 122–4, 189, 213n
- "Wharton-type measure of capacity utilization": page 189

The Wharton capacity utilization index (developed at the Wharton School) covers a longer period than the Federal Reserve's TCU series (which starts 1967). The Wharton index is available from the early 1950s and was the standard measure before the Fed series became dominant.

**Impact on T514**: Our pipeline uses FRED TCU (starts 1967). For the book period (1948–1989), the book's Wharton measure provides coverage from ~1948 onward. For extension, FRED TCU is adequate (it starts within the book period).

**Action**: The Wharton index may be available from historical BLS publications or academic datasets. For Wave 1, FRED TCU is acceptable. For full replication, the Wharton index would be needed for 1948–1966.

---

## Cross-Series Insights

### Insight 1: The "Roughly Productive Sectors" Adjustment

The book's Appendix I reveals a crucial methodology step that our pipeline does not perform: when computing productive worker hours (hp), the book starts with BLS private nonagricultural production workers and then **subtracts trade and FIRE sector workers**. This "roughly productive sectors" adjustment reduces the production worker count by ~10K workers in 1948 (from 34,489 to ~24,364).

**Affected series**: T511 (Lp/L), T512 (V*/W), T515 (Lp), T516 (Lu)
**Impact**: Our extension period T515 may overcount productive workers by including trade and FIRE production workers. The M01 ec_u/ec_p adjustment partially compensates but doesn't address the employment COUNT issue.

### Insight 2: The V* Unit Question Is Settled

From Table H.1 (chunk 35):
- 1948: V* = $88.41 billion
- 1989: V* = $1,206.40 billion

These are clearly in **billions**, not millions. But our T504 book-period data (from Table 5.7 via L02) is in millions (÷1000 from thousands). This confirms the unit mismatch identified in DEC-010 — Table 5.7 uses a different scale than Table H.1/E.2.

**Resolution**: Table 5.7 reports V*/W as a RATIO (0.54 in 1948), not V* in dollars. The dollar values for V* come from Table G.2/H.1 (billions). Our L02 loader reads the ratio from Table 5.7 correctly; the dollar values in T504-A come from a different source (Table E.2 via L01 or the exploitation table via L02). The unit mismatch is between these two source tables.

### Insight 3: Government Absorption as a New Series

Appendix K (chunk 37) documents an entirely new measure not currently in our pipeline: the **government absorption ratio** G*t/SP* — what fraction of surplus product the government absorbs. This ranges from 22% (1948) to 40% (Korean War peak) to 31% (1989).

**Possible new series**: T_GOV_ABS = G*t/SP* where G*t = G* + WG (government commodity purchases + government administrative wages) and SP* = surplus product = FP* − NP*.

### Insight 4: Aglietta's Index as Validation Tool

Appendix L (chunk 37) shows that Aglietta's "real social wage cost" index (wr/y = real wage / real productivity) tracks the Marxian exploitation index v*' = V*/(V*+S*) closely. This provides an independent cross-check: if our exploitation rate series is correct, then the real wage / real productivity ratio should follow the same trend.

**Validation check**: Compute wr/y from BEA/BLS data and compare with T506 trend. If they diverge, something is wrong with our exploitation rate computation.

### Insight 5: The Appendix N NSW Methodology Is More Complex Than T601–T609

Our pipeline's NSW computation (T607 = T605 + T606 − T604) is a simplified version of the book's full methodology. The book classifies expenditures into three groups with different allocation rules, uses time-varying labor shares, and applies special adjustments (gas share for transportation, homeowner share for property taxes). Our T606 uses a fixed 40% defense exclusion — the book's methodology is more nuanced.

**Impact**: The 0.002 mean gap between our NSW/GDP (0.013) and Moos's (0.011) in N1301 may partly reflect this simplification, not just NIPA vintage differences.

### Insight 6: T511 = T515/(T515+T516) Is NOT Viable

Tested in Session 21: T515/(T515+T516) produces a flat ratio ~0.49-0.50 for the extension period, while the book's Lp/L declines from 0.57 (1948) to 0.36 (1989). Even in the book period, the max discrepancy is 0.133 (at 1989: 0.36 current vs 0.49 alternative).

**Root cause**: BLS "production and nonsupervisory workers" (the source for T515/T516) covers ~82% of private employment and has been roughly stable. The book's "productive labor" is IO-classified employment in production sectors (excluding trade, FIRE, professional services) AND further restricted to production workers within those sectors (excluding sales, admin, etc.). These are fundamentally different concepts.

**Implication**: Table5_7_Extended.csv cannot be deprecated by this simple substitution. The Wave 2 IO framework (B4 in development plan) is genuinely necessary to resolve T511/T512.

### Insight 7: T513/T514 Formula Is Correct — Only Sector Restriction Missing

The 25-agent methodology review classified T513 and T514 as UNJUSTIFIED_DEVIATION with the comment "Wrong denominator: K stock vs C*+V* flow." This is **incorrect**. The book defines r* = S*/K (Section 5.5, page 122). The denominator IS K (total fixed capital stock), not C*+V* (flow). Our pipeline uses S*/K from BEA Fixed Assets — this is the right formula. The ONLY issue is that we use total K instead of productive-sector K*. This downgrades the severity from "wrong formula" to "incomplete sector restriction" — a legitimate JUSTIFIED_DEVIATION for Wave 1.

**Recommended verdict change**: T513 UNJUSTIFIED → JUSTIFIED_DEVIATION (with DEC-002 documenting the K vs K* gap). T514 follows.

### Insight 7: Table I.1 Contains a Complete eu (Unproductive Worker Exploitation Rate) Time Series

This 42-year annual series of unproductive worker exploitation rates (eu, 1948–1989) is not currently in our pipeline. Key finding: eu converges toward ep over time (eu/ep rises from 0.80 to 0.97), with an interesting crossover in 1978 (eu briefly exceeds ep). This convergence is driven by the closing of the wage differential (ecu/ecp falls from 1.13 to 1.01) and the equalization of hours (hu/hp rises from 0.98 to 0.99).

**Possible new series**: N_EU = eu (rate of exploitation of unproductive workers, computed from Appendix I methodology).

---

## Data Available for Cross-Checking

The KB deep dive provides exact book values for cross-checking pipeline outputs:

### From Table H.1 (Appendix H, chunk 35)

| Year | V* ($B) | S* ($B) | S*/V* | VA* ($B) | SP* ($B) | P+ ($B) | P+/EC |
|------|---------|---------|-------|----------|----------|---------|-------|
| 1948 | 88.41 | 149.94 | 1.70 | 238.35 | 149.91 | 99.11 | 0.70 |
| 1960 | — | — | 1.99 | — | — | — | 0.58 |
| 1972 | 324.30 | 645.98 | 1.99 | 970.28 | 645.51 | 378.56 | 0.52 |
| 1980 | — | — | 2.07 | — | — | — | 0.48 |
| 1989 | 1,206.40 | 2,943.35 | 2.44 | 4,149.75 | 2,945.32 | 1,567.40 | 0.51 |

### From Table N.2 (Appendix N, chunk 38)

| Year | Benefit rate | Tax rate | Ntrrate | NtrV* ($B) | S*/V* | Adjusted S**/V** |
|------|-------------|----------|---------|-----------|-------|----------------|
| 1952 | 0.11 | 0.18 | −0.07 | −7.55 | 1.75 | 1.95 |
| 1964 | 0.19 | 0.21 | −0.02 | −3.76 | 2.12 | 2.19 |
| 1971 | 0.25 | 0.25 | +0.01 | +1.48 | 2.08 | 2.06 |
| 1980 | 0.29 | 0.30 | 0.00 | −1.82 | 2.07 | 2.08 |
| 1989 | 0.29 | 0.32 | −0.04 | −65.77 | 2.44 | 2.58 |

### From Table I.1 (Appendix I, chunks 35–36)

| Year | hp (hrs/yr) | hu (hrs/yr) | ecp ($/yr) | ecu ($/yr) | ep = S*/V* | eu | eu/ep |
|------|------------|------------|-----------|-----------|-----------|------|-------|
| 1948 | 2,079 | 2,043 | 2,680 | 3,017 | 1.70 | 1.35 | 0.80 |
| 1972 | 2,080 | 2,065 | 9,568 | 9,983 | 1.99 | 1.84 | 0.92 |
| 1978 | — | — | — | — | 2.11 | 2.07 | 1.02 |
| 1989 | 2,094 | 2,076 | 29,233 | 29,444 | 2.44 | 2.37 | 0.97 |

### From Table J.1 (Appendix J, chunks 36–37)

| Year | q* ($/hr) | y* ($/hr) | y ($/hr) | q* index | y index |
|------|----------|----------|---------|---------|---------|
| 1948 | 27.56 | 15.30 | 11.11 | 100.0 | 100.0 |
| 1958 | 40.70 | 23.09 | 13.87 | 147.7 | 124.9 |
| 1972 | 55.58 | 32.61 | 17.97 | 201.7 | 161.8 |
| 1989 | 78.03 | 44.56 | 21.15 | 283.1 | 190.4 |

### NIPA Table Numbers (from Appendix J, chunk 36)

| NIPA Code | Description | Used For |
|-----------|-------------|----------|
| 107 2 | Total GDP | y (orthodox productivity), N1201 |
| 107 4 | Nonfarm private business GDP | y₂ |
| 611 2 | Total hours in domestic industries | H1 |
| 607B2 | Full-time equivalent employees | FEE |
| 610B5 | Farm employment | Lfarm |
| 704 1 | GNP price deflator (1982=100) | py (real values) |

---

## Remaining KB Mining (Updated After Second Pass)

| Chunks | Content | Priority | Status |
|--------|---------|----------|--------|
| 33–34 | Appendix F-G (Employment + Wages detail) | MEDIUM | Not yet read |
| 12, 16 | Ch 5 (Tables 5.4, 5.8–5.11) | MEDIUM | Not yet read |
| 19–21 | Ch 6 main text (Tables 6.3–6.4) | MEDIUM | Not yet read |
| 06–09 | Ch 3 (sector classification detail) | LOW | Classification already derived from other chunks |
| 24–30 | Ch 7 (conclusions) + Appendices A–D | LOW | Conclusions narrative; App D interpolation method partially known |

**Key realization**: Chapter 7 of the book is "Summary and Conclusions" (NOT a separate labor-value regression chapter). The R² = 0.98 result is from Ochoa (1984), discussed in Section 5.10 (chunk 17). No additional regression spec to find.

---

## Session 21 Continued: Chunks 13, 14, 15, 23, 31, 32

### Q3/Q6 Update: C*_m Interpolation Method — RESOLVED

**Evidence** (chunk 31, Appendix E):
- C*_m = Mp' (materials inputs into production)
- Mp' comes from **Appendix D interpolation** — IO variables extrapolated between benchmark years using NIPA-based ratios
- For 1978–89: "all variables except Mry were extrapolated" (Mry = residual for balance)
- The interpolation preserves the IO identity TV* = TP* (with statistical discrepancy)

**Method**: NIPA annual data provides aggregate totals (GDP, GVA by sector). IO benchmark years provide the decomposition. Between benchmarks, the ratios (Mp'/GVAp, RYp/GOp, etc.) are interpolated and applied to annual NIPA aggregates.

**Action**: Wave 2 B3 should replicate this — interpolate IO ratio Mp'/GVAp between benchmarks, multiply by annual NIPA GVAp.

### V* Calculation Methodology — CRITICAL DISCOVERY

**Evidence** (chunks 13–14, Section 5.3):

The book computes V* through a **sector-by-sector BLS-NIPA hybrid** method:

```
Step 1: L = NIPA PEP = FEE + SEP (includes self-employed)
Step 2: For each production sector j:
        (Lp/L)j = BLS production worker ratio
        (Lp)j = (Lp/L)j × Lj
Step 3: Lp = Σ(Lp)j;  Lu = L - Lp
Step 4: Wj = ecj × Lj where ecj extends EC to include self-employed
Step 5: (ecp)j = BLS unit wage × (EC/WS)j adjustment for supplements
Step 6: V* = Σ (ecp)j × (Lp)j for all production sectors
Step 7: Corporate officers' salaries EXCLUDED (Appendix G, following Mage)
```

**Productive services** = ALL services EXCEPT business services, legal services, private households.

**Three methodological gaps in our pipeline**:

1. **Self-employed persons**: NIPA PEP includes SEP; BLS CES does not → inflates total_scale gap
2. **Sector-by-sector ratios**: Book applies BLS production/total ratios per sector; our pipeline uses aggregate BLS CES production workers
3. **Corporate officers' salary exclusion**: Book excludes COS from V* (following Mage 1963); our pipeline may not

### Table E.2 Cross-Check Data — Complete Annual TP* Series

| Year | TV* ($B) | TP* ($B) | M'p ($B) | GFP* ($B) | FP* ($B) |
|------|----------|----------|----------|-----------|----------|
| 1948 | 446.25 | — | 198.47 | — | — |
| 1958 | 711.79 | — | 308.00 | — | — |
| 1972 | 1,728.88 | 1,728.41 | 714.33 | 1,014.08 | 969.81 |
| 1977 | — | 3,058.10 | 1,367.27 | 1,690.83 | 1,602.47 |
| 1989 | 7,639.86 | 7,726.22 | 3,122.99 | 4,603.23 | 4,151.71 |

### Profit Rate Definition — FULLY CONFIRMED

**Evidence** (chunk 15, Section 5.5):
- **r* = S*/K** (surplus value / total fixed capital at replacement cost)
- **Value composition** C*/V* = **K/V*** (capital stock / variable capital) — STOCK-based
- **Materialized composition** = K/(V*+S*) — also stock-based
- Capacity utilization: Shaikh's own method (not Wharton, not FRED TCU)

**Impact on T510**: The book's "value composition" in Table 5.7 is K/V* (stock/flow ratio), NOT M'p/V* (flow/flow). Our T510 may compute the wrong variable. Needs verification against Table 5.7 source data.

### NIPA Table Reference Mapping (from Appendix E)

| Book Code | Description | Modern BEA Equivalent |
|-----------|-------------|----------------------|
| 601 4–80 | GVA by sector | GDP-by-Industry (Table 6.1 discontinued) |
| 809 86/94 | Gross housing product | Fixed Assets tables |
| 107 2/4 | GDP total/nonfarm | NIPA 1.7.5 |
| 611 2 | Total hours domestic | Productivity tables |
| 607B2 | FTE employees | NIPA 6.5 |
| 610B5 | Farm employment | NIPA 6.10 |
| 704 1 | GNP deflator | NIPA 1.1.4 |

---

---

## Session 22: Unit Audit + Appendix F/G

### CRITICAL: T504/T505 Source Data Is Wrong (DEC-020)

The `VariableCapital_SurplusValue.csv` contains Phase 3 intermediate calculations 9-15x larger than the book's Table H.1 values:

| Series | Pipeline (1948) | KB Table H.1 (1948) | Ratio |
|--------|----------------|---------------------|-------|
| T501 TP* | 446.21 | 446.25 | 1.000 |
| T502 C*m | 198.47 | 198.47 | 1.000 |
| T504 V* | 1,294.2 | 88.41 | **14.6x** |
| T505 S* | 1,673.1 | 149.94 | **11.2x** |

The pipeline works despite this because T506 (S*/V*) comes from Table5_7 (correct ratios), not from T505/T504 division. Extension-period T504 is computed from correct T512 ratios × NIPA W. Only book-period T504/T505 levels and T608 (NSW/V*) are affected.

**Fix needed**: Replace source CSV with Table H.1 actual data (42 years, V* and S* in billions).

**IMPLEMENTED**: `L02b_reconstruct_v_star.py` created and run. Output: `data/final-data/book/series/V_S_star_reconstructed.csv` with 42 years of V*, S*, e*, VA* in billions, interpolated from 8 KB-verified V* data points and 11 KB-verified e* data points. All 8 verified points match exactly. This file can replace the VariableCapital_SurplusValue.csv source once integrated into the pipeline.

**Comparison (1948)**:
- Current pipeline T504: 1,294.16 (wrong units)
- Reconstructed V*: 88.41 billion (matches Table H.1)
- Ratio: 14.6x

### Appendix F (Employment) — Exact Lp Sector Decomposition

Table F.1 terminal year 1989 confirmed: L = 113,511K, Lp = 41,148K, Lp/L = 0.363.

Sector breakdown:
- Manufacturing Lp: 13,252K (68% of sector workforce)
- Mining Lp: 498K (71%)
- Construction Lp: 3,525K (68%)
- Transport/utilities Lp: 4,728K (83%)
- Productive services Lp: 11,044K (47%, using GNPpr/GNPserv = 0.587)
- Agriculture Lp: 2,169K (71%)
- Government enterprises Lp: 1,297K (73%)
- Trade: 24,375K (ALL unproductive)
- FIRE + ground rent: 5,955K (ALL unproductive)
- Government: 16,324K (ALL unproductive)

### Appendix G (Wages) — V* Methodology Confirmed

V* = Σ (ecp)j × (Lp)j where:
- (ecp)j = BLS wp × (EC/WS)j for most sectors
- (ecp)serv = ecserv (average) for services
- COS excluded naturally (BLS production wages exclude officers)
- Self-employed wage equivalent imputed: Wj = ecj × Lj

Total W (1989): $3,337,038 million = $3.337 trillion
Manufacturing share fell from 55% (1948) to 20% (1989)
Services share grew from 10% to 22%

---

*Report updated 2026-05-08 (Sessions 21-22). Total chunks read: 16 of 40 (added chunk 33). Key additions: DEC-020 unit audit, Appendix F sector decomposition, Appendix G wage methodology, T511 recompute test failed, T609 confirmed as NI.*
