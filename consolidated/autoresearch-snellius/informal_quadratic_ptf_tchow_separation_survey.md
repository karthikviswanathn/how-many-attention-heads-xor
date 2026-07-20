Web search permission wasn't granted, so I'll rely on my own knowledge for external attributions (marking anything genuinely uncertain) — and on the in-repo lemmas I just read, which settle the core question. Here is the survey.

---

# Literature survey: quadratic threshold functions vs. unrestricted tangential-Chow complexity

## Bottom line up front (flag for the lead)

**This target is, for all practical purposes, already proved inside the repo.** It is the exact mirror of Lemmas 20/22, with the head-complexity counting bound (Lemma 19) swapped for the tangential-Chow counting bound (Lemma 21):

- **Upper-bound half — already done.** Lemma 21 (`021_tchow_warren_count_upper_bound.md`) proves $\log_2|\mathcal T_{n,H}|\le CHn(n+\log_2(H+1))$ with the *same* shape and constants as the head-complexity Lemma 19. This is the harder, load-bearing half, and it is complete.
- **Lower-bound half — already done, verbatim reusable.** Lemmas 20/22 contain a fully self-contained, elementary proof that the number of degree-$\le 2$ threshold functions is $|\mathcal Q_n|\ge 2^{n^3/243}$ (their "Lemma 2"), built from an explicit $|\mathrm{LTF}_m|\ge 2^{m^2/9}$ count (their "Lemma 1"). Neither of these touches the attention model — they are statements about $\deg_\pm$, so they transfer to the tChow setting unchanged.
- **Combination.** The "$n^2$-vs-$n^3$ capacity gap" pigeonhole in Lemmas 20/22's "Lemma 3" works identically: for $H_n=\lfloor cn\rfloor$ with $c=\min\{1,\,a/4C\}$, $a=1/243$, Lemma 21 gives $\log_2|\mathcal T_{n,H_n}|\le \tfrac a2 n^3 < a n^3\le \log_2|\mathcal Q_n|$, so some $f_n\in\mathcal Q_n\setminus\mathcal T_{n,H_n}$ exists, i.e. $\mathrm{tChow}_\pm(f_n)>cn$ while $\deg_\pm(f_n)\le 2$.

So the lead should **not** re-derive the Warren bound or the $2^{\Omega(n^3)}$ PTF count. The only genuinely new bookkeeping is the "$\deg_\pm=2$ exactly" upgrade in the tChow language (see Actionable leads). My confidence that the target is true and that this route closes it is **very high**.

Note also the target is **strictly stronger** than Lemmas 20/22: by Lemma 16's sandwich $\deg_\pm(f)\le\mathrm{tChow}_\pm(f)\le H^\ast(f)$, proving $\mathrm{tChow}_\pm(f_n)\ge cn$ immediately re-implies $H^\ast(f_n)\ge cn$. The tChow form drops the attention positivity/admissibility restrictions, which only *enlarges* the class $\mathcal T_{n,H}\supseteq\mathcal F_{n,H}$ — so this is the cleaner, more robust separation, and it is the right statement to record as the "canonical" one.

## 1. The core technique: counting sign patterns (Warren / Milnor–Thom)

The entire argument is an instance of the **dimension-counting / sign-pattern method**, the standard nonconstructive way to lower-bound a "low-complexity" representation cost.

