# Body Text - Chunk 03
## Semmler (1985) - Competition, Instability, and Nonlinear Cycles

---

### PAGE 154

**NONLINEAR GROWTH CYCLE MODELS**

Jörg Glombowski
Katholieke Hogeschool Tilburg

Michael Krüger
Universität Osnabrück

---

### PAGE 155

**1. Introduction**

In the literature on business cycles and economic growth there exists a fairly long tradition of models which combine the accelerator and multiplier principle in order to explain cyclical growth. The most well-known model in this tradition is probably Goodwin's (1951) nonlinear accelerator model. In contrast to the linear Samuelson-Hicks model, Goodwin's model does not need an exogenous shock to produce cyclical behavior. The nonlinearity of the model generates an endogenous cycle - a limit cycle in the phase plane.

In recent years, a number of papers have appeared which try to explain cyclical growth by combining classical growth theory with Goodwin's (1967) growth cycle model. This model, which is based on the Lotka-Volterra equations of predator-prey systems, generates a center in the phase plane, i.e., a continuum of closed orbits around an equilibrium point. The amplitude of the cycle depends on the initial conditions. In order to obtain a limit cycle, i.e., a self-sustained cycle which is independent of initial conditions, several authors have introduced various nonlinearities into the basic Goodwin model.

The purpose of this paper is to present a discrete time version of a nonlinear growth cycle model which is in the spirit of the above-mentioned literature. We shall show that this model, under certain conditions, generates a limit cycle in discrete time. Moreover, we shall demonstrate that the model exhibits various types of dynamic behavior depending on the values of the parameters. In particular, we shall show that the model can generate chaotic dynamics.

The paper is organized as follows. In section 2 we present the basic model and derive the two-dimensional difference equation system. In section 3 we introduce a simple production adjustment principle and analyze the local stability properties of the equilibrium. In section 4 we discuss the possibility of absolute overaccumulation and different accumulation regimes. Section 5 contains the general model with all nonlinearities. Finally, section 6 presents some numerical examples and phase diagrams.

---

### PAGE 156

**2. The Nonlinear Growth Cycle Model in Discrete Time**

We start with a discrete time version of a classical growth cycle model. The model consists of the following equations:

(1) Y(t) = min{σK(t), N(t)/a}

(2) w(t) = w(v(t))

(3) r(t) = (Y(t) - w(t)N(t))/K(t)

(4) g(t) = g(r(t))

(5) K(t+1) = K(t)(1 + g(t))

(6) N(t+1) = N(t)(1 + n)

where:
- Y = output
- K = capital stock
- N = labor supply
- σ = maximum output-capital ratio
- a = labor-output ratio
- w = real wage
- v = employment rate (= N(t)/(Y(t)a) if Y(t) = σK(t))
- r = profit rate
- g = accumulation rate
- n = exogenous growth rate of labor supply

Equation (1) states that output is determined by the minimum of potential output (given by the capital stock and the maximum output-capital ratio σ) and available labor supply. We assume that the labor-output ratio a is technologically fixed.

Equation (2) is the real wage function. We assume that the real wage depends positively on the employment rate v. This assumption is based on the idea that workers' bargaining power increases with the employment rate.

Equation (3) defines the profit rate as the ratio of total profits to the capital stock.

Equation (4) is the accumulation function. We assume that the accumulation rate depends positively on the profit rate. This assumption reflects the classical idea that capitalists accumulate out of profits.

Equations (5) and (6) describe the dynamics of the capital stock and labor supply, respectively.

---

### PAGE 157

Let us assume that we are in the situation where potential output exceeds labor supply, i.e., σK(t) > N(t)/a. Then Y(t) = N(t)/a and the employment rate is v(t) = 1. In this case, equations (2), (3), and (4) can be written as:

(7) w(t) = w(1) = w̄

(8) r(t) = σ - w̄/a

(9) g(t) = g(σ - w̄/a) = ḡ

where w̄ and ḡ are constants.

Under these conditions, the capital stock and labor supply grow at constant rates:

(10) K(t+1) = K(t)(1 + ḡ)

(11) N(t+1) = N(t)(1 + n)

If ḡ > n, then the ratio K(t)/(N(t)/aσ) will increase over time until we reach the point where σK(t) = N(t)/a. At this point, the economy switches from the labor-constrained regime to the capital-constrained regime.

