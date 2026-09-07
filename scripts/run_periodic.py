import time
import subprocess
import sys
import os
import argparse
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\MSI\.gemini\antigravity\scratch\france-cyber-crypto-internships"
PYTHON_EXE = sys.executable

INTERVAL_HOURS = 3
INTERVAL_SECONDS = INTERVAL_HOURS * 3600  # 10800 seconds

def run_scrape():
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now_str}] === Starting periodic scraping & verification run ===", flush=True)
    
    # 1. Rebuild & update verified stages
    subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "scraper", "build_verified_database.py")], cwd=BASE_DIR)
    
    # 2. Verify all links
    subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "scraper", "verify_all_links.py")], cwd=BASE_DIR)
    
    next_run = datetime.now() + timedelta(seconds=INTERVAL_SECONDS)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Run completed. Next run scheduled in {INTERVAL_HOURS:g} hours ({INTERVAL_SECONDS}s) at {next_run.strftime('%Y-%m-%d %H:%M:%S')}.\n", flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Continuous re-scrap scheduler")
    parser.add_argument("--hours", type=float, default=3.0, help="Interval in hours (default: 3.0)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    INTERVAL_HOURS = args.hours
    INTERVAL_SECONDS = int(INTERVAL_HOURS * 3600)

    print("=====================================================", flush=True)
    print("France Cyber & Crypto Tracker: Periodic Re-Scraper", flush=True)
    print(f"Scraping interval: Every {INTERVAL_HOURS:g} hours ({INTERVAL_SECONDS} seconds)", flush=True)
    print("Press Ctrl+C to stop the scheduler anytime.", flush=True)
    print("=====================================================\n", flush=True)
    
    if args.once:
        run_scrape()
        sys.exit(0)

    while True:
        try:
            run_scrape()
            time.sleep(INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n[INFO] Periodic scheduler stopped by user.", flush=True)
            break
        except Exception as e:
            print(f"[ERROR] Scheduler exception: {e}", flush=True)
            time.sleep(60)
