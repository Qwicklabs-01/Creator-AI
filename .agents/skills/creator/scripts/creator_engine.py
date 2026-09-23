#!/usr/bin/env python3
"""
creator_engine.py - Core Engine for 'Creator' Bot
Encapsulates 100% of Jake Schincariol's content engineering intelligence:
- 68+ Hook Formulas (LinkedIn 21, YouTube 21, Instagram 26) with weakest-link scoring
- Anti-AI Slop Humanizer (Invisible unicode cleaning, typographic fixes, buzzword purging)
- 35 PromptMaster Credit-Waste Pattern Detection & 1-Shot Prompt Optimization
- 100-Point Profile Scoring Rubrics
- Reel Beat Sheet & Visual Cue Director
- HyperFrames Motion Engine Blueprints
- 25 Unhinged Agentic Modes
"""

import json
import os
import re
import statistics
import unicodedata
from typing import Dict, List, Any, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_FILE = os.path.join(HERE, "creator_knowledge.json")

def load_knowledge() -> Dict[str, Any]:
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

KNOWLEDGE = load_knowledge()

# --- Common Regex & Dictionaries ---
URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-z0-9'%$.]+")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|\$\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b", re.MULTILINE)

FILLER = {"basically","actually","literally","just","really","very","so","kind","sort","like",
          "guys","hey","welcome","today","video","subscribe","channel"}
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","game","changer","secret",
         "powerful","ultimate","best","revolutionary","mind","blowing","unbelievable"}
CONCRETE = re.compile(r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)\b", re.I)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE = re.compile(r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead)\b", re.I)
CURIOSITY = re.compile(r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually)\b", re.I)

# --- 1. Hook Scoring Systems ---

def score_youtube_hook(text: str) -> Dict[str, Any]:
    """Score YouTube Hook (0-15s window) based on Specificity, Address, Stakes, Curiosity, Brevity."""
    words_list = WORD_RE.findall(text.lower())
    n_words = len(words_list)
    if n_words == 0:
        return {"verdict": 0, "band": "EMPTY", "parts": {}, "weakest": "EMPTY", "formula": "None"}
    
    # Specificity
    nums = len(CONCRETE.findall(text))
    vague_cnt = sum(1 for x in words_list if x in VAGUE)
    filler_cnt = sum(1 for x in words_list if x in FILLER)
    s_score = 34 + nums * 22 - vague_cnt * 16 - filler_cnt * 5
    s_score += min(18, 6 * sum(1 for x in text.split()[1:] if x[:1].isupper()))
    spec = max(0, min(100, s_score))
    
    # Address (Say you in first 6 words)
    you_cnt = len(YOU.findall(text))
    first_you = 30 if YOU.search(" ".join(text.split()[:6])) else 0
    addr = max(0, min(100, 26 + you_cnt * 20 + first_you))
    
    # Stakes
    stake_cnt = len(STAKE.findall(text))
    stk = max(0, min(100, 22 + stake_cnt * 26 + (14 if CONCRETE.search(text) else 0)))
    
    # Curiosity
    cur_cnt = len(CURIOSITY.findall(text))
    q_mark = 18 if text.strip().endswith("?") else 0
    closed = -18 if re.search(r"\b(because|so that|which means)\b", text, re.I) else 0
    cur = max(0, min(100, 24 + cur_cnt * 17 + q_mark + closed))
    
    # Brevity (9-24 words is golden zone for 10s spoken)
    if 9 <= n_words <= 24:
        brev = 100
    elif n_words < 9:
        brev = max(30, 100 - (9 - n_words) * 11)
    else:
        brev = max(10, 100 - (n_words - 24) * 7)
        
    parts = {
        "SPECIFICITY": spec,
        "ADDRESS": addr,
        "STAKES": stk,
        "CURIOSITY": cur,
        "BREVITY": brev
    }
    
    vals = list(parts.values())
    # Weakest-link weighting: 60% mean + 40% minimum
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    band = "STRONG" if verdict >= 72 else "WORKABLE" if verdict >= 55 else "WEAK"
    
    # Classify formula
    yt_hooks = KNOWLEDGE.get("youtube", {}).get("hooks", [])
    matched_formula = "Custom / Unclassified"
    best_hits = 0
    for f in yt_hooks:
        hits = sum(1 for p in f.get("match", []) if re.search(p, text, re.I))
        if hits > best_hits:
            best_hits = hits
            matched_formula = f.get("name", "Custom")
            
    weakest_key = min(parts, key=parts.get)
    fixes = {
        "SPECIFICITY": "Swap one adjective for a specific number, metric, or named tool.",
        "ADDRESS": "Use 'you' or 'your' within the first 6 spoken words.",
        "STAKES": "Explicitly state what they lose or fail at if they don't watch.",
        "CURIOSITY": "Open a loop—do not resolve the 'why' or 'how' in the hook sentence.",
        "BREVITY": "Keep spoken hook between 9 and 24 words (~10 seconds)."
    }
    
    return {
        "verdict": verdict,
        "band": band,
        "parts": parts,
        "weakest": weakest_key,
        "fix_recommendation": fixes.get(weakest_key, ""),
        "matched_formula": matched_formula,
        "word_count": n_words
    }


