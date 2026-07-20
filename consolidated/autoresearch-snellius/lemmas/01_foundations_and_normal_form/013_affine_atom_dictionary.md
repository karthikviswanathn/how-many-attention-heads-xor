# Affine Atom Dictionary for One Head

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md). By [010_linear_fractional_normal_form.md](010_linear_fractional_normal_form.md), a one-head atom is a function

$$
\phi(x)=\frac{\eta+\sum_{i=1}^{n}\rho_i\alpha^{x_i}(m_i+\delta x_i)}{\gamma+\sum_{i=1}^{n}\rho_i\alpha^{x_i}},
$$

where $x\in\{0,1\}^n$, $\gamma>0$, $\rho_i>0$, $\alpha>0$, and $\eta,m_i,\delta\in\mathbb{R}$.

Then every such atom can be written on the Boolean cube as

$$
\phi(x)=\frac{N(x)}{D(x)},\qquad N(x)=a_0+\sum_{i=1}^{n}a_i x_i,\qquad D(x)=d_0+\sum_{i=1}^{n}d_i x_i,
$$

with $D(x)>0$ for every $x\in\{0,1\}^n$.

For $n\geq1$, the possible affine denominators are exactly the following three classes:

1. $D$ is constant positive, namely $d_i=0$ for all $i$ and $d_0>0$.

2. All coordinate coefficients are strictly positive, namely $d_i>0$ for all $i$ and $d_0>0$.

3. All coordinate coefficients are strictly negative and the all-ones value is positive, namely $d_i<0$ for all $i$ and $d_0+\sum_i d_i>0$.

For $n=0$, only the constant positive class occurs. Conversely, every affine denominator in one of these classes arises from some choice of $\gamma>0$, $\rho_i>0$, and $\alpha>0$.

Finally, if $D$ is nonconstant, then any affine numerator $N$ can be realized with that same $D$. If $D$ is constant, then in a direct atom representation the numerator coefficients $a_i$ are either all strictly positive, all strictly negative, or all zero, while the constant coefficient $a_0$ is arbitrary.

## Proof

All identities below are identities of functions on the Boolean cube.

If $n=0$, all sums are empty. The denominator is $D(x)=\gamma>0$ and the numerator is $N(x)=\eta$, so the affine representation and the constant-denominator case are immediate. Thus assume $n\geq1$ for the rest of the proof.

### Lemma 1. Boolean linearization

For every coordinate $i$ and every $x\in\{0,1\}^n$,

$$
x_i^2=x_i,
\qquad
\alpha^{x_i}=1+(\alpha-1)x_i.
$$

**Proof.** If $x_i=0$, then $x_i^2=x_i$ and both sides of the second identity are $1$. If $x_i=1$, then $x_i^2=x_i$ and both sides of the second identity are $\alpha$. $\blacksquare$

### Lemma 2. Forward affine form

Define

$$
D(x):=\gamma+\sum_{i=1}^{n}\rho_i\alpha^{x_i}.
$$

By Lemma 1,

$$
\begin{aligned}
D(x)
&=\gamma+\sum_{i=1}^{n}\rho_i\left(1+(\alpha-1)x_i\right) \\
&=\gamma+\sum_{i=1}^{n}\rho_i+\sum_{i=1}^{n}\rho_i(\alpha-1)x_i.
\end{aligned}
$$

Thus, with

$$
d_0:=\gamma+\sum_{i=1}^{n}\rho_i,
\qquad
d_i:=\rho_i(\alpha-1),
$$

we have

$$
D(x)=d_0+\sum_{i=1}^{n}d_i x_i.
$$

For the numerator, define

$$
N(x):=\eta+\sum_{i=1}^{n}\rho_i\alpha^{x_i}(m_i+\delta x_i).
$$

For each $i$, Lemma 1 gives

$$
\begin{aligned}
\alpha^{x_i}(m_i+\delta x_i)
&=\left(1+(\alpha-1)x_i\right)(m_i+\delta x_i) \\
&=m_i+\delta x_i+(\alpha-1)m_i x_i+(\alpha-1)\delta x_i^2 \\
&=m_i+\delta x_i+(\alpha-1)m_i x_i+(\alpha-1)\delta x_i \\
&=m_i+\left(\delta+(\alpha-1)m_i+(\alpha-1)\delta\right)x_i \\
&=m_i+\left(\alpha(m_i+\delta)-m_i\right)x_i.
\end{aligned}
$$

