"""
Export plain text from PDFs in a folder to per-file .txt outputs.
"""

from .exporter import export_folder
from pdf_common.text import extract_text

__all__ = ["export_folder", "extract_text"]
