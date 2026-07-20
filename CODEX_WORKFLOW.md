# Working with Codex (and subagents) on Lean proofs — field notes

Practical lessons from formalizing Theorems 4–12 of this project with OpenAI's Codex
CLI as a peer reviewer. These extend the basic guidance in [`CLAUDE.md`](CLAUDE.md).
The throughline: **Codex is a fast idea/-API engine; the Lean build is the only
oracle.** Use Codex to shorten the path to a *candidate* proof, then verify every
line yourself with the build loop.

## The non-negotiables (learned the hard way)

1. **Always `codex exec "…" </dev/null`.** `codex exec` reads its prompt argument
   *and also drains stdin*. Launched as a background job (`run_in_background`),
   stdin is an open pipe that never sends EOF, so Codex hangs forever on
   "Reading additional input from stdin…". The `</dev/null` makes it take only the
   argument and return. This is mandatory for every background consult.

2. **Codex cannot run long builds.** With stdin closed (the fix above), Codex
   errors `stdin is closed for this session; rerun exec_command with tty=true`
   when it tries to manage a long-running sub-command (e.g. a 90 s `lake build`).
   So in the prompt, tell it **"do NOT run lake; reason from the code/goal"** and
   feed it the build results yourself. (`lake`/`lean` *are* on its `PATH` via
   `~/.bashrc` → `ELAN_HOME`, so quick `lake --version` / `rg` are fine; heavy
   builds are not.)

3. **Keep questions FOCUSED — bounded to one obstacle.** A broad question
   ("prove this injectivity AND plan all of Theorem 11") sent Codex into a
   13 000-line mathlib-grep loop that never converged; I killed it and solved the
   piece myself (`finFunctionFinEquiv`). The same model, asked one tight question
   ("what is the cleanest single-head construction realizing `b/(t(x)+a)`"),
   returned a complete, correct construction in ~130 k tokens. Recipe for a good
   consult prompt:
   - one specific obstacle (a single theorem, a single error, a single design fork);
   - the exact goal state / error text + the minimal surrounding definitions;
   - "be concise, <N words, concrete theorem names / tactics";
   - "do not run lake; reason from the goal";
   - if asking for a construction, give the working *template* it should mirror.

## What Codex is good / bad at here

- **Good:** model-level constructions (it designed the `atomHead` softmax gadget
  and the weighted/affine generalizations), naming the right mathlib theorem when
  you describe the goal, spotting a faithfulness gap, and giving a proof *skeleton*.
