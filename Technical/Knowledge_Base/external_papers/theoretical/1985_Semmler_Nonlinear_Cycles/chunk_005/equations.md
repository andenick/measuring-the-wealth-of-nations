# Equations - Chunk 05

## Paper 1: Reproduction Scheme Conclusion (Pages 320-323)

### No explicit mathematical equations in this section
This concluding section contains textual discussion and references but no numbered equations.

---

## Paper 2: Testing Non-Linearity in Business Cycles (Pages 324-340)

### Equation (1) - Linear Differential Equation (Page 325)

```latex
\dot{X}_t = \beta X_t + K \quad , \quad X_0 = \text{given}
```

**Description:** General form of a linear differential equation with constant K and parameter β. Represents typical linear economic model dynamics.

---

### Equation (2) - Solution to Linear Differential Equation (Page 325)

```latex
X_t = \left(X_0 + \frac{K}{\beta}\right) e^{\beta t} - \frac{K}{\beta}
```

**Description:** Solution to equation (1). If β < 0, converges to -K/β as t → ∞. If β > 0, solution diverges.

---

### Equation (2) [renumbered] - Non-linear Differential Equation (Page 325)

```latex
\dot{X}_t = f(X_t, \beta)
```

**Description:** General non-linear differential equation. Can generate limit cycles for certain choices of β, unlike linear models.

**Note:** This equation is also labeled (2) in the original text, appearing to be a numbering error.

---

### Equation (3) - Non-linear Moving Average Representation (Page 327)

```latex
X_t = a_1 \varepsilon_t \varepsilon_{t-1} + \varepsilon_t
```

**Description:** Non-linear moving average model (Robinson 1978). Can generate asymmetric behavior (sharp drops and gradual upward movements) if parameter a₁ is positive.

---

### Large Scale Macro Model Representation (Page 329)

```latex
B(L)y(t) = C(L)x(t) + u(t)
```

**Description:** General form of large scale simultaneous equation model. B(L) and C(L) are matrices of polynomials in lag operators, u(t) is serially uncorrelated error term with zero mean and variance-covariance matrix Σ. Roots of B(z) = 0 lie outside unit circle for stability.

---

### Equation (3) - Reduced Form of Macro Model (Page 330)

```latex
y(t) = B(L)^{-1}C(L)x(t) + B(L)^{-1}u(t)
```

**Description:** Reduced form showing that existence of B(L)⁻¹ implies system stability. Without perturbations from u(t) or cyclical X_t, endogenous variables cannot show persistent cycles.

---

### Spectral Density Calculation (Page 330)

```latex
S_y = a * Y(\omega)\overline{Y(\omega)}
```

**Description:** Spectral density of variable X_t. "*" is convolution operator, "a" is spectral window, Y(ω) is Fourier transform.

---

### Model-Implied Periodogram (Page 330)

```latex
S^* = a * T(\omega)S_u(\omega)\overline{T(\omega)}
```

**Description:** Periodogram of residuals implied by the model. T(ω) is Fourier transform of B(L)⁻¹, S_u is periodogram of residuals u_t.

---

### Equation (4) - Bilinear Time Series Model (Page 334)

```latex
X_t - \sum a_i X_{t-i} = \varepsilon_t + \sum b_j \varepsilon_{t-j} + \sum\sum c_{kl} X_{t-k} \varepsilon_{t-l}
```

**Description:** Bilinear model (Granger and Anderson). Linear in X_t and ε_t separately, but non-linear jointly. Can represent non-linear business cycle phenomena.

---

### Hypothesis Test for Bilinearity (Page 335)

```latex
H_0: (c_{kl} = 0, \quad k=1,...,K, \quad l=1,...,L)
```

**Description:** Null hypothesis that all bilinear coefficients are zero. Rejection suggests non-linear model is needed.

---

### Equation (5) - Non-linear Moving Average Model (Page 335)

```latex
X_t = \sum b_s \varepsilon_{t-s} + \sum c_{kl} \varepsilon_{t-k} \varepsilon_{t-l}
```

**Description:** Non-linear moving average model with ε_t i.i.d. and b₀ = 0 by definition. Robinson (1978) provides moment method for estimation.

---

### Recurrence Time Definitions (Page 336)

```latex
\tau^p_n = T^h_n - T^p_n
```

```latex
\tau^h_n = T^p_n - T^h_n
```

**Description:** Definitions of recurrence times. τᵖ represents duration from peak to trough, τʰ represents duration from trough to peak. {T^p_n} denotes occurrence times of cyclical peaks, {T^t_n} denotes occurrence times of troughs.

---

### Equation (6) - Bivariate VAR for Cycle Stages (Page 336)

```latex
\begin{bmatrix} \tau^p_i \\ \tau^h_i \end{bmatrix} = \begin{bmatrix} \beta_{10} \\ \beta_{20} \end{bmatrix} + \begin{bmatrix} \beta_{11}(L) & \beta_{12}(L) \\ \beta_{21}(L) & \beta_{22}(L) \end{bmatrix} \begin{bmatrix} \tau^p_{i-1} \\ \tau^h_{i-1} \end{bmatrix} + \begin{bmatrix} \varepsilon_{1i} \\ \varepsilon_{2i} \end{bmatrix}
```

**Description:** Bivariate autoregression model for lengths of business cycle phases. β_{ij}(L) are polynomials in lag operator, {ε_{ji}} are innovations in the lengths of the two stages.

---

## Summary of Mathematical Content

**Total Equations:** 12 distinct equations (with one numbering duplication in original)

**Equation Categories:**
1. **Linear models:** Equations (1), (2) - demonstrating limitations of linear systems
2. **Non-linear models:** Equations (2-alternate), (3), (4), (5) - showing capabilities of non-linear systems
3. **Econometric models:** Large-scale macro model, equation (3-alternate) - simultaneous equation systems
4. **Spectral analysis:** S_y, S* - frequency domain analysis
5. **Time series:** Equations (4), (5), (6) - bilinear and VAR models
6. **Descriptive:** Recurrence time definitions - business cycle measurement

**Mathematical Techniques:**
- Differential equations (continuous time)
- Difference equations (discrete time)
- Lag operators
- Fourier transforms
- Spectral analysis
- Vector autoregressions
- Maximum likelihood/moment estimation methods

**Key Mathematical Concepts:**
1. Limit cycles in non-linear systems
2. Time reversibility/irreversibility
3. Asymmetric dynamics
4. Spectral decomposition
5. Bilinear time series models
6. Phase diagrams

All equations are clearly presented and serve to illustrate the theoretical differences between linear and non-linear approaches to business cycle modeling.
