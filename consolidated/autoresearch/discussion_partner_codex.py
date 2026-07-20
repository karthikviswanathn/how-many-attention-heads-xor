#!/usr/bin/env python3
"""Discussion partner — subscription port of numina-lean-agent's discussion_partner.py.

Free-form strategy / brainstorm discussion about a proof, a stuck point, or a math
problem. Unlike informal_prover_codex.py (which runs a full generate -> verify ->
refine loop), this is a SINGLE pass: send the question to one engine, print its answer.

    --engine codex   (default)  ->  codex exec   (your Codex plan)
    --engine claude             ->  claude -p    (your Max plan, Opus @ max effort)

No API keys needed (no Gemini/GPT/Anthropic). Same arg surface as the original:
positional question, --file, or stdin.
"""
from __future__ import annotations  # allow `str | None` annotations on Python 3.9

import argparse
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(Path(os.environ.get("CLI_LOG_PATH", Path(__file__).parent / "cli.log")))],
)
logger = logging.getLogger(__name__)

# Agent configuration (mirrors informal_prover_codex.py).
CODEX_EFFORT = "xhigh"
CLAUDE_MODEL = "opus"
CLAUDE_EFFORT = "max"        # no fast mode (premium-priced)
CODEX_BIN = os.environ.get("CODEX_BIN", "codex")
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
AGENT_TIMEOUT = int(os.environ.get("INFORMAL_PROVER_TIMEOUT", "1800"))

DISCUSS_SYSTEM = (
    "You are a mathematical proof-strategy discussion partner. The user is stuck or "
    "wants high-level guidance, not a fully written-out solution. Give a clear strategy: "
    "the key idea(s), how to decompose the problem into sub-lemmas if it is large, "
    "specific candidate Mathlib lemma names if any come to mind, and the likely pitfalls. "
    "Do not use any tools, do not read or edit files, do not run commands; reason from the "
    "prompt and reply with prose."
)


def _call_codex(prompt: str) -> str | None:
    out_path = None
    try:
        fd, out_path = tempfile.mkstemp(prefix="codex_discuss_", suffix=".txt")
        os.close(fd)
        cmd = [CODEX_BIN, "exec", prompt,
               "-c", f'model_reasoning_effort="{CODEX_EFFORT}"',
               "-s", "read-only",
               "--skip-git-repo-check",
               "-o", out_path]
        logger.info("_call_codex: discuss (effort=%s) prompt_len=%d", CODEX_EFFORT, len(prompt))
        proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=AGENT_TIMEOUT)
        text = ""
        try:
            text = Path(out_path).read_text().strip()
        except OSError:
            pass
        if not text:
            text = (proc.stdout or "").strip()
        if proc.returncode != 0 and not text:
            logger.error("_call_codex failed rc=%d stderr=%s", proc.returncode, proc.stderr[-500:])
            print(f"codex error (rc={proc.returncode}): {proc.stderr[-300:]}", file=sys.stderr)
            return None
        return text or None
    except subprocess.TimeoutExpired:
        print(f"codex timed out after {AGENT_TIMEOUT}s", file=sys.stderr)
        return None
    except Exception as e:
        logger.exception("_call_codex failed: %s", e)
        print(f"codex error: {e}", file=sys.stderr)
        return None
    finally:
        if out_path:
            try:
                os.unlink(out_path)
            except OSError:
                pass


def _call_claude(prompt: str) -> str | None:
    try:
        cmd = [CLAUDE_BIN, "-p",
               "--model", CLAUDE_MODEL,
               "--effort", CLAUDE_EFFORT,
               "--output-format", "text",
               "--append-system-prompt", DISCUSS_SYSTEM]
        logger.info("_call_claude: discuss (model=%s effort=%s) prompt_len=%d", CLAUDE_MODEL, CLAUDE_EFFORT, len(prompt))
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=AGENT_TIMEOUT)
        text = (proc.stdout or "").strip()
        if proc.returncode != 0 and not text:
            logger.error("_call_claude failed rc=%d stderr=%s", proc.returncode, proc.stderr[-500:])
            print(f"claude error (rc={proc.returncode}): {proc.stderr[-300:]}", file=sys.stderr)
            return None
        return text or None
    except subprocess.TimeoutExpired:
        print(f"claude timed out after {AGENT_TIMEOUT}s", file=sys.stderr)
        return None
    except Exception as e:
        logger.exception("_call_claude failed: %s", e)
        print(f"claude error: {e}", file=sys.stderr)
        return None


def discuss(question: str, engine: str = "codex") -> None:
    if not question.strip():
        print("Error: No question provided.", file=sys.stderr)
        sys.exit(1)
    logger.info("discuss: engine=%s question_len=%d", engine, len(question))
    if engine == "codex":
        # Wrap the question so Codex stays in strategy mode (it sees this as the task).
        prompt = DISCUSS_SYSTEM + "\n\n---\n\n" + question
        answer = _call_codex(prompt)
    elif engine == "claude":
        answer = _call_claude(question)
    else:
        print(f"Error: engine must be 'codex' or 'claude', got '{engine}'", file=sys.stderr)
        sys.exit(1)
    if not answer:
        print("Error: engine returned no response.", file=sys.stderr)
        sys.exit(1)
    print(answer)


def main() -> None:
    parser = argparse.ArgumentParser(description="Discuss proof strategy with Codex/Claude (subscription-only).")
    parser.add_argument("question", nargs="?", default=None, help="Question text, '-' or omit to read from stdin")
    parser.add_argument("--file", "-f", default=None, metavar="PATH", help="Read question from a file (avoids shell escaping)")
    parser.add_argument("--engine", choices=["codex", "claude"], default="codex", help="Which engine answers (default codex)")
    args = parser.parse_args()

    if args.file:
        question = Path(args.file).read_text(encoding="utf-8")
    elif args.question is None or args.question == "-":
        question = sys.stdin.read()
    else:
        question = args.question
    discuss(question, args.engine)


if __name__ == "__main__":
    main()
