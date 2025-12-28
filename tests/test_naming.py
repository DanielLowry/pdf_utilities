from chapterize.naming import suggest_filename, sanitize_filename, DEFAULT_TEMPLATES

def test_suggest_filename_default():
    orig = "3-dialogue.pdf"
    assert suggest_filename(orig, "3") == "3 - 3-dialogue.pdf"

def test_suggest_filename_template():
    orig = "threads-lock.pdf"
    assert suggest_filename(orig, "7", DEFAULT_TEMPLATES[1]) == "Chapter 07 - threads-lock.pdf"

def test_suggest_filename_none():
    orig = "no-chapter.pdf"
    assert suggest_filename(orig, None) == "no-chapter.pdf"

def test_sanitize_filename():
    bad = "bad:file*name?.pdf"
    assert sanitize_filename(bad) == "badfilename.pdf"
