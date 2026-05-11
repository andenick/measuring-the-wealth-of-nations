# Body Text - Chunk 05 (FINAL)

## [Page 320]

Figure 2.5 displays total labor productivity: value of production in constant dollars divided by total employment in a vertically integrated department. If the well known slowdown in productivity since the end of the sixties affects the three departments, the relatively poor performance of I_fix is striking.

[FIGURE 2.5: Graph showing Total labor productivity from 1950-1975 for Ifix (solid line), Imat (dashed line), and II (dotted line). Y-axis ranges from 10 to 20. All three lines show upward trends with slowdown after late 1960s. Ifix shows poorest performance.]

Figure 2.5: Total labor productivity.

The two previous diagrams are then summarized in the following way: the labor required to satisfy the needs in fixed capital of the different department can best be described by the ratio of total labor embodied in investment goods over total labor embodied in the production for each department (Figure 2.6).

This ratio is called labor composition of the production by Bertrand (1978). Through the variations induced by the business cycle, this ratio shows in each sector an increase in the requirement for investment per unit of output.

---

## [Page 321]

[FIGURE 2.6: Graph showing Ratio labor embodied in investment / total labor embodied (%) from 1950-1975 for Ifix (solid line, top), Imat (dotted line, middle), and II (solid line, bottom). Y-axis ranges from approximately 2 to 8%. Shows cyclical variations with overall upward trends for Ifix and Imat.]

Figure 2.6: Ratio labor embodied in investment / total labor embodied (%).

### Part III: Conclusion

It has been shown that Morishima's version of the expanded reproduction scheme can only deal with balanced growth, because, when the economy is off the balanced growth path, the set of assumptions used by Morishima implies an investment behavior by the different sectors which completely lacks theoretical foundation. A corollary is that in a production linear model, full utilization of capacity, full realization of capital goods, and explicit investment behavior represent an overdetermination of the model and can only be reconciled in a balanced growth situation.

When we consider models where a single type of capital good has to be advanced for expanded reproduction in the next period, the assumption of full realization of the production implies fixed proportions for the vector of output and therefore balanced growth. The dynamic of the system is then similar to a one sector model of the kind Domar(1957) developed.

In these conditions, one may conclude that the imbalance encountered in actual economies can not be generated endogenously by a linear reproduction model as depending on particular proportions of the vector of output, but rather should be viewed as the result of the variation of the structural parameters of the model.

---

## [Page 322]

Data constructed to describe the actual process of reproduction of the US economy between 1948 and 1980, shows a decline in the requirement of intermediary goods per unit of output, when both of them are measured in labor equivalent. This tendency, combined with an increase in the share of imports for intermediary goods, results in almost no growth for the department I_mat in the entire period.

However, the economy shows a net increase in the requirement for fixed capital goods. This tendency, reinforced by the relatively poor performance of I_fix in labor productivity, contributes to the relative development of department I_fix.

Such structural changes imply corresponding changes in the repartition of income and relative prices. However, nothing warrants that changes on the income side will be compatible with maintaining profitability of capital and increasing workers standard of living. But that is the subject of another study.

### REFERENCES

Bertrand, Hugues (1978). La croissance française analysée en sections productives (1950-1974). Statistiques & Etudes Financières, (35), 3-36.

Bertrand, Hugues (1980). Accumulation et croissance en moyenne et longue période. Analyse formelle en sections productives. Paris: Ministère de l'Economie. Direction de la Prévision.

Bertrand, Hugues (1983). Accumulation, régulation, crise: un modèle sectionnel théorique et appliqué. Revue Economique, 34, 305-343.

Carter, Anne P. (1970). Structural changes in the American economy. Cambridge, MA: Harvard University Press.

Domar, E.D. (1957). Essays in the theory of economic growth. New York: Oxford University Press.

Leontief, Wassily (1953). Dynamic analysis. In W. Leontief (Ed.), Studies in the structure of the American economy. Theoretical and empirical explorations in input output analysis (pp. 53-90). New York: Oxford University Press.

Leontief, Wassily (1970). The dynamic inverse. In A.P. Carter & A. Brody (Eds.), Contributions to input output analysis (pp. 17-46). Amsterdam: North-Holland.

---

## [Page 323]

Meyer, Ulrich (1982). Why singularity of dynamic Leontief systems doesn't matter? In Proceedings of the Third Hungarian Conference on input output techniques (pp. 181-189). Budapest: Statistical Publishing House.

Morishima, Michio (1973). Marx's economics. A dual theory of value and growth. Cambridge: Cambridge University Press.

Pasinetti, Luigi L. (1973). The notion of vertical integration in economic analysis, Metroeconomica, 25, 1-29.

