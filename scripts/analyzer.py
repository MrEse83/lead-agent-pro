"""
analyzer.py — Step 3
AI website analysis with industry-aware scoring.

Examples:
  python scripts/analyzer.py --industry medspas_us
"""

import os
import sys
import time
import json
import logging
import importlib
import argparse
import requests
from datetime import datetime
from openai import OpenAI
from db import get_connection
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
REQUEST_DELAY = 2


def load_industry(name: str):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "industries"))
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        log.error(f"Industry '{name}' not found.")
        sys.exit(1)


def fetch_homepage_text(url: str) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()
            return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception:
        pass
    return ""


def call_ai(system_prompt: str, user_message: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=300,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                log.warning(f"Rate limit — waiting 30s (attempt {attempt + 1}/{retries})")
                time.sleep(30)
            elif "503" in error_str or "502" in error_str:
                log.warning(f"OpenAI unavailable — waiting 10s (attempt {attempt + 1}/{retries})")
                time.sleep(10)
            else:
                log.warning(f"OpenAI error: {error_str}")
                return ""
    log.error("Max retries reached — skipping lead")
    return ""


def analyze_lead(lead: dict, industry) -> dict:
    page_text = fetch_homepage_text(lead["website"])
    if not page_text:
        return {"score": 0, "summary": "Could not fetch website.", "reason": "Website inaccessible."}

    system_prompt = f"""
You are an expert at analyzing Med-Spa websites to determine how much they would benefit
from an AI WhatsApp receptionist that automates booking, reminders, and client re-activation.

Product being sold: {industry.PRODUCT_DESCRIPTION}

Scoring guide:
{industry.SCORING_CONTEXT}

Respond ONLY with valid JSON, no markdown, no explanation:
{{"score": 85, "summary": "Two sentence summary of the site.", "reason": "One sentence score explanation."}}
"""

    user_message = f"""
Business: {lead['name']}
Category: {lead['category'] or 'unknown'}
City: {lead['city']}
Has chatbot: {lead['has_chatbot']}
Has booking form: {lead['has_booking_form']}
Has WhatsApp: {lead['has_whatsapp']}
Instagram handle: {lead['instagram_handle'] or 'Not found'}
Runs ads: {lead['runs_ads']}

Website text:
{page_text}
"""

    raw = call_ai(system_prompt, user_message)
    if not raw:
        return {"score": 0, "summary": "Analysis failed.", "reason": "No response from AI."}

    try:
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"score": 0, "summary": "Analysis failed.", "reason": "Could not parse AI response."}


def score_to_priority(score: int) -> str:
    if score >= 70: return "hot"
    elif score >= 40: return "warm"
    return "cold"


def score_to_status(score: int) -> str:
    if score >= 70: return "qualified"
    elif score >= 40: return "warm"
    return "low"


def run(industry_name: str):
    industry = load_industry(industry_name)
    log.info(f"Analyzing leads for: {industry.INDUSTRY_LABEL}")
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, website, category, city,
                   has_chatbot, has_booking_form, has_whatsapp,
                   instagram_handle, runs_ads
            FROM leads
            WHERE enrichment_status = 'done'
            AND analysis_status = 'pending'
            AND source LIKE %s
            ORDER BY id
        """, (f"serpapi_{industry.INDUSTRY_NAME}%",))
        leads = cur.fetchall()

    log.info(f"Found {len(leads)} leads to analyze")

    for i, lead in enumerate(leads, 1):
        log.info(f"[{i}/{len(leads)}] {lead['name']}")
        result = analyze_lead(lead, industry)
        score = result.get("score", 0)

        if i % 100 == 0:
            try: conn.close()
            except Exception: pass
            conn = get_connection()
            log.info("DB connection refreshed")

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE leads SET
                        ai_summary=%s, automation_score=%s, score_reason=%s,
                        analysis_status='done', analyzed_at=%s,
                        lead_status=%s, priority=%s
                    WHERE id=%s
                """, (
                    result.get("summary"), score, result.get("reason"),
                    datetime.now(), score_to_status(score),
                    score_to_priority(score), lead["id"],
                ))
            conn.commit()
        except Exception as e:
            log.warning(f"DB write failed, reconnecting: {e}")
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE leads SET
                        ai_summary=%s, automation_score=%s, score_reason=%s,
                        analysis_status='done', analyzed_at=%s,
                        lead_status=%s, priority=%s
                    WHERE id=%s
                """, (
                    result.get("summary"), score, result.get("reason"),
                    datetime.now(), score_to_status(score),
                    score_to_priority(score), lead["id"],
                ))
            conn.commit()

        log.info(f"  Score: {score} — {result.get('reason', '')[:70]}")
        time.sleep(REQUEST_DELAY)

    conn.close()
    log.info("Analysis complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--industry", default="medspas_us")
    args = parser.parse_args()
    run(args.industry)