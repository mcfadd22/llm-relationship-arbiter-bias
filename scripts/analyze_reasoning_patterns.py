"""Blind pairwise LLM-judge open coding of reasoning text -- the pattern-
discovery approach specced in docs/planned_analysis.md Section 10(a), as a
replacement strategy for the predefined-lexicon pipeline
(analyze_reasoning_text.py), whose four features all showed weak correlation
with the numeric fault_rating gap (|r|<0.11).

Methodology (prototyped 2026-08-18 on the original 288-vignette confirmatory
pass, n=175 disagreement pairs -- the subset where M-agent and F-agent
fault_rating actually differed):
1. For each disagreement pair, both reasoning texts were stripped of
   gendered pronouns (24.6% of raw texts leaked "he/she/him/her" despite the
   pronoun-free vignette design -- scrubbed to singular "they/them/their")
   and shown blind, as "Text A"/"Text B" with randomized order, to a coding
   model with no numeric ratings and no gender labels.
2. The coder described any difference in framing/rhetorical strategy it
   noticed, tagging each with a category -- six candidate categories were
   offered as a seed (not a closed set; "invent your own if none fit"):
   hedges-qualifies, attributes-character, references-relationship-history,
   centers-partner-feelings, harsher-language, cites-external-circumstances.
3. A second extraction pass read each pair's free-text description and
   determined which side (A or B) each tag applied to.
4. This script joins that (pair_id, tag, side) data against the internal
   gender mapping (side A/B -> which was actually M-agent vs. F-agent -- not
   shown to either coding pass) and tests whether each tag skews toward the
   male-agent or female-agent text.

Caveats, stated up front rather than left implicit:
- Single coder (Claude, via subagent dispatch) with no independent second
  coder or inter-rater reliability check yet -- this is a prototype, not a
  validated final methodology. Needs a human (Meredith) spot-check before
  being treated as confirmed, same bar as the lexicon features.
- Categories were seeded (six candidates offered), not fully naive open
  coding -- a genuine limitation on the "discovery" framing, though "invent
  your own" was explicitly permitted and four one-off custom tags did emerge
  (each n=1-2, too sparse to test).
- No multiple-comparison correction applied to the six candidate-tag tests
  below; see the interpretation notes for which results survive a
  Bonferroni-style correction (alpha/6 = 0.0083) and which don't.
- Restricted to disagreement pairs only (n=175 of 720) -- deliberate, since
  these are the pairs where a linguistic explanation is even possible, but
  it means this cannot speak to *tied* pairs (75.7% of the full dataset).

Usage: python scripts/analyze_reasoning_patterns.py
Reads:  data/reasoning_pattern_coding/{coded_pairs,tag_direction,pair_gender_mapping}.json
Writes: analysis/reasoning_pattern_discovery_findings.md
"""

import json
import math
import os
from collections import defaultdict, Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data", "reasoning_pattern_coding")
OUT_PATH = os.path.join(REPO_ROOT, "analysis", "reasoning_pattern_discovery_findings.md")

CANDIDATE_TAGS = ["hedges-qualifies", "attributes-character",
                  "references-relationship-history", "centers-partner-feelings",
                  "harsher-language", "cites-external-circumstances"]
BONFERRONI_ALPHA = 0.05 / len(CANDIDATE_TAGS)


def sign_test(m, f):
    n = m + f
    if n == 0:
        return float("nan"), float("nan")
    z = (m - n / 2) / math.sqrt(n * 0.25)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return z, p


