# Equations - 2011 Paitaridis & Tsoulfidis: Core Formulas

**Source**: Paitaridis, D., & Tsoulfidis, L. (2011). "The Growth of Unproductive Activities, the Rate of Profit, and the Phase-Change of the U.S. Economy"
**Journal**: Review of Radical Political Economics, 44(2), 213-233
**Extraction Date**: October 23, 2025

---

## 1. Rate of Surplus Value (RSV) - Decomposition

### Formula (Page 220)

```latex
RSV = \frac{MVA - V}{V} = \frac{(MVA / P_{GDP}) / L_P \cdot P_{GDP}}{(V / P_{CPI}) / L_P \cdot P_{CPI}} - 1 = \frac{y \cdot P_{GDP}}{w_P \cdot P_{CPI}} - 1
```

**Where**:
- `MVA` = Marxian Value Added
- `V` = Variable capital (wages of productive workers)
- `L_P` = Number of productive workers
- `P_GDP` = GDP deflator
- `P_CPI` = Consumer Price Index
- `y` = Productivity (MVA per productive worker, deflated by P_GDP)
- `w_P` = Real wage of productive workers (deflated by P_CPI)

### Simplified Form

```latex
RSV = \frac{y}{w_P} \cdot \frac{P_{GDP}}{P_{CPI}} - 1
```

**Interpretation**:
- RSV determined by ratio of productivity to real wage
- Adjusted for differential price movements (GDP deflator vs. CPI)
- Rising productivity + stagnant wages → rising RSV

### Empirical Application

**From Table 1 growth rates**:
- Productivity (y) growth 1964-2007: 1.76% annually
- Real wage (w_P) growth 1964-2007: 0.26% annually
- **Gap**: 1.50 percentage points
- **Result**: RSV rose from ~2.15 (1964) to ~3.55 (2007)

---

## 2. Marxian Value Added (MVA)

### Definition (Page 219)

```latex
MVA = \sum_{j \in Productive} VA_j^{net} + Royalties_P + GO_{Trade}^{net}
```

**Where**:
- `VA_j^net` = Net value added (gross value added minus depreciation) of productive sector j
- `Royalties_P` = Royalties (taxes, rents, interests) paid by productive sectors to:
  - Financial institutions
  - Unproductive services
  - Government
- `GO_Trade^net` = Gross output of trade and real estate sectors, net of imputations

### Exclusions from MVA

**Excluded**:
1. "Output" of private households
2. "Output" of government sector (public administration, defense, government services)

**Included productive government services**:
- Transportation and communications (government-operated)
- Public utilities

### Net of Imputations

```latex
GO_{Trade}^{net} = GO_{Trade} - Imputations_{Trade}
```

**Imputation percentages** (page 219, footnote 2):
- 1964: 10.8% of GDP
- 2007: 14.7% of GDP
- Real estate sector: 55-56% (stable over time - owner-occupied housing)

---

## 3. Total Surplus Value

### Formula

```latex
S = MVA - V
```

**Where**:
- `S` = Total surplus value
- `MVA` = Marxian Value Added (as defined above)
- `V` = Variable capital (wages of productive workers, including employer contributions)

### Decomposition

```latex
S = NetProfits + UnproductiveActivities
```

```latex
S = \pi + (UnproductiveWages + UnproductiveDepreciation + Taxes + Royalties)
```

**From Figure 2 (2007 values, billions $)**:
- S ≈ $8,500
- Unproductive Activities ≈ $6,000 (71% of S)
- Net Profits (π) ≈ $1,000 (12% of S)

---

## 4. General Rate of Profit

### Formula

```latex
R = \frac{S}{C + V}
```

**Where**:
- `R` = General rate of profit
- `S` = Total surplus value
- `C` = Constant capital (net fixed capital stock)
- `V` = Variable capital

### Alternative Expression

```latex
R = \frac{S/V}{C/V + 1} = \frac{RSV}{VCC + 1}
```

**Where**:
- `RSV` = Rate of surplus value (S/V)
- `VCC` = Value composition of capital (C/V)

**Interpretation**:
- R rises with RSV (exploitation rate)
- R falls with VCC (mechanization)
- Counteracting tendencies

---

## 5. Net Rate of Profit

### Formula (Page 224, footnote 13)

```latex
r = \frac{\pi}{C} = \frac{NetProfits}{NetCapitalStock}
```

**Calculation of Net Profits**:

```latex
\pi = GDP - W_{GeneralGovt} - Imputations - TotalEmploymentCompensation_{adj} - NetIndirectBusinessTaxes - CorporateIncomeTaxes
```

**Where**:
- `W_GeneralGovt` = Wages of general government
- `TotalEmploymentCompensation_adj` = Adjusted for self-employed
- Net of all unproductive deductions

### Relationship to General Rate

