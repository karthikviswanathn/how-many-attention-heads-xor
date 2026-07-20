"""Command-line interface for certified head-complexity intervals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .boolean_cube import signs_from_mask, signs_from_vertex_bitstring
from .certified import estimate_certified_hstar
from .fractional import verify_head_certificate
from .signed_secant_mccormick import (
    verify_signed_secant_cell_cover,
    verify_signed_secant_mccormick_leaf,
)
from .sparse_ptf import verify_sparse_ptf_certificate


def _add_truth_table_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dimension", type=int, required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--mask",
        help="integer or 0x truth mask; bit v is the label at integer-coded vertex v",
    )
    source.add_argument(
        "--vertex-bitstring",
        help="binary labels in vertex order, with the value at vertex zero first",
    )


def _signs(arguments: argparse.Namespace):
    if arguments.mask is not None:
        return signs_from_mask(int(arguments.mask, 0), arguments.dimension)
    return signs_from_vertex_bitstring(arguments.vertex_bitstring, arguments.dimension)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Return rigorous intervals for Boolean attention-head complexity."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    estimate = subparsers.add_parser("estimate")
    _add_truth_table_arguments(estimate)
    estimate.add_argument("--output", type=Path)
    estimate.add_argument("--export-directory", type=Path)
    estimate.add_argument("--no-z3-threshold", action="store_true")
    estimate.add_argument("--threshold-timeout-seconds", type=float, default=30.0)
    estimate.add_argument("--projection-permutations", type=int, default=720)
    estimate.add_argument("--partition-spectral-limit", type=int, default=64)
    estimate.add_argument("--partition-spectral-max-side", type=int, default=128)
    estimate.add_argument("--optimal-fourier-tail", action="store_true")
    estimate.add_argument(
        "--optimal-fourier-tail-max-transitions",
        type=int,
        default=50_000_000,
    )
    estimate.add_argument(
        "--optimal-fourier-tail-max-vertices",
        type=int,
        default=4096,
    )
    estimate.add_argument("--sparse-ptf", action="store_true")
    estimate.add_argument("--sparse-ptf-iterations", type=int, default=32)
    estimate.add_argument("--sparse-ptf-batch-size", type=int, default=8)
    estimate.add_argument("--sparse-ptf-max-columns", type=int, default=256)
    estimate.add_argument("--sparse-ptf-max-vertices", type=int, default=4096)
    estimate.add_argument("--heuristic-restarts", type=int, default=100)
    estimate.add_argument("--heuristic-max-heads", type=int)
    estimate.add_argument("--exact-nra", action="store_true")
    estimate.add_argument("--nra-timeout-seconds", type=float, default=60.0)
    estimate.add_argument("--nra-max-heads", type=int)
    estimate.add_argument("--seed", type=int, default=0)

    verify = subparsers.add_parser("verify")
    _add_truth_table_arguments(verify)
    verify.add_argument("--certificate", type=Path, required=True)
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    signs = _signs(arguments)
    if arguments.command == "verify":
        certificate = json.loads(arguments.certificate.read_text())
        if certificate.get("certificate_type") == "sparse-ptf-upper":
            report = verify_sparse_ptf_certificate(
                certificate,
                signs,
                arguments.dimension,
            )
        elif certificate.get("certificate_type") == "signed-secant-mccormick-leaf":
            report = verify_signed_secant_mccormick_leaf(certificate, signs)
        elif certificate.get("certificate_type") == "signed-secant-cell-cover":
            report = verify_signed_secant_cell_cover(certificate, signs)
        else:
            report = verify_head_certificate(certificate, signs, arguments.dimension)
        print(json.dumps(report, indent=2, sort_keys=True))
        if not report["valid"]:
            raise SystemExit(1)
        return

    result = estimate_certified_hstar(
        signs,
        arguments.dimension,
        use_z3_threshold_degree=not arguments.no_z3_threshold,
        threshold_timeout_milliseconds=int(1000 * arguments.threshold_timeout_seconds),
        projection_permutation_limit=arguments.projection_permutations,
        partition_spectral_limit=arguments.partition_spectral_limit,
        partition_spectral_max_side=arguments.partition_spectral_max_side,
        use_optimal_fourier_tail=arguments.optimal_fourier_tail,
        optimal_fourier_tail_max_transitions=(
            arguments.optimal_fourier_tail_max_transitions
        ),
        optimal_fourier_tail_max_vertices=(
            arguments.optimal_fourier_tail_max_vertices
        ),
        use_sparse_ptf_column_generation=arguments.sparse_ptf,
        sparse_ptf_max_iterations=arguments.sparse_ptf_iterations,
        sparse_ptf_batch_size=arguments.sparse_ptf_batch_size,
        sparse_ptf_max_columns=arguments.sparse_ptf_max_columns,
        sparse_ptf_max_vertices=arguments.sparse_ptf_max_vertices,
        heuristic_restarts=arguments.heuristic_restarts,
        heuristic_max_heads=arguments.heuristic_max_heads,
        exact_nra=arguments.exact_nra,
        nra_timeout_milliseconds=int(1000 * arguments.nra_timeout_seconds),
        nra_max_heads=arguments.nra_max_heads,
        seed=arguments.seed,
        export_directory=arguments.export_directory,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
        temporary.write_text(rendered)
        temporary.replace(arguments.output)
    print(rendered, end="")


if __name__ == "__main__":
    main()
