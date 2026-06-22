#!/bin/bash
#SBATCH --job-name=lean-chk2
#SBATCH --account=gusr38169
#SBATCH --partition=cbuild,staging
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=32G
#SBATCH --time=00:20:00
#SBATCH --output=/gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity/check2.slurm.out
set -uo pipefail
export ELAN_HOME=/gpfs/work5/0/gusr0688/fair_stuff/.elan
export PATH="$ELAN_HOME/bin:$PATH"
export LEAN_NUM_THREADS="${SLURM_CPUS_PER_TASK:-12}"
cd /gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity
echo "host=$(hostname)"; date
echo "=== build dep oleans (ThresholdDegree, UnivariateSignChanges) ==="
lake build HeadComplexity.ThresholdDegree HeadComplexity.UnivariateSignChanges
echo "DEP_RC=$?"
echo "=== check ModelToPolynomial ==="
lake env lean HeadComplexity/ModelToPolynomial.lean
echo "CHECK_RC=$?"; date; echo "DONE_SENTINEL"
