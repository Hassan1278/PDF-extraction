from pathlib import Path
import pdfplumber

TEXT_THRESHOLD = 0.20
IMAGE_THRESHOLD = 0.15
MIN_TEXT_CHARS = 50  # fallback: sparse layouts can have low coverage but real text


def _text_coverage(page) -> float:
    words = page.extract_words()
    if not words:
        return 0.0
    page_area = page.width * page.height
    if page_area == 0:
        return 0.0
    text_area = sum((w["x1"] - w["x0"]) * (w["bottom"] - w["top"]) for w in words)
    return min(text_area / page_area, 1.0)


def _image_coverage(page) -> float:
    images = page.images
    if not images:
        return 0.0
    page_area = page.width * page.height
    if page_area == 0:
        return 0.0
    image_area = sum(abs(img["x1"] - img["x0"]) * abs(img["y1"] - img["y0"]) for img in images)
    return min(image_area / page_area, 1.0)


def _classify(text_coverage: float, image_coverage: float) -> str:
    has_text = text_coverage > TEXT_THRESHOLD
    has_image = image_coverage > IMAGE_THRESHOLD

    if has_text and has_image:
        return "mixed"
    if has_text:
        return "text"
    if has_image:
        return "image"
    return "empty"


def inspect_pdf(pdf_path: Path) -> list[dict]:
    results = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text_cov = _text_coverage(page)
            image_cov = _image_coverage(page)
            page_type = _classify(text_cov, image_cov)
            chars = len((page.extract_text() or "").strip())

            # Coverage underestimates sparse layouts (short invoices, forms).
            # If pdfplumber found significant chars, treat as text regardless.
            if page_type == "empty" and chars >= MIN_TEXT_CHARS:
                page_type = "text"

            results.append({
                "page": i,
                "chars": chars,
                "images": len(page.images),
                "width": page.width,
                "height": page.height,
                "text_coverage": round(text_cov, 3),
                "image_coverage": round(image_cov, 3),
                "page_type": page_type,
            })

    return results
