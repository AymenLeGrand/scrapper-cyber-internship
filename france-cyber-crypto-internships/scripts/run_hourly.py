import time
import subprocess
import sys
import os
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\MSI\.gemini\antigravity\scratch\france-cyber-crypto-internships"
PYTHON_EXE = sys.executable

def run_scrape():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now_str}] === Starting hourly scraping & verification run ===", flush=True)
    
    # 1. Rebuild & update verified stages
    subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "scraper", "build_verified_database.py")], cwd=BASE_DIR)
    
    # 2. Verify all links
    subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "scraper", "verify_all_links.py")], cwd=BASE_DIR)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Run completed. Next run scheduled in 1 hour (3600s).\n", flush=True)

if __name__ == '__main__':
    print("=====================================================", flush=True)
    print("France Cyber & Crypto Tracker: Local Hourly Scheduler", flush=True)
    print("Scraping interval: Every 1 hour (3600 seconds)", flush=True)
    print("Press Ctrl+C to stop the scheduler anytime.", flush=True)
    print("=====================================================\n", flush=True)
    
    while True:
        try:
            run_scrape()
            time.sleep(3600)
        except KeyboardInterrupt:
            print("\n[INFO] Hourly scheduler stopped by user.", flush=True)
            break
        except Exception as e:
            print(f"[ERROR] Scheduler exception: {e}", flush=True)
            time.sleep(60)
