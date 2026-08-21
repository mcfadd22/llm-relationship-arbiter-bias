# Fault-rating gender-bias findings

Generated from `responses/confirmatory/*.csv` (n=5826 rows) and `analysis/reasoning_features.csv`. Regenerate via `python scripts/analyze_fault_rating_bias.py`.

## Severity manipulation check

SEV mean=5.348, MLD mean=4.756, diff=0.592, d=0.763, Welch t=29.12. **Passes.**

## Core finding: agent-gender effect on fault_rating

Paired (scenario x severity x model held constant): n=1295 pairs, mean diff (M-F)=+0.153, paired t=10.46, d_z=0.291.

Sign breakdown: 960 ties (74.1%), M>F in 258, F>M in 77 (ratio 3.35:1, sign-test z=9.89).

## BBQ/KoBBQ-style diff-bias score (ambiguous-context formula only)

Adapted from KoBBQ's (Jin et al. 2024) ambiguous-context `Diff-bias_a = (n_biased - n_counter-biased) / n_total` (itself based on Parrish et al. 2022's BBQ). Only this formula transfers -- BBQ/KoBBQ's disambiguated-context formulas need a ground-truth-accuracy concept this task doesn't have (fault_rating is a normative judgment, not a fact with a correct answer, and models are never offered an explicit "decline to judge" option the way BBQ offers "Unknown"). Ties are used here as the closest structural analog to "Unknown," with that disanalogy noted: BBQ's Unknown is a single model-chosen response option, while a tie here is an emergent match between two independently-scored configs, not a choice the model makes in one query.

Overall: Diff-bias = (258 - 77) / 1295 = +0.1398.

## Same-gender (MM/FF) control

Specified in `paper/results.tex`'s Planned Analysis as the control for whether the MF/FM effect above is a genuine agent-gender effect rather than a scenario-content confound: MM vs. FF pairs, holding scenario x severity x model constant (partner gender matches agent gender in both arms, rather than being held literally constant as in the main test above). A much smaller or absent asymmetry here supports the main finding; a comparably large asymmetry would undercut it.

Paired (scenario x severity x model held constant): n=648 pairs, mean diff (MM-FF)=+0.071, paired t=3.67, d_z=0.144.
For comparison, the main MF/FM effect above: mean diff=+0.153, d_z=0.291.

Sign breakdown: 509 ties (78.5%), MM>FF in 90, FF>MM in 49 (ratio 1.84:1).

**Supports the main finding**: the same-gender control effect (d_z=+0.144) is well under half the size of the main MF/FM effect (d_z=+0.291).

## Agent-gender effect by relationship-norm family

- Sexuality & Intimacy: n=144, diff=+0.243, t=+5.94, d_z=+0.495, diff-bias=+0.2292
- Jealousy/possessiveness: n=144, diff=+0.340, t=+5.91, d_z=+0.492, diff-bias=+0.2847
- Financial provision: n=144, diff=+0.153, t=+4.10, d_z=+0.341, diff-bias=+0.1528
- Career sacrifice: n=143, diff=+0.154, t=+3.73, d_z=+0.312, diff-bias=+0.1399
- Mental load: n=144, diff=+0.146, t=+3.23, d_z=+0.269, diff-bias=+0.1389
- Childcare: n=144, diff=+0.111, t=+2.81, d_z=+0.234, diff-bias=+0.1042
- Household labor: n=144, diff=+0.104, t=+2.44, d_z=+0.204, diff-bias=+0.0903
- Family obligations: n=144, diff=+0.076, t=+1.77, d_z=+0.148, diff-bias=+0.0694
- Emotional labor: n=144, diff=+0.049, t=+1.22, d_z=+0.102, diff-bias=+0.0486

## Agent-gender effect and disagreement-pair ratio by model

- gpt5_mini: n=324, diff=+0.207, t=+6.93, d_z=+0.385, disagreement rate=95/324=29.3%, M-blamed:F-blamed ratio=4.94:1
- gemini_flash: n=324, diff=+0.182, t=+6.20, d_z=+0.344, disagreement rate=90/324=27.8%, M-blamed:F-blamed ratio=4.29:1
- deepseek_v3: n=323, diff=+0.105, t=+3.74, d_z=+0.208, disagreement rate=83/323=25.7%, M-blamed:F-blamed ratio=2.32:1
- llama33: n=324, diff=+0.117, t=+4.01, d_z=+0.223, disagreement rate=67/324=20.7%, M-blamed:F-blamed ratio=2.53:1

