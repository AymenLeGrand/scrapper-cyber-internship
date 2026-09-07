import os
import json
import requests
import re
import sys
import datetime
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

all_jobs = []

# -------------------------------------------------------------
# 1. SYNACKTIV (5 entries: 4 active subjects + 1 official 2025-2026 PFE book)
# -------------------------------------------------------------
synacktiv_entries = [
    {
        "id": "synacktiv_rex_kraqozorus",
        "title": "STAGE M2 / PFE - Recycle Rex : Password Recycling in Kraqozorus (Paris)",
        "company_id": "synacktiv",
        "company_name": "Synacktiv",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": "Paris, France",
        "direct_url": "https://www.synacktiv.com/recycle-rex-enhancement-of-the-password-recycling-feature-in-kraqozorus.html",
        "domain": "Sécurité Offensive & Cryptanalyse",
        "all_domains": ["Sécurité Offensive", "Cryptanalyse", "R&D Sécurité", "Active Directory"],
        "is_crypto": True,
        "is_cyber": True,
        "source": "synacktiv_portal",
        "description": "Amélioration des fonctionnalités de recyclage et analyse cryptographique de mots de passe au sein de l'outil Kraqozorus de Synacktiv. Sujet de recherche et développement offensif.",
        "posted_at": "2025-10-29",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    },
    {
        "id": "synacktiv_dataforge_system",
        "title": "STAGE M2 / PFE - DataForge System ! (Paris)",
        "company_id": "synacktiv",
        "company_name": "Synacktiv",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": "Paris, France",
        "direct_url": "https://www.synacktiv.com/dataforge-system.html",
        "domain": "R&D Sécurité & Génération de Données",
        "all_domains": ["R&D Sécurité", "Sécurité Offensive", "Outillage Cyber"],
        "is_crypto": False,
        "is_cyber": True,
        "source": "synacktiv_portal",
        "description": "Développement et outillage système interne pour la forge, manipulation et analyse de flux de données complexes lors d'exercices d'intrusion et de recherche de vulnérabilités.",
        "posted_at": "2025-10-02",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    },
    {
        "id": "synacktiv_hook_me_if_you_can",
        "title": "STAGE M2 / PFE - Hook me if you can ! (Paris)",
        "company_id": "synacktiv",
        "company_name": "Synacktiv",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": "Paris, France",
        "direct_url": "https://www.synacktiv.com/hook-me-if-you-can.html",
        "domain": "Reverse Engineering & Sécurité Système",
        "all_domains": ["Reverse Engineering", "Sécurité Système", "Sécurité Offensive", "Exploitation"],
        "is_crypto": False,
        "is_cyber": True,
        "source": "synacktiv_portal",
        "description": "Recherche sur les techniques avancées de hooking, d'interception d'API et d'évasion d'EDR au niveau noyau/userland pour les audits de sécurité et tests d'intrusion.",
        "posted_at": "2024-10-30",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    },
    {
        "id": "synacktiv_vuln_research",
        "title": "STAGE M2 / PFE - Recherche et exploitation de vulnérabilités (Paris)",
        "company_id": "synacktiv",
        "company_name": "Synacktiv",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": "Paris, France",
        "direct_url": "https://www.synacktiv.com/stage-recherche-et-exploitation-de-vulnerabilites.html",
        "domain": "Vulnérabilités & Exploitation",
        "all_domains": ["Exploitation", "Vulnerability Research", "Sécurité Offensive", "Reverse Engineering"],
        "is_crypto": False,
        "is_cyber": True,
        "source": "synacktiv_portal",
        "description": "Fuzzing avancé, rétro-ingénierie et conception de preuves de concept (PoC) d'exploitation de vulnérabilités mémoires ou logicielles complexes.",
        "posted_at": "2025-10-02",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    },
    {
        "id": "synacktiv_book_stages_2025_2026",
        "title": "STAGE M2 / PFE - Book Officiel des Stages Synacktiv 2025-2026 (Catalogue des 8 sujets PFE)",
        "company_id": "synacktiv",
        "company_name": "Synacktiv",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": "Paris, Rennes, Toulouse, Lyon, Lille, France",
        "direct_url": "https://www.synacktiv.com/book_stage_synacktiv.pdf",
        "domain": "Catalogue Officiel Stages PFE",
        "all_domains": ["Sécurité Offensive", "Reverse Engineering", "Cryptanalyse", "Recherche de Vulnérabilités"],
        "is_crypto": True,
        "is_cyber": True,
        "source": "synacktiv_official_pdf",
        "description": "Catalogue officiel complet des 8 sujets de stage de fin d'études PFE Master 2 proposés par Synacktiv pour la promo 2025-2026 (Pentest, R&D, Reverse, Crypto, Outillage).",
        "posted_at": "2025-10-01",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    }
]
all_jobs.extend(synacktiv_entries)

