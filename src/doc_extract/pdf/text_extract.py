from pathlib import Path
import pdfplumber

def extract_text(pdf_path: Path, seite_num: int) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        seite = pdf.pages[seite_num]
        text = seite.extract_text() or ""
        return text.strip()

def extract_tabellen(pdf_path: Path, seite_num: int) -> list:
    with pdfplumber.open(pdf_path) as pdf:
        seite = pdf.pages[seite_num]
        tabellen = seite.extract_tables() or []
        return tabellen