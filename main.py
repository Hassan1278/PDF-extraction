from pathlib import Path
from src.doc_extract.pdf.inspect import inspect_pdf
from src.doc_extract.pdf.render import render_seite
from src.doc_extract.pdf.text_extract import extract_text, extract_tabellen

ergebnisse = inspect_pdf(Path("sample_pdfs/sample.pdf"))
for e in ergebnisse:
    print(e)

bild_bytes = render_seite(Path("sample_pdfs/sample.pdf"), 0)
Path("output.png").write_bytes(bild_bytes)
print("Bild gespeichert!")

text = extract_text(Path("sample_pdfs/sample.pdf"), 0)
print(text[:200])

tabellen = extract_tabellen(Path("sample_pdfs/sample.pdf"), 0)
print(f"{len(tabellen)} Tabellen gefunden")