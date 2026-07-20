#!/usr/bin/env python3
"""Literature survey — Claude's support role, using the survey *techniques* from the
two Claude-led repos:

  * numina-lean-agent's Mathlib semantic-search CLIs (ported into ./search/):
    leansearch, leanfinder, loogle, state_search, hammer_premise  (all key-free).
  * how-many-attention-heads-xor's multi-round Claude survey style: a first broad
    pass, then an optional deeper pass on the most promising route, ending in a
    short "Actionable leads" list.

It seeds NO prior survey content (per the run's "technique only" choice): every
survey is generated fresh on the cluster. Flow for a target:

  1. Claude (cheap pass) proposes a few search queries for the target.
  2. We run the ported Mathlib search CLIs on those queries (deterministic, fast),
     collecting whatever relevant formal results exist.
  3. Claude (Opus @ max) synthesizes a survey from the target + project context +
     the search hits + its own knowledge. `--rounds 2` adds one deeper pass.

Web search is OFF by default (the live-web pass is slow and was timing out under
unattended use); pass `--web` to allow it. No API keys (Claude Max via `claude -p`).

    python3 literature_survey_claude.py --file informal_target.md \
        --context model.md --context lemmas.md --out informal_target_survey.md
"""
from __future__ import annotations  # allow `str | None` on Python 3.9

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(Path(os.environ.get("CLI_LOG_PATH", Path(__file__).parent / "cli.log")))],
)
logger = logging.getLogger(__name__)

CLAUDE_MODEL = "opus"
CLAUDE_EFFORT = "max"          # synthesis effort; query-gen uses a cheaper effort
QUERYGEN_EFFORT = "low"
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
WEB_TOOLS = "WebSearch,WebFetch"
AGENT_TIMEOUT = int(os.environ.get("INFORMAL_PROVER_TIMEOUT", "1800"))
SEARCH_DIR = os.environ.get("LEAN_SEARCH_DIR", str(Path(__file__).parent / "search"))
SEARCH_CALL_TIMEOUT = int(os.environ.get("LEAN_SEARCH_TIMEOUT", "30"))
MAX_QUERIES = 5

SURVEY_SYSTEM = (
    "You are a mathematical literature-survey assistant supporting a theorem-proving "
    "effort. You are given a research TARGET (a lemma, conjecture, or question), some "
    "project context, and the results of semantic searches over Mathlib. Produce a "
    "focused survey of the relevant KNOWN mathematics, not a proof. Specifically:\n"
    "- Name the relevant theorems, lemmas, inequalities, and named techniques, with "
    "authors / papers / approximate dates where you can.\n"
    "- State what is already established in the literature vs. what is open, and how "
    "confident you are; mark uncertain recollections as such.\n"
    "- Identify which standard proof techniques most plausibly apply to the target, "
    "and any known result the target might be a special case or corollary of.\n"
    "- Use the provided Mathlib search hits when they are relevant (cite the lemma "
    "names); ignore irrelevant hits.\n"
    "- Flag if the target (or something equivalent) appears already proved, and where, "
    "so the lead does not redo known work.\n"
    "Do NOT write a proof of the target. Be concrete and specific. End with a short "
    "'## Actionable leads' section: the 2-5 most useful known results or techniques to "
    "try first, each one line."
)

QUERYGEN_SYSTEM = (
    "You generate search queries for a Mathlib semantic-search engine. Given a research "
    "target, output ONLY a JSON array of up to 5 short query strings (mathematical "
    "concepts, theorem names, or statement fragments likely to have a Mathlib lemma), "
    "no prose, no code fences. Example: [\"sum of squares is nonnegative\", "
    "\"polynomial sign representation\"]."
)


def _read(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        logger.warning("could not read %s: %s", path, e)
        return ""


def _claude(prompt: str, system: str, effort: str, use_web: bool) -> str | None:
    cmd = [CLAUDE_BIN, "-p", "--model", CLAUDE_MODEL, "--effort", effort,
           "--output-format", "text", "--append-system-prompt", system]
    if use_web:
        cmd += ["--allowedTools", WEB_TOOLS]
    try:
        logger.info("_claude: effort=%s web=%s prompt_len=%d", effort, use_web, len(prompt))
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=AGENT_TIMEOUT)
        text = (proc.stdout or "").strip()
        if proc.returncode != 0 and not text:
            logger.error("_claude rc=%d stderr=%s", proc.returncode, proc.stderr[-400:])
            return None
        return text or None
    except subprocess.TimeoutExpired:
        logger.error("_claude timed out after %ds", AGENT_TIMEOUT)
        print(f"claude timed out after {AGENT_TIMEOUT}s", file=sys.stderr)
        return None
    except Exception as e:
        logger.exception("_claude failed: %s", e)
        return None


