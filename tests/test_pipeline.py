import json
import pytest
from pathlib import Path
from unittest.mock import patch

from src.doc_extract.pipeline import run_pipeline, extract_json
from src.doc_extract.models import ExtractionResult

PDF_PATH = Path(__file__).parent.parent / "sample_pdfs" / "test.pdf"

SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": ["string", "null"]},
        "sender": {"type": "string"},
    },
    "required": ["date", "sender"],
}

VALID_RESPONSE = json.dumps({"date": "01.01.2024", "sender": "Test Corp"})


# --- extract_json ---

def test_extract_json_simple():
    assert extract_json('{"name": "Jane"}') == {"name": "Jane"}


def test_extract_json_with_surrounding_text():
    assert extract_json('Here is the JSON: {"name": "Jane"} Done.') == {"name": "Jane"}


def test_extract_json_no_json_raises():
    with pytest.raises(ValueError):
        extract_json("No JSON here")


def test_extract_json_invalid_json_raises():
    with pytest.raises(Exception):
        extract_json("{invalid}")


# --- run_pipeline ---

def test_pipeline_returns_extraction_result():
    with patch("src.doc_extract.pipeline.send_request", return_value=VALID_RESPONSE), \
         patch("src.doc_extract.pipeline.ocr_page", return_value="OCR text"):
        result = run_pipeline(PDF_PATH, SCHEMA)
    assert isinstance(result, ExtractionResult)


def test_pipeline_valid_response():
    with patch("src.doc_extract.pipeline.send_request", return_value=VALID_RESPONSE), \
         patch("src.doc_extract.pipeline.ocr_page", return_value="OCR text"):
        result = run_pipeline(PDF_PATH, SCHEMA)
    assert result.valid is True
    assert result.errors == []


def test_pipeline_data_contains_fields():
    with patch("src.doc_extract.pipeline.send_request", return_value=VALID_RESPONSE), \
         patch("src.doc_extract.pipeline.ocr_page", return_value="OCR text"):
        result = run_pipeline(PDF_PATH, SCHEMA)
    assert "date" in result.data
    assert "sender" in result.data


def test_pipeline_has_request_id():
    with patch("src.doc_extract.pipeline.send_request", return_value=VALID_RESPONSE), \
         patch("src.doc_extract.pipeline.ocr_page", return_value="OCR text"):
        result = run_pipeline(PDF_PATH, SCHEMA)
    assert result.request_id != ""


def test_pipeline_invalid_response_sets_valid_false():
    invalid_response = json.dumps({"date": "01.01.2024"})  # sender missing
    with patch("src.doc_extract.pipeline.send_request", return_value=invalid_response), \
         patch("src.doc_extract.pipeline.ocr_page", return_value=""):
        result = run_pipeline(PDF_PATH, SCHEMA)
    assert result.valid is False
    assert len(result.errors) > 0


def test_pipeline_api_failure():
    with patch("src.doc_extract.pipeline.send_request", side_effect=Exception("Connection failed")), \
         patch("src.doc_extract.pipeline.ocr_page", return_value=""):
        result = run_pipeline(PDF_PATH, SCHEMA)
    assert len(result.pages_failed) > 0


def test_pipeline_retry_count_on_failure():
    with patch("src.doc_extract.pipeline.send_request", side_effect=Exception("Error")), \
         patch("src.doc_extract.pipeline.ocr_page", return_value=""):
        result = run_pipeline(PDF_PATH, SCHEMA)
    assert result.retry_count == 0
    assert len(result.pages_failed) >= 1
