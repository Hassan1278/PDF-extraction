import json
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile

from src.doc_extract.pipeline import run_pipeline

app = FastAPI()


@app.post("/extract")
async def extract(
    pdf: UploadFile = File(...),
    schema_json: str = "",
):
    schema = json.loads(schema_json)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(await pdf.read())
        tmp_path = Path(tmp.name)

    result = run_pipeline(tmp_path, schema)

    return {
        "valid": result.valid,
        "data": result.data,
        "errors": result.errors,
        "pages": result.pages,
        "retry_count": result.retry_count,
        "pages_succeeded": result.pages_succeeded,
        "pages_failed": result.pages_failed,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
