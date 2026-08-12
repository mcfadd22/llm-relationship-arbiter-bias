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
model output drafted. The confirmatory pass (1 run/vignette, all 5 models, full
288-vignette set) has now been run and committed (`responses/confirmatory/`) --
see "Confirmatory-pass analysis" below for the fault_rating gender-bias findings
and the reasoning-text linguistic-bias pass now underway on top of it.

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

## Confirmatory-pass analysis (started 2026-08-12)

Analysis of `responses/confirmatory/*.csv` (5 models x 288 vignettes = 1,440 rows).

- **Severity manipulation check: passes.** SEV mean `fault_rating` = 5.45 vs. MLD
  = 4.79 (Cohen's d = 0.84, Welch t = 15.8). This resolves open item 1 below (the
  pilot manipulation/severity check) -- the core dataset can be treated as
  analysis-ready on this criterion.
- **Core finding -- agent-gender bias on `fault_rating`:** using the
  design-correct test (paired within scenario x severity x model, comparing
  male-agent vs. female-agent ratings holding partner gender constant), male
  agents are rated as more at fault than female agents: combined diff = +0.144
  (0--7 scale), paired t = 7.73, d_z = 0.29, n = 720 matched pairs. Holds in
  all 9 relationship-norm families and all 5 models (direction never reverses),
  and in both severities. Of the 720 pairs, 545 (76%) show no gender difference
  at all; among the 175 that do differ, 137 blame the male agent more vs. 38
  blaming the female agent more (~3.6:1, sign-test z=7.5) -- the bias is
  concentrated in disagreement cases, not universal. Smaller, opposite-signed
  secondary effect: agents rated slightly more at fault when the partner/victim
  is female (d=-0.11). Cross-model fault_rating agreement is moderate (pairwise
  r=0.57-0.74 on matched vignettes).
