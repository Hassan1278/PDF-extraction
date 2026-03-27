from pathlib import Path
import fitz

def render_seite(pdf_path: Path, seite_num: int, matrix: float = 2.0) -> bytes:
    doc = fitz.open(pdf_path)
    seite = doc[seite_num]
    
    m = fitz.Matrix(matrix, matrix)
    bild = seite.get_pixmap(matrix=m)
    
    return bild.tobytes("png")