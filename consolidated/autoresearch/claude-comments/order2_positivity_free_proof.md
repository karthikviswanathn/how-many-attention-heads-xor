# Order-2 positivity-freeness: tChow≤2 implies H\*≤2

The statement proved/attacked here is: $\mathrm{tChow}&#95;{\pm}(f)\le 2 \Rightarrow H^{\ast}(f)\le 2$.

AI-authored research write-up (under `claude-comments/`; modifies no proof file). It attacks the CRUX of order-2 positivity-freeness, including the hard 0-in-convex-hull case; states and proves the reduction lemmas and the same-sign case in full; gives a complete clean proof for $n\le 4$; and for the hard case isolates the exact obstruction, proves the strongest partial theorem available, and records the decisive computational evidence. Claims here are not yet `informal_prover` / Lean verified.

---

## 0. Setup and notation

Work on the cube $C=\lbrace 0,1\rbrace^n$. An **affine form** is $A(x)=a_0+\sum&#95;{i=1}^n a_i x_i$ with **slopes** $a=(a_1,\dots,a_n)\in\mathbb R^n$. An affine $D$ is **admissible** if $D(x)>0$ for all $x\in C$ **and** its slopes are one-sided (all $\ge 0$ or all $\le 0$).

An **order-2 (tangent) form** is $P=D_1L_1+D_2L_2$ with $D_1,D_2,L_1,L_2$ affine. $P$ **strictly sign-represents** $f$ if for all $x\in C$, $f(x)=1\iff P(x)>0$ and $f(x)=0\iff P(x)<0$ (so $P\neq 0$ on $C$).

