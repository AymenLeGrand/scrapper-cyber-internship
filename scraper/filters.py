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
    r"\bbac\+5\b",
    r"\bderni[eè]re\s+ann[eé]e\b",
    r"\b[eé]l[eè]ve\s+ing[eé]nieur\b",
    r"\bstage\s+ing[eé]nieur\b",
    r"\bing[eé]nieur\s+stagiaire\b",
    r"\btrainee\b",
    r"\btraineeship\b",
    r"\bgraduation\s+internship\b",
    r"\bfinal\s+year\s+project\b",
    r"\bfinal\s+year\s+internship\b",
    r"\bdiploma\s+project\b",
    r"\bstudent\s+intern\w*\b",
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
    r"\bqkd\b",
    r"\baes\b",
    r"\brsa\b",
    r"\bsha-?[23]\b",
    r"\bchacha20\b",
    r"\bpoly1305\b",
    r"\bquantum-?safe\b",
    r"\bcrypto-?agilit\w*",
    r"\bcryptographic\s+engineering\b",
    r"\bsignature\s+num[eé]rique\b",
    r"\bdigital\s+signature\b",
    r"\bsecret\s+sharing\b",
    r"\bpartage\s+de\s+secret\b",
    r"\bverifiable\s+credentials?\b",
    r"\bzk-?proof\w*"
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
    r"\bcan\s+bus\b",
    r"\bctf\b",
    r"\bcapture\s+the\s+flag\b",
    r"\bcve\b",
    r"\bcve-20\w*",
    r"\bweb\s*sec\w*",
    r"\bwebsec\b",
    r"\bowasp\b",
    r"\btop\s*10\s*owasp\b",
    r"\binjection\s+sql\b",
    r"\bsqli\b",
    r"\bxss\b",
    r"\bcsrf\b",
    r"\bssrf\b",
    r"\brce\b",
    r"\bxxe\b",
    r"\bidor\b",
    r"\bmetasploit\b",
    r"\bburp\b",
    r"\bburp\s*suite\b",
    r"\bnmap\b",
    r"\bactive\s+directory\b",
    r"\bad\s+security\b",
    r"\bbloodhound\b",
    r"\bmimikatz\b",
    r"\bkerberos\b",
    r"\bprivilege\s+escalation\b",
    r"\b[eé]l[eé]vation\s+de\s+privil[eè]ges?\b",
    r"\bprivesc\b",
    r"\bpwn\w*",
    r"\brop\b",
    r"\bshellcode\w*",
    r"\bheap\s+exploitation\b",
    r"\bstack\s+overflow\b",
    r"\bbuffer\s+overflow\b",
    r"\bradare2\b",
    r"\br2\b",
    r"\bcutter\b",
    r"\bbinary\s+exploitation\b",
    r"\bsocial\s+engineering\b",
    r"\bing[eé]nierie\s+sociale\b",
    r"\bphishing\b",
    r"\bhame[cç]onnage\b",
    r"\bredteaming\b",
    r"\badversary\s+emulation\b",
    r"\b[eé]mulation\s+d['’]attaque\b",
    r"\bmalware\s+dev\w*",
    r"\bhardening\b",
    r"\bdurcissement\b"
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
    r"\bsupervision\s+de\s+s[eé]curit[eé]\b",
    r"\brecherche\s+de\s+menaces?\b",
    r"\breverse\s+malware\b",
    r"\banalyse\s+de\s+malware\w*",
    r"\bmalware\s+analysis\b",
    r"\bsandbox\w*",
    r"\bcuckoo\b",
    r"\bany\.run\b",
    r"\bsplunk\b",
    r"\bqradar\b",
    r"\bsentinel\b",
    r"\belastic\s+security\b",
    r"\bwazuh\b",
    r"\bcrowdstrike\b",
    r"\bdefender\s+for\s+endpoint\b",
    r"\bcarbon\s+black\b",
    r"\bvolatility\b",
    r"\bautopsy\b",
    r"\bftk\b",
    r"\bmisp\b",
    r"\bopencti\b",
    r"\bthreat\s+feed\w*",
    r"\bplaybook\w*",
    r"\brunbook\w*",
    r"\bgestion\s+de\s+crise\s+cyber\b",
    r"\bcyber\s+crisis\b",
    r"\bveille\s+(en\s+)?vuln[eé]rabilit[eé]s?\b",
    r"\bvulnerability\s+management\b"
]

