# Problem: The head complexity of INT_3 is exactly 2

## Background and definitions (self-contained)

Work on $\lbrace 0,1\rbrace^6$ with variables $x_1,x_2,x_3,y_1,y_2,y_3$. The set-intersection function on $3$ pairs is
$$
\mathrm{INT}_3(x,y) = (x_1\wedge y_1)\vee(x_2\wedge y_2)\vee(x_3\wedge y_3),
$$
i.e. $\mathrm{INT}_3 = 1$ iff $x_i = y_i = 1$ for some $i \in \lbrace 1,2,3\rbrace$, and $0$ otherwise.

An **affine** function is $A(x,y) = a_0 + \sum_i a_i x_i + \sum_i a'_i y_i$. An affine $D$ is **admissible as a denominator** if $D(x,y) > 0$ for all $(x,y) \in \lbrace 0,1\rbrace^6$ and all of its slopes $a_1,a_2,a_3,a'_1,a'_2,a'_3$ share one common sign (all $\geq 0$ or all $\leq 0$). 

**Established facts (cite as given).**
- **(Order-2 admissible tangent form, L16.)** $H^{*}(f) \leq 2$ if there exist affine $N_1, D_1, N_2, D_2$ with $D_1, D_2$ admissible denominators, and $\theta \in \mathbb{R}$, such that
  $$ P(x,y) = \theta\, D_1 D_2 + N_1 D_2 + N_2 D_1 $$
  strictly sign-represents $f$: $f(x,y) = 1 \iff P(x,y) > 0$ and $f(x,y) = 0 \iff P(x,y) < 0$, for all $(x,y) \in \lbrace 0,1\rbrace^6$.
- **(Lower bound, L11.)** $H^{*}(f) \geq 2$ whenever $f$ is not a linear threshold function (not constant and not sign-representable by a single affine function).

## Claim to prove

$H^{*}(\mathrm{INT}_3) = 2$.

## Guidance (prove every step rigorously)

**Lower bound $H^{*}(\mathrm{INT}_3) \geq 2$.** Show $\mathrm{INT}_3$ is not a linear threshold function: exhibit four points forming an XOR-type obstruction. Consider $P_1 = (x{=}e_1, y{=}e_1)$, $P_2 = (e_1, e_2)$, $P_3 = (e_2, e_1)$, $P_4 = (e_2, e_2)$ (all other coordinates $0$), with $\mathrm{INT}_3$-values $1,0,0,1$. For any affine $A$, $A(P_1)+A(P_4) = A(P_2)+A(P_3)$, contradicting the sign requirements. Conclude $H^{*}(\mathrm{INT}_3) \geq 2$ by L11.

**Upper bound $H^{*}(\mathrm{INT}_3) \leq 2$.** Exhibit an explicit admissible order-2 tangent form that sign-represents $\mathrm{INT}_3$:
1. Give explicit affine $D_1, D_2$ (with rational coefficients), and verify each is admissible: $D_h > 0$ at all $8$ relevant denominator values (or argue positivity from the constant term dominating the sum of negative slopes), and its slopes are one-signed.
2. Give explicit affine $N_1, N_2$ and a rational $\theta$.
3. Form $P = \theta D_1 D_2 + N_1 D_2 + N_2 D_1$ and verify $\mathrm{sgn}\,P(x,y) = \mathrm{INT}_3(x,y)$ for **all** $64$ points $(x,y) \in \lbrace 0,1\rbrace^6$. Since $P$ depends on $(x,y)$ only through which pairs $(x_i,y_i)$ equal $(1,1)$ and the individual bit pattern, organize the verification by the relevant cases (e.g. by the multiset of pair-states $(x_i,y_i) \in \lbrace 00,01,10,11\rbrace$), and check each case has the correct sign. Be exhaustive: every one of the $64$ points must be covered by some case with the verified sign.

Conclude $H^{*}(\mathrm{INT}_3) = 2$ from the two bounds.

## Pitfalls to address explicitly

- Admissibility is a real constraint: both $D_1, D_2$ must be strictly positive on the whole cube AND have one-signed slopes. State the constant and slopes and verify both.
- The sign-representation must be strict ($P \neq 0$ on the cube) and correct at every one of the $64$ points — do not check only representative points without arguing the cases are exhaustive.
- A clean construction is preferred (small integer/rational coefficients); if a symmetric construction exists (symmetric under permuting the three pairs and under swapping $x \leftrightarrow y$), present it, as it is easiest to verify and most likely to generalize.
