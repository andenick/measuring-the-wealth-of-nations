# Full Transcription - [2002] Matthews: An Econometric Model of the Circuit of Capital

**Source**: Matthews, Peter Hans (2000). "An Econometric Model of the Circuit of Capital." *Metroeconomica* 51:1, pp. 1-39.
**Extraction Date**: October 23, 2025
**Document Type**: Journal Article (39 pages)
**HDARP Protocol**: Part 4 of 4 - Complete Transcription

---

## Publication Information

**Journal**: Metroeconomica 51:1 (2000) 1-39
**Publisher**: Blackwell Publishers Ltd 2000, 108 Cowley Road, Oxford OX4 1JF, UK and 350 Main Street, Malden, MA 02148, USA
**Author**: Peter Hans Matthews, Middlebury College, Vermont
**Submission**: December 1993; revised June 1998

---

## Abstract

The circuit of value outlined in the second volume of Marx's *Capital* provides a coherent framework for the characterization of macroeconomic phenomena from a classical perspective. This paper builds on Foley's (*Journal of Economic Theory*, 28 (1982), pp. 300-319) formal reconstruction of the circuit to derive estimable forms for its three critical mechanisms: the production, realization and recommittal lags. The entire model is then estimated for the United States over the period 1948-89 on the basis of the Shaikh and Tonak (*Measuring the Wealth of Nations: The Political Economy of National Accounts*, Cambridge University Press, New York, 1995) data set, and the results are used to explore a number of current controversies, including (on the basis of simulation exercises) the consequence of various deficit reduction proposals.

---

## 1. INTRODUCTION

The identification of labor as the wellspring of value remains a touchstone of the classical tradition, but the principle is now (often) articulated in macroeconomic terms: the annual flow of value added is understood to be the embodiment of all the "simple, abstract and productive labor" expended on its production. A fraction of this labor is current, of course, but the remainder represents the release of labor "petrified" in the form of constant capital. The observation that prices, not labor values, constitute the *de facto* metric of capitalist economies then raises familiar (but still difficult) questions about their connection.

### The New Solution/New Interpretation

In the recent contributions of Dumenil (1980), de Vroey (1981), Lipietz (1982) and Foley (1982a, 1982b, 1986b), the resolution of this "transformation problem" at a macroeconomic level turns on the redefinition of the "value of money" as the ratio of total productive labor time to nominal (dollar) value added. While the "new solution" or, as some have called it, "new interpretation" breaks with the standard "dual systems" perspective on the problem, some of its most basic features can nevertheless be illustrated with a simple Leontief model.

**Leontief Model Setup**: Consider n constant returns industries each producing a distinct and perishable output with labor and some (perhaps all) of the n commodities combined in fixed proportions. Let:
- **A** = [a_{i,j}] denote the n × n input-output matrix
- **l** = [l_j] the 1 × n row vector of per unit labor requirements
- **x** = [x_i] and **y** = [y_i] the n × 1 column vectors of total and net outputs (assumed known)
- **p** = [p_j] the 1 × n row vector of prices that equalizes rates of profits across sectors when the nominal price of labor power is w

So that: **p** = (1 + π)[**pA** + w**l**]

If the net product is the embodiment of all the labor expended in production, the vector of individual labor values **v** must be such that **v**:**y** = **l**:**x** which, since the net product **x** is equal to [**I** - **A**]^(-1)**y**, implies that **v** = **l**[**I** - **A**]^(-1).

**Value of Money**: The value of money m can then be defined as the ratio of inner products **l**:**x**/(**p**:**y**) or **v**:**y**/(**p**:**y**) and becomes a conversion factor of sorts: the product of m and nominal net product is, from their respective definitions, its labor value, and the product of m and nominal profits is surplus value (1 - mw)**v**:**y**, where ω = mw is the "value of labor power", the proportion of the value of net product that returns to productive workers in the form of labor income.

The equivalence of profits (the difference between net nominal income and total labor costs) and surplus value, which fails to obtain in most resolutions of the transformation problem, follows from two simple equalities: m**p**:**y** = **v**:**y** and mw**l**[**I** - **A**]^(-1)**y** = mw**v**:**y**.

The conversion of other nominal stocks and flows into their labor time equivalents is also possible, of course, even if their interpretation is (often) more complicated.

### Operationalism and Data Requirements

It comes as no surprise, then, that advocates of the new solution have drawn particular attention to its apparent **operationalism**: in principle, the specification, estimation and simulation of distinctly classical econometric models requires little more than a complete set of national income and product accounts (NIPA) and the prior construction of an m_t series. This said, the "recontextualization" of published NIPA or input-output data often proves difficult in practice, even if Shaikh and Tonak's recent *Measuring the Wealth of Nations* (1995) has alleviated the problem.

### The Circuit of Capital Framework

This paper considers one such model, Foley's (1982b, 1986b) formal account of the evolution of macroeconomic time series as the "motion of value" through a "circuit of capital", a characterization based on the second volume of Marx's (1885) *Capital*.

**The Classical Circular Flow** starts with capitalists' expenditure of labor value, "immobilized" in the form of money capital, on the labor power and the means of production needed to meet anticipated demand and/or maximize profits/surplus value. Because some part of the value committed to production assumes the form of durable capital and is therefore released over several periods, the resultant **"production lag"** modulates the flow of value in the circuit.

The subsequent "petrification" of this flow as stocks of finished commodities available for sale—an outcome that is neither instantaneous nor automatic—leads to the circuit's second critical mechanism, the **"realization lag"**, a precursor of the effective demand mechanism estimated here.

Under normal conditions, the flow of "realized value" will nevertheless exceed the value of advances on constant and variable capital and the difference, surplus value, will be distributed to unproductive workers, capitalists, landowners and the state as salaries, profits, rents and tax revenues. A substantial portion of this surplus is consumed but the remainder is returned, with the flow of "replacement value", over time to production, so that the **"recommittal lag"** closes the circuit.

### Paper Structure

What follows is a first, tentative characterization of the production, realization and recommittal mechanisms in the United States over the period 1948-89, the period for which Shaikh and Tonak (1995) have constructed their accounts.

- **Section 2**: Sketches a modified discrete-time version of the Foley (1986b) model and reviews its most important implications
- **Section 3.1**: Constructs a candidate m series and explores its statistical properties, including presence of a possible "unit root"
- **Section 3**: Core section concerns specification of estimable forms of the circuit's principal components and their estimation via nonlinear and autocorrelation-consistent generalized method of moments (GMM) techniques
- **Section 4**: Considers applications—calculation of maximum rate of balanced expansion and implied stock-flow relations—and on the basis of simulation exercises, reaches tentative but provocative conclusions about transmission of macroeconomic disturbances and consequences of various deficit reduction policies
- **Appendix**: Definitions and data sources

