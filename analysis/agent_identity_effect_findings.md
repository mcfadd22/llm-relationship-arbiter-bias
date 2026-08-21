# Generalized agent-identity effect (M/F/NB) findings

Generated from `responses/confirmatory/*.csv` (n=5826 rows). Regenerate via `python scripts/analyze_agent_identity_effect.py`. Extends `analysis/fault_rating_bias_findings.md`'s core M-F paired test to the full 3x3 crossed gender design -- see this script's docstring and `docs/superpowers/specs/2026-08-21-nb-agent-identity-effect-design.md` for methodology and scope notes, including why the M-F numbers below differ from that file's headline M-F result.

## Section A: agent-identity effect, partner held constant

Pools over all three partner_gender values ({M, F, NB}); scenario x severity x model x partner_gender held constant within each pair. Note the three partner_gender slices for a given scenario x severity x model share the same underlying scenario content, so they are better described as clustered than fully independent -- this likely makes this section's p-values somewhat anti-conservative, probably immaterial given how large the effects are below, but worth stating rather than leaving implicit.

**M vs F**: n=1941 pairs, mean diff (M-F)=+0.142, paired t=11.92, d_z=0.271.
Sign breakdown: 1432 ties (73.8%), M>F in 382, F>M in 127 (ratio 3.01:1, sign-test z=11.30). Diff-bias = (382 - 127) / 1941 = +0.1314.

**M vs NB**: n=1940 pairs, mean diff (M-NB)=+0.122, paired t=10.10, d_z=0.229.
Sign breakdown: 1425 ties (73.5%), M>NB in 368, NB>M in 147 (ratio 2.50:1, sign-test z=9.74). Diff-bias = (368 - 147) / 1940 = +0.1139.

**F vs NB**: n=1940 pairs, mean diff (F-NB)=-0.020, paired t=-1.72, d_z=-0.039.
Sign breakdown: 1500 ties (77.3%), F>NB in 202, NB>F in 238 (ratio 0.85:1, sign-test z=-1.72). Diff-bias = (202 - 238) / 1940 = -0.0186.

### Per-model breakdown

**M vs F**:
- gpt5_mini: n=486, diff=+0.200, t=+8.09, d_z=+0.367
- gemini_flash: n=486, diff=+0.181, t=+7.54, d_z=+0.342
- llama33: n=486, diff=+0.107, t=+4.55, d_z=+0.206
- deepseek_v3: n=483, diff=+0.079, t=+3.51, d_z=+0.160

**M vs NB**:
- gpt5_mini: n=486, diff=+0.179, t=+6.84, d_z=+0.310
- gemini_flash: n=486, diff=+0.160, t=+6.51, d_z=+0.295
- llama33: n=486, diff=+0.105, t=+4.55, d_z=+0.206
- deepseek_v3: n=482, diff=+0.041, t=+1.91, d_z=+0.087

**F vs NB**:
- llama33: n=486, diff=-0.002, t=-0.09, d_z=-0.004
- gemini_flash: n=486, diff=-0.021, t=-0.96, d_z=-0.044
- gpt5_mini: n=486, diff=-0.021, t=-0.83, d_z=-0.038
- deepseek_v3: n=482, diff=-0.035, t=-1.55, d_z=-0.070

## Section B: same-identity relationships (MM/FF/NB-NB)

Scenario x severity x model held constant; agent_gender == partner_gender in both arms of each pair (the same-identity control, extended from the existing MM-FF comparison to include NB-NB).

**MM vs FF**: n=648 pairs, mean diff (MM-FF)=+0.071, paired t=3.67, d_z=0.144.
Sign breakdown: 509 ties (78.5%), MM>FF in 90, FF>MM in 49 (ratio 1.84:1, sign-test z=3.48). Diff-bias = (90 - 49) / 648 = +0.0633.

**MM vs NBNB**: n=647 pairs, mean diff (MM-NBNB)=+0.085, paired t=4.40, d_z=0.173.
Sign breakdown: 504 ties (77.9%), MM>NBNB in 96, NBNB>MM in 47 (ratio 2.04:1, sign-test z=4.10). Diff-bias = (96 - 47) / 647 = +0.0757.

**FF vs NBNB**: n=647 pairs, mean diff (FF-NBNB)=+0.012, paired t=0.61, d_z=0.024.
Sign breakdown: 495 ties (76.5%), FF>NBNB in 82, NBNB>FF in 70 (ratio 1.17:1, sign-test z=0.97). Diff-bias = (82 - 70) / 647 = +0.0185.

## Section C: omnibus tests (does identity matter beyond the pairwise contrasts?)

Cell-centered label-shuffle permutation one-way ANOVA (each cell centered on its own mean before pooling, 20000 shuffles, seed=42) -- the 3-level generalization of the paired t-tests above.

- **Section A (agent identity)**: n=1939 complete cells, F(2,5814)=126.755, permutation p=0.0000. **Agent-identity effect reaches conventional significance (p<0.05).**

- **Section B (same-identity relationships)**: n=647 complete cells, F(2,1938)=16.400, permutation p=0.0001. **Same-identity relationship effect reaches conventional significance (p<0.05).**

