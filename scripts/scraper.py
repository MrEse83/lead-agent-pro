"""
scraper.py — Step 1
Searches Google Maps for businesses using SerpAPI.
Industry is set by passing --industry flag.

Examples:
  python scripts/scraper.py --industry clinics_uk
  python scripts/scraper.py --industry salons_uk
  python scripts/scraper.py --industry restaurants_uk
"""

import os
import sys
import time
import logging
import importlib
import argparse
from serpapi import GoogleSearch
from dotenv import load_dotenv
from db import get_connection

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

RESULTS_PER_QUERY = 20


def load_industry(name: str):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "industries"))
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        log.error(f"Industry config '{name}' not found in /industries/")
        log.error("Available: clinics_uk, salons_uk, restaurants_uk")
        sys.exit(1)


def search_businesses(keyword: str, city: str, country: str, api_key: str) -> list:
    params = {
        "engine": "google_maps",
        "q": f"{keyword} in {city} {country}",
        "type": "search",
        "api_key": api_key,
        "num": RESULTS_PER_QUERY,
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("local_results", [])
    except Exception as e:
        log.error(f"SerpAPI error for '{keyword} in {city}': {e}")
        return []


def save_lead(conn, lead: dict, city: str, keyword: str, industry):
    category = industry.CATEGORY_MAP.get(keyword, "other")
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clinic_leads (
                name, address, phone, website, google_maps_url,
                category, city, country, source, rating
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            lead.get("title"),
            lead.get("address"),
            lead.get("phone"),
            lead.get("website"),
            lead.get("place_id_search") or lead.get("link") or lead.get("place_id"),
            category,
            city,
            industry.COUNTRY,
            f"serpapi_{industry.INDUSTRY_NAME}",
            float(lead.get("rating")) if lead.get("rating") else None,
        ))
    conn.commit()


def run(industry_name: str):
    industry = load_industry(industry_name)
    log.info(f"Starting scraper for: {industry.INDUSTRY_LABEL}")

    conn = get_connection()
    api_key = os.getenv("SERPAPI_KEY")
    total = 0

    for city in industry.CITIES:
        for keyword in industry.KEYWORDS:
            log.info(f"  Searching: '{keyword}' in {city}")
            results = search_businesses(keyword, city, industry.COUNTRY, api_key)
            for result in results:
                if not result.get("website"):
                    continue
                save_lead(conn, result, city, keyword, industry)
                total += 1
            log.info(f"    -> {len(results)} results found")
            time.sleep(1.5)

    conn.close()
    log.info(f"Done. Industry: {industry.INDUSTRY_LABEL} | Saved: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--industry", default="clinics_uk")
    args = parser.parse_args()
    run(args.industry)
