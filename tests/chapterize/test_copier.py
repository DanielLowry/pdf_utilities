import tempfile
import os
from pathlib import Path
from chapterize.copier import copy_files_with_mapping, get_next_folder
from chapterize.naming import suggest_filename

def test_get_next_folder(tmp_path):
    folder = get_next_folder(tmp_path, "chapterize")
    assert folder.exists()
    # Create a file to simulate non-empty
    (folder / "dummy.txt").write_text("x")
    folder2 = get_next_folder(tmp_path, "chapterize")
    assert folder2.name.startswith("chapterize_")
    assert folder2.exists()

def test_copy_files_with_mapping(tmp_path):
    # Create source files
    src = tmp_path / "src"
    src.mkdir()
    files = ["a.pdf", "b.pdf", "c.pdf"]
    for fname in files:
        (src / fname).write_text(f"PDF {fname}")
    assignments = {"a.pdf": "1", "b.pdf": "2", "c.pdf": None}
    mapping, target_folder = copy_files_with_mapping(src, assignments, suggest_filename)
    for fname in files:
        assert fname in mapping
    # Check mapping.json exists in the folder just used
    assert (target_folder / "mapping.json").exists()
