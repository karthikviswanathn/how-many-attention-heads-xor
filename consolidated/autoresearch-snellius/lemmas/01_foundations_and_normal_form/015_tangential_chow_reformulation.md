# Tangential-Chow Reformulation of the Cleared-Denominator Invariant

## Statement

Let $f : \{0,1\}^{n} \to \{0,1\}$, and let $H \geq 1$. Let $(N_h,D_h)$, $1\leq h\leq H$, be admissible affine pairs in the sense of Lemma 13, with

$$
D_h(x)>0
\qquad
\text{for all }x\in\{0,1\}^{n}.
$$

Suppose

$$
P(x)=\theta\prod_{h=1}^{H}D_h(x)+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x)
$$

is a cleared-denominator polynomial of the form in Lemma 14, and that it strictly sign-represents $f$ on the Boolean cube, meaning

$$
f(x)=1
\quad\Longleftrightarrow\quad
P(x)>0
$$

for every $x\in\{0,1\}^{n}$.

Write the affine forms as

$$
D_h(x)=d_{h0}+\sum_{i=1}^{n}d_{hi}x_i,
\qquad
N_h(x)=a_{h0}+\sum_{i=1}^{n}a_{hi}x_i,
$$

and homogenize them by

$$
\widetilde D_h(x_0,x)=d_{h0}x_0+\sum_{i=1}^{n}d_{hi}x_i,
\qquad
\widetilde N_h(x_0,x)=a_{h0}x_0+\sum_{i=1}^{n}a_{hi}x_i.
$$

Equivalently, on the affine chart $x_0\neq0$, these are $x_0D_h(x/x_0)$ and $x_0N_h(x/x_0)$. Define

$$
\widetilde P(x_0,x)=\theta\prod_{h=1}^{H}\widetilde D_h(x_0,x)+\sum_{h=1}^{H}\widetilde N_h(x_0,x)\prod_{g\neq h}\widetilde D_g(x_0,x).
$$

Then $\widetilde P$ is a homogeneous degree-$H$ form lying in the parameter affine tangent space at $\prod_h\widetilde D_h$ to the degree-$H$ Chow cone of products of $H$ linear forms.

Conversely, every homogeneous form with such an admissibility-restricted parameter tangent presentation dehomogenizes at $x_0=1$ to a cleared-denominator polynomial of Lemma 14.

Consequently, with the $H=0$ empty-product convention for constant functions, $H^{\ast}(f)$ is exactly the least $H$ for which $f$ has a strict Boolean-cube sign-representer obtained by dehomogenizing an admissibility-restricted parameter tangent vector to the degree-$H$ Chow cone.

## Proof

Let $V_1$ be the real vector space of linear forms in the variables $(x_0,x_1,\ldots,x_n)$, and let $S_H$ be the real vector space of homogeneous degree-$H$ forms in those variables. Define

$$
\mu:V_1^{H}\to S_H,
\qquad
\mu(\ell_1,\ldots,\ell_H)=\prod_{h=1}^{H}\ell_h.
$$

The affine Chow cone of degree-$H$ split forms is the image of $\mu$. For a fixed presentation

$$
F=\prod_{h=1}^{H}\ell_h,
$$

we use the parameter affine tangent space attached to that presentation:

$$
T^{\mathrm{par}}_{F,\ell}\operatorname{Ch}_H:=\operatorname{im}d\mu_{\ell}.
$$

By the Leibniz rule, this image is

$$
T^{\mathrm{par}}_{F,\ell}\operatorname{Ch}_H
=
\left\{
\sum_{h=1}^{H}\delta_h\prod_{g\neq h}\ell_g:
\delta_h\in V_1
\right\}.
$$

Indeed, after replacing $\ell_h$ by $\ell_h+t\delta_h$ and keeping only the coefficient of $t$, one obtains exactly the displayed sum. This parameter tangent space is always contained in the intrinsic affine tangent space to the image at $F$, and it agrees with the intrinsic tangent space at smooth reduced points. If factors repeat, the intrinsic tangent space can be larger. In this lemma, an admissibility-restricted tangent vector means a vector given with the parameter tangent presentation above, together with the admissibility data described below.

Set

$$
\ell_h:=\widetilde D_h,
\qquad
\nu_h:=\widetilde N_h,
\qquad
F:=\prod_{h=1}^{H}\ell_h.
$$

The termwise definition of $\widetilde P$ gives

$$
\widetilde P=\theta F+\sum_{h=1}^{H}\nu_h\prod_{g\neq h}\ell_g.
$$

Each $\ell_h$ and $\nu_h$ is linear, so each summand has degree $H$. Hence $\widetilde P\in S_H$.

Define

