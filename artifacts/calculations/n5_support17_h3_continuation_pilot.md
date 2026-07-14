# Five-Bit Support-17 H3 Continuation Pilot

## Scope

This pilot uses the $23116$ exact-degree-three-only circuit families of support $17$. Join two canonical families when their $15$-vertex free sets differ by one exchanged cube vertex.

The graph has $50569$ edges, $22243$ nonisolated vertices, and $1282$ connected components. Its largest component has $20896$ vertices. The global-dictionary seed family $16737$ lies in this largest component.

## One-neighborhood result

Family $16737$ has exactly $12$ neighbors in this graph. A finite deterministic direct-kernel search attempted all $12$. Nine were exactified in a first pass. The first-pass misses were

$$ (16404,16735,16857). $$

A stronger second pass exactified these remaining three. Thus the final one-neighborhood result is $12$ exact hits and no remaining search misses.

The exact-hit families are

$$ (14950,16404,16454,16725,16735,16738,16739,16741,16809,16846,16856,16857). $$

Every hit is independently rechecked using the exact $32$ by $16$ cleared integer matrix. The check proves positivity of all denominators, rank $15$ on the free set, and the forced circuit signs of the unique kernel score.

The retained first-pass miss list records the finite-search history. The second pass shows directly why such misses cannot be treated as head lower bounds.

## Example certificate

For family $16725$, one exact denominator triple is

$$ \begin{aligned} D_1&=(300,-1,-70,-21,-14,-6), \\ D_2&=(298,-108,-30,-1,-6,-134), \\ D_3&=(299,-51,-53,-44,-31,-67). \end{aligned} $$

All three are negative-orientation denominators and are strictly positive on the Boolean cube.

## Verification

Run:

```bash
python artifacts/calculations/verify_n5_support17_h3_continuation_pilot.py
```

The verifier reconstructs the full adjacency graph, checks its exact counts, verifies the seed, and exactifies all $12$ archived continuation hits.