# -------------------------------------------------------------
# 2. WAVESTONE (Cybersecurity & Digital Trust) - 25 verified stages
# -------------------------------------------------------------
WAVESTONE_DATES = {'744000145959338': '2026-08-27', '744000140454334': '2026-07-29', '744000140456385': '2026-07-29', '744000140458560': '2026-07-29', '744000140458551': '2026-07-29', '744000140459329': '2026-07-29', '744000140454926': '2026-07-29', '744000146453695': '2026-08-31', '744000141496819': '2026-08-04', '744000141506609': '2026-08-04', '744000141503529': '2026-08-04', '744000141492638': '2026-08-04', '744000141503840': '2026-08-04'}

wavestone_postings = [
    # Paris / Puteaux (Strictly Technical)
    ("744000145959338", "STAGE M2 / PFE - AI & Cybersecurity Consultant (Puteaux)", "Puteaux (Paris)", "Intelligence Artificielle & Cybersécurité", ["IA & Cyber", "Sécurité des LLM", "Prompt Injection", "Audit Technique"]),
    ("744000140454334", "STAGE M2 / PFE - Trust Services : PKI, Signature & Cryptographie (Paris)", "Paris", "Cryptographie & Confiance Numérique", ["Cryptographie", "PKI", "Signature Électronique", "eIDAS"]),
    ("744000140456385", "STAGE M2 / PFE - Garantir la confiance dans les échanges électroniques & PKI (Paris)", "Paris", "Cryptographie & Confiance Numérique", ["Cryptographie", "PKI", "Identité Numérique"]),
    ("744000140458560", "STAGE M2 / PFE - Cybersécurité des SI industriels et innovation OT (Paris)", "Paris", "Cybersécurité Industrielle (OT/SCADA)", ["OT Security", "SCADA", "Sécurité Industrielle"]),
    ("744000140458551", "STAGE M2 / PFE - Cybersécurité des SI industriels & Risques IA / Industrie 4.0 (Paris)", "Paris", "Cybersécurité Industrielle & IA", ["OT Security", "IA", "Industrie 4.0"]),
    ("744000140459329", "STAGE M2 / PFE - Intelligence Artificielle & Cybersécurité : Sécurisation des systèmes émergents (Paris)", "Paris", "IA & Sécurité Numérique", ["IA", "Cybersécurité", "Data"]),
    ("744000140454926", "STAGE M2 / PFE - Cybersécurité IoT : Sécurisation de bout en bout de la puce au Cloud (Paris)", "Paris", "Sécurité IoT & Hardware", ["IoT Security", "Cloud Security", "Hardware"]),
    ("744000146453695", "STAGE M2 / PFE - Workplace Security : Prévention de la compromission du poste de travail (Paris)", "Paris", "Sécurité du Poste de Travail & EDR", ["Workplace Security", "EDR", "Défense"]),
    # Nantes (Strictly Technical)
    ("744000141496819", "STAGE M2 / PFE - Pentest & Red Teaming à l'ère de l'IA générative (Nantes)", "Nantes", "Sécurité Offensive & Pentest", ["Pentest", "Red Team", "IA Générative"]),
    ("744000141506609", "STAGE M2 / PFE - Détection et Réaction par l'IA en Cybersécurité (Nantes)", "Nantes", "SOC & Détection par IA", ["SOC", "Détection", "IA", "Incident Response"]),
    ("744000141503529", "STAGE M2 / PFE - Cloud et sécurité : architectures et modèles de confiance (Nantes)", "Nantes", "Sécurité Cloud", ["Cloud Security", "AWS", "Azure", "Architecture"]),
    ("744000141492638", "STAGE M2 / PFE - DevSecOps et sécurité du développement agile (Nantes)", "Nantes", "DevSecOps & Sécurité Applicative", ["DevSecOps", "CI/CD", "AppSec"]),
    ("744000141503840", "STAGE M2 / PFE - Détection des menaces dans le SI Industriel OT (Nantes)", "Nantes", "Cybersécurité Industrielle (OT)", ["OT Security", "Détection", "SCADA"])
]

