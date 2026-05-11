# Equations - 2017 Moos NSW in 21st Century

**Source**: Moos, Katherine A. (2017). "Neoliberal Redistributive Policy: The U.S. Net Social Wage in the 21st Century." Working Paper No. 2017-18, University of Massachusetts Amherst.
**Extraction Date**: October 23, 2025
**Section Focus**: NSW methodology equations (Section 2, pages 3-4)

---

## Core NSW Definition

### Equation 1: Net Social Wage (Basic)

```latex
NetSocialWage = TotalLaborBenefits - TotalLaborTaxes
```

**Text form** (page 3):
```
NSW = Total Labor Benefits − Total Labor Taxes
```

**Where**:
- `NSW` = Net Social Wage (net fiscal transfer to labor from state)
- `TotalLaborBenefits` = All benefits and transfers received by workers from government
- `TotalLaborTaxes` = All taxes paid by workers to government

**Interpretation**:
- If `NSW > 0`: Workers receive more than they pay (net beneficiaries, state subsidizes labor)
- If `NSW < 0`: Workers pay more than they receive (net contributors, labor subsidizes state)
- If `NSW = 0`: Break-even (workers pay for their own benefits)

**Shaikh-Tonak Finding (1952-1997)**: Average NSW ≈ 0
- "In effect, workers paid for their own social benefits" (Shaikh 2003:542)

**Moos Finding (1959-2012)**:
- Average NSW = 0.020 (2.0% of GDP)
- **But**: Average 1959-2000 ≈ 0, Average 2001-2012 ≈ 5% of GDP
- **21st century shows dramatic positive NSW**

---

## Benefits to Labor

### Equation 2: Total Labor Benefits

```latex
TotalLaborBenefits = E1 + E2 * LS
```

**Where**:
- `E1` = Direct benefits to labor (unambiguously benefiting workers)
- `E2` = Mixed public goods (benefit both labor and capital)
- `LS` = Labor Share (proportion of GDP going to labor)

**E1 Categories** (Direct Labor Benefits):
1. **Social Security** (old-age retirement benefits)
2. **Medicare** (health insurance for 65+)
3. **Medicaid** (health insurance for low-income)
4. **Public Assistance** (TANF, SSI, etc.)
5. **SNAP/Food Stamps**
6. **Refundable Tax Credits** (EITC, Child Tax Credit)
7. **Unemployment Insurance**
8. **Public Housing** assistance
9. **Pensions and Disability**
10. **Veterans' benefits** (explicitly excluded from NSW per Shaikh-Tonak - treated as cost of war, not social policy)

**E2 Categories** (Mixed Public Goods, allocated by LS):
1. **Education** (K-12, higher education)
2. **Health** (hospitals, clinics - NOT insurance programs)
3. **Recreation and Culture**
4. **Natural Resources**
5. **Energy**
6. **Transportation** (roads, public transit)
7. **Postal Services**

**Note on E2 Allocation**:
- E2 items benefit **both** workers and capitalists
- Labor Share (`LS`) used to approximate portion benefiting workers
- Assumes benefits are distributed proportional to income shares

**Moos Finding**:
- E1 has grown dramatically (especially income support)
- E2 relatively stable or declining (as % of GDP)
- Income support (E1) is main driver of benefit growth

---

## Taxes from Labor

### Equation 3: Total Labor Taxes

```latex
TotalLaborTaxes = T1 + T2 * LS
```

**Where**:
- `T1` = Direct taxes on labor (unambiguously paid by workers)
- `T2` = Indirect and mixed taxes (allocated by labor share)
- `LS` = Labor Share

**T1 Categories** (Direct Labor Taxes):
1. **Employee Contributions** to Social Security
2. **Employer Contributions** to Social Security (treated as part of labor cost)
3. **Employee Contributions** to Medicare
4. **Employer Contributions** to Medicare
5. **Employee Contributions** to Unemployment Insurance
6. **Employer Contributions** to Unemployment Insurance

