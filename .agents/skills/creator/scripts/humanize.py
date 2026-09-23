#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import creator_engine

def main():
    parser = argparse.ArgumentParser(description="Audit and strip AI slop from text drafts.")
    parser.add_argument("--text", type=str, help="Text to humanize")
    parser.add_argument("--detect-only", action="store_true", help="Only run 5-check detection")
    args = parser.parse_args()

    text = args.text
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            text = input("Enter text to inspect: ").strip()

    detection = creator_engine.detect_ai_slop(text)
    print("\n=== AI SLOP DETECTION PANEL ===")
    print(f"Human Score: {detection['human_score']}/100 ({detection['verdict']})")
    print(f"Invisible Chars: {detection['invisible_chars']} | Em-Dashes: {detection['em_dashes']} | Sentence CV: {detection['sentence_variation_cv']}")
    print("Dimension Scores:")
    for k, v in detection['checks'].items():
        print(f"  {k:<14} {v:3d}/100")

    if detection['slop_terms_found']:
        print("\nBanned Buzzwords Detected:")
        for s in detection['slop_terms_found']:
            print(f"  - '{s['term']}' (x{s['count']}) -> Suggest: '{s['replace']}'")

    if not args.detect_only:
        humanized = creator_engine.humanize_text(text)
        print("\n=== HUMANIZED DRAFT ===")
        print(humanized['humanized_text'])
        print(f"\nNew Human Score: {humanized['new_human_score']}/100 ({humanized['new_verdict']})")
        print(f"Total Replacements: {len(humanized['replacements'])}\n")

if __name__ == "__main__":
    main()
