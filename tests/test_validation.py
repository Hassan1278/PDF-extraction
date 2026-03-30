from src.doc_extract.postprocess.validation import validate_result

SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": ["string", "null"]},
        "sender": {"type": "string"},
    },
    "required": ["date", "sender"],
}


def test_valid_data():
    data = {"date": "01.01.2024", "sender": "Jane Smith"}
    valid, errors = validate_result(data, SCHEMA)
    assert valid is True
    assert errors == []


def test_missing_required_field():
    data = {"date": "01.01.2024"}  # sender missing
    valid, errors = validate_result(data, SCHEMA)
    assert valid is False
    assert len(errors) == 1


def test_wrong_type():
    data = {"date": 123, "sender": "Jane"}  # date should be string
    valid, errors = validate_result(data, SCHEMA)
    assert valid is False
    assert len(errors) == 1


def test_date_can_be_null():
    data = {"date": None, "sender": "Jane"}
    valid, errors = validate_result(data, SCHEMA)
    assert valid is True
    assert errors == []


def test_empty_object_fails():
    valid, errors = validate_result({}, SCHEMA)
    assert valid is False


def test_extra_fields_allowed():
    data = {"date": "01.01.2024", "sender": "Jane", "extra": "ignored"}
    valid, errors = validate_result(data, SCHEMA)
    assert valid is True
