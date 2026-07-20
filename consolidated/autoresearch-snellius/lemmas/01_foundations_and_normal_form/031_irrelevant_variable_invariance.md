# Irrelevant Variables Do Not Change Head Complexity

## Statement

Work in the one-layer attention model of [../../model.md](../../model.md), with a final strict threshold at the query token. Let $H^{\ast}(f)$ denote the least number of heads needed to compute $f$.

Equivalently, by Lemma 10, $H^{\ast}(f)$ is the least $H$ such that $f : \{0,1\}^{n}\to\{0,1\}$ is sign-represented on the Boolean cube by a score

$$
\theta+\sum_{h=1}^{H}\phi_h(x),
$$

where $H=0$ means the empty sum, and each one-head atom has the form

$$
\phi_h(x)=
\frac{
\eta_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}(m_{hi}+\delta_h x_i)
}{
\gamma_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}
},
$$

with

$$
\gamma_h>0,
\qquad
\rho_{hi}>0,
\qquad
\alpha_h>0.
$$

For any Boolean function $f:\{0,1\}^{n}\to\{0,1\}$ and any $m\geq 0$, define the dummy-variable extension

$$
\widetilde f:\{0,1\}^{n+m}\to\{0,1\},
\qquad
\widetilde f(x,z)=f(x).
$$

Then

$$
H^{\ast}(\widetilde f)=H^{\ast}(f).
$$

Moreover, for every permutation $\pi$ of the input coordinates,

$$
H^{\ast}(f\circ \pi)=H^{\ast}(f),
$$

and for the Boolean complement $1-f$,

$$
H^{\ast}(1-f)=H^{\ast}(f).
$$

## Proof

For an integer $q\geq 0$, write

$$
[q]:=\{1,\ldots,q\},
\qquad
[0]:=\varnothing.
$$

If $f$ is constant, then $H^{\ast}(f)=0$ by using a positive constant score for the constant-one function and a negative constant score for the constant-zero function. The functions $\widetilde f$, $f\circ\pi$, and $1-f$ are also constant, so all three asserted equalities hold. We assume from now on that $f$ is nonconstant.

### Lemma 1. Finite strict margins

Let $X$ be finite, let $g:X\to\{0,1\}$ be nonconstant, and let $T:X\to\mathbb R$ satisfy

$$
g(u)=1 \Longleftrightarrow T(u)>0.
$$

Then there is a real number $\lambda$ such that $T-\lambda$ strictly sign-represents $g$ with positive margin. That is,

$$
g(u)=1 \Longrightarrow T(u)-\lambda>0,
\qquad
g(u)=0 \Longrightarrow T(u)-\lambda<0,
$$

and

$$
\min_{u\in X}|T(u)-\lambda|>0.
$$

Consequently, any score within this margin uniformly has the same signs on $X$.

**Proof.** Since $g$ is nonconstant, both fibers of $g$ are nonempty. Define

$$
a:=\max\{T(u):g(u)=0\},
\qquad
b:=\min\{T(u):g(u)=1\}.
$$

The strict threshold rule gives $a\leq 0$ and $b>0$, hence $a<b$. Set

$$
\lambda:=\frac{a+b}{2}.
$$

If $g(u)=0$, then

$$
T(u)-\lambda\leq a-\frac{a+b}{2}=\frac{a-b}{2}<0.
$$

If $g(u)=1$, then

$$
T(u)-\lambda\geq b-\frac{a+b}{2}=\frac{b-a}{2}>0.
$$

Because $X$ is finite,

$$
\mu:=\min_{u\in X}|T(u)-\lambda|>0.
$$

If another score $R$ satisfies $\max_{u\in X}|R(u)-(T(u)-\lambda)|<\mu$, then $R(u)$ has the same sign as $T(u)-\lambda$ for every $u\in X$. $\blacksquare$

Set

$$
K:=H^{\ast}(f).
$$

By Lemma 10, there are $K$ one-head atoms $\phi_1,\ldots,\phi_K$ and a constant $\theta_0$ such that

$$
T(x):=\theta_0+\sum_{h=1}^{K}\phi_h(x)
$$

computes $f$ by the strict threshold rule on $\{0,1\}^{n}$. Applying Lemma 1 and absorbing the shift into the constant term, we may write

$$
S(x):=\theta+\sum_{h=1}^{K}\phi_h(x)
$$

so that

$$
f(x)=1 \Longrightarrow S(x)>0,
\qquad
f(x)=0 \Longrightarrow S(x)<0.
$$

Define the positive margin

$$
\mu:=\min_{x\in\{0,1\}^{n}}|S(x)|>0.
$$

For each $h\in[K]$, write

$$
\phi_h(x)=
\frac{
\eta_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}(u_{hi}+\delta_h x_i)
}{
\gamma_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}
},
$$