---

## 2. THE CIRCUIT OF CAPITAL MODEL

### 2.1 The Production Mechanism

With minor modifications to the notation in Foley (1986b), the discrete-time "production function" can be expressed as the convolution:

**Q_t = Σ_{j=-∞}^t a_{t-j,j} C_j**  ...(2.1)

Where:
- **Q_t** is the flow of production value in period t
- **C_j** is the flow of value recommitted to production in period j < t (sum of expenditures on variable and constant capital)
- **a_{t-j,j}** ∈ [0,1] is the proportion of capital spending in period t-j that appears as finished output j periods later
- Σ_{j=-1}^t a_{t-j,j} = 1 for all t

The evolution of the stock of productive capital K_t (one of the three forms in which value is immobilized outside the circuit) is then equal to ΔK_t = C_t - Q_t.

### 2.2 The Realization Mechanism

The flow of sales or realized value in period t, denoted S_t, can be expressed:

**S_t = Σ_{j=-∞}^t h_{t-j,j} P_j**  ...(2.2)

Where:
- **P_t** = Σ_{j=-1}^t a_{t-j,j}(1 + q_j)C_j is the value of period j production after the imposition of a "point of production" mark-up q_j

The distribution h_{t-j,j} is itself a reflection, however, of the recommittal (and other) decisions of capitalists and workers, and can be "endogenized" as follows:

**S_t = (1 - k_t)C_t + Σ_{j=-∞}^t b_{t-j,j} k_j C_j + Σ_{j=-∞}^t c_{t-j,j}(1 - p_j)S²_j + B¹_t**  ...(2.3)

Where:
- **S²_j** is the flow of surplus value in period j
- **B¹_t** is the flow of state and household spending in period t financed with new debt
- **p_j** is the proportion of surplus value S²_j in period j that will (over time) be recommitted to production
- **k_j** is the ratio of variable to total capital spending in period j
- **b_{t-j,j}** ∈ [0,1] is the proportion of variable capital advanced in period t-j that materializes as workers' demands for consumption in period t
- **c_{t-j,j}** ∈ [0,1] is the fraction of surplus value capitalists set aside for consumption in period t-j that becomes effective j periods after, in period t
- Σ_{j=-1}^t b_{t-j,j} = Σ_{j=-1}^t c_{t-j,j} = 1

The first term in (2.3) is therefore the current value of capitalists' expenditures on the means of production, while the second and third are the values of the demands for consumption on the part of workers and capitalists—a classical statement of the effective demand principle.

Movements in the level of inventories or "commercial capital" M_t are then determined as ΔM_t = Q_t - S¹_t, where S¹_t = S_t - S²_t is the flow of "cost replacement" value or classical depreciation, and the second form in which value is petrified.

### 2.3 Underconsumption and External Stimuli

It is not difficult to show that without the additional and external stimuli that new capitalist borrowing B¹ and/or new state and household borrowing B² (see below) provide, effective demand would be insufficient to sustain an increasing flow of value through the circuit. While the extent to which Marx anticipated the logic of underconsumption continues to be debated, Robinson notes in her introduction to *The Accumulation of Capital* (1913) that Luxemberg's statement, explicit if incomplete, of the effective demand principle was rooted in her studies of the circuit's internal properties.

### 2.4 The Recommittal Mechanism

The specification of the recommittal mechanism then closes the circuit. The value of capital advances C_t in period t is determined as:

**C_t = Σ_{j=-∞}^t d_{t-j,j} S¹_j + Σ_{j=-∞}^t d_{t-j,j} p_j S²_j + B²_t**  ...(2.4)

Where:
- **B²_t** is the value of capital expenditures financed with new debt
- **d_{t-j,j}** ∈ [0,1] is the fraction of the period j flow S¹_j + p_j S²_j recommitted to production in period t
- Σ_{j=-1}^t d_{t-j,j} = 1 for all t

Since S¹_t = S_t - S²_t, the recommittal process can also be expressed as:

**C_t = Σ_{j=-∞}^t d_{t-j,j} S_j - Σ_{j=-∞}^t (1 - p_j) d_{t-j,j} S²_j + B²_t**  ...(2.5)

Where fluctuations in the stock of "financial capital" F_t in the hands of capitalist firms—understood in the classical sense of the word—follow ΔF_t = S¹_t + p_t S²_t - C_t + B²_t.

---

## 2.5 Balanced Growth Analysis

Foley (1982b, 1986b) restricts his analysis of the circuit's dynamic properties to the special case of constant growth and stationary lag distribution. Under these conditions, the production mechanism (2.1) becomes:

**Q_0 = Σ_{j=-∞}^t (1 + g)^{-(t-j)} a_{t-j} C_0**  ...(2.6)

Where g is the rate of growth of value through the circuit and the choice of baseline t = 0 is arbitrary but unimportant. Given the transformation of variables t' = t - j, (2.6) can be rewritten as:

**Q_0 = a*(g) C_0**  ...(2.7)

Where:

