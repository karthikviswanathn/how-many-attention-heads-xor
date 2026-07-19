# Building & verifying the Lean proofs

This document gives **exact, reproducible** instructions for compiling the
`head-complexity` Lean 4 formalization and checking that the results are
axiom-clean. It covers both a generic machine and the specific HPC environment
(SURF Snellius, project `gusr0688`) the proofs were developed on.

For the wider project context see [`README.md`](README.md), and for the current
proof architecture see [`PROOF_OVERVIEW.md`](PROOF_OVERVIEW.md).

---

## 1. Toolchain and dependencies

| Component | Pinned version | Where pinned |
|-----------|----------------|--------------|
| Lean      | `leanprover/lean4:v4.31.0` | `lean-toolchain` |
| Lake      | `5.0.0-src` (ships with the toolchain) | — |
| mathlib   | `v4.31.0` (`leanprover-community/mathlib4`) | `lakefile.toml` → `[[require]]`, locked in `lake-manifest.json` |
| elan      | `4.2.3` (any recent elan works) | — |

`elan` installs the exact Lean/Lake the toolchain file requests, so you do **not**
need to install Lean by hand — just have `elan` on `PATH` and let it resolve the
pin on first `lake` invocation.

The project builds against a stock mathlib with **no patches**; the only thing
that must match is the rev. Everything below assumes you are in the
`head-complexity/` directory (the Lake package root, where `lakefile.toml` lives).

---

## 2. Generic build (any machine with internet)

```bash
cd head-complexity
lake exe cache get   # download prebuilt mathlib oleans (first time only; ~minutes)
lake build           # compile the HeadComplexity library (~minutes once cache is in)
```

`lake exe cache get` fetches mathlib's prebuilt `.olean` files so you don't
recompile mathlib (which would take hours). `lake build` then compiles the public
`HeadComplexity` umbrella, including all `Results` and `Examples`. A clean full
build of `HeadComplexity` is a few minutes on a modern multi-core machine once the
mathlib cache is present.

If `lake exe cache get` fails with a TLS/`curl`/JSON error, see §4.

---

## 3. Verifying the headline result is axiom-clean

The point of the formalization is a *trusted* proof, so always confirm the final
theorems depend only on Lean's three standard axioms
(`propext`, `Classical.choice`, `Quot.sound`) — i.e. no `sorry`, no extra axioms:

```bash
cat > /tmp/AxiomCheck.lean <<'EOF'
import HeadComplexity
open HeadComplexity
#print axioms theorem12_symmetric                  -- L12, unconditional equality
#print axioms symmetricFn_computable             -- L12 upper bound
#print axioms signChanges_le_of_computableWithHeadsN  -- L12 lower bound
#print axioms theorem6_degree_le                   -- L6 (model → threshold degree)
#print axioms f10Q_ne_zero                         -- exact nonvanishing certificate
#print axioms theorem13_strict_separation          -- explicit strict separation
EOF
lake env lean /tmp/AxiomCheck.lean
```

Expected output — every line ends in exactly `[propext, Classical.choice, Quot.sound]`:

```
'HeadComplexity.theorem12_symmetric' depends on axioms: [propext, Classical.choice, Quot.sound]
...
```

A grep for `sorry`/`admit` should also come back empty:

```bash
rg -n "sorry|admit\b" HeadComplexity.lean HeadComplexity   # → no matches
```

`build.slurm` (§5) runs an expanded version of this axiom check automatically and
prints `AXIOM_RC=0` on success.

---

## 4. The mathlib-cache `curl` fix (required on some systems)

**Symptom:** `lake exe cache get` fails. mathlib's cache tool ships its own static
`curl-7.88.1`, which on some hosts links a broken OpenSSL 3.0.8 and dies with
`error:16000069 STORE routines::unregistered scheme`. Substituting the system
`curl` then trips a second bug: `curl --write-out %{json}` emits the token
`"http_connect":000`, and JSON forbids leading zeros, so the cache tool's JSON
parser chokes.

**Fix:** place a wrapper at the path mathlib's `getCurl` (in `Cache/IO.lean`)
probes — `<mathlib-cache-dir>/curl-7.88.1` — that delegates to a working system
`curl` and repairs the writeout JSON on the fly. On Snellius the cache dir is
`/projects/gusr0688/.cache/mathlib`; adjust for your `XDG`/cache location.

```bash
#!/usr/bin/env bash
# Delegate to the system curl (working TLS) and repair the one invalid JSON
# token ("http_connect":000 → :0) that mathlib's cache parser rejects.
# Downloaded bodies use `-o <file>`, so only the small writeout JSON flows
# through this pipe.
set -o pipefail
/usr/bin/curl "$@" | sed -u 's/:000\([,}]\)/:0\1/g'
exit "${PIPESTATUS[0]}"
```

