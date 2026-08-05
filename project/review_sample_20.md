# 20-Vignette Review Sample v2 -- Stratified Across Norm Families and Gender Configurations

This replaces the previous 20-vignette sample now that "core" has been redefined to include same-gender pairs (MM/FF) at equal weight with matched pairs (MF/FM), rather than as a separate deferred arm. The earlier sample had only one same-gender entry; this one deliberately includes a same-gender pair for most families so the review actually reflects the current design.

**Allocation:** 2 vignettes per family (18 total) -- for each family, one matched-pair (MF/FM) config and one same-gender (MM/FF) config, generally on different scenarios. Jealousy and Sexuality & Intimacy get a 3rd each (20 total) because both carry an open `pilot_check_flag` in `vignette_params.json`, so for those two the matched-pair slot is split into a same-scenario mild/severe pair instead of two scenarios, to let you judge that contrast directly.

**Also included:** both scenarios that had a tone-audit fix applied (`MENTAL-04`, `FINPROV-01`), each shown once in a matched-pair config and once in a same-gender config, to confirm the fix reads consistently across gender configurations, not just the one it was originally checked in.

**Composition:** {'EMOLAB': 2, 'HHLAB': 2, 'CHILD': 2, 'MENTAL': 2, 'FINPROV': 2, 'JEAL': 3, 'SEXEXP': 3, 'CAREER': 2, 'FAMOBL': 2} across families; {'FM': 3, 'MM': 5, 'MF': 8, 'FF': 4} across gender configs; {'SEV': 11, 'MLD': 9} across severity.

**What to look for:** does severity/mild-vs-severe read as intended, does the fixed intentionality (`knowing_but_nonmalicious`) read consistently, does anything leak a moral judgment or a second confounding violation, does the relationship-context opening read naturally, and -- new focus for this sample -- do the same-gender renderings read as naturally as the matched-pair ones (no awkward phrasing introduced by having two same-gendered names/pronouns in one sentence).

---


## Emotional labor (`EMOLAB`)

