"""
industries/medspas_ng.py
Industry config: Med Spas & Aesthetic Clinics — Nigeria market
"""

INDUSTRY_NAME = "medspas_ng"
INDUSTRY_LABEL = "Med Spas & Aesthetic Clinics (Nigeria)"

CITIES = [
    "Lagos", "Abuja", "Port Harcourt", "Benin City",
]

KEYWORDS = [
    "med spa",
    "aesthetic clinic",
    "skin clinic",
    "beauty clinic",
    "laser clinic",
    "botox clinic",
    "glow clinic",
    "skincare clinic",
    "slimming clinic",
    "facial clinic",
    "body contouring",
    "hair removal clinic",
]

COUNTRY = "Nigeria"

PRODUCT_DESCRIPTION = (
    "MedFlow AI builds a custom AI receptionist that lives inside a clinic's "
    "WhatsApp. It handles treatment enquiries, books appointments, sends reminders, "
    "and re-activates lapsed clients — 24/7, without any staff involvement. "
    "No more losing bookings at night or on weekends."
)

SCORING_CONTEXT = """
High score (70-100): Aesthetic or skincare clinic that takes bookings manually
via WhatsApp DMs, phone calls, or Instagram DMs. No automation, no booking system.
Staff spend hours every day answering the same questions about treatments and prices.
These businesses lose bookings every night when no one is available to respond.

Medium score (40-69): Has a basic booking system or uses Fresha/similar but still
handles most enquiries manually on WhatsApp. Upsell opportunity — the AI layer
handles enquiries, pricing questions, and reminders that booking tools can't.

Low score (0-39): Already has automation or a chatbot in place. Move on.
"""

OUTREACH_ANGLE = (
    "Focus on the volume of WhatsApp and Instagram DM enquiries Nigerian aesthetic "
    "clinics receive daily — treatment questions, pricing, availability — all answered "
    "manually by staff or owners. Lead with the bookings lost at night and on weekends "
    "when no one is online to respond. Nigerian clinic owners understand this pain instantly."
)

CATEGORY_MAP = {
    "med spa": "med_spa",
    "aesthetic clinic": "aesthetic",
    "skin clinic": "skin",
    "beauty clinic": "beauty",
    "laser clinic": "laser",
    "botox clinic": "botox",
    "glow clinic": "glow",
    "skincare clinic": "skincare",
    "slimming clinic": "slimming",
    "facial clinic": "facial",
    "body contouring": "body",
    "hair removal clinic": "hair_removal",
}