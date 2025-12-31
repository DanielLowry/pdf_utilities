from pathlib import Path
from typing import List

import pdfplumber


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from all pages of a PDF (best-effort, ignores images)."""
    chunks: List[str] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text:
                chunks.append(text.strip())
    return "\n\n".join(chunks)


def export_folder(
    input_dir: Path | str,
    output_dir: Path | str,
    warn_on_overwrite: bool = True,
    progress: bool = False,
) -> List[Path]:
    """
    Export text for every PDF in a folder to matching .txt files.
    Returns the list of created text file paths.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    if not input_dir.exists() or not input_dir.is_dir():
        raise ValueError(f"Input directory does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []
    pdfs = sorted(input_dir.glob("*.pdf"))
    total = len(pdfs)
    for idx, pdf_path in enumerate(pdfs, start=1):
        text_path = output_dir / (pdf_path.stem + ".txt")
        if warn_on_overwrite and text_path.exists():
            print(f"Warning: overwriting existing file {text_path}")
        content = extract_text_from_pdf(pdf_path)
        text_path.write_text(content, encoding="utf-8")
        outputs.append(text_path)
        if progress:
            print(f"[{idx}/{total}] {pdf_path.name}", end="\r" if idx < total else "\n")
    return outputs
