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
    r"\bprojet de fin d['’]?[eé]tudes?\b",
    r"\bfin d['’]?[eé]tudes?\b",
    r"\bm2\b",
    r"\bmaster\s*2\b",
    r"\bbac\s*\+\s*5\b",
    r"\bderni[eè]re ann[eé]e\b",
    r"\b[eé]l[eè]ve\s+ing[eé]nieur\b",
    r"\bstage\s+de\s+6\s+mois\b",
    r"\b6\s+mois\b"
]

INTERNSHIP_EXCLUDE_PATTERNS = [
    r"\bcdi\b",
    r"\bcdd\b",
    r"\balternance\b",
    r"\bapprentissage\b",
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
    r"\bcryptolog\w*",
    r"\bcryptograph\w*",
    r"\bcryptanalys\w*",
    r"\bpost-?quantum\b",
    r"\bpqc\b",
    r"\blattice-?based\b",
    r"\bside-?channel\b",
    r"\bcanal\s+auxiliaire\b",
    r"\bcanaux\s+cach[eé]s\b",
    r"\bfault\s+injection\b",
    r"\binjection\s+de\s+fautes?\b",
    r"\bsmart\s*card\b",
    r"\bcarte\s+[aà]\s+puce\b",
    r"\bsecure\s+elements?\b",
    r"\bhardware\s+crypto\w*",
    r"\bwhite-?box\b",
    r"\bbo[iî]te\s+blanche\b",
    r"\bhomomorphic\b",
    r"\bhomomorphe\b",
    r"\bfhe\b",
    r"\bzero-?knowledge\b",
    r"\bzkp\b",
    r"\bsecure\s+mpc\b",
    r"\bchiffrement\b",
    r"\bencryption\b",
    r"\bpki\b",
    r"\bcoproc\w*\s+crypto\w*"
]

CYBER_OFFENSIVE_PATTERNS = [
    r"\bpentest\w*",
    r"\bintrusion\w*",
    r"\boffensive\b",
    r"\bred\s+team\b",
    r"\bvulnerabilit\w*",
    r"\bexploit\w*",
    r"\breverse\b",
    r"\br[eé]tro-?ing[eé]nierie\b",
    r"\bcesti\b",
    r"\bbug\s+bounty\b",
    r"\bghidra\b",
    r"\bida\s+pro\b",
    r"\bbinary\s+analysis\b",
    r"\bhardware\s+security\b",
    r"\bs[eé]curit[eé]\s+mat[eé]rielle\b"
]

CYBER_DEFENSIVE_PATTERNS = [
    r"\bsoc\b",
    r"\bcert\b",
    r"\bcsirt\b",
    r"\bincident\s+response\b",
    r"\br[eé]ponse\s+[aà]s?\s+incidents?\b",
    r"\bdfir\b",
    r"\bforensics?\b",
    r"\bthreat\s+intelligence\b",
    r"\bcti\b",
    r"\bdetection\s+engineering\b",
    r"\bedr\b",
    r"\bxdr\b",
    r"\bndr\b",
    r"\bsiem\b",
    r"\bmalware\b"
]

CYBER_ARCHITECTURE_GRC_PATTERNS = [
    r"\bdevsecops\b",
    r"\bcloud\s+security\b",
    r"\bappsec\b",
    r"\biam\b",
    r"\bpam\b",
    r"\bgrc\b",
    r"\biso\s*27001\b",
    r"\bebios\b",
    r"\bnis\s*2\b",
    r"\bot\s+security\b",
    r"\bics\b",
    r"\bscada\b"
]

# =============================================================================
# 3. NATIONALITY & SECURITY CLEARANCE EXCLUSION (Algerian / Non-EU Eligibility)
# =============================================================================

FRENCH_NATIONALITY_EXCLUSIVE_PATTERNS = [
    r"nationalit[eé]\s+fran[cç]aise\s+(obligatoire|requise|imp[eé]rative|exclusive)",
    r"ressortissant\s+fran[cç]ais\s+(uniquement|obligatoire|requis)",
    r"de\s+nationalit[eé]\s+fran[cç]aise\s+uniquement",
    r"r[eé]serv[eé]\s+aux\s+citoyens?\s+fran[cç]ais",
    r"habilitation\s+secret\s+d[eé]fense.*nationalit[eé]\s+fran[cç]aise",
    r"citoyennet[eé]\s+fran[cç]aise\s+(requise|obligatoire)",
    r"exclusivement\s+ouvert\s+aux\s+ressortissants\s+fran[cç]ais",
    r"uniquement\s+aux\s+ressortissants\s+de\s+l['’]union\s+europ[eé]enne",
    r"r[eé]serv[eé]\s+aux\s+ressortissants\s+ue\b"
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

    # Check negative exclude patterns
    for ex in INTERNSHIP_EXCLUDE_PATTERNS:
        if re.search(ex, title_lower):
            return False

    return True


def categorize_job(title: str, description: str = "") -> Dict[str, Any]:
    """
    Categorizes the domain: Cryptology, Cyber Offensive, Cyber Defensive, GRC/DevSecOps.
    """
    text = f"{title} {description}".lower()

    is_crypto = any(re.search(pat, text, re.IGNORECASE) for pat in CRYPTO_PATTERNS)
    is_offensive = any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_OFFENSIVE_PATTERNS)
    is_defensive = any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_DEFENSIVE_PATTERNS)
    is_arch_grc = any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_ARCHITECTURE_GRC_PATTERNS)

    categories = []
    if is_crypto:
        categories.append("Cryptology")
    if is_offensive:
        categories.append("Cyber Offensive / Hardware / Pentest")
    if is_defensive:
        categories.append("Cyber Defensive / SOC / DFIR")
    if is_arch_grc:
        categories.append("Cloud / GRC / DevSecOps")

    # If general cybersecurity
    if not categories and ("cyber" in text or "s[eé]curit[eé]" in text or "security" in text):
        categories.append("Cybersecurity (General)")

    primary = "Cryptology" if is_crypto else (categories[0] if categories else "Cybersecurity")

    return {
        "is_crypto": is_crypto,
        "is_cyber": len(categories) > 0 and (not is_crypto or is_offensive or is_defensive or is_arch_grc),
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
    "île-de-france", "ile-de-france", "bretagne", "occitanie", "remote", "télétravail"
]


def is_france_location(location_str: str) -> bool:
    """Checks if a location string corresponds to France or remote."""
    if not location_str:
        return True
    loc_lower = location_str.lower()
    return any(city in loc_lower for city in FRANCE_CITIES_REGIONS)

