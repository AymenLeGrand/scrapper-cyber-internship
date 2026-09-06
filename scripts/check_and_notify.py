"""
Autonomous 12-Hour Pipeline Runner for France Cyber & Crypto M2 Tracker.
Runs:
1. build_verified_database.py (ATS scrape + Quarkslab blog monitor)
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

from scraper.notifier import send_all_notifications, load_seen_job_ids, save_seen_job_ids

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting 12-hour automated verification pipeline...")
    
    # 1. Run database builder
    builder_script = os.path.join(BASE_DIR, 'scraper', 'build_verified_database.py')
    subprocess.run([sys.executable, builder_script], check=True, cwd=BASE_DIR)
    
    # 2. Run liveness verification
    validator_script = os.path.join(BASE_DIR, 'scraper', 'verify_all_links.py')
    subprocess.run([sys.executable, validator_script], check=True, cwd=BASE_DIR)
    
    # 3. Detect brand new postings
    jobs_file = os.path.join(BASE_DIR, 'data', 'jobs.json')
    seen_file = os.path.join(BASE_DIR, 'data', 'seen_jobs.json')
    
    with open(jobs_file, 'r', encoding='utf-8') as f:
        current_jobs = json.load(f)
        
    seen_ids = load_seen_job_ids(seen_file)
    new_unseen_jobs = [j for j in current_jobs if j['id'] not in seen_ids]
    
    if new_unseen_jobs:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected {len(new_unseen_jobs)} brand new M2 internship(s)!")
        send_all_notifications(new_unseen_jobs, seen_file_path=seen_file)
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] No new unnotified internships. All {len(current_jobs)} active positions are up to date.")

if __name__ == '__main__':
    main()
