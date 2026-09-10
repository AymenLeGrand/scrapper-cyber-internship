"""
Non-regression test suite for France Cyber & Cryptology M2 Internship Tracker.
"""

import json
import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scraper.filters import (
    is_internship,
    categorize_job,
    check_algerian_national_eligibility,
    is_france_location,
    is_valid_cyber_crypto_job,
)
from scraper.notifier import (
    load_seen_job_ids,
    save_seen_job_ids,
    build_email_content,
)
from scraper.validator import EXPIRED_PAGE_PHRASES


class TestFilters(unittest.TestCase):
    def test_is_internship(self):
        # Valid internship titles
        self.assertTrue(is_internship("Stage M2 - Analyste SOC"))
        self.assertTrue(is_internship("STAGE PFE - Cryptographie Post-Quantique"))
        self.assertTrue(is_internship("End-of-study internship in Hardware Security"))
        self.assertTrue(is_internship("Stagiaire Pentest (6 mois)"))

        # Excluded non-internship contracts
        self.assertFalse(is_internship("CDI Senior Security Consultant"))
        self.assertFalse(is_internship("Alternance - Chef de projet digital"))
        self.assertFalse(is_internship("Post-doc Cryptanalysis"))

    def test_categorize_job(self):
        crypto_res = categorize_job("Stage Cryptographie et chiffrement homomorphe")
        self.assertTrue(crypto_res["is_crypto"])
        self.assertIn("Cryptology", crypto_res["all_domains"])

        pentest_res = categorize_job("Stage Pentest & Red Teaming")
        self.assertTrue(pentest_res["is_cyber"])
        self.assertIn("Cyber Offensive / Hardware / Pentest", pentest_res["all_domains"])

    def test_check_algerian_national_eligibility(self):
        # Normal offer without nationality restriction
        eligible, _ = check_algerian_national_eligibility("Stage Sécurité Cloud", "Mission ouverte aux étudiants M2")
        self.assertTrue(eligible)

        # Restricted offer
        restricted, reason = check_algerian_national_eligibility(
            "Stage Cyber Défense",
            "Poste avec habilitation secret défense, nationalité française obligatoire"
        )
        self.assertFalse(restricted)
        self.assertIn("nationalité française", reason.lower())

    def test_is_france_location(self):
        self.assertTrue(is_france_location("Paris, France"))
        self.assertTrue(is_france_location("Rennes / Télétravail"))
        self.assertTrue(is_france_location("Pessac (Bordeaux)"))
        self.assertFalse(is_france_location("Munich, Germany"))
        self.assertFalse(is_france_location("London, UK"))

    def test_is_valid_cyber_crypto_job(self):
        self.assertTrue(is_valid_cyber_crypto_job("STAGE M2 / PFE - Pentest Web & Mobile"))
        self.assertTrue(is_valid_cyber_crypto_job("Stage Cryptologie Appliquée"))
        self.assertTrue(is_valid_cyber_crypto_job("Stage AI & Cybersecurity Consultant"))
        # Pure non-cyber GRC / generic business should be excluded
        self.assertFalse(is_valid_cyber_crypto_job("Stage Juriste Droit des Affaires & RGPD"))


class TestNotifier(unittest.TestCase):
    def test_safe_seen_job_handling(self):
        # None path should not raise TypeError
        self.assertEqual(load_seen_job_ids(None), set())
        save_seen_job_ids(None, {"job_1"})  # Should not raise exception

        # Empty string path
        self.assertEqual(load_seen_job_ids(""), set())
        save_seen_job_ids("", {"job_1"})

    def test_build_email_content(self):
        sample_jobs = [
            {
                "id": "test_1",
                "title": "Stage Cryptographie PQC",
                "company_name": "CryptoCorp",
                "location": "Paris",
                "direct_url": "https://example.com/job1",
                "is_crypto": True,
                "is_cyber": True,
                "domain": "Cryptology",
            }
        ]
        subject, text, html = build_email_content(sample_jobs)
        self.assertIn("M2 Cyber & Crypto", subject)
        self.assertIn("CryptoCorp", text)
        self.assertIn("https://example.com/job1", html)
        self.assertIn("Nouveaux Stages M2", html)


class TestDatabaseIntegrity(unittest.TestCase):
    def test_jobs_json_validity(self):
        jobs_file = os.path.join(BASE_DIR, "data", "jobs.json")
        self.assertTrue(os.path.exists(jobs_file), "data/jobs.json must exist")

        with open(jobs_file, "r", encoding="utf-8") as f:
            jobs = json.load(f)

        self.assertIsInstance(jobs, list)
        self.assertGreater(len(jobs), 0, "jobs.json should not be empty")

        for j in jobs:
            self.assertIn("id", j)
            self.assertIn("title", j)
            self.assertIn("company_name", j)
            self.assertIn("direct_url", j)
            self.assertTrue(j["direct_url"].startswith("http"), f"Invalid direct_url in {j['id']}")
            self.assertIn("status", j)


class TestValidatorPhrases(unittest.TestCase):
    def test_expired_phrases_compiled(self):
        import re
        self.assertGreater(len(EXPIRED_PAGE_PHRASES), 5)
        for pattern in EXPIRED_PAGE_PHRASES:
            compiled = re.compile(pattern, re.IGNORECASE)
            self.assertIsNotNone(compiled)

    def test_posted_at_format(self):
        import re
        jobs_file = os.path.join(BASE_DIR, "data", "jobs.json")
        with open(jobs_file, "r", encoding="utf-8") as f:
            jobs = json.load(f)

        iso_or_date = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(\.\d+)?Z)?$")
        for j in jobs:
            posted = j.get("posted_at")
            self.assertIsNotNone(posted, f"Job {j['id']} is missing posted_at")
            self.assertTrue(bool(iso_or_date.match(posted)), f"Job {j['id']} has invalid posted_at format: {posted}")


if __name__ == "__main__":
    unittest.main()
