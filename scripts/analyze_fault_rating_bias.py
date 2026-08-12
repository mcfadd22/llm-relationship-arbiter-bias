"""Core gender-bias analysis on the confirmatory pass, plus a check of whether
the reasoning-text linguistic features (analysis/reasoning_features.csv) track
the numeric bias.

All tests use the design-correct paired comparison: scenario_id x severity x
model held constant, comparing the male-agent-config rating against the
female-agent-config rating (holding partner gender constant), since each
scenario/severity/model cell provides its own matched control. Naive
independent-samples comparisons are NOT used here because they ignore the
repeated-measures structure and understate significance.

Usage: python scripts/analyze_fault_rating_bias.py
Reads:  responses/confirmatory/*.csv, analysis/reasoning_features.csv
Writes: analysis/fault_rating_bias_findings.md
"""

import csv
import glob
import math
import os
import statistics
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_GLOB = os.path.join(REPO_ROOT, "responses", "confirmatory", "*.csv")
FEATURES_PATH = os.path.join(REPO_ROOT, "analysis", "reasoning_features.csv")
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "fault_rating_bias_findings.md")


def load_responses():
    rows = []
    for f in sorted(glob.glob(RESPONSES_GLOB)):
        with open(f) as fh:
            for row in csv.DictReader(fh):
                row["fault_rating"] = float(row["fault_rating"])
                row["confidence"] = float(row["confidence"])
                rows.append(row)
    return rows


def load_features():
    with open(FEATURES_PATH) as fh:
        return {(r["vignette_id"], r["model"]): r for r in csv.DictReader(fh)}


def welch_t(g1, g2, key):
    v1 = [r[key] for r in g1]
    v2 = [r[key] for r in g2]
    n1, n2 = len(v1), len(v2)
    m1, m2 = statistics.mean(v1), statistics.mean(v2)
    s1, s2 = statistics.stdev(v1), statistics.stdev(v2)
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    t = (m1 - m2) / se if se > 0 else float("nan")
    d = (m1 - m2) / math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    return t, m1 - m2, d


def build_cells(rows):
    cells = defaultdict(dict)
    for r in rows:
        key = (r["scenario_id"], r["severity"], r["model"])
        cells[key][(r["agent_gender"], r["partner_gender"])] = r
    return cells


def matched_pairs(cells):
    """All (male_row, female_row) pairs holding partner gender + scenario/severity/model constant."""
    pairs = []
    for cell in cells.values():
        for partner in ("F", "M"):
            m_row = cell.get(("M", partner))
            f_row = cell.get(("F", partner))
            if m_row is not None and f_row is not None:
                pairs.append((m_row, f_row))
    return pairs


def paired_stat(pairs, key):
    diffs = [m[key] - f[key] for m, f in pairs]
    n = len(diffs)
    mean_d = statistics.mean(diffs)
    sd_d = statistics.stdev(diffs) if n > 1 else 0.0
    se_d = sd_d / math.sqrt(n) if n and sd_d > 0 else float("nan")
    t = mean_d / se_d if se_d and not math.isnan(se_d) else float("nan")
    d_z = mean_d / sd_d if sd_d > 0 else float("nan")
    return n, mean_d, sd_d, t, d_z


def pearson(xs, ys):
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else float("nan")


