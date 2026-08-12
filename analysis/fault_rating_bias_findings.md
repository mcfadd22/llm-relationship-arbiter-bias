# Fault-rating gender-bias findings

Generated from `responses/confirmatory/*.csv` (n=1440 rows) and `analysis/reasoning_features.csv`. Regenerate via `python scripts/analyze_fault_rating_bias.py`.

## Severity manipulation check

SEV mean=5.447, MLD mean=4.794, diff=0.653, d=0.835, Welch t=15.84. **Passes.**

## Core finding: agent-gender effect on fault_rating

Paired (scenario x severity x model held constant): n=720 pairs, mean diff (M-F)=+0.144, paired t=7.73, d_z=0.288.

Sign breakdown: 545 ties (75.7%), M>F in 137, F>M in 38 (ratio 3.61:1, sign-test z=7.48).

## Agent-gender effect by relationship-norm family

- Jealousy/possessiveness: n=80, diff=+0.275, t=+3.65, d_z=+0.408
- Sexuality & Intimacy: n=80, diff=+0.225, t=+3.51, d_z=+0.393
- Household labor: n=80, diff=+0.188, t=+3.50, d_z=+0.391
- Career sacrifice: n=80, diff=+0.113, t=+2.39, d_z=+0.267
- Family obligations: n=80, diff=+0.113, t=+2.39, d_z=+0.267
- Childcare: n=80, diff=+0.113, t=+2.24, d_z=+0.250
- Mental load: n=80, diff=+0.125, t=+2.08, d_z=+0.233
- Emotional labor: n=80, diff=+0.075, t=+1.62, d_z=+0.181
- Financial provision: n=80, diff=+0.075, t=+1.42, d_z=+0.159

## Agent-gender effect and disagreement-pair ratio by model

- gpt5_mini: n=144, diff=+0.250, t=+5.23, d_z=+0.436, disagreement rate=50/144=34.7%, M-blamed:F-blamed ratio=5.25:1
- deepseek_v3: n=144, diff=+0.111, t=+2.51, d_z=+0.210, disagreement rate=36/144=25.0%, M-blamed:F-blamed ratio=2.60:1
- gemini_flash: n=144, diff=+0.104, t=+2.59, d_z=+0.215, disagreement rate=35/144=24.3%, M-blamed:F-blamed ratio=2.50:1
- claude_sonnet: n=144, diff=+0.132, t=+3.55, d_z=+0.296, disagreement rate=31/144=21.5%, M-blamed:F-blamed ratio=4.17:1
- llama33: n=144, diff=+0.125, t=+3.29, d_z=+0.274, disagreement rate=23/144=16.0%, M-blamed:F-blamed ratio=4.75:1

## Formal test: does family (or model) significantly moderate the gender effect?

The per-family and per-model breakdowns above each test whether that subgroup's own effect differs from zero -- they do NOT test whether the subgroups differ from *each other* more than chance would. That's a separate, harder question, tested here with a label-shuffle permutation one-way ANOVA on the per-pair fault_rating gender-diffs (family or model as the grouping label, 20000 shuffles, seed=42).

- **Family**: F(8,711)=1.538, permutation p=0.1349
- **Model**: F(4,715)=2.073, permutation p=0.0847

**Neither reaches conventional significance (both p>0.05).** The per-family and per-model rankings reported above are a real, corroborated *descriptive* pattern (consistent across effect size, disagreement rate, and -- for family -- language visibility), but this formal test says we do not yet have the statistical power/evidence to claim family or model *significantly* moderates the size of the gender effect. With only 9 family groups or 5 model groups of ~80-144 pairs each, and the pooled effect itself modest (d_z=0.29), this omnibus test is inherently underpowered relative to the individual within-subgroup tests. **Correct framing for the paper:** the bias direction is remarkably consistent (never reverses across 9 families, 5 models, 2 severities), but claims that specific domains (e.g. Sexuality/Jealousy) show a *significantly larger* bias than others (e.g. Financial provision/Emotional labor) are not currently supported by a formal test and should be described as a suggestive, not confirmed, pattern -- a good candidate for the stability-pass/larger-N follow-up rather than a claim in the current paper's Results section.

