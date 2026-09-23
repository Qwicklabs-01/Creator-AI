#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
import creator_engine

def main():
    parser = argparse.ArgumentParser(description="Score hooks for YouTube, LinkedIn, or Instagram Reels.")
    parser.add_argument("--platform", choices=["yt", "li", "ig"], default="yt", help="Platform: yt, li, or ig")
    parser.add_argument("--text", type=str, help="Hook text or full draft")
    parser.add_argument("--visual", type=str, default="", help="On-screen visual hook (for IG Reels)")
    args = parser.parse_args()

    text = args.text
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            text = input("Enter hook text: ").strip()

    if args.platform == "yt":
        res = creator_engine.score_youtube_hook(text)
        print("\n=== YOUTUBE HOOK SCORE ===")
        print(f"Verdict: {res['verdict']}/100 ({res['band']})")
        print(f"Matched Formula: {res['matched_formula']}")
        print(f"Word Count: {res['word_count']} words")
        print("Score Dimensions:")
        for k, v in res['parts'].items():
            bar = "#" * (v // 5)
            print(f"  {k:<12} {v:3d}/100  {bar}")
        print(f"Weakest Link: {res['weakest']}")
        print(f"Recommendation: {res['fix_recommendation']}\n")

    elif args.platform == "li":
        res = creator_engine.score_linkedin_hook(text)
        print("\n=== LINKEDIN HOOK SCORE ===")
        print(f"Verdict: {res['verdict']}/100 ({res['band']})")
        print(f"Characters: {res['char_count']} (Desktop Safe: {res['desktop_safe']})")
        print(f"Matched Formula: {res['matched_formula']}")
        print(f"Hook Line: {res['hook_line']}")
        print(f"Payoff Line: {res['payoff_line']}\n")

    elif args.platform == "ig":
        res = creator_engine.score_instagram_reel(text, args.visual)
        print("\n=== INSTAGRAM REEL DUAL-HOOK SCORE ===")
        print(f"Verdict: {res['verdict']}/100 ({res['band']})")
        print(f"Visual Text Score: {res['visual_score']}/100 - {res['visual_feedback']}")
        print(f"Spoken Voice Score: {res['spoken_score']}/100")
        print(f"Synergy: {res['synergy_score']}/100 - {res['synergy_feedback']}\n")

if __name__ == "__main__":
    main()
