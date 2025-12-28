"""
cli.py — Main entrypoint for chapterize

This script integrates extraction, inference, interactive sign-off, naming, and copying logic.
"""
import sys
from pathlib import Path
from chapterize.extract import extract_first_page_text
from chapterize.candidates import extract_candidates
from chapterize.inference import global_inference
from chapterize.naming import suggest_filename
from chapterize.interactive import interactive_signoff
from chapterize.copier import copy_files_with_mapping


def main():
    print("Welcome to chapterize!")
    while True:
        folder_input = input("Enter the path to your PDF folder: ").strip()
        folder = Path(folder_input)
        if folder.is_dir():
            break
        print(f"Error: {folder} is not a directory. Please try again.")
    pdf_files = [f for f in folder.iterdir() if f.suffix.lower() == ".pdf"]
    if not pdf_files:
        print("No PDF files found in the folder.")
        sys.exit(1)
    print(f"Found {len(pdf_files)} PDF files.")
    # Step 1: Extract candidates
    file_candidates = {}
    for f in pdf_files:
        text = extract_first_page_text(f)
        file_candidates[f.name] = extract_candidates(text)
    print("\nRunning chapter inference and global logic. This may take a moment...")
    # Step 2: Inference
    result = global_inference(file_candidates, {})
    # Step 3: Interactive sign-off
    assignments = interactive_signoff(result)
    # Step 4: Copy files
    mapping, target_folder = copy_files_with_mapping(folder, assignments, suggest_filename)
    print(f"Files copied to {target_folder}")
    print(f"Mapping saved to {target_folder / 'mapping.json'}")

if __name__ == "__main__":
    main()
