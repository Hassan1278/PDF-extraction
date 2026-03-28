import uuid
import json
import base64
from pathlib import Path
from src.doc_extract.pdf.inspect import inspect_pdf
from src.doc_extract.pdf.text_extract import extract_text
from src.doc_extract.pdf.render import render_seite
from src.doc_extract.prompts.builder import baue_prompt
from src.doc_extract.inference.vllm_client import sende_anfrage
from src.doc_extract.models import ExtractionErgebnis
from src.doc_extract.postprocess.validation import validiere_ergebnis
from src.doc_extract.config import DEFAULT_SCHEMA_PATH

def extrahiere_json(text: str) -> dict:
    text = text.strip()
    start = text.find("{")
    ende = text.rfind("}") + 1
    if start == -1 or ende == 0:
        raise ValueError(f"Kein JSON gefunden in: {text}")
    return json.loads(text[start:ende])

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

    MAX_RETRIES = 3

    for seite in seiten_info:
        seite_num = seite["seite"]
        gesamt_seiten = len(seiten_info)
        versuch = 0
        letzter_fehler = None
        while versuch < MAX_RETRIES:
            try:
                text = extract_text(pdf_path, seite_num)

                prompt = baue_prompt(
                    text=text,
                    schema=schema,
                    seite_num=seite_num,
                    gesamt_seiten=gesamt_seiten,
                    letzter_fehler=letzter_fehler
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
        seiten_fehlgeschlagen=seiten_fehlgeschlagen
    )
    
