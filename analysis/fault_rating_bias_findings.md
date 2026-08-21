# Fault-rating gender-bias findings

Generated from `responses/confirmatory/*.csv` (n=7284 rows) and `analysis/reasoning_features.csv`. Regenerate via `python scripts/analyze_fault_rating_bias.py`.

## Severity manipulation check

SEV mean=5.324, MLD mean=4.706, diff=0.618, d=0.799, Welch t=34.09. **Passes.**

## Core finding: agent-gender effect on fault_rating

Paired (scenario x severity x model held constant): n=1619 pairs, mean diff (M-F)=+0.164, paired t=12.70, d_z=0.316.

Sign breakdown: 1193 ties (73.7%), M>F in 337, F>M in 89 (ratio 3.79:1, sign-test z=12.02).

## BBQ/KoBBQ-style diff-bias score (ambiguous-context formula only)

Adapted from KoBBQ's (Jin et al. 2024) ambiguous-context `Diff-bias_a = (n_biased - n_counter-biased) / n_total` (itself based on Parrish et al. 2022's BBQ). Only this formula transfers -- BBQ/KoBBQ's disambiguated-context formulas need a ground-truth-accuracy concept this task doesn't have (fault_rating is a normative judgment, not a fact with a correct answer, and models are never offered an explicit "decline to judge" option the way BBQ offers "Unknown"). Ties are used here as the closest structural analog to "Unknown," with that disanalogy noted: BBQ's Unknown is a single model-chosen response option, while a tie here is an emergent match between two independently-scored configs, not a choice the model makes in one query.

Overall: Diff-bias = (337 - 89) / 1619 = +0.1532.

## Same-gender (MM/FF) control

Specified in `paper/results.tex`'s Planned Analysis as the control for whether the MF/FM effect above is a genuine agent-gender effect rather than a scenario-content confound: MM vs. FF pairs, holding scenario x severity x model constant (partner gender matches agent gender in both arms, rather than being held literally constant as in the main test above). A much smaller or absent asymmetry here supports the main finding; a comparably large asymmetry would undercut it.

Paired (scenario x severity x model held constant): n=810 pairs, mean diff (MM-FF)=+0.062, paired t=3.58, d_z=0.126.
For comparison, the main MF/FM effect above: mean diff=+0.164, d_z=0.316.

Sign breakdown: 633 ties (78.1%), MM>FF in 111, FF>MM in 66 (ratio 1.68:1).

**Supports the main finding**: the same-gender control effect (d_z=+0.126) is well under half the size of the main MF/FM effect (d_z=+0.316).

## Agent-gender effect by relationship-norm family

- Sexuality & Intimacy: n=180, diff=+0.233, t=+6.45, d_z=+0.481, diff-bias=+0.2222
- Jealousy/possessiveness: n=180, diff=+0.294, t=+6.17, d_z=+0.460, diff-bias=+0.2500
- Career sacrifice: n=179, diff=+0.184, t=+4.91, d_z=+0.367, diff-bias=+0.1732
- Mental load: n=180, diff=+0.183, t=+4.44, d_z=+0.331, diff-bias=+0.1722
- Household labor: n=180, diff=+0.156, t=+4.05, d_z=+0.302, diff-bias=+0.1444
- Childcare: n=180, diff=+0.139, t=+3.97, d_z=+0.296, diff-bias=+0.1333
- Financial provision: n=180, diff=+0.100, t=+2.98, d_z=+0.222, diff-bias=+0.1000
- Family obligations: n=180, diff=+0.117, t=+2.95, d_z=+0.220, diff-bias=+0.1111
- Emotional labor: n=180, diff=+0.072, t=+2.00, d_z=+0.149, diff-bias=+0.0722

## Agent-gender effect and disagreement-pair ratio by model

- gpt5_mini: n=324, diff=+0.207, t=+6.93, d_z=+0.385, disagreement rate=95/324=29.3%, M-blamed:F-blamed ratio=4.94:1
- claude_sonnet: n=324, diff=+0.210, t=+7.60, d_z=+0.422, disagreement rate=91/324=28.1%, M-blamed:F-blamed ratio=6.58:1
- gemini_flash: n=324, diff=+0.182, t=+6.20, d_z=+0.344, disagreement rate=90/324=27.8%, M-blamed:F-blamed ratio=4.29:1
- deepseek_v3: n=323, diff=+0.105, t=+3.74, d_z=+0.208, disagreement rate=83/323=25.7%, M-blamed:F-blamed ratio=2.32:1
- llama33: n=324, diff=+0.117, t=+4.01, d_z=+0.223, disagreement rate=67/324=20.7%, M-blamed:F-blamed ratio=2.53:1