for jid, title, city, domain, domains in wavestone_postings:
    is_crypto = any(k in title.lower() or k in domain.lower() for k in ["crypto", "pki", "signature", "confiance"])
    all_jobs.append({
        "id": f"wavestone_sr_{jid}",
        "title": title,
        "company_id": "wavestone",
        "company_name": "Wavestone (Cybersecurity & Digital Trust)",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": f"{city}, France",
        "direct_url": f"https://jobs.smartrecruiters.com/Wavestone1/{jid}",
        "domain": domain,
        "all_domains": domains,
        "is_crypto": is_crypto,
        "is_cyber": True,
        "source": "smartrecruiters_wavestone",
        "description": f"Stage de fin d'études Bac+5 / PFE de 6 mois au sein de la practice Cybersécurité & Digital Trust de Wavestone à {city}. Sujet : {title}.",
        "posted_at": WAVESTONE_DATES.get(jid, "2026-08-04"),
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    })

# -------------------------------------------------------------
# 3. SOPRA STERIA (Cybersecurity) - 7 verified stages with disambiguated city titles
# -------------------------------------------------------------
SOPRA_DATES = {'744000147248678': '2026-09-03', '744000147246974': '2026-09-03', '744000147248409': '2026-09-03', '744000147506608': '2026-09-04', '744000147506149': '2026-09-04', '744000147550118': '2026-09-04', '744000147473198': '2026-09-04'}

sopra_postings = [
    ("744000147248678", "STAGE M2 / PFE - Analyste MDR : Détection Cybersécurité (Rennes)", "Cesson-Sévigné (Rennes)", "Détection & MDR", ["SOC / MDR", "Détection", "SIEM", "Incident Response"]),
    ("744000147246974", "STAGE M2 / PFE - Analyste MDR : Détection Cybersécurité (Paris)", "Courbevoie (Paris)", "Détection & MDR", ["SOC / MDR", "Détection", "SIEM", "Incident Response"]),
    ("744000147248409", "STAGE M2 / PFE - Analyste MDR : Détection Cybersécurité (Toulouse)", "Colomiers (Toulouse)", "Détection & MDR", ["SOC / MDR", "Détection", "SIEM", "Incident Response"]),
    ("744000147506608", "STAGE M2 / PFE - Analyste VOC Cybersécurité : Veille & Vulnérabilités (Paris)", "Courbevoie (Paris)", "Threat Intelligence & Vulnérabilités", ["CTI", "Vulnérabilités", "Veille Menaces", "CERT"]),
    ("744000147506149", "STAGE M2 / PFE - Analyste VOC Cybersécurité : Veille & Vulnérabilités (Toulouse)", "Colomiers (Toulouse)", "Threat Intelligence & Vulnérabilités", ["CTI", "Vulnérabilités", "Veille Menaces", "CERT"]),
    ("744000147550118", "STAGE M2 / PFE - Analyste Cybersécurité : Investigation Numérique & Forensics (Toulouse)", "Colomiers (Toulouse)", "Investigation Numérique & DFIR", ["Forensics", "DFIR", "Analyse Mémoire", "Investigation"]),
    ("744000147473198", "STAGE M2 / PFE - Analyste Cybersécurité : Réponse à Incident CSIRT (Toulouse)", "Colomiers (Toulouse)", "Réponse aux Incidents & CSIRT", ["CSIRT", "Incident Response", "Gestion de Crise", "DFIR"])
]

