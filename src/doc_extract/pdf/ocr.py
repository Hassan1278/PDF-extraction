import io
import logging
from pathlib import Path

import pytesseract
from PIL import Image

from src.doc_extract.pdf.render import render_seite

logger = logging.getLogger(__name__)

# Auf Windows: Pfad zu tesseract.exe anpassen falls nicht im PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_seite(pdf_path: Path, seite_num: int, sprachen: str = "deu+eng") -> str:
    """
    Rendert eine PDF-Seite und extrahiert Text via Tesseract OCR.
    Gibt leeren String zurück wenn OCR fehlschlägt.
    """
    try:
        bild_bytes = render_seite(pdf_path, seite_num)
        bild = Image.open(io.BytesIO(bild_bytes))
        text = pytesseract.image_to_string(bild, lang=sprachen)
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        logger.error("Tesseract nicht gefunden. Bitte installieren: https://github.com/UB-Mannheim/tesseract/wiki")
        raise
    except Exception as e:
        logger.warning("OCR auf Seite %d fehlgeschlagen: %s", seite_num, e)
        return ""
