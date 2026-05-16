import sys
from pathlib import Path

from pypdf import PdfReader

from pdf_common.cli import confirm, prompt_path
from .splitter import extract_sections, split_pdf


def main() -> int:
    print("PDF Splitter (bookmark-based)")
    source = prompt_path("Source PDF", must_exist=True)
    default_out = str(source.with_name(f"{source.stem}_split"))
    dest = prompt_path("Output folder", default_out, must_exist=False)
    template = input("Optional filename template (press Enter for default): ").strip() or None
    export_text = confirm("Also export per-section text files?")

    try:
        reader = PdfReader(str(source))
        sections = extract_sections(reader)
    except Exception as exc:
        print(f"Error reading PDF: {exc}", file=sys.stderr)
        return 1

    if not sections:
        print("No outline/bookmarks found; nothing to split.", file=sys.stderr)
        return 1

    print(f"Found {len(sections)} sections:")
    for idx, sec in enumerate(sections, start=1):
        title = str(sec.get("title") or f"Section {idx}")
        print(f"  {idx:02d}. {title} (pages {sec['start'] + 1}–{sec['end']})")

    if not confirm("Proceed with splitting?"):
        print("Aborted.")
        return 0

    try:
        outputs = split_pdf(source, dest, template=template, extract_text=export_text)
    except Exception as exc:
        print(f"Error while splitting: {exc}", file=sys.stderr)
        return 1

    print("\nCreated files:")
    for path in outputs:
        print(f" - {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
