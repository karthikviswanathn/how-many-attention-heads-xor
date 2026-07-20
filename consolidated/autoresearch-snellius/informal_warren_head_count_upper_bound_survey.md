Web search isn't permitted in this session, so I'll ground the survey in my own knowledge of the literature and mark anything whose exact constants/dates I'm less than fully certain of. The mathematics here is standard enough that I'm confident in the substance.

---

# Literature survey: Warren counting bound for low head complexity

## Verdict up front

This target is **not new mathematics**. It is a textbook-template application of **sign-pattern counting for polynomially-parametrized families** (Warren's theorem) to the project's own normal form. The only project-specific ingredient — that "$H^\ast(f)\le H$" forces $f$ to be the sign of a polynomial of degree $O(H)$ in $O(Hn)$ real parameters — is **already proved in your stack** (Lemmas 10, 13, 14). Once you grant that, the bound follows by a routine count. Expect a short proof, and expect the stated $+\log(H+1)$ term to be *slack*, not a tight feature.

The lead should **not** redo the normal-form work — it's done — and should resist the VC-dimension detour (see below), which gives a *weaker* bound than the one asked for.

## The core technique and its provenance

The whole proof is one classical idea: **a family of classifiers cut out by signs of polynomials in $\ell$ real parameters can realize only a bounded number of distinct labelings on $m$ fixed points, and the bound is sub-exponential in $\ell$.** Named results, oldest to most directly usable:

- **Shannon (1949)** — the counting/cardinality method itself: there are $2^{2^n}$ Boolean functions, so any class described by few parameters can cover only a vanishing fraction. This is the conceptual frame and the reason the lemma is wanted (see "downstream use").
- **Oleĭnik–Petrovskiĭ (1949), Milnor (1964), Thom (1965)** — bounds on the sum of Betti numbers (in particular the number of connected components) of a real algebraic set defined by polynomials of degree $d$ in $\ell$ variables, of the form $d(2d-1)^{\ell-1}=(O(d))^\ell$. The 0-th Betti number version is what underlies cell/sign-pattern counts.
- **Warren (1968)**, *"Lower bounds for approximation by nonlinear manifolds,"* Trans. AMS **133**, 167–178 — **the canonical citation for this target** (its name is literally "Warren counting bound"). Warren bounds the number of connected components of the complement of a real-polynomial arrangement, equivalently the number of distinct **strict sign vectors** $(\operatorname{sgn} p_1(\theta),\dots,\operatorname{sgn} p_m(\theta))\in\{-,+\}^m$ realizable as $\theta$ ranges over $\mathbb{R}^\ell$. Standard packaged form: for $m\ge \ell\ge1$ and degrees $\le d$,
$$
\#\{\text{sign patterns}\}\;\le\;\Big(\tfrac{4\,e\,d\,m}{\ell}\Big)^{\ell}.
$$
  *(I'm confident in the $(O(dm/\ell))^\ell$ shape and the $\ell$-in-denominator; the precise constant $4e$ is the commonly quoted form but varies by reference — Warren's own statement and the Anthony–Bartlett restatement differ by small factors. Mark the constant, not the shape, as the thing to pin down.)*
- **Pollack–Roy (1993)** and **Basu–Pollack–Roy**, *Algorithms in Real Algebraic Geometry* (book, 2003/2006) — the modern, citable refinement that bounds the number of **sign conditions** including zeros, $\{-1,0,+1\}^m$, by $\binom{m}{\le\ell}(O(d))^\ell=(O(dm/\ell))^\ell$. **Use this version**, not the strict one, because your threshold is strict ("$>0$"), so a function is determined by the weak pattern $\{P>0\}$ vs. $\{P\le 0\}$ and you must account for the $P=0$ boundary cleanly.
- **Goldberg–Jerrum (1995)**, *"Bounding the VC dimension of concept classes parameterized by real numbers,"* Machine Learning **18**, 131–148 — the exact packaging you want: a class whose membership test is the sign of a degree-$d$ polynomial in $\ell$ real parameters realizes $\le(O(dm/\ell))^\ell$ labelings on $m$ points (and has VC dimension $O(\ell\log d)$). This is the cleanest black box to cite; their proof *is* the Warren argument. **Anthony–Bartlett**, *Neural Network Learning: Theoretical Foundations* (1999), Ch. 7–8, gives the same bounds in textbook form.

If you ever need to count **without** clearing denominators — working directly with the softmax/exponential parametrization — the relevant generalizations are **Khovanskiĭ's "Fewnomials" (1991)** and **Karpinski–Macintyre (1997)** (VC bounds for Pfaffian/sigmoid networks). You almost certainly do **not** need these: clearing denominators (below) keeps everything polynomial.

## The bridge: your own normal form supplies the polynomial parametrization

This is the only non-generic step, and it's done. To apply Warren you must exhibit, for each $f$ with $H^\ast(f)\le H$, a polynomial $P(\,\cdot\,;\Theta)$ with $f(x)=\mathbf 1[P(x;\Theta)>0]$, of controlled degree-in-$\Theta$ and parameter count. Your stack gives exactly this:

- **Lemma 13 (affine atom dictionary)** linearizes each head: for fixed $x\in\{0,1\}^n$, head $h$ contributes $N_h(x),D_h(x)$ that are **affine in the parameters**, with $D_h>0$ under admissibility. So each head carries $\approx 2(n{+}1)$ real parameters $\Rightarrow \ell=O(Hn)$ total (plus $O(H)$ readout coefficients).
- **Lemma 14 (cleared-denominator invariant)** gives the actual polynomial:
$$
P(x;\Theta)=\theta\prod_{h}D_h(x)+\sum_{h}N_h(x)\prod_{g\ne h}D_g(x),
$$
which for **fixed $x$** is a polynomial in $\Theta$ of degree $\le H+1=O(H)$. Crucially, **denominator positivity** (admissibility, $D_h>0$) is what makes $\operatorname{sgn}(\text{rational score})=\operatorname{sgn}(P)$, so clearing denominators preserves the Boolean function — that's the content you're leaning on.
- **Lemma 10** is the underlying normal form these rest on.

So the $m=2^n$ "polynomials" fed to Warren are $\{P(x;\cdot)\}_{x\in\{0,1\}^n}$, each degree $\le H+1$ in $\ell=O(Hn)$ variables. The map $\Theta\mapsto(\operatorname{sgn}P(x;\Theta))_x$ has image $\supseteq\mathcal F_{n,H}$, so $|\mathcal F_{n,H}|\le\#\{\text{sign patterns}\}$.

## Hitting the stated bound (and why it's loose)

Direct count, $m=2^n\ge\ell$:
$$
\log_2|\mathcal F_{n,H}|\le \ell\log_2\!\Big(\tfrac{4edm}{\ell}\Big)
= O(Hn)\cdot\log_2\!\Big(\tfrac{O(H)\,2^n}{O(Hn)}\Big)
= O(Hn)\,(n+O(1))=O(Hn^2).
$$
Note the $H$ in the degree $d=O(H)$ **cancels** the $H$ in $\ell=O(Hn)$, so the clean direct count already gives $O(Hn^2)$ — *stronger* than the target. The target's extra $+\log(H+1)$ appears only if you bound cruder, e.g. $\log_2(4edm/\ell)\le n+\log_2 d+O(1)=n+\log_2(H+1)+O(1)$ without cancelling $\ell$, giving $O(Hn)\,(n+\log(H+1))$. Either bookkeeping proves the claim; the target is comfortably true.

**Steer away from VC + Sauer–Shelah.** VCdim $=O(\ell\log d)=O(Hn\log H)$, then Sauer–Shelah over $2^n$ points gives $\log_2|\mathcal F|=O(Hn^2\log H)$ — an *extra* $\log H$ on the leading term, which is **larger** than the target $Hn(n+\log H)$ and therefore does **not** establish it. The direct sign-pattern count is the route that matches the stated bound.

## Technical points a "fully rigorous" proof must not skip

- **Strict threshold / zeros.** Use the sign-*condition* count (Basu–Pollack–Roy), which allows $P=0$, since $f$ is determined by $\{x:P>0\}$ and $P=0$ falls on the $f=0$ side.
- **Admissibility is harmless for the upper bound.** Restricting $\Theta$ to the semialgebraic admissible set ($\gamma>0,\rho_i>0,D_h>0$) only *shrinks* the realizable set, so Warren over all of $\mathbb R^\ell$ still bounds it. (Admissibility is used positively only to justify clearing denominators.)
- **The regime $\ell>m$** (i.e. $Hn\gtrsim 2^n$). Warren needs $m\ge\ell$. When $\ell>m=2^n$, fall back to the trivial $|\mathcal F_{n,H}|\le 2^{2^n}$; check it's $\le 2^{CHn(n+\log H)}$ there (it is, since $Hn\gtrsim 2^n\Rightarrow Hn(n+\log H)\gtrsim 2^n$). Split the proof into these two regimes.
- **Pin the constants $\ell\le c_1Hn$, $d\le c_2H$** against the exact atom parametrization in Lemmas 13/14 — the only place the proof can go quantitatively wrong.

## Consistency / sanity checks (use these to catch errors)

- **$H=1$:** Lemma 11 says $\mathcal F_{n,1}=\{$nonconstant LTFs$\}\cup\{$const$\}$. The number of **linear threshold functions** on $\{0,1\}^n$ is $2^{n^2(1-o(1))}$, precisely $\log_2\#\mathrm{LTF}_n=n^2-n\log_2 n+O(n)$ — upper bound from **Schläfli/Cover (1965)** function-counting, matching lower bound from **Zuev (1989)**. The target at $H=1$ gives $O(n^2)$, consistent, and shows the leading $Hn^2$ is the **right order** (cannot be improved to $Hn\cdot\mathrm{polylog}$).
- **Downstream use (why this lemma exists):** combined with Shannon counting ($2^{2^n}$ total functions), it yields a **lower bound** — a $1-o(1)$ fraction of Boolean functions need $H^\ast(f)=\Omega(2^n/n^2)$ heads. The interesting regime is therefore $H$ up to $\sim 2^n/n^2$, exactly where the bound is non-vacuous.

## Mathlib search hits — honest assessment

- `Polynomial.signVariations`, `Polynomial.roots_countP_pos_le_signVariations`, `Polynomial.succ_signVariations_le_X_sub_C_mul` (`Mathlib.Algebra.Polynomial.RuleOfSigns`): this is **Descartes' rule of signs**, the *univariate* ancestor of sign counting. It is **not** Warren's theorem and does **not** give the multivariate bound you need. Relevant only as evidence that **Mathlib lacks Warren / Milnor–Thom / multivariate sign-condition counting**. For an *informal* proof this is fine (cite Warren as a black box); for any future formalization, this gap is real and large.
- `ChevalleyThm.numBound`, `degBound`, `ConstructibleSetData.degBound`: complexity bounds for **Chevalley's theorem on constructible sets** (scheme-theoretic / over general rings). Unrelated to real cell-counting. **Red herrings.**
- `Set.Countable.isConnected_compl_of_one_lt_rank`, `isConnected_compl_of_one_lt_codim`, etc.: connectedness of complements of low-codimension/countable sets. Unrelated to counting cells of an arrangement. **Red herrings.**

## Actionable leads

1. **Cite Goldberg–Jerrum (1995) / Warren (1968)** as the black box: $\#\{\text{sign patterns of }m\text{ degree-}d\text{ polys in }\ell\text{ vars}\}\le(4edm/\ell)^\ell$ for $m\ge\ell$ — this is the entire engine.
2. **Build the polynomial from Lemmas 13 + 14**: each $f$ with $H^\ast(f)\le H$ is $\mathbf 1[P(x;\Theta)>0]$ with $\deg_\Theta P\le H+1=O(H)$ and $\ell=O(Hn)$ parameters; verify these two constants explicitly — they are the only quantitative risk.
3. **Count directly, not via VC dimension**: the direct sign-pattern count gives $O(Hn^2)\le CHn(n+\log(H{+}1))$; the VC+Sauer–Shelah route gives $O(Hn^2\log H)$ and fails to prove the stated bound.
4. **Use the sign-*condition* count (Basu–Pollack–Roy) to absorb $P=0$**, and **split off the $\ell>m=2^n$ regime** with the trivial $2^{2^n}$ bound.
5. **Sanity-check at $H=1$** against $\#\mathrm{LTF}_n=2^{n^2(1-o(1))}$ (Cover 1965; Zuev 1989) to confirm the leading $Hn^2$ order is correct.