```latex
r = R - \frac{UnproductiveActivities}{C}
```

**Interpretation**:
- Net r always < General R
- Gap = burden of unproductive sector
- As unproductive activities grow, gap widens

---

## 6. Value Composition of Capital

### Formula

```latex
VCC = \frac{C}{V}
```

**Where**:
- `C` = Net fixed capital stock (current cost)
- `V` = Variable capital (productive workers' compensation)

### Data Source (Page 223, footnote 11)

**BEA data**: Current-cost net stock of private non-residential fixed assets and government enterprises

**Excludes**:
- Residential capital
- Financial assets
- Land values (except as embodied in fixed assets)

---

## 7. Crisis Condition: Stagnant Mass of Profits

### Derivation (Pages 226-227)

Starting with definition:

```latex
\pi = r \cdot C
```

Taking differences:

```latex
\Delta \pi = r \cdot \Delta C + C \cdot \Delta r
```

Dividing by ΔC:

```latex
\frac{\Delta \pi}{\Delta C} = r + \frac{C}{\Delta C} \cdot \Delta r
```

Factoring out r:

```latex
\frac{\Delta \pi}{\Delta C} = r \left(1 + \frac{\Delta r}{\Delta C} \cdot \frac{C}{r}\right)
```

### Crisis Tipping Point

**Condition for stagnant mass of profits**: Δπ/ΔC = 0

This requires:

```latex
1 + \frac{\Delta r}{\Delta C} \cdot \frac{C}{r} = 0
```

Or equivalently:

```latex
\frac{\Delta r}{\Delta C} \cdot \frac{C}{r} = -1
```

**Elasticity form**:

```latex
\varepsilon_{r,C} = \frac{\Delta r / r}{\Delta C / C} = -1
```

**Interpretation**:
- Percentage change in r with respect to percentage change in C equals -1
- Fall in profit rate exactly offsets rise in capital stock
- Additional investment yields NO additional profit
- Investment becomes redundant → accumulation disrupted

**Quoted from page 227**:
> "The necessary condition is attained when the elasticity of the rate of profit, that is the term (ΔrC/ΔCr), is equal to –1, which is equivalent to saying that the percentage change in the fall in the rate of profit (Δr/r) is exactly matched by a rise in capital accumulation (ΔC/C), a condition requiring a persistently and sufficiently falling rate of profit."

### Empirical Verification

**Figure 8 shows**: ln(π) flat during 1965-1984
- Crisis condition approximately met
- Mass of real profits stagnant for ~20 years
- "Silent depression"

---

## 8. Productivity

### Formula

```latex
y = \frac{MVA / P_{GDP}}{L_P}
```

**Where**:
- `y` = Labor productivity (real MVA per productive worker)
- `MVA` = Marxian Value Added
- `P_GDP` = GDP deflator (2005 base year)
- `L_P` = Number of productive workers

### Growth Rates (from Table 1)

| Period | y (PT) | y (ST) |
|--------|--------|--------|
| 1948-1965 | - | 3.60% |
| 1965-1982 | 1.40% | 2.50% |
| 1982-2007 | 1.96% | - |
| 1964-2007 | 1.76% | - |

**Note**: PT estimates show sharper productivity slowdown in 1965-1982 than ST estimates

---

## 9. Real Wage of Productive Workers

### Formula

```latex
w_P = \frac{V / P_{CPI}}{L_P}
```

**Where**:
- `w_P` = Real wage of productive workers
- `V` = Variable capital (total compensation of productive workers)
- `P_CPI` = Consumer Price Index
- `L_P` = Number of productive workers

### Growth Rates (from Table 1)

| Period | w_P (PT) |
|--------|----------|
| 1965-1982 | 0.20% |
| 1982-2007 | 0.15% |
| 1964-2007 | 0.26% |

**Key finding**: Real wage growth near zero for entire 43-year period

---

## 10. Variable Capital Calculation

### Methodology (Appendix, page 231)

**Step 1**: Estimate productive employment in sector j

```latex
(L_P)_j = \left(\frac{L_P}{L}\right)_j \times (L_j)_{NIPA}
```

**Where**:
- `(L_P/L)_j` = Share of productive to total employees in sector j (from BLS)
- `(L_j)_NIPA` = Total workers in sector j from NIPA (including self-employed)

**Step 2**: Calculate social security markup

```latex
x_j = \left(\frac{EC}{WS}\right)_j
```

**Where**:
- `EC` = Employee compensation
- `WS` = Wages and salaries
- `x_j` = Markup to account for employer social security contributions

**Step 3**: Calculate variable capital for sector j

```latex
V_j = (w_j \times x_j) \times (L_P)_j
```

**Where**:
- `w_j` = Average weekly wage of productive workers in sector j
- Multiplied by 52 to get annual wage
- Multiplied by `x_j` to include social security
- Multiplied by `(L_P)_j` to get total variable capital

**Step 4**: Sum across all productive sectors

```latex
V = \sum_{j \in Productive} V_j
```

---

## 11. Capital Accumulation Rate

### Formula

```latex
g = \frac{\Delta C}{C}
```

**Where**:
- `g` = Capital accumulation rate (growth rate of capital stock)
- `ΔC` = Change in net fixed capital stock
- `C` = Net fixed capital stock

### Growth Rates (from Table 1)

| Period | ΔC/C (PT) |
|--------|-----------|
| 1948-1965 | 3.28% |
| 1965-1982 | 3.88% |
| 1982-2007 | 2.61% |
| 1964-2007 | 3.17% |

**Paradox of 1965-1982**:
- Net r falling at -6.29% annually
- Yet g = 3.88% (capital still accumulating)
- Explained by: Rising general R, expectations, institutional supports, debt financing

---

## 12. Relationship Between R, RSV, and VCC

### Identity

```latex
R = \frac{S}{C + V} = \frac{S/V}{C/V + 1} = \frac{RSV}{VCC + 1}
```

**Taking logs and differentiating**:

```latex
\frac{dR}{dt} / R = \frac{dRSV}{dt} / RSV - \frac{d(VCC)}{dt} / (VCC + 1)
```

**Approximate growth rate**:

```latex
\hat{R} \approx \hat{RSV} - \frac{VCC}{VCC + 1} \cdot \hat{VCC}
```

**Where** ˆ denotes percentage change.

**Interpretation**:
- R grows with RSV
- R falls with VCC
- Weight on VCC depends on level of VCC

### Empirical Application (1982-2007)

From Table 1:
- RSV growth: 1.64%
- VCC growth: 0.56%
- VCC/(VCC+1) ≈ 6.5/7.5 ≈ 0.87
- Predicted R growth: 1.64% - 0.87×0.56% ≈ 1.15%
- Actual R growth: 1.08%
- Close match!

---

## 13. Unproductive Labor Share

### Formulas (from Figure 1 data)

**Unproductive wage share**:

```latex
UWS = \frac{W_{UP}}{W_{Total}} = \frac{UnproductiveWages}{TotalWages}
```

- 1963: 0.51
- 2007: 0.66
- Growth: 15 percentage points

**Unproductive employment share**:

```latex
UES = \frac{L_{UP}}{L_{Total}} = \frac{UnproductiveEmployment}{TotalEmployment}
```

- 1963: 0.43
- 2007: 0.50
- Growth: 7 percentage points (plateaus after 1990)

### Implication

**Average wage ratio**:

```latex
\frac{w_{UP}}{w_P} = \frac{UWS / UES}{(1-UWS) / (1-UES)}
```

- 1963: (0.51/0.43) / (0.49/0.57) = 1.19/0.86 ≈ 1.38
- 2007: (0.66/0.50) / (0.34/0.50) = 1.32/0.68 ≈ 1.94

**Unproductive workers earn ~40% more (1963) to 94% more (2007) than productive workers**

---

## 14. Share of Unproductive Activities in Surplus Value

### Formula

```latex
\frac{UnproductiveActivities}{S} = \frac{S - \pi}{S} = 1 - \frac{\pi}{S}
```

### Empirical Trend (from Figure 2)

| Year | S (approx.) | π (approx.) | UnprodShare |
|------|-------------|-------------|-------------|
| 1963 | $500B | $250B | 50% |
| 1980 | $2000B | $600B | 70% |
| 2007 | $8500B | $1000B | 88% |

**Interpretation**: By 2007, unproductive activities absorb 88% of total surplus value!

---

## Summary of Key Formulas

| Variable | Formula | Page |
|----------|---------|------|
| RSV | (MVA - V) / V = (y/w_P)(P_GDP/P_CPI) - 1 | 220 |
| General R | S / (C + V) | 224 |
| Net r | NetProfits / C | 224 |
| VCC | C / V | 223 |
| Productivity | (MVA/P_GDP) / L_P | 219-220 |
| Crisis Condition | Δπ/ΔC = 0 ⟺ ε_r,C = -1 | 226-227 |
| Variable Capital | Σ_j (w_j × x_j × L_P,j) | 231 |

---

## Cross-References to Shaikh & Tonak (1994)

**Methodological Consistency**:
- All formulas follow S&T framework
- Extensions: Better data (NAICS vs. SIC), longer series (through 2007)
- Refinements: More accurate productive employment estimates

**Key Differences**:
- PT estimates 13.3% more productive workers than ST
- PT productivity estimates ~0.05% lower MVA than ST
- PT shows sharper 1965-1982 productivity slowdown
- PT rate of surplus value higher (ST overestimated V in productive services)

---

**Extraction Status**: All core formulas documented with LaTeX notation, derivations, empirical applications, and cross-references.
