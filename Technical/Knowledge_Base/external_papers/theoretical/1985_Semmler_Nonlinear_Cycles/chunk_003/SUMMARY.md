# SUMMARY - Chunk 03
## Semmler (1985) - Competition, Instability, and Nonlinear Cycles
### Nonlinear Growth Cycle Models by Jörg Glombowski and Michael Krüger

---

## Document Metadata

**Chunk:** 03 of larger proceedings volume
**Pages:** 154-176 (23 pages)
**Authors:** Jörg Glombowski (Katholieke Hogeschool Tilburg) and Michael Krüger (Universität Osnabrück)
**Paper Title:** Nonlinear Growth Cycle Models
**Publication:** Conference Proceedings - Competition, Instability, and Nonlinear Cycles (1985)
**Document Type:** Academic research paper (theoretical economics with mathematical modeling)

---

## Executive Summary

This paper presents a discrete time version of a nonlinear growth cycle model in the classical economics tradition. The authors demonstrate that by combining nonlinear specifications of wage determination and investment behavior with discrete time dynamics, the model can generate a rich variety of cyclical behaviors including stable limit cycles, multiple attractors, period doubling, and deterministic chaos. This work represents an important bridge between classical growth theory, Goodwin's growth cycle model, and emerging chaos theory, showing that endogenous business cycles with complex, irregular patterns can arise from purely deterministic economic mechanisms without requiring exogenous shocks.

---

## Main Research Questions and Objectives

1. **Can discrete time formulation generate limit cycles?** - Can a discrete time version of classical growth cycle models produce self-sustained oscillations (limit cycles) that are independent of initial conditions?

2. **What types of dynamics are possible?** - What range of dynamic behaviors (stable equilibria, limit cycles, chaos) can the model exhibit depending on parameter values?

3. **What role does discrete time play?** - How does discrete time formulation differ from continuous time in terms of the complexity of dynamics generated?

4. **Can the model explain irregular cycles?** - Can nonlinear specifications generate chaotic dynamics that might explain the irregular patterns observed in real business cycles?

---

## Theoretical Framework

### Classical Growth Tradition

The paper builds on the classical tradition that emphasizes:
- Profit-driven capital accumulation
- Conflict between capital and labor over income distribution
- Reserve army of labor mechanism (employment rate affects wages)
- Cyclical tendencies inherent in capitalist accumulation

### Goodwin's Growth Cycle Model (1967)

Foundation: Lotka-Volterra predator-prey equations adapted to economics
- Capital (predator) and Labor (prey) dynamics
- Generates center in phase plane (continuum of closed orbits)
- Amplitude depends on initial conditions
- Limitation: No attractor, no limit cycle

### Nonlinear Accelerator Tradition

Goodwin (1951):
- Nonlinearity generates endogenous cycles
- Limit cycle in phase plane
- No exogenous shocks needed (unlike linear Samuelson-Hicks model)

### Innovation of Current Paper

Combines:
1. Classical growth theory (profit-accumulation nexus)
2. Goodwin's growth cycle framework (capital-labor dynamics)
3. Nonlinear specifications (wage function, accumulation function)
4. **Discrete time formulation** (creates additional dynamic complexity)

---

## Model Structure

### Core Variables

**State Variables:**
- K(t) = Capital stock at time t
- N(t) = Labor supply at time t
- u(t) = Inverse employment rate = K(t)σa/N(t) where v(t) = 1/u(t)

**Economic Variables:**
- Y(t) = Output
- v(t) = Employment rate = employed labor / total labor
- w(t) = Real wage
- r(t) = Profit rate
- g(t) = Accumulation rate (investment rate)

**Parameters:**
- σ = Maximum output-capital ratio (technical parameter)
- a = Labor-output ratio (technical parameter)
- n = Exogenous growth rate of labor supply

### Two Regimes

**1. Labor-Constrained Regime:**
- Condition: σK(t) > N(t)/a
- Output determined by labor availability: Y(t) = N(t)/a
- Employment rate: v(t) = 1 (full employment)
- Wages constant at w̄, profit rate and accumulation constant
- System grows at constant rates until switching to capital-constrained regime

**2. Capital-Constrained Regime:**
- Condition: σK(t) ≤ N(t)/a
- Output determined by capital: Y(t) = σK(t)
- Employment rate variable: v(t) = N(t)/(σK(t)a)
- Wages and profit rate vary with employment
- Source of cyclical dynamics

