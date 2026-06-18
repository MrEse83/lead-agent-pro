"""
outreach.py — Step 4
Generates personalized outreach messages, industry-aware.

Examples:
  python scripts/outreach.py --industry medspas_us
"""

import os
import sys
import time
import logging
import importlib
import argparse
from datetime import datetime
from openai import OpenAI
from db import get_connection
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read sender name from .env — no hardcoding
SENDER_NAME = os.getenv("SENDER_NAME", "Your Name")


def load_industry(name: str):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "industries"))
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        log.error(f"Industry '{name}' not found.")
        sys.exit(1)


def generate_email(lead: dict, industry) -> str:
    system = f"""
You are a cold email copywriter. Write short, personalized cold emails for AI automation products.
Product: {industry.PRODUCT_DESCRIPTION}
Outreach angle: {industry.OUTREACH_ANGLE}

Rules: Max 120 words. No buzzwords. Sound human. One CTA (15-min call or demo).
Sign off as: {SENDER_NAME}, MedFlow AI
"""
    prompt = f"""
Business: {lead['name']} ({lead['category']}, {lead['city']})
Instagram: {lead['instagram_handle'] or 'Not found'}
AI found: {lead['ai_summary']}
Score reason: {lead['score_reason']}

Write the cold email.
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            max_tokens=300, temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        log.warning(f"Email generation failed: {e}")
        return ""


def generate_whatsapp(lead: dict, industry) -> str:
    system = f"""
Write a WhatsApp cold outreach message. Under 60 words. Friendly, not pushy.
Product: {industry.PRODUCT_DESCRIPTION}
Angle: {industry.OUTREACH_ANGLE}
End with a simple yes/no question. Sign off as: {SENDER_NAME}, MedFlow AI
"""
    prompt = f"Business: {lead['name']} ({lead['city']})\nFound: {lead['ai_summary']}\nWrite the message."
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            max_tokens=150, temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        log.warning(f"WhatsApp generation failed: {e}")
        return ""


def run(industry_name: str):
    industry = load_industry(industry_name)
    log.info(f"Generating outreach for: {industry.INDUSTRY_LABEL}")
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, category, city, ai_summary, score_reason,
                   has_whatsapp, has_chatbot, automation_score, instagram_handle
            FROM leads
            WHERE lead_status IN ('qualified', 'warm')
            AND outreach_email IS NULL
            AND source LIKE %s
            ORDER BY automation_score DESC
        """, (f"serpapi_{industry.INDUSTRY_NAME}%",))
        leads = cur.fetchall()

    log.info(f"Generating for {len(leads)} leads")

    for i, lead in enumerate(leads, 1):
        log.info(f"[{i}/{len(leads)}] {lead['name']}")
        email_msg = generate_email(lead, industry)
        wa_msg = generate_whatsapp(lead, industry)

        with conn.cursor() as cur:
            cur.execute("""
                UPDATE leads SET
                    outreach_email=%s, outreach_whatsapp=%s, outreach_generated_at=%s
                WHERE id=%s
            """, (email_msg, wa_msg, datetime.now(), lead["id"]))
        conn.commit()
        time.sleep(1.5)

    conn.close()
    log.info("Outreach generation complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--industry", default="medspas_us")
    args = parser.parse_args()
    run(args.industry)