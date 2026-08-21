# Pairing Structure Effect (Item 5f) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `scripts/analyze_pairing_structure_effect.py`, testing whether the gender-normativity/identity-sharing structure of a pairing changes how the agent is judged -- new item 5f of `docs/planned_analysis.md`, explicitly distinct from (and not a re-framing of) the orientation question in items 5a-5e, per `docs/superpowers/specs/2026-08-21-orientation-and-pairing-structure-design.md`.

**Architecture:** One new script covering all 9 gender configs via a real 2x2 factorial crossing two objective structural properties (identity-sharing: same vs. different; binary-involvement: binary-only vs. NB-involved) -- not a social inference about presumed orientation. Introduces one piece of genuinely new methodology to this codebase: a sign-flip one-sample permutation test (the paired/one-sample analog of the label-shuffle omnibus tests already used elsewhere). Flagged for extra review scrutiny given that novelty, the same way `analyze_agent_identity_effect.py`'s within-cell-shuffle omnibus needed a real review pass -- and a real fix, commit `80b75db` -- before it was trustworthy.

**Tech Stack:** Python 3.11 stdlib only (`csv`, `glob`, `math`, `os`, `random`, `statistics`, `collections.defaultdict`) -- no new dependencies.

---

## Verification approach

No unit-test suite exists for this codebase's analysis scripts (matches existing convention). Given this script introduces new methodology, verification here goes beyond the usual "run it, check for NaN" -- Task 1 includes a hand-arithmetic check on one real cell before trusting the aggregate output.

## Task 1: Build and run the pairing-structure script

**Files:**
- Create: `scripts/analyze_pairing_structure_effect.py`

- [ ] **Step 1: Write the complete script**

