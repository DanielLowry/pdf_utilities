from chapterize.candidates import extract_candidates

def test_extract_candidates_arabic():
    text = "Chapter 3\nSome content"
    cands = extract_candidates(text)
    assert any(c[0] == '3' for c in cands)

def test_extract_candidates_roman():
    text = "CHAPTER IV\nIntro"
    cands = extract_candidates(text)
    assert any(c[0] == '4' for c in cands)

def test_extract_candidates_none():
    assert extract_candidates("") == []
