# Document Inventory -- Repo Upload

Snapshot as of this writing. Design is at 12 of 36 target scenarios drafted; several files will need small re-runs (not rewrites) as more scenarios get added -- see each entry's "state" line.

---

## Design & content

### `vignette_params.json`
**What it is:** Single source of truth for the entire design. Everything else in this repo is either generated from this file or documentation about it.
**Contains:** `design_summary` (core formula, DV design, robustness-arm sizing, sequencing rules), `intentionality_fixed_value`, `relationship_context_by_family`, `id_scheme`, `name_bank`, `pronoun_map`, `obligation_sources` (8 cited types), and `families` -- each with a `scenarios` array (up to 4 per family).
**State:** Architecture complete and stable. Content partial -- 12/36 scenarios drafted (Sexuality & Intimacy has all 4; the other 8 families have 1 of 4 each). Two known bugs were caught and fixed at the source during generation (a subject/object pronoun error, and a possessive-pronoun error that only surfaced once same-gender vignettes were generated) -- neither should recur in newly drafted scenarios since both were schema-level fixes, not per-scenario patches.

### `generate_vignettes.py`
**What it is:** The generator -- reads `vignette_params.json`, renders every drafted scenario across all 4 gender configurations (MF/FM/MM/FF) and both severities, writes `vignette_core_set.csv`.
**State:** Complete and stable. Re-running it after new scenarios are drafted requires no code changes -- it automatically picks up anything marked `"status": "drafted"` and skips placeholders. This is the piece that makes the dataset mechanically reproducible rather than hand-assembled.

### `vignette_core_set.csv`
**What it is:** Generated output -- one row per vignette, full rendered text plus all factor columns (`scenario_id`, `task_object`, `violation_form`, `relationship_context`, `obligation_source`, gender/severity).
**State:** 96 rows currently (12 drafted scenarios x 4 gender configs x 2 severity). Target once all 36 scenarios are drafted: **288**. This file will regenerate automatically and grow as scenario content is added -- it is not something to hand-edit. Grammar/formatting audit passes clean at 0 issues.

---

## Reasoning & reference

### `vignette_schema.md`
**What it is:** The structural reasoning behind the design -- why obligations are held constant within a scenario, why severity is a construct with family-specific proxies, the canonical sentence-beat order, the name bank.
**State:** Carries a design-change notice at the top flagging which original sections are superseded (old ID scheme, old intentionality/relationship-type crossing) vs. still valid (name bank, core reasoning). `vignette_params.json` wins wherever the two disagree.

### `vignette_narrative_templates.md`
**What it is:** Human-readable rendering of every drafted scenario's template, generated directly from the JSON (not maintained separately, so it can't drift out of sync). Undrafted scenarios are explicitly labeled rather than omitted, so it's visible at a glance which families need more content.
**State:** Current as of the last JSON rebuild. Will need regenerating (one script run, not a rewrite) once more scenarios are drafted.

### `vignette_writing_standards.md`
**What it is:** Post-drafting quality checklist -- parity within a family's scenarios, banned-language rules, the single-violation test, obligation-strength consistency, plus two newer sections specific to the current design (scenario balance across a family, and cross-family tone consistency for the fixed `knowing_but_nonmalicious` intentionality value).
**State:** The tone-consistency check has actually been run once already (caught and fixed 4 families' explanation text). The scenario-balance check hasn't been run yet -- most families only have 1 of 4 scenarios so far, so there's nothing to balance across yet.

---

## Measurement design

### `prompt_and_measurement_protocol.md`
**What it is:** The actual system prompt, user-message convention, output JSON schema, and full confidence-measurement protocol for running vignettes through models.
**Contains:** Exact system-prompt text (single 0-7 `fault_rating` scale, "in the wrong" framing with cited precedent rather than "asshole"), the JSON output schema, the empirical-stability confidence method (multi-sample verdict-flip rate, not self-report), and hedge/refusal handling guidance.
**State:** Prompt and schema are finalized and ready to use as-is. Several parameters are explicitly flagged open rather than decided (stability-pass sample count N, stability-pass temperature, whether the stability pass runs on all core vignettes or a subset, and the coding method for `obligation_identified`) -- these need a decision, not more drafting. Also still pending: merging this draft with Thulasi's independent scoring-prompt draft.

---

## Project tracking (useful context, not part of the dataset itself)

### `README_for_thulasi.md`
**What it is:** Handoff-oriented summary of every file above, written for a specific check-in meeting.
**State:** Accurate as of the last major design rebuild. Numbers (12/36 scenarios, 96/288 vignettes) will drift as content work continues -- treat as a snapshot.

### `project_status_summary.md`
**What it is:** Overall done/flagged/not-started tracker plus a suggested meeting agenda.
**State:** Same caveat as above -- current as a snapshot, not a live document. Most useful for the "what's actually still open" section rather than the specific counts.

---

## What's genuinely still missing from this repo

- **24 of 36 scenarios** -- real content-design work, not generation
- **A finalized, merged scoring prompt** -- this doc's draft still needs reconciling with Thulasi's
- **Any actual model-response data** -- nothing here has been run through a model yet; everything above is the stimulus set and measurement design, not results
