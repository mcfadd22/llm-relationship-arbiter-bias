# Presumed Orientation Effect (Items 5a-5e) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `scripts/analyze_orientation_effect.py`, testing whether the *same* violation gets judged differently depending on whether the couple reads as opposite-gender (MF/FM, presumed heterosexual) or same-gender (MM/FF, presumed gay/lesbian) -- items 5a-5e of `docs/planned_analysis.md`, per `docs/superpowers/specs/2026-08-21-orientation-and-pairing-structure-design.md`.

**Architecture:** One new script with five sections sharing a common per-cell grouping (opposite-gender: MF+FM pooled; same-gender: MM+FF pooled), reusing this project's existing paired-differencing and permutation-test machinery throughout. **NB-involving configs are excluded entirely** -- that's a deliberate, already-approved scope boundary (see the spec's Motivation section), not an oversight; the corresponding non-orientation question covering all 9 configs is a separate script (item 5f, planned separately).

**Tech Stack:** Python 3.11 stdlib only (`csv`, `glob`, `math`, `os`, `random`, `statistics`, `collections.defaultdict`) -- no new dependencies, matches every sibling `analyze_*.py` script except `analyze_reasoning_text.py`.

---

## Verification approach

No unit-test suite exists for this codebase's analysis scripts (matches existing convention). Verification is: run end-to-end, sanity-check output (no NaN, plausible `n` values -- Section A/C's ~810 cells should match the scale of the existing MM-vs-FF same-gender control in `analysis/fault_rating_bias_findings.md`).

## Task 1: Build and run the orientation-effect script

**Files:**
- Create: `scripts/analyze_orientation_effect.py`

- [ ] **Step 1: Write the complete script**

