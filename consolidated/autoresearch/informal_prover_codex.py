#!/usr/bin/env python3
"""Informal math prover — same workflow as numina-lean-agent's informal_prover.py,
with the agents swapped to run entirely on subscriptions (no API credits):

    generate -> Codex      (`codex exec`,  your Codex plan)
    verify   -> Claude     (`claude -p`,   your Max plan, Opus @ max)
    refine   -> Codex      (`codex exec`,  your Codex plan)

The loop is unchanged from the original: generate a solution, score it with the
verifier (which ends its evaluation with \\boxed{0|0.5|1}); if the score is < 1,
feed the verifier's issues back to the generator for a revised solution and
re-verify, up to --max-attempts. Accepted iff the verifier returns \\boxed{1}.

Prompts (SOLUTION_PROMPT / VERIFY_PROMPT / REFINEMENT_PROMPT) are copied verbatim
from numina-lean-agent/skills/cli/informal_prover.py so behavior matches.
"""
from __future__ import annotations  # allow `str | None` annotations on Python 3.9

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(Path(os.environ.get("CLI_LOG_PATH", Path(__file__).parent / "cli.log")))],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Agent configuration — the only place to tune which engine/effort each role uses.
# ---------------------------------------------------------------------------
CODEX_MODEL = None          # None -> use your codex default (latest). Or e.g. "gpt-5.2-codex".
CODEX_EFFORT = "xhigh"      # model_reasoning_effort
CLAUDE_MODEL = "opus"       # alias -> latest Opus (4.8) on your Max plan
CLAUDE_EFFORT = "max"       # NO fast mode (premium-priced); standard speed.
CODEX_BIN = os.environ.get("CODEX_BIN", "codex")
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
AGENT_TIMEOUT = int(os.environ.get("INFORMAL_PROVER_TIMEOUT", "1800"))  # seconds per agent call

# ---------------------------------------------------------------------------
# Prompts — verbatim from numina-lean-agent/skills/cli/informal_prover.py
# ---------------------------------------------------------------------------
SOLUTION_PROMPT = """You are a Formal Logic Expert and Mathematical Proof Engine. Your goal is to derive proofs that are rigorously structured, formalization-ready, and devoid of ambiguity.

Core Constraints:

- Purely Algebraic/Symbolic: Do NOT use geometric intuition, visual symmetry, or graphical interpretations as proof. All geometric concepts must be translated into their precise algebraic or analytic definitions.

- Atomic Steps: Decompose reasoning into the smallest possible logical units. Do not combine multiple deductive steps into one.

- No Hand-waving: Forbidden phrases include 'obviously,' 'it is clear that,' 'by inspection,' or 'intuitively.'

Instructions:

- Definitions: Explicitly state all variable types, definitions, and assumptions at the start.

- Step-by-Step Derivation: Number every step (1, 2, 3...).

- Explicit Justification: For EACH step, you must explicitly state the rule of inference, algebraic identity, axiom, or theorem used (e.g., "Distributive Property," "Triangle Inequality," "Definition of Continuity").

- Formal Structure: Present the proof in a format that could easily be translated into a proof assistant language (like Lean or Coq).

- Calculations: Show every intermediate stage of simplification or substitution. Do not skip algebraic manipulation steps.

Problem Statement: {problem}"""

VERIFY_PROMPT = """Your task is to evaluate the quality of a solution to a problem. The problem may ask for a proof of a statement, or ask for an answer. If finding an answer is required, the solution should present the answer, and it should also be a rigorous proof of that answer being valid.

Please evaluate the solution and score it according to the following criteria:

- If the solution is completely correct, with all steps executed properly and clearly demonstrated, then the score is 1

- If the solution is generally correct, but with some details omitted or minor errors, then the score is 0.5

- If the solution does not actually address the required problem, contains fatal errors, or has severe omissions, then the score is 0

- Additionally, referencing anything from any paper does not save the need to prove the reference. It's okay IF AND ONLY IF the solution also presents a valid proof of the reference argument(s); otherwise, if the solution omits the proof or if the proof provided is not completely correct, the solution should be scored according to the criteria above, and definitely not with a score of 1

Please carefully reason out and analyze the quality of the solution below, and in your final response present a detailed evaluation of the solution's quality followed by your score.

Therefore, your response should be in the following format:

Here is my evaluation of the solution:

[Your evaluation here. You are required to present in detail the key steps of the solution or the steps for which you had doubts regarding their correctness, and explicitly analyze whether each step is accurate: for correct steps, explain why you initially doubted their correctness and why they are indeed correct; for erroneous steps, explain the reason for the error and the impact of that error on the solution.]

Based on my evaluation, the final overall score should be: \\boxed{{...}}

[where ... should be the final overall score (0, 0.5, or 1, and nothing else) based on the above criteria]

---

Here is your task input:

## Problem
{problem}

## Solution
{student_solution}"""

