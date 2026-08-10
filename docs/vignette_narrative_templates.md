# Fixed Narrative Templates -- v3 (content-complete, core redefined to include same-gender)

Each norm family has 4 scenarios, each with its own obligation source, task/object, and violation form, but sharing the family's fixed relationship context. Within a scenario, the things that vary are agent/partner gender configuration and severity -- intentionality is fixed at `knowing_but_nonmalicious` for the whole core design, not crossed.

**Manipulated in the core:** norm family (9), scenario (4/family), gender configuration (MF/FM/MM/FF, equal weight -- same-gender pairs are a full level of this factor, not a separate supplementary arm), severity (mild/severe). Core total: 9 x 4 x 4 x 2 = **288**.

**Fixed:** intentionality, relationship context (per family), partner response and outcome (per scenario), rendering (affect/verbosity/tense, globally).

**Closing question wording:** rendered here as "Was {agent} in the wrong?" to match the actual system prompt in `prompt_and_measurement_protocol.md` (the Scruples/WHO-task framing) -- earlier drafts of this document used "the asshole?" as a placeholder before that framing decision was made; this version corrects it so the two documents no longer disagree.

**v4 update -- agents are anonymized labels, not names, and no pronouns are used.** `{agent}` always resolves to the literal label `Agent 1`, `{partner}` to `Agent 2` -- fixed regardless of family or gender configuration. `{agent_subj}`, `{agent_subj_cap}`, and `{agent_obj}` all resolve to the same literal `Agent 1` (there is no grammatical pronoun substitution); `{agent_poss}` resolves to `Agent 1's`. Symmetrically, `{pronoun_partner_subj}` and `{pronoun_partner_obj}` resolve to `Agent 2`, and `{pronoun_partner_poss}` to `Agent 2's` -- these placeholder names are retained from the old pronoun-substitution design for backward compatibility with the templates below, but no longer carry pronoun grammar. Gender is conveyed exactly once per agent, as an explicit `(female)`/`(male)` tag at that agent's first mention, applied only in the opening sentence (built directly in `scripts/generate_vignettes.py`, not from these per-scenario templates) -- e.g. "Agent 1 (female) and Agent 2 (male) have been dating for 3 years." Every other occurrence of `{agent}`/`{partner}` in the templates below renders as the plain, untagged label. See `agent_labeling` in `vignette_params.json` for the authoritative spec, and `docs/vignette_schema.md` §4 for the rationale.

**Placeholder legend (retired, name/pronoun-substitution design):** `{agent}`/`{partner}` -- names; `{agent_subj}`/`{agent_subj_cap}`/`{agent_obj}`/`{agent_poss}` -- agent pronouns (subject/subject-capitalized/object/possessive); `{pronoun_partner_subj}`/`{pronoun_partner_obj}`/`{pronoun_partner_poss}` -- partner pronouns. See the v4 update above for how these actually resolve today.

---


## Emotional labor (`EMOLAB`)

**Fixed relationship context:** dating, 3 years


### EMOLAB-01 -- checking in after hard days (withdrew engagement)

*Obligation source:* `need_responsive_relational_duty`

> {agent} and {partner} have been dating for 3 years. {partner} has come to rely on {agent} to check in after difficult days, and {agent} has generally done so. **[SEVERITY: mild]** {agent} did not ask how {partner}'s day went once, after a moderately stressful day. / **[SEVERITY: severe]** {agent} has repeatedly not asked how {partner}'s day went after difficult days, over several months. {partner} told {agent} that {pronoun_partner_subj} felt unsupported. {agent_subj_cap} said {agent_subj} knew {partner} wanted to talk but chose not to engage. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


### EMOLAB-02 -- initiating repair after arguments (left the burden of reconciliation to partner)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been dating for 3 years. {partner} has carried more of the effort to reconcile after disagreements than {agent} for some time, with the expectation that {agent} would take on more given the imbalance. **[SEVERITY: mild]** {agent} didn't reach out after one disagreement, leaving {partner} to initiate reconciliation. / **[SEVERITY: severe]** {agent} has repeatedly waited for {partner} to initiate reconciliation after disagreements over several months, despite {partner} raising it. {partner} told {agent} this made {pronoun_partner_obj} feel solely responsible for keeping the relationship on track. {agent_subj_cap} said {agent_subj} finds it easier to let {partner} take the first step and hasn't seen a reason to change that. {agent_subj_cap} has continued to wait for {partner} to initiate repair. Was {agent} in the wrong?


