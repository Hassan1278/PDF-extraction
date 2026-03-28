import json
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from src.doc_extract.pipeline import run_pipeline
from pathlib import Path
import tempfile

app = FastAPI()

class ExtractionRequest(BaseModel):
    schema_dict: dict

@app.post("/extract")
async def extract(
    pdf: UploadFile = File(...),
    schema_json: str = ""
):
    schema_dict = json.loads(schema_json)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await pdf.read())
        tmp_path = Path(tmp.name)

    ergebnis = run_pipeline(tmp_path, schema_dict)

    return {
        "valid": ergebnis.valid,
        "daten": ergebnis.daten,
        "fehler": ergebnis.fehler,
        "seiten": ergebnis.seiten,
        "retry_count": ergebnis.retry_count,
        "seiten_erfolgreich": ergebnis.seiten_erfolgreich,
        "seiten_fehlgeschlagen": ergebnis.seiten_fehlgeschlagen,
    }

@app.get("/health")
def health():
    return {"status": "ok"}