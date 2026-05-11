# Equations and Methodology - Chunk_10 (Pages 78-87)

**Source**: Tonak, E. A. (1984). Chapter IV: "State in Distribution Process"
**Extraction Date**: October 23, 2025
**Section Focus**: Phases IV-VI completion and tax category methodology (pages 78-87)
**Chunk**: chunk_10

---

## No New Formal Equations

This chunk (pages 78-87) does not introduce new formal equations beyond those already documented in chunk_09. Instead, it provides:

1. **Figure I** (page 78): Visual representation of the six-phase framework
2. **Phases IV-VI descriptions** (pages 79-80): Narrative completion of the framework
3. **Section B**: Detailed taxonomy of the 9 tax categories (pages 80-87)
4. **Historical context** for each tax type

---

## Phase Descriptions (Completion from Page 79)

### Phase IV: Government Expenditures Allocation

**Description** (page 79):
> "In this phase government expertiudres are allocated to labor and non-labor, based on some assumptions regarding their content and intermediary calculations, obtaining each segment's share. The procedure itself will be outlined in the next section and details will be presented in Appendix II."

**Implicit Formula**:
```
Benefits to Labor (E) = E₁ + E₂ × LS
Benefits to Non-Labor = E₃ + E₂ × (1 - LS)
```

Where:
- E₁ = Expenditures unambiguously benefiting labor
- E₂ = Mixed expenditures (allocated by labor share)
- E₃ = Expenditures unambiguously benefiting capital
- LS = Labor Share

---

### Phase V: Net-Tax Derivation

**Description** (page 79):
> "This step allows us to develop the concept of 'net-tax' both for labor and non-labor, based on Phase II and IV findings, i.e., taxes paid and benefits and income received. The net-tax category is obtained by subtracting benefits and income from taxes."

**Formula** (from chunk_09, reinforced here):
```latex
NetTax = Taxes - Benefits
```

For labor:
```latex
NetTax_{Labor} = (T₁ + T₂ × LS) - (E₁ + E₂ × LS)
```

Rearranging:
```latex
NetTax_{Labor} = (T₁ - E₁) + LS × (T₂ - E₂)
```

---

### Phase VI: After-Net-Tax Income

**Description** (page 80):
> "Depending upon the magnitude and sign of the net-taxes, after-tax incomes are now adjusted and after-benefits incomes obtained. These last adjusted income categories then allow us to get a more accurate picture of the State's distributive effect on labor."

**Formulas**:

For labor:
```latex
AfterNetTaxIncome_{Labor} = AfterTaxIncome_{Labor} + Benefits_{Labor}
```

Or equivalently:
```latex
AfterNetTaxIncome_{Labor} = GLI - NetTax_{Labor}
```

For non-labor:
```latex
AfterNetTaxIncome_{NonLabor} = GNLI - NetTax_{NonLabor}
```

---

## Taxonomy of Tax Categories

### Nine Tax Categories (Page 80)

Federal, state, and local taxes broken into **nine categories**:

1. Personal Income Taxes
2. Contributions for Social Insurance (Payroll Taxes)
3. Corporate Profit Taxes
4. Estate and Gift Taxes
5. Personal Non-taxes and Other Taxes
6. Motor Vehicle Licenses
7. Indirect Business Taxes
8. Property Taxes
9. Surpluses from Government-administered Lotteries and Parimutuels

---

## Tax Allocation Methodology (Implicit Framework)

### Direct Allocation (T₁ and T₃)

Some taxes are **unambiguously** allocated:
- **T₁ (Direct Labor Taxes)**: Personal income taxes on wages, payroll taxes (both employee and employer portions)
- **T₃ (Direct Capital Taxes)**: Corporate profit taxes, estate and gift taxes on large estates

### Mixed Allocation (T₂)

Some taxes require **intermediary assumptions**:
- **Property Taxes**: Split based on homeownership (~50% labor) vs. business property (~50% capital)
- **Indirect Business Taxes**: Corrected for NIPA's treatment of homeowners as businesses
- **Motor Vehicle Licenses**: Allocated based on personal vs. commercial vehicle ownership

### Allocation by Labor Share

For truly mixed taxes where direct allocation is impossible:
```latex
Labor's Share of Tax_{i} = Total Tax_{i} × LS
```

