from pathlib import Path

from pypdf import PdfReader, PdfWriter


def replace_page(
    source_pdf: Path | str,
    page_number: int,
    replacement_pdf: Path | str,
    output_pdf: Path | str,
) -> Path:
    """
    Replace a specific page in a PDF with all pages from a replacement PDF.

    Args:
        source_pdf: Path to the source PDF
        page_number: 1-based page number to replace
        replacement_pdf: Path to the PDF whose pages will replace the target page
        output_pdf: Path for the output PDF

    Returns:
        Path to the output PDF

    Raises:
        ValueError: If page_number is out of range
    """
    source_pdf = Path(source_pdf)
    replacement_pdf = Path(replacement_pdf)
    output_pdf = Path(output_pdf)

    source_reader = PdfReader(str(source_pdf))
    replacement_reader = PdfReader(str(replacement_pdf))

    # Convert 1-based to 0-based
    page_idx = page_number - 1

    if page_idx < 0 or page_idx >= len(source_reader.pages):
        raise ValueError(
            f"Page {page_number} is out of range. Source PDF has {len(source_reader.pages)} pages."
        )

    writer = PdfWriter()

    # Add pages before the target page
    for i in range(page_idx):
        writer.add_page(source_reader.pages[i])

    # Add all pages from replacement PDF
    for page in replacement_reader.pages:
        writer.add_page(page)

    # Add pages after the target page
    for i in range(page_idx + 1, len(source_reader.pages)):
        writer.add_page(source_reader.pages[i])

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as handle:
        writer.write(handle)

    return output_pdf