CYBER_NETSEC_PATTERNS = [
    r"\bnetsec\b",
    r"\bnetwork\s+sec\w*",
    r"\bs[eé]curit[eé]\s+(des\s+)?r[eé]seaux?\b",
    r"\bs[eé]curit[eé]\s+infra\w*\b",
    r"\binfrastructure\s+security\b",
    r"\bfirewall\w*",
    r"\bpare-?feu\w*",
    r"\bvpn\b",
    r"\bipsec\b",
    r"\bwireguard\b",
    r"\bopenvpn\b",
    r"\btls\b",
    r"\bssl\b",
    r"\bssh\b",
    r"\bproxy\b",
    r"\breverse-?proxy\b",
    r"\bwaf\b",
    r"\bweb\s+application\s+firewall\b",
    r"\bnac\b",
    r"\bnetwork\s+access\s+control\b",
    r"\b802\.1x\b",
    r"\bids\b",
    r"\bips\b",
    r"\bids/ips\b",
    r"\bnids\b",
    r"\bsuricata\b",
    r"\bsnort\b",
    r"\bzeek\b",
    r"\bbro\b",
    r"\bddos\b",
    r"\banti-?ddos\b",
    r"\bd[eé]ni\s+de\s+service\b",
    r"\bwireshark\b",
    r"\btcpdump\b",
    r"\bpacket\s+analysis\b",
    r"\banalyse\s+de\s+trames?\b",
    r"\banalyse\s+flux\b",
    r"\bsegmentation\s+r[eé]seau\b",
    r"\bmicro-?segmentation\b",
    r"\bsd-?wan\b",
    r"\bsse\b",
    r"\bsase\b",
    r"\bztna\b",
    r"\bdnssec\b",
    r"\bdoh\b",
    r"\bdot\b",
    r"\bbgp\b",
    r"\brpki\b",
    r"\bswitch\s+security\b",
    r"\brouter\s+security\b",
    r"\bvlan\b",
    r"\bvxlan\b",
    r"\b5g\s+security\b",
    r"\bs[eé]curit[eé]\s+5g\b",
    r"\bt[eé]l[eé]com\w*\s+sec\w*",
    r"\bfortinet\b",
    r"\bfortigate\b",
    r"\bpalo\s*alto\b",
    r"\bpaloalto\b",
    r"\bcheckpoint\b",
    r"\bstormshield\b",
    r"\bpfsense\b",
    r"\bopnsense\b",
    r"\bbastion\w*",
    r"\bcyberark\b",
    r"\bwallix\b"
]

CYBER_ARCHITECTURE_CLOUD_DEVSECOPS_PATTERNS = [
    r"\bdevsecops\b",
    r"\bcloud\s+security\b",
    r"\bs[eé]curit[eé]\s+(du\s+)?cloud\b",
    r"\bappsec\b",
    r"\bs[eé]curit[eé]\s+applicative\b",
    r"\biam\b",
    r"\bpam\b",
    r"\bidentity\s+and\s+access\b",
    r"\bzero\s+trust\b",
    r"\bot\s+security\b",
    r"\bics\b",
    r"\bscada\b",
    r"\bci/cd\s+sec\w*",
    r"\bpipeline\s+sec\w*",
    r"\bsupply\s+chain\s+sec\w*",
    r"\bsbom\b",
    r"\bsast\b",
    r"\bdast\b",
    r"\biast\b",
    r"\bsca\b",
    r"\bsonarqube\b",
    r"\bsnyk\b",
    r"\bsemgrep\b",
    r"\bcheckmarx\b",
    r"\bkubernetes\s+sec\w*",
    r"\bk8s\s+sec\w*",
    r"\bcontainer\s+sec\w*",
    r"\bdocker\s+sec\w*",
    r"\bcspm\b",
    r"\bciem\b",
    r"\bcwpp\b",
    r"\bcnapp\b",
    r"\baws\s+sec\w*",
    r"\bazure\s+sec\w*",
    r"\bgcp\s+sec\w*",
    r"\boauth2?\b",
    r"\boidc\b",
    r"\bsaml\b",
    r"\bsso\b",
    r"\bkeycloak\b",
    r"\bentra\s+id\b",
    r"\bsecrets?\s+management\b",
    r"\bhashicorp\s+vault\b",
    r"\bssi\b",
    r"\brssi\b",
    r"\bcssi\b",
    r"\bs[eé]curit[eé]\s+des\s+syst[eè]mes\s+d['’]information\b"
]

