"""
Export plain text from PDFs in a folder to per-file .txt outputs.
"""

from .exporter import export_folder, extract_text_from_pdf

__all__ = ["export_folder", "extract_text_from_pdf"]
