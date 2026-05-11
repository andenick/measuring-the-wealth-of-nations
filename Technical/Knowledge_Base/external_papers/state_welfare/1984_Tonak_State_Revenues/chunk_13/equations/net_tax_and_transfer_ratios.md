# Equations - Chunk_13: Net Tax and Transfer Ratios

**Source**: Tonak, E. A. (1984). Chapter IV: "State in Distribution Process"
**Extraction Date**: October 23, 2025
**Section**: Final NSW calculation and surplus value adjustment (pages 108-117)
**Chunk**: chunk_13

---

## Core Net-Tax Formula (Refined)

### Definition (Page 110)

**Quoted from text**:
> "Net tax was defined as 'taxes paid minus benefits and income received' and is applicable both to labor and non-labor."

### Formula: Net-Tax for Labor

```latex
NetTax_{Labor} = Taxes_{Labor} - Benefits_{Labor}
```

**Where**:
- `Taxes_Labor` = Total taxes paid by labor (from Table V/X, column 1)
- `Benefits_Labor` = Benefits and income received by labor (from Table IX/X, column 2)
- `NetTax_Labor` = Net fiscal transfer (Table X, column 3)

**Sign Convention**:
- **Positive NetTax**: Labor pays more than receives → **Labor subsidizes state and non-labor**
- **Negative NetTax**: Labor receives more than pays → State subsidizes labor
- **Zero NetTax**: Break-even (fiscal neutrality)

---

## Empirical Finding (Page 111)

**Quoted from text**:
> "Net labor taxes, all through the years 1952-1980, were positive, except for 1975. **In other words, employed workers paid more in taxes than they received in benefits or income from the State.**"

### Key Insight

```latex
NetTax_{Labor,t} > 0 \quad \text{for } t \in [1952, 1980] \setminus \{1975\}
```

**Interpretation**: For 28 out of 29 years, workers experienced a **net income transfer FROM labor TO non-labor**.

---

## Transfer Ratio (Standard)

### Formula (Page 111)

**Quoted from text**:
> "Another way of looking at this empirical evidence concerning the performance or the very existence of a welfare state is to construct a ratio of benefits and income received to taxes paid (by employed labor) which I call the transfer-ratio."

```latex
TransferRatio_t = \frac{Benefits_{Employed,t}}{Taxes_{Employed,t}}
```

**Where**:
- `Benefits_Employed` = Benefits and income received by employed labor (Table XI, column 1)
- `Taxes_Employed` = Taxes paid by employed labor (Table XI, column 2)

### Interpretation

```latex
\begin{cases}
TR < 1 & \text{Workers pay more than receive (net-tax)} \\
TR = 1 & \text{Break-even (fiscal neutrality)} \\
TR > 1 & \text{Workers receive more than pay (net benefit)}
\end{cases}
```

### Empirical Result (Page 111)

**Quoted from text**:
> "The progression of that ratio is presented in the table and the graph on the pages 114 and 115. The same phenomenon as manifested by the movement of net labor taxes now becomes more apparent in the value of the transfer-ratio throughout the period of 1952-1980, – **always less than one**, except 1975."

```latex
TransferRatio_t < 1 \quad \text{for } t \in [1952, 1980] \setminus \{1975\}
```

---

## Welfare-Adjusted Transfer Ratio

### Motivation (Page 116)

**Quoted from text**:
> "In order to be able to compare benefits and income received by employed labor with benefits and income received by employed, umemployed and other members of the labor force, another welfare adjusted-transfer-ratio is constructed."

### Calculation Procedure (Pages 116-117)

**Step 1**: Add welfare to employed labor benefits

```latex
WelfareAdjustedBenefits = Benefits_{Employed} + Welfare_{Services}
```

Where `Welfare_Services` = "welfare and social services" expenditures (Table XI, column 4)

**Step 2**: Calculate welfare-adjusted transfer ratio

```latex
WATR_t = \frac{Benefits_{Employed,t} + Welfare_{t}}{Taxes_{Employed,t}}
```

**Data Source**: Table XI, column 6

### Alternative Notation

From Table XI structure:

```latex
WATR = \frac{\text{Col. 1} + \text{Col. 4}}{\text{Col. 2}}
```

Or equivalently:

```latex
WATR = \frac{\text{Col. 5}}{\text{Col. 2}}
```

Where Column 5 = "Welfare-adjusted Benefits & Income Received by Labor as a Whole"

---

## Comparison: Transfer Ratio vs. Welfare-Adjusted Transfer Ratio

### Relationship

```latex
WATR_t \geq TR_t \quad \forall t
```

**Always true** because welfare expenditures are non-negative.

### Gap Interpretation

