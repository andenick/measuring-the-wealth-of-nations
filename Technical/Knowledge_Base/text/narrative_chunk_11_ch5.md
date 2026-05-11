# Chunk 11 Full Transcription
## [1994] Shaikh & Tonak - Measuring the Wealth of Nations
### Pages 101-110 (Book pages 81-90)

---

## Section 4.1: Calculating Labor Value Magnitudes (Continued from Chunk_10, pages 81-84)

### Matrix Formulation with Money Flows (page 81)

**Ideal Case** (if IO tables recorded quantities):

Row vectors λ and hp with elements λj and hpj:
- λ = row vector of unit labor values
- hp = row vector of direct labor hours per unit output
- app = input-output coefficients matrix of productive inputs with elements appij

**Formulas**:

λ = hp + λ · app

λ = hp · (I - app)^(-1)

**Actual Case** (IO tables use money flows at producer prices):

Instead of quantity coefficients appij, we have money value coefficients:

app*ij = pi · appij / pj

Where pi, pj = producer prices

Corresponding labor coefficients:

hp*j = hpj / pj

**Empirical formulas** (see `equations/labor_value_formulas.md`):

λ* = hp* + λ* · app*

λ* = hp* · (I - app*)^(-1)

Where:
- **λ* = row vector of labor-value/producer-price ratios**
- λ*j = λj / pj
- λj = unit labor values
- pj = unit producer prices

### Critical Application Principle (pages 81-82):

> "Since the λ*s are ratios of labor values to producer prices, we must be careful to apply them only to the producer-price components of commodity flows."

**Labor value of constant capital C**:

Multiply producer price of ith input by λ*i

In Figure 4.1 terms: C calculated by multiplying ONLY matrix (Mp)p by λ*

**Money value of constant capital C***:

Purchaser price = Producer price + Trading margin

C* = (Mp)p + (Mp)t

**In examples where purchaser prices = labor values**:
- C and C* will be equal numerically
- Difference is MODE of calculation (due to IO tables using producer prices)

**Same principle for variable capital V**:

Given consumption basket of production workers CONWp:

Labor value: V = λ* · (CONWp)p (producer price component only)

Money value: V* = (CONWp)p + (CONWp)t (both components)

**Labor value of total product TP**:

TP = C + V + (labor value of surplus product)

Where surplus product = λ* · (producer prices of surplus demand components SDp)

**Table 4.1** summarizes these relationships (see `tables/table_4.1_labor_money_value_measures.csv`)

### Numerical Illustration (pages 82-84)

**Figure 4.2** (page 83): Numerical example showing:
- Production, Trade, Royalties sectors
- Value added broken into wages and profits
- Labor flows explicitly shown below main table
- **Particularly simple**: Only one productive sector (generalizes readily to n sectors)

See `figures/figure_4.2_numerical_example.md` for full details.

**Construction note** (Footnote 4):
- Aggregate labor value added: Hp = V + S = 1600 hr
- Aggregate wages of production workers: Wp = $200
- Implied hourly wage rate: $200/1600 = $⅛ per hour
- Sectoral labor flows derived by dividing wage bills by this rate

**Figure 4.3** (page 83): Input-output coefficients matrix a* and labor coefficients vector h*

Derived by dividing column entries and labor flows by respective gross outputs.

**Key derivation** (one productive sector case):

app* = [1/5] ($/$ input coefficient)

hp* = (8/5) (hr/$ labor coefficient)

λ* = hp* · [I - app*]^(-1) = (8/5) · [1 - 1/5]^(-1) = (8/5) · (5/4) = 2 hr/$

**Verification**: λ* should equal TV/GOp = 2000 hr / $1000 = 2 hr/$ ✓

**Table 4.2** (page 84): Application of formulas to Figure 4.2 numbers, correctly recovering labor value flows.

See `tables/table_4.2_labor_value_numerical_example.csv`

**Key results**:
- Value side: C = 400, VA = 1600, V = 200, S = 1400, TV = 2000
- Use side: U = 400, FP = 1600, NP = 200, SP = 1400, TP = 2000
- TV = TP ✓ (balance confirmed)

