import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

repos = [
    "linkedin-agent-skill",
    "youtube-agent-skill",
    "instagram-agent-skill",
    "promptmaster-skill",
    "unhinged-claude-skills",
    "video-production-skills",
    "claude-illegal-codes",
    "Influencer-Clone",
    "chatgpt-youtube-agent-skill"
]

os.makedirs("repo_knowledge", exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

for repo in repos:
    repo_dir = os.path.join("repo_knowledge", repo)
    os.makedirs(repo_dir, exist_ok=True)
    
    print(f"Fetching repo: {repo}...")
    # Fetch tree
    try:
        url = f"https://api.github.com/repos/Jakeschincariol/{repo}/git/trees/main?recursive=1"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            tree_data = json.loads(resp.read().decode('utf-8'))
            
            with open(os.path.join(repo_dir, "_tree.json"), "w", encoding="utf-8") as f:
                json.dump(tree_data, f, indent=2)
                
            for item in tree_data.get("tree", []):
                path = item["path"]
                if item["type"] == "blob" and (path.endswith(".md") or path.endswith(".txt") or path.endswith(".json") or path.endswith(".py") or path.endswith(".sh") or path.endswith(".yaml") or path.endswith(".yml")):
                    raw_url = f"https://raw.githubusercontent.com/Jakeschincariol/{repo}/main/{path}"
                    try:
                        file_req = urllib.request.Request(raw_url, headers=headers)
                        with urllib.request.urlopen(file_req) as f_resp:
                            content = f_resp.read().decode('utf-8', errors='ignore')
                            target_file = os.path.join(repo_dir, path.replace("/", "_"))
                            with open(target_file, "w", encoding="utf-8") as out:
                                out.write(content)
                            print(f"  Saved: {path}")
                    except Exception as e:
                        print(f"  Failed {path}: {e}")
    except Exception as e:
        print(f"Failed to fetch tree for {repo}: {e}")

print("Done fetching repos!")
