# Planned Analysis Plan -- Next Confirmatory Run

**Status: pre-registered, written 2026-08-18, before any data exists for the
expanded dataset.** This covers the 1,458-vignette set (9 families x 9
scenarios x 9 gender configs x 2 severities -- see
`project/project_status_summary.md`'s "Dataset (2026-08-18 expansion)"
section) once Thulasi runs it against the 5-model roster. Written against the
existing response schema (`fault_rating` 0-7, `confidence` 0-100, `reasoning`
text, `obligation_identified`) -- nothing below requires a schema change
unless explicitly flagged.

Every test that already has a script is marked **[implemented]** and will
just be re-run on the new data. Tests marked **[needs new code]** extend
existing logic to the NB gender configs (or a new bias dimension) and don't
exist yet. Tests marked **[decision needed]** have an open methodological
choice that should be settled *before* results come in, consistent with how
the ambivalent-sexism contrast and RQ1-3 were handled.

---

## 0. Gate: manipulation checks (run first)

- **Severity manipulation check** -- SEV vs. MLD mean `fault_rating`, Welch
  t/d. **[implemented]**, `scripts/analyze_fault_rating_bias.py`. Passed on
  the original 288-vignette data (d=0.84); must re-pass on the new data
  before treating it as analysis-ready, since the 45 new scenarios haven't
  been piloted the way the original 36 were.
- **NB-tag registration sanity check** -- no formal test planned yet;
  eyeball schema-failure/retry rates by gender config once collected (via
  whatever attempt-level logging `collect-responses.py` already produces),
  to catch a model handling the `(nonbinary)` tag differently at the
  API/schema level before trusting any downstream comparison involving it.

## 1. RQ1 -- Core binary agent-gender effect (replication at larger N)

- Paired test (scenario x severity x model held constant, partner gender
  held constant): M agent vs. F agent `fault_rating`. Mean diff, paired t,
  d_z, sign-test on disagreement pairs. **[implemented]**.
- BBQ/KoBBQ-style ambiguous-context diff-bias score
  (`(n_M-blamed - n_F-blamed) / n_total`), overall and by family/model.
  **[implemented]**. See `analysis/fault_rating_bias_findings.md` for the
  formula provenance (Parrish et al. 2022; Jin et al. 2024) and the
  disanalogy caveat (no ground-truth answer or "Unknown" option in this
  task, unlike BBQ/KoBBQ).

## 2. RQ1-extended -- NB agent effect (the core motivation for the NB arm)

- **NB vs. M**, partner held constant at F: existing MF cell's
  `fault_rating` vs. new NBF cell, same scenario/severity/model. Paired t,
  d_z.
- **NB vs. F**, partner held constant at M: FM cell vs. NBM cell. Paired t,
  d_z.
- Report all three pairwise comparisons (M vs. F, M vs. NB, F vs. NB) side
  by side to see whether NB patterns with M, with F, in between, or
  independently -- this is the actual new finding the NB arm exists to
  produce.
- **[needs new code]** -- extend `matched_pairs()`-style logic in
  `scripts/analyze_fault_rating_bias.py` (or a new script) to a 3-level
  gender comparison; nothing currently handles NB as an agent-gender level.

## 3. Partner-gender secondary effect, extended to NB partner

- Existing secondary finding: partner=M vs. partner=F, unpaired Welch t
  across all rows. **[implemented]**.
- **New, matched version**: hold agent gender constant at M, compare
  partner=F (MF) vs. partner=NB (MNB); same holding agent=F (FM vs. FNB).
  Paired t, d_z. Tests whether a nonbinary partner changes how the agent is
  judged, the same logical structure as RQ1 but with partner as the
  manipulated factor.
- **[decision needed]**: the *existing* partner=M-vs-F secondary finding is
  currently an unpaired comparison pooling all rows, which is weaker than
  the matched design used for agent gender. Worth deciding whether to
  upgrade the M/F partner comparison to the same matched design (holding
  agent gender constant) for consistency and comparability with the new
  NB-partner test and the orientation analysis in Section 5, rather than
  reporting three related findings via three different methods.
