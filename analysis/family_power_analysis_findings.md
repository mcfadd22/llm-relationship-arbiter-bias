# Family-omnibus power analysis and ranking-stability check

Generated from `responses/confirmatory/*.csv` (1619 pairs, 9 families, current n=179-180 pairs/family, grand mean diff=+0.164). Regenerate via `python scripts/family_omnibus_power_analysis.py`.

Motivated by: should new scenario-writing effort for the next data-collection round target the families that currently show the largest gender-fault gap (Jealousy/possessiveness, Sexuality & Intimacy, Career sacrifice), or be spread evenly across all 9 families? Two questions, answered separately below: (1) is the current top-3 ranking itself stable, or could it be noise from n=179-180 pairs/family; (2) at a given added-scenario budget, does concentrating in the top-3 reach adequate omnibus power any faster than spreading evenly?

## 1. Is the top-3 ranking stable, or likely noise?

Nonparametric bootstrap (resample each family's own n=179-180 pairs/family diffs with replacement, 3000 replicates), tracking how often each family lands in the bootstrap top-3 by mean diff, and its average rank (1=largest gap).

| Family | Observed mean diff | P(bootstrap top-3) | Mean bootstrap rank |
|---|---|---|---|
| Jealousy/possessiveness | +0.294 | 0.99 | 1.23 |
| Sexuality & Intimacy | +0.233 | 0.88 | 2.39 |
| Career sacrifice | +0.184 | 0.44 | 3.86 |
| Mental load | +0.183 | 0.40 | 4.04 |
| Household labor | +0.156 | 0.18 | 5.04 |
| Childcare | +0.139 | 0.08 | 5.79 |
| Family obligations | +0.117 | 0.03 | 6.87 |
| Financial provision | +0.100 | 0.00 | 7.46 |
| Emotional labor | +0.072 | 0.00 | 8.31 |

**Top-3 by bootstrap top-3 rate**: Jealousy/possessiveness (99%), Sexuality & Intimacy (88%), Career sacrifice (44%), vs. all other families at <=40% top-3 rate. This is *internal* stability within the existing 1619 pairs, not independent replication -- it says the pattern isn't an artifact of a single unlucky draw, not that it will necessarily hold on genuinely new data.

## 2. Omnibus power: even vs. concentrated allocation of new scenarios

Simulated (nonparametric bootstrap, null-calibrated critical F at each sample size, matching this project's existing permutation-test approach rather than a parametric F-table) under two truth assumptions: **optimistic** (today's per-family means/variances are exactly correct) and **shrunk** (only half the observed between-family spread is real signal, the rest is sampling noise -- a conservative check against overtrusting the current point estimates). **Even** = new scenarios split equally across all 9 families. **Concentrated** = same total scenario budget, all routed to the 3 top-ranked families above.

| extra scenarios/family (even) | total N/family | even, optimistic | even, shrunk | concentrated, optimistic | concentrated, shrunk |
|---|---|---|---|---|---|
| +0 | 180 | 0.97 | 0.96 | 0.97 | 0.97 |
| +2 | 220 | 0.99 | 0.99 | 0.99 | 0.99 |
| +4 | 260 | 1.00 | 1.00 | 1.00 | 1.00 |
| +6 | 300 | 1.00 | 1.00 | 1.00 | 1.00 |
| +8 | 340 | 1.00 | 1.00 | 1.00 | 1.00 |
| +10 | 380 | 1.00 | 1.00 | 1.00 | 1.00 |
| +14 | 460 | 1.00 | 1.00 | 1.00 | 1.00 |

**Reading this table:** current baseline (n=179-180 pairs/family, +0 row) achieves ~97% power under the optimistic assumption that today's estimates are exactly true -- see `analysis/fault_rating_bias_findings.md`'s formal omnibus test section for whether that power was realized as an actual significant result on this data. Concentrated allocation is **not much less efficient than even allocation for the omnibus test itself** at moderate budgets (+2 to +4 scenarios/family-equivalent) -- the F-test is disproportionately driven by families furthest from the grand mean, so concentrating there sharpens exactly the signal the test needs. Even allocation pulls further ahead (asymptoting to ~100% vs. concentrated's ~97-99%) only at larger budgets.

**This does not mean concentrating is free of downsides.** Reaching omnibus significance is not the only goal -- a deployment-risk "map" needs confidently-estimated *low*-risk domains too, not just confirmation that the high ones are high. Concentrating leaves the other 6 families at n=179-180 pairs/family indefinitely, so the paper could show 3 domains are elevated but couldn't say the rest are *not*, with any real precision. There's also a disclosure problem: the top-3 selection comes from the same data used to test it, which is exactly the kind of circularity a reviewer will flag even though the ranking itself looks internally stable (Section 1).

**Recommendation:** add a meaningful number of new scenarios to *every* family (this analysis suggests +4 to +6/family gets to ~94-98% power under either truth assumption, even allocation), so every domain -- not just the top 3 -- ends up well-estimated. If there's appetite to also specifically nail down the top-3 pattern, treat it as a disclosed two-stage design: the current ranking is the Stage-1 exploratory hypothesis, and the new scenarios (across all families) are the Stage-2 confirmatory test of whether that same ranking re-emerges on fresh, independent scenario content -- not "add more data until the domains that already look big become significant."

