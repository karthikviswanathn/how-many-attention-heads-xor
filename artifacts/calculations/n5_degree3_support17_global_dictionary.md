# Support-Seventeen Global Three-Head Dictionary

## Exact fixed-space criterion

Fix three admissible positive affine denominators $D_1,D_2,D_3$. After clearing their positive product, the three-head score space has the following independent $16$-column presentation:

$$ D_1D_2D_3, \qquad x_iD_2D_3, \qquad x_iD_1D_3, \qquad x_iD_1D_2 \quad\text{for }1\leq i\leq5. $$

Let $C$ be a support-seventeen signed circuit and let $F=C^{\mathsf{c}}$, so $\lvert F\rvert=15$. This fixed space shatters every sign extension of $C$ if and only if:

1. its restriction to $F$ has rank $15$;

2. the resulting one-dimensional kernel score vanishes on $F$ and has the forced circuit signs on $C$, up to a global sign.

Both conditions use only exact integer arithmetic after denominators are fixed.

## Global dictionary pilot

The exact affine dichotomy leaves $23116$ support-seventeen families in which every extension has threshold degree exactly three. A deterministic global dictionary of $512$ denominator triples was screened against all of them at once. The dictionary mixes:

- independent log-uniform triples;

- triples with two nearly coincident denominators;

- triples with all three denominators nearly coincident.

Column-whitened batched linear algebra found only two incidences. Both survived exact reconstruction. The selected dictionary sources are $438$ and $466$, covering family indices $432$ and $16737$. Thus the exact finite result is

$$ 2 \text{ covered families}, \qquad 23114 \text{ uncovered families}. $$

The two exact denominator triples are

$$ \begin{aligned} &(8,1,9,645,64,33), \quad (481,380,49,678,164,725), \quad (837,-4,-1,-4,-143,-548), \\ &(999999,-1101,-8721,-206419,-868,-780890), \quad (1023341,-844279,-1,-1,-67592,-111467), \\ &\hspace{8em}(1039074,-791803,-1,-50224,-45368,-56119). \end{aligned} $$

Every denominator is strictly positive on the cube and has one common slope orientation within its head.

## Interpretation

Generic global spaces are far too sparse for a practical set-cover proof. The observed density is two exact incidences among

$$ 512\cdot23116=11835392 $$

space-family tests. This does not imply that the uncovered families need more than three heads. It shows that useful denominator triples occupy thin, circuit-dependent regions, consistent with the near-confluent tuples returned by targeted tangent factorization.

The compact exact archive is [`n5_support17_global_dictionary_coverage.npz`](n5_support17_global_dictionary_coverage.npz). The [dictionary verifier](search_n5_support17_global_dictionary.py) reconstructs the independent cleared matrix, its exact restriction rank, and its integer kernel sign certificate for every assignment. The precise uncovered set consists of the archive entries with assignment $-1$. Zero-set layer profiles for the largest uncovered classes are recorded in [`n5_support17_global_dictionary_summary.json`](n5_support17_global_dictionary_summary.json).
