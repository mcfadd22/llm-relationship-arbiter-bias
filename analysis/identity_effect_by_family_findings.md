# Identity effects by relationship-norm family findings

Generated from `responses/confirmatory/*.csv` (n=5826 rows). Regenerate via `python scripts/analyze_identity_effect_by_family.py`. Adds a per-family breakdown to all 9 comparisons across items 2/3/4 (`analysis/agent_identity_effect_findings.md`, `analysis/partner_identity_effect_findings.md`), none of which have one yet. See this script's docstring and `docs/superpowers/specs/2026-08-21-identity-effect-by-family-design.md` for full methodology.

## Reference: binary M-F agent-gender effect by family

Recomputed here (not imported) to guarantee the synthesis section below always compares against a live number, not a hardcoded one that could go stale. Matches `analysis/fault_rating_bias_findings.md`'s existing per-family breakdown.

### M vs F

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Jealousy/possessiveness | 144 | +0.340 | +5.91 | +0.492 | +0.2847 |
| Sexuality & Intimacy | 144 | +0.243 | +5.94 | +0.495 | +0.2292 |
| Career sacrifice | 143 | +0.154 | +3.73 | +0.312 | +0.1399 |
| Financial provision | 144 | +0.153 | +4.10 | +0.341 | +0.1528 |
| Mental load | 144 | +0.146 | +3.23 | +0.269 | +0.1389 |
| Childcare | 144 | +0.111 | +2.81 | +0.234 | +0.1042 |
| Household labor | 144 | +0.104 | +2.44 | +0.204 | +0.0903 |
| Family obligations | 144 | +0.076 | +1.77 | +0.148 | +0.0694 |
| Emotional labor | 144 | +0.049 | +1.22 | +0.102 | +0.0486 |

Family moderation test: F(8,1286)=4.260, permutation p=0.0002 -- reaches conventional significance.

## Axis 1: agent-identity effect by family (item 2, partner held constant)

### M vs F

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Jealousy/possessiveness | 216 | +0.282 | +6.28 | +0.428 | +0.2454 |
| Sexuality & Intimacy | 216 | +0.190 | +5.50 | +0.375 | +0.1759 |
| Career sacrifice | 215 | +0.186 | +5.61 | +0.383 | +0.1767 |
| Mental load | 216 | +0.167 | +4.64 | +0.315 | +0.1620 |
| Household labor | 216 | +0.120 | +3.27 | +0.223 | +0.1065 |
| Childcare | 215 | +0.112 | +3.48 | +0.237 | +0.1070 |
| Financial provision | 216 | +0.088 | +2.76 | +0.187 | +0.0880 |
| Family obligations | 215 | +0.070 | +1.97 | +0.134 | +0.0605 |
| Emotional labor | 216 | +0.060 | +1.87 | +0.127 | +0.0602 |

Family moderation test: F(8,1932)=4.061, permutation p=0.0001 -- reaches conventional significance.

### M vs NB

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Jealousy/possessiveness | 215 | +0.223 | +4.91 | +0.335 | +0.1953 |
| Sexuality & Intimacy | 215 | +0.177 | +5.01 | +0.342 | +0.1674 |
| Career sacrifice | 216 | +0.153 | +4.40 | +0.299 | +0.1389 |
| Mental load | 216 | +0.139 | +3.44 | +0.234 | +0.1250 |
| Household labor | 216 | +0.125 | +3.68 | +0.250 | +0.1204 |
| Childcare | 215 | +0.098 | +2.88 | +0.196 | +0.1023 |
| Emotional labor | 216 | +0.074 | +2.44 | +0.166 | +0.0741 |
| Family obligations | 215 | +0.065 | +1.88 | +0.128 | +0.0605 |
| Financial provision | 216 | +0.042 | +1.26 | +0.086 | +0.0417 |

Family moderation test: F(8,1931)=2.608, permutation p=0.0080 -- reaches conventional significance.

### F vs NB

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Emotional labor | 216 | +0.014 | +0.47 | +0.032 | +0.0139 |
| Household labor | 216 | +0.005 | +0.14 | +0.010 | +0.0139 |
| Family obligations | 215 | -0.005 | -0.15 | -0.010 | -0.0047 |
| Childcare | 216 | -0.014 | -0.44 | -0.030 | -0.0139 |
| Sexuality & Intimacy | 215 | -0.014 | -0.39 | -0.027 | -0.0093 |
| Mental load | 216 | -0.028 | -0.71 | -0.048 | -0.0370 |
| Career sacrifice | 215 | -0.033 | -1.04 | -0.071 | -0.0326 |
| Financial provision | 216 | -0.046 | -1.55 | -0.105 | -0.0417 |
| Jealousy/possessiveness | 215 | -0.056 | -1.30 | -0.088 | -0.0558 |

