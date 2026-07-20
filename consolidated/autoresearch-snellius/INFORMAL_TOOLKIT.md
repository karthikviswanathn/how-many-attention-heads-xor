# Informal Theorem-Proving Toolkit

Subscription-only port of numina-lean-agent's informal (pre-Lean) stage. Every
LLM call goes through the Codex CLI (`codex exec`, Codex plan) or Claude Code
headless (`claude -p`, Max plan). **No `GEMINI_API_KEY` / `OPENAI_API_KEY` /
`ANTHROPIC_API_KEY` required.**

## Roles: Codex leads, Claude supports

- **Codex = lead.** It drives the research loop (plan, pick target, draft proofs,
  write up verified lemmas) and is the generator inside the prover. See `GOAL.md`
  for the autonomous-run instructions and `AGENTS.md` for its lead brief.
- **Claude = support**, two roles only: (1) **literature survey**
  (`literature_survey_claude.py`, web-enabled) and (2) **verification** (the strict
  `\boxed` oracle inside `informal_prover_codex.py`, no tools).

## Tools

| File | What it does | Engines |
|---|---|---|
| `autoresearch.py` | The unattended driver loop: Codex plans + formats lemmas, Claude surveys + verifies, the wrapper runs the prover and commits. Launch via `run_autoresearch.sh`. | wrapper; Codex (read-only) lead + Claude support |
| `informal_prover_codex.py` | Full loop: generate → verify (\boxed score) → refine → repeat. Outputs JSON `{solution, verification, attempts}`. | gen/refine = Codex (xhigh, lead); verify = Claude Opus (max, support) |
| `literature_survey_claude.py` | Fresh literature survey for a target using the *techniques* from both Claude-led repos: Claude proposes queries → runs the ported Mathlib search CLIs in `search/` → multi-round synthesis (`--rounds`). Web off by default (`--web` to enable). | Claude Opus (max, support) + `search/` CLIs |
| `search/*.py` | Ported key-free Mathlib semantic-search CLIs from numina-lean-agent: `leansearch`, `leanfinder`, `loogle`, `state_search`, `hammer_premise`. | public search APIs, no keys |
| `discussion_partner_codex.py` | Single-pass strategy / brainstorm (no verify loop). Outlines, candidate lemmas, pitfalls. | `--engine codex` (default) or `--engine claude` |

## Docs / templates

| File | Purpose |
|---|---|
| `informal_solution_template.md` | Structured format for each node's informal proof + the quality gate the verifier enforces. |
| `informal_decomposition.md` | How to break a hard theorem into a sub-lemma dependency graph (split criteria, complexity→budget, 2ⁿ refine checkpoints). |
| `BLUEPRINT.md` | The dependency-graph single source of truth. One node per lemma; fill and keep in sync. |

## Typical session

```bash
# 0. Sketch the decomposition into BLUEPRINT.md (consult the brainstorm tool freely)
python3 discussion_partner_codex.py --file thm_main.md

# 0b. Before a hard target, have Claude survey what's already known (web-enabled)
python3 literature_survey_claude.py --file informal_lem_sub1.md \
  --context model.md --context lemmas.md --out informal_lem_sub1_survey.md

# 1. For each leaf node whose `uses` deps are done, attempt a verified proof
#    (fold the survey's "Actionable leads" into the target file first)
python3 informal_prover_codex.py --file informal_lem_sub1.md \
  --max-attempts 20 --log-dir informal_proofs

# 2. Write the accepted proof into the template format, run its quality gate,
#    mark the node `done` in BLUEPRINT.md, move up the graph.
```

## What is NOT here (and why)

These upstream pieces are Lean-formalization-stage, not informal, so they were
deliberately left out: `code_golf` / golfer (optimizes finished Lean proofs),
the hard/medium/evaluation/complete-file mode prompts (Lean coordinator / proof
agents), and `sketch_agent` / `proof_agent` (informal → Lean → tactics). The Lean
**search** CLIs (`leanfinder`, `leansearch`, `loogle`, ...) are already key-free
and are useful here only for populating the "Relevant Mathlib Lemmas" field;
run them in place from the numina-lean-agent repo rather than re-implementing.

## Config

All engine knobs live at the top of each `*_codex.py` (`CODEX_EFFORT="xhigh"`,
`CLAUDE_MODEL="opus"`, `CLAUDE_EFFORT="max"`). Override the binaries with
`CODEX_BIN` / `CLAUDE_BIN`, or the per-call timeout with
`INFORMAL_PROVER_TIMEOUT`. Per the project rule, any numpy/torch the agents end
up running goes through `conda run -n llmenv` (see `AGENTS.md`).
