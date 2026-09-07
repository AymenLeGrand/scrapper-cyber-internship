"""
Filtering & Categorization Engine for M2 Cyber & Cryptology Internships.
Features:
- M2 / PFE / End-of-Studies internship verification
- Strict Cryptology vs Cybersecurity domain taxonomy
- Algerian & Non-EU nationality clearance validation (skips French-only restrictions)
"""

import re
from typing import Dict, Any, Tuple, List

# =============================================================================
# 1. INTERNSHIP & M2 LEVEL PATTERNS
# =============================================================================

INTERNSHIP_POSITIVE_PATTERNS = [
    r"\bstage\b",
    r"\bstagiaire\b",
    r"\bintern\b",
    r"\binternship\b",
    r"\bpfe\b",
    r"\bsfe\b", # Stage fin d'études / Student Final Exam
    r"\bprojet\s+de\s+fin\s+d['’]?[eé]tudes?\b",
    r"\bstage\s+de\s+fin\s+d['’]?[eé]tudes?\b",
    r"\bfin\s+d['’]?[eé]tudes?\b",
    r"\bend-?of-?studies\b",
    r"\bend-?of-?study\b",
    r"\bmaster\s*thesis\b",
    r"\bm2\b",
    r"\bmaster\s*2\b",
    r"\bbac\s*\+\s*5\b",
    r"\bderni[eè]re\s+ann[eé]e\b",
    r"\b[eé]l[eè]ve\s+ing[eé]nieur\b",
    r"\bstage\s+de\s+6\s+mois\b",
    r"\b6\s+mois\b",
    r"\bpr[eé]-?embauche\b",
    r"\bc[eé]sure\b"
]

INTERNSHIP_EXCLUDE_PATTERNS = [
    r"\bcdi\b",
    r"\bcdd\b",
    r"\balternance\b",
    r"\bapprentissage\b",
    r"\bfreelance\b",
    r"\bind[eé]pendant\b",
    r"\bsenior\b",
    r"\blead\b",
    r"\bdirector\b",
    r"\bmanager\b",
    r"\bdocteur\b",
    r"\bpost-?doc\b"
]

# =============================================================================
# 2. DOMAIN & TECH TAXONOMY
# =============================================================================

CRYPTO_PATTERNS = [
    # Core cryptology & cryptanalysis
    r"\bcryptolog\w*",
    r"\bcryptograph\w*",
    r"\bcryptanalys\w*",
    r"\bchiffrement\b",
    r"\bencryption\b",
    r"\bdecryption\b",
    r"\bd[eé]chiffrement\b",
    r"\bprimitives?\s+crypto\w*",
    r"\bcryptosyst[eè]me\w*",
    r"\bcipher\w*",
    
    # Post-Quantum Cryptography (PQC & NIST Standards)
    r"\bpost-?quantum\b",
    r"\bpqc\b",
    r"\blattice-?based\b",
    r"\br[eé]seaux\s+euclidiens\b",
    r"\bkyber\b",
    r"\bml-?kem\b",
    r"\bdilithium\b",
    r"\bml-?dsa\b",
    r"\bsphincs\b",
    r"\bslh-?dsa\b",
    r"\bfalcon\b",
    r"\bisog[eé]n\w*",
    r"\bcode-?based\b",
    r"\bfips\s*20[345]\b",
    
    # Physical Security, Hardware Crypto & Side-Channel
    r"\bside-?channel\b",
    r"\bcanal\s+auxiliaire\b",
    r"\bcanaux\s+cach[eé]s\b",
    r"\bcanaux\s+auxiliaires\b",
    r"\bsca\b",
    r"\bfault\s+injection\b",
    r"\binjection\s+de\s+fautes?\b",
    r"\bfia\b",
    r"\bsmart\s*cards?\b",
    r"\bcartes?\s+[aà]\s+puces?\b",
    r"\bsecure\s+elements?\b",
    r"\bhsm\b",
    r"\bhardware\s+security\s+module\b",
    r"\btpm\b",
    r"\bhardware\s+crypto\w*",
    r"\bcryptoprocesseur\w*",
    r"\bcoproc\w*\s+crypto\w*",
    r"\bwhite-?box\b",
    r"\bbo[iî]te\s+blanche\b",
    
    # Advanced & Privacy-Preserving Cryptography
    r"\bhomomorphic\b",
    r"\bhomomorphe\b",
    r"\bfhe\b",
    r"\bzero-?knowledge\b",
    r"\bzkp\b",
    r"\bzk-?snarks?\b",
    r"\bzk-?starks?\b",
    r"\bplonk\b",
    r"\bbulletproofs?\b",
    r"\bsecure\s+mpc\b",
    r"\bmultiparty\s+computation\b",
    r"\bcalcul\s+multipartite\b",
    r"\bthreshold\s+crypto\w*",
    r"\bcryptographie\s+[aà]\s+seuil\b",
    
    # PKI, Signatures & Mathematical Foundations
    r"\bpki\b",
    r"\bigc\b",
    r"\binfrastructure\s+de\s+gestion\s+de\s+cl[eé]s?\b",
    r"\belliptic\s+curve\w*",
    r"\bcourbes?\s+elliptiques?\b",
    r"\becc\b",
    r"\bpairing\b",
    r"\bcouplages?\b",
    r"\bquantum\s+crypto\w*",
    r"\bqkd\b"
]

