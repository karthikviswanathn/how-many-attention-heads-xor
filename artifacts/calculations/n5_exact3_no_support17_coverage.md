# Exact Degree Three Without Exact-Only Support-17 Coverage

## Statement

Define $f:\lbrace0,1\rbrace^5\to\lbrace-1,1\rbrace$ by declaring its positive vertices to be

$$ \lbrace1,5,6,7,8,9,10,11,13,16,17,22,24,26,29\rbrace. $$

Equivalently, the $32$-bit positive mask is $625160162$.

Then $\deg_{\pm}(f)=3$, but the sign table of $f$ contains no conformal exact-degree-three-only circuit of support $17$.

Thus exhaustive continuation over the $23116$ exact-only circuit orbits of support $17$ cannot cover every five-bit truth table of exact threshold degree three.

## Exact cubic separator

In degree-first lexicographic monomial order, an integer cubic sign representation is

$$ \begin{aligned} p(x)={}&-14+30x_1-15x_2+27x_4+27x_5-15x_1x_2+42x_1x_3+23x_1x_4-30x_1x_5 \\ &+42x_2x_3+37x_2x_4-12x_2x_5-42x_3x_4-42x_3x_5-18x_4x_5 \\ &-58x_1x_2x_3-60x_1x_2x_4-60x_1x_2x_5+48x_1x_3x_4-27x_1x_3x_5 \\ &-60x_1x_4x_5-60x_2x_3x_4+27x_2x_3x_5-19x_2x_4x_5+48x_3x_4x_5. \end{aligned} $$

Exact evaluation gives

$$ \min_{x\in\lbrace0,1\rbrace^5} f(x)p(x)=12. $$

Hence $\deg_{\pm}(f)\leq3$.

## Exact quadratic obstruction

Use the support

$$ S=(2,6,7,10,11,15,16,17,21,25,28,29) $$

with positive weights

$$ \lambda=(2,1,1,1,1,2,1,1,2,2,1,3). $$

For every squarefree monomial $m$ of degree at most two, exact integer arithmetic gives

$$ \sum_{v\in S}\lambda_v f(v)m(v)=0. $$

If a quadratic $q$ strictly sign represented $f$, every summand $\lambda_v f(v)q(v)$ would be positive, while their sum would be zero. This contradiction proves $\deg_{\pm}(f)\geq3$.

Therefore $\deg_{\pm}(f)=3$.

## Exhaustive support-17 exclusion

Start from all $23116$ exact-only representatives of support $17$. Apply all $120$ coordinate permutations and simultaneous input complementation, giving $240$ input automorphisms. Check both output orientations.

The expansion has $5547840$ transformed incidences and $5286336$ distinct packed oriented circuits. Sorting the packed $64$-bit codes gives this SHA-256 digest:

```text
6ecc8f5fbafe4768f7f8ec726af5d54a4468b9206f409f9cdec5e336389d187f
```

Regard the masks as subsets of the cube. For a packed circuit with positive set $P$, negative set $N$, and support $C=P\cup N$, conformity is the exact condition

$$ F\cap C=P \qquad\text{or}\qquad F\cap C=N, $$

where $F=625160162$. Neither condition holds for any of the $5286336$ circuits.

This exclusion concerns only the continuation strategy on circuits of support $17$. It is not an H3 lower bound for $f$.

## Verification

Run:

```bash
python3 artifacts/calculations/verify_n5_exact3_no_support17_coverage.py
```

The verifier uses exact integer polynomial arithmetic and exact bit-mask enumeration throughout.
