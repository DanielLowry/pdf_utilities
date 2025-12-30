"""
Shared helpers for PDF utilities.

This package contains reusable helpers for parsing chapter information and
producing consistent filenames across tools.
"""

from .naming import DEFAULT_TEMPLATES, sanitize_filename, suggest_filename
from .filenames import extract_chapter_from_filename
from .numerals import roman_to_int

__all__ = [
    "DEFAULT_TEMPLATES",
    "sanitize_filename",
    "suggest_filename",
    "extract_chapter_from_filename",
    "roman_to_int",
]