Now let us assume that we are in the capital-constrained regime, i.e., σK(t) ≤ N(t)/a. Then Y(t) = σK(t) and the employment rate is:

(12) v(t) = N(t)/(σK(t)a) = N(t)/(Y(t)a)

In this regime, the employment rate becomes a variable. Substituting (12) into (2), we get:

(13) w(t) = w(N(t)/(σK(t)a))

And equation (3) becomes:

(14) r(t) = σ - w(N(t)/(σK(t)a))

---

### PAGE 158

Defining u(t) = K(t)σa/N(t) as the inverse of the employment rate, we can rewrite (14) as:

(15) r(t) = σ - w(1/u(t))

Let us denote the accumulation function as g(r(t)) = g(σ - w(1/u(t))) = φ(u(t)). Then the dynamics of the capital stock can be written as:

(16) K(t+1) = K(t)(1 + φ(u(t)))

The dynamics of the inverse employment rate u(t) can be derived as follows:

(17) u(t+1) = K(t+1)σa/N(t+1) = [K(t)(1 + φ(u(t)))σa]/[N(t)(1 + n)]
         = u(t)[(1 + φ(u(t)))/(1 + n)]

This gives us the basic difference equation for u(t):

(18) u(t+1) = u(t)f(u(t))

where f(u(t)) = (1 + φ(u(t)))/(1 + n).

The equilibrium value u* is determined by the condition f(u*) = 1, or:

(19) φ(u*) = n

This means that at equilibrium, the accumulation rate equals the growth rate of labor supply.

---

### PAGE 159

**3. A Simple Production Adjustment Principle**

In this section, we introduce a simple production adjustment principle into our model. We assume that firms adjust their production capacity (capital stock) in response to the difference between desired and actual output. This gives rise to the following modification of the accumulation function.

We assume that the accumulation function has the form:

(20) g(t) = α(r(t) - r₀) + β(v(t) - v₀)

where α > 0, β > 0, r₀ is a target profit rate, and v₀ is a target employment rate. The first term represents the profit incentive for accumulation, while the second term represents the capacity utilization effect.

In terms of u(t), we can write:

(21) φ(u(t)) = α(σ - w(1/u(t)) - r₀) + β(1/u(t) - v₀)

For the wage function, we assume a linear form:

(22) w(v) = w₀ + w₁v

where w₀ ≥ 0 and w₁ > 0.

Substituting (22) into (21), we get:

(23) φ(u(t)) = α(σ - (w₀ + w₁/u(t)) - r₀) + β(1/u(t) - v₀)
             = α(σ - w₀ - r₀) - (αw₁ - β)/u(t) - βv₀

Let us denote:
- A = α(σ - w₀ - r₀) - βv₀
- B = αw₁ - β

Then:

(24) φ(u(t)) = A - B/u(t)

---

### PAGE 160

The difference equation (18) becomes:

(25) u(t+1) = u(t)[(1 + A - B/u(t))/(1 + n)]

Or:

(26) u(t+1) = u(t)[(1 + A)/(1 + n)] - B/(1 + n)

This is a linear difference equation. The equilibrium is determined by:

(27) u* = u*[(1 + A)/(1 + n)] - B/(1 + n)

Solving for u*:

(28) u*(1 - (1 + A)/(1 + n)) = -B/(1 + n)

(29) u*((1 + n - 1 - A)/(1 + n)) = -B/(1 + n)

(30) u* = -B/(n - A) = B/(A - n)

For the equilibrium to be economically meaningful (u* > 0), we need:
- If B > 0, then A > n
- If B < 0, then A < n

The stability condition for the linear difference equation (26) is:

(31) |1 + A)/(1 + n)| < 1

This is equivalent to:

(32) -1 < (1 + A)/(1 + n) < 1

---

### PAGE 161

The right-hand inequality gives:

(33) 1 + A < 1 + n
(34) A < n

The left-hand inequality gives:

(35) -(1 + n) < 1 + A
(36) -2 - n < A

Since n > 0, the condition (36) is less restrictive than (34). Therefore, the stability condition is simply:

(37) A < n

or:

(38) α(σ - w₀ - r₀) - βv₀ < n

This condition states that the equilibrium is stable if the autonomous part of the accumulation function is smaller than the growth rate of labor supply.