Takayama, Akira (1985). Mathematical economics, 2nd ed., Cambridge, MA: Cambridge University Press.

---

## [Page 324 - NEW PAPER BEGINS]

# TESTING NON-LINEARITY IN BUSINESS CYCLES

Salih N. Neftci
Graduate School, CUNY
NY,NY 10036

## I. Introduction:

Compared to studies that use linear models there are, relatively speaking, few attempts to test non-linear business cycle models. The existing work can be grouped under three broad categories. First, there is the class of structural models that have several non-linear properties, but end up generating (simulated) cycles with linear characteristics. [e.g. Hickman (1972)]. Second, there is some work on the estimation of non-linear time series models which characterize non-linear aspects of cyclical phenomena better. [e.g. Marraval (1983)]. Finally, a small number of papers have attempted to investigate non-linear cyclical behavior using non-regression based techniques. [e.g. Neftci (1984), DeLong and Summers (1984)].

This paper is a review of these approaches.

We first discuss the exact meaning of non-linearity in business cycles and time series analyses. The paper then discusses various approaches to non-linearity.

## II. Characterizing Non-linear Movements:

What are exactly the major properties of a non-linear model that differentiates it from a linear model? This question should be answered before a review of the literature on testing non-linear business cycle theory.

There are basically five types of behavior that linear models would fail to capture. First of all, linear economic models are incapable of generating stationary solutions that are cyclical. All stationary solutions

---

## [Page 325]

of linear difference or differential equations will be constants. Indeed, a linear differential equation will, in general, be of the following form:

Ẋ_t = βX_t + K     ,     X_o = given     (1)

The solution will be given by:

X_t = (X_o + K/β) e^(βt) - K/β     (2)

if β<0, the solution converges to -K/β as t→∞.

On the other hand if β>0 then the solution will diverge. But, it is clear that, to get stable cycles as t→∞ we need to constantly perturb equation (1), otherwise the solution will be -K/β.

On the other hand, non-linear models can produce stationary solutions that are cyclical. This is in the sense that the "cycle" will not be a product of initial conditions or "perturbations" but will be a result of the parameters of the system. As an example, assume that an economic variable is driven by the following non-linear differential equation:

Ẋ_t = f(X_t, β)     (2)

The "limit cycle" will then be that curve on the phase diagram to which all trajectories starting near it will approach as t tends to infinity. [Tong (1980)]. Figure I illustrates the case. It can be shown that for some choices of β, (2) may generate such "limit cycles".

---

## [Page 326]

[FIGURE I: A Limit Cycle - Phase diagram showing concentric circular/elliptical trajectories in X_t vs Ẋ_t space, with arrows indicating direction of movement toward a stable limit cycle]

FIGURE I: A Limit Cycle

---

## [Page 327]

A second characteristic of non-linear models is their potential to generate asymmetric behavior. For example, the non-linear moving average representation given below [Robinson 1978]:

X_t = a_1 ε_t ε_{t-1} + ε_t

will be able to generate sharp drops and gradual movements upwards if the parameter a_1 is positive. To generate similar asymmetries with linear moving average models requires judicious choices for the distribution of the error term ε_t. Often such a choice will look a bit artificial and unrealistic. But more importantly, the non-linearity will again have to be supplied from outside -- i.e. through the error term -- when the model is linear.

The ability to account for jump phenomena is the third characteristic of non-linear models. Jumps in economic time series occur for many reasons, but often they are a result of level crossings. Non-linear business cycle models are known to incorporate several such thresholds. Crossings of these thresholds then generate jumps in observed quantities.

Fourthly, one may simply be interested in population moments of economic time series other than the first and second. Under these conditions non-linear models appear to be natural choices. The class of bi-linear time series models introduced by Granger and Anderson (1980) are able to duplicate the movements due to higher order moments.

Finally, non-linear models are capable of representing time irreversibility whereas linear models would be incapable of doing so. Before we discuss this notion, we need to provide the following definition:

---

## [Page 328]

[FIGURE II: Graph showing unemployment rates from 1959-1978. Three lines plotted: "Unemployment rate, all civilian workers" (solid line at top, showing sharp peaks and asymmetric patterns), "Unemployment rate, both sexes, 25 years and over" (dotted line in middle), and "Unemployment rate, job losers" (dotted line at bottom). Shows clear asymmetric cyclical behavior.]

FIGURE II

---

## [Page 329]

