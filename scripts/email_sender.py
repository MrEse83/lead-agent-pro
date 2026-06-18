"""
email_sender.py
Sends cold outreach emails via Gmail SMTP.
"""

import os
import smtplib
import logging
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
from db import get_connection

# Fix: load .env from project root regardless of where this file is called from
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

log = logging.getLogger(__name__)

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME", "Your Name")
DAILY_CAP = 30


def get_smtp_connection():
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        raise ValueError("GMAIL_ADDRESS or GMAIL_APP_PASSWORD missing from .env")
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    return server


def build_email(to_address: str, to_name: str, body: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Quick question about {to_name}"
    msg["From"] = f"{SENDER_NAME} <{GMAIL_ADDRESS}>"
    msg["To"] = to_address
    msg.attach(MIMEText(body, "plain"))
    return msg


def send_one(server, lead: dict) -> bool:
    if not lead.get("email"):
        log.warning(f"  No email for {lead['name']} — skipping")
        return False
    if not lead.get("outreach_email"):
        log.warning(f"  No outreach message for {lead['name']} — skipping")
        return False
    try:
        msg = build_email(
            to_address=lead["email"],
            to_name=lead["name"],
            body=lead["outreach_email"],
        )
        server.sendmail(GMAIL_ADDRESS, lead["email"], msg.as_string())
        log.info(f"  Sent to {lead['name']} <{lead['email']}>")
        return True
    except Exception as e:
        log.error(f"  Failed to send to {lead['name']}: {e}")
        return False


def mark_contacted(conn, lead_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE leads SET
                lead_status = 'contacted',
                contacted_at = %s,
                contact_channel = 'email'
            WHERE id = %s
        """, (datetime.now(), lead_id))
    conn.commit()


def run_batch(limit: int = DAILY_CAP):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, email, outreach_email
            FROM leads
            WHERE lead_status IN ('qualified', 'warm')
            AND email IS NOT NULL
            AND outreach_email IS NOT NULL
            AND contacted_at IS NULL
            ORDER BY automation_score DESC
            LIMIT %s
        """, (limit,))
        leads = cur.fetchall()

    if not leads:
        log.info("No leads ready to contact.")
        conn.close()
        return

    log.info(f"Sending to {len(leads)} leads (cap: {limit}/day)")

    try:
        server = get_smtp_connection()
        sent = 0
        for i, lead in enumerate(leads, 1):
            log.info(f"[{i}/{len(leads)}] {lead['name']}")
            success = send_one(server, lead)
            if success:
                mark_contacted(conn, lead["id"])
                sent += 1
                time.sleep(45)
        server.quit()
        log.info(f"Batch complete. Sent: {sent}/{len(leads)}")
    except Exception as e:
        log.error(f"SMTP connection failed: {e}")

    conn.close()


def send_single(lead_id: int, custom_message: str = None):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, email, outreach_email
            FROM leads WHERE id = %s
        """, (lead_id,))
        lead = cur.fetchone()

    if not lead:
        log.error(f"Lead {lead_id} not found")
        conn.close()
        return False

    if custom_message and custom_message.strip():
        lead = dict(lead)
        lead["outreach_email"] = custom_message.strip()

    try:
        server = get_smtp_connection()
        success = send_one(server, lead)
        server.quit()
        if success:
            mark_contacted(conn, lead_id)
        conn.close()
        return success
    except Exception as e:
        log.error(f"SMTP error: {e}")
        conn.close()
        return False


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=DAILY_CAP)
    parser.add_argument("--lead-id", type=int, default=None)
    args = parser.parse_args()
    if args.lead_id:
        send_single(args.lead_id)
    else:
        run_batch(limit=args.limit)