# Identity Effects By Family Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `scripts/analyze_identity_effect_by_family.py`, which adds a per-family descriptive breakdown and a formal family-moderation test to all 9 comparisons across items 2/3/4 (agent-identity, partner-identity, same-identity), plus a synthesis section testing whether NB-related bias concentrates in the same relationship domains as the already-established binary bias, per `docs/superpowers/specs/2026-08-21-identity-effect-by-family-design.md`.

**Architecture:** One new script, self-contained per this codebase's per-script-duplication convention (recomputes cell structures rather than importing from the sibling scripts). Reuses proven helpers verbatim: `paired_stat`/`sign_breakdown` (descriptive stats), `one_way_anova_F` + the **global-shuffle** `permutation_omnibus_test` (the pattern already correct in `analyze_fault_rating_bias.py` for a between-groups question -- deliberately NOT the within-cell-shuffle `cell_centered_omnibus` pattern used elsewhere, which would be the wrong tool here), and the three cell-builders from the two sibling identity-effect scripts.

**Tech Stack:** Python 3.11 stdlib only (`csv`, `glob`, `math`, `os`, `random`, `statistics`, `collections.defaultdict`) -- no new dependencies.

---

## Verification approach

No unit-test suite exists for this codebase's analysis scripts (matches existing convention). Verification: run end-to-end, sanity-check per-family `n` values against the already-computed power audit (item 2/3 comparisons: ~210-220/family; item 4 comparisons: ~68-75/family), and cross-check one comparison's overall numbers against its already-committed sibling finding (e.g. this script's own agent-identity M-F comparison, pooled across all 9 families, should reproduce `analysis/agent_identity_effect_findings.md`'s Section A M-F result exactly, since it's the same underlying pairs just also broken out by family).

## Task 1: Build and run the script

**Files:**
- Create: `scripts/analyze_identity_effect_by_family.py`

- [ ] **Step 1: Write the complete script**

```python
"""Identity effects by relationship-norm family -- adds a per-family
breakdown to all 9 comparisons across items 2/3/4 (agent-identity,
partner-identity, same-identity), none of which have one yet (each
sibling script explicitly flags this as out of scope in its own
docstring). Answers the genuinely new question: does NB-related bias
concentrate in the same relationship domains as the already-established
binary bias (RQ2, docs/planned_analysis.md Section 6), or different ones?

Nine comparisons, three axes, each already established elsewhere without
a family breakdown -- this script adds only the family stratification, no
new pairwise logic:

- Agent-identity (item 2): M-F, M-NB, F-NB, partner held constant.
- Partner-identity (item 3): M-F, M-NB, F-NB, agent held constant.
- Same-identity (item 4): MM-FF, MM-NBNB, FF-NBNB.

For each comparison: (1) a descriptive per-family table (mean diff, t,
d_z, diff-bias -- mirrors analyze_fault_rating_bias.py's existing
per-family breakdown exactly), and (2) a formal family-moderation test.

The moderation test uses the GLOBAL-shuffle permutation_omnibus_test
pattern (same as analyze_fault_rating_bias.py's family/model moderation
test) -- NOT the within-cell-shuffle cell_centered_omnibus pattern used in
analyze_agent_identity_effect.py/analyze_partner_identity_effect.py for
their 3-level repeated-measures omnibus tests. This distinction matters:
"does family moderate a 2-way pairwise diff's size" is a genuine
between-groups question (each family's pairs are independent of every
other family's), so the simple global shuffle is the correct null-
distribution construction here -- reusing the within-cell-shuffle logic
instead would be applying the wrong tool, the same class of error commit
`80b75db` fixed in the other direction (a global shuffle being wrong for a
repeated-measures question).

Also includes a freshly-recomputed reference: the plain binary M-F effect
by family (matches analyze_fault_rating_bias.py's own per-family
breakdown) -- recomputed here rather than imported, so the synthesis
section below always compares against a live number, never a hardcoded
one that could go stale if the sibling script's data changes.

Power caveat, stated explicitly per the design spec: item 2/3's
comparisons have ~210-220 pairs/family (well-powered, comparable to or
better than the original RQ2 test). Item 4's comparisons have ~68-75
pairs/family (meaningfully thinner) -- reported descriptively, flagged as
likely underpowered for a full 9-way split, not omitted and not oversold.

Usage: python scripts/analyze_identity_effect_by_family.py
Reads:  responses/confirmatory/*.csv
Writes: analysis/identity_effect_by_family_findings.md
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
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "identity_effect_by_family_findings.md")

GENDERS = ("M", "F", "NB")
PAIR_ORDER = [("M", "F"), ("M", "NB"), ("F", "NB")]


def load_responses():
    rows = []
    for f in sorted(glob.glob(RESPONSES_GLOB)):
        with open(f) as fh:
            for row in csv.DictReader(fh):
                row["fault_rating"] = float(row["fault_rating"])
                rows.append(row)
    return rows


def build_cells(rows):
    """(scenario_id, severity, model) -> {(agent_gender, partner_gender): row}"""
    cells = defaultdict(dict)
    for r in rows:
        key = (r["scenario_id"], r["severity"], r["model"])
        cells[key][(r["agent_gender"], r["partner_gender"])] = r
    return cells


def build_partner_held_cells(cells):
    """(scenario_id, severity, model, partner_gender) -> {agent_gender: row}
    -- from analyze_agent_identity_effect.py, used here for the agent-
    identity (item 2) axis."""
    out = defaultdict(dict)
    for (scenario_id, severity, model), sub in cells.items():
        for (agent_gender, partner_gender), row in sub.items():
            out[(scenario_id, severity, model, partner_gender)][agent_gender] = row
    return out


def build_agent_held_cells(cells):
    """(scenario_id, severity, model, agent_gender) -> {partner_gender: row}
    -- from analyze_partner_identity_effect.py, used here for the partner-
    identity (item 3) axis."""
    out = defaultdict(dict)
    for (scenario_id, severity, model), sub in cells.items():
        for (agent_gender, partner_gender), row in sub.items():
            out[(scenario_id, severity, model, agent_gender)][partner_gender] = row
    return out


def build_same_identity_cells(cells):
    """(scenario_id, severity, model) -> {identity: row} where
    agent_gender == partner_gender == identity -- from
    analyze_agent_identity_effect.py, used here for the same-identity
    (item 4) axis."""
    out = {}
    for key, sub in cells.items():
        d = {g: sub[(g, g)] for g in GENDERS if (g, g) in sub}
        out[key] = d
    return out


def binary_matched_pairs(cells):
    """(M-agent, F-agent) pairs holding partner in {F, M} constant --
    matches analyze_fault_rating_bias.py's matched_pairs() exactly. Used
    only as the reference ranking the synthesis section compares against."""
    pairs = []
    for cell in cells.values():
        for partner in ("F", "M"):
            m_row = cell.get(("M", partner))
            f_row = cell.get(("F", partner))
            if m_row is not None and f_row is not None:
                pairs.append((m_row, f_row))
    return pairs


def pairwise(cell_dict, g1, g2):
    """(row_g1, row_g2) pairs across all extended cells where both g1 and g2
    are present."""
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
    use case as analyze_fault_rating_bias.py's family/model omnibus). Do
    NOT confuse with cell_centered_omnibus (the sibling scripts' within-
    cell-shuffle pattern for repeated-measures questions) -- that would be
    the wrong tool for this question."""
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


def pearson(xs, ys):
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else float("nan")


def spearman_rank_corr(family_values_a, family_values_b):
    """Spearman rank correlation between two family->mean_diff dicts
    covering the same set of families."""
    families = sorted(family_values_a.keys())
    order_a = sorted(families, key=lambda f: -family_values_a[f])
    order_b = sorted(families, key=lambda f: -family_values_b[f])
    ranks_a = {fam: r for r, fam in enumerate(order_a, 1)}
    ranks_b = {fam: r for r, fam in enumerate(order_b, 1)}
    xs = [ranks_a[f] for f in families]
    ys = [ranks_b[f] for f in families]
    return pearson(xs, ys)


def write_family_breakdown(out, pairs, label1, label2, power_caveat=None):
    """Writes a per-family descriptive table plus a formal family-
    moderation test for one comparison. Returns {family_name: mean_diff}
    for use in the synthesis section."""
    out.append(f"### {label1} vs {label2}\n")
    if power_caveat:
        out.append(f"*{power_caveat}*\n")
    by_family = defaultdict(list)
    for r1, r2 in pairs:
        by_family[r1["family_name"]].append((r1, r2))
    fam_stats = {}
    for fam, fam_pairs in by_family.items():
        n, mean_d, sd_d, t, d_z = paired_stat(fam_pairs)
        n_pos, n_neg, n_tie, z, diff_bias = sign_breakdown(fam_pairs)
        fam_stats[fam] = (n, mean_d, t, d_z, diff_bias)
    out.append("| Family | n | mean diff | t | d_z | diff-bias |")
    out.append("|---|---|---|---|---|---|")
    for fam in sorted(fam_stats, key=lambda f: -fam_stats[f][1]):
        n, mean_d, t, d_z, diff_bias = fam_stats[fam]
        out.append(f"| {fam} | {n} | {mean_d:+.3f} | {t:+.2f} | {d_z:+.3f} | {diff_bias:+.4f} |")
    out.append("")

    fam_labels = [r1["family_name"] for r1, r2 in pairs]
    diffs = [r1["fault_rating"] - r2["fault_rating"] for r1, r2 in pairs]
    F, df1, df2, p = permutation_omnibus_test(fam_labels, diffs)
    sig = "reaches" if p < 0.05 else "does not reach"
    out.append(f"Family moderation test: F({df1},{df2})={F:.3f}, permutation p={p:.4f} "
                f"-- {sig} conventional significance.\n")
    return {fam: v[1] for fam, v in fam_stats.items()}


def main():
    rows = load_responses()
    cells = build_cells(rows)
    partner_held_cells = build_partner_held_cells(cells)
    agent_held_cells = build_agent_held_cells(cells)
    same_identity_cells = build_same_identity_cells(cells)

    out = []
    out.append("# Identity effects by relationship-norm family findings\n")
    out.append(f"Generated from `responses/confirmatory/*.csv` (n={len(rows)} rows). "
                f"Regenerate via `python scripts/analyze_identity_effect_by_family.py`. "
                "Adds a per-family breakdown to all 9 comparisons across items 2/3/4 "
                "(`analysis/agent_identity_effect_findings.md`, "
                "`analysis/partner_identity_effect_findings.md`), none of which have "
                "one yet. See this script's docstring and "
                "`docs/superpowers/specs/2026-08-21-identity-effect-by-family-design.md` "
                "for full methodology.\n")

    rankings = {}

    out.append("## Reference: binary M-F agent-gender effect by family\n")
    out.append("Recomputed here (not imported) to guarantee the synthesis section below "
                "always compares against a live number, not a hardcoded one that could "
                "go stale. Matches `analysis/fault_rating_bias_findings.md`'s existing "
                "per-family breakdown.\n")
    ref_pairs = binary_matched_pairs(cells)
    ref_ranking = write_family_breakdown(out, ref_pairs, "M", "F")
    rankings["Reference (binary M-F)"] = ref_ranking

    out.append("## Axis 1: agent-identity effect by family (item 2, partner held constant)\n")
    for g1, g2 in PAIR_ORDER:
        pairs = pairwise(partner_held_cells, g1, g2)
        rankings[f"Agent-identity {g1} vs {g2}"] = write_family_breakdown(out, pairs, g1, g2)

    out.append("## Axis 2: partner-identity effect by family (item 3, agent held constant)\n")
    for g1, g2 in PAIR_ORDER:
        pairs = pairwise(agent_held_cells, g1, g2)
        rankings[f"Partner-identity {g1} vs {g2}"] = write_family_breakdown(out, pairs, g1, g2)

    out.append("## Axis 3: same-identity relationships by family (item 4)\n")
    thin_power_note = ("Power note: same-identity cells don't pool across a third held-"
                        "constant role the way Axes 1-2 do, so per-family n here is "
                        "meaningfully thinner (~68-75/family vs. ~210-220/family for "
                        "Axes 1-2) -- likely underpowered for a full 9-way split. "
                        "Reported descriptively, not as a confirmatory claim.")
    for g1, g2 in PAIR_ORDER:
        pairs = pairwise(same_identity_cells, g1, g2)
        label1, label2 = f"{g1}{g1}", f"{g2}{g2}"
        rankings[f"Same-identity {label1} vs {label2}"] = write_family_breakdown(
            out, pairs, label1, label2, power_caveat=thin_power_note)

    out.append("## Synthesis: does the NB-related bias concentrate in the same domains as the binary bias?\n")
    ref_top3 = sorted(ref_ranking, key=lambda f: -ref_ranking[f])[:3]
    out.append(f"Reference top-3 families by binary M-F effect size: {', '.join(ref_top3)}.\n")
    out.append("| Comparison | Spearman rank correlation vs. reference | Top-3 families | Top-3 overlap with reference |")
    out.append("|---|---|---|---|")
    for label, fam_vals in rankings.items():
        if label == "Reference (binary M-F)":
            continue
        rho = spearman_rank_corr(ref_ranking, fam_vals)
        top3 = sorted(fam_vals, key=lambda f: -fam_vals[f])[:3]
        overlap = len(set(top3) & set(ref_top3))
        out.append(f"| {label} | {rho:+.3f} | {', '.join(top3)} | {overlap}/3 |")
    out.append("")
    out.append("**Interpretation guidance**: a high positive Spearman correlation and "
                "substantial top-3 overlap would suggest the NB-related and binary "
                "biases share a common underlying domain-sensitivity mechanism; low "
                "or negative correlation would suggest the NB-related bias has its own, "
                "distinct pattern across relationship domains, not explained by "
                "\"wherever the binary bias is big, the NB bias is too.\"\n")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_identity_effect_by_family.py`
Expected: exits 0, prints `Wrote .../analysis/identity_effect_by_family_findings.md`. This runs 10 global-shuffle permutation tests (much cheaper than the sibling scripts' within-cell-shuffle omnibus tests -- expect well under a minute total).

- [ ] **Step 3: Sanity-check per-family n values**

Run:
```bash
python3 -c "
import re
with open('analysis/identity_effect_by_family_findings.md') as f:
    text = f.read()
assert not re.search(r'\bnan\b', text, re.IGNORECASE), 'found a NaN in the output'
assert text.count('Family moderation test') == 10, f'expected 10 moderation tests (1 reference + 9 comparisons), found {text.count(\"Family moderation test\")}'
print('basic sanity checks passed')
"
```
Expected: `basic sanity checks passed`. Then read `analysis/identity_effect_by_family_findings.md` directly and confirm: Axis 1/2 tables show per-family `n` in the 210-220 range; Axis 3 tables show per-family `n` in the 68-75 range. If either range is off by a large factor, stop and investigate the relevant cell-builder before proceeding.

- [ ] **Step 4: Cross-check one comparison against its already-committed sibling result**

Run: `grep -A3 "Reference: binary M-F" analysis/identity_effect_by_family_findings.md`

This won't show an "overall" pooled number directly (the table is per-family) -- instead, manually verify consistency by computing the pair-count-weighted average of the reference table's per-family `mean diff` column and confirming it's close to `analysis/fault_rating_bias_findings.md`'s headline M-F mean diff (currently +0.153 on the 4-model post-exclusion dataset). They won't be identical (this script's `binary_matched_pairs` recomputes independently), but should be very close since it's the same underlying data and pairing logic. If they diverge substantially, there's a bug in `binary_matched_pairs` or `build_cells` -- stop and investigate.

- [ ] **Step 5: Read the synthesis table and note the actual finding**

Read the "Synthesis" section's table. This is the actual deliverable of this whole analysis -- record (for your task report) which comparisons show high positive Spearman correlation / high top-3 overlap with the reference (suggesting shared domain-sensitivity) and which show low/negative correlation (suggesting the NB-related pattern has its own domain structure). Don't just confirm the table rendered -- read what it says.

- [ ] **Step 6: Commit**

```bash
git add scripts/analyze_identity_effect_by_family.py analysis/identity_effect_by_family_findings.md
git commit -m "$(cat <<'EOF'
Add per-family breakdown for all identity-effect comparisons (items 2/3/4)

Adds descriptive per-family stats + a formal family-moderation test
(correctly using the global-shuffle permutation pattern, not the
within-cell-shuffle one used elsewhere for repeated-measures
questions) to all 9 agent-identity/partner-identity/same-identity
comparisons, none of which had a family breakdown before. Adds a
synthesis section (Spearman rank correlation + top-3 overlap) testing
whether NB-related bias concentrates in the same relationship domains
as the already-established binary bias.
EOF
)"
```

## Task 2: Document and update tracking

**Files:**
- Modify: `README.md` (Analysis section)
- Modify: `docs/planned_analysis.md`

- [ ] **Step 1: Add a README entry**

In the `## Analysis` section of `README.md`, after the `scripts/analyze_partner_identity_effect.py` bullet, insert:
```markdown
- **`scripts/analyze_identity_effect_by_family.py`** -- reads
  `responses/confirmatory/*.csv`, adds a per-family descriptive breakdown
  and formal family-moderation test to all 9 comparisons across
  `analyze_agent_identity_effect.py` and `analyze_partner_identity_effect.py`
  (agent-identity, partner-identity, same-identity), plus a synthesis
  section testing whether NB-related bias concentrates in the same
  relationship domains as the established binary bias. Writes
  `analysis/identity_effect_by_family_findings.md`. See
  `docs/superpowers/specs/2026-08-21-identity-effect-by-family-design.md`.
```

- [ ] **Step 2: Add a new tracked item to `docs/planned_analysis.md`**

Before editing, get the real synthesis-table values from Task 1 Step 5's notes. Add a new subsection right after item 4's bullet list in Section 4 ("Same-identity controls") of `docs/planned_analysis.md`, titled `## 4b. Per-family breakdown of items 2/3/4 (agent-identity, partner-identity, same-identity)`, with: a short motivation paragraph (matching this file's existing prose style, referencing the RQ2 domain-heterogeneity finding and explaining this extends it to the NB axis), the actual Spearman/top-3-overlap findings from the synthesis table, and a `**[implemented] 2026-08-21**, `scripts/analyze_identity_effect_by_family.py`` marker.

- [ ] **Step 3: Add a new row to the summary table**

Add a new row to the summary table near the bottom of `docs/planned_analysis.md`, after item 4's row (or after item 13's row if item 4 doesn't have its own row -- check first with `grep -n "^| 4 |" docs/planned_analysis.md`; if there's no existing row for item 4, add this as a new row anywhere after item 4/13):

```
| 4b | Per-family breakdown of items 2/3/4 (agent-identity, partner-identity, same-identity) | No -- existing data sufficient | **implemented 2026-08-21**, `scripts/analyze_identity_effect_by_family.py` -- [insert the actual Spearman correlation / top-3-overlap summary from Task 1 Step 5's notes]. |
```

Replace the bracketed instruction with the real finding text -- do not leave literal brackets in the committed file.

- [ ] **Step 4: Commit**

```bash
git add README.md docs/planned_analysis.md
git commit -m "Document analyze_identity_effect_by_family.py and add item 4b to the tracked backlog"
```
