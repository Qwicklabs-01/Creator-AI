import json
import os
import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = "repo_knowledge"

def safe_load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 1. LinkedIn Knowledge
li_hooks = safe_load_json(os.path.join(base, "linkedin-agent-skill", "skills_li-post_hooks.json"))
li_slop = safe_load_json(os.path.join(base, "linkedin-agent-skill", "skills_li-human_slop.json"))
li_rubric = safe_load_json(os.path.join(base, "linkedin-agent-skill", "skills_li-profile_rubric.json"))

# 2. YouTube Knowledge
yt_hooks = safe_load_json(os.path.join(base, "youtube-agent-skill", "skills_yt-script_hooks.json"))

# 3. Instagram Knowledge
ig_hooks = safe_load_json(os.path.join(base, "instagram-agent-skill", "skills_ig-reel_hooks.json"))
ig_slop = safe_load_json(os.path.join(base, "instagram-agent-skill", "skills_ig-human_slop.json"))
ig_rubric = safe_load_json(os.path.join(base, "instagram-agent-skill", "skills_ig-profile_rubric.json"))

# 4. PromptMaster Knowledge
pm_waste = safe_load_json(os.path.join(base, "promptmaster-skill", "waste-patterns.json"))

# 5. Video Production / HyperFrames Blueprints
hyperframes_blueprints = []
blueprints_dir = os.path.join(base, "video-production-skills")
for fpath in glob.glob(os.path.join(blueprints_dir, "hyperframes-animation_blueprints_*.md")):
    b_name = os.path.basename(fpath).replace("hyperframes-animation_blueprints_", "").replace(".md", "")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else b_name.replace("-", " ").title()
        hyperframes_blueprints.append({
            "id": b_name,
            "title": title,
            "content": content[:2000]
        })

# 6. Unhinged Skills
unhinged_skills = []
for fpath in glob.glob(os.path.join(base, "unhinged-claude-skills", "*_SKILL.md")):
    s_name = os.path.basename(fpath).replace("_SKILL.md", "")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else s_name.replace("-", " ").title()
        unhinged_skills.append({
            "id": s_name,
            "title": title,
            "content": content
        })

# 7. SingDia Knowledge (AI Song & Lyrics Studio)
singdia_knowledge = {
    "brand": "SingDia",
    "description": "AI-Powered Personalized Song & Lyrics Studio in 12+ Indian & Global Languages",
    "languages": [
        {"id": "hindi", "name": "Hindi (हिंदी)", "popular": True},
        {"id": "hinglish", "name": "Hinglish (Urban Hindi-English)", "popular": True},
        {"id": "english", "name": "English", "popular": True},
        {"id": "punjabi", "name": "Punjabi (ਪੰਜਾਬੀ)", "popular": True},
        {"id": "tamil", "name": "Tamil (தமிழ்)", "popular": True},
        {"id": "telugu", "name": "Telugu (తెలుగు)", "popular": True},
        {"id": "marathi", "name": "Marathi (मराठी)", "popular": True},
        {"id": "bengali", "name": "Bengali (বাংলা)", "popular": True},
        {"id": "gujarati", "name": "Gujarati (ગુજરાતી)", "popular": True},
        {"id": "kannada", "name": "Kannada (ಕನ್ನಡ)", "popular": True},
        {"id": "malayalam", "name": "Malayalam (മലയാളം)", "popular": True},
        {"id": "urdu", "name": "Urdu (اردو)", "popular": True}
    ],
    "occasions": [
        {"id": "birthday", "name": "Birthday Song", "desc": "Custom celebration track with name, age & milestones"},
        {"id": "wedding", "name": "Wedding & Sangeet", "desc": "Energetic sangeet dance anthem or emotional bidaai song"},
        {"id": "anniversary", "name": "Anniversary", "desc": "Romantic retrospective celebrating years of togetherness"},
        {"id": "romance", "name": "Love & Romance", "desc": "Proposal, girlfriend/boyfriend special or heartfelt surprise"},
        {"id": "diwali", "name": "Diwali & Festivals", "desc": "Festive celebration song for family groups"},
        {"id": "rakhi", "name": "Raksha Bandhan", "desc": "Heartwarming brother-sister bond celebration"},
        {"id": "farewell", "name": "Farewell & Retirement", "desc": "Tribute to teachers, colleagues, or moving friends"},
        {"id": "corporate", "name": "Brand Anthem & Jingle", "desc": "Catchy company jingle, startup anthem or event opener"}
    ],
    "genres": [
        {"id": "bollywood", "name": "Bollywood Romantic Ballad", "mood": "Lush strings, acoustic guitar, emotional vocals, melodic flute"},
        {"id": "punjabi", "name": "Punjabi Sangeet / Bhangra", "mood": "Heavy dhol beats, tumbi, energetic drop, festive dance"},
        {"id": "hindi_pop", "name": "Hindi Pop / Urban", "mood": "Modern synth pop, 808 bass, upbeat rhythm, catchy hook"},
        {"id": "ghazal", "name": "Ghazal & Sufi", "mood": "Traditional harmonium, tabla, poetic Urdu shayars, deep soul"},
        {"id": "hiphop", "name": "Hindi Hip-Hop / Rap", "mood": "Trap drums, rapid-fire flow, storytelling verses, bass"},
        {"id": "retro", "name": "90s Bollywood Disco", "mood": "Vintage synth, brass section, disco beat, nostalgic melody"},
        {"id": "acoustic", "name": "Acoustic / Lo-Fi", "mood": "Soft guitar fingerpicking, piano chords, intimate vocals"},
        {"id": "lullaby", "name": "Sweet Lullaby (Loree)", "mood": "Gentle music box, soft strings, soothing parental warmth"}
    ],
    "song_structure": {
        "mukhda": "Chorus / Hook (Repeated theme with recipient's name)",
        "antara1": "Verse 1 (Personal memory, inside joke, origin story)",
        "antara2": "Verse 2 (Emotional gratitude, future wishes, milestones)",
        "bridge": "High-emotion musical build-up",
        "outro": "Warm closing sign-off and memorable tagline"
    }
}