- **[needs new code]** either way.

## 4. Same-identity controls

- **MM vs. FF** (binary same-gender control from `paper/results.tex`'s
  Planned Analysis) -- re-run on new data. **[implemented]**. Supported the
  main finding on the old data (d_z=0.105, about a third of the main
  MF/FM effect).
- **NBNB** -- no binary counterpart to difference against directly.
  Planned as a descriptive comparison: NBNB's own mean `fault_rating` and
  dispersion, set alongside MM and FF, as an exploratory three-way
  same-identity comparison rather than a paired test. **[needs new code]**.

## 5. Presumed relationship orientation (heterosexual vs. same-sex pairs)

**Terminology note, important to get right**: the vignettes never state
sexual orientation explicitly -- only agent/partner gender tags within an
established romantic relationship (dating/married/cohabiting). MF and FM are
opposite-gender pairings (read as heterosexual); MM and FF are same-gender
pairings (read as gay male / lesbian, respectively). **NB-involving configs
(NBM, NBF, NBNB, MNB, FNB) are a separate identity axis (gender identity, not
sexual orientation) and are deliberately NOT folded into this
heterosexual/non-heterosexual grouping** -- a nonbinary person can have any
orientation, and conflating gender identity with sexual orientation would be
exactly the kind of sloppy intersectionality claim GeBNLP's "beyond binary
gender" framing warns against, not an example of engaging with it well.
NB-involving configs have their own analyses in Sections 2-4.

- **(a) Absolute `fault_rating` level by presumed orientation category**:
  opposite-gender pairs (MF+FM pooled) vs. same-gender pairs (MM+FF pooled),
  holding scenario/severity/model constant, independent of which agent is
  blamed. Does the *same* violation get judged as more or less blameworthy
  depending on whether the couple reads as heterosexual or same-sex?
  **[needs new code]**.
- **(b) Matched partner-gender-as-orientation test**, reusing Section 3's
  design: hold agent=M constant, compare partner=F (MF, opposite-gender) vs.
  partner=M (MM, same-gender) `fault_rating` -- does a male agent get judged
  differently depending on whether his partner/victim is female or male?
  Symmetric test holding agent=F constant (FM vs. FF). **[needs new code]**.
- **(c) Orientation-category diff-bias score**, directly BBQ-comparable:
  BBQ's own 9 bias categories include "Sexual orientation" by name, so this
  connects straight to the benchmark already cited in Section 1. Same
  ambiguous-context-style formula, redefining "biased"/"counter-biased" as
  opposite-gender-pair-favored vs. same-gender-pair-favored. **[needs new
  code]**.
- **(d) Cross-model agreement and mean confidence, split by presumed
  orientation category** -- do models agree with each other less, or report
  lower confidence, judging a same-sex pairing than an opposite-sex one? A
  plausible signature of less-calibrated priors for non-normative
  relationship configurations in training data. **[needs new code]**.
- **(e) Exploratory: family x orientation-category interaction** -- is the
  male-agent-blamed-more pattern specifically larger or smaller within
  same-sex pairings, in particular families (e.g. Jealousy)? Explicitly
  flagged as exploratory and likely underpowered -- the family omnibus
  itself (Section 6) is only just reaching adequate power for the simpler
  9-way test; a 9-family x 2-orientation interaction needs meaningfully more
  data than either main effect alone. Report as a descriptive lead, not a
  confirmatory claim, consistent with how this project has handled every
  other underpowered interaction (the ambivalent-sexism contrast, the
  original family/model/source omnibus tests).

## 6. RQ2 -- Domain (relationship-norm family) heterogeneity

**This is the main research question and the reason the scenario count grew
from 4 to 9 per family** -- see `analysis/family_power_analysis_findings.md`
for the power justification (~65-67% power at the old n=80/family, ~94-98%
projected at the new n=180/family).

