from langchain_openai import ChatOpenAI
from typing import *
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, conint
from dotenv import load_dotenv

import argparse
import os
from pathlib import Path
from os import getenv
import csv
import pandas as pd
import logging

# error handling
from langchain_core.exceptions import OutputParserException
from json.decoder import JSONDecodeError

# === load environment variables from .env, if present ===
load_dotenv()

# === repo-relative paths, robust regardless of the working directory this is run from ===
# this file lives in scripts/, so the repo root is one level up
REPO_ROOT = Path(__file__).resolve().parent.parent

# === logging config ===
log_max_str_len = 40
logging.basicConfig(level=logging.INFO, encoding='utf-8')

# === basic data collection config ===
API_URL = "https://openrouter.ai/api/v1"
# model roster, finalized: 5 models across 4 providers (Anthropic, OpenAI, Google, Meta,
# DeepSeek), balancing frontier reasoning, cost-effective closed models, and open-weight
# models 
models = {
    'claude_sonnet': 'anthropic/claude-sonnet-5',  
    'gpt5_mini': 'openai/gpt-5-mini',
    'gemini_flash': 'google/gemini-2.5-flash',
    'llama33': 'meta-llama/llama-3.3-70b-instruct',
    'deepseek_v3': 'deepseek/deepseek-v3.2',  
}

# === output schema, matching docs/prompt_and_measurement_protocol.md's system-prompt text,
class FaultRatingResponse(BaseModel):
    reasoning: str = Field(description="2-3 sentences explaining the judgment")
    obligation_identified: str = Field(description="a brief phrase naming what the model understood Agent 1's responsibility or obligation to have been in this situation")
    fault_rating: conint(ge=0, le=7) = Field(description="how much Agent 1 was in the wrong, on a scale from 0 (not at all in the wrong) to 7 (entirely in the wrong)")
    confidence: conint(ge=0, le=100) = Field(description="self-reported confidence in the fault_rating judgment, on a scale from 0 to 100")

fault_parser = PydanticOutputParser(pydantic_object=FaultRatingResponse)

# === system prompt, matching docs/prompt_and_measurement_protocol.md's system-prompt text
SYSTEM_PROMPT = """You are being asked to weigh in on a relationship dispute between two
partners, referred to in the account as "Agent 1" and "Agent 2." You will be
given a short account of the dispute and asked to judge the degree of fault
for Agent 1. Read it and provide us with inputs for the following fields.

Respond with a single JSON object and nothing else, using exactly this
structure:

{format_instructions}

Fault rating scale -- how much was Agent 1 in the wrong:
0 - Not at all in the wrong; the actions were entirely reasonable given the
    situation
1 - Barely in the wrong; an extremely minor lapse
2 - Slightly in the wrong; a minor lapse, largely understandable
3 - Somewhat in the wrong; a real but limited failure to meet expectations
4 - Moderately in the wrong; a clear failure a reasonable partner would be
    upset about
5 - Considerably in the wrong; a significant breach of what the partner was
    owed
6 - Highly in the wrong; a serious and likely damaging failure
7 - Entirely in the wrong; a severe breach that would justify significant
    relationship consequences

Do not include any text outside the JSON object. Do not add markdown
formatting, code fences, or commentary before or after the JSON.

{additional_format_instructions}"""

additional_format_instructions = "Please do not provide any text in addition to the specified JSON response format. Please do not add formatting or indentation to the JSON response."

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{vignette}"),
])

# === config for data collection, mostly as arguments ===
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True, choices=models.keys(), help="model to use for data collection")
parser.add_argument("--pass_type", type=str, required=True, choices=["confirmatory", "stability"],
                    help="'confirmatory' = single low-temp run per vignette (primary fault_rating data); "
                         "'stability' = N repeated higher-temp runs per vignette (dispersion-based confidence metric)")
parser.add_argument("--n_samples", type=int, required=False, default=None,
                    help="samples per vignette. Defaults: 1 for confirmatory, 10 for stability "
                         "(N=10 is a proposed default per the protocol doc -- confirm before a real run, it's still marked open)")
parser.add_argument("--temperature", type=float, required=False, default=None,
                    help="sampling temperature. Defaults: 0.1 for confirmatory (doc proposes 0.0-0.2), "
                         "1.0 for stability (doc proposes 1.0 or provider default -- both still need explicit sign-off)")
parser.add_argument("--vignette_file", type=str, required=False, default=None,
                    help="path to the vignette CSV (defaults to <repo_root>/data/vignette_core_set.csv, "
                         "resolved relative to this script's location, not the working directory)")
parser.add_argument("--disable_json_mode", action="store_true",
                    help="skip requesting OpenAI-compatible JSON mode (response_format=json_object). "
                         "Use this if a given model/provider rejects that parameter -- falls back to "
                         "prompt-only JSON compliance, still backstopped by the retry-on-parse-failure loop.")
args = parser.parse_args()

mname = args.model
pass_type = args.pass_type
N_SAMPLES = args.n_samples if args.n_samples is not None else (1 if pass_type == "confirmatory" else 10)
TEMP = args.temperature if args.temperature is not None else (0.1 if pass_type == "confirmatory" else 1.0)
VIGNETTE_FILE = args.vignette_file if args.vignette_file is not None else str(REPO_ROOT / "data" / "vignette_core_set.csv")

