# Problem: The minimized positive-order alternation number bounds head complexity (and is exact for symmetric f)

## Background and definitions (self-contained)

Fix $n \geq 1$, work on $\{0,1\}^n$. A weight vector $w = (w_1,\dots,w_n)$ with all $w_i > 0$ is **generic** if the linear form $t_w(x) = \sum_i w_i x_i$ takes $2^n$ distinct values on the cube (equivalently, no two distinct subsets have equal $w$-sum). Generic positive $w$ exist (e.g. $w_i = 2^{i-1}$).

For a generic positive $w$, $t_w$ induces a strict total order on $\{0,1\}^n$; list the points as $x^{(1)}, x^{(2)}, \dots, x^{(2^n)}$ with $t_w(x^{(1)}) < \dots < t_w(x^{(2^n)})$. Define the **alternation count**

$$
A_w(f) = \#\{\, j \in \{1,\dots,2^n-1\} : f(x^{(j)}) \neq f(x^{(j+1)}) \,\},
$$

and the **minimized positive-order alternation number**

$$
A_{+}(f) = \min_{w>0 \text{ generic}} A_w(f).
$$

**Established results (cite as given):**
- **(Weighted-score upper bound.)** If $g(x) = G(t(x))$ for a positive weighted sum $t$ with image of size $M$, and $C$ is the number of sign changes of $G$ along the increasing values of $t$, then $H^{*}(g) \leq C$.
- **(Symmetric exact value, L12.)** If $f$ is symmetric, $f(x) = F(|x|)$, then $H^{*}(f) = C(F)$, the number of $k \in \{1,\dots,n\}$ with $F(k-1) \neq F(k)$.

## Claim to prove

**(a) General upper bound.** For every $f : \{0,1\}^n \to \{0,1\}$,

$$
H^{*}(f) \leq A_{+}(f).
$$

**(b) Exact for symmetric $f$.** If $f$ is symmetric then $A_{+}(f) = C(F) = H^{*}(f)$.

Thus $A_{+}$ is a simple, computable invariant (the minimum number of times $f$ alternates along a positive linear ordering of the cube) that upper-bounds head complexity in general and equals it for symmetric functions, recovering L12.

## Guidance (prove every step rigorously)

**Part (a).** Fix any generic positive $w$ achieving $A_w(f) = A_+(f)$ (the min over the finite set of order-types is attained). Since $t_w$ has $2^n$ distinct values, $f$ is (trivially) a function of $t_w$: $f(x) = G(t_w(x))$ where $G(t_w(x^{(j)})) = f(x^{(j)})$. The number of sign changes of $G$ along the increasing values of $t_w$ is exactly $A_w(f)$. By the weighted-score upper bound, $H^{*}(f) \leq A_w(f) = A_+(f)$.

**Part (b).** Let $f$ be symmetric, $f(x) = F(|x|)$.

1. **$A_+(f) \leq C(F)$.** Choose a generic positive $w$ with all $w_i$ close to $1$ (e.g. $w_i = 1 + i\eta$ for small $\eta > 0$, generic for small enough $\eta$) so that the $t_w$-order refines the Hamming-weight order: any $x$ with $|x| < |y|$ has $t_w(x) < t_w(y)$ (possible because for small $\eta$ the weight differences cannot overcome a unit gap in Hamming weight). Then in the $t_w$-order the points appear grouped by Hamming weight, blocks $|x|=0,1,\dots,n$ in order. Within a block $f$ is constant ($=F(k)$), so no alternation occurs inside a block; an alternation occurs only at a block boundary $k \to k+1$, exactly when $F(k) \neq F(k+1)$. Hence $A_w(f) = C(F)$, so $A_+(f) \leq C(F)$.

2. **$A_+(f) \geq C(F)$.** Let $w$ be any generic positive weight. Consider the Hamming chain $\emptyset = S_0 \subset S_1 \subset \dots \subset S_n = \{1,\dots,n\}$ obtained by adding coordinates one at a time (any fixed order), with indicator points $z^{(0)}, z^{(1)}, \dots, z^{(n)}$, $|z^{(k)}| = k$. Since each $z^{(k+1)}$ is $z^{(k)}$ with one more coordinate set to $1$ and $w > 0$, $t_w(z^{(k)}) < t_w(z^{(k+1)})$. So $z^{(0)}, \dots, z^{(n)}$ is an increasing subsequence of the $t_w$-order, with $f(z^{(k)}) = F(k)$. The number of alternations of $f$ along this subsequence is $C(F)$. Since the number of alternations of a sequence is at least the number of alternations of any subsequence, $A_w(f) \geq C(F)$. As $w$ was arbitrary, $A_+(f) \geq C(F)$.

3. Combining, $A_+(f) = C(F)$, and by L12 this equals $H^{*}(f)$.

Also include the following **remark** (it need not be proved in full, but state it): $A_{+}$ is *not* tight in general. For $f(x) = \mathbf{1}[x_1 \geq x_2]$ (a linear threshold function, so $H^{*}(f) = 1$), every positive ordering puts $00$ first and $11$ last with $10, 01$ in the middle in some order, giving truth values $1,1,0,1$ or $1,0,1,1$ along $t_w$, hence $A_w(f) = 2$ for all generic positive $w$ and $A_+(f) = 2 > 1 = H^{*}(f)$. The gap reflects that a single head's *numerator* may be any affine form (including mixed-sign), which a single monotone score cannot mimic.

Give a complete, rigorous proof of (a) and (b).
