"""
industries/clinics_uk.py
Industry config: Medical & dental clinics — UK market
"""

INDUSTRY_NAME = "clinics_uk"
INDUSTRY_LABEL = "Medical & Dental Clinics (UK)"

CITIES = [
    "London", "Manchester", "Birmingham", "Leeds", "Glasgow",
    "Edinburgh", "Liverpool", "Bristol", "Sheffield", "Cardiff"
]

KEYWORDS = [
    "dental clinic",
    "private clinic",
    "eye clinic",
    "medical centre",
    "physiotherapy clinic",
    "ENT clinic",
    "GP surgery private",
    "cosmetic clinic",
]

COUNTRY = "UK"

# What you're selling to this industry
PRODUCT_DESCRIPTION = (
    "An AI WhatsApp assistant that automatically handles appointment booking, "
    "patient reminders, and FAQ responses for clinics — 24/7, no receptionist needed."
)

# What signals make a good lead in this industry
SCORING_CONTEXT = """
High score (70-100): Clinic uses manual booking (phone/form only), has a WhatsApp number 
but no automation, no chatbot on the website. These clinics waste hours on appointment calls.

Medium score (40-69): Has Calendly or basic online booking but no WhatsApp automation.
Still worth contacting — there is an upsell opportunity.

Low score (0-39): Already has a chatbot or advanced booking system. Move on.
"""

# Email tone/angle for outreach
OUTREACH_ANGLE = (
    "Focus on how much time receptionists waste answering appointment calls "
    "and how the clinic loses bookings outside working hours."
)

# Category label saved to DB
CATEGORY_MAP = {
    "dental clinic": "dental",
    "private clinic": "private",
    "eye clinic": "eye",
    "medical centre": "general",
    "physiotherapy clinic": "physiotherapy",
    "ENT clinic": "ent",
    "GP surgery private": "gp",
    "cosmetic clinic": "cosmetic",
}
