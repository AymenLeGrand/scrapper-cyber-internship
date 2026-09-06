import urllib3
urllib3.disable_warnings()
import json
import requests
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

with open("data/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

print(f"Testing liveness for all {len(jobs)} jobs in data/jobs.json...\n")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

failures = 0
for i, j in enumerate(jobs, 1):
    url = j["direct_url"]
    try:
        r = requests.get(url, headers=headers, timeout=8, allow_redirects=True, verify=False)
        status = r.status_code
        body_lower = r.text.lower()
        is_404 = (
            "<title>404" in body_lower or 
            "<title>page introuvable" in body_lower or 
            "cette offre n'est plus active" in body_lower or
            "cette offre est actuellement pourvue" in body_lower or
            "ce poste a été pourvu" in body_lower or
            "this job is no longer available" in body_lower or
            "position has been filled" in body_lower
        )
        is_ok = (status == 200) and not is_404
        symbol = "✓" if is_ok else "✗"
        comp = j.get("company_name", "")
        title = j.get("title", "")[:45]
        print(f"[{i:02d}/{len(jobs)}] {symbol} HTTP {status} | {comp} | {title}...")
        print(f"       -> {url}")
        if not is_ok:
            failures += 1
    except Exception as e:
        print(f"[{i:02d}/{len(jobs)}] ✗ ERROR: {url} -> {e}")
        failures += 1

print(f"\n==================================================")
print(f"AUDIT COMPLETE: {len(jobs) - failures}/{len(jobs)} URLs are 100% HTTP 200 OK.")
if failures > 0:
    print(f"WARNING: {failures} URLs failed.")
    sys.exit(1)
else:
    print("ALL LINKS ARE VERIFIED LIVE AND ACTIVE!")