Family moderation test: F(8,1931)=0.455, permutation p=0.8853 -- does not reach conventional significance.

## Axis 2: partner-identity effect by family (item 3, agent held constant)

### M vs F

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Financial provision | 216 | +0.000 | +0.00 | +0.000 | +0.0000 |
| Family obligations | 216 | -0.060 | -1.87 | -0.127 | -0.0602 |
| Emotional labor | 216 | -0.088 | -2.60 | -0.177 | -0.0880 |
| Childcare | 216 | -0.125 | -3.68 | -0.250 | -0.1204 |
| Household labor | 216 | -0.144 | -4.35 | -0.296 | -0.1296 |
| Mental load | 216 | -0.148 | -3.68 | -0.250 | -0.1389 |
| Jealousy/possessiveness | 216 | -0.181 | -4.41 | -0.300 | -0.1481 |
| Sexuality & Intimacy | 215 | -0.181 | -5.51 | -0.376 | -0.1721 |
| Career sacrifice | 215 | -0.181 | -5.03 | -0.343 | -0.1628 |

Family moderation test: F(8,1933)=3.190, permutation p=0.0019 -- reaches conventional significance.

### M vs NB

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Financial provision | 216 | -0.023 | -0.78 | -0.053 | -0.0231 |
| Family obligations | 214 | -0.056 | -1.67 | -0.114 | -0.0514 |
| Childcare | 215 | -0.070 | -2.12 | -0.144 | -0.0651 |
| Emotional labor | 216 | -0.083 | -2.63 | -0.179 | -0.0880 |
| Household labor | 216 | -0.097 | -3.12 | -0.213 | -0.0972 |
| Sexuality & Intimacy | 216 | -0.134 | -3.83 | -0.261 | -0.1296 |
| Career sacrifice | 215 | -0.135 | -3.70 | -0.252 | -0.1163 |
| Mental load | 216 | -0.144 | -3.40 | -0.232 | -0.1250 |
| Jealousy/possessiveness | 215 | -0.219 | -4.72 | -0.322 | -0.1767 |

Family moderation test: F(8,1930)=2.628, permutation p=0.0074 -- reaches conventional significance.

### F vs NB

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Childcare | 215 | +0.056 | +1.82 | +0.124 | +0.0558 |
| Sexuality & Intimacy | 215 | +0.047 | +1.27 | +0.087 | +0.0326 |
| Household labor | 216 | +0.046 | +1.34 | +0.091 | +0.0463 |
| Career sacrifice | 216 | +0.046 | +1.55 | +0.105 | +0.0463 |
| Family obligations | 214 | +0.005 | +0.15 | +0.010 | +0.0047 |
| Emotional labor | 216 | +0.005 | +0.15 | +0.010 | +0.0046 |
| Mental load | 216 | +0.005 | +0.11 | +0.008 | +0.0139 |
| Financial provision | 216 | -0.023 | -0.76 | -0.052 | -0.0231 |
| Jealousy/possessiveness | 215 | -0.033 | -0.79 | -0.054 | -0.0279 |

Family moderation test: F(8,1930)=0.913, permutation p=0.5075 -- does not reach conventional significance.

## Axis 3: same-identity relationships by family (item 4)

### MM vs FF

*Power note: same-identity cells don't pool across a third held-constant role the way Axes 1-2 do, so per-family n here is meaningfully thinner (~68-75/family vs. ~210-220/family for Axes 1-2) -- likely underpowered for a full 9-way split. Reported descriptively, not as a confirmatory claim.*

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Jealousy/possessiveness | 72 | +0.194 | +2.77 | +0.326 | +0.1667 |
| Financial provision | 72 | +0.153 | +2.49 | +0.293 | +0.1389 |
| Sexuality & Intimacy | 72 | +0.097 | +1.98 | +0.233 | +0.0972 |
| Family obligations | 72 | +0.083 | +1.62 | +0.191 | +0.0833 |
| Childcare | 72 | +0.056 | +1.00 | +0.118 | +0.0694 |
| Mental load | 72 | +0.056 | +0.75 | +0.089 | +0.0278 |
| Career sacrifice | 72 | +0.028 | +0.70 | +0.083 | +0.0278 |
| Emotional labor | 72 | +0.000 | +0.00 | +0.000 | +0.0000 |
| Household labor | 72 | -0.028 | -0.47 | -0.055 | -0.0417 |