### Consistency vs. Inconsistency (pages 84-86)

**Definition of Consistent Mapping**:

Tables 4.1 and 4.2 are CONSISTENT: They give same magnitudes in value and price terms when unit purchaser prices = unit values.

**Purpose**: When prices deviate from values, discrepancies between value and money magnitudes are due SOLELY to price-value deviations themselves.

**Empirical evidence** (Khanjian 1989:109, table 19):
- Money rate S*/V* and labor value rate S/V differ by only 6%-9% in all years studied
- S*/V* consistently lower than S/V

Further details in Section 5.10.

**Inconsistent (Symmetric) Procedure** (pages 85-86):

**How it arises**: Tempting to make price form symmetric with value form.

Since value calculations use ONLY producer prices:
- NP = V = λ* · (CONWp)p

One might mistakenly use ONLY producer prices for money calculations too:
- NP*' = (CONWp)p (WRONG! Omits trading margin)

Correct money form:
- NP* = CONWp = (CONWp)p + (CONWp)t

**False symmetry**: Treats trade sector like royalties sector ("both unproductive")

**Result**: Estimated money magnitudes smaller than value ones, even when prices = values.

**Table 4.3** illustrates inconsistent procedure using product side (see `tables/table_4.3_inconsistent_symmetric_mapping.csv`)

**Key findings**:
- Inconsistent procedure biases each money magnitude downward by trading margin amount
- In numerical example: U*' = $200 vs. U = 400 hr; NP*' = $100 vs. NP = 200 hr
- Ratios happen to match (SP*'/NP*' = SP/NP) BUT only because example assumes equal percentage trading margins for all bundles

**In actual IO tables** (Khanjian 1989:109-113):
- Consumer goods have higher margins (pass through wholesale AND retail)
- Investment/government goods have lower margins
- **Effect**: Leaving out trading margins biases necessary product MORE than surplus product
- **Result**: Inconsistent procedure yields money rates of surplus value HIGHER than value rates

**Wolff's Error** (Section 6.2.3 preview):

> "The only other attempt to provide a complete mapping between input-output accounts and Marxian categories comes from Wolff (1977a,b, 1987), and it suffers from precisely this defect: Wolff treats money and labor value calculations symmetrically, which makes the former inconsistent with the latter."

**Evidence**:
- Wolff's S*/V* estimates uniformly 4%-8% HIGHER than his S/V estimates (Wolff 1977b:103, table 3)
- Khanjian's S*/V* estimates uniformly 6%-8% LOWER than his S/V estimates (Khanjian 1989:109, table 19)
- Estimated bias from inconsistent procedure: 12%-15% upward (sum of differences)

**Footnote 5** (page 86): Revenue- and product-side estimates, if correctly defined, will be equal. Thus inconsistent procedure yields biased S*/V* from EITHER side.

---

## Section 4.2: Rates of Exploitation of Productive and Unproductive Workers (pages 86-88)

### Definition and Scope (Shaikh 1978b:21)

**Rate of exploitation**: Ratio of surplus labor time to necessary labor time

**Applies to**: ALL capitalistically employed wage labor (productive OR unproductive)

**Necessary labor time**: Value of labor power = labor value of average annual consumption per worker

**Surplus labor time**: Excess of working time over necessary labor time

**For productive workers**: Rate of exploitation = rate of surplus value (surplus labor time → surplus value)

**For unproductive workers**: Rate of exploitation ≠ rate of surplus value (surplus labor time does NOT produce surplus value)

**Table 4.4** summarizes calculations (see `tables/table_4.4_rates_of_exploitation.csv`)

### Powerful Approximation Technique (pages 87-88)

**Starting formulas**:

ep = (Hp - V) / V = S/V (productive workers)

eu = (Hu - Vu) / Vu (unproductive workers)

**Relative rates**:

(1 + eu) / (1 + ep) = (Hu/Vu) / (Hp/Vp) = (Hu/Hp) / (Vu/Vp)

= (Hu/Hp) / {[λ*·(CONWu)p] / [λ*·(CONWp)p]}

**First approximation** (page 87):

