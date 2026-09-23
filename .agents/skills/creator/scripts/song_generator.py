#!/usr/bin/env python3
"""
song_generator.py - SingDia AI Personalized Song & Lyrics Studio CLI
Generates customized Indian & global song lyrics, Suno AI audio prompts,
rhyming meter scoring, and gift dedication messages.
"""

import sys
import os
import argparse
import json

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import creator_engine

def main():
    parser = argparse.ArgumentParser(description="SingDia AI Personalized Song & Lyrics Generator")
    parser.add_argument("--recipient", type=str, default="Pooja", help="Recipient Name")
    parser.add_argument("--sender", type=str, default="Rahul", help="Sender Name / From")
    parser.add_argument("--occasion", type=str, default="Birthday", help="Occasion (Birthday, Anniversary, Wedding, etc.)")
    parser.add_argument("--relationship", type=str, default="Best Friend", help="Relationship")
    parser.add_argument("--language", type=str, default="Hinglish", help="Language: Hindi, Hinglish, Punjabi, English, etc.")
    parser.add_argument("--genre", type=str, default="Modern Hindi Pop", help="Genre: Modern Hindi Pop, Bollywood Romantic, Punjabi Dhol, etc.")
    parser.add_argument("--memory", type=str, default="that crazy Goa road trip where the car broke down", help="Shared memory or special story")
    parser.add_argument("--inside-joke", type=str, default="always stealing my fries", help="Inside jokes or quirks")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    res = creator_engine.generate_singdia_song(
        recipient=args.recipient,
        sender=args.sender,
        occasion=args.occasion,
        relationship=args.relationship,
        memory=args.memory,
        inside_joke=args.inside_joke,
        language=args.language,
        genre=args.genre
    )

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    arr1 = res["arrangements"][0]
    arr2 = res["arrangements"][1]
    m1 = arr1["meter_analysis"]

    print("=" * 60)
    print(f"🎵 SINGDIA AI PERSONALIZED SONG STUDIO — {args.recipient.upper()}")
    print("=" * 60)
    print(f"Occasion:     {res['meta']['occasion']} ({res['meta']['relationship']})")
    print(f"Language:     {res['meta']['language']} | Genre: {res['meta']['genre']}")
    print(f"Tempo & Mood: {res['meta']['tempo']} • {res['meta']['mood']}")
    print(f"Meter Score:  {m1['overall_score']}/100 | Rhyme Flow: {m1['rhyme_grade']}")
    print("-" * 60)
    print("\n🎧 [SUNO AI AUDIO GENERATION PROMPT]:")
    print(f"{res['audio_prompts']['suno_prompt']}")
    print(f"\n🏷️  [UDIO TAGS]: {res['audio_prompts']['udio_tags']}")
    print(f"🎤 [VOCAL DIRECTION]: {res['audio_prompts']['voice_style']}")
    print("-" * 60)
    print(f"\n📜 [ARRANGEMENT 1: {arr1['title'].upper()}]:\n")
    print(arr1['lyrics'])
    print("-" * 60)
    print(f"\n⚡ [ARRANGEMENT 2: {arr2['title'].upper()}]:\n")
    print(arr2['lyrics'])
    print("-" * 60)
    print(f"\n💌 [GIFT DEDICATION CARD MESSAGE]:")
    print(f"\"{res['gift_card_message']}\"\n")
    print("=" * 60)

if __name__ == "__main__":
    main()