- **Warren's theorem** (Hugh E. Warren, *Lower bounds for the degree of approximation*, Trans. Amer. Math. Soc. **133** (1968), 167–178). The number of distinct sign vectors $(\operatorname{sign}p_1,\dots,\operatorname{sign}p_m)\in\{-,0,+\}^m$ realized by $m$ real polynomials of degree $\le d$ in $\ell$ real variables is at most $\bigl(\tfrac{4edm}{\ell}\bigr)^{\ell}$ when $m\ge\ell$. This is exactly the black box Lemma 21 invokes (with an absolute constant $A$ and the $\bigl(\tfrac{Adm}{\ell}\bigr)^\ell$ form). *Confidence: high on the statement; medium on the exact page/volume.*
- **Milnor–Thom / Oleĭnik–Petrovskiĭ** (Oleĭnik–Petrovskiĭ 1949; J. Milnor, *On the Betti numbers of real varieties*, Proc. AMS **15** (1964), 275–280; R. Thom 1965): the sum of Betti numbers of a real variety cut by degree-$d$ equations in $N$ variables is $\le d(2d-1)^{N-1}$. This is the topological engine behind Warren-type counts and gives the same asymptotics.
- **Sharp sign-condition counts** (Pollack–Roy, *On the number of cells defined by a set of polynomials*, 1993; Basu–Pollack–Roy, *Algorithms in Real Algebraic Geometry*, Springer, 2nd ed. 2006, Thm. 7.x): the number of sign conditions of $m$ polynomials of degree $d$ on a variety of dimension $\ell$ is $\binom{m}{\le \ell}(O(d))^{\ell}$. Any of these forms yields the $2^{O(Hn^2)}$ bound; the repo's choice of Warren is the most economical.
- **Application to parameterized concept classes** (the template Lemmas 19/21 follow): **Goldberg & Jerrum**, *Bounding the VC dimension of concept classes parameterized by real numbers*, Machine Learning **18** (1995), 131–148; and **Anthony & Bartlett**, *Neural Network Learning: Theoretical Foundations*, Cambridge, 1999 (the chapter bounding VC dimension of real-parameterized networks via Warren/Milnor–Thom). Both are cited in the repo's Lemma 20 "Consequence" and are the correct lineage. The key move — "a family with $\ell$ real parameters whose membership is decided by signs of $2^n$ polynomials of bounded degree realizes only $2^{O(\ell\cdot n)}$ Boolean functions" — is precisely what makes $\mathcal T_{n,H}$ ($\ell=\Theta(Hn)$) yield $2^{O(Hn^2)}$.

The earliest "counting beats construction" instance in this circle of ideas is **Shannon** (*The synthesis of two-terminal switching circuits*, Bell System Tech. J. **28** (1949)), correctly invoked in the repo's prose.

## 2. The two sides of the count

**Side A — the representation class is small (Lemma 21, done).** With $\ell=1+2H(n+1)=\Theta(Hn)$ free parameters and per-point parameter-degree $\le H+1$, Warren gives $\log_2|\mathcal T_{n,H}|=O(Hn^2)$ (up to the $\log H$ term). The crucial structural facts that make this work and are worth keeping in view:
 - $P(x)$ has **degree $\le H$ in $x$** (each term is a product of $H$ affine forms, or $N_h$ times $H-1$ of them) — this is what ties tChow to threshold degree via the sandwich.
 - $P$ has **degree $\le H+1$ in the parameters** — this is what feeds Warren.
 - Strict representation requires $P\ne0$ on the cube; Warren counts the zero sign conditions too, so it is a valid over-count. Lemma 21 handles this correctly.