Family moderation test: F(8,639)=1.492, permutation p=0.1607 -- does not reach conventional significance.

### MM vs NBNB

*Power note: same-identity cells don't pool across a third held-constant role the way Axes 1-2 do, so per-family n here is meaningfully thinner (~68-75/family vs. ~210-220/family for Axes 1-2) -- likely underpowered for a full 9-way split. Reported descriptively, not as a confirmatory claim.*

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Sexuality & Intimacy | 72 | +0.139 | +2.00 | +0.236 | +0.1250 |
| Jealousy/possessiveness | 71 | +0.113 | +1.82 | +0.216 | +0.0986 |
| Career sacrifice | 72 | +0.111 | +2.04 | +0.241 | +0.1111 |
| Childcare | 72 | +0.097 | +1.84 | +0.216 | +0.0972 |
| Household labor | 72 | +0.083 | +1.51 | +0.178 | +0.0833 |
| Financial provision | 72 | +0.069 | +1.22 | +0.143 | +0.0694 |
| Mental load | 72 | +0.056 | +0.78 | +0.092 | +0.0139 |
| Family obligations | 72 | +0.056 | +1.16 | +0.136 | +0.0556 |
| Emotional labor | 72 | +0.042 | +0.83 | +0.098 | +0.0278 |

Family moderation test: F(8,638)=0.308, permutation p=0.9654 -- does not reach conventional significance.

### FF vs NBNB

*Power note: same-identity cells don't pool across a third held-constant role the way Axes 1-2 do, so per-family n here is meaningfully thinner (~68-75/family vs. ~210-220/family for Axes 1-2) -- likely underpowered for a full 9-way split. Reported descriptively, not as a confirmatory claim.*

| Family | n | mean diff | t | d_z | diff-bias |
|---|---|---|---|---|---|
| Household labor | 72 | +0.111 | +1.73 | +0.204 | +0.1250 |
| Career sacrifice | 72 | +0.083 | +1.62 | +0.191 | +0.0833 |
| Emotional labor | 72 | +0.042 | +1.00 | +0.118 | +0.0417 |
| Childcare | 72 | +0.042 | +0.73 | +0.085 | +0.0417 |
| Sexuality & Intimacy | 72 | +0.042 | +0.62 | +0.073 | +0.0278 |
| Mental load | 72 | +0.000 | +0.00 | +0.000 | +0.0417 |
| Family obligations | 72 | -0.028 | -0.70 | -0.083 | -0.0278 |
| Financial provision | 72 | -0.083 | -1.28 | -0.151 | -0.0833 |
| Jealousy/possessiveness | 71 | -0.099 | -1.41 | -0.167 | -0.0845 |

Family moderation test: F(8,638)=1.374, permutation p=0.2051 -- does not reach conventional significance.

## Synthesis: does the NB-related bias concentrate in the same domains as the binary bias?

Reference top-3 families by binary M-F effect size: Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice.

| Comparison | Spearman rank correlation vs. reference | Top-3 families | Top-3 overlap with reference |
|---|---|---|---|
| Agent-identity M vs F | +0.883 | Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice | 3/3 |
| Agent-identity M vs NB | +0.717 | Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice | 3/3 |
| Agent-identity F vs NB | -0.867 | Emotional labor, Household labor, Family obligations | 0/3 |
| Partner-identity M vs F | -0.667 | Financial provision, Family obligations, Emotional labor | 0/3 |
| Partner-identity M vs NB | -0.567 | Financial provision, Family obligations, Childcare | 0/3 |
| Partner-identity F vs NB | -0.133 | Childcare, Sexuality & Intimacy, Household labor | 1/3 |
| Same-identity MM vs FF | +0.633 | Jealousy/possessiveness, Financial provision, Sexuality & Intimacy | 2/3 |
| Same-identity MM vs NBNB | +0.800 | Sexuality & Intimacy, Jealousy/possessiveness, Career sacrifice | 3/3 |
| Same-identity FF vs NBNB | -0.350 | Household labor, Career sacrifice, Emotional labor | 1/3 |

**Interpretation guidance**: a high positive Spearman correlation and substantial top-3 overlap would suggest the NB-related and binary biases share a common underlying domain-sensitivity mechanism; low or negative correlation would suggest the NB-related bias has its own, distinct pattern across relationship domains, not explained by "wherever the binary bias is big, the NB bias is too."

