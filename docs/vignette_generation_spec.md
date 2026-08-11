# Vignette Generation Spec (for LLM-assisted scenario drafting)

**How to use this document:** this is a self-contained brief. Paste it (or point an
LLM at this file) along with a concrete request -- e.g. "draft 3 new scenarios for
the Career Sacrifice family, obligation sources X/Y/Z" or "write the
accidental/negligent/purposeful intentionality variants for CHILD-01 and JEAL-02"
-- and the output should already comply with everything below, ready for the
review gate at the end. This distills `vignette_schema.md`, `vignette_writing_standards.md`,
`vignette_params.json`'s own `basis` fields, and the lessons captured in item G
(added 2026-08-11 after a manual review pass and a follow-up audit) into one place.
Where those source docs disagree with this one, treat this doc as the current
synthesis but `vignette_params.json` remains the actual data -- update this spec if
the design changes again rather than letting it drift stale.

---

## 1. Output format

Each scenario is one object added to its family's `scenarios` array in
`data/vignette_params.json`:

```json
{
  "scenario_id": "FAMILY-NN",
  "status": "drafted",
  "task_object": "short phrase naming the concrete task/object in conflict",
  "violation_form": "short phrase naming the kind of violation",
  "obligation_source": "one of the 8 types in Section 3",
  "obligation_sentence": "template sentence, see Section 3 -- or \"\" if baseline_relational_norm",
  "mild_violation": "template sentence, see Section 4",
  "severe_violation": "template sentence, see Section 4",
  "knowing_nonmalicious_explanation": "template sentence, see Sections 4 and 5",
  "partner_response": "template sentence",
  "outcome": "template sentence"
}
```

`scenario_id` follows `{FAMILY}-{NN}` (zero-padded two digits, next available number
for that family). Every string field uses the placeholder slots in Section 2 --
never a literal name, and never a literal pronoun.

## 2. Placeholder slots

Only these placeholders are ever used inside template strings; the generator
(`scripts/generate_vignettes.py`) resolves all of them to the literal labels
`Agent 1` / `Agent 2` (or `Agent 1's` / `Agent 2's` for the `_poss` slots) --
there are no real pronouns anywhere in the rendered output, by design:

| Placeholder | Resolves to |
|---|---|
| `{agent}`, `{agent_subj}`, `{agent_subj_cap}`, `{agent_obj}` | `Agent 1` |
| `{agent_poss}` | `Agent 1's` |
| `{partner}` | `Agent 2` |
| `{pronoun_partner_subj}`, `{pronoun_partner_obj}` | `Agent 2` |
| `{pronoun_partner_poss}` | `Agent 2's` |

These names are legacy (`pronoun_partner_*` predates the anonymization change) but
the resolution is fixed: never write an actual pronoun (he/she/him/her/his/hers) or
an actual name anywhere in a template string. Gender is conveyed exactly once, by
the generator itself at first mention (`Agent 1 (female) and Agent 2 (male) have
been...`), never by the template.

## 3. Canonical render order (7 beats) -- and why it matters here

`generate_vignettes.py` concatenates fields in exactly this order:

1. **Opening** (fixed, not authored): `Agent 1 (gender) and Agent 2 (gender) have
   been {relationship_type} for {duration}.` (+ a child clause if applicable)
2. **`obligation_sentence`** (skipped entirely if empty string)
3. **`mild_violation` OR `severe_violation`** (whichever severity is being rendered)
4. **`partner_response`**
5. **`knowing_nonmalicious_explanation`**
6. **`outcome`**
7. **Question** (fixed, not authored): `Was Agent 1 in the wrong?`

This order is why the antecedent rule in Section 6 checks fields in this specific
sequence, and why `obligation_sentence` and the shared explanation/response fields
(rendered into *both* severity cells) can silently pre-empt whatever the violation
sentence claims -- see Section 5.

## 4. The 8 obligation sources -- literature basis and, critically, what each one
   implies about severity

