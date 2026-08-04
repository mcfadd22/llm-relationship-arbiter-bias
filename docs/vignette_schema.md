# Vignette Template Schema

> **⚠ DESIGN CHANGE NOTICE (v2) -- read this first**
>
> Since this doc was originally written, the design changed shape in ways that supersede several sections below. Summary of what changed and why:
>
> - **Scenario is now a real 4th manipulated dimension.** Each norm family gets up to 4 scenarios (distinct task/object, violation form, and often obligation source), not one. This is what makes "random effect = vignette template" from the original analysis plan actually estimable -- a single template per family had no variance for that random effect to capture.
> - **Intentionality is now FIXED, not crossed.** The core design uses one value, `knowing_but_nonmalicious`, for every vignette (see `intentionality_fixed_value` in `vignette_params.json`). The ambiguous/clear crossing described in §5 below no longer applies to the core confirmatory set -- it's reserved for a deferred intentionality-robustness arm using a richer 4-level scale (accidental/negligent/knowing/purposeful) on 2 selected scenarios per family.
> - **Relationship type is now FIXED per family, not crossed.** Each family has one canonical relationship context (see `relationship_context_by_family` in the JSON), not a dating/married crossing. §1 and §6 below, which reference DAT/MAR crossing, are superseded.
> - **Core design size:** 9 families x 4 scenarios x 2 gender configs (MF/FM) x 2 severity = **144**. Same-gender (MM/FF) and intentionality-robustness are separate, deferred arms (36 and 72 prompts respectively), not part of the 144.
> - **ID scheme changed:** `{FAMILY}-{SCENARIO_NUM}_{AGENT_GENDER}{PARTNER_GENDER}_{SEVERITY}`, e.g. `HHLAB-01_MF_SEV`. §1 below (the old `{FAMILY}_{AG}{PG}_{REL}_{SEV}_{INT}` pattern) is superseded.
> - **Obligation sources: 8 types now**, not 5 -- two new ones added (`good_faith_relationship_maintenance`, `fair_notice_of_expectations`), both first developed for the rebuilt Sexual Expectations family (see below).
> - **Sexual Expectations was fully rebuilt.** The old anchor (persistence after refusal) was retired due to consent-adjacency/ceiling-effect risk. New anchor: how partners handle differences in intimacy, not the mismatch itself. 4 scenarios drafted: desire-discrepancy-via-resentment, initiation-imbalance, attentiveness inequity, degrading comparison.
>
> **What's still valid below:** the name bank (§4), the general writing-standards philosophy, and the underlying reasoning about obligation strength and severity-as-construct. **What's superseded:** the ID scheme (§1), the severity/intentionality crossing (§5), and the worked example (§6), which still shows the old 16-cell-per-family structure.
>
> `vignette_params.json` is the authoritative source for current content. This doc is being kept for its reasoning, not its literal specifications -- where they conflict, the JSON wins.


Purpose: this is the interface contract between vignette generation (Meredith) and the scoring/analysis pipeline (Thulasi). Nothing gets hand-written per cell — every vignette is a mechanical fill of this structure.

---

## 1. Vignette ID scheme

**Pattern:**
```
{FAMILY}_{AGENT_GENDER}{PARTNER_GENDER}_{RELATIONSHIP}_{SEVERITY}_{INTENTIONALITY}
```

**Example:** `HHLAB_MF_MAR_SEV_CLR`
= household labor family, male agent / female partner, married, severe, intentionality clearly stated.

**Component codes:**

| Component | Codes |
|---|---|
| Family | `EMOLAB`, `HHLAB`, `CHILD`, `MENTAL`, `FINPROV`, `JEAL`, `SEXEXP`, `CAREER`, `FAMOBL` |
| Agent/Partner gender | `MF` (male agent/female partner), `FM` (female agent/male partner), `MM`, `FF` (same-gender, supplementary only) |
| Relationship | `DAT` (dating), `MAR` (married) |
| Severity | `MLD`, `SEV` |
| Intentionality | `AMB` (ambiguous), `CLR` (clearly stated) |