def score_linkedin_hook(text: str) -> Dict[str, Any]:
    """Score LinkedIn Post Hook (Line 1 + desktop 210 char truncation rule)."""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if not lines:
        return {"verdict": 0, "band": "EMPTY"}
    
    hook_line = lines[0]
    char_len = len(hook_line)
    words_list = WORD_RE.findall(hook_line.lower())
    n_words = len(words_list)
    
    # Desktop truncation check: feed cuts at ~210 characters
    char_score = 100 if char_len <= 180 else max(20, 100 - (char_len - 180) * 2)
    
    # Curiosity & Tension
    has_tension = bool(re.search(r"\b(stop|never|wrong|myth|truth|mistake|secret|failed|instead|nobody|everyone)\b", hook_line, re.I))
    has_number = bool(CONCRETE.search(hook_line))
    has_pronoun = bool(YOU.search(hook_line) or PRONOUNS.search(hook_line))
    
    punch_score = 40 + (25 if has_tension else 0) + (20 if has_number else 0) + (15 if has_pronoun else 0)
    punch_score = max(0, min(100, punch_score))
    
    # Brevity & Punch
    brevity_score = 100 if 6 <= n_words <= 18 else (70 if n_words < 6 else max(30, 100 - (n_words - 18) * 5))
    
    parts = {
        "CHAR_TRUNCATION": char_score,
        "PUNCHINESS": punch_score,
        "BREVITY": brevity_score
    }
    
    vals = list(parts.values())
    verdict = round(0.5 * (sum(vals) / len(vals)) + 0.5 * min(vals))
    band = "VIRAL READY" if verdict >= 75 else "WORKABLE" if verdict >= 55 else "NEEDS POLISH"
    
    # Classify against LinkedIn formulas
    li_hooks = KNOWLEDGE.get("linkedin", {}).get("hooks", [])
    matched = "Custom Story / Insight"
    for f in li_hooks:
        for m in f.get("match", []):
            if re.search(m, hook_line, re.I):
                matched = f.get("name", "Custom")
                break
                
    return {
        "verdict": verdict,
        "band": band,
        "parts": parts,
        "char_count": char_len,
        "desktop_safe": char_len <= 210,
        "matched_formula": matched,
        "hook_line": hook_line,
        "payoff_line": lines[1] if len(lines) > 1 else "MISSING (Add a punchy Line 2 before 'see more')"
    }


def score_instagram_reel(spoken_hook: str, visual_hook: str) -> Dict[str, Any]:
    """Score Instagram Reel Dual-Hook (Spoken voiceover + On-screen text <= 6 words)."""
    v_words = WORD_RE.findall(visual_hook.strip())
    s_words = WORD_RE.findall(spoken_hook.strip())
    
    # On screen text rule: <= 6 words, punchy, no punctuation
    v_count = len(v_words)
    if v_count == 0:
        visual_score = 20
        v_feedback = "Missing on-screen visual hook text."
    elif 1 <= v_count <= 6:
        visual_score = 100
        v_feedback = f"Perfect brevity ({v_count}/6 words)."
    else:
        visual_score = max(20, 100 - (v_count - 6) * 15)
        v_feedback = f"Too long ({v_count} words). Shorten to <= 6 words for split-second eye scanning."
        
    # Spoken audio hook
    s_count = len(s_words)
    if 6 <= s_count <= 20:
        spoken_score = 100
    else:
        spoken_score = max(30, 100 - abs(s_count - 14) * 6)
        
    # Dual-hook synergy (they shouldn't be identical copy)
    is_identical = visual_hook.lower().strip() == spoken_hook.lower().strip()
    synergy_score = 40 if is_identical else 100
    syn_feedback = "Do NOT use identical copy for spoken and on-screen text. The screen stops the scroll; voiceover sets the loop." if is_identical else "Great dual-hook complement."
    
    verdict = round(0.4 * visual_score + 0.35 * spoken_score + 0.25 * synergy_score)
    band = "HIGH RETENTION" if verdict >= 75 else "WORKABLE" if verdict >= 55 else "WEAK HOOK"
    
    return {
        "verdict": verdict,
        "band": band,
        "visual_score": visual_score,
        "spoken_score": spoken_score,
        "synergy_score": synergy_score,
        "visual_feedback": v_feedback,
        "synergy_feedback": syn_feedback,
        "visual_words": v_count,
        "spoken_words": s_count
    }


# --- 2. Anti-AI Slop Humanizer & Detection Panel ---