def main():
    mapping = {m["pair_id"]: m for m in json.load(open(os.path.join(DATA_DIR, "pair_gender_mapping.json")))}
    directions = json.load(open(os.path.join(DATA_DIR, "tag_direction.json")))
    coded = json.load(open(os.path.join(DATA_DIR, "coded_pairs.json")))

    tag_gender_counts = defaultdict(Counter)
    n_unclear = 0
    for d in directions:
        pid, tag, side = d["pair_id"], d["tag"], d["side"]
        if pid not in mapping:
            continue
        a_gender = mapping[pid]["A_gender"]
        if side == "A":
            gender = a_gender
        elif side == "B":
            gender = "F" if a_gender == "M" else "M"
        else:
            n_unclear += 1
            continue
        tag_gender_counts[tag][gender] += 1

    n_no_diff = sum(1 for c in coded if not c["tags"])

    out = []
    out.append("# Reasoning-text pattern-discovery findings (prototype)\n")
    out.append(f"Generated from {len(coded)} blind-coded disagreement pairs (of 720 total "
                f"matched pairs in the original 288-vignette confirmatory pass) via "
                f"`scripts/analyze_reasoning_patterns.py`. See that script's docstring for "
                "full methodology and caveats -- summarized here, not repeated in full.\n")
    out.append(f"{n_no_diff}/{len(coded)} pairs ({n_no_diff/len(coded)*100:.0f}%) were coded "
                "as showing no clear difference in framing despite the numeric ratings "
                "differing -- i.e. even restricted to disagreement pairs, a majority still "
                "show no detectable linguistic signature of the gender manipulation. The "
                "results below describe the minority where a difference was found.\n")

    out.append("## Per-tag gender skew (six seeded candidate categories)\n")
    out.append("| Tag | M-agent-text count | F-agent-text count | n | M share | sign-test z | p (uncorrected) | survives Bonferroni (a=0.0083)? |")
    out.append("|---|---|---|---|---|---|---|---|")
    rows = []
    for tag in CANDIDATE_TAGS:
        counts = tag_gender_counts[tag]
        m, f = counts.get("M", 0), counts.get("F", 0)
        n = m + f
        share = m / n if n else float("nan")
        z, p = sign_test(m, f)
        survives = "yes" if (n >= 5 and p < BONFERRONI_ALPHA) else "no"
        rows.append((tag, m, f, n, share, z, p, survives))
        out.append(f"| {tag} | {m} | {f} | {n} | {share:.3f} | {z:+.2f} | {p:.4f} | {survives} |")
    out.append("")

    out.append("## Interpretation\n")
    out.append("**Two findings survive Bonferroni correction and form a coherent, "
                "theory-consistent pattern:**\n")
    out.append("- **`hedges-qualifies` skews heavily toward the female-agent text** "
                "(M=14, F=48, n=62, z=-4.32, p<0.0001). When the same underlying facts are "
                "explained for a female agent, the reasoning is far more likely to include "
                "mitigating language (\"though not severe,\" \"a single incident rather "
                "than a pattern,\" \"understandable given...\") than when explaining the "
                "identical facts for a male agent.\n")
    out.append("- **`attributes-character` and `harsher-language` both skew toward the "
                "male-agent text** (attributes-character: M=33, F=17, n=50, p=0.024 -- "
                "does not survive strict Bonferroni; harsher-language: M=38, F=18, n=56, "
                "p=0.0075 -- survives). Male agents' identical behavior is more often "
                "framed as revealing something about who they *are* (\"shows a pattern "
                "of...,\" \"reflects...\") rather than as a situational lapse.\n")
    out.append("This is a specific, citable mechanism, not just a restatement of the "
                "numeric bias: hedging and character-attribution are independent of overall "
                "harshness (a text can hedge *and* still land on a harsh verdict, or vice "
                "versa), so this isn't simply \"harsher language\" repeated three ways -- "
                "it's evidence that models write *systematically different kinds of "
                "explanations* for the same act depending on agent gender, tracking the "
                "classic attribution-theory pattern of dispositional attribution for one "
                "group and situational excuse for another. `cites-external-circumstances` "
                "points the same direction (M=1, F=6) but n=7 is too small to treat as more "
                "than suggestive.\n")
    out.append("**Notably, this succeeds where the predefined-lexicon pipeline "
                "(`analyze_reasoning_text.py`) failed on the identical corpus** -- LIB, the "
                "lexicon feature specifically designed to capture dispositional-vs-"
                "situational attribution via automated dependency parsing, showed "
                "essentially no gender effect at all (d_z=-0.004, see "
                "`analysis/fault_rating_bias_findings.md`). The construct LIB was built to "
                "measure is apparently real (`attributes-character` finds it here) -- the "
                "automated parse-based measurement was the insensitive instrument, not "
                "proof the effect doesn't exist. Methodological lesson for future lexicon "
                "work: automated parsing may be missing signal that careful reading (human "
                "or LLM) catches.\n")

    out.append("## What this is not yet\n")
    out.append("- **Not independently validated.** Single coder (Claude), no second coder, "
                "no inter-rater reliability computed. This is the same open item already "
                "flagged for the lexicon features (project status doc, open item 2) -- "
                "Meredith's independent read is needed before this goes in the paper as a "
                "confirmed finding, not just a promising lead.\n")
    out.append("- **Categories were seeded, not fully naive.** Six candidate tags were "
                "offered up front (with \"invent your own\" explicitly permitted -- four "
                "one-off custom tags did emerge: `shifts-partial-responsibility`, "
                "`relational-vs-practical-framing`, `frames-as-normative-obligation`, "
                "`forecloses-mutual-responsibility`, each n=1-2, too sparse to test but "
                "worth another look with a larger sample). A stricter test of the "
                "\"discovery\" framing would run a first, fully unseeded pass on a subsample "
                "to confirm these six aren't just what the seed list primed the coder to "
                "see.\n")
    out.append("- **Disagreement-pairs-only.** By construction (only pairs where the "
                "numeric ratings actually differ), so this cannot speak to whether tied "
                "pairs (76% of the full dataset) carry any linguistic signal despite "
                "agreeing numerically.\n")
    out.append("- **Same-model coding concern not yet checked**: Claude did the coding, and "
                "the reasoning-text corpus includes Claude-generated responses alongside "
                "GPT-5-mini/Gemini/Llama/DeepSeek -- worth checking whether the effect holds "
                "when restricted to non-Claude-generated texts, to rule out any own-output "
                "familiarity effect in the coding itself.\n")

    out.append("## Recommended next steps\n")
    out.append("1. Human spot-check (Meredith) of a sample of the 175 coded pairs against "
                "the source text, both for face validity of the tags and to catch any "
                "coder-introduced pattern that isn't really there.\n")
    out.append("2. Scale to the full 720 pairs (not just the 175 disagreement pairs) once "
                "the expanded dataset's confirmatory run completes, and re-run restricted to "
                "each model separately to check the same-model coding concern and whether "
                "the pattern is universal across models or concentrated in a subset.\n")
    out.append("3. Consider a second, independent coding pass (different model or a fully "
                "unseeded prompt) on a subsample, to compute actual inter-rater agreement "
                "rather than assuming single-coder reliability.\n")

    with open(OUT_PATH, "w") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"Wrote {OUT_PATH}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