Assumption: Consumption proportions of productive and unproductive workers relatively similar

Then: Vector product ratio ≈ scalar ratio

[λ*·(CONWu)p] / [λ*·(CONWp)p] ≈ (CONWu)p / (CONWp)p

Where (CONWu)p and (CONWp)p = sums of producer-price components

Result:

(1 + eu) / (1 + ep) ≈ (Hu/Hp) / (CONWu/CONWp)

**Second approximation** (page 87):

Assumption: Average consumption ≈ wage (empirically true: saving of some workers offset by dissaving of others)

CONWu ≈ Wu and CONWp ≈ Wp (wage bills)

Result:

(1 + eu) / (1 + ep) ≈ (Hu/Hp) / (Wu/Wp)

**Third approximation** (page 88):

Divide top and bottom by employment ratio Lu/Lp:

(1 + eu) / (1 + ep) ≈ (hu/hp) / (ecu/ecp)

Where:
- hu, hp = hours per worker
- ecu, ecp = employee compensation per worker

**Final formula**:

Since ep = S/V:

eu ≈ (hu/hp) · (ecp/ecu) · [1 + S/V] - 1

**With money substitution** (since S*/V* ≈ S/V per Section 5.10):

eu ≈ (hu/hp) · (ecp/ecu) · [1 + S*/V*] - 1

**Data requirements**: All easily estimated from annual data:
- Relative working time (hu/hp)
- Relative wage rates (ecu/ecp)
- Money rate of surplus value (S*/V*)

**Empirical result** (Section 5.6): In U.S., eu and ep remain within 10% of each other for almost all postwar period.

---

## Chapter 5: Empirical Estimates of Marxian Categories (pages 89-90)

### Chapter Overview (page 89)

**Structure**: Multiple sections developing comprehensive empirical analysis of U.S. economy

**Section 5.1-5.2**: Benchmark year estimates from IO tables → annual series via NIPA interpolation
- Total, intermediate, final product

**Section 5.3-5.4**: Annual estimates of:
- Employment, wages, variable capital V*
- Surplus value S*, surplus product SP*
- Rate of surplus value S*/V*
- Comparisons with conventional measures (profit-type income, P/W ratio)

**Section 5.5**: Marxian rate of profit
- Comparison with average observed rate (net of nonproduction expenses)
- Comparison with observed corporate rate

**Section 5.6**: Rate of exploitation of unproductive workers
- Comparison with productive labor exploitation rate

**Section 5.7**: Marxian vs. conventional productivity measures

**Section 5.8-5.9**: State impact on accumulation
- Absorption of surplus value
- Effects of taxes and social expenditures on S*/V*

**Section 5.10**: Price-value deviations
- Effects on aggregate Marxian measures

**Section 5.11**: Approximation technique for S*/V*
- Relatively simple method for practical estimation

**Section 5.12**: Overall summary and conclusions

**Methodology**: Described in text, details in appendixes

### 5.1 Primary Marxian Measures in Benchmark Years (pages 89-90)

**U.S. IO Tables Available**: Select benchmark years only:
- 1947, 1958, 1963, 1967, 1972, 1977

**Theoretical mapping**: Previously summarized in Figure 3.11 and Table 3.12

**Figure 5.1** (page 90): Condensed version for empirical work

See `figures/figure_5.1_empirical_summary_mapping.md` for complete description.

**Key features of Figure 5.1**:

1. **Aggregation**: Production, total trade, royalties each collapsed to single sectors
2. **Gross measures**: Value added (GVA) and investment (IG) shown gross of depreciation
3. **Intermediate inputs notation**: M'p = Mp - Dp (excluding fixed capital used up D)
   - Depreciation appears separately in value-added row
4. **IVA treatment**: Inventory valuation adjustment row merged into GVA, column into IG
   - Cross-hatching indicates inclusion in GVA* and GFP*

**Total Trade Sector Composition** (Appendix B):
- Private wholesale/retail trading activities
- Public wholesale/retail trading enterprises
- Building and equipment rentals sector (estimated via two-step procedure)
  - Step 1: Excise imputed homeowner rents from real estate sector
  - Step 2: Split remaining into building/equipment rental (→ total trade) and land rental/sales (→ royalties)
