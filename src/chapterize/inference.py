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
    For each file, select the best candidate (highest confidence, most common across files, matches filename if present).
    Returns a dict: {filename: {"best": (chapter, conf), "candidates": [...], "status": "ok"|"ambiguous"|"none"}}
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
