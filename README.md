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
--pass_type choices: confirmatory (1 run/vignette, low temp -- primary data), stability (N repeated runs/vignette, higher temp -- for the dispersion-based confidence metric), or confirmatory_hedge (same as confirmatory plus a `hedged` self-report field and a per-attempt log, for the RQ3 hedge-rate analysis -- see docs/prompt_and_measurement_protocol.md; writes to its own responses/confirmatory_hedge/ folder)
Optional: --n_samples, --temperature, --vignette_file to override the defaults (see --help for details), --verbose for per-call logs

Running the reasoning-text linguistic-bias analysis needs a separate venv on
Python >=3.10 (spaCy doesn't build on the system Python 3.9 used above):

```bash
/opt/homebrew/bin/python3.11 -m venv venv   # or any Python >=3.10
source venv/bin/activate
pip install -r requirements-analysis.txt
python -m spacy download en_core_web_sm
python scripts/analyze_reasoning_text.py
```

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
  `--pass_type confirmatory` (1 run/vignette, low temp), `stability` (N repeated
  runs/vignette, higher temp, for the dispersion-based confidence metric), or
  `confirmatory_hedge` (adds a `hedged` self-report field plus an always-on
  per-attempt log at `responses/confirmatory_hedge/<model>_attempt_log.csv`,
  for the RQ3 hedge-rate analysis -- see
  `docs/prompt_and_measurement_protocol.md`; additive, doesn't change
  `confirmatory`/`stability` behavior). Calls `validate.py` automatically at
  the end of every run.
- **`scripts/validate.py`** -- validates a collected responses CSV against the
  expected schema and value domains. Standalone: `python scripts/validate.py
  --file <path>`.
- **`requirements.txt`** -- pinned Python dependencies.

## Analysis

- **`scripts/analyze_fault_rating_bias.py`** -- reads
  `responses/confirmatory/*.csv` and `analysis/reasoning_features.csv`, runs
  the design-correct paired (scenario x severity x model held constant)
  gender-bias tests on `fault_rating` plus family/model/obligation_source
  moderator breakdowns, and checks whether the reasoning-text linguistic
  features track the numeric bias. Writes
  `analysis/fault_rating_bias_findings.md`.
- **`scripts/analyze_reasoning_text.py`** -- reads `responses/confirmatory/*.csv`,
  extracts three linguistic-bias features from each response's free-text
  `reasoning` field (LIB dispositional-abstraction score, agentic/communal
  domain-word rate, moral-intensity harsh-minus-mitigating rate), writes
  `analysis/reasoning_features.csv`. Requires `requirements-analysis.txt`
  (`spacy` + the `en_core_web_sm` model, `nltk`) on top of the base venv --
  spaCy needs Python >=3.10 (this repo's venv uses 3.11 via Homebrew, not the
  system Python 3.9). Method and validation notes: see the script's docstring
  and `project/project_status_summary.md`'s "Confirmatory-pass analysis"
  section.
- **`analysis/lexicons/agentic_communal.csv`**,
  **`analysis/lexicons/moral_intensity.csv`** -- the word lists
  `analyze_reasoning_text.py` matches against, one term per row with a
  `source_note` citing its literature basis and/or corpus frequency. Edit
  these (not the script) to adjust what counts as a hit.
- **`analysis/reasoning_features.csv`** -- generated output, one row per
  response (regenerate via `analyze_reasoning_text.py` after any lexicon or
  script edit).

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