```latex
Gap_t = WATR_t - TR_t = \frac{Welfare_t}{Taxes_{Employed,t}}
```

**Meaning**: The gap represents the welfare component (benefits to unemployed and non-employed workers) as a share of taxes paid by employed workers.

---

## Empirical Finding: Welfare-Adjusted Ratio (Page 116)

**Quoted from text**:
> "As can be seen from Table XI and Figure II, although the latter ratio itself is naturally of the 'success' of the U.S. welfare state vis a vis the working class has not changed considerably. Excluding welfare and social services and looking only from the point of view of employed labor, worke±s have received from the State, only once (in 1975) more than what they have already paid to it throughout the period 1952-1980."

### When WATR > 1 (Page 116)

**Quoted from text**:
> "On the other hand, in the context of welfare-adjusted-transfer-ratio, which includes welfare and social services, and takes the entire working class into consideration, workers received a net trnasfer from the State in 1971, 1974, 1975, 1976, 1977, 1978, and 1980 during the same period under study."

```latex
WATR_t > 1 \quad \text{for } t \in \{1971, 1974, 1975, 1976, 1977, 1978, 1980\}
```

**That's only 7 years out of 29!**

---

## Rate of Surplus Value Adjustment

### Section IV.C: The State and the Rate of Surplus-Value (Page 117)

**Quoted from text**:
> "Net labor-tax, as a concept, presents a quantified measure of the role of the State vis-=a-vis labor as a class, at the level of redistribution of value."

### Impact on Variable Capital

**Concept**: Net-tax paid by workers **reduces** their variable capital (consumption fund).

```latex
v_{adjusted} = v_{nominal} - NetTax_{ProductiveWorkers}
```

**Where**:
- `v_nominal` = Employee compensation (wage bill)
- `NetTax_ProductiveWorkers` = Net-tax paid specifically by productive workers
- `v_adjusted` = Effective variable capital after state redistribution

### Impact on Surplus Value

**Concept**: Net-tax increases capitalists' surplus value by reducing workers' consumption.

```latex
s_{adjusted} = s_{nominal} + NetTax_{ProductiveWorkers}
```

**Where**:
- `s_nominal` = Surplus value before state redistribution
- `s_adjusted` = Surplus value after accounting for state's role

### Adjusted Rate of Surplus Value

```latex
\frac{s'}{v'} = \frac{s_{nominal} + NetTax_{ProductiveWorkers}}{v_{nominal} - NetTax_{ProductiveWorkers}}
```

**Compared to nominal rate**:

```latex
\frac{s_{nominal}}{v_{nominal}}
```

### Inequality Result (Page 117)

**Quoted from text**:
> "In other words, as long as a portion of net labor tax comes out of the wage bill of productive workers, calculated before State redistributive acitivities, a new adjusted, effective and reduced variable capital will result: hence increased surplus-value and increased after-state, adjusted rate of surplus value."

**Mathematical Expression**:

```latex
\frac{s_{adjusted}}{v_{adjusted}} > \frac{s_{nominal}}{v_{nominal}} \quad \text{if } NetTax_{ProductiveWorkers} > 0
```

### U.S. Empirical Finding (Page 117)

**Quoted from text**:
> "This has been the case in the U.S. since 1952: redistributive activities of the..."

```latex
\frac{s'_{1952-1980}}{v'_{1952-1980}} > \frac{s_{1952-1980}}{v_{1952-1980}}
```

**Interpretation**: The state's redistributive activities have **increased** the rate of surplus value extraction throughout the entire 1952-1980 period.

---

## Benefit Allocation Formulas (Pages 108-109)

### Income Support Categories

**Social Security and Unemployment** (Page 109):

**Quoted from text**:
> "These items are treated completely as labor income since 'they do represent a reflux of forced savings out of past labor income' (Shaikh, 1980, p. 37) in order to make both retirement and unemployment financially feasible for the capitalist state."

```latex
Benefits_{SocialSecurity} \to Labor_{100\%}
```

```latex
Benefits_{Unemployment} \to Labor_{100\%}
```

**Rationale**: These are **deferred wages** (forced savings from past labor income), not state generosity.

### Housing and Community Services (Page 109)

**Quoted from text**:
> "The category of housing and community service is entirely allocated to labor since the workers are the main beneficiaries of these expenditures."

```latex
Benefits_{Housing} \to Labor_{100\%}
```

**Exception** (Page 109):
> "However, the existence of expenses related to the 'Environmental Protection Agency' and to 'water, sewerage and sanitation' at the Federal and State and Local levels respectively will definitely overestimate the labor share in the category of housing and community services and hence underestimate the net tax paid by labor."

