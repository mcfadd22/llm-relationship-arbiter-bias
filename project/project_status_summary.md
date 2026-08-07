# Project status -- content-complete update

This supersedes the earlier "Week 1 check-in" snapshot, which was written when only 12 of 36 scenarios existed. The design architecture hasn't changed since then; what's changed is that content drafting is now finished.

## The big picture: content is now complete, design is unchanged

Design formula, revised: "core" is now redefined to include same-gender pairs at equal weight -- 9 families x 4 scenarios x 4 gender configurations (MF/FM/MM/FF) x 2 severity = **288**. The earlier separate 36-vignette same-gender arm is retired as redundant, since gender_configuration is now fully crossed inside the core itself. Intentionality and relationship type remain fixed, not crossed, exactly as decided previously.

## Done

**Everything previously listed as done in the design-architecture section is unchanged** -- three-level separation (normative/behavioral/narrative), severity as a construct with family-specific proxies, 8 cited obligation-source types, relationship context fixed per family, intentionality fixed at `knowing_but_nonmalicious`, Sexuality & Intimacy's reconceptualization.

**Content, newly complete:**
- **All 36 target scenarios drafted** (previously 12/36) -- the 8 families that had only their original scenario now each have 3 additional scenarios covering distinct task/objects, obligation sources, and violation forms, following the scenario-balance rule (at least 2 distinct obligation sources per family, prefer 3; 4 distinct task/objects; at least 3 distinct violation forms). One family (Jealousy) sits at the 2-source minimum rather than 3, judged as a reasonable fit for a family that's inherently about autonomy violations without couple-specific agreements rather than an oversight -- flagged for your own judgment, not treated as settled.
- **All 288 target core vignettes generated** (previously 48/144 under the old partial state) -- 36 scenarios x 4 gender configs x 2 severity.
- **Quality checks run against the full set:** banned-language scan (0 real hits after one fix), scenario-balance check (all 9 families meet or exceed the minimum), word-count parity within each scenario's 8 cells (no scenario exceeds 15% spread), placeholder/formatting audit (clean).
- **Tone-consistency audit (item F) re-run against all 36 scenarios**, not just the original 12. Two fixes applied: EMOLAB-03 (read as vague minimization, reworded to show clear awareness) and FINPROV-01 (read as dismissive -- "regardless of what partner would think" -- reworded to match the plain misprioritization tone used elsewhere).

## Resolved this round

- **MM/FF scoping question.** Redefined "core" to include same-gender pairs as a full, equal-weight level of gender_configuration rather than a separate deferred arm. The JSON's `design_summary.same_gender_supplementary.status` now explicitly reads `REMOVED -- redundant`. Total planned inventory recalculates from 324 to **432** (288 core + 72 intentionality-robustness + 72 contamination/generalization).
- **`docs/vignette_narrative_templates.md`** regenerated against the complete JSON -- also fixed a wording mismatch it had carried since early drafts (closing question said "the asshole?" instead of "in the wrong?", which didn't match the finalized prompt protocol).

- Data collection pipeline

- Model roster

## Flagged, not yet resolved

- **Novel-premise/contamination-check spec still undefined** -- size and selection method not decided.

## Not yet started

- **Pilot manipulation/severity check against the full 288** -- the original plan was to pilot before scaling past the initial 12 scenarios; that pilot never happened, and now needs to cover all 4 gender configs, not just MF/FM. This is the most important remaining step before treating the dataset as analysis-ready. A 20-vignette stratified review sample (2 per family, +1 each for Jealousy and Sexuality & Intimacy given their open `pilot_check_flag`) has been pulled for a first human read-through, but that's a spot-check, not the full pilot.
- **Secondary/exploratory DV scales** -- still deprioritized, unchanged.
- **Intentionality-robustness and contamination/generalization arms** -- still deliberately deferred until the core has been piloted.

## Suggested agenda for the next check-in

1. Review the 20-vignette stratified sample together -- flags anything before committing to the full pilot design
2. Walk through the tone-audit fixes (EMOLAB-03, MENTAL-04, FINPROV-01) and the core redefinition (288, same-gender folded in) -- both happened since the last sync
3. Schedule the manipulation/severity pilot against the full 288, across all 4 gender configs
4. Confirm the contamination/generalization arm's structure (72, inferred)
5. Agree on model roster
