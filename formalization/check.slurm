#!/bin/bash
#SBATCH --job-name=lean-check
#SBATCH --account=gusr38169
#SBATCH --partition=cbuild,staging
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=24G
#SBATCH --time=00:15:00
#SBATCH --output=/gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity/check.slurm.out
set -uo pipefail
export ELAN_HOME=/gpfs/work5/0/gusr0688/fair_stuff/.elan
export PATH="$ELAN_HOME/bin:$PATH"
export LEAN_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
cd /gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity
echo "host=$(hostname) file=$CHECK_FILE"; date
lake env lean "$CHECK_FILE"
echo "CHECK_RC=$?"; date; echo "DONE_SENTINEL"
