# head-complexity

Lean 4 formalization of the head-complexity results for one-layer attention. The
definitions and theorems mirror the informal proofs in the top-level `lemmas/` writeups.

Depends on [mathlib](https://github.com/leanprover-community/mathlib4) (`v4.29.0`, pinned
in `lakefile.toml`). Build with:

```bash
lake exe cache get   # fetch prebuilt mathlib (first time only)
lake build
```

See the [repository README](../README.md) for the wider project context.
