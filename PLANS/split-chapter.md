# Plan: PDF Chapter Splitter

**TL;DR:** Build a new tool (package: `pdf_splitter`) that splits a single PDF file into multiple files based on its internal structure (Outlines/Bookmarks). It will reuse the robust naming and formatting logic from `chapterize` to ensure consistent, clean output filenames (e.g., `01 - Introduction.pdf`).

## Goals
1.  **Input:** A single PDF file and a nominated target directory.
2.  **Process:**
    *   Parse the PDF's internal Outline (Bookmarks).
    *   Calculate page ranges for each section.
    *   Extract pages and write them to separate PDF files.
3.  **Output:** Individual PDF files for each chapter/section.
4.  **Naming:** Filenames must contain the chapter number at the front. We will leverage `chapterize`'s existing logic to parse titles and apply standard formatting.

## Architecture & Refactoring

Since the naming logic "overlaps heavily" with `chapterize`, we will extract shared components into a common library to avoid duplication.

*   **New Shared Module (`src/pdf_common`):**
    *   Move `chapterize.naming` (filename templating/suggestion) here.
    *   Move `chapterize.filenames` (string cleaning, chapter hint extraction) here.
    *   Update `chapterize` to import from `pdf_common`.
*   **New Package (`src/pdf_splitter`):**
    *   Contains the splitting logic, outline parsing, and CLI for the new tool.

## Implementation Steps

### Phase 1: Refactoring (Shared Code)
*   Create `src/pdf_common`.
*   Move `suggest_filename`, `extract_chapter_from_filename`, and related string utilities from `src/chapterize` to `src/pdf_common`.
*   Refactor `src/chapterize` to use these new import paths.
*   Ensure existing `chapterize` tests pass.

### Phase 2: Core Splitting Logic
*   **Dependency:** Add `pypdf` to `requirements.txt` (efficient for reading outlines and writing page ranges).
*   **Logic:**
    *   Load the source PDF.
    *   Traverse the Outline/Bookmark tree.
    *   Determine the start page for each bookmark and the end page (based on the next bookmark's start).
    *   *Constraint:* For the MVP, we will flatten the structure (treat nested bookmarks as sequential chapters) or only split at the top level.

### Phase 3: Naming Integration
*   Iterate through the extracted sections.
*   **Title Source:** Use the Bookmark label (e.g., "Introduction", "Chapter 1: The Beginning").
*   **Numbering:**
    *   If the bookmark title contains a number (e.g., "1. Intro"), parse it.
    *   If not, use the sequential index (1, 2, 3...) as the chapter number.
*   **Formatting:** Pass the number and title to `pdf_common.naming.suggest_filename` to generate the final canonical filename.

### Phase 4: CLI & Interface
*   Create `src/pdf_splitter/cli.py`.
*   Arguments: `input_pdf` (required), `output_folder` (required).
*   Behavior: Create the output folder if it doesn't exist; warn before overwriting existing files.

### Phase 5: Testing
*   **Unit Tests:** Create a PDF with known bookmarks in memory (using `reportlab` or `pypdf`) and verify the splitter detects ranges correctly.
*   **Integration:** Verify that the output filenames match the expected pattern (e.g., `01 - Intro.pdf`).

## Future Considerations
*   **Text-based Splitting:** If a PDF has no bookmarks, fall back to `chapterize`-style text inference to detect page breaks (significantly more complex).