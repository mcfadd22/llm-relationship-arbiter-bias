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
