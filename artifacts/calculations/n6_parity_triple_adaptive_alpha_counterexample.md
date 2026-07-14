# Adaptive-alpha Antipodal Dual Counterexample

## Setup

Let $s(z)$ be the sign of the six-bit parity-triple target, and let $B_1,\ldots,B_4$ be positive affine denominators. Put

$$ D(z)=\prod_{h=1}^4B_h(z). $$

After eliminating the four constant numerator coefficients, the evaluation feature vector has one global constant coordinate and the twenty-four coordinates $z_i/B_h(z)$. Write $u(z)$ for this feature vector multiplied by $s(z)$.

The target has the same sign on twenty-nine antipodal pairs. It has opposite signs on the three pairs containing the exceptional vertices. The adaptive-alpha ansatz gives one multiplier $\gamma_p\geq0$ to each ordinary pair $p=\lbrace z,-z\rbrace$ and ties its two vertex weights in the ratio $D(z)^\alpha:D(-z)^\alpha$. Its grouped row is therefore

$$ G_p(\alpha)=D(z)^\alpha u(z)+D(-z)^\alpha u(-z). $$

The six endpoints in the exceptional pairs remain separate rows. A nonzero nonnegative dependence among these thirty-five rows would be a valid Gordan obstruction for the full evaluation inequalities.

## Normalized moment form

For one ordinary pair, define

$$ \delta_p=\frac{1}{2}\log\frac{D(z)}{D(-z)}, \qquad \tau_p(\alpha)=\tanh(\alpha\delta_p). $$

Divide $G_p(\alpha)$ by the positive number $D(z)^\alpha+D(-z)^\alpha$. Its constant coordinate is $s(z)$. Its coordinate indexed by head $h$ and variable $i$ is $s(z)z_i$ times

$$ \frac{1}{2}\left(\frac{1}{B_h(z)}-\frac{1}{B_h(-z)}\right)+\frac{\tau_p(\alpha)}{2}\left(\frac{1}{B_h(z)}+\frac{1}{B_h(-z)}\right). $$

Thus the path is affine in twenty-nine pair-specific hyperbolic tangent parameters. As $\alpha\to+\infty$, each ordinary row selects the endpoint with larger $D$. As $\alpha\to-\infty$, it selects the endpoint with smaller $D$.

## Exact counterexample

Consider the four denominator coefficient rows

$$ \begin{aligned} B_1&=(78,-3,-12,-13,-20,-2,-13), \\ B_2&=(95,-28,-2,-29,-2,-29,-2), \\ B_3&=(95,-17,-1,-27,-11,-7,-4), \\ B_4&=(63,-10,-6,-16,-7,-16,-6). \end{aligned} $$

Each row lists the intercept followed by its six slopes. Every slope is strictly negative, and the four intercept inequalities are

$$ 78>63, \qquad 95>92, \qquad 95>67, \qquad 63>61. $$

Hence all four denominators are strictly positive on the cube and belong to one admissible orientation component.

For this tuple, the grouped rows have no nonzero nonnegative dependence for any real $\alpha$. Equivalently, for every $\alpha$ there is a numerator vector $v$ that is strictly positive on all thirty-five grouped rows.

## Finite exact audit

Fix a rational numerator vector $v$, and put $a(z)=u(z)\cdot v$. Its inequality on an ordinary pair is

$$ a(z)D(z)^\alpha+a(-z)D(-z)^\alpha>0. $$

If $D(z)\neq D(-z)$, the left side has at most one real zero after division by either positive exponential term. If the two products are equal, its sign is constant. Consequently, one numerator that works at both endpoints of an interval works throughout that interval.

For a rational endpoint $\alpha=p/q$, every check reduces to an integer-power comparison. For example, if $a(z)>0>a(-z)$, the pair inequality is equivalent to

$$ \left(\frac{D(z)}{D(-z)}\right)^p>\left(\frac{-a(-z)}{a(z)}\right)^q. $$

The verifier uses numerical linear programming only to discover candidate numerator vectors. It rounds each candidate to an integer vector and then checks every exceptional endpoint and every pair comparison with exact rational arithmetic. It finds fifty-eight adjacent dyadic intervals covering $[-8,8]$. The largest dyadic denominator is $4096$. Two further exact numerators cover the tails by checking the finite endpoint and the coefficient of the dominant exponential at the corresponding limit.

Run

```text
python3 artifacts/calculations/verify_n6_parity_triple_adaptive_alpha_counterexample.py
```

The expected output is

```text
admissible denominator heads: 4
ordinary antipodal pairs: 29
independent exceptional endpoints: 6
exact finite interval certificates: 58
exact tail certificates: 2
verified adaptive-alpha grouped-dual counterexample
```

## Consequence

Allowing the exponent $\alpha$ to depend on the denominator tuple does not make the antipodally tied power family universal. This counterexample only refutes that restricted dual ansatz. It does not provide a four-head representation of the target, because unrestricted full-evaluation duals still exist numerically on this denominator tuple.
