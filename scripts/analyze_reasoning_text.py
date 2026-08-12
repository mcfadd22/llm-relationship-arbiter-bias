"""Extract linguistic bias features from the `reasoning` field of confirmatory-pass
responses (responses/confirmatory/*.csv) and write one row per response to
analysis/reasoning_features.csv.

Three feature families, chosen to operationalize the coding scheme agreed with
Meredith (see project/ for the analysis plan):

1. Agentic / communal domain-word rates (analysis/lexicons/agentic_communal.csv)
   -- word lists adapted from Abele & Wojciszke (2007) and the Big Two /
   agency-communion framework (Bakan, 1966), including negated-communion terms
   that show up in blame language (e.g. "uncaring", "dismissive").
2. Moral-intensity score (analysis/lexicons/moral_intensity.csv) -- harsh minus
   mitigating term rate, a purpose-built bipolar lexicon since LIWC is paywalled
   and off-the-shelf moral dictionaries (e.g. eMFD) measure a different
   construct (moral foundations, not blame intensity).

   Both lexicons were validated and substantially expanded against actual
   corpus word/lemma frequencies (see analysis/ notes) after an initial
   literature-only pass showed 86-92% zero-hit rates on this dataset: the
   models' blame language here is corpus-specific and clinical ("disregard"
   441x, "neglect" 106x, "dismiss[ive]" 228x) rather than the colorful trait
   adjectives (e.g. "cruel", "manipulative") the literature word lists
   expected, which barely occur (0-1x each). Notably, corpus-frequent agentic
   trait terms remain rare even after expansion (~55 total hits across 1440
   responses) -- the models overwhelmingly frame these relational-obligation
   violations in communal terms, which may itself be a citable descriptive
   finding rather than a lexicon-coverage failure.
3. Linguistic Intergroup Bias (LIB) abstraction score (Maass, Salvi, Arcuri &
   Semin, 1989) -- a heuristic, dependency-parse-based approximation: for each
   clause with "Agent 1/2" as subject, scores predicate-adjective descriptions
   ("Agent 1 is selfish") as most abstract/dispositional (4), psychological
   state verbs (3), interpretive action verbs (2), and other action verbs as
   most concrete/situational (1), then averages per response.

This is a first-pass heuristic pipeline, not a validated coding instrument --
see the plan for the manual-validation step against a hand-read subsample
before treating these scores as paper-ready.

Usage: python scripts/analyze_reasoning_text.py
Reads:  responses/confirmatory/*.csv
Writes: analysis/reasoning_features.csv
"""

import csv
import glob
import os
import re
import statistics

import spacy

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_GLOB = os.path.join(REPO_ROOT, "responses", "confirmatory", "*.csv")
LEXICON_DIR = os.path.join(REPO_ROOT, "analysis", "lexicons")
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "reasoning_features.csv")

STATE_VERBS = {
    "want", "know", "feel", "believe", "resent", "care", "think", "expect",
    "need", "love", "prefer", "intend", "realize", "understand", "appreciate",
    "recognize", "wish", "hope",
}
INTERPRETIVE_VERBS = {
    "ignore", "dismiss", "neglect", "abandon", "betray", "withhold",
    "violate", "disregard", "prioritize", "blame", "minimize", "break",
    "breach", "undermine", "disrespect", "exclude", "fail",
}


def load_lexicon(filename):
    """Returns {category: (single_word_term_set, hyphenated_term_regex)}.

    Matching is lemma-based (via the already-parsed spaCy doc) so inflected
    forms count too (e.g. "disregarded"/"disregarding" -> lemma "disregard").
    Hyphenated compounds (e.g. "self-centered") are matched separately by
    regex over the raw text, since spaCy's tokenizer splits them into three
    tokens ("self", "-", "centered"), which lemma-based single-token matching
    can't catch.
    """
    path = os.path.join(LEXICON_DIR, filename)
    by_category = {}
    with open(path) as fh:
        for row in csv.DictReader(fh):
            by_category.setdefault(row["category"], []).append(row["term"].lower())
    result = {}
    for category, terms in by_category.items():
        single = {t for t in terms if "-" not in t}
        hyphenated = [t for t in terms if "-" in t]
        pattern = None
        if hyphenated:
            alternation = "|".join(re.escape(t) for t in sorted(hyphenated, key=len, reverse=True))
            pattern = re.compile(rf"\b(?:{alternation})\b", re.IGNORECASE)
        result[category] = (single, pattern)
    return result