## Agent-gender effect by obligation_source

- good_faith_relationship_maintenance: n=20, diff=+0.250, t=+2.03, d_z=+0.454
- need_responsive_relational_duty: n=60, diff=+0.200, t=+3.01, d_z=+0.389
- fair_notice_of_expectations: n=20, diff=+0.300, t=+1.67, d_z=+0.374
- baseline_relational_norm: n=120, diff=+0.208, t=+4.05, d_z=+0.370
- established_joint_practice: n=80, diff=+0.163, t=+2.97, d_z=+0.332
- recognized_reliance_on_disclosure: n=40, diff=+0.200, t=+2.08, d_z=+0.329
- accepted_role_responsibility: n=220, diff=+0.109, t=+3.41, d_z=+0.230
- contribution_based_reciprocity: n=160, diff=+0.069, t=+2.23, d_z=+0.176

Same formal-test caveat as family/model above: permutation omnibus test F(7,712)=1.554, p=0.1458 -- does not reach conventional significance. The ranking above is descriptive, corroborated by the disagreement-rate-by-source breakdown below, but not (yet) a confirmed difference between sources.

## Obligation_source profile across all vignettes (not nested in family)

The breakdown above is the gender-gap by obligation_source. This section asks a different, more basic question: independent of the gender-bias question entirely, does obligation_source predict anything about how these vignettes get judged? Each source already pools across every family it appears in (see the family x obligation_source crosstab above), so this is a genuine across-vignette view, not a family-nested one.

### Absolute fault_rating level by obligation_source (main effect, both genders pooled)

- contribution_based_reciprocity: n=320, mean fault_rating=5.428 (sd=0.593), mean confidence=87.5
- accepted_role_responsibility: n=440, mean fault_rating=5.273 (sd=0.720), mean confidence=87.7
- recognized_reliance_on_disclosure: n=80, mean fault_rating=5.175 (sd=0.591), mean confidence=85.8
- need_responsive_relational_duty: n=120, mean fault_rating=5.150 (sd=0.694), mean confidence=83.3
- good_faith_relationship_maintenance: n=40, mean fault_rating=4.975 (sd=0.620), mean confidence=84.9
- baseline_relational_norm: n=240, mean fault_rating=4.787 (sd=1.083), mean confidence=83.6
- established_joint_practice: n=160, mean fault_rating=4.706 (sd=1.073), mean confidence=85.7
- fair_notice_of_expectations: n=40, mean fault_rating=4.600 (sd=0.778), mean confidence=85.0

Range runs from fair_notice_of_expectations (mean=4.60) to contribution_based_reciprocity (mean=5.43) -- obligation_source clearly predicts how blameworthy a violation is judged overall, well before gender enters the picture at all. This is a distinct, and arguably more basic, finding from the gender-gap-by-source result above.

### Disagreement-pair rate and language, by obligation_source

