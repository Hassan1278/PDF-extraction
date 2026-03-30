from pathlib import Path
import fitz


def render_page(pdf_path: Path, page_num: int, scale: float = 2.0) -> bytes:
    with fitz.open(pdf_path) as doc:
        page = doc[page_num]
        matrix = fitz.Matrix(scale, scale)
        image = page.get_pixmap(matrix=matrix)
        return image.tobytes("png")
