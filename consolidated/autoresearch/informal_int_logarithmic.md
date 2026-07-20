# Problem: An explicit unbounded (logarithmic) separation of head complexity from threshold degree

## Background and definitions (self-contained)

For $n \geq 1$, the **set-intersection function** on $2n$ bits is
$$
\mathrm{INT}_n(x,y) = \bigvee_{i=1}^n (x_i \wedge y_i), \qquad x,y \in \lbrace 0,1\rbrace^n .
$$
$\deg_{\pm}(g)$ is the least degree of a real polynomial that sign-represents the Boolean function $g$ (positive on $g=1$, negative on $g=0$). $H^{*}(g)$ is the head complexity. $\mathrm{sr}_{x|y}(g)$ is the cut sign-rank across the partition separating $x$- from $y$-coordinates (least rank of a real matrix that strictly sign-represents $g$ across that cut).

**Established results (cite as given).**

- **(L33, threshold degree and sign-rank of $\mathrm{INT}_n$.)** $\deg_{\pm}(\mathrm{INT}_n) = 2$ for all $n \geq 2$, and $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \geq n$ for all $n \geq 1$.
- **(L22, flattening bound.)** For every Boolean function $g$ on $N$ bits and every bipartition $A \sqcup B$ of its coordinates, $\mathrm{sr}_{A|B}(g) \leq (H^{*}(g)+1)\,2^{H^{*}(g)} + 1$.

## Claim to prove

For every $n \geq 6$,
$$
H^{*}(\mathrm{INT}_n) \;\geq\; \tfrac12 \log_2 n .
$$
Consequently $H^{*}(\mathrm{INT}_n) \to \infty$ as $n \to \infty$, while $\deg_{\pm}(\mathrm{INT}_n) = 2$ for all $n \geq 2$: $\mathrm{INT}_n$ is an explicit family realizing an **unbounded** gap between head complexity and threshold degree.

## Guidance (prove every step rigorously)

Write $H = H^{*}(\mathrm{INT}_n)$ and $\Phi(H) = (H+1)2^H + 1$.

1. **Combine the two cited bounds.** By L33 and L22 on the cut $x|y$,
   $$
   n \;\leq\; \mathrm{sr}_{x|y}(\mathrm{INT}_n) \;\leq\; \Phi(H) = (H+1)2^H + 1 . \tag{$\ast$}
   $$
   *(justification: chain L33's lower bound with L22's upper bound on the same quantity.)*

2. **$H \geq 2$ when $n \geq 6$.** $\Phi$ is strictly increasing on integers $H \geq 0$ (shown below) with $\Phi(0)=2$, $\Phi(1)=5$. If $H \leq 1$ then $\Phi(H) \leq \Phi(1) = 5$, so $(\ast)$ gives $n \leq 5$. Contrapositively, $n \geq 6 \Rightarrow H \geq 2$.
   - *Monotonicity:* $\Phi(H+1) - \Phi(H) = (H+2)2^{H+1} - (H+1)2^H = 2^H\big(2(H+2) - (H+1)\big) = 2^H(H+3) > 0$.

3. **Elementary inequality: $\Phi(H) \leq 4^H$ for integer $H \geq 2$.**
   - First, $H + 2 \leq 2^H$ for all integers $H \geq 2$. *(Base $H=2$: $4 \leq 4$. Inductive step: if $H+2 \leq 2^H$ then $2^{H+1} = 2\cdot 2^H \geq 2(H+2) = 2H+4 \geq H+3 = (H+1)+2$, using $H \geq 1$.)*
   - Hence, for $H \geq 2$, $\Phi(H) = (H+1)2^H + 1 \leq (H+1)2^H + 2^H = (H+2)2^H \leq 2^H \cdot 2^H = 4^H$. *(justification: $1 \leq 2^H$ since $H \geq 0$, then the previous bullet.)*

4. **Solve for $H$.** Fix $n \geq 6$. By Step 2, $H \geq 2$, so Step 3 applies: $(\ast)$ gives $n \leq \Phi(H) \leq 4^H = 2^{2H}$. Taking $\log_2$ of both sides (monotone), $\log_2 n \leq 2H$, i.e. $H \geq \tfrac12 \log_2 n$.

5. **Unbounded separation.** Since $\tfrac12\log_2 n \to \infty$, $H^{*}(\mathrm{INT}_n) \to \infty$. By L33, $\deg_{\pm}(\mathrm{INT}_n) = 2$ for every $n \geq 2$, a constant. Hence the gap $H^{*}(\mathrm{INT}_n) - \deg_{\pm}(\mathrm{INT}_n) \to \infty$ along an explicit family. $\blacksquare$

## Pitfalls to address explicitly

- The inequality $\Phi(H) \leq 4^H$ is used **only** for $H \geq 2$; it is false at $H=0$ ($\Phi(0)=2 > 1 = 4^0$) and $H=1$ ($\Phi(1)=5 > 4$). The case split via $n \geq 6 \Rightarrow H \geq 2$ (Step 2) is essential — do not apply Step 3 without it.
- $\tfrac12\log_2 n$ is consistent with $H \geq 2$ only once $n \geq 16$; for $6 \leq n \leq 15$ the stated bound $H \geq \tfrac12\log_2 n$ still holds (it is $\leq 2 \leq H$), so the claim is correct for all $n \geq 6$.
- The bound is genuinely logarithmic, not polynomial: $\mathrm{sr}_{x|y}(\mathrm{INT}_n) \leq \binom{2n}{\leq 2} = O(n^2)$ because $\deg_{\pm} = 2$, so $(\ast)$ cannot give more than $H = \Omega(\log n)$. Do not claim a stronger rate.
