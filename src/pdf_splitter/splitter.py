from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from pypdf import PdfReader, PdfWriter
from pdf_common.filenames import extract_chapter_from_filename
from pdf_common.naming import suggest_filename
from pdf_common.text import extract_text_range

Section = Dict[str, object]  # keys: title (str), start (int), end (int)


def _flatten_outline(reader: PdfReader, outline: Iterable) -> Iterable[Tuple[str, int]]:
    """
    Yield (title, page_index) for every destination in the outline, flattening nested lists.
    """
    for item in outline:
        if isinstance(item, list):
            yield from _flatten_outline(reader, item)
            continue
        try:
            page_index = reader.get_destination_page_number(item)
        except Exception:
            continue
        if hasattr(item, "title"):
            title = getattr(item, "title")
        elif hasattr(item, "get"):
            title = item.get("/Title")
        else:
            title = None
        title = title or str(item)
        yield title, page_index


def extract_sections(reader: PdfReader) -> List[Section]:
    """
    Convert the PDF outline/bookmarks into a list of sections with page ranges.
    Nested outlines are flattened and sorted by starting page.
    """
    outline = getattr(reader, "outlines", None) or getattr(reader, "outline", None) or []
    entries = list(_flatten_outline(reader, outline))
    if not entries:
        return []

    # Sort and drop duplicate starting pages to avoid zero-length ranges.
    entries.sort(key=lambda item: item[1])
    deduped = []
    seen = set()
    for title, page_idx in entries:
        if page_idx in seen:
            continue
        seen.add(page_idx)
        deduped.append((title, page_idx))

    total_pages = len(reader.pages)
    sections: List[Section] = []
    for idx, (title, start) in enumerate(deduped):
        end = deduped[idx + 1][1] if idx + 1 < len(deduped) else total_pages
        if end <= start:
            continue
        sections.append({"title": title, "start": start, "end": end})
    return sections


def split_pdf(
    input_pdf: Path | str,
    output_dir: Path | str,
    template: str | None = None,
    warn_on_overwrite: bool = True,
    extract_text: bool = False,
) -> List[Path]:
    """
    Split a PDF into per-section files based on its outline/bookmarks.

    Returns the list of generated PDF file paths.
    """
    input_pdf = Path(input_pdf)
    output_dir = Path(output_dir)
    reader = PdfReader(str(input_pdf))
    sections = extract_sections(reader)
    if not sections:
        raise ValueError("No outline/bookmarks found; nothing to split.")

    output_dir.mkdir(parents=True, exist_ok=True)
    generated: List[Path] = []
    for idx, section in enumerate(sections, start=1):
        title = section["title"] or f"Section {idx}"
        chapter = extract_chapter_from_filename(str(title)) or str(idx)
        filename = suggest_filename(str(title), chapter, template)
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"
        out_path = output_dir / filename
        if warn_on_overwrite and out_path.exists():
            print(f"Warning: overwriting existing file {out_path}")
        writer = PdfWriter()
        for page_idx in range(int(section["start"]), int(section["end"])):
            writer.add_page(reader.pages[page_idx])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as handle:
            writer.write(handle)
        generated.append(out_path)

        if extract_text:
            text_path = out_path.with_suffix(".txt")
            if warn_on_overwrite and text_path.exists():
                print(f"Warning: overwriting existing file {text_path}")
            content = extract_text_range(input_pdf, int(section["start"]), int(section["end"]))
            text_path.write_text(content, encoding="utf-8")
    return generated
