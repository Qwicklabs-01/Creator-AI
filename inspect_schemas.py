import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = "repo_knowledge"

def show_json_schema(filepath, name):
    print(f"\n=================== {name} ===================")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            print(f"Type: dict with {len(data)} keys: {list(data.keys())[:10]}")
            for k, v in list(data.items())[:3]:
                print(f"  Key '{k}': {type(v)} -> {str(v)[:120]}...")
        elif isinstance(data, list):
            print(f"Type: list with {len(data)} items")
            for item in data[:3]:
                print(f"  Item: {type(item)} -> {str(item)[:120]}...")

show_json_schema(os.path.join(base, "linkedin-agent-skill", "skills_li-post_hooks.json"), "LinkedIn Post Hooks")
show_json_schema(os.path.join(base, "linkedin-agent-skill", "skills_li-human_slop.json"), "LinkedIn Slop Words")
show_json_schema(os.path.join(base, "youtube-agent-skill", "skills_yt-script_hooks.json"), "YouTube Script Hooks")
show_json_schema(os.path.join(base, "instagram-agent-skill", "skills_ig-reel_hooks.json"), "Instagram Reel Hooks")
show_json_schema(os.path.join(base, "promptmaster-skill", "waste-patterns.json"), "PromptMaster Waste Patterns")
show_json_schema(os.path.join(base, "linkedin-agent-skill", "skills_li-profile_rubric.json"), "LinkedIn Profile Rubric")
show_json_schema(os.path.join(base, "instagram-agent-skill", "skills_ig-profile_rubric.json"), "Instagram Profile Rubric")