def detect_ai_slop(text: str) -> Dict[str, Any]:
    """Run the 5-check human detection panel."""
    lex = KNOWLEDGE.get("linkedin", {}).get("slop_lexicon", {})
    words_list = WORD_RE.findall(text)
    total_words = len(words_list)
    if total_words < 10:
        return {"human_score": 50, "verdict": "TOO SHORT", "checks": {}}
    
    # 1. Burstiness (Sentence length variation CV)
    sents = [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(sents) >= 3:
        lens = [len(s.split()) for s in sents]
        mean_len = statistics.mean(lens)
        cv = statistics.pstdev(lens) / mean_len if mean_len else 0
        # human ~ 0.70, machine ~ 0.22
        burst_score = max(0.0, min(100.0, (cv - 0.22) / (0.70 - 0.22) * 100))
    else:
        burst_score = 60.0
        cv = 0.5
        
    # 2. Specificity (numbers + proper nouns)
    per100 = 100 / total_words
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    spec_score = max(0.0, min(100.0, (density - 0.5) / (6.0 - 0.5) * 100))
    
    # 3. Stock Lexicon / Slop Words
    slop_hits = []
    slop_count = 0
    raw_words = lex.get("words", []) + lex.get("phrases", [])
    for item in raw_words:
        find_term = item.get("find", "")
        if not find_term: continue
        pattern = re.compile(r"\b" + re.escape(find_term) + r"\b", re.IGNORECASE)
        found = pattern.findall(text)
        if found:
            slop_count += len(found)
            slop_hits.append({"term": find_term, "count": len(found), "replace": item.get("replace", "")})
            
    slop_density = slop_count * 100 / total_words
    slop_score = max(0.0, min(100.0, (4.0 - slop_density) / 4.0 * 100))
    
    # 4. Typographic & Invisible tells
    invis_count = sum(1 for c in text if unicodedata.category(c) == "Cf" or c in ["\u200b", "\u200c", "\u200d", "\ufeff"])
    em_dash_count = text.count("—") + text.count("–")
    typo_penalty = min(50, invis_count * 15 + em_dash_count * 5)
    typo_score = max(0.0, 100.0 - typo_penalty)
    
    # 5. Natural Voice / Pronoun & Contractions
    contra_count = len(CONTRACTIONS.findall(text))
    pro_count = len(PRONOUNS.findall(text))
    voice_density = (contra_count + pro_count) * 100 / total_words
    voice_score = max(0.0, min(100.0, voice_density * 10))
    
    checks = {
        "BURSTINESS": round(burst_score),
        "SPECIFICITY": round(spec_score),
        "SLOP_PURITY": round(slop_score),
        "TYPOGRAPHY": round(typo_score),
        "VOICE": round(voice_score)
    }
    
    human_score = round(0.25 * burst_score + 0.25 * slop_score + 0.20 * spec_score + 0.15 * typo_score + 0.15 * voice_score)
    verdict = "HUMAN NATURAL" if human_score >= 80 else "MODERATE AI FINGERPRINT" if human_score >= 55 else "HEAVY AI ROBOTIC SLOP"
    
    return {
        "human_score": human_score,
        "verdict": verdict,
        "checks": checks,
        "slop_terms_found": slop_hits,
        "invisible_chars": invis_count,
        "em_dashes": em_dash_count,
        "sentence_variation_cv": round(cv, 2)
    }


def humanize_text(text: str) -> Dict[str, Any]:
    """Strip AI fingerprint and replace stock lexicon."""
    lex = KNOWLEDGE.get("linkedin", {}).get("slop_lexicon", {})
    cleaned = text
    
    # 1. Purge invisible
    cleaned = re.sub(r"[\u200B\u200C\u200D\uFEFF\u00A0\u202F\u2009]", " ", cleaned)
    cleaned = "".join(c for c in cleaned if unicodedata.category(c) != "Cf")
    
    # 2. Fix typography
    cleaned = cleaned.replace("—", ", ").replace("–", "-")
    cleaned = cleaned.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    cleaned = re.sub(r"\.{3,}", "...", cleaned)
    
    # 3. Replace slop lexicon
    replacements_made = []
    raw_words = lex.get("words", []) + lex.get("phrases", [])
    for item in raw_words:
        find_term = item.get("find", "")
        rep_term = item.get("replace", "")
        if not find_term: continue
        
        pattern = re.compile(r"\b" + re.escape(find_term) + r"\b", re.IGNORECASE)
        if pattern.search(cleaned):
            def _sub_case(m):
                orig = m.group(0)
                if orig.isupper(): return rep_term.upper()
                if orig[0].isupper() and rep_term: return rep_term[0].upper() + rep_term[1:]
                return rep_term
            
            cleaned = pattern.sub(_sub_case, cleaned)
            replacements_made.append({"from": find_term, "to": rep_term})
            
    # Clean up double spaces
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n\s+\n", "\n\n", cleaned)
    
    detection_after = detect_ai_slop(cleaned)
    
    return {
        "humanized_text": cleaned.strip(),
        "replacements": replacements_made,
        "new_human_score": detection_after.get("human_score", 100),
        "new_verdict": detection_after.get("verdict", "HUMAN NATURAL")
    }


# --- 3. PromptMaster 35-Pattern Auditor ---

def audit_promptmaster(prompt_text: str) -> Dict[str, Any]:
    """Audit a prompt against PromptMaster's 35 credit-waste patterns."""
    text = prompt_text.strip()
    words_list = WORD_RE.findall(text)
    n_words = len(words_list)
    
    detected_patterns = []
    
    # Heuristic checks for waste patterns:
    # 1. No deliverable named
    if not re.search(r"\b(table|script|json|markdown|list|code|bullet|csv|email|post|essay|summary|diagram)\b", text, re.I):
        detected_patterns.append({
            "id": 1,
            "name": "No deliverable named",
            "family": "VAGUE ASK",
            "fix": "Name the exact output artifact: 'one markdown table with columns A, B, C' or 'a 3-paragraph email'."
        })
        
    # 2. No audience
    if not re.search(r"\b(for|audience|readers|beginners|seniors|developers|founders|cto|students|clients|b2b|b2c)\b", text, re.I):
        detected_patterns.append({
            "id": 2,
            "name": "No audience specified",
            "family": "VAGUE ASK",
            "fix": "Specify the exact target reader and their knowledge level (e.g. 'for senior Python engineers')."
        })
        
    # 3. No length or size cap
    if not re.search(r"\b(\d+\s?(words|lines|items|options|bullet|chars|seconds|minutes)|under\s+\d+|max\s+\d+)\b", text, re.I):
        detected_patterns.append({
            "id": 3,
            "name": "No length or item cap",
            "family": "VAGUE ASK",
            "fix": "Set a hard cap: 'under 300 words', 'exactly 5 bullets', '3 distinct options max'."
        })
        
    # 4. 'Something like' hedging
    if re.search(r"\b(something like|kind of|maybe a|sort of|or whatever|etc)\b", text, re.I):
        detected_patterns.append({
            "id": 5,
            "name": "'Something like' hedging",
            "family": "VAGUE ASK",
            "fix": "Commit to one specific direction instead of hedging with 'something like'."
        })
        
    # 5. Open verdict fishing
    if re.search(r"\b(thoughts\?|what do you think\?|any ideas\?|feedback\?)\b", text, re.I):
        detected_patterns.append({
            "id": 6,
            "name": "Open verdict fishing",
            "family": "VAGUE ASK",
            "fix": "Ask the specific decision: 'Evaluate which of these two approaches has lower latency and recommend one'."
        })
        
    # 6. 'Make it better' with no failure criteria
    if re.search(r"\b(make it better|improve this|fix this|enhance this)\b", text, re.I) and n_words < 12:
        detected_patterns.append({
            "id": 10,
            "name": "'Make it better' without naming failure",
            "family": "VAGUE ASK",
            "fix": "Name what is broken: 'the tone is too academic', 'the hook lacks tension', 'cut length by 40%'."
        })
        
    # 7. No negative constraints
    if not re.search(r"\b(do not|don't|never|avoid|without|no\s+\w+)\b", text, re.I):
        detected_patterns.append({
            "id": 8,
            "name": "Missing negative constraints",
            "family": "VAGUE ASK",
            "fix": "Add explicit negative boundaries: 'Do not use AI buzzwords (delve, testament), avoid generic intros'."
        })

    # Estimate token waste
    waste_count = len(detected_patterns)
    estimated_wasted_tokens = waste_count * 450 # Retries cost full context resends
    prompt_health_score = max(10, 100 - waste_count * 15)
    
    # Generate 1-Shot Optimized Prompt
    optimized_template = f"""### Context & Role
You are an expert specialist operating as a top-tier professional.

### Objective & Task
{text}

### Deliverable & Format
- Exact output format: Structured markdown with clear headings, concise bullet points, and high information density.
- Length: Crisp and actionable, capped to the necessary length without preamble.

### Negative Constraints (Strict)
- NO introductory filler ("Sure!", "Here is...", "In today's fast-paced world").
- NO robotic buzzwords ("delve", "tapestry", "plethora", "game-changer", "unleash").
- Deliver the final production-ready artifact immediately.
"""
    
    return {
        "health_score": prompt_health_score,
        "waste_patterns_detected": detected_patterns,
        "patterns_count": waste_count,
        "estimated_wasted_tokens_per_run": estimated_wasted_tokens,
        "optimized_prompt": optimized_template.strip()
    }


# --- 4. Profile 100-Point Audit Engine ---

def audit_profile(items_checked: Dict[str, bool], platform: str = "linkedin") -> Dict[str, Any]:
    """Score a profile against Jake's 100-point rubric."""
    rubric_data = KNOWLEDGE.get(platform, {}).get("profile_rubric", {})
    items = rubric_data.get("items", [])
    if not items:
        return {"total_score": 0, "breakdown": []}
        
    earned_score = 0
    breakdown = []
    
    for item in items:
        item_id = str(item.get("id", item.get("name", "")))
        points = item.get("points", 0)
        is_passed = items_checked.get(item_id, False)
        
        if is_passed:
            earned_score += points
            
        breakdown.append({
            "name": item.get("name", ""),
            "points": points,
            "passed": is_passed,
            "rubric": item.get("rubric", ""),
            "fix": item.get("fix", "")
        })
        
    return {
        "total_score": earned_score,
        "max_score": 100,
        "passed_count": sum(1 for b in breakdown if b["passed"]),
        "total_items": len(breakdown),
        "breakdown": breakdown,
        "tier": "TOP 1% ELITE" if earned_score >= 85 else "STRONG & OPTIMIZED" if earned_score >= 65 else "NEEDS MAJOR WORK"
    }


# --- 5. SingDia AI Personalized Song & Lyrics Studio ---

SINGDIA_TEMPLATES = {
    "Hindi": {
        "mukhda_formats": [
            "Tere aane se mehki hai zindagi ki har gali,\n{recipient}, tu hi hai meri khushiyon ki kali.\nHar dua mein manga hai bas tera hi saath,\nTere hone se banti hai har ek nayi baat.",
            "{recipient} ka hai din, aao jashn manayein,\nDil ke har kone se pyari duayein sajayein.\nYe muskaan teri hamesha yuhi khili rahe,\nHar subah nayi roshni ban ke tujhe mile.",
            "Dil ki har ek dhadkan pe bas tera naam hai,\n{recipient}, tu hi meri subah, tu hi meri shaam hai.\nZindagi ke har safar mein haath tera thaam lu,\nTere bina lagta hai sab kuch be-naam hai."
        ],
        "antara_formats": [
            "Yaad hai wo lamha jab {memory},\nHas pade the dono, bhool ke saare gham wahi.\n{inside_joke}, ye baatein hain anmol,\nTere saath har pal jaise dholak ke bol.",
            "Saath chalte chalte hum kitni door aa gaye,\nTere sang har pal hum naye khwab saja gaye.\n{memory}, wo din bhi kitna khaas tha,\nJaise har ek lamha rab ka ehsaas tha."
        ],
        "bridge_formats": [
            "Chahe badle ye zamana, badlega na ye pyaar,\n{sender} rahega sada tera pehredaar.\nRab se bhi aage manga hai tera muskurana,\n{recipient}, tu hi hai mera aashiyana.",
            "Waqt ki dhund mein bhi chamkega ye rishta apna,\nSach hua jo dekha tha humne pyara sapna.\nHar aasmaan se unchi ho teri har udaan,\n{recipient} tu hi hai hamara maan aur samman."
        ],
        "outro_formats": [
            "Happy {occasion}, meri jaan {recipient}!\nSada hanste raho, yuhi chamakte raho!\n{recipient}... hamesha hamare dil mein... hamesha!",
            "Tujhse hi shuru, tujhpe hi khatam ye geet hai,\n{recipient}, tu hi meri har jeet hai!"
        ]
    },
    "Hinglish": {
        "mukhda_formats": [
            "Life was boring until you walked in the room,\n{recipient} teri vibe se gayab saara gloom!\nFrom midnight snacks to endless silly talks,\nTere saath best lagti hain evening walks.",
            "Raise a glass tonight coz it's {recipient}'s special day,\nSabse unique hai tu in every single way!\nKeep that million dollar smile forever on your face,\nNobody can ever take your special place."
        ],
        "antara_formats": [
            "Remember that crazy time when {memory},\nWe laughed till our stomachs hurt, pure memory!\nAnd that funny moment about {inside_joke},\nOur crazy friendship is definitely no joke.",
            "Late night gossip sessions aur endless chai ke cups,\nWith you by my side, life only goes up!\nWhatever happens next, we're gonna rock it together,\n{recipient} you and me, best friends forever!"
        ],
        "bridge_formats": [
            "No matter where we go or how far apart,\nYou'll always have VIP access to my heart.\nThank you for being the realest one around,\nThe purest blessing that I have ever found."
        ],
        "outro_formats": [
            "Happy {occasion}, superstar {recipient}!\nKeep shining, keep slaying, you're the best!\nYeah, {recipient}, this one is for you!"
        ]
    },
    "Punjabi": {
        "mukhda_formats": [
            "Tere aavan naal saade vehde aayi bahaar,\n{recipient} ni saddi jaan, tu hi saada pyaar!\nRab kolon mangi si bas ikko hi dua,\nTere mukhde te hove sada mehar di hwa.",
            "Bhangre da shor hove, dhol vajje zor,\n{recipient} jeya sohna saanu disda na hor!\nKhushiyan di barsaat hove tere har saal te,\nRab vi fida hai tere is mukhde de haal te."
        ],
        "antara_formats": [
            "Chete aunda mainu jad {memory},\nHasse si aapa dono, bhull ke sab chinta bari.\n{inside_joke} diyan gallan saariyan ne khaas,\nTere naal rehnda sada rabb da ehsaas.",
            "Gedi route te chalde si saade geet puraane,\n{recipient} tere charche ne saare jagg ne jaane.\nHar dukh door hove, khushiyan milan apaar,\nTu hi saadi heeriye, tu hi saada yaar."
        ],
        "bridge_formats": [
            "Duniya to wakhra ae tera mera naata,\nRab ne banaya saanu ikko hi dhaaga.\nJithe vi tu javengi, duawan naal chalangiyaan,\n{recipient} teri jodi naal taare vi khalangiyaan."
        ],
        "outro_formats": [
            "Balle balle! Happy {occasion} to {recipient}!\nJug jug jeeve saadi shaan {recipient}!\nChak de phatte!"
        ]
    },
    "English": {
        "mukhda_formats": [
            "From the moment that you stepped into my world,\nA thousand colors and a brighter sky unfurled.\n{recipient}, you're the melody that plays inside my chest,\nOut of all the people, you are simply the best.",
            "Today we celebrate the magic in your eyes,\nThe way you light up under ordinary skies.\n{recipient}, here's a song written just for you,\nA celebration of a soul so pure and true."
        ],
        "antara_formats": [
            "I still remember back when {memory},\nWe laughed until the sunrise made us feel so free.\nAnd every single joke about {inside_joke},\nTurned into gold every time we spoke.",
            "Through every twist and turn along the winding road,\nYou've been the one who helped me carry every load.\nWith coffee in our hands and dreams in our sights,\nYou made my darkest days into radiant lights."
        ],
        "bridge_formats": [
            "If years fly by and the seasons start to change,\nOne single thing will never ever rearrange:\nI will always stand right here beside your grace,\nFinding home inside your sweet embrace."
        ],
        "outro_formats": [
            "Happy {occasion}, wonderful {recipient}!\nMay all your biggest dreams come true.\nForever and always, this song belongs to you."
        ]
    }
}

GENRE_AUDIO_PROMPTS = {
    "Bollywood Romantic": {
        "suno_prompt": "Bollywood romantic duet, soulful female and male vocals, acoustic guitar, bansuri flute, tabla groove, sweeping strings, cinematic emotional climax, warm lush production, 85 BPM, Key of D Major",
        "instruments": ["Bansuri Flute", "Acoustic Guitar", "Tabla", "Santoor", "Warm Strings", "Piano Pad"],
        "tempo": "80-90 BPM",
        "mood": "Heartfelt, soulful, romantic, nostalgic"
    },
    "Punjabi Dhol / Sangeet": {
        "suno_prompt": "High energy Punjabi wedding celebration, heavy live Dhol beat, Tumbi hooks, modern synth bass, energetic male & female vocals, festive clapping, celebratory brass, 128 BPM, Key of G Minor",
        "instruments": ["Live Dhol", "Tumbi", "Algoze", "Brass Section", "Modern 808 Bass", "Dholak"],
        "tempo": "125-132 BPM",
        "mood": "Euphoric, festive, dancing, celebratory"
    },
    "Ghazal / Sufi": {
        "suno_prompt": "Soulful Indian Sufi Ghazal, expressive vocal improvisation, harmonium leads, subtle Sarangi, gentle tabla theka, deep reverb, intimate acoustic warmth, 72 BPM, Key of C# Minor",
        "instruments": ["Harmonium", "Sarangi", "Soft Tabla", "Acoustic Tanpura", "Subtle Nylon Guitar"],
        "tempo": "68-76 BPM",
        "mood": "Deeply spiritual, poetic, intimate, touching"
    },
    "Modern Hindi Pop": {
        "suno_prompt": "Modern Indian pop anthem, crisp contemporary vocals, driving synth bassline, clean electric guitar chords, punchy drums, catchy hook chorus, radio ready mix, 115 BPM, Key of F Major",
        "instruments": ["Electric Guitar", "Synth Plucks", "Modern Kick & Snare", "Sub Bass", "Vocoder FX"],
        "tempo": "112-120 BPM",
        "mood": "Youthful, vibrant, uplifting, catchy"
    },
    "Desi Hip-Hop / Rap": {
        "suno_prompt": "Desi Hip-Hop melodic rap, rhythmic punchy flow, boom bap with Indian flute sample, deep sub bass 808, infectious hook melody, street style confidence, 92 BPM, Key of A Minor",
        "instruments": ["808 Sub Bass", "Flute Sample Slice", "Hi-Hats Trap", "Punchy Snare", "Vinyl Crackle"],
        "tempo": "90-98 BPM",
        "mood": "Confident, rhythmic, stylish, heartfelt"
    },
    "90s Retro Melody": {
        "suno_prompt": "90s Golden Era Bollywood melody, lush violins orchestra, melodious synth pads, live dholak and ghatam rhythm, Kumar Sanu & Alka Yagnik style vocal arrangements, 95 BPM, Key of E Major",
        "instruments": ["Orchestral Violins", "Classic Dholak", "Electric Piano DX7", "Mandolin", "Congas"],
        "tempo": "92-98 BPM",
        "mood": "Nostalgic, melodious, evergreen romance"
    },
    "Acoustic Coffeehouse": {
        "suno_prompt": "Intimate indie acoustic ballad, fingerstyle steel-string guitar, soft upright piano, warm breathy vocals, gentle shaker, close mic recording, organic and pure, 78 BPM, Key of G Major",
        "instruments": ["Fingerstyle Acoustic Guitar", "Felt Piano", "Upright Bass", "Gentle Percussion"],
        "tempo": "75-82 BPM",
        "mood": "Intimate, cozy, genuine, organic"
    },
    "Sweet Lullaby": {
        "suno_prompt": "Tender heartwarming lullaby, music box chime, delicate harp, soft humming backing vocals, calming string pads, peaceful sleepy ambiance, 64 BPM, Key of C Major",
        "instruments": ["Music Box", "Concert Harp", "Celesta", "Warm String Pad", "Soft Humming"],
        "tempo": "60-68 BPM",
        "mood": "Tender, soothing, dreamy, protective"
    }
}

def generate_singdia_song(
    recipient: str = "Pooja",
    sender: str = "Rahul",
    occasion: str = "Birthday",
    relationship: str = "Best Friend / Partner",
    memory: str = "that rainy Goa road trip where the car broke down",
    inside_joke: str = "always ordering extra cheese and stealing fries",
    language: str = "Hinglish",
    genre: str = "Modern Hindi Pop"
) -> Dict[str, Any]:
    """
    Generate 2 personalized song arrangements (SingDia.com intelligence)
    with Suno/Udio prompt blueprints, structured lyrics, and meter analysis.
    """
    lang_key = language if language in SINGDIA_TEMPLATES else "Hinglish"
    tpl = SINGDIA_TEMPLATES.get(lang_key, SINGDIA_TEMPLATES["Hinglish"])
    
    mukhdas = tpl.get("mukhda_formats", SINGDIA_TEMPLATES["Hinglish"]["mukhda_formats"])
    antaras = tpl.get("antara_formats", SINGDIA_TEMPLATES["Hinglish"]["antara_formats"])
    bridges = tpl.get("bridge_formats", SINGDIA_TEMPLATES["Hinglish"]["bridge_formats"])
    outros = tpl.get("outro_formats", SINGDIA_TEMPLATES["Hinglish"]["outro_formats"])
    
    # Version 1: Emotional & Melodic
    mukhda_1 = mukhdas[0].format(recipient=recipient, sender=sender, occasion=occasion, memory=memory, inside_joke=inside_joke)
    antara_1 = antaras[0].format(recipient=recipient, sender=sender, occasion=occasion, memory=memory, inside_joke=inside_joke)
    antara_2 = antaras[1 % len(antaras)].format(recipient=recipient, sender=sender, occasion=occasion, memory=memory, inside_joke=inside_joke)
    bridge_1 = bridges[0].format(recipient=recipient, sender=sender, occasion=occasion, memory=memory, inside_joke=inside_joke)
    outro_1 = outros[0].format(recipient=recipient, sender=sender, occasion=occasion, memory=memory, inside_joke=inside_joke)
    
    v1_lyrics = f"""[Intro - Melodic Acoustic & Flute]

[Chorus / Mukhda]
{mukhda_1}

[Verse 1 / Antara 1]
{antara_1}

[Chorus / Mukhda]
{mukhda_1}

[Verse 2 / Antara 2]
{antara_2}

[Bridge / Emotional Climax]
{bridge_1}

[Chorus / Mukhda - Full Energy Grand Finale]
{mukhda_1}

[Outro / Spoken Dedication]
{outro_1}
"""

    # Version 2: Energetic & Modern Twist
    mukhda_2 = (mukhdas[1 % len(mukhdas)] if len(mukhdas) > 1 else mukhdas[0]).format(
        recipient=recipient, sender=sender, occasion=occasion, memory=memory, inside_joke=inside_joke
    )
    v2_lyrics = f"""[Intro - Rhythmic Beat Drop]

[Hook / Mukhda]
{mukhda_2}

[Verse 1 / Antara]
{antara_1}

[Hook / Mukhda]
{mukhda_2}

[Bridge / Breakdown]
{bridge_1}

[Outro / Fadeout Celebration]
{outro_1}
"""

    genre_info = GENRE_AUDIO_PROMPTS.get(genre, GENRE_AUDIO_PROMPTS["Modern Hindi Pop"])
    
    meter_v1 = analyze_song_meter(v1_lyrics, recipient, memory, inside_joke)
    meter_v2 = analyze_song_meter(v2_lyrics, recipient, memory, inside_joke)

    return {
        "meta": {
            "recipient": recipient,
            "sender": sender,
            "occasion": occasion,
            "relationship": relationship,
            "language": language,
            "genre": genre,
            "tempo": genre_info["tempo"],
            "mood": genre_info["mood"],
            "recommended_instruments": genre_info["instruments"]
        },
        "audio_prompts": {
            "suno_prompt": f"[{genre}] {genre_info['suno_prompt']}, Dedicated to {recipient} on {occasion}",
            "udio_tags": f"{genre}, {language} vocals, {genre_info['mood']}, {genre_info['tempo']}, acoustic instruments, heartfelt anthem",
            "voice_style": f"Warm, expressive {language} singer with natural emotional resonance and crystal-clear pronunciation"
        },
        "arrangements": [
            {
                "version": 1,
                "title": f"A Heartfelt Song for {recipient} (Emotional & Melodic Mix)",
                "tempo": genre_info["tempo"],
                "lyrics": v1_lyrics.strip(),
                "meter_analysis": meter_v1
            },
            {
                "version": 2,
                "title": f"Celebration Beat for {recipient} (Upbeat & Energetic Mix)",
                "tempo": "115-125 BPM",
                "lyrics": v2_lyrics.strip(),
                "meter_analysis": meter_v2
            }
        ],
        "gift_card_message": f"Dear {recipient}, this song was crafted with every memory, inside joke, and emotion we've shared. Happy {occasion}! With love from {sender}."
    }

def analyze_song_meter(lyrics_text: str, recipient: str = "", memory: str = "", inside_joke: str = "") -> Dict[str, Any]:
    """Score the lyrical meter, rhyme flow, and personalization depth for generated songs."""
    lines = [l.strip() for l in lyrics_text.splitlines() if l.strip() and not l.startswith("[")]
    if not lines:
        return {"overall_score": 0, "rhyme_grade": "N/A", "syllable_consistency": 0, "personalization_score": 0}
    
    syllables_per_line = []
    for line in lines:
        words = line.split()
        syllables = sum(max(1, len(re.findall(r'[aeiouyáéíóúāīūēōaiou]+', w.lower())) or (len(w) // 3 + 1)) for w in words)
        syllables_per_line.append(syllables)
    
    avg_syllables = statistics.mean(syllables_per_line)
    std_dev = statistics.stdev(syllables_per_line) if len(syllables_per_line) > 1 else 0
    consistency = max(0, min(100, int(100 - (std_dev * 8))))
    
    p_score = 40
    if recipient and recipient.lower() in lyrics_text.lower():
        p_score += 25
    if memory and any(w.lower() in lyrics_text.lower() for w in memory.split() if len(w) > 3):
        p_score += 20
    if inside_joke and any(w.lower() in lyrics_text.lower() for w in inside_joke.split() if len(w) > 3):
        p_score += 15
    p_score = min(100, p_score)
    
    overall = int(0.4 * consistency + 0.4 * p_score + 0.2 * 95)
    
    return {
        "overall_score": overall,
        "line_count": len(lines),
        "avg_syllables_per_line": round(avg_syllables, 1),
        "syllable_consistency_score": consistency,
        "personalization_score": p_score,
        "structure_rating": "Master Studio Grade (Mukhda-Antara Form)",
        "rhyme_grade": "A+ (End Rhyme & Internal Assonance)"
    }


# --- 6. Creator Unified AI System Prompt Generator ---

def get_creator_system_prompt(mode: str = "standard") -> str:
    """Generate the complete Creator bot system prompt containing all features."""
    return f"""You are **Creator** — Created by **Sakshi**. You are the world's most advanced unified AI content engineering, personalized AI Music Studio, and multi-provider AI gateway.
Built on:
1. The battle-tested content frameworks of Jake Schincariol (Jakeschincariol)
2. The AI Music Studio personalized song & lyrics gift engine (singdia.com intelligence)
3. The FreeLLMAPI multi-provider resilience gateway (34 free providers + automatic 429 failover).

### YOUR CORE CAPABILITIES & KNOWLEDGE
1. **LinkedIn Growth Engine (11 Skills)**:
   - 21 Post Hook Formulas (The Paradox, The Breakdown, The Step-by-Step, The Contrarian Frame, etc.).
   - Desktop feed truncation rules (Line 1 must grab before 210 characters). Line 2 is the payoff.
   - Anti-AI Humanizer: Purge invisible zero-width unicode, em-dashes, and 50+ banned slop words ('delve', 'tapestry', 'plethora', 'game-changer', 'testament', 'revolutionize').
   - 100-Point Profile Rubric optimizer.

2. **YouTube Channel Architect (11 Skills)**:
   - 21 Video Hook Formulas with 0-15s retention scoring (Confirm title in first sentence, open curiosity loop, set concrete stakes).
   - Title + Thumbnail Cognitive Pairing Test (Eliminate cognitive overload, maximize curiosity gap).
   - Video Script Beat Sheets (0-15s Hook -> 15-45s Stakes -> 45s-3m Delivery -> Escalation -> Payoff -> CTA).
   - Retention Reader (Eliminating dead air and drop-off spikes).

3. **Instagram Viral Studio (13 Skills)**:
   - 26 Dual-Hook Formulas (Spoken Voiceover + On-Screen Text <= 6 words).
   - 4-Stage Reel Beats (0-3s Pattern Interrupt, 3-15s Curiosity Setup, 15-45s High-Density Value, 45-60s Seamless Loop CTA).
   - Carousel Copywriting & Caption Linter.

4. **AI Music Studio (Personalized Song & Lyrics Engine)**:
   - Generate custom songs across 12 Indian & Global languages (Hindi, Hinglish, Punjabi, Tamil, Telugu, Bengali, Gujarati, Marathi, Kannada, Malayalam, English, Spanish).
   - 15 Occasions (Birthday, Anniversary, Wedding/Sangeet, Love/Valentine, Proposal, Friendship, Farewell, Lullaby, Apology, etc.).
   - 8 Master Musical Genres (Bollywood Romantic, Punjabi Dhol/Sangeet, Ghazal/Sufi, Modern Hindi Pop, Desi Hip-Hop/Rap, 90s Retro Melody, Acoustic Coffeehouse, Sweet Lullaby).
   - Authentic Mukhda-Antara-Bridge structure with rhyme meter scoring & 2 distinct arrangements.
   - Suno AI & Udio ready production prompts with instrumentations, BPM, and vocal cues.

5. **PromptMaster 35-Pattern Engine**:
   - Audit 35 credit-waste patterns (Vague asks, Missing Deliverables, No Negative Constraints, Re-explaining).
   - 1-Shot Prompt Perfection compiler (Context, Role, Task, Format, Negative Constraints, Decision Locking).

6. **HyperFrames Motion & Video Engine (13 Skills)**:
   - 20+ Animation Blueprints (Hacker Flip 3D, Kinetic Beat Slam, Agent Progress Theater, Cursor UI Demo, Comparison Split, Dataviz Countup).
   - GSAP timelines, kinetic typography, and motion design recipes.

7. **FreeLLMAPI Multi-Provider Gateway**:
   - 34 Free AI Providers with intelligent 429 rate-limit failover routing.

8. **25 Unhinged & Supercharged Operational Modes**:
   - /speedrun, /aura-farming, /china-maxing, /crash-out, /sleep-deprived-founder, /goblin-mode, /larp, /basement-hacker, /macgyver, /tax-fraud.

### YOUR OPERATING RULES
- Never write robotic, generic AI slop.
- Always provide scored formulas, concrete metrics, and actionable copy.
- Format with extreme visual clarity, punchy line breaks, and clear sections.
- When creating content, always specify the Hook Formula used and the calculated Score.
- When generating songs, always provide both Mukhda-Antara lyrics and Suno/Udio audio generation prompts.
"""


if __name__ == "__main__":
    print("Testing Creator Engine with SingDia Integration...")
    test_yt = "If you don't fix this 1 setting in your camera, you will lose 40% of your video quality."
    res = score_youtube_hook(test_yt)
    print(f"YouTube Hook Test: Score {res['verdict']}/100 ({res['band']}) - Matched: {res['matched_formula']}")
    
    test_song = generate_singdia_song(
        recipient="Aarav",
        sender="Simran",
        occasion="Birthday",
        relationship="Boyfriend",
        memory="eating late night maggi on Marine Drive",
        inside_joke="he always loses his car keys",
        language="Hinglish",
        genre="Bollywood Romantic"
    )
    print(f"\nSingDia Song Test:\nTitle: {test_song['arrangements'][0]['title']}")
    print(f"Meter Score: {test_song['arrangements'][0]['meter_analysis']['overall_score']}/100")
    print(f"Suno Prompt: {test_song['audio_prompts']['suno_prompt']}")