- fair_notice_of_expectations: n=20, disagreement=8/20=40.0%, M-blamed:F-blamed=3.00:1, language agentic=+0.000(t=+nan), communal=+0.005(t=+0.0), moral=+0.854(t=+1.8), lib=-0.083(t=-0.2)
- good_faith_relationship_maintenance: n=20, disagreement=7/20=35.0%, M-blamed:F-blamed=6.00:1, language agentic=+0.388(t=+2.3), communal=+0.544(t=+1.4), moral=-0.370(t=-1.5), lib=+0.067(t=+0.6)
- recognized_reliance_on_disclosure: n=40, disagreement=13/40=32.5%, M-blamed:F-blamed=5.50:1, language agentic=+0.000(t=+nan), communal=+0.040(t=+0.2), moral=+0.410(t=+1.4), lib=-0.176(t=-1.2)
- baseline_relational_norm: n=120, disagreement=34/120=28.3%, M-blamed:F-blamed=4.67:1, language agentic=-0.045(t=-0.4), communal=+0.342(t=+2.0), moral=+0.334(t=+1.4), lib=-0.147(t=-1.7)
- established_joint_practice: n=80, disagreement=21/80=26.2%, M-blamed:F-blamed=4.25:1, language agentic=+0.019(t=+1.0), communal=-0.124(t=-0.8), moral=+0.034(t=+0.2), lib=-0.014(t=-0.2)
- need_responsive_relational_duty: n=60, disagreement=15/60=25.0%, M-blamed:F-blamed=6.50:1, language agentic=+0.000(t=+nan), communal=-0.011(t=-0.1), moral=-0.333(t=-1.7), lib=+0.055(t=+0.5)
- accepted_role_responsibility: n=220, disagreement=52/220=23.6%, M-blamed:F-blamed=2.71:1, language agentic=+0.006(t=+0.1), communal=+0.038(t=+0.4), moral=+0.193(t=+1.7), lib=+0.042(t=+1.4)
- contribution_based_reciprocity: n=160, disagreement=25/160=15.6%, M-blamed:F-blamed=2.57:1, language agentic=+0.021(t=+1.4), communal=+0.242(t=+1.9), moral=+0.218(t=+1.4), lib=+0.038(t=+0.6)

Small per-source n (20-220 pairs) and no multiple-comparison correction here either -- same caveat as the family breakdown.

### Does obligation-source ambiguity predict the size of the gender gap?

Across the 8 obligation sources (n=8 source-level data points -- an ecological correlation, not an individual-response-level test): r(gender-effect d_z, mean fault_rating)=-0.624, r(gender-effect d_z, mean confidence)=-0.824. Sources judged with *lower* absolute blame and *lower* confidence tend to show *larger* gender gaps; sources judged as clearly and confidently blameworthy (contribution_based_reciprocity, accepted_role_responsibility -- the two highest mean fault_rating and confidence) show the smallest gender gaps. Only 8 data points, so this is a strong descriptive pattern and a plausible mechanism hypothesis (ambiguity leaves more room for gender to influence judgment) -- not independent statistical confirmation at the individual-response level.

## Is the obligation_source effect divorceable from family/domain?

Two obligation sources are single-family by design and cannot be separated from domain at all: `fair_notice_of_expectations` and `good_faith_relationship_maintenance` both occur only in Sexuality & Intimacy. `contribution_based_reciprocity` (8/9 families) and `accepted_role_responsibility` (6/9 families) are the most cross-cutting and the best candidates for a source-vs-family test.

Residualizing each pair's diff by its family's mean diff (i.e. asking whether obligation_source predicts anything *beyond* which family it came from):

- contribution_based_reciprocity: n=160, residual mean=-0.059, residual t=-1.94
- accepted_role_responsibility: n=220, residual mean=-0.011, residual t=-0.36
- baseline_relational_norm: n=120, residual mean=+0.002, residual t=+0.04
- recognized_reliance_on_disclosure: n=40, residual mean=+0.025, residual t=+0.26
- good_faith_relationship_maintenance: n=20, residual mean=+0.025, residual t=+0.20
- established_joint_practice: n=80, residual mean=+0.037, residual t=+0.69
- fair_notice_of_expectations: n=20, residual mean=+0.075, residual t=+0.42
- need_responsive_relational_duty: n=60, residual mean=+0.096, residual t=+1.45

Most sources' effects shrink toward ~0 and lose significance once the family mean is removed -- i.e. most of the apparent obligation_source effect above **is** the family/domain effect, not something independent of it. The one partial exception: `contribution_based_reciprocity` keeps a negative residual (t~-1.9, marginal) even after removing family means, and is the lowest- or near-lowest-bias source within its own family in 5 of 6 families where it co-occurs with another source (see per-family breakdown in `analysis/fault_rating_bias_findings.md`) -- suggestive of a real, modest, family-independent damping effect for transactional/reciprocity-framed obligations, but not strong enough to treat as confirmed on its own (small per-cell n, no multiple-comparison correction applied here).

### Within-family obligation_source breakdown (families with >=2 sources)

