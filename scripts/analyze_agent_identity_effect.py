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