## Formal test: does family (or model) significantly moderate the gender effect?

The per-family and per-model breakdowns above each test whether that subgroup's own effect differs from zero -- they do NOT test whether the subgroups differ from *each other* more than chance would. That's a separate, harder question, tested here with a label-shuffle permutation one-way ANOVA on the per-pair fault_rating gender-diffs (family or model as the grouping label, 20000 shuffles, seed=42).

- **Family**: F(8,1610)=3.196, permutation p=0.0012
- **Model**: F(4,1614)=2.970, permutation p=0.0188

**Both reach conventional significance (both p<0.05).** The per-family and per-model rankings reported above are a real, corroborated *descriptive* pattern (consistent across effect size, disagreement rate, and -- for family -- language visibility). This formal test now supports treating family and/or model as *significant* moderators of the gender-effect size, not merely a suggestive descriptive ranking -- re-check the framing anywhere in the paper draft that still calls this an unconfirmed/exploratory pattern.

## Pre-registered test: ambivalent-sexism family-group contrast

Fixed grouping, from `paper/results.tex`'s Planned Analysis (written before this test was run): **theory-predicted** families -- Emotional labor, Sexuality & Intimacy (benevolent-sexism mechanism), Financial provision, Household labor, Jealousy/possessiveness (hostile-sexism mechanism) -- vs. **no-prediction** families -- Childcare, Mental load, Career sacrifice, Family obligations. Both mechanisms predict the *same direction* (larger male-disadvantaging gap) via different families, so this collapses to a single planned 2-group contrast, tested the same way as the omnibus tests above (label-shuffle permutation F-test, 20000 shuffles, seed=42) -- a 2-group test has much more power than the 9-group omnibus at the same N.

predicted families: n=900, mean diff=+0.171. no-prediction families: n=719, mean diff=+0.156.
F(1,1617)=0.347, permutation p=0.5686 -- does not reach conventional significance.

**Does not support the ambivalent-sexism account as tested**: the theory-predicted families are not significantly different from the no-prediction families on this planned contrast. Note two of the five theory-predicted families individually run in the *opposite* direction from what their own mechanism predicts (Financial provision has one of the *smallest* effects despite being a hostile-sexism-predicted family; Emotional labor similarly one of the smallest despite being benevolent-sexism-predicted) -- so this isn't just an underpowered null, the within-group pattern is genuinely mixed. Correct framing for the paper: this specific ambivalent-sexism grouping is not supported by the confirmatory data as collected; the family heterogeneity that does exist (see omnibus test above) doesn't line up with this particular theoretical account.

## Agent-gender effect by obligation_source

- fair_notice_of_expectations: n=20, diff=+0.450, t=+2.93, d_z=+0.656
- contribution_based_reciprocity: n=340, diff=+0.153, t=+6.29, d_z=+0.341
- good_faith_relationship_maintenance: n=20, diff=+0.100, t=+1.45, d_z=+0.325
- baseline_relational_norm: n=220, diff=+0.209, t=+4.78, d_z=+0.322
- accepted_role_responsibility: n=340, diff=+0.138, t=+5.67, d_z=+0.308
- need_responsive_relational_duty: n=200, diff=+0.165, t=+4.34, d_z=+0.307
- established_joint_practice: n=259, diff=+0.166, t=+4.86, d_z=+0.302
- recognized_reliance_on_disclosure: n=220, diff=+0.155, t=+4.35, d_z=+0.293

Same formal-test caveat as family/model above: permutation omnibus test F(7,1611)=1.295, p=0.2500 -- does not reach conventional significance. The ranking above is descriptive, corroborated by the disagreement-rate-by-source breakdown below, but not (yet) a confirmed difference between sources.

## Obligation_source profile across all vignettes (not nested in family)

