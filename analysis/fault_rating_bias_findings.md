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

## Agent-gender effect by obligation_source

- good_faith_relationship_maintenance: n=20, diff=+0.250, t=+2.03, d_z=+0.454
- need_responsive_relational_duty: n=60, diff=+0.200, t=+3.01, d_z=+0.389
- fair_notice_of_expectations: n=20, diff=+0.300, t=+1.67, d_z=+0.374
- baseline_relational_norm: n=120, diff=+0.208, t=+4.05, d_z=+0.370
- established_joint_practice: n=80, diff=+0.163, t=+2.97, d_z=+0.332
- recognized_reliance_on_disclosure: n=40, diff=+0.200, t=+2.08, d_z=+0.329
- accepted_role_responsibility: n=220, diff=+0.109, t=+3.41, d_z=+0.230
- contribution_based_reciprocity: n=160, diff=+0.069, t=+2.23, d_z=+0.176

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
