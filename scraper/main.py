"""
Main Execution Script for France Cyber & Cryptology M2 Internship Scraper.
Orchestrates:
1. Scraping official company career portals
2. Verifying URL liveness and removing expired postings
3. Updating data/jobs.json
4. Sending automated email notifications for newly discovered positions
"""

import argparse
import datetime
import json
import logging
import os
import sys
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from scraper.companies import COMPANIES
from scraper.ats_scrapers import scrape_company_jobs
from scraper.validator import validate_all_jobs
from scraper.notifier import send_all_notifications, load_seen_job_ids, build_email_content

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("scraper.main")


def load_existing_jobs(jobs_file: str) -> list:
    if os.path.exists(jobs_file):
        try:
            with open(jobs_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read existing jobs file {jobs_file}: {e}")
    return []


def save_jobs(jobs_file: str, jobs: list):
    os.makedirs(os.path.dirname(jobs_file), exist_ok=True)
    with open(jobs_file, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(jobs)} jobs to {jobs_file}")


def run_pipeline(
    verify: bool = True,
    notify: bool = True,
    dry_run: bool = False,
    test_mode: bool = False
):
    load_dotenv()

    jobs_file = os.path.join(BASE_DIR, "data", "jobs.json")
    seen_file = os.path.join(BASE_DIR, "data", "seen_jobs.json")

    logger.info("=" * 60)
    logger.info("Starting France Cyber & Cryptology M2 Internship Scraper")
    logger.info("=" * 60)

    # 1. Load existing jobs
    existing_jobs = load_existing_jobs(jobs_file)
    existing_by_id = {j["id"]: j for j in existing_jobs}
    seen_ids = load_seen_job_ids(seen_file)

    # Target company selection
    target_companies = COMPANIES
    if test_mode:
        # In test mode, pick 8 key representative companies
        test_ids = [
            "serma-safety-security",
            "ledger",
            "stormshield",
            "sekoia",
            "tehtris",
            "harfanglab",
            "gitguardian",
            "wavestone"
        ]
        target_companies = [c for c in COMPANIES if c["id"] in test_ids]
        logger.info(f"Running in TEST mode with {len(target_companies)} companies.")
    else:
        logger.info(f"Scanning {len(target_companies)} French cybersecurity & cryptology organizations.")

    # 2. Scrape jobs directly from official company portals
    discovered_jobs = []
    for comp in target_companies:
        logger.info(f"Checking {comp['name']} ({comp.get('direct_ats_type', 'custom')})...")
        try:
            jobs = scrape_company_jobs(comp)
            if jobs:
                logger.info(f"  -> Found {len(jobs)} matching M2 offer(s)")
                discovered_jobs.extend(jobs)
        except Exception as e:
            logger.error(f"  -> Error scanning {comp['name']}: {e}")

    # Merge newly discovered jobs with existing jobs
    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    newly_found_unseen = []

    for job in discovered_jobs:
        jid = job["id"]
        if jid in existing_by_id:
            # Update existing with refreshed metadata
            existing_by_id[jid]["last_seen"] = now_iso
            existing_by_id[jid]["direct_url"] = job["direct_url"]
        else:
            job["first_seen"] = now_iso
            job["last_seen"] = now_iso
            job["status"] = "active"
            existing_by_id[jid] = job

            if jid not in seen_ids:
                newly_found_unseen.append(job)

    all_jobs = list(existing_by_id.values())

    # 3. Verify URL liveness (removes/marks expired postings)
    if verify and all_jobs:
        logger.info(f"Validating liveness for {len(all_jobs)} posting(s)...")
        active_jobs, expired_jobs = validate_all_jobs(all_jobs)
        logger.info(f"Verification complete: {len(active_jobs)} active, {len(expired_jobs)} expired.")
        all_jobs = active_jobs

    # Sort: Cryptology first, then latest first
    all_jobs.sort(key=lambda x: (not x.get("is_crypto", False), x.get("posted_at", "")), reverse=True)

    # 4. Save to data/jobs.json
    save_jobs(jobs_file, all_jobs)

    # 5. Email Notifications for newly discovered postings
    if newly_found_unseen:
        logger.info(f"Detected {len(newly_found_unseen)} brand new M2 internship(s)!")
        if dry_run:
            subject, plain_text, _ = build_email_content(newly_found_unseen)
            logger.info("[DRY RUN] Would have sent email alert:")
            print(f"\nSubject: {subject}\n\n{plain_text}\n")
        elif notify:
            send_all_notifications(newly_found_unseen, seen_file_path=seen_file)
    else:
        logger.info("No new unnotified postings found in this run.")

    logger.info("Run finished successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="France Cyber & Crypto Internship Pipeline")
    parser.add_argument("--no-verify", dest="verify", action="store_false", help="Skip URL liveness verification")
    parser.add_argument("--no-notify", dest="notify", action="store_false", help="Disable sending email notifications")
    parser.add_argument("--dry-run", action="store_true", help="Print email notification without sending")
    parser.add_argument("--test", action="store_true", help="Run test scan on representative companies")
    
    args = parser.parse_args()
    run_pipeline(verify=args.verify, notify=args.notify, dry_run=args.dry_run, test_mode=args.test)