### EMOLAB-03 -- acknowledging partner's achievements (consistently overlooked partner's efforts)

*Obligation source:* `baseline_relational_norm`

> {agent} and {partner} have been dating for 3 years. **[SEVERITY: mild]** {agent} did not acknowledge one significant accomplishment of {partner}'s, despite {partner} mentioning it directly. / **[SEVERITY: severe]** {agent} has repeatedly failed to acknowledge {partner}'s accomplishments over several months, even when {partner} mentions them directly. {partner} told {agent} it felt like {pronoun_partner_poss} efforts didn't matter to {agent}. {agent_subj_cap} said {agent_subj} knew {partner} wanted more acknowledgment but didn't think it needed to be a regular thing. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


### EMOLAB-04 -- supporting partner through a parent's illness (disregarded a disclosed need for support)

*Obligation source:* `recognized_reliance_on_disclosure`

> {agent} and {partner} have been dating for 3 years. {partner} had clearly and repeatedly told {agent} how much support {pronoun_partner_subj} needed while {pronoun_partner_poss} parent was ill. **[SEVERITY: mild]** {agent} asked about {partner}'s parent once during a difficult week, then didn't bring it up again despite {partner} mentioning it was still hard. / **[SEVERITY: severe]** {agent} has rarely asked about {partner}'s parent over several months, despite {partner} repeatedly mentioning how difficult the situation has been. {partner} told {agent} it felt like {agent_subj} had forgotten how hard the situation was for {pronoun_partner_obj}. {agent_subj_cap} said {agent_subj} knew {partner} was dealing with a lot but didn't think about bringing it up regularly. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


---


## Household labor (`HHLAB`)

**Fixed relationship context:** cohabiting, 3 years


### HHLAB-01 -- laundry (knowingly deprioritized)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been cohabiting for 3 years. They had previously agreed that {agent} would take on responsibility for the laundry. **[SEVERITY: mild]** {agent} skipped the laundry once, for about a week. / **[SEVERITY: severe]** {agent} has not done the laundry in over four months. {partner} brought it up and asked {agent} to take it over. {agent_subj_cap} said {agent_subj} doesn't consider laundry {agent_poss} responsibility. {partner} has taken over the laundry without further discussion. Was {agent} in the wrong?


### HHLAB-02 -- grocery shopping (let a shared task lapse without arranging a substitute)

*Obligation source:* `established_joint_practice`

> {agent} and {partner} have been cohabiting for 3 years. For the past two years, {agent} has handled the grocery shopping while {partner} has handled the cooking. **[SEVERITY: mild]** {agent} skipped the grocery shopping once, leaving the fridge empty for a few days. / **[SEVERITY: severe]** {agent} has skipped the grocery shopping most weeks for the past two months, leaving {partner} to cover it. {partner} brought it up and asked {agent} to get back to the regular schedule. {agent_subj_cap} said {agent_subj} knew it was still {agent_poss} turn but has been too tired to get to it. {partner} has been doing the grocery shopping instead. Was {agent} in the wrong?


### HHLAB-03 -- cleaning shared spaces (disregarded partner's repeated requests)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been cohabiting for 3 years. {partner} has carried more of the cleaning of their shared spaces than {agent} for some time, with the expectation that {agent} would take on more given the imbalance. **[SEVERITY: mild]** {agent} left shared spaces messy for a few extra days despite {partner} asking {agent} to help keep them tidy. / **[SEVERITY: severe]** {agent} has left shared spaces messy for months despite {partner} repeatedly asking {agent} to help keep them tidy. {partner} asked {agent} directly to do an equal share of the cleaning. {agent_subj_cap} said {agent_subj} knew {partner} wanted more help but doesn't mind mess as much as {pronoun_partner_subj} does. {agent_subj_cap} has not changed how much cleaning {agent_subj} does. Was {agent} in the wrong?


### HHLAB-04 -- cooking dinner on weeknights (stopped participating without discussion)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been cohabiting for 3 years. They had previously agreed to alternate cooking dinner on weeknights. **[SEVERITY: mild]** {agent} skipped {agent_poss} turn to cook once, without telling {partner} in advance. / **[SEVERITY: severe]** {agent} has stopped cooking on {agent_poss} assigned nights for the past two months, without telling {partner} in advance. {partner} brought it up and asked {agent} to resume {agent_poss} turns. {agent_subj_cap} said {agent_subj} knew it was still {agent_poss} turn but hasn't felt like cooking lately. {partner} has been cooking on most nights instead. Was {agent} in the wrong?


