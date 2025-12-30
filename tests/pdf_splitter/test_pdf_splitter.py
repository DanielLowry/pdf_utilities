from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_splitter.splitter import extract_sections, split_pdf


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
