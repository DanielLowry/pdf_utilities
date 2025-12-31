from pathlib import Path

import pytest
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from pdf_text_exporter.exporter import export_folder, extract_text_from_pdf


def make_pdf_with_text(tmp_path: Path, name: str, lines: list[str]) -> Path:
    pdf_path = tmp_path / name
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    for line in lines:
        c.drawString(100, 700, line)
        c.showPage()
    c.save()
    return pdf_path


def test_extract_text_from_pdf(tmp_path):
    pdf_path = make_pdf_with_text(tmp_path, "sample.pdf", ["Hello world", "Second page"])
    text = extract_text_from_pdf(pdf_path)
    assert "Hello world" in text
    assert "Second page" in text


def test_export_folder_writes_txt_files(tmp_path):
    make_pdf_with_text(tmp_path, "a.pdf", ["Alpha"])
    make_pdf_with_text(tmp_path, "b.pdf", ["Beta"])
    out_dir = tmp_path / "out"
    outputs = export_folder(tmp_path, out_dir, progress=True)
    assert len(outputs) == 2
    contents = "\n".join(p.read_text(encoding="utf-8") for p in outputs)
    assert "Alpha" in contents
    assert "Beta" in contents