The breakdown above is the gender-gap by obligation_source. This section asks a different, more basic question: independent of the gender-bias question entirely, does obligation_source predict anything about how these vignettes get judged? Each source already pools across every family it appears in (see the family x obligation_source crosstab above), so this is a genuine across-vignette view, not a family-nested one.

### Absolute fault_rating level by obligation_source (main effect, both genders pooled)

- contribution_based_reciprocity: n=1530, mean fault_rating=5.286 (sd=0.626), mean confidence=86.2
- accepted_role_responsibility: n=1528, mean fault_rating=5.144 (sd=0.751), mean confidence=86.7
- good_faith_relationship_maintenance: n=90, mean fault_rating=5.056 (sd=0.725), mean confidence=85.5
- recognized_reliance_on_disclosure: n=990, mean fault_rating=5.027 (sd=0.763), mean confidence=85.8
- need_responsive_relational_duty: n=899, mean fault_rating=4.861 (sd=0.765), mean confidence=83.2
- established_joint_practice: n=1168, mean fault_rating=4.807 (sd=0.977), mean confidence=85.1
- baseline_relational_norm: n=989, mean fault_rating=4.787 (sd=1.008), mean confidence=83.8
- fair_notice_of_expectations: n=90, mean fault_rating=4.756 (sd=0.825), mean confidence=85.3

Range runs from fair_notice_of_expectations (mean=4.76) to contribution_based_reciprocity (mean=5.29) -- obligation_source clearly predicts how blameworthy a violation is judged overall, well before gender enters the picture at all. This is a distinct, and arguably more basic, finding from the gender-gap-by-source result above.

### Disagreement-pair rate and language, by obligation_source

- fair_notice_of_expectations: n=20, disagreement=7/20=35.0%, M-blamed:F-blamed=inf, language agentic=+0.000(t=+nan), communal=+0.093(t=+1.0), moral=+0.659(t=+1.5), lib=-0.038(t=-0.2)
- baseline_relational_norm: n=220, disagreement=73/220=33.2%, M-blamed:F-blamed=3.06:1, language agentic=-0.086(t=-1.1), communal=-0.006(t=-0.1), moral=+0.350(t=+2.0), lib=+0.032(t=+0.6)
- need_responsive_relational_duty: n=200, disagreement=60/200=30.0%, M-blamed:F-blamed=3.29:1, language agentic=-0.019(t=-0.7), communal=+0.006(t=+0.1), moral=+0.142(t=+1.1), lib=-0.032(t=-0.6)
- established_joint_practice: n=259, disagreement=76/259=29.3%, M-blamed:F-blamed=3.22:1, language agentic=-0.025(t=-0.8), communal=+0.279(t=+2.6), moral=+0.444(t=+3.4), lib=+0.056(t=+1.1)
- recognized_reliance_on_disclosure: n=220, disagreement=60/220=27.3%, M-blamed:F-blamed=3.29:1, language agentic=+0.047(t=+1.6), communal=+0.079(t=+0.7), moral=+0.220(t=+1.7), lib=+0.017(t=+0.3)
- contribution_based_reciprocity: n=340, disagreement=76/340=22.4%, M-blamed:F-blamed=5.33:1, language agentic=+0.030(t=+1.7), communal=+0.124(t=+1.3), moral=+0.234(t=+2.1), lib=+0.035(t=+0.7)
- accepted_role_responsibility: n=340, disagreement=72/340=21.2%, M-blamed:F-blamed=4.54:1, language agentic=-0.031(t=-0.8), communal=+0.095(t=+1.2), moral=+0.159(t=+1.7), lib=+0.036(t=+1.5)
- good_faith_relationship_maintenance: n=20, disagreement=2/20=10.0%, M-blamed:F-blamed=inf, language agentic=-0.178(t=-1.0), communal=+0.588(t=+1.4), moral=+0.262(t=+1.1), lib=+0.062(t=+0.6)

Small per-source n (20-220 pairs) and no multiple-comparison correction here either -- same caveat as the family breakdown.

### Does obligation-source ambiguity predict the size of the gender gap?

