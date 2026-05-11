# Body Text - Chunk 002
## Competition, Instability, and Nonlinear Cycles - Conference Proceedings

---

## PAGE 71

### III. The global behaviour of the process

Whether locally stable or not, we are now going to inquire into the more global tendencies inherent in process (19). For lack of space, we shall content ourselves with a rough outline of the most important features. In particular, the following lemmata and the concluding theorem will just be stated, without formal proofs (they can be found in Franke, 1985). Step by step, we shall consider possible divergence phenomena and introduce some assumptions to rule them out. We regard them as quite reasonable. Thus, in the end, we shall be in a position to apply the Poincaré-Bendixson Theorem, which constitues the basic idea of the following analysis.

Let us mention beforehand that, right from the outset, we have made a variety of exploratory simulation experiments on the computer and plotted the resulting trajectories of relative magnitudes in the positive (q,y)-plane, where y is read off on the horizontal, and q on the vertical axis (a convention that will be maintained in the following). They all have indicated clockwise rotations of (q,y) around the long-run equilibrium values (q*,y*). These motions can easily be described in economic terms, too.

### Step 1

If we also globally stick to the Auxiliary Assumption of the preceding section, then readily examples can be given such that

(21) q(t) → 0 and y(t) → ∞ as t → ∞

---

## PAGE 72

(quite apart from a possible φ₁(t)/X₁(t) < -1, i.e., a negative flow of production). It may be observed that, at low values of q, sector 1 is not only less profitable than the other sector, but he even produces at an absolute loss. For this situation the assumption suggests itself that the first sector does not wish to produce at all, or 'φ₁ = -X₁' in formal terms. If q should not rise, he just awaits running out of its inventories (which, then, would be a mess for the total economy since the other sector is dependent on the capital good). So, we modify the Auxiliary Assumption in the following way.

### Assumption 2

(i) The investment function φ(·,·) satisfies

φ(λp,X) = φ(p,X), φ(p,λX) = λφ(p,X)

for all p,X∈ R²₊₊ and all real numbers λ > 0.

(ii) Define, in obvious notation,

f(q,y) := φ₁(p,X)/X₁ - φ₂(p,X)/X₂,

the difference in the expected sectoral growth rates.
For all y > 0 it satisfies

f(q*,y) = 0, q > q* ⇒ f(q,y) > 0,
q < q* ⇒ f(q,y) < 0

(iii) There are two positive real numbers q₁ and q₂ such that

p₁/p₂ ≤ q₁ ⇒ φ₁(p,X) = -X₁
p₁/p₂ ≥ q₂ ⇒ φ₂(p,X) = -X₂

---

## PAGE 73

The function of relative excess demand, E(·,·), is now to refer to this function f = f(q,y). The introduction of the latter, however, has no influence on the stationary point (q*,y*). Likewise, its uniqueness is maintained, and since ∂f(q*,y*)/∂y = 0, the local stability analysis does not nee to be modified in any way.

Assumption 2 proves sufficient to exclude the divergencies of (21).

### Lemma 1

Suppose that Assumpions 1 and 2 hold. Then there are positive numbers q̄₁ ≤ q₁ and q̄₂ ≥ q₂ such that for all y > 0

q ≤ q̄₁ implies F(q,y) < 0, and
q ≥ q̄₂ implies F(q,y) > 0

Consequently, for every y > 0 there exists a price q > 0 bringing about F(q,y) = 0.

We add, as a side-remark, that for very small q inventories of sector 2 not only rise in relative terms, but then in any case Ẋ₂ > 0 results. As for the second part of the Lemma, in general one has to be prepared that such a q is not uniquely determined, so that oscillations of (q,y) may be "bouncing".

### Step 2

It will be expected that, if inventories of one sector are very small in relation to those of the other, the excess demand in the respective commodity will turn out to be posi-

---

## PAGE 74

tive. Actually, the following lemma is a bit stronger. It rules out another kind of divergence, namely that

(22) q(t) → ∞, y(t) → ∞ as t → ∞

(or both tending to zero, respectively).

### Lemma 2

Suppose that Assumptions 1 and 2 hold. Then for all q = qᵃ > 0 there exists a yᵃ > 0 such that

0 < q ≤ qᵃ, 0 < y ≤ yᵃ ⇒ E(q,y) > 0.

