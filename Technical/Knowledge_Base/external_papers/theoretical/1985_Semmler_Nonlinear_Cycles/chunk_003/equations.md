# Equations - Chunk 03
## Semmler (1985) - Competition, Instability, and Nonlinear Cycles

---

## Section 2: The Nonlinear Growth Cycle Model in Discrete Time

### Basic Model Structure (Equations 1-6)

**Equation (1) - Production Function:**
```latex
Y(t) = \min\{\sigma K(t), \frac{N(t)}{a}\}
```
Output is determined by minimum of capital-constrained output and labor-constrained output.

**Equation (2) - Wage Function:**
```latex
w(t) = w(v(t))
```
Real wage depends on employment rate.

**Equation (3) - Profit Rate:**
```latex
r(t) = \frac{Y(t) - w(t)N(t)}{K(t)}
```
Profit rate defined as total profits divided by capital stock.

**Equation (4) - Accumulation Function:**
```latex
g(t) = g(r(t))
```
Accumulation rate depends on profit rate.

**Equation (5) - Capital Stock Dynamics:**
```latex
K(t+1) = K(t)(1 + g(t))
```
Capital stock evolution equation.

**Equation (6) - Labor Supply Dynamics:**
```latex
N(t+1) = N(t)(1 + n)
```
Labor supply grows at exogenous rate n.

---

### Labor-Constrained Regime (Equations 7-11)

**Equation (7) - Full Employment Wage:**
```latex
w(t) = w(1) = \bar{w}
```
When v(t) = 1 (full employment), wage is constant.

**Equation (8) - Profit Rate at Full Employment:**
```latex
r(t) = \sigma - \frac{\bar{w}}{a}
```

**Equation (9) - Constant Accumulation Rate:**
```latex
g(t) = g\left(\sigma - \frac{\bar{w}}{a}\right) = \bar{g}
```

**Equation (10) - Capital Stock Growth:**
```latex
K(t+1) = K(t)(1 + \bar{g})
```

**Equation (11) - Labor Supply Growth:**
```latex
N(t+1) = N(t)(1 + n)
```

---

### Capital-Constrained Regime (Equations 12-19)

**Equation (12) - Employment Rate:**
```latex
v(t) = \frac{N(t)}{\sigma K(t) a} = \frac{N(t)}{Y(t)a}
```

**Equation (13) - Wage as Function of Employment:**
```latex
w(t) = w\left(\frac{N(t)}{\sigma K(t) a}\right)
```

**Equation (14) - Profit Rate:**
```latex
r(t) = \sigma - w\left(\frac{N(t)}{\sigma K(t) a}\right)
```

**Equation (15) - Profit Rate in Terms of Inverse Employment:**
```latex
r(t) = \sigma - w\left(\frac{1}{u(t)}\right)
```
where u(t) = K(t)σa/N(t) is the inverse of employment rate.

**Equation (16) - Capital Stock Dynamics:**
```latex
K(t+1) = K(t)(1 + \phi(u(t)))
```
where φ(u(t)) = g(σ - w(1/u(t))).

**Equation (17) - Inverse Employment Rate Dynamics:**
```latex
u(t+1) = \frac{K(t+1)\sigma a}{N(t+1)} = \frac{K(t)(1 + \phi(u(t)))\sigma a}{N(t)(1 + n)} = u(t)\frac{1 + \phi(u(t))}{1 + n}
```

**Equation (18) - Basic Difference Equation:**
```latex
u(t+1) = u(t)f(u(t))
```
where f(u(t)) = (1 + φ(u(t)))/(1 + n).

**Equation (19) - Equilibrium Condition:**
```latex
\phi(u^*) = n
```
At equilibrium, accumulation rate equals labor supply growth rate.

---

## Section 3: A Simple Production Adjustment Principle

### Linear Specification (Equations 20-30)

**Equation (20) - Linear Accumulation Function:**
```latex
g(t) = \alpha(r(t) - r_0) + \beta(v(t) - v_0)
```
where α > 0, β > 0.

