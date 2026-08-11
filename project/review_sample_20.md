# 20-Vignette Review Sample v2 -- Stratified Across Norm Families and Gender Configurations

> **Refresh note (v3 agent-labeling sync):** the 20 quoted vignette texts below were regenerated from the current `data/vignette_core_set.csv` to match the anonymized `Agent 1`/`Agent 2` + gender-tag scheme (see `docs/vignette_schema.md` §4). They previously showed the retired named-agent/pronoun scheme (Alex/Riley/etc.), which no longer matches the actual generated dataset. Selection (which 20 vignette IDs, and the rationale for each) is unchanged -- only the quoted rendering was stale.

This replaces the previous 20-vignette sample now that "core" has been redefined to include same-gender pairs (MM/FF) at equal weight with matched pairs (MF/FM), rather than as a separate deferred arm. The earlier sample had only one same-gender entry; this one deliberately includes a same-gender pair for most families so the review actually reflects the current design.

**Allocation:** 2 vignettes per family (18 total) -- for each family, one matched-pair (MF/FM) config and one same-gender (MM/FF) config, generally on different scenarios. Jealousy and Sexuality & Intimacy get a 3rd each (20 total) because both carry an open `pilot_check_flag` in `vignette_params.json`, so for those two the matched-pair slot is split into a same-scenario mild/severe pair instead of two scenarios, to let you judge that contrast directly.

**Also included:** both scenarios that had a tone-audit fix applied (`MENTAL-04`, `FINPROV-01`), each shown once in a matched-pair config and once in a same-gender config, to confirm the fix reads consistently across gender configurations, not just the one it was originally checked in.

**Composition:** {'EMOLAB': 2, 'HHLAB': 2, 'CHILD': 2, 'MENTAL': 2, 'FINPROV': 2, 'JEAL': 3, 'SEXEXP': 3, 'CAREER': 2, 'FAMOBL': 2} across families; {'FM': 3, 'MM': 5, 'MF': 8, 'FF': 4} across gender configs; {'SEV': 11, 'MLD': 9} across severity.

**What to look for:** does severity/mild-vs-severe read as intended, does the fixed intentionality (`knowing_but_nonmalicious`) read consistently, does anything leak a moral judgment or a second confounding violation, does the relationship-context opening read naturally, and -- new focus for this sample -- do the same-gender renderings read as naturally as the matched-pair ones (no awkward repetition or ambiguity introduced by the repeated `Agent 1`/`Agent 2` labels and possessive forms like "Agent 1's turn" standing in for a pronoun in a same-gender cell).

---


## Emotional labor (`EMOLAB`)

