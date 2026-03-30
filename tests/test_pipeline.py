import json
import pytest
from pathlib import Path
from unittest.mock import patch

from src.doc_extract.pipeline import run_pipeline, extrahiere_json
from src.doc_extract.models import ExtractionErgebnis

PDF_PATH = Path(__file__).parent.parent / "sample_pdfs" / "test.pdf"

SCHEMA = {
    "type": "object",
    "properties": {
        "datum": {"type": ["string", "null"]},
        "absender": {"type": "string"},
    },
    "required": ["datum", "absender"],
}

VALIDE_ANTWORT = json.dumps({"datum": "01.01.2024", "absender": "Test GmbH"})


# --- extrahiere_json ---

def test_extrahiere_json_einfach():
    ergebnis = extrahiere_json('{"name": "Max"}')
    assert ergebnis == {"name": "Max"}


def test_extrahiere_json_mit_text_darum():
    ergebnis = extrahiere_json('Hier ist das JSON: {"name": "Max"} Ende.')
    assert ergebnis == {"name": "Max"}


def test_extrahiere_json_kein_json_wirft_fehler():
    with pytest.raises(ValueError):
        extrahiere_json("Kein JSON hier")


def test_extrahiere_json_ungueltiges_json_wirft_fehler():
    with pytest.raises(Exception):
        extrahiere_json("{ungueltig}")


# --- run_pipeline (sende_anfrage + ocr_seite gemockt) ---

def test_pipeline_gibt_extraction_ergebnis_zurueck():
    with patch("src.doc_extract.pipeline.sende_anfrage", return_value=VALIDE_ANTWORT), \
         patch("src.doc_extract.pipeline.ocr_seite", return_value="OCR Text"):
        ergebnis = run_pipeline(PDF_PATH, SCHEMA)
    assert isinstance(ergebnis, ExtractionErgebnis)


def test_pipeline_valide_antwort():
    with patch("src.doc_extract.pipeline.sende_anfrage", return_value=VALIDE_ANTWORT), \
         patch("src.doc_extract.pipeline.ocr_seite", return_value="OCR Text"):
        ergebnis = run_pipeline(PDF_PATH, SCHEMA)
    assert ergebnis.valid is True
    assert ergebnis.fehler == []


def test_pipeline_daten_enthalten_felder():
    with patch("src.doc_extract.pipeline.sende_anfrage", return_value=VALIDE_ANTWORT), \
         patch("src.doc_extract.pipeline.ocr_seite", return_value="OCR Text"):
        ergebnis = run_pipeline(PDF_PATH, SCHEMA)
    assert "datum" in ergebnis.daten
    assert "absender" in ergebnis.daten


def test_pipeline_hat_request_id():
    with patch("src.doc_extract.pipeline.sende_anfrage", return_value=VALIDE_ANTWORT), \
         patch("src.doc_extract.pipeline.ocr_seite", return_value="OCR Text"):
        ergebnis = run_pipeline(PDF_PATH, SCHEMA)
    assert ergebnis.request_id != ""


def test_pipeline_invalide_antwort_setzt_valid_false():
    ungueltige_antwort = json.dumps({"datum": "01.01.2024"})  # absender fehlt
    with patch("src.doc_extract.pipeline.sende_anfrage", return_value=ungueltige_antwort), \
         patch("src.doc_extract.pipeline.ocr_seite", return_value=""):
        ergebnis = run_pipeline(PDF_PATH, SCHEMA)
    assert ergebnis.valid is False
    assert len(ergebnis.fehler) > 0


def test_pipeline_fehler_bei_api_ausfall():
    with patch("src.doc_extract.pipeline.sende_anfrage", side_effect=Exception("Verbindung fehlgeschlagen")), \
         patch("src.doc_extract.pipeline.ocr_seite", return_value=""):
        ergebnis = run_pipeline(PDF_PATH, SCHEMA)
    assert len(ergebnis.seiten_fehlgeschlagen) > 0


def test_pipeline_retry_count_bei_fehler():
    with patch("src.doc_extract.pipeline.sende_anfrage", side_effect=Exception("Fehler")), \
         patch("src.doc_extract.pipeline.ocr_seite", return_value=""):
        ergebnis = run_pipeline(PDF_PATH, SCHEMA)
    assert ergebnis.retry_count == 0
    assert len(ergebnis.seiten_fehlgeschlagen) >= 1
