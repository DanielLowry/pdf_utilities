## Plan: Interactive PDF Chapter Renamer (chapterize)

**TL;DR:** Build a lightweight, interactive Python tool named **chapterize** that suggests cleaned chapter filenames for PDF files, lets the user edit/skip/accept interactively in the console (no flags), then copies **all** files into `original_folder/chapterize` (or `chapterize_2`, `chapterize_3`, … if the target folder already exists), resolving filename collisions by appending numeric suffixes (`_1`, `_2`, …). MVP excludes OCR and advanced packaging; include light unit tests. ✅

> **Scope & constraints:** Python-only; interactive console (no CLI flags); default action copies *all* files (including already-named) into `original_folder/chapterize`; no OCR for MVP; conflict resolution uses numeric suffixes.

### Steps (3–6 succinct items) 🔧
1. Create project skeleton and config: add `src/chapterize` package, a `PROGRAM_NAME` constant (default: `chapterize`), and a `PLANS/rename-chapter.md` plan file.
2. Implement name-suggestion logic: simple heuristic parsing from filenames (regex, split on common delimiters) and a short set of rules to propose clean chapter names (no OCR).
3. Build interactive console UI: show list of files with suggestions, allow per-file **edit / skip / accept**, and a global **accept all** before committing copies.
4. Copying & collision handling: copy files to `original_folder/chapterize` (create if missing); if a filename already exists, append `_1`, `_2`, etc., until unique.
5. Add light unit tests and simulated interactive tests: test suggestion heuristics, collision suffixing, and a non-interactive simulation of accept/skip/accept-all flows.
6. Documentation & usage: add `docs/USAGE.md` explaining default behavior, how to change `PROGRAM_NAME`, and sample workflows.

### Further Considerations (1–3 items) 💡
- Future improvements: richer metadata extraction (PDF metadata), optional GUI, and optional OCR in later iterations. ⚠️ Exclude for MVP.
- Consider adding a dry-run / preview mode and more sophisticated conflict policies later (timestamps, UUIDs).

---

### Defaults & quick notes 🔍
- **Default target folder naming convention:** `original_folder/chapterize` (the program will copy everything there by default). If `chapterize` already exists, create `chapterize_2`, `chapterize_3`, etc., incrementing the index to keep runs separated.
- **Program name:** `chapterize` (alternative suggestion: `chapternamer`). To change the name, update the `PROGRAM_NAME` constant in `src/chapterize/config.py` or rename the package/entry point before packaging.
- **Conflict behavior:** append `_1`, `_2`, ... to filenames on collision.
- **Interactivity:** must support per-file edit/skip/accept and an **accept-all** shortcut; use stdin prompts and confirm before copying.
- **Testing:** use `pytest` with small unit tests for suggestion & collision logic and an integration test that simulates user input.

> **Deliverable:** this file should be saved as `PLANS/rename-chapter.md` and used as the committed plan for the PR.
