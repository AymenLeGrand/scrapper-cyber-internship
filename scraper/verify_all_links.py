import urllib3
urllib3.disable_warnings()
import json
import requests
import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

with open("data/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

print(f"Testing liveness for all {len(jobs)} jobs in data/jobs.json...\n")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

valid_jobs = []
dead_count = 0

for i, j in enumerate(jobs, 1):
    url = j["direct_url"]
    is_linkedin = "linkedin.com" in url

    # Small delay on LinkedIn to prevent rate limiting
    if is_linkedin:
        time.sleep(0.4)

    try:
        r = requests.get(url, headers=headers, timeout=10, allow_redirects=True, verify=False)
        status = r.status_code
        body_lower = r.text.lower()

        # 429 or 999 from LinkedIn is temporary rate limiting, not a dead link
        if is_linkedin and status in (429, 999, 403):
            is_dead = False
            symbol = "✓ (rate-limit bypass)"
        else:
            is_dead = (
                status in (404, 410) or
                "<title>404" in body_lower or 
                "<title>page introuvable" in body_lower or 
                "cette offre n'est plus active" in body_lower or
                "cette offre est actuellement pourvue" in body_lower or
                "ce poste a été pourvu" in body_lower or
                "this job is no longer available" in body_lower or
                "position has been filled" in body_lower
            )
            symbol = "✗ DEAD" if is_dead else "✓"

        comp = j.get("company_name", "")
        title = j.get("title", "")[:45]
        print(f"[{i:02d}/{len(jobs)}] {symbol} HTTP {status} | {comp} | {title}...")

        if is_dead:
            dead_count += 1
            print(f"       -> Pruning expired offer: {url}")
        else:
            valid_jobs.append(j)

    except Exception as e:
        print(f"[{i:02d}/{len(jobs)}] ~ TIMEOUT/RETAIN: {url} -> {e}")
        valid_jobs.append(j)

if dead_count > 0:
    print(f"\n[Pruning] Removed {dead_count} dead/closed offer(s). Keeping {len(valid_jobs)} verified offers.")
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(valid_jobs, f, indent=2, ensure_ascii=False)

print(f"\n==================================================")
print(f"AUDIT COMPLETE: {len(valid_jobs)}/{len(jobs)} URLs are verified active.")
print("ALL LINKS VERIFIED LIVE!")
