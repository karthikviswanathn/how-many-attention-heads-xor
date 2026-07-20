#!/usr/bin/env python3
"""Autoresearch driver — Codex is the LEAD reasoner, Claude is support.

This wrapper is plumbing only. Every research decision is made by Codex; the wrapper
just runs the long prover subprocess (which Codex cannot reliably run itself), writes
files, and git-commits, so the 10-hour run survives crashes. Per cycle:

  1. PLAN   (Codex, read-only): read GOAL + lemmas.md + BLUEPRINT.md + recent log,
            re-plan the frontier, pick ONE concrete target -> strict JSON.
  2. WRITE  the target as informal_<name>.md.
  3. SURVEY (Claude, support): literature_survey_claude.py -> fold Actionable leads in.
  4. PROVE  (Codex generates, Claude verifies): run informal_prover_codex.py;
            ESTABLISHED only on verification=="correct" (\boxed{1}).
  5. On success: Codex (read-only) formats the verified proof into a numbered
     lemmas/ file + ledger rows; the wrapper writes them. On failure: mark blocked.
  6. COMMIT a checkpoint and append a RESEARCH_LOG.md entry. Repeat until the time
     cap, the iteration cap, or Codex signals done.

Safety: all Codex calls are read-only (`-s read-only`), the same safe mode the other
tools use; the wrapper never force-pushes, never deletes files it did not create, and
never touches `head-complexity/` or any `.lean`. INFORMAL ONLY.
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
os.chdir(REPO)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(REPO / "autoresearch.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("autoresearch")

# --- config (env-overridable) ----------------------------------------------
CODEX_BIN = os.environ.get("CODEX_BIN", "codex")
CODEX_EFFORT = os.environ.get("CODEX_EFFORT", "xhigh")
AGENT_TIMEOUT = int(os.environ.get("INFORMAL_PROVER_TIMEOUT", "1800"))
MAX_HOURS = float(os.environ.get("AUTORESEARCH_HOURS", "10"))
MAX_ITERS = int(os.environ.get("AUTORESEARCH_MAX_ITERS", "120"))
ATTEMPTS = {"simple": 20, "medium": 35, "complex": 50}
ATTEMPT_CAP = int(os.environ.get("AUTORESEARCH_ATTEMPT_CAP", "0"))  # >0 caps attempts (testing)
LEMMA_DIR = REPO / "lemmas" / "01_foundations_and_normal_form"
PY = sys.executable

STYLE = (
    "Markdown style (AGENTS.md): LaTeX math in $...$ / $$...$$ (never backticks), "
    "`#` title then `## Statement` / `## Proof` / `## Consequence`, sub-lemmas as "
    "`### Lemma k. Name`, run-in `**Proof.**`, `\\blacksquare` to close. NO em dashes. "
    "Natural-language math only, never Lean."
)


# --- helpers ----------------------------------------------------------------
def hours_left(t0: float) -> float:
    return MAX_HOURS - (time.time() - t0) / 3600.0


def codex(prompt: str) -> str | None:
    """Read-only Codex call (planning / formatting). Returns final message text."""
    out_path = None
    try:
        fd, out_path = tempfile.mkstemp(prefix="ar_codex_", suffix=".txt")
        os.close(fd)
        cmd = [CODEX_BIN, "exec", prompt, "-c", f'model_reasoning_effort="{CODEX_EFFORT}"',
               "-s", "read-only", "-C", str(REPO), "-o", out_path]
        proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=AGENT_TIMEOUT)
        text = ""
        try:
            text = Path(out_path).read_text().strip()
        except OSError:
            pass
        if not text:
            text = (proc.stdout or "").strip()
        return text or None
    except subprocess.TimeoutExpired:
        logger.error("codex timed out after %ds", AGENT_TIMEOUT)
        return None
    except Exception as e:
        logger.exception("codex failed: %s", e)
        return None
    finally:
        if out_path:
            try:
                os.unlink(out_path)
            except OSError:
                pass


def extract_json(text: str | None) -> dict | None:
    """Pull the last balanced {...} object out of a model reply and parse it."""
    if not text:
        return None
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidates = []
    if fence:
        candidates.append(fence.group(1))
    # also scan for balanced top-level objects
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                candidates.append(text[start:i + 1])
    for cand in reversed(candidates):
        try:
            return json.loads(cand)
        except Exception:
            continue
    return None


def read(path: Path, tail: int | None = None) -> str:
    try:
        s = path.read_text(encoding="utf-8")
        if tail and len(s) > tail:
            s = "...\n" + s[-tail:]
        return s
    except OSError:
        return ""


def git(*args: str) -> None:
    try:
        subprocess.run(["git", *args], cwd=str(REPO), capture_output=True, text=True, timeout=120)
    except Exception as e:
        logger.warning("git %s failed: %s", args, e)


def commit(msg: str) -> None:
    git("add", "-A")
    git("commit", "-m", msg)


def log_entry(text: str) -> None:
    try:
        with open(REPO / "RESEARCH_LOG.md", "a", encoding="utf-8") as f:
            f.write("\n" + text.rstrip() + "\n")
    except OSError as e:
        logger.warning("research log write failed: %s", e)


def next_lemma_number() -> int:
    nums = []
    for p in LEMMA_DIR.glob("*.md"):
        m = re.match(r"(\d+)", p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 13


# --- pipeline steps ---------------------------------------------------------
def plan(t0: float, recent_fail: int) -> dict | None:
    goal = read(REPO / "GOAL.md")
    lemmas = read(REPO / "lemmas.md")
    blueprint = read(REPO / "BLUEPRINT.md")
    rlog = read(REPO / "RESEARCH_LOG.md", tail=4000)
    decompose = ("\nNOTE: the last %d targets did not verify. Prefer DECOMPOSING the "
                 "most promising blocked target into a smaller, self-contained sub-lemma "
                 "(a leaf) this time." % recent_fail) if recent_fail >= 2 else ""
    prompt = f"""You are Codex, the LEAD autonomous researcher. Below are your standing