**Side B — the target class is large: the $n^2$-vs-$n^3$ gap.** The number of degree-$\le 2$ polynomial threshold functions on $n$ bits is $2^{\Theta(n^3)}$. This is the $d=2$ case of the classical fact
$$\#\{\text{degree-}d\text{ PTFs on }\{0,1\}^n\}=2^{\Theta(n^{d+1})}\quad(d\text{ fixed}).$$
 - *Upper bound:* Warren / Sauer–Shelah with VC-dimension of degree-$d$ PTFs $=\binom{n}{\le d}=\Theta(n^d)$, evaluated at $2^n$ points $\Rightarrow 2^{O(n^{d+1})}$.
 - *Lower bound* ($2^{\Omega(n^{d+1})}$): the slightly nontrivial direction. For $d=1$ this is the LTF count $2^{\Theta(n^2)}$ — **Cover** (*Geometrical and statistical properties of systems of linear inequalities…*, IEEE Trans. EC **14** (1965), function-counting theorem) and the tight **Zuev** lower bound $2^{n^2(1-o(1))}$ (Yu. A. Zuev, Soviet Math. Dokl. **39** (1989)). Surveyed in **Saks**, *Slicing the hypercube* (Surveys in Combinatorics, 1993) and **Anthony**, *Discrete Mathematics of Neural Networks* (SIAM, 2001). *Confidence: high on $2^{\Theta(n^{d+1})}$ and on Zuev for $d=1$; medium on the cleanest single citation for the general-$d$ lower bound.*

 Importantly, the repo's "Lemma 2" in `020/022` **sidesteps the general-position subtlety** of the classical $2^{\Omega(n^3)}$ PTF lower bound with a transparent bilinear construction: it plants $m=\lfloor n/2\rfloor$ independent LTFs $\ell_i(v)$ on a $v$-block and reads them off via $q(u,v)=t+\sum_i u_i\ell_i(v)$ on the diagonal $u=e_i$, giving $|\mathcal Q_n|\ge|\mathrm{LTF}_m|^m\ge 2^{m^3/9}=2^{\Omega(n^3)}$. This is cleaner than citing the literature count and is reusable as-is. It is morally a "product/tensor of LTFs" construction — the bilinear-form $\operatorname{sign}(x^\top A x-\theta)$ family — which is the usual witness that quadratic PTFs carry $\Theta(n^3)$ bits.

The separation is then pure arithmetic: $2^{O(Hn^2)}$ (representations) vs $2^{\Omega(n^3)}$ (targets) forces $H=\Omega(n)$.

## 3. Threshold degree and the sandwich (why this is a degree-vs-complexity separation)

- **Threshold degree** $\deg_\pm(f)$ (least degree of a real polynomial sign-representing $f$) is the **"order"** of Minsky & Papert, *Perceptrons* (MIT Press, 1969) — they proved $\deg_\pm(\mathrm{PARITY}_n)=n$ and exhibited functions of threshold degree $\Theta(\sqrt n)$. Modern lower-bound machinery (Sherstov's pattern-matrix method; O'Donnell–Servedio) is **not needed here** — for this target $\deg_\pm$ is only used as the *cheap* invariant pinned at $2$.
- The content is the **gap** between an "ordinary" degree invariant and a structured-representation cost. Lemma 16's $\deg_\pm\le\mathrm{tChow}_\pm\le H^\ast$ makes $\deg_\pm$ a lower bound for both; the target shows this lower bound can be **off by a factor $\Theta(n)$** even at $\deg_\pm=2$. This is the same phenomenon as "low threshold degree but high *weight*/*density*/*sparsity*" separations in the LTF literature (e.g. threshold-of-ANDs vs. degree), and it shows Lemma 6 ($\deg_\pm\le H^\ast$) is far from tight — exactly the repo's stated takeaway.

## 4. The tangential-Chow geometry (naming only — not load-bearing)

The form $P=\theta\prod_h D_h+\sum_h N_h\prod_{g\ne h}D_g$ is, as Lemma 15 records, a **tangent vector to the Chow variety of products of linear forms** (the variety of completely decomposable / "split" forms, classical: Chow–van der Waerden 1937), plus a scalar multiple $\theta\prod_h D_h$ of the base point: differentiating $\prod_h(D_h+tN_h)$ at $t=0$ gives $\sum_h N_h\prod_{g\ne h}D_g$. Tangential/secant varieties of Chow varieties are an active small topic (e.g. work of Oeding and coauthors on "secant and tangential varieties of Chow varieties"; Arrondo–Bernardi), but **none of that AG is needed for the counting proof** — the only facts used are the two degree bounds in §2 (degree $\le H$ in $x$, $\le H+1$ in parameters). I flag this so the lead does not go looking for an algebraic-geometry lemma that the argument does not require. *Confidence on specific modern AG refs: low; on the irrelevance to the proof: high.*

