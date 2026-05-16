import sys
from pathlib import Path

from pypdf import PdfReader

from pdf_common.cli import confirm, prompt_path
from .replacer import replace_page


def main() -> int:
    print("PDF Page Replacer")
    source = prompt_path("Source PDF", must_exist=True)

    try:
        reader = PdfReader(str(source))
        num_pages = len(reader.pages)
    except Exception as exc:
        print(f"Error reading PDF: {exc}", file=sys.stderr)
        return 1

    print(f"Source PDF has {num_pages} page(s).")

    while True:
        try:
            page_str = input("Page number to replace (1-based): ").strip()
            page_num = int(page_str)
            if page_num < 1 or page_num > num_pages:
                print(f"Please enter a page number between 1 and {num_pages}.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")
            continue

    replacement = prompt_path("Replacement PDF", must_exist=True)

    try:
        repl_reader = PdfReader(str(replacement))
        repl_pages = len(repl_reader.pages)
        print(f"Replacement PDF has {repl_pages} page(s).")
    except Exception as exc:
        print(f"Error reading replacement PDF: {exc}", file=sys.stderr)
        return 1

    default_out = str(source.with_name(f"{source.stem}_replaced.pdf"))
    output = prompt_path("Output PDF", default_out, must_exist=False)

    if output.exists() and not confirm(f"Overwrite {output}?"):
        print("Aborted.")
        return 0

    try:
        result = replace_page(source, page_num, replacement, output)
        expected_pages = num_pages - 1 + repl_pages
        print(f"\nReplaced page {page_num} with {repl_pages} page(s) from replacement PDF.")
        print(f"Output PDF has {expected_pages} page(s).")
        print(f"Created: {result}")
        return 0
    except Exception as exc:
        print(f"Error while replacing: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