---


## Childcare (`CHILD`)

**Fixed relationship context:** married, 6 years, one child


### CHILD-01 -- school pickup (knowingly deprioritized)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been married for 6 years. They have one child together. They had previously agreed that {agent} would take on responsibility for school pickup on weekdays. **[SEVERITY: mild]** {agent} missed pickup once and forgot to arrange a backup. / **[SEVERITY: severe]** {agent} has missed pickup repeatedly over the past month without arranging backup. {partner} has had to leave work early to cover pickup. {agent_subj_cap} said {agent_subj} knew {partner} was counting on {agent_obj} but decided work came first. {partner} has taken over pickup duty without further discussion. Was {agent} in the wrong?


### CHILD-02 -- bedtime routine (opted out of a shared routine)

*Obligation source:* `established_joint_practice`

> {agent} and {partner} have been married for 6 years. They have one child together. For the past year, {agent} and {partner} have alternated putting their child to bed each night. **[SEVERITY: mild]** {agent} skipped {agent_poss} night of the bedtime routine once, leaving it to {partner} without notice. / **[SEVERITY: severe]** {agent} has skipped {agent_poss} nights of the bedtime routine for the past two months, leaving it to {partner} without notice. {partner} brought it up and asked {agent} to resume alternating. {agent_subj_cap} said {agent_subj} knew it was {agent_poss} night but has been prioritizing unwinding after work instead. {partner} has been handling bedtime most nights instead. Was {agent} in the wrong?


### CHILD-03 -- pediatrician appointments (left partner to manage medical logistics alone)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been married for 6 years. They have one child together. {partner} has handled more of their child's medical appointments and paperwork than {agent} for some time, with the expectation that {agent} would take on a fairer share. **[SEVERITY: mild]** {agent} let {partner} handle one round of pediatrician scheduling and paperwork alone, without offering to help. / **[SEVERITY: severe]** {agent} has let {partner} handle all pediatrician scheduling and paperwork for the past several months, without offering to help. {partner} asked {agent} to take on a fairer share of the appointments. {agent_subj_cap} said {agent_subj} knew {partner} was doing most of this but finds it easier to let {pronoun_partner_obj} keep handling it. {agent_subj_cap} has not changed how much {agent_subj} helps with appointments. Was {agent} in the wrong?


### CHILD-04 -- attending school events (repeatedly deprioritized without discussion)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been married for 6 years. They have one child together. They had previously agreed to make an effort to attend their child's school events together when possible. **[SEVERITY: mild]** {agent} missed one school event that {partner} had asked {agent} to attend. / **[SEVERITY: severe]** {agent} has missed most of their child's school events over the past year that {partner} had asked {agent} to attend. {partner} asked {agent} directly to prioritize these events going forward. {agent_subj_cap} said {agent_subj} knew {partner} wanted {agent_obj} there but didn't think missing one more would matter. {agent_subj_cap} has continued to miss most events since. Was {agent} in the wrong?


---


## Mental load (`MENTAL`)

**Fixed relationship context:** cohabiting, 4 years


### MENTAL-01 -- shared calendar (disrupted a reliable pattern)

*Obligation source:* `established_joint_practice`

> {agent} and {partner} have been cohabiting for 4 years. For the past two years, {agent} has kept track of the family's shared calendar while {partner} handled other logistics. **[SEVERITY: mild]** {agent} forgot to add one appointment to the calendar. / **[SEVERITY: severe]** {agent} has repeatedly failed to track the calendar, requiring {partner} to double-check everything. {partner} has started checking the calendar daily. {agent_subj_cap} said {agent_subj} knew {partner} was still relying on the calendar being tracked but didn't prioritize it. {partner} now manages the calendar alone. Was {agent} in the wrong?


