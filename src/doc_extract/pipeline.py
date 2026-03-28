import uuid
from pathlib import Path
from src.doc_extract.pdf.inspect import inspect_pdf
from src.doc_extract.pdf.text_extract import extract_text
from src.doc_extract.pdf.render import render_seite
from src.doc_extract.prompts.builder import baue_prompt
from src.doc_extract.inference.vllm_client import sende_anfrage
from src.doc_extract.models import ExtractionErgebnis
import json

def run_pipeline(pdf_path: Path, schema: dict) -> ExtractionErgebnis:
    request_id = str(uuid.uuid4())
    seiten_info = inspect_pdf(pdf_path)
    gesammelte_daten = {}
    fehler = []
    retry_count = 0

    for seite in seiten_info:
        seite_num = seite["seite"]

        try:
            text = extract_text(pdf_path, seite_num)
            prompt = baue_prompt(text, schema)
            antwort = sende_anfrage(prompt)
            daten = json.loads(antwort)
            gesammelte_daten.update(daten)

        except Exception as e:
            fehler.append(f"Seite {seite_num}: {str(e)}")

    return ExtractionErgebnis(
        request_id=request_id,
        seiten=len(seiten_info),
        valid=len(fehler) == 0,
        daten=gesammelte_daten,
        fehler=fehler,
        retry_count=retry_count
    )