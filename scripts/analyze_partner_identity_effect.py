"""Partner-identity effect (M/F/NB) on fault_rating -- the mirror image of
`analyze_agent_identity_effect.py`'s agent-identity test: does the
partner's gender identity change how the agent is judged, holding the
agent's own gender constant? Uses the same full 3x3 crossed gender design
(agent_gender x partner_gender, each in {M, F, NB}) already collected in
responses/confirmatory/*.csv.

Section A (partner-identity effect, agent held constant): for each
(scenario, severity, model, agent_gender) cell with all three partner
genders present, three pairwise diffs -- partner M-vs-F, M-vs-NB, F-vs-NB.
Pools over all three agent_gender values. This supersedes the older,
weaker unpaired partner M-vs-F secondary finding in
`analyze_fault_rating_bias.py` ("Secondary finding: partner (victim)
gender effect") -- that section now points here as the authoritative,
matched version; it is not deleted, just cross-referenced.

Section B (omnibus test): one 3-level cell-centered, within-cell
label-shuffle permutation ANOVA -- the same corrected methodology as
`analyze_agent_identity_effect.py`'s `cell_centered_omnibus` (commit
`80b75db`), reused verbatim rather than reintroducing the original global-
shuffle bug that methodology fixed.

Why there is no "NB-NB" comparison in this script -- explicit, not just
implied: this script's three pairwise tests are contrasts *between
different values* of partner gender (M vs F, M vs NB, F vs NB), each held
against a fixed agent gender. There is no meaningful "NB vs NB" version of
that contrast -- comparing a category against itself isn't a difference
test, it's zero by construction. What "NB-NB" actually refers to is a
different question: *both people in the relationship being NB* (agent=NB
**and** partner=NB together) -- a same-identity relationship-type
question, not a partner-identity-holding-agent-constant question. That
question is already answered, by
`analyze_agent_identity_effect.py`'s Section B (NB-NB vs MM vs FF). This
script asks "does the partner's identity change how the agent is judged";
that other script's Section B asks "do NB-NB relationships get judged
differently than MM/FF relationships" -- different independent variable,
different question. Conflating them would repeat the exact mistake
`docs/planned_analysis.md` Section 5 warns against for the presumed-
orientation analyses (confusing gender identity with relationship-type
groupings).

Caveats:
- No per-family breakdown yet, matching `analyze_agent_identity_effect.py`'s
  own scope boundary -- natural follow-up once this version is in.
- Reasoning-text engagement/misgendering for NB-involving rows remains an
  open, separately-tracked question (project/project_status_summary.md
  open item 10) -- not a blocker here either, for the same reason it isn't
  a blocker in the sibling script (the outcome variable is the numeric
  fault_rating, not reasoning-text pronoun choice).
- Section A pools the three agent_gender slices of each (scenario,
  severity, model) triplet as if independent, but they share the same
  underlying scenario content -- more plausibly clustered than fully
  independent, which likely makes Section A's p-values somewhat
  anti-conservative. Probably immaterial given the effect sizes typically
  seen in this project's other sections, but stated explicitly rather than
  left implicit.

Usage: python scripts/analyze_partner_identity_effect.py
Reads:  responses/confirmatory/*.csv
Writes: analysis/partner_identity_effect_findings.md
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
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "partner_identity_effect_findings.md")

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


def build_agent_held_cells(cells):
    """(scenario_id, severity, model, agent_gender) -> {partner_gender: row}."""
    out = defaultdict(dict)
    for (scenario_id, severity, model), sub in cells.items():
        for (agent_gender, partner_gender), row in sub.items():
            out[(scenario_id, severity, model, agent_gender)][partner_gender] = row
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


def cell_centered_omnibus(cell_dict, genders=GENDERS, n_perm=N_PERMUTATIONS, seed=PERMUTATION_SEED):
    """3-level permutation omnibus test for a within-subjects/repeated-measures
    factor: centers each cell on its own mean (removing between-cell variance
    the same way pairwise differencing does), then pools the centered values
    into a one-way ANOVA. Only cells with all len(genders) levels present are
    used.

    The permutation null is built by shuffling gender labels WITHIN each cell
    only -- for every iteration, each cell's own set of centered values is
    independently re-labeled among {genders}, and a value never moves to a
    different cell. This is the direct generalization of "flip within-pair,
    don't shuffle across pairs" from a paired t-test's own permutation test.
    A global/unrestricted shuffle across all pooled values would be the wrong
    reference distribution here: after per-cell centering, a cell's values are
    linearly dependent (they sum to zero within that cell), and the observed
    statistic never mixes values from different cells under the same label,
    so the null must respect that same restriction."""
    genders_list = list(genders)
    cell_values = []  # one [v_g1, v_g2, ...] list per complete cell, same order as genders_list
    labels_obs, values_obs = [], []
    for sub in cell_dict.values():
        if not all(g in sub for g in genders_list):
            continue
        cell_vals = {g: sub[g]["fault_rating"] for g in genders_list}
        cell_mean = statistics.mean(cell_vals.values())
        centered = [cell_vals[g] - cell_mean for g in genders_list]
        cell_values.append(centered)
        labels_obs.extend(genders_list)
        values_obs.extend(centered)
    n_complete = len(cell_values)

    F_obs, df1, df2 = one_way_anova_F(labels_obs, values_obs)

    rng = random.Random(seed)
    count_ge = 0
    for _ in range(n_perm):
        perm_labels = []
        for _ in cell_values:
            shuffled = list(genders_list)
            rng.shuffle(shuffled)
            perm_labels.extend(shuffled)
        F_perm, _, _ = one_way_anova_F(perm_labels, values_obs)
        if F_perm >= F_obs:
            count_ge += 1
    p = (count_ge + 1) / (n_perm + 1)
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
    agent_held_cells = build_agent_held_cells(cells)

    out = []
    out.append("# Partner-identity effect (M/F/NB) findings\n")
    out.append(f"Generated from `responses/confirmatory/*.csv` (n={len(rows)} rows). "
                f"Regenerate via `python scripts/analyze_partner_identity_effect.py`. "
                "Supersedes `analysis/fault_rating_bias_findings.md`'s older, unpaired "
                "\"Secondary finding: partner (victim) gender effect\" -- this is the "
                "matched (agent-gender-held-constant) version of that comparison, "
                "extended to the NB partner level. See this script's docstring and "
                "`docs/superpowers/specs/2026-08-21-partner-identity-effect-design.md` "
                "for full methodology, including why there is no NB-NB comparison "
                "below (that question is answered by "
                "`analysis/agent_identity_effect_findings.md`'s Section B instead).\n")

    out.append("## Section A: partner-identity effect, agent held constant\n")
    out.append("Pools over all three agent_gender values ({M, F, NB}); scenario x "
                "severity x model x agent_gender held constant within each pair. Note "
                "the three agent_gender slices for a given scenario x severity x model "
                "share the same underlying scenario content, so they are better "
                "described as clustered than fully independent -- this likely makes "
                "this section's p-values somewhat anti-conservative, worth stating "
                "rather than leaving implicit.\n")
    for g1, g2 in PAIR_ORDER:
        pairs = pairwise(agent_held_cells, g1, g2)
        write_comparison_block(out, pairs, g1, g2)
    out.append("### Per-model breakdown\n")
    for g1, g2 in PAIR_ORDER:
        out.append(f"**{g1} vs {g2}**:")
        write_per_model_breakdown(out, agent_held_cells, g1, g2)

    out.append("## Section B: omnibus test (does partner identity matter beyond the pairwise contrasts?)\n")
    out.append("Cell-centered, within-cell label-shuffle permutation one-way ANOVA "
                f"(each cell centered on its own mean before pooling, {N_PERMUTATIONS} "
                f"shuffles restricted to within-cell label reassignment, "
                f"seed={PERMUTATION_SEED}) -- the 3-level generalization of the paired "
                "t-tests above; see this script's docstring for why the permutation "
                "must be within-cell, not global.\n")
    n_a, F_a, df1_a, df2_a, p_a = cell_centered_omnibus(agent_held_cells)
    out.append(f"- **Section A (partner identity)**: n={n_a} complete cells, "
                f"F({df1_a},{df2_a})={F_a:.3f}, permutation p={p_a:.4f}. "
                f"{significance_sentence(p_a, 'Partner-identity effect')}\n")

    out.append("## Why there is no NB-NB comparison in this script\n")
    out.append("This script's pairwise tests are contrasts *between different values* "
                "of partner gender (M vs F, M vs NB, F vs NB), each held against a fixed "
                "agent gender -- there is no meaningful \"NB vs NB\" version of that "
                "contrast, since comparing a category against itself isn't a difference "
                "test. \"NB-NB\" as a concept refers to a different question -- *both* "
                "agent and partner being NB together, a same-identity relationship-type "
                "question, not a partner-identity-holding-agent-constant question -- and "
                "that question is already answered by "
                "`analysis/agent_identity_effect_findings.md`'s Section B (NB-NB vs MM "
                "vs FF). Conflating the two would repeat the mistake "
                "`docs/planned_analysis.md` Section 5 explicitly warns against for the "
                "presumed-orientation analyses.\n")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
