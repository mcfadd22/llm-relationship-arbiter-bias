import json, csv, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

d = json.load(open(os.path.join(SCRIPT_DIR, 'vignette_params.json')))
families = d['families']
pronoun_map = d['pronoun_map']
rel_ctx = d['relationship_context_by_family']

order = ["EMOLAB","HHLAB","CHILD","MENTAL","FINPROV","JEAL","SEXEXP","CAREER","FAMOBL"]

# name pairs, one fixed per family (unchanged from before)
name_pairs = {
    "EMOLAB": ("Sam", "Casey"), "HHLAB":  ("Alex", "Riley"), "CHILD":  ("Jordan", "Taylor"),
    "MENTAL": ("Morgan", "Jamie"), "FINPROV":("Alex", "Riley"), "JEAL":   ("Sam", "Casey"),
    "SEXEXP": ("Jordan", "Taylor"), "CAREER": ("Morgan", "Jamie"), "FAMOBL": ("Alex", "Riley"),
}
# same-gender name pairs: two distinct names from the SAME coded pool (pronouns can't disambiguate agent/partner)
male_pool = d.get('name_bank', {}).get('male_coded', ["Alex","Sam","Jordan","Morgan"])
female_pool = d.get('name_bank', {}).get('female_coded', ["Riley","Casey","Taylor","Jamie"])

def pron_kwargs(agent_gender, partner_gender, agent_name, partner_name):
    pa, pp = pronoun_map[agent_gender], pronoun_map[partner_gender]
    return {
        "agent": agent_name, "partner": partner_name,
        "agent_subj": pa["subj"], "agent_subj_cap": pa["subj"].capitalize(),
        "agent_obj": pa["obj"], "agent_poss": pa["poss"],
        "pronoun_partner_subj": pp["subj"], "pronoun_partner_obj": pp["obj"], "pronoun_partner_poss": pp["poss"],
    }

def render(scenario, agent_gender, partner_gender, sev, agent_name, partner_name, ctx):
    kw = pron_kwargs(agent_gender, partner_gender, agent_name, partner_name)
    obligation = scenario['obligation_sentence'].format(**kw) if scenario['obligation_sentence'] else ""
    violation = (scenario['mild_violation'] if sev == "MLD" else scenario['severe_violation']).format(**kw)
    explanation = scenario['knowing_nonmalicious_explanation'].format(**kw)
    partner_resp = scenario['partner_response'].format(**kw)
    outcome = scenario['outcome'].format(**kw)

    ctx_type = ctx['type']
    duration = ctx['duration']
    child_clause = " They have one child together." if ctx.get('children') else ""
    opening = f"{agent_name} and {partner_name} have been {ctx_type} for {duration}.{child_clause}"

    parts = [opening]
    if obligation:
        parts.append(obligation)
    parts.append(f"{violation}.")
    parts.append(f"{partner_resp}.")
    parts.append(f"{explanation}.")
    parts.append(f"{outcome}.")
    parts.append(f"Was {agent_name} in the wrong?")
    return " ".join(parts)

rows = []
for fid in order:
    fam = families[fid]
    ctx = rel_ctx[fid]
    m_name, f_name = name_pairs[fid]
    for scenario in fam['scenarios']:
        if scenario.get('status') != 'drafted':
            continue
        for agent_gender, partner_gender, agent_name, partner_name in [
            ("M", "F", m_name, f_name), ("F", "M", f_name, m_name),
            ("M", "M", male_pool[0], male_pool[2]), ("F", "F", female_pool[0], female_pool[1]),
        ]:
            for sev in ["MLD", "SEV"]:
                vid = f"{scenario['scenario_id']}_{agent_gender}{partner_gender}_{sev}"
                text = render(scenario, agent_gender, partner_gender, sev, agent_name, partner_name, ctx)
                rows.append({
                    "vignette_id": vid, "family_id": fid, "family_name": fam['name'],
                    "scenario_id": scenario['scenario_id'], "task_object": scenario.get('task_object',''),
                    "violation_form": scenario.get('violation_form',''),
                    "agent_gender": agent_gender, "partner_gender": partner_gender,
                    "relationship_context": f"{ctx['type']}, {ctx['duration']}" + (", one child" if ctx.get('children') else ""),
                    "severity": sev, "intentionality": "knowing_but_nonmalicious",
                    "agent_name": agent_name, "partner_name": partner_name,
                    "obligation_source": scenario['obligation_source'],
                    "vignette_text": text
                })

print(f"Total drafted-scenario vignettes generated: {len(rows)}")
print(f"(Target once all 36 scenarios are drafted: 288)")

with open(os.path.join(SCRIPT_DIR, 'vignette_core_set.csv'), 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
print("wrote vignette_core_set.csv")
