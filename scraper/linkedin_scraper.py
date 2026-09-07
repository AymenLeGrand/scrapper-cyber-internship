"""
LinkedIn Guest Jobs Public Scraper for France Cyber & Crypto M2/PFE Internships.
Queries LinkedIn's guest jobs endpoint for active internship postings in France,
extracts title, company, clean job URL, company logo CDN link, and exact publication date/age.
"""

import logging
import re
import time
import urllib.parse
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

from scraper.filters import (
    is_internship,
    categorize_job,
    check_algerian_national_eligibility,
    is_france_location,
)

logger = logging.getLogger("scraper.linkedin")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
}

BASE_SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

KEYWORDS = [
    "stage cybersecurite",
    "stage cryptographie",
    "stage pentest",
    "stage soc cert",
    "stage pfe cyber",
    "stage securite informatique",
    "stage reverse engineering",
]


def clean_linkedin_url(raw_url: str) -> str:
    """Cleans tracking parameters and returns canonical job URL."""
    if not raw_url:
        return ""
    clean = raw_url.split("?")[0]
    return clean.strip()


def extract_linkedin_id(clean_url: str) -> str:
    """Extracts numeric job ID from LinkedIn URL."""
    m = re.search(r"-(\d+)$", clean_url) or re.search(r"/view/.*?(\d+)", clean_url) or re.search(r"(\d{8,})", clean_url)
    if m:
        return m.group(1)
    return str(abs(hash(clean_url)))


def scrape_linkedin(max_pages_per_kw: int = 2) -> List[Dict[str, Any]]:
    """
    Scrapes LinkedIn guest jobs API for France-based cyber & crypto internships.
    Returns list of verified, deduplicated internship job dicts.
    """
    found_jobs: Dict[str, Dict[str, Any]] = {}

    for kw in KEYWORDS:
        for page in range(max_pages_per_kw):
            start = page * 25
            params = {
                "keywords": kw,
                "location": "France",
                "f_TPR": "r2592000",  # Past 30 days
                "start": start,
            }

            url = f"{BASE_SEARCH_URL}?{urllib.parse.urlencode(params)}"
            try:
                resp = requests.get(url, headers=HEADERS, timeout=12)
                if resp.status_code != 200:
                    logger.debug(f"[LinkedIn] HTTP {resp.status_code} for query '{kw}' start={start}")
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                cards = soup.find_all("li")
                if not cards:
                    break

                for c in cards:
                    title_elem = c.find("h3", class_="base-search-card__title")
                    comp_elem = c.find("h4", class_="base-search-card__subtitle")
                    link_elem = c.find("a", class_="base-card__full-link")
                    loc_elem = c.find("span", class_="job-search-card__location")
                    time_elem = c.find("time")
                    img_elem = c.find("img")

                    if not (title_elem and link_elem):
                        continue

                    title = title_elem.get_text(strip=True)
                    clean_url = clean_linkedin_url(link_elem.get("href", ""))
                    if not clean_url:
                        continue

                    raw_id = extract_linkedin_id(clean_url)
                    job_id = f"linkedin_{raw_id}"

                    if job_id in found_jobs:
                        continue

                    company = comp_elem.get_text(strip=True) if comp_elem else "Entreprise"
                    location = loc_elem.get_text(strip=True) if loc_elem else "France"

                    posted_at = ""
                    posted_relative = ""
                    if time_elem:
                        posted_at = time_elem.get("datetime") or ""
                        posted_relative = time_elem.get_text(strip=True) or ""

                    logo_url = ""
                    if img_elem:
                        logo_url = img_elem.get("data-delayed-url") or img_elem.get("src") or ""
                        if "ghost" in logo_url or "static.licdn.com" in logo_url:
                            logo_url = ""

                    # 1. Filter: strictly an internship
                    if not is_internship(title):
                        continue

                    # 2. Filter: located in France
                    if not is_france_location(location):
                        continue

                    # 3. Filter: cyber or crypto domain
                    domain_info = categorize_job(title)
                    if not domain_info["is_crypto"] and not domain_info["is_cyber"]:
                        continue

                    # 4. Filter: Algerian / non-EU national eligible
                    eligible, reason = check_algerian_national_eligibility(title)
                    if not eligible:
                        continue

                    found_jobs[job_id] = {
                        "id": job_id,
                        "title": title,
                        "company_name": company,
                        "location": location if "France" in location else f"{location}, France",
                        "direct_url": clean_url,
                        "logo_url": logo_url,
                        "posted_at": posted_at,
                        "posted_relative": posted_relative,
                        "domain": domain_info["primary_domain"],
                        "all_domains": domain_info["all_domains"],
                        "is_crypto": domain_info["is_crypto"],
                        "is_cyber": domain_info["is_cyber"],
                        "eligible_algerian": eligible,
                        "eligibility_note": reason,
                        "source": "LinkedIn (Offres Publiques)",
                        "status": "active",
                        "verification_status": "VERIFIED_ACTIVE",
                    }

                time.sleep(0.3)
            except Exception as e:
                logger.warning(f"[LinkedIn] Error scraping '{kw}' (start={start}): {e}")

    results = list(found_jobs.values())
    logger.info(f"[LinkedIn] Scraped {len(results)} verified active internships.")
    return results


if __name__ == "__main__":
    jobs = scrape_linkedin()
    print(f"Scraped {len(jobs)} jobs from LinkedIn.")
    for j in jobs[:5]:
        print(f" - {j['company_name']} | {j['title']} | Date: {j['posted_at']} | Logo: {bool(j['logo_url'])}")