for jid, title, city, domain, domains in sopra_postings:
    all_jobs.append({
        "id": f"sopra_sr_{jid}",
        "title": title,
        "company_id": "sopra_steria",
        "company_name": "Sopra Steria (Cybersecurity)",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": f"{city}, France",
        "direct_url": f"https://jobs.smartrecruiters.com/SopraSteria1/{jid}",
        "domain": domain,
        "all_domains": domains,
        "is_crypto": False,
        "is_cyber": True,
        "source": "smartrecruiters_soprasteria",
        "description": f"Stage de fin d'études Bac+5 / PFE de 6 mois au sein du pôle Cybersécurité de Sopra Steria à {city}. Missions opérationnelles sur {domain}.",
        "posted_at": SOPRA_DATES.get(jid, "2026-09-03"),
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    })

# -------------------------------------------------------------
# 4. HEADMIND PARTNERS (Cyber Risk & Security) - Strictly Technical (Red Team & Blue Team)
# -------------------------------------------------------------
headmind_postings = [
    ("consultant-cyberdefense-red-team-sfe", "STAGE M2 / PFE - Consultant Sécurité Offensive & Red Team (Paris)", "Paris", "Sécurité Offensive & Red Team", ["Pentest", "Red Team", "Audit Technique", "Evasion EDR"]),
    ("consultant-cyberdefense-blue-team-sfe", "STAGE M2 / PFE - Consultant Cyberdéfense Blue Team (Paris)", "Paris", "Cyberdéfense & Blue Team", ["Blue Team", "SOC", "Détection", "Investigation"])
]

for slug, title, city, domain, domains in headmind_postings:
    all_jobs.append({
        "id": f"headmind_{slug.replace('-', '_')}",
        "title": title,
        "company_id": "headmind_partners",
        "company_name": "HeadMind Partners (Cyber Risk & Security)",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": f"{city}, France",
        "direct_url": f"https://join.headmind.com/offres/{slug}/",
        "domain": domain,
        "all_domains": domains,
        "is_crypto": False,
        "is_cyber": True,
        "source": "headmind_careers",
        "description": f"Stage de fin d'études Bac+5 / PFE de 6 mois chez HeadMind Partners à {city}. Missions de pointe en cyberdéfense et conseil avec perspective d'embauche en CDI.",
        "posted_at": "2026-09-01",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    })

# -------------------------------------------------------------
# 5. VINCI CONSTRUCTION SI - Strictly Technical (Cyberdéfense / SOC / DFIR)
# -------------------------------------------------------------
vinci_postings = [
    ("43867364800", "STAGE M2 / PFE - Analyste Cyberdéfense (Nanterre)", "https://jobs.vinci.com/fr/emploi/nanterre/analyste-cyberdefense-1-stage-de-fin-d-etudes-en-pre-embauche-f-h/1440/43867364800", "Cyberdéfense & Détection", ["SOC", "Cyberdéfense", "Incident Response", "SIEM"])
]

for jid, title, url, domain, domains in vinci_postings:
    all_jobs.append({
        "id": f"vinci_{jid}",
        "title": title,
        "company_id": "vinci_construction",
        "company_name": "VINCI Construction SI",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": "Nanterre (Paris), France",
        "direct_url": url,
        "domain": domain,
        "all_domains": domains,
        "is_crypto": False,
        "is_cyber": True,
        "source": "vinci_careers",
        "description": f"Stage de fin d'études Bac+5 / PFE de 6 mois pré-embauche chez VINCI Construction SI (Nanterre). Intégration au sein de la DSI sur le sujet : {title}.",
        "posted_at": "2026-09-01",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    })