# Backward compatibility alias
CYBER_ARCHITECTURE_GRC_PATTERNS = CYBER_ARCHITECTURE_CLOUD_DEVSECOPS_PATTERNS

CYBER_AI_PATTERNS = [
    r"\b(ia|ai)\s*(&|and|et|\+)\s*(cyber\w*|s[eé]curi\w*|security)\b",
    r"\b(cyber\w*|s[eé]curi\w*|security)\s*(&|and|et|\+)\s*(ia|ai)\b",
    r"\badversarial\s+machine\s+learning\b",
    r"\badversarial\s+ml\b",
    r"\bprompt\s+injection\b",
    r"\bjailbreak\s+llm\b",
    r"\bmachine\s+learning\s+security\b",
    r"\bs[eé]curisation\s+des?\s+(mod[eè]les?\s+d['’]?)?ia\b",
    r"\bia\s+pour\s+la\s+(d[eé]tection|cybers[eé]curit[eé]|s[eé]curit[eé])\b",
    r"\bai\s+for\s+(cybersecurity|security|detection)\b",
    r"\bai\s+security\b",
    r"\br&d\s+ia\s*(&|et|\+)?\s*cyber\w*",
    r"\bllm\s+security\b",
    r"\bgenai\s+security\b"
]

# =============================================================================
# EXCLUSIONS: NON-TECHNICAL GRC, COMPLIANCE, MARKETING & GENERIC DIGITAL/BUSINESS
# =============================================================================
EXCLUDE_NON_CYBER_PATTERNS = [
    # Pure GRC, Governance, Compliance, Legal, DPO
    r"\bgrc\b",
    r"\bgouvernance\b",
    r"\bgovernance\b",
    r"\bconformit[eé]\b",
    r"\bcompliance\b",
    r"\bsmsi\b",
    r"\brgpd\b",
    r"\bgdpr\b",
    r"\bdpo\b",
    r"\bjurid\w*",
    r"\bdroit\b",
    r"\br[eé]glementation\w*",
    
    # Generic Digital & Business & Non-cyber IT/Consulting
    r"\btransformation\s+digitale\b",
    r"\btransformation\s+num[eé]rique\b",
    r"\bstrat[eé]gie\s+digitale\b",
    r"\bstrat[eé]gie\s+num[eé]rique\b",
    r"\bdigitale?\s+transformation\b",
    r"\bbusiness\s+development\b",
    r"\bbusiness\s+developer\b",
    r"\bbizdev\b",
    r"\bmarketing\b",
    r"\bcommunication\b",
    r"\bvente\b",
    r"\bcommercial\b",
    r"\bchef\s+de\s+projet\s+digital\b",
    r"\bfinops\b",
    r"\bgreenops\b",
    r"\bgenbi\b",
    r"\brse\b",
    r"\broi\b",
    r"\bcto\s*[/&]\s*cio\b",
    r"\bcio\s+office\b",
    r"\bcto\s+office\b"
]

STRONG_TECH_CYBER_KEYWORDS = [
    r"\bcrypt\w*", r"\bpentest\w*", r"\boffensive\b", r"\bred\s*team\b",
    r"\bblue\s*team\b", r"\bforensic\w*", r"\breverse\b", r"\bmalware\b",
    r"\bsoc\b", r"\bcsirt\b", r"\bcert\b", r"\bincident\b", r"\bnetsec\b",
    r"\bfirewall\b", r"\bvpn\b", r"\bdevsecops\b", r"\bpki\b",
    r"\bhardware\s+sec\w*", r"\bembedded\s+sec\w*"
]


def is_valid_cyber_crypto_job(title: str, description: str = "") -> bool:
    """
    Checks whether a posting is strictly within technical Cybersecurity or Cryptology.
    Rejects pure non-technical GRC, compliance, legal, and generic digital/business transformation.
    """
    title_lower = title.lower()

    # Check GRC & Digital exclusions
    for pat in EXCLUDE_NON_CYBER_PATTERNS:
        if re.search(pat, title_lower):
            # Allow only if overridden by strong technical domain keywords
            if not any(re.search(tk, title_lower) for tk in STRONG_TECH_CYBER_KEYWORDS):
                return False

    # Exclude generic AI if it has no cybersecurity/security context
    has_ai = any(re.search(p, title_lower) for p in [r"\bia\b", r"\bai\b", r"\bintelligence\s+artificielle\b", r"\bgenai\b", r"\brag\b"])
    has_cyber = any(re.search(p, title_lower) for p in [
        r"\bcyber\w*", r"\bs[eé]curi\w*", r"\bsecurity\b", r"\bcrypt\w*", r"\bpassi\b",
        r"\bpentest\w*", r"\bred\s*team\b", r"\boffensive\b", r"\bsoc\b", r"\bforensic\w*",
        r"\biam\b", r"\bidentity\b", r"\baccess\s+management\b", r"\btrust\b", r"\bnetsec\b"
    ])
    if has_ai and not has_cyber:
        return False

    return True


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

    # Strict rejection of non-cyber GRC and generic digital/business postings
    if not is_valid_cyber_crypto_job(title, description):
        return False

    return True


