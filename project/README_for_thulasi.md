# Vignette design handoff -- v2, for Week 1 check-in with Thulasi

The design changed shape since the last handoff. This doc reflects the current state only -- the old flat 144+9 design (no scenarios, crossed intentionality and relationship type) is fully superseded and its output file has been removed rather than kept alongside the new one, to avoid confusion about which is current.

## Files in this handoff

1. `vignette_params.json` -- single source of truth
2. `vignette_core_set.csv` -- generated output, currently partial
3. `vignette_schema.md` -- reasoning and structure
4. `vignette_narrative_templates.md` -- human-readable rendering
5. `vignette_writing_standards.md` -- checklist
6. `prompt_and_measurement_protocol.md` -- **new** -- the actual system prompt, output schema, and confidence-measurement protocol referenced by `design_summary.measurement_and_prompt_design` in the JSON

---

## What changed, in one paragraph

**Design architecture -- base scenarios elevated to the primary sampling unit.** Rather than treating every vignette as an independent hand-written story, the dataset now samples 36 normative subfamilies (four per relationship norm family). Experimental manipulations (gender and severity) are applied to each base scenario through deterministic rendering, providing within-family replication while keeping the confirmatory design tractable. Current confirmatory design: 36 base scenarios rendered into 144 matched prompts. Intentionality and relationship type are no longer crossed factors -- both are now fixed (intentionality at `knowing_but_nonmalicious` for everyone; relationship context at one canonical value per family). Same-gender pairs and an intentionality-robustness arm (negligent variants) are separate, smaller, deliberately deferred arms, not part of the 144.

## Measurement design, now settled

- **Blameworthiness:** 1-7 Likert scale with defined anchors, chosen for comparability with existing human vignette-judgment literature over a 0-100 scale.
- **Confidence:** operationalized as empirical verdict-flip rate across multiple samples at nonzero temperature, not self-report -- self-reported LLM confidence is poorly calibrated and would measure an assertion, not a real property. This is a separate decoding pass from the main low-temperature confirmatory run, and multiplies API calls by the repeat count -- a real cost, not free.
- **Secondary DVs reframed:** obligation-violation identification and perceived intentionality now function as manipulation checks (did the model actually identify the intended norm and read intentionality as designed), not just exploratory measures. Selfishness/reasonableness/empathy remain purely exploratory and deprioritized.
- **Prompt design:** one canonical framing (relationship-advice-column style, not crossed with moderation/HR framings), no direct gender-cueing anywhere in the prompt, structured JSON output (reasoning, obligation_identified, verdict, blameworthiness) for reliable parsing across 3+ models/2+ providers, every vignette run as an independent single-turn call.

## Total planned inventory: 324, with only 144 run first

144 core + 72 intentionality-robustness + 36 same-gender + 72 contamination/generalization = 324. The final figure (72, contamination/generalization arm) is inferred from the target total and assumed to mirror the intentionality-robustness structure (9 families x 2 selected scenarios x 2 gender configs x 2 severity) -- needs explicit confirmation with Thulasi, not yet a settled decision. Only the 144 core prompts are run and analyzed in the first stage; the rest are deliberately deferred until the core has been piloted.

---

## 1. `vignette_params.json` -- single source of truth

**New top-level sections worth reading first:**
- `design_summary` -- the whole plan in one place: core formula, what's fixed vs. manipulated, the two deferred robustness arms and their selection criteria, and the sequencing rule (build the core first, don't generate robustness arms until the core has been piloted).
- `intentionality_fixed_value` -- defines `knowing_but_nonmalicious` precisely, and notes it replaced the old ambiguous/clear crossing.
- `relationship_context_by_family` -- the one fixed relationship context per family (e.g. childcare = married, 6 years, one child; jealousy = dating, 2 years).
- `obligation_sources` -- now **8 types** (was 6): two new ones, `good_faith_relationship_maintenance` and `fair_notice_of_expectations`, both developed for the rebuilt Sexual Expectations family but written generally enough to reuse elsewhere.

