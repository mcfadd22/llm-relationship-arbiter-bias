# Document Inventory -- Repo Upload

Snapshot as of this writing. **All 36 target scenarios are now drafted and the full core set (288 vignettes) has been generated.** This supersedes the earlier "12 of 36" partial-content snapshot.

---

## Design & content

### `data/vignette_params.json`
**What it is:** Single source of truth for the entire design. Everything else in this repo is either generated from this file or documentation about it.
**Contains:** `design_summary` (core formula, DV design, robustness-arm sizing, sequencing rules), `intentionality_fixed_value`, `relationship_context_by_family`, `id_scheme`, `name_bank`, `pronoun_map`, `obligation_sources` (8 cited types), and `families` -- each with a `scenarios` array (4 per family, 36 total).
**State:** Architecture complete and stable. **Content now complete -- 36/36 scenarios drafted** (all 9 families have all 4 scenarios). A tone-consistency audit was run against every `knowing_but_nonmalicious` explanation across all 36 scenarios (not just the original 12): one issue was found and fixed in the newly drafted content (EMOLAB-03 read as vague minimization rather than clear awareness) and one was found and fixed in previously-approved content (FINPROV-01 read as dismissive -- "regardless of what partner would think" -- rather than the plain misprioritization tone used elsewhere). Two earlier known bugs (a subject/object pronoun error, and a possessive-pronoun error) remain fixed at the schema level and did not recur in the new content.

### `scripts/generate_vignettes.py`
**What it is:** The generator -- reads `data/vignette_params.json`, renders every drafted scenario across all 4 gender configurations (MF/FM/MM/FF) and both severities, writes `data/vignette_core_set.csv`.
**State:** Complete and stable, unchanged. Re-running it after any future content edits requires no code changes.

### `data/vignette_core_set.csv`
**What it is:** Generated output -- one row per vignette, full rendered text plus all factor columns (`scenario_id`, `task_object`, `violation_form`, `relationship_context`, `obligation_source`, gender/severity).
**State:** **288 rows -- full target reached** (36 scenarios x 4 gender configs x 2 severity). Grammar/formatting audit passes clean at 0 issues (no unfilled placeholders, no pronoun-case errors, no double periods/spaces). Word-count parity checked within each scenario's 8 cells -- no scenario exceeds a 15% spread.

**Scope question from the last update, now resolved:** "core" is redefined to mean all 4 gender configurations at equal weight -- 9 families x 4 scenarios x 4 gender configs (MF/FM/MM/FF) x 2 severity = 288. Same-gender pairs are not a separate supplementary arm anymore; that arm is retired as redundant now that gender_configuration is fully crossed inside the core itself (`design_summary.same_gender_supplementary.status` in the JSON is explicitly marked `REMOVED`). Total planned inventory recalculates to 288 core + 72 intentionality-robustness + 72 contamination/generalization = **432** (down from the earlier 324 figure, which assumed same-gender as a separate 36-vignette arm).

---

## Reasoning & reference

### `docs/vignette_schema.md`
**What it is:** The structural reasoning behind the design -- why obligations are held constant within a scenario, why severity is a construct with family-specific proxies, the canonical sentence-beat order, the name bank.
**State:** Unchanged this round. Carries a design-change notice at the top flagging which original sections are superseded vs. still valid. `data/vignette_params.json` wins wherever the two disagree.

### `docs/vignette_narrative_templates.md`
**What it is:** Human-readable rendering of every drafted scenario's template, generated directly from the JSON.
**State:** Regenerated -- now shows all 36 scenarios. Also corrects a wording mismatch inherited from earlier drafts: the closing question now reads "Was {agent} in the wrong?" to match `prompt_and_measurement_protocol.md`'s actual system prompt, rather than the placeholder "the asshole?" phrasing used before that framing decision was finalized.

### `docs/vignette_writing_standards.md`
**What it is:** Post-drafting quality checklist.
**State:** Unchanged this round. The scenario-balance check (item E) and tone-consistency check (item F) were both applied against the new content as part of this update (see `vignette_params.json` state note above) -- worth noting in the doc itself that both have now been run against the full 36, not just the original 12, next time this file is touched.

---

## Measurement design

### `docs/prompt_and_measurement_protocol.md`
**State:** Unchanged this round.

---

## Project tracking (useful context, not part of the dataset itself)

### `project/README_for_thulasi.md`
**State:** Updated this round to reflect 36/36 scenarios and 288/288 vignettes.

### `project/project_status_summary.md`
**State:** Updated this round to reflect current content-completion state and revised open items.

---

## What's genuinely still missing from this repo

- **Novel-premise/contamination-check spec** -- still undefined (size and selection method)
- **A finalized, merged scoring prompt** -- this doc's draft still needs reconciling with Thulasi's
- **Model roster** -- not yet chosen
- **Intentionality-robustness and contamination/generalization arms** -- deliberately deferred until the 288-vignette core has been piloted
- **Pilot manipulation/severity check against the full 288** -- not yet run
- **Any actual model-response data** -- nothing here has been run through a model yet
