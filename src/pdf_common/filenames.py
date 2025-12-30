import re
from typing import Optional

from .numerals import roman_to_int

# Patterns to identify chapter numbers from filenames.
_LEADING_NUMERIC = re.compile(r"^\s*0*(\d{1,3})(?=[\s\-_\.]|$)")
_CHAPTER_WORD = re.compile(r"(?i)\bchapter\s*[:\-\.]?\s*([ivxlcdm]+|\d{1,3})\b")
_CH_PREFIX = re.compile(r"(?i)\bch(?:apter)?\.?\s*([ivxlcdm]+|\d{1,3})(?=[\s\-_\.]|$)")


def _normalize_chapter(raw: str) -> Optional[str]:
    if not raw:
        return None
    raw = raw.strip()
    if not raw:
        return None
    if raw.isdigit():
        # Drop leading zeros
        return str(int(raw))
    roman_val = roman_to_int(raw)
    if roman_val is not None:
        return str(roman_val)
    return None


def extract_chapter_from_filename(filename: str) -> Optional[str]:
    """
    Try to parse a chapter number from a filename using common conventions.
    Supports leading numbers (e.g., '01-chapter.pdf'), 'Chapter X', and 'chX' prefixes.
    Returns None if no pattern matches.
    """
    name = filename
    # Strip directory portion if a path is passed
    if "/" in name or "\\" in name:
        name = name.split("/")[-1].split("\\")[-1]

    for pattern in (_LEADING_NUMERIC, _CHAPTER_WORD, _CH_PREFIX):
        match = pattern.search(name)
        if match:
            normalized = _normalize_chapter(match.group(1))
            if normalized:
                return normalized
    return None
