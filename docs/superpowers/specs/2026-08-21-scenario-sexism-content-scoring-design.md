# Scenario-level ambivalent-sexism content scoring -- design

## Motivation

The pre-registered ambivalent-sexism family-group contrast
(`analysis/fault_rating_bias_findings.md`) failed its confirmatory test on
independent data (primary: F(1,897)=0.036, p=0.8066; secondary: F(1,1617)=0.347,
p=0.5686). That test's "ground truth" for which families should show elevated
bias was a coarse, single-author theoretical judgment call -- a binary
in/out label per family, mapping Glick & Fiske's Ambivalent Sexism
Inventory (ASI, 1996) / Ambivalence toward Men Inventory (AMI, 1999)
subscales onto 5 of the study's 9 relationship-norm families, never
independently coded or validated (see the caveat added to
`paper/limitations.tex`).

Motivating question (from conversation with Meredith): real, significant
gender bias exists (`fault_rating_bias_findings.md`'s core finding, d_z=0.32)
and it varies significantly by family (9-way omnibus F=3.196, p=0.0012) --
so why did the specific ambivalent-sexism explanation for *which* families
show more of it come back null? One real possibility: ambivalent-sexism-
relevant content isn't cleanly binary at the family level -- it may be
present, in varying degrees, across families the original mapping assumed
had "no prediction," and a coarse 5-vs-4 bucket can't detect that. This
design tests that possibility directly, by scoring the actual scenario
content on continuous ASI/AMI-derived dimensions instead of relying on a
family-level label.

## Scope

Two new artifacts:
1. `scripts/score_scenario_sexism_content.py` -- a one-time LLM-coding
   script, writes `analysis/scenario_sexism_content_scores.csv` (81 rows).
2. An extension to `scripts/analyze_fault_rating_bias.py` -- a new section
   correlating those scores against each scenario's own gender-fault-gap.

**Unit of analysis: the 81 unique scenario templates**, not the 1,458
rendered vignettes or 7,284 responses. Ambivalent sexism theory is about
the norm/obligation a scenario's situation invokes, not about lexical
content -- the vignette text has zero gendered/evaluative language by
design (one `(male)/(female)/(nonbinary)` tag, otherwise identical across
all 9 gender configs per scenario_id). This means each scenario only needs
scoring once, not once per gender config or per collected response.

**Explicitly out of scope for this pass**:
- Cross-model inter-rater coding (having a second model independently code
  all 81 and checking agreement) -- a real strengthening option, floated in
  conversation and deliberately deferred; single-coder-plus-full-human-review
  is the bar for this version.
- Re-deriving the family-level binary mapping from these continuous scores
  (e.g. re-running the original 5-vs-4 contrast using a data-derived split)
  -- that would risk exactly the after-the-fact-fitting the original
  pre-registration was designed to avoid. This design adds a new,
  independent continuous test; it does not retroactively re-litigate the
  binary one.

## Rubric

Two dimensions, matching the mechanism split already used in the (failed)
family-level test, so this is a genuine like-for-like upgrade rather than a
different theory:

**Benevolent-sexism relevance** (5 items, ASI Protective Paternalism +
Heterosexual Intimacy facets, non-reverse-coded items only -- reverse
coding is a survey-response-direction artifact, not part of the construct
being scored here):
1. "A good woman should be set on a pedestal by her man."
2. "Women should be cherished and protected by men."
3. "Men should be willing to sacrifice their own well-being to provide
   financially for the women in their lives."
4. "Every man ought to have a woman he adores."
5. "No matter how accomplished he is, a man is not truly complete as a
   person unless he has the love of a woman."

**Hostile-sexism relevance** (6 items, AMI Resentment of Paternalism +
Compensatory Gender Differentiation facets, non-reverse-coded only):
1. "Men will always fight for greater control in society."
2. "Even sensitive men want traditional relationships."
3. "Men pay lip service to equality, but can't handle it."
4. "Most men are really like children."
5. "Men would be lost without women to guide them."
6. "Men act like babies when they are sick."

**Citation caveat, must be resolved before this appears in the paper**:
this item wording was pulled from a secondary research-measures
compilation site during this design session, not extracted directly from
the primary 1996/1999 publications (the primary PDF wasn't machine-readable
during this session). Verify exact wording against the original
publications or an authoritative reproduction before citing in
`paper/`-facing text. Not a blocker for running the pilot script below.

**Scoring scale**: each item rated 1-5 on a written, fully-anchored
relevance scale (every point gets a description, not just a number, so the
coder selects a described level rather than free-typing a number -- avoids
the known LLM numeric-self-report calibration problem):
1. Not relevant -- the scenario's core obligation/violation has nothing to
   do with this theme.
2. Barely relevant -- a loose, incidental connection could be drawn, but
   it's not part of what makes this obligation what it is.
3. Somewhat relevant -- the theme is a plausible undertone or secondary
   aspect of the obligation.
4. Clearly relevant -- the theme is a recognizable part of what the
   obligation is fundamentally about.
5. Central -- the obligation's core content directly instantiates this
   theme.

Dimension score = mean of its items' 1-5 ratings (benevolent_score,
hostile_score, each range 1.0-5.0).

## Scenario text preparation & blinding

