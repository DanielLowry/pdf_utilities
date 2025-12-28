## Plan: Interactive PDF Chapter Renamer (chapterize)

**TL;DR:** Build a lightweight, interactive Python tool named **chapterize** that suggests cleaned chapter filenames for PDF files, lets the user edit/skip/accept interactively in the console (no flags), then copies **all** files into `original_folder/chapterize` (or `chapterize_2`, `chapterize_3`, … if the target folder already exists), resolving filename collisions by appending numeric suffixes (`_1`, `_2`, …). MVP excludes OCR and advanced packaging; include light unit tests. ✅

> **Scope & constraints:** Python-only; interactive console (no CLI flags); default action copies *all* files (including already-named) into `original_folder/chapterize`; no OCR for MVP; conflict resolution uses numeric suffixes.

### Steps (3–6 succinct items) 🔧
1. Create project skeleton and config: add `src/chapterize` package, a `PROGRAM_NAME` constant (default: `chapterize`), and a `PLANS/rename-chapter.md` plan file.
2. Implement parsing and inference: extract first-page text for each PDF and run per-file heuristics (search top lines, regexes for Arabic numerals, Roman numerals, number-with-dash/dot, and common heading prefixes). For each file, produce multiple candidate chapter numbers (when present), each with a confidence score based on heuristic strength, candidate position, and cross-file frequency. Run a lightweight global inference algorithm that reconciles candidates across the set (using existing filenames with chapters and expected chapter counts) to compute candidate probabilities and a best-guess mapping; flag ambiguous files and low-confidence candidates. This inference step runs before any user interaction, producing a proposed mapping and candidate lists that the user must sign off on (accept all or request per-file edits) before proceeding (no OCR).
3. Build suggestion engine and interactive console UI: present the inferred mapping in a clear sign-off screen where the user can accept all before proceeding, and for files with multiple candidates show the top N candidate chapter numbers with confidence scores. Allow a per-file **choose candidate / edit / skip / accept** flow for any files the user wants to change; the UI must clearly indicate files where inference failed or returned ambiguous candidates and provide concise instructions for resolving them.
4. Copying & collision handling: copy files to `original_folder/chapterize` (create if missing); if a filename already exists, append `_1`, `_2`, etc., until unique.
5. Add light unit tests and simulated interactive tests: test parsing and global inference algorithm (including multiple candidate generation and confidence scoring), suggestion heuristics, collision suffixing, and a non-interactive simulation of accept/skip/accept-all flows.
6. Documentation & usage: add `docs/USAGE.md` explaining default behavior, how to change `PROGRAM_NAME`, and sample workflows.

### Further Considerations (1–3 items) 💡
- Future improvements: richer metadata extraction (PDF metadata), optional GUI, and optional OCR in later iterations. ⚠️ Exclude for MVP.
- Consider adding a dry-run / preview mode and more sophisticated conflict policies later (timestamps, UUIDs).

---

### Defaults & quick notes 🔍
- **Default target folder naming convention:** `original_folder/chapterize` (the program will copy everything there by default). If `chapterize` already exists, create `chapterize_2`, `chapterize_3`, etc., incrementing the index to keep runs separated.
- **Program name:** `chapterize` (alternative suggestion: `chapternamer`). To change the name, update the `PROGRAM_NAME` constant in `src/chapterize/config.py` or rename the package/entry point before packaging.
- **Conflict behavior:** append `_1`, `_2`, ... to filenames on collision.
- **Interactivity:** present a sign-off summary of the inferred mapping and must support per-file edit/skip/accept and an **accept-all** shortcut; use stdin prompts and confirm before copying. The sign-off should clearly highlight ambiguous or missing inferences.
- **Inference algorithm & workflow:** collect numeric candidates from first-page text and existing filenames, generate multiple candidate chapter numbers per file with associated confidence scores (derived from heuristic strength, position on the page, and cross-file frequency). Prefer candidates that create a consistent, mostly-unique chapter set across files (and fit within a sensible range like 1..N). The inference runs before user interaction and the program presents a sign-off summary that includes candidate lists and probabilities for each file; the user can accept the best-guess mapping or review individual candidates. If the algorithm cannot find reliable chapter numbers (e.g., fewer than a configurable default threshold such as 50% of files with confident assignments), the program should make this explicit and prompt the user for manual assignments or to skip files.
- **Testing:** use `pytest` with small unit tests for suggestion & collision logic and an integration test that simulates user input.

> **Deliverable:** this file should be saved as `PLANS/rename-chapter.md` and used as the committed plan for the PR.
