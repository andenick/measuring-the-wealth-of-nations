# [1984] Tonak - State Revenues - Chunk 06 - Equations

**Extraction Date:** October 23, 2025
**Chunk Coverage:** Pages 38-47 (Chapter III continuation: Marx on PUPL)
**Total Equations:** 0

---

## Summary

**No formal equations appear in chunk_06.**

However, this chunk contains **critical definitional statements** from Marx that will underpin all mathematical formulations in Chapter IV. These are conceptual equations - relationships that must be operationalized.

---

## Conceptual Relationships from Marx's Definitions

### 1. Productive Labor Definition (Pages 44-45)

**Marx's formulation from Resultat:**

> "Productive labor is exchanged directly for money as capital, i.e. for money which is intrinsically capital, which is destined to function as capital. Thus productive labor is labor which for the worker only reproduces the value of his labor-power as determined beforehand, while as a value-creating activity it valorizes capital and confronts the worker with the values so created and transformed into capital." (Marx, 1976, p. 1043)

**Conceptual equation:**

$$\text{Productive Labor} = \text{Labor exchanged with capital that produces surplus-value}$$

**Two necessary conditions:**

a) **Exchange with capital** (not revenue):
$$\text{PL} \Rightarrow \text{Exchanged with } M \text{ where } M \text{ functions as capital}$$

b) **Production of surplus-value**:
$$\text{PL} \Rightarrow \text{Creates } S \text{ (surplus-value)}$$

**Key distinction:**
- Worker reproduces value of labor-power: $V$
- Worker creates additional value (surplus): $S$
- Total value created: $V + S$

### 2. Unproductive Labor Definition (Pages 45-46)

**Marx's formulation from Resultat:**

> "Whenever labor is purchased to be consumed as a use-value, as a service and not to replace the value of variable capital with its own vitality and be incorporated into the capitalist process of production - whenever that happens, labor is not productive and the wage-laborer is no productive worker. His work is consumed for its use-value, not as creating exchange-value; it is consumed unproductively, not productively. Hence the capitalist does not encounter it in his role of capitalist, a representative of capital. The money that he pays for it is revenue, not capital. Its consumption is to be formulated not as M-C-M, but C-M-C (the last being the labor or service itself)." (Marx, 1976, p. 1041)

**Conceptual equation:**

$$\text{Unproductive Labor} = \text{Labor purchased as use-value/service (from revenue)}$$

**Circuit representation:**

**Productive Labor circuit:**
$$M - C \{LP, MP\} - M'$$

Where:
- $M$ = money functioning as capital
- $C$ = commodities (labor-power LP, means of production MP)
- $M'$ = money + surplus-value ($M' = M + \Delta M$)

**Unproductive Labor circuit:**
$$C - M - C'$$

