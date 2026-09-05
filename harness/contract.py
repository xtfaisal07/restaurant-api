from pathlib import Path
import yaml

from openapi_spec_validator import validate_spec
from jsonschema import Draft202012Validator, RefResolver

BASE_DIR = Path(__file__).resolve().parent.parent
SPEC_FILE = BASE_DIR / "openapi.yaml"

with open(SPEC_FILE, "r") as f:
    SPEC = yaml.safe_load(f)

# Validate OpenAPI document itself
validate_spec(SPEC)

resolver = RefResolver.from_schema(SPEC)

def load_spec():
    return SPEC

def validate_body(schema_name, body):
    schema = SPEC["components"]["schemas"][schema_name]

    Draft202012Validator(
        schema,
        resolver=resolver
    ).validate(body)

    return True