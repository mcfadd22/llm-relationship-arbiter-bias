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

--------
# Document Inventory -- Repo Upload

Snapshot as of this writing. **All 36 target scenarios are now drafted and the full core set (288 vignettes) has been generated.** This supersedes the earlier "12 of 36" partial-content snapshot.

---

## Design & content

### `data/vignette_params.json`
**What it is:** Single source of truth for the entire design. Everything else in this repo is either generated from this file or documentation about it.
**Contains:** `design_summary` (core formula, DV design, robustness-arm sizing, sequencing rules), `intentionality_fixed_value`, `relationship_context_by_family`, `id_scheme`, `agent_labeling`, `obligation_sources` (8 cited types), and `families` -- each with a `scenarios` array (4 per family, 36 total).
**State:** Architecture complete and stable. **Content now complete -- 36/36 scenarios drafted** (all 9 families have all 4 scenarios). A tone-consistency audit was run against every `knowing_but_nonmalicious` explanation across all 36 scenarios (not just the original 12): one issue was found and fixed in the newly drafted content (EMOLAB-03 read as vague minimization rather than clear awareness) and one was found and fixed in previously-approved content (FINPROV-01 read as dismissive -- "regardless of what partner would think" -- rather than the plain misprioritization tone used elsewhere). Two earlier known bugs (a subject/object pronoun error, and a possessive-pronoun error) remain fixed at the schema level and did not recur in the new content. **Latest change:** the former `name_bank`/`pronoun_map` fields (gender-neutral names, e.g. Alex/Riley, with pronoun-carried gender) were retired and replaced with `agent_labeling` -- agents are now anonymized `Agent 1`/`Agent 2` labels, gender is stated once per agent as an explicit `(female)`/`(male)` tag at first mention, and no pronouns are used anywhere in the rendered text.

### `scripts/generate_vignettes.py`
**What it is:** The generator -- reads `data/vignette_params.json`, renders every drafted scenario across all 4 gender configurations (MF/FM/MM/FF) and both severities, writes `data/vignette_core_set.csv`.
**State:** Updated to render the anonymized `Agent 1`/`Agent 2` + gender-tag scheme (no name-pair assignment, no pronoun substitution). Also fixed a path bug that resolved `vignette_params.json`/`vignette_core_set.csv` relative to `scripts/` instead of `data/` -- it now resolves both relative to the repo's `data/` directory regardless of invocation directory.

### `data/vignette_core_set.csv`
**What it is:** Generated output -- one row per vignette, full rendered text plus all factor columns (`scenario_id`, `task_object`, `violation_form`, `relationship_context`, `obligation_source`, gender/severity). `agent_name`/`partner_name` columns are now constant (`Agent 1`/`Agent 2`), kept for schema compatibility with `validate.py`/`collect-responses.py`.
**State:** **288 rows -- full target reached** (36 scenarios x 4 gender configs x 2 severity), regenerated with the anonymized agent-labeling scheme. Grammar/formatting audit passes clean at 0 issues (no unfilled placeholders, no double periods/spaces -- pronoun-case checks no longer apply since no pronouns are used). Word-count parity checked within each scenario's 8 cells -- no scenario exceeds a 15% spread.

**Scope question from the last update, now resolved:** "core" is redefined to mean all 4 gender configurations at equal weight -- 9 families x 4 scenarios x 4 gender configs (MF/FM/MM/FF) x 2 severity = 288. Same-gender pairs are not a separate supplementary arm anymore; that arm is retired as redundant now that gender_configuration is fully crossed inside the core itself (`design_summary.same_gender_supplementary.status` in the JSON is explicitly marked `REMOVED`). Total planned inventory recalculates to 288 core + 72 intentionality-robustness + 72 contamination/generalization = **432** (down from the earlier 324 figure, which assumed same-gender as a separate 36-vignette arm).

---
## Data collection pipeline
### 'scripts/collect-responses.py'

