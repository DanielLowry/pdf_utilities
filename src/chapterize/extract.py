import pdfplumber
from pathlib import Path
from typing import Iterator, Optional, Tuple


def iterate_document_pages(pdf_path: Path) -> Iterator[Tuple[int, Optional[str]]]:
    """Yield (page_index, text) for every page, text can be None for blank pages."""
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for idx, page in enumerate(pdf.pages):
                yield idx, page.extract_text()
    except Exception:
        return


def extract_document_text(pdf_path: Path) -> Optional[str]:
    """Extracts text from every page in a PDF document."""
    fragments = []
    for _, text in iterate_document_pages(pdf_path):
        if text:
            fragments.append(text)
    if not fragments:
        return None
    return "\n".join(fragments)


def extract_first_page_text(pdf_path: Path) -> Optional[str]:
    """Backward-compatible helper that returns text from the first page."""
    for _, text in iterate_document_pages(pdf_path):
        if text:
            return text
    return None