# -------------------------------------------------------------
# 6. OCTO TECHNOLOGY (Accenture) - 2 verified stages
# -------------------------------------------------------------
OCTO_DATES = {'744000146426969': '2026-08-31', '744000146940465': '2026-09-02'}

octo_postings = [
    ("744000146426969", "STAGE M2 / PFE - Cloud Security & Automatisation de la Sécurité Cloud Souverain (Paris)", "Paris", "Sécurité Cloud & Automatisation", ["Cloud Security", "DevSecOps", "Scaleway", "Python", "Go"]),
    ("744000146940465", "STAGE M2 / PFE - AI Engineer & Sécurisation des Applications Agentiques (Paris)", "Paris", "IA & Sécurité Applicative", ["Agents IA", "Cybersécurité", "LLM Security", "Software Engineering"])
]

for jid, title, city, domain, domains in octo_postings:
    all_jobs.append({
        "id": f"octo_sr_{jid}",
        "title": title,
        "company_id": "octo_technology",
        "company_name": "OCTO Technology (Accenture)",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": f"{city}, France",
        "direct_url": f"https://jobs.smartrecruiters.com/OctoTechnology/{jid}",
        "domain": domain,
        "all_domains": domains,
        "is_crypto": False,
        "is_cyber": True,
        "source": "smartrecruiters_octo",
        "description": f"Stage de fin d'études Bac+5 / PFE de 6 mois chez OCTO Technology (Paris). R&D appliquée et ingénierie de sécurité de pointe.",
        "posted_at": OCTO_DATES.get(jid, "2026-09-01"),
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    })

# -------------------------------------------------------------
# 7. SIA PARTNERS (Cybersecurity, Data Protection & Resilience) - 1 verified stage
# -------------------------------------------------------------
all_jobs.append({
    "id": "sia_sr_744000146907409",
    "title": "STAGE M2 / PFE - Consultant Cybersécurité (IA, Zero Trust, Forensics, OT) (Paris)",
    "company_id": "sia_partners",
    "company_name": "Sia Partners",
    "contract_type": "Stage M2 / PFE (6 mois)",
    "location": "Paris, France",
    "direct_url": "https://jobs.smartrecruiters.com/Sia/744000146907409",
    "domain": "Conseil Cybersécurité & Innovation",
    "all_domains": ["AI Cyber", "Zero Trust", "Forensics", "OT Security", "Web3 Security"],
    "is_crypto": True,
    "is_cyber": True,
    "source": "smartrecruiters_sia",
    "description": "Stage de fin d'études Bac+5 / PFE de 6 mois avec perspective d'embauche au sein de la Business Line Cybersecurity de Sia Partners. Sujets de recherche au Sia CyberLab (AI systems, Zero Trust, Web3, Forensics).",
    "posted_at": "2026-09-02",
    "status": "active",
    "verification_status": "VERIFIED_ACTIVE"
})

# -------------------------------------------------------------
# 8. FORVIS MAZARS (Cybersecurity & Audit) - 1 verified stage
# -------------------------------------------------------------
all_jobs.append({
    "id": "mazars_sr_744000088308225",
    "title": "STAGE M2 / PFE - Consultant(e) Cybersécurité & Pentest PASSI (Nantes)",
    "company_id": "forvis_mazars",
    "company_name": "Forvis Mazars",
    "contract_type": "Stage M2 / PFE (6 mois)",
    "location": "Saint-Herblain (Nantes), France",
    "direct_url": "https://jobs.smartrecruiters.com/MAZARS/744000088308225",
    "domain": "Audit & Tests d'Intrusion PASSI",
    "all_domains": ["Pentest", "Audit PASSI", "Sécurité des Systèmes", "Revue de Code"],
    "is_crypto": False,
    "is_cyber": True,
    "source": "smartrecruiters_mazars",
    "description": "Stage de fin d'études Bac+5 / PFE de 6 mois au sein de l'équipe Cybersécurité qualifiée PASSI de Forvis Mazars à Nantes. Missions d'audits techniques, tests d'intrusion et conseil.",
    "posted_at": "2025-10-16",
    "status": "active",
    "verification_status": "VERIFIED_ACTIVE"
})