**Equation (21) - Accumulation Function in Terms of u:**
```latex
\phi(u(t)) = \alpha\left(\sigma - w\left(\frac{1}{u(t)}\right) - r_0\right) + \beta\left(\frac{1}{u(t)} - v_0\right)
```

**Equation (22) - Linear Wage Function:**
```latex
w(v) = w_0 + w_1 v
```
where w₀ ≥ 0 and w₁ > 0.

**Equation (23) - Expanded Accumulation Function:**
```latex
\phi(u(t)) = \alpha\left(\sigma - \left(w_0 + \frac{w_1}{u(t)}\right) - r_0\right) + \beta\left(\frac{1}{u(t)} - v_0\right)
```
```latex
= \alpha(\sigma - w_0 - r_0) - \frac{\alpha w_1 - \beta}{u(t)} - \beta v_0
```

**Equation (24) - Simplified Form:**
```latex
\phi(u(t)) = A - \frac{B}{u(t)}
```
where A = α(σ - w₀ - r₀) - βv₀ and B = αw₁ - β.

**Equation (25) - Difference Equation:**
```latex
u(t+1) = u(t)\frac{1 + A - \frac{B}{u(t)}}{1 + n}
```

**Equation (26) - Linear Difference Equation:**
```latex
u(t+1) = u(t)\frac{1 + A}{1 + n} - \frac{B}{1 + n}
```

**Equation (27) - Equilibrium Condition:**
```latex
u^* = u^*\frac{1 + A}{1 + n} - \frac{B}{1 + n}
```

**Equation (28) - Rearranged:**
```latex
u^*\left(1 - \frac{1 + A}{1 + n}\right) = -\frac{B}{1 + n}
```

**Equation (29) - Further Simplification:**
```latex
u^*\frac{1 + n - 1 - A}{1 + n} = -\frac{B}{1 + n}
```

**Equation (30) - Equilibrium Solution:**
```latex
u^* = -\frac{B}{n - A} = \frac{B}{A - n}
```

---

### Stability Analysis (Equations 31-38)

**Equation (31) - Stability Condition:**
```latex
\left|\frac{1 + A}{1 + n}\right| < 1
```

**Equation (32) - Equivalent Form:**
```latex
-1 < \frac{1 + A}{1 + n} < 1
```

**Equation (33) - Right Inequality:**
```latex
1 + A < 1 + n
```

**Equation (34) - Simplified:**
```latex
A < n
```

**Equation (35) - Left Inequality:**
```latex
-(1 + n) < 1 + A
```

**Equation (36) - Simplified:**
```latex
-2 - n < A
```

**Equation (37) - Final Stability Condition:**
```latex
A < n
```

**Equation (38) - In Terms of Parameters:**
```latex
\alpha(\sigma - w_0 - r_0) - \beta v_0 < n
```

---

## Section 4: Absolute Overaccumulation and Different Accumulation Regimes

### Nonlinear Wage Functions (Equations 39-40)

**Equation (39) - Quadratic Wage Function:**
```latex
w(v) = w_0 + w_1 v + w_2 v^2
```
where w₂ > 0.

**Equation (40) - Alternative Nonlinear Form:**
```latex
w(v) = w_0 + \frac{w_1 v}{1 - v}
```
This prevents v from exceeding 1.

---

### Logistic Accumulation Function (Equation 41)

**Equation (41) - Bounded Accumulation Function:**
```latex
g(r) = g_{\min} + (g_{\max} - g_{\min})[1 + \exp(-(r - r_0)/\delta)]^{-1}
```
where:
- g_min = minimum accumulation rate
- g_max = maximum accumulation rate
- r₀ = reference profit rate
- δ = steepness parameter

---

### Two-Dimensional System (Equations 42-45)

**Equation (42) - Capital Dynamics:**
```latex
K(t+1) = K(t)(1 + g(r(t)))
```

**Equation (43) - Labor Dynamics:**
```latex
N(t+1) = N(t)(1 + n)
```

**Equation (44) - Reduced Form:**
```latex
u(t+1) = u(t)\frac{1 + g(r(u(t)))}{1 + n}
```
where r(u(t)) = σ - w(1/u(t)).

