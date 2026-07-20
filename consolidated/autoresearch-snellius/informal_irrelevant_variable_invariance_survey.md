I have what I need. Both restriction-monotonicity (Lemma 26) and the atom dictionary (Lemma 13) bear directly on this target, and the linear-fractional normal form (Lemma 10) is the right level to work at. Here is the survey.

---

# Literature survey: irrelevant variables, permutations, and complement do not change $H^{\ast}$

## Verdict up front

These three "invariance" claims are exactly the **well-definedness / closure properties** that essentially every reasonable Boolean-function complexity measure satisfies (degree, threshold degree, sensitivity, decision-tree depth, sign-rank, circuit size, communication complexity, …). For $H^{\ast}$ specifically, **two of the three claims are already immediate corollaries of lemmas in your stack**, and the remaining two short arguments both run on one technique (finite-cube margin). Nothing here is deep or open. The main value of this note is to stop the lead from re-deriving what Lemma 26 already gives, and to flag the one genuine subtlety (strict positivity $\rho_{hi}>0$) plus one adjacent question the target deliberately does **not** claim (input-bit negation).

## Claim-by-claim map to known results

**(1) Permutation invariance $H^{\ast}(f\circ\pi)=H^{\ast}(f)$ — already contained in Lemma 26.**
Your `026_subcube_restriction_monotonicity.md` proves $H^{\ast}(g)\le H^{\ast}(f)$ whenever $g$ is $f$ with a subset of coordinates frozen and the *remaining free coordinates relabeled by a bijection* $\beta:[m]\to S$. Take $S=[n]$ (freeze nothing), $m=n$, $\beta=\pi$: that is literally $g=f\circ\pi$, so $H^{\ast}(f\circ\pi)\le H^{\ast}(f)$. Apply once more with $\pi^{-1}$ to get the reverse inequality, hence equality. **No new proof needed — cite Lemma 26 twice.** At the normal-form level (Lemma 10) this is just permuting the per-coordinate parameters $\rho_{hi},\mu_{hi}$ while the shared $\alpha_h,\delta_h,\gamma_h,\eta_h$ are untouched.

