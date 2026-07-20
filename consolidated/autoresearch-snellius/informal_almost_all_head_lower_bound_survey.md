I have enough to write the survey from established knowledge (web search isn't permitted in this session, and the core argument is internal to the project anyway). Marking external recollections with confidence levels.

---

# Survey: "Almost all Boolean functions need exponentially many heads"

## Verdict up front

This target is **not a new piece of hard mathematics** — it is the classical **Shannon counting argument** ("almost every object in a low-parameter class is hard"), and the project already contains the only nontrivial input it needs: **Lemma 19** (Warren counting bound for low head complexity). The target follows from Lemma 19 plus the trivial total count $2^{2^n}$ by an elementary optimization. The exponent $2^n/n^2$ is exactly what Lemma 19's per-head cost of $\Theta(n^2)$ bits forces. **The lead should not re-derive Warren / Milnor–Thom or re-prove the sign-pattern count** — that work is Lemma 19.

This is the attention-head analogue of *Shannon's* theorem that almost all Boolean functions need circuits of size $\Theta(2^n/n)$. The only difference in the exponent ($/n^2$ here vs. $/n$ for circuits) comes from the per-unit information capacity: one head carries $\sim n^2$ bits (it is essentially a linear-threshold-shaped object), whereas one gate carries $\sim n$ bits.

## The classical template (the technique to use)

The argument is the **counting / dimension method**, a.k.a. the **probabilistic method in counting form**:

1. **Cheap upper bound on the class size.** $\bigl|\{f : H^*(f)\le H\}\bigr| \le 2^{(\text{small})}$.
2. **Total count.** There are exactly $2^{2^n}$ Boolean functions on $n$ bits.
3. **Compare.** If the class is much smaller than $2^{2^n}$, then a uniform random $f$ lies outside it whp, and *a fortiori* some $f$ has $H^*(f) > H$.

This is literally Shannon's 1949 argument transported to a new model. No first-moment subtleties, no concentration inequalities — it is a pure ratio bound. Step 1 is the entire content, and it is **already done** as Lemma 19.

## The counting input: Lemma 19, Warren, and the softmax subtlety

Lemma 19 states
$$
\log_2 \bigl|\mathcal F_{n,H}\bigr| \le C\,H\,n\bigl(n+\log_2(H+1)\bigr),\qquad \mathcal F_{n,H}=\{f:H^*(f)\le H\}.
$$
The mechanism inside it is the standard one for counting functions realizable by a family with few real parameters:

- **Warren's theorem** (H. E. Warren, *Lower bounds for approximation by nonlinear manifolds*, Trans. AMS **133** (1968), 167–178; **high confidence** on author/year/journal). The number of distinct sign patterns realized by $m$ real polynomials of degree $\le d$ in $k$ variables is at most $\bigl(\tfrac{4edm}{k}\bigr)^k$ for $m\ge k$ (constant $4e$ is the version I recall; some sources write $8e$ — **medium confidence on the exact constant**, irrelevant to the conclusion). Taking logs with $k=$ #parameters $=O(Hn)$, $m=2^n$ (one cleared-denominator score per input), and $d=\mathrm{poly}$ gives $\log_2(\#\text{patterns})=O\!\left(Hn\log_2\frac{2^n}{Hn}\right)=O(Hn^2)$ — exactly the Lemma 19 shape.
- **Ancestors / alternatives** to Warren, in case the lead wants a different route: **Oleĭnik–Petrovskiĭ (1949)**, **Milnor (1964)** *On the Betti numbers of real varieties* (Proc. AMS), **Thom (1965)** — the $\sum b_i \le (O(d))^k$ Betti-number bounds. All **high confidence**.

**The softmax subtlety — already handled.** The score is *not* a polynomial in the raw parameters because of $\exp$ inside the softmax. Lemma 19 evidently routes around this through the project's own **normal-form reductions**: Lemma 10 (linear-fractional normal form), Lemma 13 (affine atom dictionary), Lemma 14 (cleared-denominator polynomial invariant), Lemma 15 (tangential-Chow). After clearing denominators, the per-input score *is* a polynomial in finitely many real parameters on $\{0,1\}^n$ (since each $\alpha^{x_i}\in\{1,\alpha\}$), so Warren applies. This is why I'd reuse Lemma 19 verbatim rather than re-running the count.
- If one ever wanted to count *without* the normal form (directly through $\exp$), the right tool is **Pfaffian / fewnomial** theory: **Khovanskii's fewnomials** (A. Khovanskii, 1980 paper; *Fewnomials*, AMS, 1991) and its learning-theory descendant **Karpinski–Macintyre**, *Polynomial bounds for VC dimension of sigmoidal and general Pfaffian neural networks*, JCSS **54** (1997) (**high confidence**). Not needed here, but worth knowing the softmax/exp is not a real obstacle.
- The general "few real parameters ⟹ few representable functions" principle in learning theory is **Goldberg–Jerrum**, *Bounding the VC dimension of concept classes parameterized by real numbers*, Machine Learning **18** (1995) (**high confidence**). One could phrase the whole counting step as a VC-dimension/growth-function (Sauer–Shelah) bound, but the **direct count in Lemma 19 is cleaner and is what to use.**

## From Lemma 19 to the target (the elementary part)

For completeness, the entire remaining argument — so the lead sees there is nothing hidden:

Let $H=H_n:=\big\lfloor c\,2^n/n^2\big\rfloor$. For a uniform random $f$,
$$
\Pr[H^*(f)\le H]=\frac{|\mathcal F_{n,H}|}{2^{2^n}}.
$$
Since $H\le 2^n$, $\log_2(H+1)\le n+1\le 2n$, so $n+\log_2(H+1)\le 3n$ and
$$
\log_2|\mathcal F_{n,H}|\le C H n\cdot 3n = 3C H n^2 \le 3Cc\,2^n.
$$
Hence $\log_2\Pr[H^*(f)\le H]\le (3Cc-1)\,2^n$. Pick $c=\tfrac{1}{6C}$ so $3Cc=\tfrac12$; then $\Pr[H^*(f)\le H]\le 2^{-2^{n-1}}\to 0$. Therefore $\Pr[H^*(f)\ge c\,2^n/n^2]\to 1$ (after an immaterial constant adjustment to absorb the floor). The worst-case bound is then immediate: positive probability for large $n$ forces an actual $f$ with $H^*(f)\ge c\,2^n/n^2$. The stated $H^*\le 2^n-1$ ceiling is Lemma 9. **All of this is one short paragraph; no new lemma is required.**

## What is open: the matching upper bound (the real companion question)

The argument pins the lower bound at $c\,2^n/n^2$, and this is **counting-optimal** given that each head carries $\Theta(n^2)$ bits (consistent with Lemma 11: one head $=$ a nonconstant LTF, and the number of LTFs on $n$ bits is $2^{\Theta(n^2)}$). The honest gap is:
$$
c\,\frac{2^n}{n^2}\ \le\ \max_f H^*(f)\ \le\ 2^n-1\quad(\text{Lemma 9}).
$$
That is a $\widetilde\Theta(n^2)$ gap. By analogy with **Shannon (lower, 1949) + Lupanov (upper, 1958)** giving the *tight* $\Theta(2^n/n)$ for circuits, the natural open companion is a **Lupanov-style construction** computing *every* $f$ with $O(2^n/n^2)$ heads (each head absorbing its full $\sim n^2$-bit budget toward an arbitrary truth table). I do **not** see such an upper bound in the current lemma stack (best listed is Lemma 9's $2^n-1$), so whether the worst case is $\Theta(2^n/n^2)$, $\Theta(2^n/n)$, or $\Theta(2^n)$ appears **open in this project**. Flagging so the lead can decide whether to chase it next.

## Mathlib hits assessment

None of the provided hits supply the load-bearing tool (Warren / Milnor–Thom sign-pattern counting); Mathlib appears **not** to contain it. Specifically:
- `Polynomial.card_mahlerMeasure_le_prod` — "count integer polynomials in a box" (bounded Mahler measure). Same *spirit* (cardinality of a parametric family) but the wrong norm and over $\mathbb Z$; not usable here.
- `Polynomial.roots_countP_pos_le_signVariations` — Descartes' rule of signs; about roots of one polynomial, not sign patterns of a family.
- `ChevalleyThm.numBound` — real-algebraic complexity bound, but for describing constructible sets, not counting sign cells.
- `sign_apply` / `signHom` / `SignType` — only relevant at the cosmetic level of "sign representation."
- The LYM, Szemerédi-regularity, `Random.randBool`/Bernoulli, `MvPolynomial.indicator/restrictDegree` (finite-field multilinear), and `PairReduction.*` (metric entropy) hits are all off-target.

Since this is an **informal** target, the Mathlib gap doesn't matter for the proof; it would only matter for a future formalization, which would need Warren's bound built first.

## Actionable leads

1. **Cite Lemma 19 as the sole nontrivial input** and finish with the one-paragraph ratio argument above ($H=\lfloor c\,2^n/n^2\rfloor$, $|\mathcal F_{n,H}|/2^{2^n}\le 2^{(3Cc-1)2^n}\to 0$, take $c=1/(6C)$).
2. **Frame it explicitly as the Shannon (1949) counting argument**, the attention analogue of "almost all Boolean functions need $\Theta(2^n/n)$-size circuits"; the $/n^2$ vs $/n$ is the per-head ($\sim n^2$-bit) vs per-gate capacity.
3. **Note the optimization is forced**: $n+\log_2(H+1)\le 2n$ since $H\le 2^n$, so the $\log_2(H+1)$ term never matters and the threshold is exactly $2^n/n^2$.
4. **Do not touch Warren / Milnor–Thom / Pfaffian counting** — it is internal to Lemma 19 (which already handles the softmax via the cleared-denominator normal form, Lemmas 10/13/14/15).
5. **Optional next target**, not this one: a Lupanov-style $O(2^n/n^2)$-head *upper* bound to close the $\widetilde\Theta(n^2)$ gap against Lemma 9 — the genuine open question here.
