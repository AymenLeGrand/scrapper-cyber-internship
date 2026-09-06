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

    subject = f"🎯 [M2 Cyber & Crypto France] {count} nouvelle(s) offre(s) de stage détectée(s)"

    # Plain text version
    text_lines = [
        f"Alerte Stages M2 Cybersécurité & Cryptologie en France",
        f"{count} nouvelle(s) offre(s) vérifiée(s) aujourd'hui ({crypto_count} Crypto, {cyber_count} Cyber).\n",
        "=" * 60,
        ""
    ]

    for job in new_jobs:
        text_lines.append(f"• {job['title']}")
        text_lines.append(f"  Entreprise: {job['company_name']}")
        text_lines.append(f"  Lieu: {job.get('location', 'France')}")
        text_lines.append(f"  Domaine: {job.get('domain', 'Cyber')}")
        text_lines.append(f"  Lien officiel: {job['direct_url']}")
        text_lines.append("-" * 40)

    plain_text = "\n".join(text_lines)

    # HTML version
    job_cards_html = ""
    for job in new_jobs:
        badge_color = "#4f46e5" if job.get("is_crypto") else "#0ea5e9"
        domain_badge = job.get("domain", "Cybersécurité")

        job_cards_html += f"""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; background-color: {badge_color}; color: #ffffff; padding: 3px 8px; border-radius: 4px;">
                    {domain_badge}
                </span>
                <span style="font-size: 12px; color: #10b981; font-weight: 600; background: #ecfdf5; padding: 2px 8px; border-radius: 4px;">
                    Stage M2 (6 mois)
                </span>
            </div>
            <h3 style="margin: 6px 0; font-size: 16px; color: #0f172a; font-weight: 600;">
                {job['title']}
            </h3>
            <p style="margin: 4px 0 12px 0; color: #64748b; font-size: 13px;">
                🏢 <strong>{job['company_name']}</strong> &nbsp;|&nbsp; 📍 {job.get('location', 'France')}
            </p>
            <div>
                <a href="{job['direct_url']}" target="_blank" style="display: inline-block; background-color: #0f172a; color: #ffffff; font-weight: 600; font-size: 13px; padding: 8px 16px; border-radius: 6px; text-decoration: none;">
                    Postuler sur le site officiel &rarr;
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
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; padding: 24px; border-radius: 10px; margin-bottom: 24px;">
                <h1 style="margin: 0 0 8px 0; font-size: 20px; font-weight: 700;">
                    🛡️ Nouveaux Stages M2 Détectés
                </h1>
                <p style="margin: 0; font-size: 14px; opacity: 0.9;">
                    <strong>{count}</strong> nouvelle(s) offre(s) vérifiée(s) en direct sur les sites des entreprises.
                </p>
            </div>
            
            {job_cards_html}

            <div style="text-align: center; margin-top: 32px; font-size: 12px; color: #94a3b8;">
                <p>Projet open source France Cyber & Crypto Tracker • Liens 100% officiels certifiés sans agrégateurs</p>
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
    Sends instant mobile push notifications to your phone via Telegram Bot.
    Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False

    import urllib.request
    import urllib.parse

    count = len(new_jobs)
    lines = [
        f"🎯 *[M2 Cyber & Crypto France]*",
        f"*{count} nouvelle(s) offre(s) de stage détectée(s) !*",
        ""
    ]

    for j in new_jobs:
        icon = "🔐" if j.get("is_crypto") else "🛡️"
        lines.append(f"{icon} *{j['title']}*")
        lines.append(f"🏢 *{j['company_name']}* | 📍 {j.get('location', 'France')}")
        lines.append(f"👉 [Postuler en direct sur le site officiel]({j['direct_url']})")
        lines.append("")

    text = "\n".join(lines)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            logger.info(f"Telegram notification sent successfully to chat {chat_id}.")
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        return False


def send_discord_notification(new_jobs: List[Dict[str, Any]]) -> bool:
    """
    Sends rich embeds to a Discord channel (which pushes to your phone Discord app).
    Requires DISCORD_WEBHOOK_URL.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return False

    import urllib.request

    count = len(new_jobs)
    embeds = []
    for j in new_jobs[:10]: # Discord limits to 10 embeds per message
        color = 5174501 if j.get("is_crypto") else 960997 # Hex indigo or cyan
        embeds.append({
            "title": j["title"],
            "url": j["direct_url"],
            "description": f"🏢 **{j['company_name']}** • 📍 {j.get('location', 'France')}\n{j.get('description', '')[:140]}...",
            "color": color,
            "footer": {"text": "Stage Bac+5 / M2 (6 mois) • Lien 100% officiel"}
        })

    payload = json.dumps({
        "content": f"🎯 **[M2 Cyber & Crypto France]** {count} nouvelle(s) offre(s) de stage détectée(s) !",
        "embeds": embeds
    }).encode("utf-8")

    try:
        req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "CyberInternshipTracker/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            logger.info("Discord notification sent successfully.")
            return True
    except Exception as e:
        logger.error(f"Failed to send Discord notification: {e}")
        return False


def send_ntfy_notification(new_jobs: List[Dict[str, Any]]) -> bool:
    """
    Sends mobile push alerts via ntfy.sh (free open-source app, zero account needed).
    Requires NTFY_TOPIC (e.g. 'stages-cyber-tonprenom').
    """
    topic = os.getenv("NTFY_TOPIC")
    if not topic:
        return False

    import urllib.request

    count = len(new_jobs)
    body = "\n".join([f"• {j['title']} ({j['company_name']})" for j in new_jobs[:5]])
    url = f"https://ntfy.sh/{topic}"

    try:
        req = urllib.request.Request(
            url,
            data=body.encode("utf-8"),
            headers={
                "Title": f"🎯 {count} nouveau(x) stage(s) Cyber M2 !",
                "Priority": "high",
                "Tags": "shield,lock"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            logger.info(f"ntfy.sh alert sent to topic {topic}.")
            return True
    except Exception as e:
        logger.error(f"Failed to send ntfy alert: {e}")
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
    seen_ids = load_seen_job_ids(seen_file_path)
    for j in new_jobs:
        seen_ids.add(j["id"])
    save_seen_job_ids(seen_file_path, seen_ids)

    return sent_any

