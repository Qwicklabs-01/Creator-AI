#!/usr/bin/env python3
"""
freellm_gateway.py - Multi-Provider Free AI Gateway & Failover Router for 'Creator'
Synthesizes the architecture of FreeLLMAPI (tashfeenahmed/freellmapi):
- Aggregates free-tier endpoints across 34+ providers (Groq, Gemini, Cerebras, Mistral, Sambanova, OpenRouter, Cloudflare, GitHub Models, DeepSeek, etc.)
- Smart Automatic Failover: If an API key hits rate limits (HTTP 429 / Quota), it fails over to the next active provider in milliseconds.
- Unified OpenAI-compatible chat completion caller with Jake Schincariol's Creator system prompt.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Tuple

sys.stdout.reconfigure(encoding='utf-8')

# Provider Configurations & Free Tier Endpoints
FREE_PROVIDERS = {
    "groq": {
        "name": "Groq Cloud (Ultra-Fast LPUs)",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
        "default_model": "llama-3.3-70b-versatile",
        "env_var": "GROQ_API_KEY",
        "auth_type": "bearer",
        "rate_limit_rpm": 30
    },
    "cerebras": {
        "name": "Cerebras Inference (Wafer-Scale Engine)",
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "models": ["llama3.1-70b", "llama3.1-8b"],
        "default_model": "llama3.1-70b",
        "env_var": "CEREBRAS_API_KEY",
        "auth_type": "bearer",
        "rate_limit_rpm": 30
    },
    "gemini": {
        "name": "Google Gemini Free Tier",
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "models": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "default_model": "gemini-2.0-flash",
        "env_var": "GEMINI_API_KEY",
        "auth_type": "bearer",
        "rate_limit_rpm": 15
    },
    "openrouter": {
        "name": "OpenRouter (Free Router)",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "models": ["google/gemini-2.0-flash-exp:free", "meta-llama/llama-3.3-70b-instruct:free", "mistralai/mistral-7b-instruct:free"],
        "default_model": "meta-llama/llama-3.3-70b-instruct:free",
        "env_var": "OPENROUTER_API_KEY",
        "auth_type": "bearer",
        "rate_limit_rpm": 20
    },
    "mistral": {
        "name": "Mistral AI (La Plateforme Free)",
        "url": "https://api.mistral.ai/v1/chat/completions",
        "models": ["mistral-small-latest", "open-mistral-nemo", "codestral-latest"],
        "default_model": "mistral-small-latest",
        "env_var": "MISTRAL_API_KEY",
        "auth_type": "bearer",
        "rate_limit_rpm": 20
    },
    "sambanova": {
        "name": "SambaNova Systems (Fast SN40L)",
        "url": "https://api.sambanova.ai/v1/chat/completions",
        "models": ["Meta-Llama-3.1-70B-Instruct", "Qwen2.5-72B-Instruct", "Meta-Llama-3.1-8B-Instruct"],
        "default_model": "Meta-Llama-3.1-70B-Instruct",
        "env_var": "SAMBANOVA_API_KEY",
        "auth_type": "bearer",
        "rate_limit_rpm": 20
    },
    "deepseek": {
        "name": "DeepSeek API",
        "url": "https://api.deepseek.com/v1/chat/completions",
        "models": ["deepseek-chat", "deepseek-reasoner"],
        "default_model": "deepseek-chat",
        "env_var": "DEEPSEEK_API_KEY",
        "auth_type": "bearer",
        "rate_limit_rpm": 30
    },
    "github": {
        "name": "GitHub Models (Free Azure AI)",
        "url": "https://models.inference.ai.azure.com/chat/completions",
        "models": ["gpt-4o-mini", "Meta-Llama-3.1-70B-Instruct", "Mistral-large-2407"],
        "default_model": "gpt-4o-mini",
        "env_var": "GITHUB_TOKEN",
        "auth_type": "bearer",
        "rate_limit_rpm": 15
    }
}

KEY_STORAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "freellm_keys.json")

class FreeLLMGateway:
    """Smart router with automatic failover across free LLM providers."""

    def __init__(self):
        self.keys = self._load_keys()
        self.rate_limited_until: Dict[str, float] = {}

    def _load_keys(self) -> Dict[str, str]:
        keys = {}
        # 1. Load from environment
        for p_id, p_info in FREE_PROVIDERS.items():
            env_val = os.environ.get(p_info["env_var"])
            if env_val:
                keys[p_id] = env_val
        # 2. Load from local encrypted/stored config if exists
        if os.path.exists(KEY_STORAGE_FILE):
            try:
                with open(KEY_STORAGE_FILE, "r", encoding="utf-8") as f:
                    stored = json.load(f)
                    keys.update(stored)
            except Exception:
                pass
        return keys

    def set_key(self, provider_id: str, api_key: str):
        """Save an API key for a provider."""
        if provider_id in FREE_PROVIDERS:
            self.keys[provider_id] = api_key.strip()
            with open(KEY_STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.keys, f, indent=2)
            print(f"[FreeLLMGateway] Saved key for provider: {provider_id}")

    def get_active_providers(self) -> List[Dict[str, Any]]:
        """Return list of configured providers and their status."""
        now = time.time()
        result = []
        for p_id, p_info in FREE_PROVIDERS.items():
            has_key = bool(self.keys.get(p_id))
            is_limited = self.rate_limited_until.get(p_id, 0) > now
            result.append({
                "id": p_id,
                "name": p_info["name"],
                "configured": has_key,
                "status": "Rate Limited (Cooldown)" if is_limited else ("Active & Ready" if has_key else "Key Missing"),
                "models": p_info["models"],
                "default_model": p_info["default_model"]
            })
        return result

    def chat_complete(self, prompt: str, system_prompt: str, preferred_provider: Optional[str] = None) -> Dict[str, Any]:
        """Execute chat completion with automatic 429 failover."""
        now = time.time()
        
        # Determine provider priority order
        provider_order = []
        if preferred_provider and preferred_provider in FREE_PROVIDERS and self.keys.get(preferred_provider):
            provider_order.append(preferred_provider)
        
        for p_id in FREE_PROVIDERS.keys():
            if p_id not in provider_order and self.keys.get(p_id):
                provider_order.append(p_id)

        if not provider_order:
            return {
                "success": False,
                "error": "No FreeLLMAPI keys configured. Add free keys for Groq, Gemini, Cerebras, Mistral, or SambaNova.",
                "response": None,
                "provider": None
            }

        # Attempt call with failover
        attempts = []
        for p_id in provider_order:
            if self.rate_limited_until.get(p_id, 0) > now:
                attempts.append(f"{p_id}: skipped (cooldown active)")
                continue

            p_config = FREE_PROVIDERS[p_id]
            api_key = self.keys[p_id]
            model_name = p_config["default_model"]

            try:
                start_t = time.time()
                resp_text = self._call_provider(p_config["url"], api_key, model_name, prompt, system_prompt)
                latency_ms = round((time.time() - start_t) * 1000)

                return {
                    "success": True,
                    "response": resp_text,
                    "provider": p_id,
                    "provider_name": p_config["name"],
                    "model": model_name,
                    "latency_ms": latency_ms,
                    "failover_attempts": attempts
                }
            except urllib.error.HTTPError as e:
                if e.code in [429, 503, 504]:
                    # Rate limit or overload -> trigger 60s cooldown and failover
                    self.rate_limited_until[p_id] = now + 60
                    attempts.append(f"{p_id}: HTTP {e.code} (Rate Limit) -> Failing over")
                else:
                    attempts.append(f"{p_id}: HTTP {e.code} ({e.reason})")
            except Exception as e:
                attempts.append(f"{p_id}: {str(e)}")

        return {
            "success": False,
            "error": f"All configured FreeLLMAPI providers failed or are rate limited: {'; '.join(attempts)}",
            "failover_attempts": attempts
        }

    def _call_provider(self, url: str, api_key: str, model: str, prompt: str, system_prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.65,
            "max_tokens": 2048
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"]


# Global Instance
gateway = FreeLLMGateway()

if __name__ == "__main__":
    print("==================================================")
    print("  ⚡ FreeLLMAPI Multi-Provider Gateway for Creator")
    print("==================================================")
    providers = gateway.get_active_providers()
    for p in providers:
        status_icon = "🟢" if "Active" in p["status"] else ("🟡" if "Cooldown" in p["status"] else "⚪")
        print(f"{status_icon} {p['name']} [{p['id']}]: {p['status']}")
