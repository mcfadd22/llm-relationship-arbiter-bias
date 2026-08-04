# Project status -- Week 1 check-in with Thulasi

This project has run well past the original July 28-Aug 4 window in calendar time, but the actual design work has matured substantially -- what follows is the honest current state, not a re-statement of the original plan.

## The big picture: the design changed shape

The original plan was 9 families x 2 agent-gender x 2 relationship-type x 2 severity x 2 intentionality = 144, with one hand-written template per family. That design had two problems that only became visible through use: relationship-type and intentionality crossing introduced real interpretive instability (this is what surfaced the sexual-expectations consent-adjacency problem and the tone-consistency problem), and a single template per family meant the stated analysis plan's random effect (vignette template) had no variance to estimate.

**The current design:** 9 families x 4 scenarios x 2 gender configurations (MF/FM) x 2 severity = **144** (same total, different composition). Intentionality and relationship type are now fixed, not crossed -- both are real variables worth testing eventually, but as separate, deliberately deferred robustness arms rather than folded into the primary confirmatory analysis.

## Done

**Design architecture (this is where most of the last several sessions went):**
- Three-level separation formalized: normative structure (obligation, severity) / behavioral realization (task object, violation form) / narrative realization (wording, tone, affect) -- this is what let "mismatch vs. violation" become a checkable test rather than a judgment call
- Severity redefined as a construct (harm magnitude) with family-specific proxies, rather than a vague per-family axis
- Obligation-source menu grown to 8 principled, cited types (was 6), including two new general-purpose types developed while rebuilding sexual expectations
- Relationship context fixed per family (one canonical value each), replacing the dating/married crossing
- Intentionality fixed at `knowing_but_nonmalicious` for the core design, replacing the ambiguous/clear crossing; a 4-level richer scale (accidental/negligent/knowing/purposeful) reserved for a deferred robustness arm
- A tone audit run across all 9 families' fixed-intentionality text -- caught 3 families under-shooting the target tone (reading as vague rationalization) and 1 overshooting (reading as controlling rather than merely dismissive); all 4 fixed
**Design architecture -- base scenarios elevated to the primary sampling unit.** Rather than treating every vignette as an independent hand-written story, the dataset now samples 36 normative subfamilies (four per relationship norm family). Experimental manipulations (gender and severity) are applied to each base scenario through deterministic rendering, providing within-family replication while keeping the confirmatory design tractable. Current confirmatory design: 36 base scenarios rendered into 144 matched prompts.

**Sexual expectations substantially reconceptualized as Sexuality & Intimacy.** The original anchor (persistence after refusal) was retired after repeated concern that it sat too close to consent-violation scenarios and would likely produce ceiling effects. The family now centers on how partners manage differences in intimacy, desire, reciprocity, and communication, allowing the core construct to remain ordinary relationship norm violations rather than abuse-adjacent conduct.

**Measurement design settled:** blameworthiness uses a 1-7 Likert scale with defined anchors (chosen for comparability with existing human vignette-judgment literature over a 0-100 scale); confidence is operationalized as empirical verdict-flip rate across multiple samples at nonzero temperature, not self-report (self-reported LLM confidence is poorly calibrated and would measure an assertion rather than a real property).

**Planned robustness inventory: 324 total prompts** -- 144 core + 72 intentionality-robustness + 36 same-gender + 72 contamination/generalization (this last figure is inferred from the target total and mirrors the intentionality-robustness structure; needs confirmation with Thulasi, not yet a settled decision). Only the 144 core prompts are run and analyzed in the first stage.


**Content:**
- **12 of 36 target scenarios drafted** (all 8 non-sexual-expectations families have 1 of 4; sexual expectations has all 4)
- **48 of 144 target core vignettes generated** from the drafted scenarios, grammar-audited clean
- Jealousy's 3 remaining scenarios have a planned topic and grounding already sketched, not yet drafted as prose

**Documentation, all updated to match:**
1. `vignette_params.json` -- rebuilt structure, single source of truth
2. `vignette_core_set.csv` -- current partial generation (48 rows)
3. `vignette_schema.md` -- design-change notice added, superseded sections flagged
4. `vignette_narrative_templates.md` -- regenerated against new structure
5. `vignette_writing_standards.md` -- 2 new checklist items for scenario balance and cross-family tone consistency
6. `README_for_thulasi.md` -- full handoff summary
7. `project_status_summary.md` -- this file

(The old flat-structure `vignette_full_set.csv`, built under the superseded design, has been removed rather than kept alongside the new one.)

## Flagged, not yet resolved

- **24 of 36 scenarios still need drafting.** This is real per-family design work (choosing distinct obligation sources, task objects, and violation forms per the "at least 2 obligation sources, 4 task objects, 3 violation forms per family" rule), not mechanical generation. Jealousy has a head start; the other 7 families (besides sexual expectations and jealousy) haven't had this conversation yet at all.
- **One minor prose redundancy** in CAREER-01 (repeats "joint decision" across two adjacent beats) -- flagged, not fixed, low priority.
- **Novel-premise/contamination-check spec undefined.** This now formally replaces a separate paraphrase-robustness arm (same facts, different wording) that was considered and explicitly dropped in favor of this (same norm, different surface content) -- but its size and selection method still need deciding.

## Not yet started

- **Secondary/exploratory DV scales** (selfishness, reasonableness, empathy) -- deprioritized as purely exploratory; format not decided, lower priority than the two DVs now functioning as manipulation checks (obligation-violation identification, perceived intentionality)
- **Prompt template and system prompt** -- design settled (single canonical relationship-advice framing, no gender-cueing, structured JSON output with reasoning included, independent single-turn calls), but the actual prompt text hasn't been drafted yet
- **Model roster** -- "3+ models, 2+ providers" specified, no models chosen
- **Same-gender supplementary arm** (36 target) -- deliberately not started; gated on core scenarios being finalized and piloted first, per explicit sequencing decision
- **Intentionality-robustness arm** (72 target, negligent variants) -- deliberately not started, same reason; selection criteria for which 2 scenarios per family get this treatment are documented in the JSON but not yet applied
- **Pilot manipulation/severity check** -- still needed before the core's severity and (now-fixed) intentionality manipulations can be trusted, especially for any newly drafted scenario

## Suggested agenda for the Thulasi check-in

1. Walk through the design-change rationale (scenario as 4th factor, why intentionality/relationship-type got fixed instead of dropped) -- this is the thing most likely to need her buy-in before her pipeline work proceeds
2. Confirm the contamination/generalization arm's structure (72, inferred) and draft the actual prompt/system-prompt text together, now that the measurement design is settled -- probably the highest-value remaining unblock for her side
3. Divide up the remaining 24 scenarios -- this is the largest remaining raw-content task and can likely be split
4. Agree on model roster