```bash
# install it (make executable; mathlib picks it up automatically, no re-download)
install -m755 curl-wrapper.sh /projects/gusr0688/.cache/mathlib/curl-7.88.1
```

`getCurl` uses this path **only if the file exists**, otherwise it falls back to
`curl` on `PATH`. If your system `curl` is healthy you may not need this at all —
try the plain build in §2 first.

---

## 5. Building on Snellius compute nodes (recommended here)

The login node is heavily contended (load ~35–40); offload builds to a compute
node via SLURM. **All toolchain + cache state lives on shared GPFS**
(`/gpfs/work5/0/gusr0688/...` and `/projects/gusr0688/...`), visible from every
node, so compute nodes build fully **offline** — no re-fetch needed.

Environment every job must set (already baked into the scripts below):

```bash
export ELAN_HOME=/gpfs/work5/0/gusr0688/fair_stuff/.elan
export PATH="$ELAN_HOME/bin:$PATH"
export LEAN_NUM_THREADS="${SLURM_CPUS_PER_TASK:-16}"   # see CRITICAL note
```

> **CRITICAL:** set `LEAN_NUM_THREADS=$SLURM_CPUS_PER_TASK`. Otherwise Lean spawns
> one worker per *host* core (32) inside a smaller cgroup and thrashes — a 4-core
> job once stalled at ~8 s CPU in 3 min. With the cap, a full `lake build` +
> axiom check finishes in ~2–3 min.

**Account / partitions:** account `gusr38169` has budget only for `cbuild`,
`staging`, and GPU partitions (not `rome`/`genoa`). Use `--partition=cbuild,staging`
and let SLURM pick whichever is free (both are the identical shared `srv[1-10]`
hardware, 32 cores / 224 GB, ~2.0 SBU/thread-hour). `cbuild` is the official build
partition and has **outbound internet** (use it if you ever need to re-fetch the
mathlib cache or a toolchain); `staging` is officially data-transfer but works as
a fallback. Set `--mem` explicitly so the job fits the shared node's free RAM (a
too-large `--mem`, e.g. 16 cpu × 7 G = 112 G, makes the job pend on `Resources`).
A 16-thread ~3-min build costs ≈ 1.6 SBU.

### Job scripts (in this directory)

| Script | What it does | Submit with |
|--------|--------------|-------------|
| `build.slurm`   | full `lake build` + `#print axioms` check (16 cpu / 32 G / 25 min) | `sbatch build.slurm` |
| `check.slurm`   | typecheck one **already-imported** file via `lake env lean` (8 cpu / 24 G) | `sbatch --export=ALL,CHECK_FILE=HeadComplexity/Results/ThresholdDegree.lean check.slurm` |
| `checkmod.slurm`| build one module **and its deps** via `lake build <Module>` (16 cpu / 48 G) | `sbatch --export=ALL,CHECK_MOD=HeadComplexity.Results.ThresholdDegree checkmod.slurm` |

Each script writes `<name>.slurm.out` (gitignored via `*.out`) ending in a
`DONE_SENTINEL` line, with `BUILD_RC` / `CHECK_RC` / `AXIOM_RC` = `0` on success.

```bash
sbatch build.slurm
# wait, then:
grep -E "BUILD_RC|AXIOM_RC|Build completed" build.slurm.out
# → Build completed successfully (NNNN jobs).
#   BUILD_RC=0
#   AXIOM_RC=0
```

> **check vs checkmod:** `lake env lean HeadComplexity/Results/ThresholdDegree.lean`
> (what `check.slurm` runs) requires every import of that file to already have a
> built `.olean`. For a *brand-new* file whose deps aren't yet in the root build,
> use `checkmod.slurm` (`lake build HeadComplexity.Results.ThresholdDegree`),
> which builds the dependency oleans first.

---

## 6. Quick reference

```bash
# one-time, on a node with internet (login or cbuild):
cd head-complexity && lake exe cache get        # + the §4 curl fix if it errors

# full local build + axiom-cleanliness:
lake build && lake env lean /tmp/AxiomCheck.lean   # (AxiomCheck.lean from §3)

# on Snellius, offloaded:
sbatch build.slurm && tail -f build.slurm.out      # watch for DONE_SENTINEL
```

The top-level theorem proved by a clean build is

```lean
theorem HStarN_symmetricFn (F : ℕ → Bool) (n : ℕ) :
    HStarN n (symmetricFn F) = signChanges n F
```

(Theorem 12: the head complexity of a symmetric Boolean function equals the number
of sign changes of its weight profile), depending only on the three standard
Lean axioms.
