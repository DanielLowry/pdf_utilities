
"""
inference.py — Chapter number inference logic for PDF utilities

This module provides the core logic for inferring chapter numbers from a set of PDF files.
It takes candidate chapter numbers (with confidence scores) extracted from each file's text,
and reconciles them globally to produce a best-guess mapping for each file, including ambiguous cases.

Key concepts:
- Candidates: Each file may have multiple possible chapter numbers, each with a confidence score.
- Global frequency: Candidates that appear frequently across files are considered more likely.
- Filename evidence: If a filename already contains a chapter number, that candidate is boosted.
- Ambiguity: If multiple candidates have similar scores, the file is flagged as ambiguous for user review.
- Confidence threshold: If the best candidate's score is below a minimum, the file is flagged as 'none'.

Returned mapping:
    {
        filename: {
            "best": (chapter_str, confidence),
            "candidates": [(chapter_str, confidence), ...],
            "status": "ok" | "ambiguous" | "none"
        },
        ...
    }

Usage:
    file_candidates = {
        'a.pdf': [('1', 0.9)],
        'b.pdf': [('2', 0.9)],
        'c.pdf': [('1', 0.7), ('2', 0.6)]
    }
    filename_chapters = {'a.pdf': '1'}
    result = global_inference(file_candidates, filename_chapters)

See tests/test_inference.py for examples.
"""

from typing import Dict, List, Tuple, Optional
from collections import Counter

# Candidate: (chapter_str, confidence)
Candidate = Tuple[str, float]

def global_inference(
    file_candidates: Dict[str, List[Candidate]],
    filename_chapters: Dict[str, str],
    expected_count: Optional[int] = None,
    min_confidence: float = 0.5
) -> Dict[str, Dict]:
    """
    For each file, select the best candidate chapter number using confidence scores, global frequency,
    and filename evidence. Returns a mapping for each file with the best candidate, all candidates (scored),
    and a status flag:
        - 'ok': confident assignment
        - 'ambiguous': multiple candidates with similar scores
        - 'none': no confident candidate found

    Args:
        file_candidates: Dict mapping filename to list of (chapter_str, confidence) candidates.
        filename_chapters: Dict mapping filename to chapter number found in filename (if any).
        expected_count: Optional expected number of chapters (not used in MVP, but could help).
        min_confidence: Minimum confidence required for 'ok' status (default 0.5).

    Returns:
        Dict mapping filename to dict with keys:
            'best': (chapter_str, confidence)
            'candidates': list of (chapter_str, confidence)
            'status': 'ok' | 'ambiguous' | 'none'
    """
    # Count all candidate numbers for global frequency
    all_candidates = [c[0] for cands in file_candidates.values() for c in cands]
    freq = Counter(all_candidates)
    result = {}
    for fname, cands in file_candidates.items():
        if not cands:
            result[fname] = {"best": None, "candidates": [], "status": "none"}
            continue
        # Score: confidence * (1 + freq weight)
        scored = [(c, conf * (1 + 0.2 * freq[c])) for c, conf in cands]
        scored.sort(key=lambda x: x[1], reverse=True)
        best = scored[0]
        # If filename has a chapter, boost that candidate
        if fname in filename_chapters:
            for i, (c, s) in enumerate(scored):
                if c == filename_chapters[fname]:
                    scored[i] = (c, s + 0.2)
            scored.sort(key=lambda x: x[1], reverse=True)
            best = scored[0]
        # Ambiguous if top two are close in score
        if len(scored) > 1 and (scored[0][1] - scored[1][1] < 0.1):
            status = "ambiguous"
        elif best[1] < min_confidence:
            status = "none"
        else:
            status = "ok"
        result[fname] = {"best": best, "candidates": scored, "status": status}
    return result