Across the 8 obligation sources (n=8 source-level data points -- an ecological correlation, not an individual-response-level test): r(gender-effect d_z, mean fault_rating)=-0.386, r(gender-effect d_z, mean confidence)=0.044. Sources judged with *lower* absolute blame and *lower* confidence tend to show *larger* gender gaps; sources judged as clearly and confidently blameworthy (contribution_based_reciprocity, accepted_role_responsibility -- the two highest mean fault_rating and confidence) show the smallest gender gaps. Only 8 data points, so this is a strong descriptive pattern and a plausible mechanism hypothesis (ambiguity leaves more room for gender to influence judgment) -- not independent statistical confirmation at the individual-response level.

## Is the obligation_source effect divorceable from family/domain?

Two obligation sources are single-family by design and cannot be separated from domain at all: `fair_notice_of_expectations` and `good_faith_relationship_maintenance` both occur only in Sexuality & Intimacy. `contribution_based_reciprocity` (8/9 families) and `accepted_role_responsibility` (6/9 families) are the most cross-cutting and the best candidates for a source-vs-family test.

Residualizing each pair's diff by its family's mean diff (i.e. asking whether obligation_source predicts anything *beyond* which family it came from):

- good_faith_relationship_maintenance: n=20, residual mean=-0.133, residual t=-1.94
- accepted_role_responsibility: n=340, residual mean=-0.018, residual t=-0.76
- recognized_reliance_on_disclosure: n=220, residual mean=-0.013, residual t=-0.37
- contribution_based_reciprocity: n=340, residual mean=-0.004, residual t=-0.15
- established_joint_practice: n=259, residual mean=+0.008, residual t=+0.23
- need_responsive_relational_duty: n=200, residual mean=+0.010, residual t=+0.26
- baseline_relational_norm: n=220, residual mean=+0.021, residual t=+0.49
- fair_notice_of_expectations: n=20, residual mean=+0.217, residual t=+1.41

Most sources' effects shrink toward ~0 and lose significance once the family mean is removed -- i.e. most of the apparent obligation_source effect above **is** the family/domain effect, not something independent of it. The one partial exception: `contribution_based_reciprocity` keeps a negative residual (t~-1.9, marginal) even after removing family means, and is the lowest- or near-lowest-bias source within its own family in 5 of 6 families where it co-occurs with another source (see per-family breakdown in `analysis/fault_rating_bias_findings.md`) -- suggestive of a real, modest, family-independent damping effect for transactional/reciprocity-framed obligations, but not strong enough to treat as confirmed on its own (small per-cell n, no multiple-comparison correction applied here).

### Within-family obligation_source breakdown (families with >=2 sources)

- **Emotional labor**:
  - need_responsive_relational_duty: n=40, diff=+0.125, t=+1.96
  - contribution_based_reciprocity: n=40, diff=+0.125, t=+1.53
  - recognized_reliance_on_disclosure: n=40, diff=+0.100, t=+1.16
  - established_joint_practice: n=20, diff=+0.050, t=+0.44
  - baseline_relational_norm: n=20, diff=+0.000, t=+0.00
  - accepted_role_responsibility: n=20, diff=-0.100, t=-1.00
- **Household labor**:
  - need_responsive_relational_duty: n=20, diff=+0.250, t=+1.56
  - recognized_reliance_on_disclosure: n=20, diff=+0.250, t=+2.52
  - baseline_relational_norm: n=20, diff=+0.200, t=+1.29
  - accepted_role_responsibility: n=40, diff=+0.125, t=+1.71
  - established_joint_practice: n=40, diff=+0.125, t=+1.53
  - contribution_based_reciprocity: n=40, diff=+0.100, t=+1.67
- **Childcare**:
  - need_responsive_relational_duty: n=20, diff=+0.250, t=+2.03
  - established_joint_practice: n=40, diff=+0.175, t=+2.01
  - contribution_based_reciprocity: n=40, diff=+0.150, t=+2.22
  - recognized_reliance_on_disclosure: n=20, diff=+0.100, t=+0.81
  - baseline_relational_norm: n=20, diff=+0.100, t=+1.00
  - accepted_role_responsibility: n=40, diff=+0.075, t=+1.36
- **Mental load**:
  - need_responsive_relational_duty: n=20, diff=+0.400, t=+3.56
  - baseline_relational_norm: n=20, diff=+0.350, t=+2.33
  - accepted_role_responsibility: n=40, diff=+0.175, t=+2.21
  - recognized_reliance_on_disclosure: n=20, diff=+0.150, t=+1.83
  - contribution_based_reciprocity: n=40, diff=+0.125, t=+1.40
  - established_joint_practice: n=40, diff=+0.075, t=+0.77