**Rationale for including employer contributions**:
- Employer-side payroll taxes are part of **cost of hiring workers**
- Economists treat them as labor taxes (incidence on workers via lower wages)
- If payroll taxes ↑, employers reduce wages to maintain total labor cost

**T2 Categories** (Indirect/Mixed Taxes, allocated by LS):
1. **Federal Income Taxes** (on labor income)
2. **State Income Taxes**
3. **Personal Property Taxes**
4. **Motor Vehicle Taxes**
5. **Miscellaneous Taxes and Fines**

**Note on Mixed Taxes**:
- These taxes are paid by both labor and capital
- Labor Share used to estimate workers' portion
- Example: Property taxes paid by homeowners (labor) and businesses (capital)

**Moos Finding**:
- T1 relatively stable as % of GDP
- T2 (especially federal income taxes) declined dramatically 2001-2012
- Tax cuts (Bush/Obama) reduced labor taxes → positive NSW

---

## Labor Share

### Equation 4: Labor Share

```latex
LS = \frac{EmployeeCompensation}{TotalPersonalIncome}
```

**Shaikh-Tonak Definition** (page 4):
> "labor share (employee compensation / total personal income)"

**Where**:
- `EmployeeCompensation` = Wages, salaries, and supplements from NIPA
- `TotalPersonalIncome` = All income (labor + capital) from NIPA

**Alternative Definition** (not used by Moos, but discussed):
```latex
LS = \frac{EmployeeCompensation}{EmployeeCompensation + OperatingSurplus}
```

**Moos Time Series** (1959-2012):
- 1959: LS ≈ 0.73 (73%)
- 1970: LS ≈ 0.72
- 1980: LS ≈ 0.70
- 1990: LS ≈ 0.68
- 2000: LS ≈ 0.66
- 2012: LS ≈ 0.62

**Trend**: **Declining** throughout period (neoliberal era)

**Significance**:
- LS is critical parameter for allocating E2 and T2
- Declining LS means workers get smaller share of mixed benefits/taxes
- But: Moos shows NSW results **robust** to alternative LS measures

---

## Alternative Labor Share (Mohun 2016)

### Equation 5: Mohun Income Share

```latex
LS_{Mohun} = \frac{EmployeeCompensation - SupervisoryWages}{TotalIncome}
```

**Rationale** (Mohun 2006, 2016):
- High-earning supervisory/managerial workers may be more akin to capitalists
- Their "wages" may function more like profit shares
- Excluding them gives "truer" measure of workers' income share

**Moos Application**:
- Uses Mohun (2016) data to recalculate NSW
- Mohun Income Share declines **much faster** than traditional LS
  - 1970: Mohun LS ≈ 0.68 vs Traditional LS ≈ 0.72
  - 2012: Mohun LS ≈ 0.45 vs Traditional LS ≈ 0.62
- **Finding**: NSW results nearly **identical** with either LS measure
- **Conclusion**: NSW methodology **robust** to labor share specification

**See**: `figures/all_figures.md` (Figures 13-14) for visual comparison

---

## NSW as Ratio

### Equation 6: NSW/GDP Ratio

```latex
NSW\_Ratio = \frac{NSW}{GDP}
```

**Where**:
- `NSW` = Net Social Wage (from Equation 1)
- `GDP` = Gross Domestic Product

**Moos Summary Statistics (1959-2012)**:

| Statistic | Value |
|-----------|-------|
| Minimum | -0.012 (−1.2% of GDP) |
| Median | 0.013 (1.3% of GDP) |
| Mean | 0.020 (2.0% of GDP) |
| Maximum | 0.086 (8.6% of GDP, in 2010) |

**Period Breakdown**:
- **1959-2000**: Mean ≈ 0 (zero NSW, workers pay for own benefits)
- **2001-2012**: Mean ≈ 0.05 (5% of GDP, workers receive net transfer)

**Historic High**: 2010 at 8.6% of GDP

---

