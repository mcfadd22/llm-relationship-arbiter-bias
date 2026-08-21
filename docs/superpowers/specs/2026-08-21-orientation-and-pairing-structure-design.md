# Presumed orientation (items 5a-5e) and pairing structure (item 5f) -- design

## Motivation

`docs/planned_analysis.md` items 5a-5e ask whether the *same* violation gets
judged differently depending on whether the couple reads as opposite-gender
(MF/FM, presumed heterosexual) or same-gender (MM/FF, presumed gay/lesbian)
-- flagged, together with item 3, as "the highest-value remaining work --
the paper's new intersectionality contribution." No new data collection is
needed; `responses/confirmatory/*.csv` already has everything required.

During design, a further question came up (tracked here as new item 5f,
distinct from 5a-5e): items 5a-5e deliberately exclude all NB-involving
configs from the orientation axis, because a nonbinary person paired with
anyone could hold any orientation -- there's no stable cultural default
reading of an NB-involving pairing the way there arguably is (even if only
"presumed," per the plan's own caveat) for MM/FF. Folding NB into an
*orientation* proxy would be a category error, not an example of "beyond
binary" engagement. But a different, honestly-named construct is
defensible: does the pairing depart from the default two-different-binary-
genders script at all, independent of any orientation claim? That's item
5f -- **gender-normativity / identity-sharing structure of the pairing**,
covering all 9 configs, explicitly not framed as orientation.

## Part 1: items 5a-5e -- presumed orientation (MF/FM vs. MM/FF only)

### Scope

One new script, `scripts/analyze_orientation_effect.py`, covering all five
sub-analyses as sections in one file -- they share one grouping variable
and mostly reuse existing statistical machinery already proven correct
elsewhere in this project (matches how `analyze_fault_rating_bias.py`
itself bundles many related sections rather than splitting into
near-duplicate files). **NB-involving configs are excluded entirely from
this script** -- see Motivation above; this is what the plan's own
terminology note requires.

### Core grouping (shared by all five sections)

For each `(scenario_id, severity, model)` cell: pool the `{MF, FM}` rows'
`fault_rating` into one **opposite-gender** per-cell mean, and the
`{MM, FF}` rows into one **same-gender** per-cell mean. ~810 cells (same
scale as the existing MM-vs-FF same-gender control), each contributing one
`(opposite_mean, same_mean)` pair.

### Section A (item 5a) -- absolute fault-rating level by orientation

Paired diff per cell: **`same_mean - opposite_mean`** (same-gender first --
see the pair-ordering note below, this is not an arbitrary choice). Report
n, mean diff, paired t, d_z -- identical vocabulary to every other paired
test in this project.

**Implementation note**: `opposite_mean`/`same_mean` are synthetic
per-cell aggregates, not real response rows, so they don't have the full
row-dict shape (`model`, `family_name`, etc.) that `paired_stat`/
`sign_breakdown`/`write_comparison_block` expect. Wrap each as a minimal
pseudo-row -- `{"fault_rating": same_mean}` and
`{"fault_rating": opposite_mean}` -- so the existing helpers work unchanged
on a list of `(pseudo_row_same, pseudo_row_opposite)` tuples, i.e. call
`write_comparison_block(out, pairs, "same-gender", "opposite-gender")`
(same first, opposite second). Cheaper and more consistent than writing
parallel scalar-only versions of those three functions. (Section E's
per-cell diffs, used directly as flat scalars with
`one_way_anova_F`/`permutation_omnibus_test`, need no such wrapping --
those functions never assumed row-dict structure in the first place.)

**Pair-ordering note, easy to get backwards**: `sign_breakdown()`'s
`diff_bias = (n_pos - n_neg) / n` is positive when the *first* argument in
each pair is larger. Every existing diff-bias score in this project is
signed so **positive = the theoretically-relevant biased direction** (the
core M-F score: positive = male-disadvantaging, the primary hypothesis
direction). To keep that same convention here, put `same_mean` first and
`opposite_mean` second in every pair passed to `paired_stat`/
`sign_breakdown`/`write_comparison_block`, so that "biased" (same-gender
rated more at fault, confirmed above) reads as **positive** diff-bias,
matching Section C exactly rather than requiring a reader to remember an
inverted sign.

### Section B (item 5b) -- matched partner-as-orientation test

Reuses `analyze_partner_identity_effect.py`'s `build_agent_held_cells`
structure (once that script exists -- item 3), but instead of pooling
across all three agent_gender values, filters to a single agent_gender at
a time: agent=M held constant, partner=F (MF) vs. partner=M (MM); agent=F
held constant, partner=M (FM) vs. partner=F (FF). Two separate paired
tests, each reusing `pairwise`/`paired_stat` directly -- no new pairing
logic, just a filter on the existing cell-dict's key.

**Pair-ordering note (same convention as Section A)**: call
`pairwise(cell_dict, same_partner_value, opposite_partner_value)` -- i.e.
`pairwise(agent_M_cells, "M", "F")` (partner=M is same-identity when
agent=M, listed first) and `pairwise(agent_F_cells, "F", "M")` (partner=F
is same-identity when agent=F, listed first) -- so both tests' diff-bias
signs read the same way as Section A's (positive = same-gender-partner
rated more at fault).