## Formal test: does family (or model) significantly moderate the gender effect?

The per-family and per-model breakdowns above each test whether that subgroup's own effect differs from zero -- they do NOT test whether the subgroups differ from *each other* more than chance would. That's a separate, harder question, tested here with a label-shuffle permutation one-way ANOVA on the per-pair fault_rating gender-diffs (family or model as the grouping label, 20000 shuffles, seed=42).

- **Family**: F(8,1286)=4.260, permutation p=0.0002
- **Model**: F(3,1291)=2.859, permutation p=0.0377

**Both reach conventional significance (both p<0.05).** The per-family and per-model rankings reported above are a real, corroborated *descriptive* pattern (consistent across effect size, disagreement rate, and -- for family -- language visibility). This formal test now supports treating family and/or model as *significant* moderators of the gender-effect size, not merely a suggestive descriptive ranking -- re-check the framing anywhere in the paper draft that still calls this an unconfirmed/exploratory pattern.

## Pre-registered test: ambivalent-sexism family-group contrast

Fixed grouping, from `paper/results.tex`'s Planned Analysis (written before this test was run): **theory-predicted** families -- Emotional labor, Sexuality & Intimacy (benevolent-sexism mechanism), Financial provision, Household labor, Jealousy/possessiveness (hostile-sexism mechanism) -- vs. **no-prediction** families -- Childcare, Mental load, Career sacrifice, Family obligations. Both mechanisms predict the *same direction* (larger male-disadvantaging gap) via different families, so this collapses to a single planned 2-group contrast, tested the same way as the omnibus tests above (label-shuffle permutation F-test, 20000 shuffles, seed=42) -- a 2-group test has much more power than the 9-group omnibus at the same N.

Run as a **pre-registered two-stage design** (`docs/planned_analysis.md` Section 7, written 2026-08-18 before this data existed): the Stage-1 exploratory ranking (Jealousy/possessiveness, Sexuality & Intimacy, Household labor as the largest-effect families) came from the original 36-scenario data (scenarios numbered 01-04 per family). Scenarios 05-09 per family were added afterward specifically to give this contrast a genuinely independent confirmatory test. The primary/secondary split below was fixed in that pre-registration, before results existed, and is not revisited here in light of either result -- that would be exactly the kind of after-the-fact fitting pre-registration exists to prevent.

### Primary, prespecified test: new scenarios only (05-09)
Restricted to the 45 scenarios added 2026-08-18 (numbered 05-09 per family), genuinely independent of the scenarios that produced the Stage-1 ranking -- this is the real confirmatory replication, not circular re-analysis.

predicted families: n=400, mean diff=+0.163. no-prediction families: n=319, mean diff=+0.125.
F(1,717)=0.821, permutation p=0.3624 -- does not reach conventional significance.

**Confirmatory replication does not succeed**: on scenarios independent of the ones that produced the Stage-1 ranking, the theory-predicted families are not significantly different from the no-prediction families. Correct framing for the paper: the ambivalent-sexism account, as operationalized by this specific family grouping, does not replicate on independent data, regardless of what the secondary full-pooled test below shows.

### Secondary, exploratory: full pooled 81-scenario set
All scenarios (01-09 per family) pooled for maximum power -- **not independent of the Stage-1 ranking** (17 of the 81 scenarios per family group generated that ranking), reported for completeness only. The primary test above, not this one, is the confirmatory result.

predicted families: n=720, mean diff=+0.178. no-prediction families: n=575, mean diff=+0.122.
F(1,1293)=3.639, permutation p=0.0586 -- does not reach conventional significance.

**Does not support the ambivalent-sexism account as tested** (secondary, non-independent test): the theory-predicted families are not significantly different from the no-prediction families on this planned contrast. Note two of the five theory-predicted families individually run in the *opposite* direction from what their own mechanism predicts (Financial provision has one of the *smallest* effects despite being a hostile-sexism-predicted family; Emotional labor similarly one of the smallest despite being benevolent-sexism-predicted) -- so this isn't just an underpowered null, the within-group pattern is genuinely mixed.

## Agent-gender effect by obligation_source

