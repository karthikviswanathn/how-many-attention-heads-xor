# Corrected Three-Bit Head Complexity

This file supersedes the earlier provisional list of three-bit functions estimated by training to have

$$ H^{\ast}(f) = 3. $$

That estimate was too pessimistic for three of the four listed functions. The theoretical pattern is recorded in `research/head_hierarchy_pattern.md`.

## Correct Three-Bit Hierarchy

For Boolean functions on three inputs:

$$ H^{\ast}(f) = 0 \quad \Longleftrightarrow \quad f \text{ is constant}. $$

$$ H^{\ast}(f) = 1 \quad \Longleftrightarrow \quad f \text{ is a nonconstant linear threshold function}. $$

$$ H^{\ast}(f) = 3 \quad \Longleftrightarrow \quad f \text{ is parity or its complement}. $$

All remaining three-bit functions have

$$ H^{\ast}(f) = 2. $$

## Former Provisional Examples

Bitstrings are in lexicographic order $000,001,010,011,100,101,110,111$.

| Bitstring | Threshold degree | Corrected $H^{\ast}(f)$ | Reason |
|---|---:|---:|---|
| $00010110$ | $2$ | $2$ | quadratic threshold function |
| $00011000$ | $2$ | $2$ | quadratic threshold function |
| $00101001$ | $2$ | $2$ | quadratic threshold function |
| $01101001$ | $3$ | $3$ | three-bit parity |

The complement of parity,

$$ 10010110, $$

is the other three-bit function with head complexity $3$.

