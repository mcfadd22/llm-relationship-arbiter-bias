# Vignette Writing Standards (post-draft checklist)

> **v2 update:** the design now has scenarios (up to 4 per family) instead of one template per family, and intentionality is fixed at `knowing_but_nonmalicious` rather than crossed. Two new checklist items follow from this, in addition to everything below (which still applies at the scenario level):
>
> - **E. Scenario balance within a family** -- per the governing rule: at least 2 distinct obligation-source categories per family (prefer 3 where natural), 4 distinct task/conflict objects, at least 3 distinct violation forms. Check this once a family's 4 scenarios are drafted, not per-scenario.
> - **F. Fixed-intentionality tone consistency across families** -- the `knowing_but_nonmalicious` explanation text needs to read as similarly "knowing but not malicious" in every family, not just internally consistent within one. A tone audit already caught 3 families under-shooting (reading as vague rationalization rather than clearly knowing) and 1 overshooting (reading as controlling rather than merely dismissive) -- see fixes already applied in `vignette_params.json`. Re-run this check against any newly drafted scenario before treating it as final.
> - **G. Severity-aspect concordance (added 2026-08-11, after manual review flagged a recurring contradiction; sharpened same day after a follow-up review pass)** -- three related checks, all stemming from the same root cause: `knowing_nonmalicious_explanation` and `partner_response` are each a *single* field rendered into both the mild and severe cell of a scenario.
>   1. **Verb-aspect check on the agent's own conduct.** Any clause describing what the agent *did* (not the partner's situation or a background fact) must use bounded/single-event aspect (simple past: "chose to," "decided to," "didn't," "had fallen short") rather than progressive/durative aspect ("has been X-ing," "was X-ing," "hasn't been X-ing") or explicit frequency/duration markers ("lately," "generally," "hasn't seen a reason to change," "one more," "here or there"). Bounded aspect reads consistently at either severity; durative aspect reads fine for severe but silently contradicts a mild cell's "skipped it once" framing. This check is scoped to the agent's own conduct specifically -- a clause like "knew partner was counting on him" describes the partner's state, not the agent's violation frequency, and is fine as-is.
>   2. **Chronicity check on the obligation sentence, by content not by type name.** If a scenario's rendered `obligation_sentence` itself asserts an existing deficit or imbalance (e.g. "...has carried more of X than {agent} for some time, with the expectation that {agent} would take on more given the imbalance" -- currently `contribution_based_reciprocity`'s standard form, but check the actual sentence, not just the type label), the mild cell's violation must acknowledge itself as a further instance within that pattern ("again," "another," "once again") rather than implying total isolation -- the obligation sentence renders in both severity cells and pre-empts a "first-time lapse" framing regardless of what the violation sentence claims. Note this is *not* a property of every "pattern-based" obligation type: `established_joint_practice`'s standard form ("{agent} has handled X while {partner} has handled Y") asserts a *working* arrangement, not a deficit, so a genuinely isolated mild lapse is fully coherent against it and needs no such acknowledgment.
>   3. **Demonstrative-antecedent audit.** Any "this/these/that/those" used as a determiner or standalone pronoun (not the complementizer "that," as in "agreed that...") needs its noun to have actually been introduced earlier in that specific rendering -- either by name in the same clause, or by an explicit noun in an upstream field. This is a distinct risk for scenarios whose `obligation_source` is `baseline_relational_norm`, since that type renders an *empty* `obligation_sentence` -- there is nothing upstream to introduce a new referent (e.g. a third-party friend) before the violation sentence needs one.
>
>   17 scenarios were corrected across these three checks on this pass (8 for #1, 7 for #2, 2 for #3) -- see `data/vignette_params.json` diff from 2026-08-11 and the corresponding entries in `project/review_sample_20.md`. All three checks were run exhaustively against every drafted scenario's every field, not just the ones flagged by the original manual review, before treating this pass as complete.


This is a review pass, not a template rule — run it once a family's 16 core cells are drafted, ideally by someone other than the person who wrote them, or by a blind LLM check. It answers "does this vignette meet the quality bar," where the schema answers "is this vignette structured correctly."

## A. Parity across all 16 cells of one family

Check side by side, not one at a time:

- [ ] Same number of sentences
- [ ] Same sentence order (matches the canonical 7-beat structure)
- [ ] Same tense and point of view throughout
- [ ] Same approximate length (word count within ~10% across cells)
- [ ] Same grammatical structure sentence-by-sentence (cell 3's sentence 4 should be the same *kind* of sentence as cell 1's sentence 4)
- [ ] Same location of the intentionality cue (same beat number)
- [ ] Same location of the severity cue (same beat number)
- [ ] Same closing question, verbatim ("Was Agent 1 in the wrong?" -- fixed text, no longer varies by cell now that agents are anonymized labels rather than names)
- [ ] Same amount of contextual detail — mild and severe versions should differ in *what happened*, not in how much surrounding detail is given
- [ ] Same emotional intensity in narration (the facts should carry the severity difference, not the narrator's tone)

## B. Language constraints (every sentence, every cell)

- [ ] No moral adjectives ("selfish," "thoughtless," "cruel," "kind," "considerate")
- [ ] No gendered language outside the explicit `Agent 1 (female)`/`Agent 2 (male)` tag itself (no "as a woman, ..." framing, and -- per the v3 agent-labeling change, see `vignette_schema.md` §4 -- no pronouns of any kind, since gender is now conveyed solely by that one tag)
- [ ] No personality descriptors ("she's usually so patient," "he tends to be controlling")
- [ ] No occupation stereotypes (avoid occupations that carry independent status/gender associations unless the occupation is genuinely load-bearing for the story)
- [ ] No attractiveness cues

## C. Single-violation constraint

Each vignette should have exactly one norm-family violation in play. Before finalizing, check the vignette does not also prominently involve: deception, infidelity, public humiliation, threats, privacy invasion, coercion, discrimination, child endangerment, or illegal conduct — unless one of these *is* the target family itself.

**Review test:** could a reader explain the verdict without ever mentioning the target norm family? If yes, there's a confound — something other than the intended violation is doing the work, and the vignette needs revision before it goes in the set.

## D. Obligation strength

- [ ] The obligation-source sentence (see schema §2a and vignette_params.json's `obligation_sources`) uses the same standardized form across all 16 cells of a family
- [ ] The obligation is stated explicitly in the narrative (except `baseline_relational_norm` families, where the point is that no explicit grounding is needed)
- [ ] If a family's obligation source genuinely differs from another family's, that difference is recorded in metadata, not incidental
- [ ] For any family flagged `pilot_check_flag` in the params file (currently JEAL, SEXEXP), do not finalize the mild/severe wording until the pilot check described in that flag has been run

Note: an earlier draft of this project characterized Scanlon's account of promising as treating the *act of committing* as self-sufficiently binding. That overstates his view -- Scanlon explains promissory obligation through assurance, induced expectation, and a principle against unfairly frustrating reliance you intentionally created (Principle F), not through the bare fact of utterance. See *What We Owe to Each Other* (1998), pp. 295-327. This matters most for `recognized_reliance_on_disclosure` (used for sexual expectations): the wrong is disregarding a reliance you knowingly induced or ignored, not breaking a promise-shaped speech act.

## How to use this

Run sections A-D as a checklist against each family's 16-cell block once drafted, before moving to the next family. It's much cheaper to catch a parity or confound issue at the "16 cells for one family" stage than after all 144 vignettes exist — a systematic error in one family's severity-cue placement, for instance, would otherwise propagate across every cell in that family and potentially wash out or inflate the effect you're trying to measure.

Consider running this checklist twice: once by the vignette author (self-check), and once by the other project member or a blind LLM pass, since length/tone parity is genuinely hard to judge accurately while you're the one who just wrote the text.
