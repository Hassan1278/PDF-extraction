import pytest
from pathlib import Path
from src.doc_extract.pdf.inspect import inspect_pdf, _klassifiziere, _text_abdeckung, _bild_abdeckung

PDF_PATH = Path(__file__).parent.parent / "sample_pdfs" / "test.pdf"


@pytest.fixture(scope="module")
def seiten():
    return inspect_pdf(PDF_PATH)


# --- inspect_pdf: Grundstruktur ---

def test_gibt_liste_zurueck(seiten):
    assert isinstance(seiten, list)
    assert len(seiten) >= 1


def test_seite_hat_pflichtfelder(seiten):
    for seite in seiten:
        for feld in ("seite", "zeichen", "bilder", "typ", "breite", "hoehe",
                     "text_abdeckung", "bild_abdeckung"):
            assert feld in seite, f"Feld '{feld}' fehlt"


def test_seite_index_beginnt_bei_null(seiten):
    assert seiten[0]["seite"] == 0


def test_typ_ist_gueltig(seiten):
    erlaubte_typen = {"text", "bild", "gemischt", "leer"}
    for seite in seiten:
        assert seite["typ"] in erlaubte_typen, f"Unbekannter Typ: {seite['typ']}"


def test_zeichen_nicht_negativ(seiten):
    for seite in seiten:
        assert seite["zeichen"] >= 0


def test_dimensionen_positiv(seiten):
    for seite in seiten:
        assert seite["breite"] > 0
        assert seite["hoehe"] > 0


def test_abdeckung_zwischen_null_und_eins(seiten):
    for seite in seiten:
        assert 0.0 <= seite["text_abdeckung"] <= 1.0
        assert 0.0 <= seite["bild_abdeckung"] <= 1.0


# --- _klassifiziere: Logik ---

def test_klassifiziere_text():
    assert _klassifiziere(text_abdeckung=0.50, bild_abdeckung=0.05) == "text"


def test_klassifiziere_bild():
    assert _klassifiziere(text_abdeckung=0.05, bild_abdeckung=0.80) == "bild"


def test_klassifiziere_gemischt():
    assert _klassifiziere(text_abdeckung=0.40, bild_abdeckung=0.30) == "gemischt"


def test_klassifiziere_leer():
    assert _klassifiziere(text_abdeckung=0.01, bild_abdeckung=0.02) == "leer"


def test_klassifiziere_grenzwert_text():
    # Genau an der Schwelle TEXT_SCHWELLE (0.20) → noch nicht "text"
    assert _klassifiziere(text_abdeckung=0.20, bild_abdeckung=0.0) == "leer"


def test_klassifiziere_grenzwert_bild():
    # Genau an der Schwelle BILD_SCHWELLE (0.15) → noch nicht "bild"
    assert _klassifiziere(text_abdeckung=0.0, bild_abdeckung=0.15) == "leer"
