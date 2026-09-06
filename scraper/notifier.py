"""
Automated Email Notification Engine for New M2 Cyber & Cryptology Internships.
Supports:
- SMTP (Gmail, Outlook, ProtonMail Bridge, Brevo, SendGrid, custom server)
- HTML formatted digest with direct official company buttons
- Algerian student eligibility tags
- Deduplication via data/seen_jobs.json
"""

import json
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict, Any, Tuple

logger = logging.getLogger("scraper.notifier")


def load_seen_job_ids(seen_file_path: str) -> set:
    if os.path.exists(seen_file_path):
        try:
            with open(seen_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data)
        except Exception as e:
            logger.warning(f"Could not read seen jobs file: {e}")
    return set()


def save_seen_job_ids(seen_file_path: str, seen_ids: set):
    os.makedirs(os.path.dirname(seen_file_path), exist_ok=True)
    with open(seen_file_path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(seen_ids)), f, indent=2, ensure_ascii=False)


def build_email_content(new_jobs: List[Dict[str, Any]]) -> Tuple[str, str, str]:
    """Builds both HTML and plain-text versions of the email alert."""
    count = len(new_jobs)
    crypto_count = sum(1 for j in new_jobs if j.get("is_crypto"))
    cyber_count = count - crypto_count

    subject = f"[M2 Cyber & Crypto France] {count} nouvelle(s) offre(s) de stage"

    # Plain text version
    text_lines = [
        f"Stages M2 Cyber & Cryptologie - France",
        f"{count} nouvelle(s) offre(s) ({crypto_count} Crypto, {cyber_count} Cyber).\n",
        "=" * 60,
        ""
    ]

    for job in new_jobs:
        text_lines.append(f"• {job['title']}")
        text_lines.append(f"  Entreprise: {job['company_name']}")
        text_lines.append(f"  Lieu: {job.get('location', 'France')}")
        text_lines.append(f"  Domaine: {job.get('domain', 'Cyber')}")
        text_lines.append(f"  Lien: {job['direct_url']}")
        text_lines.append("-" * 40)

    plain_text = "\n".join(text_lines)

    # HTML version
    job_cards_html = ""
    for job in new_jobs:
        badge_color = "#4f46e5" if job.get("is_crypto") else "#0ea5e9"
        domain_badge = job.get("domain", "Cybersécurité")

        job_cards_html += f"""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background-color: {badge_color}; color: #ffffff; padding: 3px 8px; border-radius: 4px;">
                    {domain_badge}
                </span>
                <span style="font-size: 12px; color: #10b981; font-weight: 600; background: #ecfdf5; padding: 2px 8px; border-radius: 4px;">
                    Stage M2
                </span>
            </div>
            <h3 style="margin: 6px 0; font-size: 16px; color: #0f172a; font-weight: 600;">
                {job['title']}
            </h3>
            <p style="margin: 4px 0 12px 0; color: #64748b; font-size: 13px;">
                <strong>{job['company_name']}</strong> &nbsp;|&nbsp; {job.get('location', 'France')}
            </p>
            <div>
                <a href="{job['direct_url']}" target="_blank" style="display: inline-block; background-color: #0f172a; color: #ffffff; font-weight: 600; font-size: 13px; padding: 8px 16px; border-radius: 6px; text-decoration: none;">
                    Postuler &rarr;
                </a>
            </div>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 24px;">
        <div style="max-width: 640px; margin: 0 auto;">
            <div style="background: #0f172a; color: white; padding: 24px; border-radius: 8px; margin-bottom: 24px;">
                <h1 style="margin: 0 0 8px 0; font-size: 20px; font-weight: 700;">
                    Nouveaux Stages M2
                </h1>
                <p style="margin: 0; font-size: 14px; opacity: 0.9;">
                    <strong>{count}</strong> nouvelle(s) offre(s).
                </p>
            </div>
            
            {job_cards_html}

            <div style="text-align: center; margin-top: 32px; font-size: 12px; color: #94a3b8;">
                <p>France Cyber & Crypto Tracker</p>
            </div>
        </div>
    </body>
    </html>
    """

    return subject, plain_text, html_content