def categorize_job(title: str, description: str = "") -> Dict[str, Any]:
    """
    Categorizes the domain: Cryptology, Cyber Offensive, Cyber Defensive, NetSec, Cloud/DevSecOps, AI.
    Title-level keyword matches take precedence for the primary domain to avoid boilerplate noise.
    """
    # Strict validation: reject non-cyber GRC and generic digital/business postings
    if not is_valid_cyber_crypto_job(title, description):
        return {
            "is_crypto": False,
            "is_cyber": False,
            "primary_domain": "Non-Cyber / Excluded",
            "all_domains": []
        }

    text = f"{title} {description}".lower()
    title_lower = title.lower()

    # Title-level detection for sharp primary domain identification
    title_crypto = any(re.search(pat, title_lower, re.IGNORECASE) for pat in CRYPTO_PATTERNS)
    title_offensive = any(re.search(pat, title_lower, re.IGNORECASE) for pat in CYBER_OFFENSIVE_PATTERNS)
    title_defensive = any(re.search(pat, title_lower, re.IGNORECASE) for pat in CYBER_DEFENSIVE_PATTERNS)
    title_netsec = any(re.search(pat, title_lower, re.IGNORECASE) for pat in CYBER_NETSEC_PATTERNS)
    title_arch_grc = any(re.search(pat, title_lower, re.IGNORECASE) for pat in CYBER_ARCHITECTURE_CLOUD_DEVSECOPS_PATTERNS)
    title_ai = any(re.search(pat, title_lower, re.IGNORECASE) for pat in CYBER_AI_PATTERNS)

    is_crypto = title_crypto or any(re.search(pat, text, re.IGNORECASE) for pat in CRYPTO_PATTERNS)
    is_offensive = title_offensive or any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_OFFENSIVE_PATTERNS)
    is_defensive = title_defensive or any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_DEFENSIVE_PATTERNS)
    is_netsec = title_netsec or any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_NETSEC_PATTERNS)
    is_arch_grc = title_arch_grc or any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_ARCHITECTURE_CLOUD_DEVSECOPS_PATTERNS)
    is_ai = title_ai or any(re.search(pat, text, re.IGNORECASE) for pat in CYBER_AI_PATTERNS)

    categories = []
    if is_crypto:
        categories.append("Cryptology")
    if is_offensive:
        categories.append("Cyber Offensive / Hardware / Pentest")
    if is_defensive:
        categories.append("Cyber Defensive / SOC / DFIR")
    if is_netsec:
        categories.append("Network Security / NetSec")
    if is_arch_grc:
        categories.append("Cloud / DevSecOps")
    if is_ai:
        categories.append("AI & Cybersecurity")

    # If general cybersecurity
    if not categories and ("cyber" in text or "s[eé]curit[eé]" in text or "security" in text or "infosec" in text or "netsec" in text or "confiance numérique" in text or "digital trust" in text):
        categories.append("Cybersecurity (General)")

    # Determine primary domain: prioritize explicit title match first
    if title_crypto or is_crypto:
        primary = "Cryptology"
    elif title_ai:
        primary = "AI & Cybersecurity"
    elif title_offensive:
        primary = "Cyber Offensive / Hardware / Pentest"
    elif title_defensive:
        primary = "Cyber Defensive / SOC / DFIR"
    elif title_netsec:
        primary = "Network Security / NetSec"
    elif title_arch_grc:
        primary = "Cloud / DevSecOps"
    else:
        primary = categories[0] if categories else "Cybersecurity"

    return {
        "is_crypto": is_crypto,
        "is_cyber": len(categories) > 0 and (not is_crypto or is_offensive or is_defensive or is_netsec or is_arch_grc or is_ai),
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