**Equation (45) - Equilibrium:**
```latex
g(r(u^*)) = n
```

---

### Local Stability Analysis (Equations 46-55)

**Equation (46) - General Form:**
```latex
u(t+1) = u(t)f(u(t))
```

**Equation (47) - Derivative:**
```latex
\frac{du(t+1)}{du(t)} = f(u(t)) + u(t)f'(u(t))
```

**Equation (48) - At Equilibrium:**
```latex
\left.\frac{du(t+1)}{du(t)}\right|_{u=u^*} = 1 + u^* f'(u^*)
```
since f(u*) = 1.

**Equation (49) - Stability Condition:**
```latex
|1 + u^* f'(u^*)| < 1
```

**Equation (50) - Equivalent:**
```latex
-2 < u^* f'(u^*) < 0
```

**Equation (51) - Derivative of f:**
```latex
f'(u) = \frac{1}{1 + n} g'(r(u)) \frac{dw/dv}{u^2}
```

**Equation (52) - At Equilibrium:**
```latex
u^* f'(u^*) = \frac{1}{1 + n} g'(r^*) \left.\frac{dw}{dv}\right|_{v=v^*} \frac{u^*}{(u^*)^2}
```
```latex
= \frac{1}{1 + n} g'(r^*) \left.\frac{dw}{dv}\right|_{v=v^*} v^*
```

**Equation (53) - Stability Condition:**
```latex
-2 < \frac{1}{1 + n} g'(r^*) v^* \left.\frac{dw}{dv}\right|_{v=v^*} < 0
```

**Equation (54) - Sign Analysis:**
```latex
u^* f'(u^*) > 0
```
since g'(r*) > 0, v* > 0, and dw/dv|_{v=v*} > 0.

**Equation (55) - Impossibility:**
```latex
u^* f'(u^*) < 0
```
This is required for stability but contradicts (54).

---

## Section 5: The General Model

### General Nonlinear Specifications (Equations 56-59)

**Equation (56) - Power Wage Function:**
```latex
w(v) = w_0 + w_1 v^\gamma
```
where γ > 1.

**Equation (57) - Logistic Accumulation:**
```latex
g(r) = g_{\min} + \frac{g_{\max} - g_{\min}}{1 + \exp(-(r - r_0)/\delta)}
```

**Equation (58) - Profit Rate:**
```latex
r(u) = \sigma - w\left(\frac{1}{u}\right) = \sigma - w_0 - w_1 u^{-\gamma}
```

**Equation (59) - Complete Accumulation Function:**
```latex
g(u) = g_{\min} + \frac{g_{\max} - g_{\min}}{1 + \exp(-[(\sigma - w_0 - w_1 u^{-\gamma}) - r_0]/\delta)}
```

**Equation (60) - Master Difference Equation:**
```latex
u(t+1) = u(t) \frac{1 + g(u(t))}{1 + n}
```

---

### Equilibrium and Stability (Equations 61-70)

**Equation (61) - Equilibrium Condition:**
```latex
g_{\min} + \frac{g_{\max} - g_{\min}}{1 + \exp(-[(\sigma - w_0 - w_1 (u^*)^{-\gamma}) - r_0]/\delta)} = n
```

**Equation (62) - Derivative of F:**
```latex
F'(u) = \frac{1 + g(u) + u g'(u)}{1 + n}
```
where F(u) = u(1 + g(u))/(1 + n).

**Equation (63) - Derivative at Equilibrium:**
```latex
F'(u^*) = \frac{1 + n + u^* g'(u^*)}{1 + n} = 1 + \frac{u^* g'(u^*)}{1 + n}
```

**Equation (64) - Stability Condition:**
```latex
-2 < \frac{u^* g'(u^*)}{1 + n} < 0
```

**Equation (65) - Derivative of g:**
```latex
g'(u) = \frac{g_{\max} - g_{\min}}{[1 + \exp(-[(\sigma - w_0 - w_1 u^{-\gamma}) - r_0]/\delta)]^2}
```
```latex
\times \exp(-[(\sigma - w_0 - w_1 u^{-\gamma}) - r_0]/\delta) \times \frac{\gamma w_1 u^{-\gamma-1}}{\delta}
```

