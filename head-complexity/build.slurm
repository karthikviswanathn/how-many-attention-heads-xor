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
#print axioms NHead.numerator_additive_split
#print axioms PARITY_not_computable_with_one_head
#print axioms EXACT_not_computable_with_one_head
#print axioms symmetricFn_spike_not_computable_with_one_head
#print axioms signChanges_parity
#print axioms signChanges_le_natDegree
#print axioms signReprDegLe_of_computableWithHeadsN
#print axioms exists_univariate_of_symmetric
#print axioms signChanges_le_of_computableWithHeadsN
#print axioms HStarN_symmetricFn_eq_signChanges
EOF
lake env lean /tmp/AxiomCheck_$$.lean
echo "AXIOM_RC=$?"
rm -f /tmp/AxiomCheck_$$.lean
date
echo "DONE_SENTINEL"
