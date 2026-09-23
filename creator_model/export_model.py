#!/usr/bin/env python3
"""
export_model.py - Export & Packaging CLI for 'Creator' Model
Packages the model for:
1. Ollama (ollama create creator -f Modelfile)
2. OpenAI Custom GPT / Assistant
3. Local OpenAI-Compatible REST Server
4. HuggingFace / LoRA Fine-Tuning dataset
"""

import os
import sys
import subprocess
import shutil

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def print_banner():
    print("""
======================================================
  ⚡ CREATOR MODEL PACKAGER & EXPORT SUITE ⚡
======================================================
""")

def export_ollama():
    print("\n[1/4] Checking Ollama installation...")
    ollama_path = shutil.which("ollama")
    if ollama_path:
        print("Found Ollama executable. Building 'creator' model...")
        modelfile_path = os.path.join(ROOT, "Modelfile")
        cmd = ["ollama", "create", "creator", "-f", modelfile_path]
        try:
            subprocess.run(cmd, check=True)
            print("\n[OK] 'creator' model successfully created in Ollama!")
            print("Run it with: ollama run creator")
        except Exception as e:
            print(f"Error running ollama create: {e}")
    else:
        print("Ollama is not installed or not in PATH.")
        print("To build with Ollama, install from https://ollama.ai and run:")
        print("  ollama create creator -f Modelfile")

def test_local_model():
    print("\n[2/4] Testing CreatorModel Python interface...")
    from creator_model import CreatorModel
    model = CreatorModel()
    res = model.generate("Write 3 viral LinkedIn hooks about AI automation.")
    print("[OK] Model output generated successfully:")
    print(res["response"][:300] + "...\n")

def show_options():
    print_banner()
    print("Available Deployment Options:")
    print("  1. Build & Export to Ollama (ollama create creator -f Modelfile)")
    print("  2. Start OpenAI-Compatible REST Model Server (python creator_model/model_server.py)")
    print("  3. Run Local Python Inference Test")
    print("  4. View Custom GPT & System Prompt Specification")
    print("  0. Exit")
    
    choice = input("\nEnter choice (0-4): ").strip()
    if choice == "1":
        export_ollama()
    elif choice == "2":
        print("\nStarting Model Server on http://localhost:8000 ...")
        from model_server import run_server
        run_server()
    elif choice == "3":
        test_local_model()
    elif choice == "4":
        sys_file = os.path.join(HERE, "system_instructions.md")
        with open(sys_file, "r", encoding="utf-8") as f:
            print("\n" + "="*50)
            print(f.read())
            print("="*50)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_local_model()
    else:
        show_options()