**Definition:** [Tong (1980)] A stationary time series {X_t} is said to be time reversible if for every positive integer n, and every t_1, t_2, t_3, ..., t_n, the vectors {X_{t_1}, X_{t_2}, ..., X_{t_n}} and {X_{-t_1}, X_{-t_2}, ..., X_{-t_n}} have the same joint distributions. A stationary time series which is not time reversible is said to be time-irreversible.

The notion of time-irreversibility of stochastic processes is central to the notion of non-linear business cycle theory. An example of time irreversible economic time series is the unemployment rate for the US economy. This can be seen from figure II. It appears that to represent the behavior of the unemployment rate before and after the turning points one would need a stochastic process that switches distributions. It turns out that under these conditions the predictions of switch points--i.e. the turning points--become an interesting problem in its own right. Notice that asymmetric behavior and jump phenomena are two important examples to time irreversibility.

In the next section we will review various ways of testing the non-linearity of business cycles. Throughout this discussion the five properties of non-linear models that we just introduced will occupy the main focus.

## III. Non-linearities in Large Scale Macro-Models:

A large scale simultaneous equation model can be represented conveniently by:

B(L)y(t) = C(L)x(t) + u(t)

where the B(L) and C(L) are matrices in the polynomials of lag operators and where u(t) is a serially uncorrelated error term with zero mean and variance-covariance matrix Σ. The roots of B(z) = 0 lie outside the unit circle so that we can write:

---

## [Page 330]

y(t) = B(L)^{-1}C(L)x(t) + B(L)^{-1}u(t).     (3)

The fact that B(L)^{-1} exists is another way of saying that the system is stable. In other words, unless y(t) is perturbed by a vector of u(t) or affected by X_t's displaying cyclical movements, the endogenous variables can not show any persistant cycles--i.e. all cycles will eventually die out. Using the terminology of the previous section, this means that the process y(t) will not exhibit any "limit cycles", all cycles will be given exogenously to the system (3).

Howrey(1972) provides one way of testing the hypothesis that "stable" systems like (3) capture most of the cyclical phenomena adequately -- in other words whether the business cycle can be explained by "stable" systems responding to a continuous sequence of disturbances. To test the hypothesis Howrey calculates the periodogram of the observed data on the endogenous variables using various spectral windows. The spectral density of a variable X_t is then calculated as:

S_y = a*Y(w)Y̅(w)

where "*" is the convolution operator, "a" is a spectral window and y(w) the fourier transform.

Next, Howrey calculates the fourier transform of B(L)^{-1} and obtains the impulse response functions. Then, the periodogram of residuals to model (3) implied by the model will be given by:

S* = a*T(w)S_u(w)T̅(w)

where T(w) is the fourier transform of B(L)^{-1} and S_u is the periodogram of u_t.

---

## [Page 331]

[FIGURE III: Spectrum density plot for Gross National Product, Quarterly (W = 1200 c²/q). Shows oscillating pattern peaking around frequency 40-60 with amplitude decreasing at higher frequencies. X-axis: Frequency 0-100, Y-axis: Spectrum density 0.04-10.00]

FIGURE III

[FIGURE IV: Power spectrum for Gross National Product, Wharton (β = 1/40 C²/q). Shows smooth curve starting high around 5.000 at low frequencies, decreasing to around 0.010 at frequency 20. X-axis: Frequency 0-20, Y-axis: Power 0.005-5.000]

FIGURE IV

---

## [Page 332]

The hypothesis that the model captures reasonably well most of the cyclical characteristics of Y_t can then be tested by comparing the S_y and S*. Figures III and IV display these periodograms for the Gross National Product. Figure III is the periodogram of the observed series. In contrast, the periodogram displayed in figure IV was generated using the Wharton model. An interesting implication of these figures is that the periodogram implied by the model is very different from the periodogram obtained from raw data. In other words, "the business cycle variations are absent from the model". Howrey (1972) finds the same fact to be true for plant and equipment, residential construction and inventory investment series. He concludes that, for the Wharton model that he studied, "the power spectra implied by the model demonstrate that the model does not exhibit the twelve-to-fifteen quarter oscillations in response to random disturbances that are found in the original series. This means that the model under discussion implies that the source of the business cycles is to be found in the oscillations of exogenous variables, or in the disturbance terms, and is not due to the dynamic structure of the system."

One way to interpret Howrey (1972)'s results is by saying that the Wharton model studied by him did not have enough non-linear aspects to generate limit-cycles.

Evans et.al.(1972) investigated the same issue using another version of the Wharton model and concluded that "stochastic simulations with serially correlated error are more consistent with the historical facts on business cycles than those with serially uncorrelated errors. This again implies that the model failed to capture the dynamic properties of the cyclical phenomena.

---

## [Page 333]

