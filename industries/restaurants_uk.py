"""
industries/restaurants_uk.py
Industry config: Restaurants & dining — UK market
"""

INDUSTRY_NAME = "restaurants_uk"
INDUSTRY_LABEL = "Restaurants & Dining (UK)"

CITIES = [
    "London", "Manchester", "Birmingham", "Leeds", "Glasgow",
    "Edinburgh", "Liverpool", "Bristol", "Sheffield", "Nottingham"
]

KEYWORDS = [
    "fine dining restaurant",
    "private dining",
    "Indian restaurant",
    "Italian restaurant",
    "Nigerian restaurant",
    "African restaurant",
    "sushi restaurant",
    "steakhouse",
]

COUNTRY = "UK"

PRODUCT_DESCRIPTION = (
    "An AI WhatsApp assistant that handles table reservations, answers menu questions, "
    "sends booking confirmations, and captures customer details automatically — "
    "without staff lifting a finger."
)

SCORING_CONTEXT = """
High score (70-100): Restaurant takes reservations by phone only or has a simple 
contact form. Has WhatsApp listed but no automation. 
These restaurants miss bookings every night when they're busy or closed.

Medium score (40-69): Uses OpenTable or Resy but no WhatsApp channel for reservations.
The WhatsApp layer adds a personal touch many diners prefer.

Low score (0-39): Fully automated reservation system already in place. Skip.
"""

OUTREACH_ANGLE = (
    "Focus on missed reservations when the restaurant is busy or closed, "
    "and the personal touch of WhatsApp vs a generic booking widget. "
    "Restaurateurs are proud of their hospitality — position this as enhancing it."
)

CATEGORY_MAP = {
    "fine dining restaurant": "fine dining",
    "private dining": "private dining",
    "Indian restaurant": "indian",
    "Italian restaurant": "italian",
    "Nigerian restaurant": "nigerian",
    "African restaurant": "african",
    "sushi restaurant": "sushi",
    "steakhouse": "steakhouse",
}