def _gen_queries(target: str, contexts_blob: str, use_web: bool) -> list[str]:
    prompt = "## Target\n\n" + target.strip()
    if contexts_blob:
        prompt = "## Context (background)\n\n" + contexts_blob + "\n\n" + prompt
    raw = _claude(prompt, QUERYGEN_SYSTEM, QUERYGEN_EFFORT, use_web=False)
    if not raw:
        return []
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
        return [str(q).strip() for q in arr if str(q).strip()][:MAX_QUERIES]
    except Exception:
        logger.warning("query JSON parse failed: %r", raw[:200])
        return []


def _run_search(tool: str, query: str, n: int = 4) -> str:
    """Run a ported Mathlib search CLI; return its stdout (or '' on failure)."""
    script = Path(SEARCH_DIR) / f"{tool}.py"
    if not script.exists():
        return ""
    env = dict(os.environ)
    env.setdefault("CLI_LOG_PATH", str(Path(__file__).parent / "cli.log"))
    try:
        proc = subprocess.run([sys.executable, str(script), query, "-n", str(n)],
                              capture_output=True, text=True, timeout=SEARCH_CALL_TIMEOUT, env=env)
        out = (proc.stdout or "").strip()
        return out if out and "No results" not in out and "Error" not in out[:20] else ""
    except Exception as e:
        logger.warning("search %s(%r) failed: %s", tool, query, e)
        return ""


def _gather_search_hits(queries: list[str]) -> str:
    blocks = []
    for q in queries:
        for tool in ("leansearch", "leanfinder"):
            out = _run_search(tool, q)
            if out:
                blocks.append(f"### {tool}: {q}\n```json\n{out[:2500]}\n```")
    if not blocks:
        return "(no relevant Mathlib search hits; survey from knowledge.)"
    return "\n\n".join(blocks)


def survey(target: str, contexts: list[str], rounds: int = 1, use_web: bool = False,
           out: str | None = None) -> None:
    if not target.strip():
        print("Error: No target provided.", file=sys.stderr)
        sys.exit(1)
    contexts_blob = "\n\n".join(f"### {Path(p).name}\n\n{_read(p)}" for p in contexts if _read(p))

    # 1-2: queries -> Mathlib search hits (technique from numina).
    queries = _gen_queries(target, contexts_blob, use_web)
    logger.info("survey queries: %r", queries)
    hits = _gather_search_hits(queries) if queries else "(no queries generated.)"

    # 3: round-1 synthesis (technique from how-many-attention-heads-xor).
    base = []
    if contexts_blob:
        base.append("## Project context\n\n" + contexts_blob)
    base.append("## Mathlib search hits\n\n" + hits)
    base.append("## Research target\n\n" + target.strip())
    prompt = "\n\n".join(base)
    answer = _claude(prompt, SURVEY_SYSTEM, CLAUDE_EFFORT, use_web)
    if not answer:
        print("Error: surveyor returned no response.", file=sys.stderr)
        sys.exit(1)

    # 4: optional deeper round on the most promising route.
    for r in range(2, rounds + 1):
        deepen = (prompt + "\n\n## Round " + str(r - 1) + " survey\n\n" + answer +
                  "\n\nGo one round deeper: take the single most promising route from the "
                  "survey above, dig into the specific known results/techniques it needs, "
                  "correct anything shaky, and tighten the Actionable leads. Output the "
                  "full improved survey.")
        deeper = _claude(deepen, SURVEY_SYSTEM, CLAUDE_EFFORT, use_web)
        if deeper:
            answer = deeper

    if out:
        Path(out).write_text(answer + "\n", encoding="utf-8")
        print(f"Survey written to {out}")
    else:
        print(answer)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Literature survey via Claude using numina Mathlib search + multi-round synthesis (no keys).")
    parser.add_argument("target", nargs="?", default=None, help="Target text, '-' or omit for stdin")
    parser.add_argument("--file", "-f", default=None, metavar="PATH", help="Read target from a file")
    parser.add_argument("--context", "-c", action="append", default=[], metavar="PATH",
                        help="Project file(s) to attach as background (repeatable)")
    parser.add_argument("--rounds", type=int, default=1, help="Survey rounds (1 fast, 2 deeper)")
    parser.add_argument("--web", action="store_true", help="Allow web search (slower; off by default)")
    parser.add_argument("--out", "-o", default=None, metavar="PATH", help="Write survey to a file")
    args = parser.parse_args()

    if args.file:
        target = _read(args.file)
    elif args.target is None or args.target == "-":
        target = sys.stdin.read()
    else:
        target = args.target

    survey(target, args.context, rounds=args.rounds, use_web=args.web, out=args.out)


if __name__ == "__main__":
    main()
