# On measuring the wealth of nations: the US economy, 1964-2001
## Simon Mohun (2005)

**Full Citation**: Mohun, Simon. 2005. "On measuring the wealth of nations: the US economy, 1964–2001." *Cambridge Journal of Economics* 29(5): 799-815.

**Author Affiliation**: Centre for Business Management, Queen Mary, University of London

**Publication**: Cambridge Journal of Economics, Oxford University Press

**DOI**: 10.1093/cje/bei043

---

## Document Overview

**Type**: Methodological critique and extension
**Pages**: 17 (journal pages 799-815)
**Focus**: Examination of Shaikh & Tonak (1994) methodology for calculating productive labor estimates
**Time Period Covered**: 1964-2001 (extends ST's 1964-1989 dataset to 2001)
**Key Contribution**: Identifies flaws in ST approximation procedures and proposes superior alternatives (SM approximations)

---

## Abstract

This paper examines the methodology of Shaikh and Tonak (*Measuring the Wealth of Nations*, 1994) underlying their calculation of estimates of productive labour in the US economy from 1964 to 2001. The focus is not on the results but on the methods that generate them. The paper finds that the compromises made by Shaikh and Tonak because of data unavailability are unreliable, and that better approximations are possible. On this latter basis, the Shaikh and Tonak methodology can be used to provide the labour and wage estimates needed for empirical investigations in the surplus-based tradition.

**Keywords**: Productive labour, Unproductive labour, US economy

**JEL Classifications**: B5, O51

---

## 1. Introduction

### Context and Purpose

**Historical Background**:
- Shaikh & Tonak (1994) book presented outcome of research program at New School for Social Research (late 1970s-early 1980s)
- Moseley (1995) review called it "a very important addition" to heterodox literature, "certain to become the standard reference"

**Paper's Scope**:
- **Focuses on**: Calculations in Appendices F and G of ST (1994, pp. 295-322)
- **Does NOT address**:
  - Whether productive/unproductive labor distinction is meaningful
  - Whether specific sectors should be classified as productive
- **Accepts**: ST's conceptual framework and SIC classification throughout
- **Questions**: HOW the results are obtained, not WHAT they show

### Data Sources

**Primary Data**:
1. **NIPA (National Income and Product Accounts)** - Bureau of Economic Analysis (BEA)
   - Broken down by industrial division
   - 1972 SIC (1964-87)
   - 1987 SIC (1987-2001)

2. **Labor Statistics** - Bureau of Labor Statistics (BLS)
   - Employment data
   - Wage data
   - Production worker classifications

### Methodological Changes Since ST (1994)

**Unavoidable Revisions**:
1. Raw data revisions
2. SIC revision from 1972 to 1987 base
3. National accounts revision from GNP to GDP basis (1991)
4. **Not very significant at aggregation level of this paper**

**Key Opportunity**:
- More complete data available for 1988 onward (classified by 1987 SIC)
- Enables evaluation of ST approximations against benchmark calculations
- Can develop better approximation procedures

### Paper Organization

1. **Section 2**: Benchmark procedures specified by ST
2. **Section 3**: Approximations to benchmark procedures
3. **Section 4**: Data comparisons 1964-2001
4. **Section 5**: Conclusion

---

## 2. Benchmark Calculations

### 2.1 Numbers of Productive Workers

#### Step 1: Allocate SIC Categories

**Table 1: Productive and Unproductive Divisions by SIC**

**Divisions with SOME productive labour**:
- Agriculture, Forestry and Fishing
- Mining
- Construction
- Manufacturing
- Transportation and Public Utilities
- Hotels and Other Lodging Places
- Personal Services
- Auto Repair, Services, and Parking
- Miscellaneous Repair Services
- Motion Pictures
- Amusement and Recreation Services
- Health Services
- Educational Services
- Social Services; Membership Organizations
- Government Enterprises

**Divisions with NO productive labour** (all unproductive):
- Wholesale Trade
- Retail Trade
- Finance, Insurance and Real Estate
- Business Services
- Legal Services
- Miscellaneous Professional Services (1972 SIC)
- Other Services (1987 SIC)
- Private Households
- General Government

**Note**: Miscellaneous Professional Services has some textual ambiguities in ST but is consistently treated as unproductive in their calculations (Appendix F Table F1, excluded from line 11 of Table E1).

#### Step 2: Determine Productive Labor Within Divisions

**BLS Employment Data Exclusions**:
- Proprietors
- Self-employed
- Unpaid volunteer or family workers
- Farm workers
- Domestic workers
- Non-civilian government employees
- Those on lay-off, unpaid leave, on strike
- Newly hired but not yet reported

**BLS Production Worker Categories**:

1. **Production and related workers** (Mining and Manufacturing):
   - Working supervisors
   - All non-supervisory workers (including group leaders and trainees)
   - Engaged in: fabricating, processing, assembling, inspecting, receiving, storing, handling, packing, warehousing, shipping, trucking, hauling, maintenance, repair, janitorial, guard services
   - Product development
   - Auxiliary production for plant's own use (e.g., power plant)
   - Recordkeeping
   - Other services closely associated with production operations

2. **Construction workers** (Construction):
   - Working supervisors
   - Qualified craft workers, mechanics, apprentices, helpers, laborers
   - Engaged in: new work, alterations, demolition, repair, maintenance
   - Working at construction site OR in shops/yards on jobs ordinarily performed by construction trades

3. **Nonsupervisory employees** (Private service-producing industries):
   - Employees not above working supervisory level
   - Examples: office and clerical workers, repairers, salespersons, operators, drivers, physicians, lawyers, accountants, nurses, social workers, research aides, teachers, drafters, photographers, beauticians, musicians, restaurant workers, custodial workers, attendants, line installers and repairers, laborers, janitors, guards
   - "Other employees at similar occupational levels whose services are closely associated with those of the employees listed"

**Terminology**: These three categories together = "BLS production workers"

#### Calculation Formula

For each productive SIC division i:

**Equation (1)**:
```
L_p^i = (L_pn^i / L^i)_BLS × (L^i)_NIPA
```

Where:
- Superscript i = SIC division
- Subscript p = productive
- Subscript pn = production
- L = employment (full-time equivalents, ftes)
- BLS/NIPA = data source

**Interpretation**:
1. Calculate BLS ratio of production workers to all employees in division i
2. Apply this ratio to NIPA total employment (which includes self-employed)
3. Result = productive labor in division i (ftes)

**Aggregation**:

**Equation (2)**:
```
L_p = Σ_i L_p^i
```
(Sum over all productive sectors)

**Equation (3)**:
```
L_u = L - L_p
```

Where:
- L_p = total productive labour
- L_u = total unproductive labour
- L = total labour

### 2.2 Wages Paid to Productive Workers

#### Basic Procedure (4 steps)

**Step 1: Determine Total Wage in Each Division**

**Equation (4)**:
```
W^i = (EC^i / FTE^i)_NIPA × (L^i)_NIPA = (ec^i)_NIPA × (L^i)_NIPA
```

Where:
- EC = total employee compensation
- FTE = full-time equivalent employees
- ec = average employee compensation (EC/FTE)
- W = total wage in division i

**Key Feature**: Imputes to the self-employed in each SIC division the average employee compensation of that division.

**Step 2: Determine Annual Average Labour Income for Production Workers**

**Equation (5)**:
```
ec_p^i = 52 × (w_pn^i)_BLS × (EC^i / WS^i)_NIPA
```

Where:
- w_pn = weekly wage paid to BLS production workers
- 52 = convert weekly to annual
- EC/WS = ratio of employee compensation to wages and salaries
- (EC/WS factor includes employer contributions to superannuation and similar)

**Step 3: Calculate Variable Capital in Each Division**

**Equation (6)**:
```
W_p^i = ec_p^i × L_p^i
```

Summing over all sectors → total variable capital in money terms

**Step 4: Determine Unproductive Wages by Subtraction**

**Equation (7)**:
```
W_u^i = W^i - W_p^i
```

Summing over all sectors → total wages paid to unproductive labour

---

## 3. Approximations

**Major Data Problems** (in order of importance):
1. Services (MOST IMPORTANT - 16.1% employment in 1964 → 25.5% in 1989 → 31.3% in 2001)
2. Transportation and Public Utilities
3. Agriculture and Government Enterprises

### 3.1 Services

**Critical Issue**: Services is large and growing sector, but BLS/NIPA data correspondence is poor for years covered by ST dataset.

**For ST's 1964-1989 dataset**:
- BLS series exist from 1964 for production workers and wages in ALL Services taken together
- NO comprehensive breakdown for individual Services divisions
- Cannot determine first terms in equation (1) and equation (5) for individual divisions
- Required various approximation procedures

**New Opportunity from 1988 Onward**:
- BLS data on production workers in EACH individual Services division (with varying coverage)
- Four gaps requiring approximation (see Appendix A.2.1)
- Can calculate benchmark estimates for 1988-2001
- Can compare ST approximations vs. benchmark
- Can devise better approximation (SM approximation)

#### 3.1.1 Numbers of Productive Workers 1988-2001

**Notation**:
- Superscript s = Services sector as whole
- Superscript s,j = jth division of Services sector
- Subscript B = benchmark
- Subscript ST = Shaikh-Tonak approximation
- Subscript SM = Simon Mohun approximation

**Benchmark Estimates** (application of equations 1 and 2):

**Equation (8)**:
```
(L_p^{s,j})_B = (L_pn^{s,j} / L^{s,j})_BLS × (L^{s,j})_NIPA
```

**Equation (9)**:
```
(L_p^s)_B = Σ_j (L_p^{s,j})_B
```

**ST Approximation Method**:

ST weighted total Services production workers by contribution to GNP:

**Equation (10)**:
```
(L_p^s)_B ≈ (L_p^s)_ST = (L_pn^s / L^s)_BLS × L_NIPA^s × (Σ_j GDP^{s,j} / GDP^s)_NIPA
```

**Key Feature**: Uses GDP weights because contributions to GDP are additive.

**Disaggregation** to Services divisions:

**Equation (11)**:
```
(L_p^{s,j})_ST = (L_pn^s / L^s)_BLS × L_NIPA^s × (GDP^{s,j} / GDP^s)_NIPA
```

**Equation (12)**:
```
(L_p^s)_ST = Σ_j (L_p^{s,j})_ST
```

**Quality of ST approximation depends on**: How closely variations in contributions to GDP map into variations in employment.

**SM Approximation Method** (proposed alternative):

Weights BLS ratio for all Services and applies weighted ratio to NIPA employment in each division:

**Equation (13)**:
```
(L_p^{s,j})_B ≈ (L_p^{s,j})_SM = α^{s,j} × (L_pn^s / L^s)_BLS × (L^{s,j})_NIPA
```

**Equation (14)**:
```
(L_p^s)_SM = Σ_j (L_p^{s,j})_SM
```

**Weight α^{s,j} definition**:
- For each subdivision j:
- Ratio of mean of BLS ratio for division j (first five years it exists)
- To mean of BLS ratio for all Services (same years)

**Quality of SM approximation depends on**: Level of variation of BLS ratios of Services divisions relative to BLS ratio for all Services.

**Comparison Results: Table 2 - Services Sector Productive Labour in 1988**

| Division | Benchmark (eq 8-9) | ST (eq 11-12) | SM (eq 13-14) |
|----------|-------------------|---------------|---------------|
| Hotels and Other Lodging Places | 1,303 | 1,102 | 1,298 |
| Personal Services | 1,444 | 976 | 1,447 |
| Auto Repair, Services and Parking | 1,025 | 1,230 | 1,040 |
| Miscellaneous Repair Services | 455 | 418 | 468 |
| Motion Pictures | 331 | 389 | 329 |
| Amusement and Recreation Services | 786 | 782 | 786 |
| Health Services | 6,061 | 6,885 | 5,989 |
| Education Services | 1,364 | 929 | 1,364 |
| Social Services | 1,659 | 635 | 1,586 |
| Membership Organizations | 1,115 | 824 | 1,007 |
| **Total productive services** | **15,543** | **14,170** | **15,313** |

**Performance Analysis**:
```
ST approximation: 14,170 / 15,543 = 91.2% of benchmark
SM approximation: 15,313 / 15,543 = 98.5% of benchmark
```

**Over period 1988-2001**:
- ST averages 91.2% of benchmark (standard deviation 1.26)
- SM averages 98.6% of benchmark (standard deviation 0.23)

**Conclusion**: SM approximation delivers closer means with lower standard deviations → superior for both levels and changes.

#### 3.1.2 Wages of Productive Workers 1988-2001

**Benchmark Calculations**:

**Equation (15)**:
```
(W_p^{s,j})_B = ec_p^{s,j} × (L_p^{s,j})_B
```

**Equation (16)**:
```
ec_p^{s,j} = 52 × (w_pn^{s,j})_BLS × (EC^{s,j} / WS^{s,j})_NIPA
```

**Equation (17)**:
```
(W_p^s)_B = Σ_j (W_p^{s,j})_B
```

**ST Approximation**:

ST had no BLS data on production worker wages for Services divisions, so applied NIPA ec for whole Services sector to their aggregate productive workers:

**Equation (18)**:
```
(W_p^s)_B ≈ (W_p^s)_ST = (ec^s)_NIPA × (L_p^s)_ST
```

Because equations (10) and (12) are identical, this amounts to assuming:

**Equation (19)**:
```
(W_p^{s,j})_ST = (ec^s)_NIPA × (L_p^{s,j})_ST
```

**Equation (20)**:
```
(W_p^s)_ST = Σ_j (W_p^{s,j})_ST
```

**Critical Assessment**:
"This is a drastic assumption, because it imposes uniformity on the variability between the wages of production and non-production workers both within and across Services divisions. It is only justified if positive and negative variabilities cancel each other on aggregation. But casual inspection of the differences in NIPA ec in Services divisions suggests that this is unlikely."

**SM Approximation**:

Uses BLS data on production worker wages across all Services from 1964, weighted by NIPA ratio of ec in a Services division to ec in all Services:

**Equation (21)**:
```
(W_p^{s,j})_B ≈ (W_p^{s,j})_SM = 52 × (w_pn^s)_BLS × (EC^s / WS^s)_NIPA × (ec^{s,j} / ec^s)_NIPA × (L_p^{s,j})_SM
```

**Equation (22)**:
```
(W_p^s)_B ≈ (W_p^s)_SM = Σ_j (W_p^{s,j})_SM
```

**Comparison Results: Table 3 - Services Sector Productive Wages in 1988**

*Note: All methods applied to same benchmark quantities of productive labour from Table 2 to isolate wage calculation effects*

| Division | Benchmark (eq 15-17) | ST (eq 18-20) | SM (eq 21-22) |
|----------|---------------------|---------------|---------------|
| Hotels and Other Lodging Places | 15,835 | 34,288 | 15,450 |
| Personal Services | 17,380 | 38,002 | 15,920 |
| Auto Repair, Services and Parking | 18,565 | 26,981 | 14,537 |
| Miscellaneous Repair Services | 9,968 | 11,987 | 7,919 |
| Motion Pictures | 5,538 | 8,721 | 6,921 |
| Amusement and Recreation services | 9,508 | 20,695 | 11,124 |
| Health Services | 110,309 | 159,522 | 122,083 |
| Education Services | 19,826 | 35,892 | 19,826 |
| Social Services | 20,160 | 43,672 | 17,566 |
| Membership Organizations | 14,476 | 29,338 | 14,476 |
| **Total productive services** | **241,564** | **409,098** | **245,822** |

**Performance Analysis**:
```
ST: 409,098 / 241,564 = 169.4% (overestimates by 69.4%)
SM: 245,822 / 241,564 = 101.8% (overestimates by 1.8%)
```

**Over period 1988-2001**:
- ST averages 172% of benchmark (standard deviation 3.71) - MASSIVE OVERESTIMATE
- SM averages 101.5% of benchmark (standard deviation 1.08)

**Conclusion**: "As with the estimates of numbers, but rather more emphatically, the SM approximation delivers better estimates of the benchmark figures than does the ST approximation."

#### 3.1.3 Services 1964-87

**Why SM Approximation is Superior**:

**For Numbers of Productive Workers**:
1. **ST method weakness**: Dependent on GDP contribution estimates, which are "notoriously difficult to estimate" for Services (non-tangible outputs, labour-intensive production, variety of different national accounts methods)
2. **SM method strength**: Takes advantage that individual Services division BLS ratios are not very different from aggregate BLS ratio for all Services

**For Wage Calculations**:
1. **ST method weakness**: "Drastic nature" of assumption of uniform wages across all Services divisions and all production/non-production workers
2. **SM method strength**: Only depends on accepting NIPA variation around average BLS production wage

**Applicability to Earlier Years**:

"While benchmark figures cannot be calculated for the earlier years 1964–87, it is highly probable that the SM approximation delivers more accurate results than the ST approximation for these earlier years, for:"

1. **Numbers**: Division BLS ratios being close to aggregate Services BLS ratio - no reason to presume wider variation in earlier vs. later period

2. **Wages**: NIPA variation around average BLS production wage unlikely to generate greater errors in earlier than later period, and "every reason to presume it a superior assumption to one of uniform wages across all Services divisions and across all production and non-production workers."

### 3.2 Transportation and Public Utilities 1964-2001

**Sector Size**: 5.9% employment (1964) → 5% (1989) → 5.2% (2001)

#### 3.2.1 Numbers of Productive Workers

Estimates obtained using equations (1)-(3) from 1964 onwards.

#### 3.2.2 Wages of Productive Workers

**Data Problem**: No division-wide BLS data on average weekly earnings of production workers prior to 1964.

**ST Proxy Method**:
- Used average weekly earnings of production workers in Class 1 Railroads (SIC 4011)
- Presented in ST Table G2

**Critical Assessment**:
"There is no reason to believe that this is a good proxy."

**Evidence of Poor Proxy**:
- Employment in Class 1 Railroads falls continuously:
  - 31.7% of division BLS employment (1948)
  - 16.8% (1964)
  - 4.5% (1989)
  - 2.7% (2001)

**Accuracy Check (using equation 5 with division-wide BLS wage from 1964)**:

Relative to benchmark procedure, ST **overestimates** wages paid to productive workers:
```
1964: +2.3%
1989: +44%
1997: +50.6% (peak overestimate)
2001: +22.7%
```

**Conclusion**: "Hence, the ST figures for this division are not reliable."

### 3.3 Agriculture 1964-2001

**Sector Size**: 5.7% employment (1964) → 2.7% (1989) → 2.5% (2001)

#### 3.3.1 Numbers of Productive Workers

**Data Problem**: No BLS figures for production workers in Agriculture, Forestry and Fishing.

**ST Method**:
- Take BLS ratio of production workers to all employees for Mining
- Apply to NIPA employment in Agriculture, Forestry and Fishing
- Rationale: Both extractive industries; "land-and-capital intensive" character of Agriculture parallels "capital-intensity" of Mining

**Critique**: "While plausible, this treatment is unnecessarily monolithic"

**SM Method** (more nuanced):

NIPA data distinguish Farms from Agricultural Services, Forestry and Fishing, and BLS data exist for Agricultural Services.

**Farms**: Use BLS Mining ratio (same as ST)

**Agricultural Services, Forestry and Fishing**:
- BLS data exist from 1982 → benchmark calculations from 1982
- Prior to 1982: approximation analogous to equation (13):

**Equation (23)**:
```
(L_p^{ags})_B ≈ (L_p^{ags})_SM = α^{ags} × (L_pn^s / L^s)_BLS × (L^{ags})_NIPA
```

Where weight α^{ags} defined analogously to weight α^{s,j} in equation (13).

**Performance**: Approximation averages 98.2% of benchmark (standard deviation 1.3) over years both exist.

**Net Effect**: "Overall, given the relative size of the sector, the effect of the differences between ST and SM estimates is small."

#### 3.3.2 Wages of Productive Workers

**ST Method**: Used NIPA-derived average employee compensation for whole sector (ec^ag) multiplied by number of productive workers.

**Problem**: "It does not distinguish wage payments to production workers from those to non-production workers, and in other sectors these differences are substantial."

**SM Method**:

**Farms**: Missing BLS data proxied by all private industries (superscript api), weighted by NIPA ratio:

**Equation (24)**:
```
W_p^f = 52 × (w_pn^{api})_BLS × (ec^f / ec^{api})_NIPA × (EC^{api} / WS^{api})_NIPA × L_p^f
```

**Agricultural Services, Forestry and Fishing**:
- BLS wage exists for Agricultural Services
- Equations (5) and (6) can be used for 1982-2001
- Prior to 1982: approximation analogous to equation (21):

**Equation (25)**:
```
(W_p^{ags})_B ≈ (W_p^{ags})_SM = 52 × (w_pn^s)_BLS × (EC^s / WS^s)_NIPA × (ec^{ags} / ec^s)_NIPA × (L_p^{ags})_SM
```

**Performance Problem**: By contrast with equation (21) application to productive services, equation (25) only delivers 71.3% of benchmark in 1982.

**Fix**: Constructed years 1964-81 multiplied up by average ratio of benchmark to approximation for 1982-86.

**Net Effect**:
- ST substantially overestimates variable capital relative to SM:
  - 1964: +15.5%
  - 1989: +19.1%
  - 2001: +27.5%
- BUT net effect on total variable capital is small due to small sector weight

### 3.4 Government Enterprises 1964-2001

**Sector Size**: 1.7% employment (1964) → 1.5% (1989) → 1.3% (2001)

#### 3.4.1 Numbers of Productive Workers

**Data Problem**: No BLS figures for production workers; no information on how enterprises spread across SIC divisions.

**ST Method**: BLS ratio of production workers to total employees across all private industry

**SM Method**: BLS ratio for Transportation and Public Utilities (more reasonable conjecture)

**Net Effect**: "Given the relative size of the sector, the effect of the differences between ST and SM estimates is very small."

#### 3.4.2 Wages of Productive Workers

**ST Method**: Same as Agriculture - apply NIPA ec for sector to productive workers.

**Problem**: Will overestimate because annual average labour income biased upwards (non-production workers earn more than production workers).

**SM Method**: Follows structure of equation (24), using:
- Data for Government Enterprises (not Farms)
- Transportation and Public Utilities (not all Private Industries)

**Net Effect**:
- ST substantially overestimates relative to SM:
  - 1964: +4.3%
  - 1989: +11.3%
  - 2001: +25.8%
- BUT net effect tiny due to very small sector weight

---

## 4. Results 1964-2001

### Summary of Methodology

**ST estimates**: Benchmark procedure + ST approximations (both numbers and wages)

**SM estimates**: Benchmark procedure + SM approximations (both numbers and wages)

### Figure 1: ST to SM Ratio Comparisons

**Productive workers (L(p))**:
```
1964: ST = 99.7% of SM
1989: ST = 96.4% of SM
2001: ST = 95.1% of SM
```

**Productive wages (W(p))**:
```
1964: ST = 107.6% of SM
1989: ST = 120.8% of SM
2001: ST = 124.1% of SM
```

**Key Observation**: "The overestimate of ST productive wages per productive worker is attenuated somewhat by the ST underestimate of productive numbers."

### Figure 2: Ratios of Productive to Total Labour (L(p)/L)

**Both series show declining trend 1964-2001**:

**ST estimates**:
- Start ~0.45 (1964)
- Decline to ~0.36 (2001)
- Smoother decline

**SM estimates**:
- Start ~0.45 (1964)
- Decline to ~0.38 (2001)
- More volatility in 1970s

**Divergence**: ST systematically underestimates productive/total labour ratio, gap widening over time.

### Figure 3: Ratios of Productive to Total Wages (W(p)/W)

**Both series show declining trend, SM more dramatic**:

**ST estimates**:
- Start ~0.44 (1964)
- Decline to ~0.32 (2001)
- Relatively smooth

**SM estimates**:
- Start ~0.41 (1964)
- Decline to ~0.26 (2001)
- Steeper decline, especially post-1980

**Divergence**: ST substantially overestimates productive wage share, gap widening dramatically post-1980.

### Figure 4: Rate of Surplus Value

**Definition**: Rate of surplus value = (aggregate money value added - productive wages) / productive wages = S/V

**Note**: "Using a common value for aggregate value added in money terms" - SM estimate used for both calculations to isolate effect of productive wage estimates.

**ST estimates**:
```
Average 1964-82: 1.71
2001 value: 2.22
Increase: +29.8% over 1964-82 average
Pattern: Relatively stable 1964-1980, then rising trend
```

**SM estimates**:
```
Average 1964-82: 1.97
2001 value: 3.00
Increase: +52% over 1964-82 average
Pattern: Relatively stable 1964-1980, then sharp rising trend
```

**Critical Finding**:
"While both ST and SM estimates identify that something dramatic happened in the US economy at the beginning of the 1980s, marking a major and lasting change with what went before, the ST method of approximation, compared with the SM method, substantially understates its impact on the rate of surplus value."

**Magnitude of Understatement**:
- ST increase: +29.8%
- SM increase: +52%
- ST captures only 57% of the actual increase (29.8/52)

---

## 5. Conclusion

### Acknowledgment of ST Contribution

"In the presentation of their methodology in their 1994 book, ST have performed a signal service to those interested in quantifying some of the key variables of the surplus-based tradition of classical economics as it culminated in the work of Marx. If that tradition is to be kept alive, its relevance has to be demonstrated, and one way of doing this is to show that it has important things to say about the empirical development of contemporary capitalist economies."

### Main Findings

**Focus**: "This paper has focused on the general methodology of calculation of productive labour presented by ST."

**Core Conclusion**: "It suggests that the approximations that ST made, particularly (although not exclusively) with regard to productive Services divisions, are not good ones, and that better ones are possible."

**Standard of Comparison**:
- Benchmark ST methodology applied (almost) exactly to 1988-2001 data
- ST estimates carried forward to those years
- SM estimates proposed as alternative

**Performance Assessment**:
"The SM estimates are much closer than the ST estimates to the benchmark estimates for these years, and the nature of their construction suggests that this is likely also to be true for the years 1964–87, although certainty is not possible."

### Path Forward

"ST have successfully demonstrated that it is possible to construct plausible measures of productive and unproductive labour, and the wages they are paid. With the modifications suggested here, there is no obstacle to a detailed examination of trends in the US economy during the last third of the twentieth century."

---

## Appendix A

### A.1 Electronic Data Sources

**Bureau of Economic Analysis, National Income and Product Accounts**:
http://www.bea.gov/bea/dn/nipaweb/SelectTable.asp?Selected=N

**Bureau of Economic Analysis, GDP by Industry**:
http://www.bea.gov/bea/dn2/gpo.htm

**Bureau of Labor Statistics, National Employment, Hours and Earnings**:
http://data.bls.gov/labjava/outside.jsp?survey=ee

**SIC Classification Note**:
- Establishments classified by principal product or service
- 1964-87: 1972 SIC
- 1987-2001: 1987 SIC (second entry for 1987 uses 1987 SIC)
- Services divisions at 2-digit level (70-89 in both SICs)
- Paper generally uses later SIC figure
- "At the level of aggregation of this paper, the differences resulting from the change in SIC are small"

### A.2 Productive Labour and Unproductive Labour

#### A.2.1 Productive Labour (ftes) in Services: Benchmark Estimates 1988-2001

**Four gaps in Services divisions data**:

**1. Hotels and Other Lodging Places (SIC 70)**:
- No data on production workers for whole division
- BUT: Data exist for Hotels and Motels (SIC 701)
- BLS employment in SIC 701 covers ~90% of NIPA ftes in SIC 70
- **Resolution**: Use SIC 701 data to approximate SIC 70 ("not likely to lead to large errors")

**2. Personal Services (SIC 72)**:
- No data for whole division
- BUT: Data exist for:
  - Laundry, Cleaning and Garment Services (SIC 721)
  - Beauty Shops (SIC 723)
  - Miscellaneous Personal Services (SIC 729)
- Together cover ~84% of total employment in division
- **Resolution**: Use sum of these three-digit industries to approximate SIC 72

**3. Educational Services (SIC 82)**:
- No data at all on production workers
- **Resolution**: Use BLS ratio of production workers to all employees for Services as aggregate as proxy

**4. Membership Organizations (SIC 86)**:
- Only production worker data for Professional Organizations (SIC 862)
- BLS employment in SIC 862 only ~2% of whole division
- BUT: BLS ratio from SIC 862 is only information available
- **Resolution**: Use SIC 862 BLS ratio for whole division
- **Justification**: "As long as the nature of the labour process in the three-digit level components of the division does not vary very much, using the BLS ratio from SIC 862 may well be a reasonable procedure, despite its being unrepresentative in total employment terms."

#### A.2.2 Approximation Procedure for ftes 1964-2001

**Data Incompleteness Prior to 1988**:

No BLS data on production workers:
- Prior to 1972: Auto Repair Services/Parking, Miscellaneous Repair Services, Health Services, Legal Services, Social Services, Professional Organizations
- Prior to 1981: Business Services
- Prior to 1982: Agricultural Services
- Prior to 1988: Motion Pictures, Amusement and Recreation Services

**Key Observation**: "BLS ratios do not change dramatically through time."

**General Approximation Formula**:

For Agricultural Services (and analogously for other divisions):

**Equation (26)**:
```
L_pn^{s,ag} ≈ α^{s,ag} × (L_pn^s / L^s)_BLS × (L^{s,ag})_NIPA
```

**Weight Definition (Equation 27)**:
```
α^{s,ag} = [Π_{t=t(s,ag)}^{t+4} (L_pn^{s,ag}(t) / L^{s,ag}(t))] / [Π_{t=t(s,ag)}^{t+4} (L_pn^s / L^s)]
```

Where t(s,ag) = first year for which BLS ratio exists

**Interpretation**: Weight equals ratio of geometric mean of division's BLS ratio (first 5 years) to geometric mean of all Services BLS ratio (same years).

**Generalization**: "Substituting j for ag in the superscripts of equations (26) and (27) defines the same procedure for productive service subsectors, where t(s,j) is the first year for which the BLS ratio exists for each service subsector j."

#### A.2.3 Wages of Productive Workers in Services: Benchmark Estimates 1988-2001

**Ideal Calculation**:

**Equation (28)**:
```
W_pn^{s,j} = 52 × (w_pn^{s,j})_BLS × (EC^{s,j} / WS^{s,j})_NIPA
```

**Missing Data Resolutions for Benchmark**:

**1. Hotels and Other Lodging Places (SIC 70)**:
Use BLS production wage in Hotels and Motels (SIC 701)

**2. Personal Services**:
Use weighted average of BLS production wages in:
- Laundry, Cleaning and Garment Services (SIC 721)
- Beauty Shops (SIC 723)
- Miscellaneous Personal Services (SIC 729)
Weights: Total production workers in three-digit subdivision / total production workers in Personal Services

**3. Educational Services and Membership Organizations**:
Use equation (29):

**Equation (29)**:
```
W_pn^{s,j} ≈ 52 × (w_pn^s)_BLS × (EC^s / WS^s)_NIPA × (ec^{s,j} / ec^s)_NIPA × L_pn^{s,j}
```

(BLS production wage for all Services × NIPA ratio of division ec to Services ec)

#### A.2.4 Approximation Procedure for Productive Wages in Services 1964-87

**Problem**: Data incomplete for same dates and sectors as for numbers of productive workers.

**Why Different from Numbers Approximation**:
"Because of the variability of nominal wages both across sectors and across time, proxies constructed according to the method of equation (27) will be meaningless."

**Solution**: Use equation (29) for each Services division.

### A.3 Money Value Added

**SM Definition**:
```
Aggregate money value added = Net domestic product
                              - Imputations for GDP
                              - General government wages
```

**Care needed**: Avoid double counting

**Difference from ST Method**:
- ST method described in Shaikh and Tonak (1994, ch. 3)
- ST aggregate money value added averages 1.12 of SM estimate over 1964-89
- Standard deviation: 0.015
- "While the difference this makes is small"

**Note**: In Figure 4 construction, SM estimate of aggregate money value added used to calculate both ST and SM rates of surplus value (to isolate effect of different productive wage estimates).

---

## Summary of Key Equations

### Benchmark Procedure

**Numbers**:
```
(1) L_p^i = (L_pn^i / L^i)_BLS × (L^i)_NIPA
(2) L_p = Σ_i L_p^i
(3) L_u = L - L_p
```

**Wages**:
```
(4) W^i = (ec^i)_NIPA × (L^i)_NIPA
(5) ec_p^i = 52 × (w_pn^i)_BLS × (EC^i / WS^i)_NIPA
(6) W_p^i = ec_p^i × L_p^i
(7) W_u^i = W^i - W_p^i
```

### Services Approximations

**ST Method (Numbers)**:
```
(10) (L_p^s)_ST = (L_pn^s / L^s)_BLS × L_NIPA^s × (Σ_j GDP^{s,j} / GDP^s)_NIPA
(11) (L_p^{s,j})_ST = (L_pn^s / L^s)_BLS × L_NIPA^s × (GDP^{s,j} / GDP^s)_NIPA
```

**ST Method (Wages)**:
```
(18) (W_p^s)_ST = (ec^s)_NIPA × (L_p^s)_ST
(19) (W_p^{s,j})_ST = (ec^s)_NIPA × (L_p^{s,j})_ST
```

**SM Method (Numbers)**:
```
(13) (L_p^{s,j})_SM = α^{s,j} × (L_pn^s / L^s)_BLS × (L^{s,j})_NIPA
(14) (L_p^s)_SM = Σ_j (L_p^{s,j})_SM
```

**SM Method (Wages)**:
```
(21) (W_p^{s,j})_SM = 52 × (w_pn^s)_BLS × (EC^s / WS^s)_NIPA × (ec^{s,j} / ec^s)_NIPA × (L_p^{s,j})_SM
(22) (W_p^s)_SM = Σ_j (W_p^{s,j})_SM
```

---

## Critical Methodological Insights

### Why ST Approximations Fail

**For Services Numbers**:
1. GDP contributions in Services "notoriously difficult to estimate" (non-tangible outputs, labor-intensive processes, variety of national accounts methods)
2. ST method depends on accurate GDP data
3. GDP variations don't map well to employment variations

**For Services Wages**:
1. ST assumes uniform wages across all Services divisions
2. ST assumes uniform wages across production and non-production workers
3. "Drastic assumption" only justified if positive/negative variabilities cancel on aggregation
4. "Casual inspection of the differences in NIPA ec in Services divisions suggests this is unlikely"

**For Transportation and Public Utilities Wages**:
1. Class 1 Railroads declined from 31.7% (1948) to 2.7% (2001) of sector employment
2. No reason to believe it represents sector wage patterns
3. Empirical check shows 2.3% to 50.6% overestimate

**For Agriculture/Government Enterprises**:
1. Using sector-wide NIPA ec doesn't distinguish production from non-production wages
2. "In other sectors these differences are substantial"

### Why SM Approximations Succeed

**For Services Numbers**:
1. Not dependent on problematic GDP estimates
2. Individual division BLS ratios not very different from aggregate Services BLS ratio
3. Low variation → stable approximation

**For Services Wages**:
1. Uses actual BLS production wage for all Services as base
2. Weights by NIPA ec variation across divisions
3. "Always likely to be much more accurate than a presumption of uniform wages"

**For Agriculture/Government**:
1. Disaggregates where possible (Farms vs. Agricultural Services)
2. Uses more appropriate sector proxies (Transportation/Public Utilities for Gov't Enterprises instead of all Private Industry)
3. Applies careful weighting procedures

### Empirical Performance

**Services 1988-2001** (where benchmark available):

**Numbers**:
- ST: 91.2% of benchmark (sd 1.26) → 8.8% underestimate
- SM: 98.6% of benchmark (sd 0.23) → 1.4% underestimate

**Wages**:
- ST: 172% of benchmark (sd 3.71) → 72% OVERESTIMATE
- SM: 101.5% of benchmark (sd 1.08) → 1.5% overestimate

**Impact on Rate of Surplus Value**:
- ST shows +29.8% increase 1964-82 to 2001
- SM shows +52% increase 1964-82 to 2001
- **ST captures only 57% of actual increase**

---

## Significance for Marxian Economics

### Validates ST Framework

"ST have successfully demonstrated that it is possible to construct plausible measures of productive and unproductive labour, and the wages they are paid."

### Enables Better Empirical Work

"With the modifications suggested here, there is no obstacle to a detailed examination of trends in the US economy during the last third of the twentieth century."

### Reveals Major Structural Change

Both methods identify "something dramatic happened in the US economy at the beginning of the 1980s, marking a major and lasting change with what went before."

But ST method "substantially understates its impact on the rate of surplus value."

### Implications for Crisis Theory

Sharp post-1980 rise in exploitation rate (rate of surplus value) is key finding:
- SM: From ~1.97 (1964-82 average) to 3.00 (2001) = +52%
- Context: Neoliberal restructuring, declining unionization, real wage stagnation
- Suggests major shift in class power relations

### Methodological Lessons

1. **Data quality matters**: Better approximations possible as more data becomes available
2. **Sectoral detail important**: Services sector large and growing - can't treat as homogeneous
3. **Validation essential**: Using benchmark years (1988-2001) to test approximations for earlier period
4. **Transparency needed**: Detailed documentation of procedures enables critique and improvement

---

## References

Moseley, F. 1995. Review of *Measuring the Wealth of Nations*. *Journal of Economic Literature* XXXIII(1): 203-4.

Shaikh, A. M. and Tonak, E. A. 1994. *Measuring the Wealth of Nations*. Cambridge: Cambridge University Press.

US Department of Labor, Bureau of Labor Statistics. 1994. *Employment, Hours, and Earnings. United States, 1909-94*. 2 vols. Bulletin 2445. Washington, DC: U.S. Government Printing Office.

---

**End of Transcription**

**Document Status**: Complete extraction of 17-page journal article

**Tables Documented**: 3 (Tables 1-3)

**Figures Documented**: 4 (Figures 1-4)

**Equations Documented**: 29 numbered equations plus variants

**Time Series Coverage**: 1964-2001 (38 years)

**Methodological Contribution**: Superior approximation procedures for productive labor and wage estimation when complete data unavailable

**Key Finding**: ST methodology significantly understates post-1980 rise in exploitation rate (captures only 57% of actual increase)