master_knowledge = {
    "bot_name": "Creator",
    "author_origin": "Jake Schincariol + FreeLLMAPI + SingDia AI Music Ecosystem",
    "version": "3.0.0",
    "description": "Creator is the ultimate AI content engineering system, multi-platform growth studio, FreeLLM gateway, and SingDia personalized song studio. It unifies 68+ hook formulas, 35 PromptMaster patterns, anti-AI humanizers, 22 HyperFrames blueprints, 25 unhinged modes, and SingDia personalized music generation across 12 Indian languages.",
    "linkedin": {
        "rules": li_hooks.get("rules", []),
        "hooks": li_hooks.get("hooks", []),
        "slop_lexicon": li_slop,
        "profile_rubric": li_rubric
    },
    "youtube": {
        "rules": yt_hooks.get("rules", []),
        "hooks": yt_hooks.get("hooks", []),
        "guidelines": {
            "hook_duration": "0:00 - 0:15",
            "critical_retention_window": "0:00 - 0:30 (avoids 0:08 title disconnect drop-off)",
            "structure": ["0:00-0:15 Hook & Click Confirmation", "0:15-0:45 Context & Stakes", "0:45-3:00 Core Delivery", "Escalation & Payoff", "CTA"]
        }
    },
    "instagram": {
        "rules": ig_hooks.get("rules", []),
        "hooks": ig_hooks.get("hooks", []),
        "slop_lexicon": ig_slop,
        "profile_rubric": ig_rubric,
        "reel_structure": {
            "0-3s": "Visual Pattern Interrupt + Spoken Hook (<= 6 words on screen)",
            "3-15s": "Hold Curiosity & Setup",
            "15-45s": "High-Density Value / Delivery",
            "45-60s": "Payoff + Seamless Loop CTA"
        }
    },
    "promptmaster": {
        "count": pm_waste.get("count", 35),
        "families": pm_waste.get("families", []),
        "framework": {
            "core_elements": ["Context", "Role", "Task", "Format", "Negative Constraints", "Examples", "Decision Locks"]
        }
    },
    "hyperframes": {
        "blueprints": hyperframes_blueprints
    },
    "unhinged_skills": unhinged_skills,
    "singdia": singdia_knowledge
}

with open("creator_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(master_knowledge, f, indent=2, ensure_ascii=False)

print(f"Successfully compiled master creator_knowledge.json with SingDia Music Studio!")
print(f"SingDia Languages: {len(singdia_knowledge['languages'])}")
print(f"SingDia Occasions: {len(singdia_knowledge['occasions'])}")
print(f"SingDia Genres: {len(singdia_knowledge['genres'])}")