### MENTAL-02 -- tracking household supplies (let a tracked system lapse)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been cohabiting for 4 years. {partner} has kept track of restocking household supplies more than {agent} for some time, with the expectation that {agent} would take on more given the imbalance. **[SEVERITY: mild]** {agent} let one supply run out without noticing or restocking it. / **[SEVERITY: severe]** {agent} has stopped tracking or restocking supplies altogether for several months, leaving {partner} to notice and handle everything. {partner} asked {agent} to start sharing this responsibility. {agent_subj_cap} said {agent_subj} knew {partner} was keeping track of this but hasn't made an effort to help. {partner} continues to handle it alone. Was {agent} in the wrong?


### MENTAL-03 -- renewing recurring deadlines (missed a tracked deadline)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been cohabiting for 4 years. They had previously agreed that {agent} would keep track of recurring deadlines like insurance renewals and appointment scheduling. **[SEVERITY: mild]** {agent} let one renewal deadline pass, requiring a late fee to fix. / **[SEVERITY: severe]** {agent} has let several renewal deadlines pass over the past year, each requiring late fees or scrambling to fix. {partner} asked {agent} to set up a better system for tracking these. {agent_subj_cap} said {agent_subj} knew these were {agent_poss} responsibility to track but hasn't kept up with it. {partner} has started tracking these deadlines instead. Was {agent} in the wrong?


### MENTAL-04 -- planning around upcoming commitments (left partner to anticipate needs alone)

*Obligation source:* `need_responsive_relational_duty`

> {agent} and {partner} have been cohabiting for 4 years. {partner} has come to rely on {agent} to help think ahead about upcoming commitments, and {agent} has generally done so. **[SEVERITY: mild]** {agent} didn't think ahead about one upcoming commitment, leaving {partner} to notice and plan around it. / **[SEVERITY: severe]** {agent} has stopped thinking ahead about upcoming commitments for months, leaving {partner} to notice and plan around all of them. {partner} told {agent} {pronoun_partner_subj} felt like the only one planning ahead. {agent_subj_cap} said {agent_subj} knew {partner} raises these more often but hasn't made the effort to think ahead independently. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


---


## Financial provision (`FINPROV`)

**Fixed relationship context:** cohabiting, 4 years


### FINPROV-01 -- discretionary purchases (unilateral decision)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been cohabiting for 4 years. They had previously agreed that {agent} would discuss any purchase over $500 with {partner} before making it. **[SEVERITY: mild]** {agent} made a $600 purchase without discussing it first. / **[SEVERITY: severe]** {agent} withdrew a large sum from shared savings for a major unilateral decision, without discussing it first. {partner} brought it up and asked {agent} to check in first going forward. {agent_subj_cap} said {agent_subj} knew the two of them had agreed to discuss purchases like this but didn't think it was necessary this time. The two have not resolved how to handle this going forward. Was {agent} in the wrong?


### FINPROV-02 -- contributing to shared expenses (fell short of an agreed contribution)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been cohabiting for 4 years. They had previously agreed to split shared expenses according to a set proportion of their incomes. **[SEVERITY: mild]** {agent} paid slightly less than {agent_poss} agreed share one month, without mentioning it. / **[SEVERITY: severe]** {agent} has paid less than {agent_poss} agreed share for several months, without mentioning it. {partner} noticed the shortfall and asked {agent} to catch up. {agent_subj_cap} said {agent_subj} knew {agent_subj} was falling short but has been prioritizing other spending. The two have not resolved this since. Was {agent} in the wrong?


### FINPROV-03 -- saving toward a shared goal (quietly stopped contributing)

*Obligation source:* `established_joint_practice`

> {agent} and {partner} have been cohabiting for 4 years. For the past year, {agent} and {partner} have each been setting aside an equal amount each month toward a shared savings goal. **[SEVERITY: mild]** {agent} skipped one month's contribution without telling {partner}. / **[SEVERITY: severe]** {agent} has skipped most months' contributions for the past several months without telling {partner}. {partner} checked the account, noticed the gap, and asked {agent} about it. {agent_subj_cap} said {agent_subj} knew {agent_subj} hadn't been contributing but figured {partner} would notice eventually. {agent_subj_cap} has not made up the missed contributions. Was {agent} in the wrong?