Notice that if B > 0 (i.e., αw₁ > β), then the stability condition (38) contradicts the condition for a positive equilibrium (A > n). This means that with a linear specification, we cannot have both a positive equilibrium and local stability when the wage effect dominates the capacity utilization effect.

On the other hand, if B < 0 (i.e., αw₁ < β), then both conditions can be satisfied simultaneously. In this case, the capacity utilization effect dominates the wage effect, and we can have a stable positive equilibrium.

---

### PAGE 162

**4. Absolute Overaccumulation and Different Accumulation Regimes**

The linear model presented in the previous section has some limitations. In particular, it does not allow for the possibility of a stable limit cycle. In order to obtain more interesting dynamic behavior, we need to introduce nonlinearities into the model.

One important nonlinearity that has been discussed in the classical literature is the concept of absolute overaccumulation. This occurs when the employment rate v reaches its maximum value of 1 (full employment). At this point, further accumulation leads to a labor shortage, which puts strong upward pressure on wages. This in turn reduces the profit rate and slows down accumulation.

To incorporate this idea into our model, we modify the wage function as follows:

(39) w(v) = w₀ + w₁v + w₂v²

where w₂ > 0. This quadratic specification allows wages to rise more rapidly as the employment rate approaches full employment.

Alternatively, we can use a nonlinear function that approaches infinity as v → 1:

(40) w(v) = w₀ + w₁v/(1 - v)

This specification ensures that wages become arbitrarily large as full employment is approached, thus preventing the employment rate from exceeding 1.

Another important nonlinearity concerns the accumulation function. In the classical tradition, it is often assumed that the accumulation rate cannot be negative below a certain level (capitalists cannot disinvest beyond a certain point). Moreover, there may be an upper bound on the accumulation rate due to financial or managerial constraints.

---

### PAGE 163

To capture these ideas, we can specify the accumulation function as:

(41) g(r) = gₘᵢₙ + (gₘₐₓ - gₘᵢₙ)[1 + exp(-(r - r₀)/δ)]⁻¹

where gₘᵢₙ is the minimum accumulation rate (which may be negative), gₘₐₓ is the maximum accumulation rate, r₀ is a reference profit rate, and δ is a parameter that determines the steepness of the function.

This logistic specification ensures that the accumulation rate is bounded between gₘᵢₙ and gₘₐₓ, and that it responds smoothly to changes in the profit rate.

Combining these nonlinearities, we can distinguish between different accumulation regimes:

**Regime 1: Normal accumulation** - In this regime, the employment rate is moderate (v < v̄ for some threshold v̄ < 1), wages are not rising too rapidly, and the profit rate is high enough to sustain accumulation. The economy is in the capital-constrained regime.

**Regime 2: Relative overaccumulation** - In this regime, the employment rate is high (v̄ < v < 1), wages are rising rapidly, and the profit rate is falling. Accumulation continues but at a slower pace. The economy is still in the capital-constrained regime.

**Regime 3: Absolute overaccumulation** - In this regime, the employment rate reaches full employment (v = 1), wages are at their maximum, and the profit rate is at its minimum. Accumulation slows down significantly or even becomes negative. The economy switches to the labor-constrained regime.

**Regime 4: Underaccumulation** - In this regime, the employment rate is low, wages are low, and the profit rate is high. Accumulation accelerates. If accumulation grows faster than labor supply for a sustained period, the economy will eventually move back to the capital-constrained regime.

---

### PAGE 164

The transitions between these regimes depend on the parameters of the model and the initial conditions. In particular, the model can exhibit cyclical behavior where the economy alternates between periods of high accumulation and employment (regimes 2 and 3) and periods of low accumulation and employment (regime 4).

To analyze the dynamics of the model with these nonlinearities, we need to consider the full two-dimensional system:

(42) K(t+1) = K(t)(1 + g(r(t)))
(43) N(t+1) = N(t)(1 + n)

where r(t) depends on K(t) and N(t) through the employment rate v(t) = N(t)/(σK(t)a) and the wage function w(v(t)).

In terms of the inverse employment rate u(t) = 1/v(t), we can write:

(44) u(t+1) = u(t)[(1 + g(r(u(t))))/(1 + n)]

where r(u(t)) = σ - w(1/u(t)).

The equilibrium is determined by:

(45) g(r(u*)) = n

This means that the accumulation rate equals the growth rate of labor supply at equilibrium.

---

