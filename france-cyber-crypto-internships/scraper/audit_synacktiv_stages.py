import requests
import xml.etree.ElementTree as ET
import sys
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
r = requests.get("https://www.synacktiv.com/feed/joboffers.xml", headers=headers, timeout=10)
root = ET.fromstring(r.content)
items = root.findall(".//item")

print(f"Auditing all {len(items)} Synacktiv offers for active 6-month internships...\n")

active_stages = []
for it in items:
    link = it.find("link").text if it.find("link") is not None else ""
    title = it.find("title").text if it.find("title") is not None else ""
    
    try:
        resp = requests.get(link, headers=headers, timeout=8)
        if resp.status_code != 200:
            continue
        
        soup = BeautifulSoup(resp.text, "html.parser")
        main = soup.find("main") or soup.find("article") or soup
        text = main.get_text(" ", strip=True)
        text_lower = text.lower()
        
        # Check if it's an internship / stage
        is_stage = "stage" in text_lower or "stage" in title.lower() or "6 mois" in text_lower
        is_closed = "cette offre est actuellement pourvue" in text_lower or "pourvue" in text_lower
        has_cdi = "cdi" in text_lower and not is_stage
        
        if is_stage:
            status = "CLOSED" if is_closed else "OPEN (ACTIVE)"
            print(f"[{status}] {title}")
            print(f"       URL: {link}")
            print(f"       Extracted title: {soup.title.string if soup.title else title}")
            
            # Find description paragraphs
            desc_div = soup.select_one(".field--name-body, .job-description, article")
            desc = desc_div.get_text(" ", strip=True)[:300] if desc_div else text[:300]
            print(f"       Desc: {desc[:140]}...")
            print()
            
            active_stages.append({
                "title": title,
                "link": link,
                "is_closed": is_closed,
                "description": desc
            })
    except Exception as e:
        print(f"Error checking {link}: {e}")

print(f"\nTotal stages audited: {len(active_stages)}")
print(f"Actively open stages: {sum(1 for s in active_stages if not s['is_closed'])}")
