# Generalized agent-identity effect (M/F/NB) -- design

## Motivation

The confirmatory dataset (`responses/confirmatory/*.csv`) has a full 3x3
crossed gender design -- `agent_gender` and `partner_gender` each take values
`{M, F, NB}`, ~810 rows per combination, 7284 responses across 5 models. Every
existing analysis script (`analyze_fault_rating_bias.py`,
`analyze_confidence_ambiguity.py`, `family_omnibus_power_analysis.py`) only
uses the M-agent-vs-F-agent paired comparison (holding partner gender constant
at M or F) plus an MM-vs-FF same-gender control. NB is currently unanalyzed
anywhere. The target venue (GeBNLP 2026) explicitly wants beyond-binary
content, and generalizing the paper's core paired-comparison methodology to
NB is the highest-value, lowest-effort next step: the statistical machinery
already exists, it just needs to run over three levels instead of two.

## Scope

One new script, `scripts/analyze_agent_identity_effect.py`, reading
`responses/confirmatory/*.csv` and writing
`analysis/agent_identity_effect_findings.md`. Does not modify
`analyze_fault_rating_bias.py` or its already-committed headline M-F number.

**Explicitly out of scope for this pass** (deferred, not dismissed):
- Per-family breakdown of the new comparisons (natural follow-up once this
  version is in).
- Partner-identity effect (holding agent constant, varying partner) -- a
  different analytic dimension, not yet coded anywhere.
- Reasoning-text engagement/misgendering check for NB-involving rows -- logged
  as open item 10 in `project/project_status_summary.md`. A quick ad hoc
  heuristic spot-check (2026-08-21) on the unambiguous NB-NB subset (n=809)
  found 0% misgendering across all 5 models (66% correctly use "they", the
  rest use no personal pronoun at all -- the expected default for this
  label-based vignette design). That check was a spot-check only, not
  systematic, and doesn't cover the ambiguous mixed-partner rows. Not a
  blocker for this script, since the outcome variable here is the numeric
  `fault_rating`, not reasoning-text pronoun choice -- but any interpretation
  of an NB-involving numeric result should note this open item as an
  unresolved potential confound until the systematic pass is done.

## Data structure

Reuse the existing `build_cells()` pattern from `analyze_fault_rating_bias.py`
(cells keyed by `(scenario_id, severity, model)`, holding a dict of
`(agent_gender, partner_gender) -> row`), but iterate `partner_gender` over
all three levels `{M, F, NB}` rather than just `{M, F}` -- a deliberate scope
expansion. This means the M-vs-F comparison computed here will have a larger n
than (and differ numerically from) `fault_rating_bias_findings.md`'s headline
M-F number, which stays scoped to partner in `{M, F}` as already committed.
The script's docstring must state this explicitly to avoid two documents
quietly disagreeing on "the M-F effect."

## Analyses

**Section A -- agent-identity effect, partner held constant.** For each cell
with all three agent genders present (for a given partner_gender in
`{M, F, NB}`), form three pairwise diffs: M-F, M-NB, F-NB. For each pairwise
comparison, report (same vocabulary as the existing script): n, mean diff,
paired t, d_z, sign-breakdown (X>Y : Y>X ratio, sign-test z), BBQ-style
diff-bias score. Add a per-model breakdown (5 models x 3 comparisons).

**Section B -- same-identity relationships.** Using the diagonal of the same
cell structure (`agent_gender == partner_gender`), form three pairwise diffs
across identity: MM-FF, MM-NBNB, FF-NBNB. Same statistics as Section A.

**Section C -- omnibus tests.** Two label-shuffle permutation one-way ANOVAs
(matching this project's existing permutation-test style, `N_PERMUTATIONS`
shuffles, fixed seed), one for Section A's 3-level agent-identity factor and
one for Section B's 3-level same-identity factor, testing whether identity
has an overall effect beyond the pairwise contrasts.

## Output format

Markdown findings file matching the structure/tone of
`fault_rating_bias_findings.md`: a "Generated from..." header line with live
counts (not hardcoded), one subsection per analysis above, and an
interpretation paragraph after each table computed from the actual p-values
(not hardcoded prose -- this repo just had two scripts caught hardcoding
stale significance conclusions that silently went wrong when new data
arrived, see commit `a42f7f7`; this script must compute all interpretive
language from the live results).

## Testing / verification

No unit tests in this codebase's convention (none of the existing analysis
scripts have them); verification is: script runs cleanly end-to-end on the
current data, output numbers are sanity-checked against known quantities
(e.g. total row/pair counts should match what section A's built cells
predict), and interpretive prose is spot-read against the computed numbers
before treating the run as done.
