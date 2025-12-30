# chapterize — Usage Guide

## Overview

`chapterize` is an interactive tool for renaming and organizing PDF files by inferred chapter number. It extracts chapter numbers from PDF text (scanning every page, not just the first), proposes filenames, lets you review and edit assignments, and copies files into a new folder with a mapping for auditability.

`pdf-splitter` is a companion interactive tool that splits a single PDF into per-chapter files using its bookmarks/outlines. It reuses the same filename templating as chapterize so output names are consistent.

## Quick Start

### chapterize

1. Place your PDFs in a folder.
2. Run the main entrypoint script:
    - `uv run python -m chapterize.cli` (no install), or `uv run chapterize` after `uv run pip install -e .`.
3. Review the interactive sign-off screen:
   - Accept all assignments, or edit/skip files as needed.
4. Files are copied into `chapterize` (or `chapterize_2`, etc.), with collisions resolved by numeric suffixes.
5. A `mapping.json` is saved for audit/reversal.

### pdf-splitter

1. Run `uv run python -m pdf_splitter.cli` (no install), or `uv run pdf-splitter` after `uv run pip install -e .`.
2. Enter the source PDF path when prompted.
3. Accept the suggested output folder (defaults to `<name>_split`) or provide another.
4. Optionally provide a filename template (e.g., `Chapter {chapter:02d} - {original}`) or press Enter for the default.
5. Review the detected sections (from bookmarks) and confirm to write per-chapter PDFs using the shared naming logic. Existing files will warn before overwrite.

## Features
- Robust chapter inference (Arabic, Roman, dash-numbered, ambiguous cases)
- Interactive review and editing
- Flexible filename templates
- Safe copying, collision handling
- Mapping file for auditability
- Filename hints: filenames such as `Chapter 3 - intro.pdf` or `05-overview.pdf` are automatically parsed and used to bias inference.
- Early-page bias: the first non-blank pages get a small confidence boost so late-document noise cannot override the natural chapter order.
- Parallel extraction: each PDF is scanned across all pages, and files are processed concurrently using a process pool (GIL-free by default); the pool is kept small to limit memory.
- Progress insight: the CLI prints a live “Scanned X/Y files” counter while it gathers candidates so you can see progress.

## Requirements
- Python 3.10+
- `pdfplumber`, `pytest`, `reportlab` (for tests), `pypdf` (for splitting)

## Running Tests
- Install dependencies: `uv pip install -r requirements.txt`
- Run tests: `python -m pytest`

## Advanced
- To change the output folder name, edit `PROGRAM_NAME` in `src/chapterize/config.py`.
- For custom filename templates, modify `src/chapterize/naming.py`.
- To see what `chapterize` is doing internally, set logging via the `CHAPTERIZE_LOG_LEVEL` (defaults to `INFO`). Logs now written to `chapterize.log` in the current working directory unless you override `CHAPTERIZE_LOG_FILE`. Only entries emitted from the `chapterize` namespace are included in the log so third-party noise stays muted.

## Limitations
- No OCR fallback (yet)
- Inference is global, but does not warn about conflicting chapter assignment modes
- Only tested for single-user, single-PC scenarios

## Example Workflow
```
$ python -m chapterize.cli
Suggested Chapter Assignments:
...interactive review...
Files copied to chapterize_2/

$ python -m pdf_splitter.cli
PDF Splitter (bookmark-based)
Source PDF: /path/book.pdf
Output folder [/path/book_split]:
Found 4 sections:
  01. Intro (pages 1–3)
  ...
Proceed with splitting? [y/N]: y
Created files:
 - /path/book_split/01 - Intro.pdf
```
