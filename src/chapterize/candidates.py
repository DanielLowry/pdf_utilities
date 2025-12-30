import re
from typing import List, Tuple, Optional

from pdf_common.numerals import roman_to_int

Candidate = Tuple[str, float]  # (candidate_str, confidence)

# Regexes for chapter number extraction
CHAPTER_PATTERNS = [
    (re.compile(r"(?mi)^\s*(?:Chapter|CHAPTER|Ch)\s*[:\-\.]?\s*(\d{1,3})\b"), 0.95),
    (re.compile(r"(?mi)^\s*(?:Chapter|CHAPTER|Ch)\s*[:\-\.]?\s*([IVXLCDM]+)\b"), 0.90),
    (re.compile(r"(?mi)^\s*(\d{1,3})\s*[\.\-\)]\s+\S+"), 0.80),
    (re.compile(r"(?mi)^\s*([IVXLCDM]+)\s*[\.\-\)]\s+\S+"), 0.78),
    (re.compile(r"(?m)^\s*(\d{1,3})\s*$"), 0.70),
]

def extract_candidates(text: Optional[str]) -> List[Candidate]:
    """Extracts candidate chapter numbers from text with confidence scores."""
    if not text:
        return []
    candidates = []
    for pattern, conf in CHAPTER_PATTERNS:
        for match in pattern.findall(text):
            val = match if isinstance(match, str) else match[0]
            if re.fullmatch(r"[IVXLCDM]+", val, re.I):
                num = roman_to_int(val)
                if num:
                    candidates.append((str(num), conf))
            elif val.isdigit():
                candidates.append((val, conf))
    return candidates