**a*(g) = Σ_{t'=0}^∞ (1 + g)^{-t'} a_{t'}**  ...(2.8)

For similar reasons, the realization (2.3) and recommittal (2.5) lags can be expressed as:

**S_0 = {1 - k[1 - b*(g)]} C_0 + (1 - p)c*(g) S²_0 + B¹_0**  ...(2.9)

And:

**C_0 = d*(g)[S_0 - (1 - p)S²_0] + B²_0**  ...(2.10)

Where, of course:

**b*(g) = Σ_{t'=0}^∞ (1 + g)^{-t'} b_{t'}**  ...(2.11a)

**c*(g) = Σ_{t'=0}^∞ (1 + g)^{-t'} c_{t'}**  ...(2.11b)

**d*(g) = Σ_{t'=0}^∞ (1 + g)^{-t'} d_{t'}**  ...(2.11c)

### Equilibrium Conditions

As Foley (1982b, 1986b) then notes, equations (2.6), (2.9) and (2.10) constitute a system that is homogeneous of degree one in its flow variables for which C_0 = 1 is a sensible normalization:

**Q̄_0 = a*(g)**  ...(2.12)

**S̄_0 = {1 - k[1 - b*(g)]} + (1 - p)c*(g)S̄²_0 + B̄¹_0**  ...(2.13)

**1 = d*(g)[S̄_0 - (1 - p)S̄²_0] + B̄²_0**  ...(2.14)

Where Q̄_0, S̄_0, S̄¹_0, S̄²_0, B̄¹_0 and B̄²_0 are now understood to be relative (to C_0) flows.

### The Accumulation Mode

Given the initial values of new borrowings B¹_0 and B²_0, equations (2.13) and (2.14) can be analyzed as a proper subsystem. Letting q denote the steady-state mark-up and substituting [q/(1 + q)]S_0 for S²_0 in both equations yields:

**S̄_0 = [(1 + q){1 - k[1 - b*(g)] + B̄¹_0}] / [1 + q[1 - c*(g)(1 - p)]]**  ...(2.15)

**S̄_0 = [(1 + q)(1 - B̄²_0)] / [(1 + pq)d*(g)]**  ...(2.16)

Which, after setting the two equal and rearranging terms, produces:

**[1 - k[1 - b*(g)] + B̄¹_0] / [1 + q[1 - c*(g)(1 - p)]] = [1 - B̄²_0] / [(1 + pq)d*(g)]**  ...(2.17)

An expression that allows for the comparison of equilibrium growth paths.

### Interpretation: Mark-up and Growth Rate

The interpretation of (2.17) is perhaps best illustrated with a pair of examples drawn from Foley (1982b).

**Example 1**: Consider first the simple case in which the composition of costs k, recommittal rate p and new borrowings B¹_0 and B²_0 are all predetermined. Since b*(g), c*(g) and d*(g) are all decreasing functions of the rate of growth g, it follows that the equilibrium mark-up q and the accumulation mode g (the value of g consistent with (2.17)) are positively related. This implies that the maximum rate of balanced and feasible growth depends in some measure on the outcome of the struggle between workers and capitalists over the size of the mark-up, a standard result within the literature on theories of structural inflation.

**Example 2**: Alternatively, consider the case in which b*(g) and c*(g) are both equal to one and B¹_0 is equal to zero, a situation in which re-spending is instantaneous and borrowing for current consumption is not possible. The equilibrium condition (2.17) is then:

**B̄²_0 = 1 - d*(g)**  ...(2.18)

Which implies that the accumulation mode g is an increasing function of the rate of new business borrowing B²_0 and underscores the fundamental role of corporate finance in capitalist development. The notion that capitalists' access to new pools of credit was an essential part of the process of "primitive accumulation"—one that Schumpeter (1934) advances in quite different terms—deserves more attention within the heterodox literature.

---

## 3. ESTIMATION OF THE MODEL

### 3.1 The Value of Money

The transformation of nominal flows into flows of labor value requires the prior construction of a value of money series m_t. Recall that for the paths considered in Lipietz (1982) and Ehrbar (1990), m is the ratio of the expenditure of simple, abstract and social labor to the nominal value of the net product. There is no reason to suppose, however, that this definition holds out of equilibrium: the introduction of new methods of production, for example, undermines the equivalence between value and labor inasmuch as some of the labor released from inefficient and/or obsolete machines will be unproductive in the Marxian sense.

**Candidate Series**: The candidate series m_t = N_t/Y'_t, where N_t is the number of hours of productive labor expended in period t and Y'_t is Shaikh and Tonak's (1995) "Marxian net value added" in current dollars, must therefore be considered an approximation of sorts.

**Behavior of the Value of Labor Power**: The implied behavior of the value of labor power ω_t = m_t w_t, where w_t is the current dollar price of labor power, is pictured in figure 1. Given variations in the definitions of productive and unproductive labor, the size of ω_t is consistent with previous studies but less volatile than some have found, especially if one "purges" the series of the effects of the secular (?) decline in the ratio of productive to total hours PWR_t, as the residuals from a simple least squares regression of ω_t on PWR_t (the other series plotted there) indicate. Even without this correction, however, some would consider the relative (over shorter horizons) invariance of the value of labor power one of the "stylized facts" of classical macroeconomics.

### Unit Root Tests

This said, recent advances in time series methods allow (indeed, almost compel) the primitive series ω_t to be tested for the presence of a so-called "unit root". As table 1 reveals, the unit root hypothesis (with or without drift) cannot be rejected on the basis of the nonparametric Phillips-Perron (1988) tests for an augmented Dickey-Fuller (1981) regression.

**Interpretation**: How should this result be understood? The value of labor power would exhibit the properties of a random walk (with or without some downward drift) if, within certain bounds, short-run "innovations" in the power of workers to obtain favorable terms are somehow "folded into" the evolution of labor market contracts. The presence of a negative drift term—there is perhaps less econometric support for its inclusion than casual inspection of the data would hint—is consistent with a stochastic version of the Marxian, if not Marx's own, characterization of the laws of capitalist motion.

**Alternative Explanations**: Given the limited power of such tests, however, other (more traditional) explanations of the data should be considered. Some of the decline in the value of labor power could reflect (or be reflected in) the concomitant rise in the proportion of unproductive workers, itself the result of the evolution of the social structure of accumulation. Some would speculate, for example, that increases in real (i.e. dollar deflated) output per worker have allowed capitalists to return a smaller fraction of each hour of labor to productive workers, and to hire increased numbers of unproductive workers.

There is also some evidence that fluctuations in both "actual" and "residual" ω_t are connected to variations in the (relative) size of the unemployment pool, the corps of Marx's "reserve army", and their effects on the balance of power in the market(s) for labor power. The increased (relative to trend) net demand for domestic labor in the first half of the 1950s and the second half of the 1960s, for example, coincided with sharp (within a narrow band, however) increases in the value of labor power, increases that were in both cases "whittled down" as jobless rates returned to "normal". The reductions in the value of labor power in 1974 and from 1980 onward also call for attention: it seems reasonable to infer that the downward pressure on productive workers' real incomes cannot be explained in terms of the "productivity slowdown" alone, since the share of net income which returns to productive workers has decreased as well. The source(s) of this shift in the balance of labor market power remains a matter of active research.

---

### 3.2 The Temporal Structure of Production

There are several obstacles, both empirical and theoretical, between the characterization of production in (2.1) and an estimable form. The connection between the flow of production value Q_t at cost (for which reliable data are not available) and the same flow measured at market prices is:

**P_t = Q_t + Σ_{j=-∞}^t q_j a_{t-j,j} C_j = Σ_{j=-∞}^t (1 + q_j) a_{t-j,j} C_j**  ...(3.2.1)

Where, as before, q_j is the "point of production" mark-up. Shaikh and Tonak's (1995) "total value" series is an obvious measure of P_t, but its construction is a delicate one, so that it becomes sensible to consider also the expression of (3.2.1) in terms of the more robust value added Y_t series.

If value added is understood as the sum of variable capital expenditures (past and present) that materialize in the current period and the surplus value attributable to the materialization of current and previous capital (both constant and variable) expenditures, Y_t can (also) be expressed as:

**Y_t = Σ_{j=-∞}^t a_{t-j,j} W_j + Σ_{j=-∞}^t a_{t-j,j} q_j C_j**
**= Σ_{j=-∞}^t a_{t-j,j}(1 + q_j) W_j + Σ_{j=-∞}^t a_{t-j,j} q_j I_j**  ...(3.2.2)

Where W_j = k_j C_j and I_j = (1 - k_j)C_j.

**Note**: (3.2.1) and (3.2.2) also reveal the connection between P_t and Y_t: Y_t = P_t - Σa_{t-j} I_j, but neither (3.2.1) nor (3.2.2) models the *decision* to produce; both are (no more, but no less than) representations of the "temporal structure" of production, an account of the "pattern(s) of materialization".

### Parametrization Strategy

From a heuristic standpoint, the parametrization of either can be considered a two-step process:

1. **Shape of distribution**: Is it reasonable to suppose that the proportion of capital spending in period t-j that materializes as finished output in period t is a decreasing function of j? Or is the distribution hump-shaped?

2. **Evolution of distribution**: Does the distribution change over time? An economic historian who suspects that production has become more roundabout over time would expect the proportion of capital expenditures to be valorized within a few periods to fall from one period to the next.

### Koyck Specification

Suppose for the moment that the coefficient distribution and mark-up are both invariant: a_{t-j,j} = a_{t-j} and q_j = q for all j. This restriction, which transforms (3.2.1) and (3.2.2) from pseudo-identities into near estimable forms, is not inconsistent with innovation, but assumes that the diffusion of new methods etc. does not alter the distribution of coefficients and forces short(er) term fluctuations to be subsumed within the error process.

Because it also seems reasonable to suppose that the coefficients will decrease in t-j, the specification of a constant rate of decrease λ_a ∈ (0,1) is a natural first working hypothesis. This is the standard Koyck specification, where the a priori restriction on the sum of the coefficients implies that a_0 = 1 - λ_a, so that a_{t-j} = (1 - λ_a)λ_{a}^{t-j}.

**Interpretation**: A fraction 1 - λ_a of the labor value of capital expenditures C_j in period j will materialize as finished output within the same period, a fraction (1 - λ_a)λ_a will materialize in the subsequent period, (1 - λ_a)λ_{a}^2 will materialize two periods later, and so on. In other words, a fraction (1 - λ_a)(1 + λ_a + λ_{a}^2 + ... + λ_{a}^{t-j}) of the flow of capital expenditures C_j in period j will materialize as finished output before the end of the tth period, with a median production lag equal to log(0.5)/log(λ_a) periods.

This allows (3.2.2), for example, to be rewritten:

**Y_t = (1 + q)(1 - λ_a) Σ_{j=-∞}^t λ_{a}^{t-j} W_j + q Σ_{j=-∞}^t λ_{a}^{t-j} I_j + u¹_t**  ...(3.2.3)

Or, in terms of the polynomial lag operator L:

**Y_t = (1 + q)(1 - λ_a)(1 - λ_a L)^{-1} W_t + q(1 - λ_a)(1 - λ_a L)^{-1} I_t + u¹_t**  ...(3.2.4)

Where u¹_t is a random error term that is almost certain to be autocorrelated and (perhaps) heteroskedastic as well. Multiplication of both sides by 1 - λ_a L leads to the estimable form:

**Y_t = λ_a Y_{t-1} + (1 + q)(1 - λ_a) W_t + q(1 - λ_a) I_t + v¹_t**  ...(3.2.5)

Or, in the case of (3.2.1):

**P_t = λ_a P_{t-1} + (1 - λ_a)(1 + q) C_t + ε¹_t**  ...(3.2.6)

Where v¹_t = u¹_t - λ_a u¹_{t-1} etc.

### GMM Estimation

Because the values of W_t and I_t are determined within the circuit, the estimation of (3.2.5) or (3.2.6) requires a two-step procedure. The uncertain structure of the covariance matrix E(v¹v¹ᵀ) = Ω₁ complicates the choice of instruments, however. A pair of nonlinear GMM estimators, the autocorrelation consistent estimators described by Newey and West (1987) and Andrews (1992), are used here, with a constant, trend, squared trend and current and past values of both B¹ and B² as (conservative) instruments.

**Rationale for Instruments**: The inclusion of B¹ and B² in the common instrument set calls for some comment: while it seems reasonable to suppose prima facie that neither will be correlated with disturbances to the "production function"—in the absence of a permanent production/sales equilibrium, "feedback" from the total value P_t or value added Y_t to debt-financed expenditures (of either kind) should be tenuous—their further use in the estimation of the effective demand and recommittal equations calls for a specification test.

### Estimation Results

The results, and a further description of the estimators, are found in table 2.

**Key Findings**:
- **λ̂_a = 0.395** (Newey-West, Y_t specification): Implies 60% of capital expenditures C_t transform into finished output over the same period, with median production time of 0.746 years (9 months)
- **q̂ = 0.540**: Implies each hour/dollar spent on production returns more than 1.5 hours of realized value; more than a third (q/(1+q) = 0.351) of labor time valorized becomes surplus value

The estimates of q associated with (3.2.5) and (3.2.6) are not far apart, but there is a substantial difference between the estimates of λ_a. There is some outside evidence about the size of q which supports the choice of (3.2.5) as the more reliable specification. Foley (1986a, p. 46) finds that q = 0.40 is a reasonable first approximation based on 1974 Census of Manufactures data, though comparisons are difficult due to different sector coverage and definitions of productive labor.

The J statistics (Hansen (1982), White (1993)) of the overidentification restrictions, distributed χ² with 5 degrees of freedom in the limit, reveal that for either estimator the null hypothesis that the coefficients on the excluded variables are indeed zero cannot be rejected at the 95 percent confidence level.

### Alternative Measures of Mark-up

The existence of a pair of alternative (and variable) measures of q provides another perspective on these results. Foley (1986b) first defines the mark-up as the product of two basic Marxian aggregates: the rate of surplus value or exploitation e¹_t (defined as (1 - m_t w_t)/(m_t w_t) where ω_t = m_t w_t is the value of labor power) and the composition of costs k_t.

**Rate of Surplus Value**: The series e¹_t and several variants are plotted in figure 2. Given the time series caveats, the rate of surplus value seems to have risen, with periodic interruption(s), over the post-war era, from 180 percent in 1948 to 240 percent in 1989, which is consistent with Marx's "laws of motion" for technologically progressive economies.

**Composition of Costs**: The behavior of k_t, captured in figure 3, is also prima facie consistent with Marx's predictions, even if much of the decline is concentrated within the 1970s.

The pertinent questions are: (1) does the behavior of k_t "offset" the behavior of e¹_t, in the limited sense that the specification of a constant q becomes reasonable, and (2) if so, is the GMM estimate q̂ = 0.540 a plausible one?

The first can be answered in the affirmative, despite some important qualifications: fluctuations in q¹_t = k_t e¹_t (plotted in figure 4) are confined to a smallish band over much of the sample period, even if there is recent evidence that capitalists have been able to raise their mark-ups relative to the constant benchmark. Given these fluctuations, however, q̂ = 0.540 is a reasonable estimate.

The other series, q²_t in figure 4, is based on the national accounts themselves, and is defined as the ratio of S²_t to S¹_t = S_t - S²_t. It mirrors the behavior of q¹_t, but its fluctuations are (even) less pronounced, and so provides further support for both the specification and the estimate itself.

**Final Observations**: Some final observations about the k, q and e series are perhaps in order. Marx's own rationale for a secular fall in the composition of costs or increase in the "organic composition of capital" rests on the ostensible tendencies of capitalists to use both more "massive" and more "durable" machines. Evidence of this particular dynamic is not easily discerned, however. The estimation of (3.2.1) or (3.2.2) over various subsamples offers little support for the notion that λ_a has decreased over time. More important, perhaps, much of the cumulative decrease in k seems to be concentrated in the mid-1970s, which casts some doubt on the Marxian explanation. Also, the further, if smaller, reduction from 1980 onward is perhaps better attributed to improvements in "effort extraction"—if capitalists are able to extract more labor from each hour of labor power, fewer productive workers will be required to operate each machine, and the organic composition of capital will rise, ceteris paribus.

Last, the q and e series exhibit some provocative similarities: each is above its apparent trend from the late 1950s to the early 1970s and from 1980 onward, and below it otherwise. A persuasive explanation of this behavior lies well outside the scope of this paper, but it seems reasonable to speculate that the observed fluctuations are not cyclical in the traditional sense, but reflective of fundamental movements in the balance of labor market power.

---

### 3.3 Realization and Recommittal

The simultaneous estimation of the recommittal and effective demand relations allows for the possible covariance of error terms and exploits an important cross-equation restriction. If the distributions of parameters b_{t-j,j} and c_{t-j,j} and recommittal rate p are all invariant, effective demand (2.3) becomes:

**S_t = I_t + Σ_{j=-∞}^t b_{t-j,j} W_j + (1 - p) Σ_{j=-∞}^t c_{t-j} S²_j + B¹_t**  ...(3.3.1)

Where, as before, I_t = (1 - k_t)C_t and W_t = k_t C_t.

### Pascal Distribution

If, as some macroeconomists believe, the full effects of an increase in "income" on "consumption" are not felt at once, the assumption that both sets of coefficients b_{t-j} and c_{t-j} will decrease in t-j is difficult to rationalize. For this reason, an alternative parametrization, the r = 2 Pascal, will also be considered, in which:

**b_{t-j} = [(t - j + 1)!/(t - j)!] (1 - λ_b)² λ_{b}^{t-j}**  ...(3.3.2)

And c_{t-j} is similarly defined, where both distributions incorporate the relevant a priori restrictions. It will also be supposed that the two distributions are identical: b_{t-j} = c_{t-j} for all t-j ≥ 0. This restriction, which finds some support in recent studies of the differences in consumption propensities across households, ensures that the model is tractable and facilitates estimation.

Under these conditions, the Koyck and Pascal specifications of (3.3.1) are:

**SIB¹_t = (1 - λ_{bc})(1 - λ_{bc}L)^{-1} [W_t + (1 - p)S²_t] + u²_t**  ...(3.3.3)

And:

**SIB¹_t = (1 - λ_{bc})²(1 - λ_{bc}L)^{-2} [W_t + (1 - p)S²_t] + u²_t**  ...(3.3.4)

Where SIB¹_t = S_t - I_t - B¹_t and u²_t is an error process, the covariance properties of which are unknown. Simplification of (3.3.3) and (3.3.4) then produces:

**SIB¹_t = λ_{bc} SIB¹_{t-1} + (1 - λ_{bc})[W_t + (1 - p)S²_t] + v²_t**  ...(3.3.5)

And:

**SIB¹_t = 2λ_{bc} SIB¹_{t-1} - λ_{bc}² SIB¹_{t-2} + (1 - λ_{bc})²[W_t + (1 - p)S²_t] + v²_t**  ...(3.3.6)

Where v²_t is either an MA(1) or MA(2) process in the primitive error sequence u²_t.

### Recommittal Mechanism

Under invariance, the recommittal mechanism (2.4) is:

**CB²_t = Σ_{j=-∞}^t λ_{d}^{t-j} [S_j - (1 - p)S²_j]**  ...(3.3.7)

Where CB²_t = C_t - B²_t. In this case, the Koyck specification is a natural first choice: the proportion of S_j - (1 - p)S²_j recommitted to production in period t > j should fall as t rises. With d_{t-j} = (1 - λ_d)λ_{d}^{t-j}, (3.3.7) can be rewritten:

**CB²_t = (1 - λ_d)(1 - λ_d L)^{-1} [S_t - (1 - p)S²_t] + u³_t**  ...(3.3.8)

Or:

**CB²_t = λ_d CB²_{t-1} + (1 - λ_d)[S_t - (1 - p)S²_t] + v³_t**  ...(3.3.9)

Where v³_t = u³_t - λ_d u³_{t-1} and u³_t is another error process with unknown covariance properties.

### GMM Estimation Results

The estimable forms of (2.2) and (2.4) are therefore (3.3.5) or (3.3.6) and (3.3.9). The GMM estimates for both pairs of equations, obtained on the basis of the simultaneous equations extension(s) of the Newey-West (1988) method, are reported in table 3.

**Key Findings**:

*Koyck specification*:
- λ̂_{bc} = 0.805: Median time between receipt and expenditure about 3 periods
- p̂ = 0.038 (3.8%): Recommittal rate
- λ̂_d = 0.378: 62% of value recommitted to production creates demand for capital in same period; median recommittal time 0.712 periods (8.5 months)

*Pascal specification*:
- λ̂_{bc} = 0.674: Median time about 4 periods
- p̂ = 0.041 (4.1%): Recommittal rate
- λ̂_d = 0.369: Similar to Koyck

**Interpretation**: Before the estimates themselves are discussed, one "loose end" remains: the rationale for the use of B¹_t and B²_t as instruments. There is no reason to suppose that random fluctuations in the flow of capital expenditures C_t will be correlated with debt-financed state and household expenditures B¹_t but the series will be correlated with the flow of new capitalist borrowing B²_t if there is "feedback" from C_t to B²_t. If, on the other hand, capitalists' investment decisions are best explained in terms of "animal spirits"—if capitalists' demand for finance results from the unpredictable revision of medium-term expectations—such feedback will be attenuated. The existence of animal spirits would also "short circuit" the connection between disturbances in the flow of realized value/sales S_t and B²_t. Last, the same disturbances will be uncorrelated with new debt-financed state and household expenditure if variations in B¹_t reflect unpredictable movements in consumer confidence and/or the state's economic commitments. The econometric support for this view (in the form of DWH tests) is more substantial than perhaps expected.

There is some cause for concern, however, in the Hansen (1982) or J tests of the (joint) overidentification restrictions: in both cases, acceptance of the null (at the 95 percent confidence level) is borderline. Whether this is attributable to Basmann's (1960) "small sample rejection bias" or reflects a more serious (structural) flaw is not clear.

The characterization of effective (final) demand differs less across specifications than perhaps first appears. From the definitions of the relevant coefficients, the first five terms in the distributions b_{t-j} = c_{t-j} show that:
- Koyck: b̂_0 = ĉ_0 = 0.195, declining geometrically
- Pascal: b̂_0 = ĉ_0 = 0.106, with hump-shaped distribution

Both predict that between 10 and 15 percent will be (re)spent in each of the four periods that follow. In both cases, the median time between receipt and expenditure (about three periods in the former, and four in the latter) is more substantial than some would have expected, a result that seems to underscore the role of "life cycle" considerations. Inferences of this kind are problematic, however, because the "map" from the parameters of the circuit to those of more orthodox models can be more complicated than it first seems.

**Recommittal Rate**: It is the estimated recommittal rate p̂ that will most surprise readers: is it possible that less than 5 percent of the annual flow of surplus value is returned to production? While it would be foolish to insist that the "true" recommittal rate is not 5 percent or perhaps even 10 percent, there is reason to believe that the difference is not much more than this. On the basis of Shaikh and Tonak's (1995) national accounts, for example, most of the surplus value created each period has been used to (re)hire "unproductive" workers. Viewed from another perspective, while most of the (after tax) retained earnings of productive industries are recommitted, these represent a (very) small share of total surplus value.

The estimated covariance σ̂₂₃ between the error terms is negative, which implies, ceteris paribus, that positive "sales shocks" are associated with adverse "capital expenditure shocks", and vice versa. This is consistent with (for example) the identification of period-to-period fluctuations in the recommittal rate p as an important source of short-term macroeconomic disturbances.

---

### 3.4 A Brief Comparison of Actual and Predicted Values

A comparison of the actual and predicted values of national income, sales and (total) capital expenditure, plotted in figure 5, provides another perspective on the estimates.

**National Income (Y_t)**: The predictions of national income track its actual behavior well, with some of the unexplained difference attributable to fluctuations in the "pattern(s) of production". Some of the most substantial "residuals" occur in the last few periods of the sample, with predicted income as much as several billion hours of labor time below the actual. The further observation that the reverse (predicted above actual) occurs in the first few periods of the sample, in combination with the behavior of the constant and variable q values described earlier, hints that the recent shortfall is less the result of new patterns of production than of capitalists' increased power to "mark up".

**Sales (S_t)**: The predicted sales/realized value series also performs well, perhaps better than expected, even if the fit is (from some perspectives) the most problematic of the three. There is some evidence that the new debt-financed state and household expenditure series B¹_t constructed here is a flawed one. The predicted series also fails to capture the full extent of either the recession in the 1970s or the downturn in the 1980s, but this should come as no surprise, inasmuch as external claims on national income and/or central bank policies are not modelled here. While it is obvious that more elaborate accounts of the circuit—in particular, the sources of effective demand—are called for, the "bare bones" model performs as well (or perhaps better) than most would expect.

**Capital Expenditures (C_t)**: Given the ostensible role of "animal spirits" in the determination of (a small proportion of) constant capital expenditures, the performance of the Ĉ_t series is a surprise of sorts: it tracks C_t well over the entire sample, an assessment that, unlike the Ŷ_t series, includes the final few periods.

---

## 4. APPLICATIONS AND ADDITIONAL RESULTS

### 4.1 What is the Current Accumulation Mode?

With reasonable data and plausible estimates, it becomes possible to calculate the **current accumulation mode**, defined on the basis of (2.17) as the maximum sustainable rate of expansion of the flow of value in the circuit. This limit exists not, as in most neoclassical models, because of labor force constraints, but rather because production is not instantaneous and there are (social) limits on the expropriation of surplus value.

In particular, efforts to accelerate the realization and/or recommittal of value with, for example, new debt-financed expenditure must confront these (and other) constraints, as the von Neumann (1945) model first underscored. Furthermore, there is no reason to assume a priori that this rate of expansion will be sufficient to ensure full employment.

To estimate the accumulation mode, rewrite (2.17) as:

**[f₁(g) + B̄¹_0]/f₂(g) = [1 - B̄²_0]/f₃(g)**  ...(4.1.1)

Where:
- f₁(g) = 1 - k[1 - b*(g)]
- f₂(g) = 1 + q[1 - (1 - p)c*(g)]
- f₃(g) = (1 + pq)d*(g)

When all four distributions of coefficients are geometric:

**a*(g) = (1 - λ_a)(1 + g)/(1 + g - λ_a)**  ...(4.1.3)

And so on. The accumulation mode is therefore the root of the composite function:

**f(g) = [f₁(g) + B̄¹_0]/f₂(g) - [1 - B̄²_0]/f₃(g)**  ...(4.1.4)

**Calculation Results**: The behavior of f(·) for the parameter values λ̂_a = 0.395, λ̂_{bc} = 0.805, λ̂_d = 0.378, p̂ = 0.0039 and q̂ = 0.540, relative (to C_0) credit flows B̄¹_0 = 0.036, B̄²_0 = 0.043, and composition of costs k̂ = 0.242, is depicted in figure 6.

Given these parameters, the accumulation mode will be (about) **2.35 percent per annum**.

**Interpretation**: It is important to understand that this is not an upper bound on the rate at which real (in the conventional sense) national product can increase: if new methods of production reduce capitalists' direct and indirect labor requirements, the constant dollar value of output could of course rise at a faster rate. It does reveal, however, that the rate at which new productive workers could be "absorbed" into the labor force exceeds the current rate of new entrants, even if the bound is perhaps lower than expected. The social and economic consequences of this limit will become more pronounced as the pace of productive innovation slows and the distribution(s) of income, both within and across classes, becomes more uneven.

**Sensitivity Analysis**: It is also important to consider the responsiveness of the accumulation mode to variations in the structure of production and accumulation. To illustrate, consider the effects of a substantial increase in the recommittal rate, from 3.9 percent to 8 percent. The maximum sustainable rate of flow would then increase from 2.35 percent to more than 2.5 percent, an amount equivalent (at current values) to almost half a million workers.

---

### 4.2 Stocks and Flows

The circuit of capital framework restores the classical/Marxian identification of "intertemporal flow paths" as the proper focus of macroeconomics. In so doing, however, it also draws attention to the intertemporal behavior of the stocks of productive, financial and commercial capital.

One could ask, for example, what (relative) stocks of productive and financial capital are consistent with the accumulation mode calculated in the previous section. Recall that period-to-period movements in K_t and F_t follow:

- ΔK_t = C_t - Q_t
- ΔF_t = S¹_t + p_t S²_t - C_t + B²_t  ...(4.2.1)

If both stocks and flows expand at the same rate, these become, on the basis of (2.7), (2.10) and (2.15):

**K̄_0 = (1/g)[1 - a*(g)]**

**F̄_0 = (1/g)[(1 - B̄²_0)[1 - d*(g)]]/d*(g)**  ...(4.2.2)

**Results**: Given the previous estimates of the circuit's parameters, (4.2.2) implies that when the rate of expansion is 2.35 percent per annum capitalists will hold:
- A stock of financial assets equal to **58 percent** of annual capital expenditures
- A stock of productive capital that is about **65 percent**

Since value added will equal 77 percent of capital expenditures on this path, it follows that:
- Capitalists' stock of financial assets will be about **75 percent** of the annual flow of value added
- The "capital stock" will be **85 percent**

**Calibration**: Shaikh and Tonak's (1995) Marxian net value added was 4.15 trillion dollars in 1989, or 79 percent of conventional GDP, so that the same ratios, expressed in terms of GDP, are 95 and 108 percent. If the former seems small, it should be recalled that if the financial assets created when households and the public sector borrow are added, the totals are 211 percent of annual capital expenditure or 2.8 times the flow of value added.

---

### 4.3 Long-Run Demand Management

The equilibrium condition (2.16) can also be interpreted in terms of the combinations of B̄¹_0 and B̄²_0 that are consistent with the current accumulation mode. Given the current penchant for deficit reduction, for example, it becomes important to estimate the increase in credit-financed capital expenditures required to offset a decrease in the credit-financed demand for final commodities.

It should be remembered, however, that the perturbations considered here are one time adjustments, after which both B̄¹_0 and B̄²_0 are assumed to increase at the same maximal (2.35 percent) rate.

With the notations of section 4.1, (4.1.4) can be rewritten:

**B̄²_0 = [f₂(g) - f₁(g)f₃(g)]/[f₂(g) - f₃(g)f₂(g)] B̄¹_0**  ...(4.3.1)

Which, for the previous parameter estimates and benchmark values, becomes:

**B̄²_0 = 0.075 - 0.945B̄¹_0**  ...(4.3.2)

**Implication**: This implies that an initial reduction of 150 million hours of labor value in new state and household credit—about 80 billion dollars, more or less the federal deficit in the mid 1990s—would not affect the accumulation mode if capitalists borrowed an additional 142 million hours (75.6 billion dollars) for new production. The difference is small but perhaps not unimportant, inasmuch as it reflects the rates at which additions to the circular flow are transformed into productive capital. It can also be shown that f₃(g)/f₂(g) falls as g rises, which means that the increase in B̄²_0 required to offset a reduction in B̄¹_0 decreases when both increase at a faster rate.

---

### 4.4 Implications for Medium-Term Demand Management

Simulations of the complete model can be used to explore, in somewhat crude fashion, the effects of various fiscal policies off the balanced expansion path. The simulation here is based on (2.1), (2.2), (2.7) and the equilibrium definitions of W_t, I_t and S²_t:

- P_t = λ_a P_{t-1} + (1 + q)(1 - λ_a)C_t
- C_t = λ_d C_{t-1} + (1 - λ_d)S_t - (1 - λ_d)(1 - p)S²_t + B²_t - λ_d B²_{t-1}
- S_t = λ_{bc}S_{t-1} + I_t - λ_{bc}I_{t-1} + (1 - λ_{bc})W_t + (1 - λ_{bc})(1 - p)S²_t + B¹_t - λ_{bc}B¹_{t-1}  ...(4.4.1)
- W_t = kC_t
- I_t = (1 - k)C_t
- S²_t = [q/(1 + q)]S_t

Given the estimates of λ_a, λ_{bc}, λ_d, q and p and the previous benchmark for k, this becomes:

- P_t = 0.395P_{t-1} + 0.932C_t
- C_t = 0.378C_{t-1} + 0.622S_t - 0.598S²_t + B²_t - 0.378B²_{t-1}
- S_t = 0.805S_{t-1} + I_t - 0.805I_{t-1} + 0.195W_t + 0.187S²_t + B¹_t - 0.805B¹_{t-1}  ...(4.4.2)
- W_t = 0.241C_t
- I_t = 0.759C_t
- S²_t = 0.351S_t

Which, for specified credit B¹_t and B²_t paths, determines the values of P_t, C_t, S_t, W_t, I_t and S²_t.

**Three Scenarios**:
(i) B¹_t and B²_t remain constant at their respective "end of sample" values
(ii) B²_t remains constant but B¹_t is reduced by the labor time equivalent of 500 million hours (26.7 billion dollars) and then levels off (case of "pure" deficit reduction)
(iii) B¹_t follows the pattern in (ii) but B²_t increases an equal amount in the next period (scenario in which deficit reduction "crowds in" private investment, albeit with brief delay)

**Results** (pictured in figure 7):

*Production (P_t)*:
- Little difference between cases (i) and (iii), though P_t in "status quo" case (i) falls behind "crowding in" scenario (iii) in third period and remains so thereafter
- After eight periods, simulated difference is no more than 400 million hours (0.24% of flow)
- Consequences of pure deficit reduction are NOT transitional: difference in production flows in cases (i) and (ii) increases over time, from 300 million hours in second period to 2 billion in final (about 1.2% of total flow)
- Associated cumulative loss is 8.59 billion hours or 5.16% of last period's flow

*Capital Expenditures (C_t)*:
- After eight periods, capital expenditures under deficit reduction are 1.5 billion hours (or 80 billion dollars) lower than with status quo
- For k = 0.241, this implies 361.5 million fewer hours of labor power will be purchased or, based on current hours per worker per period, almost 200,000 fewer workers

*Sales (S_t)*:
- Predicted paths underscore potential for "coordination failures"
- While P_t is less in case (i) than case (iii) in each period after the second, the reverse holds for S_t
- Sales in (i) are more than in (iii) from first period to last, with no evidence that the smallish difference narrows over time
- Reason: Because new business credit follows deficit reduction, consequences for both capitalists and workers are persistent
- Initial reduction in B¹ leads to immediate reduction in sales S and surplus value S², which more than offsets effect of subsequent increase in new capitalist borrowing B² on S
- This behavior is similar to that exhibited in (modified) Hicksian models in which planned investment is a function of both interest rates and prior sales

*Commercial Capital (P_t - S_t)*:
- Stock of inventories rises more (or falls less) in case (iii) than case (i) in each period
- Difference in final period: 740 million hours (about 40 billion dollars)
- Cumulative difference: 4.91 billion hours or 263 billion dollars
- This means that in third case capitalists are assumed to demand new credit despite evidence of substantial overproduction
- If this demand does not materialize and/or recommittal rate p then falls, behavior of P_t, C_t and S_t will be much closer to second scenario

---

## 5. CONCLUSION

With some ease, orthodox critics often contend that classical (in particular, Marxian) models are not operational. The recent efforts of some heterodox economists, in particular Foley (1982b, 1986b), to recast the Marxian circuit of value in estimable terms represents a provocative response to this criticism.

This paper extends this line of research with the specification and estimation of the circuit's principal components—the production, recommittal and realization mechanisms, versions of the production, investment and demand functions familiar to mainstream macroeconomics—and their implications for rates of sustainable expansion and deficit reduction policies.

**Key Contributions**:
1. Construction of value of money series and exploration of its time series properties
2. GMM estimation of production mechanism (revealing 9-month median production lag and 54% mark-up)
3. Simultaneous estimation of effective demand and recommittal mechanisms (revealing low recommittal rate of ~4%)
4. Calculation of accumulation mode (~2.35% per annum)
5. Analysis of stock-flow relations implied by circuit dynamics
6. Simulation of effects of deficit reduction policies

**Limitations and Future Work**:
The model is necessarily incomplete: it does not model the behavior of B¹_t or B²_t, external claims on national income, or central bank policies. More elaborate accounts of the circuit—in particular, the sources of effective demand—are called for. Nevertheless, the "bare bones" model performs as well (or perhaps better) than most would expect, demonstrating the operational potential of classical macroeconomic frameworks.

---

## APPENDIX: DEFINITIONS AND SOURCES OF DATA

**B¹_t**: The labor value of new debt-financed state and household expenditure, the product of m_t and B¹'_t

**B¹'_t**: The current dollar value of state and household expenditure financed with new debt. This series is constructed as the current dollar value of the combined (federal, state and local) public sector deficits and the increase (or decrease) in total consumer indebtedness. The first series based on the *Economic Report of the President 1990* (ERP90), Table C-80, and the second was spliced from Table B-76, ERP95 and Table C-59, ERP75

**B²_t**: The labor value of new debt-financed capital expenditures, calculated as the product of m_t and B²'_t

**B²'_t**: The current dollar value of capital expenditures financed with new debt. This series is measured as the current dollar value of new external funds for nonfarm, nonfinancial corporate business, as reported in Table B-95 of ERP95

**C_t**: The labor time equivalent of expenditures on constant and variable capital, defined as the sum of W_t and I_t

**I_t**: The labor time equivalent of constant capital expenditures, defined as the product of m_t and I'_t

**I'_t**: The current dollar value of constant capital expenditures. This series appears as "materials inputs into production" in Shaikh and Tonak (1995, Table E.1)

**k_t**: The estimated composition of costs, calculated as the ratio of W_t to C_t

**m_t**: The labor value of the means of circulation, defined as the ratio of N_t to Y'_t

**M_t**: The labor time equivalent of the stock of commercial capital, the product of M'_t and m_t

**M'_t**: The current dollar value of the (end of period) stock of commercial capital. This is the current dollar value of (end of period) inventories of domestic business, farm and nonfarm, drawn from ERP90, Table C-18

**N_t**: The number of hours of productive labor power. This is the product of the number of productive workers and the number of hours per productive worker. The first appears in Table F.1 of Shaikh and Tonak (1995) and the second in Table L.1 of Shaikh and Tonak (1995)

**P_t**: The labor value of the flow of production, the product of m_t and P'_t

**P'_t**: The current dollar value of the flow of production. This series appears as "gross output of productive and trading sectors" or "total value" in Shaikh and Tonak (1995, Table E.1)

**S_t**: The flow of realized value, calculated as the difference between P_t and M_t

**S¹_t**: The flow of replacement value, calculated as the difference between S_t and S²_t

**S²_t**: The labor time equivalent of surplus value, calculated as the product of m_t and S²'_t

**S²'_t**: The flow of surplus value in current dollar terms. This series is calculated as the difference between Y_t and W_t, adjusted for fluctuations in the stock of commercial capital

**w_t**: The current dollar price (per hour) of productive labor power, calculated as the ratio of W'_t to N_t

**W_t**: The labor value of variable capital expenditures, calculated as the product of m_t and W'_t

**W'_t**: The current dollar value of variable capital expenditures. This series appears in Shaikh and Tonak (1995, Table E.1)

**Y_t**: The labor value of the net product flow, calculated as the product of m_t and Y'_t and (therefore) identical to N_t

**Y'_t**: The current dollar value of "Marxian value added". This series appears in Shaikh and Tonak (1995, Table E.1)

**ω_t**: The value of labor power, defined as the product of m_t and w_t

---

## REFERENCES

[Full bibliography of 40+ references omitted for brevity - includes works by Andrews, Basmann, Baumol, Brinkman, Davidson & MacKinnon, Dickey & Fuller, Dumenil, Ehrbar, Foley, Granger & Newbold, Hansen, Kmenta, Lipietz, Luxemberg, MacKinnon, Marx, Matthews, Moseley, von Neumann, Newey & West, Okishio, Phillips & Perron, Quesnay, Rubin, Samuelson, Sargan, Schumpeter, Shaikh & Tonak, Smolinski, Taylor, de Vroey, Weisskopf et al., White, and Wolff]

---

**Author Affiliation**:
Department of Economics
Munroe Hall
Middlebury College
Middlebury, VT 05753
USA

---

**End of Transcription**

*Extraction completed: October 23, 2025*
*Total pages: 39*
*Document type: Econometric analysis using Shaikh-Tonak (1994) dataset*
*Key contribution: First operational estimation of Foley's circuit of capital model for US economy 1948-89*