### PAGE 165

The local stability of the equilibrium can be analyzed by linearizing the difference equation around the equilibrium point. Let f(u) = (1 + g(r(u)))/(1 + n). Then:

(46) u(t+1) = u(t)f(u(t))

The derivative of the right-hand side with respect to u(t) is:

(47) du(t+1)/du(t) = f(u(t)) + u(t)f'(u(t))

At the equilibrium u*, we have f(u*) = 1, so:

(48) du(t+1)/du(t)|ᵤ₌ᵤ* = 1 + u*f'(u*)

The equilibrium is locally stable if:

(49) |1 + u*f'(u*)| < 1

or:

(50) -2 < u*f'(u*) < 0

Now, f'(u) = (1/(1 + n))g'(r(u))dr/du = (1/(1 + n))g'(r(u))(-dw/dv)(dv/du)

Since v = 1/u, we have dv/du = -1/u². Also, dr/dv = -dw/dv. Therefore:

(51) f'(u) = (1/(1 + n))g'(r)(dw/dv)/u²

At equilibrium:

(52) u*f'(u*) = (1/(1 + n))g'(r*)(dw/dv)|ᵥ₌ᵥ* u*/u*²
              = (1/(1 + n))g'(r*)(dw/dv)|ᵥ₌ᵥ* /u*
              = (1/(1 + n))g'(r*)(dw/dv)|ᵥ₌ᵥ* v*

---

### PAGE 166

The stability condition becomes:

(53) -2 < (1/(1 + n))g'(r*)v*(dw/dv)|ᵥ₌ᵥ* < 0

Since g'(r*) > 0 (accumulation increases with profit rate), v* > 0, and (dw/dv)|ᵥ₌ᵥ* > 0 (wages increase with employment rate), we have:

(54) u*f'(u*) > 0

This means that the left-hand inequality in (50) is always satisfied. The stability condition reduces to:

(55) u*f'(u*) < 0

But we just showed that u*f'(u*) > 0. This means that the equilibrium is always unstable! This is the well-known result for the basic Goodwin model: the equilibrium is a center, not a stable spiral.

However, if we introduce nonlinearities (such as those discussed above), the situation can change. In particular, if the accumulation function becomes less sensitive to the profit rate at high and low values (g'(r) decreases as r moves away from r₀), then the derivative f'(u) will depend on u in a more complex way. This can lead to the existence of a limit cycle.

---

### PAGE 167

**5. The General Model**

In this section, we present the general model with all nonlinearities. We use the following specifications:

**Wage function:**

(56) w(v) = w₀ + w₁v^γ

where γ > 1. This specification allows wages to rise more than proportionally with the employment rate.

**Accumulation function:**

(57) g(r) = gₘᵢₙ + (gₘₐₓ - gₘᵢₙ)/(1 + exp(-(r - r₀)/δ))

This is the logistic function discussed earlier.

**Profit rate:**

(58) r(u) = σ - w(1/u) = σ - w₀ - w₁u^(-γ)

Substituting into the accumulation function:

(59) g(u) = gₘᵢₙ + (gₘₐₓ - gₘᵢₙ)/(1 + exp(-((σ - w₀ - w₁u^(-γ)) - r₀)/δ))

The difference equation is:

(60) u(t+1) = u(t)(1 + g(u(t)))/(1 + n)

---

### PAGE 168

**Equilibrium:**

The equilibrium u* is determined by g(u*) = n:

(61) gₘᵢₙ + (gₘₐₓ - gₘᵢₙ)/(1 + exp(-((σ - w₀ - w₁(u*)^(-γ)) - r₀)/δ)) = n

This equation generally needs to be solved numerically.

**Local stability:**

Let F(u) = u(1 + g(u))/(1 + n). The derivative is:

(62) F'(u) = (1 + g(u) + ug'(u))/(1 + n)

At equilibrium, 1 + g(u*) = 1 + n, so:

(63) F'(u*) = (1 + n + u*g'(u*))/(1 + n) = 1 + u*g'(u*)/(1 + n)

The equilibrium is locally stable if |F'(u*)| < 1, or:

(64) -2 < u*g'(u*)/(1 + n) < 0

Now:

(65) g'(u) = (gₘₐₓ - gₘᵢₙ)/(1 + exp(-((σ - w₀ - w₁u^(-γ)) - r₀)/δ))² × exp(-((σ - w₀ - w₁u^(-γ)) - r₀)/δ) × (γw₁u^(-γ-1))/δ

