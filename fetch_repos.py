import urllib.request
import json
import os
import sys

# Ensure UTF-8 output encoding
sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request(
    'https://api.github.com/users/Jakeschincariol/repos?per_page=100',
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as response:
        repos = json.loads(response.read().decode('utf-8'))
        print(f"Total repos found: {len(repos)}\n")
        for r in repos:
            print(f"=== {r['name']} ({r['stargazers_count']} stars, {r['forks_count']} forks) ===")
            print(f"URL: {r['html_url']}")
            print(f"Description: {r['description']}")
            print(f"Language: {r['language']}")
            print(f"Topics: {r['topics']}")
            print("-" * 50)
except Exception as e:
    print(f"Error: {e}")
