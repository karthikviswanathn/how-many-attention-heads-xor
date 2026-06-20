# Three-Bit Projection Cases

## Statement

This note applies the one-head linear-threshold characterization and the positive-projection sign-change bound to two of the provisional three-head functions from [../three_head_functions_n3.md](../three_head_functions_n3.md).

For the function with bitstring

$$
00011000,
$$

where the input order is $000,001,010,011,100,101,110,111$, the exact value is

$$
H^{*}(00011000) = 2.
$$

For the function with bitstring

$$
00101001,
$$

we have the bounds

$$
2 \leq H^{*}(00101001) \leq 3.
$$

The second bound is sharpened to an exact value in [09_three_bit_quadratic_upper_bound.md](09_three_bit_quadratic_upper_bound.md).

## Proof

### Lemma 1. A lattice-square obstruction to one head

Let $a,b \in \{0,1\}^n$. Define

$$
m := a \wedge b,
\qquad
j := a \vee b,
$$

where meet and join are coordinatewise.

For every affine function

$$
L(x) = \beta_0 + \sum_{i=1}^{n} \beta_i x_i,
$$

we have

$$
L(a) + L(b) = L(m) + L(j).
$$

**Proof.** For each coordinate $i$,

$$
a_i + b_i = m_i + j_i.
$$

Therefore

$$
\begin{aligned}
L(a) + L(b)
&=
2\beta_0 + \sum_{i=1}^{n} \beta_i(a_i+b_i) \\
&=
2\beta_0 + \sum_{i=1}^{n} \beta_i(m_i+j_i) \\
&=
L(m) + L(j).
\end{aligned}
$$

$\blacksquare$

Consequently, if a Boolean function gives one label to $a,b$ and the opposite label to $m,j$, then it is not a linear threshold function. By the one-head characterization in [05_linear_fractional_normal_form.md](05_linear_fractional_normal_form.md), every nonconstant such function has

$$
H^{*}(f) \geq 2.
$$

### Lemma 2. The function $00011000$ has exact head complexity $2$

Let $f$ be the function with positive inputs

$$
\{011,100\}.
$$

For the lower bound, take

$$
a = 011,
\qquad
b = 100.
$$

Then

$$
a \wedge b = 000,
\qquad
a \vee b = 111.
$$

The function has

$$
f(a)=f(b)=1,
\qquad
f(a\wedge b)=f(a\vee b)=0.
$$

By Lemma 1, $f$ is not a linear threshold function. Since one head is exactly linear threshold power and $f$ is nonconstant,

$$
H^{*}(f) \geq 2.
$$

For the upper bound, use the positive projection

$$
t(x) := 2x_1+x_2+x_3.
$$

Its image is

$$
\{0,1,2,3,4\}.
$$

On these levels, $f$ has labels

$$
0,0,1,0,0.
$$

There are exactly two sign changes. By the positive-projection sign-change upper bound from [07_positive_projection_sign_changes.md](07_positive_projection_sign_changes.md),

$$
H^{*}(f) \leq 2.
$$

Combining the two inequalities gives

$$
H^{*}(00011000)=2.
$$

$\blacksquare$

### Lemma 3. The function $00101001$ has bounds $2 \leq H^{*} \leq 3$

Let $g$ be the function with positive inputs

$$
\{010,100,111\}.
$$

For the lower bound, take

$$
a = 010,
\qquad
b = 100.
$$

Then

$$
a \wedge b = 000,
\qquad
a \vee b = 110.
$$

The function has

$$
g(a)=g(b)=1,
\qquad
g(a\wedge b)=g(a\vee b)=0.
$$

So $g$ is not a linear threshold function, and therefore

$$
H^{*}(g) \geq 2.
$$

For the upper bound, use the positive projection

$$
t(x) := x_1+x_2+2x_3.
$$

Its image is

$$
\{0,1,2,3,4\}.
$$

The labels along these levels are

$$
0,1,0,0,1.
$$

There are three sign changes. Hence Lemma 13 of [../lemmas.md](../lemmas.md) gives

$$
H^{*}(g) \leq 3.
$$

Thus

$$
2 \leq H^{*}(00101001) \leq 3.
$$

$\blacksquare$

## Consequence For The Empirical List

The provisional three-head list now separates as follows:

1. `00010110` is $\mathrm{EXACT}_{3,2}$, so $H^{*}=2$ by the symmetric sign-change theorem.
2. `00011000` has $H^{*}=2$ by Lemma 2 above.
3. `00101001` has $H^{*}=2$ by [09_three_bit_quadratic_upper_bound.md](09_three_bit_quadratic_upper_bound.md).
4. `01101001` is $\mathrm{XOR}_3$, so $H^{*}=3$.