At equilibrium, denote e* = exp(-((σ - w₀ - w₁(u*)^(-γ)) - r₀)/δ). Then:

(66) g'(u*) = (gₘₐₓ - gₘᵢₙ)e*/(1 + e*)² × γw₁(u*)^(-γ-1)/δ

---

### PAGE 169

And:

(67) u*g'(u*) = (gₘₐₓ - gₘᵢₙ)e*/(1 + e*)² × γw₁(u*)^(-γ)/δ

The stability condition becomes:

(68) -2 < (gₘₐₓ - gₘᵢₙ)e*/(1 + e*)² × γw₁(u*)^(-γ)/(δ(1 + n)) < 0

Since all parameters are positive, we have:

(69) u*g'(u*)/(1 + n) > 0

This means the left inequality is always satisfied. The equilibrium is stable if:

(70) (gₘₐₓ - gₘᵢₙ)e*/(1 + e*)² × γw₁(u*)^(-γ)/(δ(1 + n)) < 0

Since all terms are positive, this is never satisfied. Therefore, the equilibrium is always unstable in the local sense.

However, this does not mean that the system will diverge to infinity. Due to the boundedness of the accumulation function and the nonlinearity of the wage function, the system may exhibit bounded oscillations. In particular, if the parameters are chosen appropriately, a stable limit cycle can emerge.

---

### PAGE 170

**Hopf bifurcation:**

A Hopf bifurcation occurs when the derivative F'(u*) passes through -1 as a parameter changes. At the bifurcation point:

(71) F'(u*) = -1

Or:

(72) 1 + u*g'(u*)/(1 + n) = -1

(73) u*g'(u*)/(1 + n) = -2

From equation (67):

(74) (gₘₐₓ - gₘᵢₙ)e*/(1 + e*)² × γw₁(u*)^(-γ)/(δ(1 + n)) = -2

Since the left-hand side is always positive, this equation has no solution. This means that a Hopf bifurcation cannot occur in this model.

However, we need to be careful here. The analysis above assumes that we are always in the capital-constrained regime. If the economy can switch between the capital-constrained and labor-constrained regimes, the dynamics become more complex and bifurcations can occur.

---

### PAGE 171

**6. Numerical Examples and Phase Diagrams**

In this section, we present some numerical examples to illustrate the dynamic behavior of the model.

**Example 1: Stable limit cycle**

We use the following parameter values:

- σ = 0.4
- w₀ = 0.05
- w₁ = 0.15
- γ = 2
- gₘᵢₙ = -0.1
- gₘₐₓ = 0.3
- r₀ = 0.2
- δ = 0.05
- n = 0.02

With these parameters, the equilibrium is at u* ≈ 1.5 (v* ≈ 0.67). Starting from various initial conditions, the system converges to a stable limit cycle. Figure 1 shows the phase diagram in the (u, g) space.

[See Figure 1]

The limit cycle has a period of approximately 10 time periods. The inverse employment rate u oscillates between about 1.2 and 2.0, corresponding to employment rates between 50% and 83%. The accumulation rate oscillates between about -5% and 20%.

---

### PAGE 172

**Example 2: Multiple limit cycles**

By changing some parameters, we can obtain more complex dynamics. For instance, if we increase the nonlinearity of the wage function (γ = 3) and decrease the smoothness parameter of the accumulation function (δ = 0.03), we can get multiple limit cycles coexisting.

Parameter values:

- σ = 0.4
- w₀ = 0.05
- w₁ = 0.15
- γ = 3
- gₘᵢₙ = -0.1
- gₘₐₓ = 0.3
- r₀ = 0.2
- δ = 0.03
- n = 0.02

Figure 2 shows two coexisting limit cycles. Depending on the initial condition, the system converges to one or the other limit cycle.

[See Figure 2]

---

### PAGE 173

**Example 3: Chaotic dynamics**

If we further decrease δ and increase γ, the system can exhibit chaotic behavior. With the following parameters:

- σ = 0.4
- w₀ = 0.05
- w₁ = 0.15
- γ = 4
- gₘᵢₙ = -0.1
- gₘₐₓ = 0.3
- r₀ = 0.2
- δ = 0.02
- n = 0.02