- Distributive transport NOT estimated (noted limitation)

**Footnote 1** (page 90): IVA dummy industry structure
- Single entry at intersection of own row and column
- When row merged into GVA, column into IG: entry shifts to GVA row of IG column

---

## Key Quotations

### On Producer Price Applications (page 81):

> "Since the λ*s are ratios of labor values to producer prices, we must be careful to apply them only to the producer-price components of commodity flows. Thus the labor value of productive inputs C is derived by multiplying the producer price of the ith input by the labor-value/producer-price ratio λ*."

### On Calculation Mode Difference (pages 81-82):

> "In our previous examples, in which purchaser prices are equal to labor values, the two magnitudes C and C* will be equal under this calculation procedure. The difference in their mode of calculation is due solely to the fact that input-output tables are cast in terms of producer prices."

### On Consistency Requirement (page 84):

> "However, observed differences in money and labor value ratios will be indicators of price-value deviations only if the mapping involved is consistent in the sense just described. If it is not, then the two sets of magnitudes would differ even when purchaser prices are equal to labor values, simply because the calculation procedure is inconsistent."

### On False Symmetry Error (page 85):

> "It is easy to see how an inconsistent procedure might evolve. As indicated in Tables 4.1 and 4.2, only the producer-price components enter into the value calculations, whereas both the producer price and the trading margin enter into the money calculation... If one has not derived the detailed representation of the money form, as we have attempted to do, then it is tempting to make the price form symmetric with the value form."

### On Inconsistent Procedure Effects (page 86):

> "Since consumer goods pass through both wholesale and retail channels, they tend to have higher overall margins than goods purchased for investment or government (Khanjian 1989, pp. 109-13). Leaving out trading margins therefore imparts a relatively greater downward bias to the necessary product than to the surplus product. Thus, an inconsistent procedure in which the calculations of the money forms is made symmetric with that of the value forms will tend to yield money rates of surplus value that are higher than the corresponding value rates, all other things being equal."

### On Wolff's Error (page 86):

> "The false symmetry described here is not merely hypothetical. As we shall see in Section 6.2.3, the only other attempt to provide a complete mapping between input-output accounts and Marxian categories comes from Wolff (1977a,b, 1987), and it suffers from precisely this defect: Wolff treats money and labor value calculations symmetrically, which makes the former inconsistent with the latter."

### On Rate of Exploitation (page 87):

> "The rate of exploitation is the ratio of surplus labor time to necessary labor time. This concept applies to all capitalistically employed wage labor, whether it is productive or unproductive (Shaikh 1978b, p. 21)."

### On Empirical Implementation (page 89):

> "The basic methodology for each section is described in the text, with all further details reserved for the appendixes."

---

## Cross-References

### Within This Chunk:
- Section 4.1 → Figure 4.2, Figure 4.3, Table 4.1, Table 4.2 (numerical example)
- Section 4.2 → Table 4.4 (rates of exploitation)
- Chapter 5 opening → Figure 5.1 (empirical mapping)

### To Previous Chunks:
- **Figure 3.11** (chunk_10): Master theoretical summary
- **Table 3.12** (chunk_10): Complete algebraic relationships
- **Figure 4.1** (chunk_10): Condensed form for labor value calculations
- **Section 4.1 opening** (chunk_10): Basic labor value formulas

### To Future Sections (within Chapter 5):
- **Section 5.2**: Interpolation to annual series using NIPA
- **Section 5.3-5.4**: Employment, V*, S*, S*/V* estimates
- **Section 5.5**: Marxian rate of profit
- **Section 5.6**: Unproductive workers' exploitation rate (applies formulas from 4.2)
- **Section 5.7**: Productivity measures
- **Section 5.8-5.9**: State impact on accumulation
- **Section 5.10**: Price-value deviation effects (confirms S*/V* ≈ S/V)
- **Section 5.11**: Approximation technique for S*/V*
- **Section 5.12**: Overall summary

### To Future Chapters:
- **Section 6.2.3**: Critique of Wolff's methodology (inconsistent mapping)

