# [1984] Tonak - State Revenues - Chunk 05 - Equations

**Extraction Date:** October 23, 2025
**Chunk Coverage:** Pages 28-37 (Chapter III: Productive and Unproductive Labor)
**Total Equations:** 0

---

## Summary

**No formal equations appear in chunk_05.**

This chunk establishes the **theoretical basis** for equations that will appear in later chapters. While no mathematical formulations are present, the text describes several **conceptual relationships** that will be quantified.

---

## Conceptual Frameworks for Future Equations

### 1. Rate of Surplus-Value (Page 33)

**Theoretical statement:**
> "Regarding the calculation of the rate of surplus-value, the distinction between PUPL also plays a crucial role. Since the rate of surplus-value is the ratio of surplus-value to variable capital, its components do not directly correspond to those categories such as profit and wage, in the NIPA framework."

**Components defined:**
- **Surplus-value (S)**: Not equivalent to NIPA profit
- **Variable capital (V)**: Not equivalent to NIPA wages

**Marxian terminology consists of** (Page 34):
- Money-forms of surplus-value: **rent** and **interest**
- **Wages of unproductive laborers**
- **Wages of productive workers** (= variable capital V)

**Fundamental equation** (to be formalized in Chapter IV):

$$e' = \frac{S}{V}$$

Where:
- $e'$ = rate of surplus-value
- $S$ = surplus-value (total value created by productive labor minus wages)
- $V$ = variable capital (wages of productive workers only)

**Critical distinction:**

NIPA framework uses:
$$\text{Profit rate} = \frac{\text{Profit}}{\text{Total Capital}}$$

Where profit includes rent, interest, and is calculated from price data.

Marxian framework requires:
$$e' = \frac{S}{V} = \frac{\text{Value created by PL} - \text{Wages of PL}}{\text{Wages of PL}}$$

Where calculations are based on labor-time/value categories.

### 2. Productive Labor Definition (Page 31, 35)

**Theoretical criterion:**
> "PL is the labor that produces surplus-value" (Page 35)

**Formal definition** (Marx, 1973, p. 1048, cited page 31):
> "only the exchange for productive labor can satisfy one of the conditions for the reconversion of surplus-value into capital"

**Implication for calculation:**

To calculate surplus-value correctly, we must:

1. **Identify productive labor** (PL)
2. **Identify unproductive labor** (UPL)
3. **Separate their wages:**
   - $V$ = wages of PL only
   - Wages of UPL = part of surplus-value distribution

**This affects the denominator** of the surplus-value rate:

$$V = \text{Wages}_{\text{productive workers}}$$

**Not:**
$$V \neq \text{Total wage bill}$$

### 3. Accumulation and Unproductive Labor (Page 32)

**Theoretical relationship:**

Yaffe (1973, p. 191) cited:
> "unproductive labor 'constitute(s) a reduction of the surplus-value that is available for reinvestment as capital'"

**Within falling rate of profit framework**, *ceteris paribus*:
> "an increasing tendency of unproductive labor means a decreasing effective rate of profit" (Page 32)

**Implied equations** (to be formalized):

If total surplus-value = $S_{total}$

And unproductive labor wages = $W_{UPL}$

Then **surplus available for accumulation**:

$$S_{available} = S_{total} - W_{UPL}$$

**Effective profit rate** (incorporating UPL):

$$r_{effective} = \frac{S_{total} - W_{UPL}}{C + V}$$

Where:
- $C$ = constant capital
- $V$ = variable capital (productive workers' wages)
- $W_{UPL}$ = wages of unproductive labor (deduction from surplus)

### 4. State Impact on Surplus-Value (Page 29)

**Research question stated:**
> "What does each class pay and what do they receive in return in their relations with the capitalist state?"

**Impact on working class share** (Page 29):
> "both in terms of the new effect of taxation and state expenditures on the share of the working class in total value-added and also in terms of possible changes in the rate of surplus-value due to the state's distributive activities"

**Implied equations for Chapter IV:**

**Without state intervention:**
$$e' = \frac{S}{V}$$

**With state intervention:**
$$e'_{adjusted} = \frac{S + \text{Taxes from workers} - \text{Benefits to workers}}{V}$$

Or alternatively:

$$e'_{adjusted} = \frac{S + \text{Net tax paid by labor}}{V}$$

Where:
$$\text{Net tax} = \text{Taxes}_{labor} - \text{Benefits}_{labor}$$

This is **the core empirical question** of the dissertation.

---

## Definitional Categories for Calculation (Page 36)

**Four fundamental human activities:**

1. **Production** = creation or transformation of use-values
2. **Distribution** = allocation of use-values
3. **Personal consumption** = individual use
4. **Social reproduction and maintenance** = collective reproduction

**For capitalist societies** (Page 37, Table I):
- Production = creation of **values and surplus-values** for exchange
- (Negligible production of use-values remains in some areas)

**Labor classification:**
- **Labor in production sphere** = may be productive or unproductive
- **Labor in distribution sphere** = unproductive by definition
- **Labor in social reproduction** = unproductive by definition

**Equation framework needed** (to be developed in later sections):

For any worker $i$:

$$\text{Classification}_i =
\begin{cases}
\text{Productive} & \text{if activity} \in \text{Production of } S \\
\text{Unproductive} & \text{otherwise}
\end{cases}$$

Then:

$$V = \sum_{i \in \text{Productive}} W_i$$

$$S = \text{Total value created} - V$$

---

## Where Equations Will Appear

Based on this theoretical foundation:

1. **Chapter III (later sections, chunks 08-09):**
   - Circuit of capital equations
   - State revenue/expenditure flows
   - Sub-circuit formulations

2. **Chapter IV (chunks 10-13):**
   - Empirical formulas for tax allocation
   - Benefit distribution calculations
   - Net tax formulas by class
   - Rate of surplus-value (nominal and adjusted)

3. **Appendix III (chunks 18-22):**
   - Detailed computational algorithms
   - NIPA-to-Marxian category conversions
   - Time-series calculation procedures

---

## Key Relationships Established (No Equations Yet)

| **Conceptual Relationship** | **Page** | **Will Be Formalized As** |
|----------------------------|----------|---------------------------|
| Productive labor → surplus-value | 31 | $S = f(\text{PL})$ |
| Unproductive labor → reduction of $S$ | 32 | $S_{net} = S - W_{UPL}$ |
| PUPL distinction → rate of surplus-value | 33-34 | $e' = S / V$ where $V$ = PL wages only |
| State activities → adjusted $e'$ | 29 | $e'_{adj} = (S + \text{Net tax}) / V$ |

---

**See Also:**

- chunk_08_equations.md: Circuit of capital mathematical framework
- chunks_10-13: Chapter IV empirical equations
- chunk_05_full_transcription.md: Complete theoretical discussion

---

**Extraction Notes:**

This chapter establishes **why** certain equations are necessary and **how** variables must be defined. The actual mathematical formulations will appear once the circuit framework is presented and then operationalized with NIPA data.