[FIGURE V: Graph showing Aggregate Hours from 1950-1980 (Dec. 1979 marked). Two lines plotted: solid line labeled "actual" showing cyclical behavior with peaks and troughs marked as P and T, and dashed line labeled "predicted" showing smoother trend. Y-axis ranges from approximately 900 to 1300.00]

FIGURE V

---

## [Page 334]

Another type of test of to what extent large scale macro models capture non-linear cyclical movements can be performed by looking at the ability of the structural models to generate time-irreversible stochastic processes. Figure V shows the actual series of man/hours in the US economy plotted on the hours predicted by the FMP model of the Federal Reserve System. The figure displays a rather interesting phenomenon: The predicted hours is a time series that is symmetric around the business cycle turning points. (In other words, it is time reversible). The actual hours on the other hand is clearly asymmetric around the business cycle turning points. Thus the FMP model fails to capture the time-irreversibility at least in the case of this particular variable. One possible test, then, is to obtain the residuals from a large scale model and subject them to tests of asymmetry such as in Neftci (1984) or Delong and Summers (1984).

## IV. Non-Linear Time Series Models:

Granger and Anderson were first to introduce the bi-linear models of time series analysis. These models can be represented by:

X_t - Σa_i X_{t-i} = ε_t + Σb_j ε_{t-j} + ΣΣc_{kl} X_{t-k} ε_{t-l}     (4)

where the ε_t is an i.i.d. process. The class of bilinear models shown in (4) are linear in X_t and in ε_t separately. But non-linear in these variables jointly. Thus, it is capable of representing reasonably well most of the characteristics of non-linear business cycle phenomena. To test for non-linearity one would estimate the system in (4) and then calculate the significance of the hypotheses:

---

## [Page 335]

H_o: (c_{kl} = 0, k=1,...K, l=1,...,L)

If this hypothesis can be rejected, the economic time series X_t should then be "explained" with non-linear business cycle models.

Marravall (1983) provides the only detailed study of whether non-linear time series models "fit" economic data well. Marravall applies linear and non-linear time series models to currency series from Spain. He calculates forecasts from linear ARMA models and from bilinear models, and then concludes that using bilinear models one achieves an 8% improvement in the forecasts.

Similar results were reached by this author in trying to estimate non-linear moving average models:

X_t = Σb_s ε_{t-s} + Σc_{kl} ε_{t-k} ε_{t-l}     (5)

where ε_t is i.i.d. and b_o = 0 by definition.

Robinson (1978) provides a moment method to estimate such models. Application of this method to estimate (5) for employment series in the US economy were not successful. The improvement in forecasts were very small.

## V. Testing Sample Path Properties

In the previous two sections we reviewed ways of testing for non-linearity in cyclical phenomena by using parametric models for the observed time series. A somewhat more robust approach is to deal directly with the sample path properties of the economic time series and test for time-irreversibility, or the existence of jumps by using characteristics of the observed sample paths.

---

## [Page 336]

To do this we define the times of onset of local minima and maxima of an observed time series in the following way: One first determines a parameter c on an a-priori basis. This parameter represents the investigators' a-priori beliefs about how far two cyclical peaks will be apart. Then, two sets of occurrence times are selected using the local minima and the local maxima of the observed series. We let the process {T^p_n} denote the occurrence time of cyclical peaks and {T^t_n} denote the occurrence times of cyclical troughs. The recurrence times are then defined as:

τ^p_n = T^h_n - T^p_n

τ^h_n = T^p_n - T^h_n

The stochastic process {τ^p_i, τ^h_i} represent the lengths of each stage of the observed "cycles".

Neftci (1985) provides empirical results using observations on the realization of the {τ^p_i, τ^h_i} processes. Basically we ask if the {τ^p_i, τ^h_i} generated by the NBER dating mechanism carry any useful information on the timing of business cycles. The selected model is very simple. We consider the bivariate auto-regression:

[τ^p_i]   [β_{10}]   [β_{11}(L)  β_{12}(L)] [τ^p_{i-1}]   [ε_{1i}]
[      ] = [      ] + [                    ] [         ] + [      ]     (6)
[τ^h_i]   [β_{20}]   [β_{21}(L)  β_{22}(L)] [τ^h_{i-1}]   [ε_{2i}]

where β_{ij}(L) polynomials of lag operator and {ε_{ji}} are innovations in the lengths of the two stages of the business cycle.

---

## [Page 337]

