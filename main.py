from pathlib import Path
from src.doc_extract.pdf.inspect import inspect_pdf

ergebnisse = inspect_pdf(Path("sample_pdfs/sample.pdf"))
for e in ergebnisse:
    print(e)