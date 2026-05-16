import sys

from pdf_common.cli import confirm, prompt_path
from .exporter import export_folder


def main() -> int:
    print("PDF Text Exporter (folder-based)")
    src = prompt_path("Source folder of PDFs", must_exist=True)
    default_out = str(src.with_name(f"{src.name}_text"))
    dest = prompt_path("Output folder for text files", default_out, must_exist=False)
    show_progress = confirm("Show progress while exporting?")

    try:
        outputs = export_folder(src, dest, progress=show_progress)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"\nCreated {len(outputs)} text file(s) in {dest}")
    if outputs:
        for path in outputs[:5]:
            print(f" - {path}")
        if len(outputs) > 5:
            print(f" ... and {len(outputs) - 5} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
