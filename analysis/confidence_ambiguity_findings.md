# Pair-level confidence / ambiguity findings

Generated from `responses/confirmatory/*.csv` (n=1440 rows, 720 matched pairs). Regenerate via `python scripts/analyze_confidence_ambiguity.py`.

Re-tests the ambiguity mechanism from `analysis/fault_rating_bias_findings.md` ("Does obligation-source ambiguity predict the size of the gender gap?") at the level of the 720 individual matched pairs, rather than the 8 obligation_source-level aggregate points used there. `confidence` here is the mean of each pair's two self-reported (0-100) confidence values -- the field already in the confirmatory-pass data, not the dispersion-based measure specced in `docs/prompt_and_measurement_protocol.md` as the eventual primary metric (that needs a stability pass that hasn't been run).

## Confidence vs. signed gender gap (M - F fault_rating)

r=-0.048, permutation p=0.2010 (n=720, 20000 shuffles, seed=42).

## Confidence vs. absolute gender gap (|M - F| fault_rating)

r=-0.036, permutation p=0.3395 (n=720).

## Confidence: disagreement pairs vs. tied pairs

Disagreement pairs (n=175): mean confidence=85.79. Tied pairs (n=545): mean confidence=86.21. diff=-0.42, Welch t=-0.80.

## Family-residualized version (is this just the family effect again?)

The obligation_source version of this finding mostly turned out to be the family effect once residualized (see `analysis/fault_rating_bias_findings.md`). Same check here: subtract each family's own mean confidence and mean signed gap before correlating, so the test asks whether confidence tracks the gap *within* families, not just because some families happen to have both lower confidence and bigger gaps.

Within-family residualized: r=-0.034, permutation p=0.3562 (n=720).

## For reference: family-level ecological correlation (analogous to the obligation_source one)

r(family mean confidence, family mean signed gap)=-0.460 (n=9 families -- ecological, same caveat as the obligation_source version).

- Jealousy/possessiveness: mean confidence=83.00, mean signed gap=+0.275
- Mental load: mean confidence=84.36, mean signed gap=+0.125
- Emotional labor: mean confidence=85.03, mean signed gap=+0.075
- Family obligations: mean confidence=86.08, mean signed gap=+0.113
- Household labor: mean confidence=86.31, mean signed gap=+0.188
- Career sacrifice: mean confidence=86.99, mean signed gap=+0.113
- Sexuality & Intimacy: mean confidence=87.19, mean signed gap=+0.225
- Childcare: mean confidence=87.56, mean signed gap=+0.113
- Financial provision: mean confidence=88.48, mean signed gap=+0.075

