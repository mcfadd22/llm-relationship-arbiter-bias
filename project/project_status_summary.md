# Project Status and Core Decisions

This replaces both the prior version of this file and `project/README_for_thulasi.md`
(deleted 2026-08-11 -- fully superseded, no unique content, was drifting out of sync
with reality and risked being read as current when it wasn't). This is now the one
place to read for "where does this stand and why" -- update it in place going
forward rather than creating another parallel status doc.

## Current state, in one paragraph

The vignette dataset is content-complete and QC-audited: 288 core vignettes (36
scenarios x 4 gender configs x 2 severity), all passing the writing-standards
checklist including a mild/severe-contradiction pass added 2026-08-11. A short-paper
draft for the JUDGe 2026 workshop is underway, with everything not gated on actual
model output drafted. Nothing has been run through a model yet -- the pilot is the
single most important next step and is not something this document's author is
executing (see Division of labor below).

## Dataset

- **Design formula:** 9 relationship-norm families x 4 scenarios per family (36
  total) x 4 gender configurations (MF/FM/MM/FF, equal weight -- same-gender pairs
  are not a separate deferred arm) x 2 severity levels = **288 vignettes**.
- **Source of truth:** `data/vignette_params.json`. Generated output:
  `data/vignette_core_set.csv` (regenerate via `scripts/generate_vignettes.py`
  after any edit to the params file).
- **Agent labeling (v3, current):** anonymized `Agent 1` (norm-violator) /
  `Agent 2` (partner) labels, no names, no pronouns anywhere. Gender stated once
  per agent as an explicit `(female)`/`(male)` tag at first mention. Retired the
  earlier gender-neutral-name-plus-pronoun scheme -- see `docs/vignette_schema.md`
  Section 4.
- **Intentionality:** fixed at a single `knowing_but_nonmalicious` level for the
  core set (not crossed). A 4-level robustness arm is designed but deferred (see
  Open items).
- **Obligation-source taxonomy:** 8 types, each with a literature basis, fully
  documented in `docs/vignette_generation_spec.md` Section 4 (the authoritative,
  consolidated version -- `docs/vignette_schema.md`'s own obligation-source table
  was stale relative to `vignette_params.json` until it was resynced 2026-08-11).
- **QC status:** word-count parity (<15% spread per scenario), banned-language
  scan, per-family scenario-balance (>=2 obligation sources, 4 task/objects, >=3
  violation forms), and fixed-intentionality tone-consistency audit all clean. A
  further manual review pass (2026-08-11) found and fixed a distinct bug class in
  17 of 36 scenarios: fields shared verbatim across both severity cells (the
  obligation sentence, the shared explanation, the partner response) silently
  implying an ongoing pattern that contradicted a mild cell's single-incident
  framing, or a demonstrative reference ("this friendship") with no antecedent.
  This check is now automated in `scripts/lint_vignette_params.py` (currently
  reports zero hard issues) and documented as checklist item G in
  `docs/vignette_writing_standards.md`.
- **Pilot manipulation/severity check against the full 288:** still not run. This
  is the most important remaining step before treating the dataset as
  analysis-ready, and needs to cover all 4 gender configs (the original plan only
  covered MF/FM, written before same-gender pairs were folded into core).

## Measurement / prompt design

Full detail in `docs/prompt_and_measurement_protocol.md`. Headline points:
- Single 0--7 `fault_rating` scale with defined anchors ("how much was Agent 1 in
  the wrong"), not a separate categorical verdict + blameworthiness pair. A
  Shaver/Model-Penal-Code-inspired revision to the anchor wording (causality/
  foreseeability/intentionality-based rather than intensity-adjective-based) was
  proposed in a design-decisions log but **is not adopted** -- confirmed
  2026-08-11 that the currently-committed intensity-adjective anchors remain
  authoritative until/unless explicitly revisited.
- "In the wrong" framing follows the Scruples/WHO-task precedent (Lourie, Le Bras
  & Choi 2021) rather than the subreddit's native "the asshole" phrasing.
- Confidence is measured empirically via dispersion of `fault_rating` across a
  repeated-sampling stability pass, not self-report. $N$ and the stability-pass
  temperature are **not yet finalized**.
- The scoring prompt still needs to be conferred and merged with Thulasi's
  independent draft -- non-negotiable elements regardless of final wording:
  no gender-cueing, schema/structured-output enforcement, the 0--7 "in the wrong"
  framing.
- Model roster (final): Claude Sonnet 5, GPT-5-mini, Gemini 2.5 Flash, Llama 3.3
  70B, DeepSeek V3.2 -- 5 models, 4 providers, via OpenRouter.

## Paper (JUDGe 2026 workshop)

Target: JUDGe 2026 ("Can We Trust the Judge?"), NeurIPS 2026, **Short Paper track**
(4pp + refs), submission deadline **2026-08-29**. Draft lives in `paper/` as
per-section files mirroring an Overleaf tab-per-section layout (`intro.tex`,
`lit_review.tex`, `dataset_design.tex`, `measurement_protocol.tex`, `results.tex`,
`limitations.tex`, `broader_impacts.tex`, `checklist.tex`, `ref.bib`), wired
together by `main.tex`. Drafted: Dataset/Design, Measurement Protocol, Related
Work (including direct engagement with Si et al. 2026's GAMA-Bench as the closest
prior work), Limitations, Broader Impacts, a pre-registered Planned Analysis
section, and the checklist items answerable without results. Blocked on the
confirmatory run: Abstract, the Introduction's opening motivation paragraph,
Results, and the statistical-significance/reproducibility/compute-resources
checklist items. `paper/sources/` holds the raw literature review and
design-decision traceability notes this draft was built from.

## Tooling added 2026-08-11

- `scripts/lint_vignette_params.py` -- automates the three item-G checks
  (chronicity-vs-mild conflict and demonstrative-antecedent gaps as hard
  failures, verb-aspect concordance as a review-level flag). Run after any edit
  to `vignette_params.json`, before regenerating the CSV.
- `docs/vignette_generation_spec.md` -- a consolidated, self-contained brief
  (output format, obligation taxonomy, severity-construction rules with
  before/after examples, antecedent rule, writing-standards checklist, worked
  example, review gate) intended to be handed directly to an LLM to draft further
  scenarios that already comply with everything learned so far, rather than
  requiring another manual-review-driven fix pass later.

## Division of labor

Meredith owns experiment design, vignette creation, and interpreting results.
Thulasi owns running the pilot and further experiments (the data collection
pipeline, actually invoking models). Don't treat pilot execution as something to
check on as a task in this document's owner's queue -- it's tracked here as a
dependency, not an action item for them.

## Open items, most to least urgent

1. **Pilot manipulation/severity check against the full 288, all 4 gender
   configs** -- not yet run. Blocks treating the core dataset as analysis-ready,
   and blocks the paper's Results section.
2. **Scoring-prompt merge** between this project's draft
   (`docs/prompt_and_measurement_protocol.md`) and Thulasi's independent draft --
   not yet reconciled.
3. **Stability-pass calibration** -- $N$ (repeat count) and sampling temperature
   not yet decided; informed by temperature-sensitivity literature now cited in
   the paper draft (Schroeder & Wood-Doughty 2024; Norman et al. 2026) but not yet
   settled to a specific value.
4. **Novel-premise/contamination-check spec** -- size and selection method still
   undefined (72 prompts planned, purpose documented in `vignette_params.json`,
   actual content not started). Deliberately deferred until the core is piloted.
5. **Intentionality-robustness arm content** -- formula and selection criteria
   defined (9 families x 2 selected scenarios x MF/FM x mild/severe = 72), but the
   actual accidental/negligent/purposeful explanation text has not been written
   for any scenario. Deliberately deferred until the core is piloted.
6. **Jealousy family sits at 2 distinct obligation sources**, the checklist
   minimum rather than the preferred 3 -- judged as a reasonable fit for a family
   inherently about autonomy violations rather than an oversight, but flagged for
   independent judgment rather than treated as settled.
