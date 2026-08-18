import json, csv, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'data')

d = json.load(open(os.path.join(DATA_DIR, 'vignette_params.json')))
families = d['families']
rel_ctx = d['relationship_context_by_family']

order = ["EMOLAB","HHLAB","CHILD","MENTAL","FINPROV","JEAL","SEXEXP","CAREER","FAMOBL"]

# Agents are anonymized labels, not names: Agent 1 is always the norm-violator
# ("agent" role), Agent 2 is always the partner. Gender is conveyed once, via an
# explicit "(female)"/"(male)" tag at each agent's first mention in the opening
# sentence -- never through a name or a pronoun. No pronouns are used anywhere
# in the rendered text; every subsequent reference is the plain label.
GENDER_LABEL = {"M": "male", "F": "female", "NB": "nonbinary"}

# Gender configurations rendered per scenario/severity cell. The original core
# crossed M/F fully (MF, FM, MM, FF). The NB extension (added 2026-08-18, full
# crossing added same day) adds NB as a full third level of both agent_gender
# and partner_gender, giving the complete 3x3 grid over {M, F, NB}: NB now
# appears both in the agent role (NB-M, NB-F, NB-NB -- lets "does the gender
# effect on fault_rating differ for an NB agent" be tested the same way "M
# agent vs F agent" already is, holding partner gender constant) and in the
# partner role opposite M/F agents (M-NB, F-NB -- lets "does the partner being
# NB change how the agent is judged" be tested the same way the existing
# partner-gender secondary effect already is). NB-NB is the same-identity
# control, analogous to how MM/FF already serve as controls for the binary
# comparison.
GENDER_CONFIGS = [("M", "F"), ("F", "M"), ("M", "M"), ("F", "F"),
                   ("NB", "M"), ("NB", "F"), ("NB", "NB"),
                   ("M", "NB"), ("F", "NB")]

def agent_kwargs():
    return {
        "agent": "Agent 1", "partner": "Agent 2",
        "agent_subj": "Agent 1", "agent_subj_cap": "Agent 1",
        "agent_obj": "Agent 1", "agent_poss": "Agent 1's",
        "pronoun_partner_subj": "Agent 2", "pronoun_partner_obj": "Agent 2", "pronoun_partner_poss": "Agent 2's",
    }

def render(scenario, agent_gender, partner_gender, sev, ctx):
    kw = agent_kwargs()
    obligation = scenario['obligation_sentence'].format(**kw) if scenario['obligation_sentence'] else ""
    violation = (scenario['mild_violation'] if sev == "MLD" else scenario['severe_violation']).format(**kw)
    explanation = scenario['knowing_nonmalicious_explanation'].format(**kw)
    partner_resp = scenario['partner_response'].format(**kw)
    outcome = scenario['outcome'].format(**kw)

    ctx_type = ctx['type']
    duration = ctx['duration']
    child_clause = " They have one child together." if ctx.get('children') else ""
    agent_first_mention = f"Agent 1 ({GENDER_LABEL[agent_gender]})"
    partner_first_mention = f"Agent 2 ({GENDER_LABEL[partner_gender]})"
    opening = f"{agent_first_mention} and {partner_first_mention} have been {ctx_type} for {duration}.{child_clause}"

    parts = [opening]
    if obligation:
        parts.append(obligation)
    parts.append(f"{violation}.")
    parts.append(f"{partner_resp}.")
    parts.append(f"{explanation}.")
    parts.append(f"{outcome}.")
    parts.append("Was Agent 1 in the wrong?")
    return " ".join(parts)

rows = []
for fid in order:
    fam = families[fid]
    ctx = rel_ctx[fid]
    for scenario in fam['scenarios']:
        if scenario.get('status') != 'drafted':
            continue
        for agent_gender, partner_gender in GENDER_CONFIGS:
            for sev in ["MLD", "SEV"]:
                vid = f"{scenario['scenario_id']}_{agent_gender}{partner_gender}_{sev}"
                text = render(scenario, agent_gender, partner_gender, sev, ctx)
                rows.append({
                    "vignette_id": vid, "family_id": fid, "family_name": fam['name'],
                    "scenario_id": scenario['scenario_id'], "task_object": scenario.get('task_object',''),
                    "violation_form": scenario.get('violation_form',''),
                    "agent_gender": agent_gender, "partner_gender": partner_gender,
                    "relationship_context": f"{ctx['type']}, {ctx['duration']}" + (", one child" if ctx.get('children') else ""),
                    "severity": sev, "intentionality": "knowing_but_nonmalicious",
                    "agent_name": "Agent 1", "partner_name": "Agent 2",
                    "obligation_source": scenario['obligation_source'],
                    "vignette_text": text
                })

print(f"Total drafted-scenario vignettes generated: {len(rows)}")

with open(os.path.join(DATA_DIR, 'vignette_core_set.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
print("wrote vignette_core_set.csv")
