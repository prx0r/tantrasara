# DONE — definition of done (ported verbatim; it is text-independent)

A rung (0/A/B) is DONE when **all four** hold:

1. **Text gates PASS** (`process/verify.sh` once the pipeline lands here:
   G0 sheet, totals, provenance, TTS, essay, film, files + G9 ears).
2. **Mix proof PASS** (order==assembly, every spec bed present at position,
   edges audible, levels in band).
3. **Two consecutive ear rounds with zero blocking findings after
   adjudication** (per-section whole files + seed; no giant single mix).
4. **Every raw finding classed and ruled** in `build/ears/EAR_LEDGER.md`.

**The raw model verdict is never the gate** (canary: blind batteries score
clean with confabulated reasons). Findings, not tokens: mechanical claims →
meters; text claims → whisper/transcript (transcript wins); then count
blocking findings.

## Taxonomy (blocking rules)

mechanical → **block** · structural → **block** · flow-with-evidence →
adjudicate (maps/cross-checks) · taste → policy row (once, never
re-litigated) · transcript-level → discard (G5 guarantees by
construction) · unstable → discard when refuted by verbatim.

## Ear-regression fixtures (run on any model/prompt/engine change)

`build/ears/ear_fixtures/` bad/good pairs + descriptive prompts; a human
reads every output each run. Drift blocks model/prompt changes, never the
build. Mid-thought stays whisper-edges.

Next product of this pattern auto-closes on gates 1+2 unless a **novel**
finding class appears (new class → ledger row → rule).
