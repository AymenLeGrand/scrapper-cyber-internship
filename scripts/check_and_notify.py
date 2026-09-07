"""
Autonomous 3-Hour Pipeline Runner for France Cyber & Crypto M2 Tracker.
Runs:
1. build_verified_database.py (ATS scrape + LinkedIn scrape + Quarkslab blog monitor)
2. verify_all_links.py (Liveness verification)
3. Computes diff with data/seen_jobs.json
4. Dispatches mobile alerts via Telegram, Discord, ntfy.sh, or Email
"""

import os
import sys
import json
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from scraper.notifier import send_all_notifications, load_seen_job_ids, save_seen_job_ids, send_ntfy_health_alert

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting 3-hour automated verification pipeline...")
    
    # 1. Run database builder
    builder_script = os.path.join(BASE_DIR, 'scraper', 'build_verified_database.py')
    subprocess.run([sys.executable, builder_script], check=True, cwd=BASE_DIR)
    
    # 2. Run liveness verification
    validator_script = os.path.join(BASE_DIR, 'scraper', 'verify_all_links.py')
    subprocess.run([sys.executable, validator_script], check=True, cwd=BASE_DIR)

    # 2b. Health check: alert if any scraper crashed
    meta_file = os.path.join(BASE_DIR, 'data', 'meta.json')
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        scraper_errors = meta.get('scraper_errors', [])
        if scraper_errors:
            print(f"[HEALTH] {len(scraper_errors)} scraper error(s) detected — sending alert.")
            send_ntfy_health_alert(scraper_errors)

    # Check notification channels status
    ntfy_topic = os.getenv("NTFY_TOPIC")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    discord_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    print("[Channels Status]")
    print(f"  • NTFY: {'Configured (Topic: ' + ntfy_topic + ')' if ntfy_topic else 'Not set (Add NTFY_TOPIC in GitHub Secrets)'}")
    print(f"  • Telegram: {'Configured' if tg_token else 'Not set (Add TELEGRAM_BOT_TOKEN in GitHub Secrets)'}")
    print(f"  • Discord: {'Configured' if discord_url else 'Not set (Add DISCORD_WEBHOOK_URL in GitHub Secrets)'}")

    # 3. Detect brand new postings
    jobs_file = os.path.join(BASE_DIR, 'data', 'jobs.json')
    seen_file = os.path.join(BASE_DIR, 'data', 'seen_jobs.json')
    
    with open(jobs_file, 'r', encoding='utf-8') as f:
        current_jobs = json.load(f)
        
    seen_ids = load_seen_job_ids(seen_file)
    new_unseen_jobs = [j for j in current_jobs if j['id'] not in seen_ids]
    test_mode = os.getenv("TEST_NOTIFICATION", "").lower() in ("true", "1", "yes") or (len(sys.argv) > 1 and sys.argv[1] == "--test")
    
    if new_unseen_jobs:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected {len(new_unseen_jobs)} brand new M2 internship(s)!")
        send_all_notifications(new_unseen_jobs, seen_file_path=seen_file)
    elif test_mode:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Test notification requested! Sending alert with {min(3, len(current_jobs))} sample internships to verify your phone...")
        # Send sample jobs without overwriting seen tracking
        send_all_notifications(current_jobs[:3], seen_file_path=None)
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] No new unnotified internships. All {len(current_jobs)} active positions are up to date.")
        print("  (To test sending a notification to your phone right now, trigger workflow with test_notification=true or set TEST_NOTIFICATION=true)")

if __name__ == '__main__':
    main()