| Type | Standard form | Basis | Implies an existing deficit? |
|---|---|---|---|
| `accepted_role_responsibility` | "They had previously agreed that {agent} would take on responsibility for {task}." | Hardimon, "Role Obligations," *J. Phil.* 91 (1994) -- role *assignment*, not mere membership | No -- a clean, working assignment |
| `established_joint_practice` | "For {duration}, {agent} has handled {task} while {partner} has handled {other_task}." | Daminger (2019) on mental load as unspoken/unassigned pattern | No -- a working arrangement |
| `need_responsive_relational_duty` | "{partner} has come to rely on {agent} to {task}, and {agent} has generally done so." | Clark & Mills (1979, 1993) on communal vs. exchange relationships | No -- "generally done so" states agent has a good track record |
| `contribution_based_reciprocity` | "{partner} has carried more of {burden} than {agent} for some time, with the expectation that {agent} would take on more given the imbalance." | Rawls (1964) on fair play; Gouldner (1960) on reciprocity; Walster, Walster & Berscheid (1978) on equity theory | **Yes** -- asserts an existing imbalance. See Section 5's rule for this type specifically. |
| `recognized_reliance_on_disclosure` | "{partner} had clearly and repeatedly told {agent} {disclosed_fact}." | Scanlon (1998), Principle F -- not promising-as-self-binding, but disregarding induced/disclosed reliance | No, but see Section 6 -- this type's sentence must actually name the disclosed fact/referent, not gesture at "this X" |
| `baseline_relational_norm` | `""` (no sentence at all -- the norm holds independent of any agreement) | Scanlon (1998); Wertheimer, *Coercion* (1987) | N/A -- but see Section 6, this is the highest-risk type for antecedent bugs since there's no sentence to introduce anything |
| `good_faith_relationship_maintenance` | "Both partners had come to expect that either of them would raise ongoing problems in the relationship rather than let them build silently." | No single named source -- a diffuse joint duty, loosely related to Gottman's "negative sentiment override" but that's not a moral-obligation theory. Document as such; don't force a citation onto it. | No |
| `fair_notice_of_expectations` | "{partner} could only reasonably be expected to meet a preference {agent} had actually made known." | General fairness principle; structurally the inverse of `recognized_reliance_on_disclosure` | No |

**Do not invent a 9th type without updating this table and `vignette_params.json`'s
own inline `basis` fields together.**

## 5. Severity construction: the rule that generated the most bugs on the last pass

`mild_violation` and `severe_violation` are alternatives -- only one renders per
vignette. But `obligation_sentence`, `partner_response`, and
`knowing_nonmalicious_explanation` are each a **single field rendered into both**
severity cells. This is where nearly every bug in the 2026-08-11 review came from.

