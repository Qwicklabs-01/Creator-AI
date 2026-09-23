#!/usr/bin/env python3
"""
model_server.py - OpenAI-Compatible Local REST Model Server for 'Creator' with FreeLLMAPI Gateway
Exposes:
- POST /v1/chat/completions (OpenAI Chat API format + FreeLLM multi-provider failover)
- GET  /v1/models (Lists 'creator', 'creator-unhinged', 'creator-humanizer')
- GET  /v1/freellm/providers (Lists all 34 supported free providers & status)
- POST /v1/freellm/keys (Save/update Free API keys)
- POST /v1/creator/score_hook
- POST /v1/creator/humanize
- POST /v1/creator/audit_prompt
"""

import http.server
import socketserver
import json
import time
import os
import sys
from urllib.parse import urlparse

sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import creator_engine
from creator_model.creator_model import CreatorModel
from creator_model.freellm_gateway import FreeLLMGateway, FREE_PROVIDERS

PORT = 8001
model_instance = CreatorModel()

class CreatorServerHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/v1/models":
            self._send_json(200, {
                "object": "list",
                "data": [
                    {
                        "id": "creator",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "creator-ecosystem",
                        "description": "Master Creator Content Engineering & Viral Model"
                    },
                    {
                        "id": "creator-unhinged",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "creator-ecosystem",
                        "description": "Creator /speedrun & High-Velocity Mode"
                    },
                    {
                        "id": "creator-humanizer",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "creator-ecosystem",
                        "description": "Anti-AI Slop & Cadence Normalizer"
                    }
                ]
            })
        elif parsed.path == "/v1/freellm/providers":
            self._send_json(200, {
                "providers": model_instance.gateway.get_active_providers(),
                "total_supported": len(FREE_PROVIDERS)
            })
        elif parsed.path == "/health" or parsed.path == "/":
            self._send_json(200, {"status": "healthy", "model": "Creator v2.0.0", "engine": "active", "freellm_active_keys": len(model_instance.gateway.keys)})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            req_data = json.loads(body) if body else {}
        except Exception:
            self._send_json(400, {"error": "Invalid JSON payload"})
            return

        # 1. OpenAI Chat Completions Endpoint (/v1/chat/completions)
        if parsed.path == "/v1/chat/completions":
            messages = req_data.get("messages", [])
            model_req = req_data.get("model", "creator")
            preferred_provider = req_data.get("provider", None)
            
            # Extract last user message
            user_msg = ""
            for m in reversed(messages):
                if m.get("role") == "user":
                    user_msg = m.get("content", "")
                    break
            if not user_msg:
                user_msg = "Explain the 0-15s YouTube retention window."

            persona = "unhinged" if "unhinged" in model_req else ("slop-hunter" if "humanizer" in model_req else "standard")
            gen_res = model_instance.generate(user_msg, persona=persona, preferred_provider=preferred_provider)
            
            openai_response = {
                "id": f"chatcmpl-creator-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model_req,
                "provider": gen_res.get("provider", gen_res.get("backend")),
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": gen_res.get("response", "")
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": len(user_msg.split()),
                    "completion_tokens": len(gen_res.get("response", "").split()),
                    "total_tokens": len(user_msg.split()) + len(gen_res.get("response", "").split())
                }
            }
            self._send_json(200, openai_response)

        # 2. Save FreeLLM Keys (/v1/freellm/keys)
        elif parsed.path == "/v1/freellm/keys":
            provider_id = req_data.get("provider")
            api_key = req_data.get("api_key")
            if provider_id and api_key:
                model_instance.gateway.set_key(provider_id, api_key)
                self._send_json(200, {"success": True, "message": f"Saved key for {provider_id}"})
            else:
                self._send_json(400, {"error": "Missing provider or api_key"})

        # 3. Hook Scoring Endpoint (/v1/creator/score_hook)
        elif parsed.path == "/v1/creator/score_hook":
            platform = req_data.get("platform", "yt")
            text = req_data.get("text", "")
            if platform == "yt":
                res = creator_engine.score_youtube_hook(text)
            elif platform == "li":
                res = creator_engine.score_linkedin_hook(text)
            else:
                visual = req_data.get("visual", "")
                res = creator_engine.score_instagram_reel(text, visual)
            self._send_json(200, res)

        # 4. Anti-AI Humanizer Endpoint (/v1/creator/humanize)
        elif parsed.path == "/v1/creator/humanize":
            text = req_data.get("text", "")
            res = creator_engine.humanize_text(text)
            self._send_json(200, res)

        # 5. PromptMaster Audit Endpoint (/v1/creator/audit_prompt)
        elif parsed.path == "/v1/creator/audit_prompt":
            prompt = req_data.get("prompt", "")
            res = creator_engine.audit_promptmaster(prompt)
            self._send_json(200, res)

        else:
            self._send_json(404, {"error": "Endpoint not recognized"})

def run_server(port=PORT):
    print(f"\n=======================================================")
    print(f"  ⚡ CREATOR MODEL + FreeLLMAPI REST SERVER (PORT {port})")
    print(f"  OpenAI API Endpoint: http://localhost:{port}/v1/chat/completions")
    print(f"  Models Endpoint:     http://localhost:{port}/v1/models")
    print(f"  Free Providers API:  http://localhost:{port}/v1/freellm/providers")
    print(f"=======================================================\n")
    with socketserver.TCPServer(("", port), CreatorServerHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