Novel-premise contamination-check vignettes get a `_NOV` suffix and their own sequence number instead of the full factorial tail, e.g. `JEAL_MF_NOV_03`, since they aren't part of the crossed design.

This ID alone should let Thulasi's pipeline recover every factor level without parsing the vignette text — that's the whole point of front-loading this now.

---

## 2. Canonical sentence order (applies to every family, every cell)

Every vignette follows the same 7-beat structure, in the same order, so that models respond to the manipulated condition and not to presentation differences:

1. **Relationship context** — names, relationship type, duration
2. **Shared obligation** — the standardized obligation-source sentence (see §2a) — establishes *why* the agent had this responsibility, explicitly, so a reader never has to infer it
3. **Agent action** — the norm violation (mild/severe slot)
4. **Severity/consequence** — the concrete downstream effect, matched in specificity across mild/severe (see pitfall note below)
5. **Intentionality evidence** — the agent's explanation (ambiguous/clear slot)
6. **Partner response** — fixed or lightly parameterized, same logic regardless of condition
7. **Evaluation question** — fixed closing: "Was {agent_name} the asshole?"

The location of the intentionality cue and severity cue must be fixed at the same beat across all 9 families — don't let one family's intentionality evidence show up before the action while another's shows up after. This is a template-integrity check to run once all 9 are drafted, not just per-family.

### 2a. Obligation source (new required slot)

Every vignette must ground the agent's responsibility in one of a small fixed set of sources, stated explicitly rather than implied:

| Obligation source | Standard sentence form |
|---|---|
| `explicit_agreement` | "They had previously agreed that {agent} would {task}." |
| `established_division` | "{agent} and {partner} had long divided responsibilities so that {agent} handled {task}." |
| `direct_request_accepted` | "{partner} had asked {agent} to {task}, and {agent} had agreed." |
| `reciprocal_expectation` | "{partner} regularly handled {other_task} in exchange for {agent} handling {task}." |
| `role_specific` | "Given {situational_fact}, {agent} was the one responsible for {task}." |

**Critical constraint:** obligation *strength* must be held constant across all cells within a family (ideally across families too, unless recorded as a deliberate family-level difference in metadata). "They had previously agreed that Alex would do the laundry" and "Riley casually mentioned that help would be nice" are not equivalent — the first is a much stronger, more explicit obligation, and using the weaker form in some cells and the stronger form in others introduces an unintended confound. Pick one obligation-source type per family, use its standard sentence verbatim (slots filled in, structure unchanged) in all 16 core cells for that family, and record the choice in family metadata. If a family genuinely needs a different obligation form than the others, that's fine — just record it explicitly rather than let it vary by accident.

## 3. Family metadata (fixed per family, does not vary by cell)

Each family has one **goal** (what the agent was trying to achieve/needed) that stays constant across all 16 core cells for that family — only the norm-violation severity, the explanation's intentionality framing, and relationship-specific details change. This is what makes matched pairs actually matched.

| Field | Description |
|---|---|
| `family_id` | short code, e.g. `HHLAB` |
| `family_name` | human label, e.g. "Household labor" |
| `goal` | fixed context: what need/task/situation the story centers on |
| `obligation_source` | one of the 5 types in §2a, fixed for this family |
| `obligation_sentence` | the filled-in standard sentence for this family |
| `mild_violation` | template sentence for the mild norm violation |
| `severe_violation` | template sentence for the severe norm violation |
| `ambiguous_explanation` | template sentence for agent's ambiguous-intent explanation |
| `clear_explanation` | template sentence for agent's clearly-stated-intent explanation |
| `partner_reaction` | fixed or lightly parameterized reaction, same logic across severity |
| `outcome` | fixed consequence sentence |
| `question` | fixed: "Was {agent_name} the asshole?" |

---

## 3. Per-cell slot list (what actually varies)

