import re
from pathlib import Path
from typing import Optional

DEFAULT_TEMPLATES = [
    "{chapter} - {original}",
    "Chapter {chapter:02d} - {original}",
]

_INVALID_CHARS = r'[<>:"/\\\\|?*]'


def sanitize_filename(name: str) -> str:
    """
    Remove characters that are invalid for filenames on common filesystems.
    Collapses repeated spaces after removal.
    """
    cleaned = re.sub(_INVALID_CHARS, "", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _coerce_chapter(chapter: str) -> str | int:
    """Return an int when chapter is numeric so templates can zero-pad."""
    chapter = chapter.strip()
    if chapter.isdigit():
        return int(chapter)
    return chapter


def suggest_filename(
    original_filename: str,
    chapter: Optional[str],
    template: Optional[str] = None,
) -> str:
    """
    Suggest a clean filename using the provided chapter number and template.
    If chapter is None/empty, returns a sanitized version of the original filename.
    """
    base_name = Path(original_filename).name
    base_name = sanitize_filename(base_name)
    if not chapter:
        return base_name

    chosen_template = template or DEFAULT_TEMPLATES[0]
    chapter_value = _coerce_chapter(str(chapter))
    try:
        rendered = chosen_template.format(chapter=chapter_value, original=base_name)
    except Exception:
        rendered = f"{chapter} - {base_name}"
    return sanitize_filename(rendered)
