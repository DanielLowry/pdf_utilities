import re
from pathlib import Path
from typing import Optional

import pdfplumber

try:
    import wordninja
except ImportError:  # pragma: no cover - dependency is required but fallback keeps runtime safer
    wordninja = None


def _segment_token(token: str) -> str:
    """Split long fused tokens into words using wordninja when available."""
    if not wordninja:
        return token
    # Preserve leading/trailing punctuation when segmenting.
    prefix_match = re.match(r"^[\"'\\(\\[\\{]+", token)
    suffix_match = re.search(r"[\"'\\)\\]\\}.,;:!?]+$", token)
    prefix = prefix_match.group(0) if prefix_match else ""
    suffix = suffix_match.group(0) if suffix_match else ""
    core_start = len(prefix)
    core_end = len(token) - len(suffix) if suffix else len(token)
    core = token[core_start:core_end]
    # Strip non-letters for segmentation but keep original casing/punctuation.
    core_alpha = re.sub(r"[^A-Za-z]", "", core)
    if len(core_alpha) < 8:
        return token
    pieces = wordninja.split(core_alpha.lower())
    if len(pieces) <= 1:
        return token
    # Restore leading capitalization if original core started with uppercase.
    if core[:1].isupper() and pieces:
        pieces[0] = pieces[0].capitalize()
    segmented = " ".join(pieces)
    return f"{prefix}{segmented}{suffix}"


def _clean_text(raw: str) -> str:
    """
    Best-effort cleanup for PDF-extracted text that can lose spacing.
    - Normalize whitespace (collapse repeated spaces/tabs, limit blank lines)
    - Insert spaces at punctuation boundaries when missing
    - Insert spaces between lowercase->Uppercase and letter<->digit boundaries
    - Attempt word segmentation on long fused tokens (wordninja)
    """
    if not raw:
        return ""
    text = raw.replace("\u00a0", " ")
    # Ensure space after punctuation if not present.
    text = re.sub(r"([,.;:!?])(?=[A-Za-z0-9])", r"\1 ", text)
    # Insert spaces at likely word boundaries that got crushed.
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[A-Za-z])(?=[0-9])", " ", text)
    text = re.sub(r"(?<=[0-9])(?=[A-Za-z])", " ", text)
    # Segment long fused tokens line by line to avoid disrupting line structure.
    cleaned_lines = []
    for line in text.splitlines():
        tokens = line.split()
        segmented = [_segment_token(tok) for tok in tokens]
        cleaned_lines.append(" ".join(segmented))
    text = "\n".join(cleaned_lines)
    # Collapse interior whitespace but preserve paragraph breaks.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text(pdf_path: Path | str) -> str:
    """Extract and clean text from all pages of a PDF."""
    pdf_path = Path(pdf_path)
    chunks = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text:
                chunks.append(text)
    return _clean_text("\n\n".join(chunks))


def extract_text_range(pdf_path: Path | str, start: int, end: Optional[int]) -> str:
    """Extract and clean text from a page range [start, end) in a PDF."""
    pdf_path = Path(pdf_path)
    chunks = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        total = len(pdf.pages)
        upper = total if end is None else min(end, total)
        for page_idx in range(start, upper):
            text = pdf.pages[page_idx].extract_text() or ""
            if text:
                chunks.append(text)
    return _clean_text("\n\n".join(chunks))


__all__ = ["extract_text", "extract_text_range", "_clean_text"]
