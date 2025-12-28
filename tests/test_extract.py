from pathlib import Path
from chapterize.extract import extract_first_page_text

def test_extract_first_page_text(tmp_path):
    # This is a placeholder; real test would use a sample PDF
    assert extract_first_page_text(Path("not_a_real_file.pdf")) is None
