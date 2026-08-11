Status Updates

(Running log -- append newest entries at the top. Plain-text formatted so each
entry can be pasted directly into a shared doc without markdown cleanup.)

---

2026-08-11

Paper drafting started for JUDGe 2026 (NeurIPS 2026 workshop, "Can We Trust the
Judge?"). Targeting the Short Paper track, 4 pages plus references, submission
deadline August 29, 2026. Drafted everything not dependent on model results:
Dataset and Design, Measurement Protocol, Related Work, Limitations, Broader
Impacts, a pre-registered Planned Analysis section, and the checklist items
answerable before data exists. Abstract, the Introduction's opening paragraph,
and Results remain blocked on the confirmatory model run. Related Work now
directly engages with Si et al. 2026 (GAMA-Bench) as the closest prior work,
since it already reports a gender asymmetry in relationship-conflict judgment --
this paper's distinguishing contribution is the family-by-family decomposition
by norm-violation type, which no prior study provides.

Incorporated additional literature and design-decision references. Verified
several previously-uncertain citations independently before adding them
(author lists, venues, arXiv IDs): Reliability without Validity (Norman, Rivera
& Hughes 2026), Can You Trust LLM Judgments (Schroeder & Wood-Doughty 2024), a
benchmark-contamination survey (Xu et al. 2024), and the memorization-scaling
paper (Carlini et al. 2023). Added a pre-registered ambivalent-sexism
prediction to the Planned Analysis section (Glick and Fiske 1996, 1999):
benevolent sexism toward women predicts female-favoring leniency in
protection-framable families; hostility toward men via resentment of
paternalism predicts male-disadvantaging harshness in power/provider-role
families. If results show a uniform effect across all nine families instead,
that argues against this account.

A manual review pass surfaced a content bug affecting 17 of the 36 drafted
scenarios: fields shared across both the mild and severe versions of a
scenario (the obligation sentence, the shared explanation, the partner
response) could silently imply an ongoing pattern that contradicted the mild
version's single-incident framing, or leave a demonstrative reference ("this
friendship") with nothing established earlier in the text for it to refer to.
All 17 were corrected -- 7 for a chronicity conflict specific to one
obligation-source type, 8 for verb-aspect leaks in the shared explanation
field, 2 for the missing-antecedent problem. Verified afterward that severity
distinction and word-count parity across each scenario's 8 cells still hold.
This is now documented as item G in the writing-standards checklist and
automated in a new script, lint_vignette_params.py, which currently reports
zero issues against the full dataset.

Also built a consolidated vignette generation spec (docs/vignette_generation_spec.md)
-- a self-contained brief intended to be handed directly to an LLM to draft
further scenarios (for the deferred intentionality-robustness and
contamination arms) that already comply with the schema, the obligation-source
taxonomy and its literature basis, the severity-construction rules learned
from this pass, and the writing-standards checklist, rather than requiring
another manual-review-driven fix pass later.

Cleaned up redundant status documentation: deleted project/README_for_thulasi.md
(a "Week 1 check-in" snapshot that had gone stale and was no longer marked as
superseded, unlike the project's other historical docs), rewrote
project/project_status_summary.md as the one current-state-and-decisions
reference, and trimmed the top-level README down to setup/run instructions
plus a short repo map, removing a second, competing "current state" narrative
that had drifted out of sync with reality.

Confirmed one open design question rather than guessing at it: a proposed
revision to the fault-rating scale's anchor wording (causality/foreseeability/
intentionality-based, following Shaver 1985 and the Model Penal Code, instead
of the current intensity-adjective anchors) is not adopted. The
currently-committed wording in the prompt and measurement protocol remains
authoritative.

Division of labor confirmed: vignette design, content, and interpretation of
results sit with this project's author; running the pilot and further model
experiments sits with the collaborator. The pilot manipulation and severity
check against the full 288-vignette core set, across all 4 gender
configurations, remains the single most important next step and has not been
run yet.

All of the above is committed to the project repository.