Similarly, for all q = qᵇ > 0 there exists a yᵇ > 0 such that

q ≥ qᵇ, y ≥ yᵇ ⇒ E(q,y) < 0.

Consequently, for all q > 0 there exists at least one y > 0 that entails E(q,y) = 0.

On the analogy of Lemma 1, with respect to a given q there may be more than one y with E(q,y) = 0 (so that we could not speak of the demand curve). Taking account of Assumption 2(iii) it can, however, be demonstrated that at least for q ≤ q₁ and q ≥ q₂ the said values of y are indeed unique.

### Step 3

We are, next, concerned with ensuring positiveness of q and y. To begin with the relative price, note that its dynamic equation has the form of a radio-active decay, though with a variable rate of decrease, -g₁[E(t)/y(t)] + g₂[-q(t)E(t)].

---

## PAGE 75

Convergence q(t) → 0 is ruled out if it is shown that this rate remains bounded in a certain time interval (i.e., before the trajectory in question reaches the south-west region of the positive orthant where, according to Lemma 2, q̇ would become positive again). This is not too difficult a problem. However, the simple idea sketched does not work this directly for the y-component. In fact, introduction of an additional hypothesis will be necessary. Considering the south-west region of the (q,y)-plane where ẏ < 0, q̇ > 0, it obviously depends upon the slope |q̇/ẏ| of a trajectory whether it will hit the q-axis before passing a borderline F=0. If the slope is sufficiently steep, i.e., if the price changes are sufficiently strong in relation to the decline of y, then the trajectory can stay within the interior of the positive orthant. We shall achieve this by imposing two restrictions on both f(q,y) and the rates at which prices are changing. Although this announcement may sound somewhat demanding, the restrictions themselves are actually comparatively mild.

### Assumption 3

(i) For any fixed q < q*, f(q,y) is bounded as y → 0; for any q > q* it is bounded as y → ∞

(ii) The functions gᵢ, regulating the change of prices in eq.(15) and the corresponding formulations, are two continuously differentiable real functions defined on the domain ℝ × (0,∞) (instead of only on ℝ₊²). Their arguments are eᵢ/Xᵢ and X₁/X₂, i=1,2

sgn gᵢ(eᵢ/Xᵢ,X₁/X₂) = sgn eᵢ, i=1,2.

---

## PAGE 76

(iii) There exists a small Y₁ > 0 such that, with respect to the q̄₂ of Lemma 1, for all (p,X) with

0 < p₁/p₂ ≤ q̄₂, X₁/X₂ ≤ Y₁, the following two inequalities hold: e₁(p,X) > 0 (existence of such a Y₁ is already guaranteed by Lemma 2) and

g₁(e₁/X₁,X₁/X₂) - g₂(e₂/X₂,X₁/X₂) ≥ e₁/X₁ - e₂/X₂.

Likewise, there exists a large Y₂ such that, with respect to the q̄₁ of Lemma 1, for all (p,X) with

p₁/p₂ ≥ q̄₁, X₁/X₂ ≥ Y₂, e₁(p,X) < 0 as well as

g₁(e₁/X₁,X₁/X₂) - g₂(e₂/X₂,X₁/X₂) ≤ e₁/X₁ - e₂/X₂.

We remark that the first part of the assumption can be shown to be consistent with Assumption 2(iii). Of course, the two main inequalities of part (iii) are satisfied by functions gᵢ = γᵢeᵢ/Xᵢ with γᵢ ≥ 1. Moreover, Theorem 2 on local stability is not affected by the new price setting functions when g'ᵢ(0) in condition (20) is replaced by ∂gᵢ(0,y*)/∂(eᵢ/Xᵢ), i=1,2; we omit further details, though.

In addition to the assertion that a trajectory of process (19) exists on the maximal time interval [0,∞), the following lemma also makes sure that it cannot "starve" in a certain region unless it approaches the equilibrium in a direct way.

---

## PAGE 77

### Lemma 3

(i) Let Assumptions 1-3 apply and (q(·),y(·)) be a trajectory of process (19) starting in the interior of the positive (q,y)-plane. Then

q(t) > 0, y(t) > 0 for all t∈ ℝ₊

(ii) Consider a region in the (q,y)-plane bounded by
- a subset (a curve) of the set {(q,y): F(q,y)=0},
- and/or a subset of {(q,y): E(q,y)=0},
- and possibly by the y- and/or q-axis.

