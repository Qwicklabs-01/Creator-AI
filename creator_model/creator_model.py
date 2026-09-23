#!/usr/bin/env python3
"""
creator_model.py - The 'Creator' Model Wrapper & Inference Engine
Unifies:
1. FreeLLMAPI multi-provider gateway (Groq, Gemini, Cerebras, Mistral, SambaNova, OpenRouter, DeepSeek)
2. Local Ollama LLM integration (Model: creator / llama3.2 / mistral / qwen2.5)
3. Local deterministic heuristic generation & scoring
4. OpenAI-compatible API bridge
"""

import json
import os
import sys
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import creator_engine
from creator_model.freellm_gateway import FreeLLMGateway, gateway

HERE = os.path.dirname(os.path.abspath(__file__))
SYSTEM_PROMPT_FILE = os.path.join(HERE, "system_instructions.md")

class CreatorModel:
    """The unified Creator Model interface."""
    
    def __init__(self, ollama_host: str = "http://localhost:11434", model_name: str = "creator"):
        self.ollama_host = ollama_host
        self.model_name = model_name
        self.system_prompt = self._load_system_prompt()
        self.knowledge = creator_engine.load_knowledge()
        self.gateway = gateway

    def _load_system_prompt(self) -> str:
        if os.path.exists(SYSTEM_PROMPT_FILE):
            with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
                return f.read()
        return creator_engine.get_creator_system_prompt()

    def generate(self, user_prompt: str, persona: str = "standard", preferred_provider: Optional[str] = None, use_ollama: bool = False) -> Dict[str, Any]:
        """Generate response from Creator model via FreeLLMAPI, Ollama, or local heuristics."""
        
        # 1. Check if any FreeLLMAPI keys are configured
        if self.gateway.keys:
            free_res = self.gateway.chat_complete(user_prompt, self.system_prompt, preferred_provider=preferred_provider)
            if free_res.get("success"):
                return {
                    "response": free_res["response"],
                    "backend": "freellmapi",
                    "provider": free_res.get("provider_name"),
                    "model": free_res.get("model"),
                    "latency_ms": free_res.get("latency_ms"),
                    "persona": persona
                }

        # 2. Check Ollama LLM
        if use_ollama:
            try:
                return self._generate_ollama(user_prompt)
            except Exception:
                pass

        # 3. Fallback to Local Engine
        return self._generate_local(user_prompt, persona)

    def _generate_ollama(self, prompt: str) -> Dict[str, Any]:
        url = f"{self.ollama_host}/api/generate"
        payload = {
            "model": self.model_name,
            "system": self.system_prompt,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.65,
                "top_p": 0.9
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "response": data.get("response", ""),
                "model": self.model_name,
                "backend": "ollama",
                "done": True
            }

    def _generate_local(self, prompt: str, persona: str) -> Dict[str, Any]:
        """Execute Creator's local rule-based AI engine."""
        q = prompt.lower()
        
        # YouTube Hook Request
        if "youtube" in q and ("hook" in q or "score" in q or "script" in q):
            clean_text = re.sub(r"^(generate|score|audit|write)\s*(a\s*)?(youtube\s*)?(hook\s*)?:?\s*", "", prompt, flags=re.I).strip()
            if not clean_text or len(clean_text) < 5:
                clean_text = "If you don't fix this 1 audio setting today, 40% of your viewers will click away in 10 seconds."
            score = creator_engine.score_youtube_hook(clean_text)
            
            resp = f"""### 🎥 YouTube Hook Audit & Diagnostic: {score['verdict']}/100 [{score['band']}]

**Hook Analyzed**:
> "{clean_text}"

- **Formula Matched**: {score['matched_formula']}
- **Word Count**: {score['word_count']} words (Target: 9-24 spoken words)
- **Weakest Link**: {score['weakest']} ({score['fix_recommendation']})

**Score Breakdown**:
"""
            for k, v in score['parts'].items():
                resp += f"- **{k:<12}**: {v:3d}/100\n"
                
            resp += f"""
---
### ⚡ 3 Alternative High-Retention Hooks:
1. **The Hard Metric (Score: 88/100)**: "I tested 10 AI video editors this month, and 9 of them are a complete waste of money. Here is the 1 that actually works."
2. **The Paradox (Score: 84/100)**: "Everyone tells you to buy a $1,000 camera, but top creators are quietly using this $30 lighting setup instead."
3. **The Urgent Mistake (Score: 92/100)**: "Stop rendering in 4K. It is quietly destroying your mobile playback retention, and here is why."
"""
            return {"response": resp.strip(), "backend": "creator-local-engine", "persona": persona}

        # LinkedIn Post Request
        if "linkedin" in q and ("hook" in q or "post" in q):
            resp = """### 💼 3 High-Tension LinkedIn Hooks (Desktop Truncation Safe)

**1. The Paradox (Score: 88/100 - Viral Ready)**
> "Most founders think marketing is about daily posting.
> 
> Here is how we generated $160,000 in pipeline with only 2 posts a week:"
*(Line 1: 52 characters — completely safe under the 210-character desktop cutoff)*

**2. The Contrarian Frame (Score: 84/100)**
> "Stop hiring junior copywriters for AI workflows.
> 
> You don't have a writing problem. You have a prompt engineering problem. Exactly what to change:"

**3. The Breakdown (Score: 91/100)**
> "I audited 50 B2B landing pages this month.
> 
> 43 of them made the exact same mistake that cuts mobile signups in half:"
"""
            return {"response": resp.strip(), "backend": "creator-local-engine", "persona": persona}

        # Slop & Humanize Request
        if "humanize" in q or "slop" in q or "delve" in q:
            hum = creator_engine.humanize_text(prompt)
            resp = f"""### 🛡️ Anti-AI Slop Humanizer Report

- **New Human Score**: {hum['new_human_score']}/100 ({hum['new_verdict']})
- **Transformations Applied**: {len(hum['replacements'])}

**Cleaned Human Draft**:
> {hum['cleaned_text']}

**Replaced Buzzwords**:
"""
            for r in hum['replacements']:
                resp += f"- *\"{r['from']}\"* → **\"{r['to']}\"**\n"
            return {"response": resp.strip(), "backend": "creator-local-engine", "persona": persona}

        # PromptMaster Audit
        if "audit" in q or "prompt" in q or "waste" in q:
            audit = creator_engine.audit_promptmaster(prompt)
            resp = f"""### 🧠 PromptMaster 35-Pattern Audit Report

- **Prompt Health Score**: {audit['health_score']}/100
- **Credit-Waste Traps Detected**: {audit['patterns_count']}
- **Estimated Wasted Tokens**: ~{audit['estimated_wasted_tokens_per_run']} tokens per retry

**Flaws Detected**:
"""
            for d in audit['waste_patterns_detected']:
                resp += f"- **[#{d['id']} {d['name']}]** ({d['family']})\n  *Fix*: {d['fix']}\n"
                
            resp += f"""
---
### ⚡ 1-Shot Production-Ready Compiled Prompt:
```markdown
{audit['optimized_prompt']}
```"""
            return {"response": resp.strip(), "backend": "creator-local-engine", "persona": persona}

        # Default Creator Response
        resp = f"""### ⚡ CREATOR MODEL [{persona.upper()} MODE]

I am the **Creator Model**, running Jake Schincariol's unified content engineering systems powered by FreeLLMAPI Gateway.

**Active Capabilities**:
1. **68+ Hook Formulas** across LinkedIn, YouTube, and Instagram Reels.
2. **5-Check Anti-AI Slop Humanizer** (Zero-width purging + 50+ banned buzzwords).
3. **PromptMaster 35 Credit-Waste Pattern Auditor**.
4. **22 HyperFrames Motion Graphics Blueprints** (GSAP / Canvas).
5. **25 Unhinged High-Leverage Operational Modes**.
6. **FreeLLMAPI Gateway Integration** (Groq, Gemini, Cerebras, Mistral, SambaNova with auto-failover)."""
        return {"response": resp.strip(), "backend": "creator-local-engine", "persona": persona}


if __name__ == "__main__":
    print("Testing CreatorModel interface with FreeLLMAPI gateway...")
    model = CreatorModel()
    res = model.generate("Write 3 viral LinkedIn hooks about AI automation.")
    print("\nModel Output (" + res.get("backend", "local") + "):\n" + res["response"])
