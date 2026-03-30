import json
import pytest
from src.doc_extract.prompts.builder import baue_prompt

SCHEMA = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}


def test_prompt_enthaelt_schema():
    prompt = baue_prompt("Hallo Welt", SCHEMA, seite_num=0, gesamt_seiten=1)
    assert json.dumps(SCHEMA, indent=2) in prompt


def test_prompt_enthaelt_text():
    prompt = baue_prompt("Mein Testtext", SCHEMA, seite_num=0, gesamt_seiten=1)
    assert "Mein Testtext" in prompt


def test_prompt_seitennummer():
    prompt = baue_prompt("Text", SCHEMA, seite_num=2, gesamt_seiten=5)
    assert "Seite 3 von 5" in prompt


def test_fehler_hinweis_erscheint():
    prompt = baue_prompt("Text", SCHEMA, seite_num=0, gesamt_seiten=1, letzter_fehler="JSON ungültig")
    assert "JSON ungültig" in prompt


def test_kein_fehler_hinweis_ohne_fehler():
    prompt = baue_prompt("Text", SCHEMA, seite_num=0, gesamt_seiten=1)
    assert "letzter Versuch" not in prompt


def test_ocr_hinweis_erscheint_wenn_ocr_verwendet():
    prompt = baue_prompt("Text", SCHEMA, seite_num=0, gesamt_seiten=1, ocr_verwendet=True)
    assert "OCR" in prompt


def test_kein_ocr_hinweis_ohne_ocr():
    prompt = baue_prompt("Text", SCHEMA, seite_num=0, gesamt_seiten=1, ocr_verwendet=False)
    assert "OCR" not in prompt
