# Pair-level confidence / ambiguity findings

Generated from `responses/confirmatory/*.csv` (n=7284 rows, 1619 matched pairs). Regenerate via `python scripts/analyze_confidence_ambiguity.py`.

Re-tests the ambiguity mechanism from `analysis/fault_rating_bias_findings.md` ("Does obligation-source ambiguity predict the size of the gender gap?") at the level of the 720 individual matched pairs, rather than the 8 obligation_source-level aggregate points used there. `confidence` here is the mean of each pair's two self-reported (0-100) confidence values -- the field already in the confirmatory-pass data, not the dispersion-based measure specced in `docs/prompt_and_measurement_protocol.md` as the eventual primary metric (that needs a stability pass that hasn't been run).

## Confidence vs. signed gender gap (M - F fault_rating)

r=-0.079, permutation p=0.0016 (n=1619, 20000 shuffles, seed=42).

## Confidence vs. absolute gender gap (|M - F| fault_rating)

r=-0.069, permutation p=0.0059 (n=1619).

## Confidence: disagreement pairs vs. tied pairs

Disagreement pairs (n=426): mean confidence=84.61. Tied pairs (n=1193): mean confidence=85.56. diff=-0.96, Welch t=-2.61.

## Family-residualized version (is this just the family effect again?)

The obligation_source version of this finding mostly turned out to be the family effect once residualized (see `analysis/fault_rating_bias_findings.md`). Same check here: subtract each family's own mean confidence and mean signed gap before correlating, so the test asks whether confidence tracks the gap *within* families, not just because some families happen to have both lower confidence and bigger gaps.

Within-family residualized: r=-0.065, permutation p=0.0090 (n=1619).

## For reference: family-level ecological correlation (analogous to the obligation_source one)

r(family mean confidence, family mean signed gap)=-0.590 (n=9 families -- ecological, same caveat as the obligation_source version).

- Jealousy/possessiveness: mean confidence=82.61, mean signed gap=+0.294
- Mental load: mean confidence=83.62, mean signed gap=+0.183
- Family obligations: mean confidence=84.96, mean signed gap=+0.117
- Household labor: mean confidence=85.28, mean signed gap=+0.156
- Emotional labor: mean confidence=85.38, mean signed gap=+0.072
- Sexuality & Intimacy: mean confidence=85.79, mean signed gap=+0.233
- Career sacrifice: mean confidence=86.37, mean signed gap=+0.184
- Childcare: mean confidence=86.62, mean signed gap=+0.139
- Financial provision: mean confidence=87.16, mean signed gap=+0.100

