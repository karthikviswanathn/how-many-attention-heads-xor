Web search isn't permitted in this session, so I'll write from the in-context lemma stack and my own knowledge, hedging external references appropriately. The substance of this target is internal to the project anyway.

---

# Survey: Homogeneous-Polarity Boolean Minors Do Not Increase Head Complexity

## Bottom line

This target is **not yet in your stack, but it is a short corollary of what is**. It factors cleanly into two pieces:

1. **(genuinely new)** Global / antipodal input-negation invariance: $H^{\ast}(f^{\dagger}) = H^{\ast}(f)$, where $f^{\dagger}(x) = f(\bar x)$, $\bar x = (1-x_1,\dots,1-x_n)$.
2. **(already proved)** Lemma 34 (positive Boolean minors don't increase $H^{\ast}$).

The homogeneous all-negated minor is just a **positive minor of $f^{\dagger}$**, so the corollary is `Lemma 34 ∘ (1)`. Only piece (1) requires new work, and it is an elementary model-level symmetry argument, not a hard theorem. I'd put high confidence (>0.95) that this is true and provable in a few lines. It does **not** appear to be already proved: Lemma 31 gives output-negation $H^{\ast}(1-f)=H^{\ast}(f)$ and permutation invariance, but **input** negation is absent; Lemma 34 is strictly the unnegated (monotone) case.

## The crux: what is new vs. what reduces to existing lemmas

The reduction is exact. Writing $f(w) = f^{\dagger}(\bar w)$, a homogeneous all-negated minor
$$g(y) = f\big(\dots, 1-y_{j(i)},\dots; \text{constants } c_i\big)$$
becomes
$$g(y) = f^{\dagger}\big(\dots, y_{j(i)},\dots;\ \text{constants } 1-c_i\big),$$
i.e. an **unnegated** substitution (constants + plain coordinates, repetitions allowed) into $f^{\dagger}$. That is precisely the hypothesis of **Lemma 34**, applied to $f^{\dagger}$ instead of $f$. So
$$H^{\ast}(g) \;\overset{\text{Lem 34}}{\le}\; H^{\ast}(f^{\dagger}) \;\overset{(1)}{=}\; H^{\ast}(f).$$
The positive-polarity branch is literally Lemma 34. **So the only thing to prove is (1).**

## Most plausible technique for (1): closure of the model class under relabeling

The right tool is the **"witness relabeling / simulation" argument** — the same pattern as Lemmas 31 and 34. $H^{\ast}$ is a *minimum over a parameter family* (a $\min$/$\inf$ over witnessing models), so to get $H^{\ast}(f^{\dagger})\le H^{\ast}(f)$ you exhibit a cost-preserving map on witnesses: **swap the two token embeddings $e_0 \leftrightarrow e_1$**, leaving positional embeddings, all $W_Q,W_K,W_V,W_O$, $w$, and $\tau$ untouched. Since $u_i(x)=e_{x_i}+p_i$ and $u_=$ is constant in $x$, the swapped model evaluated at $x$ equals the original model evaluated at $\bar x$, with the **identical head count $H$**. Hence any $H$-head witness for $f$ becomes an $H$-head witness for $f^{\dagger}$; the antipodal map is an involution ($\bar{\bar x}=x$, cf. `Bool.not_bijective` / `Equiv.boolNot` in the hits), so the inequality is two-sided and you get equality. This is exactly the "$\inf$ is invariant under a cost-preserving bijection of the index set" principle — the abstract shape captured by the Mathlib hits `Set.BijOn.iInf_congr` and `IsMinOn.on_preimage` (here the bijection is "swap $e_0,e_1$" on model-parameter space).

**Conceptual point worth flagging to the lead.** This works for the *global* complement but **not** for an individual coordinate negation $x_i \mapsto 1-x_i$: the token embeddings $e_0,e_1$ are shared across all positions, so you can only swap them everywhere at once. Position-dependent structure ($p_i$) breaks single-coordinate negation symmetry while preserving the global one. **This is why the target restricts to *homogeneous* polarity** — mixed polarities would need per-coordinate negation invariance, which the model does not obviously provide (and may genuinely fail). I would not assert a separation, but it is the reason the hypothesis is shaped this way, and it's the one subtle line in the whole result.

## Independent cross-check: normal-form closure (Lemma 10/13)

You can verify (1) a second way, purely algebraically, which is good insurance. A one-head atom (Lemma 10) has denominator $D(x)=\gamma+\sum_i \rho_i\alpha^{x_i}$ with $\gamma,\rho_i,\alpha>0$. Under $x\mapsto\bar x$,
$$\alpha^{1-x_i} = \alpha\cdot(\alpha^{-1})^{x_i},$$
so $D(\bar x)=\gamma+\sum_i(\rho_i\alpha)\,\beta^{x_i}$ with $\beta=\alpha^{-1}>0$, $\rho_i'=\rho_i\alpha>0$ — **still an admissible denominator** (the all-positive-coefficient class of Lemma 13). The numerator's $\rho_i\alpha^{x_i}(m_i+\delta x_i)$ term maps to $\rho_i'\beta^{x_i}(m_i'+\delta' x_i)$ with $m_i'=m_i+\delta,\ \delta'=-\delta$, again an admissible atom. So the atom dictionary is **closed under global negation**, giving $H^{\ast}(f^{\dagger})\le H^{\ast}(f)$ via Lemma 10 without touching the embeddings. Two independent proofs of (1) is a strong signal it's correct.

## Where this sits in the known literature

- **Symmetry group of the Boolean cube.** The isometry/automorphism group of $\{0,1\}^n$ (Hamming) is the **hyperoctahedral group** $\mathbb{Z}_2^n \rtimes S_n$ of order $2^n n!$ (signed permutations). The antipodal map $x\mapsto\bar x$ is the central involution = translation by the all-ones vector in the $\mathbb{Z}_2^n$ factor. Standard graph theory (Harary). Most Boolean-complexity measures — degree, threshold degree, sparsity, sensitivity/block sensitivity, certificate and decision-tree complexity — are invariant under this **full** group plus output negation; see O'Donnell, *Analysis of Boolean Functions* (2014), Ch. 1–2. **Your $H^{\ast}$ is the unusual case that is provably invariant only under the *subgroup* $S_n \rtimes \langle\bar{\,\cdot\,}\rangle$ (permutations + global complement) + output negation**, because the architecture is position-aware. That partial symmetry is the genuinely model-specific content; the literature gives the ambient principle, not this exact measure.

- **Threshold-function closure.** That LTFs/PTFs stay LTFs/PTFs of the *same degree* under negating any input or the output is classical (Muroga, *Threshold Logic and Its Applications*, 1971). Via Lemma 6 ($\deg_{\pm}\le H^{\ast}$) this is the algebraic reason the negation symmetry is "free" — but note $H^{\ast}$ tolerates *less* negation symmetry than $\deg_\pm$ does, exactly the global-vs-individual gap above.

- **Boolean minors / clone theory.** The notion "$g$ is obtained from $f$ by substituting constants and (possibly repeated, possibly negated) variables" is the **minor / subfunction quasi-order**. Foundations: Post's lattice of clones (E. Post, 1941); Pippenger, *"Galois theory for minors of finite functions,"* Discrete Math. ~2002 *(volume/date from memory — verify)*; Couceiro–Lehtonen and Couceiro–Pouzet on minor quasi-orders and closed classes of Boolean functions (≈2007–2012, *titles approximate*); textbook treatment of subfunctions in Crama–Hammer, *Boolean Functions: Theory, Algorithms, and Applications* (2011). In that language: your **"positive minor" (Lemma 34) = the constants-and-unnegated-variables minor**, and **"homogeneous-polarity minor" = that quasi-order enlarged by the single global reflection $\bar{\,\cdot\,}$**. Adding *all* reflections would give the full signed-variable minor relation — which is the natural next question (see leads).

- **Monotone vs. general projections.** "Unnegated substitution" is exactly a **monotone projection**; monotonicity of complexity under monotone projections/restrictions is the standard reason such operations can't increase a circuit-like measure. Lemma 26/27 (subcube restriction monotonicity) and Lemma 31 (irrelevant variables, permutation, output negation) are the same family of "reduction can't help" facts.

## On the provided Mathlib hits

Most are tangential (this is an informal-proof target), but two clusters are the right *abstract analogues* of the argument and worth citing in the write-up as conceptual scaffolding: (i) `Bool.not_bijective` / `Equiv.boolNot` — negation is an **involutive bijection**, which upgrades the one-sided inequality to equality; (ii) `Set.BijOn.iInf_congr`, `IsMinOn.on_preimage`, `OrderIso.image_setOf_minimal` — **an infimum/minimum is unchanged under a cost-preserving bijective reindexing**, the exact shape of "swap $e_0,e_1$ on witness space." The `Finset.card_inv` / `Set.natCard_inv` family (involution preserves cardinality) and the permutation-precomposition hits are not central here.

## Confidence and openness

- (1) and the corollary: essentially certain, elementary, not open. Not previously recorded in your stack (the new bit is input negation).
- The claim that *individual*-coordinate negation invariance is **not** available in this model: I'm fairly but not fully confident — it is the reason for the homogeneity hypothesis, but whether a true separation $H^{\ast}(f)\neq H^{\ast}(f\text{ with one bit negated})$ exists is, as far as I can tell, **open** in your project. Mark as conjecture.
- External references (Pippenger volume/date, Couceiro–Lehtonen exact titles): from memory, flagged — verify before citing in any writeup.

## Actionable leads

1. **Prove (1) by the embedding swap $e_0\leftrightarrow e_1$** (all other parameters fixed), then conclude $g$ is a positive minor of $f^{\dagger}$ and invoke **Lemma 34** — the whole target in ~half a page.
2. **Cross-check (1) via Lemma 10/13 atom closure** under $x\mapsto\bar x$ ($\alpha\mapsto\alpha^{-1},\ \rho_i\mapsto\rho_i\alpha$): independent confirmation, no embeddings needed.
3. **Reuse Lemma 31's proof template** (it already does output negation + permutation by relabeling) — input global negation is the same argument with the token-embedding swap substituted in.
4. **State the symmetry group explicitly** in the writeup: $H^{\ast}$ is invariant under $S_n \rtimes \langle x\mapsto\bar x\rangle$ on inputs plus output complement — and flag individual-coordinate negation as the open boundary (motivating the *homogeneous* restriction).
5. **Frame both Lemma 34 and this as one statement** in the minor quasi-order: $H^{\ast}$ is monotone under the constants+unnegated-variables minor relation enlarged by the global reflection — a cleaner ledger entry than two separate lemmas.
