# Exact tChow Certificates: f6 and f8

Date: 2026-07-17. Produced by Claude (Fable 5) with an LP-in-the-loop search seeded from the
degree-cone analytic center; every certificate below is verified in exact integer arithmetic
(no floating point in the final check; run `python3 verify_certificates.py` to re-check both
certificates from scratch).

## Setting

$\mathrm{tChow}_{\pm}(f)$ is the least $H$ such that some

$$ P(x) = \theta\prod_{h=1}^{H} D_h(x) + \sum_{h=1}^{H} N_h(x)\prod_{g\neq h} D_g(x) $$

with arbitrary affine $N_h, D_h$ strictly sign-represents $f$ on the cube (the unrestricted
tangential-Chow invariant of the autoresearch ledgers, sandwiched
$\deg_{\pm}(f) \leq \mathrm{tChow}_{\pm}(f) \leq H^{\ast}(f)$). Conventions in both JSON files:
$x \in \lbrace 0,1\rbrace^n$, code $= \sum_i x_i 2^i$, affine coefficient vectors are
$[c_0, c_1, \ldots, c_n]$ meaning $c_0 + \sum_i c_i x_i$, and $P(x) > 0$ iff $f(x) = 1$.

## Result 1: the six-bit parity triple has tChow exactly 4

$f_6$ = six-bit odd parity with the three values at codes 21, 38, 41 flipped.
`tchow4_f6_integer_certificate.json` gives $\theta = -13$, four integer denominators with
entries in $[-10, 10]$, four integer numerators with entries in $[-240, 240]$, and the minimum
of $\sigma(x)P(x)$ over all 64 points equal to $2040 > 0$. Together with the known
$\deg_{\pm}(f_6) = 4$:

$$ \mathrm{tChow}_{\pm}(f_6) = 4. $$

Consequence: the tangential-Chow lower bound cannot prove $H^{\ast}(f_6) \geq 5$. Any four-head
exclusion for $f_6$ must use the semialgebraic admissibility constraints of genuine attention
heads (denominator positivity, orientation), not only the cleared algebraic form. This
complements the jul15 finding (`n6_quartic_tangent_low_degree_invariants.md`) that the
unrestricted class has no low-degree polynomial invariant: there is no unrestricted sign
obstruction either, because an unrestricted representation exists.

Note the class is thin in practice: 3000 random-restart LP searches found nothing (margins at
solver noise), while least-squares seeding toward the degree-4 cone center found 22 distinct
solutions with margins near $2\times 10^{-2}$. The degree-4 coefficients of any representer are
fully sign-forced (all 15, LP-certified; positive pairs form the hexagon 0-3-5-1-2-4).

## Result 2: tChow separates from head complexity on the lemma 189 function

$f_8(x,y) = 1$ iff the Hamming distance of $x, y \in \lbrace 0,1\rbrace^4$ is at least 2
(bits 0-3 are $x$, bits 4-7 are $y$). `tchow2_f8_integer_certificate.json` gives a two-head
certificate ($\theta = 39$, integer entries bounded by 600, minimum signed value $840 > 0$ over
all 256 points). With $\deg_{\pm}(f_8) = 2$ and the lemma 189 result $H^{\ast}(f_8) = 3$:

$$ \mathrm{tChow}_{\pm}(f_8) = 2 < 3 = H^{\ast}(f_8). $$

So the sandwich upper inequality is strict in general: $\mathrm{tChow}_{\pm}$ is not equal to
$H^{\ast}$, and head positivity carries lower-bound content invisible to the unrestricted
tangential form. (Epistemic status: the certificate side is exact integer arithmetic; the
strictness inherits whatever confidence lemma 189's written lower-bound proof carries.)

## Files

- `tchow4_f6_integer_certificate.json`, `tchow2_f8_integer_certificate.json`: the certificates.
- `tchow4_f6_search.py`: the fixed-denominator LP oracle and outer search.
- `verify_certificates.py`: standalone exact integer verification of both certificates
  (no dependencies; the integer certificates were obtained from raw LP hits by grid
  rounding plus this exact re-verification).
