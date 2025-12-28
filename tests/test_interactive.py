import builtins
import pytest
from chapterize.interactive import print_table, interactive_signoff

# Sample mapping for UI tests
sample_mapping = {
    'a.pdf': {'best': ('1', 0.95), 'candidates': [('1', 0.95), ('2', 0.80)], 'status': 'ok'},
    'b.pdf': {'best': ('2', 0.90), 'candidates': [('2', 0.90), ('1', 0.70)], 'status': 'ambiguous'},
    'c.pdf': {'best': None, 'candidates': [], 'status': 'none'},
}

def test_print_table(capsys):
    print_table(sample_mapping, top_n=2)
    out = capsys.readouterr().out
    assert 'a.pdf' in out and 'b.pdf' in out and 'c.pdf' in out
    assert '! = ambiguous or missing assignment' in out

def test_interactive_signoff_accept_all(monkeypatch):
    # Simulate user typing 'all' to accept all assignments
    inputs = iter(['all'])
    monkeypatch.setattr(builtins, 'input', lambda _: next(inputs))
    accepted = interactive_signoff(sample_mapping, top_n=2)
    assert accepted['a.pdf'] == '1'
    assert accepted['b.pdf'] == '2'
    assert accepted['c.pdf'] is None

def test_interactive_signoff_per_file(monkeypatch):
    # Simulate user editing b.pdf to pick candidate 1, skipping c.pdf
    inputs = iter(['b.pdf', '1', 'c.pdf', 's', 'all'])
    monkeypatch.setattr(builtins, 'input', lambda _: next(inputs))
    accepted = interactive_signoff(sample_mapping, top_n=2)
    assert accepted['b.pdf'] == '2'  # Picked candidate 1 (which is '2')
    assert accepted['c.pdf'] is None
