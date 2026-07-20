# The Head Complexity of INT_3 is Exactly Two

## Statement

For $\mathrm{INT}_3(x,y) = (x_1\wedge y_1)\vee(x_2\wedge y_2)\vee(x_3\wedge y_3)$ on $\lbrace 0,1\rbrace^6$,

$$
H^{*}(\mathrm{INT}_3) = 2.
$$

> The first rigorous proof that a set-intersection function beats its DNF bound: $\mathrm{INT}_3$ has $3$ terms, so the monotone-term DNF construction (L14) gives only $H^{*}\leq 3$, but two heads suffice. This is the $n=3$ case of the conjectured $H^{*}(\mathrm{INT}_n)=n-1$ ($n\geq 3$); together with $H^{*}(\mathrm{INT}_2)=2$ (L27) it pins the small values exactly. Note the saving requires **two distinct denominators** (L38): no single-denominator form can compute the non-LTF $\mathrm{INT}_3$.

## Proof

**Lower bound $H^{*}(\mathrm{INT}_3)\geq 2$.** $\mathrm{INT}_3$ is not a linear threshold function: with all coordinates outside $\lbrace 1,2\rbrace$ set to $0$, the four points $Q_1=(e_1,e_1)$, $Q_2=(e_1,e_2)$, $Q_3=(e_2,e_1)$, $Q_4=(e_2,e_2)$ have $\mathrm{INT}_3$-values $1,0,0,1$, yet any affine $A$ satisfies $A(Q_1)+A(Q_4)=A(Q_2)+A(Q_3)$, contradicting $A(Q_1),A(Q_4)>0$ and $A(Q_2),A(Q_3)<0$. By [011_one_head_characterization.md](../01_foundations_and_normal_form/011_one_head_characterization.md), $H^{*}(\mathrm{INT}_3)\geq 2$.

**Upper bound $H^{*}(\mathrm{INT}_3)\leq 2$.** Take the admissible denominators
$$
D_1 = 2 - y_3, \qquad D_2 = 6 - x_3 - 2y_2 - 2y_3,
$$
both with one-signed (nonpositive) slopes and positive on the cube ($D_1\in\lbrace 1,2\rbrace$; $D_2\geq 6-(1+2+2)=1$), and
$$
\begin{aligned}
N_1 &= 29700+1600x_1-3200x_2+9600x_3+1600y_1-19200y_2-14850y_3,\\
N_2 &= 29700-1600x_1+9600x_2-28350x_3-1600y_1+29700y_2-11500y_3,\\
\theta &= -20800 .
\end{aligned}
$$
Form the order-2 tangent form $P = \theta D_1 D_2 + N_1 D_2 + N_2 D_1$. Expanding and reducing with $x_i^2=x_i$, $y_i^2=y_i$,
$$
\tfrac{1}{800}P = R = -15 + 8x_1+4x_3+8y_1+8y_2+8y_3 - 2x_1x_3 - 4x_1y_2 - 2x_1y_3 + 4x_2x_3 + 8x_2y_2 - 4x_2y_3 - 2x_3y_1 + 4x_3y_3 - 4y_1y_2 - 2y_1y_3 - 4y_2y_3 .
$$
Set $s_i = 2x_i + y_i \in \lbrace 0,1,2,3\rbrace$, so $s_i = 3 \iff (x_i,y_i)=(1,1)$, and $\mathrm{INT}_3 = 1 \iff$ some $s_i = 3$. Evaluating $R$ on all $4^3 = 64$ triples $(s_1,s_2,s_3)$ gives $R > 0$ exactly when at least one $s_i = 3$ and $R < 0$ otherwise (the four $s_3$-slices of the value table each have all negative entries off the "$s_i=3$" rows/columns and all positive entries on them). Since $800 > 0$, $P$ has the sign of $R$ at every point, so $P$ strictly sign-represents $\mathrm{INT}_3$. By the order-2 tangent normal form (L16), $H^{*}(\mathrm{INT}_3)\leq 2$.

Combining the bounds, $H^{*}(\mathrm{INT}_3) = 2$. $\blacksquare$

## Consequence

This is a concrete witness that the monotone-term DNF upper bound $H^{*}\leq s$ (L14) is **not tight** for $\mathrm{INT}_n$: three disjoint $2$-ANDs are computed by two heads. The two denominators are genuinely distinct (as L38 requires for any non-LTF), but here both happen to be decreasing (nonpositive slopes), refuting the naive guess that the saving needs opposite monotone biases. The construction is specific and does not transparently generalize; whether the saving extends to $H^{*}(\mathrm{INT}_n)=n-1$ for all $n\geq 3$ (numerically observed through $n=5$) is open and would, if proved, show the DNF bound is loose by exactly one head on this family.