Therefore

$$
N(x)=\eta+\sum_{i=1}^{n}\rho_i m_i+\sum_{i=1}^{n}\rho_i\left(\alpha(m_i+\delta)-m_i\right)x_i.
$$

With

$$
a_0:=\eta+\sum_{i=1}^{n}\rho_i m_i,
\qquad
a_i:=\rho_i\left(\alpha(m_i+\delta)-m_i\right),
$$

we have

$$
N(x)=a_0+\sum_{i=1}^{n}a_i x_i.
$$

Finally, since $\gamma>0$, $\rho_i>0$, $\alpha>0$, and $x_i\in\{0,1\}$, every term $\rho_i\alpha^{x_i}$ is positive. Hence

$$
D(x)=\gamma+\sum_{i=1}^{n}\rho_i\alpha^{x_i}>0
$$

on the whole cube. $\blacksquare$

### Lemma 3. Denominator trichotomy

The denominator from Lemma 2 lies in exactly one of the three stated classes.

**Proof.** Since $\alpha>0$, exactly one of $\alpha=1$, $\alpha>1$, or $0<\alpha<1$ holds.

If $\alpha=1$, then

$$
d_i=\rho_i(1-1)=0
$$

for every $i$, and

$$
d_0=\gamma+\sum_i\rho_i>0.
$$

This is the constant positive class.

If $\alpha>1$, then $\alpha-1>0$. Since each $\rho_i>0$,

$$
d_i=\rho_i(\alpha-1)>0
$$

for every $i$. Also $d_0>0$. This is the all-positive-coefficient class.

If $0<\alpha<1$, then $\alpha-1<0$. Since each $\rho_i>0$,

$$
d_i=\rho_i(\alpha-1)<0
$$

for every $i$. Moreover,

$$
\begin{aligned}
d_0+\sum_i d_i
&=\gamma+\sum_i\rho_i+\sum_i\rho_i(\alpha-1) \\
&=\gamma+\alpha\sum_i\rho_i \\
&>0.
\end{aligned}
$$

This is the all-negative-coefficient class with positive all-ones value. The three cases are mutually exclusive for $n\geq1$, so the trichotomy follows. $\blacksquare$

### Lemma 4. Converse denominator realization

Every denominator in one of the stated classes is realized by suitable parameters $\gamma>0$, $\rho_i>0$, and $\alpha>0$.

**Proof.** First suppose $D$ is constant positive. For $n=0$, choose $\gamma=d_0$ and any $\alpha>0$. For $n\geq1$, choose

$$
\alpha:=1,
\qquad
\rho_i:=\frac{d_0}{2n},
\qquad
\gamma:=\frac{d_0}{2}.
$$

Then $\rho_i>0$, $\gamma>0$, and

$$
\gamma+\sum_i\rho_i=d_0,
\qquad
\rho_i(\alpha-1)=0.
$$

Thus the denominator is $D(x)=d_0$.

Next suppose $d_i>0$ for every $i$ and $d_0>0$. Let

$$
S:=\sum_i d_i>0.
$$

Choose

$$
\alpha:=1+\frac{2S}{d_0},
\qquad
\rho_i:=\frac{d_i}{\alpha-1},
\qquad
\gamma:=d_0-\sum_i\rho_i.
$$

Then $\alpha>1$ and $\rho_i>0$. Also

$$
\sum_i\rho_i=\frac{S}{\alpha-1}=\frac{d_0}{2},
\qquad
\gamma=\frac{d_0}{2}>0.
$$

Therefore the coefficients obtained from Lemma 2 are exactly the prescribed $d_0,d_1,\ldots,d_n$.

Finally suppose $d_i<0$ for every $i$ and

$$
d_0+\sum_i d_i>0.
$$

Let

$$
S:=-\sum_i d_i>0,
\qquad
q:=d_0+\sum_i d_i=d_0-S>0.
$$

Then $d_0=S+q>0$. Choose

