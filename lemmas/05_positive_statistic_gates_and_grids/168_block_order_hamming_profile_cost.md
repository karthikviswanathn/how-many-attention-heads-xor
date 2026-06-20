# Block-Order Hamming Profile Cost

## Statement

Let the variables be split into blocks

$$
B_1,\ldots,B_b
$$

of sizes $n_1,\ldots,n_b$, and suppose

$$
f(x)=F(\lvert x_{B_1}\rvert,\ldots,\lvert x_{B_b}\rvert).
$$

For a block order $\pi$, let $L_{\pi}^{\mathrm{Ham}}(F)$ be the sign-change count obtained by reading the Hamming-weight grid

$$
\{0,\ldots,n_1\}\times\cdots\times\{0,\ldots,n_b\}
$$

lexicographically in the block order $\pi$. Define

$$
\operatorname{mhc}(F):=\min_{\pi}L_{\pi}^{\mathrm{Ham}}(F).
$$

Then

$$
H^{*}(f)\leq\operatorname{mhc}(F).
$$

If

$$
\deg_{\pm}(f)=\operatorname{mhc}(F),
$$

then

$$
H^{*}(f)=\deg_{\pm}(f)=\operatorname{mhc}(F).
$$

For each block order $\pi$ and label $b\in\{0,1\}$, let $R_{b,\pi}$ be the number of contiguous runs of label $b$ in the corresponding lexicographic Hamming-grid sequence. Then

$$
H^{*}(f)
\leq
2\min_{\pi}\min\{R_{0,\pi},R_{1,\pi}\}.
$$

More sharply, if label $b$ has first and last membership indicators $\epsilon_{0,\pi}$ and $\epsilon_{1,\pi}$ in the order $\pi$, then

$$
H^{*}(f)\leq
\min_{\pi,b}\left(2R_{b,\pi}-\epsilon_{0,\pi}-\epsilon_{1,\pi}\right).
$$

> **Interpretation.** For multiblock profile predicates, the block order is part of the certificate. Choosing the right order can lower the grid-path variation substantially.

## Proof

For each block order $\pi$, the multi-Hamming profile bound [165_multi_hamming_profile_bound.md](165_multi_hamming_profile_bound.md) gives

$$
H^{*}(f)\leq L_{\pi}^{\mathrm{Ham}}(F).
$$

Taking the minimum over $\pi$ proves

$$
H^{*}(f)\leq\operatorname{mhc}(F).
$$

If $\deg_{\pm}(f)=\operatorname{mhc}(F)$, combine this with the threshold-degree lower bound

$$
\deg_{\pm}(f)\leq H^{*}(f)
$$

to get exactness.

For the run bounds, apply the multigrid run bound [166_multigrid_run_bound.md](166_multigrid_run_bound.md) to each block order $\pi$. It gives

$$
H^{*}(f)\leq2\min\{R_{0,\pi},R_{1,\pi}\}
$$

and the sharper endpoint-adjusted bound for each label $b$. Minimizing over $\pi$ and $b$ gives the displayed inequalities. $\blacksquare$

## Consequence

This theorem is the practical multiblock profile invariant: compute the grid-path sign changes under each block order, then use the best one.