REFINEMENT_PROMPT = """You are given a mathematical problem, an existing solution, and a set of issues we found in that solution after careful review.

Your task is to produce a **revised solution** that is more complete, rigorous, and clearly justified.

---

### Problem
{problem}

---

### Previous Solution
{solution}

---

### Issues We Found
{issues}

---

### Instructions

- Carefully read each reported issue and decide whether it is **valid** or may be due to a **misunderstanding of the original argument**.
- If you **agree** that an issue is valid:
  - Revise the solution to fix it.
  - Add missing steps, clarify logical transitions, or strengthen rigor as needed.
- If you **disagree** with an issue:
  - Keep the original reasoning if it is correct.
  - Add **explicit explanations or clarifications** to prevent future misunderstandings.
- Do **not** simply restate the issues.
- The final solution should be:
  - Self-contained
  - Logically coherent
  - Mathematically rigorous
  - Easy to follow for a careful reader

---

### Output Format

Provide **only** the revised solution below.

### Revised Solution
"""

VERIFY_SYSTEM = (
    "You are acting as a strict mathematical proof verifier. Do not use any tools, "
    "do not read or edit files, and do not run commands. Read the problem and solution "
    "given in the prompt and reply with your written evaluation followed by the final "
    "score in \\boxed{...}. Output nothing else."
)


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------
def _call_codex(prompt: str) -> str | None:
    """Generate / refine via `codex exec` (Codex plan). Returns the final message text."""
    out_file = None
    try:
        fd, out_path = tempfile.mkstemp(prefix="codex_out_", suffix=".txt")
        os.close(fd)
        out_file = out_path
        cmd = [CODEX_BIN, "exec", prompt,
               "-c", f'model_reasoning_effort="{CODEX_EFFORT}"',
               "-s", "read-only",            # pure reasoning; no writes, no approval prompts
               "--skip-git-repo-check",
               "-o", out_path]
        if CODEX_MODEL:
            cmd[3:3] = ["-m", CODEX_MODEL]
        logger.info("_call_codex: exec (effort=%s model=%s) prompt_len=%d",
                    CODEX_EFFORT, CODEX_MODEL or "default", len(prompt))
        proc = subprocess.run(
            cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=AGENT_TIMEOUT
        )
        text = ""
        try:
            text = Path(out_path).read_text().strip()
        except OSError:
            pass
        if not text:                         # fall back to stdout if -o produced nothing
            text = (proc.stdout or "").strip()
        if proc.returncode != 0 and not text:
            logger.error("_call_codex failed rc=%d stderr=%s", proc.returncode, proc.stderr[-500:])
            print(f"codex error (rc={proc.returncode}): {proc.stderr[-300:]}", file=sys.stderr)
            return None
        logger.info("_call_codex: produced %d chars", len(text))
        return text or None
    except subprocess.TimeoutExpired:
        logger.error("_call_codex timed out after %ds", AGENT_TIMEOUT)
        print(f"codex timed out after {AGENT_TIMEOUT}s", file=sys.stderr)
        return None
    except Exception as e:
        logger.exception("_call_codex failed: %s", e)
        print(f"codex error: {e}", file=sys.stderr)
        return None
    finally:
        if out_file:
            try:
                os.unlink(out_file)
            except OSError:
                pass


def _call_claude(prompt: str) -> str | None:
    """Verify via `claude -p` (Max plan, Opus @ max). Returns the evaluation text."""
    try:
        cmd = [CLAUDE_BIN, "-p",
               "--model", CLAUDE_MODEL,
               "--effort", CLAUDE_EFFORT,
               "--output-format", "text",
               "--append-system-prompt", VERIFY_SYSTEM]
        logger.info("_call_claude: verify (model=%s effort=%s) prompt_len=%d",
                    CLAUDE_MODEL, CLAUDE_EFFORT, len(prompt))
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=AGENT_TIMEOUT
        )
        text = (proc.stdout or "").strip()
        if proc.returncode != 0 and not text:
            logger.error("_call_claude failed rc=%d stderr=%s", proc.returncode, proc.stderr[-500:])
            print(f"claude error (rc={proc.returncode}): {proc.stderr[-300:]}", file=sys.stderr)
            return None
        logger.info("_call_claude: produced %d chars", len(text))
        return text or None
    except subprocess.TimeoutExpired:
        logger.error("_call_claude timed out after %ds", AGENT_TIMEOUT)
        print(f"claude timed out after {AGENT_TIMEOUT}s", file=sys.stderr)
        return None
    except Exception as e:
        logger.exception("_call_claude failed: %s", e)
        print(f"claude error: {e}", file=sys.stderr)
        return None