What it is: The data collection script - reads data/vignette_core_set.csv, calls each model via OpenRouter, and writes one row per (vignette, model, sample) to responses/<pass_type>/<model>.csv. Implements the system prompt and JSON schema from docs/prompt_and_measurement_protocol.md, with two separate --pass_type modes (confirmatory: 1 run/vignette at low temperature; stability: N repeated runs/vignette at higher temperature, for the dispersion-based confidence metric). Calls validate.py automatically at the end of every run. Paths are resolved relative to the repo root via the script's own location, so it runs correctly whether invoked from the repo root or from inside scripts/. Model roster finalized: 5 models across 4 providers (Anthropic Claude Sonnet 5, OpenAI GPT-5-mini, Google Gemini 2.5 Flash, Meta Llama 3.3 70B, DeepSeek V3.2) 

### 'scripts/validate.py'

What it is: Validates a collected responses CSV against the expected schema and value domains (column set, fault_rating 0-7, confidence 0-100, gender/severity/intentionality/pass_type enums). Runs automatically at the end of collect-responses.py, or standalone via python scripts/validate.py --file <path>. 

### 'requirements.txt'

What it is: Pinned Python dependencies for the collection pipeline (langchain, langchain-openai, pandas, python-dotenv, pydantic)

---

## Reasoning & reference

### `docs/vignette_schema.md`
**What it is:** The structural reasoning behind the design -- why obligations are held constant within a scenario, why severity is a construct with family-specific proxies, the canonical sentence-beat order, agent labeling.
**State:** Updated -- §4 (formerly "Name bank") now documents the anonymized `Agent 1`/`Agent 2` + gender-tag scheme and marks the old name/pronoun design superseded; §6's worked example got a current-format rendering alongside the retired one. Carries a design-change notice at the top flagging which original sections are superseded vs. still valid. `data/vignette_params.json` wins wherever the two disagree.

### `docs/vignette_narrative_templates.md`
**What it is:** Human-readable rendering of every drafted scenario's template, generated directly from the JSON.
**State:** Updated -- placeholder legend now documents that `{agent}`/`{partner}` resolve to the literal labels `Agent 1`/`Agent 2` and that the old pronoun placeholders no longer carry pronoun grammar (see the v4 note at the top of the doc). Also corrects a wording mismatch inherited from earlier drafts: the closing question now reads "Was {agent} in the wrong?" to match `prompt_and_measurement_protocol.md`'s actual system prompt, rather than the placeholder "the asshole?" phrasing used before that framing decision was finalized.

### `docs/vignette_writing_standards.md`
**What it is:** Post-drafting quality checklist.
**State:** Updated -- item B (no gendered language) now reflects that gender comes solely from the explicit `Agent 1 (female)`/`Agent 2 (male)` tag, with no pronouns permitted anywhere; item A's closing-question check now notes the question is fully fixed text, not "verbatim except for name." The scenario-balance check (item E) and tone-consistency check (item F) were both applied against the new content as part of the prior content-completion update -- worth noting in the doc itself that both have now been run against the full 36, not just the original 12, next time this file is touched.

---

## Measurement design

### `docs/prompt_and_measurement_protocol.md`
**State:** Updated -- the example user message and the "why gender is never mentioned in the prompt" section now reflect the anonymized `Agent 1`/`Agent 2` + gender-tag scheme instead of the retired Alex/Riley name-and-pronoun example.

---

## Project tracking (useful context, not part of the dataset itself)

### `project/README_for_thulasi.md`
**State:** Updated this round to reflect 36/36 scenarios and 288/288 vignettes.

### `project/project_status_summary.md`
**State:** Updated this round to reflect current content-completion state and revised open items.

---

## What's genuinely still missing from this repo

- **Novel-premise/contamination-check spec** -- still undefined (size and selection method)
- **A finalized, merged scoring prompt** -- this doc's draft still needs reconciling with Thulasi's
- **Intentionality-robustness and contamination/generalization arms** -- deliberately deferred until the 288-vignette core has been piloted
- **Pilot manipulation/severity check against the full 288** -- not yet run
- **Any actual model-response data** -- nothing here has been run through a model yet