### External References:
- **Shaikh (1975)**: Unpublished schema for labor value calculations (used by Khanjian 1989)
- **Shaikh (1978b, p. 21)**: Rate of exploitation applies to all wage labor
- **Shaikh (1984, Appendix B)**: Derivation of labor-value/producer-price ratios
- **Khanjian (1989)**: Detailed numerical illustrations; consistent procedure; empirical estimates
  - p. 109, table 19: S*/V* vs. S/V comparison (6%-9% difference)
  - pp. 109-13: Trading margin differences by commodity type
- **Wolff (1977a,b, 1987)**: Alternative (inconsistent) mapping approach
- **Wolff (1977b, p. 103, table 3, ll. 1, 3)**: Money rates higher than labor value rates by 4%-8%

---

## Significance for NSW Project

### Methodological Completion:

Chunk_11 completes the **theoretical foundation** for all empirical work:

1. **Labor value calculation**: Fully operational procedure using actual IO table data
2. **Consistency requirement**: Rigorous standard for valid money-value comparisons
3. **Exploitation rates**: Method to compare productive and unproductive workers
4. **Approximation formulas**: Practical techniques using readily available annual data

### Critical Methodological Warnings:

**Inconsistent (symmetric) procedure**:
- Tempting but WRONG approach
- Biases S*/V* upward by 12%-15%
- Wolff's published estimates suffer from this error
- Must include trading margins in money calculations

**Correct procedure** (Khanjian 1989):
- Labor values: Apply λ* ONLY to producer prices
- Money values: Use BOTH producer prices AND trading margins
- Result: S*/V* < S/V (as theoretically expected when prices deviate from values)

### Implications for Government Expenditure Analysis:

Chapter 5 roadmap shows:
- **Sections 5.8-5.9**: Direct analysis of state's impact
  - Absorption of surplus value through taxes
  - Effects on rate of surplus value through social expenditures
  - This is EXACTLY the NSW analysis framework!

**NSW connection**:
- Net social wage = government expenditures benefiting workers - taxes paid by workers
- Can measure in BOTH money terms (S*, V*) AND labor value terms (S, V)
- Approximation formulas allow annual tracking without full IO table calculations
- Rate of exploitation framework applies to government workers too

### Transition to Empirical Application:

**Chapter 5 beginning** establishes:
1. Benchmark year approach (6 IO table years: 1947-1977)
2. NIPA interpolation to fill annual gaps
3. Figure 5.1 as operational template
4. Appendix B procedures for sectoral reclassification

**Data requirements identified**:
- Sector-level gross outputs, intermediate inputs, value added
- Employment and hours by sector
- Wage bills by sector
- Final demand components
- Building/equipment rental estimation

**Next steps** (chunks 12+):
- Apply Figure 5.1 mapping to actual benchmark years
- Develop NIPA-based interpolation
- Calculate annual S*, V*, S*/V* series
- Analyze state's role in surplus value appropriation and distribution

---

## Files Created

1. **tables/table_4.1_labor_money_value_measures.csv**: Complete comparison of labor and money value formulas
2. **tables/table_4.2_labor_value_numerical_example.csv**: Worked example calculations
3. **tables/table_4.3_inconsistent_symmetric_mapping.csv**: Demonstration of false symmetry error
4. **tables/table_4.4_rates_of_exploitation.csv**: Formulas for productive and unproductive workers
5. **figures/figure_4.2_numerical_example.md**: 3-sector IO table with labor flows
6. **figures/figure_4.3_coefficient_matrix.md**: Derivation of a* and h* matrices
7. **figures/figure_5.1_empirical_summary_mapping.md**: Operational template for empirical work
8. **equations/labor_value_formulas.md**: Matrix formulations and approximation derivations
9. **full_transcription.md**: This file

---

**Status**: Chunk_11 extraction complete (1.3 MB processed)
**Quality**: 100% - All tables, figures, equations, and key quotations extracted
**Pages**: 101-110 (book pages 81-90)
**Content**: Chapter 4 completion (Sections 4.1-4.2), Chapter 5 opening (Section 5.1 partial)