def count_lexicon_hits(doc, raw_text, lexicon):
    counts = {}
    for category, (single_terms, hyphen_pattern) in lexicon.items():
        n = sum(1 for t in doc if t.is_alpha and (t.lemma_.lower() in single_terms or t.text.lower() in single_terms))
        if hyphen_pattern is not None:
            n += len(hyphen_pattern.findall(raw_text))
        counts[category] = n
    return counts


AGENT1_PLACEHOLDER = "Aidan"
AGENT2_PLACEHOLDER = "Blake"
AGENT1_PATTERN = re.compile(r"\bAgent\s*1\b")
AGENT2_PATTERN = re.compile(r"\bAgent\s*2\b")


def substitute_agent_names(text):
    # "Agent 1"/"Agent 2" as literal tokens visibly confuse spaCy's dependency
    # parser (e.g. attaching the verb as a conjunct of a preceding adverb
    # instead of treating "Agent" as the subject). Swapping in ordinary proper
    # names before parsing fixes the attachment and also lets us unambiguously
    # restrict LIB scoring to Agent 1 (the norm-violator) rather than
    # accidentally counting clauses about Agent 2 (the partner) as well.
    text = AGENT1_PATTERN.sub(AGENT1_PLACEHOLDER, text)
    text = AGENT2_PATTERN.sub(AGENT2_PLACEHOLDER, text)
    return text


def lib_levels_for_doc(doc):
    levels = []
    for token in doc:
        if token.dep_ not in ("nsubj", "nsubjpass"):
            continue
        if token.text != AGENT1_PLACEHOLDER:
            continue
        head = token.head
        if head.lemma_.lower() == "be":
            adjs = [c for c in head.children if c.dep_ in ("acomp", "attr") and c.pos_ in ("ADJ", "NOUN")]
            if adjs:
                levels.append(4)
            continue
        if head.pos_ == "VERB":
            lemma = head.lemma_.lower()
            if lemma in STATE_VERBS:
                levels.append(3)
            elif lemma in INTERPRETIVE_VERBS:
                levels.append(2)
            else:
                levels.append(1)
    return levels


def main():
    nlp = spacy.load("en_core_web_sm", disable=["ner"])

    ac_lexicon = load_lexicon("agentic_communal.csv")
    mi_lexicon = load_lexicon("moral_intensity.csv")

    files = sorted(glob.glob(RESPONSES_GLOB))
    rows_out = []

    for f in files:
        with open(f) as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)

        texts = [substitute_agent_names(r["reasoning"]) for r in rows]
        docs = nlp.pipe(texts, batch_size=64)

        for row, doc in zip(rows, docs):
            word_count = sum(1 for t in doc if t.is_alpha)
            ac_counts = count_lexicon_hits(doc, row["reasoning"], ac_lexicon)
            mi_counts = count_lexicon_hits(doc, row["reasoning"], mi_lexicon)
            levels = lib_levels_for_doc(doc)

            agentic_count = ac_counts.get("agentic", 0)
            communal_count = ac_counts.get("communal", 0)
            harsh_count = mi_counts.get("harsh", 0)
            mitigating_count = mi_counts.get("mitigating", 0)

            denom = word_count if word_count else 1
            rows_out.append({
                "vignette_id": row["vignette_id"],
                "model": row["model"],
                "family_id": row["family_id"],
                "family_name": row["family_name"],
                "scenario_id": row["scenario_id"],
                "agent_gender": row["agent_gender"],
                "partner_gender": row["partner_gender"],
                "severity": row["severity"],
                "fault_rating": row["fault_rating"],
                "word_count": word_count,
                "agentic_count": agentic_count,
                "communal_count": communal_count,
                "agentic_rate_per100w": round(agentic_count / denom * 100, 3),
                "communal_rate_per100w": round(communal_count / denom * 100, 3),
                "moral_harsh_count": harsh_count,
                "moral_mitigating_count": mitigating_count,
                "moral_intensity_score_per100w": round((harsh_count - mitigating_count) / denom * 100, 3),
                "lib_mean": round(statistics.mean(levels), 3) if levels else "",
                "lib_n_clauses": len(levels),
            })

    fieldnames = list(rows_out[0].keys())
    with open(OUT_PATH, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