```latex
Benefits_{Housing,Actual} = Benefits_{Housing,Reported} - EPA - Sanitation_{Capitalist}
```

**Methodological note**: Tonak acknowledges this creates a **conservative bias** (understates net-tax paid by labor).

### Transportation (Page 109)

**Quoted from text**:
> "The category of transportation is allocated to the labor and non-labor segments by using both passenger cars' gas consumption" and the 'share of labor income in adjusted personal income' as proxies."

```latex
Benefits_{Transportation} = Benefits_{Transport,Total} \times AllocationFactor
```

Where:

```latex
AllocationFactor = f(GasConsumption_{Passenger}, LaborShare)
```

**Rationale**: Both workers (commuting) and businesses (freight) use transportation infrastructure.

### Economic Development & Labor Training (Page 109)

**Economic Development** (excluded from labor):

**Quoted from text**:
> "Both, the category of economic development, regulation and services and labor training and services re excluded from labor income and consumption: the first category is comprised of expenditures directed mainly toward small businesses or other administrative activities and can hardly be considered a part of labor income of consumption"

```latex
Benefits_{EconDev} \to \text{Excluded or Non-Labor}
```

**Labor Training** (allocated to labor):

**Quoted from text**:
> "the second category, on the other hand can be perceived as various activities of the state, which are entirely received by workers, and hence is treated as part of labor consumption or income."

```latex
Benefits_{LaborTraining} \to Labor_{100\%}
```

### Commercial Activities (Page 110)

**Government Lotteries and Parimutuels**:

**Quoted from text**:
> "The last category, commercial activities, which has been negative throughout 1952-1980, although listed as one of the government expenditure items, is not treated as such. Rather, one of the components of this category, 'government-administered lotteries and parimutuels' is considered as a kind of tax attributable totally to workers."

```latex
Tax_{Lotteries} = -CommercialActivities_{Lotteries} \to Labor_{100\%}
```

**Rationale**: Negative expenditure = revenue source; lotteries are effectively a **regressive tax** on workers.

**Other Commercial Activities**:

**Quoted from text**:
> "The rest of the 'commercial activities', 'publicly-owned liquor store systems' and 'others', which include parking areas and miscellaneous commercial activities, are regular government enterprises and they, after netted, are treated as a part of surplus-value like all other government enterprises."

```latex
Benefits_{CommercialOther} \to SurplusValue
```

---

## Summary of Key Formulas

| Formula | Expression | Source | Purpose |
|---------|-----------|--------|---------|
| Net-Tax | `NetTax = Taxes - Benefits` | Page 110 | Core concept |
| Transfer Ratio | `TR = Benefits/Taxes` | Page 111, Table XI col. 3 | Employed labor only |
| Welfare-Adjusted TR | `WATR = (Benefits + Welfare)/Taxes` | Page 116, Table XI col. 6 | All labor |
| Adjusted Variable Capital | `v' = v - NetTax_Productive` | Page 117 | Production analysis |
| Adjusted Surplus Value | `s' = s + NetTax_Productive` | Page 117 | Exploitation rate |
| Adjusted Rate of s/v | `s'/v' = (s + NT)/(v - NT)` | Page 117 | State's role in exploitation |

---

## Methodological Principles

### 1. Net-Tax Sign Convention

```latex
\begin{align}
NetTax > 0 &\implies \text{Labor subsidizes state/non-labor} \\
NetTax < 0 &\implies \text{State subsidizes labor} \\
NetTax = 0 &\implies \text{Fiscal neutrality}
\end{align}
```

### 2. Transfer Ratio Threshold

```latex
\begin{align}
TR < 1 &\equiv NetTax > 0 \\
TR = 1 &\equiv NetTax = 0 \\
TR > 1 &\equiv NetTax < 0
\end{align}
```

### 3. Conservative Bias

Multiple allocation decisions **understate** net-tax paid by labor:
- EPA and sanitation costs in housing category
- Employer-focused economic development
- Faux frais categories fully excluded

**Result**:

```latex
NetTax_{Reported} \leq NetTax_{Actual}
```

Tonak's estimates are **lower bounds** on net-tax paid by workers.

---

## Cross-References

- **Chunk_09**: Net-tax concept definition and Type I incidence
- **Chunk_10-12**: Tax and expenditure allocation methodology
- **Table IX** (page 112): Total benefits and labor portion
- **Table X** (page 113): Net-tax values 1952-1980
- **Table XI** (page 114): Transfer ratios calculated
- **Figure 2** (page 115): Visual representation of ratios
- **Upcoming Tables XII-XIII**: Productive worker analysis and surplus value rates

---

**Extraction Status**: Complete. All equations and formulas from chunk_13 documented with LaTeX notation, context, and interpretation.