- **Unreliable:** exact mathlib signatures (it suggested `degree_interpolate_le`
  without its explicit `r` argument; it missed that `r`/`r'` are `variable`s), and
  whether a niche theorem exists at all (it correctly reported "no ready-made
  subset-sums-of-2^i-are-injective theorem" — but only after a long search). Treat
  every theorem name as a hypothesis to check against the build.
- **Verify, don't trust:** more than once Codex's suggested tactic was *almost*
  right (e.g. `<;> simp; ring` where `simp` fully closes one branch, so the
  trailing `ring` errors on no goals). The build caught it; Codex's reasoning did
  not.

## The loop that actually works

```
design/sketch with Codex (background, </dev/null, focused)
   → write the Lean myself
   → SLURM build (fast, authoritative feedback)
   → on error: either fix directly, or hand Codex the EXACT error + goal for a fix
   → repeat until CHECK_RC=0 AND zero warnings
```

The build is the source of truth and runs on a compute node (see
[`BUILDING.md`](formalization/BUILDING.md)); a single new ~300-line module checks
in well under a minute once its deps are cached. Iterating against the build is far
faster and safer than iterating against Codex's prose.

## Delegating subtasks (parallelism)

For a big but *well-specified* piece (e.g. the Theorem 11 affine head — a concrete
`d=n+1` construction), spawn a background **subagent** with: the full design, the
worked templates to mirror (`atomHead`/`weightedAtomHead`), the exact build
commands, and explicit permission to consult Codex for stuck steps. Meanwhile work
the easy/independent parts on the main thread, and run Codex consults in the
background for orthogonal sub-theorems. Three things make this safe:

- **Non-overlapping files.** Give the subagent its own file; never edit the same
  file concurrently. Add the root `import` only when assembling.
- **Separate SLURM output files.** Concurrent `sbatch checkmod.slurm` runs clobber
  the shared `checkmod.slurm.out`. Use a per-worker copy (`checkmod2.slurm` with a
  distinct `--output=…`), and filter the queue by job name
  (`squeue -u $USER -n lean-mod2`) so each waiter only blocks on its own job.
- **A crisp contract.** The subagent's deliverable is one named theorem,
  `CHECK_RC=0`, no `sorry`, no warnings — easy to verify on return.

## Quick reference

```bash
# focused background consult
codex exec "$(cat prompt.txt)" </dev/null 2>&1   # prompt ends: "be concise; don't run lake"

# point Codex at a file by @path instead of pasting it (verified to work in `exec`):
codex exec "Review @HeadComplexity/Sandwich.lean for gaps; name the main theorem." </dev/null
#  @path is resolved relative to Codex's workdir; it reads the file itself (a SHORT
#  command, safe under </dev/null). Saves the $(cat ...)+quoting dance for code/spec
#  review. Note it still pulls the whole file into Codex's context, so for a focused
#  question prefer @-mentioning the ONE relevant file, not the whole tree. (For THEORY
#  consults keep hand-distilling context — raw files dilute the question.)

# AUTO-RESUME on flaky connection. Codex sometimes dies mid-reasoning with
# "ERROR: Reconnecting... 5/5" (transient API/network hiccup). DON'T relaunch from
# scratch — that re-pays for all the reasoning. Codex sessions are RESUMABLE:
SID=$(grep -oE 'session id: [0-9a-f-]+' out | awk '{print $3}')   # printed in the header
codex exec resume "$SID" "Your last turn was cut off by a reconnect, not by you. \
  Continue EXACTLY where you stopped; don't repeat finished reasoning." </dev/null
#  Resume preserves full context (verified). A completed turn ends with a "tokens used"
#  footer; a reconnect-death does NOT — that's the success/failure signal. The wrapper
#  bisym_scratch/codex_robust.sh automates it (run -> if no footer, resume same SID ->
#  repeat), so one background job self-heals across reconnects and notifies once with the
#  full answer. MUST run from a git repo dir (a bare scratch dir => "Not inside a trusted
#  directory").
#  PANEL-VISIBILITY GOTCHA: stream codex with `... | tee -a "$OUT" "$TMP"` (NO `>>`
#  redirect on tee). `tee "$TMP" >> "$OUT"` sends tee's passthrough INTO the file, so a
#  run_in_background task panel shows only the wrapper's own `echo` lines and looks frozen
#  ("[robust] initial run" then blank) even though the OUT file is filling fine. tee with
#  no stdout redirect passes through to the wrapper's stdout = the panel. Watch either the
#  panel or `tail -f "$OUT"`.
#  DIAGNOSING "codex is dead": on a SHARED login node, `pgrep -x codex` / `pkill -x codex`
#  match EVERY user's VSCode-extension `codex app-server` (dozens), not yours — a non-issue
#  mistaken for a pileup. Filter to your own work with `pkill -u $USER -f 'codex exec'`.
#  Reachability check: `curl -sS -o /dev/null -w '%{http_code} %{time_total}\n'
#  https://api.openai.com/v1/models` (401 fast = network FINE, auth-gated as expected).
#  A fresh `timeout 60 codex exec "Reply ALIVE" </dev/null` ending in "tokens used" = healthy;
#  transient reconnect deaths clear on their own — don't over-engineer around a blip.

# my build lane (so it doesn't collide with a subagent's checkmod.slurm)
sbatch --export=ALL,CHECK_MOD=HeadComplexity.Results.ThresholdDegree checkmod2.slurm
while squeue -u $USER -h -n lean-mod2 -o "%i" | grep -q .; do sleep 15; done
grep -nE "CHECK_RC|error:|warning:" checkmod2.slurm.out
```
