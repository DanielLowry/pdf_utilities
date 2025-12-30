from pathlib import Path
from chapterize.extract import extract_document_text

def test_extract_document_text_handles_missing_file(tmp_path):
    assert extract_document_text(Path("not_a_real_file.pdf")) is None
