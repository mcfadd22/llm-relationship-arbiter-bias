# Planned Analysis Plan -- Next Confirmatory Run

**Status: pre-registered, written 2026-08-18, before any data exists for the
expanded dataset.** This covers the 1,458-vignette set (9 families x 9
scenarios x 9 gender configs x 2 severities -- see
`project/project_status_summary.md`'s "Dataset (2026-08-18 expansion)"
section). The run has since completed and `claude_sonnet` has been
excluded (see the notice below) -- the roster referenced throughout this
document is now `gpt5_mini`, `gemini_flash`, `llama33`, `deepseek_v3`.
Written against the
existing response schema (`fault_rating` 0-7, `confidence` 0-100, `reasoning`
text, `obligation_identified`) -- nothing below requires a schema change
unless explicitly flagged.

Every test that already has a script is marked **[implemented]** and will
just be re-run on the new data. Tests marked **[needs new code]** extend
existing logic to the NB gender configs (or a new bias dimension) and don't
exist yet. Tests marked **[decision needed]** have an open methodological
choice that should be settled *before* results come in, consistent with how
the ambivalent-sexism contrast and RQ1-3 were handled.

**claude_sonnet excluded (2026-08-21).** Every result below that
references "5 models" predates this exclusion and is being progressively
re-run against the corrected 4-model dataset (`gpt5_mini`, `gemini_flash`,
`llama33`, `deepseek_v3`) -- see `project/project_status_summary.md`'s
"claude_sonnet excluded" section and `docs/superpowers/specs/
2026-08-21-exclude-claude-sonnet-design.md` for why. A new backlog item
(below, in the Summary table) tracks the deferred decision on whether/how
to add a replacement 5th model.

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
  **Checked 2026-08-21: not fully recoverable from existing data.**
  `collect-responses.py` only prints retry warnings live to the console
  (`tqdm.write`), never persists them to a file -- no logs exist anywhere in
  the repo, so the full retry-rate-by-gender-config test can't be
  reconstructed retroactively for the run that already happened. One
  narrower, real signal *is* recoverable: of deepseek_v3's 6 permanently-
  failed vignettes (documented in commit `266e0ea`), 5 of 6 involve an NB
  agent or partner (`CHILD-02_MNB_SEV`, `FAMOBL-02_FNB_MLD`,
  `FAMOBL-02_MNB_MLD`, `JEAL-02_NBNB_SEV`, `SEXEXP-07_NBF_SEV`), against a
  base rate where NB-involving configs are 5 of 9 total configs -- a real
  skew, but n=6 is far too small to be more than a flagged observation, not
  a finding. To do this properly going forward needs a code change to
  `collect-responses.py` (Thulasi's file) to persist attempt-level
  retry/failure counts, applied on some future re-run -- not retroactive.

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
  **Resolved**: yes -- superseded by the matched version below; the old
  unpaired finding stays in `fault_rating_bias_findings.md` with a
  cross-reference note, not deleted.
- **[implemented] 2026-08-21**, `scripts/analyze_partner_identity_effect.py`
  (4-model dataset, after the `claude_sonnet` exclusion). **Result: partner
  identity matters, and in the opposite direction from agent identity.**
  Holding agent gender constant, agents are judged *less* at fault when the
  partner is male than when the partner is female (M-F: n=1942, d_z=-0.237)
  or nonbinary (M-NB: n=1939, d_z=-0.202); F-vs-NB partner shows no
  significant difference (d_z=0.034). Omnibus: F(2,5811)=98.110, p<0.0001,
  significant. Coherent with (not contradicted by) the agent-identity
  finding: male agents are judged more harshly (item 2), and harm to a
  female partner is judged more harshly than harm to a male partner -- two
  distinct axes reinforcing the same overall pattern rather than
  conflicting.

## 4. Same-identity controls

- **MM vs. FF** (binary same-gender control from `paper/results.tex`'s
  Planned Analysis) -- re-run on new data. **[implemented]**. Supported the
  main finding on the old data (d_z=0.105, about a third of the main
  MF/FM effect).
- **NBNB** -- no binary counterpart to difference against directly.
  Planned as a descriptive comparison: NBNB's own mean `fault_rating` and
  dispersion, set alongside MM and FF, as an exploratory three-way
  same-identity comparison rather than a paired test. **[needs new code]**.

## 4b. Per-family breakdown of items 2/3/4 (agent-identity, partner-identity, same-identity)

RQ2 (Section 6 below) established that the binary M-F agent-gender effect
concentrates significantly in specific relationship-norm families
(Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice). None of
items 2/3/4's NB-inclusive comparisons had a per-family breakdown yet --
each explicitly flagged this as out of scope. This item asks the natural
follow-up: does the NB-related bias concentrate in the *same* domains as
the binary bias, or different ones?

- **[implemented] 2026-08-21**, `scripts/analyze_identity_effect_by_family.py`.
  Adds a per-family descriptive table + formal family-moderation test
  (global-shuffle permutation, verified independently -- see the design
  spec for why this is the correct tool here, not the within-cell-shuffle
  pattern used for items 2/3's own 3-level omnibus tests) to all 9
  comparisons, plus a synthesis comparing each comparison's per-family
  ranking (Spearman rank correlation) against a freshly-recomputed binary
  M-F reference ranking.
- **Result: a genuinely mixed, non-uniform pattern -- not "wherever the
  binary bias is big, the NB bias follows."** Comparisons where **M is one
  of the two sides being compared** track the binary bias's domain
  structure closely and reach significance: agent-identity M-F (Spearman
  rho=+0.883, 3/3 top-family overlap, family moderation p=0.0001),
  agent-identity M-NB (rho=+0.717, 3/3, p=0.0080), same-identity MM-NBNB
  (rho=+0.800, 3/3, though this one's own moderation test does not reach
  significance, p=0.9654 -- concentrated ranking but not confirmed as
  significantly domain-dependent), and same-identity MM-FF (rho=+0.633,
  2/3, p=0.1607). Comparisons **not involving M** show a distinct,
  unrelated domain pattern: agent-identity F-NB (rho=-0.867, 0/3 overlap,
  top families instead Emotional labor/Household labor/Family
  obligations), partner-identity M-F (rho=-0.667, 0/3), partner-identity
  M-NB (rho=-0.567, 0/3), partner-identity F-NB (rho=-0.133, 1/3), and
  same-identity FF-NBNB (rho=-0.350, 1/3).
- **Interpretation**: the domain-concentration pattern found for the core
  binary effect appears specifically tied to *male* agent/same-identity
  comparisons, not to "NB-relatedness" as a general property -- F-vs-NB
  and partner-identity comparisons pattern by a different, currently
  unexplained domain structure (leaning toward provider/caregiving
  families -- Financial provision, Family obligations, Emotional labor,
  Household labor, Childcare -- rather than the power/intimacy families
  that dominate the M-linked comparisons). Worth a citable sentence in the
  paper, and a candidate lead for further investigation, not yet a fully
  explained mechanism.
- Of the 9 non-reference comparisons, family significantly moderates 4
  (agent-identity M-F p=0.0001, agent-identity M-NB p=0.0080,
  partner-identity M-F p=0.0019, partner-identity M-NB p=0.0074) -- a bare
  majority is non-significant (5/9), so "most comparisons show no
  significant family moderation" is accurate but only barely; not an
  overwhelming pattern either way. The reference (binary M-F) itself also
  reaches significance (p=0.0002).

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
projected at n=180/family with 5 models). After the `claude_sonnet`
exclusion (2026-08-21), the actual achieved baseline is n=143-144/family
(4 models) -- still within the projected power range, and the top-3
family ranking by effect size is unchanged in order (Jealousy/possessiveness,
Sexuality & Intimacy, Career sacrifice), though now more compressed at the
bottom of that top-3.

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
  fit to the data afterward. **Resolved**: the split above, as written in
  this pre-registration, is what was implemented -- not revisited after
  seeing either result.
- **[implemented] 2026-08-21**, `scripts/analyze_fault_rating_bias.py`
  (see `analysis/fault_rating_bias_findings.md`'s "Pre-registered test:
  ambivalent-sexism family-group contrast" section). **Result: the
  confirmatory replication does not succeed.** Primary test (new scenarios
  05-09 only, n=717 pairs after excluding `claude_sonnet`): F(1,717)=0.821,
  p=0.3624. Secondary test (full 81-scenario pool, n=1293 pairs,
  non-independent): F(1,1293)=3.639, p=0.0586 -- still null, but notably
  closer to the significance threshold than before the exclusion (moved
  from clearly null to borderline; worth a sentence in the paper draft
  rather than treated as a settled non-result). Both remain null overall,
  and in agreement with each other -- the ambivalent-sexism account, as
  operationalized by this specific theory-predicted-vs-no-prediction family
  grouping, is not supported by either the exploratory or the confirmatory
  data. This does not mean the family heterogeneity itself is fake (the
  9-way family omnibus above *is* significant: F(8,1286)=4.260, p=0.0002
  after excluding `claude_sonnet`, actually strengthened relative to the
  pre-exclusion p=0.0012) -- it means this particular theoretical grouping
  doesn't explain which families show the larger effect. (Numbers above
  reflect the 4-model dataset after `claude_sonnet`'s exclusion,
  2026-08-21; the original 5-model figures were F(1,897)=0.036/p=0.8066 and
  F(1,1617)=0.347/p=0.5686.)

## 7b. Post-hoc/exploratory follow-up: scenario-level ambivalent-sexism content scoring

**Not pre-registered -- added 2026-08-21, after seeing Section 7's null
result.** This must be reported as exploratory/hypothesis-generating, not
as a second confirmatory test of the same theory -- the whole reason
Section 7 was pre-registered was to prevent exactly this kind of
after-the-fact theory-testing from being presented as confirmatory. A null
on Section 7's coarse, unvalidated binary family-level proxy doesn't settle
whether ambivalent-sexism *content* matters; this asks that question
directly instead of relying on the proxy.

Motivating question: real, significant gender bias exists and varies
significantly by family (9-way omnibus F(8,1286)=4.260, p=0.0002 on the
4-model dataset after excluding `claude_sonnet`) -- so why did the
specific ambivalent-sexism explanation for *which* families show more of it
come back null in Section 7? Possibility: ambivalent-sexism-relevant
content isn't cleanly binary at the family level and may be present, in
varying degree, across families the original mapping assumed had "no
prediction" -- a coarse 5-vs-4 bucket can't detect that; a continuous,
item-level content score can.

- Blind-codes each of the 81 scenario templates (not the 1,458 rendered
  vignettes -- content is gender-invariant by design) against ASI/AMI
  subscale items (Protective Paternalism + Heterosexual Intimacy for
  benevolent-sexism relevance; Resentment of Paternalism + Compensatory
  Gender Differentiation for hostile-sexism relevance), each item on a
  fully-anchored 1-5 relevance scale, using an external coder model
  (`mistralai/mistral-large`, outside the study's 4-model roster, to avoid
  the same model being both a study subject and the instrument explaining
  the subjects' pooled behavior) plus full human review of all 81 items
  (stronger validation bar than this project's other coding work, achievable
  because n=81 is small enough to review in full).
- Correlates the resulting continuous scores against each scenario's own
  gender-fault-gap (reusing the same M-F `pairs` and the same
  permutation-tested-Pearson-r machinery already in
  `scripts/analyze_confidence_ambiguity.py`, just regrouped by
  `scenario_id` instead of `family_name`).
- Full design: `docs/superpowers/specs/
  2026-08-21-scenario-sexism-content-scoring-design.md`.
- **[needs new code]**: `scripts/score_scenario_sexism_content.py` (new) +
  an extension to `scripts/analyze_fault_rating_bias.py`. Not yet built.
- **Citation caveat to resolve before paper-facing use**: the ASI/AMI item
  wording used was pulled from a secondary research-measures compilation
  during this design session, not verified against the original 1996/1999
  publications directly.

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

- Self-reported `confidence` (0-100) was originally shown **not** to track
  the gender gap at the individual-pair level on the old, pre-expansion
  data (r=-0.05, ns). **This has since changed and needs a fresh decision,
  not the original framing**: on the full expanded dataset it reached
  significance (r=-0.079, p=0.0016, 5 models), and after excluding
  `claude_sonnet` it remains significant, though weaker (r=-0.068,
  p=0.0125, n=1295 pairs -- see `analysis/confidence_ambiguity_findings.md`).
  See item 9's row in the Summary table below: this is now a judgment call
  on whether to report it as a real (if modest) finding, not a code task.
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

This table is the running status/backlog for the whole plan -- update it in
place as items complete rather than tracking progress anywhere else.

| # | Item | New data collection needed? | Status |
|---|---|---|---|
| 0 | NB-tag registration sanity check (schema-failure/retry rates by gender config) | **Yes, prospectively** -- not recoverable retroactively | **Checked 2026-08-21, not fully recoverable.** No retry logs exist anywhere (`collect-responses.py` only prints live, never persists). Partial signal recovered from existing data instead: 5 of deepseek_v3's 6 permanently-failed vignettes involve NB (base rate 5/9 configs) -- a real skew, but n=6, flagged not confirmed. Full version needs a `collect-responses.py` code change (Thulasi's file) + a future re-run. |
| 2 | NB-vs-M / NB-vs-F matched-pair comparison | No -- existing data sufficient | **implemented 2026-08-21, re-run after excluding `claude_sonnet`**, `scripts/analyze_agent_identity_effect.py` (Section A) -- NB patterns much closer to F than to M (M-F d_z=0.271, M-NB d_z=0.229, F-NB d_z=-0.039). **Note a real conclusion change from the pre-exclusion run**: F-vs-NB was significant before excluding `claude_sonnet` (paired t=-3.36) and is **no longer significant** after (paired t=-1.72, p>0.05) -- update anywhere this contrast is described as significant. |
| 3 | Matched partner-gender comparison (incl. NB partner) | No -- full 3x3 crossing already collected | **implemented 2026-08-21**, `scripts/analyze_partner_identity_effect.py` -- partner=M gets *less* blame attributed to the agent than partner=F (d_z=-0.237) or partner=NB (d_z=-0.202); F-vs-NB partner not significant. Omnibus p<0.0001. Opposite-sign, complementary axis to item 2's agent-identity effect, not a contradiction. |
| 4 | NBNB descriptive comparison | No -- existing data sufficient | **implemented 2026-08-21, re-run after excluding `claude_sonnet`**, `scripts/analyze_agent_identity_effect.py` (Section B) -- upgraded beyond the planned descriptive-only comparison to a full paired test (MM-NBNB, FF-NBNB); NB-NB still patterns with FF (d_z=0.024, near-null) not MM (d_z=0.173) -- same qualitative pattern as before the exclusion, values updated (MM-FF d_z=0.144). |
| 4b | Per-family breakdown of items 2/3/4 (agent-identity, partner-identity, same-identity) | No -- existing data sufficient | **implemented 2026-08-21**, `scripts/analyze_identity_effect_by_family.py` -- mixed pattern, not uniform: comparisons involving M (agent-identity M-F rho=+0.883, M-NB rho=+0.717; same-identity MM-NBNB rho=+0.800, MM-FF rho=+0.633) track the binary bias's domain ranking closely; comparisons not involving M (agent-identity F-NB rho=-0.867; partner-identity M-F/M-NB/F-NB; same-identity FF-NBNB) show a distinct, unrelated domain pattern (provider/caregiving families rather than power/intimacy ones). See Section 4b above for full results and interpretation. |
| 5a | Orientation-category absolute `fault_rating` level | No -- existing data sufficient | needs new code |
| 5b | Matched partner-gender-as-orientation test | No -- existing data sufficient | needs new code |
| 5c | Orientation-category diff-bias score | No -- existing data sufficient | needs new code |
| 5d | Cross-model agreement/confidence by orientation | No -- existing data sufficient | needs new code |
| 5e | Family x orientation interaction (exploratory) | No -- existing data sufficient, but likely underpowered regardless | needs new code |
| 7 | New-scenarios-only (05-09) subset filter for the ambivalent-sexism contrast | No | **implemented 2026-08-21, re-run after excluding `claude_sonnet`.** `scripts/analyze_fault_rating_bias.py` -- **confirmatory replication does not succeed** (primary test, new scenarios only: F(1,717)=0.821, p=0.3624; secondary full-pool test: F(1,1293)=3.639, p=0.0586 -- both null, though the secondary test moved from clearly null to borderline). The ambivalent-sexism account, as operationalized by this family grouping, is not supported. |
| 7b | Scenario-level ambivalent-sexism content scoring (**exploratory/post-hoc, not confirmatory** -- see Section 7b above) | No -- needs a new LLM *coding* pass (~$1, external model), not primary data collection | **spec'd and plan'd 2026-08-21** (`docs/superpowers/specs/2026-08-21-scenario-sexism-content-scoring-design.md`, `docs/superpowers/plans/2026-08-21-scenario-sexism-content-scoring.md`) -- staged, not yet run. |
| 9 | Confidence-vs-gender-gap correlation -- **worth revisiting** | No | re-run after excluding `claude_sonnet` (`analysis/confidence_ambiguity_findings.md`): r=-0.068, p=0.0125 (n=1295) -- still significant though weaker than the pre-exclusion r=-0.079/p=0.0016, and much stronger than the old-data result (r=-0.05, ns) this plan's "not a primary test" framing was based on. The family-residualized version is also still significant but now fragile (p=0.0442, was p=0.0090). Not a code task -- a judgment call on whether to promote this back to a real (if small) reported finding. |
| 10a | Blind pairwise LLM-judge open coding of reasoning text | No -- needs a new LLM coding pass on existing `reasoning` text, not primary collection | **prototyped, promising** -- needs independent validation (single coder, no inter-rater check yet), then scale to full 720 pairs and the new run |
| 10b | Disparate-impact ratio | No | needs new code + the cutpoint decision (protocol doc, still open) |
| 10c | Regard score on reasoning text | No -- needs new code (lexicon/scoring pass on existing `reasoning` text) | lower priority, needs new code, sequence after 10a |
| 13 | Decide on a replacement 5th model (or explicitly settle on 4) | Yes, if a replacement is chosen -- a full confirmatory-pass collection run for one model | **deferred, not urgent** -- claude_sonnet excluded 2026-08-21 for a vignette-drafting familiarity confound (see `project/project_status_summary.md`). No principled reason the roster needs exactly 5, so this is an open question to revisit deliberately, not a gap to rush to fill. |

Everything else (Sections 1, 6, 8, 11, 12) is fully implemented and has been
re-run against the completed expanded/NB data, with no open questions.

**Data-sufficiency headline (checked 2026-08-21): nothing remaining needs a
new primary data-collection run from Thulasi**, except item 0's full
version, which can't be reconstructed retroactively and would need a code
change plus a *future* run to do properly. Items 7b/10a/10c need a new LLM
*coding* pass (scoring/classifying existing text), which is a different,
much cheaper thing than re-running the study against the model roster --
everything else is buildable today from `responses/confirmatory/*.csv` as
it already stands.

Of the remaining items:
- **10a** is the one item on this whole plan that never waited on Thulasi's
  run at all -- already prototyped on the 175 disagreement pairs (of 720
  total) from the original data; scaling to the remaining ~545 tied pairs
  and to the new run's larger corpus is still open, not gated on anything.
- **0** (NB-tag registration check) -- its full version isn't cheap
  (retroactively unrecoverable), but the partial deepseek_v3 skew finding
  above is worth keeping in mind as a caveat on NB-involving deepseek_v3
  results specifically, at essentially zero further cost.
- **5a-e** (the orientation analyses) remain the highest-value undone work
  -- the paper's new intersectionality contribution -- ahead of 10b/10c.
  (Item 3 is now done -- see its row above.)
- **7b** is a genuine open methodological question (does a direct,
  continuous sexism-content measure succeed where the family-level proxy
  failed?) but must stay labeled exploratory in any writeup; it does not
  replace or re-litigate 7's confirmatory result.
- **9** just needs a decision, not new code: whether the new significant
  correlation changes how confidence should be discussed in the paper.
