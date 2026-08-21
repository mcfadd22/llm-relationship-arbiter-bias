# Generalized agent-identity effect (M/F/NB) findings

Generated from `responses/confirmatory/*.csv` (n=7284 rows). Regenerate via `python scripts/analyze_agent_identity_effect.py`. Extends `analysis/fault_rating_bias_findings.md`'s core M-F paired test to the full 3x3 crossed gender design -- see this script's docstring and `docs/superpowers/specs/2026-08-21-nb-agent-identity-effect-design.md` for methodology and scope notes, including why the M-F numbers below differ from that file's headline M-F result.

## Section A: agent-identity effect, partner held constant

Pools over all three partner_gender values ({M, F, NB}); scenario x severity x model x partner_gender held constant within each pair.

**M vs F**: n=2427 pairs, mean diff (M-F)=+0.151, paired t=14.32, d_z=0.291.
Sign breakdown: 1784 ties (73.5%), M>F in 494, F>M in 149 (ratio 3.32:1, sign-test z=13.61). Diff-bias = (494 - 149) / 2427 = +0.1422.

**M vs NB**: n=2426 pairs, mean diff (M-NB)=+0.117, paired t=11.13, d_z=0.226.
Sign breakdown: 1806 ties (74.4%), M>NB in 444, NB>M in 176 (ratio 2.52:1, sign-test z=10.76). Diff-bias = (444 - 176) / 2426 = +0.1105.

**F vs NB**: n=2426 pairs, mean diff (F-NB)=-0.034, paired t=-3.36, d_z=-0.068.
Sign breakdown: 1876 ties (77.3%), F>NB in 235, NB>F in 315 (ratio 0.75:1, sign-test z=-3.41). Diff-bias = (235 - 315) / 2426 = -0.0330.

### Per-model breakdown

**M vs F**:
- gpt5_mini: n=486, diff=+0.200, t=+8.09, d_z=+0.367
- claude_sonnet: n=486, diff=+0.187, t=+8.30, d_z=+0.376
- gemini_flash: n=486, diff=+0.181, t=+7.54, d_z=+0.342
- llama33: n=486, diff=+0.107, t=+4.55, d_z=+0.206
- deepseek_v3: n=483, diff=+0.079, t=+3.51, d_z=+0.160

**M vs NB**:
- gpt5_mini: n=486, diff=+0.179, t=+6.84, d_z=+0.310
- gemini_flash: n=486, diff=+0.160, t=+6.51, d_z=+0.295
- llama33: n=486, diff=+0.105, t=+4.55, d_z=+0.206
- claude_sonnet: n=486, diff=+0.097, t=+4.68, d_z=+0.212
- deepseek_v3: n=482, diff=+0.041, t=+1.91, d_z=+0.087

**F vs NB**:
- llama33: n=486, diff=-0.002, t=-0.09, d_z=-0.004
- gemini_flash: n=486, diff=-0.021, t=-0.96, d_z=-0.044
- gpt5_mini: n=486, diff=-0.021, t=-0.83, d_z=-0.038
- deepseek_v3: n=482, diff=-0.035, t=-1.55, d_z=-0.070
- claude_sonnet: n=486, diff=-0.091, t=-4.27, d_z=-0.194

## Section B: same-identity relationships (MM/FF/NB-NB)

Scenario x severity x model held constant; agent_gender == partner_gender in both arms of each pair (the same-identity control, extended from the existing MM-FF comparison to include NB-NB).

**MM vs FF**: n=810 pairs, mean diff (MM-FF)=+0.062, paired t=3.58, d_z=0.126.
Sign breakdown: 633 ties (78.1%), MM>FF in 111, FF>MM in 66 (ratio 1.68:1, sign-test z=3.38). Diff-bias = (111 - 66) / 810 = +0.0556.

**MM vs NBNB**: n=809 pairs, mean diff (MM-NBNB)=+0.068, paired t=4.06, d_z=0.143.
Sign breakdown: 640 ties (79.1%), MM>NBNB in 109, NBNB>MM in 60 (ratio 1.82:1, sign-test z=3.77). Diff-bias = (109 - 60) / 809 = +0.0606.

**FF vs NBNB**: n=809 pairs, mean diff (FF-NBNB)=+0.005, paired t=0.28, d_z=0.010.
Sign breakdown: 619 ties (76.5%), FF>NBNB in 99, NBNB>FF in 91 (ratio 1.09:1, sign-test z=0.58). Diff-bias = (99 - 91) / 809 = +0.0099.

## Section C: omnibus tests (does identity matter beyond the pairwise contrasts?)

Cell-centered label-shuffle permutation one-way ANOVA (each cell centered on its own mean before pooling, 20000 shuffles, seed=42) -- the 3-level generalization of the paired t-tests above.

- **Section A (agent identity)**: n=2425 complete cells, F(2,7272)=174.260, permutation p=0.0000. **Agent-identity effect reaches conventional significance (p<0.05).**

- **Section B (same-identity relationships)**: n=809 complete cells, F(2,2424)=14.399, permutation p=0.0000. **Same-identity relationship effect reaches conventional significance (p<0.05).**

