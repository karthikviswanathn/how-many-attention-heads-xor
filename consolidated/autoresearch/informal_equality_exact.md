# Problem: The head complexity of bitwise equality is exactly two

## Background and definitions (self-contained)

Bitwise equality on $2n$ bits is
$$
\mathrm{EQ}_n(x,y) = \mathbf 1[\,x = y\,] = \prod_{i=1}^n \mathbf 1[x_i = y_i] = \bigwedge_{i=1}^n \overline{(x_i\oplus y_i)} ,
$$
i.e. $1$ iff $x_i=y_i$ for every $i$ (an AND of $n$ disjoint XNORs). $H^{*}(f)$ is the least number of admissible one-head atoms in a cleared sign-representation of $f$.

**Established results (cite as given).**
- **(L25, weighted-score sign changes.)** If $f(u) = F(t(u))$ for a positive weighted sum $t(u)=\sum_k c_k u_k$ ($c_k>0$) and $F:\mathrm{Im}(t)\to\lbrace0,1\rbrace$, then $H^{*}(f)\le C(F)$, the number of sign changes of $F$ along the increasing order of $\mathrm{Im}(t)$. (In particular a single-value indicator $F(s)=\mathbf 1[s=W]$ with $W$ strictly interior to $\mathrm{Im}(t)$ has $C(F)=2$; this is the degenerate weighted band $\theta_1=\theta_2=W$ of L44.)
- **(L3, checkerboard obstruction.)** If $f$ has a 2-bit checkerboard restriction — two coordinates and a fixed assignment to the rest under which the restricted $f$ takes one value on $\lbrace(0,0),(1,1)\rbrace$ and the other value on $\lbrace(0,1),(1,0)\rbrace$ — then $H^{*}(f)\ge 2$.
- **(L15, negation/permutation closure.)** Flipping any input variable $u_k\mapsto 1-u_k$ (or permuting variables) leaves $H^{*}$ unchanged.

## Claim to prove

$$
H^{*}(\mathrm{EQ}_n) = 2 \qquad\text{for all } n\ge 1 .
$$

## Guidance (prove every step rigorously)

**Upper bound $H^{*}(\mathrm{EQ}_n)\le 2$.**

1. *Flip the $y$-inputs.* By L15, $H^{*}(\mathrm{EQ}_n)=H^{*}(g)$ where $g(x,z):=\mathrm{EQ}_n(x,\overline z)$ is $\mathrm{EQ}_n$ with each $y_i$ replaced by $z_i:=1-y_i$. Since $x_i=y_i \iff x_i = 1-z_i \iff x_i + z_i = 1$, we have $g(x,z)=\mathbf 1[\,x_i+z_i=1 \text{ for all } i\,]$.

2. *Distinct subset sums make equality a single value.* Put $w_i = 2^{\,i-1}>0$ and the positive weighted sum
$$
t(x,z)=\sum_{i=1}^n w_i x_i + \sum_{i=1}^n w_i z_i \qquad(\text{all weights } >0),
$$
and let $W=\sum_i w_i = 2^n-1$. Claim: $g(x,z)=\mathbf 1[\,t(x,z)=W\,]$.
   - *If $x_i+z_i=1$ for all $i$:* then $t=\sum_i w_i(x_i+z_i)=\sum_i w_i = W$.
   - *Conversely if $t=W$:* write $t=\sum_i w_i(x_i+z_i)$ with each $x_i+z_i\in\lbrace0,1,2\rbrace$. Subtracting, $\sum_i w_i\big((x_i+z_i)-1\big)=0$ with each coefficient $(x_i+z_i)-1\in\lbrace-1,0,1\rbrace$. Because the weights $w_i=2^{i-1}$ have **distinct subset sums** (every signed combination $\sum_i \epsilon_i 2^{i-1}$, $\epsilon_i\in\lbrace-1,0,1\rbrace$, vanishes only when all $\epsilon_i=0$ — indeed $|\sum_{i<n}\epsilon_i 2^{i-1}|\le 2^{n-1}-1 < 2^{n-1}$ forces $\epsilon_n=0$, then induct), we get $x_i+z_i=1$ for all $i$. Hence $g=\mathbf 1[t=W]$.

3. *Apply the weighted-score bound.* $W=2^n-1$ is strictly interior to $\mathrm{Im}(t)=\lbrace0,1,\dots,2(2^n-1)\rbrace$ (indeed $0<2^n-1<2^{n+1}-2$ for $n\ge1$), so the single-value indicator $F(s)=\mathbf 1[s=W]$ has exactly two sign changes, $C(F)=2$. By L25 (equivalently L44(a) for the degenerate band $\theta_1=\theta_2=W$), $H^{*}(g)\le 2$, hence $H^{*}(\mathrm{EQ}_n)\le 2$.

**Lower bound $H^{*}(\mathrm{EQ}_n)\ge 2$.**

4. Restrict to the first pair $(x_1,y_1)$ by fixing $x_k=y_k=0$ for all $k\ge 2$ (so those pairs agree). Then $\mathrm{EQ}_n$ restricts to $\mathbf 1[x_1=y_1]$, which equals $1$ on $\lbrace(0,0),(1,1)\rbrace$ and $0$ on $\lbrace(0,1),(1,0)\rbrace$ — a 2-bit checkerboard (the diagonal pattern). By L3, $H^{*}(\mathrm{EQ}_n)\ge 2$.

Combining, $H^{*}(\mathrm{EQ}_n)=2$. $\blacksquare$

## Consequence (state briefly)

Equality is **constant-head**: despite being an AND of $n$ checkerboards (each XNOR alone needs $2$ heads, L3), the whole conjunction still needs only $2$. The mechanism is that *string equality linearizes*: distinct-subset-sum weights turn $x=y$ into a single value of one positive weighted sum (compare two integers), so it is a degenerate weighted band. This is a sharp contrast with set intersection $\mathrm{INT}_n=\bigvee_i(x_i\wedge y_i)$ on the same $2n$ bits, which needs $H^{*}=\widetilde\Theta(n)$ (L35/L45): "all pairs equal" is a single linear comparison, while "some pair both-$1$" is irreducibly multiplicative ($A_{+}(\mathrm{INT}_n)=2^n-1$).

## Pitfalls

- The positive weighted sum is in the variables $(x,z)$ with $z=\overline y$; the $y$-flip (L15) is what makes all weights positive — state it. (In the original variables $(x,y)$ the score $\sum w_i x_i-\sum w_i y_i$ has mixed-sign weights, which L25 does not allow.)
- The converse in Step 2 needs the **distinct-subset-sum** property of $2^{i-1}$ over coefficients in $\lbrace-1,0,1\rbrace$ (not just $\lbrace0,1\rbrace$); give the $|\cdot|<2^{n-1}$ induction. Any super-increasing positive weight sequence works.
- $C(F)=2$ requires $W$ strictly interior to $\mathrm{Im}(t)$ (true here); otherwise a single-value band could be a half-line with fewer sign changes (still $\le2$, so the bound holds regardless, but state interiority for the exact count).
- The lower bound is the XNOR checkerboard, present already at $n=1$ ($\mathrm{EQ}_1=$ XNOR).
