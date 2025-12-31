from pdf_common.text import _clean_text


def test_clean_text_inserts_spaces_between_words():
    raw = "dialoguethreeeasy"
    cleaned = _clean_text(raw)
    assert "dialogue three easy" in cleaned.lower()


def test_clean_text_handles_punctuation_spacing():
    raw = "Hello,world!Next"
    cleaned = _clean_text(raw)
    assert "Hello, world!" in cleaned
    assert "Next" in cleaned.split()[-1]


def test_clean_text_letter_digit_boundaries():
    raw = "ABC123def"
    cleaned = _clean_text(raw)
    assert "ABC 123 def" in cleaned