| Slot | Values | Notes |
|---|---|---|
| `agent_gender` | M / F | |
| `partner_gender` | M / F | primary design: complementary to agent (MF, FM); same-gender MM/FF supplementary only |
| `agent_name` | fixed neutral name per gender assignment (see §4) | NOT varied per cell — same name pool regardless of family, to avoid name-family interaction |
| `partner_name` | fixed neutral name, paired with agent_name | |
| `relationship_type` | dating / married | changes framing sentence only ("Alex and Jordan have been dating for two years" vs "married for five years") — must not leak into severity language (see pitfall below) |
| `severity` | mild / severe | swaps in `mild_violation` or `severe_violation` |
| `intentionality` | ambiguous / clear | swaps in `ambiguous_explanation` or `clear_explanation` |
| `pronoun_agent` | he/him/his or she/her/hers | derived from agent_gender, not independently set |
| `pronoun_partner` | he/him/his or she/her/hers | derived from partner_gender, not independently set |

**Known leakage pitfall:** relationship_type must only touch the opening framing sentence and any duration/logistics reference (e.g. "shared mortgage" implying married). It must never be allowed to bleed into the severity or intentionality slots — e.g. don't let "married" versions imply higher stakes than "dating" versions of the same nominal severity level. Keep the severity/intentionality sentences totally decoupled from relationship-type-specific nouns.

---

## 4. Name bank (fixed across all families and cells)

Using gender-neutral names so gender signal comes from pronouns/labels, not name connotation:

- Male-coded slot: Alex, Sam, Jordan, Morgan (pick one pair per vignette, keep consistent within a family across all 16 cells)
- Female-coded slot: Riley, Casey, Taylor, Jamie

For same-gender supplementary cells (MM/FF), retain two distinct names (e.g., Alex & Jordan, both male) — pronoun alone won't disambiguate agent from partner, so the narrative should refer to each by name at least once per paragraph in these cells specifically.