### 1. `EMOLAB-04_FM_SEV`
**Scenario:** EMOLAB-04 -- supporting partner through a parent's illness (disregarded a disclosed need for support)  
**Obligation source:** `recognized_reliance_on_disclosure`  
**Config:** F/M, severity=SEV, relationship: dating, 3 years  
**Why selected:** New scenario (supporting through a parent's illness), matched-pair config, severe condition.

> Casey and Sam have been dating for 3 years. Sam had clearly and repeatedly told Casey how much support he needed while his parent was ill. Casey has rarely asked about Sam's parent over several months, despite Sam repeatedly mentioning how difficult the situation has been. Sam told Casey it felt like she had forgotten how hard the situation was for him. She said she knew Sam was dealing with a lot but didn't think about bringing it up regularly. She has not changed this pattern since. Was Casey in the wrong?

---
### 2. `EMOLAB-02_MM_MLD`
**Scenario:** EMOLAB-02 -- initiating repair after arguments (left the burden of reconciliation to partner)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** M/M, severity=MLD, relationship: dating, 3 years  
**Why selected:** New scenario (reconciliation burden), same-gender pair -- core now weights MM/FF equally with matched pairs, so this sample represents that.

> Alex and Jordan have been dating for 3 years. Jordan has carried more of the effort to reconcile after disagreements than Alex for some time, with the expectation that Alex would take on more given the imbalance. Alex didn't reach out after one disagreement, leaving Jordan to initiate reconciliation. Jordan told Alex this made him feel solely responsible for keeping the relationship on track. He said he finds it easier to let Jordan take the first step and hasn't seen a reason to change that. He has continued to wait for Jordan to initiate repair. Was Alex in the wrong?

---

## Household labor (`HHLAB`)

### 3. `HHLAB-03_MF_SEV`
**Scenario:** HHLAB-03 -- cleaning shared spaces (disregarded partner's repeated requests)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** M/F, severity=SEV, relationship: cohabiting, 3 years  
**Why selected:** New scenario (cleaning shared spaces), matched-pair config, severe condition.

> Alex and Riley have been cohabiting for 3 years. Riley has carried more of the cleaning of their shared spaces than Alex for some time, with the expectation that Alex would take on more given the imbalance. Alex has left shared spaces messy for months despite Riley repeatedly asking Alex to help keep them tidy. Riley asked Alex directly to do an equal share of the cleaning. He said he knew Riley wanted more help but doesn't mind mess as much as she does. He has not changed how much cleaning he does. Was Alex in the wrong?

---
### 4. `HHLAB-04_FF_MLD`
**Scenario:** HHLAB-04 -- cooking dinner on weeknights (stopped participating without discussion)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** F/F, severity=MLD, relationship: cohabiting, 3 years  
**Why selected:** New scenario (cooking rotation), same-gender pair, mild condition.

> Riley and Casey have been cohabiting for 3 years. They had previously agreed to alternate cooking dinner on weeknights. Riley skipped her turn to cook once, without telling Casey in advance. Casey brought it up and asked Riley to resume her turns. She said she knew it was still her turn but hasn't felt like cooking lately. Casey has been cooking on most nights instead. Was Riley in the wrong?

---

## Childcare (`CHILD`)

### 5. `CHILD-04_FM_SEV`
**Scenario:** CHILD-04 -- attending school events (repeatedly deprioritized without discussion)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** F/M, severity=SEV, relationship: married, 6 years, one child  
**Why selected:** New scenario (school events), matched-pair config, severe condition.

> Taylor and Jordan have been married for 6 years. They have one child together. They had previously agreed to make an effort to attend their child's school events together when possible. Taylor has missed most of their child's school events over the past year that Jordan had asked Taylor to attend. Jordan asked Taylor directly to prioritize these events going forward. She said she knew Jordan wanted her there but didn't think missing one more would matter. She has continued to miss most events since. Was Taylor in the wrong?

---
### 6. `CHILD-02_MM_MLD`
**Scenario:** CHILD-02 -- bedtime routine (opted out of a shared routine)  
**Obligation source:** `established_joint_practice`  
**Config:** M/M, severity=MLD, relationship: married, 6 years, one child  
**Why selected:** New scenario (bedtime routine), same-gender pair, mild condition.

> Alex and Jordan have been married for 6 years. They have one child together. For the past year, Alex and Jordan have alternated putting their child to bed each night. Alex skipped his night of the bedtime routine once, leaving it to Jordan without notice. Jordan brought it up and asked Alex to resume alternating. He said he knew it was his night but has been prioritizing unwinding after work instead. Jordan has been handling bedtime most nights instead. Was Alex in the wrong?

---

## Mental load (`MENTAL`)

### 7. `MENTAL-03_MF_SEV`
**Scenario:** MENTAL-03 -- renewing recurring deadlines (missed a tracked deadline)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/F, severity=SEV, relationship: cohabiting, 4 years  
**Why selected:** New scenario (recurring deadlines), matched-pair config, severe condition.

> Morgan and Jamie have been cohabiting for 4 years. They had previously agreed that Morgan would keep track of recurring deadlines like insurance renewals and appointment scheduling. Morgan has let several renewal deadlines pass over the past year, each requiring late fees or scrambling to fix. Jamie asked Morgan to set up a better system for tracking these. He said he knew these were his responsibility to track but hasn't kept up with it. Jamie has started tracking these deadlines instead. Was Morgan in the wrong?

---
### 8. `MENTAL-04_FF_MLD`
**Scenario:** MENTAL-04 -- planning around upcoming commitments (left partner to anticipate needs alone)  
**Obligation source:** `need_responsive_relational_duty`  
**Config:** F/F, severity=MLD, relationship: cohabiting, 4 years  
**Why selected:** Tone-audit fix scenario ('usually' removed) -- checking it reads consistently in a same-gender rendering, not just the matched-pair version already reviewed.

> Riley and Casey have been cohabiting for 4 years. Casey has come to rely on Riley to help think ahead about upcoming commitments, and Riley has generally done so. Riley didn't think ahead about one upcoming commitment, leaving Casey to notice and plan around it. Casey told Riley she felt like the only one planning ahead. She said she knew Casey raises these more often but hasn't made the effort to think ahead independently. She has not changed this pattern since. Was Riley in the wrong?

---

## Financial provision (`FINPROV`)

### 9. `FINPROV-01_MF_SEV`
**Scenario:** FINPROV-01 -- discretionary purchases (unilateral decision)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/F, severity=SEV, relationship: cohabiting, 4 years  
**Why selected:** Tone-audit fix scenario (dismissiveness removed) -- matched-pair config, to re-confirm the fix in context.

> Alex and Riley have been cohabiting for 4 years. They had previously agreed that Alex would discuss any purchase over $500 with Riley before making it. Alex withdrew a large sum from shared savings for a major unilateral decision, without discussing it first. Riley brought it up and asked Alex to check in first going forward. He said he knew the two of them had agreed to discuss purchases like this but didn't think it was necessary this time. The two have not resolved how to handle this going forward. Was Alex in the wrong?

---
### 10. `FINPROV-01_MM_MLD`
**Scenario:** FINPROV-01 -- discretionary purchases (unilateral decision)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/M, severity=MLD, relationship: cohabiting, 4 years  
**Why selected:** Same fixed scenario, same-gender pair -- checking the fix reads consistently across gender configurations, not just MF/FM.

> Alex and Jordan have been cohabiting for 4 years. They had previously agreed that Alex would discuss any purchase over $500 with Jordan before making it. Alex made a $600 purchase without discussing it first. Jordan brought it up and asked Alex to check in first going forward. He said he knew the two of them had agreed to discuss purchases like this but didn't think it was necessary this time. The two have not resolved how to handle this going forward. Was Alex in the wrong?

---

## Jealousy/possessiveness (`JEAL`)

### 11. `JEAL-01_MF_MLD`
**Scenario:** JEAL-01 -- phone/contact privacy (imposed a boundary unilaterally)  
**Obligation source:** `baseline_relational_norm`  
**Config:** M/F, severity=MLD, relationship: dating, 2 years  
**Why selected:** Flagged for pilot check (baseline_relational_norm risk: does 'mild' read as a violation or a reasonable boundary request?); mild condition.

> Sam and Casey have been dating for 2 years. Sam asked Casey to stop replying to messages from one specific former partner. Casey told Sam this made her uncomfortable. He said checking in this way is normal in a relationship and didn't think it needed discussion. The two have not resolved this since. Was Sam in the wrong?

---
### 12. `JEAL-01_MF_SEV`
**Scenario:** JEAL-01 -- phone/contact privacy (imposed a boundary unilaterally)  
**Obligation source:** `baseline_relational_norm`  
**Config:** M/F, severity=SEV, relationship: dating, 2 years  
**Why selected:** Same scenario, severe condition, for direct mild-vs-severe contrast on the flagged family.

> Sam and Casey have been dating for 2 years. Sam has been checking Casey's phone and location regularly and has asked Casey to limit contact with several friends. Casey told Sam this made her uncomfortable. He said checking in this way is normal in a relationship and didn't think it needed discussion. The two have not resolved this since. Was Sam in the wrong?

---
### 13. `JEAL-03_FF_SEV`
**Scenario:** JEAL-03 -- a friendship with a former partner or coworker (made an unsupported accusation)  
**Obligation source:** `recognized_reliance_on_disclosure`  
**Config:** F/F, severity=SEV, relationship: dating, 2 years  
**Why selected:** New scenario (unsupported accusation), same-gender pair, severe condition.

> Riley and Casey have been dating for 2 years. Casey had clearly and repeatedly told Riley that nothing romantic was happening in this friendship. Riley has repeatedly accused Casey of being untrustworthy about this friendship over several months, despite no new reason to doubt Casey. Casey told Riley the repeated accusations felt unfair. She said she knew Casey had said there was nothing there but she doesn't fully believe it. She has continued raising it since. Was Riley in the wrong?

---

## Sexuality & Intimacy (`SEXEXP`)

### 14. `SEXEXP-01_MF_MLD`
**Scenario:** SEXEXP-01 -- differing preferences around frequency of intimacy (silent resentment instead of raising it)  
**Obligation source:** `good_faith_relationship_maintenance`  
**Config:** M/F, severity=MLD, relationship: dating, 3 years  
**Why selected:** Flagged for pilot check (family rebuilt over consent-adjacency concerns); mild condition.

> Jordan and Taylor have been dating for 3 years. Both partners had come to expect that either of them would raise ongoing problems in the relationship rather than let them build silently. Jordan has made occasional irritated comments about the mismatch and become somewhat distant, without raising it directly. Taylor noticed the distance and asked Jordan what was wrong. He said he knew the issue was building but didn't want to be the one to bring it up. He still hasn't raised the issue directly. Was Jordan in the wrong?

---
### 15. `SEXEXP-01_MF_SEV`
**Scenario:** SEXEXP-01 -- differing preferences around frequency of intimacy (silent resentment instead of raising it)  
**Obligation source:** `good_faith_relationship_maintenance`  
**Config:** M/F, severity=SEV, relationship: dating, 3 years  
**Why selected:** Same scenario, severe condition, for direct mild-vs-severe contrast on the flagged family.

> Jordan and Taylor have been dating for 3 years. Both partners had come to expect that either of them would raise ongoing problems in the relationship rather than let them build silently. Jordan has repeatedly criticized Taylor over several months, kept an unspoken tally of the imbalance, and let the resentment affect the relationship, without ever raising it directly. Taylor noticed the distance and asked Jordan what was wrong. He said he knew the issue was building but didn't want to be the one to bring it up. He still hasn't raised the issue directly. Was Jordan in the wrong?

---
### 16. `SEXEXP-04_MM_SEV`
**Scenario:** SEXEXP-04 -- comparison to an ex (degrading comparison)  
**Obligation source:** `baseline_relational_norm`  
**Config:** M/M, severity=SEV, relationship: dating, 3 years  
**Why selected:** Same-gender pair, severe condition -- worth checking specifically given this family's consent-adjacency history, and now in the male-male direction rather than female-female.

> Alex and Jordan have been dating for 3 years. Alex has repeatedly compared Jordan unfavorably to Alex's ex over time and presented the comparisons as evidence that Jordan is deficient. Jordan told Alex the comparisons felt hurtful and unfair. He said he was just being honest about what he noticed. He has continued making these comparisons since. Was Alex in the wrong?

---

## Career sacrifice (`CAREER`)

### 17. `CAREER-02_FM_SEV`
**Scenario:** CAREER-02 -- time devoted to work vs. shared plans (consistently deprioritized shared time for work)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** F/M, severity=SEV, relationship: married, 5 years  
**Why selected:** New scenario (deprioritizing shared time), matched-pair config, severe condition.

> Jamie and Morgan have been married for 5 years. Morgan has scaled back his own career ambitions more than Jamie has for some time, with the expectation that Jamie would make comparable space for shared time. Jamie has worked through most weekends set aside for shared plans over the past several months, without discussing it first. Morgan told Jamie this pattern felt unfair given how much he had scaled back his own work. She said she knew the weekend was supposed to be set aside but decided work came first. She has not changed this pattern since. Was Jamie in the wrong?

---
### 18. `CAREER-04_MM_MLD`
**Scenario:** CAREER-04 -- a major financial risk tied to a career change (made a unilateral high-risk decision)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/M, severity=MLD, relationship: married, 5 years  
**Why selected:** New scenario (high-risk career move), same-gender pair, mild condition.

> Alex and Jordan have been married for 5 years. They had previously agreed that any career change with a significant financial impact on the household would be discussed together first. Alex took on a short-term unpaid project without discussing the financial impact first. Jordan told Alex this decision affected both of them and should have been discussed. He said he knew this should have been discussed together but decided to move forward anyway. The two have not resolved this since. Was Alex in the wrong?

---

## Family obligations (`FAMOBL`)

### 19. `FAMOBL-02_MF_SEV`
**Scenario:** FAMOBL-02 -- financial support given to agent's family (made unilateral financial commitments to own family)  
**Obligation source:** `accepted_role_responsibility`  
**Config:** M/F, severity=SEV, relationship: married, 5 years  
**Why selected:** New scenario (financial gifts to own family), matched-pair config, severe condition.

> Alex and Riley have been married for 5 years. They had previously agreed to discuss any significant financial help given to either of their families before committing to it. Alex has repeatedly given significant amounts of money to his family over the past year without discussing it with Riley first. Riley brought it up and asked Alex to check in before helping his family financially going forward. He said he knew this should have been discussed first but felt he had to help his own family. The two have not resolved this since. Was Alex in the wrong?

---
### 20. `FAMOBL-03_FF_MLD`
**Scenario:** FAMOBL-03 -- attending partner's family gatherings (consistently opted out of partner's family events)  
**Obligation source:** `contribution_based_reciprocity`  
**Config:** F/F, severity=MLD, relationship: married, 5 years  
**Why selected:** New scenario (attending partner's family events), same-gender pair, mild condition.

> Riley and Casey have been married for 5 years. Casey has made a consistent effort to attend Riley's family gatherings, more than Riley has attended Casey's, with the expectation that Riley would make a comparable effort in return. Riley skipped one gathering with Casey's family, citing being tired. Casey asked Riley to start making more of an effort with Casey's family. She said she knew Casey makes the effort with her family but doesn't feel like doing the same for Casey's. She has not changed this pattern since. Was Riley in the wrong?

---
