from pathlib import Path
import pdfplumber

def inspect_pdf(pdf_path: Path) -> list[dict]:
    ergebnisse = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, seite in enumerate(pdf.pages):
            text = seite.extract_text() or ""
            zeichen = len(text.strip())
            bilder = len(seite.images)

            if zeichen >= 200 and bilder == 0:
                typ = "text"
            elif bilder > 0 and zeichen < 20:
                typ = "bild"
            elif zeichen >= 70 and bilder > 0:
                typ = "gemischt"
            else:
                typ = "leer"

            ergebnisse.append({
                "seite": i,
                "zeichen": zeichen,
                "bilder": bilder,
                "breite": seite.width,
                "hoehe": seite.height,
                "typ": typ,
            })

    return ergebnisse