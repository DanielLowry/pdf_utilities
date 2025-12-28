"""
filenames.py — Chapter hints derived from PDF filenames

This module provides helpers for extracting chapter numbers directly from filenames,
which complements the text-based inference pipeline and prevents misclassification
when filenames already encode the chapter number.
"""
from pathlib import Path
import re
from typing import Optional

from chapterize.candidates import roman_to_int

ROMAN_FILENAME_PATTERN = re.compile(r"^(?:chapter|ch)[\s._-]*([IVXLCDM]+)\b", re.IGNORECASE)
CHAPTER_FILENAME_PATTERN = re.compile(r"^(?:chapter|ch)[\s._-]*(\d{1,3})\b", re.IGNORECASE)
NUMBER_PREFIX_PATTERN = re.compile(r"^(\d{1,3})(?:[\s._-]|$)")


def extract_chapter_from_filename(filename: str) -> Optional[str]:
    """Return the chapter number embedded in the filename, if present."""
    stem = Path(filename).stem
    for pattern, kind in (
        (ROMAN_FILENAME_PATTERN, "roman"),
        (CHAPTER_FILENAME_PATTERN, "digits"),
        (NUMBER_PREFIX_PATTERN, "digits"),
    ):
        match = pattern.match(stem)
        if not match:
            continue
        value = match.group(1)
        if kind == "roman":
            converted = roman_to_int(value)
            if converted:
                return str(converted)
        else:
            try:
                return str(int(value))
            except ValueError:
                return value
    return None
