import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), 'data', 'vignette_params.json')

# Fields in the order generate_vignettes.py actually concatenates them (see render()
# in that script). mild_violation/severe_violation are alternatives -- only one is
# used per rendered vignette, depending on severity -- so callers pick which one goes
# in the "violation" slot before building the ordered field list for a given severity.
FIELD_ORDER = ["obligation_sentence", "violation", "partner_response",
               "knowing_nonmalicious_explanation", "outcome"]

# === Check A: chronicity-vs-mild conflict ===
# If obligation_sentence asserts an existing deficit/imbalance ("more ... than {agent}"),
# a mild_violation that implies total isolation ("once", "one X") contradicts it, since
# obligation_sentence renders in both severity cells. Content-based, not keyed to
# obligation_source's type name (see vignette_writing_standards.md item G.2).
DEFICIT_RE = re.compile(r"more\s+.{0,60}?than\s+\{agent\}", re.IGNORECASE)
# "once again"/"yet again" is the recurrence-acknowledgment idiom itself (the fix for
# this exact check), not an isolation claim -- exclude it rather than flag it.
ISOLATION_RE = re.compile(r"\bonce\b(?!\s+again)|\bone\s+\w+", re.IGNORECASE)


def check_chronicity_mild_conflict(scenario):
    issues = []
    obligation = scenario.get("obligation_sentence") or ""
    mild = scenario.get("mild_violation") or ""
    if DEFICIT_RE.search(obligation) and ISOLATION_RE.search(mild):
        issues.append(
            "HARD: obligation_sentence asserts an existing deficit/imbalance "
            f"({DEFICIT_RE.search(obligation).group()!r}) but mild_violation implies "
            f"total isolation ({ISOLATION_RE.search(mild).group()!r}). The mild cell "
            "should acknowledge it's a further instance within the pattern "
            "(e.g. 'again', 'another') rather than a first-time lapse."
        )
    return issues


# === Check B: demonstrative-antecedent audit ===
# Bare "these" always needs a specific plural noun nearby to be unambiguous. "this X"/
# "these X" need X to have actually been introduced upstream -- UNLESS X is a generic
# discourse-summary noun ("this pattern", "this decision", "this responsibility") that
# refers back to "the whole situation just described" rather than a specific earlier
# noun phrase; those are idiomatic and were confirmed safe throughout the corpus during
# manual audit. Only the next single word after this/these is treated as the candidate
# noun -- "this made X feel..." has "this" as a bare pronoun (subject of "made", a verb,
# not a determiner), so common verb/function words immediately after this/these are
# recognized as pronoun usage and skipped rather than misparsed as a noun.
# "that"/"those" are excluded: in this corpus they only ever appear as the subordinating
# complementizer ("agreed that...", "knew that...", "said that..."), not as demonstratives,
# and including them would swamp real findings in false positives.
DETERMINER_NEXT_WORD_RE = re.compile(r"\b(this|these)\s+([a-z][a-z'-]*)\b", re.IGNORECASE)
BARE_THESE_RE = re.compile(r"\bthese\b(?!\s+[a-z])", re.IGNORECASE)

# "this/these" + one of these next words means "this/these" is a bare pronoun (subject/
# object), not a determiner -- e.g. "resolved this since", "this made {partner} feel",
# "this should have been", "this was a concern".
PRONOUN_USAGE_NEXT_WORDS = {
    "since", "but", "felt", "feels", "made", "makes", "was", "wasn't", "is", "isn't",
    "didn't", "doesn't", "should", "shouldn't", "would", "wouldn't", "has", "hasn't",
    "affected", "matter", "matters", "mattered", "needed", "going",
}

# Generic discourse-summary nouns: "this <noun>" reads as "the situation/thing just
# described", not a reference requiring a specific earlier noun phrase.
GENERIC_ANAPHORA_NOUNS = {
    "pattern", "decision", "situation", "dynamic", "way", "responsibility",
    "concern", "thing", "things", "issue",
    "time",  # "this time" is idiomatic ("on this occasion"), not a noun reference
}


