import uuid
import json
import logging
from pathlib import Path

from src.doc_extract.pdf.inspect import inspect_pdf
from src.doc_extract.pdf.text_extract import extract_text
from src.doc_extract.pdf.ocr import ocr_seite
from src.doc_extract.prompts.builder import baue_prompt
from src.doc_extract.inference.vllm_client import sende_anfrage
from src.doc_extract.models import ExtractionErgebnis
from src.doc_extract.postprocess.validation import validiere_ergebnis
from src.doc_extract.config import DEFAULT_SCHEMA_PATH

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def extrahiere_json(text: str) -> dict:
    text = text.strip()
    start = text.find("{")
    ende = text.rfind("}") + 1
    if start == -1 or ende == 0:
        raise ValueError(f"Kein JSON gefunden in: {text}")
    return json.loads(text[start:ende])


def _hole_seitentext(pdf_path: Path, seite: dict) -> tuple[str, bool]:
    """
    Gibt (text, ocr_verwendet) zurück.
    - text-Seiten:    pdfplumber-Text
    - bild-Seiten:    OCR-Text
    - gemischt-Seiten: pdfplumber-Text + OCR-Text kombiniert
    - leer-Seiten:    leerer String
    """
    seite_num = seite["seite"]
    typ = seite["typ"]

    if typ == "text":
        return extract_text(pdf_path, seite_num), False

    if typ == "bild":
        ocr_text = ocr_seite(pdf_path, seite_num)
        logger.debug("Seite %d: OCR lieferte %d Zeichen", seite_num, len(ocr_text))
        return ocr_text, True

    if typ == "gemischt":
        digital_text = extract_text(pdf_path, seite_num)
        ocr_text = ocr_seite(pdf_path, seite_num)
        kombiniert = digital_text
        if ocr_text:
            kombiniert += "\n\n[OCR-Ergänzung]\n" + ocr_text
        logger.debug("Seite %d: gemischt — %d digital + %d OCR Zeichen", seite_num, len(digital_text), len(ocr_text))
        return kombiniert, True

    return "", False  # leer


def run_pipeline(pdf_path: Path, schema: dict) -> ExtractionErgebnis:
    if schema is None:
        schema = json.loads(DEFAULT_SCHEMA_PATH.read_text())

    request_id = str(uuid.uuid4())
    seiten_info = inspect_pdf(pdf_path)
    gesammelte_daten = {}
    fehler = []
    retry_count = 0
    seiten_erfolgreich = []
    seiten_fehlgeschlagen = []

    for seite in seiten_info:
        seite_num = seite["seite"]
        gesamt_seiten = len(seiten_info)
        versuch = 0
        letzter_fehler = None

        while versuch < MAX_RETRIES:
            try:
                text, ocr_verwendet = _hole_seitentext(pdf_path, seite)
                prompt = baue_prompt(
                    text=text,
                    schema=schema,
                    seite_num=seite_num,
                    gesamt_seiten=gesamt_seiten,
                    letzter_fehler=letzter_fehler,
                    ocr_verwendet=ocr_verwendet,
                )
                antwort = sende_anfrage(prompt)
                daten = extrahiere_json(antwort)
                gesammelte_daten.update(daten)
                seiten_erfolgreich.append(seite_num)
                retry_count += versuch
                break

            except Exception as e:
                letzter_fehler = str(e)
                versuch += 1
                logger.warning("Seite %d, Versuch %d fehlgeschlagen: %s", seite_num, versuch, e)
                if versuch == MAX_RETRIES:
                    fehler.append(f"Seite {seite_num} nach {MAX_RETRIES} Versuchen fehlgeschlagen: {letzter_fehler}")
                    seiten_fehlgeschlagen.append(seite_num)

    valid, validierungs_fehler = validiere_ergebnis(gesammelte_daten, schema)
    fehler.extend(validierungs_fehler)

    return ExtractionErgebnis(
        request_id=request_id,
        seiten=len(seiten_info),
        valid=valid,
        daten=gesammelte_daten,
        fehler=fehler,
        retry_count=retry_count,
        seiten_erfolgreich=seiten_erfolgreich,
        seiten_fehlgeschlagen=seiten_fehlgeschlagen,
    )