CYBER_OFFENSIVE_PATTERNS = [
    r"\bpentest\w*",
    r"\btest\w*\s+d['’]?intrusion\w*",
    r"\boffensive\b",
    r"\bred\s+team\w*",
    r"\bpurple\s+team\w*",
    r"\bvulnerabilit\w*",
    r"\bexploit\w*",
    r"\breverse\b",
    r"\br[eé]tro-?ing[eé]nierie\b",
    r"\breversing\b",
    r"\bcesti\b",
    r"\bbug\s+bounty\b",
    r"\bethical\s+hack\w*",
    r"\bhacking\s+[eé]thique\b",
    r"\bpiratage\s+[eé]thique\b",
    r"\bfuzzing\b",
    r"\bfuzzer\w*",
    r"\bafl\b",
    r"\blibfuzzer\b",
    r"\bghidra\b",
    r"\bida\s+pro\b",
    r"\bbinary\s+analysis\b",
    r"\banalyse\s+binaire\b",
    r"\bkernel\s+security\b",
    r"\brootkit\w*",
    r"\bjailbreak\w*",
    r"\bhardware\s+security\b",
    r"\bs[eé]curit[eé]\s+mat[eé]rielle\b",
    r"\bfirmware\b",
    r"\biot\s+security\b",
    r"\bs[eé]curit[eé]\s+iot\b",
    r"\bradiofr[eé]quence\b",
    r"\bsdr\b",
    r"\bsoftware\s+defined\s+radio\b",
    r"\bautomotive\s+security\b",
    r"\bcan\s+bus\b"
]

CYBER_DEFENSIVE_PATTERNS = [
    r"\bsoc\b",
    r"\bsecops\b",
    r"\bblue\s+team\w*",
    r"\bop[eé]rations?\s+(de\s+)?cybers?[eé]curit[eé]\b",
    r"\bmdr\b",
    r"\bmanaged\s+detection\b",
    r"\bcert\b",
    r"\bcsirt\b",
    r"\bincident\s+response\b",
    r"\br[eé]ponse\s+[aà]s?\s+incidents?\b",
    r"\bdfir\b",
    r"\bforensics?\b",
    r"\banalyse\s+forensique\b",
    r"\bthreat\s+intelligence\b",
    r"\bcti\b",
    r"\bthreat\s+hunting\b",
    r"\bchasse\s+aux\s+menaces\b",
    r"\bdetection\s+engineering\b",
    r"\bing[eé]nierie\s+de\s+d[eé]tection\b",
    r"\bedr\b",
    r"\bxdr\b",
    r"\bndr\b",
    r"\bsiem\b",
    r"\bsoar\b",
    r"\bmalware\w*",
    r"\bransomware\w*",
    r"\bran[cç]ongiciel\w*",
    r"\byara\b",
    r"\bsigma\s+rules?\b",
    r"\bmitre\s+att&?ck\b",
    r"\bioc\b",
    r"\bsurveillance\s+de\s+s[eé]curit[eé]\b",
    r"\bsupervision\s+de\s+s[eé]curit[eé]\b"
]