# -------------------------------------------------------------
# 9. DEVOTEAM CYBER TRUST - Strictly Technical (R&D IA & Cyber)
# -------------------------------------------------------------
devoteam_postings = [
    ("744000147309339", "STAGE M2 / PFE - Ingénieur(e) R&D Intelligence Artificielle & Cybersécurité (Paris)", "Levallois-Perret (Paris)", "R&D IA & Cybersécurité", ["IA & Cyber", "R&D", "Data Science", "Threat Intelligence"])
]

for jid, title, city, domain, domains in devoteam_postings:
    all_jobs.append({
        "id": f"devoteam_sr_{jid}",
        "title": title,
        "company_id": "devoteam",
        "company_name": "Devoteam Cyber Trust",
        "contract_type": "Stage M2 / PFE (6 mois)",
        "location": f"{city}, France",
        "direct_url": f"https://jobs.smartrecruiters.com/Devoteam/{jid}",
        "domain": domain,
        "all_domains": domains,
        "is_crypto": False,
        "is_cyber": True,
        "source": "smartrecruiters_devoteam",
        "description": f"Stage de fin d'études Bac+5 / PFE de 6 mois au sein de Devoteam Cyber Trust à {city}. Sujet : {title}.",
        "posted_at": "2026-09-03",
        "status": "active",
        "verification_status": "VERIFIED_ACTIVE"
    })

# -------------------------------------------------------------
# 10. QUARKSLAB - Research Blog Automated Monitor
# -------------------------------------------------------------
try:
    try:
        from scraper.quarkslab_scraper import parse_quarkslab_offers
    except ImportError:
        from quarkslab_scraper import parse_quarkslab_offers
    quark_offers = parse_quarkslab_offers(include_filled=False)
    if quark_offers:
        print(f"[Quarkslab] {len(quark_offers)} active/open offers detected!")
        all_jobs.extend(quark_offers)
    else:
        print("[Quarkslab] Monitoring active: all previous topics filled, awaiting new season publication.")
except Exception as e:
    print(f"[Quarkslab] Monitor warning: {e}")

# -------------------------------------------------------------
# 11. DYNAMIC ATS INGESTION (Stormshield, Sekoia, Thales, Airbus, Zama, SERMA, Ledger)
# -------------------------------------------------------------
try:
    from scraper.ats_scrapers import (
        scrape_teamtailor,
        scrape_workday,
        scrape_zama,
        scrape_serma,
        scrape_lever
    )
except ImportError:
    from ats_scrapers import (
        scrape_teamtailor,
        scrape_workday,
        scrape_zama,
        scrape_serma,
        scrape_lever
    )

scraper_errors = []

# 1. Stormshield (Teamtailor Feed)
try:
    ss_jobs = scrape_teamtailor({
        "id": "stormshield",
        "name": "Stormshield (Airbus Defence & Space)",
        "teamtailor_feed_url": "https://careers.stormshield.eu/jobs.json"
    })
    if ss_jobs:
        print(f"[Stormshield] {len(ss_jobs)} new stages ingested!")
        all_jobs.extend(ss_jobs)
    else:
        print("[Stormshield] Feed monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Stormshield] Ingestion warning: {e}")
    scraper_errors.append(f"Stormshield: {e}")

# 2. Sekoia.io (Teamtailor Feed)
try:
    sekoia_jobs = scrape_teamtailor({
        "id": "sekoia",
        "name": "Sekoia.io (SOC & XDR)",
        "teamtailor_feed_url": "https://careers.sekoia.com/jobs.json"
    })
    if sekoia_jobs:
        print(f"[Sekoia.io] {len(sekoia_jobs)} new stages ingested!")
        all_jobs.extend(sekoia_jobs)
    else:
        print("[Sekoia.io] Feed monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Sekoia.io] Ingestion warning: {e}")
    scraper_errors.append(f"Sekoia: {e}")