### Basic Difference Equation

In capital-constrained regime, dynamics reduce to single equation:

**u(t+1) = u(t) · [(1 + g(u(t)))/(1 + n)]**

where:
- g(u(t)) is accumulation function depending on inverse employment rate
- Equilibrium condition: g(u*) = n (accumulation equals labor growth)

---

## Functional Specifications

### Wage Function Specifications

**Linear (Section 3):**
```
w(v) = w₀ + w₁v
```
Simple but insufficient for limit cycles.

**Power Function (Section 5):**
```
w(v) = w₀ + w₁v^γ where γ > 1
```
Allows wages to rise more than proportionally as employment approaches full employment.

**Alternative Barrier Form:**
```
w(v) = w₀ + w₁v/(1-v)
```
Prevents employment from exceeding 100% by making wages approach infinity at v → 1.

**Economic Logic:**
- Higher employment → stronger worker bargaining power → higher wages
- Nonlinearity captures accelerating wage pressure near full employment
- Absolute overaccumulation: when v → 1, wages rise sharply, profit falls, accumulation slows

### Accumulation Function Specifications

**Linear (Section 3):**
```
g(t) = α(r(t) - r₀) + β(v(t) - v₀)
```
- α > 0: profit incentive for accumulation
- β > 0: capacity utilization effect
- Too simple for limit cycles

**Logistic/Bounded (Sections 4-5):**
```
g(r) = g_min + (g_max - g_min)/(1 + exp(-(r - r₀)/δ))
```
- Bounded between g_min and g_max
- Smooth S-shaped response to profit rate
- δ controls steepness of response
- Captures: financial constraints, managerial limits, decreasing returns to investment

**Economic Logic:**
- Higher profits → more resources for investment → higher accumulation
- Bounded above: can't exceed certain rate due to constraints
- Bounded below: some minimal disinvestment even at low profits
- Nonlinearity essential for generating limit cycles and complex dynamics

---

## Mathematical Analysis

### Linear Model Results (Section 3)

**Equilibrium:**
```
u* = B/(A - n)
```
where A = α(σ - w₀ - r₀) - βv₀ and B = αw₁ - β

**Stability Condition:**
```
A < n
```

**Key Finding:** Cannot simultaneously have positive equilibrium and stability when wage effect dominates (B > 0). Linear specification inadequate for limit cycles.

### Nonlinear Model - Local Stability (Sections 4-5)

**Derivative at Equilibrium:**
```
F'(u*) = 1 + u*g'(u*)/(1 + n)
```

**Stability Requires:**
```
|F'(u*)| < 1  ⟹  -2 < u*g'(u*)/(1 + n) < 0
```

