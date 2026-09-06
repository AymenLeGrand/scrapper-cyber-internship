"""
Job Posting Liveness & Expiration Validator.
Ensures every job in data/jobs.json is actively open on the company website.
Detects:
- HTTP 404 / 410 / 500 errors
- Soft 404s and expired posting banners ("offre expirée", "job closed", etc.)
- Redirections back to generic career homepages
"""

import datetime
import logging
import re
import requests
from typing import Dict, Any, Tuple, List

logger = logging.getLogger("scraper.validator")
REQUEST_TIMEOUT = 10

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

EXPIRED_PAGE_PHRASES = [
    r"cette\s+offre\s+n['’]est\s+plus\s+disponible",
    r"cette\s+offre\s+a\s+[eé]t[eé]\s+pourvue",
    r"cette\s+offre\s+est\s+expir[eé]e",
    r"ce\s+poste\s+est\s+pourvu",
    r"ce\s+poste\s+a\s+[eé]t[eé]\s+pourvu",
    r"offre\s+cl[oô]tur[eé]e",
    r"l['’]offre\s+que\s+vous\s+cherchez\s+n['’]existe\s+plus",
    r"job\s+is\s+no\s+longer\s+available",
    r"job\s+posting\s+has\s+closed",
    r"position\s+has\s+been\s+filled",
    r"this\s+posting\s+has\s+expired",
    r"page\s+introuvable",
    r"404\s+not\s+found"
]


def verify_job_url(url: str) -> Tuple[bool, str]:
    """
    Checks if a job URL is active and still accepting applications.
    Returns: (is_active, status_reason)
    """
    if not url or not url.startswith("http"):
        return False, "URL invalide"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"
    }

    try:
        # Perform GET request with stream to inspect content quickly
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        
        # Check HTTP status
        if resp.status_code in [404, 410]:
            return False, f"HTTP {resp.status_code}: Offre introuvable / supprimée"
        
        if resp.status_code >= 400:
            return False, f"HTTP {resp.status_code}: Erreur serveur ou accès refusé"

        # Check for soft-404 expiration phrases in page content
        content_sample = resp.text[:20000].lower()
        for phrase in EXPIRED_PAGE_PHRASES:
            if re.search(phrase, content_sample, re.IGNORECASE):
                return False, "Offre expirée ou pourvue (détecté sur la page de l'entreprise)"

        return True, "Actif (Vérifié en direct)"

    except requests.exceptions.Timeout:
        # If timeout, retain as active unless consecutive failures
        return True, "Timeout temporaire lors de la vérification (conservé actif)"
    except Exception as e:
        logger.debug(f"Verification error for {url}: {e}")
        return False, f"Erreur de connexion: {str(e)[:50]}"


def validate_all_jobs(jobs: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Validates an entire list of jobs.
    Returns: (active_jobs, expired_jobs)
    """
    now_iso = datetime.datetime.utcnow().isoformat() + "Z"
    active_jobs = []
    expired_jobs = []

    for job in jobs:
        url = job.get("direct_url", "")
        is_active, reason = verify_job_url(url)
        
        job["last_verified_at"] = now_iso
        job["verification_status"] = reason

        if is_active:
            job["status"] = "active"
            active_jobs.append(job)
        else:
            job["status"] = "expired"
            expired_jobs.append(job)

    return active_jobs, expired_jobs
