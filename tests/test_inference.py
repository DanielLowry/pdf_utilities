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


def test_global_inference_duplicate_penalty_score_visible_on_confidence():
    file_candidates = {
        'a.pdf': [('1', 0.9)],
        'b.pdf': [('1', 0.9), ('2', 0.6)]
    }
    result = global_inference(file_candidates, {})
    # Candidate '1' sees a -0.4 penalty because it appears twice, dropping the reported confidence.
    assert result['a.pdf']['best'][1] == 0.5
    assert result['a.pdf']['status'] == 'ok'
    # File b has a unique '2' candidate that outranks the duplicated '1'.
    assert result['b.pdf']['best'][0] == '2'


def test_global_inference_duplicate_penalty_skipped_for_filename_evidence():
    file_candidates = {
        'a.pdf': [('1', 0.9)],
        'b.pdf': [('1', 0.9)]
    }
    filename_chapters = {'a.pdf': '1'}
    result = global_inference(file_candidates, filename_chapters)
    # Filename evidence should lift the score for a.pdf, overriding the duplicate penalty.
    assert result['a.pdf']['best'][1] == 1.0
    assert result['a.pdf']['status'] == 'ok'


def test_duplicate_candidates_different_confidence_produces_mixed_statuses():
    file_candidates = {
        'a.pdf': [('1', 0.95)],
        'b.pdf': [('1', 0.55)]
    }
    result = global_inference(file_candidates, {})
    assert result['a.pdf']['best'] == ('1', 0.55)
    assert result['a.pdf']['status'] == 'ok'
    assert result['b.pdf']['best'] == ('1', 0.15)
    assert result['b.pdf']['status'] == 'none'


def test_duplicate_candidates_same_score_rejects_low_unique_option():
    file_candidates = {
        'a.pdf': [('1', 0.95)],
        'b.pdf': [('1', 0.95), ('2', 0.2)]
    }
    result = global_inference(file_candidates, {})
    assert result['a.pdf']['best'][0] == '1'
    assert result['b.pdf']['best'][0] == '1'
    assert result['b.pdf']['candidates'][0][1] == 0.55
    assert result['b.pdf']['candidates'][1][0] == '2'


def test_duplicate_candidates_same_score_close_alternative_flags_ambiguous():
    file_candidates = {
        'a.pdf': [('1', 0.95)],
        'b.pdf': [('1', 0.95), ('2', 0.52)]
    }
    result = global_inference(file_candidates, {})
    assert result['b.pdf']['best'][0] == '1'
    assert result['b.pdf']['status'] == 'ambiguous'
    score_diff = result['b.pdf']['candidates'][0][1] - result['b.pdf']['candidates'][1][1]
    assert score_diff < 0.1


def test_candidates_below_threshold_are_dropped():
    file_candidates = {'a.pdf': [('1', 0.95), ('2', 0.08)]}
    result = global_inference(file_candidates, {})
    assert result['a.pdf']['best'] == ('1', 0.95)
    assert result['a.pdf']['candidates'] == [('1', 0.95)]


def test_all_candidates_dropped_results_in_none_status():
    file_candidates = {'a.pdf': [('1', 0.09), ('2', 0.05)]}
    result = global_inference(file_candidates, {})
    assert result['a.pdf']['best'] is None
    assert result['a.pdf']['candidates'] == []
    assert result['a.pdf']['status'] == 'none'
