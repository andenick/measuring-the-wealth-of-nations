# Equations - Chunk_12: Expenditure Allocation Methodology

**Source**: Tonak, E. A. (1984). Chapter IV: "State in Distribution Process"
**Extraction Date**: October 23, 2025
**Section**: Expenditure classification and allocation (pages 98-107)
**Chunk**: chunk_12

---

## No New Formal Equations

This chunk does not introduce new mathematical equations beyond those already established in chunks 09-11. Instead, it provides:

1. **Complete empirical data** (Tables V-VIII)
2. **Functional classification framework** for expenditures
3. **Allocation logic** for determining which expenditures benefit labor vs. capital

---

## Expenditure Allocation Framework (Conceptual)

### Total Government Expenditures Decomposition

**Implicit Formula** (from pages 100-107):

```
TotalExpenditures = E_excluded + E_1 + E_2 + E_3
```

**Where**:
- `E_excluded` = Expenditures excluded from NSW calculation (defense, veterans, agriculture subsidies, net interest, etc.)
- `E_1` = Direct benefits to labor
- `E_2` = Mixed expenditures (allocated by labor share)
- `E_3` = Direct benefits to capital

---

## Benefit Allocation to Labor

### Formula: Benefits Received by Labor

From chunk_09, applied here:

```latex
BenefitsToLabor = E_1 + E_2 \times LS
```

**Where**:
- `E_1` = Expenditures unambiguously benefiting workers
- `E_2` = Mixed expenditures
- `LS` = Labor Share (from Table II)

### E₁ Categories (Direct Labor Benefits)

Based on functional classification (Table VII-VIII):
- Education (K-12, higher education)
- Health and hospitals
- **Income support, social security, and welfare**
- Housing and community development
- Recreational and cultural activities

### E₂ Categories (Mixed - Allocated by LS)

- Transportation (highways, transit, railroad)
- Postal service
- Economic development programs
- Labor training and services
- Natural resources
- Energy
- Commercial activities (partially)

### E₃ and E_excluded Categories

**Excluded Entirely** (pages 106-107):
1. Central executive, legislative, judicial activities
2. International affairs
3. Space
4. National defense (military)
5. Civilian safety (police, fire, prisons)
6. Veteran benefits and services
7. Agriculture subsidies
8. Net interest paid
9. "Other and unallocable"

**Rationale**: These are either **faux frais** (overhead costs of maintaining capitalism) or direct subsidies to capital, not benefits to workers.

---

## Faux Frais Concept

### Marx's Framework (quoted on page 106)

```
FauxFrais = StateExpendituresForCirculation + StateExpendituresForCoercion
```

**From Marx (1893, p. 420)**:
> "The sum of labor-power and social means of production that is spent in the annual production of gold and silver as instruments of circulation forms a heavy item for faux frais for the capitalist mode of production..."

**Modern Application**:
- Circulation costs: Net interest, commercial activities regulation
- Coercion costs: Military, police, prisons, judicial system
- Administrative costs: Executive, legislative functions

**These are NOT benefits to labor** - they are costs of maintaining the capitalist system.

---

## Government Expenditure Growth Rate (Implicit)

### Average Annual Growth Rate Formula

```latex
AAGR = \left(\frac{Expend_{1980}}{Expend_{1952}}\right)^{\frac{1}{28}} - 1
```

**Calculation** (from Table VI data):
```
AAGR = (872.53 / 94.07)^(1/28) - 1
AAGR = (9.275)^(0.0357) - 1
AAGR ≈ 0.083 = 8.3% annually
```

**Interpretation**: Government expenditures grew at 8.3% per year, outpacing GNP growth, leading to increased government share of economy from 27% to 33% of GNP.

---

## Government Share of Economy

### Ratio Formula (from Table VI)

```latex
GovtShare = \frac{TotalGovtExpenditures}{GNP}
```

**Trend**:
- 1952-1966: Average 27%
- 1967-1980: Average 32%
- Change: +5 percentage points

### Alternative Measure (Mattick's Approach)

**Footnote b** (page 99) presents alternative:

```latex
UnproductiveRatio = \frac{TotalGovtExpenditures}{GNP - TotalGovtExpenditures}
```

**Where** `GNP - TotalGovtExpenditures` = Net productive output

**Trend**:
- 1952: 0.37 (government absorbed 37% of net output)
- 1980: 0.50 (government absorbed 50% of net output)

**Interpretation**: Government's claim on productive resources increased from 37% to 50%, suggesting growing burden of **unproductive activities** on capitalist economy.

---

## Labor's Tax Burden Growth

### Growth Rate Comparison

From Table V data:

**Labor Taxes Growth**:
```
Growth_Labor = (456.39 / 34.58) = 13.2x over 28 years
AAGR_Labor ≈ 9.7% annually
```

**Non-Labor Taxes Growth**:
```
Growth_NonLabor = (382.80 / 55.53) = 6.9x over 28 years
AAGR_NonLabor ≈ 7.2% annually
```

**Key Finding**: Labor's tax burden grew **faster** than non-labor's (9.7% vs 7.2% annually), despite stable labor share of income (~72%).

---

## Proportional Tax Burden Shift

### Labor's Share of Total Taxes Formula

```latex
LaborTaxShare_t = \frac{LaborTaxes_t}{TotalTaxes_t}
```

**Trend**:
- 1952: 34.58 / 90.105 = **38.4%**
- 1960: 59.96 / 139.497 = **43.0%**
- 1970: 151.39 / 302.883 = **50.0%** ← **Crossover**
- 1980: 456.39 / 839.189 = **54.4%**

**Change**: +16 percentage points (from 38% to 54%)

**Interpretation**: Despite earning ~72% of income, labor went from paying 38% of taxes (1952) to 54% of taxes (1980). The tax structure became **less progressive** (or more regressive).

---

## Summary of Key Relationships

| Formula | Expression | Purpose |
|---------|-----------|---------|
| Benefits to Labor | `E₁ + E₂ × LS` | Allocate expenditures |
| Govt Share (Standard) | `GovtExpend / GNP` | Track govt sector growth |
| Govt Share (Mattick) | `GovtExpend / (GNP - GovtExpend)` | Unproductive burden |
| Labor Tax Share | `LaborTax / TotalTax` | Track tax burden shift |
| Faux Frais | `Excluded Expenditures` | Non-benefit overhead |

---

## Methodological Principles

**Two-Part Classification** (page 101):

1. **Activities supporting working class reproduction**
   → Included in benefit calculation
   → Examples: Education, health, income support, housing

2. **Activities reproducing capital/capitalist class**
   → Excluded from benefit calculation
   → Examples: Military, police, agriculture subsidies, net interest

**Rationale**: NSW measures net fiscal transfer **to labor class**, not total government spending. Many government activities serve capital's interests, not workers'.

---

## Cross-References

- **Core NSW Formula** (chunk_09): `NSW = (E₁ + E₂ × LS) - (T₁ + T₂ × LS)`
- **Labor Share** (chunk_11, Table II): LS values for allocation
- **Tax Allocation** (chunk_11, Table IV): Methodology for T₁, T₂
- **Upcoming Table IX**: Will show empirical E₁, E₂ values
- **Upcoming Table X**: Will calculate NSW = E - T

---

**Methodological Significance**: This chunk establishes the **functional classification** needed to distinguish state expenditures that benefit labor from those that don't. This is crucial because total government spending grew substantially, but not all of it benefited workers.
