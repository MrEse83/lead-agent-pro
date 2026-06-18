"""
industries/salons_uk.py
Industry config: Beauty salons & barbershops — UK market
"""

INDUSTRY_NAME = "salons_uk"
INDUSTRY_LABEL = "Beauty Salons & Barbershops (UK)"

CITIES = [
    "London", "Manchester", "Birmingham", "Leeds", "Glasgow",
    "Edinburgh", "Liverpool", "Bristol", "Sheffield", "Leicester"
]

KEYWORDS = [
    "hair salon",
    "beauty salon",
    "nail salon",
    "barbershop",
    "lash studio",
    "spa and beauty",
    "threading salon",
    "waxing salon",
]

COUNTRY = "UK"

PRODUCT_DESCRIPTION = (
    "An AI WhatsApp assistant that automatically handles appointment booking, "
    "sends reminders to reduce no-shows, and answers common questions — "
    "so you can focus on clients, not your phone."
)

SCORING_CONTEXT = """
High score (70-100): Salon takes bookings by phone/DM only, has a WhatsApp number 
visible on the site or Google listing, no online booking system detected.
These owners spend hours managing bookings manually on their phones.

Medium score (40-69): Uses Booksy or Fresha but no WhatsApp automation or reminders.
Upsell opportunity — the reminder and FAQ layer adds clear value.

Low score (0-39): Already fully automated. Move on.
"""

OUTREACH_ANGLE = (
    "Focus on no-shows and the time lost managing bookings on WhatsApp manually. "
    "Salon owners hate chasing clients for confirmations — lead with that pain."
)

CATEGORY_MAP = {
    "hair salon": "hair",
    "beauty salon": "beauty",
    "nail salon": "nails",
    "barbershop": "barber",
    "lash studio": "lashes",
    "spa and beauty": "spa",
    "threading salon": "threading",
    "waxing salon": "waxing",
}
