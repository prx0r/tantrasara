#!/usr/bin/env bash
# verify.sh — one-command audit. Text stage (audio gates land with the pipeline port).
set -e
cd "$(dirname "$0")/.."
echo "== span pool + essay0 + beats + layers =="
python3 tools/verify_text.py
echo "== rung picks (budgets, A-B nesting, flow) =="
python3 tools/check_picks.py
echo "== files =="
for f in AGENTS.md HANDOVER.md VISION.md BUILD-NOTES.md DONE.md \
         build/canon/essay0.json build/canon/spans_pool.json \
         build/canon/spans_gold.json build/canon/spans_core.json \
         build/canon/beats_core.json build/canon/blunt_key.json; do
  [ -f "$f" ] || { echo "MISSING $f"; exit 1; }
done
echo "ALL GATES PASS"
