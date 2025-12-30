import pytest
from pathlib import Path
from chapterize.extract import extract_document_text
from chapterize.candidates import extract_candidates
from chapterize.inference import global_inference
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def make_pdf_with_text(text: str, tmp_path: Path, fname: str) -> Path:
    pdf_path = tmp_path / fname
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    y = 700
    for line in text.splitlines() or [""]:
        c.drawString(100, y, line)
        y -= 20
    c.save()
    return pdf_path

def test_inference_multiple_pdfs_robust(tmp_path):
    # Create a diverse set of PDFs
    pdf_specs = [
        ("Chapter 1", "a.pdf", "1"),
        ("CHAPTER II", "b.pdf", "2"),
        ("2. Introduction", "c.pdf", "2"),
        ("No chapter here", "d.pdf", None),
        ("Chapter 1", "e.pdf", "1"),
        ("III. Advanced", "f.pdf", "3"),
        ("5 - Results", "g.pdf", "5"),
        ("Random text", "h.pdf", None),
        ("Ch. 4", "i.pdf", "4"),
        ("1", "j.pdf", "1"),
        ("Chapter X", "k.pdf", "10"),
        ("Chapter 1\nChapter 2", "l.pdf", "1"),  # Multiple chapters, should pick top
        ("", "m.pdf", None),  # Empty
    ]
    files = [make_pdf_with_text(text, tmp_path, fname) for text, fname, _ in pdf_specs]
    file_candidates = {}
    for idx, f in enumerate(files):
        text = extract_document_text(f)
        file_candidates[f.name] = extract_candidates(text)
    # Simulate filename chapters for a few files
    filename_chapters = {"a.pdf": "1", "b.pdf": "2", "k.pdf": "10"}
    result = global_inference(file_candidates, filename_chapters)
    # Assert correct best candidate and status for each file
    for idx, (text, fname, expected) in enumerate(pdf_specs):
        info = result[fname]
        if expected is None:
            assert info["status"] == "none", f"{fname} should be none, got {info['status']}"
            assert info["best"] is None
        else:
            # Should have a candidate matching expected
            candidates = [c[0] for c in info["candidates"]]
            assert expected in candidates, f"{fname} missing expected candidate {expected}"
            # Status should be ok or ambiguous
            assert info["status"] in ("ok", "ambiguous"), f"{fname} unexpected status {info['status']}"
            # If filename chapter present, best should match
            if fname in filename_chapters:
                assert info["best"][0] == filename_chapters[fname], f"{fname} best candidate mismatch"
