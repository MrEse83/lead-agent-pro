"""
industries/medspas_us.py

Med-Spas and Aesthetic Clinics — United States
Run: python scripts/scraper.py --industry medspas_us
"""

INDUSTRY_NAME = "medspas_us"
INDUSTRY_LABEL = "Med-Spas & Aesthetic Clinics (USA)"

CITIES = [
    # Tier 1 — Florida
    "Miami FL", "Tampa FL", "Orlando FL", "Fort Lauderdale FL", "Jacksonville FL",
    # Tier 1 — Texas
    "Houston TX", "Dallas TX", "Austin TX", "San Antonio TX",
    # Tier 1 — California
    "Los Angeles CA", "San Diego CA", "Orange County CA",
    # Tier 2
    "New York NY", "Atlanta GA", "Phoenix AZ", "Las Vegas NV", "Charlotte NC",
]

KEYWORDS = [
    "med spa",
    "medical spa",
    "aesthetic clinic",
    "botox clinic",
    "laser skin clinic",
    "medspa",
    "cosmetic clinic",
    "skin rejuvenation clinic",
]

COUNTRY = "United States"

# medspas_us.py — update PRODUCT_DESCRIPTION
PRODUCT_DESCRIPTION = (
    "MedFlow AI builds a custom AI receptionist that handles appointment booking, "
    "no-show prevention, and client re-activation automatically via SMS — "
    "the channel US clients already use daily. No app downloads, no friction, "
    "just instant replies that turn inquiries into confirmed bookings 24/7."
)

SCORING_CONTEXT = """
You are scoring Med-Spa and aesthetic clinic leads for an AI receptionist product
that automates WhatsApp booking, no-show reminders, and client re-activation.

High score (70-100): 
- Owner-operated Med-Spa with 4.0+ Google rating and 50+ reviews
- Active on Instagram (posts regularly, runs ads)
- No visible online booking system or using a basic contact form
- Multiple treatment categories (botox, laser, body contouring etc.)
- Located in a high-income urban area (Miami, LA, Houston, Dallas etc.)
- WhatsApp number visible on website — already using it informally

Medium score (40-69):
- Established clinic with 20-50 reviews and 3.5+ rating
- Has basic booking but it's clunky (Calendly link, email to book)
- Some Instagram presence but not running ads
- Single treatment focus (e.g. laser only)
- Suburban location with moderate client volume

Low score (0-39):
- Franchise or chain location — too many decision makers
- Already using a sophisticated booking platform (Boulevard, Vagaro, Mindbody)
  with no clear automation gap
- Less than 20 reviews — too small, low budget
- No website or social presence — not investing in growth
- Hospital-affiliated or medically institutional — not a fit
"""

OUTREACH_ANGLE = (
    "Med-Spa owners are losing 15-20% of their monthly revenue to no-shows and "
    "cold leads that go unanswered because their front desk is overwhelmed. "
    "Every missed Instagram DM is a potential $500 treatment walking out the door. "
    "Focus the cold email on this specific dollar cost — not on technology. "
    "The hook is recovered revenue, not automation. Keep it under 120 words, "
    "sound like a human, and end with a single low-friction CTA: "
    "a 15-minute call to show them exactly how many bookings they are losing."
)

CATEGORY_MAP = {
    "med spa": "medspa",
    "medical spa": "medspa",
    "aesthetic clinic": "aesthetic",
    "botox clinic": "botox",
    "laser skin clinic": "laser",
    "medspa": "medspa",
    "cosmetic clinic": "aesthetic",
    "skin rejuvenation clinic": "laser",
}