def _extract_score(verification: str | None) -> str | None:
    if not verification:
        return None
    match = re.search(r"\\boxed\{(.*?)\}", verification)
    return match.group(1).strip() if match else None


def _verify(problem: str, solution: str) -> tuple[bool, str | None, str | None]:
    """Single Claude-Opus verifier (replaces the old 3-model panel).

    Returns (accepted, issues, verification_text). Accepted iff score == "1";
    on a lower score the full evaluation text becomes the "issues" fed to refine.
    """
    verify_prompt = VERIFY_PROMPT.format(problem=problem, student_solution=solution)
    text = _call_claude(verify_prompt)
    score = _extract_score(text)
    logger.info("verify score=%s", score)
    if not text or score is None:
        logger.warning("verifier produced no parseable score; treating as not accepted")
        return False, (text or "Verifier produced no score."), text
    if score == "1":
        return True, None, text
    return False, text, text


# ---------------------------------------------------------------------------
# Workflow — identical structure to informal_prover.py's prove()
# ---------------------------------------------------------------------------
def prove(math_problem: str, max_attempts: int = 10, log_dir: str | None = None) -> None:
    logger.info("prove called: max_attempts=%d problem_len=%d", max_attempts, len(math_problem))
    solution: str | None = None
    issues: str | None = None
    last_verification: str | None = None

    for attempt in range(1, max_attempts + 1):
        # Generate (attempt 1) or refine (attempt > 1) — both via Codex.
        if attempt == 1:
            prompt = SOLUTION_PROMPT.format(problem=math_problem)
            solution = _call_codex(prompt)
        else:
            if not issues:
                break
            prompt = REFINEMENT_PROMPT.format(
                problem=math_problem, solution=solution, issues=issues
            )
            solution = _call_codex(prompt)

        if not solution:
            if attempt == max_attempts:
                print(json.dumps({"solution": None, "verification": "Failed to generate solution",
                                  "attempts": attempt}))
                return
            continue

        # Verify — single Claude-Opus verifier.
        accepted, issues, last_verification = _verify(math_problem, solution)
        logger.info("attempt %d: accepted=%s", attempt, accepted)

        if accepted:
            result = {"solution": solution, "verification": "correct", "attempts": attempt}
            _log(log_dir, math_problem, solution, "correct")
            print(json.dumps(result))
            return

    # Exhausted attempts (or no issues to refine) without acceptance.
    verification = "incorrect\n" + (last_verification or "")
    _log(log_dir, math_problem, solution or "", verification)
    print(json.dumps({"solution": solution, "verification": verification, "attempts": max_attempts}))


def _log(log_dir: str | None, problem: str, solution: str, verification: str) -> None:
    if not log_dir:
        return
    try:
        d = Path(log_dir)
        d.mkdir(parents=True, exist_ok=True)
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "problem": problem,
               "solution": solution, "verification": verification}
        with open(d / "results.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception as e:
        logger.warning("failed to write log: %s", e)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Informal math prover: Codex generates/refines, Claude Opus verifies (subscription-only)."
    )
    parser.add_argument("problem", nargs="?", help="Math problem text, '-' or omit to read from stdin")
    parser.add_argument("--file", "-f", help="Read problem from a file (avoids shell escaping)")
    parser.add_argument("--max-attempts", type=int, default=10, help="Max generate+verify+refine cycles")
    parser.add_argument("--log-dir", help="Directory to persist results as JSONL")
    args = parser.parse_args()

    if args.file:
        problem = Path(args.file).read_text()
    elif args.problem and args.problem != "-":
        problem = args.problem
    else:
        problem = sys.stdin.read()

    problem = problem.strip()
    if not problem:
        print("Error: empty problem", file=sys.stderr)
        sys.exit(1)

    prove(problem, max_attempts=args.max_attempts, log_dir=args.log_dir)


if __name__ == "__main__":
    main()
