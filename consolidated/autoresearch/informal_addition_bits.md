# Problem: Every output bit of integer addition has head complexity at most three

## Background and definitions (self-contained)

For $x\in\{0,1\}^n$ write the integer value $I(x)=\sum_{i=0}^{n-1}2^i x_i\in\{0,\dots,2^n-1\}$. For inputs $x,y\in\{0,1\}^n$ let $S=I(x)+I(y)\in\{0,\dots,2^{n+1}-2\}$ be their integer sum, and for $0\le j\le n$ let
$$
\mathrm{ADD}_{n,j}(x,y)=\Big\lfloor S/2^j\Big\rfloor \bmod 2
$$
be the **$j$-th output bit of addition** (so $j=0$ is the least significant bit, $j=n$ is the carry-out). This is the bit computed at position $j$ of a ripple-carry adder, $\mathrm{ADD}_{n,j}=x_j\oplus y_j\oplus c_j$ with carry $c_j$, but we will not need the recursive carry form.

**Established results (cite as given).**
- **(L25, weighted-score sign changes.)** If $h(u)=F(t(u))$ for a positive weighted sum $t(u)=\sum_k c_k u_k$ ($c_k>0$) and $F:\mathrm{Im}(t)\to\{0,1\}$, then $H^{*}(h)\le C(F)$, the number of sign changes of $F$ along the increasing order of $\mathrm{Im}(t)$.
- **(L3, checkerboard obstruction.)** A 2-bit checkerboard restriction forces $H^{*}\ge 2$.
- **(L21, junta invariance.)** $H^{*}$ is unchanged by adding/removing irrelevant variables.

## Claim to prove

For all $n$ and all $0\le j\le n$,
$$
H^{*}(\mathrm{ADD}_{n,j})\le 3 .
$$
More precisely: the carry-out $\mathrm{ADD}_{n,n}$ has $H^{*}\le1$ (a linear threshold function), the least significant bit $\mathrm{ADD}_{n,0}=x_0\oplus y_0$ has $H^{*}=2$, and every interior bit ($1\le j\le n-1$) has $H^{*}\in\{2,3\}$. In particular **the head complexity of every addition bit is bounded by an absolute constant, independent of $n$ and $j$** — the carry chain costs nothing.

## Guidance (prove every step rigorously)

**Step 1 (locality: bit $j$ depends only on the low bits).** Split $I(x)=I(x_{\le j})+2^{j+1}I(x_{>j})$ where $I(x_{\le j})=\sum_{i=0}^{j}2^i x_i$ and $I(x_{>j})=\sum_{i>j}2^{i-j-1}x_i$. Then $S=A'+2^{j+1}H$ with $A'=I(x_{\le j})+I(y_{\le j})$ and $H=I(x_{>j})+I(y_{>j})$ an integer. Since $2^{j+1}H$ is a multiple of $2^{j+1}$, it contributes $0$ to bits $0,\dots,j$ of $S$; hence
$$
\mathrm{ADD}_{n,j}(x,y)=\big\lfloor A'/2^j\big\rfloor \bmod 2 ,
$$
a function of $A'$ alone. (For $j=n$ there is no "$>j$" part and $A'=S$.)

**Step 2 ($A'$ is a positive weighted sum, and the bit has $\le 3$ sign changes).** $A'=\sum_{i=0}^{j}2^i(x_i+y_i)$ is a positive weighted sum of the $2(j+1)$ variables $x_0,\dots,x_j,y_0,\dots,y_j$ (all weights $2^i>0$). Its range is $\mathrm{Im}(A')=\{0,1,\dots,2^{j+2}-2\}$ (each $x_i+y_i\in\{0,1,2\}$, redundant binary covers the full interval). Let $F(a)=\lfloor a/2^j\rfloor\bmod 2$. As $a$ increases through $[0,2^{j+2}-2]$, $\lfloor a/2^j\rfloor$ takes the values $0,1,2,3$ on the four blocks $[0,2^j),[2^j,2^{j+1}),[2^{j+1},3\cdot2^j),[3\cdot2^j,2^{j+2}-2]$, so $F=0,1,0,1$ there: **at most $3$ sign changes**, $C(F)\le 3$. (For $j=0$ the top block is absent and $C(F)=2$; for $j=n$, $A'=S$ ranges only over $[0,2^{n+1}-2]$, i.e. two blocks $[0,2^n),[2^n,2^{n+1}-2]$, so $F=0,1$ and $C(F)=1$.)

**Step 3 (apply L25, with junta invariance).** $\mathrm{ADD}_{n,j}=F(A')$ with $A'$ a positive weighted sum and $C(F)\le 3$; by L25 (and L21, since $\mathrm{ADD}_{n,j}$ ignores bits $>j$), $H^{*}(\mathrm{ADD}_{n,j})\le C(F)\le 3$. The refined values follow: $C(F)=1$ at $j=n$ (LTF, $H^{*}\le1$), $C(F)=2$ at $j=0$, $C(F)=3$ for interior $j$.

**Step 4 (lower bound for the non-carry bits).** For $0\le j\le n-1$, fix all variables except $x_j,y_j$ so that the incoming carry $c_j$ is a constant $\in\{0,1\}$ (e.g. set $x_i=y_i=0$ for $i<j$, giving $c_j=0$, and set the bits $>j$ arbitrarily — they don't affect bit $j$). Then $\mathrm{ADD}_{n,j}$ restricts to $x_j\oplus y_j\oplus c_j$, which on $(x_j,y_j)$ is a 2-bit checkerboard ($x_j\oplus y_j$ or its negation: equal on the diagonal, opposite on the antidiagonal). By L3, $H^{*}(\mathrm{ADD}_{n,j})\ge 2$. Hence interior bits have $H^{*}\in\{2,3\}$ and the LSB has $H^{*}=2$. $\blacksquare$

## Consequence (state briefly)

Integer addition, despite its carry chain (a sequential dependency of bit $j$ on all $j$ lower bits), has every output bit computable by a **constant** number of attention heads. The reason is that the carry into position $j$ is a *threshold of a positive weighted sum* $A'=I(x_{\le j})+I(y_{\le j})$, and the output bit is a function of that single sum with only $\le3$ sign changes — so it sits squarely on the "easy" (weighted-score / integer-comparison) side of the head-complexity dichotomy, not the multiplicative/membership side. (Contrast multiplication bits, which are not functions of any single weighted sum.)

## Pitfalls

- The score must be the **low-bit** sum $A'=I(x_{\le j})+I(y_{\le j})$, not the full $S=I(x)+I(y)$: using $S$ gives a function with $\approx2^{n+1-j}$ sign changes (the bit flips every $2^j$ over the full range), a vastly looser bound; locality (Step 1) is what makes $A'$ span only four half-periods.
- $C(F)$ is counted over $\mathrm{Im}(A')$, which is the full integer interval $[0,2^{j+2}-2]$ (redundant binary); state this so the four-block count is valid.
- A random-restart admissible-form search badly *over-reports* $H^{*}$ here (it returns $5,6,7$ for $n=4$); these are search failures, not the true value. The clean weighted-score construction gives the correct $\le3$. (The bounded sign-rank of the bit — its $x|y$ matrix is a diagonal-conjugated comparison matrix, sign-rank $\le3$ — is the structural tell that $H^{*}$ is bounded.)
