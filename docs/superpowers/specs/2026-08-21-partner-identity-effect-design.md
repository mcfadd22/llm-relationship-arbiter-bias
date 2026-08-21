# Partner-identity effect (item 3) -- design

## Motivation

`docs/planned_analysis.md` item 3: does the partner's gender identity
change how the agent is judged, holding the agent's own gender constant?
This is the mirror image of item 2 (`scripts/analyze_agent_identity_effect.py`'s
Section A: does the agent's own identity change how they're judged, holding
partner constant), and item 5b (a planned orientation analysis) explicitly
reuses this design once it exists. No new data collection is needed --
`responses/confirmatory/*.csv` already has the full 3x3 crossed gender
design.

Also resolves item 3's flagged `[decision needed]`: the existing partner
M-vs-F secondary finding in `analyze_fault_rating_bias.py` ("Secondary
finding: partner (victim) gender effect") is an unpaired Welch-t across all
rows, weaker than the matched design this script introduces. Decision:
**supersede, with a cross-reference note** -- leave the old committed
finding in place, add a note pointing to this script's matched version as
the authoritative one. Same pattern already used in
`analyze_agent_identity_effect.py`'s docstring (explaining why its M-F
sub-result differs from `fault_rating_bias_findings.md`'s headline number)
-- don't let two documents quietly disagree about the same question.

## Scope

One new script, `scripts/analyze_partner_identity_effect.py`, mirroring
`scripts/analyze_agent_identity_effect.py`'s Section A + Section C
structure with agent and partner roles swapped. One small addition to
`scripts/analyze_fault_rating_bias.py` (the cross-reference note above) --
no computation changes there, text only.

**Why there is no "NB-NB" comparison in this script -- explicit, not just
implied**: this script's three pairwise tests are contrasts *between
different values* of partner gender (M vs F, M vs NB, F vs NB), each held
against a fixed agent gender. There is no meaningful "NB vs NB" version of
that contrast -- comparing a category against itself isn't a difference
test, it's zero by construction. What "NB-NB" actually refers to is a
different question: *both people in the relationship being NB*
(agent=NB **and** partner=NB together) -- a same-identity relationship-type
question, not a partner-identity-holding-agent-constant question. That
question is already answered, by item 4
(`analyze_agent_identity_effect.py`'s Section B, NB-NB vs MM vs FF). Item 3
asks "does the partner's identity change how the agent is judged"; item 4
asks "do NB-NB relationships get judged differently than MM/FF
relationships" -- different independent variable, different question.
Conflating them would repeat the exact mistake
`docs/planned_analysis.md` Section 5 explicitly warns against for the
orientation analyses (confusing gender identity with relationship-type/
orientation groupings). This must be stated in the new script's module
docstring, not just understood implicitly.

## Data structure

`build_agent_held_cells(cells)`: keyed by
`(scenario_id, severity, model, agent_gender)` -> `{partner_gender: row}`
-- the mirror image of `analyze_agent_identity_effect.py`'s
`build_partner_held_cells`, which is keyed by
`(scenario_id, severity, model, partner_gender)` -> `{agent_gender: row}`.
Reuses `build_cells()` unchanged as the input to this new function, exactly
as the existing script does.

## Analyses

**Section A -- partner-identity effect, agent held constant.** For each
cell with all three partner genders present (for a given agent_gender in
`{M, F, NB}`), three pairwise diffs: partner M-vs-F, M-vs-NB, F-vs-NB.
Pools over all three agent_gender values. Per comparison: n, mean diff,
paired t, d_z, sign-breakdown/ratio, BBQ-style diff-bias score -- identical
vocabulary to the existing script. Per-model breakdown (5 models x 3
comparisons).

**Section B -- omnibus test.** One 3-level cell-centered, **within-cell**
label-shuffle permutation ANOVA (the corrected methodology from
`analyze_agent_identity_effect.py`'s `cell_centered_omnibus`, commit
`80b75db` -- implement it correctly the first time here, reusing that
exact, already-fixed function logic verbatim rather than the original
buggy global-shuffle version).

No Section equivalent to the existing script's "same-identity relationships"
(Section B there) -- that concept doesn't apply to a partner-identity test;
it's already covered by item 4, as explained above.

## Output

`analysis/partner_identity_effect_findings.md`, same structural style as
`analysis/agent_identity_effect_findings.md` (header with live counts,
per-comparison blocks, per-model breakdown, omnibus section, dynamically
computed significance language -- no hardcoded interpretive prose, per the
lesson from commit `a42f7f7`).

## Cross-reference edit to `scripts/analyze_fault_rating_bias.py`

In the "Secondary finding: partner (victim) gender effect" section, add a
sentence noting that a matched (agent-gender-held-constant) version of this
comparison, plus the NB-partner extension, now exists in
`analysis/partner_identity_effect_findings.md`, and that it -- not this
unpaired result -- is the version to cite going forward. Text-only change;
does not alter this section's existing computed numbers.

## Documentation

README entry (matching the style of every prior script's bullet) and an
update to `docs/planned_analysis.md` item 3's status (mark implemented,
record the actual result once run, note the decision resolution above).

## Testing / verification

Matches this codebase's convention: run end-to-end, sanity-check output.
Specific cross-checks available here (unlike item 2, which had an existing
committed number to reproduce, item 3 has no prior matched result to check
against) -- instead, verify structural correctness by confirming: (a) the
three pairwise comparisons' `n` values are each close to what
`analyze_agent_identity_effect.py`'s own cell-completeness counts would
predict for the mirrored structure (roughly the same order of magnitude as
that script's Section A, since it's the same underlying cells just
re-grouped), and (b) the omnibus test's `n_complete` cell count and F/p
values are plausible (not NaN, not degenerate).
