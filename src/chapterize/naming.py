"""
Compatibility wrapper around shared naming helpers.

Historically these utilities lived in chapterize; they now reside in pdf_common
so other tools can reuse them.
"""

from pdf_common.naming import DEFAULT_TEMPLATES, sanitize_filename, suggest_filename

__all__ = ["DEFAULT_TEMPLATES", "sanitize_filename", "suggest_filename"]