Then a trajectory starting in this region either leaves it again in finite time or, staying there, converges to the equilibrium (q*,y*).

### Step 4

We are now turning to the last divergence phenomenon to be eliminated, namely that a trajectory, though not approaching either of the axes directly, has a point of accumulation (q̄,ȳ) there. This means there exists a sequence {tₖ}ₖ∈ℕ such that

(23) tₖ → ∞ and (q(tₖ),y(tₖ)) → (q̄,ȳ) as k → ∞

We cannot help introducing another assumption. Whereas Assumption 3(iii) above has taken care of that, for small y and q ≤ the q̄₂ of Lemma 1, price changes must not be too reserved, here we shall require that for at least one very high

---

## PAGE 78

relative price q > q̄₂ the rate of change in (only) the first absolute price p₁ does not tend to infinity if the relative excess demand does. For the sake of simplicity, the formulations of the assumption itself is a bit more specific and relates to more global situations (incidentally, in all simulation experiments neither this assumption nor a weaker version of it has been needed to prevent (23)).

### Assumption 4

There exist two positive real numbers α and β such that, for all small X₁/X₂, e₁/X₁ > α implies

g₁(e₁/X₁,X₁/X₂) = β.

In conjunction with the former results, we actually are now in a position to conclude that, in a broad sense, process (19) can be regarded as stable. To wit, what can be called stable (and it is a global stability) is not necessarily the long-run equilibrium position (q*,y*) itself, but a whole, possibly quite large area in the (q,y)-plane.

### Lemma 4

Let Assumptions 1-4 be satisfied. Then there exists a compact subset in the interior of ℝ²₊ such that
- each trajectory of process (19) starting in it stays there, and
- each trajectory starting outside enters it within a finite time.

---

## PAGE 79

At the same time Lemma 4 establishes the conditions that permit application of the famous Poincaré-Bendixson Theorem, which is the main upshot of our global analysis. As a matter of fact, thanks to the fact that we are sure of the existence of just one stationary point and thanks to a result of its local analysis (namely that the determinant of the Jacobian C is positive, which rules out (q*,y*) is a saddle), we obtain a stronger and more aesthetic statement than the mere assertion of the Poincaré-Bendixson Theorem.

### Theorem 3

Suppose that Assumptions 1-4 hold and let (q(·),y(·)) be a trajectory of process (19) starting anywhere in the interior of the (q,y)-plane. Then it has a non-void limit set it tends to, and this is either the long-run position (q*,y*) or a periodic orbit around it.

As a final remark on the stability behaviour of process (19) let us mention that all this section's analysis is independent of Assumption 1(i), according to which good 2 is the only consumption good. The lemmata as well as Theorem 3 remain valid if it is replaced by the consumption function

c = c(p,X) = C(p,X)/(p₁c + p₂) [c/1]

where c is any fixed non-negative real number. Nevertheless, substitution effects are still assumed to be absent.

---

## PAGE 80

### Conclusion

The theorem on the global behaviour of the process does not say anything about the number of periodic orbits. Yet, in all numerical calculations of concrete economies performed on a computer (where the equilibrium was unstable) we have obtained just one (stable) limit cycle. Since this might give an unduely harmonic impression, we add a warning. Examples can easily be found (and surprisingly, also globally there still seems to be a certain relationship to the positiveness of det A - cf. the local stability conditions) in which the swings of q and y periodically go the extreme; the turning points of pᵢ being near zero and near unity, if prices are normalized such that p₁ + p₂ = 1, and the same for inventories. So, although Theorem 3 has assured us of certain global stability properties, in these cases they may be judged to be quite irrelevant.

Even if the basic approach here presented is accepted, this observation indicates that the analysis should seek to exploit some more features of cross-over dynamics. Let us leave aside issues as that of variable and endogenously determined turn-over periods or the determination of the total sum (of money) of aggregate demand in a stock-flow economy, which would raise new conceptual problems. We confine ourselves to mentioning the following three general ideas from the literature that might lead to an improvement in the performance of stability. In the respective works they are introduced to obtain a sufficient condition for the asymptotic stability of the equilibrium itself. Likewise, one or the other might be a point of departure for a study of the stability of a whole set (in the sense of Lemma 4), which, nevertheless, should not be "too great".

