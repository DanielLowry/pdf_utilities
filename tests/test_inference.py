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
