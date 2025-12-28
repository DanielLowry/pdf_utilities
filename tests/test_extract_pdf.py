import io
from pathlib import Path
import pytest
from chapterize.extract import extract_first_page_text
from chapterize.candidates import extract_candidates

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    pytest.skip("reportlab not installed", allow_module_level=True)

def make_pdf_with_text(text: str, tmp_path: Path) -> Path:
    pdf_path = tmp_path / "sample.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 700, text)
    c.save()
    return pdf_path

def test_extract_and_candidates(tmp_path):
    # Create a PDF with a known chapter heading
    pdf_path = make_pdf_with_text("Chapter 5", tmp_path)
    text = extract_first_page_text(pdf_path)
    assert text is not None and "Chapter 5" in text
    cands = extract_candidates(text)
    assert any(c[0] == '5' for c in cands)