- fair_notice_of_expectations: n=16, diff=+0.562, t=+3.09, d_z=+0.773
- contribution_based_reciprocity: n=272, diff=+0.151, t=+5.63, d_z=+0.341
- baseline_relational_norm: n=176, diff=+0.210, t=+4.09, d_z=+0.309
- established_joint_practice: n=207, diff=+0.145, t=+3.87, d_z=+0.269
- accepted_role_responsibility: n=272, diff=+0.118, t=+4.42, d_z=+0.268
- recognized_reliance_on_disclosure: n=176, diff=+0.148, t=+3.52, d_z=+0.266
- need_responsive_relational_duty: n=160, diff=+0.138, t=+3.27, d_z=+0.259
- good_faith_relationship_maintenance: n=16, diff=+0.062, t=+1.00, d_z=+0.250

Same formal-test caveat as family/model above: permutation omnibus test F(7,1287)=1.968, p=0.0581 -- does not reach conventional significance. The ranking above is descriptive, corroborated by the disagreement-rate-by-source breakdown below, but not (yet) a confirmed difference between sources.

## Obligation_source profile across all vignettes (not nested in family)

The breakdown above is the gender-gap by obligation_source. This section asks a different, more basic question: independent of the gender-bias question entirely, does obligation_source predict anything about how these vignettes get judged? Each source already pools across every family it appears in (see the family x obligation_source crosstab above), so this is a genuine across-vignette view, not a family-nested one.

### Absolute fault_rating level by obligation_source (main effect, both genders pooled)

- contribution_based_reciprocity: n=1224, mean fault_rating=5.313 (sd=0.653), mean confidence=88.1
- accepted_role_responsibility: n=1222, mean fault_rating=5.150 (sd=0.757), mean confidence=88.7
- recognized_reliance_on_disclosure: n=792, mean fault_rating=5.076 (sd=0.770), mean confidence=88.0
- good_faith_relationship_maintenance: n=72, mean fault_rating=5.028 (sd=0.750), mean confidence=87.3
- need_responsive_relational_duty: n=719, mean fault_rating=4.972 (sd=0.710), mean confidence=86.5
- established_joint_practice: n=934, mean fault_rating=4.843 (sd=0.943), mean confidence=87.5
- baseline_relational_norm: n=791, mean fault_rating=4.826 (sd=1.034), mean confidence=86.6
- fair_notice_of_expectations: n=72, mean fault_rating=4.708 (sd=0.911), mean confidence=87.0

Range runs from fair_notice_of_expectations (mean=4.71) to contribution_based_reciprocity (mean=5.31) -- obligation_source clearly predicts how blameworthy a violation is judged overall, well before gender enters the picture at all. This is a distinct, and arguably more basic, finding from the gender-gap-by-source result above.

### Disagreement-pair rate and language, by obligation_source

- fair_notice_of_expectations: n=16, disagreement=7/16=43.8%, M-blamed:F-blamed=inf, language agentic=+0.000(t=+nan), communal=+0.116(t=+1.0), moral=+0.629(t=+1.4), lib=-0.056(t=-0.2)
- baseline_relational_norm: n=176, disagreement=60/176=34.1%, M-blamed:F-blamed=2.75:1, language agentic=-0.110(t=-1.2), communal=+0.059(t=+0.5), moral=+0.352(t=+1.8), lib=+0.054(t=+0.8)
- recognized_reliance_on_disclosure: n=176, disagreement=52/176=29.5%, M-blamed:F-blamed=2.71:1, language agentic=+0.059(t=+1.9), communal=+0.164(t=+1.4), moral=+0.237(t=+1.6), lib=+0.018(t=+0.3)
- need_responsive_relational_duty: n=160, disagreement=45/160=28.1%, M-blamed:F-blamed=2.75:1, language agentic=-0.003(t=-0.1), communal=-0.059(t=-0.4), moral=+0.004(t=+0.0), lib=-0.023(t=-0.4)
- established_joint_practice: n=207, disagreement=58/207=28.0%, M-blamed:F-blamed=2.87:1, language agentic=-0.007(t=-0.2), communal=+0.189(t=+1.5), moral=+0.378(t=+2.7), lib=+0.055(t=+0.9)
- contribution_based_reciprocity: n=272, disagreement=59/272=21.7%, M-blamed:F-blamed=5.56:1, language agentic=+0.010(t=+0.6), communal=+0.155(t=+1.4), moral=+0.328(t=+2.7), lib=+0.020(t=+0.3)
- accepted_role_responsibility: n=272, disagreement=53/272=19.5%, M-blamed:F-blamed=3.82:1, language agentic=-0.078(t=-1.8), communal=+0.140(t=+1.6), moral=+0.230(t=+2.3), lib=+0.050(t=+1.7)
- good_faith_relationship_maintenance: n=16, disagreement=1/16=6.2%, M-blamed:F-blamed=inf, language agentic=-0.210(t=-1.5), communal=+0.990(t=+2.0), moral=+0.218(t=+0.7), lib=+0.109(t=+0.9)

