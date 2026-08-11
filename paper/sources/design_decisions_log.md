# Design Decisions Log: Source → Decision Traceability

Purpose: the lit review documents what's known in the relevant literatures. This document tracks the narrower, more important thing — which specific sources directly caused a specific design choice in *this* study, as opposed to sources read for general grounding or context. Update this alongside the lit review as new decisions get made; each entry should be checkable against the actual current design (vignette params, prompt, scale) at any time.

Format per entry: **Source → Decision it drove → Where that shows up in the design → Status**

---

## Vignette construction

**Clark & Mills (1979, 1993), "communal vs. exchange relationships"**
→ Directly determined the `need_responsive_relational_duty` obligation-source template ("{partner} has come to rely on {agent} to check in during difficult moments, and {agent} has generally done so") — the specific choice to frame need-responsiveness, not tracked reciprocity, as the obligation basis for the emotional-labor family.
→ Shows up in: `vignette_params.json`, `obligation_sources.need_responsive_relational_duty`.
→ Status: implemented.

**Hardimon (1994), "Role Obligations"**
→ Directly determined the `accepted_role_responsibility` obligation-source template, specifically the choice to frame it as a *role assigned and accepted* ("They had previously agreed that {agent} would take on responsibility for {task}") rather than role membership alone — i.e., marriage/partnership itself doesn't create the obligation, a specific assignment within it does.
→ Shows up in: `vignette_params.json`, `obligation_sources.accepted_role_responsibility`.
→ Status: implemented.

**Daminger (2019), "The Cognitive Dimension of Household Labor"**
→ Directly determined the `established_joint_practice` obligation-source template and the decision to treat mental load as a *pattern-based, often-unspoken* obligation rather than an explicitly agreed one — the template's own basis note cites this paper by name for exactly this reasoning.
→ Shows up in: `vignette_params.json`, `obligation_sources.established_joint_practice`; directly informs the MENTAL family's vignette construction specifically.
→ Status: implemented.

**Scanlon (1998), *What We Owe to Each Other***
→ Directly determined the `recognized_reliance_on_disclosure` obligation-source template, and specifically the corrected framing (per your own earlier feedback) that it's not promising-as-self-binding but *inducing/ignoring reasonable reliance on a stated fact* that carries moral weight — this reframing is attributed directly to Scanlon's Principle F (assurance) in the template's basis note.
→ Shows up in: `vignette_params.json`, `obligation_sources.recognized_reliance_on_disclosure`.
→ Status: implemented.

**Gouldner (1960), "The Norm of Reciprocity"; Rawls (1964); Walster, Berscheid & Walster (1978)**
→ Jointly determined the `contribution_based_reciprocity` obligation-source template — fairness/reciprocity grounded in unequal contribution over time, explicitly distinguished from a discrete promise.
→ Shows up in: `vignette_params.json`, `obligation_sources.contribution_based_reciprocity`.
→ Status: implemented.

**Wertheimer (1987), *Coercion*; Scanlon (1998)**
→ Jointly determined the `baseline_relational_norm` obligation-source template — grounding a norm that doesn't need relational agreement to bind (duty not to coerce/violate autonomy), and flagged the pilot-check requirement on this category specifically (confirm the "mild" condition reads as an actual violation and not a reasonable boundary request).
→ Shows up in: `vignette_params.json`, `obligation_sources.baseline_relational_norm`, plus the associated `pilot_check_flag`.
→ Status: implemented, pilot check still open.

**Real-world AITA convention (parenthetical age/gender self-tagging, e.g. "I (24F) am upset with my partner (28M)")**
→ Directly reversed an earlier design instinct: originally argued the parenthetical tag was an atypical, non-naturalistic addition; once the actual AITA convention was pointed out, this flipped to being the *more* naturalistic choice, not less. Determined the decision to add `(agent_gender)` / `(partner_gender)` tags to vignette text alongside pronouns, while keeping gender-neutral names — combining the tag convention with the pre-existing name-confound mitigation rather than treating them as competing choices.
→ Shows up in: vignette rendering template (name + parenthetical tag + pronoun, redundant exactly as the genre does it).
→ Status: agreed in principle; not yet regenerated in the actual vignette CSV (pending file re-upload from prior session).

---

## Fault-rating scale construction

**Shaver (1985), *The Attribution of Blame***
→ Directly caused the restructuring of the 0–7 scale anchors from stacked intensity-adjectives ("minor" → "significant" → "severe") to qualitatively distinct explanations for the conduct (causality, foreseeability, intentionality, presence/absence of excuse or justification) — this is the specific theoretical basis cited for *why* the anchors should differ in kind, not just degree.
→ Shows up in: revised fault-rating scale wording (0–7 anchors keyed to distinct explanations, e.g. "reasonable response" vs. "small oversight" vs. "knowingly disregarded"), directly replacing the original intensity-adjective version.
→ Status: implemented in the revised prompt draft.

**Malle & Nelson (2003), "Judging Mens Rea"**
→ Directly supported treating obligation-clarity and intentionality as separate, explicitly measurable inputs to the fault judgment — validated that the `obligation_identified` field and the intentionality manipulation (already present in the design) were tracking a real, named construct rather than an ad hoc combination.
→ Shows up in: justification for keeping `obligation_identified` as a distinct output field, and for treating intentionality as a first-class manipulated factor rather than folding it into severity.
→ Status: confirms existing design choice rather than changing it.