- 9-way family omnibus permutation test (label-shuffle F-test) on the
  per-pair `fault_rating` gender diff. **[implemented]**. Prior result:
  F=1.54, p=0.135 (underpowered) -- this is the test the expansion is meant
  to give a fair shot at.
- Per-family descriptive breakdown (mean diff, t, d_z, diff-bias score).
  **[implemented]**.
- Model heterogeneity omnibus (same permutation logic, model as the
  grouping label). **[implemented]**.
- Obligation_source heterogeneity omnibus, plus the family-residualized
  version (is the obligation_source effect separable from family, or just
  family in disguise). **[implemented]**. Now meaningfully more testable
  since every obligation_source spans all 9 families as of this expansion
  (see dataset section of the status doc).

## 7. Pre-registered ambivalent-sexism family contrast -- Stage 2 (confirmatory)

The Stage-1 exploratory ranking (Jealousy/possessiveness, Sexuality &
Intimacy, Household labor as the top-3 by effect size) came from the
*original* 288-vignette data and was shown (2026-08-18 bootstrap check,
`scripts/family_omnibus_power_analysis.py`) to be reasonably stable
in-sample (93%/82%/69% bootstrap top-3 rates) but not yet independently
confirmed.

- **Primary, prespecified test**: re-run the same 2-group planned contrast
  (theory-predicted families vs. no-prediction families, from
  `paper/results.tex`) using **only the new scenarios (05-09)** -- these are
  genuinely independent of the scenarios that generated the Stage-1 ranking,
  so this is a real confirmatory replication, not circular re-analysis.
- **Secondary, exploratory**: the same contrast on the full pooled 81-scenario
  set, for maximum power, reported explicitly as non-independent of the
  original ranking.
- **[decision needed]**: confirm this primary/secondary split before results
  come in -- the whole point of specifying it now is that it can't be
  fit to the data afterward.
- **[needs new code]**: the existing contrast test
  (`scripts/analyze_fault_rating_bias.py`) doesn't currently filter by
  scenario-number range; needs a small extension to run on the 05-09 subset
  specifically.

## 8. Reasoning-text linguistic-bias pipeline

- LIB dispositional-attribution score, agentic/communal lexicon rates,
  moral-intensity score, extracted from the `reasoning` field.
  **[implemented]**, `scripts/analyze_reasoning_text.py` (feature
  extraction) + `scripts/analyze_fault_rating_bias.py` (paired stats and
  correlation with the `fault_rating` gap). Re-run on the much larger new
  reasoning-text corpus once collected.
- By-family breakdown of these features. **[implemented]**.
- Prior finding on old data: weak correlation with the numeric bias
  (|r|<0.11) -- worth checking whether that holds at the new, higher power,
  or was itself an underpowered null. **This is the motivation for Section
  10's pairwise open-coding approach**, which doesn't rely on a predefined
  lexicon the way these four features do, and (unlike everything else in
  this document) doesn't need the new run at all -- it can be prototyped
  right now on the existing 720 matched pairs from the original confirmatory
  pass.

## 9. Confidence -- not a primary test on this run's data

- Self-reported `confidence` (0-100) already shown **not** to track the
  gender gap at the individual-pair level (r=-0.05, ns; see
  `analysis/confidence_ambiguity_findings.md`) -- not being re-tested as a
  primary hypothesis. The correlation can be recomputed on the new data for
  consistency-checking (`scripts/analyze_confidence_ambiguity.py` already
  handles this cheaply) but should not be reported as a meaningful test.
- True dispersion-based confidence (a stability pass at nonzero temperature)
  remains undecided/unscheduled -- not part of this run.
- A `confidence_reasoning` free-text field was discussed but is **not yet
  decided or built** (open item 9a, project status doc) -- if it gets added
  before this run, it would need its own coding-scheme analysis plan, not
  written yet.