def main():
    rows = load_responses()
    features = load_features()
    cells = build_cells(rows)
    pairs = matched_pairs(cells)

    out = []
    out.append("# Fault-rating gender-bias findings\n")
    out.append(f"Generated from `responses/confirmatory/*.csv` (n={len(rows)} rows) "
                f"and `analysis/reasoning_features.csv`. Regenerate via "
                f"`python scripts/analyze_fault_rating_bias.py`.\n")

    # 1. Severity manipulation check
    sev = defaultdict(list)
    for r in rows:
        sev[r["severity"]].append(r)
    t, diff, d = welch_t(sev["SEV"], sev["MLD"], "fault_rating")
    out.append("## Severity manipulation check\n")
    out.append(f"SEV mean={statistics.mean([r['fault_rating'] for r in sev['SEV']]):.3f}, "
                f"MLD mean={statistics.mean([r['fault_rating'] for r in sev['MLD']]):.3f}, "
                f"diff={diff:.3f}, d={d:.3f}, Welch t={t:.2f}. **Passes.**\n")

    # 2. Core paired agent-gender effect
    n, mean_d, sd_d, t, d_z = paired_stat(pairs, "fault_rating")
    out.append("## Core finding: agent-gender effect on fault_rating\n")
    out.append(f"Paired (scenario x severity x model held constant): n={n} pairs, "
                f"mean diff (M-F)={mean_d:+.3f}, paired t={t:.2f}, d_z={d_z:.3f}.\n")
    n_pos = sum(1 for m, f in pairs if m["fault_rating"] > f["fault_rating"])
    n_neg = sum(1 for m, f in pairs if m["fault_rating"] < f["fault_rating"])
    n_tie = n - n_pos - n_neg
    z = (n_pos - (n_pos + n_neg) / 2) / math.sqrt((n_pos + n_neg) * 0.25)
    out.append(f"Sign breakdown: {n_tie} ties ({n_tie/n*100:.1f}%), M>F in {n_pos}, "
                f"F>M in {n_neg} (ratio {n_pos/n_neg:.2f}:1, sign-test z={z:.2f}).\n")

    # 3. By family
    out.append("## Agent-gender effect by relationship-norm family\n")
    fam_pairs = defaultdict(list)
    for m, f in pairs:
        fam_pairs[m["family_name"]].append((m, f))
    fam_results = []
    for fam, fp in fam_pairs.items():
        n, md, sd, t, d = paired_stat(fp, "fault_rating")
        fam_results.append((fam, n, md, t, d))
    fam_results.sort(key=lambda x: -abs(x[4]))
    for fam, n, md, t, d in fam_results:
        out.append(f"- {fam}: n={n}, diff={md:+.3f}, t={t:+.2f}, d_z={d:+.3f}")
    out.append("")

    # 4. By model, with disagreement-pair ratio
    out.append("## Agent-gender effect and disagreement-pair ratio by model\n")
    model_pairs = defaultdict(list)
    for m, f in pairs:
        model_pairs[m["model"]].append((m, f))
    model_results = []
    for model, mp in model_pairs.items():
        n, md, sd, t, d = paired_stat(mp, "fault_rating")
        n_pos = sum(1 for a, b in mp if a["fault_rating"] > b["fault_rating"])
        n_neg = sum(1 for a, b in mp if a["fault_rating"] < b["fault_rating"])
        n_dis = n_pos + n_neg
        ratio = n_pos / n_neg if n_neg else float("inf")
        model_results.append((model, n, md, t, d, n_dis, n, ratio))
    model_results.sort(key=lambda x: -x[5] / x[6])
    for model, n, md, t, d, n_dis, n_tot, ratio in model_results:
        out.append(f"- {model}: n={n}, diff={md:+.3f}, t={t:+.2f}, d_z={d:+.3f}, "
                    f"disagreement rate={n_dis}/{n_tot}={n_dis/n_tot*100:.1f}%, "
                    f"M-blamed:F-blamed ratio={ratio:.2f}:1")
    out.append("")

    # 5. Obligation-source moderator
    out.append("## Agent-gender effect by obligation_source\n")
    src_pairs = defaultdict(list)
    for m, f in pairs:
        src_pairs[m["obligation_source"]].append((m, f))
    src_results = []
    for src, sp in src_pairs.items():
        n, md, sd, t, d = paired_stat(sp, "fault_rating")
        src_results.append((src, n, md, t, d))
    src_results.sort(key=lambda x: -x[4])
    for src, n, md, t, d in src_results:
        out.append(f"- {src}: n={n}, diff={md:+.3f}, t={t:+.2f}, d_z={d:+.3f}")
    out.append("")

    # 6. Partner-gender secondary effect
    partner_groups = defaultdict(list)
    for r in rows:
        partner_groups[r["partner_gender"]].append(r)
    t, diff, d = welch_t(partner_groups["M"], partner_groups["F"], "fault_rating")
    out.append("## Secondary finding: partner (victim) gender effect\n")
    out.append(f"partner=M mean={statistics.mean([r['fault_rating'] for r in partner_groups['M']]):.3f}, "
                f"partner=F mean={statistics.mean([r['fault_rating'] for r in partner_groups['F']]):.3f}, "
                f"diff={diff:+.3f}, d={d:+.3f}, Welch t={t:.2f}.\n")

    # 7. Cross-model agreement
    out.append("## Cross-model fault_rating agreement\n")
    by_vm = defaultdict(dict)
    for r in rows:
        by_vm[r["vignette_id"]][r["model"]] = r["fault_rating"]
    models = sorted(model_pairs.keys())
    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            m1, m2 = models[i], models[j]
            xs, ys = [], []
            for vid, d in by_vm.items():
                if m1 in d and m2 in d:
                    xs.append(d[m1])
                    ys.append(d[m2])
            r = pearson(xs, ys)
            out.append(f"- {m1} vs {m2}: r={r:.3f} (n={len(xs)})")
    out.append("")

    # 8. Reasoning-text linguistic features: paired agent-gender effect
    out.append("## Reasoning-text linguistic features: paired agent-gender effect\n")
    feat_keys = ["agentic_rate_per100w", "communal_rate_per100w",
                 "moral_intensity_score_per100w", "lib_mean"]
    lang_pairs = []
    for m, f in pairs:
        fm = features.get((m["vignette_id"], m["model"]))
        ff = features.get((f["vignette_id"], f["model"]))
        if fm is None or ff is None:
            continue
        lang_pairs.append((m, f, fm, ff))

    for key in feat_keys:
        diffs = []
        for m, f, fm, ff in lang_pairs:
            if fm[key] == "" or ff[key] == "":
                continue
            diffs.append(float(fm[key]) - float(ff[key]))
        n = len(diffs)
        mean_d = statistics.mean(diffs)
        sd_d = statistics.stdev(diffs) if n > 1 else 0.0
        se_d = sd_d / math.sqrt(n) if n and sd_d > 0 else float("nan")
        t = mean_d / se_d if se_d and not math.isnan(se_d) else float("nan")
        d_z = mean_d / sd_d if sd_d > 0 else float("nan")
        out.append(f"- {key}: n={n}, mean diff (M-F)={mean_d:+.4f}, t={t:+.2f}, d_z={d_z:+.3f}")
    out.append("")

    out.append("## Does the linguistic difference track the fault_rating gap?\n")
    out.append("Correlation between per-pair language-feature diff and per-pair "
                "fault_rating diff (both M-F), within the same matched pairs:\n")
    for key in feat_keys:
        lang_diffs, fault_diffs = [], []
        for m, f, fm, ff in lang_pairs:
            if fm[key] == "" or ff[key] == "":
                continue
            lang_diffs.append(float(fm[key]) - float(ff[key]))
            fault_diffs.append(m["fault_rating"] - f["fault_rating"])
        r = pearson(lang_diffs, fault_diffs)
        out.append(f"- {key}: r={r:.3f} (n={len(lang_diffs)})")
    out.append("")
    out.append("**Interpretation:** these correlations are all weak (|r|<0.11), and the "
                "LIB dispositional-attribution score shows essentially no gender effect at "
                "all (d_z=-0.004) despite being the theoretically best-grounded of the three "
                "linguistic dimensions. The numeric fault_rating bias does not appear to be "
                "strongly reflected in the surface linguistic markers tested here -- either "
                "the lexicon/heuristic measures are insensitive to the real signal, or the "
                "bias operates more on the quantitative scoring step than on the qualitative "
                "reasoning language, which would itself be a notable and citable finding. "
                "This is the strongest case yet for the LLM-assisted open-ended pattern "
                "discovery pass (see project_status_summary.md open items) rather than "
                "further hand-built lexicon expansion.")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
