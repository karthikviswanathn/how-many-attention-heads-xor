# Problem: Equal denominators collapse a tangent form to a linear threshold function

## Background and definitions (self-contained)

Work on $\lbrace 0,1\rbrace^n$. An **affine** function is $A(x) = a_0 + \sum_i a_i x_i$. An affine $D$ is an **admissible denominator** if $D(x) > 0$ for all $x \in \lbrace 0,1\rbrace^n$ (positivity is all that is used here). A Boolean function $f$ is a **linear threshold function (LTF)** if $f$ is constant or there is an affine $A$ with $f(x) = 1 \iff A(x) > 0$ for all $x$.

For $H \geq 1$, an **order-$H$ tangent form** is
$$
P(x) = \theta \prod_{h=1}^H D_h(x) + \sum_{h=1}^H N_h(x) \prod_{g \neq h} D_g(x),
$$
with $\theta \in \mathbb{R}$, each $N_h$ affine and each $D_h$ an admissible denominator. It **sign-represents** $f$ if $f(x) = 1 \iff P(x) > 0$ and $f(x) = 0 \iff P(x) < 0$ for all $x$.

## Claim to prove

Suppose $f$ is sign-represented by an order-$H$ tangent form ($H \geq 1$) in which all denominators are equal: $D_1 = D_2 = \cdots = D_H = D$. Then $f$ is a linear threshold function.

Equivalently: any $f$ that is **not** an LTF cannot be sign-represented by a tangent form with all denominators equal; at least two distinct denominators are required.

## Guidance (prove every step rigorously)

1. **Substitute equal denominators.** With $D_h = D$ for all $h$, $\prod_{h=1}^H D_h = D^H$, and for each $h$, $\prod_{g \neq h} D_g = D^{H-1}$ (a product of $H-1$ copies of $D$). *(justification: there are $H$ factors in the full product and $H-1$ in each leave-one-out product.)*

2. **Factor out $D^{H-1}$.** Hence
   $$
   P(x) = \theta D(x)^H + \sum_{h=1}^H N_h(x) D(x)^{H-1} = D(x)^{H-1}\Big(\theta D(x) + \sum_{h=1}^H N_h(x)\Big).
   $$
   *(justification: $D^H = D^{H-1}\cdot D$, and each term $N_h D^{H-1}$ shares the factor $D^{H-1}$; distribute.)*

3. **Name the affine cofactor.** Let $A(x) := \theta D(x) + \sum_{h=1}^H N_h(x)$. As a sum of affine functions ($\theta D$ is affine, each $N_h$ is affine), $A$ is affine. *(justification: affine functions are closed under addition and scalar multiples.)*

4. **Positivity of $D^{H-1}$.** Since $D$ is an admissible denominator, $D(x) > 0$ for all $x$, hence $D(x)^{H-1} > 0$ for all $x$ (a positive number raised to a nonnegative integer power; if $H = 1$ then $D^{0} = 1 > 0$). *(justification: positivity is preserved by powers.)*

5. **Sign of $P$ equals sign of $A$.** For every $x$, $P(x) = D(x)^{H-1} A(x)$ with $D(x)^{H-1} > 0$, so $\mathrm{sgn}\,P(x) = \mathrm{sgn}\,A(x)$; in particular $P(x) > 0 \iff A(x) > 0$ and $P(x) < 0 \iff A(x) < 0$. *(justification: multiplying by a strictly positive number preserves sign.)*

6. **Conclude $f$ is an LTF.** Since $P$ sign-represents $f$, $f(x) = 1 \iff P(x) > 0 \iff A(x) > 0$ with $A$ affine. Thus $f$ is a linear threshold function (taking the constant case into account when $A$ has constant sign). $\blacksquare$

## Pitfalls to address explicitly

- The argument uses only $D > 0$ on the cube (positivity), not the one-sided-slope part of admissibility; state this. (It therefore also holds for the positivity-free $\mathrm{tChow}_{\pm}$ when the common factor $D$ is required positive; if $D$ may vanish or change sign the factorization still holds but $\mathrm{sgn}\,D^{H-1}$ need not be constant, so the conclusion can fail — note this restriction.)
- Handle $H = 1$ cleanly: then $P = \theta D + N_1 = A$ directly ($D^{0} = 1$), already affine.
- "LTF" includes the constant case (when $A$ does not change sign on the cube); do not claim $A$ must be nonconstant.
