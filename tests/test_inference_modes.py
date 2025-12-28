import pytest
from pathlib import Path
from chapterize.extract import extract_document_text
from chapterize.candidates import extract_candidates
from chapterize.inference import global_inference

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    pytest.skip("reportlab not installed", allow_module_level=True)

def make_pdf_with_text(text: str, tmp_path: Path, fname: str) -> Path:
    pdf_path = tmp_path / fname
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 700, text)
    c.save()
    return pdf_path

def test_inference_conflicting_modes(tmp_path):
    # Group 1: Arabic numerals
    group1 = [
        ("Chapter 1", "a1.pdf"),
        ("Chapter 2", "a2.pdf"),
        ("Chapter 3", "a3.pdf"),
    ]
    # Group 2: Roman numerals
    group2 = [
        ("CHAPTER I", "b1.pdf"),
        ("CHAPTER II", "b2.pdf"),
        ("CHAPTER III", "b3.pdf"),
    ]
    # Group 3: Dash-numbered
    group3 = [
        ("1 - Intro", "c1.pdf"),
        ("2 - Methods", "c2.pdf"),
        ("3 - Results", "c3.pdf"),
    ]
    files = [make_pdf_with_text(text, tmp_path, fname) for text, fname in group1 + group2 + group3]
    file_candidates = {}
    for f in files:
        text = extract_document_text(f)
        file_candidates[f.name] = extract_candidates(text)
    result = global_inference(file_candidates, {})
    # Check that all files have candidates, but ambiguous status may occur due to conflicting modes
    for fname in [f for _, f in group1 + group2 + group3]:
        info = result[fname]
        assert info["candidates"], f"{fname} should have candidates"
        # If multiple modes present, status should be ambiguous or ok
        assert info["status"] in ("ok", "ambiguous"), f"{fname} unexpected status {info['status']}"
    # Document limitation: current inference does not explicitly warn about conflicting modes
    # Future enhancement: add logic to detect and warn about inconsistent chapter assignment patterns
