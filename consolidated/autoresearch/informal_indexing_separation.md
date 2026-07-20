# Problem: The indexing (multiplexer) function is an explicit near-linear separation

## Background and definitions (self-contained)

For $k \geq 1$ the **indexing function** $\mathrm{IDX}_k$ is the Boolean function on $N = 2^k + k$ bits: an **address** $a \in \lbrace 0,1\rbrace^k$ and a **memory** $m \in \lbrace 0,1\rbrace^{2^k}$ whose coordinates are indexed by addresses $b \in \lbrace 0,1\rbrace^k$, defined by
$$
\mathrm{IDX}_k(a, m) = m_a
$$
(output the memory bit at the addressed location). $\deg_{\pm}(g)$ is the threshold degree (least degree of a sign-representing real polynomial). $H^{*}(g)$ is the head complexity.

**Established (cite as given).**
- **(Shatter-rectangle certificate, L37.)** If a Boolean $g$ admits a **shatter-rectangle of order $s$** — a partition of its coordinates into $V_{\mathrm{row}} \sqcup V_{\mathrm{col}}$ and assignments $\rho_S \in \lbrace0,1\rbrace^{V_{\mathrm{row}}}$ ($S \subseteq [s]$), $\kappa_j \in \lbrace0,1\rbrace^{V_{\mathrm{col}}}$ ($j \in [s]$) with $g(\rho_S, \kappa_j) = [\,j \in S\,]$ for all $S, j$ — then there is an absolute constant $c>0$ with $H^{*}(g) \geq \mathrm{tChow}_{\pm}(g) \geq c\,s/\log_2 s$ (for $s$ large).

## Claim to prove

For all large $k$, writing $N = 2^k + k$:

**(a)** $\deg_{\pm}(\mathrm{IDX}_k) \leq k+1$.

**(b)** $\mathrm{IDX}_k$ admits a shatter-rectangle of order $s = 2^k$, hence $H^{*}(\mathrm{IDX}_k) \geq c\,2^k/k = \Omega(N/\log N)$.

**(c)** Therefore $\mathrm{IDX}_k$ is an **explicit separation** of head complexity from threshold degree: $\deg_{\pm}(\mathrm{IDX}_k) = O(\log N)$ while $H^{*}(\mathrm{IDX}_k) = \Omega(N/\log N)$, on a canonical function whose $2^k$ implicit DNF terms **share** the address variables (so it is not a disjoint DNF — outside the reach of the disjoint-DNF bound).

## Guidance (prove every step rigorously)

**Part (a).** For $b \in \lbrace 0,1\rbrace^k$ define $\mathrm{eq}_b(a) = \prod_{i=1}^k \big(a_i b_i + (1-a_i)(1-b_i)\big)$, a degree-$k$ polynomial in $a$ with $\mathrm{eq}_b(a) = 1$ if $a = b$ and $0$ otherwise (for $a, b \in \lbrace0,1\rbrace^k$). Then
$$
m_a = \sum_{b \in \lbrace0,1\rbrace^k} \mathrm{eq}_b(a)\, m_b
$$
holds for all $(a,m)$: exactly one term ($b = a$) is nonzero. This is a multilinear polynomial of degree $k+1$ (degree $k$ in $a$ times degree $1$ in $m$). Since $\mathrm{IDX}_k = m_a \in \lbrace0,1\rbrace$, the polynomial $p = m_a - \tfrac12$ satisfies $p > 0 \iff \mathrm{IDX}_k = 1$ and $p < 0 \iff \mathrm{IDX}_k = 0$, so $p$ sign-represents $\mathrm{IDX}_k$ and $\deg_{\pm}(\mathrm{IDX}_k) \leq \deg p = k+1$.

**Part (b).** Identify $[2^k]$ with the addresses $\lbrace0,1\rbrace^k$. Set $V_{\mathrm{row}} = $ the memory coordinates, $V_{\mathrm{col}} = $ the address coordinates. For $S \subseteq \lbrace0,1\rbrace^k$ let $\rho_S$ be the memory assignment $m_b = [\,b \in S\,]$; for an address $j \in \lbrace0,1\rbrace^k$ let $\kappa_j$ set the address bits to $j$. Then
$$
\mathrm{IDX}_k(\rho_S, \kappa_j) = m_j = [\,j \in S\,].
$$
This is a shatter-rectangle of order $s = 2^k$ (the row $\rho_S$ and column $\kappa_j$ assignments live on the disjoint memory/address coordinates, and the value is membership). By L37, $H^{*}(\mathrm{IDX}_k) \geq c\,2^k/\log_2(2^k) = c\,2^k/k$. Since $N = 2^k + k$, this is $\Omega(N/\log N)$.

**Part (c).** Combine: $\deg_{\pm}(\mathrm{IDX}_k) \leq k+1 = O(\log N)$ (Part a) while $H^{*}(\mathrm{IDX}_k) \geq c\,2^k/k = \Omega(N/\log N)$ (Part b). For large $k$ these differ by a $\Omega(2^k/k^2)$ factor, an explicit near-linear separation. (The positivity-free version $\mathrm{tChow}_{\pm}(\mathrm{IDX}_k) = \Omega(N/\log N)$ also holds, since L37 bounds $\mathrm{tChow}_{\pm}$.) $\blacksquare$

## Pitfalls

- In Part (a), verify $\mathrm{eq}_b(a) \in \lbrace0,1\rbrace$ with $\mathrm{eq}_b(a)=1 \iff a=b$ on the Boolean cube, and that exactly one summand survives so $\sum_b \mathrm{eq}_b(a) m_b = m_a$ identically; conclude degree $k+1$.
- In Part (b), the row assignments touch only memory coordinates and column assignments only address coordinates — a genuine coordinate partition, as L37 requires. The value $\mathrm{IDX}_k(\rho_S,\kappa_j) = m_{\text{(addr }j)} = [j\in S]$ must be checked from the definition.
- The $2^k$ DNF terms of $\mathrm{IDX}_k$ (one per address, each = address-match $\wedge$ memory-bit) share the $k$ address variables, so this is NOT a disjoint monotone DNF; the shatter-rectangle (which needs only the coordinate partition, not disjointness) is what applies.
- State that $N = 2^k + k$ so $k = \Theta(\log N)$ and $2^k = \Theta(N)$.
