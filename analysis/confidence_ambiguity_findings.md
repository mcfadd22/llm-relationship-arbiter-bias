# Pair-level confidence / ambiguity findings

Generated from `responses/confirmatory/*.csv` (n=5826 rows, 1295 matched pairs). Regenerate via `python scripts/analyze_confidence_ambiguity.py`.

Re-tests the ambiguity mechanism from `analysis/fault_rating_bias_findings.md` ("Does obligation-source ambiguity predict the size of the gender gap?") at the level of the 720 individual matched pairs, rather than the 8 obligation_source-level aggregate points used there. `confidence` here is the mean of each pair's two self-reported (0-100) confidence values -- the field already in the confirmatory-pass data, not the dispersion-based measure specced in `docs/prompt_and_measurement_protocol.md` as the eventual primary metric (that needs a stability pass that hasn't been run).

## Confidence vs. signed gender gap (M - F fault_rating)

r=-0.068, permutation p=0.0125 (n=1295, 20000 shuffles, seed=42).

## Confidence vs. absolute gender gap (|M - F| fault_rating)

r=-0.108, permutation p=0.0001 (n=1295).

## Confidence: disagreement pairs vs. tied pairs

Disagreement pairs (n=335): mean confidence=86.98. Tied pairs (n=960): mean confidence=87.88. diff=-0.90, Welch t=-3.33.

## Family-residualized version (is this just the family effect again?)

The obligation_source version of this finding mostly turned out to be the family effect once residualized (see `analysis/fault_rating_bias_findings.md`). Same check here: subtract each family's own mean confidence and mean signed gap before correlating, so the test asks whether confidence tracks the gap *within* families, not just because some families happen to have both lower confidence and bigger gaps.

Within-family residualized: r=-0.056, permutation p=0.0442 (n=1295).

## For reference: family-level ecological correlation (analogous to the obligation_source one)

r(family mean confidence, family mean signed gap)=-0.380 (n=9 families -- ecological, same caveat as the obligation_source version).

- Jealousy/possessiveness: mean confidence=85.70, mean signed gap=+0.340
- Mental load: mean confidence=86.06, mean signed gap=+0.146
- Family obligations: mean confidence=87.09, mean signed gap=+0.076
- Household labor: mean confidence=87.43, mean signed gap=+0.104
- Emotional labor: mean confidence=88.02, mean signed gap=+0.049
- Sexuality & Intimacy: mean confidence=88.18, mean signed gap=+0.243
- Childcare: mean confidence=88.44, mean signed gap=+0.111
- Career sacrifice: mean confidence=88.65, mean signed gap=+0.154
- Financial provision: mean confidence=89.23, mean signed gap=+0.153