---

## PAGE 81

1. According to the device put forward in Flaschel and Semmler (1985), investment decisions not only take account of the present profit rates differentials, but, in addition, also of their momentary rates of change. (For reasons of symmetry, price changes too may depend not only on excess demands, but also on their rates of change. In the Flaschel-Semmler model each of these two elements, taken in isolation, has a stabilizing effect. It is, however, another problem what will be the outcome when both are operating in conjunction)

2. Beside different sectoral rates of profits, capitalists' flow of investment may also take the market situation into consideration. So, for example, at the same set of profit rates investment in a sector will be less the higher the excess supply of its commodity. Using this idea, in another section of Franke (1985) a Liapunov function could be provided. However, an unresolved problem was to make sure of, in particular, the underlying assumption that absolute prices are bounded away from zero.

3. In Boggio (1985) a modification of the price equation is proposed. Recalling the good stability properties of some dynamical processes where prices are obtained by a simple mark-up on full cost, he considers price changes as determined both by full cost and excess demand. The mark-up factor of the former is based on changes of target profit margins, which, in turn, are determined endogenously by, again, excess demands.

---

## PAGE 82

### References

L.Boggio (1984), "Convergence to production prices under alternative disequilibrium assumptions", Cahiers de la R.C.P. Systèmes de Prix de Production, no.2,3, "La Gravitation", Nanterre

-- (1985), "Production prices and barriers to entry: a model of general interdependence and the stability of long-run equilibrium position", enclosed in this volume

G.Duménil and D.Lévy (1983), "La concurrence capitaliste: un processus dynamique", Paris, mimeo

P.Flaschel and W.Semmler (1985), "The dynamic equalization of profit rates for input-output models with fixed capital", enclosed in this volume

R. Franke (1985), Production prices and dynamical processes of the gravitation of market prices, doctoral thesis, Bremen

E.Hosoda (1984), "On the classical convergence theorem", Manchester, mimeo

A.Mas-Collel (1974), "Algunas observaciones sobre la teoria del tatonnement de Walras en economias productivas", Anales de Economia, Época 3, nums. 21-22

M.Morishima (1960), "A reconsideration of the Walras-Cassel-Leontief model of general equilibrium", K.J.Arrow et al. (eds.), Mathematical Methods in the Social Sciences, Stanford; 63-76

---

## PAGE 83

# STABILITY OF PRODUCTION PRICES IN A MODEL OF GENERAL INTERDEPENDENCE

LUCIANO BOGGIO

Università di Parma
Istituto di Scienze Economiche
Via J. Kennedy 6b
43100 - Parma

Università Cattolica del S. Cuore
Dipartimento di Scienze Economiche
Largo Gemelli 1
20145 - Milano

In the modern theory of production prices - which is mainly derived from the works of Sraffa, Von Neumann and Leontief - the question of the relation between such prices and those actually prevailing in the economy has been for a long time almost completly neglected.

Recently this question has been attracting more attention and, among the authors closer to the Sraffa approach, the view has been advanced that Sraffa prices should be seen as "centres of gravitation" in the sense of the Classics, i.e. as long run positions towards which actual prices tend to move. [See in particular Garegnani (1976)]

However awareness that "gravitation" cannot be taken for granted and that the study of the problem must meet contemporary standards of dynamic analysis is spreading rather quickly (1).

Familiarity with the methods of dynamic analysis leads one most naturally to regard production prices as an equilibrium vector, i.e. a vector such that, when the actual price vector coincides with it, the forces of change (in the description of the Classics, entry and exit movements of firms across industries) come to a stop; and to consider the question of gravitation as a case of a typical problem of dynamic analysis: the stability of equilibrium.

In my previous works (Boggio, 1980, 1984 and 1985) I examined the stability of production prices within two different models of price-formation.

In the first model, price changes were a sign-preserving function of excess-demand and

(1) A useful presentation of the problem and a discussion of the literature can be found in Steedman (1984). For a discussion of approaches and results particularly relevant for our previous and present works see Boggio (1985).

---

## PAGE 84

quantity changes were an increasing function of profit rates. In this model, which we may call a "pure-competition model", if consumption with strong price-substitution effects is not introduced, the production price vector, with any (finite) number of goods, is an unstable equilibrium and, with two goods, under not particulary unplausible assumption, it is strongly unstable (2).

