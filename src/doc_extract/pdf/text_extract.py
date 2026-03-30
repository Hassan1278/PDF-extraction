from pathlib import Path
import pdfplumber


def extract_text(pdf_path: Path, page_num: int) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        return (page.extract_text() or "").strip()


def extract_tables(pdf_path: Path, page_num: int) -> list:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        return page.extract_tables() or []
