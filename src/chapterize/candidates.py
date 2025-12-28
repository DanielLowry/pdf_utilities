import re
from typing import List, Tuple, Optional

Candidate = Tuple[str, float]  # (candidate_str, confidence)

# Regexes for chapter number extraction
CHAPTER_PATTERNS = [
    (re.compile(r"(?mi)^\s*(?:Chapter|CHAPTER|Ch)\s*[:\-\.]?\s*(\d{1,3})\b"), 0.95),
    (re.compile(r"(?mi)^\s*(?:Chapter|CHAPTER)\s+([IVXLCDM]+)\b"), 0.90),
    (re.compile(r"(?mi)^\s*Ch\.?\s*(\d{1,3})\b"), 0.85),
    (re.compile(r"(?m)^(\d{1,3})[\.\-\)]\s+\S+"), 0.80),
    (re.compile(r"(?m)^\s*(\d{1,3})\s*$"), 0.70),
]

ROMAN_MAP = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20
}

def roman_to_int(roman: str) -> Optional[int]:
    roman = roman.upper()
    return ROMAN_MAP.get(roman)

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
