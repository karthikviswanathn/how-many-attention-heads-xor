# Six-Bit Slice-Cone Limitation

## Purpose

This note records an exact limitation of the one-exception slice inequalities for the parity-triple candidate. Those inequalities are necessary for a quartic sign representative, but they do not by themselves exclude a four-head tangent polynomial.

The exact verifier is [verify_n6_parity_triple_slice_cone_limit.py](verify_n6_parity_triple_slice_cone_limit.py).

## Construction

Work in Fourier sign coordinates on six variables. The exceptional vertices are

$$ E=\lbrace21,38,41\rbrace. $$

Take four affine denominator coefficient rows

$$ D=\begin{pmatrix}21&-1&-1&-15&-1&-1&-1\\40&-1&-1&-1&-6&-1&-29\\25&-12&-1&-4&-5&-1&-1\\46&5&3&1&27&7&2\end{pmatrix}. $$

Their strict diagonal-dominance slacks are

$$ (1,1,1,1). $$

The first three rows have six negative slopes, and the fourth row has six positive slopes. Thus every denominator is strictly positive on the sign cube and has an admissible orientation.

Take four affine numerator coefficient rows

$$ A=\begin{pmatrix}-100&-54&4&60&-71&15&-99\\100&-72&23&-46&100&-66&68\\-18&100&-15&-100&70&29&-5\\-100&-18&-3&-21&-51&1&-3\end{pmatrix}. $$

Let $q$ be the Boolean Fourier coefficient vector of the tangent polynomial

$$ P=\sum_{h=1}^{4}A_h\prod_{g\neq h}D_g. $$

Products here use XOR convolution, which is multiplication in the Boolean Fourier coefficient ring. The verifier checks that $q_S=0$ whenever $\lvert S\rvert>4$.

## All 186 slice inequalities

For coordinate $i$, let $e_i$ be the unique exceptional point on the selected one-exception slice, and let $c_i$ be the fixed sign-coordinate value on that slice. In coordinate order,

$$ (e_0,\ldots,e_5)=(38,38,41,41,21,21), \qquad (c_0,\ldots,c_5)=(1,-1,1,-1,-1,1). $$

Every subset $S$ of the other five coordinates with $\lvert S\rvert\leq4$ gives the necessary strict inequality

$$ \chi_S(e_i)\left(q_S+c_iq_{S\cup\lbrace i\rbrace}\right)>0. $$

There are $6\cdot31=186$ such rows. Exact integer arithmetic gives

$$ \min \chi_S(e_i)\left(q_S+c_iq_{S\cup\lbrace i\rbrace}\right)=1001>0. $$

The 120 middle-level rows with $\lvert S\rvert\in\lbrace2,3\rbrace$ also hold strictly, with minimum

$$ 1327>0. $$

## Consequence for the proof strategy

This tangent polynomial does not sign-represent the target. It fails at $29$ of the $64$ vertices. Its worst signed target value is

$$ -23919252 $$

at vertex $52$.

Therefore no universal four-head obstruction can follow from the 120 middle-level inequalities, or even from all 186 one-exception slice coefficient inequalities, alone. A proof for this candidate must add constraints that couple different slices globally, such as direct truth-table evaluation inequalities, quotient-cut constraints, or another compatibility condition not implied by the six separate one-exception slices.
