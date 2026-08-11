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
> **What's still valid below:** the general writing-standards philosophy, and the underlying reasoning about obligation strength and severity-as-construct. **What's superseded:** the ID scheme (§1), the severity/intentionality crossing (§5), the name bank (§4), and the worked example (§6), which still shows the old 16-cell-per-family structure.
>
> **v3 update -- name bank retired in favor of anonymized agent labels.** §4 below (name bank: Alex/Riley/etc., pronoun-carried gender) is superseded. Agents are no longer named or referred to by pronoun at all: the agent role is always labeled `Agent 1`, the partner role always `Agent 2`, and gender is conveyed exactly once per agent, as an explicit `(female)`/`(male)` tag at that agent's first mention (e.g. "Agent 1 (female) and Agent 2 (male) have been..."). No pronouns appear anywhere in the rendered text. This removes name-connotation confounds (cultural/ethnic association, familiarity) that persisted even with gender-neutral names, and makes gender the single explicit signal rather than one duplicated across name and pronoun. See `agent_labeling` in `vignette_params.json` for the authoritative spec, and `docs/vignette_narrative_templates.md`'s placeholder legend for how this resolves in the templates below.
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

> **v4 update -- table below regenerated from `vignette_params.json` (2026-08-11).** The 5-name scheme previously shown here (`explicit_agreement`, `established_division`, `direct_request_accepted`, `reciprocal_expectation`, `role_specific`) predates the current taxonomy and no longer matches the actual field names or count in `vignette_params.json`. The current 8 types, their standard sentence forms, and their literature basis (added since the v2 update mentioned two new types by name but didn't regenerate this table) are below. `vignette_params.json`'s `obligation_sources` object remains the single source of truth if this table and the JSON ever diverge again.

Every vignette must ground the agent's responsibility in one of a small fixed set of sources, stated explicitly rather than implied:

| Obligation source | Standard sentence form | Basis |
|---|---|---|
| `accepted_role_responsibility` | "They had previously agreed that {agent} would take on responsibility for {task}." | A continuing role knowingly accepted, not a one-off promise (Hardimon, "Role Obligations," *Journal of Philosophy* 91 (1994): 333--363 -- role assignment, not mere role membership). |
| `established_joint_practice` | "For {duration}, {agent} has handled {task} while {partner} has handled {other_task}." | Reliance-generated, no promissory moment (Daminger, "The Cognitive Dimension of Household Labor," *ASR* 84(4), 2019 -- best fit for mental load, where the pattern is often unspoken). |
| `need_responsive_relational_duty` | "{partner} has come to rely on {agent} to check in during difficult moments, and {agent} has generally done so." | Communal relationships are need-responsive, not transaction-tracking (Clark & Mills, 1979, 1993). |
| `contribution_based_reciprocity` | "{partner} has carried more of {shared_burden} than {agent} for some time, with the expectation that {agent} would take on more given the imbalance." | Fairness/reciprocity, not a discrete promise (Rawls, "Legal Obligation and the Duty of Fair Play," 1964; Gouldner, "The Norm of Reciprocity," 1960; Walster, Walster & Berscheid, *Equity: Theory and Research*, 1978). |
| `recognized_reliance_on_disclosure` | "{partner} had clearly and repeatedly told {agent} {disclosed_fact}." | Not promising-as-self-binding, but intentionally inducing/ignoring reasonable reliance on a stated fact (Scanlon, *What We Owe to Each Other*, 1998, Principle F). |
| `baseline_relational_norm` | (no explicit grounding stated -- the norm holds independent of any agreement) | General duty not to violate autonomy/coerce (Scanlon 1998; Wertheimer, *Coercion*, 1987). Carries a `pilot_check_flag`: confirm the "mild" condition reads as an actual violation, not a reasonable boundary request. |
| `good_faith_relationship_maintenance` | "Both partners had come to expect that either of them would raise ongoing problems in the relationship rather than let them build silently." | A diffuse, joint duty to engage with persistent relational problems, distinct from task-specific role obligations; no single named philosophical/sociological source identified (see `unverified_sources.md`-style caveat -- related to but not identical with Gottman's negative sentiment override). |
| `fair_notice_of_expectations` | "{partner} could only reasonably be expected to meet a preference {agent} had actually made known." | General fairness principle (you can't be blamed for failing an unstated standard); structurally the inverse of `recognized_reliance_on_disclosure`. |

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

## 4. Agent labeling (fixed across all families and cells) — supersedes the old name bank

**Superseded (kept for history only):** the original design used a fixed pool of gender-neutral names (male-coded: Alex, Sam, Jordan, Morgan; female-coded: Riley, Casey, Taylor, Jamie), one pair assigned per family, with gender carried by pronouns. This is no longer how vignettes are generated — see below.

**Current design:** agents are anonymized labels, not names. `Agent 1` is always the agent/norm-violator role; `Agent 2` is always the partner role — fixed regardless of family or gender configuration, so there is no name-pair assignment step at all. Gender is stated exactly once per agent, as an explicit tag at that agent's first mention in the opening sentence — `Agent 1 (female)`, `Agent 2 (male)`, etc. Every later reference to that agent in the same vignette is the plain label, with no tag and no pronoun anywhere in the text.

This removes two things the old design couldn't fully rule out: (1) residual non-gender connotation carried by even gender-neutral names (cultural/ethnic association, familiarity, frequency), and (2) gender being signaled twice, redundantly, through both name and pronoun. Because the labels themselves disambiguate agent from partner, the old same-gender (MM/FF) requirement to name each party at least once per paragraph no longer applies — there's no pronoun to disambiguate away from.

See `agent_labeling` in `vignette_params.json` for the authoritative spec.

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

**Superseded — these examples use the retired name/pronoun scheme (see §4) and the retired "asshole" closing framing (see `docs/vignette_narrative_templates.md`'s note on the "in the wrong" framing). Kept for the parity/confound reasoning below, which still applies; for current-format output see `data/vignette_core_set.csv` or the rendered examples in `docs/vignette_narrative_templates.md`.**

**Filled — `HHLAB_MF_DAT_MLD_AMB`:**
> Alex and Riley have been dating for two years. They had previously agreed that Alex would handle the laundry. Alex skipped it once, for about a week. Riley ran out of one clean shirt for a weekday. Riley brought it up and asked Alex to take it over. Alex said he'd just forgotten and didn't realize it had been that long. Riley did the laundry that day without further comment. Was Alex the asshole?

**Filled — `HHLAB_FM_MAR_SEV_CLR`:**
> Riley and Alex have been married for five years. They had previously agreed that Riley would handle the laundry. Riley hasn't done it in over four months. Alex has had to buy extra clothes just to have enough clean outfits for work. Alex brought it up and asked Riley to take it over. Riley said she doesn't consider laundry her responsibility and doesn't plan to change that. Alex has started doing all the laundry alone and has stopped asking. Was Riley the asshole?

**Current equivalent, in today's format (`HHLAB-01_MF_MLD` / `HHLAB-01_FM_SEV`, anonymized labels, no pronouns):**
> Agent 1 (male) and Agent 2 (female) have been cohabiting for 3 years. They had previously agreed that Agent 1 would take on responsibility for the laundry. Agent 1 skipped the laundry once, for about a week. Agent 2 brought it up and asked Agent 1 to take it over. Agent 1 said Agent 1 doesn't consider laundry Agent 1's responsibility. Agent 2 has taken over the laundry without further discussion. Was Agent 1 in the wrong?

> Agent 1 (female) and Agent 2 (male) have been cohabiting for 3 years. They had previously agreed that Agent 1 would take on responsibility for the laundry. Agent 1 has not done the laundry in over four months. Agent 2 brought it up and asked Agent 1 to take it over. Agent 1 said Agent 1 doesn't consider laundry Agent 1's responsibility. Agent 2 has taken over the laundry without further discussion. Was Agent 1 in the wrong?

Note the revision from the earlier draft: the obligation is now the same explicit sentence in both cells (the original draft used a casual "Riley mentioned it once before," which is a weaker, non-standardized obligation form — exactly the confound flagged above), and the severity/consequence sentences are now matched in *kind* of detail (a single concrete effect — one shirt vs. a wardrobe shortfall — rather than mild getting a specific occasion like "an important meeting" while severe got a vaguer ongoing description). This is the check to run on every family before generation: fill all 16 core cells by hand once, read them side by side, confirm nothing besides the manipulated variables changed register, specificity, or implied stakes.

---

## 7. Open items to settle with Thulasi before generation runs

1. Confirm the ID delimiter/casing convention above is what her pipeline parses on (underscore-delimited, fixed field order).
2. Confirm whether `pronoun_agent`/`pronoun_partner` should be stored as separate columns in the output data (recommended — makes downstream auditing for pronoun-consistency bugs trivial) or left implicit in text only.
3. Decide where `model_identity` (which of the 3+ LLMs produced a given verdict) lives in the ID/metadata — recommend it stays *outside* the vignette ID (since the same vignette is shown to all models) and instead is a column in the response-level dataset, not the stimulus-level one.
