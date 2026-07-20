# Informal Decomposition Guide

> How to break a hard theorem into a dependency graph of sub-lemmas, each with a
> rigorous informal proof, **before** any Lean formalization. Adapted from
> numina-lean-agent's `blueprint_agent.md`, `coordinator.md`, and `common.md`,
> with every Gemini/GPT call swapped for the subscription tools
> (`informal_prover_codex.py`, `discussion_partner_codex.py`). No API keys.

The single source of truth for the decomposition is `BLUEPRINT.md`. Update it
immediately after any node changes (do not batch).

## The loop

```
read BLUEPRINT.md
  -> pick a target node whose `uses:` dependencies are all `done`
  -> assess complexity (Simple / Medium / Complex)  ->  set attempt budget
  -> generate an informal proof (v1) with informal_prover_codex.py
  -> if Codex's proof has 3+ distinct steps / mixed techniques / >20 lines:
        SPLIT into sub-lemma nodes, add them to BLUEPRINT.md, recurse
     else:
        keep refining the single node
  -> refine at 2^n checkpoints (attempts 2, 4, 8, 16, 32), feeding the
     verifier's issues back in
  -> when the verifier returns a passing score, mark the node `done`
  -> sync BLUEPRINT.md, move to the next dependency-satisfied target
```

## Split criteria (from blueprint_agent.md §3)

Split a node into sub-lemmas when **any** of these holds:

- the informal proof has **3 or more distinct steps**, or
- the steps require **different techniques**, or
- the informal proof is **longer than ~20 lines**.

Otherwise do not split; just refine the single node's proof.

## Complexity routing -> attempt budget (from sketch_agent.md)

| Complexity | Expected proof size | Attempt budget |
|---|---|---|
| Simple | < 5 lines | 20 |
| Medium | 5 to 20 lines | 35 |
| Complex | > 20 lines | 50 |

(`--max-attempts` on `informal_prover_codex.py` is the per-node budget. The
prover's own refine loop already does the 2^n re-attempts internally.)

## When stuck

- **Need a full attempt with auto-verification** ->
  `python3 informal_prover_codex.py --file node.md --max-attempts <budget> --log-dir informal_proofs`
- **Need strategy / how to break it down / which trick** ->
  `python3 discussion_partner_codex.py --file node.md`  (codex engine by default;
  add `--engine claude` for a second opinion)
- **Need candidate Mathlib lemma names** (key-free, run from the numina repo) ->
  `python skills/cli/leanfinder.py` / `leansearch.py` / `loogle.py`

## Each node's informal proof

Write it in the format of `informal_solution_template.md` and run it through that
file's quality gate. A node is not `done` until its proof passes the gate (which
is what the Claude-Opus verifier checks).

## CHECKLIST discipline (from common.md)

- `BLUEPRINT.md` is the single source of truth; update it the moment a node's
  status changes.
- No line numbers in node references; use `label + structural position`.
- Track version history per node (v1 -> v2 -> ...), including failed approaches,
  so refinement builds on prior insight instead of restarting.
