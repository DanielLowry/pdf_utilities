from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_splitter.splitter import extract_sections, split_pdf
from pdf_common.text import extract_text_range, _clean_text


def make_outlined_pdf(tmp_path: Path) -> Path:
    pdf_path = tmp_path / "outlined.pdf"
    writer = PdfWriter()
    for _ in range(5):
        writer.add_blank_page(width=612, height=792)
    intro = writer.add_outline_item("Intro", 0)
    writer.add_outline_item("Chapter 2 - Methods", 1)
    part3 = writer.add_outline_item("Part III", 2)
    # nested bookmark should still be handled in sequence
    writer.add_outline_item("Subsection A", 3, parent=part3)
    with pdf_path.open("wb") as handle:
        writer.write(handle)
    return pdf_path


def test_extract_sections_from_outline(tmp_path):
    pdf_path = make_outlined_pdf(tmp_path)
    reader = PdfReader(str(pdf_path))
    sections = extract_sections(reader)
    assert [s["start"] for s in sections] == [0, 1, 2, 3]
    assert sections[-1]["end"] == 5  # last section runs to end of document


def test_split_pdf_creates_named_files(tmp_path):
    pdf_path = make_outlined_pdf(tmp_path)
    output_dir = tmp_path / "out"
    outputs = split_pdf(pdf_path, output_dir)
    names = sorted(p.name for p in outputs)
    assert names == [
        "1 - Intro.pdf",
        "2 - Chapter 2 - Methods.pdf",
        "3 - Part III.pdf",
        "4 - Subsection A.pdf",
    ]
    # Each output should contain at least one page
    for out in outputs:
        reader = PdfReader(str(out))
        assert len(reader.pages) >= 1


def test_split_pdf_respects_template_and_fallback_numbering(tmp_path):
    pdf_path = tmp_path / "outlined.pdf"
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(width=612, height=792)
    writer.add_outline_item("Preface", 0)  # no explicit number, should fallback to index 1
    writer.add_outline_item("Chapter 7", 1)  # explicit number
    with pdf_path.open("wb") as handle:
        writer.write(handle)

    output_dir = tmp_path / "templated"
    outputs = split_pdf(pdf_path, output_dir, template="Chapter {chapter:02d} - {original}")
    names = sorted(p.name for p in outputs)
    assert names == [
        "Chapter 01 - Preface.pdf",
        "Chapter 07 - Chapter 7.pdf",
    ]


def test_split_pdf_can_export_text(tmp_path):
    # Build a PDF with actual text using reportlab, then add outlines via pypdf
    rich_pdf = tmp_path / "rich.pdf"
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
    except Exception:
        pytest.skip("reportlab not available for text extraction test")

    c = canvas.Canvas(str(rich_pdf), pagesize=letter)
    c.drawString(100, 700, "Intro page text")
    c.showPage()
    c.drawString(100, 700, "Chapter 2 text here")
    c.save()

    reader = PdfReader(str(rich_pdf))
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.add_outline_item("Intro", 0)
    writer.add_outline_item("Chapter 2", 1)
    outlined = tmp_path / "outlined.pdf"
    with outlined.open("wb") as handle:
        writer.write(handle)

    out_dir = tmp_path / "txt_out"
    outputs = split_pdf(outlined, out_dir, extract_text=True)
    # Two PDFs and two text files should be present
    text_files = sorted(out_dir.glob("*.txt"))
    assert len(outputs) == 2
    assert len(text_files) == 2
    content = text_files[0].read_text(encoding="utf-8") + text_files[1].read_text(encoding="utf-8")
    assert "Intro page text" in content
    assert "Chapter 2 text here" in content


def test_extract_text_range_uses_cleaning(tmp_path):
    # Create a PDF where extractor may return concatenated words (simulated via manual string)
    pdf_path = tmp_path / "range.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with pdf_path.open("wb") as handle:
        writer.write(handle)
    # Instead of relying on PDF quirks, directly test the cleaner
    raw = "wordOnewordTwo"
    cleaned = _clean_text(raw)
    assert "word One" in cleaned or "word Two" in cleaned
