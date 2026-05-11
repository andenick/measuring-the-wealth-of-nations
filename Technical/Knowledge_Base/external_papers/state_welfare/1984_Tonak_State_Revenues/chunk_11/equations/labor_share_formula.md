# Equations - Chunk_11: Labor Share Calculation

**Source**: Tonak, E. A. (1984). Chapter IV: "State in Distribution Process"
**Extraction Date**: October 23, 2025
**Section**: Labor share methodology (pages 88-97)
**Chunk**: chunk_11

---

## Labor Share Formula (Table II)

### Equation: Labor Share

```latex
LS = \frac{TotalLaborIncome}{AdjustedPersonalIncome}
```

**Expanded**:

```latex
LS = \frac{TotalLaborIncome}{PersonalIncome - ImputedIncome}
```

**Where**:
- `LS` = Labor Share (ratio, typically 0.71-0.74 for 1952-1980)
- `TotalLaborIncome` = Wage and salary disbursement + Other labor income
- `PersonalIncome` = Total personal income from NIPA
- `ImputedIncome` = Imputed income items (imputed rent, imputed interest, etc.)
- `AdjustedPersonalIncome` = Personal Income minus Imputed Income

**Data Sources** (from Table II footnotes):
- Total Labor Income: NIPA Table 2-1, line 2 = line 8
- Personal Income: NIPA Table 2-1, line 1
- Imputed Income: NIPA Table 8-3, line 5

**Example Calculation (1980)**:
```
LS = 1483.370 / (2160.401 - 59.299)
LS = 1483.370 / 2101.10
LS = 0.71 (71%)
```

---

## Weisskopf's Alternative Labor Share (Table III)

### Equation: Weisskopf Labor Share

```latex
LS_{Weisskopf} = \frac{FederalIncomeTaxOnWages}{TotalFederalIncomeTax}
```

**Where**:
- `LS_Weisskopf` = Weisskopf's estimate of labor share
- `FederalIncomeTaxOnWages` = Federal income taxes paid on wage and salary income (from IRS data)
- `TotalFederalIncomeTax` = Total federal income tax revenue

**Example Calculation (1979)**:
```
LS_Weisskopf = 176637.1 / 224844
LS_Weisskopf = 0.79 (79%)
```

**Comparison**:
- Tonak (1979): 0.71
- Weisskopf (1979): 0.79
- Difference: +0.08 (Weisskopf's estimate 8 percentage points higher)

**Implication**: Tonak's method is more conservative, meaning his estimates of taxes paid by labor are unlikely to be overstated.

---

## Tax Allocation Formulas (Table IV Implementation)

### Equation: Taxes Paid by Labor (Mixed Taxes)

For taxes that cannot be directly attributed, labor's share is:

```latex
TaxesPaidByLabor_{i} = TotalTax_{i} \times LS
```

**Where**:
- `i` = Tax category (income tax, property tax, indirect business tax, etc.)
- `TotalTax_i` = Total revenue from tax category i
- `LS` = Labor Share from Table II

**Example: Income Tax Allocation (1980)**:
```
Income Tax Paid by Labor = Total Income Tax × LS
= 298.333 × 0.71
= 211.82 billion
```

### Equation: Taxes Paid by Non-Labor (Mixed Taxes)

```latex
TaxesPaidByNonLabor_{i} = TotalTax_{i} \times (1 - LS)
```

**Example: Income Tax Allocation (1980)**:
```
Income Tax Paid by Non-Labor = Total Income Tax × (1 - LS)
= 298.333 × (1 - 0.71)
= 298.333 × 0.29
= 86.52 billion
```

---

## Direct Allocation (No Formula Needed)

### T₁ (Direct Labor Taxes)

Allocated 100% to labor:
- Contributions for Social Insurance (payroll taxes)
- Government Lotteries and Parimutuels (page 96 justification)

```latex
TaxesPaidByLabor_{DirectLabor} = TotalTax_{T1}
```

### T₃ (Direct Capital Taxes)

Allocated 100% to non-labor:
- Corporate Profit Taxes
- Estate and Gift Taxes

```latex
TaxesPaidByNonLabor_{DirectCapital} = TotalTax_{T3}
```

---

## Total Tax Burden Calculation

### Equation: Total Taxes Paid by Labor

```latex
TotalTaxesByLabor = \sum T_{1} + LS \times \sum T_{2}
```

**Where**:
- `∑T₁` = Sum of all direct labor taxes
- `∑T₂` = Sum of all mixed taxes
- `LS` = Labor Share

### Equation: Total Taxes Paid by Non-Labor

```latex
TotalTaxesByNonLabor = \sum T_{3} + (1 - LS) \times \sum T_{2}
```

**Where**:
- `∑T₃` = Sum of all direct capital taxes

---

## Labor Share as Percentage of Total Taxes (Validation)

### Equation: Labor's Share of Total Tax Burden

```latex
LaborTaxShare = \frac{TotalTaxesByLabor}{TotalTaxRevenue}
```

**Empirical Results**:
- 1952: Labor pays ~60% of total taxes (despite LS = 73%)
- 1980: Labor pays ~60% of total taxes (despite LS = 71%)

**Interpretation**: The tax system is mildly progressive - labor's share of taxes (~60%) is less than labor's share of income (~72%).

---

## Property Tax Correction (NIPA Adjustment)

### Equation: Property Tax Allocation

**NIPA Framework (incorrect)**:
- Treats all property taxes on owner-occupied homes as "indirect business taxes"
- Allocates to non-labor income

**Tonak's Correction**:
```latex
PropertyTaxByLabor = HomeownerPropertyTax + (BusinessPropertyTax \times LS)
```

**Where**:
- `HomeownerPropertyTax` ≈ 50% of total property taxes (paid by individuals)
- `BusinessPropertyTax` ≈ 50% of total property taxes (paid by firms)

**Result**: More accurate allocation that recognizes homeowners as workers, not businesses.

---

## Summary of Key Formulas

| Formula | Expression | Purpose |
|---------|-----------|---------|
| Labor Share | `TLI / (PI - II)` | Core allocation coefficient |
| Mixed Tax to Labor | `Tax × LS` | Allocate taxes by income share |
| Mixed Tax to Non-Labor | `Tax × (1 - LS)` | Residual to capital |
| Total Labor Taxes | `∑T₁ + LS × ∑T₂` | Aggregate labor's tax burden |
| Total Non-Labor Taxes | `∑T₃ + (1 - LS) × ∑T₂` | Aggregate capital's tax burden |

---

**Cross-References**:
- **Table II** (page 92): Empirical labor share calculations 1952-1980
- **Table III** (page 93): Validation against Weisskopf estimates
- **Table IV** (page 95): Application to tax allocation
- **Chunk_09 equations**: Net-tax = Taxes - Benefits (uses these tax allocations)

---

**Methodological Significance**: Labor share is the **critical coefficient** that allows Tonak to move from observable aggregates (total taxes, total expenditures) to class-specific allocations (taxes paid by labor vs. capital). The robustness checks in Table III validate this approach.
