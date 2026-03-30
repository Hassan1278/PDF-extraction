from src.doc_extract.pipeline import run_pipeline
from pathlib import Path

result = run_pipeline(Path("sample_pdfs/test.pdf"), schema=None)
print(result)
