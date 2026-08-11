import pandas as pd
from pydantic import BaseModel, field_validator, ValidationError

# === Define the schema for one row of a responses/<pass_type>/<model>.csv file ===
class ResponseRowSchema(BaseModel):
    vignette_id: str
    model: str
    pass_type: str
    temperature: float
    sample_num: int
    family_id: str
    family_name: str
    scenario_id: str
    task_object: str
    violation_form: str
    agent_gender: str
    partner_gender: str
    relationship_context: str
    severity: str
    intentionality: str
    agent_name: str
    partner_name: str
    obligation_source: str
    reasoning: str
    obligation_identified: str
    fault_rating: int
    confidence: int

    @field_validator('pass_type')
    @classmethod
    def check_pass_type(cls, v):
        allowed = {'confirmatory', 'stability'}
        if v not in allowed:
            raise ValueError(f"pass_type must be one of {allowed}, got '{v}'")
        return v

    @field_validator('agent_gender', 'partner_gender')
    @classmethod
    def check_gender(cls, v):
        # matches the actual values in data/vignette_core_set.csv: 'M', 'F'
        allowed = {'M', 'F'}
        if v not in allowed:
            raise ValueError(f"gender must be one of {allowed}, got '{v}'")
        return v

    @field_validator('severity')
    @classmethod
    def check_severity(cls, v):
        # matches data/vignette_core_set.csv: 'MLD' (mild), 'SEV' (severe)
        allowed = {'MLD', 'SEV'}
        if v not in allowed:
            raise ValueError(f"severity must be one of {allowed}, got '{v}'")
        return v

    @field_validator('intentionality')
    @classmethod
    def check_intentionality(cls, v):
        # currently fixed to a single value per docs/prompt_and_measurement_protocol.md
        # and project/project_status_summary.md -- update this set if the design ever crosses it again
        allowed = {'knowing_but_nonmalicious'}
        if v not in allowed:
            raise ValueError(f"intentionality must be one of {allowed}, got '{v}'")
        return v

    @field_validator('fault_rating')
    @classmethod
    def check_fault_rating(cls, v):
        if not (0 <= v <= 7):
            raise ValueError(f"fault_rating must be between 0 and 7, got {v}")
        return v

    @field_validator('confidence')
    @classmethod
    def check_confidence(cls, v):
        if not (0 <= v <= 100):
            raise ValueError(f"confidence must be between 0 and 100, got {v}")
        return v

    @field_validator('temperature')
    @classmethod
    def check_temperature(cls, v):
        if not (0.0 <= v <= 2.0):
            raise ValueError(f"temperature must be between 0.0 and 2.0, got {v}")
        return v


REQUIRED_COLUMNS = {
    "vignette_id", "model", "pass_type", "temperature", "sample_num",
    "family_id", "family_name", "scenario_id", "task_object", "violation_form",
    "agent_gender", "partner_gender", "relationship_context", "severity",
    "intentionality", "agent_name", "partner_name", "obligation_source",
    "reasoning", "obligation_identified", "fault_rating", "confidence"
}


def validate_dataframe(df: pd.DataFrame) -> int:
    """Validate a responses dataframe against the expected schema.
    Returns the number of invalid rows found (0 = all rows valid)."""

    if set(df.columns) != REQUIRED_COLUMNS:
        missing = REQUIRED_COLUMNS - set(df.columns)
        extra = set(df.columns) - REQUIRED_COLUMNS
        raise ValueError(
            f"DataFrame columns do not match expected schema.\n"
            f"Missing: {missing or 'none'}\nUnexpected: {extra or 'none'}"
        )

    n_invalid = 0
    for idx, row in df.iterrows():
        try:
            ResponseRowSchema(
                vignette_id=row['vignette_id'],
                model=row['model'],
                pass_type=row['pass_type'],
                temperature=row['temperature'],
                sample_num=row['sample_num'],
                family_id=row['family_id'],
                family_name=row['family_name'],
                scenario_id=row['scenario_id'],
                task_object=row['task_object'],
                violation_form=row['violation_form'],
                agent_gender=row['agent_gender'],
                partner_gender=row['partner_gender'],
                relationship_context=row['relationship_context'],
                severity=row['severity'],
                intentionality=row['intentionality'],
                agent_name=row['agent_name'],
                partner_name=row['partner_name'],
                obligation_source=row['obligation_source'],
                reasoning=row['reasoning'],
                obligation_identified=row['obligation_identified'],
                fault_rating=row['fault_rating'],
                confidence=row['confidence'],
            )
        except ValidationError as e:
            print(f"Row {idx} (vignette_id={row.get('vignette_id')}) is invalid: {e}")
            n_invalid += 1

    if n_invalid == 0:
        print(f"All {len(df)} rows passed validation.")
    else:
        print(f"{n_invalid} of {len(df)} rows failed validation.")
    return n_invalid


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="path to a responses CSV to validate, e.g. ../responses/confirmatory/claude_sonnet.csv (relative to this script's location if run from scripts/, or responses/confirmatory/claude_sonnet.csv if run from the repo root)")
    args = parser.parse_args()

    df = pd.read_csv(args.file)
    validate_dataframe(df)
