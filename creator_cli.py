#!/usr/bin/env python3
"""
creator_cli.py - Standalone Interactive Terminal Bot for 'Creator'
Provides interactive terminal menus, real-time hook scoring, prompt auditing,
and anti-slop cleaning based on Jake Schincariol's ecosystem.
"""

import os
import sys
import json
import creator_engine

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
 =========================================================================
   ⚡ CREATOR — AI Content Engineering & Growth Terminal Bot ⚡
   👑 Created by Sakshi • Synthesizing 68+ Hooks & AI Music Studio
 =========================================================================
    """
    print(banner)

def menu_linkedin():
    print("\n--- 💼 LINKEDIN HOOK SCORER & LINTER ---")
    print("Desktop truncation test (210 chars / 3 lines mobile) + formula detection")
    text = input("\nEnter LinkedIn Hook (or full draft):\n> ").strip()
    if not text: return
    res = creator_engine.score_linkedin_hook(text)
    print("\n" + "="*50)
    print(f"VERDICT: {res['verdict']}/100 [{res['band']}]")
    print(f"Hook Length: {res['char_count']} chars (Desktop Safe: {'YES' if res['desktop_safe'] else 'NO - TRUNCATES'})")
    print(f"Formula Match: {res['matched_formula']}")
    print(f"Line 1 Hook: {res['hook_line']}")
    print(f"Line 2 Payoff: {res['payoff_line']}")
    print("="*50)

def menu_youtube():
    print("\n--- 🎥 YOUTUBE RETENTION HOOK SCORER ---")
    print("0-15s Critical retention window & weakest-link scoring")
    text = input("\nEnter 0-15s Spoken Hook:\n> ").strip()
    if not text: return
    res = creator_engine.score_youtube_hook(text)
    print("\n" + "="*50)
    print(f"RETENTION VERDICT: {res['verdict']}/100 [{res['band']}]")
    print(f"Matched Formula: {res['matched_formula']} ({res['word_count']} words)")
    print("\n5-Dimension Score Breakdown:")
    for k, v in res['parts'].items():
        bar = "#" * (v // 5)
        print(f"  {k:<12} {v:3d}/100  {bar}")
    print(f"\nWeakest Link: {res['weakest']}")
    print(f"Fix Recommendation: {res['fix_recommendation']}")
    print("="*50)

def menu_instagram():
    print("\n--- 📸 INSTAGRAM REEL DUAL-HOOK SCORER ---")
    v_hook = input("On-Screen Text (<= 6 words):\n> ").strip()
    s_hook = input("Spoken Voiceover Hook:\n> ").strip()
    res = creator_engine.score_instagram_reel(s_hook, v_hook)
    print("\n" + "="*50)
    print(f"REEL VERDICT: {res['verdict']}/100 [{res['band']}]")
    print(f"On-Screen Score: {res['visual_score']}/100 - {res['visual_feedback']}")
    print(f"Spoken Voice Score: {res['spoken_score']}/100")
    print(f"Synergy: {res['synergy_score']}/100 - {res['synergy_feedback']}")
    print("="*50)

def menu_promptmaster():
    print("\n--- 🧠 PROMPTMASTER 35 CREDIT-WASTE AUDITOR ---")
    prompt = input("Enter raw prompt to audit:\n> ").strip()
    if not prompt: return
    res = creator_engine.audit_promptmaster(prompt)
    print("\n" + "="*50)
    print(f"PROMPT HEALTH SCORE: {res['health_score']}/100")
    print(f"Credit-Waste Traps Found: {res['patterns_count']}")
    print(f"Tokens Wasted in Retries: ~{res['estimated_wasted_tokens_per_run']} tokens")
    if res['waste_patterns_detected']:
        print("\nFlaws Detected:")
        for p in res['waste_patterns_detected']:
            print(f"  - [#{p['id']} {p['name']}] ({p['family']})")
            print(f"    Fix: {p['fix']}")
    print("\n--- 1-SHOT COMPILED PRODUCTION PROMPT ---")
    print(res['optimized_prompt'])
    print("="*50)

def menu_humanizer():
    print("\n--- 🛡️ ANTI-AI SLOP HUMANIZER ---")
    text = input("Enter text to inspect & clean:\n> ").strip()
    if not text: return
    det = creator_engine.detect_ai_slop(text)
    print("\n" + "="*50)
    print(f"HUMAN DETECTION SCORE: {det['human_score']}/100 ({det['verdict']})")
    print(f"Sentence CV: {det['sentence_variation_cv']} | Invisible Chars: {det['invisible_chars']} | Em-Dashes: {det['em_dashes']}")
    if det['slop_terms_found']:
        print("\nBanned Words Detected:")
        for s in det['slop_terms_found']:
            print(f"  - '{s['term']}' (x{s['count']}) -> '{s['replace']}'")
    
    hum = creator_engine.humanize_text(text)
    print("\n--- CLEANED HUMAN DRAFT ---")
    print(hum['humanized_text'])
    print(f"\nNew Human Score: {hum['new_human_score']}/100")
    print("="*50)

def menu_freellm():
    print("\n--- ⚡ FREELLMAPI MULTI-PROVIDER GATEWAY ---")
    from creator_model.freellm_gateway import gateway, FREE_PROVIDERS
    providers = gateway.get_active_providers()
    print("Configured Providers:")
    for p in providers:
        status_icon = "🟢" if "Active" in p["status"] else ("🟡" if "Cooldown" in p["status"] else "⚪")
        print(f" {status_icon} {p['name']} [{p['id']}]: {p['status']}")
    
    print("\nOptions:")
    print(" [1] Add/Update Free API Key (Groq, Gemini, Cerebras, Mistral, SambaNova)")
    print(" [2] Test Free Live Chat Completion")
    print(" [0] Back")
    
    sub = input("\nSelect: ").strip()
    if sub == "1":
        p_id = input("Enter Provider ID (groq, gemini, cerebras, mistral, sambanova, openrouter): ").strip().lower()
        key_val = input("Enter API Key: ").strip()
        if p_id and key_val:
            gateway.set_key(p_id, key_val)
            print(f"✓ Key saved for {p_id.upper()}!")
    elif sub == "2":
        prompt = input("Enter prompt to test live multi-provider inference:\n> ").strip()
        res = gateway.chat_complete(prompt, "You are Creator, the viral content engineering model.")
        if res.get("success"):
            print(f"\n✓ Generated via {res['provider_name']} ({res['model']}) in {res['latency_ms']}ms:")
            print(res["response"])
        else:
            print(f"\n⚠️ Error: {res.get('error')}")

def menu_singdia():
    print("\n--- 🎵 AI MUSIC STUDIO (Created by Sakshi) ---")
    print("Generate custom Indian songs across 12 languages with Suno/Udio prompts")
    recipient = input("Recipient Name [Pooja]: ").strip() or "Pooja"
    sender = input("From / Sender Name [Rahul]: ").strip() or "Rahul"
    occasion = input("Occasion (Birthday, Anniversary, Wedding, Friendship, Lullaby) [Birthday]: ").strip() or "Birthday"
    language = input("Language (Hindi, Hinglish, Punjabi, English, Tamil, Telugu, etc.) [Hinglish]: ").strip() or "Hinglish"
    genre = input("Genre (Bollywood Romantic, Punjabi Dhol, Modern Hindi Pop, Ghazal, Desi Hip-Hop) [Modern Hindi Pop]: ").strip() or "Modern Hindi Pop"
    memory = input("Shared Memory: ").strip() or "that crazy Goa road trip where the car broke down and we ate maggi at 3 AM"
    inside_joke = input("Inside Jokes / Quirks: ").strip() or "always stealing my fries and calling everyone bro"

    res = creator_engine.generate_singdia_song(
        recipient=recipient,
        sender=sender,
        occasion=occasion,
        memory=memory,
        inside_joke=inside_joke,
        language=language,
        genre=genre
    )

    arr1 = res["arrangements"][0]
    m1 = arr1["meter_analysis"]
    print("\n" + "="*60)
    print(f"🎵 AI MUSIC STUDIO ARRANGEMENT FOR {recipient.upper()} ({m1['overall_score']}/100 - {m1['rhyme_grade']})")
    print("="*60)
    print(f"\n🎧 [SUNO AI PROMPT]:\n{res['audio_prompts']['suno_prompt']}")
    print(f"\n📜 [LYRICS PREVIEW - {arr1['title']}]:\n")
    print(arr1["lyrics"])
    print("\n" + "="*60)

def main():
    while True:
        print_banner()
        print("Select Tool:")
        print(" [1] 💼 LinkedIn Hook Scorer & Truncation Linter")
        print(" [2] 🎥 YouTube 0-15s Retention Hook Auditor")
        print(" [3] 📸 Instagram Reel Dual-Hook Director")
        print(" [4] 🧠 PromptMaster 35 Credit-Waste Auditor")
        print(" [5] 🛡️ Anti-AI Slop Humanizer & Purifier")
        print(" [6] 🎵 AI Music Studio (12 Langs / Suno Prompts)")
        print(" [7] ⚡ FreeLLMAPI Multi-Provider Gateway (34 Free APIs)")
        print(" [8] 📚 Show Creator Master Stats & Knowledge")
        print(" [0] ❌ Exit")
        
        choice = input("\nEnter choice (0-8): ").strip()
        if choice == "1":
            menu_linkedin()
        elif choice == "2":
            menu_youtube()
        elif choice == "3":
            menu_instagram()
        elif choice == "4":
            menu_promptmaster()
        elif choice == "5":
            menu_humanizer()
        elif choice == "6":
            menu_singdia()
        elif choice == "7":
            menu_freellm()
        elif choice == "8":
            k = creator_engine.load_knowledge()
            print("\n" + "="*50)
            print("CREATOR KNOWLEDGE BASE STATS:")
            print(f"  - LinkedIn Hooks: {len(k.get('linkedin', {}).get('hooks', []))}")
            print(f"  - YouTube Hooks: {len(k.get('youtube', {}).get('hooks', []))}")
            print(f"  - Instagram Hooks: {len(k.get('instagram', {}).get('hooks', []))}")
            print(f"  - SingDia Music Languages: {len(k.get('singdia', {}).get('languages', []))}")
            print(f"  - SingDia Music Genres: {len(k.get('singdia', {}).get('genres', []))}")
            print(f"  - HyperFrames Blueprints: {len(k.get('hyperframes', {}).get('blueprints', []))}")
            print(f"  - Unhinged Modes: {len(k.get('unhinged_skills', []))}")
            print("="*50)
        elif choice == "0":
            print("\nExiting Creator. Keep shipping!")
            break
        else:
            print("\nInvalid option.")
        
        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    main()

