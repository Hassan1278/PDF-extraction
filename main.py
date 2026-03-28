from src.doc_extract.pipeline import run_pipeline
from pathlib import Path

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "datum": {
            "type": "string",
            "description": "Datum im Format DD.MM.YYYY"
        }
    },
    "required": ["name", "datum"]
}

ergebnis = run_pipeline(Path("sample_pdfs/test.pdf"), schema)
print(ergebnis)