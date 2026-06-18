"""
industries/medspas_uk.py
Industry config: Med Spas & Aesthetic Clinics — UK market
"""

INDUSTRY_NAME = "medspas_uk"
INDUSTRY_LABEL = "Med Spas & Aesthetic Clinics (UK)"

CITIES = [
    "London", "Manchester", "Birmingham", "Leeds", "Edinburgh",
    "Glasgow", "Bristol", "Liverpool", "Sheffield", "Nottingham",
    "Brighton", "Leicester", "Cardiff", "Newcastle", "Reading",
]

KEYWORDS = [
    "med spa",
    "medical spa",
    "aesthetic clinic",
    "skin clinic",
    "beauty clinic",
    "laser clinic",
    "botox clinic",
    "dermal filler clinic",
    "anti ageing clinic",
    "cosmetic clinic",
]

COUNTRY = "UK"

PRODUCT_DESCRIPTION = (
    "MedFlow AI builds a custom AI receptionist that lives inside a Med-Spa's "
    "WhatsApp. It handles treatment inquiries, books appointments, sends no-show "
    "reminders, and re-activates lapsed clients — 24/7, without any staff involvement."
)

SCORING_CONTEXT = """
High score (70-100): Med spa or aesthetic clinic with no online booking system,
no WhatsApp automation, no chatbot. Relies on phone calls, emails or manual DMs
to book appointments. These businesses lose bookings every evening and weekend
when staff are unavailable.

Medium score (40-69): Has basic online booking (e.g. Fresha, Booksy) but no
WhatsApp automation or AI assistant. Upsell opportunity — the WhatsApp layer
handles inquiries, consultation pre-screening and reminders that booking widgets can't.

Low score (0-39): Already has a chatbot or advanced automation system. Move on.
"""

OUTREACH_ANGLE = (
    "Focus on the volume of WhatsApp and Instagram DM inquiries aesthetic clinics "
    "receive daily — treatment questions, pricing, availability — all answered manually "
    "by staff. Lead with the time wasted and bookings lost after hours."
)

CATEGORY_MAP = {
    "med spa": "med_spa",
    "medical spa": "med_spa",
    "aesthetic clinic": "aesthetic",
    "skin clinic": "skin",
    "beauty clinic": "beauty",
    "laser clinic": "laser",
    "botox clinic": "botox",
    "dermal filler clinic": "fillers",
    "anti ageing clinic": "anti_ageing",
    "cosmetic clinic": "cosmetic",
}