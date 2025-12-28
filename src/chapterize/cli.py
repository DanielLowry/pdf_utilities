"""
cli.py — Main entrypoint for chapterize

This script integrates extraction, inference, interactive sign-off, naming, and copying logic.
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple

from chapterize.candidates import extract_candidates
from chapterize.copier import copy_files_with_mapping
from chapterize.extract import iterate_document_pages
from chapterize.filenames import extract_chapter_from_filename
from chapterize.inference import global_inference
from chapterize.interactive import interactive_signoff
from chapterize.logging_config import configure_logging
from chapterize.naming import suggest_filename


def _page_bonus(offset: int) -> float:
    """Return the confidence bonus for candidates offset from the first meaningful page."""
    return max(0.0, 0.25 - min(offset, 6) * 0.04)


def collect_candidates_from_pdf(pdf_path: Path) -> List[Tuple[str, float]]:
    """Collect chapter candidates from every page while weighting early pages."""
    candidates: List[Tuple[str, float]] = []
    first_non_blank = None
    for page_index, text in iterate_document_pages(pdf_path):
        if not text:
            continue
        if first_non_blank is None:
            first_non_blank = page_index
        offset = page_index - (first_non_blank or page_index)
        for chapter, conf in extract_candidates(text):
            boosted = min(1.0, conf + _page_bonus(offset))
            candidates.append((chapter, boosted))
    return candidates

logger = configure_logging()


def main():
    print("Welcome to chapterize!")
    while True:
        folder_input = input("Enter the path to your PDF folder: ").strip()
        folder = Path(folder_input)
        if folder.is_dir():
            break
        print(f"Error: {folder} is not a directory. Please try again.")
    logger.debug("User selected folder %s", folder.resolve())
    pdf_files = [f for f in folder.iterdir() if f.suffix.lower() == ".pdf"]
    if not pdf_files:
        print("No PDF files found in the folder.")
        sys.exit(1)
    print(f"Found {len(pdf_files)} PDF files.")
    # Step 1: Extract candidates (whole document) in parallel. This step is still memory hungry
    # because `pdfplumber` loads page buffers, so keep the pool small and stream outputs.
    file_candidates = {}
    workers = max(1, min(4, os.cpu_count() or 2))
    max_workers = min(workers, len(pdf_files))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(collect_candidates_from_pdf, f): f for f in pdf_files}
        scanned = 0
        print("Scanning PDF files for chapter candidates...")
        for future in as_completed(future_to_file):
            f = future_to_file[future]
            candidates = future.result()
            file_candidates[f.name] = candidates
            logger.debug("Extracted %d candidates for %s", len(candidates), f.name)
            scanned += 1
            print(f"\r Scanned {scanned}/{len(pdf_files)} files", end="", flush=True)
        print()
    logger.debug("Filename-based chapter hints:")
    filename_chapters = {}
    for f in pdf_files:
        chapter_hint = extract_chapter_from_filename(f.name)
        if chapter_hint:
            filename_chapters[f.name] = chapter_hint
            logger.debug("Filename %s yields chapter %s", f.name, chapter_hint)
    logger.debug("Using filename chapters: %s", filename_chapters)
    print("\nRunning chapter inference and global logic. This may take a moment...")
    # Step 2: Inference
    result = global_inference(file_candidates, filename_chapters)
    summary = {
        fname: {"best": info["best"], "status": info["status"]}
        for fname, info in result.items()
    }
    logger.debug("Inference summary: %s", summary)
    # Step 3: Interactive sign-off
    assignments = interactive_signoff(result)
    # Step 4: Copy files
    mapping, target_folder = copy_files_with_mapping(folder, assignments, suggest_filename)
    print(f"Files copied to {target_folder}")
    print(f"Mapping saved to {target_folder / 'mapping.json'}")

if __name__ == "__main__":
    main()
