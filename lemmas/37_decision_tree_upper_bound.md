# Decision-Tree Leaf-Profile Upper Bound

## Statement

Let $\mathcal{T}$ be a deterministic decision tree computing

$$
f:\{0,1\}^n\to\{0,1\}.
$$

For a leaf $\ell$, let $P_\ell$ be the set of variables fixed to $1$ along the root-to-leaf path, and let $N_\ell$ be the set of variables fixed to $0$ along that path. Let $\mathcal{L}_1$ and $\mathcal{L}_0$ be the leaves labeled $1$ and $0$.

Then

$$
H^{*}(f)
\leq
\min\left\{
\sum_{\ell\in\mathcal{L}_1}2^{\lvert P_\ell\rvert},
\sum_{\ell\in\mathcal{L}_1}2^{\lvert N_\ell\rvert},
\sum_{\ell\in\mathcal{L}_0}2^{\lvert P_\ell\rvert},
\sum_{\ell\in\mathcal{L}_0}2^{\lvert N_\ell\rvert}
\right\}.
$$

In particular, if $\mathcal{T}$ has depth at most $d$, then

$$
H^{*}(f)
\leq
2^d\min\{\lvert\mathcal{L}_0\rvert,\lvert\mathcal{L}_1\rvert\}.
$$

If $f$ is nonconstant and has deterministic decision-tree depth $D(f)=d\geq1$, then

$$
H^{*}(f)\leq2^{2d-1}.
$$

> **Interpretation.** Adaptive decision structure gives a head upper bound controlled by the signed leaf profile, independent of the ambient number of variables except through the variables actually queried on paths.

## Proof

Each $1$-leaf $\ell\in\mathcal{L}_1$ contributes the mixed-literal certificate term

$$
T_\ell(x)
:=
\left(\prod_{i\in P_\ell}x_i\right)
\left(\prod_{j\in N_\ell}(1-x_j)\right).
$$

The accepting leaves partition $f^{-1}(1)$, so

$$
f(x)=\bigvee_{\ell\in\mathcal{L}_1}T_\ell(x).
$$

Applying the DNF literal-expansion upper bound [36_dnf_cnf_literal_expansion_upper_bound.md](36_dnf_cnf_literal_expansion_upper_bound.md) gives

$$
H^{*}(f)
\leq
\min\left\{
\sum_{\ell\in\mathcal{L}_1}2^{\lvert P_\ell\rvert},
\sum_{\ell\in\mathcal{L}_1}2^{\lvert N_\ell\rvert}
\right\}.
$$

Similarly, the rejecting leaves give

$$
1-f(x)=\bigvee_{\ell\in\mathcal{L}_0}T_\ell(x).
$$

The same DNF bound applied to $1-f$ gives

$$
H^{*}(1-f)
\leq
\min\left\{
\sum_{\ell\in\mathcal{L}_0}2^{\lvert P_\ell\rvert},
\sum_{\ell\in\mathcal{L}_0}2^{\lvert N_\ell\rvert}
\right\}.
$$

Complement invariance from [22_restrictions_and_sign_rank.md](22_restrictions_and_sign_rank.md) gives $H^{*}(f)=H^{*}(1-f)$, so the four-term minimum follows.

If the tree has depth at most $d$, then for every leaf

$$
\lvert P_\ell\rvert\leq d,
\qquad
\lvert N_\ell\rvert\leq d.
$$

Therefore

$$
\sum_{\ell\in\mathcal{L}_b}2^{\lvert P_\ell\rvert}
\leq
2^d\lvert\mathcal{L}_b\rvert,
\qquad
\sum_{\ell\in\mathcal{L}_b}2^{\lvert N_\ell\rvert}
\leq
2^d\lvert\mathcal{L}_b\rvert
$$

for $b\in\{0,1\}$, proving

$$
H^{*}(f)
\leq
2^d\min\{\lvert\mathcal{L}_0\rvert,\lvert\mathcal{L}_1\rvert\}.
$$

Finally, a depth-$d$ binary decision tree has at most $2^d$ leaves. If $f$ is nonconstant, both labels occur, so

$$
\min\{\lvert\mathcal{L}_0\rvert,\lvert\mathcal{L}_1\rvert\}
\leq
2^{d-1}.
$$

Thus

$$
H^{*}(f)\leq2^d2^{d-1}=2^{2d-1}.
$$

$\blacksquare$

## Consequence

If a function is computed by a shallow decision tree, then its head complexity is bounded in terms of the tree depth alone:

$$
H^{*}(f)\leq2^{2D(f)-1}
$$

for every nonconstant $f$ with $D(f)\geq1$.

The leaf-profile bound can be sharper. If all accepting leaves have at most $r$ negative literals after choosing the original orientation, then

$$
H^{*}(f)\leq\lvert\mathcal{L}_1\rvert\,2^r.
$$

The analogous statements hold for rejecting leaves and after the global bit flip.