where

$$
\gamma_h>0,
\qquad
\rho_{hi}>0,
\qquad
\alpha_h>0.
$$

We first prove the dummy-variable upper bound. For $\varepsilon>0$ and $y=(x,z)\in\{0,1\}^{n+m}$, define

$$
\Phi_{h,\varepsilon}(x,z):=
\frac{
\eta_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}(u_{hi}+\delta_h x_i)
+\sum_{r=1}^{m}\varepsilon\alpha_h^{z_r}\delta_h z_r
}{
\gamma_h+\sum_{i=1}^{n}\rho_{hi}\alpha_h^{x_i}
+\sum_{r=1}^{m}\varepsilon\alpha_h^{z_r}
}.
$$

This is a valid one-head atom on $n+m$ variables. The original coordinates keep their old positive weights. Each dummy coordinate has positive weight $\varepsilon$, the same $\alpha_h$, the same shared $\delta_h$, and dummy numerator parameter $0$.

For fixed $h$, as $\varepsilon\to0^{+}$, the numerator and denominator of $\Phi_{h,\varepsilon}(x,z)$ converge pointwise to the numerator and denominator of $\phi_h(x)$. The cube $\{0,1\}^{n+m}$ is finite, and the original denominators are positive, so this convergence is uniform. Since $K$ is finite, the sum over $h$ also converges uniformly. Therefore we can choose $\varepsilon>0$ such that

$$
\max_{(x,z)\in\{0,1\}^{n+m}}
\left|
\sum_{h=1}^{K}\Phi_{h,\varepsilon}(x,z)
-
\sum_{h=1}^{K}\phi_h(x)
\right|
<\frac{\mu}{2}.
$$

For this choice of $\varepsilon$, the score

$$
S_{\varepsilon}(x,z):=\theta+\sum_{h=1}^{K}\Phi_{h,\varepsilon}(x,z)
$$

has the same sign as $S(x)$ for every $(x,z)$. Hence

$$
S_{\varepsilon}(x,z)>0 \Longleftrightarrow f(x)=1 \Longleftrightarrow \widetilde f(x,z)=1.
$$

By Lemma 10,

$$
H^{\ast}(\widetilde f)\leq K=H^{\ast}(f).
$$

Conversely, fix the dummy variables to any value, for instance $z=(0,\ldots,0)$. Then $f$ is obtained from $\widetilde f$ by fixing coordinates and relabeling none of the remaining coordinates. Lemma 26 gives

$$
H^{\ast}(f)\leq H^{\ast}(\widetilde f).
$$

Thus

$$
H^{\ast}(\widetilde f)=H^{\ast}(f).
$$

Now let $\pi$ be a permutation of the $n$ input coordinates. The function $f\circ\pi$ is obtained from $f$ by relabeling coordinates and fixing no coordinates. By Lemma 26,

$$
H^{\ast}(f\circ\pi)\leq H^{\ast}(f).
$$

Applying the same argument to $\pi^{-1}$ gives

$$
H^{\ast}(f)\leq H^{\ast}(f\circ\pi).
$$

Therefore

$$
H^{\ast}(f\circ\pi)=H^{\ast}(f).
$$

It remains to prove complement invariance. Since $S$ strictly sign-represents $f$ with both signs separated from zero,

$$
-S(x)>0 \Longleftrightarrow (1-f)(x)=1.
$$

Also

$$
-S(x)=-\theta+\sum_{h=1}^{K}(-\phi_h(x)).
$$

Each $-\phi_h$ is again a valid one-head atom. Indeed, replace

$$
\eta_h \text{ by } -\eta_h,
\qquad
u_{hi} \text{ by } -u_{hi},
\qquad
\delta_h \text{ by } -\delta_h,
$$

and keep $\gamma_h$, $\rho_{hi}$, and $\alpha_h$ unchanged. The denominator is unchanged and the numerator is multiplied by $-1$. This is also the atom-negation closure recorded in Lemma 13.

Thus $1-f$ is computable with $K$ heads, so

$$
H^{\ast}(1-f)\leq H^{\ast}(f).
$$

Applying the same argument to $1-f$ and using $1-(1-f)=f$ gives

$$
H^{\ast}(f)\leq H^{\ast}(1-f).
$$

Consequently

$$
H^{\ast}(1-f)=H^{\ast}(f).
$$

All three claims follow. $\blacksquare$

## Consequence

The value of $H^{\ast}$ depends only on the active variables, up to coordinate relabeling, and is unchanged by Boolean output complement. Thus later upper and lower bounds may add or remove dummy ambient coordinates without changing head complexity.

This lemma does not assert invariance under complementing individual input bits $x_i\mapsto1-x_i$. Such maps are not coordinate relabelings in Lemma 26 and are not used in the proof above.
