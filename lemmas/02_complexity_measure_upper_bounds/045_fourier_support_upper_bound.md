# Fourier Support-Cost Upper Bound

## Statement

For $S\subseteq\lbrace1,\ldots,n\rbrace$, define the Walsh character

$$ \chi_S(x):=(-1)^{\sum_{i\in S}x_i} = \prod_{i\in S}(1-2x_i). $$

Let $q:\lbrace0,1\rbrace^n\to\lbrace-1,1\rbrace$ be the sign-valued version of $f$, with $q(x)=1$ on $f^{-1}(1)$ and $q(x)=-1$ on $f^{-1}(0)$.

Suppose a Fourier-sparse polynomial

$$ R(x)=\sum_{S\in\mathcal{A}}c_S\chi_S(x) $$

sign-represents $f$, meaning

$$ q(x)R(x)>0 $$

for every $x\in\lbrace0,1\rbrace^n$. Then

$$ H^{\ast}(f) \leq \sum_{\substack{S\in\mathcal{A}\\ S\neq\varnothing}} \left(2^{\lvert S\rvert}-1\right). $$

In particular, if $\mathcal{A}\subseteq\lbrace S:\lvert S\rvert\leq d\rbrace$ and $\lvert\mathcal{A}\rvert=m$, then

$$ H^{\ast}(f)\leq m(2^d-1). $$

As a Fourier-tail corollary, if

$$ \left\lVert q-\sum_{S\in\mathcal{A}}\widehat q(S)\chi_S \right\rVert_{\infty} <1, $$

then the same upper bound holds.

> **Interpretation.** A sparse Walsh sign approximant gives a head upper bound. The cost is not just the number of Fourier terms; a character on $\lvert S\rvert$ bits expands into $2^{\lvert S\rvert}-1$ nonconstant monotone monomials.

## Proof

For each $S$,

$$ \chi_S(x) = \prod_{i\in S}(1-2x_i) = \sum_{U\subseteq S} (-2)^{\lvert U\rvert} \prod_{i\in U}x_i. $$

Thus every nonempty Fourier character $\chi_S$ expands into at most

$$ 2^{\lvert S\rvert}-1 $$

nonconstant monomials in the monotone basis $\prod_{i\in U}x_i$. The constant parts of all characters are absorbed into the overall constant term.

Therefore $R$ is a sign-representing polynomial with at most

$$ \sum_{\substack{S\in\mathcal{A}\\ S\neq\varnothing}} \left(2^{\lvert S\rvert}-1\right) $$

nonconstant monomials before cancellations. By the polynomial-threshold sparsity upper bound [041_ptf_sparsity_upper_bound.md](041_ptf_sparsity_upper_bound.md),

$$ H^{\ast}(f) \leq \sum_{\substack{S\in\mathcal{A}\\ S\neq\varnothing}} \left(2^{\lvert S\rvert}-1\right). $$

If every set in $\mathcal{A}$ has size at most $d$, then each summand is at most $2^d-1$, giving

$$ H^{\ast}(f)\leq m(2^d-1). $$

Finally, suppose

$$ \left\lVert q-\sum_{S\in\mathcal{A}}\widehat q(S)\chi_S \right\rVert_{\infty} <1. $$

Let

$$ R_{\mathcal{A}}(x):=\sum_{S\in\mathcal{A}}\widehat q(S)\chi_S(x). $$

Then for every $x$,

$$ \lvert q(x)-R_{\mathcal{A}}(x)\rvert<1. $$

Since $q(x)\in\lbrace-1,1\rbrace$, this implies $q(x)R&#95;{\mathcal{A}}(x)>0$. Hence $R&#95;{\mathcal{A}}$ sign-represents $f$, and the first part applies. $\blacksquare$

## Consequence

The Fourier-tail threshold-degree certificate [031_fourier_tail_threshold_degree.md](031_fourier_tail_threshold_degree.md) proves low threshold degree by retaining all Fourier levels up to $d$. This lemma gives a direct head bound that can be sharper when only a few low-degree Fourier coefficients need to be retained.

For a degree $d$ Fourier truncation supported on $\mathcal{A}$,

$$ H^{\ast}(f) \leq \sum_{S\in\mathcal{A}}\left(2^{\lvert S\rvert}-1\right), $$

which can be much smaller than the uniform degree-only upper bound

$$ \sum_{r=1}^{d}\binom{n}{r}. $$
