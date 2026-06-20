# One-Bit LTF Branching

## Statement

Let

$$
L(y)=\beta+\sum_{i\in S}\alpha_i y_i
$$

be a strict affine sign representation of a Boolean function

$$
T:\{0,1\}^{m}\to\{0,1\},
\qquad
T(y)=1
\Longleftrightarrow
L(y)>0,
$$

and assume $L(y)\neq0$ on the cube. Thus $T(y)=0$ if and only if $L(y)<0$. Assume $\alpha_i\neq0$ for $i\in S$. Let

$$
G:\{0,1\}^2\to\{0,1\}
$$

be arbitrary, and define

$$
f(z,y):=G(z,T(y)).
$$

Then

$$
H^{*}(f)\leq1+\lvert S\rvert.
$$

In particular, if $\lvert S\rvert\leq1$, then

$$
H^{*}(f)
=
\begin{cases}
0 & \text{if } f \text{ is constant},\\
1 & \text{if } f \text{ is a nonconstant linear threshold function},\\
2 & \text{otherwise}.
\end{cases}
$$

> **Interpretation.** Branching on one raw bit between two labels determined by the same LTF costs at most one head plus the number of variables used by that LTF. This includes $z\wedge T(y)$, $z\vee T(y)$, $z\oplus T(y)$, and their complements.

## Proof

Split on the coordinate $z$. The two cofactors are

$$
f_0(y)=G(0,T(y)),
\qquad
f_1(y)=G(1,T(y)).
$$

For each $b\in\{0,1\}$, the map $u\mapsto G(b,u)$ is a one-bit Boolean function. Hence $f_b$ is one of the four functions

$$
0,
\qquad
1,
\qquad
T,
\qquad
1-T.
$$

Choose affine sign representations as follows:

$$
-1
\quad\text{for the constant }0,
\qquad
1
\quad\text{for the constant }1,
\qquad
L
\quad\text{for }T,
\qquad
-L
\quad\text{for }1-T.
$$

The strictness of $L$ on the finite cube ensures that $-L$ strictly sign-represents $1-T$.

The slope vectors of any two choices in this list differ only on coordinates in $S$. Therefore their slope distance is at most

$$
\lvert S\rvert.
$$

The LTF cofactor slope-distance theorem [70_ltf_cofactor_slope_distance.md](70_ltf_cofactor_slope_distance.md) gives

$$
H^{*}(f)\leq1+\lvert S\rvert.
$$

If $\lvert S\rvert\leq1$, then the same theorem gives $H^{*}(f)\leq2$. The exact value is forced by the zero-head and one-head characterization [05_linear_fractional_normal_form.md](../01_foundations_and_normal_form/05_linear_fractional_normal_form.md): constants have value $0$, nonconstant LTFs have value $1$, and every remaining function has value exactly $2$. $\blacksquare$

## Consequences

The XOR-with-an-LTF family satisfies

$$
H^{*}(z\oplus T(y))\leq1+\lvert\operatorname{supp}(L)\rvert.
$$

When $T$ is a single input bit, this recovers the exact two-head XOR$_2$ case. More generally, the theorem gives a simple bound for every two-variable outer Boolean gate applied to one raw coordinate and one LTF feature.