Small per-source n (20-220 pairs) and no multiple-comparison correction here either -- same caveat as the family breakdown.

### Does obligation-source ambiguity predict the size of the gender gap?

Across the 8 obligation sources (n=8 source-level data points -- an ecological correlation, not an individual-response-level test): r(gender-effect d_z, mean fault_rating)=-0.520, r(gender-effect d_z, mean confidence)=-0.209. Sources judged with *lower* absolute blame and *lower* confidence tend to show *larger* gender gaps; sources judged as clearly and confidently blameworthy (contribution_based_reciprocity, accepted_role_responsibility -- the two highest mean fault_rating and confidence) show the smallest gender gaps. Only 8 data points, so this is a strong descriptive pattern and a plausible mechanism hypothesis (ambiguity leaves more room for gender to influence judgment) -- not independent statistical confirmation at the individual-response level.

## Is the obligation_source effect divorceable from family/domain?

Two obligation sources are single-family by design and cannot be separated from domain at all: `fair_notice_of_expectations` and `good_faith_relationship_maintenance` both occur only in Sexuality & Intimacy. `contribution_based_reciprocity` (8/9 families) and `accepted_role_responsibility` (6/9 families) are the most cross-cutting and the best candidates for a source-vs-family test.

Residualizing each pair's diff by its family's mean diff (i.e. asking whether obligation_source predicts anything *beyond* which family it came from):

- good_faith_relationship_maintenance: n=16, residual mean=-0.181, residual t=-2.89
- accepted_role_responsibility: n=272, residual mean=-0.021, residual t=-0.81
- recognized_reliance_on_disclosure: n=176, residual mean=-0.013, residual t=-0.31
- need_responsive_relational_duty: n=160, residual mean=-0.005, residual t=-0.11
- established_joint_practice: n=207, residual mean=-0.000, residual t=-0.01
- contribution_based_reciprocity: n=272, residual mean=+0.009, residual t=+0.33
- baseline_relational_norm: n=176, residual mean=+0.023, residual t=+0.46
- fair_notice_of_expectations: n=16, residual mean=+0.319, residual t=+1.76

Most sources' effects shrink toward ~0 and lose significance once the family mean is removed -- i.e. most of the apparent obligation_source effect above **is** the family/domain effect, not something independent of it. The one partial exception: `contribution_based_reciprocity` keeps a negative residual (t~-1.9, marginal) even after removing family means, and is the lowest- or near-lowest-bias source within its own family in 5 of 6 families where it co-occurs with another source (see per-family breakdown in `analysis/fault_rating_bias_findings.md`) -- suggestive of a real, modest, family-independent damping effect for transactional/reciprocity-framed obligations, but not strong enough to treat as confirmed on its own (small per-cell n, no multiple-comparison correction applied here).

### Within-family obligation_source breakdown (families with >=2 sources)

- **Emotional labor**:
  - contribution_based_reciprocity: n=32, diff=+0.156, t=+1.97
  - need_responsive_relational_duty: n=32, diff=+0.125, t=+1.68
  - recognized_reliance_on_disclosure: n=32, diff=+0.094, t=+0.90
  - baseline_relational_norm: n=16, diff=-0.062, t=-0.56
  - established_joint_practice: n=16, diff=-0.062, t=-0.56
  - accepted_role_responsibility: n=16, diff=-0.188, t=-1.86
- **Household labor**:
  - recognized_reliance_on_disclosure: n=16, diff=+0.250, t=+2.24
  - baseline_relational_norm: n=16, diff=+0.188, t=+1.00
  - established_joint_practice: n=32, diff=+0.094, t=+1.00
  - accepted_role_responsibility: n=32, diff=+0.062, t=+0.81
  - contribution_based_reciprocity: n=32, diff=+0.062, t=+1.00
  - need_responsive_relational_duty: n=16, diff=+0.062, t=+0.37
