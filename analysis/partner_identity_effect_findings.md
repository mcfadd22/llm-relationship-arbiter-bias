# Partner-identity effect (M/F/NB) findings

Generated from `responses/confirmatory/*.csv` (n=5826 rows). Regenerate via `python scripts/analyze_partner_identity_effect.py`. Supersedes `analysis/fault_rating_bias_findings.md`'s older, unpaired "Secondary finding: partner (victim) gender effect" -- this is the matched (agent-gender-held-constant) version of that comparison, extended to the NB partner level. See this script's docstring and `docs/superpowers/specs/2026-08-21-partner-identity-effect-design.md` for full methodology, including why there is no NB-NB comparison below (that question is answered by `analysis/agent_identity_effect_findings.md`'s Section B instead).

## Section A: partner-identity effect, agent held constant

Pools over all three agent_gender values ({M, F, NB}); scenario x severity x model x agent_gender held constant within each pair. Note the three agent_gender slices for a given scenario x severity x model share the same underlying scenario content, so they are better described as clustered than fully independent -- this likely makes this section's p-values somewhat anti-conservative, worth stating rather than leaving implicit.

**M vs F**: n=1942 pairs, mean diff (M-F)=-0.123, paired t=-10.46, d_z=-0.237.
Sign breakdown: 1462 ties (75.3%), M>F in 130, F>M in 350 (ratio 0.37:1, sign-test z=-10.04). Diff-bias = (130 - 350) / 1942 = -0.1133.

**M vs NB**: n=1939 pairs, mean diff (M-NB)=-0.107, paired t=-8.91, d_z=-0.202.
Sign breakdown: 1457 ties (75.1%), M>NB in 147, NB>M in 335 (ratio 0.44:1, sign-test z=-8.56). Diff-bias = (147 - 335) / 1939 = -0.0970.

**F vs NB**: n=1939 pairs, mean diff (F-NB)=+0.017, paired t=1.49, d_z=0.034.
Sign breakdown: 1496 ties (77.2%), F>NB in 238, NB>F in 205 (ratio 1.16:1, sign-test z=1.57). Diff-bias = (238 - 205) / 1939 = +0.0170.

### Per-model breakdown

**M vs F**:
- deepseek_v3: n=484, diff=-0.089, t=-3.87, d_z=-0.176
- llama33: n=486, diff=-0.093, t=-4.12, d_z=-0.187
- gemini_flash: n=486, diff=-0.126, t=-5.24, d_z=-0.238
- gpt5_mini: n=486, diff=-0.185, t=-7.56, d_z=-0.343

**M vs NB**:
- llama33: n=486, diff=-0.078, t=-3.54, d_z=-0.161
- deepseek_v3: n=481, diff=-0.089, t=-3.84, d_z=-0.175
- gpt5_mini: n=486, diff=-0.128, t=-4.93, d_z=-0.223
- gemini_flash: n=486, diff=-0.132, t=-5.41, d_z=-0.245

**F vs NB**:
- gpt5_mini: n=486, diff=+0.058, t=+2.43, d_z=+0.110
- llama33: n=486, diff=+0.014, t=+0.65, d_z=+0.029
- deepseek_v3: n=481, diff=+0.002, t=+0.09, d_z=+0.004
- gemini_flash: n=486, diff=-0.006, t=-0.26, d_z=-0.012

## Section B: omnibus test (does partner identity matter beyond the pairwise contrasts?)

Cell-centered, within-cell label-shuffle permutation one-way ANOVA (each cell centered on its own mean before pooling, 20000 shuffles restricted to within-cell label reassignment, seed=42) -- the 3-level generalization of the paired t-tests above; see this script's docstring for why the permutation must be within-cell, not global.

- **Section A (partner identity)**: n=1938 complete cells, F(2,5811)=98.110, permutation p=0.0000. **Partner-identity effect reaches conventional significance (p<0.05).**

## Why there is no NB-NB comparison in this script

This script's pairwise tests are contrasts *between different values* of partner gender (M vs F, M vs NB, F vs NB), each held against a fixed agent gender -- there is no meaningful "NB vs NB" version of that contrast, since comparing a category against itself isn't a difference test. "NB-NB" as a concept refers to a different question -- *both* agent and partner being NB together, a same-identity relationship-type question, not a partner-identity-holding-agent-constant question -- and that question is already answered by `analysis/agent_identity_effect_findings.md`'s Section B (NB-NB vs MM vs FF). Conflating the two would repeat the mistake `docs/planned_analysis.md` Section 5 explicitly warns against for the presumed-orientation analyses.

