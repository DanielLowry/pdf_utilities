from chapterize.filenames import extract_chapter_from_filename


def test_extracts_decimal_prefix():
    assert extract_chapter_from_filename("1-intro.pdf") == "1"
    assert extract_chapter_from_filename("01-setup.pdf") == "1"
    assert extract_chapter_from_filename("23.final.pdf") == "23"


def test_extracts_chapter_keyword():
    assert extract_chapter_from_filename("Chapter 5 - part.pdf") == "5"
    assert extract_chapter_from_filename("ch12_more.pdf") == "12"


def test_extracts_roman_prefix():
    assert extract_chapter_from_filename("Chapter IX.pdf") == "9"
    assert extract_chapter_from_filename("chvII-intro.pdf") == "7"


def test_returns_none_when_no_match():
    assert extract_chapter_from_filename("overview.pdf") is None
    assert extract_chapter_from_filename("appendix-final.pdf") is None
