# Next Steps

**Last updated: 2026-08-21.** A short, skimmable orientation doc. For full
methodology, numbers, and history, see `docs/planned_analysis.md` (the
detailed, continuously-updated backlog) and the design specs/plans under
`docs/superpowers/specs/` and `docs/superpowers/plans/`.

## Data integrity note (read this first)

`claude_sonnet` is excluded from all analyses as of 2026-08-21 -- Meredith
drafted the vignette scenario text using Claude Code, and `claude_sonnet`
was one of the 5 study models judging those same vignettes, a genuine
familiarity confound. All results below reflect the corrected 4-model
roster (`gpt5_mini`, `gemini_flash`, `llama33`, `deepseek_v3`). Full
rationale: `project/project_status_summary.md`'s "claude_sonnet excluded"
section and `docs/superpowers/specs/2026-08-21-exclude-claude-sonnet-design.md`.
A replacement 5th model is an open, deliberately deferred decision (item
13) -- not urgent, no principled reason the roster needs exactly 5.

## Done this session, verified

- **Core binary M-F effect** re-confirmed on the full, corrected dataset
  (d_z=0.291) -- `analysis/fault_rating_bias_findings.md`.
- **Family/model heterogeneity** (RQ2) -- family moderation significant
  and strengthened after the exclusion (p=0.0002); model moderation
  significant but fragile (p=0.038).
- **Pre-registered ambivalent-sexism contrast** (item 7) -- confirmatory
  replication does not succeed (both primary and secondary tests null,
  secondary now borderline at p=0.059).
- **Agent-identity effect** (item 2, M/F/NB) -- NB patterns closer to F
  than M; note the F-vs-NB contrast lost significance after excluding
  claude_sonnet (a real, reportable conclusion change).
- **Same-identity relationships** (item 4, MM/FF/NB-NB) -- NB-NB patterns
  with FF, not MM.
- **Partner-identity effect** (item 3, new) -- partner=M gets *less* blame
  attributed to the agent than partner=F or partner=NB -- a distinct,
  complementary axis to item 2, not a contradiction.
- **Per-family breakdown of items 2/3/4** (item 4b, new) -- the headline
  finding of this whole session's work: domain concentration is tied
  specifically to comparisons involving **M**, not to "NB-relatedness" in
  general. M-linked comparisons (agent-identity M-F/M-NB, same-identity
  MM-FF/MM-NBNB) track the binary bias's domain ranking closely
  (Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice).
  Comparisons not involving M (agent-identity F-NB, all partner-identity
  comparisons, same-identity FF-NBNB) show a distinct, unexplained pattern
  concentrated in provider/caregiving families instead. See item 4b in
  `docs/planned_analysis.md` for full numbers.

## Staged and ready to run (spec'd, plan'd, not yet executed)

- **Items 5a-5e** -- presumed relationship orientation (opposite-gender
  MF/FM vs. same-gender MM/FF; NB deliberately excluded from this specific
  axis). `docs/superpowers/plans/2026-08-21-orientation-effect.md`.
- **Item 5f** -- pairing structure (identity-sharing x NB-involvement, a
  real 2x2 factorial covering all 9 configs, explicitly *not* an
  orientation proxy). `docs/superpowers/plans/2026-08-21-pairing-structure-effect.md`.
- **Item 7b** -- scenario-level ambivalent-sexism content scoring
  (exploratory/post-hoc, ~$1 LLM coding cost, external coder model).
  `docs/superpowers/plans/2026-08-21-scenario-sexism-content-scoring.md`.

None of these three need new primary data collection -- everything reads
from `responses/confirmatory/*.csv` as it already stands (7b needs a new,
cheap *coding* pass, not new fault-rating collection).

## Still open, not yet designed

- **Item 9** -- confidence-vs-gender-gap correlation is now significant
  (r=-0.068, p=0.0125) but was previously dismissed as "not primary."
  Needs a framing decision, not code.
- **Items 10a-c** -- reasoning-text pattern-discovery scale-up (10a,
  independent of any collection run), disparate-impact ratio (10b, needs
  the cutpoint decision), regard score (10c, lower priority).
- **Item 0** -- NB-tag registration/retry-rate check. Not recoverable
  retroactively; needs a `collect-responses.py` code change (Thulasi's
  file) and a future run to do properly.
- **Item 13** -- replacement 5th model. Deliberately deferred, not urgent.
- **`README.md`/`scripts/collect-responses.py`** still list `claude_sonnet`
  as a valid `--model` choice -- someone re-running collection could
  accidentally undo the exclusion. Worth a quick fix; touches Thulasi's
  file, flagged rather than changed unilaterally.
- Reasoning-text analysis (lexicon + pairwise coding) has never been
  extended to the NB comparisons -- items 8/10a are both scoped to M-vs-F
  only. Identified as a candidate direction, not yet spec'd.
- NB "erasure/engagement" (does the model meaningfully engage with
  nonbinary identity in its reasoning, or default to silence) is still
  just an ad hoc spot-check (project status doc open item 10), not a
  formal analysis.
- Severity as a moderator of the gender/NB effects -- currently untouched;
  severity is only used for the manipulation check so far.

## Suggested priority, if picking up cold

1. Run the three staged plans (5a-5e, 5f, 7b) -- they're ready, reviewed,
   and cheap.
2. Decide item 9's framing (no code needed).
3. Design and build the reasoning-text-for-NB and/or erasure-formalization
   directions -- these pair well with the numeric NB findings and are
   likely stronger GeBNLP material than 10b/10c.
4. Fix the `README.md`/`collect-responses.py` stale `claude_sonnet` option
   (small, but real risk of silently undoing the exclusion).
5. Item 13 (5th model) and item 0 (full retry-rate check) whenever there's
   appetite for new data collection -- neither is blocking anything else.
