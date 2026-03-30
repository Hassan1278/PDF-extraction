import io
import logging
from pathlib import Path

from PIL import Image

from src.doc_extract.pdf.render import render_page

logger = logging.getLogger(__name__)

_reader = None


def _get_reader():
    """Lazy singleton — loads easyocr models once on first use."""
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(["de", "en"], verbose=False)
    return _reader


def ocr_page(pdf_path: Path, page_num: int) -> str:
    """
    Renders a PDF page and extracts text via easyocr.
    Returns an empty string if OCR fails.
    """
    try:
        image_bytes = render_page(pdf_path, page_num)
        image = Image.open(io.BytesIO(image_bytes))
        results = _get_reader().readtext(image)
        return " ".join(text for _, text, _ in results).strip()
    except Exception as e:
        logger.warning("OCR failed on page %d: %s", page_num, e)
        return ""
