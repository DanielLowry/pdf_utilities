"""
PDF splitter tool that uses PDF outlines/bookmarks to create per-chapter files.
"""

from .splitter import extract_sections, split_pdf

__all__ = ["extract_sections", "split_pdf"]
