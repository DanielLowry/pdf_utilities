import sys
from pathlib import Path

from pypdf import PdfReader

from .splitter import extract_sections, split_pdf


def prompt_path(prompt: str, default: str | None = None, must_exist: bool = False) -> Path:
    """
    Ask the user for a path with an optional default, retrying until a value is provided.
    """
    while True:
        suffix = f" [{default}]" if default else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default:
            raw = default
        if not raw:
            print("Please enter a path.")
            continue
        # Accept pasted paths with quotes (common when paths contain spaces)
        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            raw = raw[1:-1]
        path = Path(raw).expanduser()
        if must_exist and not path.exists():
            print(f"{path} does not exist. Try again.")
            continue
        return path


def confirm(prompt: str) -> bool:
    resp = input(f"{prompt} [y/N]: ").strip().lower()
    return resp in ("y", "yes")


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