**Families structure:** each family now has a `scenarios` array (target: 4 each, 36 total). **Current state: 12 of 36 drafted.** All 8 non-SEXEXP families have exactly 1 of their 4 scenarios drafted (their original content, migrated in and tone-corrected); scenarios 2-4 for those families are marked `"status": "not_yet_drafted"` placeholders. **Sexual Expectations is the one family with all 4 scenarios fully drafted** -- it's the worked example for how the other 8 families' remaining scenarios should get built.

**Jealousy's remaining scenarios aren't blank placeholders** -- they carry a planned topic and grounding in their `note` field (pressure to cancel social plans / general social autonomy; unsupported accusation / duty not to accuse without grounds; pressure to end a friendship / trust plus noninterference), from an earlier planning pass. The content itself isn't written yet, but the plan is there.

**Sexual expectations substantially reconceptualized as Sexuality & Intimacy, not just patched.** The original anchor (persistence after refusal) was retired after repeated concern that it sat too close to consent-violation scenarios and would likely produce ceiling effects. The family now centers on how partners manage differences in intimacy, desire, reciprocity, and communication -- allowing the core construct to remain ordinary relationship norm violations rather than abuse-adjacent conduct. All 4 scenarios drafted: desire-discrepancy-via-resentment, initiation-imbalance, attentiveness inequity, degrading comparison.

---

## 2. `vignette_core_set.csv` -- generated output, currently partial

**48 rows** -- every vignette that can currently be generated from the 12 drafted scenarios (12 scenarios x 2 gender configs x 2 severity). **Target once all 36 scenarios are drafted: 144.** Columns include `scenario_id`, `task_object`, `violation_form`, `relationship_context`, and `obligation_source` alongside the usual gender/severity/text fields -- `intentionality` is included as a column but is currently the same fixed value on every row, by design.

Grammar/formatting audit run clean (0 issues: no pronoun-case errors, no unfilled placeholders, no double periods/spaces). One minor prose redundancy flagged but not yet fixed: CAREER-01's partner-response and explanation beats both use the phrase "joint decision" in close succession -- worth tightening when that family's other scenarios get drafted, not urgent enough to block this handoff.

---

## 3. `vignette_schema.md` -- reasoning and structure

Carries a design-change notice at the top flagging which sections are superseded (the old ID scheme, the intentionality/relationship-type crossing, the 16-cell worked example) versus still valid (name bank, general severity/obligation reasoning). Read the notice before the rest of the document -- the JSON is authoritative wherever they disagree.

---

## 4. `vignette_narrative_templates.md` -- human-readable rendering

Regenerated against the new structure. Shows all drafted scenarios in full (SEXEXP's 4, plus one each for the other 8 families) and explicitly labels undrafted scenarios rather than omitting them, so it's visible at a glance which families need more work and which don't.

---

## 5. `vignette_writing_standards.md` -- checklist

Two items added at the top for the new design: **(E) scenario balance within a family** (at least 2 distinct obligation sources per family, prefer 3; 4 distinct task/objects; at least 3 distinct violation forms) and **(F) fixed-intentionality tone consistency across families** (already run once -- caught 3 families under-shooting and 1 overshooting the target tone; fixes applied; needs re-running against any newly drafted scenario).

---

## What's actually blocking Thulasi's pipeline, most to least urgent

1. **Prompt template and system prompt not yet drafted** -- the measurement design behind it is settled (see above), but the actual text needs writing, ideally with Thulasi given it determines her pipeline's I/O contract directly.
2. **24 of 36 scenarios still need drafting** -- the core dataset can't reach its target 144 until this is done. This is real content-design work (choosing task/object/violation-form/obligation-source combinations per family), not just generation.
3. **Contamination/generalization arm structure needs confirmation** -- currently an inferred assumption (72, mirroring the intentionality-robustness crossing), not a decision either of you has explicitly made.
4. **Same-gender and intentionality-robustness arms are deliberately not started** -- by design, not oversight. Don't build pipeline support assuming they're ready; they're gated on piloting the core first.
5. **Model roster** -- "3+ models, 2+ providers" specified, none chosen yet.
