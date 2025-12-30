import io
from pathlib import Path
import pytest
from chapterize.extract import extract_document_text
from chapterize.candidates import extract_candidates

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    pytest.skip("reportlab not installed", allow_module_level=True)

def make_pdf_with_pages(texts: list[str], tmp_path: Path) -> Path:
    pdf_path = tmp_path / "sample.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    for text in texts:
        c.drawString(100, 700, text)
        c.showPage()
    c.save()
    return pdf_path

def test_extract_and_candidates(tmp_path):
    # Create a PDF with a known chapter heading
    pdf_path = make_pdf_with_pages(["Chapter 5", "Chapter 6 extra"], tmp_path)
    text = extract_document_text(pdf_path)
    assert text is not None and "Chapter 5" in text
    cands = extract_candidates(text)
    assert any(c[0] == '5' for c in cands)


def test_extract_document_text_includes_all_pages(tmp_path):
    pdf_path = make_pdf_with_pages(["Chapter 1", "Chapter 2 second page"], tmp_path)
    text = extract_document_text(pdf_path)
    assert text is not None
    assert "Chapter 2" in text