CYBER_ARCHITECTURE_GRC_PATTERNS = [
    r"\bdevsecops\b",
    r"\bcloud\s+security\b",
    r"\bs[eé]curit[eé]\s+(du\s+)?cloud\b",
    r"\bappsec\b",
    r"\bs[eé]curit[eé]\s+applicative\b",
    r"\biam\b",
    r"\bpam\b",
    r"\bidentity\s+and\s+access\b",
    r"\bgrc\b",
    r"\bgouvernance\b",
    r"\bconformit[eé]\b",
    r"\bcompliance\b",
    r"\brisk\s+management\b",
    r"\bgestion\s+des\s+risques?\b",
    r"\biso\s*2700[125]\b",
    r"\bebios\b",
    r"\bebios\s+rm\b",
    r"\bnis\s*2\b",
    r"\bdora\b",
    r"\bcra\b",
    r"\bcyber\s+resilience\s+act\b",
    r"\brgpd\b",
    r"\bgdpr\b",
    r"\bpci-?dss\b",
    r"\bpssi\b",
    r"\bsmsi\b",
    r"\baudit\s+(de\s+)?s[eé]curit[eé]\b",
    r"\baudit\s+ssi\b",
    r"\bzero\s+trust\b",
    r"\bot\s+security\b",
    r"\bics\b",
    r"\bscada\b"
]

CYBER_AI_PATTERNS = [
    r"\bia\s+et\s+cybers?[eé]curit[eé]\b",
    r"\bcybers?[eé]curit[eé]\s+et\s+ia\b",
    r"\bintelligence\s+artificielle\b",
    r"\bartificial\s+intelligence\b",
    r"\bllm\b",
    r"\bgenai\b",
    r"\bia\s+g[eé]n[eé]rative\b",
    r"\bgenerative\s+ai\b",
    r"\badversarial\s+machine\s+learning\b",
    r"\badversarial\s+ml\b",
    r"\bprompt\s+injection\b",
    r"\bjailbreak\s+llm\b",
    r"\bmachine\s+learning\s+security\b",
    r"\bs[eé]curisation\s+des?\s+(mod[eè]les?\s+d['’]?)?ia\b",
    r"\bia\s+pour\s+la\s+d[eé]tection\b"
]

# =============================================================================
# 3. NATIONALITY & SECURITY CLEARANCE EXCLUSION (Algerian / Non-EU Eligibility)
# =============================================================================

FRENCH_NATIONALITY_EXCLUSIVE_PATTERNS = [
    r"nationalit[eé]\s+fran[cç]aise\s+(obligatoire|requise|imp[eé]rative|exclusive|strictement)",
    r"ressortissant\s+fran[cç]ais\s+(uniquement|obligatoire|requis)",
    r"de\s+nationalit[eé]\s+fran[cç]aise\s+uniquement",
    r"r[eé]serv[eé]\s+aux\s+citoyens?\s+fran[cç]ais",
    r"habilitation\s+secret\s+d[eé]fense.*nationalit[eé]\s+fran[cç]aise",
    r"citoyennet[eé]\s+fran[cç]aise\s+(requise|obligatoire)",
    r"exclusivement\s+ouvert\s+aux\s+ressortissants\s+fran[cç]ais",
    r"uniquement\s+aux\s+ressortissants\s+de\s+l['’]union\s+europ[eé]enne",
    r"r[eé]serv[eé]\s+aux\s+ressortissants\s+ue\b",
    r"clause\s+de\s+nationalit[eé]\s+fran[cç]aise\b",
    r"tr[eè]s\s+secret\s+d[eé]fense\b"
]


