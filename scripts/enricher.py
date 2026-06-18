"""
enricher.py — Step 2
Visits each lead website and extracts:
- Email addresses
- WhatsApp numbers
- Instagram handle
- Whether they have a booking form
- Whether they have a chatbot widget

Run: python scripts/enricher.py --industry medspas_us
"""

import re
import time
import logging
import argparse
import importlib
import sys
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from db import get_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}
TIMEOUT = 10

CONTACT_PATHS = ["", "/contact", "/contact-us", "/about", "/about-us", "/team"]

CHATBOT_SIGNATURES = [
    "intercom.io", "tidio.com", "crisp.chat", "tawk.to",
    "livechat.com", "drift.com", "zendesk.com", "freshchat.com",
    "hubspot.com/conversations", "chaport.com",
]

# Updated with US Med-Spa specific booking platforms
BOOKING_SIGNATURES = [
    # US Med-Spa platforms
    "vagaro.com", "boulevard.io", "mindbodyonline.com", "glossgenius.com",
    "squareup.com/appointments", "acuityscheduling.com", "jane.app",
    "patientpop.com", "zenoti.com", "booker.com",
    # Generic
    "calendly.com", "fresha.com", "practicebetter.io",
]


def load_industry(name: str):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "industries"))
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        log.error(f"Industry config '{name}' not found.")
        sys.exit(1)


def fetch_page(url: str) -> BeautifulSoup | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, "html.parser")
    except Exception:
        pass
    return None


def extract_emails(soup: BeautifulSoup) -> str | None:
    blocked = ["example.", "noreply", "no-reply", "support@wordpress", "wixpress"]

    # Priority 1: mailto: links (most reliable — no concatenation risk)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("mailto:"):
            email = href.replace("mailto:", "").split("?")[0].strip().lower()
            if "@" in email and "." in email and not any(b in email for b in blocked):
                return email

    # Priority 2: scan text nodes individually (never join them)
    email_pattern = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
    for element in soup.find_all(string=True):
        text = element.strip()
        if not text:
            continue
        matches = email_pattern.findall(text)
        for email in matches:
            email = email.lower()
            if not any(b in email for b in blocked):
                return email

    return None


def extract_whatsapp(soup: BeautifulSoup, page_text: str) -> str | None:
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "wa.me" in href or "api.whatsapp.com" in href:
            number = re.search(r"[\d]{7,15}", href)
            if number:
                return "+" + number.group()
    matches = re.findall(r"(?:WhatsApp|whatsapp|WA)[^\d]{0,10}(\+?[\d\s\-]{10,15})", page_text)
    if matches:
        return matches[0].strip()
    return None


def extract_instagram(soup: BeautifulSoup) -> str | None:
    """Extract Instagram handle from any instagram.com link on the page."""
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "instagram.com/" in href:
            # Extract handle from URL
            match = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", href)
            if match:
                handle = match.group(1)
                # Skip generic Instagram pages
                if handle.lower() not in ["p", "explore", "accounts", "reel", "stories"]:
                    return f"@{handle}"
    return None


def detect_chatbot(html: str) -> bool:
    return any(sig in html.lower() for sig in CHATBOT_SIGNATURES)


def detect_booking_form(html: str) -> bool:
    return any(sig in html.lower() for sig in BOOKING_SIGNATURES)


def detect_contact_form(soup: BeautifulSoup) -> bool:
    forms = soup.find_all("form")
    for form in forms:
        inputs = form.find_all("input")
        if len(inputs) >= 2:
            return True
    return False


def enrich_lead(conn, lead: dict):
    base_url = lead["website"].rstrip("/")
    lead_id = lead["id"]

    email = None
    whatsapp = None
    instagram = None
    has_chatbot = False
    has_booking = False
    has_contact_form = False
    error = None

    try:
        for path in CONTACT_PATHS:
            url = base_url + path
            soup = fetch_page(url)
            if not soup:
                continue

            html = str(soup)
            page_text = soup.get_text()

            if not email:
                email = extract_emails(soup)
            if not whatsapp:
                whatsapp = extract_whatsapp(soup, page_text)
            if not instagram:
                instagram = extract_instagram(soup)
            if not has_chatbot:
                has_chatbot = detect_chatbot(html)
            if not has_booking:
                has_booking = detect_booking_form(html)
            if not has_contact_form:
                has_contact_form = detect_contact_form(soup)

            time.sleep(0.5)

        status = "done"

    except Exception as e:
        error = str(e)
        status = "failed"
        log.warning(f"  Failed to enrich {base_url}: {error}")

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE leads SET
                email = %s,
                whatsapp_number = %s,
                has_whatsapp = %s,
                has_chatbot = %s,
                has_booking_form = %s,
                has_contact_form = %s,
                instagram_handle = %s,
                enrichment_status = %s,
                enrichment_error = %s,
                enriched_at = %s
            WHERE id = %s
        """, (
            email,
            whatsapp,
            bool(whatsapp),
            has_chatbot,
            has_booking,
            has_contact_form,
            instagram,
            status,
            error,
            datetime.now(),
            lead_id,
        ))
    conn.commit()

    log.info(
        f"  [{lead_id}] {lead['name'][:40]} | "
        f"email={'Y' if email else 'N'} "
        f"wa={'Y' if whatsapp else 'N'} "
        f"ig={'Y' if instagram else 'N'} "
        f"chatbot={'Y' if has_chatbot else 'N'} "
        f"booking={'Y' if has_booking else 'N'}"
    )


def run(industry_name: str):
    log.info("Starting enrichment...")
    load_industry(industry_name)  # validates industry exists
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, website FROM leads
            WHERE website IS NOT NULL
            AND enrichment_status = 'pending'
            AND source LIKE %s
            ORDER BY id
        """, (f"serpapi_{industry_name}%",))
        leads = cur.fetchall()

    log.info(f"Found {len(leads)} leads to enrich")

    for i, lead in enumerate(leads, 1):
        log.info(f"[{i}/{len(leads)}] Enriching: {lead['name']}")
        enrich_lead(conn, lead)
        time.sleep(1)

    conn.close()
    log.info("Enrichment complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--industry", default="medspas_us")
    args = parser.parse_args()
    run(args.industry)