## 5. Assessment of the Mathlib search hits

None of the provided Mathlib hits are the right tool, and the closest-looking ones are false friends:
- `Polynomial.signVariations`, `Polynomial.roots_countP_pos_le_signVariations`, `Polynomial.succ_signVariations_le_X_sub_C_mul` — these are **Descartes' rule of signs** for *univariate* polynomials (sign changes of a coefficient sequence). That is unrelated to the **multivariate sign-condition counting** (Warren/Milnor–Thom) the proof needs; do not try to route the argument through them.
- `Polynomial.card_mahlerMeasure_le_prod` — a count of integer polynomials of bounded degree and bounded Mahler measure. Same *flavor* (cardinality of a polynomial family) but a different mechanism; not applicable.
- `MvPolynomial.degrees_prod_le`, `MvPolynomial.degreeOf_prod_le`, `Polynomial.degree_prod_le` — these *are* the right way to certify the "degree of a product of affine forms is $\le H$" bookkeeping if this were ever formalized, but the target is informal, so they are at most cosmetic.
- `MvPolynomial.indicator`, `degree_quadratic_lt` — peripheral.

**Takeaway:** Mathlib does **not** currently contain the Warren / Oleĭnik–Petrovskiĭ–Milnor–Thom sign-condition bound, so (as Lemma 21 already does) the counting must be invoked as a cited black box, not pulled from Mathlib. *Confidence: high* (I know of no `Warren`/`signCondition` counting lemma in Mathlib as of my cutoff; worth a quick `leanfinder` check for "number of connected components of semialgebraic set" if a formalization is ever attempted, but do not expect a hit).

## Actionable leads

1. **Transcribe Lemmas 20/22, swapping Lemma 19 → Lemma 21 and $\mathcal F_{n,H},H^\ast\to\mathcal T_{n,H},\mathrm{tChow}_\pm$.** Their "Lemma 1" ($2^{m^2/9}$ LTFs) and "Lemma 2" ($2^{n^3/243}$ degree-$2$ PTFs) are about $\deg_\pm$ only and carry over verbatim; the pigeonhole constant $c=\min\{1,a/4C\}$, $a=1/243$ is unchanged. This is the whole proof.
2. **Do the "$\deg_\pm=2$ exactly" upgrade directly in tChow language:** show $\mathrm{tChow}_\pm(f)\le 1\iff\deg_\pm(f)\le 1$ — order $K{=}1$ gives $P=\theta L_1+M_1$, an arbitrary affine form (all LTFs + constants), and order $0$ gives constants. Then $\mathrm{tChow}_\pm(f_n)>H_n\ge1$ forces $\deg_\pm(f_n)\ge2$. (Equivalently route through Lemma 16 + Lemma 11.)
3. **Or upgrade by cardinality, avoiding any characterization:** $\#\{\deg_\pm\le1\}\le 2^{O(n^2)}\ll 2^{n^3/243}$ (Warren/Zuev), so $\{\deg_\pm=2\}$ alone still beats $|\mathcal T_{n,H_n}|$; run the pigeonhole on that subset. Most robust option.
4. **Cite the counting black box as Warren (1968)** (or Milnor–Thom / Basu–Pollack–Roy), exactly as Lemma 21 already does — do not attempt a Mathlib lemma; the multivariate sign-condition bound is not in Mathlib (the `signVariations` hits are univariate Descartes, a false friend).
5. **State the result as the canonical separation** (it implies Lemmas 20/22 via the sandwich $\mathrm{tChow}_\pm\le H^\ast$); the geometric "tangential Chow" naming is descriptive only — the proof needs just degree $\le H$ in $x$ and $\le H+1$ in the parameters.