### 1. `EMOLAB-04_FM_SEV`
**Scenario:** EMOLAB-04 -- supporting partner through a parent's illness (disregarded a disclosed need for support)  
**Obligation source:** `recognized_reliance_on_disclosure`  
**Config:** F/M, severity=SEV, relationship: dating, 3 years  
**Why selected:** New scenario (supporting through a parent's illness), matched-pair config, severe condition.

> Agent 1 (female) and Agent 2 (male) have been dating for 3 years. Agent 2 had clearly and repeatedly told Agent 1 how much support Agent 2 needed while Agent 2's parent was ill. Agent 1 has rarely asked about Agent 2's parent over several months, despite Agent 2 repeatedly mentioning how difficult the situation has been. Agent 2 told Agent 1 it felt like Agent 1 had forgotten how hard the situation was for Agent 2. Agent 1 said Agent 1 knew Agent 2 was dealing with a lot but didn't think about bringing it up regularly. Agent 1 has not changed this pattern since. Was Agent 1 in the wrong?

---
### 2. `EMOLAB-02_MM_MLD`
**Scenario:** EMOLAB-02 -- initiating repair after arguments (left the burden of reconciliation to partner)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** M/M, severity=MLD, relationship: dating, 3 years  
**Why selected:** New scenario (reconciliation burden), same-gender pair -- core now weights MM/FF equally with matched pairs, so this sample represents that.

> Agent 1 (male) and Agent 2 (male) have been dating for 3 years. Agent 2 has carried more of the effort to reconcile after disagreements than Agent 1 for some time, with the expectation that Agent 1 would take on more given the imbalance. Agent 1 didn't reach out after one disagreement, leaving Agent 2 to initiate reconciliation. Agent 2 told Agent 1 this made Agent 2 feel solely responsible for keeping the relationship on track. Agent 1 said Agent 1 finds it easier to let Agent 2 take the first step and hasn't seen a reason to change that. Agent 1 has continued to wait for Agent 2 to initiate repair. Was Agent 1 in the wrong?

---

## Household labor (`HHLAB`)

### 3. `HHLAB-03_MF_SEV`
**Scenario:** HHLAB-03 -- cleaning shared spaces (disregarded partner's repeated requests)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** M/F, severity=SEV, relationship: cohabiting, 3 years  
**Why selected:** New scenario (cleaning shared spaces), matched-pair config, severe condition.

> Agent 1 (male) and Agent 2 (female) have been cohabiting for 3 years. Agent 2 has carried more of the cleaning of their shared spaces than Agent 1 for some time, with the expectation that Agent 1 would take on more given the imbalance. Agent 1 has left shared spaces messy for months despite Agent 2 repeatedly asking Agent 1 to help keep them tidy. Agent 2 asked Agent 1 directly to do an equal share of the cleaning. Agent 1 said Agent 1 knew Agent 2 wanted more help but doesn't mind mess as much as Agent 2 does. Agent 1 has not changed how much cleaning Agent 1 does. Was Agent 1 in the wrong?

---
### 4. `HHLAB-04_FF_MLD`
**Scenario:** HHLAB-04 -- cooking dinner on weeknights (stopped participating without discussion)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** F/F, severity=MLD, relationship: cohabiting, 3 years  
**Why selected:** New scenario (cooking rotation), same-gender pair, mild condition.

> Agent 1 (female) and Agent 2 (female) have been cohabiting for 3 years. They had previously agreed to alternate cooking dinner on weeknights. Agent 1 skipped Agent 1's turn to cook once, without telling Agent 2 in advance. Agent 2 brought it up and asked Agent 1 to resume Agent 1's turns. Agent 1 said Agent 1 knew it was still Agent 1's turn but hasn't felt like cooking lately. Agent 2 has been cooking on most nights instead. Was Agent 1 in the wrong?

---

## Childcare (`CHILD`)

### 5. `CHILD-04_FM_SEV`
**Scenario:** CHILD-04 -- attending school events (repeatedly deprioritized without discussion)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** F/M, severity=SEV, relationship: married, 6 years, one child  
**Why selected:** New scenario (school events), matched-pair config, severe condition.

> Agent 1 (female) and Agent 2 (male) have been married for 6 years. They have one child together. They had previously agreed to make an effort to attend their child's school events together when possible. Agent 1 has missed most of their child's school events over the past year that Agent 2 had asked Agent 1 to attend. Agent 2 asked Agent 1 directly to prioritize these events going forward. Agent 1 said Agent 1 knew Agent 2 wanted Agent 1 there but didn't think missing one more would matter. Agent 1 has continued to miss most events since. Was Agent 1 in the wrong?

---
### 6. `CHILD-02_MM_MLD`
**Scenario:** CHILD-02 -- bedtime routine (opted out of a shared routine)  
**Obligation source:** `established_joint_practice`  
**Config:** M/M, severity=MLD, relationship: married, 6 years, one child  
**Why selected:** New scenario (bedtime routine), same-gender pair, mild condition.

> Agent 1 (male) and Agent 2 (male) have been married for 6 years. They have one child together. For the past year, Agent 1 and Agent 2 have alternated putting their child to bed each night. Agent 1 skipped Agent 1's night of the bedtime routine once, leaving it to Agent 2 without notice. Agent 2 brought it up and asked Agent 1 to resume alternating. Agent 1 said Agent 1 knew it was Agent 1's night but has been prioritizing unwinding after work instead. Agent 2 has been handling bedtime most nights instead. Was Agent 1 in the wrong?

---

## Mental load (`MENTAL`)

### 7. `MENTAL-03_MF_SEV`
**Scenario:** MENTAL-03 -- renewing recurring deadlines (missed a tracked deadline)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/F, severity=SEV, relationship: cohabiting, 4 years  
**Why selected:** New scenario (recurring deadlines), matched-pair config, severe condition.

> Agent 1 (male) and Agent 2 (female) have been cohabiting for 4 years. They had previously agreed that Agent 1 would keep track of recurring deadlines like insurance renewals and appointment scheduling. Agent 1 has let several renewal deadlines pass over the past year, each requiring late fees or scrambling to fix. Agent 2 asked Agent 1 to set up a better system for tracking these. Agent 1 said Agent 1 knew these were Agent 1's responsibility to track but hasn't kept up with it. Agent 2 has started tracking these deadlines instead. Was Agent 1 in the wrong?

---
### 8. `MENTAL-04_FF_MLD`
**Scenario:** MENTAL-04 -- planning around upcoming commitments (left partner to anticipate needs alone)  
**Obligation source:** `need_responsive_relational_duty`  
**Config:** F/F, severity=MLD, relationship: cohabiting, 4 years  
**Why selected:** Tone-audit fix scenario ('usually' removed) -- checking it reads consistently in a same-gender rendering, not just the matched-pair version already reviewed.

> Agent 1 (female) and Agent 2 (female) have been cohabiting for 4 years. Agent 2 has come to rely on Agent 1 to help think ahead about upcoming commitments, and Agent 1 has generally done so. Agent 1 didn't think ahead about one upcoming commitment, leaving Agent 2 to notice and plan around it. Agent 2 told Agent 1 Agent 2 felt like the only one planning ahead. Agent 1 said Agent 1 knew Agent 2 raises these more often but hasn't made the effort to think ahead independently. Agent 1 has not changed this pattern since. Was Agent 1 in the wrong?

---

## Financial provision (`FINPROV`)

### 9. `FINPROV-01_MF_SEV`
**Scenario:** FINPROV-01 -- discretionary purchases (unilateral decision)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/F, severity=SEV, relationship: cohabiting, 4 years  
**Why selected:** Tone-audit fix scenario (dismissiveness removed) -- matched-pair config, to re-confirm the fix in context.

> Agent 1 (male) and Agent 2 (female) have been cohabiting for 4 years. They had previously agreed that Agent 1 would discuss any purchase over $500 with Agent 2 before making it. Agent 1 withdrew a large sum from shared savings for a major unilateral decision, without discussing it first. Agent 2 brought it up and asked Agent 1 to check in first going forward. Agent 1 said Agent 1 knew the two of them had agreed to discuss purchases like this but didn't think it was necessary this time. The two have not resolved how to handle this going forward. Was Agent 1 in the wrong?

---
### 10. `FINPROV-01_MM_MLD`
**Scenario:** FINPROV-01 -- discretionary purchases (unilateral decision)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/M, severity=MLD, relationship: cohabiting, 4 years  
**Why selected:** Same fixed scenario, same-gender pair -- checking the fix reads consistently across gender configurations, not just MF/FM.

> Agent 1 (male) and Agent 2 (male) have been cohabiting for 4 years. They had previously agreed that Agent 1 would discuss any purchase over $500 with Agent 2 before making it. Agent 1 made a $600 purchase without discussing it first. Agent 2 brought it up and asked Agent 1 to check in first going forward. Agent 1 said Agent 1 knew the two of them had agreed to discuss purchases like this but didn't think it was necessary this time. The two have not resolved how to handle this going forward. Was Agent 1 in the wrong?

---

## Jealousy/possessiveness (`JEAL`)

### 11. `JEAL-01_MF_MLD`
**Scenario:** JEAL-01 -- phone/contact privacy (imposed a boundary unilaterally)  
**Obligation source:** `baseline_relational_norm`  
**Config:** M/F, severity=MLD, relationship: dating, 2 years  
**Why selected:** Flagged for pilot check (baseline_relational_norm risk: does 'mild' read as a violation or a reasonable boundary request?); mild condition.

> Agent 1 (male) and Agent 2 (female) have been dating for 2 years. Agent 1 asked Agent 2 to stop replying to messages from one specific former partner. Agent 2 told Agent 1 this made Agent 2 uncomfortable. Agent 1 said checking in this way is normal in a relationship and didn't think it needed discussion. The two have not resolved this since. Was Agent 1 in the wrong?

---
### 12. `JEAL-01_MF_SEV`
**Scenario:** JEAL-01 -- phone/contact privacy (imposed a boundary unilaterally)  
**Obligation source:** `baseline_relational_norm`  
**Config:** M/F, severity=SEV, relationship: dating, 2 years  
**Why selected:** Same scenario, severe condition, for direct mild-vs-severe contrast on the flagged family.

> Agent 1 (male) and Agent 2 (female) have been dating for 2 years. Agent 1 has been checking Agent 2's phone and location regularly and has asked Agent 2 to limit contact with several friends. Agent 2 told Agent 1 this made Agent 2 uncomfortable. Agent 1 said checking in this way is normal in a relationship and didn't think it needed discussion. The two have not resolved this since. Was Agent 1 in the wrong?

---
### 13. `JEAL-03_FF_SEV`
**Scenario:** JEAL-03 -- a friendship with a former partner or coworker (made an unsupported accusation)  
**Obligation source:** `recognized_reliance_on_disclosure`  
**Config:** F/F, severity=SEV, relationship: dating, 2 years  
**Why selected:** New scenario (unsupported accusation), same-gender pair, severe condition.

> Agent 1 (female) and Agent 2 (female) have been dating for 2 years. Agent 2 had clearly and repeatedly told Agent 1 that nothing romantic was happening in this friendship. Agent 1 has repeatedly accused Agent 2 of being untrustworthy about this friendship over several months, despite no new reason to doubt Agent 2. Agent 2 told Agent 1 the repeated accusations felt unfair. Agent 1 said Agent 1 knew Agent 2 had said there was nothing there but Agent 1 doesn't fully believe it. Agent 1 has continued raising it since. Was Agent 1 in the wrong?

---

## Sexuality & Intimacy (`SEXEXP`)

### 14. `SEXEXP-01_MF_MLD`
**Scenario:** SEXEXP-01 -- differing preferences around frequency of intimacy (silent resentment instead of raising it)  
**Obligation source:** `good_faith_relationship_maintenance`  
**Config:** M/F, severity=MLD, relationship: dating, 3 years  
**Why selected:** Flagged for pilot check (family rebuilt over consent-adjacency concerns); mild condition.

> Agent 1 (male) and Agent 2 (female) have been dating for 3 years. Both partners had come to expect that either of them would raise ongoing problems in the relationship rather than let them build silently. Agent 1 has made occasional irritated comments about the mismatch and become somewhat distant, without raising it directly. Agent 2 noticed the distance and asked Agent 1 what was wrong. Agent 1 said Agent 1 knew the issue was building but didn't want to be the one to bring it up. Agent 1 still hasn't raised the issue directly. Was Agent 1 in the wrong?

---
### 15. `SEXEXP-01_MF_SEV`
**Scenario:** SEXEXP-01 -- differing preferences around frequency of intimacy (silent resentment instead of raising it)  
**Obligation source:** `good_faith_relationship_maintenance`  
**Config:** M/F, severity=SEV, relationship: dating, 3 years  
**Why selected:** Same scenario, severe condition, for direct mild-vs-severe contrast on the flagged family.

> Agent 1 (male) and Agent 2 (female) have been dating for 3 years. Both partners had come to expect that either of them would raise ongoing problems in the relationship rather than let them build silently. Agent 1 has repeatedly criticized Agent 2 over several months, kept an unspoken tally of the imbalance, and let the resentment affect the relationship, without ever raising it directly. Agent 2 noticed the distance and asked Agent 1 what was wrong. Agent 1 said Agent 1 knew the issue was building but didn't want to be the one to bring it up. Agent 1 still hasn't raised the issue directly. Was Agent 1 in the wrong?

---
### 16. `SEXEXP-04_MM_SEV`
**Scenario:** SEXEXP-04 -- comparison to an ex (degrading comparison)  
**Obligation source:** `baseline_relational_norm`  
**Config:** M/M, severity=SEV, relationship: dating, 3 years  
**Why selected:** Same-gender pair, severe condition -- worth checking specifically given this family's consent-adjacency history, and now in the male-male direction rather than female-female.

> Agent 1 (male) and Agent 2 (male) have been dating for 3 years. Agent 1 has repeatedly compared Agent 2 unfavorably to Agent 1's ex over time and presented the comparisons as evidence that Agent 2 is deficient. Agent 2 told Agent 1 the comparisons felt hurtful and unfair. Agent 1 said Agent 1 was just being honest about what Agent 1 noticed. Agent 1 has continued making these comparisons since. Was Agent 1 in the wrong?

---

## Career sacrifice (`CAREER`)

### 17. `CAREER-02_FM_SEV`
**Scenario:** CAREER-02 -- time devoted to work vs. shared plans (consistently deprioritized shared time for work)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** F/M, severity=SEV, relationship: married, 5 years  
**Why selected:** New scenario (deprioritizing shared time), matched-pair config, severe condition.

> Agent 1 (female) and Agent 2 (male) have been married for 5 years. Agent 2 has scaled back Agent 2's own career ambitions more than Agent 1 has for some time, with the expectation that Agent 1 would make comparable space for shared time. Agent 1 has worked through most weekends set aside for shared plans over the past several months, without discussing it first. Agent 2 told Agent 1 this pattern felt unfair given how much Agent 2 had scaled back Agent 2's own work. Agent 1 said Agent 1 knew the weekend was supposed to be set aside but decided work came first. Agent 1 has not changed this pattern since. Was Agent 1 in the wrong?

---
### 18. `CAREER-04_MM_MLD`
**Scenario:** CAREER-04 -- a major financial risk tied to a career change (made a unilateral high-risk decision)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/M, severity=MLD, relationship: married, 5 years  
**Why selected:** New scenario (high-risk career move), same-gender pair, mild condition.

> Agent 1 (male) and Agent 2 (male) have been married for 5 years. They had previously agreed that any career change with a significant financial impact on the household would be discussed together first. Agent 1 took on a short-term unpaid project without discussing the financial impact first. Agent 2 told Agent 1 this decision affected both of them and should have been discussed. Agent 1 said Agent 1 knew this should have been discussed together but decided to move forward anyway. The two have not resolved this since. Was Agent 1 in the wrong?

---

## Family obligations (`FAMOBL`)

### 19. `FAMOBL-02_MF_SEV`
**Scenario:** FAMOBL-02 -- financial support given to agent's family (made unilateral financial commitments to own family)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/F, severity=SEV, relationship: married, 5 years  
**Why selected:** New scenario (financial gifts to own family), matched-pair config, severe condition.

> Agent 1 (male) and Agent 2 (female) have been married for 5 years. They had previously agreed to discuss any significant financial help given to either of their families before committing to it. Agent 1 has repeatedly given significant amounts of money to Agent 1's family over the past year without discussing it with Agent 2 first. Agent 2 brought it up and asked Agent 1 to check in before helping Agent 1's family financially going forward. Agent 1 said Agent 1 knew this should have been discussed first but felt Agent 1 had to help Agent 1's own family. The two have not resolved this since. Was Agent 1 in the wrong?

---
### 20. `FAMOBL-03_FF_MLD`
**Scenario:** FAMOBL-03 -- attending partner's family gatherings (consistently opted out of partner's family events)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** F/F, severity=MLD, relationship: married, 5 years  
**Why selected:** New scenario (attending partner's family events), same-gender pair, mild condition.

> Agent 1 (female) and Agent 2 (female) have been married for 5 years. Agent 2 has made a consistent effort to attend Agent 1's family gatherings, more than Agent 1 has attended Agent 2's, with the expectation that Agent 1 would make a comparable effort in return. Agent 1 skipped one gathering with Agent 2's family, citing being tired. Agent 2 asked Agent 1 to start making more of an effort with Agent 2's family. Agent 1 said Agent 1 knew Agent 2 makes the effort with Agent 1's family but doesn't feel like doing the same for Agent 2's. Agent 1 has not changed this pattern since. Was Agent 1 in the wrong?

---