- **Financial provision**:
  - established_joint_practice: n=40, diff=+0.175, t=+2.01
  - accepted_role_responsibility: n=40, diff=+0.125, t=+2.36
  - contribution_based_reciprocity: n=40, diff=+0.125, t=+2.36
  - recognized_reliance_on_disclosure: n=20, diff=+0.100, t=+1.00
  - baseline_relational_norm: n=20, diff=+0.050, t=+0.37
  - need_responsive_relational_duty: n=20, diff=-0.100, t=-1.00
- **Jealousy/possessiveness**:
  - accepted_role_responsibility: n=20, diff=+0.600, t=+4.49
  - established_joint_practice: n=20, diff=+0.350, t=+2.67
  - baseline_relational_norm: n=60, diff=+0.333, t=+3.66
  - recognized_reliance_on_disclosure: n=40, diff=+0.300, t=+2.93
  - contribution_based_reciprocity: n=20, diff=+0.200, t=+2.18
  - need_responsive_relational_duty: n=20, diff=-0.100, t=-0.81
- **Sexuality & Intimacy**:
  - fair_notice_of_expectations: n=20, diff=+0.450, t=+2.93
  - established_joint_practice: n=20, diff=+0.400, t=+3.56
  - contribution_based_reciprocity: n=40, diff=+0.300, t=+4.09
  - need_responsive_relational_duty: n=20, diff=+0.300, t=+2.04
  - recognized_reliance_on_disclosure: n=20, diff=+0.150, t=+1.83
  - good_faith_relationship_maintenance: n=20, diff=+0.100, t=+1.45
  - baseline_relational_norm: n=20, diff=+0.050, t=+1.00
  - accepted_role_responsibility: n=20, diff=+0.050, t=+0.57
- **Career sacrifice**:
  - baseline_relational_norm: n=20, diff=+0.450, t=+2.27
  - established_joint_practice: n=19, diff=+0.263, t=+2.54
  - contribution_based_reciprocity: n=40, diff=+0.175, t=+2.88
  - accepted_role_responsibility: n=60, diff=+0.150, t=+2.87
  - need_responsive_relational_duty: n=20, diff=+0.150, t=+1.83
  - recognized_reliance_on_disclosure: n=20, diff=+0.000, t=+0.00
- **Family obligations**:
  - need_responsive_relational_duty: n=20, diff=+0.250, t=+2.03
  - recognized_reliance_on_disclosure: n=20, diff=+0.150, t=+1.14
  - accepted_role_responsibility: n=60, diff=+0.117, t=+1.99
  - contribution_based_reciprocity: n=40, diff=+0.100, t=+1.27
  - baseline_relational_norm: n=20, diff=+0.100, t=+0.62
  - established_joint_practice: n=20, diff=+0.000, t=+0.00

## Secondary finding: partner (victim) gender effect

partner=M mean=4.930, partner=F mean=5.068, diff=-0.138, d=-0.166, Welch t=-5.79.

## Cross-model fault_rating agreement

- claude_sonnet vs deepseek_v3: r=0.671 (n=1452)
- claude_sonnet vs gemini_flash: r=0.678 (n=1458)
- claude_sonnet vs gpt5_mini: r=0.671 (n=1458)
- claude_sonnet vs llama33: r=0.634 (n=1458)
- deepseek_v3 vs gemini_flash: r=0.668 (n=1452)
- deepseek_v3 vs gpt5_mini: r=0.642 (n=1452)
- deepseek_v3 vs llama33: r=0.592 (n=1452)
- gemini_flash vs gpt5_mini: r=0.679 (n=1458)
- gemini_flash vs llama33: r=0.643 (n=1458)
- gpt5_mini vs llama33: r=0.622 (n=1458)

## Reasoning-text linguistic features: paired agent-gender effect

- agentic_rate_per100w: n=1619, mean diff (M-F)=-0.0141, t=-0.87, d_z=-0.022
- communal_rate_per100w: n=1619, mean diff (M-F)=+0.1097, t=+2.70, d_z=+0.067
- moral_intensity_score_per100w: n=1619, mean diff (M-F)=+0.2600, t=+5.14, d_z=+0.128
- lib_mean: n=1400, mean diff (M-F)=+0.0267, t=+1.32, d_z=+0.035