For each of the 81 `scenario_id`s, take one rendered `vignette_text` from
`data/vignette_core_set.csv` (any single gender config/severity combination
-- content is identical across all 9 gender configs by design; mild
severity is the natural default since it's the less elaborated version).
Strip the `(male)`/`(female)`/`(nonbinary)` tag via a simple text
replacement (e.g. `"Agent 1 (female) and Agent 2 (male)"` ->
`"Agent 1 and Agent 2"`), producing a fully gender-neutral render. Do not
include `scenario_id`, `family_name`, or any reference to the original
theoretical prediction in what's shown to the coder -- blind to exactly the
things that could bias the coder toward confirming the existing mapping,
not to the topical content itself (which is unavoidably visible and fine).

## Coding pass: `scripts/score_scenario_sexism_content.py`

Reuses `scripts/collect-responses.py`'s exact model-calling pattern rather
than inventing new API-calling code: `langchain_openai.ChatOpenAI` against
OpenRouter (`OPENROUTER_API_KEY` env var, same as the existing pipeline),
JSON mode (`response_format={"type": "json_object"}`) plus a
`PydanticOutputParser` for schema validation, and the same
retry-on-malformed-JSON loop (`MAX_RETRIES_PER_CALL`, catching
`OutputParserException`/`JSONDecodeError`).

**Model: `mistralai/mistral-large`** (Mistral AI), not one of the 5 models
used in `responses/confirmatory/` (Anthropic/OpenAI/Google/Meta/DeepSeek).
This isn't about data leakage -- the coder never sees any `fault_rating`
output or gender tag, so there's no literal circular data path -- it's
about avoiding a reviewer-visible independence concern: the statistical
test below pools the fault-rating gap across all 5 study models per
scenario, and using one of those same models to also produce the
explanatory content score would put a shared "voice" on both sides of the
analysis. An external coder removes that concern at negligible cost
(estimated well under $1 for all 81 calls -- see Cost below).

One API call per scenario (81 total, fully independent calls, no shared
context between them). Request schema (Pydantic):

```python
class ItemRating(BaseModel):
    item_text: str  # echoed back for validation/spot-check convenience
    rating: conint(ge=1, le=5)
    justification: str = Field(description="one sentence explaining the rating")

class ScenarioSexismContentRating(BaseModel):
    benevolent_ratings: List[ItemRating]  # exactly 5, in the fixed order above
    hostile_ratings: List[ItemRating]     # exactly 6, in the fixed order above
```

**Output: `analysis/scenario_sexism_content_scores.csv`**, one row per
scenario_id, columns: `scenario_id`, `family_name` (added back after
scoring, not shown to the coder), `benevolent_score`, `hostile_score`, then
one column pair (`{item_key}_rating`, `{item_key}_justification`) per each
of the 11 items for full auditability.

## Validation

**Full review of all 81 rows** (not a subsample) -- Meredith reads every
scenario's ratings + justifications against the source text. This is a
stronger bar than this project's existing coding validation practice
(the reasoning-text pairwise coding is spot-checked on a sample, disclosed
as such) -- achievable here specifically because n=81 is small enough to
review in full, unlike n=720. Disclose as "single automated coder, fully
human-reviewed" rather than "single coder, no inter-rater check" -- a
materially different and stronger claim.

## Statistical test: extends `scripts/analyze_fault_rating_bias.py`

Reuses the exact same M-F `pairs` list already computed for the headline
finding (`matched_pairs(cells)`, partner in `{M, F}`) -- no new pairing
logic. Regroup those pairs' per-pair `fault_rating` diffs by `scenario_id`
instead of `family_name` (81 groups of ~20 pairs each, vs. the existing
9 groups of ~180) to get each scenario's own mean gender-fault-gap.

Correlate (Pearson r, permutation-tested -- reuse the exact pattern already
implemented as `permutation_corr_test()` in
`scripts/analyze_confidence_ambiguity.py`, not new statistical machinery)
each scenario's mean diff against:
1. `benevolent_score`
2. `hostile_score`
3. `max(benevolent_score, hostile_score)` -- a combined indicator matching
   the theory's own claim that either mechanism alone predicts the same
   direction of effect, via different families.

Report all three, transparently, rather than picking one combination rule
and hiding the others -- consistent with how this project already reports
multiple angles (per-family and per-model breakdowns side by side, primary
and secondary tests side by side for the family contrast).

New section written to `analysis/fault_rating_bias_findings.md` (appended,
not a separate file, since it's a direct extension/reinterpretation of the
existing ambivalent-sexism contrast section immediately above it).

## Cost

Estimated well under $1 for the full 81-call pass (rough estimate: ~120K
input tokens + ~40K output tokens at Mistral Large's published OpenRouter
rates, ~$2/M input + ~$6/M output). One-time cost; only needs re-running if
the rubric or scenario text changes. Billed through the same
`OPENROUTER_API_KEY` account already funding the main confirmatory pass.

## Testing / verification

Matches this codebase's existing convention (no unit-test suite for
analysis scripts): run `score_scenario_sexism_content.py` end-to-end,
confirm 81 rows written with no NaN/missing ratings, spot-check a handful
of scenario/justification pairs immediately for face validity before
moving to the full human review pass. Then re-run
`analyze_fault_rating_bias.py` and confirm the new correlation section
appears with real (non-placeholder) computed values, and that nothing
elsewhere in that file's output changed (this is a pure addition).