def check_demonstrative_antecedents(scenario, field_order_for_severity, field_values):
    """field_order_for_severity: list of field names in render order for one severity.
    field_values: dict of field name -> rendered text (post-slot-substitution is not
    required here; the raw template text with {placeholders} is fine since we're only
    checking for plain-English nouns, not the placeholders themselves)."""
    issues = []
    upstream = ""
    for field in field_order_for_severity:
        text = field_values.get(field) or ""

        for m in BARE_THESE_RE.finditer(text):
            issues.append(
                f"HARD [{field}]: bare 'these' with no noun attached "
                f"(context: ...{text[max(0, m.start()-25):m.end()+15]}...). "
                "Needs an explicit plural noun or should be reworded."
            )

        for m in DETERMINER_NEXT_WORD_RE.finditer(text):
            next_word = m.group(2).lower()
            if next_word in PRONOUN_USAGE_NEXT_WORDS:
                continue  # bare pronoun, not a determiner+noun -- nothing to check
            head_noun_singular = re.sub(r"(es|s)$", "", next_word)
            if head_noun_singular in GENERIC_ANAPHORA_NOUNS or next_word in GENERIC_ANAPHORA_NOUNS:
                continue  # idiomatic discourse-summary reference, always fine
            if head_noun_singular and re.search(re.escape(head_noun_singular), upstream, re.IGNORECASE):
                continue  # substring match also catches e.g. "friend" within "friendship"
            issues.append(
                f"HARD [{field}]: '{m.group(0)}' -- noun '{next_word}' does not appear "
                f"in any upstream field for this severity path."
            )

        upstream += " " + text

    return issues


# === Check C: severity-aspect concordance (review-level, not a hard rule) ===
# Regex can't reliably tell "agent was falling short" from "partner was counting on
# agent" without real parsing, so this is a flag-for-human-review check, not a hard
# fail -- see vignette_writing_standards.md item G.1.
ASPECT_RE = re.compile(r"\b(was|wasn't|has been|hasn't been)\s+\w+ing\b", re.IGNORECASE)
AGENT_TOKEN_RE = re.compile(r"\{agent(_subj|_obj|_poss|_subj_cap)?\}", re.IGNORECASE)
PARTNER_TOKEN_RE = re.compile(r"\{partner\}|\{pronoun_partner_\w+\}", re.IGNORECASE)


def check_aspect_concordance(scenario):
    issues = []
    for field in ("knowing_nonmalicious_explanation", "partner_response"):
        text = scenario.get(field) or ""
        for m in ASPECT_RE.finditer(text):
            window = text[max(0, m.start() - 40):m.start()]
            near_agent = bool(AGENT_TOKEN_RE.search(window))
            near_partner = bool(PARTNER_TOKEN_RE.search(window))
            if near_agent and not near_partner:
                confidence = "likely describes the agent's own conduct"
            elif near_partner and not near_agent:
                confidence = "likely describes the partner's state -- probably fine, double-check"
            else:
                confidence = "subject unclear from nearby text -- check manually"
            issues.append(
                f"REVIEW [{field}]: progressive/durative phrase {m.group()!r} -- {confidence}. "
                f"context: ...{text[max(0,m.start()-20):m.end()+20]}..."
            )
    return issues


def lint_scenario(scenario):
    """Returns (hard_issues, review_issues) for one scenario."""
    hard = []
    review = []

    hard.extend(check_chronicity_mild_conflict(scenario))

    for sev, violation_field in (("MLD", "mild_violation"), ("SEV", "severe_violation")):
        field_values = dict(scenario)
        field_values["violation"] = scenario.get(violation_field) or ""
        order = ["obligation_sentence", "violation", "partner_response",
                 "knowing_nonmalicious_explanation", "outcome"]
        sev_issues = check_demonstrative_antecedents(scenario, order, field_values)
        hard.extend(f"[{sev}] {issue}" for issue in sev_issues)

    review.extend(check_aspect_concordance(scenario))

    return hard, review


def lint_params_file(path):
    with open(path) as f:
        d = json.load(f)

    total_hard = 0
    total_review = 0
    for fid, fam in d["families"].items():
        for scenario in fam.get("scenarios", []):
            if scenario.get("status") != "drafted":
                continue
            hard, review = lint_scenario(scenario)
            if hard or review:
                print(f"=== {scenario['scenario_id']} ({fid}, obligation={scenario.get('obligation_source')}) ===")
                for issue in hard:
                    print(f"  {issue}")
                for issue in review:
                    print(f"  {issue}")
                print()
            total_hard += len(hard)
            total_review += len(review)

    print(f"Total: {total_hard} hard issue(s), {total_review} review flag(s).")
    return total_hard


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Lint data/vignette_params.json for the mild/severe contradiction "
                    "and antecedent bugs documented in docs/vignette_writing_standards.md item G."
    )
    parser.add_argument("--file", type=str, default=DEFAULT_PATH,
                        help="path to vignette_params.json (default: data/vignette_params.json)")
    args = parser.parse_args()

    n_hard = lint_params_file(args.file)
    raise SystemExit(1 if n_hard > 0 else 0)