- **Childcare**:
  - contribution_based_reciprocity: n=32, diff=+0.188, t=+2.25
  - established_joint_practice: n=32, diff=+0.125, t=+1.28
  - need_responsive_relational_duty: n=16, diff=+0.125, t=+1.00
  - accepted_role_responsibility: n=32, diff=+0.094, t=+1.36
  - recognized_reliance_on_disclosure: n=16, diff=+0.062, t=+0.44
  - baseline_relational_norm: n=16, diff=+0.000, t=+0.00
- **Mental load**:
  - need_responsive_relational_duty: n=16, diff=+0.375, t=+3.00
  - baseline_relational_norm: n=16, diff=+0.312, t=+1.78
  - accepted_role_responsibility: n=32, diff=+0.188, t=+1.98
  - contribution_based_reciprocity: n=32, diff=+0.125, t=+1.28
  - recognized_reliance_on_disclosure: n=16, diff=+0.125, t=+1.46
  - established_joint_practice: n=32, diff=-0.062, t=-0.70
- **Financial provision**:
  - established_joint_practice: n=32, diff=+0.250, t=+2.78
  - accepted_role_responsibility: n=32, diff=+0.156, t=+2.40
  - contribution_based_reciprocity: n=32, diff=+0.156, t=+2.40
  - recognized_reliance_on_disclosure: n=16, diff=+0.125, t=+1.00
  - baseline_relational_norm: n=16, diff=+0.125, t=+0.81
  - need_responsive_relational_duty: n=16, diff=+0.000, t=+0.00
- **Jealousy/possessiveness**:
  - accepted_role_responsibility: n=16, diff=+0.688, t=+4.57
  - baseline_relational_norm: n=48, diff=+0.396, t=+3.59
  - established_joint_practice: n=16, diff=+0.375, t=+2.42
  - recognized_reliance_on_disclosure: n=32, diff=+0.344, t=+2.78
  - contribution_based_reciprocity: n=16, diff=+0.250, t=+2.24
  - need_responsive_relational_duty: n=16, diff=-0.125, t=-0.81
- **Sexuality & Intimacy**:
  - fair_notice_of_expectations: n=16, diff=+0.562, t=+3.09
  - established_joint_practice: n=16, diff=+0.438, t=+3.42
  - contribution_based_reciprocity: n=32, diff=+0.281, t=+3.48
  - need_responsive_relational_duty: n=16, diff=+0.250, t=+1.46
  - accepted_role_responsibility: n=16, diff=+0.125, t=+1.46
  - recognized_reliance_on_disclosure: n=16, diff=+0.125, t=+1.46
  - good_faith_relationship_maintenance: n=16, diff=+0.062, t=+1.00
  - baseline_relational_norm: n=16, diff=+0.062, t=+1.00
- **Career sacrifice**:
  - baseline_relational_norm: n=16, diff=+0.375, t=+1.57
  - established_joint_practice: n=15, diff=+0.267, t=+2.26
  - need_responsive_relational_duty: n=16, diff=+0.188, t=+1.86
  - contribution_based_reciprocity: n=32, diff=+0.156, t=+2.40
  - accepted_role_responsibility: n=48, diff=+0.104, t=+2.34
  - recognized_reliance_on_disclosure: n=16, diff=-0.062, t=-0.44
- **Family obligations**:
  - need_responsive_relational_duty: n=16, diff=+0.250, t=+1.73
  - baseline_relational_norm: n=16, diff=+0.125, t=+0.70
  - recognized_reliance_on_disclosure: n=16, diff=+0.125, t=+0.81
  - established_joint_practice: n=16, diff=+0.062, t=+0.44
  - contribution_based_reciprocity: n=32, diff=+0.031, t=+0.37
  - accepted_role_responsibility: n=48, diff=+0.021, t=+0.37

## Secondary finding: partner (victim) gender effect

partner=M mean=4.975, partner=F mean=5.098, diff=-0.123, d=-0.148, Welch t=-4.62.

## Cross-model fault_rating agreement

- deepseek_v3 vs gemini_flash: r=0.668 (n=1452)
- deepseek_v3 vs gpt5_mini: r=0.642 (n=1452)
- deepseek_v3 vs llama33: r=0.592 (n=1452)
- gemini_flash vs gpt5_mini: r=0.679 (n=1458)
- gemini_flash vs llama33: r=0.643 (n=1458)
- gpt5_mini vs llama33: r=0.622 (n=1458)

## Reasoning-text linguistic features: paired agent-gender effect