```python
"""Pairing structure (item 5f, docs/planned_analysis.md) -- does the
gender-normativity/identity-sharing structure of a pairing change how the
agent is judged? A genuinely different, explicitly non-orientation
question from scripts/analyze_orientation_effect.py (items 5a-5e): this
script covers all 9 gender configs via a real 2x2 factorial crossing two
objective structural properties, not a social inference about the
pairing's presumed sexual orientation.

The four groups, defined by two structural properties (identity-sharing:
does the pairing have one shared gender identity or two different ones?;
binary-involvement: does either partner identify as NB?):

                  | Different identity | Same identity
    Binary only   | opposite-binary:    | same-binary:
                  |   MF, FM            |   MM, FF
    NB-involved   | NB-mixed:           | NB-NB:
                  |   NBM, NBF,         |   NBNB
                  |   MNB, FNB          |

NB-NB is a same-identity pairing, structurally identical in kind to
MM/FF -- NOT to NB-mixed pairings, which are different-identity pairings
structurally identical in kind to MF/FM. Pooling NB-NB with NB-mixed under
one "NB-involving" label would put a same-identity pairing in with
different-identity pairings, the same category error avoided by not
folding NB into orientation in analyze_orientation_effect.py.

Three tests, all derived from per-cell group means (average of whichever
rows are present in each group, per (scenario, severity, model) cell). A
cell only contributes if all four groups are present in it:

1. Main effect: identity-sharing (different vs. same), pooled over
   binary-involvement. Per cell: different_identity_mean = mean(
   opposite_binary_mean, nb_mixed_mean); same_identity_mean = mean(
   same_binary_mean, nbnb_mean) -- averaging the two subgroup means, NOT
   row-count-weighting them, so the 4-config NB-mixed group doesn't
   outweigh the 2-config opposite-binary group.
2. Main effect: binary-involvement (binary-only vs. NB-involved), pooled
   over identity-sharing. Per cell: binary_only_mean = mean(
   opposite_binary_mean, same_binary_mean); nb_involved_mean = mean(
   nb_mixed_mean, nbnb_mean).
3. Interaction: does the identity-sharing effect differ between
   binary-only and NB-involved pairings? Per cell: diff_binary_only =
   same_binary_mean - opposite_binary_mean; diff_nb_involved = nbnb_mean -
   nb_mixed_mean; interaction quantity = diff_binary_only -
   diff_nb_involved. Tested as a PAIRED, one-sample question (both halves
   come from the same cell, so pairing removes the same between-scenario
   variance every other test in this project removes by
   pairing/differencing) -- not an unpaired two-group ANOVA.

Each of the three derived per-cell quantities is tested via a one-sample
paired-style statistic (mean/sd/t/d_z) plus a sign-flip permutation test
(randomly flip each cell's diff's sign, recompute the mean, compare to the
observed mean) -- the permutation-test analog of a one-sample/paired
t-test, distribution-free, matching this project's permutation-test-first
convention. This is new methodology for this codebase (no prior script
needed a one-sample sign-flip test) -- called out explicitly for extra
review scrutiny, the same way analyze_agent_identity_effect.py's
within-cell-shuffle omnibus needed a real review pass (and a real fix,
commit 80b75db) before it was trustworthy.

Usage: python scripts/analyze_pairing_structure_effect.py
Reads:  responses/confirmatory/*.csv
Writes: analysis/pairing_structure_effect_findings.md
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
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "pairing_structure_effect_findings.md")

OPPOSITE_BINARY_CONFIGS = (("M", "F"), ("F", "M"))
SAME_BINARY_CONFIGS = (("M", "M"), ("F", "F"))
NB_MIXED_CONFIGS = (("NB", "M"), ("NB", "F"), ("M", "NB"), ("F", "NB"))
NBNB_CONFIG = ("NB", "NB")


def load_responses():
    rows = []
    for f in sorted(glob.glob(RESPONSES_GLOB)):
        with open(f) as fh:
            for row in csv.DictReader(fh):
                row["fault_rating"] = float(row["fault_rating"])
                rows.append(row)
    return rows


def build_cells(rows):
    cells = defaultdict(dict)
    for r in rows:
        key = (r["scenario_id"], r["severity"], r["model"])
        cells[key][(r["agent_gender"], r["partner_gender"])] = r
    return cells


def group_mean(sub, configs):
    """Mean fault_rating across whichever of `configs` are present in this
    cell's sub-dict, or None if none are present."""
    vals = [sub[c]["fault_rating"] for c in configs if c in sub]
    return statistics.mean(vals) if vals else None


def cell_group_means(cells):
    """(scenario_id, severity, model) -> dict with keys 'opposite_binary',
    'same_binary', 'nb_mixed', 'nbnb', each None if that group has no rows
    in this cell."""
    out = {}
    for key, sub in cells.items():
        out[key] = {
            "opposite_binary": group_mean(sub, OPPOSITE_BINARY_CONFIGS),
            "same_binary": group_mean(sub, SAME_BINARY_CONFIGS),
            "nb_mixed": group_mean(sub, NB_MIXED_CONFIGS),
            "nbnb": sub[NBNB_CONFIG]["fault_rating"] if NBNB_CONFIG in sub else None,
        }
    return out


def complete_cells(gm):
    """Only cells where all four groups are present -- required for every
    test in this script, since each test's per-cell quantity needs all
    four group means."""
    return [v for v in gm.values()
            if None not in (v["opposite_binary"], v["same_binary"], v["nb_mixed"], v["nbnb"])]


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
    -- the permutation analog of a one-sample/paired t-test. Distribution-
    free, matching this project's permutation-test-first convention."""
    obs_mean = statistics.mean(diffs)
    rng = random.Random(seed)
    count_ge = 0
    for _ in range(n_perm):
        flipped = [d if rng.random() < 0.5 else -d for d in diffs]
        if abs(statistics.mean(flipped)) >= abs(obs_mean):
            count_ge += 1
    p = (count_ge + 1) / (n_perm + 1)
    return obs_mean, p


def write_one_sample_block(out, diffs, label):
    n, mean_d, sd_d, t, d_z = one_sample_stat(diffs)
    obs_mean, p = sign_flip_test(diffs)
    out.append(f"**{label}**: n={n} cells, mean={mean_d:+.3f}, t={t:.2f}, d_z={d_z:.3f}, "
                f"sign-flip permutation p={p:.4f} -- "
                f"{'reaches' if p < 0.05 else 'does not reach'} conventional significance.\n")


def main():
    rows = load_responses()
    cells = build_cells(rows)
    gm = cell_group_means(cells)
    complete = complete_cells(gm)

    out = []
    out.append("# Pairing structure (identity-sharing x NB-involvement) findings\n")
    out.append(f"Generated from `responses/confirmatory/*.csv` (n={len(rows)} rows). "
                f"Regenerate via `python scripts/analyze_pairing_structure_effect.py`. "
                "Item 5f, `docs/planned_analysis.md` -- a genuinely different, "
                "explicitly non-orientation question from "
                "`analysis/orientation_effect_findings.md` (items 5a-5e): does the "
                "gender-normativity/identity-sharing structure of a pairing change how "
                "the agent is judged? Covers all 9 gender configs via a real 2x2 "
                "factorial (identity-sharing x binary-involvement), not a social "
                "inference about presumed orientation. See this script's docstring and "
                "`docs/superpowers/specs/"
                "2026-08-21-orientation-and-pairing-structure-design.md` for full "
                "methodology, including why NB-NB is not pooled with NB-mixed "
                "pairings.\n")
    out.append(f"{len(complete)} of {len(gm)} cells have all four groups present and "
                "are used below.\n")

    diffs_identity = [
        statistics.mean([v["opposite_binary"], v["nb_mixed"]])
        - statistics.mean([v["same_binary"], v["nbnb"]])
        for v in complete
    ]
    out.append("## Main effect 1: identity-sharing (different vs. same), "
                "pooled over binary-involvement\n")
    out.append("Per cell: mean(opposite-binary, NB-mixed) vs. mean(same-binary, "
                "NB-NB) -- averaging the two subgroups' means, not row-count-weighting "
                "them.\n")
    write_one_sample_block(out, diffs_identity, "Different-identity minus same-identity")

    diffs_binary = [
        statistics.mean([v["nb_mixed"], v["nbnb"]])
        - statistics.mean([v["opposite_binary"], v["same_binary"]])
        for v in complete
    ]
    out.append("## Main effect 2: binary-involvement (NB-involved vs. binary-only), "
                "pooled over identity-sharing\n")
    out.append("Per cell: mean(NB-mixed, NB-NB) vs. mean(opposite-binary, "
                "same-binary).\n")
    write_one_sample_block(out, diffs_binary, "NB-involved minus binary-only")

    diffs_interaction = [
        (v["same_binary"] - v["opposite_binary"]) - (v["nbnb"] - v["nb_mixed"])
        for v in complete
    ]
    out.append("## Interaction: does the identity-sharing effect differ between "
                "binary-only and NB-involved pairings?\n")
    out.append("Per cell: (same-binary minus opposite-binary) minus (NB-NB minus "
                "NB-mixed) -- a paired, one-sample test on this derived quantity, not "
                "an unpaired two-group ANOVA, since both halves come from the same "
                "cell.\n")
    write_one_sample_block(out, diffs_interaction,
                            "Interaction (binary identity-sharing effect minus NB identity-sharing effect)")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_pairing_structure_effect.py`
Expected: exits 0, prints `Wrote .../analysis/pairing_structure_effect_findings.md`, and prints the full markdown report to stdout with no tracebacks.

- [ ] **Step 3: Hand-check one cell's arithmetic (required -- this is new methodology, not a routine sanity check)**

Run this to find one real, complete cell and print its raw rows:
```bash
python3 -c "
import csv, glob
from collections import defaultdict

cells = defaultdict(dict)
for f in sorted(glob.glob('responses/confirmatory/*.csv')):
    with open(f) as fh:
        for row in csv.DictReader(fh):
            key = (row['scenario_id'], row['severity'], row['model'])
            cells[key][(row['agent_gender'], row['partner_gender'])] = float(row['fault_rating'])

for key, sub in cells.items():
    needed = [('M','F'),('F','M'),('M','M'),('F','F'),('NB','M'),('NB','F'),('M','NB'),('F','NB'),('NB','NB')]
    if all(c in sub for c in needed):
        print('scenario/severity/model:', key)
        for c in needed:
            print(' ', c, '=', sub[c])
        break
"
```
This prints one `(scenario_id, severity, model)` triplet with all 9 configs present and their raw `fault_rating` values. By hand (or with a calculator), compute:
- `opposite_binary_mean` = mean of the MF and FM values
- `same_binary_mean` = mean of the MM and FF values
- `nb_mixed_mean` = mean of the NBM, NBF, MNB, FNB values
- `nbnb_mean` = the NBNB value alone
- `different_identity_mean` = mean(`opposite_binary_mean`, `nb_mixed_mean`)
- `same_identity_mean` = mean(`same_binary_mean`, `nbnb_mean`)
- Main effect 1 quantity for this cell = `different_identity_mean - same_identity_mean`
- Main effect 2 quantity for this cell = `mean(nb_mixed_mean, nbnb_mean) - mean(opposite_binary_mean, same_binary_mean)`
- Interaction quantity for this cell = `(same_binary_mean - opposite_binary_mean) - (nbnb_mean - nb_mixed_mean)`

Then add a one-off print statement inside `main()` (temporarily, or in a throwaway `python3 -c` snippet importing the script's functions) to print this same cell's entry from `gm` and confirm the script's computed values match your hand calculation exactly. Remove any temporary debug prints before committing -- this is a one-time verification step, not permanent code.

- [ ] **Step 4: Sanity-check the full output**

Run:
```bash
python3 -c "
import re
with open('analysis/pairing_structure_effect_findings.md') as f:
    text = f.read()
assert not re.search(r'\bnan\b', text, re.IGNORECASE), 'found a NaN in the output'
assert 'Main effect 1' in text and 'Main effect 2' in text and 'Interaction' in text
print('basic sanity checks passed')
print()
print(text)
"
```
Expected: `basic sanity checks passed`, followed by the full report. Confirm the reported cell count (`N of M cells have all four groups present`) is close to 810 (the same scale as every other cross-cell comparison in this project) -- if it's drastically smaller, investigate `cell_group_means`/`complete_cells` before trusting the results.

- [ ] **Step 5: Commit**

```bash
git add scripts/analyze_pairing_structure_effect.py analysis/pairing_structure_effect_findings.md
git commit -m "$(cat <<'EOF'
Add pairing-structure effect analysis (item 5f)

Tests whether the gender-normativity/identity-sharing structure of a
pairing changes how the agent is judged, via a real 2x2 factorial
(identity-sharing x binary-involvement) covering all 9 gender configs
-- explicitly not an orientation proxy, unlike items 5a-5e. Introduces
a sign-flip one-sample permutation test to this codebase (the paired
analog of the label-shuffle omnibus tests used elsewhere), verified
against a hand-computed cell before trusting the aggregate output.
EOF
)"
```

## Task 2: Document and update tracking

**Files:**
- Modify: `README.md` (Analysis section)
- Modify: `docs/planned_analysis.md` (new item 5f entry and summary table row)

- [ ] **Step 1: Add a README entry**

In the `## Analysis` section of `README.md`, after the `scripts/analyze_orientation_effect.py` bullet (add this one after Task 2 of the orientation-effect plan has run, or after the last existing bullet if that hasn't happened yet), insert:
```markdown
- **`scripts/analyze_pairing_structure_effect.py`** -- reads
  `responses/confirmatory/*.csv`, tests whether the gender-normativity/
  identity-sharing structure of a pairing (not presumed orientation)
  changes how the agent is judged, via a 2x2 factorial (identity-sharing x
  binary-involvement) covering all 9 gender configs. Introduces a
  sign-flip one-sample permutation test to this codebase. Writes
  `analysis/pairing_structure_effect_findings.md`. See
  `docs/superpowers/specs/2026-08-21-orientation-and-pairing-structure-design.md`.
```

- [ ] **Step 2: Add item 5f to `docs/planned_analysis.md`**

Before editing, get the real numbers: run
```bash
grep -A2 "Main effect 1" analysis/pairing_structure_effect_findings.md
grep -A2 "Main effect 2" analysis/pairing_structure_effect_findings.md
grep -A2 "^\*\*Interaction" analysis/pairing_structure_effect_findings.md
```
and read off the actual `n=`, `mean=`, `d_z=`, and `p=` values for all three tests. **Use those literal numbers below -- do not write placeholder text into the file.**

Add a new subsection immediately after item 5e's bullet in Section 5 of `docs/planned_analysis.md` (before the "## 6. RQ2" heading), titled `## 5f. Pairing structure (identity-sharing x NB-involvement) -- explicitly not orientation`, with a short paragraph (matching this file's existing prose style) explaining the motivation in 2-3 sentences (why NB-NB can't be pooled with NB-mixed under an orientation framing, referencing the design spec), then the three real results (main effect 1, main effect 2, interaction) using the values you just read, each with one sentence of plain-language interpretation.

- [ ] **Step 3: Add item 5f to the summary table**

Using the same real values you read in Step 2, add a new row to the
summary table near the bottom of `docs/planned_analysis.md`, immediately
after item 5e's row, in this format (substituting the actual numbers, not
the words "the real value"):
```
| 5f | Pairing structure (identity-sharing x NB-involvement, **explicitly not orientation**) | **implemented 2026-08-21**, `scripts/analyze_pairing_structure_effect.py` -- identity-sharing d_z=<the real value> (p=<the real value>), binary-involvement d_z=<the real value> (p=<the real value>), interaction d_z=<the real value> (p=<the real value>). |
```

- [ ] **Step 4: Commit**

```bash
git add README.md docs/planned_analysis.md
git commit -m "Document analyze_pairing_structure_effect.py and add item 5f to the tracked backlog"
```