**Equation (66) - At Equilibrium:**
```latex
g'(u^*) = \frac{(g_{\max} - g_{\min}) e^*}{(1 + e^*)^2} \times \frac{\gamma w_1 (u^*)^{-\gamma-1}}{\delta}
```
where e* = exp(−[(σ − w₀ − w₁(u*)^{−γ}) − r₀]/δ).

**Equation (67) - Product:**
```latex
u^* g'(u^*) = \frac{(g_{\max} - g_{\min}) e^*}{(1 + e^*)^2} \times \frac{\gamma w_1 (u^*)^{-\gamma}}{\delta}
```

**Equation (68) - Stability in Terms of Parameters:**
```latex
-2 < \frac{(g_{\max} - g_{\min}) e^*}{(1 + e^*)^2} \times \frac{\gamma w_1 (u^*)^{-\gamma}}{\delta(1 + n)} < 0
```

**Equation (69) - Sign:**
```latex
\frac{u^* g'(u^*)}{1 + n} > 0
```

**Equation (70) - Required but Impossible:**
```latex
\frac{(g_{\max} - g_{\min}) e^*}{(1 + e^*)^2} \times \frac{\gamma w_1 (u^*)^{-\gamma}}{\delta(1 + n)} < 0
```
This is never satisfied since all terms are positive.

---

### Hopf Bifurcation Analysis (Equations 71-74)

**Equation (71) - Bifurcation Point:**
```latex
F'(u^*) = -1
```

**Equation (72) - Equivalent:**
```latex
1 + \frac{u^* g'(u^*)}{1 + n} = -1
```

**Equation (73) - Required Value:**
```latex
\frac{u^* g'(u^*)}{1 + n} = -2
```

**Equation (74) - In Terms of Parameters:**
```latex
\frac{(g_{\max} - g_{\min}) e^*}{(1 + e^*)^2} \times \frac{\gamma w_1 (u^*)^{-\gamma}}{\delta(1 + n)} = -2
```
Since LHS is always positive, no solution exists (in the capital-constrained regime).

---

## Section 6: Numerical Examples

### Continuous Time Comparison (Equation 75)

**Equation (75) - Continuous Time Model:**
```latex
\frac{du}{dt} = u[g(u) - n]
```

---

## Summary of Mathematical Content

**Total Equations:** 75 numbered equations

**Equation Categories:**
1. **Model Definition** (Equations 1-6): Basic structure
2. **Labor-Constrained Regime** (Equations 7-11): Full employment case
3. **Capital-Constrained Regime** (Equations 12-19): Variable employment
4. **Linear Specification** (Equations 20-30): Simple case
5. **Stability Analysis** (Equations 31-38): Linear model stability
6. **Nonlinear Extensions** (Equations 39-41): Advanced specifications
7. **General Dynamics** (Equations 42-55): Full nonlinear analysis
8. **Complete Model** (Equations 56-70): General case with all nonlinearities
9. **Bifurcation Theory** (Equations 71-74): Hopf bifurcation
10. **Continuous Time** (Equation 75): Comparison model

**Mathematical Techniques Used:**
- Discrete time difference equations
- Nonlinear dynamics
- Phase plane analysis
- Local stability analysis (linearization)
- Bifurcation theory
- Logistic functions
- Power functions
- Exponential functions

**Key Variables:**
- Y = output
- K = capital stock
- N = labor supply
- v = employment rate
- u = inverse employment rate (u = 1/v)
- w = real wage
- r = profit rate
- g = accumulation rate
- n = labor supply growth rate
- σ = output-capital ratio
- a = labor-output ratio

**Key Parameters:**
- w₀, w₁, w₂, γ = wage function parameters
- g_min, g_max = bounds on accumulation rate
- r₀ = reference profit rate
- δ = smoothness parameter
- α, β = adjustment speed parameters
- v₀ = target employment rate