```python
"""Presumed relationship orientation (items 5a-5e, docs/planned_analysis.md
Section 5) -- does the *same* violation get judged differently depending
on whether the couple reads as opposite-gender (MF/FM, presumed
heterosexual) or same-gender (MM/FF, presumed gay/lesbian)?

**NB-involving configs are excluded entirely from this script.** A
nonbinary person paired with anyone could hold any orientation -- there is
no stable cultural default reading of an NB-involving pairing the way
there arguably is (even if only "presumed," see the terminology note in
docs/planned_analysis.md Section 5) for MM/FF. Folding NB into an
orientation proxy would be a category error, not "beyond binary"
engagement. The corresponding non-orientation question -- does the pairing
depart from the default two-different-binary-genders script at all,
covering all 9 configs -- is a separate, explicitly-not-orientation
analysis: see scripts/analyze_pairing_structure_effect.py (item 5f).

Five sections, sharing one grouping variable (opposite-gender: MF+FM
pooled per cell; same-gender: MM+FF pooled per cell) and reusing this
project's existing paired-differencing/permutation-test machinery
throughout:

(a) Section A: absolute fault_rating level by orientation, independent of
    which agent is blamed.
(b) Section B: matched partner-as-orientation test, holding agent gender
    constant at a single value (not pooled) -- the mirror-image structure
    of scripts/analyze_partner_identity_effect.py's agent-held-constant
    design, restricted to a single agent value per test instead of pooling
    across all three.
(c) Section C: BBQ/KoBBQ-style diff-bias score for this axis. Bias
    direction: "biased" = same-gender pair rated more at fault than the
    matched opposite-gender pair -- mirrors BBQ/KoBBQ's convention of
    defining bias relative to the socially disadvantaged category, and
    this project's own agent-gender diff-bias convention (positive =
    the theoretically-relevant biased direction).
(d) Section D: cross-model agreement and mean confidence, split by
    orientation category.
(e) Section E: exploratory family x orientation interaction -- likely
    underpowered per docs/planned_analysis.md's own framing; reported as a
    descriptive lead, not a confirmatory claim, consistent with every
    other underpowered interaction in this project.

Pair-ordering convention (Sections A, B): the same-gender/same-identity
row or pseudo-row is always passed FIRST to paired_stat/sign_breakdown/
write_comparison_block, so diff-bias reads positive = same-gender-favored
= "biased" per (c) above, without an inverted sign anywhere.

Usage: python scripts/analyze_orientation_effect.py
Reads:  responses/confirmatory/*.csv
Writes: analysis/orientation_effect_findings.md
"""

import csv
import glob
import math
import os
import random
import statistics
from collections import defaultdict

N_PERMUTATIONS = 20000
PERMUTATION_SEED = 42

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_GLOB = os.path.join(REPO_ROOT, "responses", "confirmatory", "*.csv")
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "orientation_effect_findings.md")


def load_responses():
    rows = []
    for f in sorted(glob.glob(RESPONSES_GLOB)):
        with open(f) as fh:
            for row in csv.DictReader(fh):
                row["fault_rating"] = float(row["fault_rating"])
                row["confidence"] = float(row["confidence"])
                rows.append(row)
    return rows


def build_cells(rows):
    """(scenario_id, severity, model) -> {(agent_gender, partner_gender): row}"""
    cells = defaultdict(dict)
    for r in rows:
        key = (r["scenario_id"], r["severity"], r["model"])
        cells[key][(r["agent_gender"], r["partner_gender"])] = r
    return cells


def build_agent_held_cells(cells):
    """(scenario_id, severity, model, agent_gender) -> {partner_gender: row}."""
    out = defaultdict(dict)
    for (scenario_id, severity, model), sub in cells.items():
        for (agent_gender, partner_gender), row in sub.items():
            out[(scenario_id, severity, model, agent_gender)][partner_gender] = row
    return out


def pairwise(cell_dict, g1, g2):
    pairs = []
    for sub in cell_dict.values():
        r1, r2 = sub.get(g1), sub.get(g2)
        if r1 is not None and r2 is not None:
            pairs.append((r1, r2))
    return pairs


def paired_stat(pairs, key="fault_rating"):
    diffs = [a[key] - b[key] for a, b in pairs]
    n = len(diffs)
    mean_d = statistics.mean(diffs)
    sd_d = statistics.stdev(diffs) if n > 1 else 0.0
    se_d = sd_d / math.sqrt(n) if n and sd_d > 0 else float("nan")
    t = mean_d / se_d if se_d and not math.isnan(se_d) else float("nan")
    d_z = mean_d / sd_d if sd_d > 0 else float("nan")
    return n, mean_d, sd_d, t, d_z


def sign_breakdown(pairs, key="fault_rating"):
    n = len(pairs)
    n_pos = sum(1 for a, b in pairs if a[key] > b[key])
    n_neg = sum(1 for a, b in pairs if a[key] < b[key])
    n_tie = n - n_pos - n_neg
    denom = n_pos + n_neg
    z = (n_pos - denom / 2) / math.sqrt(denom * 0.25) if denom > 0 else float("nan")
    diff_bias = (n_pos - n_neg) / n if n else float("nan")
    return n_pos, n_neg, n_tie, z, diff_bias


def write_comparison_block(out, pairs, label1, label2):
    n, mean_d, sd_d, t, d_z = paired_stat(pairs)
    n_pos, n_neg, n_tie, z, diff_bias = sign_breakdown(pairs)
    out.append(f"**{label1} vs {label2}**: n={n} pairs, mean diff ({label1}-{label2})="
                f"{mean_d:+.3f}, paired t={t:.2f}, d_z={d_z:.3f}.")
    ratio = f"{n_pos/n_neg:.2f}:1" if n_neg else "undefined (0 in denominator)"
    out.append(f"Sign breakdown: {n_tie} ties ({n_tie/n*100:.1f}%), {label1}>{label2} in "
                f"{n_pos}, {label2}>{label1} in {n_neg} (ratio {ratio}, sign-test "
                f"z={z:.2f}). Diff-bias = ({n_pos} - {n_neg}) / {n} = {diff_bias:+.4f}.\n")


def one_way_anova_F(labels, values):
    groups = defaultdict(list)
    for l, v in zip(labels, values):
        groups[l].append(v)
    k = len(groups)
    n = len(values)
    grand = statistics.mean(values)
    group_means = {l: statistics.mean(g) for l, g in groups.items()}
    ss_between = sum(len(g) * (group_means[l] - grand) ** 2 for l, g in groups.items())
    ss_within = sum(sum((x - group_means[l]) ** 2 for x in g) for l, g in groups.items())
    df_between = k - 1
    df_within = n - k
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    F = ms_between / ms_within if ms_within > 0 else float("inf")
    return F, df_between, df_within


def permutation_omnibus_test(labels, values, n_perm=N_PERMUTATIONS, seed=PERMUTATION_SEED):
    """Label-shuffle permutation test -- correct here because family is a
    genuine between-subjects grouping label over independent pairs (same
    use case as analyze_fault_rating_bias.py's family/model omnibus, not
    the repeated-measures case that needed a within-cell-restricted
    shuffle in analyze_agent_identity_effect.py)."""
    F_obs, df1, df2 = one_way_anova_F(labels, values)
    rng = random.Random(seed)
    shuffled = list(labels)
    count_ge = 0
    for _ in range(n_perm):
        rng.shuffle(shuffled)
        F_perm, _, _ = one_way_anova_F(shuffled, values)
        if F_perm >= F_obs:
            count_ge += 1
    p = (count_ge + 1) / (n_perm + 1)
    return F_obs, df1, df2, p


def welch_t(xs, ys):
    n1, n2 = len(xs), len(ys)
    m1, m2 = statistics.mean(xs), statistics.mean(ys)
    s1, s2 = statistics.stdev(xs), statistics.stdev(ys)
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    t = (m1 - m2) / se if se > 0 else float("nan")
    return t, m1 - m2


def pearson(xs, ys):
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else float("nan")


def orientation_bucket_means(cells):
    """(scenario_id, severity, model) -> (opposite_mean, same_mean, family_name)
    for cells with at least one row in each of the opposite-gender
    ({MF,FM}) and same-gender ({MM,FF}) buckets."""
    out = {}
    for key, sub in cells.items():
        opposite_rows = [sub[c] for c in (("M", "F"), ("F", "M")) if c in sub]
        same_rows = [sub[c] for c in (("M", "M"), ("F", "F")) if c in sub]
        if not opposite_rows or not same_rows:
            continue
        opposite_mean = statistics.mean(r["fault_rating"] for r in opposite_rows)
        same_mean = statistics.mean(r["fault_rating"] for r in same_rows)
        family_name = opposite_rows[0]["family_name"]
        out[key] = (opposite_mean, same_mean, family_name)
    return out


def main():
    rows = load_responses()
    cells = build_cells(rows)
    agent_held_cells = build_agent_held_cells(cells)
    bucket_means = orientation_bucket_means(cells)

    out = []
    out.append("# Presumed relationship orientation (items 5a-5e) findings\n")
    out.append(f"Generated from `responses/confirmatory/*.csv` (n={len(rows)} rows). "
                f"Regenerate via `python scripts/analyze_orientation_effect.py`. "
                "Covers opposite-gender (MF+FM, presumed heterosexual) vs. same-gender "
                "(MM+FF, presumed gay/lesbian) pairs only -- NB-involving configs are "
                "deliberately excluded from this orientation axis; see this script's "
                "docstring and `docs/superpowers/specs/"
                "2026-08-21-orientation-and-pairing-structure-design.md` for why, and "
                "see `analysis/pairing_structure_effect_findings.md` (item 5f) for the "
                "separate, explicitly-non-orientation question covering all 9 configs.\n")

    out.append("## Section A (item 5a): absolute fault_rating level by orientation\n")
    out.append("Per (scenario, severity, model) cell: mean fault_rating of the "
                "same-gender bucket (MM+FF rows) vs. the opposite-gender bucket "
                "(MF+FM rows), paired by cell, independent of which agent is blamed.\n")
    pairs_a = [({"fault_rating": same}, {"fault_rating": opp}) for opp, same, fam in bucket_means.values()]
    write_comparison_block(out, pairs_a, "same-gender", "opposite-gender")

    out.append("## Section B (item 5b): matched partner-as-orientation test\n")
    out.append("Holds agent gender constant at a single value (not pooled across all "
                "three, unlike the agent-/partner-identity scripts): agent=M, partner=F "
                "(MF, opposite) vs. partner=M (MM, same); agent=F, partner=M (FM, "
                "opposite) vs. partner=F (FF, same).\n")
    agent_m_cells = {k: v for k, v in agent_held_cells.items() if k[3] == "M"}
    agent_f_cells = {k: v for k, v in agent_held_cells.items() if k[3] == "F"}
    out.append("**Agent=M held constant**:")
    write_comparison_block(out, pairwise(agent_m_cells, "M", "F"), "partner=M (same)", "partner=F (opposite)")
    out.append("**Agent=F held constant**:")
    write_comparison_block(out, pairwise(agent_f_cells, "F", "M"), "partner=F (same)", "partner=M (opposite)")

    out.append("## Section C (item 5c): orientation diff-bias score\n")
    out.append("Adapted from the same BBQ/KoBBQ ambiguous-context formula used "
                "throughout this project (see `analysis/fault_rating_bias_findings.md`). "
                "\"Biased\" = same-gender pair rated more at fault than the matched "
                "opposite-gender pair for the identical scenario (mirrors BBQ/KoBBQ's "
                "convention of defining bias relative to the socially disadvantaged "
                "category for this axis). Reuses Section A's per-cell diffs.\n")
    n_pos, n_neg, n_tie, z, diff_bias = sign_breakdown(pairs_a)
    out.append(f"Diff-bias = ({n_pos} - {n_neg}) / {len(pairs_a)} = {diff_bias:+.4f} "
                f"(positive = biased toward rating same-gender pairs more at fault).\n")

    out.append("## Section D (item 5d): cross-model agreement and confidence by orientation\n")
    out.append("Restricts this project's existing cross-model fault_rating agreement "
                "logic (pairwise Pearson r between models on matching vignette_id) to "
                "opposite-gender-config rows and same-gender-config rows separately, "
                "plus mean confidence in each bucket (Welch t).\n")
    opposite_rows = [r for r in rows if (r["agent_gender"], r["partner_gender"]) in (("M", "F"), ("F", "M"))]
    same_rows = [r for r in rows if (r["agent_gender"], r["partner_gender"]) in (("M", "M"), ("F", "F"))]
    for label, subset in [("Opposite-gender", opposite_rows), ("Same-gender", same_rows)]:
        by_vm = defaultdict(dict)
        for r in subset:
            by_vm[r["vignette_id"]][r["model"]] = r["fault_rating"]
        models = sorted({r["model"] for r in subset})
        rs = []
        for i in range(len(models)):
            for j in range(i + 1, len(models)):
                m1, m2 = models[i], models[j]
                xs, ys = [], []
                for vid, d in by_vm.items():
                    if m1 in d and m2 in d:
                        xs.append(d[m1])
                        ys.append(d[m2])
                if xs:
                    rs.append(pearson(xs, ys))
        mean_r = statistics.mean(rs) if rs else float("nan")
        mean_conf = statistics.mean(r["confidence"] for r in subset)
        out.append(f"- **{label}**: mean pairwise cross-model r={mean_r:.3f} "
                    f"(over {len(rs)} model pairs), mean confidence={mean_conf:.2f} "
                    f"(n={len(subset)} rows).")
    t_conf, diff_conf = welch_t(
        [r["confidence"] for r in opposite_rows],
        [r["confidence"] for r in same_rows],
    )
    out.append(f"\nConfidence diff (opposite-same)={diff_conf:+.3f}, Welch t={t_conf:.2f}.\n")

    out.append("## Section E (item 5e): family x orientation interaction (exploratory)\n")
    out.append("**Exploratory, likely underpowered** (per `docs/planned_analysis.md`'s "
                "own framing) -- reported as a descriptive lead, not a confirmatory "
                "claim, consistent with every other underpowered interaction in this "
                "project. Reuses the same label-shuffle permutation omnibus test as the "
                "existing family/model heterogeneity tests, applied to Section A's "
                "per-cell (same-opposite) diffs with family as the grouping label.\n")
    fam_labels = [fam for opp, same, fam in bucket_means.values()]
    diffs_e = [same - opp for opp, same, fam in bucket_means.values()]
    F_e, df1_e, df2_e, p_e = permutation_omnibus_test(fam_labels, diffs_e)
    out.append(f"F({df1_e},{df2_e})={F_e:.3f}, permutation p={p_e:.4f} -- "
                f"{'reaches' if p_e < 0.05 else 'does not reach'} conventional "
                "significance (exploratory reading only, not confirmatory).\n")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_orientation_effect.py`
Expected: exits 0, prints `Wrote .../analysis/orientation_effect_findings.md`, and prints the full markdown report to stdout with no tracebacks.

- [ ] **Step 3: Sanity-check the output**

Run:
```bash
python3 -c "
import re
with open('analysis/orientation_effect_findings.md') as f:
    text = f.read()
assert not re.search(r'\bnan\b', text, re.IGNORECASE), 'found a NaN in the output'
assert 'Section A' in text and 'Section B' in text and 'Section C' in text and 'Section D' in text and 'Section E' in text
print('basic sanity checks passed')
print()
print(text[:2500])
"
```
Expected: `basic sanity checks passed`, followed by the report's start. Read the excerpt and confirm Section A's `n` is in the same order of magnitude as the existing MM-vs-FF same-gender control in `analysis/fault_rating_bias_findings.md` (n=810) -- both compare MM/FF-derived quantities across the same ~810 (scenario, severity, model) cells. If it's drastically different, stop and investigate `orientation_bucket_means` before proceeding.

- [ ] **Step 4: Commit**

```bash
git add scripts/analyze_orientation_effect.py analysis/orientation_effect_findings.md
git commit -m "$(cat <<'EOF'
Add presumed-orientation effect analysis (items 5a-5e)

Five sections testing whether the same violation gets judged
differently depending on whether the couple reads as opposite-gender
(MF/FM, presumed heterosexual) or same-gender (MM/FF, presumed
gay/lesbian): absolute level, matched partner-as-orientation test,
BBQ-style diff-bias score, cross-model agreement/confidence split, and
an exploratory family x orientation interaction. NB-involving configs
are deliberately excluded -- see item 5f (separate) for the
non-orientation question covering all 9 configs.
EOF
)"
```

## Task 2: Document and update tracking

**Files:**
- Modify: `README.md` (Analysis section)
- Modify: `docs/planned_analysis.md` (items 5a-5e entries and summary table rows)

- [ ] **Step 1: Add a README entry**

In the `## Analysis` section of `README.md`, after the last existing `analyze_*.py` bullet, insert:
```markdown
- **`scripts/analyze_orientation_effect.py`** -- reads
  `responses/confirmatory/*.csv`, tests whether the same violation is
  judged differently depending on presumed relationship orientation
  (opposite-gender MF/FM vs. same-gender MM/FF; NB-involving configs
  deliberately excluded -- see `analyze_pairing_structure_effect.py` for
  that separate question). Five sections: absolute level, matched
  partner-as-orientation test, diff-bias score, cross-model
  agreement/confidence, exploratory family interaction. Writes
  `analysis/orientation_effect_findings.md`. See
  `docs/superpowers/specs/2026-08-21-orientation-and-pairing-structure-design.md`.
```

- [ ] **Step 2: Update items 5a-5e in `docs/planned_analysis.md`**

Before editing, get the real numbers: run
```bash
grep -A2 "Section A (item 5a)" analysis/orientation_effect_findings.md
grep -A2 "Agent=M held constant" analysis/orientation_effect_findings.md
grep -A2 "Agent=F held constant" analysis/orientation_effect_findings.md
grep "Diff-bias =" analysis/orientation_effect_findings.md
grep -A3 "Section D" analysis/orientation_effect_findings.md
grep "permutation p=" analysis/orientation_effect_findings.md
```
and read off the actual `n=`, `d_z=`, `diff_bias=`, `r=`, and `p=` values printed. **Use those literal numbers in the write-up below -- do not write placeholder text into the file.**

Find Section 5's five sub-bullets in `docs/planned_analysis.md` (the ones starting "**(a) Absolute `fault_rating` level...**" through "**(e) Exploratory: family x orientation-category interaction**") and, after each one's existing `**[needs new code]**` marker, add a sentence reporting that item's actual result using the real values you just read, in the same style already used for items 2, 4, and 7's write-ups elsewhere in this file (state the number, then one sentence of plain-language interpretation).

- [ ] **Step 3: Update the summary table rows for 5a-5e**

Find the five rows for items 5a-5e in the summary table near the bottom of `docs/planned_analysis.md` (each currently reading `| needs new code |` in the last column) and replace each with `**implemented 2026-08-21**, `scripts/analyze_orientation_effect.py`` followed by a short one-line result summary using the real values from Step 2, matching the style already used for items 2, 4, and 7's rows.

- [ ] **Step 4: Commit**

```bash
git add README.md docs/planned_analysis.md
git commit -m "Document analyze_orientation_effect.py and update items 5a-5e's tracked status"
```