- **Reasoning-text linguistic-bias pass (in progress):**
  `scripts/analyze_reasoning_text.py` extracts three features per response's
  free-text `reasoning` field into `analysis/reasoning_features.csv`:
  - LIB (Linguistic Intergroup Bias, Maass et al. 1989) dispositional-abstraction
    score, via spaCy dependency parse of Agent-1-subject clauses. Required a
    preprocessing fix: substituting placeholder names ("Aidan"/"Blake") for the
    literal "Agent 1"/"Agent 2" tokens before parsing, since those tokens
    visibly confused spaCy's parser and the original code wasn't restricting
    subject-matching to Agent 1 specifically (was leaking in Agent 2/partner
    clauses). Verified on a hand-checked example and a 100-row sample.
  - Agentic/communal domain-word rate (`analysis/lexicons/agentic_communal.csv`)
    and moral-intensity harsh-minus-mitigating rate
    (`analysis/lexicons/moral_intensity.csv`), both adapted from the
    Abele & Wojciszke (2007)/Bakan (1966) agency-communion literature. An
    initial literature-only pass had 86-92% zero-hit rates on this corpus, so
    both lexicons were expanded against actual corpus word/lemma frequencies
    (documented per-term in each CSV's `source_note` column) and matching was
    switched to lemma-based (catches inflections like "disregarded") plus a
    hyphenated-term regex fallback. Coverage after expansion: communal zero-hit
    86.5%->40.5%, moral-intensity 52.9%->29.4%, LIB stayed at 9.1%. Agentic
    stayed sparse (92.4%->91.7%) even after expansion -- read as a likely
    genuine finding (the models describe these relational-obligation violations
    almost entirely in communal terms, ~1,167 communal hits vs. ~138 agentic
    hits total) rather than a lexicon-coverage failure.
  - **Paired stats now run** (`scripts/analyze_fault_rating_bias.py`,
    output in `analysis/fault_rating_bias_findings.md`): agentic_rate shows no
    gender effect (d_z=0.02), communal_rate and moral_intensity show small
    effects in the same direction as the fault_rating bias (d_z=0.08 and 0.09),
    LIB shows essentially none (d_z=-0.004) despite being the theoretically
    best-grounded dimension. Correlating the per-pair linguistic-feature diff
    against the per-pair fault_rating diff gives weak results across the board
    (|r|<0.11) -- **the numeric bias is not strongly reflected in these surface
    linguistic markers**. Either the measures are insensitive, or the bias
    operates more on the quantitative scoring step than the qualitative
    reasoning language -- itself a notable, citable finding, and the strongest
    argument yet for the LLM-assisted pattern-discovery pass (open item below)
    over further hand-built lexicon expansion.
  - **Still not done:** an independent hand-read validation subsample (a
    self-conducted spot-check during pipeline development suggested the
    lexicon scores are reasonable, but that's not a substitute for Meredith's
    own independent read before these numbers go in the paper).
- **Moderator breakdowns** (all in `analysis/fault_rating_bias_findings.md`,
  generated by `scripts/analyze_fault_rating_bias.py`):
  - **obligation_source**: effect ranges from d_z=0.45 (good-faith relationship
    maintenance) down to d_z=0.18 (contribution-based reciprocity) -- bias is
    stronger for emotional/interpersonal-responsiveness obligations than for
    concrete transactional-reciprocity ones. **Descriptive pattern only** --
    see the formal omnibus test below before citing this as a confirmed effect.
  - **relationship_context**: no clean monotonic pattern by relationship
    length/stage; effect stays positive (d_z=0.20-0.41) throughout.
  - **Per-model disagreement-pair rate**: every model shows the male-blamed-more
    asymmetry when it disagrees by gender at all, ranging 2.5:1 (Gemini Flash)
    to 5.25:1 (GPT-5-mini). GPT-5-mini's own effect is individually significant
    on its own data (d_z=0.44, t=+5.23, n=144) -- that claim stands on its own.
    Whether GPT-5-mini's effect is *significantly larger* than the other
    models' is a different, harder claim; see the formal test below.
  - **Per-family disagreement-pair rate**: highest in Jealousy/possessiveness
    (37.5%) and Sexuality & Intimacy (30.0%), lowest in Emotional labor (17.5%)
    -- consistent with the family-level effect-size ranking, but again see the
    formal test below before treating family differences as confirmed.
- **Formal test: does family / model / obligation_source significantly
  moderate the gender effect? No, not yet.** Each per-subgroup breakdown above
  tests whether *that subgroup's own* effect differs from zero -- it does NOT
  test whether the subgroups differ from *each other* more than chance would
  (that's the actual interaction/moderation question). Tested with a
  label-shuffle permutation one-way ANOVA on the 720 per-pair fault_rating
  gender-diffs (20,000 shuffles): **family F(8,711)=1.54, p=0.135; model
  F(4,715)=2.07, p=0.085; obligation_source F(7,712)=1.55, p=0.146**. None
  reach conventional significance. With only 9 (or 5, or 8) groups of
  ~80-220 pairs each and a modest pooled effect (d_z=0.29), this omnibus test
  is inherently underpowered relative to the individual within-subgroup
  tests reported above -- a case where many subgroup analyses can each look
  individually significant while the heterogeneity between them remains
  statistically unconfirmed. **Correct framing for the paper:** the bias
  *direction* is remarkably consistent (never reverses across 9 families, 5
  models, 8 obligation sources, 2 severities) -- that consistency is real and
  citable. But claims that specific domains/models/obligation-types show a
  *significantly larger* bias than others are not currently supported by a
  formal test and should be written up as a suggestive, not confirmed,
  pattern -- a candidate for the stability-pass/larger-N follow-up rather
  than a Results-section claim as-is.
- **Is the obligation_source effect divorceable from family/domain?** Mostly
  not. Two sources (`fair_notice_of_expectations`,
  `good_faith_relationship_maintenance`) occur only in Sexuality & Intimacy --
  fully confounded by design, cannot be separated at all. For the rest,
  residualizing each pair's diff by its own family's mean diff shows most
  sources' apparent effect shrinking toward ~0 (|residual t|<1.5) once family
  is removed -- i.e. most of the obligation_source ranking above **is** the
  family/domain effect. One partial exception: `contribution_based_reciprocity`
  (the most cross-cutting source, 8/9 families) keeps a negative residual
  (t~-1.9, marginal) after removing family means, and is the lowest-or-near-
  lowest-bias source within its own family in 5 of 6 families where it
  co-occurs with another source -- a real but modest, family-independent
  damping effect for transactional/reciprocity-framed obligations. Small
  per-cell n and no multiple-comparison correction throughout.
- **Obligation_source profile independent of the gender question entirely**
  (a more basic finding, not nested in family): absolute `fault_rating` level
  varies by ~0.8 points (0-7 scale) by obligation type alone --
  `contribution_based_reciprocity` judged most harshly and most confidently
  (mean=5.43, confidence=87.5), `fair_notice_of_expectations` least (mean=4.60).
  **Ambiguity appears to predict the size of the gender gap**: across the 8
  sources, lower mean confidence and lower mean fault_rating correlate with a
  *larger* gender gap (r=-0.82 with confidence, r=-0.62 with mean fault_rating,
  n=8 source-level points -- an ecological correlation, a strong descriptive
  pattern and plausible mechanism hypothesis, not an individual-response-level
  significance test). The two lowest-bias sources are also the two judged most
  harshly/confidently overall. This is the closest thing to a unifying
  explanation across today's findings: **when a violation is clear-cut, models
  judge it harshly and consistently regardless of agent gender; when it's more
  ambiguous, gender has more room to influence the verdict.**
- **Linguistic features by family** (extends the corpus-wide near-null
  language result): small per-cell n (~20-80 pairs/family/feature), no
  multiple-comparison correction across 9 families x 4 features -- exploratory
  leads, not confirmed effects.
  - **Sexuality & Intimacy** is the only family with a significant
    agentic-language gender gap (t=+2.4) and has by far the largest
    communal-language gap (t=+2.3) -- here the numeric bias comes *with*
    visible language differentiation, unlike most other families.
  - **Jealousy/possessiveness** -- the family with the single largest numeric
    fault_rating bias -- shows a significant *negative* LIB effect (t=-2.1):
    female agents get *more* dispositional/trait-level blame language there
    even though male agents get the higher numeric fault_rating. Verdict and
    narrative point opposite directions in this one domain -- plausibly
    jealousy read as a character trait when a woman is judged vs. a
    situational lapse when a man is. Worth a sentence in Discussion and a
    candidate target for the LLM-assisted pattern-discovery pass.

## Options for further data collection (not yet run; Thulasi's call)

None of these are required to write up the findings above, but each answers a
different open question if Thulasi has bandwidth:

1. **Targeted stability check on the disagreement subset (recommended first
   if any).** Rerun `--pass_type stability` only on the ~300-350 rows that
   participated in one of the 175 disagreement pairs, at N=5-10 repeats. Cheap
   and directly answers the single biggest open question: is the 3.6:1
   disagreement asymmetry a stable signal, or would it reshuffle under
   resampling noise at temp=0.1? This is the number the paper's headline claim
   rests on.
2. **Full stability pass, all 288 vignettes x 5 models.** The already-built
   `--pass_type stability` path, at a still-undecided N and temperature (open
   item 5 below). Answers the dispersion/confidence-metric question for the
   whole dataset, not just the disagreement subset -- more expensive (N x 288
   x 5 calls) and not required to write up the current findings.
3. **LLM-assisted reasoning-text pattern-discovery pass.** Doesn't need new
   vignette runs -- reuses the existing 1,440 `reasoning` texts, having a
   separate model code them for open-ended patterns beyond the three
   predefined linguistic dimensions. Directly motivated by the finding above
   that lexicon/LIB features barely track the fault_rating gap. Needs new API
   calls but no new vignette content, so it's the cheapest "new experiment" to
   greenlight. (This is open item 2 below, already tracked.)
4. **Intentionality-robustness arm (72 vignettes).** Tests whether the bias
   holds/changes when intent varies (accidental/negligent/purposeful) instead
   of the fixed `knowing_but_nonmalicious` level. Blocked on Meredith writing
   the vignette content first (not started) -- not just a "run it" decision.
5. **Novel-premise/contamination check (72 prompts).** Tests whether the
   bias reflects genuine relational reasoning vs. pattern-matching on
   AITA-familiar training data. Strengthens the internal-validity case for
   reviewers but doesn't refine the bias-magnitude estimate. Also blocked on
   content not yet written.
6. **Broader model roster.** Marginal value given the effect already replicates
   across 5 models / 4 providers without reversing; would mostly add
   robustness rather than new mechanism insight.

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

1. **Independent hand-read validation of the reasoning-text linguistic
   features** -- paired statistical tests are now done (see Confirmatory-pass
   analysis above); what's still missing is Meredith's own independent
   spot-check of the automated agentic/communal/moral-intensity/LIB scores
   against the actual text (only a self-conducted developer sanity-check has
   been done so far). Blocks fully trusting these numbers in the paper.
2. **LLM-assisted open-ended pattern discovery in reasoning text** -- explicitly
   wanted in addition to (not instead of) the lexicon/LIB pipeline, to surface
   further significant patterns beyond the three predefined dimensions above.
   Now further motivated by the finding that the lexicon/LIB features barely
   track the fault_rating gap (|r|<0.11) -- see "Options for further data
   collection" above. Not yet started.
3. ~~**Pilot manipulation/severity check against the full 288, all 4 gender
   configs**~~ -- **done, passes** (see Confirmatory-pass analysis above).
4. **Scoring-prompt merge** between this project's draft
   (`docs/prompt_and_measurement_protocol.md`) and Thulasi's independent draft --
   not yet reconciled.
5. **Stability-pass calibration** -- $N$ (repeat count) and sampling temperature
   not yet decided; informed by temperature-sensitivity literature now cited in
   the paper draft (Schroeder & Wood-Doughty 2024; Norman et al. 2026) but not yet
   settled to a specific value.
6. **Novel-premise/contamination-check spec** -- size and selection method still
   undefined (72 prompts planned, purpose documented in `vignette_params.json`,
   actual content not started). Deliberately deferred until the core is piloted.
7. **Intentionality-robustness arm content** -- formula and selection criteria
   defined (9 families x 2 selected scenarios x MF/FM x mild/severe = 72), but the
   actual accidental/negligent/purposeful explanation text has not been written
   for any scenario. Deliberately deferred until the core is piloted.
8. **Jealousy family sits at 2 distinct obligation sources**, the checklist
   minimum rather than the preferred 3 -- judged as a reasonable fit for a family
   inherently about autonomy violations rather than an oversight, but flagged for
   independent judgment rather than treated as settled.
