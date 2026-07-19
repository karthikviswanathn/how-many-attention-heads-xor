#!/usr/bin/env bash
# Bootstrap a Lean4 v4.29.0 + mathlib environment and build the head-complexity project.
# Logs everything; designed to be run in the background.
set -uo pipefail

export ELAN_HOME=/gpfs/work5/0/gusr0688/fair_stuff/.elan
export PATH="$ELAN_HOME/bin:$PATH"
PROJ=/gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity

echo "=================== STEP 1: install elan ==================="
date
if ! command -v elan >/dev/null 2>&1; then
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o /tmp/elan-init.sh || {
    echo "FAILED to download elan-init.sh"; exit 11; }
  sh /tmp/elan-init.sh -y --no-modify-path --default-toolchain none || {
    echo "FAILED elan install"; exit 12; }
fi
elan --version || { echo "elan not on PATH after install"; exit 13; }

echo "=================== STEP 2: toolchain (from lean-toolchain) ==================="
date
cd "$PROJ" || { echo "no project dir"; exit 14; }
# Running lake in the project triggers install of the pinned toolchain.
lake --version || { echo "lake/toolchain install failed"; exit 15; }
lean --version || true

echo "=================== STEP 3: fetch mathlib cache (oleans) ==================="
date
# Resolve deps + download precompiled mathlib oleans. Retries because the bucket can be flaky.
for attempt in 1 2 3; do
  echo "--- cache get attempt $attempt ---"
  if lake exe cache get; then echo "cache get OK"; break; fi
  echo "cache get attempt $attempt failed; retrying"; sleep 5
done

echo "=================== STEP 4: build head-complexity ==================="
date
lake build 2>&1
RC=$?
echo "=================== BUILD EXIT CODE: $RC ==================="
date
echo "DONE_SENTINEL_RC=$RC"
exit $RC