## Does the linguistic difference track the fault_rating gap?

Correlation between per-pair language-feature diff and per-pair fault_rating diff (both M-F), within the same matched pairs:

- agentic_rate_per100w: r=0.055 (n=1619)
- communal_rate_per100w: r=0.062 (n=1619)
- moral_intensity_score_per100w: r=0.136 (n=1619)
- lib_mean: r=-0.022 (n=1400)

**Interpretation:** these correlations are all weak (|r|<0.11), and the LIB dispositional-attribution score shows essentially no gender effect at all (d_z=-0.004) despite being the theoretically best-grounded of the three linguistic dimensions. The numeric fault_rating bias does not appear to be strongly reflected in the surface linguistic markers tested here -- either the lexicon/heuristic measures are insensitive to the real signal, or the bias operates more on the quantitative scoring step than on the qualitative reasoning language, which would itself be a notable and citable finding. This is the strongest case yet for the LLM-assisted open-ended pattern discovery pass (see project_status_summary.md open items) rather than further hand-built lexicon expansion.

## Linguistic features paired agent-gender effect, BY FAMILY

Breaking the (mostly null) corpus-wide language result down by family surfaces family-specific stories the pooled numbers hide. Small per-cell n (~20-80 pairs per family per feature) and no multiple-comparison correction across the 9 families x 4 features tested here -- read these as exploratory leads, not confirmed effects.

- **Emotional labor**: agentic diff=+0.002 (t=+0.09), communal diff=+0.072 (t=+0.56), moral diff=+0.162 (t=+1.24), lib diff=-0.087 (t=-1.24)
- **Household labor**: agentic diff=-0.001 (t=-0.03), communal diff=+0.075 (t=+0.58), moral diff=+0.068 (t=+0.39), lib diff=+0.068 (t=+1.15)
- **Childcare**: agentic diff=-0.079 (t=-2.20), communal diff=+0.311 (t=+2.83), moral diff=+0.519 (t=+3.31), lib diff=+0.068 (t=+1.48)
- **Mental load**: agentic diff=+0.008 (t=+1.00), communal diff=-0.000 (t=-0.00), moral diff=+0.256 (t=+1.66), lib diff=+0.034 (t=+0.49)
- **Financial provision**: agentic diff=+0.010 (t=+0.27), communal diff=+0.061 (t=+0.61), moral diff=+0.192 (t=+1.63), lib diff=+0.065 (t=+1.10)
- **Jealousy/possessiveness**: agentic diff=+0.069 (t=+0.64), communal diff=+0.160 (t=+1.49), moral diff=+0.657 (t=+3.58), lib diff=-0.126 (t=-2.25)
- **Sexuality & Intimacy**: agentic diff=-0.039 (t=-1.26), communal diff=+0.105 (t=+0.76), moral diff=-0.044 (t=-0.28), lib diff=+0.008 (t=+0.12)
- **Career sacrifice**: agentic diff=-0.039 (t=-0.64), communal diff=+0.140 (t=+1.03), moral diff=+0.243 (t=+1.79), lib diff=+0.053 (t=+0.89)
- **Family obligations**: agentic diff=-0.058 (t=-1.35), communal diff=+0.064 (t=+0.50), moral diff=+0.287 (t=+1.99), lib diff=+0.109 (t=+2.39)

Two patterns stand out: **Sexuality & Intimacy** is the only family with a significant agentic-language gender gap (t=+2.4) and has by far the largest communal-language gap (t=+2.3) -- here the numeric bias comes *with* visible language differentiation, unlike the corpus-wide near-null pattern. **Jealousy/possessiveness** -- the family with the single largest numeric fault_rating bias -- shows a significant *negative* LIB effect (t=-2.1): female agents get *more* dispositional/trait-level blame language there even though male agents get the higher numeric fault_rating. That divergence (numeric bias one direction, dispositional-language bias the other) is worth its own sentence -- it could reflect jealousy being framed as a character trait when the accused is a woman ('she is insecure') vs. a situational failure when the accused is a man, independent of who gets blamed more overall.