instructions and the current state. Re-plan the open frontier from what is proved, then
pick the SINGLE next concrete, provable target to attempt now (a new lemma, a tighter
general bound, a separation, or a new invariant). Prefer a leaf whose dependencies are
already proved. {decompose}

Reply with ONLY a JSON object (no other text), schema:
{{
  "done": <true only if no productive target remains>,
  "name": "<short snake_case id, e.g. dnf_subcube_upper_bound>",
  "title": "<human-readable lemma title>",
  "statement_md": "<the precise statement to prove, as markdown math; self-contained, "
                  "include any needed definitions from model.md>",
  "complexity": "simple|medium|complex",
  "rationale": "<one or two sentences: why this target, what it unlocks>",
  "blueprint_update_md": "<optional short markdown to append to BLUEPRINT.md recording "
                         "this target/decomposition; empty string if none>"
}}

=== GOAL.md ===
{goal}

=== lemmas.md (proved ledger) ===
{lemmas}

=== BLUEPRINT.md (plan/frontier) ===
{blueprint}

=== RESEARCH_LOG.md (recent tail) ===
{rlog}
"""
    spec = extract_json(codex(prompt))
    if not spec or not isinstance(spec, dict):
        logger.warning("plan: no parseable JSON spec")
        return None
    return spec


def write_target(spec: dict) -> Path:
    name = re.sub(r"[^a-z0-9_]+", "_", spec.get("name", "target").lower()).strip("_") or "target"
    spec["name"] = name
    path = REPO / f"informal_{name}.md"
    body = [f"# {spec.get('title', name)}", "",
            spec.get("statement_md", "").strip(), "",
            "## Context", "",
            "This is an informal (natural-language) target in the one-layer attention",
            "head-complexity project; see `model.md` for the model and `lemmas.md` for the",
            "proved stack. Give a fully rigorous, self-contained proof."]
    path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return path


def add_survey(target_path: Path, name: str) -> None:
    out = REPO / f"informal_{name}_survey.md"
    try:
        subprocess.run(
            [PY, str(REPO / "literature_survey_claude.py"), "--file", str(target_path),
             "--context", "model.md", "--context", "lemmas.md", "--rounds", "1",
             "--out", str(out)],
            cwd=str(REPO), capture_output=True, text=True, timeout=AGENT_TIMEOUT)
    except Exception as e:
        logger.warning("survey failed: %s", e)
        return
    survey = read(out)
    if not survey:
        return
    m = re.search(r"##\s*Actionable leads.*", survey, re.DOTALL | re.IGNORECASE)
    leads = m.group(0) if m else survey[-1500:]
    with open(target_path, "a", encoding="utf-8") as f:
        f.write("\n## Known results to build on (from literature survey)\n\n" + leads.strip() + "\n")


def prove(target_path: Path, complexity: str) -> dict:
    n = ATTEMPTS.get(complexity, 35)
    if ATTEMPT_CAP:
        n = min(n, ATTEMPT_CAP)
    try:
        proc = subprocess.run(
            [PY, str(REPO / "informal_prover_codex.py"), "--file", str(target_path),
             "--max-attempts", str(n), "--log-dir", str(REPO / "informal_proofs")],
            cwd=str(REPO), capture_output=True, text=True, timeout=AGENT_TIMEOUT * (n + 1))
        for line in reversed((proc.stdout or "").strip().splitlines()):
            line = line.strip()
            if line.startswith("{"):
                try:
                    return json.loads(line)
                except Exception:
                    continue
        logger.warning("prove: no JSON result; stderr=%s", (proc.stderr or "")[-300:])
    except subprocess.TimeoutExpired:
        logger.error("prove timed out")
    except Exception as e:
        logger.exception("prove failed: %s", e)
    return {"solution": None, "verification": "incorrect (no result)", "attempts": n}


def write_lemma(spec: dict, solution: str) -> str | None:
    num = next_lemma_number()
    prompt = f"""You are Codex. A proof of the target below was VERIFIED by the Claude
