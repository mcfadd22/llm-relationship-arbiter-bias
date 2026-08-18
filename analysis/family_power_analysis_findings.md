# Family-omnibus power analysis and ranking-stability check

Generated from `responses/confirmatory/*.csv` (720 pairs, 9 families, current n=80 pairs/family, grand mean diff=+0.144). Regenerate via `python scripts/family_omnibus_power_analysis.py`.

Motivated by: should new scenario-writing effort for the next data-collection round target the families that currently show the largest gender-fault gap (Jealousy/possessiveness, Sexuality & Intimacy, Household labor), or be spread evenly across all 9 families? Two questions, answered separately below: (1) is the current top-3 ranking itself stable, or could it be noise from n=80/family; (2) at a given added-scenario budget, does concentrating in the top-3 reach adequate omnibus power any faster than spreading evenly?

## 1. Is the top-3 ranking stable, or likely noise?

Nonparametric bootstrap (resample each family's own 80 diffs with replacement, 3000 replicates), tracking how often each family lands in the bootstrap top-3 by mean diff, and its average rank (1=largest gap).

| Family | Observed mean diff | P(bootstrap top-3) | Mean bootstrap rank |
|---|---|---|---|
| Jealousy/possessiveness | +0.275 | 0.93 | 1.68 |
| Sexuality & Intimacy | +0.225 | 0.82 | 2.51 |
| Household labor | +0.188 | 0.69 | 3.15 |
| Mental load | +0.125 | 0.21 | 5.36 |
| Career sacrifice | +0.113 | 0.08 | 6.00 |
| Childcare | +0.113 | 0.13 | 5.75 |
| Family obligations | +0.113 | 0.08 | 6.13 |
| Emotional labor | +0.075 | 0.03 | 7.11 |
| Financial provision | +0.075 | 0.03 | 7.28 |

**Not pure noise.** Jealousy/possessiveness (93% of resamples land in the top-3), Sexuality & Intimacy (82%), and Household labor (69%, occasionally displaced by Mental load at 20%) form a reasonably stable cluster distinct from the other 6 families (all <=20% top-3 rate). This is *internal* stability within the existing 720 pairs, not independent replication -- it says the pattern isn't an artifact of a single unlucky draw, not that it will necessarily hold on genuinely new data.

## 2. Omnibus power: even vs. concentrated allocation of new scenarios

Simulated (nonparametric bootstrap, null-calibrated critical F at each sample size, matching this project's existing permutation-test approach rather than a parametric F-table) under two truth assumptions: **optimistic** (today's per-family means/variances are exactly correct) and **shrunk** (only half the observed between-family spread is real signal, the rest is n=80 sampling noise -- a conservative check, motivated by 3 families currently sharing the identical rounded diff +0.113). **Even** = new scenarios split equally across all 9 families. **Concentrated** = same total scenario budget, all routed to the 3 top-ranked families above.

| extra scenarios/family (even) | total N/family | even, optimistic | even, shrunk | concentrated, optimistic | concentrated, shrunk |
|---|---|---|---|---|---|
| +0 | 80 | 0.68 | 0.67 | 0.67 | 0.66 |
| +2 | 120 | 0.85 | 0.85 | 0.85 | 0.85 |
| +4 | 160 | 0.94 | 0.95 | 0.92 | 0.92 |
| +6 | 200 | 0.98 | 0.98 | 0.95 | 0.96 |
| +8 | 240 | 0.99 | 0.99 | 0.97 | 0.98 |
| +10 | 280 | 1.00 | 1.00 | 0.99 | 0.98 |
| +14 | 360 | 1.00 | 1.00 | 0.99 | 0.99 |

**Reading this table:** current baseline (n=80/family, +0 row) achieves only ~65-67% power even under the optimistic assumption that today's estimates are exactly true -- so the actual observed non-significant omnibus result (p=0.135) is a plausible, not-even-that-unlucky draw, not evidence the effect is absent. Concentrated allocation is **not much less efficient than even allocation for the omnibus test itself** at moderate budgets (+2 to +4 scenarios/family-equivalent) -- the F-test is disproportionately driven by families furthest from the grand mean, so concentrating there sharpens exactly the signal the test needs. Even allocation pulls further ahead (asymptoting to ~100% vs. concentrated's ~97-99%) only at larger budgets.

**This does not mean concentrating is free of downsides.** Reaching omnibus significance is not the only goal -- a deployment-risk "map" needs confidently-estimated *low*-risk domains too, not just confirmation that the high ones are high. Concentrating leaves the other 6 families at n=80 indefinitely, so the paper could show 3 domains are elevated but couldn't say the rest are *not*, with any real precision. There's also a disclosure problem: the top-3 selection comes from the same data used to test it, which is exactly the kind of circularity a reviewer will flag even though the ranking itself looks internally stable (Section 1).

**Recommendation:** add a meaningful number of new scenarios to *every* family (this analysis suggests +4 to +6/family gets to ~94-98% power under either truth assumption, even allocation), so every domain -- not just the top 3 -- ends up well-estimated. If there's appetite to also specifically nail down the top-3 pattern, treat it as a disclosed two-stage design: the current ranking is the Stage-1 exploratory hypothesis, and the new scenarios (across all families) are the Stage-2 confirmatory test of whether that same ranking re-emerges on fresh, independent scenario content -- not "add more data until the domains that already look big become significant."