### Equation 7: NSW/Employee Compensation Ratio

```latex
NSW\_EC\_Ratio = \frac{NSW}{EmployeeCompensation}
```

**Alternative presentation** used by Shaikh-Tonak (2000).

**Moos Summary Statistics (1959-2012)**:

| Statistic | Value |
|-----------|-------|
| Minimum | -0.022 (−2.2% of EC) |
| Median | 0.024 (2.4% of EC) |
| Mean | 0.037 (3.7% of EC) |
| Maximum | 0.161 (16.1% of EC, in 2010) |

**Interpretation**:
- At peak (2010), workers received **16.1% of their compensation** back from state (net)
- Emphasizes magnitude relative to wages
- More volatile than NSW/GDP (EC fluctuates more with business cycle)

---

## Unemployment Intensity (Shaikh 2013)

### Equation 8: Unemployment Intensity

```latex
UnemploymentIntensity = UnemploymentRate \times DurationIndex
```

**Where** (from Shaikh 2013):
- `UnemploymentRate` = Official U-3 unemployment rate (%)
- `DurationIndex` = Index of average unemployment duration (weeks unemployed)

**Purpose**:
- Captures not just **how many** are unemployed
- But also **how long** they remain unemployed
- Long-term unemployment has greater economic/social impact

**Moos Application** (Section 4.2.1):

**Comparison 1983 vs 2010**:

| Year | Unemployment Rate | Unemployment Intensity | NSW/GDP |
|------|-------------------|------------------------|---------|
| 1983 | 9.6% | 18.95% | 2.1% |
| 2010 | 9.6% | 31.46% | 8.6% |

**Key Finding**:
- Same unemployment rate (9.6%)
- But unemployment intensity 66% higher in 2010
- Corresponds to NSW being 4x higher in 2010

**Interpretation**:
- Great Recession unemployment was **longer duration** than 1980s recession
- Longer unemployment → longer benefit collection periods
- Helps explain why 2010 NSW so much higher than 1983 despite same U-rate

**See**: `table_descriptions/table_descriptions.md` (Table 3) for detailed comparison

---

## Decomposition Equations (Implicit)

### Equation 9: NSW Decomposition

```latex
NSW = (E1 - T1) + LS \times (E2 - T2)
```

Expanding Equations 2 and 3:

```latex
NSW = (E1 + E2 \times LS) - (T1 + T2 \times LS)
```

Rearranging:

```latex
NSW = (E1 - T1) + LS \times (E2 - T2)
```

**Components**:
1. **Direct component**: `(E1 - T1)`
   - Net direct fiscal transfer to labor
   - Not affected by labor share

2. **Indirect component**: `LS × (E2 - T2)`
   - Labor's share of net mixed fiscal items
   - Affected by labor share

**Moos Findings**:
- Direct component (E1 - T1) is **largest** and **growing**
  - E1 (income support) grew dramatically
  - T1 (payroll taxes) grew modestly
  - Result: (E1 - T1) increasingly positive

- Indirect component LS × (E2 - T2) is **smaller** and **relatively stable**
  - E2 (education, transport) stable or declining
  - T2 (income taxes) declined after 2001
  - LS declining offsets some gains

**Implication**:
- Income support (E1) is main driver of positive NSW
- Tax cuts (T2 ↓) contribute significantly
- Declining labor share (LS ↓) is NOT undermining NSW
  - Because E1-T1 dominates and is not multiplied by LS

---

## Real NSW

### Equation 10: Real Net Social Wage

```latex
RealNSW = \frac{NominalNSW}{GDPDeflator} \times 100
```

**Moos Conversion**:
- Base year: **2010**
- All NSW values converted to 2010 constant dollars
- Controls for inflation over 54-year period

**Moos Summary Statistics (Real NSW, 2010 dollars)**:

| Statistic | Value (billions, 2010$) |
|-----------|-------------------------|
| Minimum | -76.48 |
| Median | 119.40 |
| Mean | 255.10 |
| Maximum | 1288.00 (in 2010) |

