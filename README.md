# How To Run

How to run the pipeline

One-time setup (from the repo root):

```bash
python3 -m venv venv
source venv/bin/activate      
pip install -r requirements.txt
cp .env.example .env          # then edit .env and add your real OPENROUTER_API_KEY
```

Run collection for a given model and pass type (works whether you run it from the repo root or from inside scripts/ -- paths resolve relative to the script's own location, not the working directory):

```bash
python scripts/collect-responses.py --model claude_sonnet --pass_type confirmatory
```

--model choices: claude_sonnet, gpt5_mini, gemini_flash, llama33, deepseek_v3
--pass_type choices: confirmatory (1 run/vignette, low temp -- primary data) or stability (N repeated runs/vignette, higher temp -- for the dispersion-based confidence metric)
Optional: --n_samples, --temperature, --vignette_file to override the defaults (see --help for details)

---

# Repo Map

For current project status, open decisions, and what's blocking what, see
**`project/project_status_summary.md`** -- that is the one place tracking state;
this section only says what each file/folder *is*, not what state it's currently
in, so it doesn't need to be kept in sync with every content change.

## Design & content

- **`data/vignette_params.json`** -- single source of truth for the entire vignette
  design. Everything else here is either generated from this file or documentation
  about it. Contains `design_summary`, `intentionality_fixed_value`,
  `relationship_context_by_family`, `id_scheme`, `agent_labeling`,
  `obligation_sources`, and `families` (each with a `scenarios` array).
- **`scripts/generate_vignettes.py`** -- renders every drafted scenario across all
  4 gender configurations and both severities into `data/vignette_core_set.csv`.
- **`scripts/lint_vignette_params.py`** -- lints `vignette_params.json` for the
  mild/severe-contradiction and antecedent bug classes documented in
  `docs/vignette_writing_standards.md` item G. Run after editing the params file,
  before regenerating the CSV.
- **`data/vignette_core_set.csv`** -- generated output, one row per vignette.

## Data collection pipeline

- **`scripts/collect-responses.py`** -- reads `data/vignette_core_set.csv`, calls
  each model via OpenRouter, writes `responses/<pass_type>/<model>.csv`.
  `--pass_type confirmatory` (1 run/vignette, low temp) or `stability` (N repeated
  runs/vignette, higher temp, for the dispersion-based confidence metric). Calls
  `validate.py` automatically at the end of every run.
- **`scripts/validate.py`** -- validates a collected responses CSV against the
  expected schema and value domains. Standalone: `python scripts/validate.py
  --file <path>`.
- **`requirements.txt`** -- pinned Python dependencies.

## Reasoning & reference

- **`docs/vignette_schema.md`** -- the structural reasoning behind the design: why
  obligations are held constant within a scenario, severity as a family-specific
  construct, the canonical sentence-beat order, agent labeling. Carries its own
  design-change notices flagging superseded sections; `vignette_params.json` wins
  wherever the two disagree.
- **`docs/vignette_writing_standards.md`** -- the post-drafting quality checklist
  (items A-G).
- **`docs/vignette_generation_spec.md`** -- a consolidated, self-contained brief
  intended to be handed directly to an LLM to draft further scenarios that already
  comply with the schema, taxonomy, and writing standards.
- **`docs/vignette_narrative_templates.md`** -- human-readable rendering of every
  drafted scenario's template.
- **`docs/prompt_and_measurement_protocol.md`** -- the actual system prompt,
  output schema, and confidence-measurement protocol.

## Paper

- **`paper/`** -- JUDGe 2026 workshop submission draft, one file per section
  (mirrors an Overleaf tab-per-section layout). `paper/sources/` holds the raw
  literature review and design-decision traceability notes it was built from.
- **`Formatting_Instructions_For_NeurIPS_2026/`** -- the downloaded NeurIPS 2026
  template, kept as reference/instructions only, never edited or compiled from
  directly.

## Project tracking

- **`project/project_status_summary.md`** -- current state, core decisions, and
  open items. Start here.
- **`project/review_sample_20.md`** -- a 20-vignette stratified human
  read-through sample, kept in sync with `data/vignette_core_set.csv`.
