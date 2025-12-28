# chapterize — Usage Guide

## Overview

`chapterize` is an interactive tool for renaming and organizing PDF files by inferred chapter number. It extracts chapter numbers from PDF text, proposes filenames, lets you review and edit assignments, and copies files into a new folder with a mapping for auditability.

## Quick Start

1. Place your PDFs in a folder.
2. Run the main entrypoint script:
    - Example: `python -m chapterize.cli` (or integrate your own runner)
3. Review the interactive sign-off screen:
   - Accept all assignments, or edit/skip files as needed.
4. Files are copied into `chapterize` (or `chapterize_2`, etc.), with collisions resolved by numeric suffixes.
5. A `mapping.json` is saved for audit/reversal.

## Features
- Robust chapter inference (Arabic, Roman, dash-numbered, ambiguous cases)
- Interactive review and editing
- Flexible filename templates
- Safe copying, collision handling
- Mapping file for auditability

## Requirements
- Python 3.10+
- `pdfplumber`, `pytest`, `reportlab` (for tests)

## Running Tests
- Install dependencies: `uv pip install -r requirements.txt`
- Run tests: `python -m pytest`

## Advanced
- To change the output folder name, edit `PROGRAM_NAME` in `src/chapterize/config.py`.
- For custom filename templates, modify `src/chapterize/naming.py`.

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
```