Where:
- $C$ = commodity (capitalist's consumption fund or revenue)
- $M$ = money (revenue, not capital)
- $C'$ = labor or service consumed

**Fundamental difference:**
- PL circuit: $M < M'$ (value expansion)
- UPL circuit: $C \rightarrow C'$ (exchange of equivalents, no surplus-value)

### 3. Revenue vs. Capital Distinction (Page 46)

**Critical statement:**

> "The money that he pays for it is **revenue**, not **capital**. Its consumption is to be formulated not as M-C-M, but C-M-C"

**Implication for classification:**

If labor expenditure is paid from **revenue**:
$$\text{Labor} \in \text{UPL}$$

If labor expenditure is paid from **capital**:
$$\text{Labor} \in \text{PL (potentially)}$$

**But this is necessary, not sufficient:**

Being exchanged with capital is **one of two necessary conditions** (page 46):
> "Being exchanged with capital is only **one of two necessary conditions**, of which the other is the fact that labor engages in the production of surplus-value."

### 4. Surplus-Value Production Criterion (Pages 45-46)

**From Marx (1976, p. 1038):**

> "Since the immediate purpose and the authentic product of capitalist production is surplus-value, labor is only productive, and an exponent of labor-power is only a productive worker, if it or he creates surplus-value directly, i.e. the only productive labor is that which is directly consumed in the course of production for the valorization of capital."

**Formal criterion:**

$$\text{PL} \iff \begin{cases}
\text{Exchanged with capital} \\
\text{AND} \\
\text{Creates surplus-value directly}
\end{cases}$$

**Mathematical representation:**

For worker $i$ engaged in activity $a$:

$$\text{Classification}_i = \begin{cases}
\text{Productive} & \text{if } a \text{ produces } S \text{ AND exchanged with capital} \\
\text{Unproductive} & \text{otherwise}
\end{cases}$$

### 5. Value-Creating vs. Value-Transferring (Page 44)

**Marx's distinction in M-C phase:**

In M-C ... P ... C'-M', during production (P):

- Labor-power creates **new value**: $V + S$
- Means of production transfer **existing value**: $C$ (constant capital)

**Value created:**

$$\text{New value} = V + S$$

**Value transferred:**

$$\text{Transferred value} = C$$

**Total commodity value:**

$$W = C + V + S$$

**Only labor that creates new value** can be productive:
> "objectifies itself directly during the labor process as a fluid quantum of value" (Marx, 1973, p. 1040)

---

## Implications for Quantification (Chapter IV)

### A. Classification Algorithm

Based on Marx's criteria, Chapter IV will need:

**Step 1:** Identify if labor is exchanged with capital or revenue
$$\text{If revenue} \Rightarrow \text{UPL (stop)}$$

**Step 2:** If exchanged with capital, determine if it produces surplus-value
$$\text{If produces } S \Rightarrow \text{PL}$$
$$\text{If does not produce } S \Rightarrow \text{UPL}$$

### B. Variable Capital Calculation

$$V = \sum_{i \in \text{PL}} W_i$$

Where $W_i$ = wages of productive worker $i$

**NOT:**
$$V \neq \sum_{j \in \text{All workers}} W_j$$

### C. Surplus-Value Calculation

$$S = \text{Total value created} - V$$

Where total value created includes:
- Rent
- Interest
- Profit
- Wages of unproductive workers

**In Marxian categories:**

$$S = \text{Rent} + \text{Interest} + \text{Industrial Profit} + W_{UPL}$$

### D. Rate of Surplus-Value

$$e' = \frac{S}{V}$$

Where:
- $S$ must include unproductive wages
- $V$ must include only productive wages

### E. State Workers Classification

**State workers are paid from revenue** (taxes, which are deductions from surplus-value):

$$\text{State workers} \in \text{UPL}$$

**Their wages are part of surplus-value distribution:**

$$S_{distributed} = \text{Rent} + \text{Interest} + \text{State wages} + \text{Other UPL wages}$$

---

## Common Errors Addressed (Page 46)

**Error 1:** Assuming labor paid from capital is always productive

**Correction:** Must also produce surplus-value
$$\text{Exchanged with capital} \not\Rightarrow \text{Productive}$$
$$\text{Exchanged with capital} + \text{Produces } S \Rightarrow \text{Productive}$$

**Error 2:** Confusing productive labor with useful labor

All labor is useful/necessary, but not all creates surplus-value.

**Error 3:** Using occupation or industry to classify

Must use **relation to capital** and **production of surplus-value**, not job title.

---

## Where Formal Equations Will Appear

1. **Chapter III (later sections):** Circuit equations showing state flows
2. **Chapter IV:** Empirical formulas for:
   - Allocating NIPA categories to PL/UPL
   - Calculating V and S from data
   - Computing e' (nominal and adjusted for state)
3. **Appendix III:** Detailed algorithms for classification

---

## Key Definitional Inequalities

From this chunk's analysis:

| **Statement** | **Implication** |
|--------------|----------------|
| $\text{Labor} \neq \text{Productive Labor}$ | Being labor is necessary but not sufficient |
| $\text{Production activity} \neq \text{Productive Labor}$ | Some production workers are unproductive |
| $\text{Exchanged with capital} \neq \text{Productive}$ | Also must create surplus-value |
| $\text{Socially necessary} \neq \text{Productive}$ | UPL can be necessary (police, teachers) |
| $\text{NIPA wages} \neq V$ | Variable capital is subset of total wages |
| $\text{NIPA profit} \neq S$ | Surplus-value includes UPL wages |

---

**See Also:**

- chunk_05_equations.md: Earlier conceptual framework
- chunk_08_equations.md: Circuit of capital equations (expected)
- chunks_10-13: Chapter IV empirical formulas

---

**Extraction Notes:**

This chunk provides Marx's **definitive statements** on PUPL from the Resultat (Results of the Immediate Process of Production). These are the theoretical foundation for all calculations in Chapter IV. While no formal equations appear, the conceptual relationships are precise and will be operationalized mathematically.
