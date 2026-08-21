# Exclude claude_sonnet from all analyses -- design

## Motivation

Meredith confirmed she personally drafted the vignette scenario text using
Claude Code. `claude_sonnet` (`anthropic/claude-sonnet-5`) is one of the 5
models in the study's roster whose gender bias is measured by judging
those same vignettes. This is a genuine familiarity/self-authorship
confound specific to `claude_sonnet`'s results -- not a hypothetical one,
and not shared by the other 4 models (`gpt5_mini`, `gemini_flash`,
`llama33`, `deepseek_v3`), none of which touched vignette drafting.

Mildly suggestive (not conclusive) supporting observation:
`claude_sonnet` already showed the *largest* agent-gender effect size among
all 5 models before this decision (d_z=0.42, the most skewed M:F
disagreement ratio at 6.58:1, per the now-superseded
`fault_rating_bias_findings.md`) -- consistent with a drafting-familiarity
confound, though equally explainable by other factors. Not treated as
proof, just as context for why this was worth investigating rather than
dismissing.

Decision (confirmed with Meredith): **exclude `claude_sonnet` from all
analyses and results interpretation, effective immediately.** A
replacement 5th model is explicitly **not** decided now -- flagged for
future deliberation, since there was no principled reason the original
roster needed exactly 5 models. Nothing in this spec should read as
committing to restoring a 5-model roster.

## Scope

**In scope:**
1. Move `responses/confirmatory/claude_sonnet.csv` out of the glob path
   every analysis script reads, so exclusion is automatic and total (every
   current and future `analyze_*.py` script globs
   `responses/confirmatory/*.csv` -- moving the file, not touching every
   script, is the DRY fix).
2. Update the project's central status/tracking docs to document the
   exclusion and its rationale.
3. Add a new limitation to `paper/limitations.tex`.
4. Re-run every already-committed analysis that included `claude_sonnet`,
   since those are live results currently describing a 5-model study that
   no longer reflects the decided scope.

**Explicitly out of scope:**
- Deciding on, sourcing, or collecting data for a replacement 5th model --
  a separate, future, longer-lead-time decision (would need a new primary
  data-collection run, likely Thulasi's to execute per this project's
  established division of labor).
- Re-running the four *staged-but-not-yet-executed* plans (item 3's
  `analyze_partner_identity_effect.py`, item 7b's
  `score_scenario_sexism_content.py`, items 5a-5e's
  `analyze_orientation_effect.py`, item 5f's
  `analyze_pairing_structure_effect.py`) -- none of these have been run
  yet, so they need no rework; whenever they eventually run, they'll
  automatically read the corrected 4-model dataset. (`score_scenario_sexism_content.py`
  is unaffected either way -- it scores scenario content, not per-model
  responses.)

## Mechanism: move, don't filter

Move `responses/confirmatory/claude_sonnet.csv` to
`responses/excluded/claude_sonnet.csv` (preserved, not deleted -- useful
for reference and fully reversible if this decision is ever revisited).
Add `responses/excluded/README.md` explaining why the file lives there and
linking to the fuller explanation in `project/project_status_summary.md`.

This is preferred over adding an `EXCLUDED_MODELS` filter constant to every
`analyze_*.py` script: the move fixes every existing script with zero code
changes, and every future script automatically inherits the exclusion by
construction (it globs the same directory) rather than by remembering to
add a filter. The tradeoff -- a script's own code no longer self-documents
which models it covers -- is handled by each re-run's regenerated
"Generated from `responses/confirmatory/*.csv` (n=... rows)" header line
naturally reflecting the smaller n once the file is moved, plus the
central documentation update below.

## Documentation updates

- **`project/project_status_summary.md`**: add a prominent entry (top-level,
  not buried) stating the exclusion, the reason (Meredith drafted vignette
  text via Claude Code; `claude_sonnet` is a study subject judging that
  same text), the date, and that the 5th-model question is open/deferred,
  not decided. Cross-reference from the existing "Current state, in one
  paragraph" section so it's not missed.
- **`docs/planned_analysis.md`**: add a note near the top (in the existing
  status framing, alongside the other "before treating this data as
  analysis-ready" caveats) that all analyses below now describe a 4-model
  roster, and add a new tracked backlog item for "decide on a replacement
  5th model (or explicitly settle on 4)" -- explicitly not urgent, listed
  as deferred.
- **`paper/limitations.tex`**: add a new limitation sentence disclosing the
  exclusion and its rationale -- this is a citable methodological-
  transparency point (proactively catching and correcting a confound) once
  documented, not just a loose end to hide.

## Re-run scope

Re-run, in this order (later ones may depend on earlier ones' output
files):
1. `scripts/analyze_reasoning_text.py` (regenerates
   `analysis/reasoning_features.csv` -- needed before the next script,
   which reads it)
2. `scripts/analyze_fault_rating_bias.py` (the headline findings,
   `analysis/fault_rating_bias_findings.md`)
3. `scripts/analyze_agent_identity_effect.py`
   (`analysis/agent_identity_effect_findings.md`)
4. `scripts/family_omnibus_power_analysis.py`
   (`analysis/family_power_analysis_findings.md`)
5. `scripts/analyze_confidence_ambiguity.py`
   (`analysis/confidence_ambiguity_findings.md`)

Each of these already prints its own live row/pair counts in its output
header (no hardcoded model-count assumptions were found in any of them
during this project's earlier review passes), so no code changes are
needed in any of them -- only re-running against the corrected data
directory.

**Expect real numeric changes, not just smaller n.** Removing the model
with the single largest agent-gender effect size will very likely shift
pooled effect sizes downward to some degree, and could change which
significance thresholds are or aren't crossed in the family/model omnibus
tests (`fault_rating_bias_findings.md`'s "Formal test" section, currently
significant at p=0.0012/p=0.019) -- this needs to be read and reported
honestly after re-running, not assumed to be unchanged.

## Verification

Matches this codebase's convention: run each script end-to-end, confirm
`claude_sonnet` no longer appears in any per-model breakdown table in the
regenerated output, and confirm each file's own reported row/pair counts
dropped by roughly one-fifth (consistent with removing one of five models)
rather than by some other fraction (which would indicate the exclusion
didn't apply cleanly). Diff each regenerated file against its prior
committed version and read the actual changes -- don't just check that the
scripts ran without error.