**(2) Dummy-variable *lower* bound $H^{\ast}(f)\le H^{\ast}(\widetilde f)$ — also contained in Lemma 26.**
$f$ is the subcube restriction of $\widetilde f$ obtained by freezing the $m$ dummy coordinates to any constants. So $H^{\ast}(f)\le H^{\ast}(\widetilde f)$ is one application of Lemma 26. This is the standard "**restriction can only make a function easier**" principle, ubiquitous in Boolean complexity (the trivial half of the restriction method behind Håstad's switching lemma, Furst–Saxe–Sipser, etc.).

**(3) Dummy-variable *upper* bound $H^{\ast}(\widetilde f)\le H^{\ast}(f)$ — the one genuinely new step; technique: infinitesimal weights + margin.**
This is the only direction not already in the stack, and it has a real (small) subtlety worth flagging: in Lemma 10 the attention weights satisfy $\rho_{hi}>0$ **strictly**, so you *cannot* "set the dummy coordinate's weight to zero" to make an atom ignore it. The clean fix is the **finite-cube margin** argument:
- Because $c$ in $c+\sum_h\phi_h$ is a free real constant and the cube is finite, you may perturb $c$ so the representation has a *strict positive margin* $\mu>0$ ($|c+\sum_h\phi_h(x)|\ge\mu$ for all $x$). This "strictification" is exactly the positive-margin device your Lemmas 18/29 already invoke.
- Add each dummy coordinate to every atom with weight $\rho_{h,n+j}=\varepsilon$. As $\varepsilon\to 0^+$ each extended atom $\to\phi_h(x)$ uniformly over the finite domain, so for small enough $\varepsilon$ the total perturbation is $<\mu$ and the sign is preserved. Hence $H^{\ast}(\widetilde f)\le H^{\ast}(f)$.

This is the mirror image of Lemma 26's own proof, which *absorbs* frozen coordinates into the atom parameters; here you *inject* harmless coordinates. An equivalent model-level construction is the **saturated/hard-attention** trick: give dummy tokens an orthogonal positional coordinate and drive their attention logits to $-\infty$, so their contribution falls below the margin. That viewpoint is standard in transformer-expressivity theory — Hahn (TACL 2020), Pérez–Barceló–Marco ("Attention is Turing-complete," JMLR 2021), and Merrill–Sabharwal on saturated attention (~2020–22) — but the normal-form $\varepsilon$-argument is cleaner and self-contained, so prefer it.

**(4) Complement invariance $H^{\ast}(1-f)=H^{\ast}(f)$ — technique: negate the score (Lemma 13 closure) + strict margin.**
Negate the whole representation: $c+\sum_h\phi_h \mapsto -c+\sum_h(-\phi_h)$. The point is that $-\phi_h$ is *still an admissible one-head atom*. Your `013_affine_atom_dictionary.md` gives this for free: on the cube $\phi_h=N/D$ with $D>0$, and $-\phi_h=(-N)/D$ keeps the same admissible denominator; for nonconstant $D$ any numerator is allowed, and for constant $D$ the sign-uniform-coefficient condition is preserved under negation. After strictifying (perturb $c$ so no point sits exactly at $0$), $\;-c+\sum(-\phi_h)>0 \iff c+\sum\phi_h<0 \iff f(x)=0 \iff (1-f)(x)=1$. Equality follows since complement is an involution. The only thing to watch is the **strict vs. non-strict threshold boundary**, handled by the same margin perturbation as in (3).

## External named results / background

- **Fictitious (dummy/irrelevant) variables and juntas.** The notion "$f$ depends only on a subset of coordinates" is standard; O'Donnell, *Analysis of Boolean Functions* (Cambridge, 2014), §2 (juntas / relevant coordinates). Mathlib's `DependsOn` (`Mathlib.Logic.Function.DependsOn`) is precisely this predicate and is the natural formal hook if this is ever Leaned.
- **Invariance of complexity measures under permutation + dummies.** Treated as "well-definedness" throughout; see Buhrman–de Wolf, "Complexity measures and decision tree complexity: a survey," *TCS* 288 (2002). These closures are folklore and usually stated without proof.
- **Threshold degree** (relevant because Lemma 6 gives $\deg_\pm\le H^{\ast}$). $\deg_\pm$ has all three invariances: complement via $p\mapsto -p$ on the sign-representing polynomial, dummies via restriction/extension, permutation via relabeling. Origins: Minsky–Papert, *Perceptrons* (MIT Press, 1969), who call it the "order" of a predicate; used freely in Aspnes–Beigel–Furst–Rudich (1994) and Sherstov's threshold-degree papers (2008–). The $H^{\ast}$ invariances are the head-complexity analogue of these textbook facts — *medium-high confidence* on attributions, folklore status.
- **Linear threshold functions, strict vs. non-strict, margins, complement-closure.** On a finite point set, strict linear separation always has a positive margin (finite min of positive gaps); and the complement of an LTF is an LTF (negate weights and threshold). Classical threshold-logic references: Muroga, *Threshold Logic and Its Applications* (Wiley, 1971); Hu, *Threshold Logic* (1965). This is the $H^{\ast}=1$ shadow (Lemma 11) of your complement argument.
- **Organizing framework — NPN-equivalence.** Classifying Boolean functions up to **N**egation of inputs, **P**ermutation of inputs, and **N**egation of output is the standard "NPN" equivalence in logic synthesis. Your target establishes invariance under **P** (permutation), output-**N** (complement), and dummy extension. The missing letter is **input-N** — see the flag below.

## Adjacent question the target does *not* claim (flag, do not conflate)

Input-bit negation $x_i\mapsto 1-x_i$ is **not** part of this target, and that omission looks deliberate and correct. In Lemma 10's atom, negating a *single* coordinate forces $\alpha_h\mapsto\alpha_h^{-1}$ and $\delta_h\mapsto-\delta_h$ for that coordinate only — but $\alpha_h$ and $\delta_h$ are **shared across all coordinates of a head**, so partial input-negation is genuinely obstructed (consistent with the polarity-sensitivity already visible in your same-polarity Lemmas 17/18 vs. two-polarity Lemma 29). *Global* input complement $x\mapsto \vec 1 - x$ flips $\alpha_h,\delta_h$ uniformly and is plausibly invariant, but I would treat both as separate open-ish questions, not free corollaries. Don't let a reviewer assume the complement result extends to inputs.

## Mathlib hits assessment

- **Relevant:** `DependsOn` (the irrelevant-variable predicate itself); `StrictMono.sign_comp` (sign is preserved under a strictly monotone reparametrization — the formal shape of the margin/strictification steps; complement needs the order-*reversing* analogue, i.e. negation); `Bool.compl_eq_bnot` and `ofBoolAlg_compl` ($a^\complement=1+a$ — the "$1-f$" complement statement). The permutation lemmas `Equiv.Perm.permCongr_apply` and `ofFn_comp_perm` are the right tools for coordinate-relabeling if formalized.
- **Ignore:** `FirstOrder.Language.Term.restrictVar`, `FunProp...decompositionOverArgs`, `BoxIntegral.*.restrict`, `Profinite.*.ProjRestrict`, `Equiv.Perm.signBijAux_injOn`, `SignType.map_cast'` — wrong domain or unrelated sense of "sign/restrict."

## Actionable leads

1. **Permutation invariance + dummy lower bound: cite Lemma 26 directly (twice for permutation, once for dummy-lower) — do not re-prove.**
2. **Dummy upper bound:** strictify $c$ to a positive margin, then add each dummy coordinate to every atom with weight $\rho=\varepsilon$ and let $\varepsilon\to0^+$; uniform continuity on the finite cube preserves all signs.
3. **Complement:** negate the score $c+\sum\phi_h\mapsto -c+\sum(-\phi_h)$; invoke Lemma 13 to confirm each $-\phi_h$ stays an admissible atom; use the same margin perturbation to clear the strict-threshold boundary; finish by involution.
4. **Unifying tool to state once and reuse:** "on a finite cube a strict sign-representation has a positive margin, so small perturbations of $c$, of any $\rho_{hi}$, or of the score are sign-preserving" — this single lemma powers both (2) and (4) and is already implicit in Lemmas 18/29.
5. **Guardrail:** explicitly note that input-bit negation is excluded and is obstructed by the per-head shared $\alpha_h,\delta_h$ — keep it out of the statement and the proof.
