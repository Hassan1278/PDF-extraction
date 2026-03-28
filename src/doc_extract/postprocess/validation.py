import json
from jsonschema import validate, ValidationError

def validiere_ergebnis(daten: dict, schema: dict) -> tuple[bool, list[str]]:
    try:
        validate(instance=daten, schema=schema)
        return True, []
    except ValidationError as e:
        return False, [e.message]