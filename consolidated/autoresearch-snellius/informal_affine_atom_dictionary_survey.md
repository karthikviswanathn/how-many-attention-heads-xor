Confirmed the grounding I needed. Here is the survey.

## Literature survey: Affine Atom Dictionary for One Head

### What this target actually is (framing)

Strip away the model dressing and the target is an **elementary, self-contained algebra problem on the Boolean cube**, not a deep theorem. The atom is a ratio of two functions, each a sum over coordinates of one-variable functions of $x_i\in\{0,1\}$. The entire content rests on one fact and two refinements of it:

- **Core identity (Boolean-cube linearization):** since $x_i^2=x_i$, *any* function of a single bit is affine in that bit. Concretely $\alpha^{x_i}=1+(\alpha-1)x_i$ and $\alpha^{x_i}(m_i+\delta x_i)=m_i+\bigl(\alpha(m_i+\delta)-m_i\bigr)x_i$. Summing gives the affine $N,D$ immediately, with
$$d_0=\gamma+\textstyle\sum_i\rho_i,\quad d_i=\rho_i(\alpha-1),\qquad a_0=\eta+\textstyle\sum_i\rho_i m_i,\quad a_i=\rho_i\bigl(\alpha(m_i+\delta)-m_i\bigr).$$

Everything in the statement is read off these four formulas. The two *non-obvious* pieces — the only places where real thought is needed — are:

1. **The denominator trichotomy is a "shared-base" sign-uniformity phenomenon.** Because a *single* $\alpha$ is shared across all coordinates and all $\rho_i>0$, every $d_i=\rho_i(\alpha-1)$ inherits the sign of $\alpha-1$. So $d$ is all-zero ($\alpha=1$), all-positive ($\alpha>1$), or all-negative ($0<\alpha<1$) — **mixed-sign denominators cannot arise**, even though mixed-sign affine functions can be positive on the cube. This is the heart of the dictionary, and it is the thing to state crisply.
2. **The numerator-freedom asymmetry** is the *same* sign-uniformity hitting the numerator only in the degenerate case: when $\alpha=1$, $a_i=\rho_i\delta$ collapses to a shared sign, whereas when $\alpha\ne1$ the map from $(m_i,\delta,\eta)$ to $(a_0,\dots,a_n)$ is surjective.

### Relevant known mathematics (mostly backdrop / technique names)

This target is not a corollary of any single named theorem; it is folklore-level. The useful "literature" is the standard toolkit it instantiates:

- **Multilinear (Möbius) extension / analysis of Boolean functions.** The fact that functions on $\{0,1\}^n$ are uniquely multilinear, with per-coordinate degree $\le 1$, is the foundational fact of the area — O'Donnell, *Analysis of Boolean Functions* (2014), Ch. 1; the $\{0,1\}$-basis interpolation $g(t)=(1-t)g(0)+t\,g(1)$. Your atom has **no cross terms**, so it is not just multilinear but genuinely *affine* (degree-1 separable) — a stronger and simpler structure than generic multilinearity. Confidence: high.
- **Positivity of an affine function on a polytope ⇒ check the vertices** (Bauer maximum/minimum principle; affine maps attain extrema at extreme points of a compact convex set). For the cube, an affine $D$ with all $d_i>0$ is coordinatewise increasing, so $\min_{\{0,1\}^n}D=D(\mathbf 0)=d_0$; with all $d_i<0$, $\min=D(\mathbf 1)=d_0+\sum_i d_i$. This is exactly the "$d_0>0$" and "$d_0+\sum d_i>0$" corner conditions in classes 2 and 3. (Attribution: Heinz Bauer, ~1958; standard in convex analysis.) **Caveat for the forward direction:** you don't even need this — $D=\gamma+\sum_i\rho_i\alpha^{x_i}$ is a sum of strictly positive terms, so $D>0$ on the cube is immediate. The corner principle is only the clean way to phrase the *converse* positivity bookkeeping. Confidence: high.
- **Linear-fractional structure.** $\phi=N/D$ with $N,D$ affine is a *linear-fractional* function; the literature is **linear-fractional programming**, Charnes–Cooper (1962), whose normalizing change of variables ($D>0$ on the feasible region) is the same positivity hypothesis you carry. This is conceptual context, not a tool you'll invoke. Confidence: high on the attribution; low that it shortens the proof.
- **The converse is a linear-feasibility computation.** "Given target $(d_0,d_i)$, do there exist $\gamma,\rho_i,\alpha>0$?" is, *after fixing the regime $\alpha\gtrless1$*, a linear system with positivity constraints — the domain of **Farkas' lemma / Fourier–Motzkin elimination / LP feasibility**. Here it is solved explicitly (pick $\alpha$ in the right regime; set $\rho_i=d_i/(\alpha-1)>0$; set $\gamma=d_0-\sum_i\rho_i$, positive for $\alpha$ large in class 2 / small in class 3, the threshold being exactly $d_0+\sum d_i>0$). You will not need the general machinery, but it is the right name for *why* the three corner conditions are necessary **and** sufficient. Confidence: high.
- **Sign-representation / threshold context.** The project already uses threshold degree (Lemma 6–8). This dictionary is the algebraic substrate for "cleared-denominator" sign-representation arguments: $c+\sum_h\phi_h>0 \iff \bigl(\prod_h D_h\bigr)\bigl(c+\sum_h N_h/D_h\bigr)>0$ since each $D_h>0$. The numerator-freedom clause is precisely what controls what polynomials survive that clearing — flagging it as the *point* of the exercise.