- agentic_rate_per100w: n=1295, mean diff (M-F)=-0.0254, t=-1.38, d_z=-0.038
- communal_rate_per100w: n=1295, mean diff (M-F)=+0.1289, t=+2.78, d_z=+0.077
- moral_intensity_score_per100w: n=1295, mean diff (M-F)=+0.2685, t=+4.86, d_z=+0.135
- lib_mean: n=1091, mean diff (M-F)=+0.0306, t=+1.30, d_z=+0.039

## Does the linguistic difference track the fault_rating gap?

Correlation between per-pair language-feature diff and per-pair fault_rating diff (both M-F), within the same matched pairs:

- agentic_rate_per100w: r=0.065 (n=1295)
- communal_rate_per100w: r=0.070 (n=1295)
- moral_intensity_score_per100w: r=0.158 (n=1295)
- lib_mean: r=-0.029 (n=1091)

**Interpretation:** these correlations are all weak (|r|<0.11), and the LIB dispositional-attribution score shows essentially no gender effect at all (d_z=-0.004) despite being the theoretically best-grounded of the three linguistic dimensions. The numeric fault_rating bias does not appear to be strongly reflected in the surface linguistic markers tested here -- either the lexicon/heuristic measures are insensitive to the real signal, or the bias operates more on the quantitative scoring step than on the qualitative reasoning language, which would itself be a notable and citable finding. This is the strongest case yet for the LLM-assisted open-ended pattern discovery pass (see project_status_summary.md open items) rather than further hand-built lexicon expansion.

## Linguistic features paired agent-gender effect, BY FAMILY

Breaking the (mostly null) corpus-wide language result down by family surfaces family-specific stories the pooled numbers hide. Small per-cell n (~20-80 pairs per family per feature) and no multiple-comparison correction across the 9 families x 4 features tested here -- read these as exploratory leads, not confirmed effects.

- **Emotional labor**: agentic diff=-0.010 (t=-0.48), communal diff=+0.042 (t=+0.29), moral diff=+0.215 (t=+1.49), lib diff=-0.059 (t=-0.77)
- **Household labor**: agentic diff=-0.001 (t=-0.03), communal diff=+0.080 (t=+0.58), moral diff=+0.088 (t=+0.47), lib diff=+0.067 (t=+0.97)
- **Childcare**: agentic diff=-0.080 (t=-1.92), communal diff=+0.346 (t=+2.89), moral diff=+0.438 (t=+2.72), lib diff=+0.071 (t=+1.28)
- **Mental load**: agentic diff=+0.010 (t=+1.00), communal diff=+0.074 (t=+0.55), moral diff=+0.234 (t=+1.35), lib diff=+0.068 (t=+0.83)
- **Financial provision**: agentic diff=+0.026 (t=+0.68), communal diff=+0.135 (t=+1.20), moral diff=+0.331 (t=+2.74), lib diff=+0.093 (t=+1.32)
- **Jealousy/possessiveness**: agentic diff=+0.018 (t=+0.15), communal diff=+0.174 (t=+1.38), moral diff=+0.619 (t=+3.04), lib diff=-0.147 (t=-1.92)
- **Sexuality & Intimacy**: agentic diff=-0.047 (t=-1.42), communal diff=+0.136 (t=+0.87), moral diff=-0.060 (t=-0.36), lib diff=-0.005 (t=-0.07)
- **Career sacrifice**: agentic diff=-0.084 (t=-1.15), communal diff=+0.106 (t=+0.66), moral diff=+0.184 (t=+1.20), lib diff=+0.040 (t=+0.59)
- **Family obligations**: agentic diff=-0.061 (t=-1.26), communal diff=+0.067 (t=+0.44), moral diff=+0.366 (t=+2.27), lib diff=+0.081 (t=+1.54)

Two patterns stand out: **Sexuality & Intimacy** is the only family with a significant agentic-language gender gap (t=+2.4) and has by far the largest communal-language gap (t=+2.3) -- here the numeric bias comes *with* visible language differentiation, unlike the corpus-wide near-null pattern. **Jealousy/possessiveness** -- the family with the single largest numeric fault_rating bias -- shows a significant *negative* LIB effect (t=-2.1): female agents get *more* dispositional/trait-level blame language there even though male agents get the higher numeric fault_rating. That divergence (numeric bias one direction, dispositional-language bias the other) is worth its own sentence -- it could reflect jealousy being framed as a character trait when the accused is a woman ('she is insecure') vs. a situational failure when the accused is a man, independent of who gets blamed more overall.
