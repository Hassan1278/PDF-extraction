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

def run_pipeline(pdf_path: Path, schema: dict) -> ExtractionErgebnis:
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

        try:
            text = extract_text(pdf_path, seite_num)
            bild_bytes = render_seite(pdf_path, seite_num)
            bild_base64 = base64.b64encode(bild_bytes).decode("utf-8")

            prompt = baue_prompt(
                text=text,
                schema=schema,
                seite_num=seite_num,
                gesamt_seiten=gesamt_seiten
            )

            antwort = sende_anfrage(prompt)
            daten = json.loads(antwort)
            gesammelte_daten.update(daten)
            seiten_erfolgreich.append(seite_num)

        except Exception as e:
            fehler.append(f"Seite {seite_num}: {str(e)}")
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