**Critical Result:** With standard assumptions (g'(r) > 0, dw/dv > 0), we have u*g'(u*) > 0, so equilibrium is locally unstable.

**Interpretation:** Equilibrium is a repeller or at best a center (like basic Goodwin model). System doesn't converge to steady state.

### Global Dynamics - Limit Cycles

Despite local instability, nonlinearities create bounded oscillations:

1. **Boundedness from above:** As u decreases (v increases), wages rise sharply due to nonlinear wage function, reducing profits and accumulation. Prevents indefinite expansion.

2. **Boundedness from below:** As u increases (v decreases), wages fall, profits rise, accumulation accelerates due to nonlinear accumulation function. Prevents indefinite contraction.

3. **Result:** System trapped in bounded region, cycles emerge.

**Limit Cycle:** Closed orbit in phase space that is:
- Self-sustained (persists without external forcing)
- Stable (nearby trajectories converge to it)
- Independent of initial conditions (unique attractor)

### Hopf Bifurcation Analysis (Section 5)

**Bifurcation Condition:**
```
F'(u*) = -1  ⟹  u*g'(u*)/(1 + n) = -2
```

**Finding:** Cannot occur in capital-constrained regime since u*g'(u*) > 0.

**Implication:** Standard Hopf bifurcation doesn't explain limit cycle emergence in this model. Limit cycles arise from global nonlinear structure, not local bifurcation. Regime switching may play role.

---

## Accumulation Regimes (Section 4)

The paper identifies four distinct regimes of accumulation:

### Regime 1: Normal Accumulation
- Employment rate moderate: v < v̄ (some threshold below full employment)
- Wages rising moderately
- Profit rate sufficient for sustained accumulation
- Economy in capital-constrained regime
- Accumulation proceeds smoothly

### Regime 2: Relative Overaccumulation
- Employment rate high: v̄ < v < 1
- Wages rising rapidly due to tight labor market
- Profit rate falling but still positive
- Accumulation continues but slowing
- Still capital-constrained
- Approaching crisis

### Regime 3: Absolute Overaccumulation
- Employment rate at maximum: v = 1 (full employment)
- Wages at maximum
- Profit rate at minimum
- Accumulation slows dramatically or becomes negative
- Economy switches to labor-constrained regime
- Crisis/downturn

### Regime 4: Underaccumulation
- Employment rate low
- Wages depressed
- Profit rate high
- Accumulation accelerates
- Recovery phase
- Eventually returns to capital-constrained regime

**Cyclical Pattern:** Economy cycles through these regimes: Normal (1) → Relative overaccumulation (2) → Absolute overaccumulation (3) → Crisis/downturn → Underaccumulation (4) → Recovery → back to Normal (1).

---

## Numerical Examples and Dynamic Behaviors

### Example 1: Stable Limit Cycle (Page 171)

**Parameters:**
- γ = 2 (moderate wage nonlinearity)
- δ = 0.05 (moderate smoothness)
- Other parameters: σ=0.4, w₀=0.05, w₁=0.15, g_min=-0.1, g_max=0.3, r₀=0.2, n=0.02

**Results:**
- Equilibrium: u* ≈ 1.5 (v* ≈ 67%)
- Converges to stable limit cycle from various initial conditions
- Period ≈ 10 time periods
- Oscillations: u ∈ [1.2, 2.0], v ∈ [50%, 83%], g ∈ [-5%, 20%]

**Interpretation:** Self-sustained business cycle. Employment oscillates between 50% (recession) and 83% (boom). Accumulation alternates between expansion (20%) and contraction (-5%). Cycle independent of shocks or initial conditions.

### Example 2: Multiple Limit Cycles (Page 172)

**Parameter Changes from Example 1:**
- γ = 3 (increased wage nonlinearity)
- δ = 0.03 (decreased smoothness, steeper accumulation response)

**Results:**
- Two coexisting stable limit cycles
- Which cycle system approaches depends on initial condition
- Path dependence: history matters for long-run behavior

**Interpretation:**
- Economic bistability: economy can settle into different cyclical patterns
- Small disturbances might not change pattern, but large shocks could switch between cycles
- Hysteresis: past states influence future dynamics
- Policy implications: interventions might shift economy between different cyclical regimes

### Example 3: Chaotic Dynamics (Page 173)

**Parameter Changes from Example 2:**
- γ = 4 (further increased nonlinearity)
- δ = 0.02 (further decreased smoothness)

**Results:**
- Irregular, aperiodic oscillations over 200+ periods
- Sensitive dependence on initial conditions (SDIC)
- Bounded but non-repeating pattern
- Deterministic chaos

**Characteristics:**
1. **SDIC:** Tiny differences in starting point lead to dramatically different trajectories
2. **Aperiodicity:** No repeating cycle, ever-changing pattern
3. **Boundedness:** Doesn't diverge, remains in finite range
4. **Deterministic:** No randomness, purely from nonlinear structure

**Interpretation:**
- Economic cycles can appear random even with deterministic model
- Long-run prediction impossible (due to SDIC) even though model is deterministic
- Challenges traditional equilibrium and forecasting approaches
- Natural explanation for irregular business cycles without exogenous shocks

### Example 4: Bifurcation Diagram (Page 173)

**Method:** Vary δ from 0.01 to 0.1, hold other parameters fixed (γ = 4)

**Results - Period Doubling Cascade:**
- High δ (≈ 0.1): Stable limit cycle (few discrete points)
- Intermediate δ: Period-2 cycle (bifurcation 1)
- Lower δ: Period-4 cycle (bifurcation 2)
- Even lower δ: Period-8 cycle (bifurcation 3)
- Continued period doublings...
- Low δ (≈ 0.01-0.02): Chaotic regime (dense scatter)

**Interpretation:**
- Classic Feigenbaum route to chaos
- As accumulation function becomes steeper (lower δ), dynamics become more complex
- Systematic transition from simple to complex behavior
- Economic parameters determine whether cycles are regular or chaotic

### Example 5: Continuous vs Discrete Time Comparison (Page 174)

**Comparison:** Same parameter values, continuous time differential equation vs discrete time difference equation

**Findings:**

**Continuous Time Model:**
```
du/dt = u[g(u) - n]
```
- Smooth limit cycle
- Relatively simple dynamics

**Discrete Time - Small Time Step:**
- Closely approximates continuous time
- Similar smooth cycle

**Discrete Time - Moderate Time Step:**
- Overshooting and undershooting
- More angular cycle shape
- Some additional complexity

**Discrete Time - Large Time Step:**
- Pronounced overshooting
- Period doubling possible
- Can generate chaos even when continuous time has simple limit cycle

**Interpretation:**
- Discrete time not just technical detail - fundamentally affects dynamics
- Large discrete steps (slow adjustment) → more complex behavior
- Realistic for economics: decisions made quarterly, annually, not continuously
- Additional complexity from discrete time may help explain real cycle irregularity

---

## Key Theoretical Contributions

### 1. Endogenous Cycles Without Exogenous Shocks

**Traditional View:** Business cycles require random shocks (technology shocks, policy shocks, etc.)

**This Paper:** Nonlinear deterministic mechanisms alone can generate:
- Regular cycles (limit cycles)
- Irregular cycles (chaos)
- No randomness needed

**Implication:** Internal structure of capitalist economy may be sufficient to explain cyclical behavior.

### 2. Rich Taxonomy of Dynamics

Demonstrates that single model framework can exhibit:
- Stable equilibrium (with certain parameters)
- Stable periodic cycles (limit cycles)
- Multiple coexisting cycles (bistability)
- Aperiodic chaos
- Transitions via bifurcations

**Implication:** Historical variability in cycle patterns could reflect parameter changes rather than fundamental structural changes.

### 3. Role of Discrete Time

Shows discrete time formulation introduces:
- Overshooting
- Period doubling
- Chaotic dynamics

**Implication:**
- Continuous time models may underestimate dynamic complexity
- Discrete time more realistic for economic decision-making
- Timing of adjustments matters for dynamics

### 4. Classical Mechanisms Can Generate Complexity

Nonlinearities in:
- Wage determination (labor market conflict)
- Investment behavior (profit-driven accumulation with constraints)

These classical mechanisms, properly specified, generate modern complex dynamics.

**Implication:** Reconciles classical political economy with modern nonlinear dynamics/chaos theory.

### 5. Path Dependence and Hysteresis

Multiple limit cycles demonstrate:
- History matters (initial conditions determine long-run pattern)
- Economy can be "trapped" in different cyclical regimes
- Large shocks might shift between regimes

**Implication:** Policy interventions could have persistent effects by shifting economy between attractors.

---

## Methodological Innovations

### 1. Discrete Time Formulation

Most growth cycle models (including Goodwin 1967) use continuous time. This paper:
- Formulates in discrete time from outset
- Shows discrete time creates additional complexity
- More realistic for economic planning horizons

### 2. Nonlinear Function Specifications

Goes beyond linearization:
- Power functions for wages: w(v) = w₀ + w₁v^γ
- Logistic functions for accumulation: bounded S-shaped response
- Captures economic constraints and accelerating effects

### 3. Numerical Methods

Extensive use of:
- Numerical iteration of difference equations
- Phase plane visualization
- Bifurcation diagrams
- Time series analysis

Demonstrates need to go beyond analytical methods for nonlinear systems.

### 4. Parameter Variation Analysis

Systematic exploration of parameter space:
- Shows how changing γ, δ affects dynamics
- Maps transition from order to chaos
- Connects model behavior to economic interpretation

---

## Economic Interpretation and Mechanisms

### The Cyclical Mechanism

**Upswing (Boom Phase):**
1. Low initial employment (high u, low v)
2. Low wages → high profits
3. High accumulation (rapid capital growth)
4. Capital grows faster than labor supply
5. Employment rate rises (u falls, v rises)
6. Eventually wages begin rising, profits falling
7. But momentum carries expansion further...

**Peak and Reversal:**
8. Employment reaches high levels
9. Wage acceleration due to nonlinearity
10. Profits squeezed
11. Accumulation slows sharply
12. May reach absolute overaccumulation (v → 1)

**Downswing (Recession Phase):**
13. Accumulation below labor growth rate
14. Employment falls (u rises, v falls)
15. Wages decline
16. Profits begin recovering
17. But negative momentum continues initially...

**Trough and Recovery:**
18. Employment very low
19. Wages depressed
20. Profits high
21. Accumulation accelerates
22. Cycle begins anew

**Key Insight:** Nonlinearities create overshooting in both directions, generating sustained oscillations rather than smooth convergence.

### Role of Absolute Overaccumulation

Classical concept formalized:
- Accumulation can proceed "too far"
- Hits labor supply constraint
- Wages explode, profits collapse
- Forces contraction

This acts as upper bound on expansion, essential for bounded cycles.

### Profit-Wage Conflict

At heart of dynamics:
- Wages and profits inversely related (given technology σ, a)
- Employment mediates: high v → high w → low r
- Accumulation depends on profits
- But accumulation affects employment
- Creates feedback loop driving cycles

---

## Limitations and Caveats Noted by Authors

### 1. Simplified Framework

Model abstracts from:
- Technological change
- Monetary sector (prices, credit, interest rates)
- Open economy (trade, capital flows)
- Government sector (fiscal policy, taxation)
- Multiple sectors or industries
- Heterogeneous agents

### 2. Parameter Calibration

Examples use hypothetical parameter values:
- Not estimated from data
- No empirical validation
- Illustrative rather than predictive

### 3. Regime Switching

Analysis focuses on capital-constrained regime:
- Labor-constrained regime less developed
- Transitions between regimes not fully analyzed
- May affect bifurcation analysis

### 4. Chaotic Dynamics - Interpretation

While chaotic dynamics demonstrated:
- Economic interpretation of chaos debatable
- Is extreme sensitivity realistic?
- Measurement error might obscure chaos in data

---

## Future Research Directions Suggested

The paper concludes by suggesting extensions:

1. **Incorporating Technological Change**
   - Labor productivity growth
   - Capital-saving technical progress
   - Induced innovation

2. **Adding Monetary Sector**
   - Price dynamics
   - Credit and debt
   - Interest rates and financial constraints
   - Potential for financial instability

3. **Open Economy Aspects**
   - International trade
   - Capital mobility
   - Exchange rate dynamics

4. **Empirical Estimation**
   - Calibrate parameters to real data
   - Test model predictions
   - Compare with observed business cycles

5. **Policy Implications**
   - Counter-cyclical policies
   - Can policy eliminate cycles or just dampen?
   - Optimal policy in chaotic regime

---

## Connections to Broader Literature

### Growth Cycle Models
- Goodwin (1967) - foundation
- Subsequent extensions adding nonlinearities
- This paper adds discrete time dimension

### Chaos Theory in Economics
- Early 1980s: emerging application of chaos theory to economics
- May (1976) - chaos in simple ecological models
- This paper applies to macro/growth context

### Classical Economics
- Marx - crisis theory, overaccumulation
- Ricardo - distribution and accumulation
- Formalizes classical insights with modern math

### Business Cycle Theory
- Alternative to RBC (Real Business Cycle) models
- Endogenous cycles vs exogenous shocks
- Nonlinear deterministic vs stochastic linear

---

## Significance and Impact

### Theoretical Significance

1. **Bridges Classical and Modern:** Connects classical political economy concepts (profit-wage conflict, overaccumulation) with cutting-edge nonlinear dynamics and chaos theory.

2. **Demonstrates Complexity from Simple Rules:** Shows that relatively simple economic mechanisms, when properly nonlinear, can generate extraordinarily complex dynamics.

3. **Challenges Equilibrium Paradigm:** Provides alternative framework where disequilibrium, cycles, and chaos are inherent, not aberrations.

4. **Enriches Growth Cycle Literature:** Extends Goodwin framework beyond center/neutral stability to richer set of attractors.

### Methodological Significance

1. **Discrete Time:** Demonstrates importance of discrete vs continuous time formulation.

2. **Numerical Analysis:** Shows necessity of computational methods for nonlinear systems.

3. **Parameter Space Exploration:** Systematic mapping of how dynamics change with parameters.

### Policy Implications

1. **Limits to Prediction:** Chaotic dynamics imply fundamental limits to long-run forecasting even with perfect model.

2. **Nonlinear Policy Effects:** Small parameter changes can cause qualitative shifts (bifurcations) in behavior.

3. **Path Dependence:** Multiple attractors mean history and timing of interventions matter.

4. **Stabilization Challenges:** If cycles are endogenous and potentially chaotic, traditional stabilization policy may be ineffective or counterproductive.

---

## Mathematical and Technical Summary

### Core Equation
Single nonlinear difference equation in inverse employment rate:
```
u(t+1) = u(t) · [(1 + g(u(t)))/(1 + n)]
```
where g(u) captures combined effects of wage-profit-accumulation nexus.

### Equilibrium
u* such that g(u*) = n

### Local Stability
Equilibrium generically unstable: F'(u*) > 1

### Global Dynamics
Bounded oscillations due to:
- Nonlinear wage function (bounding from above)
- Bounded accumulation function (bounding from below)

### Bifurcations
Period-doubling cascade as δ decreases (accumulation function becomes steeper)

### Chaos
For sufficiently strong nonlinearities (high γ, low δ):
- Positive Lyapunov exponent (implied)
- Sensitive dependence on initial conditions
- Aperiodic bounded dynamics

---

## Data and Tables Summary

**No empirical data presented.** All numerical examples use hypothetical parameter values.

**Four CSV tables created from examples:**

1. **example_1_parameters.csv** - Stable limit cycle (18 parameters/results)
2. **example_2_parameters.csv** - Multiple limit cycles (10 parameters)
3. **example_3_parameters.csv** - Chaotic dynamics (13 parameters)
4. **bifurcation_parameters.csv** - Period doubling analysis (11 parameters)

---

## Figures Summary

**Five figures referenced** (not reproduced in PDF, only described):

1. **Figure 1:** Phase diagram showing stable limit cycle in (u,g) space - Example 1
2. **Figure 2:** Phase diagram with two coexisting limit cycles - Example 2
3. **Figure 3:** Time series of u(t) showing chaotic behavior - Example 3
4. **Figure 4:** Bifurcation diagram, δ on x-axis, long-run u values on y-axis
5. **Figure 5:** Comparison of continuous vs discrete time phase diagrams

---

## References Summary

**Seven references** spanning 1925-1976:

**Foundational:**
- Lotka (1925), Volterra (1926) - predator-prey mathematics
- Samuelson (1939), Hicks (1950) - business cycle theory

**Key Economics:**
- Goodwin (1951) - nonlinear accelerator
- Goodwin (1967) - growth cycle model

**Chaos Theory:**
- May (1976) - chaos in simple models

**Notable:** Interdisciplinary (biology, economics, mathematics), relatively short reference list suggesting early contribution to field.

---

## Conclusion

This paper makes important contributions to understanding economic dynamics by:

1. **Demonstrating** that classical growth mechanisms with realistic nonlinearities can generate endogenous, self-sustained cycles without exogenous shocks.

2. **Showing** that discrete time formulation can produce richer dynamics than continuous time, including period doubling and chaos.

3. **Illustrating** a systematic transition from simple periodic behavior to chaotic dynamics through parameter variation.

4. **Providing** a framework that reconciles classical political economy (profit-wage conflict, overaccumulation) with modern nonlinear dynamics and chaos theory.

5. **Challenging** both neoclassical equilibrium frameworks and simple stochastic shock-based business cycle models.

The work represents an important early application of chaos theory to macroeconomics and growth theory, demonstrating that complex, irregular business cycles can emerge from deterministic economic mechanisms. This has profound implications for economic forecasting, policy design, and our fundamental understanding of capitalist dynamics.

The paper's emphasis on discrete time, nonlinear specifications, and numerical methods also points toward future directions in macroeconomic modeling, presaging later developments in computational economics and complexity theory.

---

**Document Length:** 23 pages
**Equations:** 75 numbered equations
**Figures:** 5 referenced
**Tables/Examples:** 4 numerical examples
**References:** 7 citations
**Mathematical Level:** Advanced (difference equations, nonlinear dynamics, bifurcation theory, chaos theory)
**Economic Level:** Graduate/research (assumes familiarity with growth theory and classical economics)