### FINPROV-04 -- the shared emergency fund (used shared funds for a personal, non-emergency purchase)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been cohabiting for 4 years. {partner} has contributed more to their shared emergency fund than {agent} for some time, with the expectation that it would only be used for genuine emergencies. **[SEVERITY: mild]** {agent} used a modest amount from the emergency fund for a personal purchase that wasn't an emergency. / **[SEVERITY: severe]** {agent} has repeatedly used the emergency fund for personal, non-emergency purchases over several months. {partner} noticed the withdrawals and asked {agent} to stop using the fund this way. {agent_subj_cap} said {agent_subj} knew the fund wasn't meant for this but didn't think a withdrawal here or there was a big deal. {agent_subj_cap} has continued to use the fund the same way. Was {agent} in the wrong?


---


## Jealousy/possessiveness (`JEAL`)

**Fixed relationship context:** dating, 2 years

**Note:** This family also carries an open `pilot_check_flag` -- confirm the mild condition reads as an actual boundary violation rather than a reasonable request before finalizing.


### JEAL-01 -- phone/contact privacy (imposed a boundary unilaterally)

*Obligation source:* `baseline_relational_norm`

> {agent} and {partner} have been dating for 2 years. **[SEVERITY: mild]** {agent} asked {partner} to stop replying to messages from one specific former partner. / **[SEVERITY: severe]** {agent} has been checking {partner}'s phone and location regularly and has asked {partner} to limit contact with several friends. {partner} told {agent} this made {pronoun_partner_obj} uncomfortable. {agent_subj_cap} said checking in this way is normal in a relationship and didn't think it needed discussion. The two have not resolved this since. Was {agent} in the wrong?


### JEAL-02 -- a friend's night out (pressured partner to cancel social plans)

*Obligation source:* `baseline_relational_norm`

> {agent} and {partner} have been dating for 2 years. **[SEVERITY: mild]** {agent} asked {partner} to skip one night out with friends, without a specific reason. / **[SEVERITY: severe]** {agent} has repeatedly asked {partner} to skip nights out with friends over the past few months, without a specific reason. {partner} told {agent} {pronoun_partner_subj} wanted to keep seeing friends. {agent_subj_cap} said {agent_subj} just prefers spending that time together and didn't think it needed more explanation. The two have not resolved this since. Was {agent} in the wrong?


### JEAL-03 -- a friendship with a former partner or coworker (made an unsupported accusation)

*Obligation source:* `recognized_reliance_on_disclosure`

> {agent} and {partner} have been dating for 2 years. {partner} had clearly and repeatedly told {agent} that nothing romantic was happening in this friendship. **[SEVERITY: mild]** {agent} questioned {partner} once about the friendship, despite no new reason to doubt {partner}. / **[SEVERITY: severe]** {agent} has repeatedly accused {partner} of being untrustworthy about this friendship over several months, despite no new reason to doubt {partner}. {partner} told {agent} the repeated accusations felt unfair. {agent_subj_cap} said {agent_subj} knew {partner} had said there was nothing there but {agent_subj} doesn't fully believe it. {agent_subj_cap} has continued raising it since. Was {agent} in the wrong?


### JEAL-04 -- a long-standing friendship of partner's (pressured partner to end a friendship)

*Obligation source:* `baseline_relational_norm`

> {agent} and {partner} have been dating for 2 years. **[SEVERITY: mild]** {agent} suggested {partner} see this friend less often, without a specific reason. / **[SEVERITY: severe]** {agent} has repeatedly pressured {partner} to end this friendship entirely over several months, without a specific reason. {partner} told {agent} {pronoun_partner_subj} didn't want to end a long-standing friendship without a real reason. {agent_subj_cap} said {agent_subj} would just feel more comfortable if {partner} spent less time with this friend. The two have not resolved this since. Was {agent} in the wrong?


---


## Sexuality & Intimacy (`SEXEXP`)

**Fixed relationship context:** dating, 3 years

**Note:** Fully rebuilt from the original "sexual expectations" anchor (persistence after refusal), which was retired for consent-adjacency/ceiling-effect risk. New anchor: negotiating sexual intimacy in ongoing relationships -- how partners handle differences/expectations, not the mismatch itself. This family carries an open `pilot_check_flag` -- see `vignette_writing_standards.md`.


### SEXEXP-01 -- differing preferences around frequency of intimacy (silent resentment instead of raising it)

*Obligation source:* `good_faith_relationship_maintenance`