Where LS = Labor Share (employee compensation / total personal income)

---

## Key Methodological Points

### 1. NIPA Correction (Page 77, chunk_09; reinforced page 85, chunk_10)

**Problem**: NIPA treats homeowners as "individual capitalist firms" renting to themselves.

**Impact**:
- Property taxes on owner-occupied homes (~50% of total property taxes) are incorrectly classified as "indirect business taxes"
- This **overestimates** Gross Non-Labor Income
- This **underestimates** Gross Labor Income

**Solution** (Phase II):
Reallocate property taxes based on actual incidence (homeowners vs. businesses).

### 2. Payroll Tax Incidence (Page 82)

**Both sides counted as labor taxes**:
- Employee contributions for Social Insurance
- Employer contributions for Social Insurance

**Rationale** (from Hyman 1983, Musgrave & Musgrave 1980):
Employer-side payroll taxes are part of the cost of hiring workers. Economic incidence falls on labor through reduced wages, even though legal incidence is on employers.

**Quote** (page 82):
> "Taken by itself, this tax is regressive (i.e., the ratio of tax revenue to income falls as we move up the income scales) over the middle to-upper income ranges." (Musgrave and Musgrave, 1980, p. 331)

### 3. Corporate Tax Incidence (Page 82-83)

**Effective vs. Nominal Rates** (Page 83, citing Hyman 1983):
> "...after considering all the loopholes, effective rates averaged about 30% while the marginal effective tax rates for all corporations are estimated to 34.4%" (Hyman, 1983, pp. 535-6)

**Declining Share**:
Corporate profit tax fell from 22% of total revenue (1952) to 10% (1980), reflecting favorable tax treatment through:
- Accelerated depreciation
- Capital consumption allowances
- Investment tax credits

---

## Historical Tax Data (1952-1980)

### Income Tax Evolution (Pages 81-82)

**Federal Level**:
- 1920s: 60% of federal revenue
- 1927: 25.6% of federal revenue
- 1940: 16.9% of federal revenue
- 1980: 46% of federal revenue

**State and Local Level**:
- First instituted: 1911 (Wisconsin)
- 1960s: 6.3% of state and local revenues
- 1966: Approximately 11%
- 1980: Approximately 11%

**Stability**: Income tax as share of total revenue has been "generally fluctuating around 30-35 percent" since 1952 (page 82).

### Payroll Tax Growth (Page 82)

**Evolution**:
- Instituted: Social Security Act of 1935
- 1952: 10% of total tax revenue
- 1980: 24% of total tax revenue

**Rate Progression**:
- 1980: 6.13% each (employee and employer)
- 1990 (scheduled): 7.65%

**Implication**: Payroll taxes are the **second largest** component (after income tax) and are **regressive**.

### Property Tax Trends (Page 86)

**Federal Level**: 18.2% of total indirect business tax (1980)
- Sales taxes: 38.9%
- Property taxes: 32.1%
- Other: 10.8%

**State and Local Level**:
- 1980: ~2% of total property taxes (personal property tax)
- Remaining 89%: Rental homes (50%), business property (43%), utility real estate (5%)

**Overall Trend**: Property taxes declined from 9.6% (1952) to 8.3% (1980) as share of total tax revenue.

---

## Tax Structure Summary (Page 86)

**Pro-Corporate Bias** (page 86):
> "Still, even a cursory glance at the tax structure reveals the pro-corporate bias in the taxation policies pursued by the state."

**Evidence**:
- Corporate income tax share: 22% (1952) → 10% (1980) [55% decline]
- Social insurance (payroll) tax share: 10% (1952) → 24% (1980) [140% increase]

**Implication**: Tax burden shifted from capital to labor over the 1952-1980 period.

---

## Cross-References

- **Core Equations**: See `chunk_09/equations/net_tax_equations.md` for formal mathematical framework
- **Figure I**: See `figures/figure_1_description.md` for visual representation of six-phase derivation
- **Detailed Calculations**: Appendix I (pages 162+) will contain full allocation methodology
- **Empirical Tables**: Expected in chunks 11-13 (pages 88-120)

---

**Methodological Status**: This chunk completes the **conceptual framework** for net-tax calculation. The next sections will present the empirical results in tabular form.
