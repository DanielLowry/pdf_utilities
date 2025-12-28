from pathlib import Path
from chapterize.cli import collect_candidates_from_pdf


def test_collect_candidates_prefers_early_pages_and_order(monkeypatch):
    pages = [
        (0, "16\nSegmentation"),
        (1, "1. intro material"),
        (5, "2. later section"),
    ]

    def fake_iterate(_path):
        for idx, text in pages:
            yield idx, text

    def fake_extract(text):
        if "16" in text:
            return [("16", 0.7)]
        if text.startswith("1."):
            return [("1", 0.8)]
        if text.startswith("2."):
            return [("2", 0.8)]
        return []

    monkeypatch.setattr("chapterize.cli.iterate_document_pages", fake_iterate)
    monkeypatch.setattr("chapterize.cli.extract_candidates", fake_extract)

    result = collect_candidates_from_pdf(Path("dummy.pdf"))
    assert result[0][0] == "16"
    assert result[1][0] == "1"
    assert result[-1][0] == "2"