**Rule 5a -- verb-aspect concordance.** Any clause describing what *the agent did*
(not the partner's situation, not a background fact) must use bounded/single-event
aspect in `knowing_nonmalicious_explanation` and `partner_response`: simple past
("chose to," "decided to," "didn't," "had fallen short"), never progressive/durative
aspect ("has been X-ing," "was X-ing," "hasn't been X-ing") or explicit
frequency/duration words ("lately," "generally," "hasn't seen a reason to change,"
"one more," "here or there"). Bounded aspect reads naturally at either severity;
durative aspect reads fine for severe but silently contradicts a mild cell's "did
X once" framing.
- Bad: *"...but hasn't felt like cooking lately."* (durative -- implies an ongoing mood, contradicts "skipped it once")
- Good: *"...but didn't feel like cooking."* (bounded -- works whether this happened once or as part of a longer pattern)
- Exception: clauses about the *partner's* state or a background fact are unaffected -- *"knew {partner} was counting on {agent}"* is fine regardless of severity, since it's not describing the agent's violation frequency.

**Rule 5b -- chronicity in the obligation sentence, checked by content, not by type
name.** If the rendered `obligation_sentence` itself asserts an existing deficit
("more...than {agent}...for some time," "given the imbalance" -- currently
`contribution_based_reciprocity`'s standard form, but check the actual sentence, not
the label), then `mild_violation` must **not** claim total isolation. Add an
explicit recurrence-acknowledgment marker ("again," "another") while keeping the
*stakes* clearly lower than severe:
- Bad: *"{agent} didn't reach out after one disagreement..."* (obligation sentence already says "for some time... given the imbalance" -- "one disagreement" falsely implies this is the first lapse)
- Good: *"{agent} again didn't reach out after a recent disagreement..."*
- This does **not** apply to `established_joint_practice`, whose standard form
  asserts a *working* arrangement, not a deficit -- a genuinely isolated mild lapse
  is fully coherent there and needs no recurrence marker.
- Watch for the idiom trap: "once again" literally contains the word "once" and
  reads as isolation-flavored on a naive check -- prefer plain "again"/"another"
  over "once again" for exactly this reason.

**Rule 5c -- what severity is actually a proxy for.** Per `vignette_params.json`'s
`severity_construct`: severity represents magnitude of harm/burden to the partner
and relationship, and the *observable feature* that carries it is allowed to vary
by family (accumulation via repetition, stakes of a single act, breadth of a
restriction). Mild and severe should differ in *what happened* and *how much harm
resulted*, not in how much surrounding detail, narrator tone, or moral coloring is
given -- see the writing-standards item A checklist in Section 7.

## 6. Demonstrative-antecedent rule

Any "this X" / "these X" (or a bare "these") needs its noun to have actually been
introduced earlier in the *specific render path* being written (Section 3's order,
for the severity being checked) -- with two exceptions:
- **Generic discourse-summary nouns** are always fine without a literal earlier
  mention, since they refer to "the situation just described" as a whole, not a
  specific noun phrase: `pattern`, `decision`, `situation`, `dynamic`, `way`,
  `responsibility`, `concern`, `thing(s)`, `issue`, and the idiom "this time."
- A **bare "this"** with no noun attached is fine (e.g. "the two have not resolved
  this since") -- it's a standard discourse anaphor for "the whole preceding
  situation," not a bug.
- `"that"`/`"those"` aren't part of this rule at all in this corpus -- "that" only
  ever appears here as the subordinating complementizer ("agreed that...," "knew
  that...") not as a demonstrative.

Everything else -- a **concrete** noun like "this friendship," "this friend,"
"these deadlines," "these events," "these comparisons" -- needs that noun to
actually appear upstream, either verbatim or as a substring (e.g. "friend" is
satisfied by an earlier "friendship").

**`baseline_relational_norm` is the highest-risk type for this bug**, because its
`obligation_sentence` is empty -- there is *nothing* upstream to introduce a new
referent before the violation sentence needs one. If a scenario using this type
needs to reference a specific third party (an ex, a friend, a coworker), introduce
them by description on first mention instead of a demonstrative:
- Bad: *"{agent} suggested {partner} see this friend less often..."* (first mention of anyone at all, using "this")
- Good: *"{agent} suggested {partner} see a long-standing friend of {pronoun_partner_poss} less often..."*

For `recognized_reliance_on_disclosure` specifically, the same risk shows up inside
the obligation sentence itself if it gestures at something ("this friendship")
instead of naming it:
- Bad: *"{partner} had clearly and repeatedly told {agent} that nothing romantic was happening in this friendship."*
- Good: *"{partner} had clearly and repeatedly told {agent} that nothing romantic was happening in {pronoun_partner_poss} friendship with a former coworker."*

## 7. Writing-standards checklist (apply to every new scenario)

From `vignette_writing_standards.md`, items still in force:

- **A. Parity across all 8 cells of one scenario** (4 gender configs x 2 severity):
  same sentence count/order/tense, same closing question verbatim, same amount of
  contextual detail in mild vs. severe (they should differ in *what happened*, not
  in how much detail is given or how emotionally colored the narration is), word
  count within ~15% across the 8 cells.
- **B. No moral adjectives** ("selfish," "cruel," "kind," "considerate"), **no
  personality descriptors** ("tends to be controlling"), **no occupation
  stereotypes**, **no attractiveness cues**, and **no gendered language outside the
  one explicit `(female)`/`(male)` tag** -- no pronouns anywhere, ever (see Section
  2).
- **C. Single-violation constraint.** Exactly one norm-family violation per
  scenario. Before finalizing: could a reader explain the verdict without ever
  mentioning the target norm family? If yes, something else (deception, threats,
  privacy invasion, coercion, discrimination, illegal conduct) is doing the work
  and the scenario needs revision -- unless that *is* the target family itself.
- **D. Obligation strength held constant** within a family (the same
  `obligation_source`'s standard sentence form, verbatim structure, across all 8
  cells of a scenario -- and ideally across a family's scenarios unless a
  difference is deliberately recorded).
- **E. Scenario balance**, checked once a family's full scenario set is drafted,
  not per-scenario: at least 2 distinct `obligation_source` types per family
  (prefer 3), at least 4 distinct `task_object`s, at least 3 distinct
  `violation_form`s.
- **F. Fixed-intentionality tone consistency.** The `knowing_nonmalicious_explanation`
  needs to read as "knowing but not malicious" -- consistently across every family,
  not just internally. Previously caught failure modes: reading as vague
  rationalization (under-shooting) or as controlling/hostile (over-shooting).
- **G. Severity-aspect concordance** -- Sections 5 and 6 above.

## 8. Worked example -- a fully correct scenario

```json
{
  "scenario_id": "HHLAB-01",
  "status": "drafted",
  "task_object": "laundry",
  "violation_form": "knowingly deprioritized",
  "obligation_source": "accepted_role_responsibility",
  "obligation_sentence": "They had previously agreed that {agent} would take on responsibility for the laundry.",
  "mild_violation": "{agent} skipped the laundry once, for about a week",
  "severe_violation": "{agent} has not done the laundry in over four months",
  "knowing_nonmalicious_explanation": "{agent_subj_cap} said {agent_subj} doesn't consider laundry {agent_poss} responsibility",
  "partner_response": "{partner} brought it up and asked {agent} to take it over",
  "outcome": "{partner} has taken over the laundry without further discussion"
}
```

Rendered (MF, mild): *"Agent 1 (male) and Agent 2 (female) have been cohabiting for
3 years. They had previously agreed that Agent 1 would take on responsibility for
the laundry. Agent 1 skipped the laundry once, for about a week. Agent 2 brought it
up and asked Agent 1 to take it over. Agent 1 said Agent 1 doesn't consider laundry
Agent 1's responsibility. Agent 2 has taken over the laundry without further
discussion. Was Agent 1 in the wrong?"*

Note this is a case where `knowing_nonmalicious_explanation` states a categorical
belief ("doesn't consider X my responsibility") without a duration/frequency
marker -- that's fine under Rule 5a, since a belief statement doesn't itself commit
to how many times the agent has acted on it, unlike "hasn't felt like it lately."

## 9. Review gate -- run before treating any generated batch as final

1. Run `python scripts/generate_vignettes.py` to render the new scenarios into
   `data/vignette_core_set.csv` and confirm the row count matches expectations.
2. Run `python scripts/lint_vignette_params.py` -- must report zero hard issues.
   Review-level flags (aspect concordance near ambiguous subjects) still need a
   human read.
3. Check word-count parity and the banned-language scan (Section 7, items A/B) --
   not currently scripted; do this manually or ask an LLM to check a batch at a
   time.
4. Run the Section 7 checklist end-to-end, ideally by someone other than the
   drafter (or a second, independent LLM pass) -- tone and clarity judgment isn't
   fully covered by the lint script and shouldn't be treated as if it were.

## 10. Explicitly undecided -- do not invent these, flag and ask instead

- **Intentionality-robustness arm content** (72 planned prompts: 9 families x 2
  selected scenarios x MF/FM x mild/severe). The *formula* and *selection
  criteria* for which scenarios are good candidates are defined in
  `vignette_params.json`'s `design_summary.intentionality_robustness` (prefer
  forgetting/poor-planning/mistaken-assumption cases; avoid anything that becomes a
  different offense entirely if reframed as negligent, e.g. checking a phone
  without permission). The actual accidental/negligent/purposeful explanation text
  per selected scenario has not been written anywhere yet.
- **Contamination/generalization arm structure** (72 planned prompts, same formula
  shape). `vignette_params.json` states the *purpose* (unfamiliar surface content,
  same normative structure, to test whether an effect survives on material unlikely
  to resemble memorized training data) but the actual scenario content and
  selection method are undefined -- `project_status_summary.md` flags this
  explicitly as still open.
- Both arms are gated on piloting the 288-vignette core first, per the design's own
  sequencing rule -- don't draft full content for either arm as if that gate has
  already passed.
