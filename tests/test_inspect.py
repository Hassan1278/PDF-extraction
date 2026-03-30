import pytest
from pathlib import Path
from src.doc_extract.pdf.inspect import inspect_pdf, _classify, TEXT_THRESHOLD, IMAGE_THRESHOLD

PDF_PATH = Path(__file__).parent.parent / "sample_pdfs" / "test.pdf"


@pytest.fixture(scope="module")
def pages():
    return inspect_pdf(PDF_PATH)


# --- inspect_pdf: structure ---

def test_returns_list(pages):
    assert isinstance(pages, list)
    assert len(pages) >= 1


def test_page_has_required_fields(pages):
    for page in pages:
        for field in ("page", "chars", "images", "page_type", "width", "height",
                      "text_coverage", "image_coverage"):
            assert field in page, f"Missing field: '{field}'"


def test_page_index_starts_at_zero(pages):
    assert pages[0]["page"] == 0


def test_page_type_is_valid(pages):
    valid_types = {"text", "image", "mixed", "empty"}
    for page in pages:
        assert page["page_type"] in valid_types, f"Unknown type: {page['page_type']}"


def test_chars_non_negative(pages):
    for page in pages:
        assert page["chars"] >= 0


def test_dimensions_positive(pages):
    for page in pages:
        assert page["width"] > 0
        assert page["height"] > 0


def test_coverage_between_zero_and_one(pages):
    for page in pages:
        assert 0.0 <= page["text_coverage"] <= 1.0
        assert 0.0 <= page["image_coverage"] <= 1.0


# --- _classify: logic ---

def test_classify_text():
    assert _classify(text_coverage=0.50, image_coverage=0.05) == "text"


def test_classify_image():
    assert _classify(text_coverage=0.05, image_coverage=0.80) == "image"


def test_classify_mixed():
    assert _classify(text_coverage=0.40, image_coverage=0.30) == "mixed"


def test_classify_empty():
    assert _classify(text_coverage=0.01, image_coverage=0.02) == "empty"


def test_classify_at_text_threshold():
    assert _classify(text_coverage=TEXT_THRESHOLD, image_coverage=0.0) == "empty"


def test_classify_at_image_threshold():
    assert _classify(text_coverage=0.0, image_coverage=IMAGE_THRESHOLD) == "empty"
