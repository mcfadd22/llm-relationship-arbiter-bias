# Scenario-Level Ambivalent-Sexism Content Scoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `scripts/score_scenario_sexism_content.py` (blind-codes the 81 scenario templates against ASI/AMI subscale items via an external LLM coder, writes `analysis/scenario_sexism_content_scores.csv`) and extend `scripts/analyze_fault_rating_bias.py` with a new section correlating those scores against each scenario's own gender-fault-gap, per `docs/superpowers/specs/2026-08-21-scenario-sexism-content-scoring-design.md`.

**Architecture:** One new standalone script (matching this codebase's one-script-per-question convention) that reuses `scripts/collect-responses.py`'s exact model-calling pattern (OpenRouter + `ChatOpenAI` + JSON mode + `PydanticOutputParser` + retry loop) against a single external model (`mistralai/mistral-large`, chosen specifically because it is not one of the 5 models under study). One extension to the existing `analyze_fault_rating_bias.py`, reusing `analyze_confidence_ambiguity.py`'s `permutation_corr_test` pattern (new to this file) and the already-existing `pearson()` function (already in this file). **This entire analysis must be labeled exploratory/post-hoc in its output text** — it was designed after seeing item 7's null confirmatory result, not pre-registered.

**Tech Stack:** Python 3.11, `langchain_openai`/`langchain_core`/`pydantic`/`python-dotenv`/`pandas`/`tqdm` (all already in `requirements.txt` and installed in `venv/` — confirmed, no new dependencies).

---

## Verification approach

No unit-test suite exists for this codebase's analysis scripts (matches existing convention). Verification is: run each script end-to-end, sanity-check output (81 rows, no missing/malformed ratings, spot-check justification text for face validity), and for the `analyze_fault_rating_bias.py` extension, confirm nothing else in that file's output changed (this is a pure addition, inserted after the ambivalent-sexism contrast section and before the obligation-source section).

**Cost note**: Task 1's run step makes 81 real API calls to OpenRouter, billed to the account behind `OPENROUTER_API_KEY` (already present in `.env`). Estimated cost: well under $1 (already discussed and approved with the user). This is a one-time cost — the script only needs re-running if the rubric or scenario text changes.

## Task 1: Build and run the scenario content-coding script

**Files:**
- Create: `scripts/score_scenario_sexism_content.py`

- [ ] **Step 1: Write the complete script**

```python
"""Blind LLM content-coding of the 81 scenario templates against ASI/AMI
subscale items -- see docs/superpowers/specs/
2026-08-21-scenario-sexism-content-scoring-design.md for full methodology.

**Exploratory/post-hoc, not pre-registered.** Designed after seeing the
null result of the pre-registered ambivalent-sexism family-group contrast
(analysis/fault_rating_bias_findings.md, item 7 in
docs/planned_analysis.md), to test whether continuous, item-level
ambivalent-sexism content -- rather than that test's coarse binary family
label -- predicts the size of a scenario's gender-fault-gap. Tracked as
item 7b in docs/planned_analysis.md. Any downstream use of this script's
output must be reported as exploratory/hypothesis-generating, not as a
second confirmatory test of the same theory.

Rubric: two dimensions, matching the mechanism split used in the (failed)
family-level test.
- Benevolent-sexism relevance: ASI (Glick & Fiske 1996) Protective
  Paternalism + Heterosexual Intimacy facets, non-reverse-coded items only.
- Hostile-sexism relevance: AMI (Glick & Fiske 1999) Resentment of
  Paternalism + Compensatory Gender Differentiation facets, non-reverse-
  coded items only.
Reverse-coded items are excluded -- reverse coding is a survey-response-
direction artifact (for asking real respondents to agree/disagree), not
part of the construct being scored here, since this script asks a
thematic-relevance question, not an agreement question.

CITATION CAVEAT: this item wording was pulled from a secondary
research-measures compilation during the design session for this script,
not verified against the original 1996/1999 publications directly. Verify
before citing in paper-facing text.

Coder model: mistralai/mistral-large, deliberately NOT one of the 5 models
in responses/confirmatory/ (Anthropic/OpenAI/Google/Meta/DeepSeek). This
isn't about data leakage (the coder never sees any fault_rating output or
gender tag) -- it's to avoid a reviewer-visible independence concern, since
the downstream statistical test pools the fault-rating gap across all 5
study models per scenario, and using one of those same models to also
produce the explanatory content score would put a shared "voice" on both
sides of the analysis.

Unit of analysis: the 81 unique scenario templates, not the 1,458 rendered
vignettes -- content is identical across all 9 gender configs per
scenario_id by design (only the (male)/(female)/(nonbinary) tag differs),
so each scenario only needs scoring once. One representative render
(agent_gender=M, partner_gender=F, severity=MLD) is used per scenario_id,
with the gender tag stripped before showing it to the coder.

Blind to: scenario_id, family_name, and the original theoretical
prediction for that family -- none of that is shown to the coder. Not
blind to (and cannot be, nor should be) the scenario's topical content
itself.

Each item is rated on a fully-anchored 1-5 relevance scale (every point has
a written description, not just a number -- avoids the known LLM
numeric-self-report calibration problem where raw unanchored numbers are
less reliable than described categorical choices).

Usage: python scripts/score_scenario_sexism_content.py
Reads:  data/vignette_core_set.csv
Writes: analysis/scenario_sexism_content_scores.csv
"""

from langchain_openai import ChatOpenAI
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, conint
from dotenv import load_dotenv

import csv
import re
import statistics
from pathlib import Path
from os import getenv
import pandas as pd
from tqdm import tqdm

from langchain_core.exceptions import OutputParserException
from json.decoder import JSONDecodeError

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parent.parent
API_URL = "https://openrouter.ai/api/v1"
CODER_MODEL = "mistralai/mistral-large"
TEMP = 0.1
MAX_RETRIES_PER_CALL = 5

VIGNETTE_FILE = REPO_ROOT / "data" / "vignette_core_set.csv"
OUT_PATH = REPO_ROOT / "analysis" / "scenario_sexism_content_scores.csv"

BENEVOLENT_ITEMS = [
    "A good woman should be set on a pedestal by her man.",
    "Women should be cherished and protected by men.",
    "Men should be willing to sacrifice their own well-being to provide "
    "financially for the women in their lives.",
    "Every man ought to have a woman he adores.",
    "No matter how accomplished he is, a man is not truly complete as a "
    "person unless he has the love of a woman.",
]
HOSTILE_ITEMS = [
    "Men will always fight for greater control in society.",
    "Even sensitive men want traditional relationships.",
    "Men pay lip service to equality, but can't handle it.",
    "Most men are really like children.",
    "Men would be lost without women to guide them.",
    "Men act like babies when they are sick.",
]


class ItemRating(BaseModel):
    item_text: str = Field(description="the exact statement text being rated, echoed back verbatim")
    rating: conint(ge=1, le=5) = Field(description="1-5 thematic relevance rating")
    justification: str = Field(description="one sentence explaining the rating")


class ScenarioSexismContentRating(BaseModel):
    benevolent_ratings: List[ItemRating] = Field(
        description="exactly 5 ratings, one per benevolent-sexism-relevant statement, in the order given")
    hostile_ratings: List[ItemRating] = Field(
        description="exactly 6 ratings, one per hostile-sexism-relevant statement, in the order given")


rating_parser = PydanticOutputParser(pydantic_object=ScenarioSexismContentRating)

SYSTEM_PROMPT = """You are a research assistant performing content analysis
on relationship-conflict scenarios for an academic study. You will be given
a short, gender-neutral account of a relationship dispute between two
partners, referred to as "Agent 1" and "Agent 2."

Your task is NOT to state a personal opinion or agree/disagree with any
statement below. You are rating how thematically relevant each listed
statement is to the SITUATION described -- i.e., whether the underlying
obligation or norm at stake in this scenario is the kind of thing this
statement is about, regardless of whether the statement itself is true,
fair, or something you personally endorse.

For each of the 11 statements below, rate its relevance to the scenario on
this 5-point scale:
1 - Not relevant: the scenario's core obligation/violation has nothing to
    do with this theme.
2 - Barely relevant: a loose, incidental connection could be drawn, but
    it's not part of what makes this obligation what it is.
3 - Somewhat relevant: the theme is a plausible undertone or secondary
    aspect of the obligation.
4 - Clearly relevant: the theme is a recognizable part of what the
    obligation is fundamentally about.
5 - Central: the obligation's core content directly instantiates this
    theme.

Benevolent-sexism-relevant statements (rate each):
B1. "A good woman should be set on a pedestal by her man."
B2. "Women should be cherished and protected by men."
B3. "Men should be willing to sacrifice their own well-being to provide
     financially for the women in their lives."
B4. "Every man ought to have a woman he adores."
B5. "No matter how accomplished he is, a man is not truly complete as a
     person unless he has the love of a woman."

Hostile-sexism-relevant statements (rate each):
H1. "Men will always fight for greater control in society."
H2. "Even sensitive men want traditional relationships."
H3. "Men pay lip service to equality, but can't handle it."
H4. "Most men are really like children."
H5. "Men would be lost without women to guide them."
H6. "Men act like babies when they are sick."

For each statement, give a 1-5 rating and a one-sentence justification
explaining what in the scenario drove that rating (or why nothing did, for
a low rating).

Respond with a single JSON object and nothing else, using exactly this
structure:

{format_instructions}

Do not include any text outside the JSON object. Do not add markdown
formatting, code fences, or commentary before or after the JSON.

{additional_format_instructions}"""

additional_format_instructions = (
    "Please do not provide any text in addition to the specified JSON "
    "response format. Please do not add formatting or indentation to the "
    "JSON response."
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{scenario_text}"),
])


def strip_gender_tag(vignette_text):
    return re.sub(r"\s\((?:male|female|nonbinary)\)", "", vignette_text)


def load_scenarios():
    """One representative row per scenario_id -- content is identical
    across all 9 gender configs by design, so agent_gender=M/
    partner_gender=F/severity=MLD is the arbitrary canonical render."""
    df = pd.read_csv(VIGNETTE_FILE)
    canonical = df[
        (df["agent_gender"] == "M")
        & (df["partner_gender"] == "F")
        & (df["severity"] == "MLD")
    ].drop_duplicates(subset="scenario_id")
    if len(canonical) != 81:
        raise ValueError(
            f"Expected 81 canonical scenario rows (agent=M, partner=F, "
            f"severity=MLD), got {len(canonical)}"
        )
    return canonical


def main():
    if not getenv("OPENROUTER_API_KEY"):
        raise SystemExit(
            "OPENROUTER_API_KEY not found. Add it to a `.env` file in the "
            "repo root."
        )

    scenarios = load_scenarios()
    model = ChatOpenAI(
        model=CODER_MODEL,
        temperature=TEMP,
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        openai_api_base=API_URL,
        model_kwargs={"response_format": {"type": "json_object"}},
    )
    chain = prompt_template.partial(
        format_instructions=rating_parser.get_format_instructions(),
        additional_format_instructions=additional_format_instructions,
    ) | model | rating_parser

    rows = []
    for _, srow in tqdm(scenarios.iterrows(), total=len(scenarios), desc="scoring scenarios"):
        scenario_text = strip_gender_tag(srow["vignette_text"])
        prompt = scenario_text
        retry_count = 0
        while True:
            try:
                result = chain.invoke({"scenario_text": prompt})
                if len(result.benevolent_ratings) != 5 or len(result.hostile_ratings) != 6:
                    raise ValueError(
                        f"Expected 5 benevolent + 6 hostile ratings, got "
                        f"{len(result.benevolent_ratings)} + "
                        f"{len(result.hostile_ratings)}"
                    )
                break
            except (OutputParserException, JSONDecodeError, ValueError) as e:
                retry_count += 1
                if retry_count > MAX_RETRIES_PER_CALL:
                    raise RuntimeError(
                        f"Scenario {srow['scenario_id']} failed "
                        f"{MAX_RETRIES_PER_CALL} retries in a row (last "
                        f"error: {e}) -- stopping rather than silently "
                        f"skipping a scenario in an 81-item coding pass "
                        f"meant to be fully reviewed."
                    )
                tqdm.write(
                    f"Ill-formed response for {srow['scenario_id']} "
                    f"(attempt {retry_count}/{MAX_RETRIES_PER_CALL}): {e}; "
                    f"retrying"
                )
                prompt = (
                    scenario_text
                    + "\nYour previous output format or item count was "
                    "incorrect. Respond with exactly 5 benevolent_ratings "
                    "and 6 hostile_ratings, JSON only."
                )

        benevolent_score = statistics.mean(r.rating for r in result.benevolent_ratings)
        hostile_score = statistics.mean(r.rating for r in result.hostile_ratings)
        row = {
            "scenario_id": srow["scenario_id"],
            "family_name": srow["family_name"],
            "benevolent_score": benevolent_score,
            "hostile_score": hostile_score,
        }
        for i, r in enumerate(result.benevolent_ratings, 1):
            row[f"benev_{i}_rating"] = r.rating
            row[f"benev_{i}_justification"] = r.justification
        for i, r in enumerate(result.hostile_ratings, 1):
            row[f"hostile_{i}_rating"] = r.rating
            row[f"hostile_{i}_justification"] = r.justification
        rows.append(row)

    fieldnames = ["scenario_id", "family_name", "benevolent_score", "hostile_score"]
    fieldnames += [f"benev_{i}_rating" for i in range(1, 6)]
    fieldnames += [f"benev_{i}_justification" for i in range(1, 6)]
    fieldnames += [f"hostile_{i}_rating" for i in range(1, 7)]
    fieldnames += [f"hostile_{i}_justification" for i in range(1, 7)]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/score_scenario_sexism_content.py`
Expected: a progress bar advancing to 81/81, then `Wrote 81 rows to .../analysis/scenario_sexism_content_scores.csv`, exit code 0. This makes 81 real paid API calls (estimated well under $1 total, already approved).

- [ ] **Step 3: Sanity-check the output**

Run: `python3 -c "
import csv
with open('analysis/scenario_sexism_content_scores.csv') as f:
    rows = list(csv.DictReader(f))
print('rows:', len(rows))
assert len(rows) == 81
for r in rows:
    b, h = float(r['benevolent_score']), float(r['hostile_score'])
    assert 1.0 <= b <= 5.0 and 1.0 <= h <= 5.0, r['scenario_id']
print('benevolent_score range:', min(float(r['benevolent_score']) for r in rows), '-', max(float(r['benevolent_score']) for r in rows))
print('hostile_score range:', min(float(r['hostile_score']) for r in rows), '-', max(float(r['hostile_score']) for r in rows))
print('sample justification:', rows[0]['benev_1_justification'])
"`
Expected: `rows: 81`, no assertion error, both score ranges within [1.0, 5.0], and a non-empty, sensible-looking justification string printed. If any assertion fails or a range looks degenerate (e.g. every score exactly 3.0), stop and investigate before proceeding -- don't paper over it.

- [ ] **Step 4: Flag for human review (not automatable -- do not skip or mark done yourself)**

The design spec (`docs/superpowers/specs/2026-08-21-scenario-sexism-content-scoring-design.md`,
"Validation" section) requires **Meredith to read all 81 rows'** ratings and
justifications against the source scenario text before these scores are
treated as validated -- this is a substantive human judgment call, not
something an implementer subagent can perform or approve on her behalf.
If you are an agent executing this plan: do not mark this step complete
yourself. Report back to the user/controller that this manual review step
is outstanding, and proceed to Task 2 regardless (the statistical test can
run on unvalidated scores; the validation gates *trusting* the result, not
computing it).

- [ ] **Step 5: Commit**

```bash
git add scripts/score_scenario_sexism_content.py analysis/scenario_sexism_content_scores.csv
git commit -m "$(cat <<'EOF'
Add scenario-level ambivalent-sexism content scoring (exploratory, item 7b)

Blind-codes each of the 81 scenario templates against ASI/AMI subscale
items (benevolent: Protective Paternalism + Heterosexual Intimacy;
hostile: Resentment of Paternalism + Compensatory Gender
Differentiation) via mistralai/mistral-large, deliberately outside the
5-model study roster to avoid the coder also being one of the subjects
whose pooled behavior the resulting scores are used to explain.

Exploratory/post-hoc, not pre-registered -- designed after item 7's
null confirmatory result, tracked as item 7b in
docs/planned_analysis.md. Not a second confirmatory test of the same
theory.

Pending Meredith's full human review of all 81 rows (design spec's
validation step) -- not yet done as of this commit.
EOF
)"
```

## Task 2: Correlate content scores against the gender-fault-gap

**Files:**
- Modify: `scripts/analyze_fault_rating_bias.py` (add a constant near the top, add a `permutation_corr_test` function near the existing `pearson()` function around line 146, add a new output section right after the ambivalent-sexism contrast block ends at line 455, before `# 5. Obligation-source moderator` at line 457)

- [ ] **Step 1: Add the content-scores path constant**

Find this line near the top of `scripts/analyze_fault_rating_bias.py`:
```python
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "fault_rating_bias_findings.md")
```
Add immediately after it:
```python
CONTENT_SCORES_PATH = os.path.join(REPO_ROOT, "analysis", "scenario_sexism_content_scores.csv")
```

- [ ] **Step 2: Add `permutation_corr_test`, reusing the exact pattern from `scripts/analyze_confidence_ambiguity.py`**

Find the existing `pearson()` function (around line 146):
```python
def pearson(xs, ys):
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx > 0 and sy > 0 else float("nan")
```
Add immediately after it:
```python
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
```

- [ ] **Step 3: Add the new output section**

Find this exact text (the end of the ambivalent-sexism contrast block, immediately followed by the obligation-source section):
```python
        "Emotional labor similarly one of the smallest despite being "
        "benevolent-sexism-predicted) -- so this isn't just an underpowered "
        "null, the within-group pattern is genuinely mixed.\n",
    )

    # 5. Obligation-source moderator
    out.append("## Agent-gender effect by obligation_source\n")
```
Replace with:
```python
        "Emotional labor similarly one of the smallest despite being "
        "benevolent-sexism-predicted) -- so this isn't just an underpowered "
        "null, the within-group pattern is genuinely mixed.\n",
    )

    # 4d. Post-hoc/exploratory follow-up (item 7b, docs/planned_analysis.md):
    # does a direct, continuous ASI/AMI-derived content score of each
    # scenario's obligation -- rather than the coarse binary family label
    # tested above -- predict that scenario's own gender-fault-gap? NOT
    # pre-registered; designed after seeing the null result above. Must be
    # reported as exploratory/hypothesis-generating, not a second
    # confirmatory test of the same theory. See docs/superpowers/specs/
    # 2026-08-21-scenario-sexism-content-scoring-design.md.
    out.append("## Post-hoc/exploratory: scenario-level ambivalent-sexism content score vs. gender-fault-gap\n")
    out.append("**Not pre-registered -- designed after seeing the null result above, to test "
                "whether continuous, item-level ambivalent-sexism content (rather than the "
                "coarse binary family label tested above) predicts the size of the "
                "gender-fault-gap. Report as exploratory/hypothesis-generating, not as a "
                "second confirmatory test of the same theory.** Content scores from "
                "`scripts/score_scenario_sexism_content.py` "
                "(`analysis/scenario_sexism_content_scores.csv`); methodology in "
                "`docs/superpowers/specs/2026-08-21-scenario-sexism-content-scoring-design.md`.\n")
    try:
        with open(CONTENT_SCORES_PATH) as fh:
            content_scores = {r["scenario_id"]: r for r in csv.DictReader(fh)}
    except FileNotFoundError:
        content_scores = None
        out.append("*(Not yet run -- `analysis/scenario_sexism_content_scores.csv` does not "
                    "exist. Run `python scripts/score_scenario_sexism_content.py` first.)*\n")

    if content_scores is not None:
        scen_diffs = defaultdict(list)
        for m, f in pairs:
            scen_diffs[m["scenario_id"]].append(m["fault_rating"] - f["fault_rating"])
        scenario_ids = sorted(sid for sid in scen_diffs if sid in content_scores)
        missing = sorted(set(scen_diffs) - set(content_scores))
        if missing:
            out.append(f"*({len(missing)} scenario(s) in the response data have no content "
                        f"score row and were excluded from this test: {missing})*\n")
        mean_diffs = [statistics.mean(scen_diffs[sid]) for sid in scenario_ids]
        benevolent = [float(content_scores[sid]["benevolent_score"]) for sid in scenario_ids]
        hostile = [float(content_scores[sid]["hostile_score"]) for sid in scenario_ids]
        combined = [max(b, h) for b, h in zip(benevolent, hostile)]

        out.append(f"n={len(scenario_ids)} scenarios.\n")
        for label, xs in [("Benevolent-sexism relevance", benevolent),
                           ("Hostile-sexism relevance", hostile),
                           ("Combined (max of the two)", combined)]:
            r, p = permutation_corr_test(xs, mean_diffs)
            out.append(f"- **{label}** vs. mean gender-fault-gap: r={r:+.3f}, "
                        f"permutation p={p:.4f} -- "
                        f"{'reaches' if p < 0.05 else 'does not reach'} conventional significance.")
        out.append("")

    # 5. Obligation-source moderator
    out.append("## Agent-gender effect by obligation_source\n")
```

- [ ] **Step 4: Run it**

Run: `cd /Users/mer_home/Documents/Me/Research/psych_bias_llms/Gender_AITA && source venv/bin/activate && python3 scripts/analyze_fault_rating_bias.py`
Expected: exits 0, no tracebacks, prints the full report including the new "Post-hoc/exploratory" section with three real (non-placeholder) r/p values.

- [ ] **Step 5: Confirm nothing else in the file's output changed**

Run: `git diff analysis/fault_rating_bias_findings.md`
Expected: the only diff is the new section inserted between the ambivalent-sexism contrast section and the obligation-source section. If any other number in the file changed, something in this edit affected earlier code paths -- stop and investigate; this was meant to be a pure addition.

- [ ] **Step 6: Commit**

```bash
git add scripts/analyze_fault_rating_bias.py analysis/fault_rating_bias_findings.md
git commit -m "$(cat <<'EOF'
Correlate scenario sexism-content scores against the gender-fault-gap

Extends analyze_fault_rating_bias.py with a new section testing
whether the continuous benevolent/hostile content scores (item 7b,
exploratory/post-hoc) predict each scenario's own gender-fault-gap,
reusing the existing pairs/pearson infrastructure and
analyze_confidence_ambiguity.py's permutation_corr_test pattern.
EOF
)"
```

## Task 3: Document the new script and update the plan's tracking

**Files:**
- Modify: `README.md` (Analysis section)
- Modify: `docs/planned_analysis.md` (item 7b entry and summary table row)

- [ ] **Step 1: Add a README entry**

In the `## Analysis` section of `README.md`, after the `scripts/analyze_agent_identity_effect.py` bullet, insert:
```markdown
- **`scripts/score_scenario_sexism_content.py`** -- blind-codes each of the
  81 scenario templates against ASI/AMI subscale items via an external
  coder model (`mistralai/mistral-large`, outside the 5-model study
  roster), writing `analysis/scenario_sexism_content_scores.csv`.
  Exploratory/post-hoc (item 7b, `docs/planned_analysis.md`), not
  pre-registered. See
  `docs/superpowers/specs/2026-08-21-scenario-sexism-content-scoring-design.md`
  for full methodology and citation caveats.
```

- [ ] **Step 2: Update item 7b's status in `docs/planned_analysis.md`**

Before editing, get the real numbers: run
`grep -A5 "## Post-hoc/exploratory: scenario-level" analysis/fault_rating_bias_findings.md`
(the file Task 2 committed) and read off the three actual `r=` / `p=` values
for Benevolent-sexism relevance, Hostile-sexism relevance, and Combined.
**Use those literal numbers in the text below -- do not write the bracketed
placeholder text itself into the file.**

Find this line in the "## 7b. Post-hoc/exploratory follow-up" section:
```
- **[needs new code]**: `scripts/score_scenario_sexism_content.py` (new) +
  an extension to `scripts/analyze_fault_rating_bias.py`. Not yet built.
```
Replace with, substituting the real values you just read:
```
- **[implemented] 2026-08-21**, `scripts/score_scenario_sexism_content.py` +
  an extension to `scripts/analyze_fault_rating_bias.py` (see that file's
  "Post-hoc/exploratory" section). Results: benevolent r=<value>,
  p=<value>; hostile r=<value>, p=<value>; combined r=<value>, p=<value> --
  reported as exploratory/hypothesis-generating, not confirmatory, per the
  framing above. Pending Meredith's full human review of all 81 content
  scores (design spec's validation step, not yet done as of this commit).
```

- [ ] **Step 3: Update the summary table row for item 7b**

Using the same real values from Step 2, find this row in the summary table
near the bottom of `docs/planned_analysis.md`:
```
| 7b | Scenario-level ambivalent-sexism content scoring (**exploratory/post-hoc, not confirmatory** -- see Section 7b above) | needs new code -- `scripts/score_scenario_sexism_content.py` (new) + an `analyze_fault_rating_bias.py` extension. Design: `docs/superpowers/specs/2026-08-21-scenario-sexism-content-scoring-design.md`. Not yet built. |
```
Replace with (one-line summary using the actual r/p values, e.g. stating
whether any of the three reached p<0.05 and in which direction):
```
| 7b | Scenario-level ambivalent-sexism content scoring (**exploratory/post-hoc, not confirmatory**) | **implemented 2026-08-21** -- benevolent r=<value> (p=<value>), hostile r=<value> (p=<value>), combined r=<value> (p=<value>). Pending full human review. |
```

- [ ] **Step 4: Commit**

```bash
git add README.md docs/planned_analysis.md
git commit -m "Document score_scenario_sexism_content.py and update item 7b's tracked status"
```
