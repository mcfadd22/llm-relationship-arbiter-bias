"""Pair-level test of the ambiguity/confidence mechanism hypothesis.

`analysis/fault_rating_bias_findings.md`'s "Does obligation-source ambiguity
predict the size of the gender gap?" section correlates mean confidence
against gender-effect size, but only at the obligation_source level (n=8
aggregated points) -- an ecological correlation, not an individual-response-
level test, and confounded with family (two sources are single-family by
design; the residualization analysis shows most of the source ranking IS the
family effect).

This script re-runs that test at the actual unit of analysis: the 720 matched
(male-agent, female-agent) pairs. For each pair, "confidence" is the mean of
the two rows' self-reported confidence (0-100) -- these are the self-reported
field currently in responses/confirmatory/*.csv, NOT the dispersion-based
measure docs/prompt_and_measurement_protocol.md specs as the eventual primary
confidence metric (that requires a not-yet-run stability pass). This script
tests what the self-report field can tell us now, as a first pass before any
new data collection.

Usage: python scripts/analyze_confidence_ambiguity.py
Reads:  responses/confirmatory/*.csv
Writes: analysis/confidence_ambiguity_findings.md
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
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "confidence_ambiguity_findings.md")


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
    cells = defaultdict(dict)
    for r in rows:
        key = (r["scenario_id"], r["severity"], r["model"])
        cells[key][(r["agent_gender"], r["partner_gender"])] = r
    return cells


def matched_pairs(cells):
    pairs = []
    for cell in cells.values():
        for partner in ("F", "M"):
            m_row = cell.get(("M", partner))
            f_row = cell.get(("F", partner))
            if m_row is not None and f_row is not None:
                pairs.append((m_row, f_row))
    return pairs


def pearson(xs, ys):
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else float("nan")


def permutation_corr_test(xs, ys, n_perm=N_PERMUTATIONS, seed=PERMUTATION_SEED):
    """Two-sided permutation test for |r|, shuffling ys against xs."""
    r_obs = pearson(xs, ys)
    rng = random.Random(seed)
    shuffled = list(ys)
    count_ge = 0
    for _ in range(n_perm):
        rng.shuffle(shuffled)
        r_perm = pearson(xs, shuffled)
        if abs(r_perm) >= abs(r_obs):
            count_ge += 1
    p = (count_ge + 1) / (n_perm + 1)
    return r_obs, p


def welch_t(xs, ys):
    n1, n2 = len(xs), len(ys)
    m1, m2 = statistics.mean(xs), statistics.mean(ys)
    s1, s2 = statistics.stdev(xs), statistics.stdev(ys)
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    t = (m1 - m2) / se if se > 0 else float("nan")
    return t, m1 - m2


def main():
    rows = load_responses()
    cells = build_cells(rows)
    pairs = matched_pairs(cells)
    n = len(pairs)

    pair_conf = [(m["confidence"] + f["confidence"]) / 2 for m, f in pairs]
    pair_diff = [m["fault_rating"] - f["fault_rating"] for m, f in pairs]
    pair_absdiff = [abs(d) for d in pair_diff]
    pair_family = [m["family_name"] for m, f in pairs]

    out = []
    out.append("# Pair-level confidence / ambiguity findings\n")
    out.append(f"Generated from `responses/confirmatory/*.csv` (n={len(rows)} rows, "
                f"{n} matched pairs). Regenerate via "
                f"`python scripts/analyze_confidence_ambiguity.py`.\n")
    out.append("Re-tests the ambiguity mechanism from "
                "`analysis/fault_rating_bias_findings.md` (\"Does obligation-source "
                "ambiguity predict the size of the gender gap?\") at the level of the "
                "720 individual matched pairs, rather than the 8 obligation_source-level "
                "aggregate points used there. `confidence` here is the mean of each pair's "
                "two self-reported (0-100) confidence values -- the field already in the "
                "confirmatory-pass data, not the dispersion-based measure specced in "
                "`docs/prompt_and_measurement_protocol.md` as the eventual primary metric "
                "(that needs a stability pass that hasn't been run).\n")

    # 1. Signed diff (the actual claim: lower confidence -> larger M-F gap specifically)
    out.append("## Confidence vs. signed gender gap (M - F fault_rating)\n")
    r_signed, p_signed = permutation_corr_test(pair_conf, pair_diff)
    out.append(f"r={r_signed:.3f}, permutation p={p_signed:.4f} (n={n}, "
                f"{N_PERMUTATIONS} shuffles, seed={PERMUTATION_SEED}).\n")

    # 2. Absolute gap magnitude, in case the mechanism is "ambiguity -> more
    # room for gender to swing the verdict either way" rather than
    # specifically "-> more male blame."
    out.append("## Confidence vs. absolute gender gap (|M - F| fault_rating)\n")
    r_abs, p_abs = permutation_corr_test(pair_conf, pair_absdiff)
    out.append(f"r={r_abs:.3f}, permutation p={p_abs:.4f} (n={n}).\n")

    # 3. Disagreement pairs vs tied pairs: do lower-confidence pairs disagree more often?
    out.append("## Confidence: disagreement pairs vs. tied pairs\n")
    dis_conf = [c for c, d in zip(pair_conf, pair_diff) if d != 0]
    tie_conf = [c for c, d in zip(pair_conf, pair_diff) if d == 0]
    t_dis, diff_dis = welch_t(dis_conf, tie_conf)
    out.append(f"Disagreement pairs (n={len(dis_conf)}): mean confidence={statistics.mean(dis_conf):.2f}. "
                f"Tied pairs (n={len(tie_conf)}): mean confidence={statistics.mean(tie_conf):.2f}. "
                f"diff={diff_dis:+.2f}, Welch t={t_dis:.2f}.\n")

    # 4. Family-residualized version: is this just the family confound again?
    out.append("## Family-residualized version (is this just the family effect again?)\n")
    out.append("The obligation_source version of this finding mostly turned out to be "
                "the family effect once residualized (see `analysis/fault_rating_bias_findings.md`). "
                "Same check here: subtract each family's own mean confidence and mean "
                "signed gap before correlating, so the test asks whether confidence tracks "
                "the gap *within* families, not just because some families happen to have "
                "both lower confidence and bigger gaps.\n")
    fam_conf = defaultdict(list)
    fam_diff = defaultdict(list)
    for c, d, fam in zip(pair_conf, pair_diff, pair_family):
        fam_conf[fam].append(c)
        fam_diff[fam].append(d)
    fam_mean_conf = {fam: statistics.mean(v) for fam, v in fam_conf.items()}
    fam_mean_diff = {fam: statistics.mean(v) for fam, v in fam_diff.items()}
    resid_conf = [c - fam_mean_conf[fam] for c, fam in zip(pair_conf, pair_family)]
    resid_diff = [d - fam_mean_diff[fam] for d, fam in zip(pair_diff, pair_family)]
    r_resid, p_resid = permutation_corr_test(resid_conf, resid_diff)
    out.append(f"Within-family residualized: r={r_resid:.3f}, permutation p={p_resid:.4f} (n={n}).\n")

    # 5. For reference: the family-level means themselves (analogous to the
    # obligation_source-level ecological correlation, but for family).
    out.append("## For reference: family-level ecological correlation (analogous to the obligation_source one)\n")
    fams = sorted(fam_mean_conf.keys())
    fam_c_vals = [fam_mean_conf[f] for f in fams]
    fam_d_vals = [fam_mean_diff[f] for f in fams]
    r_fam_eco = pearson(fam_c_vals, fam_d_vals)
    out.append(f"r(family mean confidence, family mean signed gap)={r_fam_eco:.3f} "
                f"(n={len(fams)} families -- ecological, same caveat as the obligation_source version).\n")
    for fam in sorted(fams, key=lambda f: fam_mean_conf[f]):
        out.append(f"- {fam}: mean confidence={fam_mean_conf[fam]:.2f}, mean signed gap={fam_mean_diff[fam]:+.3f}")
    out.append("")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
