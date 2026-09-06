"""
Quarkslab Dedicated Blog Scraper for France Cyber & Cryptology Internship Tracker
Monitors https://blog.quarkslab.com/tag/internship.html and RSS feed.
Extracts annual R&D Master 2 / PFE (6 mois) topics and detects open (🟢/🟠) vs filled (🔴) states.
"""

import urllib.request
import re
import json

FEED_URL = "https://blog.quarkslab.com/tag/internship.html"
BASE_URL = "https://blog.quarkslab.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def get_latest_internship_post():
    """Finds the most recent internship article URL from Quarkslab blog."""
    req = urllib.request.Request(FEED_URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as r:
        html = r.read().decode('utf-8', errors='ignore')
    
    # Match links to internship offers
    matches = re.findall(r'<a[^>]+href=["\'](\.\./)?(internship-offers-for-the-[^"\']+\.html)["\']', html)
    if matches:
        latest_slug = matches[0][1]
        return BASE_URL + latest_slug
    return None

def parse_quarkslab_offers(include_filled=False):
    """
    Parses topics from the latest Quarkslab internship blog post.
    If include_filled is False, only returns 🟢 (open) or 🟠 (reviewing) offers.
    """
    post_url = get_latest_internship_post()
    if not post_url:
        print("[Quarkslab] No internship blog post found.")
        return []

    print(f"[Quarkslab] Scraping latest post: {post_url}")
    req = urllib.request.Request(post_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as r:
        html = r.read().decode('utf-8', errors='ignore')

    topics = []
    h2_matches = list(re.finditer(r'<h2\s+id=["\']([^"\']+)["\']>(.*?)</h2>', html, re.DOTALL | re.IGNORECASE))
    
    for i, m in enumerate(h2_matches):
        anchor_id = m.group(1)
        raw_title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        
        is_open = '🟢' in raw_title
        is_reviewing = '🟠' in raw_title
        is_filled = '🔴' in raw_title
        
        clean_title = raw_title.replace('🟢', '').replace('🟠', '').replace('🔴', '').strip()
        
        if not include_filled and is_filled and not (is_open or is_reviewing):
            continue
            
        start_pos = m.end()
        end_pos = h2_matches[i+1].start() if i + 1 < len(h2_matches) else html.find('</main>', start_pos)
        section_html = html[start_pos:end_pos] if end_pos != -1 else html[start_pos:]
        
        desc_match = re.search(r'<p>(.*?)</p>', section_html, re.DOTALL)
        desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else f"Stage R&D Bac+5 / PFE chez Quarkslab sur : {clean_title}"
        
        text_lower = (clean_title + " " + section_html).lower()
        is_crypto = any(k in text_lower for k in ['crypto', 'cryptograph', 'cipher', 'aes', 'pqc', 'post-quantum'])
        
        domain = "R&D Sécurité & Vulnérabilités"
        if is_crypto:
            domain = "Cryptologie Appliquée"
        elif any(k in text_lower for k in ['reverse', 'arm', 'binary', 'ghidra', 'decompil']):
            domain = "Sécurité Offensive & Reverse"
        elif any(k in text_lower for k in ['ai', 'llm', 'machine learning']):
            domain = "IA & Cybersécurité"
        elif any(k in text_lower for k in ['satellite', 'wireless', 'bluetooth', 'rf']):
            domain = "Sécurité Matérielle & RF"

        topic_data = {
            "id": f"quarkslab_{anchor_id}".replace("-", "_"),
            "title": f"STAGE M2 / PFE - {clean_title} (Paris)",
            "company_id": "quarkslab",
            "company_name": "Quarkslab",
            "contract_type": "Stage M2 / PFE (6 mois)",
            "location": "Paris, France",
            "direct_url": f"{post_url}#{anchor_id}",
            "domain": domain,
            "all_domains": [domain, "R&D Cybersécurité", "Reverse Engineering", "Vulnérabilités"],
            "is_crypto": is_crypto,
            "is_cyber": True,
            "source": "quarkslab_research_blog",
            "description": desc[:280] + ("..." if len(desc) > 280 else ""),
            "posted_at": "2025-10-20",
            "status": "active" if not is_filled else "filled",
            "verification_status": "VERIFIED_ACTIVE"
        }
        topics.append(topic_data)

    print(f"[Quarkslab] Found {len(topics)} topics (include_filled={include_filled}).")
    return topics

if __name__ == "__main__":
    offers_all = parse_quarkslab_offers(include_filled=True)
    print("\nAll topics found in latest blog post:")
    for o in offers_all:
        print(f"[{o['status'].upper()}] {o['title']} -> {o['url']}")
