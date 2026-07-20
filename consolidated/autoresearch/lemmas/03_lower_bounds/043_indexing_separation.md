# The Indexing (Multiplexer) Function Is an Explicit Near-Linear Separation

## Statement

For $k \geq 1$ the indexing function $\mathrm{IDX}_k(a, m) = m_a$ (address $a \in \lbrace 0,1\rbrace^k$, memory $m \in \lbrace 0,1\rbrace^{2^k}$) on $N = 2^k + k$ bits satisfies, for all large $k$,

$$
\deg_{\pm}(\mathrm{IDX}_k) \leq k+1 = O(\log N), \qquad H^{*}(\mathrm{IDX}_k) \geq \frac{c\,2^k}{k} = \Omega\!\left(\frac{N}{\log N}\right).
$$

Hence $\mathrm{IDX}_k$ is an **explicit near-linear separation** of head complexity from threshold degree, on a canonical function.

> A second named explicit separation after $\mathrm{INT}_n$ (L35), of a different flavor: $\mathrm{IDX}_k$ is the storage-access / multiplexer function central in communication and circuit complexity, and its $2^k$ implicit DNF terms (one per address, each = address-match $\wedge$ memory-bit) **share** the $k$ address variables — so it is *not* a disjoint DNF. The lower bound comes from the shatter-rectangle (L37), which needs only a coordinate partition, not disjointness; this is exactly why L37 is strictly more general than the disjoint-DNF bound (L36). The separation here is even sharper in ratio than $\mathrm{INT}_n$: $\deg_{\pm}$ is *logarithmic* while $H^{*}$ is near-linear.

## Proof

**Threshold degree (upper).** For $b \in \lbrace 0,1\rbrace^k$ let $\mathrm{eq}_b(a) = \prod_{i=1}^k\big(a_i b_i + (1-a_i)(1-b_i)\big)$, a degree-$k$ polynomial equal to $1$ if $a = b$ and $0$ otherwise on the cube. Then $m_a = \sum_{b} \mathrm{eq}_b(a)\,m_b$ identically (the unique surviving term is $b = a$), a multilinear polynomial of degree $k+1$. Since $\mathrm{IDX}_k \in \lbrace 0,1\rbrace$, $p = m_a - \tfrac12$ sign-represents it, so $\deg_{\pm}(\mathrm{IDX}_k) \leq k+1$.

**Head complexity (lower).** Identify $[2^k]$ with addresses $\lbrace 0,1\rbrace^k$. Take $V_{\mathrm{row}} = $ memory coordinates, $V_{\mathrm{col}} = $ address coordinates; for $S \subseteq \lbrace 0,1\rbrace^k$ set $\rho_S$ to be the memory $m_b = [b \in S]$, and for $j \in \lbrace 0,1\rbrace^k$ set $\kappa_j$ to address $j$. Then $\mathrm{IDX}_k(\rho_S, \kappa_j) = m_j = [j \in S]$. This is a shatter-rectangle of order $s = 2^k$ (row and column assignments live on the disjoint memory/address coordinate blocks). By the shatter-rectangle certificate [037_shatter_rectangle_lower.md](037_shatter_rectangle_lower.md), $H^{*}(\mathrm{IDX}_k) \geq \mathrm{tChow}_{\pm}(\mathrm{IDX}_k) \geq c\,2^k/\log_2(2^k) = c\,2^k/k$.

**Separation.** With $N = 2^k + k$, $k = \Theta(\log N)$ and $2^k = \Theta(N)$, so $\deg_{\pm}(\mathrm{IDX}_k) = O(\log N)$ while $H^{*}(\mathrm{IDX}_k) = \Omega(N/\log N)$: the ratio is $\Omega(2^k/k^2) \to \infty$. $\blacksquare$

## Consequence

The explicit-separation phenomenon is not special to set intersection: a canonical, overlapping-term function exhibits it too, with a *logarithmic* threshold degree against near-linear head complexity (a wider ratio than $\mathrm{INT}_n$, where $\deg_{\pm}=2$ but $N=2n$). It is positivity-free ($\mathrm{tChow}_{\pm}(\mathrm{IDX}_k) = \Omega(N/\log N)$ too). Together with $\mathrm{INT}_n$ (disjoint, $\deg_{\pm}=2$) and disjoint monotone DNFs (L36), $\mathrm{IDX}_k$ shows the shatter-rectangle method covers the natural "membership/addressing" structures regardless of whether the implicit terms are disjoint — the operative hypothesis is the row/column coordinate partition, not term-disjointness.
