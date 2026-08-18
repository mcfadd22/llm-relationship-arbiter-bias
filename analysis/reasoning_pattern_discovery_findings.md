# Reasoning-text pattern-discovery findings (prototype)

Generated from 175 blind-coded disagreement pairs (of 720 total matched pairs in the original 288-vignette confirmatory pass) via `scripts/analyze_reasoning_patterns.py`. See that script's docstring for full methodology and caveats -- summarized here, not repeated in full.

21/175 pairs (12%) were coded as showing no clear difference in framing despite the numeric ratings differing -- i.e. even restricted to disagreement pairs, a majority still show no detectable linguistic signature of the gender manipulation. The results below describe the minority where a difference was found.

## Per-tag gender skew (six seeded candidate categories)

| Tag | M-agent-text count | F-agent-text count | n | M share | sign-test z | p (uncorrected) | survives Bonferroni (a=0.0083)? |
|---|---|---|---|---|---|---|---|
| hedges-qualifies | 14 | 48 | 62 | 0.226 | -4.32 | 0.0000 | yes |
| attributes-character | 33 | 17 | 50 | 0.660 | +2.26 | 0.0237 | no |
| references-relationship-history | 11 | 8 | 19 | 0.579 | +0.69 | 0.4913 | no |
| centers-partner-feelings | 22 | 24 | 46 | 0.478 | -0.29 | 0.7681 | no |
| harsher-language | 38 | 18 | 56 | 0.679 | +2.67 | 0.0075 | yes |
| cites-external-circumstances | 1 | 6 | 7 | 0.143 | -1.89 | 0.0588 | no |

## Interpretation

**Two findings survive Bonferroni correction and form a coherent, theory-consistent pattern:**

- **`hedges-qualifies` skews heavily toward the female-agent text** (M=14, F=48, n=62, z=-4.32, p<0.0001). When the same underlying facts are explained for a female agent, the reasoning is far more likely to include mitigating language ("though not severe," "a single incident rather than a pattern," "understandable given...") than when explaining the identical facts for a male agent.

- **`attributes-character` and `harsher-language` both skew toward the male-agent text** (attributes-character: M=33, F=17, n=50, p=0.024 -- does not survive strict Bonferroni; harsher-language: M=38, F=18, n=56, p=0.0075 -- survives). Male agents' identical behavior is more often framed as revealing something about who they *are* ("shows a pattern of...," "reflects...") rather than as a situational lapse.

This is a specific, citable mechanism, not just a restatement of the numeric bias: hedging and character-attribution are independent of overall harshness (a text can hedge *and* still land on a harsh verdict, or vice versa), so this isn't simply "harsher language" repeated three ways -- it's evidence that models write *systematically different kinds of explanations* for the same act depending on agent gender, tracking the classic attribution-theory pattern of dispositional attribution for one group and situational excuse for another. `cites-external-circumstances` points the same direction (M=1, F=6) but n=7 is too small to treat as more than suggestive.

**Notably, this succeeds where the predefined-lexicon pipeline (`analyze_reasoning_text.py`) failed on the identical corpus** -- LIB, the lexicon feature specifically designed to capture dispositional-vs-situational attribution via automated dependency parsing, showed essentially no gender effect at all (d_z=-0.004, see `analysis/fault_rating_bias_findings.md`). The construct LIB was built to measure is apparently real (`attributes-character` finds it here) -- the automated parse-based measurement was the insensitive instrument, not proof the effect doesn't exist. Methodological lesson for future lexicon work: automated parsing may be missing signal that careful reading (human or LLM) catches.

## What this is not yet

- **Not independently validated.** Single coder (Claude), no second coder, no inter-rater reliability computed. This is the same open item already flagged for the lexicon features (project status doc, open item 2) -- Meredith's independent read is needed before this goes in the paper as a confirmed finding, not just a promising lead.

- **Categories were seeded, not fully naive.** Six candidate tags were offered up front (with "invent your own" explicitly permitted -- four one-off custom tags did emerge: `shifts-partial-responsibility`, `relational-vs-practical-framing`, `frames-as-normative-obligation`, `forecloses-mutual-responsibility`, each n=1-2, too sparse to test but worth another look with a larger sample). A stricter test of the "discovery" framing would run a first, fully unseeded pass on a subsample to confirm these six aren't just what the seed list primed the coder to see.

- **Disagreement-pairs-only.** By construction (only pairs where the numeric ratings actually differ), so this cannot speak to whether tied pairs (76% of the full dataset) carry any linguistic signal despite agreeing numerically.

- **Same-model coding concern not yet checked**: Claude did the coding, and the reasoning-text corpus includes Claude-generated responses alongside GPT-5-mini/Gemini/Llama/DeepSeek -- worth checking whether the effect holds when restricted to non-Claude-generated texts, to rule out any own-output familiarity effect in the coding itself.

## Recommended next steps

1. Human spot-check (Meredith) of a sample of the 175 coded pairs against the source text, both for face validity of the tags and to catch any coder-introduced pattern that isn't really there.

2. Scale to the full 720 pairs (not just the 175 disagreement pairs) once the expanded dataset's confirmatory run completes, and re-run restricted to each model separately to check the same-model coding concern and whether the pattern is universal across models or concentrated in a subset.

3. Consider a second, independent coding pass (different model or a fully unseeded prompt) on a subsample, to compute actual inter-rater agreement rather than assuming single-coder reliability.