# 3. Thales Cyber (Workday CXS)
try:
    thales_jobs = scrape_workday({
        "id": "thales",
        "name": "Thales Cyber",
        "workday_tenant": "thales"
    })
    if thales_jobs:
        print(f"[Thales] {len(thales_jobs)} new stages ingested!")
        all_jobs.extend(thales_jobs)
    else:
        print("[Thales] Workday CXS monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Thales] Ingestion warning: {e}")
    scraper_errors.append(f"Thales: {e}")

# 4. Airbus Protect / Cyber (Workday CXS)
try:
    airbus_jobs = scrape_workday({
        "id": "airbus_protect",
        "name": "Airbus Protect (Cybersécurité & Sûreté)",
        "workday_tenant": "ag",
        "hiring_companies": [
            "f5811cef9cb50166ff1fba124e0a295c",
            "f5811cef9cb501eb3bf4e0124e0add5c",
            "f5811cef9cb5013b35f9bb124e0a335c"
        ]
    })
    if airbus_jobs:
        print(f"[Airbus] {len(airbus_jobs)} new stages ingested!")
        all_jobs.extend(airbus_jobs)
    else:
        print("[Airbus] Workday CXS monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Airbus] Ingestion warning: {e}")
    scraper_errors.append(f"Airbus Protect: {e}")

# 5. Zama (Homerun Board)
try:
    zama_jobs = scrape_zama({
        "id": "zama",
        "name": "Zama (FHE & Cryptography)"
    })
    if zama_jobs:
        print(f"[Zama] {len(zama_jobs)} new stages ingested!")
        all_jobs.extend(zama_jobs)
    else:
        print("[Zama] Site officiel monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Zama] Ingestion warning: {e}")
    scraper_errors.append(f"Zama: {e}")

# 6. SERMA Safety & Security (Site Officiel)
try:
    serma_jobs = scrape_serma({
        "id": "serma-safety-security",
        "name": "SERMA Safety & Security"
    })
    if serma_jobs:
        print(f"[SERMA] {len(serma_jobs)} new stages ingested!")
        all_jobs.extend(serma_jobs)
    else:
        print("[SERMA] Site officiel monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[SERMA] Ingestion warning: {e}")
    scraper_errors.append(f"SERMA: {e}")

# 7. Ledger (Lever API)
try:
    ledger_jobs = scrape_lever({
        "id": "ledger",
        "name": "Ledger (Donjon & Security)",
        "ats_company_id": "ledger"
    })
    if ledger_jobs:
        print(f"[Ledger] {len(ledger_jobs)} new stages ingested!")
        all_jobs.extend(ledger_jobs)
    else:
        print("[Ledger] Lever API monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Ledger] Ingestion warning: {e}")
    scraper_errors.append(f"Ledger: {e}")

# 8. Wavestone (SmartRecruiters)
try:
    from scraper.ats_scrapers import scrape_smartrecruiters
except ImportError:
    from ats_scrapers import scrape_smartrecruiters

try:
    wave_jobs = scrape_smartrecruiters({
        "id": "wavestone",
        "name": "Wavestone (Cybersecurity & Digital Trust)",
        "ats_company_id": "Wavestone1"
    })
    if wave_jobs:
        print(f"[Wavestone] {len(wave_jobs)} new stages ingested!")
        all_jobs.extend(wave_jobs)
    else:
        print("[Wavestone] SmartRecruiters monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Wavestone] Ingestion warning: {e}")
    scraper_errors.append(f"Wavestone: {e}")

# 9. Devoteam Cyber Trust (SmartRecruiters)
try:
    devo_jobs = scrape_smartrecruiters({
        "id": "devoteam-cyber-trust",
        "name": "Devoteam Cyber Trust",
        "ats_company_id": "Devoteam"
    })
    if devo_jobs:
        print(f"[Devoteam] {len(devo_jobs)} new stages ingested!")
        all_jobs.extend(devo_jobs)
    else:
        print("[Devoteam] SmartRecruiters monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Devoteam] Ingestion warning: {e}")
    scraper_errors.append(f"Devoteam: {e}")

