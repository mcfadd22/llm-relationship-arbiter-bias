# Generalized Agent-Identity Effect (M/F/NB) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `scripts/analyze_agent_identity_effect.py`, which generalizes the existing paired M-F `fault_rating` bias test to the full 3x3 crossed gender design `{M, F, NB}` already collected in `responses/confirmatory/*.csv` but never analyzed for the NB level, per `docs/superpowers/specs/2026-08-21-nb-agent-identity-effect-design.md`.

**Architecture:** One self-contained script (matching this codebase's one-script-per-question convention — see `scripts/analyze_fault_rating_bias.py`, `scripts/family_omnibus_power_analysis.py`). It reads the same CSVs, builds cell structures keyed by scenario/severity/model (and derived partner-held / same-identity variants), runs three pairwise paired-difference tests plus one 3-level permutation omnibus per section, and writes `analysis/agent_identity_effect_findings.md`. All interpretive prose is computed from the live p-values (not hardcoded — see commit `a42f7f7`, which fixed two scripts that hardcoded now-wrong significance conclusions).

**Tech Stack:** Python 3.11 stdlib only (`csv`, `glob`, `math`, `os`, `random`, `statistics`, `collections.defaultdict`) — no external dependencies, matching every other `analyze_*.py` script except `analyze_reasoning_text.py`.

---

## Verification approach

This codebase has no unit-test suite for its analysis scripts (none of `analyze_fault_rating_bias.py`, `analyze_confidence_ambiguity.py`, `family_omnibus_power_analysis.py` have tests) — verification is: run the script end-to-end, and sanity-check the output against known quantities. This plan follows that existing convention rather than introducing pytest for one file when nothing else in the repo has it. The key sanity check: Section B's MM-vs-FF numbers **must** closely match the already-committed same-gender control in `analysis/fault_rating_bias_findings.md` (n=810 pairs, mean diff=+0.062, d_z=+0.126) — it's the same comparison, computed a different way, and a mismatch would mean a bug in the new cell-building logic.

## Task 1: Write the script

**Files:**
- Create: `scripts/analyze_agent_identity_effect.py`

- [ ] **Step 1: Write the complete script**

```python
"""Generalized agent-identity effect (M/F/NB) on fault_rating -- extends the
core paired gender-bias test in `analyze_fault_rating_bias.py` from
male/female-only to the full 3x3 crossed gender design already collected
(agent_gender x partner_gender, each in {M, F, NB}) but never analyzed for
the NB level.

Two comparisons, both using the same paired-differencing logic as the
existing M-F test (scenario x severity x model held constant removes
between-scenario variance, which otherwise swamps the gender effect):

1. Agent-identity effect, partner held constant (Section A): for each
   (scenario, severity, model, partner_gender) cell with all three agent
   genders present, three pairwise diffs -- M-F, M-NB, F-NB. Pools over all
   three partner_gender values (M, F, NB), which is why this M-F sub-result
   has a larger n than (and will not numerically match) the headline M-F
   result in `fault_rating_bias_findings.md`, which is scoped to partner in
   {M, F} only -- that scoping stays as committed; this script does not
   change it.
2. Same-identity relationships (Section B): for each (scenario, severity,
   model) cell, three pairwise diffs across same-agent-and-partner identity
   -- MM-FF, MM-NBNB, FF-NBNB. MM-FF reproduces the existing same-gender
   control's numbers (n=810, mean diff=+0.062, d_z=+0.126) as a cross-check
   that this script's cell-building logic is correct.

Section C runs one 3-level omnibus permutation test per section (does
identity have any effect beyond the pairwise contrasts), via a cell-centered
label-shuffle one-way ANOVA -- centering each cell on its own mean before
pooling removes the same between-cell variance the pairwise tests remove by
differencing, so this is the direct 3-level generalization of the paired
t-test, not a naive one-way ANOVA on raw fault_rating (which would be
swamped by between-scenario variance).

Caveats:
- No per-family breakdown yet (see docs/superpowers/specs/
  2026-08-21-nb-agent-identity-effect-design.md's "explicitly out of scope"
  list) -- natural follow-up once this version is in.
- Reasoning-text engagement/misgendering for NB-involving rows is an open,
  separately-tracked question (project/project_status_summary.md open item
  10) -- a spot-check on the cleanest subset found 0% misgendering, but that
  was not a systematic pass. Not a blocker for this script (the outcome
  variable here is the numeric fault_rating, not reasoning-text pronoun
  choice), but worth keeping in mind when interpreting any NB-involving
  result below.

Usage: python scripts/analyze_agent_identity_effect.py
Reads:  responses/confirmatory/*.csv
Writes: analysis/agent_identity_effect_findings.md
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
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "agent_identity_effect_findings.md")

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
    """(scenario_id, severity, model, partner_gender) -> {agent_gender: row},
    pooling all three partner_gender values into separate extended cells --
    the structure Section A's comparisons and omnibus test both read from."""
    out = defaultdict(dict)
    for (scenario_id, severity, model), sub in cells.items():
        for (agent_gender, partner_gender), row in sub.items():
            out[(scenario_id, severity, model, partner_gender)][agent_gender] = row
    return out


def build_same_identity_cells(cells):
    """(scenario_id, severity, model) -> {identity: row} where
    agent_gender == partner_gender == identity."""
    out = {}
    for key, sub in cells.items():
        d = {g: sub[(g, g)] for g in GENDERS if (g, g) in sub}
        out[key] = d
    return out


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


def cell_centered_omnibus(cell_dict, genders=GENDERS):
    """3-level permutation omnibus test: centers each cell on its own mean
    (removing between-cell variance the same way pairwise differencing does)
    before pooling into a single label-shuffle one-way ANOVA. Only cells with
    all len(genders) levels present are used."""
    labels, values = [], []
    n_complete = 0
    for sub in cell_dict.values():
        if not all(g in sub for g in genders):
            continue
        n_complete += 1
        cell_vals = {g: sub[g]["fault_rating"] for g in genders}
        cell_mean = statistics.mean(cell_vals.values())
        for g, v in cell_vals.items():
            labels.append(g)
            values.append(v - cell_mean)
    F_obs, df1, df2, p = permutation_omnibus_test(labels, values)
    return n_complete, F_obs, df1, df2, p


def significance_sentence(p, subject):
    if p < 0.05:
        return f"**{subject} reaches conventional significance (p<0.05).**"
    return f"**{subject} does not reach conventional significance (p>0.05).**"


def write_comparison_block(out, pairs, label1, label2):
    n, mean_d, sd_d, t, d_z = paired_stat(pairs)
    n_pos, n_neg, n_tie, z, diff_bias = sign_breakdown(pairs)
    out.append(f"**{label1} vs {label2}**: n={n} pairs, mean diff ({label1}-{label2})="
                f"{mean_d:+.3f}, paired t={t:.2f}, d_z={d_z:.3f}.")
    ratio = f"{n_pos/n_neg:.2f}:1" if n_neg else "undefined (0 in denominator)"
    out.append(f"Sign breakdown: {n_tie} ties ({n_tie/n*100:.1f}%), {label1}>{label2} in "
                f"{n_pos}, {label2}>{label1} in {n_neg} (ratio {ratio}, sign-test "
                f"z={z:.2f}). Diff-bias = ({n_pos} - {n_neg}) / {n} = {diff_bias:+.4f}.\n")


def write_per_model_breakdown(out, cell_dict, g1, g2):
    by_model = defaultdict(list)
    for r1, r2 in pairwise(cell_dict, g1, g2):
        by_model[r1["model"]].append((r1, r2))
    rows = []
    for model, pairs in by_model.items():
        n, mean_d, sd_d, t, d_z = paired_stat(pairs)
        rows.append((model, n, mean_d, t, d_z))
    rows.sort(key=lambda r: -r[2])
    for model, n, mean_d, t, d_z in rows:
        out.append(f"- {model}: n={n}, diff={mean_d:+.3f}, t={t:+.2f}, d_z={d_z:+.3f}")
    out.append("")


def main():
    rows = load_responses()
    cells = build_cells(rows)
    partner_held_cells = build_partner_held_cells(cells)
    same_identity_cells = build_same_identity_cells(cells)

    out = []
    out.append("# Generalized agent-identity effect (M/F/NB) findings\n")
    out.append(f"Generated from `responses/confirmatory/*.csv` (n={len(rows)} rows). "
                f"Regenerate via `python scripts/analyze_agent_identity_effect.py`. "
                "Extends `analysis/fault_rating_bias_findings.md`'s core M-F paired "
                "test to the full 3x3 crossed gender design -- see this script's "
                "docstring and `docs/superpowers/specs/"
                "2026-08-21-nb-agent-identity-effect-design.md` for methodology and "
                "scope notes, including why the M-F numbers below differ from that "
                "file's headline M-F result.\n")

    out.append("## Section A: agent-identity effect, partner held constant\n")
    out.append("Pools over all three partner_gender values ({M, F, NB}); scenario x "
                "severity x model x partner_gender held constant within each pair.\n")
    for g1, g2 in PAIR_ORDER:
        pairs = pairwise(partner_held_cells, g1, g2)
        write_comparison_block(out, pairs, g1, g2)
    out.append("### Per-model breakdown\n")
    for g1, g2 in PAIR_ORDER:
        out.append(f"**{g1} vs {g2}**:")
        write_per_model_breakdown(out, partner_held_cells, g1, g2)

    out.append("## Section B: same-identity relationships (MM/FF/NB-NB)\n")
    out.append("Scenario x severity x model held constant; agent_gender == "
                "partner_gender in both arms of each pair (the same-identity control, "
                "extended from the existing MM-FF comparison to include NB-NB).\n")
    for g1, g2 in PAIR_ORDER:
        pairs = pairwise(same_identity_cells, g1, g2)
        write_comparison_block(out, pairs, f"{g1}{g1}", f"{g2}{g2}")

    out.append("## Section C: omnibus tests (does identity matter beyond the pairwise contrasts?)\n")
    out.append("Cell-centered label-shuffle permutation one-way ANOVA (each cell "
                f"centered on its own mean before pooling, {N_PERMUTATIONS} shuffles, "
                f"seed={PERMUTATION_SEED}) -- the 3-level generalization of the paired "
                "t-tests above.\n")
    n_a, F_a, df1_a, df2_a, p_a = cell_centered_omnibus(partner_held_cells)
    out.append(f"- **Section A (agent identity)**: n={n_a} complete cells, "
                f"F({df1_a},{df2_a})={F_a:.3f}, permutation p={p_a:.4f}. "
                f"{significance_sentence(p_a, 'Agent-identity effect')}\n")
    n_b, F_b, df1_b, df2_b, p_b = cell_centered_omnibus(same_identity_cells)
    out.append(f"- **Section B (same-identity relationships)**: n={n_b} complete cells, "
                f"F({df1_b},{df2_b})={F_b:.3f}, permutation p={p_b:.4f}. "
                f"{significance_sentence(p_b, 'Same-identity relationship effect')}\n")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_agent_identity_effect.py`
Expected: exits 0, prints `Wrote .../analysis/agent_identity_effect_findings.md`, and prints the full markdown report to stdout with no tracebacks.

- [ ] **Step 3: Commit**

```bash
git add scripts/analyze_agent_identity_effect.py analysis/agent_identity_effect_findings.md
git commit -m "$(cat <<'EOF'
Add generalized M/F/NB agent-identity effect analysis

Extends the existing paired M-F fault_rating test to the full 3x3
crossed gender design already collected but unused for NB: three
pairwise comparisons (M-F, M-NB, F-NB) holding partner constant, the
same three comparisons for same-identity relationships (MM/FF/NB-NB),
and a 3-level cell-centered permutation omnibus per section.
EOF
)"
```

## Task 2: Verify the numbers are correct

**Files:**
- Read only: `analysis/agent_identity_effect_findings.md`, `analysis/fault_rating_bias_findings.md`

- [ ] **Step 1: Cross-check Section B's MM-vs-FF block against the existing committed same-gender control**

Run: `grep -A2 "MM vs FF" analysis/agent_identity_effect_findings.md`
Expected: `n=810 pairs, mean diff (MM-FF)=+0.062` (or within rounding) and `d_z=0.126` — matching `analysis/fault_rating_bias_findings.md`'s already-committed same-gender control section (`n=810 pairs, mean diff (MM-FF)=+0.062, paired t=3.58, d_z=0.126`). If these don't match, there is a bug in `build_same_identity_cells` or `build_cells` — stop and debug before proceeding; do not paper over a mismatch with a comment.

- [ ] **Step 2: Sanity-check Section A's cell-completeness count**

Run: `grep "Section A (agent identity)" analysis/agent_identity_effect_findings.md`
Expected: `n=` close to 2430 complete cells (810 (scenario,severity,model) cells x 3 partner_gender values), minus a handful for `deepseek_v3`'s 6 known-undeliverable vignettes (see commit `266e0ea`). A number wildly different from ~2430 (e.g. off by a factor of 2-3) indicates `build_partner_held_cells` is keying incorrectly.

- [ ] **Step 3: Eyeball the full report for anything that looks like a hardcoded/stale claim**

Read `analysis/agent_identity_effect_findings.md` in full and confirm every significance claim ("reaches conventional significance" / "does not") actually matches the p-value printed right next to it in the same block — this script computes `significance_sentence()` dynamically, but a manual read is the same check that would have caught the two hardcoded-text bugs fixed in commit `a42f7f7` sooner.

- [ ] **Step 4: If any check in Steps 1-3 fails, fix and re-commit**

Fix the bug in `scripts/analyze_agent_identity_effect.py`, re-run Task 1 Step 2, re-run this task's checks, then:

```bash
git add scripts/analyze_agent_identity_effect.py analysis/agent_identity_effect_findings.md
git commit -m "Fix cell-building bug in agent-identity-effect analysis"
```

(Skip this step entirely if Steps 1-3 all passed on the first run.)

## Task 3: Document the new script

**Files:**
- Modify: `README.md` (Analysis section, after the `analyze_fault_rating_bias.py` entry)

- [ ] **Step 1: Add a README entry matching the existing style**

In the `## Analysis` section of `README.md`, immediately after the `scripts/analyze_fault_rating_bias.py` bullet (currently ending `... Writes analysis/fault_rating_bias_findings.md.`), insert:

```markdown
- **`scripts/analyze_agent_identity_effect.py`** -- reads
  `responses/confirmatory/*.csv`, generalizes the M-F paired test above to
  the full 3x3 crossed gender design `{M, F, NB}`: agent-identity pairwise
  comparisons (M-F, M-NB, F-NB) holding partner constant, same-identity
  relationship comparisons (MM-FF, MM-NBNB, FF-NBNB), and a 3-level omnibus
  per section. Writes `analysis/agent_identity_effect_findings.md`. See
  `docs/superpowers/specs/2026-08-21-nb-agent-identity-effect-design.md` for
  why this script's M-F numbers differ from the headline result above.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Document analyze_agent_identity_effect.py in README"
```

## Task 4: Update the open-items tracker

**Files:**
- Modify: `project/project_status_summary.md` (open item 10, added earlier this session)

- [ ] **Step 1: Add a one-line pointer from open item 10 to the new findings file**

Open item 10 currently ends with "...to rule out reasoning-level engagement failures as a confound on any NB-involving numeric result." Append a sentence noting the numeric result now exists:

Find this text in `project/project_status_summary.md`:
```
    engagement failures as a confound on any NB-involving numeric result.
```

Replace with:
```
    engagement failures as a confound on any NB-involving numeric result.
    That numeric result now exists -- see
    `analysis/agent_identity_effect_findings.md` -- so this item is no
    longer speculative groundwork; it directly bears on interpreting that
    file's Section A/B results wherever they involve NB.
```

- [ ] **Step 2: Commit**

```bash
git add project/project_status_summary.md
git commit -m "Link NB pronoun-handling open item to the new agent-identity-effect findings"
```