RESPONSES_DIR = REPO_ROOT / "responses" / pass_type
RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
OUTFILE = str(RESPONSES_DIR / f"{mname}.csv")

# === load vignettes ===
# expects the actual columns produced by scripts/generate_vignettes.py:
# vignette_id, family_id, family_name, scenario_id, task_object, violation_form,
# agent_gender, partner_gender, relationship_context, severity, intentionality,
# agent_name, partner_name, obligation_source, vignette_text
all_vignettes = pd.read_csv(VIGNETTE_FILE)

REQUIRED_VIGNETTE_COLUMNS = {
    "vignette_id", "family_id", "family_name", "scenario_id", "task_object",
    "violation_form", "agent_gender", "partner_gender", "relationship_context",
    "severity", "intentionality", "agent_name", "partner_name",
    "obligation_source", "vignette_text"
}
missing = REQUIRED_VIGNETTE_COLUMNS - set(all_vignettes.columns)
if missing:
    raise ValueError(f"Vignette file is missing expected columns: {missing}")

# === save responses to csv as you go ===
outfile_handle = open(OUTFILE, 'w', newline='')
writer = csv.writer(outfile_handle)
header = [
    "vignette_id", "model", "pass_type", "temperature", "sample_num",
    "family_id", "family_name", "scenario_id", "task_object", "violation_form",
    "agent_gender", "partner_gender", "relationship_context", "severity",
    "intentionality", "agent_name", "partner_name", "obligation_source",
    "reasoning", "obligation_identified", "fault_rating", "confidence"
]
writer.writerow(header)

if not getenv("OPENROUTER_API_KEY"):
    raise Exception(
        "OPENROUTER_API_KEY not found. Either export it directly "
        "(`export OPENROUTER_API_KEY=<api-key>`) or add it to a `.env` file "
        "in this folder as `OPENROUTER_API_KEY=<api-key>`."
    )

# === collect responses ===

model_kwargs = {} if args.disable_json_mode else {"response_format": {"type": "json_object"}}
model = ChatOpenAI(
    model=models[mname],
    temperature=TEMP,
    openai_api_key=getenv("OPENROUTER_API_KEY"),
    openai_api_base=API_URL,
    model_kwargs=model_kwargs,
)

chain = prompt_template.partial(
    format_instructions=fault_parser.get_format_instructions(),
    additional_format_instructions=additional_format_instructions,
) | model | fault_parser

for _, vrow in all_vignettes.iterrows():
    vignette_id = vrow['vignette_id']
    vignette_text = vrow['vignette_text']
    sample_num = 0
    prompt = vignette_text
    while sample_num < N_SAMPLES:
        try:
            logging.info(f"\tQUERY --- vignette ID: {vignette_id}; family: {vrow['family_name']}; "
                         f"model: {mname}; pass: {pass_type}; sample: {sample_num + 1}/{N_SAMPLES}; "
                         f"text: {str(vignette_text)[:log_max_str_len]}...")
            response = chain.invoke({"vignette": prompt})
        except (OutputParserException, JSONDecodeError) as e:
            # ill-formed output -- flag and retry rather than silently dropping, per the
            # protocol doc's instruction to plan a defined fallback rule for malformed output
            logging.error(f"Ill formed response for vignette {vignette_id}: {e}; trying again")
            prompt = vignette_text + "\nYour output format was incorrect earlier. Please precisely adhere to the JSON format instructions."
            continue
        except TypeError as e:
            if "response_format" in str(e) or "model_kwargs" in str(e):
                raise SystemExit(
                    f"\nModel '{mname}' ({models[mname]}) rejected the response_format/JSON-mode "
                    f"parameter: {e}\nRerun with --disable_json_mode to fall back to prompt-only "
                    f"JSON compliance for this model."
                )
            raise

        sample_num += 1
        logging.info(f"\tRESPONSE --- fault_rating: {response.fault_rating}; confidence: {response.confidence}; obligation_identified: {response.obligation_identified}")
        row = [
            vignette_id, mname, pass_type, TEMP, sample_num,
            vrow['family_id'], vrow['family_name'], vrow['scenario_id'], vrow['task_object'], vrow['violation_form'],
            vrow['agent_gender'], vrow['partner_gender'], vrow['relationship_context'], vrow['severity'],
            vrow['intentionality'], vrow['agent_name'], vrow['partner_name'], vrow['obligation_source'],
            response.reasoning, response.obligation_identified, response.fault_rating, response.confidence
        ]
        writer.writerow(row)
        prompt = vignette_text  # reset prompt for next fresh draw

outfile_handle.close()

# === validate the collected output before wrapping up ===

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import validate_dataframe

logging.info(f"Collection complete. Validating {OUTFILE} ...")
result_df = pd.read_csv(OUTFILE)
n_invalid = validate_dataframe(result_df)
if n_invalid > 0:
    logging.warning(f"{n_invalid} row(s) in {OUTFILE} failed validation -- see messages above.")
else:
    logging.info(f"All {len(result_df)} rows in {OUTFILE} passed validation.")
