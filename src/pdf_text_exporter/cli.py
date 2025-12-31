import sys
from pathlib import Path

from .exporter import export_folder


def prompt_path(prompt: str, default: str | None = None, must_exist: bool = False) -> Path:
    while True:
        suffix = f" [{default}]" if default else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default:
            raw = default
        if not raw:
            print("Please enter a path.")
            continue
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
