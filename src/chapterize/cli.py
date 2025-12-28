"""
cli.py — Main entrypoint for chapterize

This script integrates extraction, inference, interactive sign-off, naming, and copying logic.
"""
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import os

from chapterize.candidates import extract_candidates
from chapterize.copier import copy_files_with_mapping
from chapterize.extract import extract_document_text
from chapterize.filenames import extract_chapter_from_filename
from chapterize.inference import global_inference
from chapterize.interactive import interactive_signoff
from chapterize.logging_config import configure_logging
from chapterize.naming import suggest_filename

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
    # Step 1: Extract candidates (whole document) in parallel
    file_candidates = {}
    workers = max(1, min(8, os.cpu_count() or 1))
    max_workers = min(workers, len(pdf_files))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(extract_document_text, f): f for f in pdf_files}
        for future in as_completed(future_to_file):
            f = future_to_file[future]
            text = future.result()
            candidates = extract_candidates(text)
            file_candidates[f.name] = candidates
            logger.debug("Extracted %d candidates for %s", len(candidates), f.name)
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