def is_internship(title: str, description: str = "") -> bool:
    """
    Checks whether a posting is strictly an internship (stage / PFE / fin d'études / M2).
    Strict Zero-CDI Policy: Rejects any permanent contract (CDI) or regular job.
    """
    title_lower = title.lower()
    text = f"{title} {description}".lower()

    # Strict CDI rejection
    if re.search(r"\bcdi\b", title_lower) or "contrat à durée indéterminée" in text:
        return False

    # Must match at least one positive internship keyword
    has_stage = any(re.search(pat, text, re.IGNORECASE) for pat in INTERNSHIP_POSITIVE_PATTERNS)
    if not has_stage:
        return False

    # Check negative exclude patterns (protecting stage titles containing role names like "Assistant Manager")
    is_explicit_stage = any(re.search(p, title_lower) for p in [r"\bstage\b", r"\bstagiaire\b", r"\bintern\b", r"\bpfe\b", r"\bsfe\b"])
    for ex in INTERNSHIP_EXCLUDE_PATTERNS:
        if is_explicit_stage and ex in (r"\bsenior\b", r"\blead\b", r"\bdirector\b", r"\bmanager\b"):
            continue
        if re.search(ex, title_lower):
            return False

    return True


def categorize_job(title: str, description: str = "") -> Dict[str, Any]:
    """
    Categorizes the domain: Cryptology, Cyber Offensive, Cyber Defensive, GRC/DevSecOps, AI.
    """
    text = f"{title} {description}".lower()

    is_crypto = any(re.search(pat, text, re.IGNORECASE) for pat in CRYPTO_PATTERNS)
    is_offensive = any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_OFFENSIVE_PATTERNS)
    is_defensive = any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_DEFENSIVE_PATTERNS)
    is_arch_grc = any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_ARCHITECTURE_GRC_PATTERNS)
    is_ai = any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_AI_PATTERNS)

    categories = []
    if is_crypto:
        categories.append("Cryptology")
    if is_offensive:
        categories.append("Cyber Offensive / Hardware / Pentest")
    if is_defensive:
        categories.append("Cyber Defensive / SOC / DFIR")
    if is_arch_grc:
        categories.append("Cloud / GRC / DevSecOps")
    if is_ai:
        categories.append("AI & Cybersecurity")

    # If general cybersecurity
    if not categories and ("cyber" in text or "s[eé]curit[eé]" in text or "security" in text):
        categories.append("Cybersecurity (General)")

    primary = "Cryptology" if is_crypto else (categories[0] if categories else "Cybersecurity")

    return {
        "is_crypto": is_crypto,
        "is_cyber": len(categories) > 0 and (not is_crypto or is_offensive or is_defensive or is_arch_grc or is_ai),
        "primary_domain": primary,
        "all_domains": categories
    }


def check_algerian_national_eligibility(title: str, description: str = "") -> Tuple[bool, str]:
    """
    Validates if an offer is eligible for an Algerian / Non-EU national studying in France.
    Returns (is_eligible, reason_if_restricted).
    """
    text = f"{title} {description}".lower()

    for pat in FRENCH_NATIONALITY_EXCLUSIVE_PATTERNS:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return False, f"Restriction détectée: {match.group(0)}"

    return True, "Eligible (Aucune restriction de nationalité française détectée)"


FRANCE_CITIES_REGIONS = [
    "france", "paris", "meudon", "vélizy", "velizy", "limours", "cholet", "rennes",
    "bruz", "cesson", "brest", "bordeaux", "pessac", "toulouse", "lyon", "grenoble",
    "rousset", "sophia", "nice", "marseille", "lille", "nantes", "strasbourg",
    "montpellier", "toulon", "gennevilliers", "élancourt", "elancourt", "massy",
    "palaiseau", "saclay", "courbevoie", "issy", "montreuil", "fontenay", "châtillon",
    "île-de-france", "ile-de-france", "idf", "bretagne", "occitanie", "auvergne-rhône-alpes",
    "aura", "nouvelle-aquitaine", "hauts-de-france", "grand est", "paca", "remote", "télétravail"
]


def is_france_location(location_str: str) -> bool:
    """Checks if a location string corresponds to France or remote."""
    if not location_str:
        return True
    loc_lower = location_str.lower()
    return any(city in loc_lower for city in FRANCE_CITIES_REGIONS)

