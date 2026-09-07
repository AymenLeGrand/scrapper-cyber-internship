"""
Curated Registry of French Cybersecurity & Cryptology Employers.
Contains over 70 verified French organizations spanning:
- Hardware Security, CESTI Evaluation & Embedded Cryptology (SERMA, eShard, Secure-IC, NinjaLab, STMicroelectronics, NXP, etc.)
- Advanced Cryptology & R&D Labs (CryptoExperts, Quarkslab, Zama, Cosmian, Inria, CEA, Ledger)
- Pure-Play Cybersecurity Editors & Boutiques (Synacktiv, Stormshield, Sekoia, TEHTRIS, Gatewatcher, HarfangLab, GitGuardian, YesWeHack)
- Aerospace, Defense & Industrial Giants (Thales, Airbus Cyber, Safran, Naval Group, Dassault, MBDA)
- Cyber Consulting & Leading MSSPs (Orange Cyberdefense, Advens, Wavestone, Capgemini, Sopra Steria, Eviden)
- Critical Infrastructure (OIV) & Banking CERTs (BNP Paribas, Société Générale, Crédit Agricole, EDF)
"""

COMPANIES = [
    # =========================================================================
    # 1. HARDWARE SECURITY, CESTI EVALUATION & EMBEDDED CRYPTOLOGY
    # =========================================================================
    {
        "id": "serma-safety-security",
        "name": "SERMA Safety & Security / SERMA NES",
        "category": "hardware_crypto_cesti",
        "website": "https://www.serma-safety-security.com",
        "career_url": "https://www.serma.com/carrieres/offres-emploi/?company=SERMA%20Safety%20and%20Security",
        "direct_ats_type": "custom",
        "tags": ["hardware_security", "cesti", "side_channel", "fault_injection", "cryptology", "smartcard", "pentest"],
        "open_to_international": True
    },
    {
        "id": "eshard",
        "name": "eShard",
        "category": "hardware_crypto_cesti",
        "website": "https://eshard.com",
        "career_url": "https://eshard.com/careers",
        "direct_ats_type": "custom",
        "tags": ["hardware_security", "side_channel", "fault_injection", "cryptology", "mobile_security", "embedded"],
        "open_to_international": True
    },
    {
        "id": "secure-ic",
        "name": "Secure-IC",
        "category": "hardware_crypto_cesti",
        "website": "https://www.secure-ic.com",
        "career_url": "https://www.secure-ic.com/careers/",
        "direct_ats_type": "custom",
        "tags": ["embedded_security", "cryptology", "root_of_trust", "post_quantum", "side_channel", "hardware_ip"],
        "open_to_international": True
    },
    {
        "id": "ninjalab",
        "name": "NinjaLab",
        "category": "hardware_crypto_cesti",
        "website": "https://ninjalab.io",
        "career_url": "https://ninjalab.io",
        "direct_ats_type": "custom",
        "tags": ["hardware_security", "side_channel", "cryptology", "cryptanalysis"],
        "open_to_international": True
    },
    {
        "id": "oppida",
        "name": "Oppida",
        "category": "hardware_crypto_cesti",
        "website": "https://www.oppida.fr",
        "career_url": "https://www.oppida.fr/rejoignez-nous/",
        "direct_ats_type": "custom",
        "tags": ["cesti", "crypto_evaluation", "audit", "security_evaluation"],
        "open_to_international": True
    },
    {
        "id": "stmicroelectronics-fr",
        "name": "STMicroelectronics (France - Rousset, Grenoble)",
        "category": "hardware_crypto_cesti",
        "website": "https://www.st.com",
        "career_url": "https://stcareers.st.com",
        "direct_ats_type": "custom",
        "tags": ["hardware_crypto", "secure_mcu", "cryptographic_accelerators", "side_channel", "embedded"],
        "open_to_international": True
    },
    {
        "id": "nxp-fr",
        "name": "NXP Semiconductors (France - Caen, Sophia Antipolis)",
        "category": "hardware_crypto_cesti",
        "website": "https://www.nxp.com",
        "career_url": "https://www.nxp.com/company/about-nxp/careers:CAREERS",
        "direct_ats_type": "workday",
        "workday_tenant": "nxp",
        "tags": ["hardware_crypto", "nfc", "automotive_security", "embedded_crypto"],
        "open_to_international": True
    },
    {
        "id": "idemia",
        "name": "Idemia",
        "category": "hardware_crypto_cesti",
        "website": "https://www.idemia.com",
        "career_url": "https://careers.idemia.com",
        "direct_ats_type": "smartrecruiters",
        "ats_company_id": "Idemia",
        "tags": ["cryptology", "secure_elements", "biometrics", "embedded_security"],
        "open_to_international": True
    },

    # =========================================================================
    # 2. ADVANCED CRYPTOLOGY & R&D LABS
    # =========================================================================
    {
        "id": "cryptoexperts",
        "name": "CryptoExperts",
        "category": "cryptology_rd",
        "website": "https://www.cryptoexperts.com",
        "career_url": "https://www.cryptoexperts.com/careers/",
        "direct_ats_type": "custom",
        "tags": ["cryptology", "post_quantum", "white_box", "side_channel", "cryptanalysis"],
        "open_to_international": True
    },
    {
        "id": "quarkslab",
        "name": "Quarkslab",
        "category": "cryptology_rd",
        "website": "https://quarkslab.com",
        "career_url": "https://quarkslab.com/careers/",
        "direct_ats_type": "custom",
        "tags": ["cryptology", "reverse_engineering", "vulnerability_research", "binary_analysis", "obfuscation"],
        "open_to_international": True
    },
    {
        "id": "zama",
        "name": "Zama (FHE & Cryptography)",
        "category": "cryptology_rd",
        "website": "https://www.zama.ai",
        "career_url": "https://jobs.zama.org",
        "direct_ats_type": "zama",
        "tags": ["fhe", "homomorphic_encryption", "cryptology", "privacy_preserving", "applied_crypto"],
        "open_to_international": True
    },
    {
        "id": "cosmian",
        "name": "Cosmian",
        "category": "cryptology_rd",
        "website": "https://cosmian.com",
        "career_url": "https://cosmian.com/careers/",
        "direct_ats_type": "wttj",
        "ats_company_id": "cosmian",
        "tags": ["cryptology", "confidential_computing", "zero_knowledge", "fhe", "secure_mpc"],
        "open_to_international": True
    },
    {
        "id": "ledger",
        "name": "Ledger (Donjon & Security)",
        "category": "cryptology_rd",
        "website": "https://www.ledger.com",
        "career_url": "https://jobs.lever.co/ledger",
        "direct_ats_type": "lever",
        "ats_company_id": "ledger",
        "tags": ["embedded_security", "hardware_wallet", "cryptology", "reverse_engineering", "side_channel", "appsec"],
        "open_to_international": True
    },
    {
        "id": "inria-crypto",
        "name": "Inria (Equipes Crypto & Sécurité: COSMIQ, CASCADE, PRIVATICS)",
        "category": "cryptology_rd",
        "website": "https://www.inria.fr",
        "career_url": "https://jobs.inria.fr/public/classic/fr/offres-emploi",
        "direct_ats_type": "custom",
        "tags": ["cryptology", "post_quantum", "cryptanalysis", "privacy", "formal_verification"],
        "open_to_international": True
    },
    {
        "id": "cea-list-leti",
        "name": "CEA (CEA-List & CEA-Leti - Sécurité & Crypto)",
        "category": "cryptology_rd",
        "website": "https://www.cea.fr",
        "career_url": "https://emploi.cea.fr",
        "direct_ats_type": "custom",
        "tags": ["cryptology", "hardware_security", "embedded", "post_quantum", "formal_methods"],
        "open_to_international": True
    },
    {
        "id": "moabi",
        "name": "Moabi",
        "category": "cryptology_rd",
        "website": "https://moabi.com",
        "career_url": "https://moabi.com/careers",
        "direct_ats_type": "wttj",
        "ats_company_id": "moabi",
        "tags": ["binary_analysis", "firmware_security", "software_supply_chain", "reverse_engineering"],
        "open_to_international": True
    },

    # =========================================================================
    # 3. PURE-PLAY CYBERSECURITY EDITORS & ELITE BOUTIQUES
    # =========================================================================
    {
        "id": "synacktiv",
        "name": "Synacktiv",
        "category": "pure_play_cyber",
        "website": "https://www.synacktiv.com",
        "career_url": "https://www.synacktiv.com/carrieres",
        "direct_ats_type": "custom",
        "tags": ["offensive", "pentest", "reverse_engineering", "exploit_dev", "cesti", "red_team"],
        "open_to_international": True
    },
    {
        "id": "stormshield",
        "name": "Stormshield (Airbus Defence & Space)",
        "category": "pure_play_cyber",
        "website": "https://www.stormshield.com",
        "career_url": "https://careers.stormshield.eu",
        "direct_ats_type": "teamtailor",
        "teamtailor_feed_url": "https://careers.stormshield.eu/jobs.json",
        "tags": ["network_security", "firewall", "endpoint", "c_cpp", "industrial_security", "embedded"],
        "open_to_international": True
    },
    {
        "id": "sekoia",
        "name": "Sekoia.io (SOC & XDR)",
        "category": "pure_play_cyber",
        "website": "https://www.sekoia.io",
        "career_url": "https://careers.sekoia.com",
        "direct_ats_type": "teamtailor",
        "teamtailor_feed_url": "https://careers.sekoia.com/jobs.json",
        "tags": ["xdr", "cti", "soc", "threat_intelligence", "detection_engineering"],
        "open_to_international": True
    },
    {
        "id": "gatewatcher",
        "name": "Gatewatcher",
        "category": "pure_play_cyber",
        "website": "https://www.gatewatcher.com",
        "career_url": "https://www.gatewatcher.com/carrieres/",
        "direct_ats_type": "wttj",
        "ats_company_id": "gatewatcher",
        "tags": ["ndr", "network_security", "cti", "malware_analysis", "c_cpp"],
        "open_to_international": True
    },
    {
        "id": "tehtris",
        "name": "TEHTRIS",
        "category": "pure_play_cyber",
        "website": "https://tehtris.com",
        "career_url": "https://tehtris.com/fr/carrieres/",
        "direct_ats_type": "wttj",
        "ats_company_id": "tehtris",
        "tags": ["edr", "xdr", "soc", "malware_detection", "defensive"],
        "open_to_international": True
    },
    {
        "id": "harfanglab",
        "name": "HarfangLab",
        "category": "pure_play_cyber",
        "website": "https://harfanglab.io",
        "career_url": "https://harfanglab.io/carrieres/",
        "direct_ats_type": "wttj",
        "ats_company_id": "harfanglab",
        "tags": ["edr", "endpoint_security", "kernel", "rust", "c_cpp", "reverse_engineering"],
        "open_to_international": True
    },
    {
        "id": "gitguardian",
        "name": "GitGuardian",
        "category": "pure_play_cyber",
        "website": "https://www.gitguardian.com",
        "career_url": "https://www.gitguardian.com/careers",
        "direct_ats_type": "greenhouse",
        "ats_company_id": "gitguardian",
        "tags": ["appsec", "secrets_detection", "cloud_security", "devsecops"],
        "open_to_international": True
    },
    {
        "id": "yeswehack",
        "name": "YesWeHack",
        "category": "pure_play_cyber",
        "website": "https://www.yeswehack.com",
        "career_url": "https://www.yeswehack.com/careers",
        "direct_ats_type": "wttj",
        "ats_company_id": "yeswehack",
        "tags": ["bug_bounty", "vulnerability_management", "offensive", "web_security"],
        "open_to_international": True
    },
    {
        "id": "yogosha",
        "name": "Yogosha",
        "category": "pure_play_cyber",
        "website": "https://yogosha.com",
        "career_url": "https://yogosha.com/careers/",
        "direct_ats_type": "wttj",
        "ats_company_id": "yogosha",
        "tags": ["bug_bounty", "pentest_as_a_service", "offensive"],
        "open_to_international": True
    },
    {
        "id": "patrowl",
        "name": "Patrowl",
        "category": "pure_play_cyber",
        "website": "https://patrowl.com",
        "career_url": "https://patrowl.com/careers/",
        "direct_ats_type": "wttj",
        "ats_company_id": "patrowl",
        "tags": ["attack_surface_management", "asm", "threat_exposure", "offensive"],
        "open_to_international": True
    },
    {
        "id": "chapsvision",
        "name": "ChapsVision Cyber & OSINT",
        "category": "pure_play_cyber",
        "website": "https://www.chapsvision.fr",
        "career_url": "https://www.chapsvision.fr/carrieres/",
        "direct_ats_type": "wttj",
        "ats_company_id": "chapsvision",
        "tags": ["osint", "cti", "data_investigation", "cyber_intelligence"],
        "open_to_international": True
    },
    {
        "id": "wallix",
        "name": "WALLIX",
        "category": "pure_play_cyber",
        "website": "https://www.wallix.com",
        "career_url": "https://www.wallix.com/fr/carrieres/",
        "direct_ats_type": "wttj",
        "ats_company_id": "wallix",
        "tags": ["pam", "privileged_access", "identity_security", "zero_trust"],
        "open_to_international": True
    },
    {
        "id": "amossys",
        "name": "Amossys (Rennes)",
        "category": "pure_play_cyber",
        "website": "https://www.amossys.fr",
        "career_url": "https://www.amossys.fr/recrutement/",
        "direct_ats_type": "custom",
        "tags": ["cesti", "pentest", "audit", "cert", "rennes"],
        "open_to_international": True
    },
    {
        "id": "lexfo",
        "name": "Lexfo",
        "category": "pure_play_cyber",
        "website": "https://www.lexfo.fr",
        "career_url": "https://www.lexfo.fr/recrutement/",
        "direct_ats_type": "custom",
        "tags": ["offensive", "red_team", "reverse_engineering", "audit"],
        "open_to_international": True
    },
    {
        "id": "xmco",
        "name": "XMCO",
        "category": "pure_play_cyber",
        "website": "https://www.xmco.fr",
        "career_url": "https://www.xmco.fr/rejoignez-nous/",
        "direct_ats_type": "recruitee",
        "recruitee_slug": "xmco",
        "tags": ["pentest", "cti", "soc", "audit"],
        "open_to_international": True
    },
    {
        "id": "intrinsec",
        "name": "Intrinsec",
        "category": "pure_play_cyber",
        "website": "https://www.intrinsec.com",
        "career_url": "https://www.intrinsec.com/carrieres/",
        "direct_ats_type": "custom",
        "tags": ["soc", "cert", "incident_response", "pentest"],
        "open_to_international": True
    },
    {
        "id": "itracing",
        "name": "I-Tracing",
        "category": "pure_play_cyber",
        "website": "https://www.i-tracing.com",
        "career_url": "https://www.i-tracing.com/carrieres/",
        "direct_ats_type": "wttj",
        "ats_company_id": "i-tracing",
        "tags": ["soc", "cert", "cloud_security", "grc", "identity"],
        "open_to_international": True
    },

    # =========================================================================
    # 4. AEROSPACE, DEFENSE & INDUSTRIAL LEADERS
    # =========================================================================
    {
        "id": "thales-group",
        "name": "Thales (Cyber Solutions, Thales DIS, SIX GTS)",
        "category": "defense_industry",
        "website": "https://www.thalesgroup.com",
        "career_url": "https://thales.wd3.myworkdayjobs.com/fr-FR/Careers",
        "direct_ats_type": "workday",
        "workday_tenant": "thales",
        "tags": ["cryptology", "hardware_security", "soc", "incident_response", "critical_systems", "post_quantum"],
        "open_to_international": True
    },
    {
        "id": "airbus-cyber",
        "name": "Airbus Protect (Cybersécurité & Sûreté de Fonctionnement)",
        "category": "defense_industry",
        "website": "https://www.protect.airbus.com",
        "career_url": "https://www.protect.airbus.com/careers/job-offers/",
        "direct_ats_type": "workday",
        "workday_tenant": "ag",
        "hiring_companies": [
            "f5811cef9cb50166ff1fba124e0a295c",
            "f5811cef9cb501eb3bf4e0124e0add5c",
            "f5811cef9cb5013b35f9bb124e0a335c"
        ],
        "tags": ["cybersecurity", "soc", "dfir", "industrial_security", "cloud_security", "safety"],
        "open_to_international": True
    },
    {
        "id": "safran-talents",
        "name": "Safran (Electronics & Defense - Cyber)",
        "category": "defense_industry",
        "website": "https://www.safran-group.com",
        "career_url": "https://www.safran-group.com/fr/talents/nos-offres",
        "direct_ats_type": "custom",
        "tags": ["embedded_security", "avionics", "cryptology", "cybersecurity"],
        "open_to_international": True
    },
    {
        "id": "naval-group",
        "name": "Naval Group (Cybersécurité Navale)",
        "category": "defense_industry",
        "website": "https://www.naval-group.com",
        "career_url": "https://www.naval-group.com/fr/rejoignez-nous",
        "direct_ats_type": "custom",
        "tags": ["maritime_cyber", "industrial_ot", "embedded_security", "defense"],
        "open_to_international": True
    },
    {
        "id": "dassault-systemes",
        "name": "Dassault Systèmes (3DS Security)",
        "category": "defense_industry",
        "website": "https://www.3ds.com",
        "career_url": "https://careers.3ds.com",
        "direct_ats_type": "smartrecruiters",
        "ats_company_id": "DassaultSystemes",
        "tags": ["cloud_security", "appsec", "cryptology", "security_architecture"],
        "open_to_international": True
    },
    {
        "id": "schneider-electric-fr",
        "name": "Schneider Electric (Global Cyber / OT Security France)",
        "category": "defense_industry",
        "website": "https://www.se.com",
        "career_url": "https://careers.se.com/fr/fr",
        "direct_ats_type": "custom",
        "tags": ["ot_security", "ics_scada", "product_security", "firmware"],
        "open_to_international": True
    },
    {
        "id": "alstom-cyber",
        "name": "Alstom (Rail Cybersecurity)",
        "category": "defense_industry",
        "website": "https://www.alstom.com",
        "career_url": "https://jobsearch.alstom.com",
        "direct_ats_type": "custom",
        "tags": ["rail_cybersecurity", "embedded_security", "ot_security"],
        "open_to_international": True
    },

    # =========================================================================
    # 5. CYBER CONSULTING FIRMS & LEADING MSSPS (High M2/PFE hiring volume)
    # =========================================================================
    {
        "id": "orange-cyberdefense",
        "name": "Orange Cyberdefense",
        "category": "consulting_mssp",
        "website": "https://orangecyberdefense.com",
        "career_url": "https://orange.jobs/jobs/search.do?lang=fr&keyword=cyberdefense",
        "direct_ats_type": "custom",
        "tags": ["soc", "dfir", "pentest", "cert", "cloud_security", "grc", "cti"],
        "open_to_international": True
    },
    {
        "id": "wavestone",
        "name": "Wavestone (Cybersecurity & Digital Trust)",
        "category": "consulting_mssp",
        "website": "https://www.wavestone.com",
        "career_url": "https://www.wavestone.com/fr/carrieres/",
        "direct_ats_type": "smartrecruiters",
        "ats_company_id": "Wavestone",
        "tags": ["grc", "iso27001", "crisis_management", "cyber_strategy", "cloud_security"],
        "open_to_international": True
    },
    {
        "id": "advens",
        "name": "Advens (Pure-player Cybersécurité)",
        "category": "consulting_mssp",
        "website": "https://www.advens.fr",
        "career_url": "https://www.advens.fr/rejoignez-nous/",
        "direct_ats_type": "wttj",
        "ats_company_id": "advens",
        "tags": ["soc", "cert", "audit", "pentest", "grc", "cloud_security"],
        "open_to_international": True
    },
    {
        "id": "sopra-steria-cyber",
        "name": "Sopra Steria (Cybersecurity Practice)",
        "category": "consulting_mssp",
        "website": "https://www.soprasteria.com",
        "career_url": "https://www.soprasteria.com/fr/carrieres/nos-offres",
        "direct_ats_type": "custom",
        "tags": ["soc", "cloud_security", "grc", "iam", "devsecops"],
        "open_to_international": True
    },
    {
        "id": "capgemini-sogeti-cyber",
        "name": "Capgemini / Sogeti Cybersecurity",
        "category": "consulting_mssp",
        "website": "https://www.capgemini.com",
        "career_url": "https://www.capgemini.com/fr-fr/carrieres/rechercher-des-offres-d-emploi/",
        "direct_ats_type": "custom",
        "tags": ["soc", "incident_response", "pentest", "iam", "cloud_security"],
        "open_to_international": True
    },
    {
        "id": "eviden-atos-cyber",
        "name": "Eviden (Atos Big Data & Security - Crypto & Cyber)",
        "category": "consulting_mssp",
        "website": "https://eviden.com",
        "career_url": "https://eviden.com/careers/",
        "direct_ats_type": "custom",
        "tags": ["hsm", "post_quantum", "cryptology", "soc", "hardware_security", "iam"],
        "open_to_international": True
    },
    {
        "id": "devoteam-cyber-trust",
        "name": "Devoteam Cyber Trust",
        "category": "consulting_mssp",
        "website": "https://france.devoteam.com",
        "career_url": "https://france.devoteam.com/carrieres/",
        "direct_ats_type": "smartrecruiters",
        "ats_company_id": "Devoteam",
        "tags": ["cloud_security", "grc", "audit", "pentest", "iam"],
        "open_to_international": True
    },
    {
        "id": "accenture-security-fr",
        "name": "Accenture Security France",
        "category": "consulting_mssp",
        "website": "https://www.accenture.com/fr-fr",
        "career_url": "https://www.accenture.com/fr-fr/careers/jobsearch",
        "direct_ats_type": "custom",
        "tags": ["soc", "managed_security", "incident_response", "cloud_security"],
        "open_to_international": True
    },
    {
        "id": "deloitte-cyber-fr",
        "name": "Deloitte France (Cyber Risk Services)",
        "category": "consulting_mssp",
        "website": "https://www.deloitte.com/fr",
        "career_url": "https://recrute.deloitte.fr",
        "direct_ats_type": "custom",
        "tags": ["audit", "grc", "pentest", "crisis_management", "red_team"],
        "open_to_international": True
    },
    {
        "id": "pwc-cyber-fr",
        "name": "PwC France (Cybersecurity & Privacy)",
        "category": "consulting_mssp",
        "website": "https://carrieres.pwc.fr",
        "career_url": "https://carrieres.pwc.fr/fr/offres-emploi.html",
        "direct_ats_type": "custom",
        "tags": ["grc", "pentest", "dfir", "privacy", "threat_intelligence"],
        "open_to_international": True
    },
    {
        "id": "ey-cyber-fr",
        "name": "EY France (Cybersecurity Consulting)",
        "category": "consulting_mssp",
        "website": "https://www.ey.com/fr_fr",
        "career_url": "https://careers.ey.com",
        "direct_ats_type": "custom",
        "tags": ["grc", "iam", "cloud_security", "crisis_management"],
        "open_to_international": True
    },
    {
        "id": "kpmg-cyber-fr",
        "name": "KPMG France (Cyber & Privacy)",
        "category": "consulting_mssp",
        "website": "https://kpmg.com/fr",
        "career_url": "https://kpmg.com/fr/fr/home/carrieres.html",
        "direct_ats_type": "custom",
        "tags": ["audit", "grc", "compliance", "cyber_strategy"],
        "open_to_international": True
    },
    {
        "id": "niji-cyber",
        "name": "Niji (Cybersécurité)",
        "category": "consulting_mssp",
        "website": "https://www.niji.fr",
        "career_url": "https://www.niji.fr/carrieres/",
        "direct_ats_type": "custom",
        "tags": ["consulting", "rennes", "paris", "audit", "iam"],
        "open_to_international": True
    },

    # =========================================================================
    # 6. CRITICAL OPERATORS (OIV) & BANKING CERTS
    # =========================================================================
    {
        "id": "bnp-paribas-cyber",
        "name": "BNP Paribas (CERT-BNP & Group Cybersecurity)",
        "category": "banking_oiv",
        "website": "https://group.bnpparibas",
        "career_url": "https://group.bnpparibas/emploi-carriere/toutes-offres-emploi",
        "direct_ats_type": "custom",
        "tags": ["cert", "soc", "dfir", "bank_security", "cloud_security", "appsec"],
        "open_to_international": True
    },
    {
        "id": "societe-generale-cert",
        "name": "Société Générale (CERT-SG & Cyberdéfense)",
        "category": "banking_oiv",
        "website": "https://careers.societegenerale.com",
        "career_url": "https://careers.societegenerale.com/nos-offres",
        "direct_ats_type": "custom",
        "tags": ["cert", "soc", "incident_response", "threat_intel", "pentest"],
        "open_to_international": True
    },
    {
        "id": "credit-agricole-cyber",
        "name": "Crédit Agricole (CACIB / CACEIS / CAGIP Cyber)",
        "category": "banking_oiv",
        "website": "https://www.credit-agricole.com",
        "career_url": "https://www.groupecreditagricole.jobs",
        "direct_ats_type": "custom",
        "tags": ["bank_security", "cert", "soc", "iam", "cloud_security"],
        "open_to_international": True
    },
    {
        "id": "bpce-cyber",
        "name": "Groupe BPCE / Natixis (Cybersecurité)",
        "category": "banking_oiv",
        "website": "https://recrutement.bpce.fr",
        "career_url": "https://recrutement.bpce.fr/nos-offres/",
        "direct_ats_type": "custom",
        "tags": ["bank_security", "soc", "cert", "cloud_security"],
        "open_to_international": True
    },
    {
        "id": "edf-cert",
        "name": "EDF (CERT-EDF & Cybersécurité Industrielle)",
        "category": "banking_oiv",
        "website": "https://www.edf.fr",
        "career_url": "https://www.edf.fr/edf-recrute/rejoignez-nous/nos-offres",
        "direct_ats_type": "custom",
        "tags": ["cert", "ot_security", "critical_infrastructure", "incident_response"],
        "open_to_international": True
    },
    {
        "id": "totalenergies-cyber",
        "name": "TotalEnergies (Global Cyber & CERT-Total)",
        "category": "banking_oiv",
        "website": "https://totalenergies.com",
        "career_url": "https://totalenergies.avature.net/fr_FR/careers",
        "direct_ats_type": "custom",
        "tags": ["cert", "ot_security", "cloud_security", "global_soc"],
        "open_to_international": True
    },
    {
        "id": "sncf-cyber",
        "name": "SNCF (Cybersécurité Ferroviaire & Groupe)",
        "category": "banking_oiv",
        "website": "https://www.emploi.sncf.com",
        "career_url": "https://www.emploi.sncf.com/nos-offres-d-emploi",
        "direct_ats_type": "custom",
        "tags": ["rail_cyber", "soc", "cert", "grc"],
        "open_to_international": True
    },
    {
        "id": "docaposte-cyber",
        "name": "Docaposte / La Poste (Confiance Numérique)",
        "category": "banking_oiv",
        "website": "https://www.docaposte.com",
        "career_url": "https://www.docaposte.com/nous-rejoindre/nos-offres",
        "direct_ats_type": "wttj",
        "ats_company_id": "docaposte",
        "tags": ["digital_trust", "pki", "cryptology", "identity", "cloud_security"],
        "open_to_international": True
    },

    # =========================================================================
    # 7. NEW ADDITIONS (2026 expansion)
    # =========================================================================
    {
        "id": "crowdsec",
        "name": "CrowdSec",
        "category": "pure_play_cyber",
        "website": "https://www.crowdsec.net",
        "career_url": "https://crowdsec.recruitee.com",
        "direct_ats_type": "recruitee",
        "recruitee_slug": "crowdsec",
        "tags": ["ids_ips", "open_source", "threat_intelligence", "network_security"],
        "open_to_international": True
    },
    {
        "id": "synetis",
        "name": "Synetis",
        "category": "pure_play_cyber",
        "website": "https://www.synetis.com",
        "career_url": "https://www.welcometothejungle.com/fr/companies/synetis/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "synetis",
        "tags": ["pentest", "audit", "passi", "consulting", "microsoft_security"],
        "open_to_international": True
    },
    {
        "id": "almond",
        "name": "Almond (ex-Provadys)",
        "category": "pure_play_cyber",
        "website": "https://www.almond.eu",
        "career_url": "https://www.welcometothejungle.com/fr/companies/almond/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "almond",
        "tags": ["pentest", "audit", "passi", "grc", "soc"],
        "open_to_international": True
    },
    {
        "id": "formind",
        "name": "Formind",
        "category": "consulting_mssp",
        "website": "https://www.formind.fr",
        "career_url": "https://www.welcometothejungle.com/fr/companies/formind/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "formind",
        "tags": ["consulting", "soc", "incident_response", "grc"],
        "open_to_international": True
    },
    {
        "id": "akerva",
        "name": "Akerva (Rennes)",
        "category": "pure_play_cyber",
        "website": "https://www.akerva.com",
        "career_url": "https://www.akerva.com/recrutement/",
        "direct_ats_type": "custom",
        "tags": ["pentest", "audit", "passi", "rennes"],
        "open_to_international": True
    },
    {
        "id": "vaadata",
        "name": "Vaadata",
        "category": "pure_play_cyber",
        "website": "https://www.vaadata.com",
        "career_url": "https://www.vaadata.com/recrutement/",
        "direct_ats_type": "custom",
        "tags": ["pentest", "web_security", "mobile_security", "api_security"],
        "open_to_international": True
    },
    {
        "id": "algosecure",
        "name": "AlgoSecure (Lyon)",
        "category": "pure_play_cyber",
        "website": "https://www.algosecure.fr",
        "career_url": "https://www.algosecure.fr/recrutement",
        "direct_ats_type": "custom",
        "tags": ["pentest", "audit", "lyon", "red_team"],
        "open_to_international": True
    },
    {
        "id": "digitemis",
        "name": "Digitemis (Nantes)",
        "category": "pure_play_cyber",
        "website": "https://www.digitemis.com",
        "career_url": "https://www.digitemis.com/recrutement/",
        "direct_ats_type": "custom",
        "tags": ["pentest", "audit", "dpo", "nantes"],
        "open_to_international": True
    },
    {
        "id": "cybelangel",
        "name": "CybelAngel",
        "category": "pure_play_cyber",
        "website": "https://cybelangel.com",
        "career_url": "https://www.welcometothejungle.com/fr/companies/cybelangel/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "cybelangel",
        "tags": ["digital_risk", "osint", "threat_intelligence", "data_leak"],
        "open_to_international": True
    },
    {
        "id": "glimps",
        "name": "Glimps (Rennes)",
        "category": "pure_play_cyber",
        "website": "https://www.glimps.re",
        "career_url": "https://www.welcometothejungle.com/fr/companies/glimps/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "glimps",
        "tags": ["malware_analysis", "ai_detection", "reverse_engineering", "rennes"],
        "open_to_international": True
    },
    {
        "id": "hackuity",
        "name": "Hackuity",
        "category": "pure_play_cyber",
        "website": "https://www.hackuity.io",
        "career_url": "https://www.welcometothejungle.com/fr/companies/hackuity/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "hackuity",
        "tags": ["vulnerability_management", "risk_scoring", "devsecops"],
        "open_to_international": True
    },
    {
        "id": "thegreenbow",
        "name": "TheGreenBow",
        "category": "cryptology_rd",
        "website": "https://thegreenbow.com",
        "career_url": "https://thegreenbow.com/fr/a-propos/recrutement/",
        "direct_ats_type": "custom",
        "tags": ["vpn", "ipsec", "cryptology", "network_security", "post_quantum"],
        "open_to_international": True
    },
    {
        "id": "holiseum",
        "name": "Holiseum",
        "category": "consulting_mssp",
        "website": "https://www.holiseum.com",
        "career_url": "https://www.welcometothejungle.com/fr/companies/holiseum/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "holiseum",
        "tags": ["ot_security", "industrial_cyber", "ics_scada", "consulting"],
        "open_to_international": True
    },
    {
        "id": "citalid",
        "name": "Citalid",
        "category": "pure_play_cyber",
        "website": "https://citalid.com",
        "career_url": "https://www.welcometothejungle.com/fr/companies/citalid/jobs",
        "direct_ats_type": "wttj",
        "ats_company_id": "citalid",
        "tags": ["cyber_risk", "risk_quantification", "cti"],
        "open_to_international": True
    },
    {
        "id": "pradeo",
        "name": "Pradeo (Montpellier)",
        "category": "pure_play_cyber",
        "website": "https://www.pradeo.com",
        "career_url": "https://www.pradeo.com/fr/carrieres",
        "direct_ats_type": "custom",
        "tags": ["mobile_security", "app_security", "montpellier"],
        "open_to_international": True
    },
    {
        "id": "mbda-defense",
        "name": "MBDA (Systèmes de Défense)",
        "category": "defense_industry",
        "website": "https://www.mbda-systems.com",
        "career_url": "https://www.mbda-careers.com",
        "direct_ats_type": "custom",
        "tags": ["defense", "embedded_security", "cryptology", "critical_systems"],
        "open_to_international": True
    }
]

# Quick lookup helper by company ID
COMPANIES_BY_ID = {c["id"]: c for c in COMPANIES}
