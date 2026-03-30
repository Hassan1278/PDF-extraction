import json
from src.doc_extract.prompts.builder import build_prompt

SCHEMA = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}


def test_prompt_contains_schema():
    prompt = build_prompt("Hello World", SCHEMA, page_num=0, total_pages=1)
    assert json.dumps(SCHEMA, indent=2) in prompt


def test_prompt_contains_text():
    prompt = build_prompt("My test text", SCHEMA, page_num=0, total_pages=1)
    assert "My test text" in prompt


def test_prompt_page_number():
    prompt = build_prompt("Text", SCHEMA, page_num=2, total_pages=5)
    assert "page 3 of 5" in prompt


def test_error_hint_appears():
    prompt = build_prompt("Text", SCHEMA, page_num=0, total_pages=1, last_error="Invalid JSON")
    assert "Invalid JSON" in prompt


def test_no_error_hint_without_error():
    prompt = build_prompt("Text", SCHEMA, page_num=0, total_pages=1)
    assert "last attempt" not in prompt


def test_ocr_hint_appears_when_ocr_used():
    prompt = build_prompt("Text", SCHEMA, page_num=0, total_pages=1, ocr_used=True)
    assert "OCR" in prompt


def test_no_ocr_hint_without_ocr():
    prompt = build_prompt("Text", SCHEMA, page_num=0, total_pages=1, ocr_used=False)
    assert "OCR" not in prompt