- **Emotional labor**:
  - need_responsive_relational_duty: n=20, diff=+0.100, t=+1.00
  - baseline_relational_norm: n=20, diff=+0.100, t=+1.00
  - recognized_reliance_on_disclosure: n=20, diff=+0.100, t=+1.00
  - contribution_based_reciprocity: n=20, diff=+0.000, t=+0.00
- **Household labor**:
  - established_joint_practice: n=20, diff=+0.250, t=+2.52
  - accepted_role_responsibility: n=40, diff=+0.200, t=+2.45
  - contribution_based_reciprocity: n=20, diff=+0.100, t=+1.00
- **Childcare**:
  - established_joint_practice: n=20, diff=+0.200, t=+1.45
  - accepted_role_responsibility: n=40, diff=+0.125, t=+1.96
  - contribution_based_reciprocity: n=20, diff=+0.000, t=+0.00
- **Mental load**:
  - need_responsive_relational_duty: n=20, diff=+0.300, t=+2.04
  - accepted_role_responsibility: n=20, diff=+0.150, t=+1.14
  - established_joint_practice: n=20, diff=+0.050, t=+0.57
  - contribution_based_reciprocity: n=20, diff=+0.000, t=+0.00
- **Financial provision**:
  - established_joint_practice: n=20, diff=+0.150, t=+1.37
  - contribution_based_reciprocity: n=20, diff=+0.100, t=+1.45
  - accepted_role_responsibility: n=40, diff=+0.025, t=+0.30
- **Jealousy/possessiveness**:
  - recognized_reliance_on_disclosure: n=20, diff=+0.300, t=+1.83
  - baseline_relational_norm: n=60, diff=+0.267, t=+3.13
- **Sexuality & Intimacy**:
  - fair_notice_of_expectations: n=20, diff=+0.300, t=+1.67
  - good_faith_relationship_maintenance: n=20, diff=+0.250, t=+2.03
  - contribution_based_reciprocity: n=20, diff=+0.200, t=+1.71
  - baseline_relational_norm: n=20, diff=+0.150, t=+1.83
- **Career sacrifice**:
  - need_responsive_relational_duty: n=20, diff=+0.200, t=+2.18
  - contribution_based_reciprocity: n=20, diff=+0.100, t=+1.00
  - accepted_role_responsibility: n=40, diff=+0.075, t=+1.14
- **Family obligations**:
  - baseline_relational_norm: n=20, diff=+0.200, t=+1.71
  - accepted_role_responsibility: n=40, diff=+0.100, t=+1.43
  - contribution_based_reciprocity: n=20, diff=+0.050, t=+1.00

## Secondary finding: partner (victim) gender effect

partner=M mean=5.074, partner=F mean=5.168, diff=-0.094, d=-0.112, Welch t=-2.12.

## Cross-model fault_rating agreement

- claude_sonnet vs deepseek_v3: r=0.669 (n=288)
- claude_sonnet vs gemini_flash: r=0.703 (n=288)
- claude_sonnet vs gpt5_mini: r=0.743 (n=288)
- claude_sonnet vs llama33: r=0.677 (n=288)
- deepseek_v3 vs gemini_flash: r=0.677 (n=288)
- deepseek_v3 vs gpt5_mini: r=0.680 (n=288)
- deepseek_v3 vs llama33: r=0.568 (n=288)
- gemini_flash vs gpt5_mini: r=0.706 (n=288)
- gemini_flash vs llama33: r=0.670 (n=288)
- gpt5_mini vs llama33: r=0.679 (n=288)

## Reasoning-text linguistic features: paired agent-gender effect

- agentic_rate_per100w: n=720, mean diff (M-F)=+0.0120, t=+0.48, d_z=+0.018
- communal_rate_per100w: n=720, mean diff (M-F)=+0.1251, t=+2.12, d_z=+0.079
- moral_intensity_score_per100w: n=720, mean diff (M-F)=+0.1753, t=+2.39, d_z=+0.089
- lib_mean: n=625, mean diff (M-F)=-0.0029, t=-0.11, d_z=-0.004

