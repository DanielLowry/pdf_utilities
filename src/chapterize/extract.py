import pdfplumber
from pathlib import Path
from typing import Optional


def extract_document_text(pdf_path: Path) -> Optional[str]:
    """Extracts text from every page in a PDF document."""
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            if not pdf.pages:
                return None
            fragments = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    fragments.append(text)
            return "\n".join(fragments) if fragments else None
    except Exception:
        return None


def extract_first_page_text(pdf_path: Path) -> Optional[str]:
    """Backward-compatible helper that returns text from the first page."""
    full_text = extract_document_text(pdf_path)
    if not full_text:
        return None
    first_page = full_text.splitlines()
    return first_page[0] if first_page else None