**Model Penal Code §2.02 culpability levels (purposeful/knowing/reckless/negligent)**
→ Directly fixed the specific problem of anchors 6 and 7 both reaching for "serious/severe" language and being hard to distinguish — the fix (each level = a different mental state/explanation, not a stronger synonym) is a direct structural borrowing from MPC logic, not just a general inspiration.
→ Shows up in: revised scale anchors 4–7, which now hinge on distinct claims about what the agent knew and intended ("knowingly did not meet an obligation" vs. "disregarded an obligation... in a way that predictably harmed" vs. "knowingly and repeatedly disregarded... despite being aware of the harm" vs. "deliberately and knowingly violated... with disregard for wellbeing").
→ Status: implemented in the revised prompt draft.

**AITA's own YTA/NTA/ESH/NAH categorical scheme**
→ Identified a specific gap the continuous 0–7 scale can't represent (joint fault / mutual non-fault, as opposed to one party being more at fault) — proposed as a candidate addition (a categorical verdict field alongside the continuous rating), not yet built.
→ Shows up in: not yet implemented; flagged as an open design question.
→ Status: open — decision not yet made on whether to add this field.

---

## Prompt / target-identification design

**Real vignette-structure risk (identified through the design process, not a single external source)**
→ "The first-mentioned partner" as a positional reference in the original prompt was identified as fragile under any paraphrase ablation that reorders the vignette. Directly caused the switch to naming the agent explicitly (`{agent_name}`) in both the prompt instruction and the scale anchors, rather than relying on sentence position.
→ Shows up in: revised prompt ("Fault rating scale — how much was {agent_name} in the wrong"), and every anchor line now reads "{agent_name}'s action was..." instead of "the first-mentioned partner."
→ Status: implemented in the revised prompt draft.

---

## Methodological / instrument design (LLM-as-judge and contamination)

**Zheng et al. (2023), "Judging LLM-as-a-Judge"**
→ Directly identified verbosity bias and self-enhancement bias as specific, named risks to flag for the prompt-paraphrase ablation work and for any judge/target-model overlap in the model roster — not yet a design change, but a specific risk now on record to check for once the paraphrase ablation is actually run.
→ Shows up in: not yet implemented as a check; flagged as something to test for once paraphrase variants exist.
→ Status: open — no concrete design change yet, but a specific, named check to add later.

**Temperature/consistency findings (Stureborg et al. 2024; Haldar & Hockenmaier 2025, via the "Reliability without Validity" survey)**
→ Directly informs (but has not yet resolved) the question of how many repeated samples per vignette-cell are needed at whatever temperature the study uses, since same-verdict consistency drops from ~95% at T=0 to as low as ~70% at T=1. This is a concrete number to design the stability/replication pass against, rather than picking a sample count arbitrarily.
→ Shows up in: not yet implemented; the actual sample-count and temperature decision for the study's stability pass is still open.
→ Status: open — decision not yet made, but now has a concrete empirical anchor to make it against.

**Russo et al. (2025), "The Pluralistic Moral Gap"**
→ Directly suggested a specific, concrete addition to the study's contamination-mitigation plan: a manipulation check prompting a separate model call to guess whether a given vignette is real-vs-synthetic/AITA-derived, adapted from their filtering step (they checked whether GPT-4o-mini could still identify a rewritten dilemma as AITA-sourced). This project's vignettes are already written from scratch (a stronger starting position than Russo et al.'s, who launder real posts), but the verification logic transfers directly as an added check.
→ Shows up in: not yet implemented; proposed as a cheap addition to the pilot-check process.
→ Status: open — proposed, not yet decided or built.

---

## Analysis plan

**Glick & Fiske (1996) Ambivalent Sexism Inventory; Glick & Fiske (1999) Ambivalence Toward Men Inventory**
→ Directly generates a specific, falsifiable prediction to build into the analysis plan *before* results come in, rather than fitting a story after the fact: benevolent-sexism-toward-women predicts female-favoring leniency concentrated in families framable as needing protection/accommodation (e.g., emotional labor, sexual expectations); hostility-toward-men via resentment-of-paternalism predicts male-disadvantaging harshness concentrated in families involving power/control/provider-role failure (e.g., financial provision, household authority, jealousy). If the family-by-family results instead show uniform direction/magnitude across all 9 families, that argues against an ambivalent-sexism account and toward a simpler undifferentiated bias — worth stating this as a pre-registered-style contrast in the analysis plan, not just discovering it post-hoc.
→ Shows up in: not yet implemented — this should be written into the analysis plan / pre-specified hypotheses before running the main experiment, so the family-by-family breakdown can be read against this prediction rather than interpreted freely after the fact.
→ Status: open — a specific, checkable thing to add to the analysis plan before data collection.

## How to use this going forward

Add a new entry any time a specific source changes or confirms a specific, checkable piece of the design — a template, a scale anchor, a prompt sentence, a sample-size decision. Sources read only for framing, background, or the "related work" section of a write-up don't need an entry here; they belong in the lit review instead. If a decision is proposed but not yet implemented, mark it "open" so it's traceable whether it ever gets resolved.