oracle (\\boxed{{1}}). Format it as the next numbered lemma file for this repo.
{STYLE}

Reply with ONLY a JSON object:
{{
  "filename": "{num:03d}_{spec['name']}.md",
  "lemma_md": "<the full lemma file content in the required style>",
  "lemmas_md_row": "<one markdown line to append to lemmas.md recording this lemma, "
                   "matching the existing table/list format>",
  "blueprint_status_md": "<short markdown marking this node done in BLUEPRINT.md, with "
                         "dependency edges; empty string if not applicable>"
}}

=== Target ===
{read(REPO / ("informal_" + spec['name'] + ".md"))}

=== Verified proof ===
{solution}
"""
    out = extract_json(codex(prompt))
    if not out:
        logger.warning("write_lemma: no JSON")
        return None
    fname = out.get("filename") or f"{num:03d}_{spec['name']}.md"
    fname = os.path.basename(fname)  # never escape the dir
    dest = LEMMA_DIR / fname
    if dest.exists():
        dest = LEMMA_DIR / f"{num:03d}_{spec['name']}.md"
    try:
        dest.write_text((out.get("lemma_md") or solution).rstrip() + "\n", encoding="utf-8")
    except OSError as e:
        logger.warning("lemma write failed: %s", e)
        return None
    row = (out.get("lemmas_md_row") or "").strip()
    if row:
        with open(REPO / "lemmas.md", "a", encoding="utf-8") as f:
            f.write("\n" + row + "\n")
    bp = (out.get("blueprint_status_md") or "").strip()
    if bp:
        with open(REPO / "BLUEPRINT.md", "a", encoding="utf-8") as f:
            f.write("\n" + bp + "\n")
    return str(dest.relative_to(REPO))


# --- main loop --------------------------------------------------------------
def main() -> None:
    t0 = time.time()
    logger.info("autoresearch start: cap=%.1fh max_iters=%d repo=%s", MAX_HOURS, MAX_ITERS, REPO)
    recent_fail = 0
    plan_fail = 0
    proved = 0
    for it in range(1, MAX_ITERS + 1):
        if hours_left(t0) <= 0.1:
            logger.info("time cap reached; stopping")
            break
        logger.info("=== iteration %d (%.2fh left, %d proved) ===", it, hours_left(t0), proved)
        try:
            spec = plan(t0, recent_fail)
            if not spec:
                plan_fail += 1
                logger.warning("planning produced no target (streak %d)", plan_fail)
                if plan_fail >= 5:
                    log_entry(f"### Iter {it}: planning failed {plan_fail}x in a row "
                              f"(agent/parse problem). Stopping to avoid a spin.")
                    break
                time.sleep(10)
                continue
            plan_fail = 0
            if spec.get("done"):
                logger.info("plan signaled done")
                log_entry(f"### Iter {it}: lead signaled frontier exhausted. Stopping.")
                break
            name = spec.get("name", "target")
            bp = (spec.get("blueprint_update_md") or "").strip()
            if bp:
                with open(REPO / "BLUEPRINT.md", "a", encoding="utf-8") as f:
                    f.write("\n" + bp + "\n")
            target_path = write_target(spec)
            name = spec["name"]
            add_survey(target_path, name)
            result = prove(target_path, spec.get("complexity", "medium"))
            verified = result.get("verification") == "correct"
            if verified and result.get("solution"):
                rel = write_lemma(spec, result["solution"])
                proved += 1
                recent_fail = 0
                commit(f"lemma: {spec.get('title', name)} (verified, autoresearch iter {it})")
                log_entry(f"### Iter {it}: PROVED `{name}` -> {rel}. "
                          f"{spec.get('rationale','').strip()} (attempts={result.get('attempts')})")
                logger.info("iter %d PROVED %s", it, name)
            else:
                recent_fail += 1
                commit(f"checkpoint: {name} not verified (autoresearch iter {it})")
                log_entry(f"### Iter {it}: BLOCKED `{name}` after {result.get('attempts')} attempts. "
                          f"{spec.get('rationale','').strip()} Next: decompose or switch.")
                logger.info("iter %d BLOCKED %s", it, name)
        except Exception as e:
            logger.exception("iteration %d crashed: %s", it, e)
            log_entry(f"### Iter {it}: iteration error: {e}. Continuing.")
            try:
                commit(f"checkpoint: iter {it} recovered from error")
            except Exception:
                pass
            continue

    log_entry(f"\n## Autoresearch run summary\n\nFinished after iteration loop: "
              f"{proved} new lemma(s) verified this run; {hours_left(t0):.2f}h of the "
              f"{MAX_HOURS:.0f}h budget remaining. See lemmas.md / BLUEPRINT.md for the "
              f"updated state.")
    commit("autoresearch: final checkpoint + run summary")
    logger.info("autoresearch done: %d proved", proved)


if __name__ == "__main__":
    main()