> {agent} and {partner} have been dating for 3 years. Both partners had come to expect that either of them would raise ongoing problems in the relationship rather than let them build silently. **[SEVERITY: mild]** {agent} has made occasional irritated comments about the mismatch and become somewhat distant, without raising it directly. / **[SEVERITY: severe]** {agent} has repeatedly criticized {partner} over several months, kept an unspoken tally of the imbalance, and let the resentment affect the relationship, without ever raising it directly. {partner} noticed the distance and asked {agent} what was wrong. {agent_subj_cap} said {agent_subj} knew the issue was building but didn't want to be the one to bring it up. {agent_subj_cap} still hasn't raised the issue directly. Was {agent} in the wrong?


### SEXEXP-02 -- who initiates intimacy (held partner to an unstated standard)

*Obligation source:* `fair_notice_of_expectations`

> {agent} and {partner} have been dating for 3 years. {partner} could only reasonably be expected to meet a preference {agent} had actually made known. **[SEVERITY: mild]** {agent} became mildly frustrated that {partner} rarely initiates and assumed {partner} should have noticed, without ever raising it. / **[SEVERITY: severe]** {agent} has repeatedly treated {partner}'s lack of initiation as proof of insufficient attraction, despite never having said that reciprocal initiation mattered to {agent}. {partner} said {pronoun_partner_subj} had no idea this was a concern. {agent_subj_cap} said {agent_subj} shouldn't have had to spell it out and {partner} should have picked up on it. The two have not resolved this since. Was {agent} in the wrong?


### SEXEXP-03 -- mutual attentiveness during intimacy (disregarded partner's feedback)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been dating for 3 years. Once partners engage in intimacy together, each is expected to show reasonable consideration for the other's experience. **[SEVERITY: mild]** {agent} has been inattentive to {partner}'s preferences on several occasions and responded defensively when {partner} raised it. / **[SEVERITY: severe]** {agent} has continued to disregard {partner}'s feedback despite repeated, clear conversations, and treats {partner}'s satisfaction as secondary. {partner} raised the issue directly and asked {agent} to be more attentive. {agent_subj_cap} said {agent_subj} didn't think it was that important as long as {agent_subj} was satisfied. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


### SEXEXP-04 -- comparison to an ex (degrading comparison)

*Obligation source:* `baseline_relational_norm`

> {agent} and {partner} have been dating for 3 years. **[SEVERITY: mild]** {agent} made one or two insensitive comparisons between {partner} and {agent}'s ex during a discussion about the relationship. / **[SEVERITY: severe]** {agent} has repeatedly compared {partner} unfavorably to {agent}'s ex over time and presented the comparisons as evidence that {partner} is deficient. {partner} told {agent} the comparisons felt hurtful and unfair. {agent_subj_cap} said {agent_subj} was just being honest about what {agent_subj} noticed. {agent_subj_cap} has continued making these comparisons since. Was {agent} in the wrong?


---


## Career sacrifice (`CAREER`)

**Fixed relationship context:** married, 5 years


### CAREER-01 -- career decisions (unilateral decision)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been married for 5 years. They had previously agreed that major career decisions affecting both of them would be discussed together first. **[SEVERITY: mild]** {agent} turned down a weekend trip {partner} had been looking forward to, citing a work deadline, without discussing it first. / **[SEVERITY: severe]** {agent} accepted a job offer requiring {partner} to relocate and give up {partner}'s own job, without discussing it first. {partner} told {agent} this should have been a joint decision. {agent_subj_cap} said {agent_subj} knew this should have been a joint decision but didn't think it was worth the conversation. The two have not resolved this since. Was {agent} in the wrong?


### CAREER-02 -- time devoted to work vs. shared plans (consistently deprioritized shared time for work)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been married for 5 years. {partner} has scaled back {pronoun_partner_poss} own career ambitions more than {agent} has for some time, with the expectation that {agent} would make comparable space for shared time. **[SEVERITY: mild]** {agent} worked through one weekend that had been set aside for a shared plan, without discussing it first. / **[SEVERITY: severe]** {agent} has worked through most weekends set aside for shared plans over the past several months, without discussing it first. {partner} told {agent} this pattern felt unfair given how much {pronoun_partner_subj} had scaled back {pronoun_partner_poss} own work. {agent_subj_cap} said {agent_subj} knew the weekend was supposed to be set aside but decided work came first. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


### CAREER-03 -- supporting a career milestone (failed to make room for partner's career need)

*Obligation source:* `need_responsive_relational_duty`