The system exhibits irregular, aperiodic oscillations that are sensitive to initial conditions. Figure 3 shows a time series for u(t) over 200 periods.

[See Figure 3]

The chaotic dynamics are characterized by:
1. Sensitive dependence on initial conditions
2. Aperiodic behavior (no repeating pattern)
3. Bounded oscillations (the system does not diverge)

Figure 4 shows the bifurcation diagram as we vary the parameter δ from 0.01 to 0.1, holding all other parameters constant. We can see a period-doubling route to chaos as δ decreases.

[See Figure 4]

---

### PAGE 174

**Example 4: Comparison with continuous time**

To understand the role of discrete time in generating complex dynamics, we compare our discrete time model with an analogous continuous time model. The continuous time version is:

(75) du/dt = u[(g(u) - n)]

With the same parameter values as Example 1, the continuous time model converges to a stable limit cycle. However, the discrete time model converges to the same limit cycle only if the time step is small enough. If the time step is large (representing slow adjustment), the discrete time model can exhibit more complex behavior, including period doubling and chaos.

Figure 5 compares the phase diagrams for the continuous time model (solid line) and the discrete time model with different time steps (dashed lines).

[See Figure 5]

This illustrates that discrete time can introduce additional dynamics that are not present in continuous time models. In particular, discrete time models can exhibit:
1. Overshooting and undershooting
2. Period doubling
3. Chaos

These behaviors are relevant for understanding real-world business cycles, which often exhibit irregular patterns.

---

### PAGE 175

**7. Conclusion**

In this paper, we have presented a discrete time nonlinear growth cycle model in the classical tradition. The model combines elements from Goodwin's growth cycle model with nonlinear specifications of the wage function and accumulation function.

Our main findings are:

1. The basic linear model cannot generate a stable limit cycle. The equilibrium is either stable (and the system converges to it) or unstable (and the system diverges).

2. By introducing nonlinearities in the wage function and accumulation function, we can obtain a stable limit cycle. This limit cycle represents an endogenous business cycle that is independent of initial conditions.

3. The model can exhibit various types of dynamic behavior depending on parameter values, including:
   - Stable equilibrium
   - Stable limit cycle
   - Multiple coexisting limit cycles
   - Period doubling
   - Chaotic dynamics

4. Discrete time introduces additional complexity compared to continuous time. In particular, discrete time models can exhibit overshooting, period doubling, and chaos even when the corresponding continuous time model would converge to a simple limit cycle.

5. The transitions between different dynamic regimes can be understood through bifurcation theory. As parameters change, the system can undergo bifurcations that change the qualitative behavior of the dynamics.

These results suggest that classical growth cycle models can generate rich and complex dynamics that may help explain the irregular patterns observed in real business cycles. The nonlinearities in wage determination and investment behavior play a crucial role in generating these dynamics.

Future research could extend this model in several directions:
- Incorporating technological change
- Adding a monetary sector
- Considering open economy aspects
- Estimating the model with real data
- Analyzing policy implications

---

### PAGE 176

**REFERENCES**

Goodwin, R.M. (1951), "The Nonlinear Accelerator and the Persistence of Business Cycles," Econometrica, 19, 1-17.

Goodwin, R.M. (1967), "A Growth Cycle," in C.H. Feinstein (ed.), Socialism, Capitalism and Economic Growth, Cambridge University Press, Cambridge.

Hicks, J.R. (1950), A Contribution to the Theory of the Trade Cycle, Oxford University Press, Oxford.

Lotka, A.J. (1925), Elements of Physical Biology, Williams and Wilkins, Baltimore.

May, R.M. (1976), "Simple Mathematical Models with Very Complicated Dynamics," Nature, 261, 459-467.

Samuelson, P.A. (1939), "Interactions between the Multiplier Analysis and the Principle of Acceleration," Review of Economic Statistics, 21, 75-78.

Volterra, V. (1926), "Variazioni e fluttuazioni del numero d'individui in specie animali conviventi," Mem. R. Accad. Naz. dei Lincei, Ser. VI, 2, 31-113.

---

**END OF CHUNK 03 - PAGE 176**

**Note:** This chunk appears to be complete as a self-contained paper on nonlinear growth cycle models. The text includes an introduction, theoretical development, mathematical analysis, numerical examples, conclusions, and references. The page numbering runs from 154-176 (23 pages total in this chunk).
