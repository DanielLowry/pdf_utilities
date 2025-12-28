import pdfplumber
from pathlib import Path
from typing import Optional

def extract_first_page_text(pdf_path: Path) -> Optional[str]:
    """Extracts text from the first page of a PDF file."""
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            if not pdf.pages:
                return None
            return pdf.pages[0].extract_text() or None
    except Exception as e:
        return None
