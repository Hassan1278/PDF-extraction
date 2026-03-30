from jsonschema import validate, ValidationError


def validate_result(data: dict, schema: dict) -> tuple[bool, list[str]]:
    try:
        validate(instance=data, schema=schema)
        return True, []
    except ValidationError as e:
        return False, [e.message]
