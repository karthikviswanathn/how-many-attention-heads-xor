#!/usr/bin/env bash
# Continue: fetch mathlib olean cache (now via the working curl wrapper), then build.
set -uo pipefail
export ELAN_HOME=/gpfs/work5/0/gusr0688/fair_stuff/.elan
export PATH="$ELAN_HOME/bin:$PATH"
PROJ=/gpfs/work5/0/gusr0688/fair_stuff/how-many-attention-heads-xor/head-complexity
cd "$PROJ" || { echo "no proj"; echo "DONE_SENTINEL_RC=99"; exit 99; }

echo "=================== STEP 3 (retry): cache get ==================="; date
lake exe cache get
CG=$?
echo "cache_get_rc=$CG"; date

MLIB="$PROJ/.lake/packages/mathlib/.lake/build/lib"
OLEANS=$(find "$MLIB" -name "*.olean" 2>/dev/null | wc -l)
echo "=================== mathlib oleans present: $OLEANS ==================="
du -sh "$PROJ/.lake/packages/mathlib/.lake/build" 2>/dev/null || true

# Guard: refuse to build (which would compile mathlib from source) if the cache is clearly incomplete.
if [ "$OLEANS" -lt 4000 ]; then
  echo "GUARD: olean count $OLEANS < 4000 -> cache incomplete; NOT running lake build to avoid from-source mathlib compile."
  echo "DONE_SENTINEL_RC=42"
  exit 42
fi

echo "=================== STEP 4: build head-complexity ==================="; date
lake build
RC=$?
echo "=================== BUILD EXIT CODE: $RC ==================="; date
echo "DONE_SENTINEL_RC=$RC"
exit $RC