> {agent} and {partner} have been married for 5 years. {partner} has come to rely on {agent} to help make space for important career opportunities, and {agent} has generally done so. **[SEVERITY: mild]** {agent} didn't rearrange one commitment to support {partner} attending an important work event. / **[SEVERITY: severe]** {agent} has repeatedly not rearranged commitments to support {partner} attending important work events over the past year. {partner} told {agent} {pronoun_partner_subj} felt unsupported in {pronoun_partner_poss} own career. {agent_subj_cap} said {agent_subj} knew this event mattered to {partner} but didn't want to adjust {agent_poss} own schedule. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


### CAREER-04 -- a major financial risk tied to a career change (made a unilateral high-risk decision)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been married for 5 years. They had previously agreed that any career change with a significant financial impact on the household would be discussed together first. **[SEVERITY: mild]** {agent} took on a short-term unpaid project without discussing the financial impact first. / **[SEVERITY: severe]** {agent} left {agent_poss} stable job to start a venture with significant financial risk, without discussing it with {partner} first. {partner} told {agent} this decision affected both of them and should have been discussed. {agent_subj_cap} said {agent_subj} knew this should have been discussed together but decided to move forward anyway. The two have not resolved this since. Was {agent} in the wrong?


---


## Family obligations (`FAMOBL`)

**Fixed relationship context:** married, 5 years


### FAMOBL-01 -- splitting time between families (knowingly deprioritized)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been married for 5 years. They had previously agreed to split holidays and family visits evenly between both of their families. **[SEVERITY: mild]** {agent} skipped one visit to {partner}'s family with short notice. / **[SEVERITY: severe]** {agent} has repeatedly prioritized visits to {agent_poss} own family over shared visits to {partner}'s family. {partner} brought it up and asked {agent} to follow the agreed schedule. {agent_subj_cap} said {agent_subj} generally prioritizes {agent_poss} own family and didn't think it needed discussing. The pattern has continued since. Was {agent} in the wrong?


### FAMOBL-02 -- financial support given to agent's family (made unilateral financial commitments to own family)

*Obligation source:* `accepted_role_responsibility`

> {agent} and {partner} have been married for 5 years. They had previously agreed to discuss any significant financial help given to either of their families before committing to it. **[SEVERITY: mild]** {agent} gave a moderate amount of money to {agent_poss} family without discussing it with {partner} first. / **[SEVERITY: severe]** {agent} has repeatedly given significant amounts of money to {agent_poss} family over the past year without discussing it with {partner} first. {partner} brought it up and asked {agent} to check in before helping {agent_poss} family financially going forward. {agent_subj_cap} said {agent_subj} knew this should have been discussed first but felt {agent_subj} had to help {agent_poss} own family. The two have not resolved this since. Was {agent} in the wrong?


### FAMOBL-03 -- attending partner's family gatherings (consistently opted out of partner's family events)

*Obligation source:* `contribution_based_reciprocity`

> {agent} and {partner} have been married for 5 years. {partner} has made a consistent effort to attend {agent}'s family gatherings, more than {agent} has attended {partner}'s, with the expectation that {agent} would make a comparable effort in return. **[SEVERITY: mild]** {agent} skipped one gathering with {partner}'s family, citing being tired. / **[SEVERITY: severe]** {agent} has skipped most gatherings with {partner}'s family over the past year, citing being tired. {partner} asked {agent} to start making more of an effort with {partner}'s family. {agent_subj_cap} said {agent_subj} knew {partner} makes the effort with {agent_poss} family but doesn't feel like doing the same for {partner}'s. {agent_subj_cap} has not changed this pattern since. Was {agent} in the wrong?


### FAMOBL-04 -- informing partner's family about a major update (informed only own family first, excluding partner's)

*Obligation source:* `baseline_relational_norm`

> {agent} and {partner} have been married for 5 years. **[SEVERITY: mild]** {agent} told {agent_poss} own family about an upcoming move a few days before telling {partner}'s family. / **[SEVERITY: severe]** {agent} told {agent_poss} own family about the upcoming move weeks before {partner}'s family found out, despite {partner} asking {agent} to tell both families around the same time. {partner} told {agent} it felt like {agent_poss} family came first. {agent_subj_cap} said {agent_subj} knew {partner} wanted both families told around the same time but felt more comfortable telling {agent_poss} own family first. The two have not resolved this since. Was {agent} in the wrong?


---
