"""
interactive.py — Interactive sign-off UI for chapterize

This module provides a console-based interface for reviewing and confirming inferred chapter assignments.
It presents the user with a summary table of all files, their top-N candidate chapters (with confidence scores), and allows per-file actions:
- Accept best guess
- Choose another candidate
- Edit manually
- Skip file
- Accept all

Ambiguous or missing assignments are clearly highlighted for user review.
"""
from typing import Dict, List, Tuple
import sys

def format_confidence(confidence: float) -> str:
    """Return the confidence as a rounded percentage string."""
    return f"{confidence * 100:.0f}%"


def print_table(mapping: Dict[str, Dict], top_n: int = 3):
    print("\nSuggested Chapter Assignments (confidence: 0% = low, 100% = high):\n")
    print(f"{'File':40} | {'Best':8} | {'Confidence':10} | Candidates (chapter [confidence])")
    print("-" * 100)
    for fname, info in mapping.items():
        best = info['best'][0] if info['best'] else '-'
        conf = format_confidence(info['best'][1]) if info['best'] else '-'
        cands = ', '.join([f"{c[0]} [{format_confidence(c[1])}]" for c in info['candidates'][:top_n]])
        status = info['status']
        marker = '!' if status != 'ok' else ' '
        print(f"{fname:40} | {best:8} | {conf:10} | {cands} {marker}")
    print("\n! = ambiguous or missing assignment\nConfidence: 0% = low, 100% = high\n")

def interactive_signoff(mapping: Dict[str, Dict], top_n: int = 3):
    print_table(mapping, top_n)
    print("Review the suggested assignments above.")
    print("Type 'all' to accept all, or enter a filename to review/edit individually.")
    accepted = {}
    while True:
        choice = input("Accept all, or filename to edit (or 'q' to quit): ").strip()
        if choice.lower() == 'all':
            for fname, info in mapping.items():
                accepted[fname] = info['best'][0] if info['best'] else None
            print("All assignments accepted.")
            break
        elif choice.lower() == 'q':
            print("Exiting without saving.")
            sys.exit(0)
        elif choice in mapping:
            info = mapping[choice]
            print(f"Candidates for {choice}:")
            for idx, (c, s) in enumerate(info['candidates'][:top_n]):
                print(f"  {idx+1}. {c} (confidence {format_confidence(s)})")
            print("  0. Enter manually")
            sel = input("Choose candidate number, 0 for manual, or 's' to skip: ").strip()
            if sel == 's':
                accepted[choice] = None
                print(f"Skipped {choice}.")
            elif sel == '0':
                manual = input("Enter chapter number manually: ").strip()
                accepted[choice] = manual if manual else None
            elif sel.isdigit() and 1 <= int(sel) <= min(top_n, len(info['candidates'])):
                accepted[choice] = info['candidates'][int(sel)-1][0]
                print(f"Accepted candidate {accepted[choice]} for {choice}.")
            else:
                print("Invalid selection.")
        else:
            print("File not found. Try again.")
    return accepted