def send_email_notifications(new_jobs: List[Dict[str, Any]], seen_file_path: str = "data/seen_jobs.json") -> bool:
    """
    Sends email alerts for newly detected jobs via SMTP.
    Credentials retrieved from environment variables.
    """
    if not new_jobs:
        logger.info("No new jobs to notify.")
        return True

    host = os.getenv("EMAIL_HOST")
    port = int(os.getenv("EMAIL_PORT", "587"))
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    sender = os.getenv("EMAIL_FROM", user)
    recipient = os.getenv("NOTIFY_EMAIL_TO")

    if not all([host, user, password, recipient]):
        logger.warning(
            "SMTP credentials not fully configured in environment. "
            "Please set EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD, NOTIFY_EMAIL_TO in GitHub Secrets or .env"
        )
        return False

    subject, plain_text, html_content = build_email_content(new_jobs)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        logger.info(f"Connecting to SMTP server {host}:{port}...")
        server = smtplib.SMTP(host, port, timeout=15)
        server.ehlo()
        if port != 465:
            server.starttls()
            server.ehlo()
        server.login(user, password)
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()

        logger.info(f"Notification email sent successfully to {recipient} ({len(new_jobs)} jobs).")

        # Update seen jobs
        seen_ids = load_seen_job_ids(seen_file_path)
        for j in new_jobs:
            seen_ids.add(j["id"])
        save_seen_job_ids(seen_file_path, seen_ids)

        return True

    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        return False


def send_telegram_notification(new_jobs: List[Dict[str, Any]]) -> bool:
    """
    Sends one direct notification per new job via Telegram Bot.
    Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False

    import urllib.request
    import time

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    success_count = 0

    for j in new_jobs:
        text = f"*{j['company_name']}* - {j['title']}\n{j.get('domain', 'Cyber')} • {j.get('location', 'France')}\n{j['direct_url']}"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                success_count += 1
            time.sleep(0.2)
        except Exception as e:
            logger.error(f"Failed to send Telegram notification for {j['id']}: {e}")

    return success_count > 0


def send_discord_notification(new_jobs: List[Dict[str, Any]]) -> bool:
    """
    Sends direct embeds to Discord channel.
    Requires DISCORD_WEBHOOK_URL.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return False

    import urllib.request
    import time

    success_count = 0
    for j in new_jobs:
        embed = {
            "title": f"{j['company_name']} - {j['title']}",
            "url": j["direct_url"],
            "description": f"{j.get('domain', 'Cyber')} • {j.get('location', 'France')}",
            "color": 3447003
        }
        payload = json.dumps({"embeds": [embed]}).encode("utf-8")
        try:
            req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Tracker/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                success_count += 1
            time.sleep(0.2)
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")

    return success_count > 0


def send_ntfy_notification(new_jobs: List[Dict[str, Any]]) -> bool:
    """
    Sends one direct mobile push alert per new job via ntfy.sh.
    Requires NTFY_TOPIC.
    Each notification is directly linked to the job's official URL.
    """
    raw_topic = os.getenv("NTFY_TOPIC", "")
    if not raw_topic:
        print("[ntfy] NTFY_TOPIC environment variable is not set.")
        return False

    topic = raw_topic.replace("https://ntfy.sh/", "").replace("http://ntfy.sh/", "").strip("/").strip()
    if not topic:
        print("[ntfy] Topic is empty after cleanup.")
        return False

    import urllib.request
    import json
    import time

    success_count = 0

    for j in new_jobs:
        payload = {
            "topic": topic,
            "title": f"{j['company_name']} - {j['title']}",
            "message": f"{j.get('domain', 'Cyber')} • {j.get('location', 'France')}",
            "priority": 4,
            "click": j["direct_url"]
        }

        try:
            req = urllib.request.Request(
                "https://ntfy.sh",
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                success_count += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"[ntfy] Failed to send alert for {j['id']}: {e}")
            logger.error(f"Failed to send ntfy alert for {j['id']}: {e}")

    if success_count > 0:
        print(f"[ntfy] {success_count} push notification(s) sent to '{topic}'.")
        return True
    return False


def send_all_notifications(new_jobs: List[Dict[str, Any]], seen_file_path: str = "data/seen_jobs.json") -> bool:
    """
    Dispatches notifications across all configured channels (Telegram, Discord, ntfy, Email)
    and marks new jobs as seen.
    """
    if not new_jobs:
        logger.info("No new jobs to notify.")
        return True

    logger.info(f"Sending alerts for {len(new_jobs)} new job(s)...")

    # Send to active channels
    sent_any = False
    if send_telegram_notification(new_jobs):
        sent_any = True
    if send_discord_notification(new_jobs):
        sent_any = True
    if send_ntfy_notification(new_jobs):
        sent_any = True
    if send_email_notifications(new_jobs, seen_file_path):
        sent_any = True

    # Mark as seen
    if seen_file_path:
        seen_ids = load_seen_job_ids(seen_file_path)
        for j in new_jobs:
            seen_ids.add(j["id"])
        save_seen_job_ids(seen_file_path, seen_ids)

    return sent_any
