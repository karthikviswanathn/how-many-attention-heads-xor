#!/bin/bash
set -e

TEX_FILE="${1:-proposal.tex}"
BASE="${TEX_FILE%.tex}"

pdflatex -interaction=nonstopmode "$TEX_FILE"

rm -f "$BASE.aux" "$BASE.log" "$BASE.out" "$BASE.toc" "$BASE.synctex.gz" "$BASE.fls" "$BASE.fdb_latexmk"

echo
if command -v pdfinfo >/dev/null 2>&1; then
  PAGES=$(pdfinfo "$BASE.pdf" | awk '/^Pages:/ {print $2}')
  echo "Built: $BASE.pdf ($PAGES pages)"
else
  echo "Built: $BASE.pdf"
fi
