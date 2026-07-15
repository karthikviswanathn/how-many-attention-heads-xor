#!/bin/bash
#SBATCH --job-name=lean-build
#SBATCH --account=gusr38169
# cbuild is the official build partition (has internet, for refreshing elan/cache);
# staging is the same srv hardware as a fallback (officially data-transfer, but works).
# SLURM schedules on whichever is free first. Both bill 2.0 SBU/thread-hour.
#SBATCH --partition=cbuild,staging
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=00:25:00
#SBATCH --output=/gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity/build.slurm.out

set -uo pipefail
export ELAN_HOME=/gpfs/work5/0/gusr0688/fair_stuff/.elan
export PATH="$ELAN_HOME/bin:$PATH"
# CRITICAL on a shared/cgroup node: cap Lean's worker threads to the cores we
# actually own, else Lean spawns one thread per HOST core (32) inside a 16-core
# cgroup and thrashes (the earlier 4-core job stalled this way).
export LEAN_NUM_THREADS="${SLURM_CPUS_PER_TASK:-16}"
cd /gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity

echo "=== host: $(hostname)  cpus: ${SLURM_CPUS_PER_TASK:-?}  LEAN_NUM_THREADS=$LEAN_NUM_THREADS ==="
date
echo "=== lake build (refreshes stale oleans + builds new files) ==="
lake build
echo "BUILD_RC=$?"
date

echo "=== axiom check (new L1/L5/L12 theorems must depend only on standard axioms) ==="
cat > /tmp/AxiomCheck_$$.lean <<'EOF'
import HeadComplexity
open HeadComplexity
#print axioms Head.numerator_additive_split
#print axioms PARITY_not_computable_with_one_head
#print axioms EXACT_not_computable_with_one_head
#print axioms symmetricFn_spike_not_computable_with_one_head
#print axioms signChanges_parity
#print axioms signChanges_le_natDegree
#print axioms signReprDegLe_of_computableWithHeadsN
#print axioms exists_univariate_of_symmetric
#print axioms signChanges_le_of_computableWithHeadsN
#print axioms HStarN_symmetricFn_eq_signChanges
#print axioms exists_sign_poly
#print axioms real_partial_fraction
#print axioms atomHead_readout
#print axioms symmetricFn_computable
#print axioms HStarN_symmetricFn
#print axioms HStarN_parity
#print axioms thresholdDeg_parity
#print axioms HStarN_le_weighted_sum
#print axioms HStarN_le_universal_boolean
#print axioms HStarN_eq_zero_iff
#print axioms HStarN_eq_one_iff
#print axioms HStarN_eq_Lfrac
#print axioms Head.restricted_numerator_antipode
#print axioms checkerboard_restriction_HStarN_ge_two
#print axioms HStarN_threshold
#print axioms HStarN_exact
EOF
# Capture the report and FAIL if any non-standard axiom (e.g. sorryAx) appears.
AX_OUT=$(lake env lean /tmp/AxiomCheck_$$.lean 2>&1); AX_RC=$?
echo "$AX_OUT"
if [ $AX_RC -ne 0 ] || echo "$AX_OUT" | grep -qiE "sorryAx|sorry|native_decide"; then
  echo "AXIOM_RC=1"
else
  echo "AXIOM_RC=0"
fi
rm -f /tmp/AxiomCheck_$$.lean
date
echo "DONE_SENTINEL"
