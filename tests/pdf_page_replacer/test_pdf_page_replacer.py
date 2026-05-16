from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdf_page_replacer.replacer import replace_page


def make_pdf(tmp_path: Path, num_pages: int, label: str) -> Path:
    """Create a simple PDF with num_pages blank pages."""
    writer = PdfWriter()
    for i in range(num_pages):
        writer.add_blank_page(width=612, height=792)
    pdf_path = tmp_path / f"{label}.pdf"
    with pdf_path.open("wb") as handle:
        writer.write(handle)
    return pdf_path


def test_replace_middle_page(tmp_path: Path):
    """Replace a page in the middle of the document."""
    source = make_pdf(tmp_path, 5, "source")
    replacement = make_pdf(tmp_path, 1, "replacement")
    output = tmp_path / "output.pdf"

    result = replace_page(source, 3, replacement, output)

    assert result == output
    assert output.exists()
    reader = PdfReader(str(output))
    assert len(reader.pages) == 5  # 5 pages: 4 from source + 1 from replacement


def test_replace_first_page(tmp_path: Path):
    """Replace the first page."""
    source = make_pdf(tmp_path, 5, "source")
    replacement = make_pdf(tmp_path, 1, "replacement")
    output = tmp_path / "output.pdf"

    result = replace_page(source, 1, replacement, output)

    assert result == output
    reader = PdfReader(str(output))
    assert len(reader.pages) == 5


def test_replace_last_page(tmp_path: Path):
    """Replace the last page."""
    source = make_pdf(tmp_path, 5, "source")
    replacement = make_pdf(tmp_path, 1, "replacement")
    output = tmp_path / "output.pdf"

    result = replace_page(source, 5, replacement, output)

    assert result == output
    reader = PdfReader(str(output))
    assert len(reader.pages) == 5


def test_multi_page_replacement(tmp_path: Path):
    """Replace a page with multiple pages."""
    source = make_pdf(tmp_path, 3, "source")
    replacement = make_pdf(tmp_path, 4, "replacement")
    output = tmp_path / "output.pdf"

    result = replace_page(source, 2, replacement, output)

    assert result == output
    reader = PdfReader(str(output))
    # Page 1 from source + 4 from replacement + page 3 from source = 6 total
    assert len(reader.pages) == 6


def test_single_page_with_multi_page_replacement(tmp_path: Path):
    """Replace the only page with multiple pages."""
    source = make_pdf(tmp_path, 1, "source")
    replacement = make_pdf(tmp_path, 3, "replacement")
    output = tmp_path / "output.pdf"

    result = replace_page(source, 1, replacement, output)

    assert result == output
    reader = PdfReader(str(output))
    assert len(reader.pages) == 3


def test_page_number_out_of_range_too_high(tmp_path: Path):
    """Page number higher than total pages raises ValueError."""
    source = make_pdf(tmp_path, 3, "source")
    replacement = make_pdf(tmp_path, 1, "replacement")
    output = tmp_path / "output.pdf"

    with pytest.raises(ValueError, match="out of range"):
        replace_page(source, 4, replacement, output)


def test_page_number_out_of_range_zero(tmp_path: Path):
    """Page number 0 raises ValueError."""
    source = make_pdf(tmp_path, 3, "source")
    replacement = make_pdf(tmp_path, 1, "replacement")
    output = tmp_path / "output.pdf"

    with pytest.raises(ValueError, match="out of range"):
        replace_page(source, 0, replacement, output)


def test_page_number_negative(tmp_path: Path):
    """Negative page number raises ValueError."""
    source = make_pdf(tmp_path, 3, "source")
    replacement = make_pdf(tmp_path, 1, "replacement")
    output = tmp_path / "output.pdf"

    with pytest.raises(ValueError, match="out of range"):
        replace_page(source, -1, replacement, output)


def test_creates_output_directory(tmp_path: Path):
    """Output directory is created if it doesn't exist."""
    source = make_pdf(tmp_path, 3, "source")
    replacement = make_pdf(tmp_path, 1, "replacement")
    output = tmp_path / "subdir" / "nested" / "output.pdf"

    result = replace_page(source, 2, replacement, output)

    assert result == output
    assert output.exists()
    assert output.parent.exists()