**Significance**:
- Confirms positive NSW is **real**, not nominal artifact
- 2010 peak of $1.29 trillion is genuine transfer to workers
- Adjusting for inflation doesn't change main findings

**See**: `figures/all_figures.md` (Figure 10) for real NSW time series

---

## Growth Rates (Implicit Analysis)

### Equation 11: Average Annual Growth Rate

```latex
AAGR = \left(\frac{Value_{end}}{Value_{start}}\right)^{\frac{1}{years}} - 1
```

**Moos Calculations** (implicit in text):

**Income Support/GDP**:
```
AAGR = (0.125 / 0.025)^(1/53) - 1 ≈ 3.0% annually
```
- 1959: 2.5% of GDP
- 2012: 12.5% of GDP
- 5x increase over 53 years

**Old-Age Programs/GDP**:
```
AAGR = (0.085 / 0.025)^(1/53) - 1 ≈ 2.4% annually
```
- 1959: 2.5% of GDP
- 2012: 8.5% of GDP
- 3.4x increase

**Low-Income Programs/GDP**:
```
AAGR = (0.035 / 0.001)^(1/52) - 1 ≈ 7.0% annually
```
- 1960: ~0% of GDP
- 2012: 3.5% of GDP
- 35x increase (starting from near-zero)

---

## Summary of Key Formulas

| Equation | Formula | Purpose |
|----------|---------|---------|
| NSW | `(E1 + E2×LS) - (T1 + T2×LS)` | Core net social wage |
| E1 | Direct labor benefits | Income support, social insurance |
| E2 | Mixed public goods | Education, infrastructure |
| T1 | Direct labor taxes | Payroll taxes |
| T2 | Mixed taxes | Income, property taxes |
| LS | Employee Comp / Total Income | Labor share parameter |
| NSW/GDP | NSW / GDP | NSW as % of economy |
| NSW/EC | NSW / Employee Compensation | NSW as % of wages |
| U-Intensity | U-Rate × Duration Index | Shaikh unemployment intensity |

---

## Comparison: Moos vs Shaikh-Tonak

| Aspect | Shaikh-Tonak (2000) | Moos (2017) |
|--------|---------------------|-------------|
| **Period** | 1952-1997 | 1959-2012 |
| **Mean NSW/GDP** | ~0% | 2.0% |
| **Period 1959-1997 NSW** | ~0% | ~0% (consistent!) |
| **Period 1998-2012 NSW** | N/A | ~5% (new finding) |
| **Conclusion** | Workers pay for own benefits | 21st century: state subsidizes workers |

**Key Insight**:
Moos **replicates** Shaikh-Tonak for overlap period (1959-1997), validating methodology. But **extends** to show dramatic change in 21st century.

---

## Connection to Rate of Surplus Value (Not Calculated)

**Theoretical Framework** (mentioned but not empirically implemented):

### Equation 12: Effective Rate of Surplus Value

```latex
\frac{s}{v}_{eff} = \frac{S + (V_L - V_{st})}{V - (V_L - V_{st})}
```

**Where**:
- `s/v_eff` = Effective rate of exploitation (after state redistribution)
- `S` = Surplus value
- `V` = Variable capital (wages of productive workers)
- `V_L` = Taxes paid by productive workers
- `V_st` = Benefits received by productive workers

**Interpretation**:
- If NSW < 0 (workers pay more than receive): Effective exploitation rate **increases**
- If NSW > 0 (workers receive more than pay): Effective exploitation rate **decreases**

**Moos Implication**:
- 21st century positive NSW suggests **declining** effective exploitation rate
- State redistribution **reduces** the net extraction of surplus from productive workers
- However, Moos does **not calculate** this empirically (leaves for future research)

**Note**: Full s/v calculation requires distinguishing productive from unproductive labor, which Moos does not do.

---

**Extraction Complete**: All NSW calculation equations documented with US-specific applications and Moos 2017 results.