In the second model, prices are formed on a full-cost basis, i.e. they are equal to the cost of production plus a constant proportional margin, which may be different from good to good. In this model the vector of production prices (redefined to allow for fixed profit differentials) is globally asymptotically stable.

Whilst the former model, when consumption with strong price substitution effects are excluded, gives a negative answer to the question of the stability of production prices, when such effects are included, it formally offers a solution.

However, the solution is not consistent with one of the basic ideas which led, in recent years, to the development of the theory of production prices - the idea to develop a "theory of value" different from marginalist general equilibrium. For, such a model becomes stable - after the inclusion of consumption - as long as the substitution effects of prices on consumption dominate its dynamics and make the Classic mechanism, i.e. the movements of capitals across industries following profit differentials, irrelevant.

In this way, although the equilibrium solution and the associated notion of production prices are not reducible to the neo-Walrasian tradition, which has never really (or correctly) considered long-run equilibria (3), nevertheless the whole disequilibrium process, dominated by price reactions to excess-demand and by consumption reactions to price changes, is very similar to the description of the world given by the main body of the marginalist tradition.

As to the letter model, based on full-cost pricing, it does not appear very satisfactory either, since the formation of margins is not explained.

The basic idea of this paper is to maintain a fundamental role for full-cost in price formation, but, at the same time, to make the formation of margins endogenous.

The choice of full-cost as a basis for the analysis of price formation (and of the stability of production prices) is due to the fact that, for most produced goods, we consider it a much more realistic explanation of price formation than its marginalist counterpart (4).

(2) These results were obtained on the assumption of the same production model as that of this paper, except for the fact that inventories were not allowed for. Extending those results to the case in which such difference is removed looks, however, rather trivial. For a definition of unstable and strongly unstable equilibrium see Lasalle (1976).

(3) The Wicksellian general equilibrium system, however, is a long-run equilibrium and includes the condition of a uniform rate of profit.

(4) Obviously this statement implies that that we do not accept the reduction - operated in the '40s and '50s - of the full-cost hypothesis to the marginalist theory. One can imagine a full-cost rule which also fullfills, under certain conditions, the equality between short-run marginal cost and marginal revenue. But we do not believe that the full-cost rule followed by firms is of this type.

---

## PAGE 85

In any case, the alternative (Walrasian) hypothesis making price changes a sign-preserving function of excess-demand finds little support in the empirical studies (5).

The particular specification of the full-cost approach we shall choose is that based on target rates of profits.

Excess-demand however will also play a (minor) role in the determination of both prices and target profit rates.

In this way, we shall develop a dynamic model of general interdependence with four kinds of variables: price, output levels, inventories and profit margins.

The word "equilibrium" means for us simply a stationary point of a dynamic system. In our model the "equilibrium" will be a vector of relative prices, relative ouput levels, inventories and profit margins which remains unaltered, under the dynamic forces described by the model.

In general, it is rather difficult to get definite conclusions about stability in a model of this order (5 x n, where n is any positive integer). However, by making definite assumptions about the relative size of adjustment speeds and reaction coefficents, we shall be able to show that the equilibrium of the system is endowed with rather strong stability properties.

A warning is necessary from the start: this model is characterized by the important feature that production decisions are governed by price signals only, and not by quantity signals.

This feature rules out most of the analyses of Keynesian derivation, among which, of particular importance for stability analysis, business cycle analysis (accelerator models, Harrod's knife-edge, etc.).

It is obvious that the introduction of quantity signals in the explanation of production decisions would have brougth in strong elements of instability.

A traditional approach of economic theory places these aspects within the scope of "short-run" analysis and assumes them away in the "long-run" analysis.

This approach implicitly assumes that, although the production movements determined by quantity signals may exhibit instability with reference to the path that the economy would otherwise follow, nevertheless they tend to "oscillate around it", so that the work of such path remains relevant.

Hoping that future work will be able to throw some light on this aspect, for the time begin we must be content to rely on such an assumption in order to justify the exclusion of quantity signals.

(5) The marginalist theory, however, could produce for price changes more realistic hypotheses, incorporating a cost element.

---

[The text continues with subsequent pages through PAGE 154, containing detailed mathematical and economic theory. Due to length constraints, I've shown the format for the first portion. Would you like me to continue with specific sections?]
