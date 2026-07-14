# Support-54 Obstruction Counterexample

## Purpose

The fixed 54-row subsystem for the six-bit parity-triple candidate is not a universal four-head obstruction. A strict tangent separator appears after a small unequal-slope perturbation of the symmetric endpoint-complementarity stratum.

This does not give a four-head representation of the full target. The score fails at six of the ten vertices omitted from the subsystem.

## Exact denominators

In Fourier sign coordinates, use the four affine denominator rows

$$ D=\begin{pmatrix}7000&-999&-1001&-1000&-1001&-1000&-1000\\8000&-999&-1000&-1001&-1000&-999&-1001\\7000&1000&1000&1001&1000&1000&1001\\8000&1000&1000&1001&1001&1000&999\end{pmatrix}. $$

Their ranges on the sign cube are

$$ [999,13001], \qquad [2000,14000], \qquad [998,13002], \qquad [1999,14001]. $$

The first two heads have strictly negative slopes, and the last two have strictly positive slopes. All four denominators are therefore admissible and strictly positive.

## Exact tangent separator

Use one global coefficient followed by six numerator-slope coefficients for each head:

$$ \begin{aligned} x={}&(-4;\ 17404471,1964103,2135496,27504630,-74626339,17563083;\\ &-22500772,0,-271622,-37132307,100000000,-22735419;\\ &-17259383,-1682841,-1884670,-26896563,73082942,-17481914;\\ &22365675,-297405,0,36445738,-98196941,22650461). \end{aligned} $$

Let $W(z)$ be the signed cleared tangent row. Exact integer evaluation gives

$$ \min_{z\in U} W(z)x=53028365575824>0. $$

Thus the tangent space strictly separates all 54 rows in $U$.

## Full-table failures

On the full 64-point truth table, the signed score is nonpositive exactly at

$$ \lbrace6,16,21,42,47,57\rbrace. $$

All six points belong to the omitted hyperplane section. The other four omitted points, $9,27,36,54$, have the correct strict sign.

Therefore the fixed support-54 cone cannot prove that four heads are impossible. Any valid lower bound for the six-bit candidate must retain additional pointwise constraints from the omitted hyperplane section.

## One-vertex repair at this tuple

Adding code $16$ to $U$ restores an exact positive Gordan circuit. Its 26-row support is

$$ (0,1,2,4,5,8,10,15,17,20,22,23,25,31,32,34,35,44,55,58,59,60,61,62,63,16). $$

The primitive weights are large, with at most $212$ decimal digits. The verifier reconstructs them exactly by rational row reduction, checks that every weight is positive, and checks all 25 annihilation equations. Passing `--print-repair-weights` prints the complete integer tuple.

This circuit has full affine rank six and no nonidentity signed-coordinate symmetry. It is not an affine-flat or quotient circuit. The repaired 55-row set itself has a cleaner description: it contains the complete hyperplane $\chi_{58}=1$, while all nine vertices that remain omitted lie in the opposite coset.

## Verification

Run:

```shell
python3 artifacts/calculations/verify_n6_parity_triple_support54_counterexample.py
```

The verifier checks denominator orientation and positivity, evaluates the 54 subsystem rows exactly, identifies the six full-table failures, and reconstructs the exact 26-row repair circuit.
