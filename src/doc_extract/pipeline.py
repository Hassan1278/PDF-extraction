import uuid
import json
import logging
from pathlib import Path

from src.doc_extract.pdf.inspect import inspect_pdf
from src.doc_extract.pdf.text_extract import extract_text
from src.doc_extract.pdf.ocr import ocr_page
from src.doc_extract.prompts.builder import build_prompt
from src.doc_extract.inference.vllm_client import send_request
from src.doc_extract.models import ExtractionResult
from src.doc_extract.postprocess.validation import validate_result
from src.doc_extract.config import DEFAULT_SCHEMA_PATH

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
MIN_DIGITAL_CHARS = 100


def extract_json(text: str) -> dict:
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON found in: {text}")
    return json.loads(text[start:end])


def _get_page_text(pdf_path: Path, page: dict) -> tuple[str, bool]:
    """
    Returns (text, ocr_used).
    - text pages:   pdfplumber text
    - image/mixed:  pdfplumber if enough digital text, otherwise OCR
    - empty pages:  empty string
    """
    page_num = page["page"]
    page_type = page["page_type"]

    if page_type == "text":
        return extract_text(pdf_path, page_num), False

    if page_type in ["image", "mixed"]:
        digital_text = extract_text(pdf_path, page_num)
        if len(digital_text) >= MIN_DIGITAL_CHARS:
            logger.debug("Page %d: digital text sufficient (%d chars), skipping OCR", page_num, len(digital_text))
            return digital_text, False
        ocr_text = ocr_page(pdf_path, page_num)
        logger.debug("Page %d: OCR returned %d chars", page_num, len(ocr_text))
        combined = (digital_text + "\n\n[OCR supplement]\n" + ocr_text).strip() if digital_text else ocr_text
        return combined, True

    return "", False  # empty


def run_pipeline(pdf_path: Path, schema: dict | None) -> ExtractionResult:
    if schema is None:
        schema = json.loads(DEFAULT_SCHEMA_PATH.read_text())

    request_id = str(uuid.uuid4())
    pages_info = inspect_pdf(pdf_path)
    collected_data: dict = {}
    errors: list[str] = []
    retry_count = 0
    pages_succeeded: list[int] = []
    pages_failed: list[int] = []

    for page in pages_info:
        page_num = page["page"]
        total_pages = len(pages_info)
        attempt = 0
        last_error = None

        while attempt < MAX_RETRIES:
            try:
                text, ocr_used = _get_page_text(pdf_path, page)
                prompt = build_prompt(
                    text=text,
                    schema=schema,
                    page_num=page_num,
                    total_pages=total_pages,
                    last_error=last_error,
                    ocr_used=ocr_used,
                )
                response = send_request(prompt, schema=schema)
                data = json.loads(response)
                collected_data.update(data)
                pages_succeeded.append(page_num)
                retry_count += attempt
                break

            except Exception as e:
                last_error = str(e)
                attempt += 1
                logger.warning("Page %d, attempt %d failed: %s", page_num, attempt, e)
                if attempt == MAX_RETRIES:
                    errors.append(f"Page {page_num} failed after {MAX_RETRIES} attempts: {last_error}")
                    pages_failed.append(page_num)

    valid, validation_errors = validate_result(collected_data, schema)
    errors.extend(validation_errors)

    return ExtractionResult(
        request_id=request_id,
        pages=len(pages_info),
        valid=valid,
        data=collected_data,
        errors=errors,
        retry_count=retry_count,
        pages_succeeded=pages_succeeded,
        pages_failed=pages_failed,
    )