## 10. Beyond lexicons: pattern discovery and other bias metrics

The four predefined `reasoning`-text features (Section 8) came back with weak
correlations to the numeric bias (|r|<0.11) across the board, including LIB,
the theoretically best-grounded of the four. That's a real finding, not a
dead end -- but it means the fix is a different *strategy* for reading the
reasoning text, not a fifth hand-built lexicon. (An earlier draft of this
section proposed adopting GAMA-Bench's punitive-word-count and
instructional/accusatory-framing measures -- dropped after review: both are
close enough to the existing `moral_intensity` lexicon that they'd likely
just replicate the same weak-signal result, and GAMA-Bench's full-blame-rate
is a binarized `fault_rating`, which the continuous version already
subsumes. `si2026gama`/GAMA-Bench stays cited in Related Work as the closest
prior work on the numeric-rating side -- it just isn't the right source for
a new reasoning-text metric.)

- **(a) Primary: blind pairwise LLM-judge open coding -- prototyped
  2026-08-18, promising.** Run on the 175 disagreement pairs from the
  original confirmatory pass; two categories (hedging toward female agents,
  character-attribution/harsher-language toward male agents) survive
  Bonferroni correction -- see `analysis/reasoning_pattern_discovery_findings.md`
  and `scripts/analyze_reasoning_patterns.py`. Not yet independently
  validated (single coder, seeded categories, no inter-rater check) -- see
  that findings doc's "What this is not yet" and "Recommended next steps"
  before treating as confirmed. Original spec below, for the full-scale
  version once the expanded dataset's run completes.

  For each matched
  pair (same scenario/severity/model, M-agent vs. F-agent `reasoning` text),
  show a coding model both texts side by side as "Response A"/"Response B"
  -- gender labels and `fault_rating` scores stripped, order randomized --
  and ask it to describe any differences in framing, rhetorical strategy, or
  emphasis it notices, with no predefined categories to choose from. Induce
  a small taxonomy from the recurring answers across many pairs (candidate
  categories to watch for, not to impose up front: cites external
  circumstances as mitigating, attributes intent/character rather than the
  specific act, references relationship history/pattern, hedges or qualifies
  the judgment, centers the partner's stated feelings vs. the agent's stated
  reasons). Once a taxonomy is induced, classify all pairs into it and test
  whether specific categories skew toward one agent gender using the same
  paired sign-test/permutation machinery already used throughout this
  project, for methodological consistency. This keeps the causal
  matched-pair design intact (unlike a plain lexicon scan over unpaired
  text) and is a genuine discovery method rather than a confirmatory scan
  for a predicted signal.
  - **Doesn't require the new run** -- prototypeable immediately on the
    existing 720 matched pairs from the original 288-vignette confirmatory
    pass. Recommended as the actual next step, independent of when Thulasi's
    expanded-dataset run happens.
  - **Validation**: fold this into the already-open "independent hand-read
    validation" item (project status doc, open item 2) -- Meredith
    spot-checking a sample of the induced categories against the source
    text serves both that existing open item and this new analysis at once.
  - **[needs new code]** -- a coding-pass script plus a taxonomy-induction
    step; genuinely new, not an extension of `analyze_reasoning_text.py`'s
    lexicon-matching approach.
- **(b) Disparate-impact / demographic-parity ratio** -- standard in the
  algorithmic-fairness literature (e.g. the "4/5ths rule" used in US EEOC
  hiring-discrimination audits; Feldman et al. 2015's disparate-impact
  framing). Derive a categorical "high-fault" verdict via the cutpoint
  already floated in `docs/prompt_and_measurement_protocol.md`
  (`fault_rating >= 4` as "in the wrong"-leaning, still **not yet finalized**
  -- this needs that decision made first), then compute
  `P(high-fault | agent=M) / P(high-fault | agent=F)` as a disparate-impact
  ratio, and the same for the orientation (Section 5) and NB-agent (Section
  2) comparisons. Unlike (a), this doesn't touch the reasoning text at all --
  it repackages the existing continuous `fault_rating` finding into a
  categorical framing a deployment/compliance audience (moderation, HR)
  recognizes directly. Worth keeping as a secondary, low-effort framing
  device for the deployment-risk pitch, not as a source of new signal.
  **[needs new code + the cutpoint decision]**.