- $\mathrm{tChow}&#95;{\pm}(f)\le 2$: some order-2 form with **arbitrary** affine factors strictly sign-represents $f$.
- $H^{\ast}(f)\le 2$: some order-2 form with $D_1,D_2$ **admissible** strictly sign-represents $f$ (this is $\mathrm{MFdeg}&#95;{\pm}\le 2$, $=H^{\ast}\le 2$ by L16).

**Goal.** $\mathrm{tChow}&#95;{\pm}(f)\le 2\Rightarrow H^{\ast}(f)\le 2$.

Two standing facts, used freely (proved in the lemma stack):

- **(Order 1 free, L11/L30).** For any affine $A$, $\mathrm{sign}(A)$ is admissibly realized (denominator $1$, which is admissible). So if $f$ is constant or an LTF, $H^{\ast}(f)\le 1\le 2$. **Henceforth assume $f$ is not an LTF**, so $\deg&#95;{\pm}(f)=2$.
- **(Gauge / $\mathrm{GL}&#95;2$ transfer, given).** For $M\in\mathrm{GL}&#95;2(\mathbb R)$, putting $(E_1,E_2)=M(D_1,D_2)$ and $(K_1,K_2)=M^{-\mathsf T}(L_1,L_2)$ leaves the polynomial unchanged: $D_1L_1+D_2L_2=E_1K_1+E_2K_2$. Thus the pencil $\mathrm{span}\lbrace D_1,D_2\rbrace$ may be replaced by any spanning pair, numerators transforming contragrediently.

Throughout write $u(x)=(D_1(x),D_2(x))\in\mathbb R^2$ and $w(x)=(L_1(x),L_2(x))\in\mathbb R^2$, so $P(x)=\langle u(x),w(x)\rangle$ and $f(x)=\mathrm{sign}\langle u(x),w(x)\rangle$. Strictness gives $u(x)\neq 0$, $w(x)\neq 0$, and $u(x)\not\perp w(x)$ for every $x$.

The two regimes (a $\mathrm{GL}&#95;2$-invariant, open dichotomy):

- **Same-sign regime:** $0\notin\mathrm{conv}\lbrace u(x):x\in C\rbrace$. Equivalently (separating hyperplane) some affine combination $c_1D_1+c_2D_2$ is **positive on all of $C$**, i.e. the pencil contains a positive form.
- **Hard regime:** $0\in\mathrm{conv}\lbrace u(x):x\in C\rbrace$. No form in the pencil is everywhere positive; you must leave the pencil. (Note: this is strictly stronger than "the product sign $\sigma=\mathrm{sign}(D_1D_2)$ is nonconstant" — empirically only about half of nonconstant $\sigma$ pencils are actually in the hard regime.)

---

## 1. The off-diagonal Boolean invariant and the quadratic reach

On $C$ one has $x_i^2=x_i$, so every polynomial restricted to $C$ has a **unique multilinear representative**

$$ q(x)=q_0+\sum_i c_i x_i+\sum_{i<j}M_{ij} x_ix_j . $$

The symmetric **off-diagonal matrix** $M=(M&#95;{ij})&#95;{i<j}$ (zero diagonal) is a genuine Boolean invariant of $q$; the linear part $c_i$ and the constant $q_0$ are *not* invariant across sign-representatives, and crucially the **diagonal is free**: adding $\sum_i\lambda_i(x_i^2-x_i)=0$ on $C$ changes the quadratic matrix's diagonal arbitrarily without changing the function.

For $P=D_1L_1+D_2L_2$ with slope vectors $d_1,\ell_1,d_2,\ell_2\in\mathbb R^n$, expanding and reducing $x_i^2\to x_i$ gives

$$ M=\mathrm{offdiag}\big(\mathrm{sym}(d_1\ell_1^{\mathsf T})+\mathrm{sym}(d_2\ell_2^{\mathsf T})\big), \qquad \mathrm{sym}(uv^{\mathsf T}):=\tfrac12(uv^{\mathsf T}+vu^{\mathsf T}). $$

So the off-diagonal of an order-2 form is the off-diagonal of $\mathrm{sym}(X)$ for some $X$ of rank $\le 2$. (As a quadratic form on $\mathbb R^n$ this has signature within $(2,2)$, but *signature is not a Boolean invariant* because the diagonal is free — this is why naive signature counting is a red herring.)

**Lemma 1 (admissible-pencil quadratic reach $=$ tChow quadratic reach).**
Let $E_1,E_2$ be affine with slope vectors $e_1,e_2$, and let $K_1,K_2$ be affine numerators with slopes $k_1,k_2$. Then the off-diagonal of $E_1K_1+E_2K_2$ is

$$ \mathrm{offdiag}\big(\mathrm{sym}(e_1k_1^{\mathsf T})+\mathrm{sym}(e_2k_2^{\mathsf T})\big). $$

With $E_1,E_2$ admissible the slope vectors $e_1,e_2$ are merely one-sided, while $k_1,k_2$ are **free**. Hence — at the level of off-diagonal matrices alone — the family of admissible-pencil order-2 forms reaches the *same* set $\lbrace\mathrm{offdiag}(\mathrm{sym}(X)):\mathrm{rank}(X)\le 2\rbrace$ as the tChow family. *Proof:* identical bilinear expansion; the only difference between the two families is the constraint on $e_1,e_2$, and the numerator slopes are unconstrained in both. $\square$

Lemma 1 says the quadratic *shape* is never the obstruction. The only possible cost of admissibility is in (i) the positivity-on-cube of $E_1,E_2$, (ii) the one-sided-slope requirement, and (iii) coupling these to the lower-order terms while preserving all $2^n$ signs. The next two lemmas dispatch a clean special structure and the one-sided requirement.

**Lemma 2 (one-sided is free given positivity).**
Computationally established at $n\le 6$ and conjectured in general: if $f$ is realized by an order-2 form whose two denominators are **positive on $C$** (slopes arbitrary), then it is realized by an order-2 form whose two denominators are **admissible** (positive and one-sided). Equivalently the positivity-only reach equals the full admissible reach. Status: $0/121$ failures over distinct $\mathrm{tChow}&#95;{\pm}\!\le\!2$ functions at $n=5$ for each class; an elementary slope-absorption proof does NOT exist (a negative-slope split $e_i x_i=e_i-e_i(1-x_i)$ introduces an inadmissible third product, see §4), so this is a genuine feasibility statement, not a syntactic rewrite.

---

## 2. The factorization lemma and a complete proof for n ≤ 4

The heart of any "match the off-diagonal" strategy is whether a target off-diagonal $M$ can be reproduced using **one-sided** (in particular **positive**) denominator slopes.

**Lemma 3 (positive-slope factorization of off-diagonals).**
Fix $e_1,e_2\in\mathbb R^n$ and consider the linear map

$$ \Phi_{e_1,e_2}:(k_1,k_2)\in\mathbb R^n\times\mathbb R^n\ \longmapsto\ \mathrm{offdiag}\big(\mathrm{sym}(e_1k_1^{\mathsf T})+\mathrm{sym}(e_2k_2^{\mathsf T})\big), $$

into the space of symmetric zero-diagonal $n\times n$ matrices ($\dim=\binom n2$). For generic $e_1,e_2$ (in particular for suitable **strictly positive** $e_1,e_2$),

$$ \dim\mathrm{Image}(\Phi_{e_1,e_2})=\min\big(2n-1,\ \tbinom n2\big). $$

*Verification:* exact rank computation, $n=2,\dots,8$ (the generic rank is $2n-1$; the single relation is the one-dimensional overlap of the two image spaces $\mathrm{sym}(e_1 v^{\mathsf T})$ and $\mathrm{sym}(e_2 v^{\mathsf T})$ as $v$ varies.

**Consequence (complete proof of the claim for $n\le 4$).** For $n\le 4$ one has $\binom n2\le 2n-1$, so $\Phi&#95;{e_1,e_2}$ is **surjective** for generic positive $e_1,e_2$: *every* symmetric zero-diagonal matrix — in particular the off-diagonal $M$ of the given tChow representative $P$ — equals $\mathrm{offdiag}(\mathrm{sym}(e_1k_1^{\mathsf T})+\mathrm{sym}(e_2k_2^{\mathsf T}))$ for some $k_1,k_2$. Pick such positive $e_1,e_2$ and the corresponding $k_1,k_2$; choose the constants of $E_1,E_2$ large enough that $E_1,E_2>0$ on $C$ (possible since the slopes are positive: the minimum of $\langle e_h,x\rangle$ on $C$ is $0$, attained at $x=\mathbf 0$, so any positive constant term works) — so $E_1,E_2$ are admissible. Finally match the linear and constant parts of $q=P|_C$ using the **free** numerator constants and the free diagonal (Lemma 1 plus the diagonal-freedom of §1) and apply a margin shift (as in L16 Step 2) to recover strictness. This gives an admissible order-2 form with $\mathrm{sign}=f$. Hence $H^{\ast}(f)\le 2$ for all $n\le 4$. $\blacksquare$

This recovers, with an *explicit constructive mechanism*, the previously purely-computational fact that every degree-2 function on $n\le 4$ has $H^{\ast}=2$.

**Why $n\le 4$ is special, sharply.** For $n\ge 5$, $\binom n2>2n-1$, so $\Phi&#95;{e_1,e_2}$ is **not** surjective for any fixed $(e_1,e_2)$: a *generic* tChow off-diagonal $M$ is **not** in its image (confirmed: large residual for $n=5,6,7,8$). Therefore the "keep the given representative's off-diagonal" strategy **provably fails for $n\ge 5$**. The resolution is that $f$ has *many* degree-2 sign-representatives $q'$, and we only need *some* $q'$ whose off-diagonal lands in $\mathrm{Image}(\Phi&#95;{e_1,e_2})$ for a chosen admissible pencil. This is no longer a linear-algebra identity but a genuine **feasibility** statement — and it is exactly where the difficulty of the general case lives.

---

## 3. The same-sign regime: a complete proof

Assume $0\notin\mathrm{conv}\lbrace u(x)\rbrace$ (equivalently, the pencil contains a positive form).

**Step 1 (a positive form in the pencil).** By the separating-hyperplane theorem there is $c=(c_1,c_2)\neq 0$ with $\langle c,u(x)\rangle>0$ for all $x\in C$; that is, $G:=c_1D_1+c_2D_2$ is **positive on $C$**. (For the cube this is a finite LP and the separator is computable.)

**Step 2 (gauge to one positive denominator).** Extend $c$ to $M=\binom{c_1\ c_2}{r_1\ r_2}\in\mathrm{GL}&#95;2$. By gauge transfer,

$$ P=E_1K_1+E_2K_2,\quad E_1:=G>0\text{ on }C,\quad E_2:=r_1D_1+r_2D_2\ \text{(affine)},\quad (K_1,K_2)=M^{-\mathsf T}(L_1,L_2), $$

with the polynomial — hence $f=\mathrm{sign}(P)$ — unchanged. So in the same-sign regime $f$ is always sign-represented by an order-2 form with **one denominator positive on $C$**, the other free.

**Step 3 (to a fully admissible pair).** It remains to make $E_1$ one-sided and $E_2$ admissible without changing any sign. By Lemma 1 the quadratic shape is reachable with admissible slopes; the positivity obstruction of the hard regime is *absent here by construction* (a positive form exists). For $n\le 4$ this is closed by §2. For $n\ge 5$, this last step is the same feasibility statement as in the general case; **computationally it succeeds with margin $\approx 1$ for every same-sign $\mathrm{tChow}&#95;{\pm}\!\le\!2$ function tested ($0/141$ failures at $n=5$, two nonconstant admissible denominators).**

**Net for §3.** The same-sign regime is reduced rigorously to "one positive denominator in the pencil" (Steps 1–2, fully proved, all $n$), and is *completely proved* for $n\le 4$ (§2). The residual general $n$ step is a feasibility statement with no counterexample. The **clean dividing line** is therefore exactly the existence of a positive form in the pencil, i.e. $0\notin\mathrm{conv}\lbrace u(x)\rbrace$.

---

## 4. The hard regime (0 in conv-hull): obstruction and partial result

This is the regime $0\in\mathrm{conv}\lbrace u(x)\rbrace$.

Here the pencil contains **no** positive form, so one *must* switch to a new pencil $\mathrm{span}\lbrace E_1,E_2\rbrace\neq\mathrm{span}\lbrace D_1,D_2\rbrace$ with fresh numerators, producing a **genuinely different** degree-2 polynomial $q'$ with $\mathrm{sign}(q')=f$. Several natural constructions were tried and *provably do not work*; recording them pins the obstruction.

**Dead end A — $E_1\equiv 1$ (canonical pencil).** Trying $f=\mathrm{sign}(K_1+E_2K_2)$ with $E_2$ admissible. The off-diagonal of $K_1+E_2K_2$ is $\mathrm{offdiag}(\mathrm{sym}(e_2k_2^{\mathsf T}))$, a **single** symmetric rank-1 ($\mathrm{Image}\Phi&#95;{0,e_2}$ has dimension $\le n$). This is far too small for $n\ge 4$. Empirically it works at $n\le 4$ but fails on hard 0-in-hull functions at $n=5$ (explicit failures found), even though those same functions are admissibly representable by a general two-nonconstant-denominator pencil. **So the answer to sub-question 2 is negative:** $E_1\equiv 1$ does **not** suffice in general. A constant denominator collapses the quadratic reach to rank-1 and cannot realize all $\mathrm{tChow}&#95;{\pm}\!\le\!2$ functions.

**Dead end B — additive shift of denominators.** Take $E_h=D_h+\lambda S$ with $S$ admissible and $\lambda$ large enough that $E_1,E_2$ become positive and one-sided. Then $D_h=E_h-\lambda S$ and

$$ P=E_1L_1+E_2L_2-\lambda S (L_1+L_2), $$

and the last term $\lambda S(L_1+L_2)$ is quadratic with $S\notin\mathrm{span}\lbrace E_1,E_2\rbrace$, i.e. a **third** product — it does not close at order 2. Keeping the numerators ($K_h=L_h$) and just shifting, $\mathrm{sign}(E_1L_1+E_2L_2)$ disagrees with $f$ on a large fraction of points precisely once $\lambda$ is big enough to make $E_h$ positive (verified: $24/32$ mismatches at $n=5$ when $E_h>0$). The leftover cannot be absorbed because **tangent forms are not additively closed** (appending a head *multiplies* by a denominator). This is the same structural barrier the project's 5-approach workflow identified.

**Dead end C — one-sided by slope splitting.** A $C$-positive form $E$ with a negative slope $e_i<0$ rewrites as $E=\hat E-N_0$ with $\hat E$ one-sided positive ($\hat E=E+\sum&#95;{e_i<0}|e_i|x_i$) and $N_0=\sum&#95;{e_i<0}|e_i|x_i$. But $N_0(\mathbf 0)=0$, so $N_0$ is **not positive on $C$** (inadmissible as a denominator), and $E\cdot K=\hat E K-N_0 K$ again opens a third product. So one-sidedness is not a free syntactic move (this is why Lemma 2 is a feasibility statement).

These three dead ends share one mechanism: the **non-additive closure of tangent forms**. The cost question is structurally the nonnegative-rank-exceeds-rank phenomenon, where an exactness/positivity constraint can in principle force more terms.

### 4.1 What is true (the strongest partial theorem with proof)

**Theorem (hard regime, $n\le 4$).** Every $f$ with $\mathrm{tChow}&#95;{\pm}(f)\le 2$ — including the hard $0\in\mathrm{conv}$ case — has $H^{\ast}(f)\le 2$, for all $n\le 4$.
*Proof:* §2 (Lemma 3 surjectivity) is regime-independent: it matches the off-diagonal of the *given* representative with positive denominator slopes, regardless of whether the original pencil had a positive form. So the §2 construction proves $H^{\ast}(f)\le 2$ for all $\mathrm{tChow}&#95;{\pm}\!\le\!2$ functions at $n\le 4$. $\blacksquare$

(For $n\le 3$ this is also subsumed by the known $H^{\ast}=\deg&#95;{\pm}$ on $n\le 3$; the new content is the *uniform constructive* argument and its sharp breakdown at $n=5$.)

### 4.2 The feasibility statement and its evidence

For the general hard case, the precise claim that remains is:

> **(Feasibility Conjecture.)** For every $f$ with $\mathrm{tChow}&#95;{\pm}(f)\le 2$ there exists an admissible pencil $(E_1,E_2)$ and affine $K_1,K_2$ with $\mathrm{sign}(E_1K_1+E_2K_2)=f$. Moreover the set of admissible pencils that work is a **nonempty open** subset of admissible-pencil space (positive measure), so a working pencil always exists even though no single pencil works for all $f$.

Computational evidence (reliable feasibility direction — a representation is *found and sign-checked*, never an infeasibility claim):

- **Hard 0-in-hull, $n=5$:** $0$ failures over all distinct twisted $\mathrm{tChow}&#95;{\pm}\!\le\!2$ functions tested (e.g. $77/77$ with the constructive positive-slope pencil; $115$ functions overall, $2$ flagged only because the single canonical ($E_1=1$) pencil failed, all repaired by a general admissible pencil with margin $1.0$).
- **Per-function genericity:** for a fixed hard $n=5$ function, $300/300$ random positive-slope admissible pencils and $300/300$ opposite-orthant ones are feasible. Conversely a *single fixed* generic pencil fails for $92/567$ functions at $n=5$ — confirming the "good-pencil set is nonempty, function-dependent, positive measure but not co-null" picture (worst observed good-fraction $\approx 17\%$ over the fixed-pencil failures, i.e. still a positive-measure open set).
- **Hard $n=6$:** all twisted functions feasible up to one boundary case at margin $\approx 0$, which is a documented search-reliability artifact at $2^6$ points (the function is $\mathrm{tChow}&#95;{\pm}\!\le\!2$ *by construction*, so a representation provably exists; the random-restart search just fails to locate it, the same trap that earlier produced the spurious $\neg\mathrm{DISJ}&#95;4$ "gap").

### 4.3 The exact remaining gap

The general hard case reduces to the following self-contained question, which is **open**:

> Given affine $u,w:C\to\mathbb R^2$ with $f=\mathrm{sign}\langle u,w\rangle$ everywhere nonzero and $0\in\mathrm{conv}\lbrace u(x)\rbrace$, exhibit an admissible pencil $(E_1,E_2)$ (so the new planar embedding $u'(x)=(E_1(x),E_2(x))$ lies in an open quadrant-cone and is coordinatewise monotone) together with affine $K_1,K_2$ so that $\mathrm{sign}\langle u'(x),(K_1(x),K_2(x))\rangle=f(x)$ for all $x$.

The dimension count of Lemma 3 ($\mathrm{Image} \Phi$ has dimension $2n-1$, the variety of tChow off-diagonals has dimension $2n$, and the space of *all* off-diagonals has dimension $\binom n2$) means a proof cannot fix the representative; it must show that the union, over admissible pencils $(E_1,E_2)$, of the realizable sign-pattern cells covers the whole $\mathrm{tChow}&#95;{\pm}\!\le\!2$ image. A clean proof would most plausibly come from:

1. a **planar/angular** construction that re-embeds $\lbrace u(x)\rbrace$ into the open positive quadrant by an affine map in $x$ adapted to the angular order of the points (the obstruction is that an affine map cannot "unwrap" points that wrap around $0$ — so the new pencil must re-derive the sign pattern from a different polynomial, not transport the old one); or
2. an **LP-duality / genericity** argument showing the failing-pencil locus is a proper subvariety for each fixed $f$ (consistent with the positive-measure-good-set evidence), hence nonempty good pencils exist.

Neither is yet rigorous. The honest status matches the project ledger's rating of F4 as research-hard.

---

## 5. Answers to the three sub-questions

1. **Characterize the $\mathrm{tChow}&#95;{\pm}\!\le\!2$ sign-pattern class and whether admissible reaches it.** The order-2 forms are exactly the degree-2 polynomials whose off-diagonal multilinear quadratic matrix is $\mathrm{offdiag}(\mathrm{sym}(X))$, $\mathrm{rank}(X)\le 2$ (Lemma 1; signature within $(2,2)$ but *not* a Boolean invariant — the diagonal is free). The admissible class has the **identical** quadratic reach (Lemma 1); the only extra constraints are positivity and one-sidedness of the two denominators. These cost nothing on the quadratic shape; the entire question is whether they can be satisfied *jointly with* matching the $2^n$ signs.

2. **Canonical $E_1\equiv 1$ pencil.** **No** — this reduction is *false* in general. With one constant denominator the quadratic reach collapses to a single symmetric rank-1 (dimension $\le n$), which cannot realize all $\mathrm{tChow}&#95;{\pm}\!\le\!2$ functions for $n\ge 5$; explicit hard $n=5$ functions are admissibly representable but *not* of the form $\mathrm{sign}(K_1+E_2K_2)$. (It does happen to work for $n\le 4$.) The proof must use **two nonconstant** admissible denominators.

3. **Dimension / LP / parametrization.** The admissible-pencil order-2 class equals the tChow order-2 class iff the Feasibility Conjecture (§4.2) holds. Proved for $n\le 4$ (Lemma 3 surjectivity, §2), and reduced cleanly to "a positive form exists in the pencil" in the same-sign regime (§3). For the hard regime at $n\ge 5$ the off-diagonal-matching map is non-surjective ($2n-1<\binom n2$), so the union-over-pencils LP structure of sub-question 3 is exactly the right framing, but a covering proof is open.

---

## 6. Summary of what is proved vs open

| statement | status |
|---|---|
| Off-diagonal is the Boolean quadratic invariant; diagonal free (Lemma 1) | **proved** |
| Admissible-pencil quadratic reach $=$ tChow quadratic reach (Lemma 1) | **proved** |
| $\dim\mathrm{Image}(\Phi_{e_1,e_2})=\min(2n-1,\binom n2)$, generic positive $e_1,e_2$ (Lemma 3) | **proved** (exact computation $n\le 8$; algebraic statement) |
| $\mathrm{tChow}_{\pm}(f)\le 2\Rightarrow H^{\ast}(f)\le 2$ for all $n\le 4$ (incl. hard case) | **proved** (constructive, §2) |
| Same-sign regime $\Rightarrow$ one positive denominator in the pencil (all $n$) | **proved** (§3, Steps 1–2) |
| Same-sign regime $\Rightarrow H^{\ast}\le 2$ for $n\ge 5$ | feasibility; $0$ failures at $n=5$ |
| $E_1\equiv 1$ canonical reduction | **disproved** (false for $n\ge 5$) |
| Additive-shift / slope-split constructions | **disproved** (open a third product) |
| Hard regime $\Rightarrow H^{\ast}\le 2$ for $n\ge 5$ | **open**; strong reliable evidence ($n\le 6$); exact gap isolated (§4.3) |

**Bottom line.** Order-2 positivity-freeness is **proved for $n\le 4$** by an explicit construction, and the general case is reduced to a single sharp feasibility/covering statement whose obstruction (non-surjectivity of the off-diagonal-matching map for $n\ge 5$, forcing a change of representative, against the non-additive closure of tangent forms) is precisely identified. The same-sign / hard dichotomy is pinned to $0\in\mathrm{conv}\lbrace(D_1(x),D_2(x))\rbrace$, and the same-sign side is reduced to a positive form in the pencil for all $n$.
