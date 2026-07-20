# Positivity Is Free at Level One

## Statement

With $\mathrm{tChow}_{\pm}$ the positivity-free tangential-Chow sign-rank ([018_tchow_sandwich.md](018_tchow_sandwich.md)),

$$
\mathrm{tChow}_{\pm}(f) \leq 1 \iff H^{*}(f) \leq 1 \iff f \text{ is constant or a linear threshold function},
$$

and hence $\mathrm{tChow}_{\pm}(f) = H^{*}(f)$ whenever either side is $\leq 1$.

> The base case of the open question whether $\mathrm{tChow}_{\pm} = H^{*}$ in general (do the attention positivity/one-sided constraints ever cost a head?): at level one they cost **nothing**. The key point is that an order-1 tangent form $\theta D_1 + N_1$ is just an arbitrary affine function, and an LTF is realized with an admissible atom by putting the (mixed-sign) affine form in the *numerator* over a fixed positive denominator (L11). Empirically $\mathrm{tChow}_{\pm} = H^{*}$ in every computed case (`claude-comments/empirical_findings.md`); whether it holds at all levels is open.

## Proof

By L11, $H^{*}(f) \leq 1$ iff $f$ is constant or an LTF. We show the same for $\mathrm{tChow}_{\pm}$.

**$\mathrm{tChow}_{\pm}(f) \leq 1 \Rightarrow$ constant or LTF.** If $\mathrm{tChow}_{\pm}(f) = 0$, $P = \theta$ is constant, so $f$ is constant. If $\mathrm{tChow}_{\pm}(f) = 1$, $P = \theta D_1 + N_1$ with $D_1, N_1$ affine, so $P$ is affine and $f(x) = 1 \iff P(x) > 0$ is an LTF (or constant).

**Constant or LTF $\Rightarrow \mathrm{tChow}_{\pm}(f) \leq 1$.** A constant uses $H = 0$. An LTF $f = \mathbf 1[A > 0]$ ($A$ affine) uses $H = 1$ with $D_1 \equiv 1$, $N_1 = A$, $\theta = 0$, giving $P = A$.

So the three conditions are equivalent. Finally, since $\mathrm{tChow}_{\pm} \leq H^{*}$ always and both characterizations coincide, the exact values agree: $0$ for constants, $1$ for nonconstant LTFs. $\blacksquare$

## Consequence

This is the first rigorous evidence that positivity is free (not merely a numerical observation). The general statement $\mathrm{tChow}_{\pm} = H^{*}$ would resolve the F4 question and identify $H^{*}$ with the standard (unconstrained) tangential-Chow rank. The obstacle at $H \geq 2$ is that the product structure $\prod_h D_h$ couples the denominators, so the level-1 free-numerator trick does not obviously extend; see `claude-comments/lit_survey_round2.md` (P2) for the algebraic-geometry route.
