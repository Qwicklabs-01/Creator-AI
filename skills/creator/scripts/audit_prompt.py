#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import creator_engine

def main():
    parser = argparse.ArgumentParser(description="Audit prompts against PromptMaster's 35 credit-waste patterns.")
    parser.add_argument("--prompt", type=str, help="Prompt to audit")
    args = parser.parse_args()

    prompt = args.prompt
    if not prompt:
        if not sys.stdin.isatty():
            prompt = sys.stdin.read().strip()
        else:
            prompt = input("Enter prompt to audit: ").strip()

    res = creator_engine.audit_promptmaster(prompt)
    print("\n=== PROMPTMASTER CREDIT-WASTE AUDIT ===")
    print(f"Prompt Health Score: {res['health_score']}/100")
    print(f"Waste Patterns Triggered: {res['patterns_count']}")
    print(f"Estimated Tokens Wasted in Retries: ~{res['estimated_wasted_tokens_per_run']} tokens")

    if res['waste_patterns_detected']:
        print("\nFlaws Detected:")
        for p in res['waste_patterns_detected']:
            print(f"  [#{p['id']} - {p['name']}] ({p['family']})")
            print(f"     Fix: {p['fix']}")

    print("\n=== 1-SHOT PRODUCTION-READY PROMPT ===")
    print(res['optimized_prompt'])
    print()

if __name__ == "__main__":
    main()