- **(c) "Regard" score on the reasoning text** (Sheng et al. 2019, "The
  Woman Worked as a Babysitter: On Biases in Language Generation") -- a
  holistic sentiment/regard-toward-the-named-subject score, distinct from
  agentic/communal/moral-intensity/LIB. Lower priority than (a): it's still
  a predefined-dimension approach (just a different dimension), so it risks
  the same weak-signal outcome as the existing four features. Worth trying
  only as a secondary check *after* (a), and possibly better used as a way
  to quantify a category that pairwise coding surfaces (e.g. if "attributes
  intent/character" turns out to skew by gender, regard could quantify how
  negatively that attribution reads) rather than as an independent
  first-pass measure. **[needs new code]**.

## 11. Explicitly out of scope for this run's results

- **RQ3 (hedge/refusal rate)** -- needs a schema change (`hedged` field,
  attempt log) that hasn't been built or agreed with Thulasi. Belongs to a
  separate future pass (`--pass_type confirmatory_hedge`), not this run.
- **Intentionality-robustness arm** (accidental/negligent/purposeful) --
  separate, not-yet-drafted 72-vignette arm. If built, the BBQ/KoBBQ
  diff-bias framing from Section 1 is the natural metric to apply across its
  ambiguous-vs-disambiguated intentionality levels (see project status doc's
  BBQ/KoBBQ discussion) -- but that's its own future analysis plan.
- **Novel-premise/contamination-check arm** -- separate, not-yet-drafted
  72-vignette arm.

## 12. Cross-cutting reporting (run regardless of specific RQ)

- Cross-model `fault_rating` agreement (pairwise Pearson r).
  **[implemented]**.
- Obligation_source absolute-blameworthiness profile (mean
  `fault_rating`/`confidence` by source, independent of gender).
  **[implemented]**.

---

## Summary: what needs building before this plan can be fully executed

| # | Item | Status |
|---|---|---|
| 2 | NB-vs-M / NB-vs-F matched-pair comparison | needs new code |
| 3 | Matched partner-gender comparison (incl. NB partner) | needs new code + a design decision |
| 4 | NBNB descriptive comparison | needs new code |
| 5a | Orientation-category absolute `fault_rating` level | needs new code |
| 5b | Matched partner-gender-as-orientation test | needs new code |
| 5c | Orientation-category diff-bias score | needs new code |
| 5d | Cross-model agreement/confidence by orientation | needs new code |
| 5e | Family x orientation interaction (exploratory) | needs new code |
| 7 | New-scenarios-only (05-09) subset filter for the ambivalent-sexism contrast | needs new code + confirm the primary/secondary split |
| 10a | Blind pairwise LLM-judge open coding of reasoning text | **prototyped, promising** -- needs independent validation (single coder, no inter-rater check yet), then scale to full 720 pairs and the new run |
| 10b | Disparate-impact ratio | needs new code + the cutpoint decision (protocol doc, still open) |
| 10c | Regard score on reasoning text | lower priority, needs new code, sequence after 10a |

Everything else (Sections 0, 1, 6, 8, 9, 11, 12) is already implemented and
will just be re-run against the new data once it exists. Of the items above,
**10a is the one item on this whole plan that doesn't wait on Thulasi's run
at all** -- it can be prototyped immediately on the existing 720 matched
pairs. Otherwise, prioritize 2-5 (the NB and orientation analyses, since
they're the paper's new intersectionality contribution) and 7 (needed for
the domain-heterogeneity headline result to be reported honestly) before 10b
(valuable framing, but not new signal). None of this blocks Thulasi's
collection step itself.