## Does the linguistic difference track the fault_rating gap?

Correlation between per-pair language-feature diff and per-pair fault_rating diff (both M-F), within the same matched pairs:

- agentic_rate_per100w: r=0.026 (n=720)
- communal_rate_per100w: r=0.048 (n=720)
- moral_intensity_score_per100w: r=0.102 (n=720)
- lib_mean: r=0.020 (n=625)

**Interpretation:** these correlations are all weak (|r|<0.11), and the LIB dispositional-attribution score shows essentially no gender effect at all (d_z=-0.004) despite being the theoretically best-grounded of the three linguistic dimensions. The numeric fault_rating bias does not appear to be strongly reflected in the surface linguistic markers tested here -- either the lexicon/heuristic measures are insensitive to the real signal, or the bias operates more on the quantitative scoring step than on the qualitative reasoning language, which would itself be a notable and citable finding. This is the strongest case yet for the LLM-assisted open-ended pattern discovery pass (see project_status_summary.md open items) rather than further hand-built lexicon expansion.

## Linguistic features paired agent-gender effect, BY FAMILY

Breaking the (mostly null) corpus-wide language result down by family surfaces family-specific stories the pooled numbers hide. Small per-cell n (~20-80 pairs per family per feature) and no multiple-comparison correction across the 9 families x 4 features tested here -- read these as exploratory leads, not confirmed effects.

- **Emotional labor**: agentic diff=+0.000 (t=+nan), communal diff=-0.051 (t=-0.26), moral diff=-0.263 (t=-1.14), lib diff=-0.100 (t=-0.92)
- **Household labor**: agentic diff=+0.017 (t=+0.53), communal diff=+0.075 (t=+0.44), moral diff=+0.250 (t=+1.07), lib diff=-0.035 (t=-0.47)
- **Childcare**: agentic diff=-0.024 (t=-0.79), communal diff=+0.150 (t=+1.04), moral diff=+0.450 (t=+2.26), lib diff=+0.029 (t=+0.46)
- **Mental load**: agentic diff=+0.000 (t=+nan), communal diff=-0.047 (t=-0.31), moral diff=-0.119 (t=-0.53), lib diff=+0.058 (t=+0.62)
- **Financial provision**: agentic diff=+0.018 (t=+0.27), communal diff=+0.273 (t=+1.54), moral diff=+0.238 (t=+1.75), lib diff=+0.000 (t=+0.00)
- **Jealousy/possessiveness**: agentic diff=-0.067 (t=-0.38), communal diff=+0.158 (t=+0.90), moral diff=+0.292 (t=+1.16), lib diff=-0.156 (t=-2.09)
- **Sexuality & Intimacy**: agentic diff=+0.116 (t=+2.36), communal diff=+0.471 (t=+2.35), moral diff=+0.224 (t=+0.89), lib diff=-0.062 (t=-0.59)
- **Career sacrifice**: agentic diff=+0.107 (t=+1.71), communal diff=+0.049 (t=+0.28), moral diff=+0.175 (t=+0.88), lib diff=+0.069 (t=+0.89)
- **Family obligations**: agentic diff=-0.059 (t=-0.79), communal diff=+0.048 (t=+0.25), moral diff=+0.332 (t=+1.44), lib diff=+0.110 (t=+2.12)

Two patterns stand out: **Sexuality & Intimacy** is the only family with a significant agentic-language gender gap (t=+2.4) and has by far the largest communal-language gap (t=+2.3) -- here the numeric bias comes *with* visible language differentiation, unlike the corpus-wide near-null pattern. **Jealousy/possessiveness** -- the family with the single largest numeric fault_rating bias -- shows a significant *negative* LIB effect (t=-2.1): female agents get *more* dispositional/trait-level blame language there even though male agents get the higher numeric fault_rating. That divergence (numeric bias one direction, dispositional-language bias the other) is worth its own sentence -- it could reflect jealousy being framed as a character trait when the accused is a woman ('she is insecure') vs. a situational failure when the accused is a man, independent of who gets blamed more overall.
