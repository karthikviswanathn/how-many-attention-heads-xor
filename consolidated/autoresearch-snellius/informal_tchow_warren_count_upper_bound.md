# Warren Counting Bound for Unrestricted Tangential-Chow Complexity

Let $n,H \geq 1$. For affine forms $L_h(x)=a_{h,0}+\sum_{i=1}^{n}a_{h,i}x_i$ and $M_h(x)=b_{h,0}+\sum_{i=1}^{n}b_{h,i}x_i$, and a scalar $\theta\in\mathbb R$, define an unrestricted tangential-Chow sign-representer of order $H$ by

$$
P(x)=\theta\prod_{h=1}^{H}L_h(x)+\sum_{h=1}^{H}M_h(x)\prod_{g\neq h}L_g(x).
$$

Say $f:\{0,1\}^{n}\to\{0,1\}$ has $\mathrm{tChow}_{\pm}(f)\leq H$ if such a $P$ satisfies $P(x)\neq 0$ on the Boolean cube and

$$
f(x)=1 \quad\Longleftrightarrow\quad P(x)>0.
$$

Let

$$
\mathcal T_{n,H}:=\{f:\{0,1\}^{n}\to\{0,1\}:\mathrm{tChow}_{\pm}(f)\leq H\}.
$$

Then there is an absolute constant $C>0$ such that

$$
\log_2 |\mathcal T_{n,H}| \leq C H n\bigl(n+\log_2(H+1)\bigr).
$$

Equivalently, unrestricted tangential-Chow forms of order $H$ realize at most $2^{C H n(n+\log_2(H+1))}$ strict Boolean-cube sign patterns.

## Context

This is an informal (natural-language) target in the one-layer attention
head-complexity project; see `model.md` for the model and `lemmas.md` for the
proved stack. Give a fully rigorous, self-contained proof.

## Known results to build on (from literature survey)

## Actionable leads
1. **Copy `019_warren_head_count_upper_bound.md` near-verbatim**, substituting $L_h,M_h$ for $D_h,N_h$ and the class $\mathcal T_{n,H}$ for $\mathcal F_{n,H}$ — same three sub-lemmas, same constants.
2. In that copy's "Lemma 1," **replace the "By Lemma 14… cleared-denominator polynomial" step with "by definition of $\mathrm{tChow}_\pm(f)\le H$, the order-$H$ form $P$ is given; pad order-$K<H$ witnesses by $L_h\equiv1,M_h\equiv0$"** — and delete the admissibility-shrinking sentence (no constraints here).
3. **Warren's sign-condition bound** is the only external input: $m$ polys, $\ell$ vars, degree $d$ $\Rightarrow$ $\le (Adm/\ell)^\ell$ sign conditions for $m\ge\ell$ (Warren 1968; clean form in Alon's *Tools from Higher Algebra* or Basu–Pollack–Roy).
4. **Bookkeeping that produces the bound:** $\ell=1+2H(n+1)\le 5Hn$ parameters, degree $d=H+1$ (from $\theta\prod_h L_h$, which is where $\log_2(H+1)$ comes from), $m=2^n$ points.
5. **Keep the two-case split:** $m\ge\ell$ via Warren; $m<\ell$ via the trivial $|\mathcal T_{n,H}|\le 2^{2^n}$ with $2^n<\ell\le 5Hn$ — identical to Lemma 19's Lemmas 2–3.
