from pathlib import Path
import pdfplumber


# Schwellwerte für die Flächenklassifikation
TEXT_SCHWELLE = 0.20   # >20% der Seite mit Text → text-relevant
BILD_SCHWELLE = 0.15   # >15% der Seite mit Bildern → bild-relevant


def _text_abdeckung(seite) -> float:
    """Anteil der Seitenfläche, der von Wort-Bounding-Boxes bedeckt wird."""
    woerter = seite.extract_words()
    if not woerter:
        return 0.0
    seiten_flaeche = seite.width * seite.height
    if seiten_flaeche == 0:
        return 0.0
    text_flaeche = sum(
        (w["x1"] - w["x0"]) * (w["bottom"] - w["top"]) for w in woerter
    )
    return min(text_flaeche / seiten_flaeche, 1.0)


def _bild_abdeckung(seite) -> float:
    """Anteil der Seitenfläche, der von Bild-Bounding-Boxes bedeckt wird."""
    bilder = seite.images
    if not bilder:
        return 0.0
    seiten_flaeche = seite.width * seite.height
    if seiten_flaeche == 0:
        return 0.0
    bild_flaeche = sum(
        abs(b["x1"] - b["x0"]) * abs(b["y1"] - b["y0"]) for b in bilder
    )
    return min(bild_flaeche / seiten_flaeche, 1.0)


def _klassifiziere(text_abdeckung: float, bild_abdeckung: float) -> str:
    hat_text = text_abdeckung > TEXT_SCHWELLE
    hat_bild = bild_abdeckung > BILD_SCHWELLE

    if hat_text and hat_bild:
        return "gemischt"
    if hat_text:
        return "text"
    if hat_bild:
        return "bild"
    return "leer"


def inspect_pdf(pdf_path: Path) -> list[dict]:
    ergebnisse = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, seite in enumerate(pdf.pages):
            text_abdeckung = _text_abdeckung(seite)
            bild_abdeckung = _bild_abdeckung(seite)
            typ = _klassifiziere(text_abdeckung, bild_abdeckung)

            ergebnisse.append({
                "seite": i,
                "zeichen": len((seite.extract_text() or "").strip()),
                "bilder": len(seite.images),
                "breite": seite.width,
                "hoehe": seite.height,
                "text_abdeckung": round(text_abdeckung, 3),
                "bild_abdeckung": round(bild_abdeckung, 3),
                "typ": typ,
            })

    return ergebnisse