### Mathlib search-hit triage

Genuinely relevant (cite these if formalizing):
- `Real.exp_pos` — $\alpha^{x_i}=e^{x_i\ln\alpha}>0$ and positivity of each denominator term. Directly used.
- `Finset.sum_pos` (and `List.sum_pos`) — $D>0$ as a sum of strictly positive terms. Directly used for the forward positivity.
- `Monotone.map_min` / `Monotone.map_max`, `AffineMap.lineMap_mono`, `lineMap_mono_endpoints` — back the "affine, coordinatewise-monotone ⇒ min at a corner" step in the converse positivity conditions (classes 2 and 3).
- `image_extremePoints` / `surjOn_extremePoints_image` (Krein–Milman) — the abstract version of "affine extrema at vertices"; conceptually correct but **heavier than needed**; the monotonicity lemmas above are the lighter route, and the sum-of-positives argument is lighter still.
- `Pi.basisFun_repr`, `Module.Basis.repr_apply_eq`, `Module.Basis.constrL` — support **uniqueness** of the affine forms $N,D$ (an affine function on the cube is determined by its values), if you want the representation to be canonical. Optional.

Ignore as irrelevant: the `Affine.Simplex.*` hits (heights, faces, opposite sides), `EReal.add_pos`, the C\*-algebra `IsStrictlyPositive` hits — these matched on "affine/positive" keywords but concern simplices and operator algebras, not this problem.

### Already-proved check (so the lead does not redo work)

- The **atom form itself** is exactly Lemma 10 / `lemmas/01_foundations_and_normal_form/010_linear_fractional_normal_form.md` (the $\eta,\rho_i,\alpha,\gamma,m_i,\delta$ notation matches verbatim, including "$\alpha^{x_i}$ means $1$ when $x_i=0$ and $\alpha$ when $x_i=1$"). Take the atom as given.
- The **linearization/additive split** underlying the forward direction is *already* done for two coordinates in Lemma 1 / `001_checkerboard_additive_decomposition.md` ($N(a,b)=A(a)+B(b)+C$, $D=\alpha(a)+\beta(b)+\gamma$). This target is the $n$-coordinate version *with sign tracking*. Reuse that engine; do not re-derive the per-position split from softmax.
- The **denominator trichotomy and the numerator-freedom asymmetry are NEW** — not in the Lemma 1–12 stack, and the untracked file `informal_affine_atom_dictionary.md` is the live target. No duplication risk.

### Pitfalls / things to get exactly right (not a proof, just hazards)

- The trichotomy's necessity hinges on **one shared $\alpha$**; state explicitly that mixed-sign positive affine $D$ exists but is *not* an atom denominator. That asymmetry is the whole point and is easy to under-state.
- In class 3, $d_0+\sum d_i>0$ together with $d_i<0$ forces $d_0>0$ automatically — worth noting so the converse's $\gamma>0$ window $\bigl(\alpha\in(0,\,1-\sum_i|d_i|/d_0)\bigr)$ is visibly nonempty.
- For numerator freedom with **nonconstant** $D$: $\delta$ is redundant — even $\delta=0$ realizes any $(a_i)$ because $\alpha\ne1$ makes $a_i=\rho_i(\alpha-1)m_i$ invertible in $m_i$. State it cleanly; don't over-use $\delta$.
- For **constant** $D$ ($\alpha=1$): $a_i=\rho_i\delta$ — the *direct* representation cannot produce arbitrary numerators; only uniform-sign ones. Be precise that this is a statement about the direct atom parametrization, not about affine functions in general.

### Actionable leads

1. **Use $x_i^2=x_i \Rightarrow \alpha^{x_i}=1+(\alpha-1)x_i$** to read off $d_i=\rho_i(\alpha-1)$, $d_0=\gamma+\sum\rho_i$; this single identity gives the affine form and the whole denominator trichotomy via the sign of $\alpha-1$.
2. **Frame the trichotomy as shared-base sign-uniformity** ($\rho_i>0$, one $\alpha$): the genuinely informative line, and the reason mixed-sign positive denominators are excluded.
3. **Converse = explicit linear feasibility:** set $\rho_i=d_i/(\alpha-1)$, $\gamma=d_0-\sum\rho_i$, choose $\alpha$ large (class 2) or near $0$ (class 3); the feasibility threshold is exactly the corner condition $d_0+\sum d_i>0$ — cite Farkas/Fourier–Motzkin only as the framing.
4. **Positivity:** forward is a sum-of-positives (`Finset.sum_pos`, `Real.exp_pos`); converse positivity-on-cube reduces to a single corner by coordinatewise monotonicity (`Monotone.map_min`, `lineMap_mono`) / Bauer's principle.
5. **Numerator freedom:** treat $(m_i,\eta)\mapsto(a_i,a_0)$ as a linear map, invertible iff $\alpha\ne1$ — directly yields "nonconstant $D$ ⇒ any $N$" and "constant $D$ ⇒ $a_i=\rho_i\delta$ uniform-sign."
