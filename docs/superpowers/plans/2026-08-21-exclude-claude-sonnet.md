# Exclude claude_sonnet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Exclude `claude_sonnet` from every analysis in this project (a genuine vignette-drafting familiarity confound, confirmed by Meredith), and bring every already-committed analysis that included it up to date against the corrected 4-model dataset, per `docs/superpowers/specs/2026-08-21-exclude-claude-sonnet-design.md`.

**Architecture:** No new code. Move `responses/confirmatory/claude_sonnet.csv` out of the directory every `analyze_*.py` script globs (so the exclusion applies to every script automatically, with zero code changes), update three documentation files to record the decision and its rationale, then re-run five already-working scripts in dependency order against the corrected data and commit their updated output.

**Tech Stack:** Bash (file move), no code changes to any Python script.

---

## Verification approach

This is a data-correction task, not new functionality — verification means: (1) confirming the file move actually removes `claude_sonnet` from every regenerated output, (2) actually reading each diff rather than just checking exit codes, since the spec explicitly warns to expect real numeric shifts (not just a smaller n) given `claude_sonnet` had the single largest effect size among the 5 models before this exclusion.

## Task 1: Move the excluded response file

**Files:**
- Move: `responses/confirmatory/claude_sonnet.csv` -> `responses/excluded/claude_sonnet.csv`
- Create: `responses/excluded/README.md`

- [ ] **Step 1: Create the directory and move the file**

```bash
mkdir -p responses/excluded
git mv responses/confirmatory/claude_sonnet.csv responses/excluded/claude_sonnet.csv
```

- [ ] **Step 2: Write the README explaining why**

Create `responses/excluded/README.md`:

```markdown
# Excluded response data

## claude_sonnet.csv (moved here 2026-08-21)

`claude_sonnet` (`anthropic/claude-sonnet-5`) is excluded from all
analyses in this project. Meredith drafted the vignette scenario text
using Claude Code -- since `claude_sonnet` is one of the 5 models in the
study's roster judging those same vignettes, this is a genuine
familiarity/self-authorship confound, not shared by the other 4 models
(`gpt5_mini`, `gemini_flash`, `llama33`, `deepseek_v3`), none of which
touched vignette drafting.

This file is preserved here for reference, not deleted. Every
`analyze_*.py` script in `scripts/` globs `responses/confirmatory/*.csv`,
so moving this file out of that directory excludes it from every current
and future analysis automatically, without any script needing to filter
it explicitly.

A replacement 5th model is an open, deferred decision -- see
`project/project_status_summary.md` and
`docs/superpowers/specs/2026-08-21-exclude-claude-sonnet-design.md`.
```

- [ ] **Step 3: Verify the glob no longer picks it up**

Run: `python3 -c "import glob; print(sorted(glob.glob('responses/confirmatory/*.csv')))"`
Expected: a list of exactly 4 files (`deepseek_v3.csv`, `gemini_flash.csv`, `gpt5_mini.csv`, `llama33.csv`), no `claude_sonnet.csv`.

- [ ] **Step 4: Commit**

```bash
git add responses/excluded/README.md
git commit -m "$(cat <<'EOF'
Exclude claude_sonnet from all analyses

Meredith drafted the vignette scenario text using Claude Code;
claude_sonnet (anthropic/claude-sonnet-5) is one of the 5 study
models judging those same vignettes -- a genuine familiarity confound
not shared by the other 4 models. Moves the response file out of the
directory every analyze_*.py script globs, so the exclusion applies
automatically everywhere with no code changes. Data preserved, not
deleted. Replacement 5th model is a separate, deferred decision.
EOF
)"
```

(Note: `git mv` stages the move automatically; this commit captures both the move and the new README together.)

## Task 2: Update project_status_summary.md

**Files:**
- Modify: `project/project_status_summary.md`

- [ ] **Step 1: Add a prominent exclusion notice near the top**

Find this text near the top of `project/project_status_summary.md`:

```
This replaces both the prior version of this file and `project/README_for_thulasi.md`
(deleted 2026-08-11 -- fully superseded, no unique content, was drifting out of sync
with reality and risked being read as current when it wasn't). This is now the one
place to read for "where does this stand and why" -- update it in place going
forward rather than creating another parallel status doc.

## Current state, in one paragraph
```

Replace with:

```
This replaces both the prior version of this file and `project/README_for_thulasi.md`
(deleted 2026-08-11 -- fully superseded, no unique content, was drifting out of sync
with reality and risked being read as current when it wasn't). This is now the one
place to read for "where does this stand and why" -- update it in place going
forward rather than creating another parallel status doc.

## claude_sonnet excluded from all analyses (2026-08-21)

**claude_sonnet is excluded from every analysis in this project, effective
2026-08-21, and should not be included in any results or interpretation
going forward.** Meredith drafted the vignette scenario text using Claude
Code -- `claude_sonnet` (`anthropic/claude-sonnet-5`) is one of the 5
models in the study's roster, so having it also judge vignettes it (or a
closely related model) helped author is a genuine familiarity/self-
authorship confound, not shared by the other 4 models (`gpt5_mini`,
`gemini_flash`, `llama33`, `deepseek_v3`). Its response data is preserved
at `responses/excluded/claude_sonnet.csv` (moved out of
`responses/confirmatory/`, which every analysis script globs) rather than
deleted. **A replacement 5th model is an open, deferred decision, not yet
made** -- there was no principled reason the original roster needed
exactly 5 models, so this should not be read as "the study needs a 5th
model," just as "the roster is currently 4, and whether/how to expand it
again is a separate question." See
`docs/superpowers/specs/2026-08-21-exclude-claude-sonnet-design.md` for
the full design and `paper/limitations.tex` for the paper-facing framing.

## Current state, in one paragraph
```

- [ ] **Step 2: Commit**

```bash
git add project/project_status_summary.md
git commit -m "Document claude_sonnet exclusion in project status summary"
```

## Task 3: Update docs/planned_analysis.md

**Files:**
- Modify: `docs/planned_analysis.md`

- [ ] **Step 1: Add a notice near the top**

Find this text near the top of `docs/planned_analysis.md`:

```
Every test that already has a script is marked **[implemented]** and will
just be re-run on the new data. Tests marked **[needs new code]** extend
existing logic to the NB gender configs (or a new bias dimension) and don't
exist yet. Tests marked **[decision needed]** have an open methodological
choice that should be settled *before* results come in, consistent with how
the ambivalent-sexism contrast and RQ1-3 were handled.

---
```

Replace with:

```
Every test that already has a script is marked **[implemented]** and will
just be re-run on the new data. Tests marked **[needs new code]** extend
existing logic to the NB gender configs (or a new bias dimension) and don't
exist yet. Tests marked **[decision needed]** have an open methodological
choice that should be settled *before* results come in, consistent with how
the ambivalent-sexism contrast and RQ1-3 were handled.

**claude_sonnet excluded (2026-08-21).** Every result below that
references "5 models" predates this exclusion and is being progressively
re-run against the corrected 4-model dataset (`gpt5_mini`, `gemini_flash`,
`llama33`, `deepseek_v3`) -- see `project/project_status_summary.md`'s
"claude_sonnet excluded" section and `docs/superpowers/specs/
2026-08-21-exclude-claude-sonnet-design.md` for why. A new backlog item
(below, in the Summary table) tracks the deferred decision on whether/how
to add a replacement 5th model.

---
```

- [ ] **Step 2: Add a new backlog item to the summary table**

Find the last row of the summary table near the bottom of `docs/planned_analysis.md` (the `| 10c | ... |` row) and add a new row immediately after it:

```
| 13 | Decide on a replacement 5th model (or explicitly settle on 4) | **deferred, not urgent** -- claude_sonnet excluded 2026-08-21 for a vignette-drafting familiarity confound (see `project/project_status_summary.md`). No principled reason the roster needs exactly 5, so this is an open question to revisit deliberately, not a gap to rush to fill. |
```

- [ ] **Step 3: Commit**

```bash
git add docs/planned_analysis.md
git commit -m "Document claude_sonnet exclusion and add deferred 5th-model item to the backlog"
```

## Task 4: Update paper/limitations.tex

**Files:**
- Modify: `paper/limitations.tex`

- [ ] **Step 1: Add the new limitation**

Find this text at the end of `paper/limitations.tex`:

```latex
A model-based novelty
check (prompting a separate call to guess whether a vignette is
real-vs-synthetic) is designed but not yet run.
```

Replace with:

```latex
A model-based novelty
check (prompting a separate call to guess whether a vignette is
real-vs-synthetic) is designed but not yet run. One model from the
original evaluation roster, claude-sonnet-5, was excluded from all
analyses after data collection: the vignette scenario text was drafted
with assistance from Claude Code, and evaluating vignettes with a model
from the same family that helped draft them introduces a familiarity
confound not shared by the other four evaluated models. All results in
this paper reflect the four-model roster (GPT-5-mini, Gemini 2.5 Flash,
Llama 3.3 70B, DeepSeek V3.2) after this exclusion.
```

- [ ] **Step 2: Commit**

```bash
git add paper/limitations.tex
git commit -m "Disclose claude_sonnet exclusion in paper limitations section"
```

## Task 5: Re-run analyze_reasoning_text.py

**Files:**
- Regenerate: `analysis/reasoning_features.csv`

- [ ] **Step 1: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_reasoning_text.py`
Expected: exits 0, prints `Wrote N rows to .../analysis/reasoning_features.csv` where N is roughly 4/5 of the previous row count (this script has no model-count assumptions in its code -- it just processes however many rows exist in `responses/confirmatory/*.csv`).

- [ ] **Step 2: Read the diff and confirm claude_sonnet rows are gone**

Run: `git diff --stat analysis/reasoning_features.csv` then `grep -c claude_sonnet analysis/reasoning_features.csv`
Expected: the stat shows a large diff (most rows changed since row order/count shifted); the grep returns `0`.

- [ ] **Step 3: Commit**

```bash
git add analysis/reasoning_features.csv
git commit -m "Re-run analyze_reasoning_text.py after excluding claude_sonnet"
```

## Task 6: Re-run analyze_fault_rating_bias.py

**Files:**
- Regenerate: `analysis/fault_rating_bias_findings.md`

- [ ] **Step 1: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_fault_rating_bias.py`
Expected: exits 0, no tracebacks.

- [ ] **Step 2: Read the full diff -- do not just check that it ran**

Run: `git diff analysis/fault_rating_bias_findings.md`

Read the actual diff output. Specifically check and note in your task report:
- The core M-F effect's new `n`, `mean diff`, `d_z` (previously n=1619, diff=+0.164, d_z=0.316).
- Whether `claude_sonnet` still appears anywhere in the per-model breakdown (it must not).
- The "Formal test: does family (or model) significantly moderate the gender effect?" section's new p-values (previously family p=0.0012, model p=0.0188, both significant) -- **the spec explicitly flags this as likely to change materially**, possibly crossing the p<0.05 threshold in either direction now that the model with the largest effect size is removed. Report whatever the new values actually are; do not assume they stayed significant.
- The primary/secondary ambivalent-sexism contrast test's new values (previously both null).

- [ ] **Step 3: Commit**

```bash
git add analysis/fault_rating_bias_findings.md
git commit -m "$(cat <<'EOF'
Re-run analyze_fault_rating_bias.py after excluding claude_sonnet

See task report for the actual before/after numbers -- expect real
shifts, not just smaller n, since claude_sonnet had the largest
effect size among the 5 models.
EOF
)"
```

## Task 7: Re-run analyze_agent_identity_effect.py

**Files:**
- Regenerate: `analysis/agent_identity_effect_findings.md`

- [ ] **Step 1: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_agent_identity_effect.py`
Expected: exits 0, no tracebacks. This one runs the within-cell-shuffle omnibus test (~2400 cells x 20000 permutations for Section A, ~800 cells x 20000 for Section B) -- expect roughly 1-2 minutes; run in the background if needed.

- [ ] **Step 2: Read the diff**

Run: `git diff analysis/agent_identity_effect_findings.md`

Read it. Confirm `claude_sonnet` no longer appears in the per-model breakdown, and note the new Section A (M-F, M-NB, F-NB) and Section C omnibus F/p values compared to before (M-F: d_z=0.29; M-NB: d_z=0.23; F-NB: d_z=-0.07; Section A omnibus F=174.260, p<0.0001; Section B omnibus p=0.0001).

- [ ] **Step 3: Commit**

```bash
git add analysis/agent_identity_effect_findings.md
git commit -m "Re-run analyze_agent_identity_effect.py after excluding claude_sonnet"
```

## Task 8: Re-run family_omnibus_power_analysis.py

**Files:**
- Regenerate: `analysis/family_power_analysis_findings.md`

- [ ] **Step 1: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/family_omnibus_power_analysis.py`
Expected: exits 0, no tracebacks.

- [ ] **Step 2: Read the diff**

Run: `git diff analysis/family_power_analysis_findings.md`

Read it. Note the new baseline `n` per family (previously n=179-180, computed dynamically -- should now be smaller since one model's ~180-ish rows per family are gone) and whether the top-3-by-effect-size family ranking (previously Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice) changed.

- [ ] **Step 3: Commit**

```bash
git add analysis/family_power_analysis_findings.md
git commit -m "Re-run family_omnibus_power_analysis.py after excluding claude_sonnet"
```

## Task 9: Re-run analyze_confidence_ambiguity.py

**Files:**
- Regenerate: `analysis/confidence_ambiguity_findings.md`

- [ ] **Step 1: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_confidence_ambiguity.py`
Expected: exits 0, no tracebacks.

- [ ] **Step 2: Read the diff**

Run: `git diff analysis/confidence_ambiguity_findings.md`

Read it. Note the new pair-level confidence-vs-gap correlation (previously r=-0.079, p=0.0016 -- flagged elsewhere this session as newly significant and "worth revisiting"; check whether it's still significant after removing claude_sonnet).

- [ ] **Step 3: Commit**

```bash
git add analysis/confidence_ambiguity_findings.md
git commit -m "Re-run analyze_confidence_ambiguity.py after excluding claude_sonnet"
```

## Task 10: Final summary

**Files:** none (reporting only)

- [ ] **Step 1: Compile a summary of what changed**

After all prior tasks are committed, write a short summary (as your final report to the user/controller, not a new file) listing: which previously-reported significant results (if any) lost significance, which previously-null results (if any) gained it, and the new headline M-F effect size -- pulling from the notes already gathered in Tasks 6-9's Step 2s. This is the actual deliverable of this whole plan: knowing what changed, not just that the scripts re-ran.
