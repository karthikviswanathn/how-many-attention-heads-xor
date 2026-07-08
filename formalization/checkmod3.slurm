#!/bin/bash
#SBATCH --job-name=lean-mod3
#SBATCH --account=gusr38169
#SBATCH --partition=staging,cbuild
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=48G
#SBATCH --time=00:30:00
#SBATCH --output=/gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity/checkmod3.slurm.out
set -uo pipefail
export ELAN_HOME=/gpfs/work5/0/gusr0688/fair_stuff/.elan
export PATH="$ELAN_HOME/bin:$PATH"
export LEAN_NUM_THREADS="${SLURM_CPUS_PER_TASK:-16}"
cd /gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity
echo "host=$(hostname) mod=$CHECK_MOD"; date
lake build "$CHECK_MOD"
echo "CHECK_RC=$?"; date; echo "DONE_SENTINEL"
