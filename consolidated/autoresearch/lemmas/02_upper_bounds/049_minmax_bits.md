# The Bits of the Minimum (and Maximum) of Two Integers Have Head Complexity Two

## Statement

For $x,y\in\{0,1\}^n$ with integer value $I(z)=\sum_{i}2^i z_i$, the $j$-th bit of the minimum, $\mathrm{MIN}_{n,j}(x,y)=\lfloor\min(I(x),I(y))/2^j\rfloor\bmod 2$, and likewise $\mathrm{MAX}_{n,j}$, satisfy
$$
H^{*}(\mathrm{MIN}_{n,j})=H^{*}(\mathrm{MAX}_{n,j})=2\quad(0\le j\le n-2),
$$
with the top bit $j=n-1$ equal to $x_{n-1}\wedge y_{n-1}$ (min) or $x_{n-1}\vee y_{n-1}$ (max), an LTF ($H^{*}=1$).

> **Taking a min/max is a comparison-gated selection, and it is cheap.** Since the $j$-th binary digit of $I(z)$ is exactly $z_j$, $\mathrm{MIN}_{n,j}=x_j$ if $I(x)\le I(y)$ else $y_j$ — a multiplexer choosing bit $j$ of the smaller integer, gated by one comparison. The explicit quadratic $V=(x_j-y_j)(\tfrac12-d)+(x_j+y_j-1)$, $d=I(x)-I(y)$, sign-represents it (its two summands are never simultaneously nonzero), and $V=AB+g$ with $A=x_j-y_j$ — **one-sided after flipping $y_j$** (L15) — so L42 gives $H^{*}\le2$; the function is not an LTF (an affine-parallelogram crossing certificate), so $H^{*}\ge2$. This puts $\min/\max$ with integer comparison (L47) and addition (L48) on the easy weighted-comparison side. The gate being a *single comparison* and the selected values being *single literals* is what keeps it quadratic — unlike an intersection of two general halfspaces (AND of two LTFs), whose threshold degree can be $\Omega(n)$ (Sherstov), hence $H^{*}=\Omega(n)$.

## Proof

**The min-bit is a comparison-gated selection.** $\min(I(x),I(y))=I(x)$ if $I(x)\le I(y)$, else $I(y)$, and $\lfloor I(z)/2^j\rfloor\bmod 2=z_j$, so $\mathrm{MIN}_{n,j}=x_j$ if $I(x)\le I(y)$ else $y_j$ (ties $I(x)=I(y)$ force $x=y$, so $x_j=y_j$).

**Upper bound.** With $d=I(x)-I(y)$, put $V=(x_j-y_j)(\tfrac12-d)+(x_j+y_j-1)$. The two summands have disjoint support ($x_j-y_j\ne0\iff x_j\ne y_j\iff x_j+y_j-1=0$), and case analysis on $(x_j,y_j)$ gives $\mathrm{sign}(V)=2\,\mathrm{MIN}_{n,j}-1$: at $(1,1)$ $V=1$, at $(0,0)$ $V=-1$, at $(1,0)$ $V=\tfrac12-d>0\iff I(x)\le I(y)$, at $(0,1)$ $V=d-\tfrac12>0\iff I(x)>I(y)$ — all matching the selection. Now $V=AB+g$ with $A=x_j-y_j$, $B=\tfrac12-d$, $g=x_j+y_j-1$; flipping $y_j\mapsto z_j=1-y_j$ ([015](../04_closure_and_structure/015_negation_permutation_closure.md)) makes $A=x_j+z_j-1$ one-sided, so by [042](042_affine_plus_oneside_product.md), $H^{*}(\mathrm{MIN}_{n,j})\le2$.

**Lower bound ($j\le n-2$).** The four points (all coords $0$ except) $P_{00}:y_j{=}1$; $P_{01}:x_{j+1}{=}1,y_j{=}1$; $P_{10}:x_j{=}1,y_{j+1}{=}1$; $P_{11}:x_j{=}1,x_{j+1}{=}1,y_{j+1}{=}1$ satisfy $P_{00}+P_{11}=P_{01}+P_{10}$ and carry the crossing pattern $\mathrm{MIN}_{n,j}=0,1,1,0$. By the antipode identity ([002](../01_foundations_and_normal_form/002_antipode_identities.md)) every affine form is equal-summed on the two diagonals, so no one-atom sign-representation can give opposite signs on $\{P_{00},P_{11}\}$ and $\{P_{01},P_{10}\}$: $\mathrm{MIN}_{n,j}$ is not an LTF, so $H^{*}\ge\deg_{\pm}\ge2$. Hence $=2$.

**Max and the top bit.** $V_{\max}=(x_j-y_j)(d+\tfrac12)+(x_j+y_j-1)$ sign-represents $\mathrm{MAX}_{n,j}$ (selection $x_j$ when $I(x)\ge I(y)$); same one-sided-$A$ reduction gives $\le2$, and the same four points (now labelled $1,0,0,1$) give $\ge2$. The top bit: $\min\ge2^{n-1}\iff x_{n-1}\wedge y_{n-1}$, $\max\ge2^{n-1}\iff x_{n-1}\vee y_{n-1}$ — LTFs, $H^{*}=1$. $\blacksquare$

## Consequence

$\min$ and $\max$ of two integers cost exactly two heads per output bit. Together with integer comparison (L47, $\le1$) and addition (L48, $\le3$), the basic arithmetic/relational primitives are all $O(1)$-head — the "easy" weighted-comparison side. The sharp boundary: a min/max selection (gate = one comparison, choices = single bits) stays quadratic, while an intersection of two *arbitrary* halfspaces (AND of two LTFs) can need $\Omega(n)$ heads ([Sherstov, arXiv:0910.4224](https://arxiv.org/abs/0910.4224); $H^{*}\ge\deg_{\pm}$). The methodological note from the catalog applies again: the heuristic admissible-form search over-reports the min-bit's $H^{*}$ (it returns $3$ at $n=5$), but the bounded sign-rank ($\approx2$, a comparison-structured matrix) and the explicit $\mathrm{sign}(AB+g)$ construction give the true value $2$.
