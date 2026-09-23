import json
import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = "repo_knowledge"

print("================= REPOSITORIES OVERVIEW =================")
for d in os.listdir(base):
    dp = os.path.join(base, d)
    if os.path.isdir(dp):
        files = os.listdir(dp)
        print(f"Repo: {d} ({len(files)} files)")

# LinkedIn Hooks
li_hooks_p = os.path.join(base, "linkedin-agent-skill", "skills_li-post_hooks.json")
if os.path.exists(li_hooks_p):
    with open(li_hooks_p, "r", encoding="utf-8") as f:
        li_hooks = json.load(f)
        print(f"\n[LinkedIn Hooks]: {len(li_hooks)} formulas loaded")
        for i, h in enumerate(li_hooks[:5]):
            print(f"  {i+1}. {h.get('name', h.get('id', ''))} - {h.get('formula', h.get('template', ''))[:60]}...")

# YouTube Hooks
yt_hooks_p = os.path.join(base, "youtube-agent-skill", "skills_yt-script_hooks.json")
if os.path.exists(yt_hooks_p):
    with open(yt_hooks_p, "r", encoding="utf-8") as f:
        yt_hooks = json.load(f)
        print(f"\n[YouTube Hooks]: {len(yt_hooks)} formulas loaded")
        for i, h in enumerate(yt_hooks[:5]):
            print(f"  {i+1}. {h.get('name', h.get('id', ''))} - {h.get('formula', h.get('template', ''))[:60]}...")

# Instagram Hooks
ig_hooks_p = os.path.join(base, "instagram-agent-skill", "skills_ig-reel_hooks.json")
if os.path.exists(ig_hooks_p):
    with open(ig_hooks_p, "r", encoding="utf-8") as f:
        ig_hooks = json.load(f)
        print(f"\n[Instagram Hooks]: {len(ig_hooks)} formulas loaded")
        for i, h in enumerate(ig_hooks[:5]):
            print(f"  {i+1}. {h.get('name', h.get('id', ''))} - {h.get('formula', h.get('template', ''))[:60]}...")

# PromptMaster Waste Patterns
pm_p = os.path.join(base, "promptmaster-skill", "waste-patterns.json")
if os.path.exists(pm_p):
    with open(pm_p, "r", encoding="utf-8") as f:
        pm_patterns = json.load(f)
        print(f"\n[PromptMaster]: {len(pm_patterns.get('patterns', pm_patterns))} waste patterns loaded")

# LinkedIn Slop Words
slop_p = os.path.join(base, "linkedin-agent-skill", "skills_li-human_slop.json")
if os.path.exists(slop_p):
    with open(slop_p, "r", encoding="utf-8") as f:
        slop_data = json.load(f)
        print(f"\n[AI Slop Data]: Keys: {list(slop_data.keys()) if isinstance(slop_data, dict) else len(slop_data)}")

# Unhinged skills
unhinged_files = glob.glob(os.path.join(base, "unhinged-claude-skills", "*_SKILL.md"))
print(f"\n[Unhinged Skills]: {len(unhinged_files)} skills found")
for u in unhinged_files[:8]:
    print(f"  - {os.path.basename(u)}")