$$
\alpha:=\frac{q}{2d_0},
\qquad
\rho_i:=\frac{d_i}{\alpha-1},
\qquad
\gamma:=d_0-\sum_i\rho_i.
$$

Since $0<q<d_0$, we have $0<\alpha<1$. Thus $\alpha-1<0$, and since each $d_i<0$, each $\rho_i>0$.

Moreover,

$$
1-\alpha=\frac{d_0+S}{2d_0},
\qquad
\sum_i\rho_i=\frac{S}{1-\alpha}=\frac{2d_0S}{d_0+S}.
$$

Therefore

$$
\begin{aligned}
\gamma
&=d_0-\frac{2d_0S}{d_0+S} \\
&=\frac{d_0(d_0-S)}{d_0+S} \\
&=\frac{d_0q}{d_0+S} \\
&>0.
\end{aligned}
$$

Again the coefficients obtained from Lemma 2 are exactly the prescribed coefficients.

In class 2, positivity on the cube is also immediate because $D$ is minimized at $x=0$. In class 3, $D$ is minimized at $x=(1,\ldots,1)$ because every coordinate coefficient is negative, and that value is positive by assumption. Thus the three classes are precisely the realizable positive affine denominators. $\blacksquare$

### Lemma 5. Numerator freedom

If $D$ is nonconstant, then every affine numerator can be realized with the same denominator parameters. If $D$ is constant in a direct atom representation, then the coordinate numerator coefficients are sign-uniform or all zero, and the constant coefficient is arbitrary.

**Proof.** Suppose first that $D$ is nonconstant. By Lemma 3, $\alpha\neq1$, and for every $i$,

$$
d_i=\rho_i(\alpha-1)\neq0.
$$

Fix any affine numerator

$$
N(x)=a_0+\sum_i a_i x_i.
$$

Keep the denominator parameters $\gamma$, $\rho_i$, and $\alpha$ fixed, and set

$$
\delta:=0,
\qquad
m_i:=\frac{a_i}{d_i},
\qquad
\eta:=a_0-\sum_i\rho_i m_i.
$$

Then the numerator coefficients from Lemma 2 satisfy

$$
\rho_i\left(\alpha(m_i+\delta)-m_i\right)
=\rho_i(\alpha-1)m_i
=d_i\frac{a_i}{d_i}
=a_i,
$$

and

$$
\eta+\sum_i\rho_i m_i=a_0.
$$

Thus the prescribed numerator is realized with the same nonconstant denominator.

Now suppose $D$ is constant in a direct atom representation. Then $d_i=0$ for all $i$. Since

$$
d_i=\rho_i(\alpha-1)
$$

and $\rho_i>0$, we must have $\alpha=1$. With $\alpha=1$, Lemma 2 gives

$$
a_i=\rho_i\left(m_i+\delta-m_i\right)=\rho_i\delta.
$$

Hence if $\delta>0$, then all $a_i>0$; if $\delta<0$, then all $a_i<0$; and if $\delta=0$, then all $a_i=0$.

The constant coefficient is arbitrary because

$$
a_0=\eta+\sum_i\rho_i m_i,
$$

and for any prescribed value of $a_0$ one may choose

$$
\eta:=a_0-\sum_i\rho_i m_i.
$$

This proves the numerator freedom and the constant-denominator restriction. $\blacksquare$

### Conclusion

Lemma 2 gives the affine numerator and denominator representation with positive denominator. Lemmas 3 and 4 give the exact denominator dictionary. Lemma 5 gives the numerator freedom needed in the nonconstant cases and the sign-uniform restriction in the constant case. This proves the theorem. $\blacksquare$

## Consequence

Every one-head atom from Lemma 10 belongs to an explicit affine dictionary. Its denominator is an admissible positive affine form, and in the nonconstant denominator cases its numerator is an arbitrary affine form.

Thus an $H$-atom score can be cleared without changing signs on the Boolean cube:

$$
\prod_{h=1}^{H}D_h(x)\left(c+\sum_{h=1}^{H}\frac{N_h(x)}{D_h(x)}\right)
=
c\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x),
$$

because every $D_h(x)$ is strictly positive. This is the dictionary input for the cleared-denominator invariant frontier node.
