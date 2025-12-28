"""
copier.py — File copying and collision handling for chapterize

This module copies files into a target folder (e.g., 'chapterize', 'chapterize_2', ...),
appends numeric suffixes to resolve filename collisions, and saves a mapping.json for auditability.
"""
import os
import shutil
import json
from pathlib import Path
from typing import Dict, Optional

def get_next_folder(base: Path, name: str = "chapterize") -> Path:
    """Finds the next available target folder (chapterize, chapterize_2, ...)."""
    target = base / name
    idx = 2
    while target.exists() and any(target.iterdir()):
        target = base / f"{name}_{idx}"
        idx += 1
    target.mkdir(exist_ok=True)
    return target

def copy_files_with_mapping(
    src_folder: Path,
    assignments: Dict[str, Optional[str]],
    naming_func,
    target_name: str = "chapterize"
) -> Dict[str, str]:
    """
    Copies files from src_folder to target folder using assignments (filename -> chapter number),
    applies naming_func to generate target filename, resolves collisions, and returns mapping.
    """
    target_folder = get_next_folder(src_folder, target_name)
    mapping = {}
    for fname, chapter in assignments.items():
        src = src_folder / fname
        if not src.exists():
            continue
        base_name = naming_func(fname, chapter)
        target = target_folder / base_name
        suffix = 1
        while target.exists():
            stem, ext = os.path.splitext(base_name)
            target = target_folder / f"{stem}_{suffix}{ext}"
            suffix += 1
        shutil.copy2(src, target)
        mapping[fname] = str(target.relative_to(target_folder))
    # Save mapping.json
    with open(target_folder / "mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)
    return mapping
