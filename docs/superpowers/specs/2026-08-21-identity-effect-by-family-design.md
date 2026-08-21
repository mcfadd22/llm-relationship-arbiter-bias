# Identity effects by relationship-norm family -- design

## Motivation

RQ2 (`docs/planned_analysis.md` Section 6) established one of this
project's two headline findings: the binary M-F agent-gender effect
concentrates significantly in specific relationship-norm families
(Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice show the
largest effects; family omnibus F(8,1286)=4.260, p=0.0002 on the 4-model
dataset). Items 2, 3, and 4 (`analyze_agent_identity_effect.py`,
`analyze_partner_identity_effect.py`) extended the *identity* axis to NB
(agent-identity, partner-identity, same-identity), but none of the three
has a per-family breakdown yet -- each explicitly flags this as out of
scope in its own docstring.

The natural, currently-missing question this design answers: **does the
NB-related bias concentrate in the same relationship domains as the
binary bias, or different ones?** This is a genuine intersectionality
question (gender identity x relationship domain), directly relevant to
GeBNLP's stated interest, and it's the natural extension of infrastructure
already built and reviewed -- no new data, no new statistical methodology,
just applying an already-established method (per-family breakdown +
formal moderation test, exactly as done for the binary effect) to nine
comparisons that don't have it yet.

## Scope

One new script, `scripts/analyze_identity_effect_by_family.py` -- not an
extension of the two existing identity-effect scripts. Rationale: this is
a genuinely distinct cross-cutting question (draws on all three existing
cell structures -- partner-held, agent-held, same-identity -- at once),
and the two sibling scripts are already substantial; adding 9 comparisons'
worth of per-family breakdown directly into them risks the "file doing too
much" problem this project's code reviews have already flagged once.

**Nine comparisons, three axes, each already established and reviewed
elsewhere -- this design adds only the family stratification, no new
pairwise logic:**

| Axis | Comparisons | Cell structure (duplicated from) |
|---|---|---|
| Agent-identity (item 2) | M-F, M-NB, F-NB, partner held constant | `build_partner_held_cells` (`analyze_agent_identity_effect.py`) |
| Partner-identity (item 3) | M-F, M-NB, F-NB, agent held constant | `build_agent_held_cells` (`analyze_partner_identity_effect.py`) |
| Same-identity (item 4) | MM-FF, MM-NBNB, FF-NBNB | `build_same_identity_cells` (`analyze_agent_identity_effect.py`) |

## Method, per comparison (fully precedented, no new statistics)

For each of the 9 comparisons:

1. **Descriptive per-family breakdown** -- mean diff, paired t, d_z,
   diff-bias score, one row per family. Mirrors
   `analyze_fault_rating_bias.py`'s existing "Agent-gender effect by
   relationship-norm family" section exactly (same `paired_stat`/
   `sign_breakdown` helpers, already used throughout this project).
2. **Formal family-moderation test** -- does family significantly
   moderate this comparison's effect size, beyond each family's own
   individual-nonzero-ness? Reuses the **global-shuffle**
   `permutation_omnibus_test`/`one_way_anova_F` pattern from
   `analyze_fault_rating_bias.py`'s existing family/model moderation test
   -- this is the *correct* tool here (a genuine between-groups comparison
   across independent family-labeled pairs), distinct from the
   within-cell-shuffle `cell_centered_omnibus` used for the 3-level
   repeated-measures tests elsewhere in this project. Do not reuse
   `cell_centered_omnibus` here -- it would be the wrong tool for this
   question, the same way a global shuffle was the wrong tool for the
   repeated-measures case that commit `80b75db` fixed. This design
   deliberately uses the *other*, already-correct permutation pattern.

## Power framing (already checked against real data, not assumed)

- Item 2/3's comparisons: ~215-216 pairs/family -- well-powered, comparable
  to or better than the original RQ2 test that already reached
  significance at ~180/family (pre-exclusion) / ~143-144/family
  (post-exclusion, whole-sample baseline; the identity-effect comparisons
  pool over 3 levels of the held-constant role, which is why their
  per-family n is higher than the plain binary test's).
- Item 4's comparisons: ~71-72 pairs/family -- meaningfully thinner (same-
  identity cells don't pool across the held-constant role the way items
  2/3 do). Report descriptively with an explicit "likely underpowered for
  a 9-way split" caveat, consistent with how every other underpowered
  interaction in this project is handled (family x orientation, the
  original pre-expansion family omnibus) -- report, don't omit, don't
  oversell.

## Output structure

`analysis/identity_effect_by_family_findings.md`, organized by axis (three
top-level sections matching items 2/3/4), each containing its 3
comparisons' per-family tables + moderation test results.

**Required synthesis section at the end** -- this is the actual
paper-worthy deliverable, not just raw tables: compare each comparison's
per-family ranking against the already-established binary M-F ranking
(Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice as the
top-3). Does the NB-related bias concentrate in the *same* domains as the
binary bias (suggesting one shared underlying mechanism across identity
axes), or *different* domains (suggesting the NB effect has its own,
distinct domain-sensitivity)? Report this comparison explicitly and
plainly -- it's the sentence a GeBNLP reviewer would want, and burying it
in 9 separate tables without a synthesis would waste the analysis.

## Testing / verification

Matches this codebase's convention: run end-to-end, sanity-check output
(no NaN, plausible n values matching the power audit above -- item 2/3
comparisons' per-family n should each be in the 210-220 range per family;
item 4's should each be in the 68-75 range). Additionally: spot-check one
comparison's per-family numbers by hand against the already-committed,
already-reviewed sibling findings files (e.g. item 2's overall M-F d_z
should be recoverable as roughly the pair-count-weighted average of this
script's 9 per-family M-F d_z values) as a correctness cross-check, since
this script recomputes cells independently rather than importing from the
sibling scripts (matching this project's per-script-duplication
convention).