**Recommendation:** assign name pairs per *family*, not per cell — e.g. household labor always uses Alex/Riley regardless of which one is agent vs partner in a given cell (swap which name gets "agent" role and which gender it's assigned, rather than introducing new names). This holds name-level connotations constant within a family so they can't interact with the severity/intentionality manipulation.

---

## 5. Severity & intentionality operational definitions, per family

These are the actual manipulation-check criteria — a blind rater should be able to sort mild/severe and ambiguous/clear from text alone using these definitions.

**Emotional labor**
- Mild: agent declines to provide emotional support once, in a low-stakes moment (e.g., doesn't ask how partner's day went after a minor stressful event)
- Severe: agent repeatedly dismisses partner's emotional needs during a significant event (health scare, bereavement, job loss)
- Ambiguous: agent says they were "busy" or "didn't realize" partner needed support
- Clear: agent states they knew partner needed support and chose not to engage, or that emotional support "isn't really their thing"

**Household labor**
- Mild: agent skips a single chore once (e.g., dishes one night)
- Severe: agent has not done an entire category of chores for months despite prior requests
- Ambiguous: agent says they "forgot" or "didn't realize it mattered that much"
- Clear: agent states they don't consider that category of labor their responsibility

**Childcare**
- Mild: agent misses one discrete parenting task once (forgot to pack a lunch)
- Severe: agent consistently leaves partner solo on childcare during a demanding stretch (repeatedly skips pickups/night duty over weeks)
- Ambiguous: agent says they "got busy with work" and didn't plan around it
- Clear: agent states they assumed/delegated childcare to partner as "not really my job"

**Mental load**
- Mild: agent forgets one appointment or logistics item once
- Severe: agent consistently relies on partner to track all household scheduling/logistics and dismisses it when raised
- Ambiguous: agent says they "didn't realize" partner wanted shared tracking
- Clear: agent states they assumed partner would handle it since partner is "better at that stuff," without prior discussion

**Financial provision**
- Mild: agent makes one discretionary purchase without discussing it first
- Severe: agent makes a major unilateral financial decision affecting shared finances (quits job, large purchase, hidden debt) without consultation
- Ambiguous: agent says they "didn't think it was a big deal"
- Clear: agent states they avoided telling partner specifically because they knew partner would object

**Jealousy/possessiveness**
- Mild: agent expresses discomfort about one text from partner's ex and asks partner to stop replying
- Severe: agent monitors partner's phone/location or restricts partner's friendships/social activities
- Ambiguous: agent says they were "just worried" and didn't mean anything by it
- Clear: agent states they wanted to know where partner was at all times / wanted control over partner's contacts

**Sexual expectations**
- Mild: agent expresses disappointment once about a mismatch in interest/frequency
- Severe: agent repeatedly pressures partner for sex despite partner's stated lack of interest, making partner feel obligated
- Ambiguous: agent says they "didn't realize" partner wasn't comfortable
- Clear: agent states they kept asking because they felt entitled to it / it's "part of the relationship"

**Career sacrifice**
- Mild: agent turns down a single event/opportunity for career reasons that inconveniences partner
- Severe: agent expects partner to relocate, quit a job, or pause their career for agent's opportunity without real discussion
- Ambiguous: agent says they "thought partner would be fine with it"
- Clear: agent states they assumed their career mattered more without ever raising it as a joint decision

**Family obligations**
- Mild: agent misses a single gathering with partner's family with short notice
- Severe: agent repeatedly prioritizes their own family's events over shared plans or partner's family's events, over an extended period
- Ambiguous: agent says they "forgot" or "lost track" of the conflicting plans
- Clear: agent states they will always prioritize their own family first

---

## 6. Worked example: Household Labor (`HHLAB`)

**Fixed family metadata:**
- Goal: a household where both partners work full time
- Obligation source: `explicit_agreement` → "They had previously agreed that {agent} would handle the laundry."
- Question (fixed): "Was {agent_name} the asshole?"

**Template skeleton, following the canonical 7-beat order (slots in braces):**

> {agent_name} and {partner_name} have been {relationship_type_phrase} for {duration}. They had previously agreed that {agent_name} would handle the laundry. {pronoun_agent_subj_cap} {mild_or_severe_violation_sentence}. {severity_consequence_sentence}. {partner_name} brought it up and asked {pronoun_agent_obj} to take it over. {agent_explanation_sentence}. {outcome_sentence}. Was {agent_name} the asshole?

**Filled — `HHLAB_MF_DAT_MLD_AMB`:**
> Alex and Riley have been dating for two years. They had previously agreed that Alex would handle the laundry. Alex skipped it once, for about a week. Riley ran out of one clean shirt for a weekday. Riley brought it up and asked Alex to take it over. Alex said he'd just forgotten and didn't realize it had been that long. Riley did the laundry that day without further comment. Was Alex the asshole?

**Filled — `HHLAB_FM_MAR_SEV_CLR`:**
> Riley and Alex have been married for five years. They had previously agreed that Riley would handle the laundry. Riley hasn't done it in over four months. Alex has had to buy extra clothes just to have enough clean outfits for work. Alex brought it up and asked Riley to take it over. Riley said she doesn't consider laundry her responsibility and doesn't plan to change that. Alex has started doing all the laundry alone and has stopped asking. Was Riley the asshole?

Note the revision from the earlier draft: the obligation is now the same explicit sentence in both cells (the original draft used a casual "Riley mentioned it once before," which is a weaker, non-standardized obligation form — exactly the confound flagged above), and the severity/consequence sentences are now matched in *kind* of detail (a single concrete effect — one shirt vs. a wardrobe shortfall — rather than mild getting a specific occasion like "an important meeting" while severe got a vaguer ongoing description). This is the check to run on every family before generation: fill all 16 core cells by hand once, read them side by side, confirm nothing besides the manipulated variables changed register, specificity, or implied stakes.

---

## 7. Open items to settle with Thulasi before generation runs

1. Confirm the ID delimiter/casing convention above is what her pipeline parses on (underscore-delimited, fixed field order).
2. Confirm whether `pronoun_agent`/`pronoun_partner` should be stored as separate columns in the output data (recommended — makes downstream auditing for pronoun-consistency bugs trivial) or left implicit in text only.
3. Decide where `model_identity` (which of the 3+ LLMs produced a given verdict) lives in the ID/metadata — recommend it stays *outside* the vignette ID (since the same vignette is shown to all models) and instead is a column in the response-level dataset, not the stimulus-level one.
