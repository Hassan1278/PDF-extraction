import pytest
from src.doc_extract.postprocess.validation import validiere_ergebnis

SCHEMA = {
    "type": "object",
    "properties": {
        "datum": {"type": ["string", "null"]},
        "absender": {"type": "string"},
    },
    "required": ["datum", "absender"],
}


def test_valide_daten():
    daten = {"datum": "01.01.2024", "absender": "Max Mustermann"}
    valid, fehler = validiere_ergebnis(daten, SCHEMA)
    assert valid is True
    assert fehler == []


def test_fehlendes_pflichtfeld():
    daten = {"datum": "01.01.2024"}  # absender fehlt
    valid, fehler = validiere_ergebnis(daten, SCHEMA)
    assert valid is False
    assert len(fehler) == 1


def test_falscher_typ():
    daten = {"datum": 123, "absender": "Max"}  # datum soll string sein
    valid, fehler = validiere_ergebnis(daten, SCHEMA)
    assert valid is False
    assert len(fehler) == 1


def test_datum_darf_null_sein():
    daten = {"datum": None, "absender": "Max"}
    valid, fehler = validiere_ergebnis(daten, SCHEMA)
    assert valid is True
    assert fehler == []


def test_leeres_objekt_schlaegt_fehl():
    valid, fehler = validiere_ergebnis({}, SCHEMA)
    assert valid is False


def test_zusaetzliche_felder_erlaubt():
    daten = {"datum": "01.01.2024", "absender": "Max", "extra": "ignoriert"}
    valid, fehler = validiere_ergebnis(daten, SCHEMA)
    assert valid is True