If the length of a stage is important in explaining subsequent phases of the business cycle then the processes {τ^p_i} and {τ^h_i} should show some (preferably strong) correlation over time. The system (6) would give one indication to whether {τ^h_i, τ^p_i} carry any useful information. Indeed, if {β_{ij}(L)} are all insignificant then it would be difficult to argue that NBER dating mechanism has some explanatory power. On the other hand, if {β_{ij}(L)} are significant this, by itself, won't guarantee that the Bureau methodology has any additional value over the existing procedures. In a sense, the significance of {β_{ij}(L)} in (6) is like a necessary condition for the Bureau methodology to capture some part of the economic phenomena that conventional econometrics does not account for -- it is however not a sufficient condition.

The estimates of (6) are shown in Table I. Note that lag lengths were kept low while estimating the system. This was partly due to the small number of observations that we have. But it is also the case that τ^h_i, τ^p_i represent arrival times of recessions and upturns and it seems reasonable to expect that these processes won't be correlated beyond the second lag.

Table I shows that when we use 23 observations on the {τ^p_i, τ^h_i} we see that the length of upturns does affect the length of downturns significantly. The corresponding β_{ij} is significant at 2.8% marginal significance level. The sign of the relationship is negative in the sense that for every additional 12 months of upturn one will get approximately .15 × 12 = 1.8 fewer months of downturn. The upturns "explain" approximately 20% of the movements in business cycle downturns -- a share somewhat higher than one would expect. On the other hand when the second regression is

---

## [Page 338]

### TABLE I

### A Bivariate VAR for τ^h_i, τ^p_i

**Dependent Variable**

| Independent Variable | τ^h_i = lengths of downturns |       | τ^p_i = lengths of upturns |       |                    |       |
|---------------------|------------------------------|-------|----------------------------|-------|--------------------|-------|
|                     | Co-efficient                 | Sig. level | co-efficient          | Sig. level | coefficient   | Sig. level |
| constant            | 20.87                        | .00   | 25.7                       | .001  | 20.67              | .18   |
| τ^h_i(0)            | -                            | -     | -                          | -     | -.03               | .92   |
| τ^h_i(-1)           | -                            | -     | -.13                       | .59   | .13                | .70   |
| τ^p_i(0)            | -.15                         | .028  | -.16                       | .04   |                    |       |
| τ^p_i(-1)           | -                            | -     | -.05                       | .55   | .08                | .71   |
| τ^p_i(-2)           | -                            | -     | -                          | -     | .28                | .20   |
| R²                  | .21                          |       | .26                        |       | .08                |       |
| D.W.                | 2.11                         |       | 2.06                       |       | 2.03               |       |
| S.S.R.              | 1022                         |       | 922                        |       | 10472              |       |
| s.e.                | 6.97                         |       | 7.59                       |       | 21.8               |       |

number of observations: 23

---

## [Page 339]

estimated we see a totally different result. The lengths of past downturns do not effect the subsequent upturns. The relevant β_{ij} are significant only at 70% significance level.

The results discussed above suggest that some sort of information exists in the lengths of the business cycle stages as defined by the Bureau methodology.

## VI. Conclusions

In this paper we reviewed three major ways of testing nonlinearity of cyclical phenomena. To sum up the evidence, it appears that there is some evidence that observed cyclical phenomena has some nonlinear characteristics. However, the evidence is not very strong.

---

## [Page 340]

### REFERENCES

Delong, J.B. and Summers, L. "Are Business Cycles Asymmetric?", Manuscript, NBER, 1984.

Evans, M.K., Klein, L. and Saito, M. "Short-run Prediction and Long-run Simulations of the Wharton Model", in Bert Hickman Ed. Econometric Models of Cyclical Behavior, NBER 1972.

Grandmont, J.M. "On Endogenous Business Cycles", Econometrica, 1985.

Granger, C.W. and Andersen, A. "Non-linear Time Series Modelling" in Applied Time Series Analysis, Ed. D.F. Findley, Academic Press, 1978.

Howrey, E.P. "Dynamic Properties of a condensed version of the Wharton Model" Econometric Models of Cyclical Behavior, Ed. Bert Hickman, NBER.

Marravall, A. "An Application of Non-linear Time Series Forecasting" Journal of Business and Economics, January 1983.

Neftci, S.N. "Are Econometric Time Series Asymmetric around the Business Cycle?" Journal of Political Economy, 1984.

_____. "Is There a Cyclical Time Unit?" Manuscript, 1985.

Tong, H. Threshold Models in Non-linear Time Series Analysis, Lecture Notes in Statistics, Springer-Verlag, 1983.

---

## [Pages 341-343]

[PUBLICATION CATALOG LISTINGS - Lecture Notes in Economics and Mathematical Systems, Volumes 184-275, published by Springer-Verlag. Extensive bibliography of economics and mathematical systems publications from 1980-1986.]

