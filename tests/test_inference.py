from chapterize.inference import global_inference

def test_global_inference_basic():
    file_candidates = {
        'a.pdf': [('1', 0.9)],
        'b.pdf': [('2', 0.9)],
        'c.pdf': [('1', 0.7), ('2', 0.6)]
    }
    filename_chapters = {'a.pdf': '1'}
    result = global_inference(file_candidates, filename_chapters)
    assert result['a.pdf']['best'][0] == '1'
    assert result['b.pdf']['best'][0] == '2'
    assert result['c.pdf']['status'] in ('ok', 'ambiguous')

def test_global_inference_none():
    file_candidates = {'a.pdf': [], 'b.pdf': []}
    filename_chapters = {}
    result = global_inference(file_candidates, filename_chapters)
    assert result['a.pdf']['status'] == 'none'
    assert result['b.pdf']['status'] == 'none'


def test_global_inference_duplicate_penalty_prioritizes_unique_candidate():
    file_candidates = {
        'a.pdf': [('1', 0.9)],
        'b.pdf': [('1', 0.85), ('2', 0.83)],
        'c.pdf': [('3', 0.8)]
    }
    filename_chapters = {}
    result = global_inference(file_candidates, filename_chapters)
    # '1' is duplicated but '2' remains unique and should rank higher for b.pdf
    assert result['b.pdf']['best'][0] == '2'
    assert result['b.pdf']['status'] == 'ok'


def test_global_inference_many_duplicates_drives_confidence_lower():
    file_candidates = {
        'a.pdf': [('1', 0.9)],
        'b.pdf': [('1', 0.9)],
        'c.pdf': [('1', 0.9)]
    }
    result = global_inference(file_candidates, {})
    # With multiple files claiming chapter 1, confidence drops below threshold
    assert result['a.pdf']['status'] == 'none'
    assert result['b.pdf']['status'] == 'none'
    assert result['c.pdf']['status'] == 'none'
