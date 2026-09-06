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

print(f"Checking {len(items)} items from Synacktiv feed...")
stage_count = 0
for it in items:
    title = it.find("title").text if it.find("title") is not None else ""
    link = it.find("link").text if it.find("link") is not None else ""
    desc_raw = (it.find("description").text if it.find("description") is not None else "") or ""
    soup = BeautifulSoup(desc_raw, "html.parser")
    desc_text = soup.get_text(" ", strip=True)
    
    # Check if stage / internship
    full_text = (title + " " + desc_text).lower()
    is_stage = any(w in full_text for w in ["stage", "intern", "pfe", "stagiaire", "fin d'études", "6 mois"])
    has_cdi = "cdi" in full_text and not is_stage
    
    status_label = "STAGE" if is_stage else ("CDI" if has_cdi else "OTHER")
    if is_stage:
        stage_count += 1
        print(f"[{status_label}] {title}")
        print(f"   URL: {link}")
        print(f"   Snippet: {desc_text[:140]}...")
        print()

print(f"Total Stages found: {stage_count}")
