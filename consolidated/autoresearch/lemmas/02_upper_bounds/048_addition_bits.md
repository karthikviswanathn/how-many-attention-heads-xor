# Every Output Bit of Integer Addition Has Head Complexity at Most Three

## Statement

For $x,y\in\{0,1\}^n$ let $S=I(x)+I(y)$, $I(x)=\sum_{i=0}^{n-1}2^i x_i$, and let $\mathrm{ADD}_{n,j}(x,y)=\lfloor S/2^j\rfloor\bmod 2$ be the $j$-th output bit ($j=0$ LSB, $j=n$ carry-out). Then for all $n$ and all $0\le j\le n$,
$$
H^{*}(\mathrm{ADD}_{n,j})\le 3 ,
$$
with $H^{*}=1$ for the carry-out ($j=n$, an LTF), $H^{*}=2$ for the LSB ($j=0$, $=x_0\oplus y_0$), and $H^{*}\in\{2,3\}$ for every interior bit.

> **The carry chain is free.** Despite bit $j$ depending sequentially on all $j$ lower bits through carry propagation, every addition bit needs only a *constant* number of heads. The carry into position $j$ is a threshold of the positive weighted sum $A'=I(x_{\le j})+I(y_{\le j})$, and the output bit is a function of that *single* sum with at most three sign changes (it runs $0,1,0,1$ over four half-periods $\lfloor A'/2^j\rfloor=0,1,2,3$). So addition sits on the easy weighted-score side of the dichotomy (L25/L47), not the multiplicative/membership side — a sharp contrast with multiplication, whose bits are not functions of any single weighted sum. *Methodological note:* a random-restart admissible-form search badly over-reports here ($5,6,7$ heads at $n{=}4$); those are search failures. The bit's $x|y$ matrix is a diagonal-conjugated comparison matrix (sign-rank $\le3$), the structural tell that $H^{*}$ is in fact bounded — the same over-reporting caution as the equality control behind L46.

## Proof

**Locality.** Write $S=A'+2^{j+1}H$ with $A'=I(x_{\le j})+I(y_{\le j})=\sum_{i=0}^{j}2^i(x_i+y_i)$ and $H$ an integer. Since $2^{j+1}H$ contributes nothing to bits $0,\dots,j$, $\mathrm{ADD}_{n,j}=\lfloor A'/2^j\rfloor\bmod 2$, a function of $A'$ alone (so it ignores bits $>j$; junta invariance L21).

**Weighted score with $\le3$ sign changes.** $A'$ is a positive weighted sum (weights $2^i>0$) with $\mathrm{Im}(A')=\{0,\dots,2^{j+2}-2\}$ (each $x_i+y_i\in\{0,1,2\}$; redundant binary fills the interval). For $F(a)=\lfloor a/2^j\rfloor\bmod 2$, the quotient $\lfloor a/2^j\rfloor$ runs through $0,1,2,3$ on the four blocks $[0,2^j),[2^j,2^{j+1}),[2^{j+1},3\cdot2^j),[3\cdot2^j,2^{j+2}-2]$, so $F=0,1,0,1$: $C(F)\le 3$ (and $=2$ at $j=0$ where the top block is absent, $=1$ at $j=n$ where $A'=S$ spans only two blocks). By the weighted-score bound [025](025_weighted_score_upper.md), $H^{*}(\mathrm{ADD}_{n,j})\le C(F)\le 3$.

**Lower bound (non-carry bits).** For $0\le j\le n-1$, fix the lower bits $x_i=y_i=0$ ($i<j$) so the incoming carry is $0$; then $\mathrm{ADD}_{n,j}$ restricts on $(x_j,y_j)$ to $x_j\oplus y_j$, a 2-bit checkerboard, so $H^{*}\ge2$ ([003](../01_foundations_and_normal_form/003_checkerboard_obstruction.md)). Hence the LSB is exactly $2$ and interior bits are in $\{2,3\}$. $\blacksquare$

## Consequence

Integer addition is *cheap* for attention: all $n+1$ output bits together are computable with $O(1)$ heads each. This places addition firmly with equality (L46) and integer comparison (L47) on the easy side — functions of a single positive weighted sum / linear comparison — and the carry, being itself such a threshold, is absorbed at no asymptotic cost. The result also reinforces the catalog's caution that the heuristic head-complexity search returns *upper bounds only* and over-reports; the bit's bounded sign-rank ($\le3$, since its matrix is a diagonal conjugate of the comparison $\mathrm{sign}(I(x_{<j})+I(y_{<j})-2^j)$) is the reliable structural indicator of bounded $H^{*}$.
