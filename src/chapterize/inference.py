
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

MIN_CANDIDATE_CONFIDENCE = 0.1

def global_inference(
    file_candidates: Dict[str, List[Candidate]],
    filename_chapters: Dict[str, str],
    expected_count: Optional[int] = None,
    min_confidence: float = 0.5,
    candidate_threshold: float = MIN_CANDIDATE_CONFIDENCE,
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
        candidate_threshold: Minimum displayed candidate score (default 0.1).

    Returns:
        Dict mapping filename to dict with keys:
            'best': (chapter_str, confidence)
            'candidates': list of (chapter_str, confidence)
            'status': 'ok' | 'ambiguous' | 'none'
    """
    # Count all candidate numbers for global frequency
    all_candidates = [c[0] for cands in file_candidates.values() for c in cands]
    freq = Counter(all_candidates)
    chapters_in_filenames = set(filename_chapters.values())
    assigned_chapters = Counter()
    result = {}
    for fname, cands in file_candidates.items():
        if not cands:
            result[fname] = {"best": None, "candidates": [], "status": "none"}
            continue
        # Score: base confidence, penalize duplicate assignments, boost filename evidence
        scored = []
        for c, conf in cands:
            # Penalize if candidate is assigned to multiple files (except if filename evidence)
            duplicate_penalty = 0.0
            if freq[c] > 1 and (fname not in filename_chapters or filename_chapters[fname] != c):
                duplicate_penalty = -0.4 * (freq[c] - 1)
            # Boost if filename evidence
            filename_boost = 0.0
            if fname in filename_chapters and filename_chapters[fname] == c:
                filename_boost = 0.5
            score = conf + filename_boost + duplicate_penalty
            # Clamp score to [0.0, 1.0]
            score = max(0.0, min(score, 1.0))
            scored.append((c, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        filtered = [(c, s) for c, s in scored if s >= candidate_threshold]
        if not filtered:
            result[fname] = {"best": None, "candidates": [], "status": "none"}
            continue
        best = filtered[0]
        assigned_chapters[best[0]] += 1
        # Ambiguous if top two are close in score or if best score is low
        ambiguous = len(filtered) > 1 and (filtered[0][1] - filtered[1][1] < 0.1)
        if ambiguous:
            status = "ambiguous"
        elif best[1] < min_confidence:
            status = "none"
        else:
            status = "ok"
        result[fname] = {"best": best, "candidates": filtered, "status": status}
    return result
