from typing import Optional

_ROMAN_MAP = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def roman_to_int(roman: str) -> Optional[int]:
    """
    Convert a Roman numeral string to an integer.
    Returns None for invalid input.
    """
    if not roman:
        return None
    roman = roman.upper()
    total = 0
    prev = 0
    for ch in reversed(roman):
        val = _ROMAN_MAP.get(ch)
        if val is None:
            return None
        if val < prev:
            total -= val
        else:
            total += val
            prev = val
    return total if total > 0 else None