### Section C (item 5c) -- orientation diff-bias score

Same `sign_breakdown()`/diff-bias formula used throughout this project,
applied to Section A's per-cell diffs. **Bias direction (confirmed with
Meredith): "biased" = same-gender pair rated more at fault than the
matched opposite-gender pair for the identical scenario** -- mirrors
BBQ/KoBBQ's own convention of defining bias relative to the socially
disadvantaged category for that axis, and mirrors this project's existing
agent-gender diff-bias convention (biased = male agent rated more at
fault, matching that finding's actual direction).

### Section D (item 5d) -- cross-model agreement + confidence by orientation

Restrict the existing cross-model-agreement logic in
`analyze_fault_rating_bias.py` (pairwise Pearson r between models'
`fault_rating` on matching `vignette_id`s) to opposite-gender-config rows
and same-gender-config rows separately, report each bucket's mean pairwise
r. Separately, mean `confidence` in each bucket via Welch t (matching this
project's existing Welch-t helper).

### Section E (item 5e) -- family x orientation interaction (exploratory)

Reuses the existing family-omnibus permutation-test machinery
(`permutation_omnibus_test`/`one_way_anova_F`, already implemented and
correct for this genuinely between-subjects-across-families use case --
unlike the identity-effect omnibus tests, this one is not a repeated-
measures design, since family is a between-groups label over independent
pairs), applied to the same-gender-vs-opposite-gender per-cell diffs from
Section A, with family as the grouping label -- rebuilt here (a few lines,
matching this project's per-script-duplication convention) rather than
imported from the sibling script. **Explicitly reported as an exploratory
lead, not a confirmatory claim** -- the plan's own text already flags this
as likely underpowered, consistent with how every other underpowered
interaction in this project has been handled (ambivalent-sexism contrast,
original family/model/source omnibus).

### Output

`analysis/orientation_effect_findings.md`.

## Part 2: item 5f -- pairing structure (identity-sharing x NB-involvement)

### Scope

One new script, `scripts/analyze_pairing_structure_effect.py` -- separate
from Part 1's script, because this is a genuinely different research
question (structural gender-normativity, explicitly not orientation) with
a different scope (all 9 configs, not just MF/FM/MM/FF). Naming
deliberately avoids "orientation" language.

### The four groups

All 9 configs partition into exactly four mutually exclusive groups,
crossing two real structural properties -- **identity-sharing** (does the
pairing have one shared gender identity or two different ones?) and
**binary-involvement** (does either partner identify as NB?):

| | Different identity | Same identity |
|---|---|---|
| **Binary only** | opposite-binary: MF, FM | same-binary: MM, FF |
| **NB-involved** | NB-mixed: NBM, NBF, MNB, FNB | NB-NB: NBNB |

This is a full 2x2 factorial, not an arbitrary bucketing -- every group is
defined by an objective property of the configuration (whether the two
roles' genders match, and whether either role is NB), not by a social
inference about the pairing.

**Why NB-NB cannot be pooled with NB-mixed** (the mistake this design
avoids): NB-NB is a same-identity pairing, structurally identical in kind
to MM/FF; NB-mixed pairings are different-identity pairings, structurally
identical in kind to MF/FM. Pooling NB-NB with NB-mixed under one
"NB-involving" label would put a same-identity pairing in with
different-identity pairings -- the same category error Part 1 avoids by
not folding NB into orientation at all.

### Per-cell group means

For each `(scenario_id, severity, model)` cell, compute up to four
per-cell means: `opposite_binary_mean` (avg of MF/FM rows present),
`same_binary_mean` (avg of MM/FF), `nb_mixed_mean` (avg of whichever of
NBM/NBF/MNB/FNB are present), `nbnb_mean` (the single NBNB row, if
present). A cell only contributes to a given test if all groups that test
needs are present.

### Three tests, each reusing existing or trivially-extended machinery

**Main effect 1 -- identity-sharing** (different vs. same, pooled over
binary-involvement): per cell, `different_identity_mean = mean(
opposite_binary_mean, nb_mixed_mean)` and `same_identity_mean = mean(
same_binary_mean, nbnb_mean)` -- **averaging the two subgroup means, not
row-count-weighting them**, so the 4-config NB-mixed group doesn't
outweigh the 2-config opposite-binary group in this coarser main-effect
view. Diff per cell = `different_identity_mean - same_identity_mean`.

**Main effect 2 -- binary-involvement** (binary-only vs. NB-involved,
pooled over identity-sharing): per cell, `binary_only_mean = mean(
opposite_binary_mean, same_binary_mean)`, `nb_involved_mean = mean(
nb_mixed_mean, nbnb_mean)`. Diff per cell = `nb_involved_mean -
binary_only_mean`.

**Interaction -- does the identity-sharing effect differ between
binary-only and NB-involved pairings?** Per cell: `diff_binary_only =
same_binary_mean - opposite_binary_mean`, `diff_nb_involved = nbnb_mean -
nb_mixed_mean`. Interaction quantity per cell = `diff_binary_only -
diff_nb_involved`. Tested as a **paired**, one-sample question (is this
per-cell quantity's mean different from zero?) -- not an unpaired
two-group ANOVA -- because both halves are computed from the *same* cell,
so pairing removes the same between-cell (between-scenario) variance every
other test in this project removes by pairing/differencing. This is the
statistically efficient choice, not just a stylistic one.

All three quantities (two main effects, one interaction) are per-cell
scalars, tested via a new small helper mirroring `paired_stat` but for
already-computed diffs rather than row pairs, plus a **sign-flip
permutation test** (randomly flip each cell's diff's sign, recompute the
mean, compare to the observed mean -- the permutation-test analog of a
one-sample/paired t-test, distribution-free, matching this project's
existing permutation-test-first ethos):

```python
def one_sample_stat(diffs):
    n = len(diffs)
    mean_d = statistics.mean(diffs)
    sd_d = statistics.stdev(diffs) if n > 1 else 0.0
    se_d = sd_d / math.sqrt(n) if n and sd_d > 0 else float("nan")
    t = mean_d / se_d if se_d and not math.isnan(se_d) else float("nan")
    d_z = mean_d / sd_d if sd_d > 0 else float("nan")
    return n, mean_d, sd_d, t, d_z

def sign_flip_test(diffs, n_perm=N_PERMUTATIONS, seed=PERMUTATION_SEED):
    """Permutation test for whether mean(diffs) != 0, via random sign-flips
    -- the permutation analog of a one-sample/paired t-test."""
    obs_mean = statistics.mean(diffs)
    rng = random.Random(seed)
    count_ge = 0
    for _ in range(n_perm):
        flipped = [d if rng.random() < 0.5 else -d for d in diffs]
        if abs(statistics.mean(flipped)) >= abs(obs_mean):
            count_ge += 1
    p = (count_ge + 1) / (n_perm + 1)
    return obs_mean, p
```

Report both the parametric-style `t`/`d_z` (via `one_sample_stat`) and the
permutation p-value (via `sign_flip_test`) for each of the three
quantities -- matching this project's existing convention of always
showing both views (e.g. the ambivalent-sexism contrast reports a plain
diff alongside its permutation-tested F/p).

**This introduces genuinely new methodology to this codebase** (the
sign-flip one-sample permutation test, and the group-of-group-means
aggregation) -- flagged explicitly so the code-quality review pays extra
attention here, the way `cell_centered_omnibus`'s within-cell-shuffle logic
needed a real review pass (and a real fix, commit `80b75db`) before it was
trustworthy.

### Deriving flatter comparisons later, for free

The four groups are the finest-grained partition of all 9 configs, so any
coarser grouping a shorter paper draft might want later (e.g. a flat
"conventional vs. everything else" 2-group split) is just a re-pooling of
the same four groups' already-computed per-cell means -- no new data, no
new pairing logic, computed at write-up time from numbers this script
already produces. Not built in this pass (YAGNI -- build it if and when a
specific flatter framing is actually needed for the paper draft), but
noted here so it's clear the finer-grained version doesn't foreclose it.

### Output

`analysis/pairing_structure_effect_findings.md`.

## Documentation and tracking

- README entries for both new scripts, matching every prior script's
  bullet style.
- `docs/planned_analysis.md`: mark items 5a-5e implemented with results
  once run; add a new tracked item 5f (pairing structure) with its own
  entry and summary-table row, explicitly noting it is not an orientation
  analysis.

## Testing / verification

Matches this codebase's convention: run end-to-end, sanity-check output
(no NaN, plausible n values). For item 5f specifically, given the new
methodology: additionally verify by hand-checking one cell's arithmetic
(pick one `(scenario_id, severity, model)` cell with all 9 configs
present, manually compute the four group means and the three derived
quantities, confirm they match the script's output) before trusting the
aggregate results -- a targeted correctness check appropriate to genuinely
new logic, not a full test suite.
