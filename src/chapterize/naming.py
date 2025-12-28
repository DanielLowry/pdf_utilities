"""
naming.py — Filename suggestion logic for chapterize

This module provides functions to generate suggested filenames for PDF files
based on inferred chapter numbers and user-selected style templates.
"""
from typing import Optional
import re

DEFAULT_TEMPLATES = [
    "{chapter} - {original}",
    "Chapter {chapter:02d} - {original}",
    "{original} (Chapter {chapter})"
]

def sanitize_filename(name: str) -> str:
    """Remove illegal characters and normalize spaces."""
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def suggest_filename(original: str, chapter: Optional[str], template: str = None) -> str:
    """
    Generate a suggested filename using the chapter number and a style template.
    If chapter is None, returns the sanitized original filename.
    """
    if template is None:
        template = DEFAULT_TEMPLATES[0]
    if chapter is None:
        return sanitize_filename(original)
    try:
        chapter_int = int(chapter)
    except Exception:
        chapter_int = chapter
    new_name = template.format(chapter=chapter_int, original=sanitize_filename(original))
    return sanitize_filename(new_name)