$$
\delta_h:=\nu_h+\frac{\theta}{H}\ell_h.
$$

Since $H\geq1$, this is well-defined and belongs to $V_1$. Applying the differential formula gives

$$
\begin{aligned}
d\mu_{\ell}(\delta_1,\ldots,\delta_H)
&=\sum_{h=1}^{H}\left(\nu_h+\frac{\theta}{H}\ell_h\right)\prod_{g\neq h}\ell_g \\
&=\sum_{h=1}^{H}\nu_h\prod_{g\neq h}\ell_g
+\frac{\theta}{H}\sum_{h=1}^{H}\ell_h\prod_{g\neq h}\ell_g \\
&=\sum_{h=1}^{H}\nu_h\prod_{g\neq h}\ell_g
+\frac{\theta}{H}\sum_{h=1}^{H}F \\
&=\sum_{h=1}^{H}\nu_h\prod_{g\neq h}\ell_g+\theta F \\
&=\widetilde P.
\end{aligned}
$$

Therefore

$$
\widetilde P\in T^{\mathrm{par}}_{F,\ell}\operatorname{Ch}_H.
$$

This proves the forward tangential-Chow inclusion.

For the converse, suppose $R\in S_H$ is given with an admissibility-restricted parameter tangent presentation

$$
R=\theta\prod_{h=1}^{H}\ell_h+\sum_{h=1}^{H}\nu_h\prod_{g\neq h}\ell_g,
$$

where

$$
\ell_h=\widetilde D_h,
\qquad
\nu_h=\widetilde N_h,
$$

for affine forms $D_h,N_h$ such that each pair $(N_h,D_h)$ is admissible in the sense of Lemma 13 and each $D_h$ is positive on the Boolean cube. The presentation is part of the data, since parameter tangent presentations need not be unique.

Evaluating on the affine chart $x_0=1$ gives

$$
\begin{aligned}
R(1,x)
&=\theta\prod_{h=1}^{H}\ell_h(1,x)
+\sum_{h=1}^{H}\nu_h(1,x)\prod_{g\neq h}\ell_g(1,x) \\
&=\theta\prod_{h=1}^{H}D_h(x)
+\sum_{h=1}^{H}N_h(x)\prod_{g\neq h}D_g(x).
\end{aligned}
$$

This is exactly the cleared-denominator polynomial form from Lemma 14. The positivity hypotheses required there hold because admissibility gives

$$
D_h(x)>0
\qquad
\text{for all }x\in\{0,1\}^{n}.
$$

Also, strict signs are preserved on the Boolean cube because the cube is contained in the affine chart $x_0=1$ and, for every $x\in\{0,1\}^{n}$,

$$
\widetilde P(1,x)=P(x).
$$

It remains only to identify the least possible $H$. Let $\tau_{\operatorname{Ch}}^{\operatorname{adm}}(f)$ be the least integer $H\geq0$ for which $f$ has a strict Boolean-cube sign-representer obtained from the admissibility-restricted tangential-Chow construction above. For $H=0$, this means the empty-product constant witness of Lemma 14.

The forward construction sends every Lemma 14 cleared-denominator witness with $H\geq1$ to an admissibility-restricted parameter tangent vector whose dehomogenization has the same signs on the cube. The case $H=0$ is the same empty constant witness on both sides. Hence

$$
\tau_{\operatorname{Ch}}^{\operatorname{adm}}(f)\leq \mathrm{MFdeg}_{\pm}(f).
$$

The converse construction sends every admissibility-restricted tangential-Chow witness back to a Lemma 14 cleared-denominator witness with the same strict signs. Hence

$$
\mathrm{MFdeg}_{\pm}(f)\leq \tau_{\operatorname{Ch}}^{\operatorname{adm}}(f).
$$

Therefore

$$
\tau_{\operatorname{Ch}}^{\operatorname{adm}}(f)=\mathrm{MFdeg}_{\pm}(f).
$$

By Lemma 14,

$$
H^{\ast}(f)=\mathrm{MFdeg}_{\pm}(f).
$$

Combining the last two displays gives

$$
H^{\ast}(f)=\tau_{\operatorname{Ch}}^{\operatorname{adm}}(f).
$$

This is precisely the claimed tangential-Chow reformulation. $\blacksquare$

## Consequence

The cleared-denominator invariant of Lemma 14 can be read geometrically: its degree-$H$ witnesses are exactly the dehomogenizations of admissibility-restricted parameter tangent vectors to the degree-$H$ Chow cone of split forms.

Thus $H^{\ast}(f)$ is the least number of Chow factors needed for such a restricted tangent-vector sign-representer on the Boolean cube, with the same admissibility and positivity restrictions inherited from one attention head.
