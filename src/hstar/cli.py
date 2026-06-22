from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from .config import SearchConfig, TrainingConfig
from .search import run_representative_search


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Enumerate safe symmetry representatives and estimate H*(f)."
    )
    parser.add_argument("--n", type=int, required=True, help="Number of input bits.")
    parser.add_argument(
        "--max-heads",
        type=int,
        required=True,
        help="Maximum number of heads to try in the experimental search.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on the number of representatives to process.",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="Inclusive start index into the representative list.",
    )
    parser.add_argument(
        "--end-index",
        type=int,
        default=None,
        help="Exclusive end index into the representative list.",
    )
    parser.add_argument("--steps", type=int, default=1500)
    parser.add_argument("--lr", type=float, default=3e-2)
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--d-model", type=int, default=32)
    parser.add_argument("--d-head", type=int, default=32)
    parser.add_argument(
        "--device",
        choices=("auto", "cpu", "cuda", "mps"),
        default="auto",
        help="Torch device for the experimental attention search.",
    )
    parser.add_argument(
        "--no-stop-on-perfect-accuracy",
        action="store_true",
        help="Keep optimizing after perfect classification until the loss criterion is met.",
    )
    parser.add_argument(
        "--robust",
        action="store_true",
        help="Run a stronger second-pass search to reduce restart sensitivity.",
    )
    parser.add_argument(
        "--robust-steps-multiplier",
        type=int,
        default=4,
        help="Multiplier for the second-pass training steps.",
    )
    parser.add_argument(
        "--robust-restarts-multiplier",
        type=int,
        default=4,
        help="Multiplier for the second-pass restart count.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON path for the result payload.",
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=None,
        help="If set with --output, rewrite the JSON file every N processed representatives.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=5,
        help="Print progress and ETA every N processed representatives.",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable progress and ETA reporting.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print training progress for each restart.",
    )
    return parser


def _format_duration(seconds: float) -> str:
    total_seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def main() -> None:
    args = build_parser().parse_args()
    training = TrainingConfig(
        steps=args.steps,
        learning_rate=args.lr,
        restarts=args.restarts,
        d_model=args.d_model,
        d_head=args.d_head,
        device=args.device,
        stop_on_perfect_accuracy=not args.no_stop_on_perfect_accuracy,
        verbose=args.verbose,
    )
    config = SearchConfig(
        max_heads=args.max_heads,
        training=training,
        robust_estimate=args.robust,
        robust_steps_multiplier=args.robust_steps_multiplier,
        robust_restarts_multiplier=args.robust_restarts_multiplier,
    )
    start_time = time.perf_counter()

    def maybe_checkpoint(payload: dict) -> None:
        processed_count = payload["processed_count"]
        slice_total = payload["end_index"] - payload["start_index"]

        if args.output is None or args.checkpoint_every is None:
            pass
        elif processed_count % args.checkpoint_every == 0:
            text = json.dumps(payload, indent=2)
            args.output.write_text(text + "\n", encoding="utf-8")

        if args.no_progress or slice_total == 0:
            return
        should_print = processed_count % args.progress_every == 0 or processed_count == slice_total
        if not should_print:
            return

        elapsed = time.perf_counter() - start_time
        avg_seconds = elapsed / processed_count
        remaining = slice_total - processed_count
        eta_seconds = remaining * avg_seconds
        print(
            (
                f"[progress] {processed_count}/{slice_total} "
                f"elapsed={_format_duration(elapsed)} "
                f"eta={_format_duration(eta_seconds)}"
            ),
            file=sys.stderr,
            flush=True,
        )

    payload = run_representative_search(
        args.n,
        config,
        limit=args.limit,
        start_index=args.start_index,
        end_index=args.end_index,
        progress_callback=maybe_checkpoint,
    )
    text = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