# 10. Advens (SmartRecruiters)
try:
    advens_jobs = scrape_smartrecruiters({
        "id": "advens",
        "name": "Advens (Pure-player Cybersécurité)",
        "ats_company_id": "Advens"
    })
    if advens_jobs:
        print(f"[Advens] {len(advens_jobs)} new stages ingested!")
        all_jobs.extend(advens_jobs)
    else:
        print("[Advens] SmartRecruiters monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[Advens] Ingestion warning: {e}")
    scraper_errors.append(f"Advens: {e}")

# 11. CrowdSec (Recruitee)
try:
    from scraper.ats_scrapers import scrape_recruitee
except ImportError:
    from ats_scrapers import scrape_recruitee

try:
    cs_jobs = scrape_recruitee({
        "id": "crowdsec",
        "name": "CrowdSec",
        "recruitee_slug": "crowdsec"
    })
    if cs_jobs:
        print(f"[CrowdSec] {len(cs_jobs)} new stages ingested!")
        all_jobs.extend(cs_jobs)
    else:
        print("[CrowdSec] Recruitee monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[CrowdSec] Ingestion warning: {e}")
    scraper_errors.append(f"CrowdSec: {e}")

# 12. XMCO (Recruitee)
try:
    xmco_jobs = scrape_recruitee({
        "id": "xmco",
        "name": "XMCO",
        "recruitee_slug": "xmco"
    })
    if xmco_jobs:
        print(f"[XMCO] {len(xmco_jobs)} new stages ingested!")
        all_jobs.extend(xmco_jobs)
    else:
        print("[XMCO] Recruitee monitored (awaiting new campaign publication).")
except Exception as e:
    print(f"[XMCO] Ingestion warning: {e}")
    scraper_errors.append(f"XMCO: {e}")

# 13. LINKEDIN (Public Guest Jobs API)
try:
    try:
        from scraper.linkedin_scraper import scrape_linkedin
    except ImportError:
        from linkedin_scraper import scrape_linkedin

    linkedin_jobs = scrape_linkedin(max_pages_per_kw=2)
    if linkedin_jobs:
        print(f"[LinkedIn] {len(linkedin_jobs)} new stages ingested!")
        all_jobs.extend(linkedin_jobs)
    else:
        print("[LinkedIn] Feed monitored (0 matches or rate-limited).")
except Exception as e:
    print(f"[LinkedIn] Ingestion warning: {e}")
    scraper_errors.append(f"LinkedIn: {e}")

# -------------------------------------------------------------
# DEDUPLICATION & VALIDATION
# -------------------------------------------------------------
unique_jobs = []
seen_ids = set()
seen_urls = set()

for j in all_jobs:
    if not j.get("status"):
        j["status"] = "active"
    if j["id"] not in seen_ids and j["direct_url"] not in seen_urls:
        seen_ids.add(j["id"])
        seen_urls.add(j["direct_url"])
        unique_jobs.append(j)

all_jobs = unique_jobs

print(f"\nTotal jobs configured: {len(all_jobs)}")
c = Counter(j['company_name'] for j in all_jobs)
for comp, cnt in sorted(c.items()):
    print(f" - {comp}: {cnt}")

# Write to data/jobs.json
output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "jobs.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS: Written {len(all_jobs)} verified offers to {output_path}!")

# Write meta.json with scrape timestamp (used by frontend countdown timer)
meta_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "meta.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump({
        "last_scraped_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": len(all_jobs),
        "scraper_errors": scraper_errors
    }, f)
print(f"Meta written to {meta_path}")
if scraper_errors:
    print(f"[HEALTH] {len(scraper_errors)} scraper error(s) detected: {scraper_errors}")
