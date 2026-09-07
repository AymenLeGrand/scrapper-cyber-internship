"""
France Cyber & Crypto Tracker: Periodic Re-Scraper (Alias for scripts/run_hourly.py).
Runs the automated M2 Cyber & Cryptology scraping pipeline every 3 hours.
"""
import os
import sys

# Add scripts directory to sys.path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from run_hourly import main

if __name__ == '__main__':
    main()

